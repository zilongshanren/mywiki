---
tags: [source, shader, toon, terrain, urp, unity]
date: 2026-04-19
sources: 1
---

# Toon Shaders Pro for URP — Toon Terrain（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 的 *Toon Shaders Pro for URP* 里的 **Terrain 版 toon shader**，去掉 Base Color/Texture（改为从 terrain splatmap 拉 albedo），新增 *Use Stochastic Texturing*——用三次 UV 偏移采样消除 terrain 的 tiling 痕迹，代价是三倍采样带宽。其余 Diffuse / Specular / Rim 参数与普通 Toon shader 同构。

## 摘要

Unity URP terrain 本身是"一个光照壳 + 多张 splatmap 控制贴图混合"的架构。把这条管线的 albedo 替换成 toon 光照很直接：去掉 shader 本身的 base color，沿用 terrain 系统自动喂进来的 4 层材质。Ilett 额外加了 **stochastic texturing**（沿 Shopf 2017 思路：三次不同 UV 偏移采样后按哈希权重混合）来打散"看着像瓷砖"的视觉。Ambient Light Strength 独立暴露（因 terrain 通常没有 realtime 额外灯光，需要可调的环境亮度 floor）。与普通 Toon 相比无 Workflow Mode / Normal Mapping（terrain 法线来自高度场）、无 Alpha Clip。

## 关键要点

- **albedo 来源不同**：从 terrain 的 splatmap + layer textures 拉，shader 不管 base color。
- **Use Stochastic Texturing**：三倍采样消 tiling；terrain shader 常见需求。
- **Ambient Light Strength**：面板上补了 ambient floor 参数——terrain 场景常只有一盏方向光。
- **Diffuse / Specular / Rim**：共享与 Toon shader 同构的 smoothstep 阈值机制。
- **无 Normal Map**：细节依赖 terrain 本身的 normal，shader 不再叠 detail normal。

## 链接到的概念

- [[cel-shading-pipeline]]
- [[stochastic-texture-sampling]]
- [[terrain-splatmap-shader-graph]]

## 原文

- 链接：<https://danielilett.com/toon-shaders-pro/toon-terrain/>
- 本地：`raw/articles/danielilett.com/2026-01-01_toon-shaders-pro-for-urp-toon-terrain.md`
