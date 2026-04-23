---
tags: [渲染, opengl, 驱动, 同步, vbo, ubo]
date: 2026-04-19
sources: 1
---

# glMapBuffer 在多线程驱动下的隐式停顿

2010 年 [[ben-supnik|Supnik]] 的口径是：要流式更新 VBO，要么 orphan 要么 unsynchronized map buffer range，千万别 `glBufferSubData`——它"不可能比 map 更快"。2015 年这位自己写了反转：在 Windows NVIDIA/AMD/Intel 的现代驱动上，`glBufferSubData` 不但不输 map，**绑定 UBO 流式更新时甚至显著更快**。变量是什么？**驱动被搬到了另一个线程**。

## 多线程驱动下 map 为什么变贵

现代桌面 GL 驱动不是同步库——你的 `gl*` 调用只是把命令塞进 FIFO，真正干活的是一条驱动线程。这样 CPU app 线程和命令编译/提交能并行。但 `glMapBuffer` 必须**返回一个真实指针给你**，这下 app 线程没办法不等：

- **实际发生**（NVIDIA 的内部幻灯片确认）：app 线程阻塞，直到驱动线程跑到这条 map，才算出指针返回。相当于把两线程重新同步到一条串行时间轴上。
- **理论最佳**：驱动返回一块 scratch 给你写，回头再拷进真 VBO。可 API 没给出这种语义保证，而且对 AGP 映射的 VBO 来说"拿到 scratch 再 copy 回去"失去了 zero-copy 的意义。

结论：在多线程驱动下，`glMapBuffer` 是**隐式同步点**。流式 VBO / UBO 走这条路每次都吃一次跨线程往返。

## 为什么 `glBufferSubData` 反而能走 fast path

`glBufferSubData` 的 API 是**单向的**：输入参数进去，没有指针出来。这意味着整条调用可以像其他 draw 命令一样 marshal 成一条"待执行"命令进 FIFO——app 线程立即返回，驱动线程晚点再跑：

```c
// driver 线程执行时：
if (offset == 0 && size == size_of_current_vbo) {
    glBufferData(target, size, NULL, usage);  // 隐式 orphan
}
void* p = glMapBuffer(target, GL_WRITE_ONLY);
memcpy(p, marshalled_data, size);
glUnmapBuffer(target);
```

两个关键点：**全量替换时自动 orphan**（等价于 app 显式 orphan），**map 留在驱动线程内部**（对 app 透明，不再同步）。代价是 "marshal 一次 + driver 侧再 memcpy 一次" 两次内存拷贝——小数据无所谓，大几何就不划算了。

业内把这种 SubData 更新叫做 **in-band update**：要么驱动排一条 DMA 把数据在 command stream 里按时间顺序灌进去，要么 driver 做资源 renaming（参见 [[buffer-renaming]]）给每次调用换块内存。两种实现方式对 app 等价。

## 哪条路线适合哪种数据

Supnik 在 X-Plane 2015 年的测试结论：

- **流式 UBO（每次 draw call 小量更新）**：`glBufferSubData` ≈ 或略快于 loose uniforms，远快于 `glMapBuffer`。UBO 更新速度是 draw call rate 的实际瓶颈（排除换 shader 这种粗糙错误后）。
- **聚合式 UBO（一次写好 N 个 draw call 的参数）**：显著优于 per-draw 更新，但要求 app 做二次规划或把 GL 调用排队后统一提交。
- **放 attribute 代替 uniform**：依赖驱动。OS X 上 attribute 打败 loose uniform 约 2×，Windows 上差别小。
- **AMD Catalyst 13-9**（支持 pre-DX11 硬件的最后一代驱动）：没有 map buffer 的缓存，高频 map 直接不可发布。只有 DX11 GPU 的 AMD 驱动才和 NVIDIA 量级持平。

## 往后看：persistent map 与 next-gen API

评论区与 Supnik 本人都指向 `GL_MAP_PERSISTENT_BIT`——map 一次、之后每帧直接写，通过 `glFenceSync` 管理读写不冲突。配合 `GL_MAP_COHERENT_BIT` 可省掉 flush。这条路线被普遍认为是 GL 上最接近 [[d3d12-resource-binding|Vulkan/D3D12 显式内存]] 的方式。关键规避：**不要加 `MAP_READ_BIT` 和 `COHERENT_BIT` 一起**——NVIDIA 会降级到较慢的内存类型。

Supnik 的坦白判断：能用 persistent map 的硬件，恰好就是能跑 Vulkan 的硬件。**这些扩展可以 spot-fix 单个 bug**，但 GL 对多核极度敌对的基本事实（implicit flush 导致不能保留 UBO 让多线程流式写入）得靠更换后端才能真的解决。这也是 X-Plane 最终投票"用 Vulkan/Metal 替换 GL 后端"而非继续 AZDO-ify 的逻辑起点，呼应 [[vulkan-explicit-performance]]。

## 相关
- [[glbuffersubdata-in-band-streaming]] —— SubData 在多线程驱动下的 fast path 机制
- [[glbuffersubdata-serialization]] —— 同名调用在 pre-thread 时代的串行化陷阱
- [[vbo-double-buffering-orphaning]] —— 更基础的 orphan 模型
- [[buffer-renaming]]
- [[opengl-pinned-memory-vbo-streaming]]
- [[vulkan-explicit-performance]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-glmapbuffer-no-longer-cool]]
