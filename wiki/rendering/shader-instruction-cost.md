---
tags: [渲染, GPU, 着色器优化, 性能, ISA, HLSL]
date: 2026-04-14
sources: 1
---

# Shader 指令的隐藏成本

一个看起来"就一行 HLSL"的操作，在 GPU 上可能展开成几十条原生 ISA 指令。Kostas Anagnostou 把这种"指令隐藏成本"分成三大类，下面按这个分类展开——全部讨论以 GCN/RDNA 的 RDNA ISA 为例，工具是 `godbolt.org` + RGA。

## 类型 1：硬件没这条指令

最常见也最吓人的情况。HLSL 写一行，编译器铺一整页 ISA。

- **反三角函数** (`acos` / `asin` / `atan` / `atan2`)：没有原生实现。一个 `atan2()` 在 RDNA 上展开成**数十条指令**——包含两次 `v_div_scale_f32` / `v_rcp_f32` 浮点除法、一整段六次 Horner 多项式 (`v_fma_legacy_f32 ... lit(0x3b47bf1d) ... lit(0xbeaaaaa3)`)、大量 execute mask 操作和分支；整个 program 轻松超过 60 条原生 vop。这就是圈子里那句"atan2 is not free"的底气。
- **`tan()`**：没原生，硬拆成 `sin/cos/rcp/mul`。
- **`normalize()` / `length()`**：同样没原生，被拆成 `mul + fma + fma + rsq + 三次 mul` 这类套路。
- **整数除法** (vector)：没有原生 vop，一次整数除法在 RDNA 上展开成约 **35 条指令**；若操作数在 scalar register 里则约 **42 条混合 scalar+vector 指令**。
- **Cubemap 采样**：一次 `cubemap.Sample(...)` 要先算出使用哪个面——`v_cubema/v_cubetc/v_cubesc/v_cubeid` 各来一次、`v_rcp_f32` 算缩放、两次 `v_fmaak_f32` 把 UV 拉到 [0,1]，再进入 `image_sample`。相比 2D 采样多出一大块 face-select 开销。
- **动态 VGPR 数组索引**：硬件指令里寄存器号是**编译期常数**；遇到运行时下标编译器有两条路——
  - **uniform 下标**：`v_movrels_b32` 以 `m0` 为相对偏移访问相邻 VGPR（较便宜）；
  - **thread-variant 下标**：只能**对每一个可能值做一次 cmp+cndmask**，形如 `v_cmp_eq_i32 + v_cndmask_b32` 四遍完成一个 4 元数组的 gather。这是 [[register-spilling-avoidance]] 里那条"动态下标会让编译器把数组放进 local memory"警告的 ISA 级别证据。

## 类型 2：硬件实现本身有代价

**原生 ≠ 同价**。GCN/RDNA 上的延迟表非常不均：

```
v_mov_b32 / v_add_f32 / v_mul_f32 / v_mac_f32      4 cycles
v_rcp_f32 / v_cos_f32 / v_sin_f32 / v_rsq_f32     16 cycles
v_mul_lo_u32  (integer mul)                        16 cycles
```

超越函数 (`cos/sin/exp/log/rsq/sqrt`) 和整数乘法是 **4×** floating mul 的开销，也就是所谓 "quarter-rate"。这不会出现在 shader 源码里，需要看 [RGA 在 Shader Playground 上的 breakdown](https://shader-playground.timjones.io/) 才能抓到。

**scalar float 运算不存在**：GCN/RDNA 的 scalar unit 不支持浮点。所以写 `float3 result = mul(v, m)`（v 和 m 都在 scalar register 里）时，编译器会把所有 mul/fma **强制搬进 vector unit**：

```
v_mul_f32 v0, s0, s8
v_mul_f32 v1, s0, s10
v_fma_f32 v0, s9, s1, v0
...
```

代价是把本来在 SGPR 里的东西倒贴到 VGPR，可能抬高 VGPR 占用、拉低 wave occupancy，最终影响 [[gcn-wave-occupancy]] 的曲线。

## 类型 3：依赖外部资源的隐性成本

最不稳定的一类——开销和 cache/ 内存子系统的状态耦合。

- **纹理读**：cache hit 几个 cycle，miss 到 VRAM 几百个 cycle。能不能被隐藏取决于编译器的指令重排能力，以及 CU 在 flight 的 wave 数是否够多（[[gpu-latency-hiding]]）。
- **sampler 即使 cache 命中也不免费**：单通道纹理用 `pointSampler` 走 `tex.Sample(...)` 是 **16 cycles**，而 `tex[coord]` 走 `Load` 是 **4 cycles**——GCN 手册里写的"避免单通道 sampler 路径"就是这个。
- **非 uniform 资源索引的 waterfall loop**：`inputBuffer[NonUniformResourceIndex(index)]` 当 index 线程差异时，编译器生成一个 **waterfall loop**——`v_readfirstlane_b32` 拿第一个活跃线程的 index，`v_cmpx_eq_u32 exec, s6, v0` 屏蔽成和它同 index 的子集、只处理这批、然后循环。最坏情况（32 个线程 32 个不同 index）整个 loop 要绕 32 圈，吞吐降到 1/32。
- **LDS bank conflict**：RDNA 和 NVidia 的 groupshared 都分 32 banks（`index % 32`）。好模式是 `data[GTid.y*32 + GTid.x]`——连续线程命中不同 bank；坏模式是 `data[GTid.x*32 + GTid.y]`——连续线程命中同一 bank，序列化访问，单次 LDS 延迟可能被**放大 32×**。

## 为什么要关心

"隐藏成本"能不能翻译成真实性能损失，取决于这条指令所在的 shader 是不是被 ALU/ 延迟 bottleneck——有时一个 `atan2` 出现在明显延迟掩蔽的 memory-bound shader 里毫无影响，有时一个 `NonUniformResourceIndex` 在关键循环里能拖垮整个 dispatch。[[bottleneck-analysis]] 的方法论就是不假设。

对反三角函数的常见对策是近似 ([Sébastien Lagarde 的 AMD GCN 优化笔记](https://seblagarde.wordpress.com/2014/12/01/inverse-trigonometric-functions-gpu-optimization-for-amd-gcn-architecture/)) 或者[用点乘/叉乘绕开](https://iquilezles.org/articles/noacos/)。对动态下标是 `[[unroll]]`（见 [[register-spilling-avoidance]]）。对 waterfall 是提前 wave broadcast 或重构数据布局。对 LDS conflict 是调换 `GTid` 维度。

通用建议只有一个——**看 ISA，别猜**。编译器在 HLSL → DXIL → target ISA 之间做的事情永远会让人意外。

## 相关

- [[register-spilling-avoidance]] — 动态数组下标触发的另一类 ISA 膨胀
- [[gcn-wave-occupancy]] — VGPR 预算如何决定并发
- [[gpu-latency-hiding]] — 内存延迟能不能被 wave 切换掩盖
- [[bottleneck-analysis]] — 判定指令成本是否真正有感
- [[faster-math-functions]]

## Sources

- [[sources/interplay-hidden-shader-cost]]
