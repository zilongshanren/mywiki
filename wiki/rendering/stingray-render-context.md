---
tags: [渲染, 多线程, command-buffer, sort-key, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray 的 RenderContext：draw call 的录制与调度

Walkthrough 系列第 3 篇的主角。`RenderContext` (RC) 是 [[stingray-renderer-three-stage-pipeline|三阶段架构]] 中 **Render 阶段的输出结构**——worker thread 把渲染对象的 `render()` 调用结果录进它，最终由 [[stingray-render-device-dispatch|RenderDevice::dispatch]] 翻译成真实 API 调用。

## 为什么 sort_key 与 package data 要分开两条 buffer

RC 内部维护两条并行结构：

- **Command 数组**（POD）：`{ uint64_t sort_key; void *head; uint32_t command_flags; }`。
- **RenderPackageStream**：变长 package 数据的块式内存池（fixed-size block pool，灵感来自 Christian Gyrling 在 GDC 2015 讲 Naughty Dog fiber 调度时用的 allocator）。

Tobias 给出四条理由说明**为什么不把 sort_key 直接嵌进 package header**：

1. package 体积大且变长，变长元素的数组不好排。
2. 块式内存池里 package 会跨 block，排序时要处理 "jump label" 额外麻烦。
3. 一个 package 被多个 Command 共享时（multi-pass shader 里），同一份 draw data 可以挂上多条 Command，各自带不同 sort_key。
4. `command_flags` 可以放 "这个 command 是哪种类型" 的 hint，`RenderDevice` 扫描时少一次 pointer chasing。

这种 "SoA + 变长数据侧车" 的模式和 [[stingray-render-resource-context|RRC]] 用一条 command buffer 压 package 是同一思路——[[stingray-renderer-three-stage-pipeline|三阶段架构]] 里每一层都重复这个 pattern。

## 三类命令

RC API 按语义切成三类：

- **State commands**——`begin_state_command(sort_key) ... end_state_command()` 包起来的批，里面发 `set_render_target` / `clear` / `set_viewports` / `push_marker` 等。这一批共享同一 sort_key，按录制顺序执行。
- **Rendering commands**——`render(RenderJobPackage*, shader_context, interleave_sort_key, shader_pass_branch_key, job_sort_depth, gpu_affinity_mask)`。返回拷贝到 `RenderPackageStream` 后的 `RenderJobPackage*`，允许调用方就地 patch（典型用法：renderable 保留一份**静态 prototype** RenderJobPackage，因为 worker 并行访问不能 mutate 原件，`render()` 返回 copy 供 patch view/lighting-specific 常量）。
- **Resource update commands**——`map_write(resource, sort_key, ...)` 返回一段写 buffer 的内存，RC 替换 GPU 侧该 resource 的内容。

注意所有入口都带 `sort_key` 和 `gpu_affinity_mask`——前者支持 [[stingray-sort-key-bit-layout|64-bit sort key 的分段位布局]]，后者支持显式多 GPU 分派（bit 1 = GPU_DEFAULT，bit 2/3/... = 次要 GPU）。

## RenderJobPackage：一条 draw call 的自包含描述

```cpp
struct RenderJobPackage {
    BatchInfo batch_info;     // primitive_type, vertex/index offset, instances, front_face
    ComputeInfo compute_info; // thread_count[3], async (走 compute queue)
    uint32_t size, n_resources;
    uint32_t resource_offset;         // 指向 VertexStream/IndexStream/VertexDeclaration handle 数组
    uint32_t shader_resource_data_offset; // 各 stage 的 handle + 非全局常量 buffer
    RenderResource::Handle shader;
    uint64_t instance_hash;   // instance merging 的 key
    // development 下还有 resource_tag / object_tag / batch_tag 三层 debug 标签
};
```

一个 package 必须 **自包含**——所有 handle、常量都嵌在 header 后的变长数据里。这样 RenderDevice 在 dispatch 时不需要回头问 engine 层。`instance_hash` 是 shader 作者可选实现的 "可 merge 条件"：通常是所有输入 `RenderResource::Handle` 的 hash，[[stingray-render-device-dispatch|RenderDevice 侧的 instance merger]] 利用它识别可合并 draw。

## render() 返回 patched copy 的理由

Renderable（mesh / particle）在 culling 完成前不知道自己会被哪个 view 画、用哪个 lighting——这些信息只在 `render()` 被调用时以 `ShaderTemplate::Context` 和常量的形式到来。由于多个 worker 可能同时进入同一个 renderable 的 `render()`，**不能写 prototype**。

方案本可以是 "栈上拷贝 prototype + patch + pipe 给 RC"，但 `RenderContext::render()` 反正要把 package 复制进 PackageStream，**干脆把复制合进接口、返回可写的 copy 指针**——零额外拷贝，完成 view-specific patch。

## fence、多 GPU、copy

新 API（DX12 / Vulkan）的 Graphics/Compute/Copy 三条 queue 需要同步，RC 暴露：

```cpp
void signal_fence(IdString32 name, sort_key, queue, gpu_mask);
void wait_fence(IdString32 name, sort_key, queue, gpu_mask);
void copy(dst, src, sort_key, src_box, dst_offsets, queue, gpu_mask, gpu_source, gpu_destination);
```

fence 也通过 sort_key 参与排序——和普通 draw 混在同一条 Command 数组里，sort 之后按位置插入到 API 调用流里。多 GPU 在 Stingray 里是**位掩码**级的一等公民，每个 command 都能决定走到哪张卡。

## 相关

- [[stingray-sort-key-bit-layout]] —— sort_key 的 64-bit 分段含义
- [[stingray-render-device-dispatch]] —— RC 最终如何翻成 API 调用
- [[stingray-render-resource-context]] —— 资源创建端的同 pattern 姊妹结构
- [[stingray-renderer-three-stage-pipeline]] —— 三阶段架构里 RC 的定位
- [[async-compute]]
- [[gpu-fence-timeline-semaphore]]

## Sources

- [[sources/bitsquid-renderer-walkthrough-3-6-canonical]]
