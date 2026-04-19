---
tags: [source, graphics, hlsl, packing, gpu]
date: 2026-04-19
sources: 1
---

# The Art of Packing Data（Emilio López Ros）

[[emilio-lopez-ros]] 2025 年 6 月发表的技术长文。主题是 GPU 数据打包：把 color、normal、flag、timestamp 等用尽量少的 bit 表达清楚。作者用 HLSL 作为基础语法，对着 RDNA 汇编逐项分析，兼讨论 HLSL SM 6.6 的 pack/unpack intrinsics。

## 摘要

文章按数据类型从简单到复杂地铺开：

1. **Normalized**（UNORM）：乘 255/1023/65535 + 0.5 四舍五入，对应 `R8G8B8A8_UNORM` 等格式；SM 6.6 加了 `pack_u8` / `unpack_u8u32`，RGA 对比显示生成的 `v_perm_b32` 比手写版少两条指令。
2. **Signed Normalized**（SNORM）：负数处理有坑——直接 (x+1)/2 再 unorm 会让 0 无法精确表达。D3D12 的规则是「-128 和 -127 都映射到 -1.0，让 0 有精确表示」。代码上要用 `int` 而非 `uint` 才能靠左移右移保住符号扩展；HLSL SM 6.6 的 `pack_s8` 同样更快。
3. **Bitfields**：DXC 已支持 HLSL bitfield syntax（`uint feature1 : 1;`），生成 `s_bfe_i32` 能直接配合条件选择、省掉 compare 指令；但 GLSL 几乎都不支持。
4. **Bit Extraction / Insertion**：HLSL 没有一等 `bitfieldExtract` / `bitfieldInsert`——作者给出一段能让 DXC 识别并降到 RDNA `bfe`/`bfi` 的模板（注意 `1U` vs `1`、mask 要裁到 31 bit），同时告知 bfi 经常无法被编译器识别。
5. **Octahedral encoding**、**float → half**、**fixed-point timestamps**——作者罗列了若干常用组合方案并给出 RGA 汇编。
6. **工程建议**：永远 `measure`，RGA/Godbolt 是朋友；编译器的识别能力随版本波动，不要过度信任历史技巧。

## 关键要点

- **SNORM 的两个 -1.0**是硬件为了让 0 精确而牺牲掉一个 slot，手写 packer 必须照做否则会出现 mirror 反射轻微倾斜这种诡异 artefact。
- **HLSL SM 6.6** 的 `pack_u8` / `pack_s8` 不仅更短，还让编译器选择更高效的 `v_perm_b32` 指令。
- **HLSL bitfield** 是好东西，但 cross-platform 仍然要 fallback 到手写 shift/mask——GLSL 长期滞后。
- **`bfi` 比 `bfe` 更脆弱**——即使用 GLSL 内建都可能产不出 `v_bfi_b32`，要做性能关键路径请手写 mask + or。

## 链接到的概念

- [[gpu-data-packing]]
- [[compact-vertex-format]]
- [[unorm-float-conversion]]

## 原文

- 链接：https://www.elopezr.com/the-art-of-packing-data/
- 本地：`raw/articles/elopezr.com/2025-06-16_the-art-of-packing-data.md`
