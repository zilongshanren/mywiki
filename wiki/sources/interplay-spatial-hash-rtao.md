---
tags: [source, 光线追踪, ambient-occlusion, 空间哈希, 缓存, 渲染]
date: 2026-04-19
sources: 1
---

# Spatial Hashing for Raytraced Ambient Occlusion（Kostas / Interplay of Light）

[[kostas-anagnostou|Kostas Anagnostou]] 发表于 2025 年 11 月 23 日，把 Gautron 2020 talk 里的 spatial hashing 思路落地成实验性 RTAO 加速 + 去噪方案，既是稀疏 3D 缓存的教学样本，也实测了 11.4MB 的 1M 单元结构如何在大场景下通过"过期"机制维持可用。

## 摘要

传统 3D 纹理存体素 GI / light list / volumetric fog 数据访问快但占内存大、覆盖有限。**Spatial hashing** 用稀疏数组 + 位置 + 法线 + 其他 key 计算 hash 值做索引。对 RTAO 有天然契合：静态场景 AO 只依赖世界位置 + 法线，完全可以缓存复用；还能作为天然 denoiser——多帧 / 多像素的 1spp 射线被同一 cell 平均掉。

实现细节：每个世界点用 [[pcg3d-hash|pcg hash]] 做 key、xxhash32 做 checksum 放进同一单元用于冲突检测；位置量化到 cell（`floor(position / cellSize)`），法线量化到 `floor(normal * 3.0)`（大概 27 个法线格），三者 + cellSize 嵌套 hash。查找冲突时走 linear probing（cache 友好但分布不最优，替代是 rehash），最多扫 `SEARCH_COUNT=10` 个位置。GPU 侧用 `InterlockedCompareExchange(hash[i], 0, checksum, cmp)` 原子声明 cell。cell payload 是 uint 高 16 位存累计 hit、低 16 位存累计射线数，`InterlockedAdd` 更新。

cell size 不是常量：近处格子投影到屏幕上太大导致块状 artifact，远处格子又浪费。作者从 Gautron 那里抄了公式根据**距离 + 垂直 FOV + 目标屏幕空间特征大小 `sp` + 最小世界空间特征 `smin`** 计算自适应 cell size（`swd = 2^floor(log2(sw/smin)) * smin`，保证是离散级数便于哈希）。效果：近处远处 cell 投影到屏幕面积相近，2m RTAO 半径 + 1M cell hashmap + sp=3 smin=0.07 就能做出干净细节，**无需 denoising 只靠 TAA**。

Hashmap 容量有限，相机移动必然跑光。作者加了**按帧索引的 age eviction**：`hashTime[i]` 存上次写入帧号，查找时如果 checksum 不匹配但某 cell 超过 20 帧没动就强行抢占。1M cell 下飞来飞去不再出黑斑。

另一个衍生好处：静态场景下 cell 累计到一定样本数（如 500）后就**停止 raytrace 直接复用缓存值**，同 quality 下用 0.4ms 替代传统 RTAO 的 1.72ms（3080 mobile，1080p）。

锦上添花：cell 查询时对 worldPos 在 tangent-bitangent 平面做 **jitter**（不要 jitter 到射线起点），等效于零成本的空间滤波——相邻 cell AO 结果互相掺入，质量进一步提升。

内存成本：1M cell × 4 字节 × 3 buffer（hash / time / payload）≈ 11.4MB。局限：只覆盖静态场景，动态物体的处理作者留作下篇。

## 关键要点

- Spatial hashing 用 (位置 + 法线 + cellSize) 嵌套 pcg hash 做 key、xxhash32 做 checksum
- Linear probing 解决冲突：cache 友好但分布一般；rehash 分布更好但 cache 差
- cell size 按距离 + FOV 自适应：远处用大 cell 省格子、近处用小 cell 保细节
- 按帧索引的 age eviction 让 hashmap 在相机移动时不会永久跑光
- cell 平均射线结果本身就是天然 denoiser，TAA 后不需要额外空间滤波
- 静态场景 cell 达到样本数阈值后可跳过 raytrace，性能从 1.72ms → 0.4ms
- 世界位置 jitter 等效零成本空间滤波，进一步降噪
- 11.4MB 是 1M cell + 自适应 size 下一个 2m 半径 RTAO 的实测占用
- 局限：静态场景专用，动态对象需要额外机制

## 链接到的概念

- [[spatial-hash-rtao-cache]]
- [[hybrid-raytracing-pipeline]]
- [[pcg3d-hash]]
- [[open-addressing-hashtable]]
- [[temporal-antialiasing]]
- [[kostas-anagnostou]]

## 原文

- 链接：https://interplayoflight.wordpress.com/2025/11/23/spatial-hashing-for-raytraced-ambient-occlusion/
- 本地：`raw/articles/interplayoflight.wordpress.com/2025-11-23_spatial-hashing-for-raytraced-ambient-occlusion.md`
