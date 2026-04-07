---
tags: [计算机系统, csapp]
date: 2026-04-05
sources: 1
---

# 信息 = 比特 + 上下文

CSAPP 的开篇哲学：

> "All information in a system is represented as a bunch of bits. The only thing that distinguishes different data objects is the context in which we view them."

**同一个字节序列在不同解释下意义不同**。

## 表现

- `\x89PNG\r\n\x1a\n` 在 PNG 解析器眼里是文件头；在文本编辑器眼里是乱码。
- `uint32_t x = 0x3F800000` 在 int 解释下是 1,065,353,216；在 float 解释下是 1.0f。
- **字节序（Endianness）**：`0x12345678` 在 little-endian 内存中排列为 `78 56 34 12`。

## 工程含义

- **网络字节序**（big-endian）vs 主机字节序：跨平台序列化经典 bug。
- **Shader 位压缩**：把两个 float16 塞进 uint32，解压行为才赋予它们意义。
- **存档格式**：必须明确规定每个字节的解释规则——否则信息就丢失了。

## 与 APoSD 的呼应

这是 [[obscurity]] 在最底层的体现——意义不在比特里，在上下文里。没有文档或清晰的解释规则时，比特是模糊的。

## 相关

- [[compilation-pipeline]]
- [[obscurity]]

## Sources

- [[sources/csapp-day01]]
