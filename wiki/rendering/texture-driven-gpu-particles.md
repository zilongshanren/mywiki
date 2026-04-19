---
tags: [渲染, 粒子, GPU, anno, vertex-shader]
date: 2026-04-19
sources: 1
---

# Texture 驱动的 GPU 粒子（Anno 1800 版）

[[thomas-poulet]] 在 [[sources/thomas-poulet-anno-1800-frame|Anno 1800 帧分析]] 里看到的粒子系统走了一条**极度精简**的路线：geometry 只是一个 quad，所有动画参数都**预烘焙进纹理**，在 vertex shader 里读表算结果。400+ 粒子全由 `DrawIndexedInstanced` 一把过。

## 数据结构

三类缓冲：

- **ParticlePerConfigData** (最多 128 个系统类型)：每种粒子系统一行，存动画参数——flipbook（文中叫 movie）的速度 / 帧数、粒子总数、粒子寿命、bounding box、emitter 位置。
- **ParticlePerConfig** (最多 512 个系统实例)：每个正在播放的系统实例一行，存 transform matrix、颜色 modifier、scale、age。
- **ParticlePerDrawCall**：看起来只有 flag。

每个 draw 传一个 root constant，三个 index：系统类型 → 系统实例 → drawcall。shader 靠这三把钥匙从 buffer 里查出所有参数。

## 四张「时间 × 粒子」纹理

这是整个方案的核心。四张纹理各自负责一个动画维度：

- `ParticleColorTex` — 颜色随时间
- `ParticlePositionTex` — 位置随时间
- `ParticleRotationTex` — 旋转随时间
- `ParticleScaleTex` — 缩放随时间

纹理布局：**一行一个粒子，一列一个时间样本**。vertex shader 用（粒子 index, 当前 frame）坐标做纹理采样，就拿到当前瞬时的全部动画量，不需要 CPU 发任何更新。

另一张 `ParticleBornTex` 存每粒子的生命期 offset，让粒子在 emission window 内错开出生。

## Vertex Shader 的工作

拿到 quad 的两个顶点输入坐标后，vertex shader 做约 350 条指令：

1. 用 instance ID 查出是哪一颗粒子；
2. 查 config 得到寿命、bbox、system transform；
3. 用 (instance, age/frame) 查四张动画纹理得到颜色/位置/旋转/缩放；
4. 应用到 quad 顶点上，输出 world-space 三角形。

死掉但未到下个 emission window 的粒子会采样到 undefined 数据，shader 把它们踢出视锥——实际可见 bug 几乎没有，[[thomas-poulet]] 也在文中指出「用寿命显式 collapse quad 会更干净但收益微乎其微」。

## 和其他粒子系统的对比

- **对比 [[ecs-particle-system-c|CPU ECS 粒子]]**：完全不需要 CPU 每帧 integrate。
- **对比 [[particle-custom-vertex-streams|Unity custom vertex stream]]**：思路接近（把动画数据塞进 attribute 让 GPU 算），但 Anno 把动画预算好并存进 texture，进一步省 CPU。
- **对比真正的 GPU simulation（UE Niagara / Cascade 的 GPU particle）**：它们在 compute 里算速度/加速度，动画「模拟」；Anno 这套是**动画烘焙好的播放器**，不做真实物理。对烟囱烟雾这种设计好的艺术动画来说足够，且便宜得多。

关键启示：**当 motion 是艺术家设计好的曲线，不是物理模拟时，「每帧一个 CPU sim step」是浪费。把时间轴离散化成一张 2D 纹理，让 vertex shader 做 lookup 就够了。**

## Sources

- [[sources/thomas-poulet-anno-1800-frame]]
