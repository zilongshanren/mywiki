---
tags: [渲染, unity, shader, mask, 后处理, sdf]
date: 2026-04-14
sources: 2
---

# 自定义 Mask Shader（圆盘 / 圆环）

[[image-effect-mask-blend|外部贴图遮罩]] 的两个硬伤——**纵横比绑死**和**参数不能动态调**——的解法是：把遮罩**搬到 fragment shader 内部用闭式表达式实时算**。[[harry-alisavakis|Harry Alisavakis]] 在 *My take on shaders* 第四、五篇里给出最朴素的两个版本：圆盘 mask 和圆环 mask。它们只多了几行 `length` 加 `saturate` 加 `pow` 的操作，却换来「圆心、半径、硬度、宽度都能从 C# 实时驱动」的灵活度，是后续 [[shockwave-effect|冲击波]]、屏幕受击反馈、注意力引导这类动效的基础积木。

## 圆盘 mask：`length`、`saturate`、`pow` 三件套

第一篇的核心仅有 5 行：

```hlsl
float dist        = length(float2(i.uv.x - _CenterX, i.uv.y - _CenterY) * float2(_SizeX, _SizeY));
float circle      = saturate(dist / _Radius);
float circleAlpha = pow(circle, pow(_Hardness, 2));
float a           = (_Invert > 0) ? circleAlpha * _Invert : (1 - circleAlpha) * (-_Invert);
```

逐行拆开就是一个 [[sdf-2d-primitives|2D SDF]] 圆盘的最小实现：

1. **`length(uv - center)`** 给出当前像素到圆心的欧氏距离——正是圆的隐函数。乘上 `(_SizeX, _SizeY)` 是手工做**纵横比校正**：因为屏幕 UV 在 [0,1] 上但屏幕物理纵横比不是 1:1，单靠 `length` 算出来的「圆」会被拉成椭圆，所以让美术给个 `(1.6, 0.9)` 之类的比例把它扳回正圆。
2. **`saturate(dist / _Radius)`**——把距离归一化到 `[0, 1]`，圆心是 0、半径处是 1、外侧 clamp 为 1。这一步直接把「距离场」变成了**带柔边的灰度遮罩**：圆心黑、边缘白、外面全白。如果只想要硬边圆可以写成三元运算 `dist < _Radius ? 0 : 1`，但 `saturate` 版能保留过渡。
3. **`pow(circle, pow(_Hardness, 2))`**——`_Hardness` 越大、`circle` 被压得越小，柔边越窄、最终趋近一个硬圆。Alisavakis 把 `_Hardness` 自身平方一次，是为了把美术调节范围从「需要写 180」压回「写 13 就够了」的工程小 trick；同时也允许 `_Hardness` 为负走相反方向。
4. **`_Invert`**——一个范围 `[-1, 1]` 的统一旋钮，正值得到「圆内黑、圆外白」的常规遮罩，负值翻转为「圆外黑、圆内白」，绝对值控制强度。

最终 `a` 就是这个像素在「特效」与「原图」之间的 lerp 权重，丢回 [[image-effect-mask-blend|遮罩混合公式]] 即可。

## 圆环 mask：把「距离 < 半径」改成「距离接近半径」

第二篇要做的是**环形**遮罩——这才是冲击波要用到的形状。改动只在三行：

```hlsl
float rd          = _Thickness / 2;
float rc          = _Radius - rd;
float circle      = saturate(abs(dist - rc) / _Thickness);
```

关键理解：**`_Radius` 不是圆环的外半径，而是圆环中心带（最暗那一圈）所在的半径**。`rd` 是「半厚」，`rc` 是「内沿到圆心的距离」。判定一个像素是否落在环内，等价于「`dist` 距离 `rc` 不超过 `_Thickness`」——用 `abs(dist - rc)` 把内外两侧合并成一个「距中心带的偏离量」，再 `saturate(... / _Thickness)` 归一化为柔边。

可以理解成：圆盘 mask 是「距离场比 `_Radius` 小」的指示函数，圆环 mask 是「距离场到 `_Radius` 的偏离比 `_Thickness` 小」的指示函数——后者就是**带宽度的等距集**，本质是同一族 SDF 表达式的两种取阈值方式。

## 为什么是「shader 化遮罩」的范式样本

Alisavakis 这两支 shader 几乎不依赖任何高级技巧（没有三角函数、没有解析圆方程、没有分支求交），只靠 `length` + `saturate` + `pow` + 一次符号判定，却用最少的代价把「[[image-effect-mask-blend|静态贴图遮罩]] → in-shader 程序化遮罩」这一步走通：

- **参数化**：圆心、半径、宽度、硬度、反转方向都是 uniform，可以在 `Update()` 里实时改，这是冲击波动画的前提。
- **分辨率无关**：UV 是 [0,1]，不依赖屏幕像素数。换分辨率不需要换贴图。
- **可复用为 SDF 积木**：`length(uv - c)` 这一条线就是所有 [[sdf-2d-primitives|2D SDF 圆/环 / 多边形]] 的开端，后面想叠加 `min/max` 做布尔、想加 `smoothstep` 做柔边、想做多个圆的并集——都是在这套结构上加东西。

文末 Alisavakis 自己也承认：圆盘 mask 单独看几乎没用，圆环 mask 单独看也没用——它们的价值在于成为 [[shockwave-effect]]、[[uv-displacement-image-effect|UV 位移]]、`#TechnicallyAChallenge` 各种小动效的**乘子**。

## 相关

- [[image-effect-mask-blend]] —— 用静态贴图遮罩做局部后处理的前一级
- [[shockwave-effect]] —— 圆环 mask 接 UV 位移就是冲击波
- [[sdf-2d-primitives]] —— `length(uv - c)` 是 SDF 圆的最小形态
- [[unity-image-effect-basics]] —— 全屏后处理的脚架与挂接方式
- [[shaping-functions]] —— `pow`/`saturate` 控制柔边的通用思想
- [[fragment-shader]]
- [[harry-alisavakis]]

## Sources

- [[sources/halisavakis-image-effects-custom-masks-i]]
- [[sources/halisavakis-image-effects-custom-masks-ii]]
