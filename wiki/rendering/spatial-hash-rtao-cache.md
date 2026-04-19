---
tags: [光线追踪, ambient-occlusion, 空间哈希, 缓存, 去噪]
date: 2026-04-19
sources: 1
---

# Spatial Hashing 做 RTAO 缓存

传统 3D 纹理存 GI / AO / probe / light list 数据访问快但内存占用随体积立方扩张。**Spatial hashing** 用稀疏数组 + 位置 + 法线（等键）计算 hash 做索引，和 cascade 3D texture 比用内存少得多，换来 cache miss 多一点。[[kostas-anagnostou|Kostas Anagnostou]] 2025 年把它落地成 RTAO 加速 + 天然降噪方案，11.4MB 就可以缓存一个 2m 半径、自适应 cell size 的 RTAO 结构。

## 核心机制

- **key**：世界位置量化到 cell（`floor(position / cellSize)`）+ 法线量化到粗格（`floor(normal * 3.0)`）+ cellSize 本身
- **主 hash**：`pcg` 嵌套，算出 cell index
- **checksum**：另一个 hash（`xxhash32`）嵌套，存进 cell 用来识别冲突
- **冲突解决**：[[open-addressing-hashtable|linear probing]]（cache 友好、分布一般），最多扫 `SEARCH_COUNT=10` 步；替代是 rehash（分布更好、cache 差）
- **GPU 原子**：`InterlockedCompareExchange(hash[i], 0, checksum, cmp)` 声明 cell，`InterlockedAdd` 累加 payload
- **payload 打包**：uint 高 16 位累计 hit 数、低 16 位累计射线数

## 自适应 cell size

固定 cell size 近处 blocky、远处浪费。按距离 + 垂直 FOV + 目标屏幕特征 `sp` + 最小世界特征 `smin`：

```
swd = 2^floor(log2(sw / smin)) * smin
```

`sw = sp * 2 * d * tan(f/2) / Ry`。离散级数保证量化稳定、便于哈希。近处远处 cell 投影到屏幕大小相近。

## 过期（age eviction）

hashmap 容量有限，相机移动必然跑光出现黑斑。加一个 `hashTime[i]` 存上次写入帧号；找 cell 时如果 checksum 不匹配且对应 cell 超过阈值帧数（如 20）没动就抢占掉（`InterlockedExchange` 覆盖）。

## 两个衍生好处

- **天然降噪**：同一 cell 平均多像素 / 多帧 1spp 结果，无需 spatial denoiser，只配 [[temporal-antialiasing|TAA]] 就够
- **静态场景缓存复用**：cell 采样数到阈值（如 500）直接读缓存不再 raytrace，同 quality 下 0.4ms vs 传统 1.72ms（3080 mobile 1080p）

## 零成本空间滤波：jitter worldPos

查 cell 时对 worldPos 在 tangent-bitangent 平面做随机 jitter（等于 cellSize 量级），但**不要把 jitter 传给 ray origin**。效果是把一个 cell 的 AO 结果随机散到相邻 cell，相当于空间 blur，噪声进一步降。

## 局限与未解

- 只处理静态场景，动态对象需要额外机制（作者留作下篇）
- 边界 cell 少于 `SEARCH_COUNT` 个相邻位置，可能有黑斑——需要 guard band
- disocclusion / 相机突进区域需要 ramp-up 才能积累足够样本
- hashmap 大小对 quality / cost 曲线的影响作者没给系统数据

## 相关

- [[hybrid-raytracing-pipeline]]
- [[pcg3d-hash]]
- [[non-cryptographic-hash]]
- [[open-addressing-hashtable]]
- [[temporal-antialiasing]]
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-spatial-hash-rtao]]
