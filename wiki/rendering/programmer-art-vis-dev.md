---
tags: [渲染, 视觉设计, 后处理, 美术, shader]
date: 2026-04-19
sources: 1
---

# 程序员美术的视觉打磨（Vis Dev）

Xor 在 *GM Shaders: Vis Dev* 里谈一个常被 shader 系列忽略的话题：**写代码的人没美术天赋也能把画面做得好看**。关键不是画技，而是**有意识地**在四个维度上做选择——色板、分辨率、细节分布、灯光。论据来自 SUPERHOT、INK、OTXO、Thomas Was Alone、Minecraft、Inside 这类「视觉简单却高完成度」的游戏：它们都不靠细腻写实，而靠**一致性和意图**。

## 色板（Color Palette）

程序员常见误区：配色太花、饱和度太高。更稳的路线是**少即是多**——SUPERHOT 只有黑白红，OTXO 三色，足以形成识别度。Xor 的两个操作建议：

- **预处理贴图**：用一个 LUT / 调色 shader 把所有纹理过一遍，强制落入同一色板范围（结合 [[color-quantization-kmeans]] 或 [[floyd-steinberg-dithering|抖动]]）。
- **看直方图**：在 GIMP 或代码里打一下 [[color-banding|亮度直方图]]——如果发现最亮像素卡在 195/255，说明还有 30% 的亮度头；整体乘一个系数就能出戏剧性的提升。黑位同理。

这和 [[gamma-correction-srgb|gamma]] 是一对：对比度调整必须在 linear 空间做才不会出「人工橙色」。

## 分辨率与比例尺（Resolution & Scale）

**不要混用不同 pixel scale 的 sprite**。8×8 的角色放进 64×64 场景里会立刻破功——不是尺寸不对，是单个像素对应的世界单位不一致。先定好一个 native pixel size（例如一个 tile 是 16×16，屏幕 480×270），所有资产对齐到这个尺度。分辨率低 = 休闲 / 幽默；分辨率高 = 严肃 / 写实。两种都可以，但**只能选一个**。

这个约束同时限制了 [[texel-pixel-conversion|texel/pixel 关系]] 和 [[dynamic-resolution-scaling|动态分辨率]] 的调参空间——放大倍数必须是整数倍才能保持 pixel-perfect。

## 细节分布（Detail Distribution）

程序员倾向**把细节堆在 gameplay 核心对象**（锁、钥匙、道具），结果背景过空，角色看起来浮在上面。解决方法不是去给背景画素材，而是**加一点低频信息**：轻微的波纹图案、柔和 drop shadow、模糊云层、甚至一点 vignette——这些可以全部用 shader 程序化生成，不需要画师。

核心原则：**整个画面的「细节密度」应该连续**。可以故意让背景更软以凸显前景，但不能让背景空到变成色块。这一原则和摄影里的 [[scatter-bokeh-dof|DoF]] 哲学相通——刻意引导视线，而不是把所有东西都画清楚。

## 灯光与阴影（Lighting & Shading）

Xor 的偏好：**软的 drop shadow**。原理上它只是把主角 sprite 模糊一层后偏移 + 压暗——几乎零美术成本，却能立刻「把物体从背景里拎出来」，给 2D 画面加一维深度感。他甚至把软阴影**叠在物体上方**当作自遮蔽，营造廉价 3D。

再补四种几乎每款 stylized 游戏都会用的工具：

- **Bloom / Glow**：引导玩家注意到宝箱、奖励、出口。
- **Outline**：提示可交互对象——在 [[cel-shader-outline|cel 风格]] 或 [[animated-dotted-outline-shader|动画虚线]] 里尤其常见。
- **Vignette**：把视线收拢到屏幕中央。
- **Fog**：既能制造氛围也能遮 LOD 切换。

选择意图远比选择数值重要：**冷光 vs 暖光、硬影 vs 软影、全阴影 vs 无阴影**——每一种都是叙事决定。

## 执行清单

1. 选定 3~6 色的主色板，给所有贴图过一遍 LUT 统一。
2. 选一个 native pixel size，所有资产对齐。
3. 看直方图——用满亮度和对比度范围。
4. 补一层背景低频，让细节密度均匀。
5. 加软 drop shadow 抠出前景；bloom / outline / vignette 做视线引导。

## 相关

- [[color-lut]]
- [[color-quantization-kmeans]]
- [[color-banding]]
- [[gamma-correction-srgb]]
- [[cel-shader-outline]]
- [[bloom-threshold-blur-composite]]
- [[chromatic-aberration-post]]
- [[texel-pixel-conversion]]
- [[creative-coding-process]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-vis-dev]]
