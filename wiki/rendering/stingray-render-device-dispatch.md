---
tags: [渲染, api抽象, 多线程, command-buffer, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray RenderDevice：跨 API 后端与并行 dispatch

Walkthrough 系列第 5 篇。`RenderDevice` 是 Stingray 图形 API 抽象的**唯一出口**——D3D11 / D3D12 / OGL / Metal / GNM 各自实现一个子类。除了常规的初始化 / swap chain / 统计，这篇聚焦两个重载：

```cpp
virtual void dispatch(uint32_t n, RenderResourceContext **rrc, uint32_t gpu_mask) = 0;
virtual void dispatch(uint32_t n, RenderContext **rc,         uint32_t gpu_mask) = 0;
```

## 资源 dispatch：同步简单路径

[[stingray-render-resource-context|RRC]] dispatch 是同步的——这一刻没人读 `D3D12ResourceContext`，遍历 RRC 的 command buffer，逐条 alloc / dealloc。每个 `RenderDevice` 实现都维护一个类似这样的状态结构：

```cpp
struct D3D12ResourceContext {
    Array<D3D12VertexBuffer> vertex_buffers;
    Array<uint32_t>         unused_vertex_buffers; // 复用槽
    Array<D3D12IndexBuffer>  index_buffers;
    Array<uint32_t>         unused_index_buffers;
    // ...
    Array<uint32_t> resource_lut; // render_resource_handle → 局部 type 数组 index
};
```

`RenderResource::render_resource_handle` 高 8 位是 type，低 24 位通过 `resource_lut` 映射到该 type 的数组下标——这就是 RRC 里 24-bit handle 的去处。

## Context dispatch：并行翻 API 调用

RC dispatch 想 **go wide**——多 worker 并行把 Command 翻 API 调用。但 worker 们会**修改** RenderDevice 侧的 buffer（dynamic buffer 更新），这比资源 dispatch 麻烦。Stingray 的妥协：只允许 `DYNAMIC` buffer 异步更新，`UPDATABLE` buffer 在 kick worker 前**串行扫一遍**统一更新（作者坦承这不优雅，未来想统一处理）。每个 worker 有自己的 `ResourceAccessor` 副本跟踪 dynamic buffer 状态。

Shader 是资源管理里的例外——不是简单的 buffer，是一个包含多 pass 的 effect：

```cpp
struct ShaderPass {
    struct ShaderProgram {
        Array<uint8_t> bytecode;
        ConstantBufferBindInfo, ResourceBindInfo, SamplerBindInfo;
    };
    ShaderProgram vertex_shader, domain, hull, geometry, pixel, compute_shader;
    RenderStates render_states;
};
struct Shader {
    Vector<ShaderPass> passes;
    enum SortMode { IMMEDIATE, DEFERRED } sort_mode;
};
```

`Shader::sort_mode` 决定从 [[stingray-sort-key-bit-layout|sort_key]] 的 Pass Deferred 还是 Pass Immediate 区间解出当前 pass index。

## dispatch 的五个阶段

1. **Merge + Sort**：所有 RC 的 Commands 数组 concat 进 `prepare_command_list` 的 output buffer，跑 stable radix sort。output buffer 归 RenderDevice 所有以避免每帧分配。

2. **Instance Merging**：扫描 sort_key "instance bit 置位且高位相同" 的区间，为每个区间 fork worker 比对 `RenderJobPackage::instance_hash` 和 shader handle——两者相同即可合并。合并的做法：把**被 shader 作者 tag 为 instance-specific 的常量**从各 RenderJobPackage 的 constant buffer 里拽出来，塞进一个 dynamic `RawBuffer`，当 VS 输入。单次 draw call 就画掉整个区间。接口：

```cpp
namespace instance_merger {
    struct ProcessMergedCommandsResult {
        uint32_t n_instances, instanced_batches, instance_buffer_size;
    };
    ProcessMergedCommandsResult process_merged_commands(Merger&, RenderContext::Commands&);
}
```

Tobias 也承认这是老派做法——2017 年新 API + bindless 能更激进地做这件事。作者 argument：merger 独立于图形 API，按道理应该放 `RenderDevice` 之外。

3. **工作切分**：简单把 Commands 数量 ÷ worker 数，**不做 cost 模型**——假设 draw call 是主体，其他 command 视作不可避免的噪声。但强制每个 worker 至少处理 ~128 条避免碎片。

4. **State 扫描 + Execution Context 准备**：切完之后需要**串行扫一遍所有 Commands**，找 `set_render_target` 等 "big state change" 以及 `UPDATABLE` buffer 更新，同时跟踪 fence（DX12 下还要跟踪 resource barrier）。`Command::command_flags` 的 hint bit 让扫描不用 dereference `Command::head`，避免大量随机访问。每个 worker 还要创建 API 原生 command list（`ID3D12GraphicsCommandList`）。

5. **并行翻译**：worker 循环自己的 Command 区间，对每条 `RenderJobPackage`：
   - 按 pass index 查 shader pass → 绑定所有活跃 shader stage（带 MRU cache）
   - 查 render states block（Rasterizer / Depth Stencil / Blend）→ 绑定（MRU cache）
   - 遍历 `shader_resource_data_offset` 指向的 handle 数组，经 `D3D12ResourceAccessor` 解 handle → 绑资源到各 stage
   - 遍历 `resource_offset` 指向的 VB/IB/VertexDeclaration → input assembler
   - 绑 / 更新 constant buffer
   - 发 draw 或 dispatch

最后 command list 交给各自的 queue 执行。DX12 下 `ExecuteCommandList` 之间还要插 fence signal/wait。

## 为什么这个结构抗住了 2017 年的多 API 对立面

这个 dispatch 结构的精妙在于 **sort + instance merging 都发生在 "无 API" 阶段**——它们操作的是 sort_key 和 package 数据，和具体 API 无关。从第 4 步往后才进入 "真的要发 API 调用" 的阶段，而那一段已经完全可以按 API 并行。这也解释了为什么 Stingray 能相对平滑地从 D3D11 扩展到 D3D12/Vulkan/Metal——前面三阶段是共同的，后端只需要实现 "how to translate a Command into its API calls"。

## 相关

- [[stingray-render-context]] —— 输入数据结构
- [[stingray-sort-key-bit-layout]] —— sort 规则
- [[stingray-render-resource-context]] —— 资源 dispatch 路径
- [[stingray-render-interface]] —— 非渲染线程与 RenderDevice 之间的 thread-safe 中介
- [[d3d12-resource-binding]]
- [[bindless-rendering]]
- [[async-compute]]

## Sources

- [[sources/bitsquid-renderer-walkthrough-3-6-canonical]]
