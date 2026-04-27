---
tags: [渲染, 光线追踪, 发散, SER, nvidia, ada-lovelace, gpu-优化]
date: 2026-04-27
sources: 2
---

# Shader Execution Reordering（SER）：主动消减 SIMD 发散

Shader Execution Reordering 是 Nvidia 在 Ada Lovelace 架构中引入的一项光线追踪优化技术，通过显式将发散的线程重新聚合为更连贯的 warp，减少控制流发散和内存访问发散带来的性能损失。

## 发散问题的本质

GPU SIMD 模型要求同一 warp 的所有线程执行相同指令。当光线追踪时，同一批射线可能击中各不相同的几何体和材质，触发不同的条件分支（控制流发散）或访问散乱的内存地址（内存访问发散）。两种发散都会降低 lane 利用率和缓存效率。Cyberpunk 2077 Overdrive 模式的实测数据显示，光追 kernel 的 active lane 数平均仅 11.6 / 32（约 36%）。

## SER 的工作方式

SER 是显式 API，需要开发者在 shader 中主动调用：

```hlsl
NvReorderThread(coherenceHint, numCoherenceHintBitsToConsider);
```

1. Shader 调用时提供一个"coherence hint"作为排序键，以及需要考虑的 bit 数
2. 线程当前的活跃寄存器状态被 spill 到内存（L2 缓存）
3. 硬件按 key 对线程进行排序（radix sort，bit 数少则接近线性复杂度）
4. 排序后的线程重新组成 warp，恢复寄存器状态继续执行

排序推测在 SM 内部完成（每个 SM 最多 1536 threads），shared memory 可存放所有线程的 32-bit sort key，无需全局同步屏障。Ada 的大 L2 缓存（针对 SM 数量而言容量充足）使寄存器 spill/reload 的 overhead 保持在可接受范围。

## 实测效果

在 Cyberpunk 2077 Overdrive 模式（RTX 4070 Ti）：

- DispatchRays 耗时减少 **24%**
- Active lanes/warp 提升 **46%**（从约 8 提升到约 12）

## 与其他方案的对比

AMD RDNA 3 通过引入专用的 LDS BVH 遍历栈指令（`ds_bvh_rtn_stack_b32`）来减少 traversal 阶段的分支和向量 ALU 开销——这是针对光追 traversal 的局部优化。SER 则在更高层次上重组线程，适用于 traversal 之外的任意光追 kernel，但需要显式调用和 spill/reload overhead。

两者并不互斥，RDNA 上未来也可能引入类似机制。

## 局限性

- 需要开发者显式支持，不透明
- 每次 SER 调用有 overhead（寄存器 spill、排序、reload），需谨慎选择调用时机
- 光追仍比光栅化有更多固有发散，SER 只是缓解，无法根治

## Sources

- [[sources/chipsandcheese-nvidia-ser]]
- [[sources/chipsandcheese-cyberpunk-path-tracing]]
