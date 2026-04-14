---
tags: [渲染, 2d, sprite, 描边, 风格化]
date: 2026-04-14
sources: 1
---

# 八方向位移的 2D Sprite 描边

**八方向位移描边**是一种给 2D 精灵加轮廓的廉价技巧：把原 sprite 复制 8 份，染成描边色，分别往上、下、左、右和四个对角线方向各偏移一个像素再贴回去，最后在上面叠原 sprite。八份副本的并集形成了一圈均匀厚度的纯色外框，视觉上等价于「对 alpha 通道做一次腐蚀/膨胀取差」，但实现只用到平移和 alpha blending，不写任何 shader。

这招是 [[simon-trumpler|Simon Trümpler]] 在 Game Art Tricks 第一篇里从 Nicolae Berbece 那里听来的。它看起来比「整体把精灵等比放大一点」更可靠：单纯放大会让中心点发生缩放，细节（发丝、手指、武器）的相对位置跟着变，描边粗细也会被几何形状扭曲；而 8 份平移后的副本在**像素级**贡献外轮廓，原图的每一个凸起——即使小到一个像素——都会在八个方向各留下一道 1-pixel 的描边。

这套方法的几个性质是它比 Sobel / Canny 后处理更讨喜的原因：

- **无锯齿**。描边本身是原 alpha 的位移副本，不经过梯度估计，因此不会出现 screen-space 边缘检测常见的齿状边界。它相当于在做一个精确的 Chebyshev-distance ≤ 1 的形态学膨胀。
- **保留 soft alpha**。原图带柔边（例如头发、手腕的半透明像素）时，描边会自然地吸收这份透明度——这是 Sobel 做不到的，边缘检测会把 0.5 的 alpha 当成锋利的跳变。
- **形状被「放大」而非「勾画」**。非常小的细节比如一个 1px 的圆点在 8 方向外扩后会自然变成一朵小十字花——不是瑕疵，而是风格。Simon 举的例子是标点符号变成装饰花纹。
- **绘制 9 份而不是 1 份**。代价是可控的，只在需要描边的小区域付出 8 倍 fill rate，对 2D 游戏几乎可以忽略。

一个限制是**改动要重新导出**：描边粗细、颜色都烘焙在运行时的 blit 调度里，不能像后处理那样一键微调。Simon 在文末自己承认：post-FX 对美术调参更友好。这就是经典的**资产工作流 vs 渲染管线可配置性**之间的取舍——八方向位移把复杂度推到生产阶段，换来运行时 zero-cost 的确定性视觉结果。这种思路和 [[cel-shader-outline]] 里「预先把 shell mesh 烘焙好 vs 在 shader 里 extrude」的取舍，是同一个硬币的两面。

## 相关

- [[cel-shader-outline]] —— 3D 下的 shell extrude 版本，同样用「复制一份放大」的直觉
- [[depth-texture-silhouette]] —— screen-space 描边作为对照
- [[alpha-compositing]] —— 八份副本的底层原语

## Sources

- [[sources/simonschreibt-cell-shading]]
