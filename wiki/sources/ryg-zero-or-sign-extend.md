---
tags: [source, bit-twiddling, 二进制补码, c]
date: 2026-04-14
sources: 1
---

# Zero or sign extend（fgiesen / Fabian Giesen）

[[fabian-giesen]] 2024 年 10 月发表的 bit-twiddling 笔记：bit-packed 格式里常见的"窄位宽整数扩展到机器字宽、且可能是有符号或无符号"的问题，用补码定义本身推导出一个不依赖位移语义、也不需要分支的统一写法。

## 摘要

传统"左移到符号位再算术右移"的写法依赖 C 里多年未定的行为（左移进符号位的 UB、有符号右移的实现定义），C++20 才正式承认二进制补码。ryg 从补码定义切入：N 位补码只是把最高位的位值从 +2^(N-1) 翻为 -2^(N-1)、其它位不动。于是扩展就等价于"减去两倍的符号位贡献"，写成 `val - (val & sign_bit) * 2` —— 传入 `sign_bit == 0` 得无符号扩展、传入 `1 << (N-1)` 得有符号扩展，解码循环里的 if 被编码进常量。评论区 Harold Aptroot 给出更漂亮的等价式 `(val ^ sign_bit) - sign_bit`，通过 XOR 切换符号位再减回去，三种情况均可手验。整篇体现 ryg 一贯的风格：从 ISA / 语义定义出发，而不是从库函数出发。

## 关键要点

- 左移进符号位 + 算术右移的写法在 C 里有多年未定义行为历史
- 补码的符号扩展等价于"把 MSB 的位值从 +2^(N-1) 换成 -2^(N-1)"
- `val - (val & sign_bit) * 2` 统一处理有符号/无符号，解码循环不再需要 if
- `(val ^ sign_bit) - sign_bit` 是更紧凑的等价形式（Harold Aptroot）
- 写法对容器字宽零假设，可以在任意位宽场景复用

## 链接到的概念

- [[sign-extend-without-shift]]
- [[insert-zero-bit-in-middle]]

## 原文

- 链接：<https://fgiesen.wordpress.com/2024/10/23/zero-or-sign-extend/>
- 本地：`raw/articles/fgiesen.wordpress.com/2024-10-23_zero-or-sign-extend.md`
