---
tags: [渲染, 资源系统, 多线程, api抽象, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray 的 RenderResource 抽象与 RenderResourceContext

Tobias Persson "Stingray Renderer Walkthrough #2" 这篇把 Stingray 在 GPU 资源抽象上的设计讲清楚：一个 POD 句柄 + 一层 command-buffer 化的创建/销毁接口。目标很直白——**图形 API 代码只存在于一个地方，其他系统都用跨 API 通用的表示**。

## RenderResource：24 位 index + 8 位 type

一切跨 API 资源抽象最后都落到这个 POD struct：

```cpp
struct RenderResource {
    enum { TEXTURE, RENDER_TARGET, DEPENDENT_RENDER_TARGET, BACK_BUFFER_WRAPPER,
           CONSTANT_BUFFER, VERTEX_STREAM, INDEX_STREAM, RAW_BUFFER,
           BATCH_INFO, VERTEX_DECLARATION, SHADER,
           NOT_INITIALIZED = 0xFFFFFFFF };
    uint32_t render_resource_handle;
};
```

任何引擎层资源只要需要在 `RenderDevice` 里对应一块 GPU 实体，就继承这个 struct。32 位 handle 里高 8 位存 type 枚举，低 24 位是该 type 专属数组的 index。换句话说，`RenderDevice` 内部按 type 切出一组数组，handle 的低位就是 O(1) lookup 的 offset。

Stingray 支持的资源种类覆盖了"构建一条渲染管线需要的全部单元"：

- **Texture / RenderTarget / DependentRenderTarget / BackBufferWrapper** —— 纹理与可写纹理，`Dependent` 专门为跟 swap chain 一起 resize 的 RT 准备，`BackBufferWrapper` 是创建 swap chain 时引擎唯一自己造出来的那种 RT。
- **ShaderConstantBuffer** —— 面向显式更新 + 多 shader 共享，主要是"view-global"那类全局状态。
- **VertexStream / IndexStream / VertexDeclaration / RawBuffer** —— 顶点/索引 buffer + 顶点声明 + 允许 GPU-UAV 的线性 buffer。
- **Shader** —— 内部持有构造一个完整 PSO 所需的一切（shaders + render states + samplers）。

几乎所有 buffer 类资源都带一个 `validity` 字段：

- `STATIC`——不可变，DCC 里来的资产几乎都是这档；
- `UPDATABLE`——改动频率低于每帧一次（UI、post fx 几何）；
- `DYNAMIC`——每帧多次改（粒子）。

加上 "stride / size / 是否需要 UAV view / ..." 这些 metadata，RenderDevice 不需要反复问上层就能自己做出来具体 API 的原生对象。

## RenderResourceContext：线程安全靠拆实例

资源创建/销毁要线程安全，但把 `RenderResourceContext` (RRC) 本身做成 thread-safe 代价太大。他们的做法是**把线程安全下放到调用方**——RRC 单实例不可并发访问，但你可以同时开任意多个 RRC 实例，只要不同线程各自用各自的就好。

RRC 本质是一个小 helper，内部包一条 command buffer。你对它调的 `alloc(resource)` / `dealloc(resource)` 实际上是往 command buffer 里压一条变长 "package"，package 描述 "要创建这个资源需要的一切"（textures 的 layout、VB 的 size/stride、shader 的 blob 等）。

```cpp
class RenderResourceContext {
public:
    void alloc(RenderResource *resource);
    void dealloc(RenderResource *resource);
};
```

RRC 还能持有**平台专用 allocator**，允许直接从 GPU-mapped memory 申请——贴图和其他 immutable buffer 可以在支持的平台上直接 stream 到 GPU 内存，跳过 `RenderDevice` 内的任何中转拷贝。

## Dispatch：控制线程 vs 其他线程

用户录完 RRC 后要把它交出去。两条路径：

- **`RenderDevice::dispatch(n, rrc[], gpu_mask)`** —— 只能在渲染控制线程（controller thread for rendering）上调。`RenderDevice` 本身不是 thread-safe。
- **`RenderInterface::dispatch(...)`** —— 其他线程（worker、资源 streaming）走这条。`RenderInterface` 是向 renderer 派送数据的跨线程通道，细节单独讲（和 [[main-render-thread-state-reflection]] 里的 `_render_interface` 是同一种 thread-safe ring buffer 概念）。

把 allocate/deallocate 从 `RenderDevice/RenderInterface` 的接口里挪出来而不是直接暴露，带来的好处：

- **调度灵活**——可以决定什么时候真正在渲染线程里创建 GPU 原生对象。
- **不用保 RRC 的 thread-safety**——接口简单、心智负担小。
- **批量**——一个 RRC 里积攒几十次 allocate 可以一次 dispatch 过去。

## 评论区留下的悬念：handle 分配时机

评论里有人问了个很实在的问题：**`render_resource_handle` 什么时候被填好值**？

- 选项 A：dispatch 时才填——意味着 RRC dispatch 完成前，新资源不能被任何 `RenderContext` 里的 command 引用，限制并行度。
- 选项 B：创建 RRC 时给每种 type 切一段预留 index 范围——麻烦且浪费。

原文没直接回答。另一位读者给出"local handle + dispatch 时平移到全局"的方案：同一 RRC 内部用从 0 开始的本地 handle，allocate 时自增；dispatch 时 `RenderDevice` 把这些本地 handle 平移到全局空间（比如已有 10 张 texture，则 0/1/2 变成 11/12/13）。这样同一 RRC 内创建的资源可以互相引用而不用等 dispatch。

Stingray 到底是哪种路径作者没在这篇里揭晓，但这个提问本身很好地暴露了 command-buffer 化资源系统的一个本质问题：**handle 要么延迟绑定、要么本地命名空间 + 提交期映射**。

## 与其他 Stingray 子系统的关系
- [[stingray-renderer-three-stage-pipeline]] —— RRC 的 command buffer 化是三阶段架构的一致思路；
- [[main-render-thread-state-reflection]] —— 同一 pattern 的 simulation-state 版本；
- [[d3d12-resource-binding]] —— 对比现代 API 的 bindless 思路，Stingray 的 `render_resource_handle` 可以看作 CPU 侧 bindless 表的早期形态。
- [[stingray-render-context]] —— RC 是 RRC 的 draw-call 侧姊妹结构，复用 command-buffer 化 + sort_key 调度的同一 pattern

## Sources

- [[sources/bitsquid-renderer-walkthrough-2-resources]]
