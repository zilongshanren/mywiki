---
tags: [grass, vegetation, deferred, tessellation, geometry-shader, alpha-cutout, unity]
date: 2026-04-14
sources: 1
---

# 延迟渲染下的草地着色器

把一大片草地塞进一个游戏场景，同时还要享受延迟管线的光照与阴影，在技术上是个小型组合题：延迟 G-Buffer 天然不支持半透明，而草的视觉又高度依赖 alpha 边缘。Steven Sell 为他的项目 Realms 写的一个 Unity 方案把五个着色器阶段全用上了：vertex、hull、domain、geometry、fragment，每一阶段都承担一个具体职责。

## 用 alpha cutout 绕过延迟无透明的问题

延迟渲染把材质属性打到 G-Buffer 再做独立的光照 pass，中间不存在「混合源色到帧缓冲」的机会，所以 [[alpha-blending]] 不可用。唯一的出路是 alpha cutout：fragment 达不到阈值就 `discard`，剩下的都是实心像素。Unity 里通过 `AlphaToMask On` 打开，着色器里把源纹理的 alpha 和一个可被其它 pass 覆盖的 `cutAlpha` 值取 min，塞进 `UnityStandardData.occlusion` 字段——它会被写进 diffuse G-Buffer 的 alpha 通道。这样做的好处是纹理 alpha 边界清晰、延迟光照和 [[shadow-mapping-basics]] 都能正常吃到；坏处是没有中间色，需要纹理本身边缘够干净，否则会有明显锯齿。

## 生成几何：tessellation + geometry shader 的流水线

输入是一个 mesh（比如地形的 patch），但真正渲染的是大量小草片。流水线这样组织：

1. **Tessellation（hull + domain）**把一个源三角形按 density 参数切成很多小三角形。单个 density 参数同时控制边 tessellation 和内部 tessellation，世界空间三角形越大，density 越高。这解决的是「源 mesh 三角形太稀疏，生出来的草不够密」。
2. **Geometry shader** 对每个（细分后的）三角形取第一个顶点作为原点，丢掉剩下两个顶点，从那个原点生出一个草的 quad——4 个顶点 + 2 个三角形。
3. **Vertex/Fragment** 处理后续变换和采样。

每片草的宽度与高度来自 `Dimensions`（xy）加 growth map 的纹理采样——后者允许美术画一张高度贴图来控制区域性变化（幼苗 vs 成熟草）。

## 让草"看起来不像被顶视角拆穿"

几乎所有草地方案在低视角（第一人称、越肩）看都还行，视角一抬高或接近俯视就露馅——你能透过 quad 的边缘看到地面空隙。这里作者的办法叫 **perspective bend**：不是做 billboard（完全面对相机），而是把 quad **上方两个顶点**做 shear，向左或右侧局部轴滑动，方向取决于相机 view vector 与草的 right/left 局部向量谁更接近。由于每片草在生成时带了随机旋转，不同草的 shear 量各不相同，整体效果是"草尖稍稍往相机倾倒，把空隙藏起来"而不是死板地齐刷刷转向。两个参数 `GRASS_PERSPECTIVE_BEND`（最小/最大弯曲量）控制程度。

## 风、颜色、互动

- **风**：采样一张 distortion map（全局）得到每个位置的风向向量，`_WindSpeed` 是 map 的 scroll 速度、`_WindStrength` 是弯曲幅度。`GetWindRotation` / `ApplyWindRotation` 在草 quad 的本地原点绕轴旋转上方顶点。高弯曲角度下额外叠加 additive color highlight 来强化"风过时泛光"的感觉。
- **颜色梯度**：`Base Color` → `Tip Color` 从根到尖形成线性渐变，是最便宜的"活感"来源。
- **密度 dropoff**：`_CameraTargetPos` 提供相机看向的世界点，`CalculateDensityDropOff` 根据距离采一张 dropoff map（由美术画出 gradient），近处密、远处稀，比单纯线性衰减更容易调出平滑过渡。
- **互动（尚未完全落地）**：一张 `Disruption Map`，R = flatten、G = cut、B = burn、A = growth，shader 端已经预留通路——游戏代码把玩家/武器/镰刀写进这张贴图就能压草、割草、烧草、种草。

## 和相关概念的连结

这套方案依赖 [[deferred-rendering]] 的 G-Buffer 布局、靠 [[fragment-shader]] 的 alpha discard 绕开透明度限制、由 tessellation 填充几何密度，再靠几何 shear 解决视角退化。它的整体气质和 [[compute-vs-raster-points]] 里「生成大量小几何体」的思路接近，但走的是 geometry shader 这条旧派路线而不是 compute/indirect draw。生产环境里现代引擎更倾向 compute + indirect，但 geometry shader 方案胜在单 shader 自洽、易于接入既有管线。

另一条完全不同的路线见 [[gpu-driven-grass-tiles]]——[[marco-giordano]] 的方案用蓝噪声预烘焙 + vertex shader 扩展 + compute culling + 间接绘制 + 4 路 scan 压 LOD，把决策全部搬到 GPU，而不是让 tessellation/geometry shader 在 raster 阶段动态生成。两者是同题不同解的典型对照：Steven Sell 赢在单 shader 自洽、易接 Unity 管线；Marco 赢在可扩展性与性能上限。

## Sources

- [[sources/vertexfragment-deferred-grass]]
