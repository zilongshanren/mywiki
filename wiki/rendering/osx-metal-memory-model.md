---
tags: [渲染, metal, apple, 内存模型, 显式api]
date: 2026-04-19
sources: 1
---

# OS X Metal 的内存模型（Shared / Managed / Private / Auto）

Metal 从 iOS 到 2015 年 OS X 时新增的核心问题是：**桌面 GPU 是分立的**，CPU 和 GPU 有各自的内存池，Unified Memory 的假设不再成立。Apple 的选择是**提供四档 `MTLResourceOptions`**，暴露一组「常见用例」而不是 Mantle 那套「自己切内存池」的玩法。Ben Supnik 2015-06 WWDC 笔记里记下了各档的语义。

## 四档存储

- **Shared**——一份数据在 AGP 内存里，**CPU / GPU 都直接访问**。对应 GL 里的 streaming / dynamic。一致性**在 command buffer 边界**，不是连续同步——因此**不依赖 map-coherent**，推测 overhead 比 GLES 下等价路径低。是小块常变数据（UI 顶点、per-frame uniform）的默认选择。
- **Managed**——**CPU 一份 + GPU 一份**，显式同步。CPU 改完调 `didModifyRange:`flush 下去；GPU 改完要调 blit encoder 上的 `synchronizeResource:` 同步回来，**而且是排队的**。这是 OS X 静态几何的默认形式。共享内存的设备（Intel 集显）自动退化到 Shared。
- **Private**——**只在 GPU 侧**（可能是 VRAM）。好处是格式可以用 GPU 最快的 tiled / swizzled layout；唯一访问通道是 **blit command encoder**。framebuffer、render target、大型只读贴图都应走这档。
- **Auto**——**跨平台 meta 选项**——iOS 上变 Shared（iOS 没有 Managed），OS X 上变 Managed。Ben 对此有疑问：**桌面 app 多数 mesh 也应该是 Managed**，但至少 auto 让跨平台纹理代码少写一套。

## Mantle 对比：省掉 pool、省掉 reference 声明

Ben 的两条比较：

- **Mantle**让你从驱动要内存池，自己把资源塞进去，支持你实现 pool allocator。**Metal 不暴露池**——你创建资源就行，不知道 VRAM 还有多少，也不能自管分页。驱动自己 LRU / page out。
- **Mantle** 要求你**显式声明一个 command queue 能引用哪些资源**，以保证驱动在 GPU 跑时不会 evict 它们。**Metal 不需要这步**——简化了写法。
- **Mantle** 暴露**多条并行 queue**（现代 GCN2 上有独立 DMA queue），你得自己同步。**Metal 不暴露**——Ben 推测驱动内部**可能把 blit buffer offload 到 DMA queue，必要时在 render encoder 前插 wait** 来处理 blit 不及时完成的少数 case。

## 唯一一个「直通 VM」的例外

虽然没有池，Metal 允许**直接从一个 VM page 创建 buffer**（`newBufferWithBytesNoCopy:length:options:deallocator:`），省去一次 memcpy。这不等于 Mantle 的池语义，但在把已经分配好的 CPU 数组（比如 mmap 的文件）交给 GPU 时有用。

## 设计哲学上的判断

Ben 自己作为要写这些代码的人**明确偏好 Metal 的简化模型**——Mantle 那套 state / queue / reference 管理「naively 看要么复杂难懂要么次优」。他也承认**这未必是最优权衡**——Apple 的性能对比基准是 GL，不是 Mantle；想知道「driver 管资源一致性」到底丢了多少性能，得拿 Mantle 做对照。**AAA 游戏开发者**习惯于主机上的池分配模型，应当会对缺失 pool 抽象感到别扭。

## 与桌面 GPU feature gap

2015 年 Metal 带 desktop 时缺的功能：**transform feedback、geometry shader、tessellation**。Ben 在评论里提出一个当时算新颖的做法：把 **compute shader** 当做 transform feedback 的 drop-in 替代品（compute 写私有 buffer，graphics pipeline 再读这个 buffer）。现在看这条路径成了所有现代 API 的主流。

## 相关
- [[metal-api-overview]]
- [[metal-3d-rendering-pipeline]]
- [[mtl-render-pipeline-state]]
- [[mtl-render-pass-descriptor]]
- [[d3d12-resource-binding]]
- [[d3d12-resource-alignment]]
- [[vulkan-explicit-performance]]
- [[agp-vs-vram-streaming]]

## Sources
- [[sources/supnik-osx-metal-notes]]
