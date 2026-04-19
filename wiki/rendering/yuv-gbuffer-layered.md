---
tags: [渲染, GBuffer, deferred, YUV, dcs, MSAA]
date: 2026-04-19
sources: 1
---

# YUV 分层 GBuffer（DCS 风格）

[[thomas-poulet]] 在 [[sources/thomas-poulet-dcs-frame|Digital Combat Simulator 帧分析]]里看到一种少见的 GBuffer 布局：底层资源是一个 **5 层的 texture array**，每层 `R8G8_UNORM`，开 MSAA。选择窄格式 + 多层的原因大概率是要同时照顾 **HDR 范围** 和 **MSAA 带宽**。

## 五层通道分配

| 层 | Channel R | Channel G |
|---|---|---|
| 0 | Normal.x | Normal.y |
| 1 | Albedo.**Y** (luma) | — |
| 2 | Albedo.**U** | Albedo.**V** |
| 3 | Roughness | Metalness |
| 4 | Precomputed AO | 疑似 crevice/cavity |

**法线**用经典的 X/Y 存储 + Z 重建（[[tangent-space-normal-mapping|参考]]，Aras 的 *Compact Normal Storage*），shader 里看到 `mad_sat` 把 [0,1] 映射回 [-1,1]，然后用 abs-sum 重建 Z。

**albedo** 用 **YUV 三通道跨层存放** —— 单通道 `R8G8_UNORM` 装不下三色，所以 Y 单独一层，UV 合在第二层。HDR 渲染下这个编码能保留更多亮度精度（Y 通道）而不被 chroma 的量化压迫。解码时做 YUV→RGB 即可。

**stencil** 被当成 material ID 用得很 aggressive：Terrain=0x04、Runway=0x06、Plane=0x08、Building=0x0D、Vegetation=0x25、Cockpit=0x28 —— 下游的 pass 可以便宜地用 stencil test 对整个类目做选择性处理。

## 渲染顺序

GBuffer 分三段写：
1. 座舱（cockpit）先写
2. 机身 + 非静态物体
3. 地形 + 环境大规模 mesh —— 走 **compute scatter + indirect draw** 的组合，把 LOD 选择和 drawcall 生成都放在 GPU 上（和 shadow map pass 同一套）

## 为什么这种布局少见

常见 GBuffer 要么用 **宽格式单层**（R16G16B16A16，3-4 张 MRT），要么用 packed 布局（例如 normal 压到 octahedral + RGBA8）。DCS 的 5×R8G8 array + YUV 组合在内存带宽上最优但 shader 采样代价高（需要 5 次 array sample）。推测背后的权衡：

- **MSAA** + HDR 下宽格式的带宽爆炸——用 `R8G8` 窄格式按层 MSAA，能让带宽降一个量级。
- **array 结构**让 stencil shared + MSAA 同步容易，不需要手动保证 MRT 格式兼容。
- **YUV** 是为 HDR 下的 chroma subsampling 留空间（虽然这里没看到明显下采样）。

DCS 是自研引擎且面向 PC / 模拟器玩家，带宽敏感 + MSAA 必须——这是 AAA 主机游戏不太会选择的布局。

## Sources

- [[sources/thomas-poulet-dcs-frame]]
