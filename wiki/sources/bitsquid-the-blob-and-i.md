---
tags: [source, bitsquid, 序列化, 数据导向, 资源管理]
date: 2026-04-19
sources: 1
---

# The Blob and I（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2010 年 2 月的文章，讲 Bitsquid 的资源序列化方案——放弃 `placement new + pointer patching`，改成 **offset only**。

## 摘要

经典 C++ blob 用特殊构造函数重建 vtable 和修补指针，智力上过瘾，但让整个 code base 变成"serialization-aware"，所有类都得知道怎么序列化自己，STL 容器也全部不能用。Bitsquid 转向 **data-centric**——资源只是 POD struct，资源里**不存 pointer 只存 offset**，读盘就是 `fread` 一整块，不需要任何 patching pass。评论里讨论了变长数组（header + trailing bytes）、对齐（交叉编译时按最严平台对齐）、字节序（cross-compiler 做 endian swap），以及跨资源引用（用资源名 hash 到 runtime 查 pointer，存在动态数据里）。

## 关键要点

- 放弃 vtable / pointer patching，换成 offset 加法；
- 读盘单次 `fread`，内存位置可自由搬、可拼接；
- runtime 数据是 **platform-specific**，由 Win32 cross-compiler 做字节序和对齐规范化；
- 动态数组：header 里放 count，数据紧随其后；
- 跨资源引用用 **hash(name)**，runtime 由 [[handle-based-resource-manager|资源管理器]] 解析；
- 多一次"offset + base"加法的开销在实测中**看不到**——真有感知说明你在 blob 里跳太多、那是真正的瓶颈。

## 链接到的概念

- [[offset-based-resource-blobs]]
- [[data-driven-architecture]]
- [[handle-based-resource-manager]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2010/02/blob-and-i.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2010-02-12_the-blob-and-i.md`
