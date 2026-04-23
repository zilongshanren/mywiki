---
tags: [渲染, 重要性采样, monte-carlo, brdf, 半球采样]
date: 2026-04-19
sources: 1
---

# 重要性采样：PDF 与 BRDF 分布项互相抵消

[[ben-supnik|Supnik]] 2015 年写了一篇 self-described "对专业图形人来说是 duh" 的小结：当你在论文里看到 GGX、Cook-Torrance 这些 BRDF 的 importance sampling 代码时，**权重（weight）是怎么消失的**？这篇是给"从普通 Monte Carlo 跳到渲染专门 IS"时卡了几分钟的那类人——包括本 wiki 大量读者。

## 带权版的直觉

以 Lambert 光照为例：入射方向与表面法线夹角的余弦 $\cos\theta$ 是一个积分因子。均匀在半球上采样是浪费的——$\theta = 90°$ 附近的样本贡献被 $\cos\theta$ 压成零。把采样密度做成**在法线方向密、在切平面稀疏**，并配上一个**与采样密度成反比的权重**就是经典 [[inversion-sampling-prng|importance sampling]]：

```
高密度区：样本多 × 小权重 = 贡献正常
低密度区：样本少 × 大权重 = 贡献也正常
```

这种带权实现是"以 PDF 正比于 f 的形状采样，按 MC 标准公式 $\hat F = \tfrac{1}{N}\sum f/p$ 估计积分"。**通用、正确，但多做了事**。

## 让 PDF 直接吃掉 BRDF 的分布项

关键观察：**我们设计的 PDF 就是 BRDF 分布项的形状**。在实现里同时：

1. 按 PDF 采样得到样本方向；
2. 对每个样本 eval 完整 BRDF（含 $D$ 项），再乘 $\cos\theta$，除 PDF。

当 PDF 正比于 $D(h) \cos\theta_h / (4 \cos\theta_o)$（GGX normal 分布的常见 IS 选择），在最终估计里**分子里的 $D$ 被分母里的 PDF 精确抵消**——剩下的是一个只包含 shading、几何项 $G$、Fresnel 的简化表达，无需再 eval $D$、无需 sample weight。

这就是为什么教材里 GGX 的 IS 公式长得不像"BRDF × 余弦 ÷ PDF"，而是"仅剩的 $F \cdot G / (...)$ 加 sum + 除以 N"。作者**替你预先化简**过了。

## GGX 的具体形态

**BRDF 分布函数（评估用，给解析光源）**：
```glsl
float den = NdotH * NdotH * (alpha2 - 1.0) + 1.0;
float D   = alpha2 / (PI * den * den);
```

**逆变换 IS（配对的采样代码）**：
```glsl
float Phi      = 2.0 * PI * Xi.x;
float CosTheta = sqrt((1.0 - Xi.y) / (1.0 + (a*a - 1.0) * Xi.y));
float SinTheta = sqrt(1.0 - CosTheta*CosTheta);
```

这两段**配套使用**时，积分估计里 $D$ 与分母中的 PDF 被约掉，应用代码不需要调用第一段——再次出现 IS 的核心姿势：**PDF 替换 distribution，别让两者同时出现在加法里**。

## 用错 PDF 的代价

如果 PDF 并非 BRDF 分布项的"正确匹配"（比如拿 cosine-weighted PDF 去 IS 一个 GGX lobe），仍然有效但要把 weight 加回去、并且每个样本都要 eval 完整 BRDF。**从错误到正确的区别**不是 bias，是方差——匹配得越好收敛越快。Supnik 称此为"the silly way"：比均匀采样强，但离"正确 IS"还有数量级。

## 对实时 IBL 的实际意义

这条原则就是 Epic 的 *Split Sum Approximation* 能成立的前提：

- 每个预计算 cubemap 级的样本方向用 GGX IS 抽出来；
- 积分里只剩余 $L_i \cdot \text{weight}_\text{geometry}$（不含 $D$）；
- 把结果按 roughness 存进 [[parallax-corrected-cubemap|prefiltered env map]]，运行时仅查一次 + BRDF LUT 校准。

若每个样本还要 eval D + weight，预计算阶段的成本和运行时 lookup 的复杂度都会翻倍。同样的简化出现在 [[microfacet-brdf|Microfacet BRDF]] 的实时近似里。

## 相关
- [[monte-carlo-integration]]
- [[inversion-sampling-prng]]
- [[microfacet-brdf]]
- [[path-tracing-monte-carlo]]
- [[anisotropic-microfacet-sampling]]
- [[spherical-integration]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-importance-sampling-no-weights]]
