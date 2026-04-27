---
tags: [raytracing, gpu, amd, rdna4, bvh, obb, primitive-compression, intersection-engine]
date: 2026-04-27
sources: 1
---

# RDNA 4 光线追踪改进（RT IP 3.1）

RDNA 2 建立了 AMD 在 PC 端的第一套硬件光追实现，此后每代都在其保守的"compute shader 全程掌控遍历"模型上叠加改进。RDNA 4 的 RT IP 3.1 是迄今为止改动最大的一次迭代，三个方向同步推进：更高的硬件相交测试吞吐、更贴合几何体的包围盒、更紧凑的 BVH 存储。

## 双相交引擎与 8-wide BVH

RDNA 4 的 Ray Accelerator 内置两个 Intersection Engine，盒测试吞吐从每周期 4 个（RDNA 2/3）增至 8 个，三角形测试也翻倍。吞吐提升必须搭配更宽的 BVH 才能充分利用——否则每步仍只有 4 个子节点可测，第二个引擎无事可做。

因此 RDNA 4 将 box node 从 4-wide 升级为 8-wide，对应新增 `IMAGE_BVH8_INTERSECT_RAY` 指令和 `DS_BVH_STACK_PUSH8_POP1_RTN_B32` 栈指令。8-wide 的更直接收益在于**减少遍历步数**——树更"胖"意味着更浅，每条光线需要的指针追逐次数更少。GPU 的高延迟特性使得减少串行依赖跳转比提升每步计算量更有价值（见 [[bvh-traversal-hardware]]）。

另有 `IMAGE_BVH_DUAL_INTERSECT_RAY` 指令支持 BVH4x2 算法：同时弹出两条遍历路径并行测试，但需要更多内存访问，效率不如 8-wide BVH。实际游戏和测试中 AMD 驱动均使用 8-wide BVH。

## 定向包围盒（OBB）

传统轴对齐包围盒（AABB）对非轴向几何体（如斜置的链条、旋转的栏杆）拟合很差，产生大量无效相交测试。RDNA 4 引入定向包围盒，每个 8-wide box node 通过一个 OBB 矩阵索引指向 104 个预定义旋转矩阵之一，以约 800 字节的 ROM 查表实现近似最优的包围方向。

存储设计保持优雅：每个 OBB 矩阵用 9 个 6-bit 索引编码，再查 26 个 FP32 值的二级表，整个 8-wide box node 仍保持 128 字节（=GPU cacheline）。代价是只能为一个 node 的所有 8 个子节点选用同一旋转，对旋转方向分散的几何体（如多方向的枝形吊灯）效果有限。

RDNA 4 的 Ray Accelerator 新增**光线变换模块**，名义上用于 TLAS→BLAS 过渡时的光线旋转，也可服务 OBB 相交前的光线坐标变换。

## 图元节点压缩

RDNA 4 的 128 字节压缩图元节点（compressed primitive node）可打包多个共享顶点的三角形对。压缩手段：
1. 跨三角形对共享顶点，只存唯一顶点坐标
2. 对顶点坐标的 FP32 位表示找最小尾零数，截断后压缩存储
3. Box 坐标从 FP32 改为 12-bit 量化整数

实测中 RDNA 4 图元节点常能容纳超过 2 个三角形对，BVH 内存占用明显下降（Elden Ring、Port Royal 等场景有可观收益），有利于缓存命中率和带宽。Cyberpunk 2077 因场景动态性高（NPC 随机分布）收益不稳定。

## 实测效果

在 3DMark DXR Feature Test 中：
- RDNA 4 RX 9070：111.76G 盒测试/s，19.61G 三角形测试/s
- RDNA 2 RX 6900XT：38.8G 盒测试/s，10.76G 三角形测试/s

Ray Accelerator 利用率：RDNA 4 约 24%，RDNA 2 约 10%——说明 8-wide BVH 确实让硬件更容易被喂饱。每条光线的遍历步数在 Cyberpunk 2077 中大幅下降，在 Elden Ring 中略有改善。

## Sources

- [[sources/chipsandcheese-rdna4-raytracing]]
