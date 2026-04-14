---
tags: [渲染, unreal, frame-breakdown, deferred-rendering, 后处理]
date: 2026-04-14
sources: 3
---

# Unreal Engine 4.17 一帧的全流程拆解

[[kostas-anagnostou|Kostas Anagnostou]] 2017 年受 Adrian Courrèges 的 *GTA V graphics study* 启发，用 [[renderdoc|RenderDoc]] 抓了一个 UE4.17.1 编辑器里的代表性场景（几只静态 / 动态道具、若干光源、体积雾、透明物、粒子）的帧，对照引擎源码逐 pass 走了一遍。三篇连载构成了 wiki 里最完整的一份 **Unreal 默认 deferred 管线**第一手记录，可作为 UE 管线的参考地图。

本页是 Anagnostou 三篇 *How Unreal Renders a Frame* 系列的合并概括——顺着 GPU 时序走，每一段记一个关键设计决策。

## 前置：粒子模拟与 Z-prepass

帧起点是 **ParticleSimulation** compute pass，先把 GPU 粒子的位置 / 速度写到一张 RGBA32F + 一张 RGBA16F 的 RT 里（此时还没深度，所以「需要和深度碰撞」的粒子要等到后面再跑一次）。接下来是 **PrePass**，UE 把所有 opaque 道具写到一张 R24G8 深度 buffer——**reverse-Z 约定，近平面映射到 1，远平面映射到 0**，用来提高远处精度。这一 pass 由 DBuffer decal 触发，副产品被之后的 occlusion 查询、SSR、Hi-Z 反复复用。

## Occlusion：硬件 query + 分组 + 懒回读

UE 的遮挡剔除走传统 [[hardware-occlusion-query|硬件 occlusion query]] 路线。为控住 query 的 draw-call 开销，它分两级：先给每个道具发 **IndividualQueries**；一旦上一帧判出「完全不可见」，把它丢进 **GroupedQueries**——每个 group 用最多 8 个道具的 AABB 并集做一次查询，若下一帧 group 整体可见再拆回单体。静止相机下这个路径能把 query 数直接砍到 1/8。CPU 侧用标准的「延后若干帧读 query 结果」的办法回避 GPU-CPU 同步点——代价是相机快速移动时会有 popping。局部光源的 [[shadow-frustum-culling|shadow frustum]] 也走同一套：可见才生成对应的 shadow map。

Occlusion 之后立刻生成 **Hi-Z mip chain**（R16F，min 降采样因 reverse-Z），供后面 SSR / AO 共用——这和 [[hierarchical-z-buffer|HZB]] 的经典用途一致。

## Shadow map：按光源类型走三条路

UE 按 *Stationary / Movable / Static* 三种光源类型走不同的 shadow map 策略：

- **Directional Light**：一张 3×1 的 R16_TYPELESS atlas（cascaded shadow map 的三个 split 横向打包），**null pixel shader 写 depth**，速率翻倍。每帧 clear 整图，所以没有 staggered split update。
- **Stationary local light + dynamic prop**：**per-object shadow map**，每个 dynamic 道具一块 tile 存在一张 atlas 里。
- **Movable local light**：传统立方体贴图，但对静态 / stationary 部分 **shadow map caching**——第一次渲染后缓存立方体贴图的 6 个面，之后只在上面叠加 dynamic 道具的 depth。动画 light 时 cached 部分才每帧重绘。
- **Static light**：不出现在任何 draw-call list 里，完全烘焙进 lightmap。
- **几何着色器选面**：cubemap pass 用一个 GS 一次写 6 个面，减少 draw call 数。

## Light assignment：先建 cluster，但只给部分 pass 用

一个 compute shader pass（**ComputeLightGrid**）把场景灯光分配到 view-space 的 3D 网格——屏幕空间 64×64 tile，z 方向 32 个指数切分 slice（近平面略向后推，避免前端 cell 过密）。网格的 29×16×32 维度随分辨率变。光源索引先用链表写入，然后一个 **Compact** pass 把它转成紧凑数组。这套 cluster 数据**之后只被 volumetric fog、environment reflection、translucency** 三个 pass 使用；**solid geometry 的直接光照并没有用它**，而是仍然走逐光源 deferred draw。这是个值得记住的细节：UE4 并不是一个纯 [[tiled-deferred-shading|tiled/clustered deferred]] 渲染器，只是把 cluster 当缓存给一部分 consumer。

## Volumetric fog：froxel volume + TAA

体积雾用 compute shader 写三张 volume texture，tile 尺寸 8×8，128 个指数 z-slice，做法和 Assassin's Creed IV / Frostbite 的 [[volumetric-fog-froxels|froxel volumetric fog]] 基本一样，分三个 pass：

1. **InitializeVolumeAttributes**：把 scattering / absorption 参数写进 volume。
2. **LightScattering**：合并 directional + sky + local light 贡献到每个 froxel，用 history volume 做时间滤波（时间上的 TAA）。
3. **FinalIntegration**：沿 z 方向 raymarch 累加 transmittance 和 scattered light，写回 volume。后面 opaque 上雾时，直接用表面位置采这张 volume 就行。

## G-prepass 与一些小细节

