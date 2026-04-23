---
tags: [渲染, metal, apple, 显式api, pipeline]
date: 2026-04-19
sources: 1
---

# MTLRenderPipelineState：被显式锁定的完整管线

`MTLRenderPipelineState` 是 Metal 把 [[opengl-hardware-impedance-mismatch|OpenGL 的隐式 state combination cache]] 翻译成「一个可以提前创建并长期持有的 immutable 对象」的结果。**所有 GL 时代驱动偷偷合成、偷偷缓存的 shader 前置 / 后置代码都被打进同一个对象**，换来一次固定的创建成本和之后每次 draw 的可预测开销。

## PSO 包住了什么

`MTLRenderPipelineDescriptor` → 构建出一个 `MTLRenderPipelineState`，里面涵盖：

- **Vertex function** 与 **fragment function**。
- **Vertex format**——GL 里由 `glVertexAttribPointer` 描述、但[真正属于 shader 前置片段](../rendering/opengl-hardware-impedance-mismatch.md) 的一半。Metal 直接承认它属于 shader，一并锁在 PSO 里。
- **Rasterization 的 antialiasing 参数**。
- **Color attachment descriptor** 里的**写 mask + blending**——Metal 明确地把 blending 也放进 shader 后置代码 / framebuffer 合入阶段。

## PowerVR 为什么非这么建模不可

Ben Supnik 在 *Understanding PowerVR GPUs via Metal* 里指出：PowerVR（以及 Apple Silicon）是 [[tbdr-vs-imr|TBDR]] 架构，**blending 发生在片上 tile memory 里的 shader 里**（不是桌面那种固定功能 ROP）。这就意味着：

- 改变 color write mask / blend func = 需要一个新的融合着色器后缀，即**一个不同的 PSO**。
- 改变 vertex format = 需要新的 VS 前置片段，**又一个不同的 PSO**。
- 改变 VBO base pointer（但 layout 不变）= **不需要**新的 PSO（数据位置不是 shader 代码的一部分）。

**GL 等价物是：**每次你「假装」只改了 blend mode，驱动都要去 cache 里看有没有这份 combination；没有就现场 patch 并缓存。PSO 把这个动作**搬到创建期一次完成**，draw 时 `setRenderPipelineState:` 就是一次 object 切换。

## 应用侧的行为变化

- **一次 shader × 一套状态 = 一个 PSO** 是稳妥策略。X-Plane 的做法是把 blending 状态**永远绑在 shader 上**，原来的 shader 集合和 PSO 集合自然 1:1，迁移成本低（Ben 原话）。
- 反过来，如果旧代码依赖「一个 shader + 运行时改 blend 让它走多条路径」，迁移到 Metal 时 PSO 数量会**爆炸**，每个 shader × 每套 blend / write mask / vertex layout = 一个新对象。
- PSO 创建在 Apple GPU 上意味着**真的跑 compile / link**，不是免费的；要放到 app 启动 / 关卡加载期，热路径上只做 bind。

## 与 GL VAO、ARB_vertex_attrib_binding 的对比

- **VAO** 试图把 vertex format + base pointer 一起打包，但两半耦合度不同（见 [[opengl-hardware-impedance-mismatch]]）——失败。
- **ARB_vertex_attrib_binding** 把它们拆开——但仍然不涵盖 fragment 输出 / blending，combination cache 仍然存在。
- **PSO** 一步到位：**所有会生成 shader 前置/后置代码的状态**都被锁进同一个对象，combination 在创建期解决，runtime 无 hidden cache 查询。

## 相关
- [[metal-api-overview]]
- [[metal-3d-rendering-pipeline]]
- [[hsr-tbdr]]
- [[tbdr-vs-imr]]
- [[opengl-hardware-impedance-mismatch]]
- [[opengl-state-change-deferral]]
- [[mtl-render-pass-descriptor]]
- [[vulkan-explicit-performance]]

## Sources
- [[sources/supnik-powervr-via-metal]]
