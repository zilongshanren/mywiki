---
tags: [编程语言, api设计, zig, c, c++, 可读性]
date: 2026-04-19
sources: 1
---

# 头文件 vs `pub` 内联导出：消费者 vs 维护者视角

C/C++ 把「接口」（header）和「实现」（compilation unit）物理分开；Zig、C#、Rust、Go 等更现代语言选择在定义处用 `pub` / `public` 标注「这个东西对外可见」。[[sebastian-schoener]] 在把一段 C 风格 C++ 代码搬到 Zig 时表达了一个反直觉的立场：**他依然怀念 header 文件**。

## `pub` 标注内联的代价

表面看，`pub` inline 去掉了冗余——不用两处同步声明。但要回答「这个库对外暴露什么」时：

- C header：`head.h` 一打开就是全部对外接口，是**已经为消费者整理好的索引**
- Zig `pub`：要读完整个模块，把所有 `pub` 标注挑出来拼一张图

作者形容这是「读 10000 行只关心 50 行」。**维护者省的几行同步代码，成了每个消费者的额外阅读成本**——成本重心从一次性维护转嫁给了每次阅读。

## 文档页不是答案

有人会说「用文档网站就好」。但当你已经在读源码、手边是编辑器——跳去网页（Zig 有 `-femit-docs` 可产出 HTML，但作者试下来本地 WASM 也打不开）是种绕路。「阅读源码现场」和「阅读文档」是两个不同的工作流，前者不该被后者劫持。

## C++ 的反向问题

C++ header 的短板正好相反：**private 成员被迫出现在头里**。这是 header 编译模型的副作用。作者个人不在意（他的 C++ 不写 private 成员）；C 世界流行的 single-header 库也有类似「接口与实现挤在一起」的不舒服，他宁可继续 `header + .c` 的经典拆法。

## Zig 的补救：stdlib 带编译器

Zig 从 Go 偷来了一个好习惯：**标准库里就带语言解析器**。因此 30 行写一个 API 提取工具就能得到：

```zig
//! AUTO-GENERATED API SURFACE for library 'Test'.
pub const log = @import("log.zig");
pub fn add(lhs: i32, rhs: i32) i32;
pub fn name() [*:0]const u8;
```

——对消费者来说等价于一张 header。作者的结论是「可以既要又要」：**源代码用 `pub` 标注（维护者友好），工具自动抽取出头文件视图（消费者友好）**。

## 更广视角

这场争议映射到 [[zig-c-abi-boundary|Zig 跨 DLL 只能走 C ABI]] 的大背景：当作者不得不给 Zig 代码「重新发明头文件」来跨越 DLL 边界时，**头文件作为独立工件的价值又被独立验证了一次**——它不仅仅是老派写法，也是接口抽象的一种表达形式。

## 相关

- [[zig-c-abi-boundary]]
- [[abstraction]]
- [[interface-vs-implementation]]
- [[sebastian-schoener]]

## Sources

- [[sources/schoener-i-miss-header-files]]
