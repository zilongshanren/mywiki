---
tags: [渲染, shader, post-processing, outline, unity, deferred-rendering]
date: 2026-04-14
sources: 1
---

# 表面角剪影（Surface Angle Silhouette）

表面角剪影是一类最简单的描边后处理：用**表面法线和相机视向的点积**判断某个像素是不是正对着观察者，点积越接近 0——即法线和视向越垂直——越可能处于物体轮廓上。它是典型的"免费描边"，因为法线在 [[deferred-rendering|延迟渲染]] 里已经写进了 GBuffer，直接采样就能用。

公式只有一行：

```
edge = 1 - abs(dot(V, S))
```

其中 `V` 是从像素指向相机的向量，`S` 是该像素的世界空间法线。`dot` 的绝对值保证凹凸两面都能识别，`1 - x` 把正对相机的像素压到 0、侧对相机的压到 1，然后拿这个值作为描边浓度去插值场景色和描边色。

## 为什么需要「局部」视向

Sell 强调的一个点是：在透视投影下**相机视向不是一个统一的向量**——屏幕中央的像素朝 forward 方向看，屏幕角上的像素朝斜向看。如果直接用 `_WorldSpaceCameraPos - fragment.worldPos` 是正确的，但如果你只有 UV 和深度，需要手动「反投影」回世界空间：

1. 把 UV 转成 NDC：`ndc = uv * 2 - 1`
2. 用 `_ViewProjectInverse` 乘回 clip 空间
3. 做透视除法 `xyz /= w`
4. 减去 `_WorldSpaceCameraPos` 得到一个从相机出发的方向向量

这一整套在 vertex shader 里做一次，交给 rasterizer 在屏幕三角形上插值，fragment shader 直接用。这也是 Unity 后处理里一个很常见的 "camera ray reconstruction" 小技巧——有了这个方向向量再乘以 `LinearEyeDepth(depth)` 就能反推出像素的**世界坐标**，几乎所有屏幕空间效果都依赖这步反投影。

## Unity post-processing stack 的形态

Sell 的文章同时是 Unity Post Processing v2 stack 的一个入门实录。写一个自定义效果需要两个类：

- `PostProcessEffectSettings` 子类：声明参数（厚度、密度、颜色），用 `[PostProcess(typeof(Renderer), PostProcessEvent.BeforeStack, ...)]` 特性和 renderer 绑定，并选择**注入点**（`BeforeTransparent` / `BeforeStack` / `AfterStack`，决定这个 pass 插在内建效果前还是后）。
- `PostProcessEffectRenderer<T>` 子类：在 `Render(PostProcessRenderContext)` 里拿到 `CommandBuffer`，把参数写进 property sheet 的 uniform，然后 `BlitFullscreenTriangle`。

shader 本身必须声明 `_MainTex`（当前 render target）、`_CameraDepthTexture`（深度）以及 `_CameraGBufferTexture2`（法线，另外三个 GBuffer 分别是 `diffuse+occlusion`、`specular+roughness`、`cumulative lighting`）。从 GBuffer 采样出来的 normal 被打包到 `[0, 1]`，需要 `n * 2 - 1` 解码回 `[-1, 1]`。

## 缺陷与后继

这个方法的硬伤很明显：**只对有圆润曲面的模型有效**。平面墙、立方体、扁片叶子这些表面法线在整个可见区域里几乎恒定，`dot(V, S)` 不会跨越 0——没有轮廓可画。Sell 自己在同系列下一篇直接改用 **[[sobel-edge-detection|Sobel 边缘检测]]** 的深度/法线差分来替代，因为 Sobel 是**相邻像素的差**，能捕捉到"法线在短距离内急剧变化"这种几何事实，对平面交界也管用。

从描边谱系上看，它属于**法线-视向式轮廓**这一流派，和 [[cel-shader-outline|法线 extrude + stencil]] 式硬描边是两种完全不同的思路：前者是纯屏幕空间、免几何、免 stencil，但受限于模型曲率；后者靠把本体 mesh 复制外推一圈得到均匀厚度，但需要 manifold mesh 和额外 draw call。实际美术需求里两者常常一起用：圆润角色用 surface angle silhouette 做柔高光式轮廓，场景物件用 stencil 硬描边。

## 相关

- [[sobel-edge-detection]] —— 同作者同系列的后继方案
- [[cel-shader-outline]] —— 另一条描边流派：法线 extrude + stencil
- [[deferred-rendering]] —— 提供 GBuffer 法线的前提
- [[depth-texture-silhouette]] —— 基于深度差分的另一种描边

## Sources

- [[sources/vertexfragment-surface-angle-silhouette]]
