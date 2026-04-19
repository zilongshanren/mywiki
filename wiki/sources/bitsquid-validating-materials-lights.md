---
tags: [source, rendering, pbr, arnold, validation, stingray]
date: 2026-04-19
sources: 1
---

# Validating materials and lights in Stingray（Jp）

Bitsquid / Stingray 博客 2017-07-16，作者 **Jp（Jean-Philippe Guertin）**。讲 Stingray 1.9 新增物理光时，如何用 Autodesk 收购 SolidAngle 带来的 **Arnold** 作为地面真值，逐项验证 material BRDF 与 light 属性。

## 摘要

Stingray 团队起初想效仿 Fox Engine 那套"真实光室对照"，但担心拍照对比时噪声和流程误差混在一起无法定位具体 bug，就先走离线渲染器对照的路线——既然 Autodesk 这边能拿到 Arnold license 而且 SDK 免费（无 license 只是水印），就写了一个 Stingray 插件反射 scene 到 Arnold，并自定义 Arnold Output Driver 把线性数据直接送进 Stingray viewport，让同一个 gamma + tonemap 出图，尽量减少不必要的误差源。

Material 映射最麻烦。用 Arnold 4.3 时 `Standard` 不太能对齐 Metallic/Roughness；换 `alSurface` 用两套 specular 分别承担 non-metal 和 metal 分量才对上。中途 Arnold 5.0 发布 `aiStandardSurface` 直接支持 metalness，映射就干净了。对照中发现两个材质 bug：一是 Fresnel 贡献没从 diffuse 里扣除，导致掠射角反射偏强（能量不守恒）；二是金属的 Fresnel 是否要被 base color 染色——作者从 Brooke Hodgman 的推文得到优雅答案："金属反射有色是因为 Fresnel 波长相关，但所有波长在 90° 都趋近 1"，因此统一用无染色 Fresnel 加 Karis 的 2D LUT 预积分即可，结果与 Arnold 在 edge tint 上接近。

Light 侧最大问题是 Stingray 的衰减是 `I / (d+1)²` 而非物理正确的 `I / d²`——这是为了避免在 d→0 时强度爆掉污染光照累积 buffer。代价是在建筑可视化场景下曲线偏离严重，即使按 1m 校正也不对。Stingray 1.10 的修复：改成 `I / (d+ε)²`（ε = 1/max_value），并在写入/读取累积 buffer 时按 Nathan Reed 的 *artist-friendly HDR with exposure values* 做 EV 移位。IES profile 与色温也一并对照通过。

## 关键要点

- **离线渲染器做 ground truth 比摄影更可操作**：Light Path Expressions 能拆项对照（"是 diffuse 错了还是 specular 错了"），比看一张合成照片定位 bug 高效得多。
- **能量守恒是最容易翻车的点**：Fresnel 的能量没从 diffuse 扣出，场景里光滑面会"亮过头"。
- **metallic Fresnel 不染色**：染色属于 F0（基础反射率），而不属于 Fresnel curve 的形状——这是社区里流传多种错误实现的老 bug。
- **Stingray 的 `I/(d+1)²` 衰减** 是个典型 "为 HDR buffer 数值稳定性牺牲物理正确"的折中，换成 EV 移位后两边都能要。
- **自定义 Arnold Output Driver** 把离线线性数据直接喂给在线 gamma/tonemap 管线，排除色彩管理差异——是"最小对照系统"的教科书做法。

## 链接到的概念

- [[material-light-validation]]
- [[physically-based-shading]]
- [[physical-camera-model]]

## 原文

- 链接：https://bitsquid.blogspot.com/2017/07/validating-materials-and-lights-in.html
- 本地：`raw/articles/bitsquid.blogspot.com/2017-07-16_validating-materials-and-lights-in-stingray.md`
