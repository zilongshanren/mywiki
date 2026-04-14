---
tags: [windows, gdi, bitmap, image-format, image-processing]
date: 2026-04-14
sources: 1
---

# Windows 位图：DIB、DDB 与 DIB Section

Windows 下的「位图」不是一个概念，而是一族互相纠缠的对象，名字还被三十年的文档层层覆盖过。`bitmap` 在 Windows GDI 里至少可以指 **DIB**、**DDB**、**DIB Section**、**HBITMAP** 以及磁盘上的 `.bmp` 文件。Sell 的这篇长文把这些术语一次理清，重点在于它们背后的**内存所有权**和**硬件依赖性**差异。

## `.bmp` 文件 vs DIB

磁盘上的 `.bmp` 文件由一个 14 字节文件头、一个 `BITMAPINFOHEADER`、一个可选 Color Table 和像素缓冲组成。**DIB（Device-Independent Bitmap）** 正是这个结构去掉最外层 14 字节文件头之后的内存版本——用 `BITMAPINFO` 结构（info header + color table）加一个裸像素数组表示。`BITMAPINFOHEADER` 有多个历史版本（`V4`、`V5` ……），里面编码了宽高、bpp、RLE 压缩与否等元数据。

DIB 是**跨设备的**：它描述了一张和具体显示硬件无关的位图，任何 GDI 设备都能把它贴出来。这也是为什么它叫 "Device-Independent"。

## DDB：设备的私货

**DDB（Device-Dependent Bitmap）**则相反——它直接住在某个具体设备（显示器、打印机、in-memory DC）里，格式由设备自己决定。GDI 本身也不保证知道某个 DDB 的内部布局；应用程序只能通过 `GetDIBits` 把 DDB 转成指定格式的 DIB 来读写像素。NT 4.0 之后的 DDB 分配在内核 paged pool 里，属于内核地址空间。

DDB 存在的理由是**性能**：过去硬件加速绘制时把位图以设备原生格式放在显存或驱动内存里可以免去格式转换。现在 GDI 层几乎都退化成了软件 fallback，DDB 的意义主要是历史包袱。

## DIB Section：用户和 GDI 都能写

**DIB Section** 是后来为了解决"DIB 只有用户空间能写、DDB 只有 GDI 能高效画"的矛盾而引入的中间物：它**本质上仍是一个 DIB**，但像素缓冲同时对应用程序和 GDI 可见可写。`CreateDIBSection` 返回一个 `HBITMAP` 和一个指向像素的裸指针——应用程序可以直接 memcpy，GDI 也可以把它 select 进 DC 去画。作为附加 feature，像素缓冲可以由一个内存映射文件（Windows 称为 section）支撑，但传 `NULL` 忽略即可。

三者的读写权限可以画成一张小表：

| 对象 | 用户可读写 | GDI 可读写 |
|---|---|---|
| DIB | 是 | 否 |
| DDB | 否 | 是 |
| DIB Section | 是 | 是 |

## HBITMAP：不透明的句柄

`HBITMAP` 是通过 `DECLARE_HANDLE` 定义的不透明句柄，用来同时指代 DDB 和 DIB Section，对调用方来说长得一样。真正底层是什么完全不透明——在 Windows NT 以后通常是一个指向内核 paged pool 里结构体的句柄。对跨平台实现可以看 Mono 的 [libgdiplus](https://github.com/mono/libgdiplus)：它用一个 `_Image` 结构来模拟 `HBITMAP`，里面有 `active_bitmap`、`cairo_format`、`surface` 等字段——其中 Cairo 相关字段是 Linux 特有的，Windows 下不存在，但 `active_bitmap` 的对应物大致就是内核那边的 DDB/DIBSection 元数据。

## Stock bitmap：GDI 的 NULL 位图

GDI 还保留了一个**唯一的全局 stock bitmap**：`GetStockObject(OBJ_BITMAP)` 返回它，一个 1x1 单色图，不能被释放（尝试释放会失败）。新建的 memory DC 默认就绑着它——起到**哨兵（sentinel）**的作用，等价于「没有选择任何位图」。知道这个事情能解释为什么刚 `CreateCompatibleDC` 出来的 DC 画东西什么都看不见：你画的是 1x1 的 stock 位图。

## 给跨平台工程的启示

Sell 的文章是一个典型的 **platform-specific API 考古学**样本：`BITMAPINFO / BITMAPINFOHEADER / BITMAP / DIBSECTION / HBITMAP / OBJ_BITMAP`，每一个名字对应一个历史阶段留下的抽象漏洞。跨平台代码回避 GDI 是合理的防御，但一旦必须和 Windows 原生位图打交道，就得认清 DIB 与 DDB 的所有权差异和 HBITMAP 的不透明性——不然就会写出"我明明 CreateCompatibleBitmap 了为什么画不出来"一类的 bug。

Color table / palette 主要对 4、8、16 bpp 位图有意义；1 bpp 有一个退化的二色 palette；24/32 bpp 根本不支持 color table。压缩（RLE）也只在磁盘 I/O 或 GDI+ 编解码层露面——中间内存形态几乎总是未压缩的。

## 相关

- [[x11-composite-redirection]] —— 对照阅读：X11 那边的"窗口像素到底住哪"问题
- [[linux-graphics-stack-dri]] —— 另一个历史包袱沉重的平台图形栈

## Sources

- [[sources/vertexfragment-demystifying-windows-bitmaps]]