**G-prepass** 重绘所有 opaque 道具（含 skydome——因为有 Z-prepass 了，skydome overdraw 会被剔掉），写一组 [[gbuffer-layouts|G-buffer]] RT：depth 只做 z-test、stencil 标记 opaque 像素。如果 velocity 要写入 gbuffer，layout 会被重排。

Anagnostou 还注意到引擎给 opaque 道具准备了**三张 mipmap atlas**——缓存 irradiance / shadow / surface normal——dynamic Rock 之外的所有静态道具都是从这里采光照信息的。

## AO、直接光照与 translucency lighting volume

AO 分两个 pass：先一张 quarter-res（基于降采样 normal + Hi-Z + 随机向量纹理做 [[hbao-interleaved-sampling|interleaved sampling]]），再一张 full-res，时间上靠 frame jitter「超采样」。

直接光照把光源分两组：

- **NonShadowedLights**：场景里的 non-shadowing 灯 + 粒子系统的 simple light。**当非阴影灯数 > 80**，UE 切到 [[tiled-deferred-shading|tiled deferred]] compute pass 一次性处理——这是 UE4 里 classic deferred 被 tiled 接管的唯一触发点。
- **ShadowedLights**：每盏 shadowcasting 灯走三段式：
  1. **ShadowProjectionOnOpaque**——把 shadow map 投到一张屏幕空间 shadow buffer（RGBA8）。
  2. **InjectTranslucentVolume**——把 shadowed lighting 注入 **2 组 64³ RGBA16F volume**（近相机 / 远相机双 cascade，存 SH 系数 + 近似光方向）。这套 volume 是后面透明物打光的基础。
  3. **StandardDeferredLighting**——用 screen shadow buffer 蒙板做最终 deferred lighting，累加到 SceneColorDeferred。

所有 shadowing 灯复用**同一张屏幕 shadow buffer**，处理一盏清一次相关区域省显存。

## 屏幕空间反射与大气

**Screen-space reflection** 用 Hi-Z 加速 raymarch（根据粗糙度选 mip 层，粗糙表面用粗 mip），每帧 jitter ray start + TAA 提升质量；采色用**上一帧**的 scene color，所以反射里能看到体积雾、透明物、粒子。ReflectionEnvironment compute pass 把 SSR 和两颗 reflection probe 的 mipmapped cubemap 混进主 RT——reflection probe 只在游戏启动时烘焙，且**只捕静态几何**。

之后是 full-res 的大气散射（precomputed transmittance / irradiance / inscattering，Bruneton 风格）和指数雾 + light shaft。Light shaft mask 先低分辨率算出，走 TAA 再 blur。

## 透明物与折射

透明物按 blend 顺序走，使用之前生成的 translucency lighting volume + atmosphere texture + baked lightmap + reflection probe 采光。**粒子**写到一张单独的 full-res RT。**折射**的做法特殊：支持折射的透明物和粒子**再渲染一次**，把 distortion vector 写到一张 buffer，stencil 标记受影响像素；`DistortionApply` pass 读当前 main RT + distortion 合成折射结果；最后把折射纹理 copy 回主 RT，stencil 当 mask。

## 后处理链

帧尾做 **TAA → motion blur → auto-exposure → bloom → tonemapping**。TAA 分成两个 pass：一个走非 stencil 像素（blend factor 动态，依亮度 / 距离）、一个走 stencil 像素（固定 0.25 blend，减轻快速粒子的 ghosting）。Motion blur 先做 velocity dilation。Auto-exposure 用 compute shader 算场景亮度直方图——天然能跳掉最暗 / 最亮像素求更稳的均值。Bloom 是 Gaussian downscale + upscale combine。最后 `PostProcessCombineLUTs` 生成 32³ RGB10A2 colour grading LUT，`Tonemapper` 合并 bloom、应用曝光、过 LUT 输出最终像素。

## 记住的大方向

- UE4 默认 renderer 对**画质优先**——大量 precompute（lightmap、reflection probe、atmospheric LUT）+ 时间积累（TAA for volumetric / SSR / AO / shadow）。
- **Cluster / tiled 路径只是点缀**，而不是 solid opaque 的主通道；solid 仍是 per-light deferred。
- **Occlusion 是首个需要盯着成本的地方**——道具多而遮挡机会少时 query 数量会爆。
- **Shadow caching** 对 stationary 和未动 movable 灯都能省下一大截 shadow map 成本。
- **Refraction 代价是「透明物 / 粒子再绘一次」**——场景里透明物多时这块会吃掉一部分 budget。

## 相关

- [[deferred-rendering]]
- [[tiled-deferred-shading]] —— UE4 在 >80 非阴影灯时切换的路径
- [[volumetric-fog-froxels]]
- [[hierarchical-z-buffer]]
- [[occlusion-culling]]
- [[cached-shadowmaps]]
- [[temporal-antialiasing]]
- [[gbuffer-layouts]]
- [[bloom-threshold-blur-composite]]
- [[color-lut]]
- [[shadow-mapping-basics]]
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-unreal-frame-part1]]
- [[sources/interplay-unreal-frame-part2]]
- [[sources/interplay-unreal-frame-part3]]
