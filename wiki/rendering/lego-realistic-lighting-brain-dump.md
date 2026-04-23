---
tags: [lighting, brdf, normal-mapping, ldraw, rendering, lean-mapping]
date: 2026-04-19
sources: 1
---

# Lego 真实感光照的"清单帖"：BDRF、法线、边缘与环境

2013 年 [[ben-supnik]] 把 BrickSmith 新渲染管线（[[bricksmith-instancing-pipeline]]）的光照前景写成了一条**wish list**——对比一张漂亮的 POV-Ray 级 lego 渲染图和一张朴素 forward-shaded 截图，推导要做到「看起来像照片」需要模拟哪些物理效应。这篇更像设计脑图而不是实现方案，但**把小件物体的光照工程问题整理得特别清楚**：LDraw 材质非常少、纹理单元大把空着，大部分"游戏内容里成本太高"的技术在这里都可以用。

## lego 真实感的五条观察

Supnik 抓起家里唯一那套 **Maersk 列车** 对窗观察，列出下面几条视觉线索。每一条都对应一套渲染技术：

### 1. 非标准 BRDF

lego 砖高反光，但反射强度按角度衰减的形状**不是简单 exp(specular)**。因为材质种类有限（ABS 塑料的各种色），**用 lookup table 纹理为每种 surface 存一条完整 BRDF 曲线是可行的**——游戏内容里没人这么做是因为材质动辄几百种，这里只有十几种。

### 2. 砖面不是平的——法线贴图的机会

"方砖一侧"实际不是平面：中间有一丝凹陷，四个角略凸出；角上那一圈微小凸起在侧光下会产生**刚好在砖边缘之内的反光亮带**。这是**制造工艺的特征**（Supnik 打赌是 TLC 故意这么做的——公司以品控著称）。用一张 tangent-space normal map 就能重建这种反光（参见 [[tangent-space-normal-mapping]]）。

### 3. 斜坡砖的 grit 纹路 → LEAN mapping

斜坡砖（slope brick）的斜面有细粒度磨砂纹路，效果上等于**把局部 BRDF 的粗糙度拉高**。如果用普通 normal map，纹理 mipmap 下采样时法线平均，会丢掉粗糙度本身——**LEAN mapping**（Linear Efficient Antialiased Normal mapping）通过在 normal map 里额外存法线的二阶矩，保证 mipmap 后 specular 响应仍然正确。在 LEGO 场景里这个技术的成本完全吃得下。

### 4. 砖块边缘：折角与 crack AO

LDraw 格式里砖的边缘是**用线段画出来的**——目的是方便画说明书风格的 wireframe。但真实砖块的边缘略微倒角（faceted），这带来两个视觉效应：

- **沿折角的高光**——边线在柔和折角上产生的细反光。
- **砖与砖交界处的深色 crack**——本质上是**自阴影 / 环境遮蔽**。

Supnik 的想法：**给 LDraw 的 line segment 赋上"折角均值法线"**，然后用这些线段参与 specular 高光绘制——把原本只为 wireframe 服务的几何改造成光照辅助。

### 5. 装配松紧带来的位姿噪声

玩家装砖不会每块都严丝合缝，会有**微小的角度偏差**。这一层噪声导致：法线有细微扰动、砖间 crack 被放大、自阴影更明显。实现起来就是**对每个砖的 instance transform 叠一个极小的随机偏移**（正好用 [[bricksmith-instancing-pipeline]] 的 per-instance matrix）。

## 间接光：环境贴图 + SSAO 胜过硬投影

POV-Ray 风格 render 常用 **cast shadow**，但 Supnik 觉得 lego 的典型观赏环境是**室内漫射光**——阴影边缘不清晰、光源分布柔和。真实感来自**环境遮蔽（AO）**而不是直接阴影。

他勾画的延伸方案：

- **Image-based lighting with environment map**——收集室内光照的分布变化。
- **Deferred shading**——法线平面里做 normal-map blending（有些 normal 方案对 hardware blending 友好），便于把线段 / 折角法线叠加到基础法线上。
- **屏幕空间 reflectance / AO**——在屏幕空间邻域里采样 shadowing 与 color bounce，逃出去的射线查环境贴图。

这等于把一整套 AAA 延迟管线（[[xplane-deferred-pipeline-hacks]] 的近亲）重搬给一个建模软件用——成本是吃得起的，因为 lego 不需要复杂材质系统。

## 一个诚实的限制

**LDraw 格式本身没有 normal map、没有 roughness 参数、没有 material description**——上面所有方案都需要**给每种部件手工补一套材质 metadata**。这是和游戏渲染的最大区别：数据源的表达力决定了算法能走多远。Supnik 很克制地把这篇定位为"先跑平滑法线和新渲染器，然后再想 LOD（[[bricksmith-instancing-pipeline]] 里提过 Datsville 跑 5 fps），这些光照效果是后话"。

## 文章脉络的意义

这一篇少有地**不是事后反思踩过的坑**，而是**一次诚实的 forward-looking 设计稿**——展示 Supnik 在小规模真实感渲染上的品位（"环境遮蔽 > 硬阴影"、"LDraw 的小材质集合 > 游戏的大材质集合" → "那些被游戏丢掉的昂贵技术都捡回来"）。这份品位在 X-Plane 上往往要被实时预算压扁，只有在 BrickSmith 这样的业余项目里才能完整展开。

## 相关

- [[ben-supnik]]
- [[bricksmith-instancing-pipeline]]
- [[tangent-space-normal-mapping]]
- [[microfacet-brdf]]
- [[occlusion-culling]]
- [[xplane-deferred-pipeline-hacks]]

## Sources

- [[sources/supnik-lego-lighting]]
