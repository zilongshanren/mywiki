---
tags: [rendering, simd, performance, culling]
date: 2026-04-19
sources: 2
---

# ISPC / SIMD 在剔除中的应用

剔除是 SIMD 的天然场景：10,000 个物体独立测试，数据结构简单。Bruop 给出两种路径。

**手写 SSE/AVX 内建函数**：把 4×4 矩阵乘法按行广播 + FMA 重写；AABB 8 顶点用 `_mm256` 一次变换；水平 OR 归约靠 permute/shuffle 把 8 lane 压成单值。数据布局需从 AoS 转 SoA——AABB 的 `min.x,y,z / max.x,y,z` 各自成独立数组，否则就要付 gather/scatter 的代价。手写版把 1.2 ms 的线性剔除压到 0.3 ms。

**Intel [ISPC](https://ispc.github.io/)**：一种类 C 的 SPMD 语言，编译产出 SSE4/AVX2 多目标 obj，头文件直接给 C++ 调。ISPC 的陷阱也在数据布局：若传入 `Array<mat4>`，编译器会提示"需要 gather"，因为 ISPC 必须把 AoS 的 `vec4` 元素散布到 SoA 寄存器再计算。Bruop 初版把 model→view 变换放进 ISPC，反而比线性版慢 0.1 ms——最终把矩阵乘法留在外面（已手写 SSE）、AABB 转 SoA 喂给 ISPC。

ISPC 版的 [[obb-frustum-sat|SAT]] 代码几乎逐行照抄 C++，可读性远好于手写 intrinsic，并与手写 SIMD 同速（0.3 ms / 10k 物体），但测试更健壮。分支散度担忧不大——99.9% 的物体在第一组 frustum 法向就被剔或必跑满 26 轴，lane 几乎同步。

## Sources

- [[sources/bruop-frustum-culling]]
- [[sources/bruop-more-robust-frustum-culling]]
