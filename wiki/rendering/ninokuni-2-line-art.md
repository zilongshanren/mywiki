---
tags: [渲染, NPR, 描边, 线稿, ni-no-kuni, MRT]
date: 2026-04-19
sources: 1
---

# Ni No Kuni 2 的艺术家驱动线稿

Ni No Kuni 2 的视觉识别里最显眼的就是角色上的**动画线稿（line art）**，它不是靠后处理 edge detection 粗糙拉出来的，而是一套**艺术家完全驱动、由 MRT 多通道搬运信息**的管线。[[thomas-poulet]] 在 [[sources/thomas-poulet-ninokuni-2-frame|帧分析]] 里拆出了整个流程。

## MRT 作为艺术家的画布

color pass 同时写四张 RT，其中后两张只对角色生效，专门喂给线稿：

- **RT3 (材质/折叠)**：red 是 material ID（顶点数据直传，裤子的膝盖花纹就在这里 punch-through），blue 是折叠（fold）信息（也是顶点数据直传，让布料褶皱能打到线稿），alpha 是 vertex-to-camera 的点积（面向相机的朝向）。
- **RT4 (线控)**：green 是「线条颜色 / 粗细的艺术家权重」，blue 是角色 ID（0.27451，下游 SSAO 用它来排除角色像素），alpha 是角色到相机的相对距离（用于远距离软化线条）。

这套 MRT 不是存「表面属性」，而是存**艺术家塞进 mesh 顶点和贴图里的控制信号**——哪个边要出线、线条多粗、什么朝向、距离多远。典型的「美术说了算」渲染决策树。

## 线稿合成的三次 drawcall

1. **打包**：把上面四个 RT 的需要通道打包进一张独立 line art 纹理——red = 朝向点积，green = 线条权重，alpha = 角色距离。blue 通道是**此 pass 新算的**：用 material ID 做 edge detection，叠上 RT3.blue 的 fold 信息，得到初版线条。
2. **多采样 + LUT 上色**：对 blue 通道做 8× multisampling 平滑边缘，然后查一张 LUT 把线条上色（LUT 运行时可换，因此可以做「剧情变色线」之类的玩法）。线条再乘 RT4.green 做艺术家权重，避免发梢那种硬边。
3. **合成 + FXAA**：把线稿加回主 color，同时加到 depth map 上（让下游的 [[temporal-antialiasing|SMAA]] 能吃到线条的深度）。再过一遍 FXAA—[[thomas-poulet]] 对这一步存疑，因为线稿上游已经 multisample 过、下游马上还要跑全屏 SMAA，FXAA 看起来是冗余的。

## 和其他 NPR 描边的对比

- 相比 [[cel-shader-outline|cel-shader-outline]] 的「背面外扩 + 翻法线」，此法完全 screen-space，不依赖几何拓扑，更灵活但要付出 MRT 的带宽。
- 相比 [[toon-outline-post-process-modes|屏幕空间 Sobel 描边]]，此法**不用 edge detection 硬算**，而是把艺术家意图当「第一阶数据」搬运——这是为什么它能表现出手绘 line weight 变化。

关键启示：**当一个视觉特征是美术风格的核心时，别让它由一个通用 post pass 来拟合。让它变成一个「数据管道」，从 mesh 一路到最终像素。**

## Sources

- [[sources/thomas-poulet-ninokuni-2-frame]]
