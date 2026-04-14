---
tags: [source, computer-systems, windows, gdi, image-format]
date: 2026-04-14
sources: 1
---

# Demystifying Windows Bitmaps（Steven Sell / Vertex Fragment）

[[steven-sell]] 发表于 2019 年 7 月的长文，把 Windows GDI 下一团乱的"位图"族系——`.bmp`、DIB、DDB、DIB Section、HBITMAP、stock bitmap——一次梳理清楚。

## 摘要

长期避免使用 GDI(+) 的跨平台开发者被迫碰到它时往往会被一连串名字搞懵：`BITMAP`、`BITMAPINFO`、`BITMAPINFOHEADER`、`BITMAPV5HEADER`、`DIBSECTION`、`HBITMAP` ……本文按"内存所有权和硬件依赖性"两个维度把这一族对象分门别类。DIB 是 device-independent、由 `BITMAPINFO` + 像素缓冲构成，几乎等于去掉文件头的 `.bmp`；DDB 是 device-dependent，内部格式由硬件决定、GDI 也不保证能读懂；DIB Section 是让用户和 GDI 都能读写同一块像素缓冲的中间形态，可选支持 memory-mapped file。`HBITMAP` 是 `DECLARE_HANDLE` 的不透明句柄，实际上指向内核 paged pool。stock bitmap 是一个 1x1 单色的全局哨兵位图，不能释放，用于表示"DC 上还没选任何位图"。文章用一本老书 *Windows Graphics Programming: Win32 GDI and DirectDraw* 和 Mono `libgdiplus` 的源码做对照佐证。

## 关键要点

- **DIB / DDB / DIB Section** 三者的核心区分是**读写权限和像素存放位置**——DIB 在进程内存、DDB 在内核 paged pool 或设备内存、DIB Section 两头都能访问。
- `BITMAPINFO` = `BITMAPINFOHEADER` + 可选的 Color Table；`BITMAPINFOHEADER` 有历史版本 V1/V4/V5。
- `CreateDIBSection` 返回 `HBITMAP`，与 DDB 共享句柄类型——对调用方不透明。
- `GetDIBits` 是从 DDB 抽像素的唯一规范接口，可以要求以指定 bpp / 平面 / 压缩方式返回。
- **stock bitmap** 是一个 1x1 单色的全局单例，`GetStockObject(OBJ_BITMAP)` 取得；新建 memory DC 默认绑它，可以当作"NULL 位图"理解。
- Color table 只对 4/8/16 bpp 有意义，1 bpp 用退化二色 palette，24/32 bpp 不支持。
- 压缩（RLE）只在 GDI+ 编解码器内部出现，中间内存形态几乎总是未压缩。
- `libgdiplus`（Mono，Linux 上 .NET Core 3 用）提供了一份近似的 `_Image` 结构作为 `HBITMAP` 对照实现，可以借它窥探 GDI 内部可能的布局。

## 链接到的概念

- [[windows-bmp-format]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/demystifying-windows-bitmaps/
- 本地：`raw/articles/vertexfragment.com/2019-07-31_demystifying-windows-bitmaps.md`
