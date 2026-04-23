---
tags: [数据格式, 二进制布局, 序列化, 工程工具, bitsquid]
date: 2026-04-19
sources: 1
---

# 二进制数据定义语言（形式化描述二进制布局）

[[niklas-frykholm|Niklas Frykholm]] 2012 年底抱怨过一个一直悬而未决的"语言学空缺"：数学有代数符号、音乐有五线谱、棋局有 PGN，但描述**二进制数据布局**却至今靠自然语言加 ASCII 缩进表，说一句"4 bytes header id, 2 bytes header length, 0-20 bytes extra"就算是"文档"。结果是：自己写的引擎 runtime 格式无法被别人准确复现，反向解读别人的格式也每次都像破案。

他想象的形式语言应当既**可读**又**可执行**：写一份 `struct` 声明，工具就能把任意匹配的二进制文件翻译成人类可读的键值表示（甚至是 JSON）；反过来，改过 JSON 还能保存回原二进制。调试器读这份声明也能把内存上的 blob 按语义展开，不再需要 `autoexp.dat` 式的黑魔法。

## 语法的取舍

Niklas 倾向 C 风格（直接粘贴 C struct 就能复用），但 C++ 的模板语法太难吃，自造的"似 C 非 C"又容易误用。Lisp 风格容易解析但审美成本高。最终他倾向"受限 C"：保留结构体字面量、增加两项扩展——**数组长度可参数化于先前字段**、**label 生成区段偏移**：

```
struct Level {
  uint32_t num_lights;
  uoffset32_t light_data_offset;
light_data_offset:
  Light lights[num_lights];
};
```

## 完备性的两难

能描述**任意**二进制格式的代价是图灵完备，但那样就等价于"写一段 C 代码解包"，没有提高抽象。Niklas 的折中是：**声明式是语法糖，底层是过程式**——`LightData lights[num_lights]` 展开为一段 `for i=1,num_lights do unpack_light_data(stream)` 的 Lua 伪代码；常见情况保持极简可读，遇到刁钻格式再掉进过程式逃生通道。

## 先例

评论区提到几套既有方案：

- **ASN.1**：电信/协议用的老牌形式描述，威力足但冗长，过于重量。
- **Protocol Buffers**：Google 的二进制定义 + 代码生成，偏向 schema 演化，不擅长描述"把二进制文件映射成内存"这种 freeform 布局。
- **010 Editor Templates** 和 **Synalyze It!**：反向工程圈的事实标准，用类 C 语法写模板，十六进制编辑器按模板高亮——最接近 Niklas 想要的形态。
- **FlatBuffers 的 schema**：同期兴起的"offset 直接寻址、无序列化成本"方案，和 Bitsquid 自己做 [[offset-based-resource-blobs|offset-based blob]] 的思路同源。

## 与 Bitsquid 其他设计的关联

这个构想并非孤立：Bitsquid 整个工具链都在向"人可读的中间态 + 编译出的紧凑二进制"这一两层模型收敛——源数据用 JSON（见 [[bitsquid-3-way-json-merge]] 和 [[c-serialization-metadata|JSON-to-binary pipeline]]），runtime 用 offset-based blob。形式化数据定义语言正是把这种分离再升一层：**让 blob 本身自解释**，调试器、版本迁移工具、二进制 diff 工具都能基于同一份 schema 工作。

## 开放问题

- 版本化与向后兼容：Sam 在评论里点出这是最棘手的部分，ASN.1、PB、FlatBuffers 给的答案各不相同。
- 避免中间 text 表示：每次导出/导入都经 JSON 一次太慢，是否应允许 schema 直接驱动 editor？
- 代码生成：schema 同时编译出 C++ 读写代码，才能真正省下人肉写 serializer 的工作量。

## Sources

- [[sources/bitsquid-formal-language-data-definitions]]
