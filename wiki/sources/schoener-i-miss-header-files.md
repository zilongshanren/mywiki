---
tags: [source, 编程语言, zig, c, api设计]
date: 2026-04-19
sources: 1
---

# I miss header files（Sebastian Schöner）

[[sebastian-schoener]] 2026 年 3 月的短文。作者把自己的一段 C 风格 C++ 代码迁到 Zig 之后，反思了一件挺反直觉的事：**即便他和大家一样厌烦 header 文件的重复，却也怀念它们**。

## 摘要

Zig 用 `pub` 在定义处内联标注导出——省去了头文件的冗余同步，但代价是消费者必须通读整个模块才能看出「这个库对外暴露了什么」，本质是**把一次性维护成本转嫁成每次阅读成本**。文档页不是答案，因为当你人已经在源码里时再跳去浏览器是种绕路。C++ 的反向问题（private 成员漏进 header）较轻；作者反而讨厌 C 世界流行的 single-header 库，更偏好经典的「头 + 编译单元」拆分。好消息是 Zig 从 Go 偷来了「stdlib 自带语法解析器」的传统，30 行脚本就能生成一张 auto-generated API surface——**可以既要维护者友好又要消费者友好**。

## 关键要点

- `pub` inline 导出的真正成本在**消费者的阅读体验**，不是维护成本
- 「文档网站」是换工作流，不是同一工作流下的解决
- C header 的副作用（private 成员外漏）比 `pub` 的副作用（需要通读）轻
- Zig stdlib 自带 parser，API 提取工具轻易可写
- 作者怀疑这一立场部分来自「他在写库而不是消费库」——留作开放题

## 链接到的概念

- [[header-file-vs-pub-export]]
- [[zig-c-abi-boundary]]

## 原文

- 链接：https://blog.s-schoener.com/2026-03-27-headers/
- 本地：`raw/articles/blog.s-schoener.com/2026-03-27_i-miss-header-files-sebastian-schoner.md`
