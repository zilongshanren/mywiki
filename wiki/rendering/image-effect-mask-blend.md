---
tags: [渲染, unity, 后处理, mask, 屏幕效果]
date: 2026-04-14
sources: 1
---

# 屏幕后处理的遮罩混合（Image Effect Mask Blend）

把一支全屏后处理 shader（比如反色、模糊、色差）只施加在画面的**某一块区域**上，而不是整张 framebuffer，是最朴素也最常用的「定向特效」技术。做法是引入第二张纹理作为**灰度遮罩**（mask texture），用它的亮度值在「原图」与「处理后图」之间做线性插值。

## 核心思路

设 `col` 为相机原始输出，`maskedCol` 为施加了某种特效（反色、blur、色相偏移……）后的颜色，`m` 为遮罩在该像素的灰度值（0 = 黑，1 = 白），合成公式就是一个标准的 lerp：

```hlsl
return maskedCol * m + col * (1 - m);
```

或者等价的 `lerp(col, maskedCol, m)`。白色区域出特效，黑色区域保留原画，灰色区域按比例混合——和 Photoshop 里的图层蒙版同构。Harry Alisavakis 在 *My take on shaders* 第三篇里就用这一行代码把「全屏反色」改成了「圆形区域反色」，作为他给初学者的第一种「用 [[unity-image-effect-basics|image effect 骨架]] 做点空间控制」的练习。

## 这种朴素遮罩的限制

直接拿一张外部贴图当遮罩有两个明显的缺陷：

1. **必须和屏幕同宽高比**。遮罩按屏幕 UV 采样（`tex2D(_MaskTex, i.uv)`），如果原图是 16:9 而遮罩是 1:1，圆形会被拉成椭圆。要么准备多套遮罩，要么在 fragment shader 里做 aspect-ratio 校正。
2. **不能动态变化**。遮罩是一张烘焙好的位图，圆心、半径、形状都被固定下来——想做「冲击波从角色脚下扩散」这种动效得换贴图或者直接在 shader 里用 SDF / 数学函数生成遮罩。

第二点也是 Alisavakis 后续的「自定义 mask」教程要解决的问题：用 [[sdf-2d-primitives|2D SDF]] 或者 `length(uv - center)` 这类闭式表达式在 shader 里实时算遮罩，参数（中心、半径、衰减）就能从 C# 脚本传进来。

## 做特效区域化的通用配方

理解了这层「mask = 局部 lerp」之后，几乎任何全屏后处理都能被「局部化」：

- **反色 / 黑白 / 色相偏移**——Alisavakis 的入门例子。
- **模糊 / 散景**——比如 [[unity-grabpass-blur|GrabPass Gaussian blur]] 加上中心淡出的圆形遮罩，做「角色面前清晰、视野边缘模糊」的注意力引导。
- **[[chromatic-aberration-post|色差 / RGB shift]]**——把径向偏移强度乘上中心向外的 gradient mask，本质上就是这一招。
- **[[uv-displacement-image-effect|UV 位移]]**——遮罩控制哪些区域参与扭曲，是冲击波、热浪、玻璃折射效果的基础。

这种「先做全屏特效，再用 mask 把它限制到目标区域」的工作流是新手 shader 学习路径上的第二级台阶——第一级是看懂 fragment shader 一行返回 `1 - col` 反色，第二级就是知道「我可以加一张 mask 控制哪里反色」。

## 相关

- [[unity-image-effect-basics]] —— 全屏后处理的脚架与挂接方式
- [[chromatic-aberration-post]]
- [[uv-displacement-image-effect]]
- [[unity-grabpass-blur]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## Sources

- [[sources/halisavakis-image-effects-simple-masks]]
