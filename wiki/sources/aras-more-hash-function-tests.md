---
tags: [source, 计算机系统, 哈希, 性能]
date: 2026-04-14
sources: 1
---

# More Hash Function Tests（Aras Pranckevičius / aras-p.info）

[[aras-pranckevicius]] 发表于 2016 年 8 月的非加密哈希函数横向评测续篇，在前一篇博客的基础上补充了更多算法和更多目标平台（macOS/Windows 64/32、iPhone SE、Xbox One、asm.js），给出覆盖小/中/大三种输入尺寸的吞吐表，并落到一份平台相关的选型结论。

## 摘要

作者用自建的 HashFunctionsTest 测试床把 xxHash32/64、CityHash32/64、mum-hash、FarmHash32/64、SpookyV2-64、Murmur2A/Murmur3 全家、SipHash、MD5/SHA1/CRC32、FNV-1a/djb2/SDBM 一起跑了一遍，分别统计「对齐/非对齐输入」和「大/中/小数据」下的 GB/s 吞吐。结论是 64 位系统默认用 CityHash64、32 位系统用 xxHash32；大数据块上 Intel 平台选 xxHash64、Apple 移动平台选 FarmHash64、主机（Xbox One AMD Jaguar）选 SpookyV2；短字符串（<20 字节）用 FNV-1a 足矣。文中还强调了几个常被忽略的陷阱：32 位编译目标里 64 位哈希会掉速一个量级；mum-hash 的速度优势只在 GCC 下存在；Murmur/Spooky 在 asm.js 下因非对齐读取直接产出错误结果；FarmHash 和 mum-hash 在不同编译器下会产生不同的哈希值（即「非一致」）。

## 关键要点

- **平台敏感度极高**：同一个哈希函数在 x86-64、ARM、PPC、asm.js 上的排名会完全换位，选型不能只看一张表。
- **32 位目标特别处理**：xxHash64 从 13 GB/s 掉到 1 GB/s；32 位目标必须换 32 位哈希函数。
- **大数据与小数据分治**：大数据看 SIMD 友好性（xxHash/City/Farm），小数据（<20 字节）看分支代价，FNV-1a 反而更快。
- **质量均匀**：除了 SDBM 在二进制结构体输入下碰撞略多，其他 32/64 位非加密哈希质量都「够用」。
- **哈希一致性问题**：FarmHash / mum-hash 在不同平台上输出不同哈希值，不能用于跨平台 checksum 场景。
- Murmur/Spooky 依赖非对齐读取，在 ARM 32 位和 asm.js 上需要手动 define 开关。

## 链接到的概念

- [[non-cryptographic-hash]]
- [[cpu-performance-formula]]
- [[cache-friendliness]]
- [[flynn-taxonomy]]

## 原文

- 链接：https://aras-p.info/blog/2016/08/09/More-Hash-Function-Tests/
- 本地：`raw/articles/aras-p.info/2016-08-09_more-hash-function-tests-aras-website.md`
