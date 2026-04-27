---
tags: [渲染, subsurface-scattering, bssrdf, 离线渲染, pbrt, cycles]
date: 2026-04-19
sources: 1
---

# Subsurface Scattering 的工程实践

SSS（次表面散射）的理论材料不少，但「怎么把它真正接进 path tracer 且不冒 fireflies」的实战笔记罕见。[[Jiayin Cao]] 从 PBRT 3rd ed. 的 SSS 开始集成进 SORT，参考 Cycles 做了一轮轮迭代——这页提炼他的工程结论。

## BSSRDF 和 BRDF 的差别

标准 rendering equation 里积分只考虑**一个位置 $p_o$**。SSS 的广义版再加一维面积积分：

$$L_o = \int_A \int_\Omega L_i(p_i, \omega_i)\, f(p_o, p_i, \omega_i, \omega_o)\cos\theta_i\, d\omega_i\, dA$$

多出的维度是**入射位置**——它依赖几何形状，importance sampling 比方向难得多。

## 基本架构（PBRT 3rd 的 separable BSSRDF）

- $S = S_w^{out} \cdot S_p(p_o, p_i) \cdot S_w^{in}$ 三段分解。
- $S_p$ 只看**两点距离**而非 surface 上的相对位置——「diffusion profile」，与物体形状无关。
- Disney 2015 profile 有解析 pdf，可完美 inversion sampling。
- **位置采样**：投影到切平面的 disk 上采一个 $(r, \theta)$，沿法线方向投射短射线找 mesh 交点。

## 实战坑 1：fireflies

朴素集成完后作者 1k spp 仍满屏 fireflies，8k 更糟。查下来两个根源：

**根源 A：SSS 之间的反复散射**。光路 $P_0 \to P_{11} \to P_2 \to P_{31} \to \dots$ 在 SSS 体内部反复弹跳（因为外壳内部几何分层），极少数「逃出来的」路径 pdf 极低、贡献暴涨。

→ **Cao 的 trick**：**若前一次 bounce 是 SSS 材质，这次把 SSS 材质临时换成 Lambert**。这违反严格无偏但视觉几乎无差别（Lambert 近似 SSS 之间的相互散射够用），消除 90% fireflies。

**根源 B：多交点 pdf 不均**。PBRT 在短射线多点交时「均匀选一个」，相当于给 Disney pdf 再乘 $1/K$ 条件概率。在某些几何下，选中的红点远离光源而 5 个绿点靠近光源——sampling 效率塌方。

→ **Cao 的 trick**：**评估所有交点**而不是 uniform pick 一个。性能上之所以可行，是因为 A 已经阻止了指数路径膨胀。

## 实战坑 2：透明度过渡的连续性

目标：当 mean free path → 0 时，SSS 应**平滑退化为 Lambert**。PBRT 的 Fresnel 夹层破坏这个连续性（脖子接缝能看见色差）。

→ **Cao 的 trick**：去掉两侧 Fresnel，BSSRDF 简化成 $S(p_o, p_i, \omega_o, \omega_i) \approx S_p(p_o, p_i) / \pi$。数学上（$S_p$ 退化成 Dirac，MC 估计自动降维）与 $f_{lambert}$ 的结果精确相同。Fresnel 放到外层 shader 建模，不再 hardcode 在 BSSRDF 里。

## 实战坑 3：同材质多 mesh 相互干扰

两个有相同 SSS 材质的 mesh，PBRT 会让它们互相找交点。

→ **Cao 的做法**：每个 mesh 实例化独立材质副本并带 unique id；同材质不同 mesh 自动隔离。

## 材质系统重构

原系统 BSDF 只能线性组合 BXDF。要支持 BXDF+BSSRDF 混合（皮肤 = 高光 + 多 SSS profile），他引入 `ScatteringUnit` 基类，派生出 BXDF 和 BSSRDF；`ScatteringEvent` 代替 BSDF 管理两个独立数组——方便 path tracer 分别处理。

## 其他优化

- **K-nearest intersection 接口**：沿射线一次收集所有交点，避免 naive「交一个、推进一点、再交」的重复遍历。SSS 专用优化，渲染性能 +11.5%。
- **SSS 专用 MIS 关掉**：因为退化分支是 Lambert，BRDF 方向采样没意义，只 light sampling 就够。
- **max SSS bounce**：独立于 path max bounce，可单独控制。

## 未解决问题

- 薄几何（龙头）：短射线全部 miss，最终颜色偏暗。Cycles 有更好的解，作者说值得投资。
- BDPT 下的 SSS：MIS 权重推导很难。
- Random walk SSS：更通用的算法家族，下一步可探。

## 相关

- [[volume-rendering-offline]]
- [[microfacet-brdf]]
- [[path-tracing-basics]]
- [[path-tracing-monte-carlo]]
- [[fast-translucency-wraplight]]
- [[graphics-guy-notes]]

## Sources

- [[sources/graphics-guy-sss-practical-tips]]
