---
tags: [source, 渲染, unity, shader, grabpass, 透明物体]
date: 2026-04-14
sources: 1
---

# My take on shaders: GrabPass (Harry Alisavakis)

[[harry-alisavakis]] 在 *My take on shaders* 系列的第五篇（2017-05-17）从全屏 image effect 切换到「物体绑定式后处理」——用 Unity 的 GrabPass 把后处理特效贴到一块世界空间的几何体上。

## 摘要

文章把之前教过的「反色」效果改写成了一支用 `GrabPass { "_GrabTexture" }` 的 shader，挂在场景里的一块 quad / 玻璃片 / 窗户上。Unity 在绘制该物体之前，会把当前 backbuffer 里这块物体即将覆盖的区域**拷贝**进 `_GrabTexture`，shader 用 `tex2Dproj(_GrabTexture, i.uv)` 读出来后随便处理。Alisavakis 强调几个新手坑：（1）SubShader 标签必须 `Queue = Transparent`，否则不会在不透明几何之后被绘制；（2）顶点着色器里 UV 必须改用 `ComputeGrabScreenPos(o.vertex)` 得到一个 float4（包含 perspective divide 的 W），所以片元里要用 `tex2Dproj` 而不是 `tex2D`；（3）通常不需要 Properties 块，因为「显示什么颜色」由背景决定。文末他强调任何之前写过的全屏 image effect（反色、色差、blur、displacement）都能照原样塞进 GrabPass shader——区别只是输入纹理从「整张 framebuffer」换成了「物体覆盖的局部背景」。他还做了个有趣的术语澄清：「behind」并不意味着深度上在物体之后，而是「如果这个物体不存在，屏幕这块区域会画什么」。

## 关键要点

- **GrabPass 的语义**：在画当前物体之前把 backbuffer 里它即将覆盖的区域拷成纹理；不是真的「物体后面的世界」，而是「这块屏幕区域要画的东西」。
- **必须的三件套**：`Tags { Queue = Transparent }`、`GrabPass { "_GrabTexture" }`、`tex2Dproj` + `ComputeGrabScreenPos`。
- 任何 image effect 都能直接平移成 GrabPass shader——只是输入从全屏换成了局部。
- 没有 Properties 块也合法：纹理由 GrabPass 自动产生。
- **代价**：每个 GrabPass 物体都触发一次全屏 backbuffer 拷贝，物体越多越慢。这是它在 URP/HDRP 里被 `_CameraOpaqueTexture` / Copy Color pass 取代的根本原因，参见 [[unity-grabpass-blur]] 的讨论。

## 链接到的概念

- [[unity-grabpass-blur]]
- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[harry-alisavakis]]

## 原文

- 链接：<https://halisavakis.com/my-take-on-shaders-grabpass/>
- 本地：`raw/articles/halisavakis.com/2017-05-17_my-take-on-shaders-grabpass.md`
