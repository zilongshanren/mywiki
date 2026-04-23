---
tags: [渲染, 裁剪, simd, 多线程, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray 的 SIMD 球-OOBB 两级视锥剔除

Andreas Asplund 2016 年这篇讲实现细节的文章，把 Stingray 视锥剔除整条链路贴出来：**暴力扫全部对象、SIMD、多线程、两级收窄**。没有空间分割树、没有 BVH——他们坦言这种朴素方案目前够快，而且维护成本最低。

## 两级流水：sphere 先，OOBB 后

- **第一级 frustum-sphere**：用对象世界空间包围球做 6 平面测试。SIMD 4 路并行，对每个平面把 normal + d 各 splat 成 `float4`，4 个球一把算内积，6 个 plane 全 `vector_and`。输出写到 `visibility_flag[]`（0 或 `0xffffffff`）。
- **中间 compact**：`remove_not_visible` 线性扫 `visibility_flag`，把通过的对象索引压到 `indirection[]`，末尾补齐到 SIMD lane 数（用最后一个有效值填）。
- **第二级 frustum-OOBB**：对通过球测试的对象，把 OOBB 变换到 clip space 再逐平面测试。这一步借了 Fabian Giesen 和 Arseny Kapoulkine 方法——"Method 2b：把 8 顶点变到 clip 空间，测试是否全在某个裁剪面外"，并用 `simd_min_max_transform` 共享 min/max 角点的乘加。

OOBB 比 sphere 贵得多，所以靠第一级先把多数剔除对象砍掉。

## SoA 数据布局是设计核心

所有可剔除对象进 `ObjectSet`，一个巨大的 SoA：`min_x/min_y/min_z`、`max_x/max_y/max_z`、16 路 world matrix 的每个分量都各自一条 `Array<float>`，还有 `ws_pos_x/y/z`、`radius`、`visibility_flag`、`type`、`id`。SoA + pad 到 SIMD lane 数 = 任何 kernel 都只拉自己需要的那几条数组，cache 友好、load aligned。

这里 `SIMDVector`（x0..x3, y0..y3, z0..z3, w0..w3）+ `SIMDMatrix` 4×4 全部是这种 struct-of-SIMD 写法，矩阵乘法代码几乎和标量版一模一样，但一步算 4 个对象。`simd_min_max_transform` 把"对 min/max 各自乘一次再复用"压到极限，8 个顶点的 world→clip 变换只做一半的乘法。

对象在 [[main-render-thread-state-reflection|state reflection]] 的 `create_object` 里就被分类灌进 `_cullable_objects`、`_cullable_shadow_casters`、`_occluders` 三个 `ObjectSet`——每类独立跑 culling pipeline。

## 多线程：work stealing + atomic signal

`ThreadPool` 暴露 `add_tasks / do_work / wait_atomic`。culling 的拆法是 `work_size = 512` 对象一块，`n_objects / 512` 个 task 丢进队列。每个 `CullingWorkItem` 自带 `std::atomic<uint32_t> signal`，task 跑完 `signal.store(1, memory_order_release)`。

`wait_atomic(&signal, 0)` 是典型的 "help if idle" pattern：如果 signal 还是 0，自己从队列里抢一个 task 跑（`do_work`），抢不到就 `YieldProcessor()`。这意味着等 culling 完成的主线程不会闲着，直接下海帮工。

OOBB 级的多线程拆分"留给读者"——作者自己写得明明白白 ;)

## 为什么坚持暴力扫

这一点在文章里直接讲了：**Stingray 目前从未遇到被 culling 绑住的性能场景**。加空间分割树会引入构建/维护/缓存失效的复杂度，收益在当前负载上不明显。他们的价值观是"KISS + 测量驱动"——真成瓶颈再上 BVH/OCtree。

参考 [[culling]] 里的多层级思路、[[view-frustum-culling-ryg]] 里 ryg 对 AABB-vs-frustum 的 SIMD 路线、[[obb-frustum-sat]] 里 SAT 方法，Stingray 做的更接近 ryg 和 Arseny 那一派的"clip-space 8 顶点外侧判定"版本。

## 收尾：contribution culling 与 cascaded shadow 优化

末尾两个小 bonus：

- **Contribution culling**：把 OOBB 8 顶点投影到近平面，如果屏幕空间 extent 小于阈值，直接当作剔除。需要特殊处理"顶点在近平面后方"导致投影翻转（"external line segments"）——Stingray 的做法是：只要有一个角点在近平面后方，就把 extent 撑到整个屏幕，放弃 contribution 剔除这一帧。
- **级联阴影的 enclosure 优化**：如果对象的 8 clip-space 角点完全落在 cascade N 里，后续 cascade N+1..M 可以跳过——它的阴影贡献已经被 cascade N 完整覆盖。

## Sources

- [[sources/bitsquid-frustum-culling-stingray]]
