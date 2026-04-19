---
tags: [pbr, arnold, validation, material, light]
date: 2026-04-19
sources: 1
---

# 材质与光照的验证流程（Stingray + Arnold）

PBR 管线最容易悄悄走样的地方是"看起来差不多但不对"——能量不守恒、Fresnel 用错、光强度单位混乱，场景还是能出图，但光照响应不服从物理，美术只好一点点手调补偿。Stingray 在 2017 年做了一套**以 Arnold 为地面真值**的验证流程，由 Jp 记录下来。

**思路**：与其直接拿真实照片对照（噪声、色彩管理、镜头畸变混在一起难以定位 bug），不如先对照一个已知正确的**离线路径追踪渲染器**。Autodesk 当时刚收购 SolidAngle，Arnold SDK 免费（无 license 只是水印），就写了 Stingray 插件把 scene 反射成 Arnold scene graph；再自定义 Arnold Output Driver 把线性数据直接喂进 Stingray viewport，走同一个 gamma + tonemap 链路，尽量压缩误差源。

**材质映射**：Arnold 4.x 的 `Standard` shader 对 metallic/roughness 对齐不佳，用 `alSurface` 两套 specular 分别承担 non-metal 和 metal 部分才凑齐；5.0 换成 `aiStandardSurface` 直接就有 metalness，映射干净。

**对照发现两个材质 bug**：
- **能量不守恒**：Fresnel 反射贡献没从 diffuse 中扣除，导致光滑反射面在掠射角处亮过头。Arnold 的 Light Path Expression 能拆分 specular/diffuse 各项，按通道对照立刻定位。
- **金属 Fresnel 染色错用**：很多 shader 错误地把 base color 乘进整个 Fresnel 曲线。正确做法是**只把颜色放进 F0**（基础反射率），Fresnel 曲线的形状保持不染色——所有波长在 90° 都趋近 1，这是金属反射边缘发白的物理原因。Jp 用 Karis 的 2D LUT 预积分（*Real Shading in Unreal Engine 4*）实现。

**光照对照发现的 bug**：Stingray 的衰减写成 `I / (d+1)²` 而非 `I / d²`——为避免 d→0 时强度爆掉污染累积 buffer。代价是曲线整体不对，在建筑可视化这种大空间里肉眼可见偏差。修复：改成 `I / (d+ε)²`（ε = 1/max_value）+ 在写入/读取光照累积 buffer 前后各做一次 EV 移位（参考 Nathan Reed）。IES profile 与色温也一并对照通过。

**方法论外推**：这套"离线渲染器做 ground truth + 同一 tonemap 链路出图 + 按通道拆项对照"可以推广到 antialiasing、折射、毛发、体积、post-effect 全链路。下一步是对照真实照片的 [[physical-camera-model|controlled light room]]，验算单位。

## Sources

- [[sources/bitsquid-validating-materials-lights]]
