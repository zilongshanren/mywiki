---
tags: [source, OpenGL, C, 可移植性]
date: 2026-04-19
sources: 1
---

# glXGetProcAddressARB Syntax（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2010 年 2 月的一则小帖子，解读 GLX extension loader 的古怪 C 签名。

## 摘要

Supnik 吐槽 GLX 的 loader 签名写得像 puzzle，但其实只是一个普通函数：返回 `void (*)()`——一个无参无返回值的函数指针。与 WGL、AGL 把返回值定义为 `void *` 不同，GLX 走的是**函数指针类型**。Supnik 觉得没必要。评论区有读者给出了标准层的答复：**C 标准只保证 `void *` 能无损承载数据指针，不保证覆盖函数指针**。历史上确实存在 code 和 data 指针位宽不同的架构（哈佛架构、早期 DSP、9-bit-byte 机器），把函数指针塞进较窄的 `void *` 会截断高位。OpenGL ARB 要让规范覆盖所有架构，所以用函数指针类型是「ultra portable」的正确做法；POSIX 的 `dlsym` 用 `void *` 是违标但在 flat-memory 平台上将就用。

## 关键要点

- GLX 的 `glXGetProcAddressARB` 返回 `void (*)()`，不是 `void *`。
- 跨平台 loader 需要在 GLX 分支上额外 cast。
- C 标准保证任意数据指针与 `void *` 互转无损；**不覆盖函数指针**。
- 函数指针之间 cast 永远合法；函数指针与数据指针互转是 UB。
- 这个限制在哈佛架构等 code ≠ data 地址空间的机器上真实存在。

## 链接到的概念

- [[function-vs-data-pointer-portability]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/02/glxgetprocaddressarb-syntax.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-02-08_glxgetprocaddressarb-syntax.md`
