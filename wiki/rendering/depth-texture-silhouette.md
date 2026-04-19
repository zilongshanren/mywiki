---
tags: [rendering, shader, post-processing, depth-buffer, unity]
date: 2026-04-14
sources: 1
---

# 采样深度纹理做剪影效果

Unity 的 image effect 只要多声明一个 `sampler2D _CameraDepthTexture`，就能在 fragment shader 里拿到每像素的深度值——这张深度纹理是 [[z-buffer|Z-Buffer]] 在后处理阶段的只读镜像，Unity 会在相机那一侧自动填充、零额外成本。只用这一张纹理，就能做出 *Super Mario Odyssey* 里的 **Silhouette 剪影**：近处物体深色、远处物体浅色，viewers 的注意力自然被推到前景。

## 从 `_CameraDepthTexture` 拿到线性深度

原始的深度值是**1/z 的非线性分布**——投影矩阵把近平面 ~50% 的浮点精度分配给近处，远处精度极低（[[z-buffer]]、[[reversed-z]] 都是围绕这个性质做工程优化）。在 fragment shader 里直接 `tex2D` 拿到的并不是"距离相机多远"这种直观的数，所以 Unity 提供了两个宏：

```hlsl
sampler2D _CameraDepthTexture;

float raw   = UNITY_SAMPLE_DEPTH(tex2D(_CameraDepthTexture, i.uv));
float depth = Linear01Depth(raw);   // 映射到 [0,1]：近 = 0，远 = 1
```

`UNITY_SAMPLE_DEPTH` 负责从采样颜色里摘出深度分量，`Linear01Depth` 根据当前相机的 near/far 把非线性深度映射到 `[0, 1]` 线性区间。到这一步为止，你已经有一张"到相机距离"的灰度图了。

## 用 lerp 把距离染成颜色

有了线性深度，剪影就是 fragment shader 里一句 `lerp`：

```hlsl
return lerp(_NearColour, _FarColour, depth);
```

两个 Color 属性暴露给材质面板，`_NearColour` 是近平面的色调、`_FarColour` 是远处色调。Daniel Ilett 在教程里还多加了一道 `pow(depth, 0.75)` 来压缩近处分布、拉大对比——这类 remap 是后处理调参的常用手段。把同样的框架换两个颜色值，就得到"近处白、远处蓝"的深度雾；保留原 `_MainTex` 颜色再用 depth 调明度，就是廉价的距离雾。

## 为什么 image effect 不用操心半透明

不透明物体的深度缓冲由 GPU 在光栅化阶段一次性写好，image effect 看到的是"所有不透明物体画完之后的 z-buffer 快照"，这张快照没有半透明的事——半透明物体通常是 *不写* 深度缓冲（或者用额外的 soft particle 路径），正是为了避免互相遮挡。image effect shader 本身只画一个全屏四边形，既没有"前后关系"也没有"alpha 叠加"，所以**根本不需要关心透明度排序**。这一点跟普通几何 shader 的深度测试行为是完全不同的简化——对学习者是好事，对想做烟雾/玻璃后处理的人是坑。

## 实践注意

- **调 far clip plane**：相机 `far` 设得过大会让整个场景挤在 `depth ≈ 0` 附近，剪影对比全丢；调到刚好覆盖场景是常见做法（教程里用 75）。
- **精度**：远处几十米外的深度差异在 `Linear01Depth` 后可能只有小数点后几位的区别，如果要做距离精确的后处理，考虑 [[reversed-z]] 或手动拿 view-space z。
- **URP 差异**：URP 下 `_CameraDepthTexture` 需要在 pipeline asset 里显式勾选 Depth Texture；后处理写法也从 `OnRenderImage` 迁移到 [[blit-render-feature]]。

## 相关
- [[z-buffer]]
- [[reversed-z]]
- [[scene-color-depth-nodes]]
- [[unity-image-effect-basics]]
- [[image-effect-colour-transform]]
- [[separable-gaussian-blur]]
- [[coordinate-spaces]]
- [[urp-depth-prepass-passes]] —— 为什么自定义 shader 要补 DepthOnly / DepthNormals 两个 Pass，以及它们在 URP 里的填充时机
- [[urp-render-objects-feature]] —— URP 的 Renderer Feature 无代码做 X-ray、物体 mask、透视显隐

## Sources
- [[sources/danielilett-image-effects-depth-silhouette]]
- [[sources/danielilett-shader-code-depth-buffer]] —— URP + HLSL 手写版的 silhouette shader：ZWrite/ZTest 命令、`ComputeScreenPos` + `xy/w`、`Linear01Depth` + `_ZBufferParams`、自定义 shader 补 prepass、Render Objects 做 X-ray
