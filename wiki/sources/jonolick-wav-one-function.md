---
tags: [source, audio, single-file-library]
date: 2026-04-14
sources: 1
---

# WAV File Writer in One Function（Jon Olick, 2012）

[[jon-olick]] 2012 年 3 月的一则短贴，宣布发布一个"单函数"的 WAV 文件写入器。

## 摘要

Olick 延续其 STB 风格的极简美学：与其啃完 RIFF/WAV 规范的若干页细节，不如一个函数、一个 `.h` 头文件解决"把 PCM 数据落盘成 `.wav`"这个 99% 的使用场景。只支持 PCM 格式（不处理 DPCM、压缩编码，这些按需增添）。贴子里顺带提到同期在做一个同样风格的单文件 MPEG 写入器——后来确实在 2016 年发布。这条博客作为一条"声明"而非深度技术文章存在，真正的技术载体是代码仓库。

## 关键要点

- 单函数 API 思路与 [[sift-single-file-library]] 同源：复杂格式剥掉罕用分支，只保留实际开发里最高频的代码路径。
- 只支持 PCM，DPCM/其它格式留给需求驱动。
- 文章本体篇幅极短，重点在工程取向而非原理解释。

## 链接到的概念

- [[jon-olick]]
- [[sift-single-file-library]]

## 原文

- 链接：https://www.jonolick.com/home/wav-file-writer-in-one-function
- 本地：`raw/articles/jonolick.com/2012-03-12_wav-file-writer-in-one-function.md`
