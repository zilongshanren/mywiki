---
tags: [source, metal, apple, metal-4, api, 显式资源管理]
date: 2026-04-19
sources: 1
---

# Getting Started with Metal 4（Warren Moore / Metal by Example）

[[warren-moore|Warren Moore]] 发表于 2025 年 7 月 8 日，WWDC25 之后 Metal 大版本 4 的基础适配指南——配 GitHub 上的 glTF PBR 迷你引擎样例。重点不是全覆盖，而是**从现有光栅管线迁移**所必须理解的 API 重塑：命令分配器、argument table、residency set、事件驱动同步。

## 摘要

Metal 4 的核心哲学从"fire-and-forget command buffer"转向 **concurrent by default + 显式资源生命期管理**。新类型统一带 `MTL4` 前缀。

**函数描述符必须了**。`MTL4LibraryFunctionDescriptor` 填 `name` + `library`，`MTL4SpecializedFunctionDescriptor` 包裹一层用 `MTLFunctionConstantValues` 注入编译期常量。

**`MTL4Compiler` 接管编译**。`device.makeCompiler(descriptor:)` 创建 compiler，`makeRenderPipelineState(descriptor:)` / `makeLibrary(descriptor:)` 挂在 compiler 上，不再挂 device。支持 pipeline serialization 缩短启动时间。

**Render pipeline descriptor 新写法**。`MTL4RenderPipelineDescriptor` 的 `vertexFunctionDescriptor` / `fragmentFunctionDescriptor` 吃 descriptor 不是 `MTLFunction`。color attachment 用 `MTL4RenderPipelineColorAttachmentDescriptor`，blend 相关属性从 bool 改 enum（`blendingState = .enabled`）。Metal 4 **render pipeline descriptor 不再带 depth attachment 描述**——pass descriptor 里再说。

**Residency set 是唯一路径**。Metal 4 之前 residency 是隐式的；现在必须显式 `device.makeResidencySet(descriptor:)`、`addAllocation(_:)` → `commit()` 才能让资源常驻。用 `MTL4CommandQueue.addResidencySet(_:)` 或 `MTL4CommandBuffer.useResidencySet(_:)` 挂载；"resident = 所有已挂载 residency set 的并集"。

**Argument table 成显式对象**。`MTL4ArgumentTableDescriptor` 指定 `maxBufferBindCount` / `maxTextureBindCount`，`device.makeArgumentTable(descriptor:)` 创建。绑定方式变了：

- texture：`argumentTable.setTexture(someTexture.gpuResourceID, index: 0)` —— 传 64-bit gpuResourceID
- buffer：`argumentTable.setAddress(someBuffer.gpuAddress, index: 0)` —— 传 gpu address；**带 offset 直接加到 address 上**（`gpuAddress + offset`）

索引仍然对应 MSL attribute（`[[buffer(n)]]` / `[[texture(n)]]`）。Argument table state 在 draw 间被**每次拷贝**，不需要池化或 sticky 管理。

**Command allocator 显式管理命令内存**。`device.makeCommandBuffer()`（不是 queue 上）→ `device.makeCommandAllocator()`。Command buffer 可以长寿，但 allocator **在 GPU 没执行完前不能复用**，所以要池化（常见 3 或 4 个轮用）。编码前 `allocator.reset()` 清上一轮命令内存，`commandBuffer.beginCommandBuffer(allocator:)` 建立关联。**Command buffer 不再隐式保活资源**——引用的 buffer / texture 必须外部保证在 GPU 用完前不被释放。

**Render command encoder 基本照旧**。新特性：

- color attachment mapping：pass 中途切换 render target
- 跨 command buffer 的 pass suspend / resume
- `MTKView.currentMTL4RenderPassDescriptor` 自动填好新风格 descriptor

**提交和呈现三步走**：

```swift
commandQueue.waitForDrawable(drawable)
commandQueue.commit([commandBuffer])
commandQueue.signalDrawable(drawable)
drawable.present()
```

**Events 替代 dispatch semaphore**。`MTLSharedEvent` 做 CPU-GPU 帧同步：`event.wait(untilSignaledValue: N-3)` 等三帧前的工作完、`commandQueue.signalEvent(event, value: N)` 推进。Uniform buffer / command allocator 这些需要帧回收的资源靠 event 守。

作者的总结：**Metal 4 把资源管理和并发显式化**，入门成本上升，但解锁了更细粒度的优化空间。Barriers / fences 这些更深的话题留给后续博客。

## 关键要点

- Metal 4 的哲学：concurrent by default + 显式资源生命期
- Function 必须先 descriptor 再编译，specialized function 走 wrap
- Compiler 从 device 独立出来，支持 pipeline serialization
- Render pipeline descriptor 不再带 depth attachment（移到 pass descriptor）
- Residency set 从 3.2 可选升级为 Metal 4 唯一 resident 标记方式
- Argument table 是显式对象；texture 绑 `gpuResourceID`、buffer 绑 `gpuAddress`（+offset 直接加）
- Command allocator 接管命令内存，必须池化按帧轮用
- Command buffer 不再隐式保活资源——应用层管生命期
- waitForDrawable → commit → signalDrawable → present 四步走
- MTLSharedEvent 替代 dispatch semaphore 做 N-frame-ago 同步
- Metal 4 保留 color attachment mapping、pass suspend/resume 等新能力

## 链接到的概念

- [[metal-4-api-redesign]]
- [[metal-decade-history]]
- [[metal-api-overview]]
- [[bindless-rendering]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/metal-4/
- 本地：`raw/articles/metalbyexample.com/2025-07-08_getting-started-with-metal-4.md`
