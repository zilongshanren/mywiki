---
tags: [debugging, tooling, memory-inspection, cross-platform]
date: 2026-04-19
sources: 1
---

# 外部数据检查器（跨平台 watch window 设想）

[[niklas-frykholm]] 在 2011 年提出的一个设想：与其给每个 IDE、每个平台分别写 `autoexp.dat`、Visual Studio 扩展、VS 插件，不如把「变量观察」拆成一个独立的外部程序。

## 核心痛点

IDE 自带的 watch window 有几个老毛病：

- 自定义容器（`MyTree`、`MyHashSet`、`MyLinkedList`）展开困难，必须手动 cast 指针或看 Memory view；
- 紧凑 blob 资源格式（参考 [[offset-based-resource-blobs]]、[[bitsquid-the-blob-and-i]]）只是 header + offset 数组，C struct 描述不了；
- 数组里 10000 个 float 找一个 `#NaN` 只能手动滚；
- 看到一个 hash 值没法反查原字符串（参考 [[bitsquid-static-hash-values]]）。

`autoexp.dat` 能局部缓解但维护痛苦，而且只解决 Windows，跨不到 PS3/Xbox。

## 设想的结构

把数据检查器写成独立的外部程序，前端送 `(address, size)` 请求，后端回数据。后端可切换：本地进程 / 远程设备 / 直接读文件。这样：

- 平台中立，只要能访问目标内存就能接；
- 文件模式下可以当「加强版 hex 编辑器」——对 blob 资源格式尤其友好，因为磁盘格式和内存格式一致；
- 扩展机制可以插入自定义解析，比如 hash 反查、spell check、NaN 高亮等。

难点是描述数据结构：普通 C struct 不够用，需要一种能描述变长对象、对齐填充、平台字节序、嵌入数组长度等的 DSL。文章给出的伪代码：

```
struct Data {
    zero_terminated char[] name;
    pad_to_4_bytes_alignment;
    platform_endian unsigned count;
    Entry entries[count];
};
```

本质上是「一种能被解析器消费的紧凑 blob 描述语言」。这个想法和后来的 ImHex、010 Editor、Ghidra 的类型系统思路相同，但 Frykholm 写这篇时只是概念草图。评论里有人提到 010 Editor 已经能连到进程。

## 相关

- [[offset-based-resource-blobs]]
- [[bitsquid-static-hash-values]]
- [[handle-based-resource-manager]]

## Sources

- [[sources/bitsquid-better-watch-windows]]
