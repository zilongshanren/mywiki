---
tags: [source, c, cpp, 构建系统, 资源嵌入]
date: 2026-04-19
sources: 1
---

# C/C++ Embedded Files（Nikos Papadopoulos / 4rknova.com）

[[nikos-papadopoulos]] 2013 年 1 月的短文，用三段示例讲清楚「在 C/C++ 里把二进制文件打进可执行文件」的三种常见做法。

## 摘要

文章把选择分成三档：最外层是构建前跑 `xxd -i` 或 imagemagick 把资源转成 C 头文件，通用但慢；中间一档是利用预处理器 `STRINGIFY` 加 `#include` 嵌入纯文本 shader，省依赖但要求被嵌入的文件自身加宏包裹，仅适合 ASCII；最干净的是 GCC 内联汇编 `.incbin`，直接让汇编器把文件复制进 `.rodata`，用 `incbin_name_start/_end` 两个符号取指针和长度，几乎零编译开销——代价是绑定 GCC/Clang 工具链，Windows MSVC 不支持。作者坦言 ASM 方案是平台特定的，要自行考虑跨平台回退。

## 关键要点

- `xxd -i` / imagemagick 是最普适的"转 C 数组"做法，但把字节展开成巨大头文件会显著拖慢编译。
- 预处理器 `STRINGIFY(#A) + #include` 让 shader 以字符串字面量形式落到翻译单元里，但原文件得手动加宏包装。
- GCC `.incbin` 借助汇编器把任意二进制放进 `.rodata` 段，同时暴露 `_start` / `_end` 符号供 C 端 `extern` 取地址。
- `.incbin` 依赖内联汇编与 ELF 段指令，MSVC 不认；跨平台工程需另配方案。

## 链接到的概念

- [[c-cpp-embed-binary-blobs]]
- [[game-resource-pack-format]]
- [[offset-based-resource-blobs]]

## 原文

- 链接：<https://www.4rknova.com/blog/2013/01/27/cpp-embedded-files>
- 本地：`raw/articles/4rknova.com/2013-01-27_c-c-embedded-files.md`
