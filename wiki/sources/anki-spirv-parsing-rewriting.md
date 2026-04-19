---
tags: [source, 渲染, spir-v, vulkan, hlsl]
date: 2026-04-19
sources: 1
---

# Parsing and rewriting SPIR-V（Panagiotis Charitos / anki3d.org）

[[people/panagiotis-charitos|Panagiotis Christopoulos Charitos]] 2024 年 6 月发的短文，主题是为什么 AnKi 在已有 SPIRV-Tools/SPIRV-Cross/SPIRV-Reflect 的情况下仍要自己手写一个 SPIR-V 解析器——以及证明这件事并不复杂。

## 摘要

SPIR-V 对大多数图形程序员是黑盒二进制 blob，现成工具链能覆盖 90% 场景。但 AnKi 有两个 edge case 没人做：（1）检测 fragment shader 里是否含 `OpKill` 以决定能否启用 early-z；（2）HLSL→SPIR-V 后需要把 DXC 产生的"逻辑 Vulkan binding"原地改写成引擎自定义 binding。文章示范 SPIR-V 的头部是 5 个 32-bit word、指令首字 32 位里高 16 位是 length、低 16 位是 opcode，循环迭代只要 10 行 C++，改写 `OpDecorate DecorationBinding` 的 literal 同理。Charitos 的结论是 SPIR-V 的手写处理"没什么好怕的"，比拉进一个完整依赖轻得多。

## 关键要点

- SPIR-V header = 20 bytes = 5 × 32-bit word；其后是连续指令。
- 每条指令首 word：`length = word >> 16, opcode = word & 0xffff`。
- 检测 discard = 扫描 `spv::OpKill`。
- 改写 HLSL register → Vulkan binding = 找 `OpDecorate id DecorationBinding literal`，改第三个 operand。
- 自己写的理由：依赖最小化 + 现成工具都没这种原地改写 literal 的 API。

## 链接到的概念

- [[spirv-parsing-rewriting]]
- [[compilation-pipeline]]
- [[shader-permutation-explosion]]

## 原文

- 链接：https://anki3d.org/parsing-and-rewriting-spir-v/
- 本地：`raw/articles/anki3d.org/2024-06-04_parsing-and-rewriting-spir-v.md`
