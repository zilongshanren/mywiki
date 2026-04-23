---
tags: [source, bitsquid, debugging, tooling]
date: 2026-04-19
sources: 1
---

# An idea for better watch windows（Niklas Frykholm / Bitsquid）

[[niklas-frykholm]] 2011 年 8 月的博文，吐槽 IDE watch window 的局限，提出把「变量观察」拆成独立跨平台外部程序的设想。

## 摘要

Visual Studio 的 watch window 是目前最强的，但对自定义容器、紧凑 blob 资源、大数组里找 NaN、hash 反查这类场景仍然无力。`autoexp.dat` 和 VS 扩展能补一点但维护成本高，且只绑死一个平台。Frykholm 建议：既然 watcher 有整个进程内存可读且不受性能约束，就该把它写成独立外部工具——前端只发 `(address, size)` 查询，后端适配本地进程、远程设备（PS3/Xbox）、甚至文件。难点是要设计一种能描述变长 blob、字节序、对齐、嵌入 length 等结构的 DSL，外加扩展点支持 hash 反查这类需要外部索引的查询。

## 关键要点

- 三个典型痛点：自定义容器难展开；blob 资源格式 C struct 描述不了；大数组 NaN / string hash 反查没办法。
- 把 watcher 和 debugger 解耦，前端-后端两分，天然跨 IDE/平台。
- 适用于内存和文件两种场景——对 blob 资源磁盘格式 = 内存格式的设计特别适合。
- 缺一套「紧凑 blob 描述语言」+ 扩展钩子。
- 评论区补充：010 Editor 已支持连接进程；可以用类似 Unix `file` magic 的启发式猜类型。

## 链接到的概念

- [[external-data-inspector]]
- [[offset-based-resource-blobs]]
- [[bitsquid-static-hash-values]]

## 原文

- 链接：https://bitsquid.blogspot.com/2011/08/idea-for-better-watch-windows.html
- 本地：`raw/articles/bitsquid.blogspot.com/2011-08-24_an-idea-for-better-watch-windows.md`
