---
tags: [computer-systems, gpu, execution-model, vulkan, parallel]
date: 2026-04-19
sources: 1
---

# GPU 队列模型 vs. Dispatch + Barrier 模型

当前主流 GPU 编程模型里，compute pipeline 基本是一串 "dispatch → pipeline barrier → dispatch → pipeline barrier" 的大栅栏。每一段 dispatch 向某个大 buffer 写输出，下一段 dispatch 从这个大 buffer 读输入。Raph Levien 在《I Want a Good Parallel Computer》里指出这个模型的根本问题：**中间 buffer 必须在 CPU 端先把最大尺寸申好**，而对于动态工作负载（像 [[vello-gpu-2d-renderer|Vello 的 2D 渲染]]），每一 stage 的输出规模依赖输入且不可预测——预估就浪费、预估不足就失败重试（retry 还要 GPU→CPU readback，致命级别的 latency）。

他提倡的替代模型是**stage 之间用队列（queue）连接**：每个 stage 是一个 kernel，kernel 从输入队列拉 item 处理、向输出队列推结果；队列只需足够大以维持流水线饱和，不需要预估最大中间体积。这其实是经典的生产者-消费者模型，在 CPU 上完全不新鲜，但 GPU 的 compute 执行模型一直没有把它暴露给应用层——尽管 GPU 内部的 vertex→fragment→rasterop 流水线**本身**就是队列化运行的，只是隐藏在固定功能硬件后面。

学术和工业上的参考：

- **GRAMPS**（Stanford, 2009）：较早把这个想法形式化，node + queue 的执行图。
- **Brook**（CUDA 的前身，Stanford）：流式编程模型，stages 之间是流。
- **Work graphs**（D3D12, 2024）：现代最接近 GRAMPS 的生产级实现——但 Raph 指出有三个 blocker：缺 join、不保证 ordering、不支持变长 element。
- **VK_EXT_device_generated_commands**：半步——shader 可以编码命令到 command buffer，但不能真正递归发起工作。

更激进的方向是**把 Vulkan/Metal API 本身下放到 GPU 上运行**——shader 里直接调用 `vkCmdDispatch`，latency 从 100µs 级的 RPC 降到几 µs 级的本地调用。CUDA 12 的 device graph launch 已经是雏形。从 shader 运行 C 语言也是这条路的一个实验（[vcc](https://shady-gang.github.io/vcc/) 项目）。

Raph 的判断：**latency 是动态工作创建的头号 blocker**——不是 throughput，不是并行度（他的 prefix-sum 思路能扩到几十万线程），而是"在 GPU 上发起新工作"这件事本身太慢。队列模型的核心价值就是把这件事变得几乎免费。

## Sources

- [[sources/raphlinus-good-parallel-computer]]
