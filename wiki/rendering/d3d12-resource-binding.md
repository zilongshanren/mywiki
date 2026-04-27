---
tags: [渲染, directx12, 资源管理, 显式api]
date: 2026-04-14
sources: 1
---

# D3D12 资源绑定（Descriptor / Heap / State）

DirectX 12 相比 DirectX 11 最大的负担就是**资源绑定不再被驱动兜底**：应用必须自己管理描述符（descriptor）、描述符堆（heap）、资源状态（resource state）、上传堆（upload heap），以及它们在多线程、多命令列表之间的一致性。这条笔记基于 Jeremiah van Oosten 的 Learning DirectX 12 Lesson 3，把这一层框架的核心抽象梳理出来。

## 核心问题

- **描述符在哪儿？**RTV/DSV 只需要 CPU 可见；CBV/SRV/UAV/Sampler 在着色器里用时必须放进 **GPU 可见堆**。同类型的 GPU 堆在一条命令列表里**同时只能绑一个**，切换必须在两次 `Draw` / `Dispatch` 之间。
- **绑多少？**一帧里会用到多少个 descriptor 无法提前知道（尤其是 PBR 场景中动辄数十张贴图），又不能回收——GPU 还没执行完的 descriptor 不能复用。
- **资源状态怎么跟？**`ResourceBarrier` 需要 before/after 两个状态。多线程录制命令列表时，没有任何单线程变量能稳定地代表“当前状态”。
- **上传的数据放哪儿？**动态常量、粒子数据、UI 顶点每帧都在变，需要上传堆里的临时存储。

## Lesson 3 的四件套

| 类 | 解决的问题 |
|---|---|
| `UploadBuffer` | 每帧动态数据的上传堆分配器（[[linear-allocator]]） |
| `DescriptorAllocator` | CPU 可见描述符的分页分配（RTV/DSV 以及暂存的 CBV/SRV/UAV） |
| `DynamicDescriptorHeap` | 把 CPU 描述符一口气拷进 GPU 可见堆，在 `Draw` 之前调用 `SetDescriptorTable` |
| `ResourceStateTracker` | 跟踪每个 resource 的当前状态，最后一刻汇总 pending barriers |

核心思想是**把 D3D12 的显式性延后**：在录制命令列表阶段只 "stage" 状态和描述符，等到真正要提交 `Draw` / `Dispatch` 的那一刻再把 barrier、descriptor table、资源状态三者一次性对齐。这和 [[render-graph]] 是同一种推迟决策思路。

## 多线程的关键细节

`ResourceStateTracker` 会区分两层状态：

1. **局部状态**：本命令列表自己内部看到的 resource 状态；直接记录
2. **全局状态**：跨命令列表的"真身"，只有在命令列表真正 `ExecuteCommandLists` 那一刻才被提交

录制阶段遇到一次 transition，如果不知道 before 是什么（因为前面的命令列表可能还在别的线程上），就先**记一个 pending barrier**；在提交前再用全局状态回填 before。这样多线程录制不必互相等待也不必锁共享状态。

## 线性分配器的一次应用

`UploadBuffer` 是一个典型的 [[linear-allocator]]：按页（默认 2MB）分配，页内只推进 offset，页在命令列表执行完后整页回收。内部碎片来自对齐（常量缓冲 256B 对齐），外部碎片来自跨对齐的空洞。它的优点是 O(1) 分配，几乎没有开销；代价是不能 free 单个 block。

## 相关

- [[linear-allocator]]
- [[render-graph]]
- [[draw-call]]
- [[rendering-api-depth]]
- [[rendering-pipeline]]
- [[gpu-hazard-tracking]]
- [[gpu-fence-timeline-semaphore]]
- [[buffer-renaming]]

## Sources

- [[sources/3dgep-learning-directx12-lesson3]]
- [[sources/jasper-how-to-write-a-renderer]]
- [[sources/asawicki-dx12-root-signatures]]
- [[sources/asawicki-dx12-clearuav-behavior]]
