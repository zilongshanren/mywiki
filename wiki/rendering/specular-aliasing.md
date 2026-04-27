---
tags: [rendering, aliasing, specular, pbr, anti-aliasing]
date: 2026-04-27
sources: 1
---

# Specular Aliasing

Specular aliasing 是高频几何或法线贴图在高光计算中产生的闪烁/噪点，与普通几何走样不同，它的信号来源是 BRDF 的微面元镜面反射对法线频率的高敏感性。

## 成因

实时 PBR 的 specular BRDF（GGX/Beckmann 等）在 roughness 接近 0 时对法线方向极度敏感。当一张 normalmap 被近距离或斜向观察时，texel 的空间频率远高于采样分辨率，相邻像素的法线方向差异极大，导致每帧的高光强度剧烈跳动。有几类来源：

- **法线贴图**：mipmap 不能简单对法线取均值，标准双线性/各向异性滤波无法消除 specular aliasing
- **几何法线**：三角形边缘附近的顶点法线插值跳变
- **Planar reflection**：屏幕空间或 reflection card 的采样边界产生硬边高光
- **分析光源**：点光/聚光的 δ 函数 BRDF 响应对法线频率无容忍

## 常见缓解方案

- **法线贴图 roughness 派生**：对 normalmap 做 LEAN/LEADR mapping 或 NDF filtering，把高频法线变化"转移"到更高的 roughness 值（即"越远越粗糙"）
- **TOKSVIG / Kaplanyan NDF filter**：计算 mip 级别内法线向量长度的统计方差，动态增大 roughness
- **Texture space shading / stable shading**：在较低的 shading rate 下减少噪声来源
- **MSAA/TAA 联合**：时域 AA 可以平均化高频闪烁，但引入 ghosting
- **Specular occlusion**：[[angelo-pesce]] 在 BF4 评析中的核心论断——没有 occlusion 的高光是造成 aliasing 视觉可信度下降的根本原因之一，宁可砍掉也不要让没遮蔽的反射留在画面里

## 与 deferred rendering 的特殊矛盾

延迟渲染无法在 GBuffer 中存储完整的 normalmap 频率信息，高频法线会在 GBuffer 写入时损失，但分析光照依然会对存储的（已滤波的）法线产生尖锐响应。这是 deferred renderer 在高频材质上的典型弱点。

## 相关

- [[deferred-rendering]]
- [[ground-truth-ambient-occlusion]]
- [[frostbite-bf4-rendering-analysis]]
- [[pbr-practice]]

## Sources

- [[sources/c0de517e-bf4-graphics-review]]
