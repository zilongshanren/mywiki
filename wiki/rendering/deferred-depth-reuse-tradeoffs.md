---
tags: [渲染, 延迟渲染, g-buffer, depth-buffer, x-plane]
date: 2026-04-19
sources: 1
---

# 延迟管线里复用深度的三条路线（Supnik 2012）

[[ben-supnik|Supnik]] 在 2012 年 7 月给 X-Plane 10.10 延迟管线调 G-Buffer 时，把"如何让光照 pass 读到眼空间位置"这件事整理成三条互斥的工程路线。问题的背景是：**延迟渲染的光照 pass 既要采样深度去重建世界位置（做光源衰减和阴影），又要把同一张深度缓冲绑成 DEPTH 做硬件深度剔除**（light volume stencil trick、soft particle 的填充率剔除都依赖它）。同一份深度要同时当"纹理"和"深度附件"用，就撞上 API 的读写冲突。

## 路线 A：拷贝深度 buffer 到深度纹理

在 G-Buffer 写完之后 `glCopyTexSubImage` 把 D24S8 复制到一张 `GL_DEPTH_COMPONENT24` 纹理。**成本是一次整屏 full-screen copy，但省下 G-Buffer 一个颜色附件**。Supnik 实测在 2012 的硬件上性能不再是问题——早年复制深度的驱动坑"终于被磨平了"。这条路的缺点是显存里多一份深度，优点是 API 最干净，任何平台都能走。

## 路线 B：同一张深度既绑纹理又绑深度附件（NV_texture_barrier）

把 D24S8 作为**纹理附件**（不是 renderbuffer）挂到 G-Buffer FBO 的 depth slot，光照 pass 里把同一张纹理绑给 HDR accumulate target 的深度，再调 `glTextureBarrierNV()` 保证 G-Buffer fill 全部落盘，然后关 depth write / depth test、在 shader 里采样这张深度。`GL_NV_texture_barrier` 放宽了"同一张纹理不能在单 draw 里同时读写"的约束。

**只在 Windows 上可用**——这个扩展没跨到 Mac/Linux；Supnik 自己没测，因为 X-Plane 的需求（下面）决定了他走不了这条路。理论成本是三条里最低：既不多拷贝、也不占 G-Buffer 通道。

## 路线 C：往 G-Buffer 里显式写眼空间 Z

把一个浮点 Z 通道塞进 [[xplane-gbuffer-format|G-Buffer]]——Supnik 选的是 16F。**浪费 G-Buffer 带宽，但绕开了所有深度 buffer 复用问题**。在能读 Z 的平台上是"最老的"方案；在不能同时采样 + 深度测试的老硬件上，这是"唯一"方案。

## 为什么 X-Plane 必须走 C

X-Plane 在一帧里画**两个独立的深度域**：外部世界（远剪裁 100 km+），3D 座舱（近剪裁 1–5 cm）。任何单一 D24S8 都装不下这个量级比——算到尾 30+ bit 才够，但硬件只给 24 位。两个 depth domain 意味着**没有任何一张统一的 Z 缓冲持有整屏完整位置信息**。要用路线 A/B 就得给每个 domain 各做一遍完整 G-Buffer mix-down，成本翻倍。显式写 16F 眼空间 Z 是**把"分段深度"在 G-Buffer 里扁平化成一份浮点位置**，代价是一个 G-Buffer 通道。

16F 是一次权衡：近处精度要足（阴影依赖近 Z），远处只喂雾所以精度可以挂。ATI 上 16F 填充比 32F 快，Supnik 据某份 presentation 先选 16F，保留"出阴影 bug 就换 32F"的回滚空间。

## 和 log-depth 的关系（评论补充）

Outerra 当时用 log-depth 想在单缓冲里塞巨大的深度范围，读者在评论里推荐。Supnik 试过，指出两个坑：(1) `log(z)` 在 z<0 未定义——几何横跨相机平面会产出 NaN；(2) 如果靠 fragment shader 改写 depth，早期 Z 剔除被禁用。X-Plane 放弃 log-depth，留在三条主线里继续选 C。

## 分类轴

| 路线 | G-Buffer 通道 | 深度复制 | 平台约束 | 能跨 depth domain |
|------|--------------|---------|---------|------------------|
| A 拷贝 | 不占 | 每帧一次 full-screen | 通用 | 否（仍需两遍） |
| B 纹理 barrier | 不占 | 无 | NV Windows | 否 |
| C 写 Z 到 G-Buffer | 占一通道（16/32F） | 无 | 通用 | **是** |

## 相关
- [[deferred-rendering]]
- [[xplane-gbuffer-format]]
- [[multiple-render-targets]]
- [[cheat-by-solving-less]]
- [[ben-supnik]]
- [[xplane-deferred-pipeline-hacks]] —— 2012-11 四连篇：路线 C（G-Buffer 写 16F 眼空间 Z）在 10.10 完整管线里的落地全景

## Sources

- [[sources/supnik-deferred-depth-3-ways]]
