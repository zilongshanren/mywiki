---
tags: [引擎架构, 多线程, stingray, bitsquid, data-oriented]
date: 2026-04-19
sources: 1
---

# State Reflection：主线程到渲染线程的单向状态镜像

Andreas Asplund 2016 年写的这篇 Stingray 引擎博客里，把**主线程和渲染线程之间如何同步对象状态**讲得非常细致。这是 Stingray 能稳定跑 [[stingray-renderer-three-stage-pipeline|三阶段渲染管线]] 的底层基石——整个引擎其他子系统也在反复复用同一个 pattern。

## 两条 controller thread + pipelined 一帧

Stingray 有两条"控制线程"：主线程跑 simulation（帧 `N`），渲染线程跑上一帧的渲染（帧 `N-1`），它们再把重活塞给 job system 上的 worker。主线程永远不会比渲染线程领先超过 1 帧——主 loop 末尾会 `wait_for_fence(_frame_fence)` 卡住。

这样设计的结果：**两个线程几乎不共享状态**，各自持有独立的对象表示。`MeshObject` 是主线程的 mesh（VB / material / texture / shader / skinning），`RenderMeshObject` 是渲染线程的对应物，约定俗成地给渲染侧加 `Render` 前缀。所有跨线程对象都继承两个空 struct：

```cpp
struct RenderStateObject { uint32_t render_handle; StateReflection *state_reflection; };
struct RenderObject       { uint32_t type; };
```

主线程对象只记"我对应渲染侧的哪个 handle，以及向哪条 state stream 写改动"；渲染线程对象只记自己的 type 枚举。

## 主线程把"改动"写进 StateStream

核心想法是：**主线程不直接改渲染数据，而是把"要发生的变更"序列化成一段字节流**。每个 world 有一个 `WorldRenderInterface`，里面装着一条 `StateStream`（buffer + capacity + size）。无论是 `create_object`、`set_flags`，还是任何 state 改动，都走 `alloc_message<T>()` 在 stream 上拼出

```
+--------+-------------------+
| Header | ObjectManagementPackage / SetVisibilityPackage / ... |
+--------+-------------------+
```

`MessageHeader` 固定含 `type / size / data_offset`，`data` 段是具体 payload。一帧下来，stream 上 packed 出一串 header+data 的连续字节。这是典型的 [[vector-field-bytecode-vm|bytecode/command buffer 风格]]——主线程完全不知道渲染侧会怎么执行，只负责记录意图。

## 帧末把 stream 递给渲染线程

主 loop 里 `_render_interface->update_world(world)` 的实际动作：

1. 打包一条 `UpdateWorldMsg`，把当前 `state_stream` 塞进去；
2. 给 world 换一条新 `state_stream`（从对象池拿）——因为后续同一帧内新建的 object 拿到的 `WorldRenderInterface` 会写新 stream；
3. 通过线程安全的 ring buffer 把 msg 发给渲染线程。

`_render_interface` 名字里的 "interface" 不是 OOP 接口，而是**线程间通信通道**——它是一条 thread-safe ring buffer，任何线程（包括资源加载线程）都能往渲染线程发 message。

## 渲染线程消费 stream

渲染线程在一条 `render_thread_entry` 的 while 里阻塞读 message。拿到 `UPDATE_WORLD` 后调用 `render_world->update(state_stream)`：扫一遍 stream，按 `package_header->object_type` 分派到 `RenderWorld` 里的 `_object_lut[render_handle] → object_index → _objects[object_index]`，转型成 `RenderMeshObject*` 之类，再按 `message_header->type` 分派给对象的 update。

用完的 stream 回到池子——stream 本身也是 recycled resource，和 `render_handle` 的 free list 是同一种哲学。

## 为什么要 render_handle + lookup table？

评论区问了个合理问题：为什么不直接把 `RenderStateObject*` 塞给渲染线程，绕开 `_object_lut`？作者的隐含答案是：

- **handle 可以被复用**——free list 机制保证创建/销毁频繁的对象不会无限增长 handle；
- **渲染侧 `_objects` 数组可以重排**（比如按类型聚合、按距离排序），handle → index 间接层让外部引用不受重排影响；
- **handle 跨线程比指针跨线程更安全**——渲染线程可以在内部挪动、销毁对象而不怕主线程持有的 handle 悬空。

## 同步机制：fence = Windows Event

末尾 `wait_for_fence(_frame_fence)` 的实现是线程间事件。Windows 上就是 `CreateEvent` / `SetEvent` / `WaitForSingleObject`，这些 Event 从池子里取。create_fence 往渲染线程发条消息，渲染线程消费到后 `SetEvent`，主线程阻塞在 `WaitForSingleObject` 直到被唤醒。

## 这套 pattern 的扩散面

- 资源加载线程用同一 `_render_interface` 把资源交给渲染线程；
- [[stingray-simd-sphere-oobb-culling]] 从 `RenderWorld` 的 `_objects` 数组读数据，culling 的 `ObjectSet` SoA 就是在 `create_object` 的 message 处理里顺带填入的；
- [[stingray-render-resource-context]] 的 RRC 同样是"主线程 allocate，渲染线程 dispatch"的 command buffer pattern，只是作用对象是 GPU 资源。

总的 pattern：**跨线程共享 = 消息流 + 双缓冲 + handle 间接表**。主线程写不 mutate，渲染线程在自己的"世界快照"里随便转。和 [[state-reflection-game-networking|网络同步里的 state reflection]] 不同，这里是 intra-process 的——但设计思路几乎一模一样：把"状态变更"显式物化成数据。

## Sources

- [[sources/bitsquid-state-reflection]]
