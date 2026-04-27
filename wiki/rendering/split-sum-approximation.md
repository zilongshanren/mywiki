---
tags: [rendering, pbr, ibl]
date: 2026-04-19
sources: 1
---

# Split-Sum 近似

Karis 2014（UE4 PBR）提出把镜面 IBL 积分拆成两个预计算项的乘积：prefiltered environment map（按 GGX 重要性采样、按粗糙度存进 cubemap mip 链）乘以 environment BRDF LUT（2D 纹理，红通道存 scale `f_a`、绿通道存 bias `f_b`，输入 `NoV` 与 roughness）。运行时只需两次纹理采样即可组装 `F0 · f_a + f_b`，省掉对半球的在线积分。

近似成立的前提是把 NDF 当作各向同性（`N = V`），代价是丢失"拉长"的反射；Lagarde 在 Frostbite 课件中补了经验分母 `Σ NoL` 以贴合常数环境。额外的重要性采样通过 GPU Gems 3 的 [[cubemap-mip-ibl-prefilter|mip chain 技巧]] 把低 PDF 样本映射到高 mip 以加速收敛。BRDF LUT 128×128 RG16F 足够；prefilter cubemap 按 mip 对应不同 roughness。该近似只包含单次散射，高粗糙度金属会丢能量，需 [[ibl-multiple-scattering|Fdez-Agüera 多次散射]] 补偿。

## Sources

- [[sources/bruop-ibl-multiple-scattering]]
- [[sources/c0de517e-envmap-wrong]] — split-sum 误差分析与各近似层的系统梳理
