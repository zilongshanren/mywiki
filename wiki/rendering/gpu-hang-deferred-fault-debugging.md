---
tags: [opengl, opengles, powervr, ios, gpu-hang, 调试, vbo, 索引缓冲]
date: 2026-04-19
sources: 1
---

# PowerVR SGX 上 `gpus_ReturnGuiltyForHardwareRestart` 的延迟故障调试

[[ben-supnik|Supnik]] 2013 年 *What Does gpus_ReturnGuiltyForHardwareRestart Mean?* 讲清楚了一个让一代 iOS OpenGL ES 开发者抓狂的崩溃：

```
frame #0  libGPUSupportMercury.dylib`gpus_ReturnGuiltyForHardwareRestart + 10
frame #1  libGPUSupportMercury.dylib`gpusSubmitDataBuffers + 104
frame #2  IMGSGX543GLDriver`SubmitPackets + 124
frame #3  GLEngine`gleCleanupOrphans + 130
frame #4  GLEngine`glBufferData_Exec + 254
…
frame #6  OpenGLES`glBufferData + 38
```

爆在 `glBufferData`，看上去和爆炸点毫无关系的一次完全合法的上传——而且第一次调用好好的，第 405 次才死。

## 真正发生了什么

Supnik 的复盘（他本人反复声明这是 *speculative engineering*，因为 Apple / PowerVR 的源都不公开）是一条**硬件加速路径的异步失败**：

1. **硬件加速的 `glDrawElements`**：当 element array 和所有 vertex attribute 的 VBO 都绑定好时，驱动只往 command buffer 写几条命令——让 GPU 从 GPU 地址空间（在 iPhone 上就是系统内存）里**自己**去读索引和顶点，CPU 不抄数据、也不做边界检查。
2. **GPU 后延执行**：GPU 拿到命令后自己 fetch 顶点；如果索引越界（或你压根绑错 VBO），GPU 在 fetch 时检测到越界，留一张便条，等下次驱动进门时上报。
3. **下一次 GL 调用接收账单**：你随便发起下一个 GL 调用——`glBufferData` 也好、别的也好——SGX 驱动这时会先问硬件上一次有没有出事，看到越界便条就回头告诉 Apple 的 GLEngine，GLEngine 调 `gpus_ReturnGuiltyForHardwareRestart`——这其实是 Apple 让 IHV 驱动报告"GPU 自己段错误了"的标准回调，名字是这么来的。

因此：**崩溃点 ≠ 闯祸点**，而且**崩溃时机取决于 CPU 与 GPU 两边的时序**，意味着最常见的调试手段（注释一行看变化）只会让崩溃位置**漂移**，你越 bisect 越错。

## Supnik 的修复策略：自己写边界检查

他的办法是：写一个**慢但正确**的 debug 例程，把每次 `glDrawElements` / `glDrawArrays` 之前**全部** fetch 路径的索引范围与 VBO 字节范围都验一遍。这一验立刻抓到了真正的 bug——一次 client-array 调用没有 unbind VBO，而前一次调用刚好留了个 VBO 绑定，于是 client-array 变成了从那个 VBO 里取数据，越界一路翻车。

所以这位已经做了多年 OpenGL 的工程师，被这次事件教会一条**在每个 draw call 外层再套一层自己的宏**的纪律——反正 draw call 在 release 版本里只是透传，加个 debug 分支几乎白嫖。他后来在博客下面又手把手教一位读者怎么做这件事：

> 1) Scan the entire index buffer to find the lowest and highest indices in the draw call.
> 2) For each enabled vertex attribute: get VBO binding, VBO size, stride, size, type, base ptr.
> 3) Compute `start = base + stride × lo`, `end = base + stride × hi + componentSize × count`.
> 4) 越界 ⇔ `start > end` 或 `start < 0` 或 `end > VBO size`.

必须**在** `glDraw*` 之前完成，因为调用一旦发出就已经走向 GPU，没有反悔余地。

## 更一般的现象

这类"账单回单来自完全不相关的调用"的崩溃，是 GPU 编程里**异步 + 延迟验证**的一个共性后果。其他平台也会遇到类似问题（D3D 的 TDR、Vulkan 的 device lost、Metal 的 GPUError 回调），根因都是**驱动不做 per-draw 边界检查，代价从 CPU 转到 GPU 异步事件**。Supnik 的经验把它变成一条可操作的工程准则：**任何"未来可能访问 GPU 资源的异步接口"都值得在自己的包装层里加一个 debug-only 断言关**，哪怕会大幅拖慢 debug 构建。

## 相关

- [[opengl-ext-vs-arb-fast-path-leak]] —— 驱动 fast path / slow path 的隐式瀑布：本条目是 fast path 的另一面（fast path 不校验）
- [[race-condition-debug]]
- [[opengl-builtin-attribute-aliasing]] —— 另一个"对但不对"的 GL 状态陷阱
- [[gpu-queues-vs-dispatch-execution]] —— GPU 命令异步执行与 CPU 回调的边界
- [[ben-supnik]]

## Sources

- [[sources/supnik-gpus-returnguilty-restart]]
