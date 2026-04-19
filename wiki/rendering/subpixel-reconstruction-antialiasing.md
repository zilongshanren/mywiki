---
tags: [渲染, 反走样, 延迟渲染, 后处理]
date: 2026-04-19
sources: 1
---

# 子像素重建抗锯齿（Subpixel Reconstruction Antialiasing, SRAA）

**SRAA** 是 Chajdas、McGuire、Luebke 在 I3D 2011 提出的一种**把子像素可见性和单像素（1x）着色解耦**的抗锯齿方案。目标是 [[deferred-rendering|延迟着色]] 管线：MSAA 在 fat G-Buffer 上代价高得不现实，而彼时流行的 [[analytical-antialiasing|MLAA]] 只看最终彩色图做形态学重建、几何边界信息全部丢失。SRAA 介于两者之间——**只对深度 / 法线 buffer 做超采样**，着色仍然按单像素跑；在后处理阶段把低分辨率的着色结果按 subpixel 几何信息"重建"到高分辨率。

## 思路

每一帧像素只着色一次（与标准 deferred 相同），但额外渲染一对**超分辨率深度 buffer 和法线 buffer**（例如 4x 或 16x）。这两个 buffer 成本低——只跑 depth+normal 的瘦 pass，不涉及材质采样或光照计算。

SRAA 随后作为一个 post-process kernel 运行：对每个**输出子像素**，它在 3×3 单像素邻域里找权重，权重由中心子像素和邻居像素之间的**深度差 + 法线差**决定（一个双边 bilateral 核）。如果邻居几何上属于同一表面，权重高；跨了几何边界则权重趋零。最后把 9 个邻居的着色结果加权平均到这个子像素上，再把 N 个子像素平均成最终像素——相当于用几何信息反推出"这个子像素应该属于哪一块着色"。

```c
float bilateral(float3 centerN, float centerZ, float3 tapN, float tapZ) {
    return exp(-scale * max(1.0 - dot(centerN, tapN),
                            depthScale * abs(centerZ - tapZ)));
}
```

## 它在 MSAA / MLAA 谱系中的位置

| 方案 | 覆盖采样 | 着色采样 | 对几何边界 |
|---|---|---|---|
| SSAA | N× | N× | 完美，但着色代价 ×N |
| MSAA | N× | 1× | 几何边缘好，对 deferred 不友好 |
| MLAA / FXAA | 1× | 1×（后处理猜边缘） | 基于亮度边缘，丢失真几何 |
| **SRAA** | N×（仅 depth+normal） | 1× | 精确几何边界，固定成本 |

SRAA 的关键卖点：**着色成本不增加**。在 1280×720 下实现为 1.8 ms 的后处理，就得到"相当于 4–16× 着色的抗锯齿质量"。当整帧 shading 时间超过 1 ms（彼时常见 5–10 ms），SRAA 比 [[msaa-ssaa|SSAA]] 净省。

## 与 MLAA / FXAA 的本质差别

MLAA 家族只看 color buffer 做边缘检测——对高频彩色纹理、反走样几何边的判别能力都弱。SRAA 拿到**深度 + 法线**，几何边缘不会被误判成"不是边缘"，也不会把纹理内部的彩色边缘错认作几何边。此外 SRAA 的运行时间不随场景复杂度变化（固定 kernel 大小），这对 frame pacing 友好。

## 后续影响

SRAA 本身没被大量产品化——它要求一份超分辨率 depth/normal buffer，在 2011 年的显存预算下仍偏贵，而一年后 TAA 的雏形（时间抖动 + 复用历史帧）上场后，工业界逐渐转向 [[temporal-antialiasing|TAA]]：TAA 用帧间重投影免去了子像素 buffer，代价是历史帧管理和 ghosting。但 SRAA 留下了一个关键思路——**几何 buffer 比 color buffer 更可靠的边缘信号**，这在今天 [[depth-aware-upsampling|depth-aware upsampling]]、法线引导的 denoising、DLSS 早期版本里都能看到影子。

## 相关

- [[deferred-rendering]] —— SRAA 就是为延迟着色量身设计
- [[analytical-antialiasing]] —— AAA 对"已知形状"有 SDF；SRAA 对所有几何都能跑
- [[temporal-antialiasing]] —— 后来真正取代 SRAA 的路线
- [[msaa-ssaa]]
- [[aliasing]]
- [[depth-aware-upsampling]] —— 同类的"用几何引导彩色重建"思想
- [[matthaeus-chajdas]]

## Sources

- [[sources/anteru-sraa]]
