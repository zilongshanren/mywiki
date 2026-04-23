---
tags: [source, 引擎架构, 多线程, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# State Reflection（Andreas Asplund / bitsquid 博客）

[[andreas-asplund]] 发表于 2016-09-07 的博客，把 Stingray 主线程到渲染线程的**状态镜像机制**整条链路贴出来，包括数据结构、主循环、渲染线程消费逻辑。

## 摘要

Stingray 有两条 controller thread：主线程跑 simulation（帧 N），渲染线程处理上一帧（N-1），剩下交给 worker。两个线程几乎不共享状态，每个跨线程对象都持有两份表示（`MeshObject` 主线程、`RenderMeshObject` 渲染线程）。主线程改动被序列化进 `StateStream`——一条 `buffer + size + capacity` 的变长 command buffer，每条 message 是 `MessageHeader + payload`。

主 loop 末尾 `_render_interface->update_world(world)` 把当前 stream 塞进 `UpdateWorldMsg` 发给渲染线程，同时给 world 换一条新 stream，`state_reflection` 指针统一，所以新建对象自动写新 stream。渲染线程在 while 里阻塞读 message，`RenderWorld::update` 扫 stream 按 `package_header->object_type` + `message_header->type` 双层分派，通过 `_object_lut[render_handle] → object_index → _objects[]` 找到对象调 update。

跨帧同步用 fence（Windows Event 的薄包装），`wait_for_fence` 保证主线程永不领先渲染线程超过 1 帧。评论区作者也解释了 `_render_interface` 的本质——一条线程安全 ring buffer，所有向渲染线程发的 message 都走这里（包括资源 streaming 线程）。

## 关键要点

- `StateStream` = 内存 buffer + bump allocator，`alloc_message<T>()` 泛型出 `MessageHeader + T` 的紧凑布局。
- `render_handle` 是 recycled ID（free list 管理），和 `object_index` 之间靠 `_object_lut` 间接——渲染侧可以重排 `_objects` 而不影响外部引用。
- 对象创建、`set_flags` 之类 state 改动用同一条 pattern：都是往 state_stream 里拼 header + package。
- 两线程同步靠 `create_fence` / `wait_for_fence`（底层是 `CreateEvent` + `SetEvent` + `WaitForSingleObject` 加 Event 池）。
- 评论原博的 typo 作者已修正：原句把两条继承关系都写成 render thread，应是"main thread objects inherit from `RenderStateObject`"。

## 链接到的概念

- [[main-render-thread-state-reflection]]
- [[stingray-renderer-three-stage-pipeline]]
- [[stingray-simd-sphere-oobb-culling]]
- [[stingray-render-resource-context]]

## 原文

- 链接：https://bitsquid.blogspot.com/2016/09/state-reflection.html
- 本地：`raw/articles/bitsquid.blogspot.com/2016-09-07_state-reflection.md`
