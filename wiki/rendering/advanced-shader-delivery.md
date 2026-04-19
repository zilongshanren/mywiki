---
tags: [shader编译, D3D12, 管线, DirectStorage, GDC2026]
date: 2026-04-19
sources: 1
---

# Advanced Shader Delivery 与 Partial Graphics Programs

GDC 2026 上 Microsoft 公告的一组"shader 交付链"新能力。[[adam-sawicki|Adam Sawicki]] 在 GDC 2026 评注里把它分成两个彼此独立但相关的方向：一个是**把 shader 编译搬出玩家机器**，另一个是**让 PSO 分开创建再链接**。

## 背景：shader 为什么需要"交付"

- 每个 GPU 有不同的 ISA，shader 无法像 `.exe` 那样预编译到本地码
- 现状：**DXIL/SPIR-V → GPU ISA** 这一步在驱动里做，玩家第一次跑到某个 shader 时才编译
- 后果：游戏启动或场景切换时的 "Compiling shaders..." 卡顿——特别是带光追的复杂 shader，Sawicki 亲历过单个 shader 编译超过 1 分钟

## 方向 1：Advanced Shader Delivery / Shader Compiler Plugin

规范：[Shader Compiler Plugin](https://microsoft.github.io/DirectX-Specs/d3d/ShaderCompilerPlugin.html)（此前 Microsoft 已经预告过一次）

- 把 DXIL → ISA 这一步**搬到服务器侧**（或者至少是开发阶段的预处理）
- 玩家端从"编译 shader"变成"下载 shader"
- Sawicki 的冷水：**"我不觉得这是什么大事"**——下载和编译都一样会在游戏更新/驱动更新时发生；唯一确定的好处是下载可能比编译快
- 真正的理论红利是：允许离线编译器**花更多时间做更好的优化**（编译器不再受"毫秒级完成"约束）

## 方向 2：Partial Graphics Programs

规范：[Partial Graphics Programs](https://microsoft.github.io/DirectX-Specs/d3d/PartialGraphicsPrograms.html)

- **允许 PSO 只包含部分阶段**——比如只有 "pre-rasterization"（VS + 可选 HS/DS/GS/Mesh）或只有 pixel shader
- 之后把两半链接成完整 pipeline，**希望不用全量重编译**
- Sawicki 认为这是比 Delivery 更有价值的一项——尤其在开发期间 shader 频繁变动时，可以避免因为只改了 PS 就全 PSO 重建

## 同期的 DirectStorage 1.4

和 shader 交付无关但同一批公告里出场：

- 新增 **Zstandard（zstd）** 压缩格式支持——开源、免专利、Meta 维护
- 之前 Microsoft 力推的是 Nvidia 的 GDeflate，换成 zstd 被 Sawicki 看作"往厂商中立方向走"的正面信号
- 同步公开 [Game Asset Conditioning Library](https://github.com/microsoft/Game-Asset-Conditioning-Library)：给 BC1–5/BC7 纹理做 swizzling 等 pre-processing，把核心无损压缩算法的效果再压一层
- **Sawicki 的疑虑**：DirectStorage 推了好几年，至今没有大量 AAA 游戏或主流引擎**默认启用**；如果收益无法稳定压过传统文件读写，就会重蹈 DirectSR 的覆辙（后者在 retail Agility SDK 出来前被悄悄移除）

## 相关

- [[adam-sawicki]]
- [[pix-api-and-dxdmp]]
- [[dxr-tier-2-clas-ptlas]]
- [[hlsl-cooperative-vectors-tensor-cores]]
- [[d3d12-resource-binding]]

## Sources

- [[sources/asawicki-dx12-gdc-2026-comments]]
