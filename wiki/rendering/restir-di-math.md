---
tags: [渲染, 路径追踪, 实时光追, ReSTIR, 采样, 蒙特卡洛]
date: 2026-04-19
sources: 1
---

# ReSTIR DI 的数学：从 SIR 到时空复用为什么无偏

ReSTIR DI（Spatiotemporal Reservoir Resampling for Real-Time Ray Tracing with Dynamic Direct Lighting, NVIDIA 2020）是当下实时直接光照多光源采样的主力算法。[[graphics-guy-notes|Jiayin Cao]] 写了一篇 "Understanding the Math Behind ReSTIR DI"，从 [[monte-carlo-integration|Monte Carlo 积分]] 一路讲到 SIR → RIS → WRS → 时空复用，专门补齐原论文里没写清楚的几处数学盲点。本页归拢其中的关键结论。

## 预备：采样四件套

- **[[importance-sampling|重要性采样]]**：前提是 `p(x)` 的支集覆盖 `f(x)` 的支集，否则估计会缺一块。
- **[[mis-balance-heuristic|多重重要性采样 MIS]]**：两大条件 `Σm_i(x)=1` 与 `p_i(x)=0 ⇒ m_i(x)=0`；balance heuristic 自动满足，uniform weight 不满足第二条，**这正是 ReSTIR DI 产生偏差的根源**，需要按"非零 PDF 数量"修正。
- **Sample Importance Resampling (SIR)**：先从 proposal PDF 拿 M 个样本，按 `w(x) = p̂(x)/p(x)` 加权，再按权重抽一个。它**近似**于从 target PDF 抽样，M → ∞ 时 SIR PDF 收敛到 target PDF。**最重要的性质**：target 函数不必归一化（恒定缩放对算法透明）——于是可以直接用 `L(ω_i) f_r cos(θ_i)` 当 target function，不必先求它的归一化常数（那本身就是要解的积分）。代价：SIR PDF 不可解析，只能得到它的无偏倒数估计。
- **Resampled Importance Sampling (RIS)**：SIR 的基础上再写 `f(y)/p̂(y) · Σw(x_i)` 做无偏积分估计。文章给出了一份比 Talbot 论文更直接的无偏性证明。
- **Weighted Reservoir Sampling (WRS)**：用 O(1) 空间流式挑选一个加权样本，顺序无关、支持分治，且一个已经跑完的 reservoir 可以被当作"带多重样本的 mini-reservoir"再塞进另一个 WRS——这条性质是后面空间/时间复用的理论基石。

## ReSTIR DI 算法骨架

每像素每帧：

1. **Initial sampling**：从"按 emissive power 加权挑光源 → 在光源上按 light 类型采样"得到 M=32 个候选，target function 用**无阴影光贡献** `L f_r cosθ`（也可选阴影版，即 visibility reuse），通过 WRS 挑出一个候选样本。
2. **Temporal reuse**：把上一帧对应像素的 reservoir 合并进来。
3. **Spatial reuse**：循环若干轮，每轮挑若干邻域像素的 reservoir 合并。
4. **Final shading**：对胜出的 light sample 发一条 shadow ray，用 RIS 估计器积分。

一个像素"间接看到"的候选样本数每轮最多乘 `(k+1)`，n 轮后上限是 `(k+1)^n · M`——但实际有大量重复，因此多轮后收益递减。

## 文章重点澄清的几处数学

### 1. 邻居 target function 不同，为何还无偏？

空间复用里邻居像素的 target function 和当前像素不同（`p̂_b ≠ p̂_a`），看起来像在胡乱混合分布。作者把邻居那一路重绘成：邻居的 SIR 产出一个样本 → 相当于一个新的 PDF（即邻居的 SIR PDF）→ 当前像素把它当作 **另一个 proposal PDF**，和本像素自己的 light sample 一起喂进一次 RIS+MIS。只要修正权重：邻居目标样本进当前像素的 reservoir 时权重是 `(p̂_a(y)/p̂_b(y)) · r_b.w_sum`。

### 2. SIR PDF 不可解析，为什么可以用"big W"替代？

论文里 `W(y) = (1/M)(1/p̂(y)) Σ p̂(x_i)/p_i(x_i)` 的**期望等于 SIR PDF 的倒数**。作者给出：由于整个 RIS 估计器对 `W` 取期望，可以直接把 `W` 拎出来用期望替换而不引入偏差（前提是该位置存在某条 PDF > 0）。

### 3. 邻居 reservoir 贡献的 "N 倍权重"

把邻居 reservoir 看作已经访问了 N 个 proposal 的"重磅样本"。数学上不是真的每次喂 N 次，而是**一次喂入、把权重放大 N 倍、同时把 M 计数也加 N**——等价效果、O(1) 开销。作者强调：这是**乐观上限**，因为 indirectly visited 样本中有大量重复，真正有效样本数更少。

### 4. Temporal reuse 为什么无偏而 TAA 有偏？

TAA 历史帧里存的是**已经求值后的颜色**，当前帧的光照 / 遮挡变化无法反映；ReSTIR temporal reuse 存的是**尚未求值的 light sample**，最差不过是一个低质量样本，不破坏无偏性。

### 5. Visibility reuse 的数学解释

Visibility reuse = 用 `L f_r cosθ · V` 做 target function（阴影版）。难点：前半段 WRS 用的是无阴影 target，后半段 RIS 用的是阴影版。作者把前半段整段视为"独立的一次 SIR 执行"，它产出一个样本，当前像素的 reservoir 从未见过那些 light proposal samples，因此**允许和后面不同的 target function**——同一个技巧也解释了 ReSTIR GI 里"per-initial-candidate target function"的合法性。

### 6. 为什么用 uniform MIS weight 而不是 balance heuristic？

三道门槛：SIR PDF 不可解析，导致 balance heuristic 无法评估；评估 balance heuristic 需要 `O(N²)` 时间和 `O(N)` 存储；balance heuristic 要求事先知道所有 proposal PDF，破坏 streaming 性。代价是 uniform weight 不满足 MIS 第二条件，需要按"当前位置非零 PDF 的数量"做偏差修正——而 SIR PDF 是否为零只需要看 target function 与 proposal PDF 是否同时非零，这是可判定的。

## 与 [[restir-gi-math|ReSTIR GI]] 的关系

ReSTIR GI 是同一套数学用在**全局光照**上：initial candidate 不再是光源上的点，而是一条路径（或路径树），proposal PDF 变为 primary sample space 上的高维 PDF，shift mapping + Jacobian 让邻居路径能换到当前像素的积分域。GRIS 论文把这一切归纳为"允许不同 domain 的 RIS"。

## Sources

- [[sources/graphics-guy-restir-di-math]]
- [[sources/alain-rt-denoising]]
