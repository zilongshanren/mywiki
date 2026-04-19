---
tags: [渲染, shader, sdf, 距离场]
date: 2026-04-19
sources: 1
---

# SDF 在 Shader 里的修改与合成操作

[[sdf-2d-primitives|SDF 基元]] 本身只是一堆单一形状的距离函数，真正的表达力来自对它们的**修改与合成**。Xor 的 *Signed Distance Fields* 教程把这些操作归纳成三类——**距离 mod、集合 mod、空间 mod**——加上 distortion 家族，构成 shader SDF 的「乐高组合语法」。底层参考是 [Inigo Quilez 的 distfunctions 系列](https://iquilezles.org/articles/distfunctions2d)；这里做一份面向实战的压缩清单。

## 距离修改（Distance Mods）

这类操作**只动距离值，不动坐标**，最便宜。

```glsl
// 圆角（在原形状外扩 thickness；因此原形状要先缩小 thickness）
float round_dist  = shape_dist - thickness;
// 空心：留一层 thickness 的边
float hollow_dist = abs(shape_dist) - thickness;
// 洋葱：按 spacing 周期复制
float layered = mod(shape_dist + spacing * 0.5, spacing) - spacing * 0.5;
float onion   = abs(layered) - thickness;
```

`abs(shape_dist) - t` 是最精妙的一行：`abs` 把原本穿过 0 的距离折叠成两条「距边界 t」的等距线，结果是一个空心壳。Onion 把它套进 `mod` 就得到一层层嵌套的等距面——raymarched 3D 里用这个可以一步造出 [[needlets|多层同心壳]]。

## 集合操作（Set Operations）

```glsl
float u  = min(d1, d2);          // 并
float s1 = max(d1, -d2);         // d1 减 d2
float i  = max(d1, d2);          // 交
```

直觉：「距离到某物的最近边」在两个物体共存时就是两个距离的较小者——**并集 = min**。取负号相当于翻转「内外」，所以 `-d2` 代表「在 d2 的外部空间里」。

**致命坑**：这些布尔只保证**边界**准确。

- **Union** 破坏**内部**距离——两形状重叠区的内部点，`min` 给出的是更近的那个边，但真正的内部距离可能跨过另一个形状的中间。
- **Intersect / Subtract** 破坏**外部**距离。

后果：`raymarch` 步长不再是 lipschitz 上界，会抖动或穿透；`outline_thickness` 在退化区域扭曲。iq 的 [interior distance 文章](https://iquilezles.org/articles/interiordistance) 坦言这是未解问题；工程解决是退回 [[jump-flooding-algorithm|JFA]] 从 raster 重构真实距离场。

## 空间修改（Spatial Mods）

**对采样点做变换**等同于对形状做逆变换——这是 [[sdf-2d-primitives|SDF 基础]] 里已经建立的直觉，这里扩展到镜像与平铺：

```glsl
pos.y = abs(pos.y);                                         // 对 y 轴镜像
vec2 mirror_pos = pos - 2.0 * dir * max(dot(pos, dir), 0.0); // 沿任意法向镜像
vec2 repeat_pos = mod(pos + spacing * 0.5, spacing) - spacing * 0.5; // 无限平铺
```

平铺对对称形状（圆、方）无副作用；但对**非对称形状**（星形竖向）会破坏原本 seamless 的拼接。iq 的 [sdfrepetition](https://iquilezles.org/articles/sdfrepetition) 给出了「采样相邻 cell 取 min」的 2-tap/4-tap 补救法。镜像同样会在 concave 折角处破坏 interior distance——**跨过折角的那一侧 SDF 不再知道折角的存在**。

## 平滑合成（Distortion / Smooth Min）

iq 的经典 `smin`：

```glsl
float smin(float a, float b, float k) {
    float r = exp2(-a / k) + exp2(-b / k);
    return -k * log2(r);
}
```

把 `min` 换成 `smin` 就得到两形状交界处的**圆滑过渡**——raymarched metaball 的标准写法。代价是它**不再是严格 SDF**（返回值不是真实距离），步长必须保守。

类似地，坐标空间里可以加：

- 小幅位移 `d += noise(pos) * amp` —— 给边缘加毛刺 / 波纹。
- 按 y 旋转 `rot(theta * pos.y)` —— 螺旋扭曲，raymarched cloth 常见。

原则是：**distortion 越强，越远离真 SDF，raymarch 越吃步数**。Inigo 的 demo 里常用「表达式上看起来神奇、但代价是 raymarcher 最大步数从 64 涨到 128」的 trade-off。

## 为什么要用 SDF 做这些

SDF 天然适配：

- [[analytical-antialiasing|analytical AA]]（[[fwidth-derivative-antialiasing]] 模板直接套用）
- **outline / glow / drop shadow**：`dist - thickness` 即可得到偏移边缘，alpha 再套 `1 - smoothstep`；
- [[raymarching-intro|raymarching]]：每步按 `dist` 推进，shader 里直接模型 3D 物体不依赖 mesh；
- **碰撞 / 法线 / AO**：对 SDF 求梯度就是表面法线，对球壳采样就是 AO——都是一行代码。

## 相关

- [[sdf-2d-primitives]]
- [[sdf-ray-marched-shadows]]
- [[raymarching-intro]]
- [[analytical-antialiasing]]
- [[fwidth-derivative-antialiasing]]
- [[jump-flooding-algorithm]]
- [[deferred-sdf-rendering]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-sdf]]
