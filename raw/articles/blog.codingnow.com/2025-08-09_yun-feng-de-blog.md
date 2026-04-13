---
title: 云风的 BLOG
url: https://blog.codingnow.com/cat2/windows/
published: '2025-08-09'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

最近帮多个活跃的开源项目改了同一个 bug : 完善 Windows 下的 Unicode 支持。

问题源于 Windows 和其它平台不同，它有悠久的历史包袱。和现代大多数操作系统对 Unicode 支持的共识不同，它的 API 不是基于 UTF-8 而是基于 UTF-16 的，且还遗留了一套过去对 ANSI 支持的兼容 API 。

最近我接触的几个活跃开源项目，都是西方人主导开发的，他们维护者似乎对 UTF-16 均有所误解，或是懒得做全面的支持。我认为罪魁祸首就是微软自己把 ANSI 编码称为 MBCS 多字符编码字符集，和 WideChar 宽字符集对应起来，暗示 WideChar 是单字编码。而事实上 UTF-16 方案应该成为 MWCS 才合理。

Unicode 虽然常用的只有 BMP ，也就是 U+0000 到 U+FFFF 部分的字符集。但是随着 Emoji 的普及，SMP 也变得非常常见了。其实 Unicode 目前的标准有 17 的 Plane ，需要 21bit 才能表示完全。而很多人直观的觉得，UTF-16 每一个字 ( 2 字节 ）表示一个码点。这是不对的，像 Emoji ，一些罕见汉字（SIP）需要用两个字来表示。这个叫做 surrogate pair ，对于 Unicode ，U+D800 到 U+DFFF 这个区段是不存在的，专门用于实现 UTF-16 中的 surrogate pair 。