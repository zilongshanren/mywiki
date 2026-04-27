---
tags: [source, compute-shader, 性能优化, gpu, amd, 并行算法]
date: 2026-04-27
sources: 1
---

# Reloaded: Compute Shader Optimizations for AMD GPUs（Wolfgang Engel）

[[people/wolfgang-engel|Wolfgang Engel]] 2015 年 1 月发表的跟进文章，是 2014 年原帖的"再版"：修正原帖的若干错误，补充更多 GPU 型号的实测数据，并将源代码公开至 Google Code。

## 摘要

文章以 Intel GPA 为分析工具，在 AMD HD 6770 / 7750 / 7850 / R9 290X 四款显卡上重新测量了一系列并行归约 compute shader 变体的帧耗时。结论与原帖大体一致，但本次补入的新发现是：对 HD 6770，将 TGSM 预取从"2 值 + 64 线程"升级为"2 值 + 64 线程（reloaded）"后性能几乎减半，而其他卡基本持平；暗示 HD 6770 从 TGSM 利用率提升中获益更大，而较新的 290X 受内存带宽限制更明显。最终测量表明：进一步增大线程组（256、512、1024 线程）和继续增加预取值数（4 值、16 值）已不再带来显著收益——此时性能上限是设备内存读取 1080p 源缓冲区的带宽，而非计算本身。双倍共享内存（将结果写入 2× TGSM 再归约）的实验也基本无改善，因为该 shader 的临时寄存器压力本来就很低。

## 关键要点

- 对 HD 6770，预取 2 值到 TGSM（64 线程版）将帧耗时近乎减半；其他卡改善有限
- 预取 4 值 + 64 线程后，增大线程组至 256/512/1024 对性能影响不大——bottleneck 转为内存带宽
- 16 值预取（最终归约到 15×9）反而变慢：读取距离变远，空间局部性下降
- 双倍 TGSM 方案（`sharedMem[groupthreads * 2]`）在临时寄存器不足时有效，但此场景无益
- 结论：1080p 并行归约的性能天花板由源缓冲区的读带宽决定；降分辨率（720p/480p）才能进一步分离计算与带宽贡献

## 链接到的概念

- [[compute-parallel-reduction]]
- [[async-compute]]
- [[gcn-wave-occupancy]]
- [[people/wolfgang-engel]]

## 原文

- 链接：http://diaryofagraphicsprogrammer.blogspot.com/2015/01/reloaded-compute-shader-optimizations.html
- 本地：`raw/articles/diaryofagraphicsprogrammer.blogspot.com/2015-01-12_reloaded-compute-shader-optimizations-for-amd-gpus-parallel.md`
