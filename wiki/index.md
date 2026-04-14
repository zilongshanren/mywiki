---
tags: [index]
date: 2026-04-14
sources: 146
---

# 知识库索引

本知识库涵盖**软件设计哲学 · 实时渲染 · 游戏引擎 · 计算机体系结构 · 编程语言基础**五大主题。入口页：[[overview]]。品味训练指南：[[taste-development]]。

## 软件设计（wiki/software-design/）

核心概念与框架，源自 John Ousterhout 的 APoSD。

| 文章 | 一句话描述 |
|---|---|
| [[complexity]] | 复杂性的定义与整体框架，软件设计的核心敌人 |
| [[change-amplification]] | 复杂性症状之一：改动需要触及多处 |
| [[cognitive-load]] | 复杂性症状之二：需要知道太多东西 |
| [[unknown-unknowns]] | 复杂性症状之三：不知道自己不知道（最危险） |
| [[dependencies]] | 复杂性根源之一：代码间的相互牵连 |
| [[obscurity]] | 复杂性根源之二：重要信息不显而易见 |
| [[red-flags]] | 识别设计问题的信号集合 |
| [[tactical-programming]] | 短视的「让它工作」心态 |
| [[strategic-programming]] | 投资心态，优秀设计恰好也能工作 |
| [[tactical-tornado]] | 外部化成本的高产出工程师 |
| [[zero-tolerance]] | 对复杂性增量的日常纪律 |
| [[continuous-design]] | 软件设计是持续过程，不是一次性活动 |
| [[modular-design]] | 模块化的真正目标是认知隔离 |
| [[deep-modules]] | 强大功能 + 简单接口的设计理想 |
| [[shallow-modules]] | 接口复杂度接近实现复杂度的反模式 |
| [[classitis]] | 「类越多越好」的系统性设计疾病 |
| [[interface-vs-implementation]] | 接口是成本，功能是收益 |
| [[abstraction]] | 省略不重要细节的简化视图 |
| [[false-abstraction]] | 省略了重要细节的「简洁」陷阱 |
| [[information-hiding]] | 把设计决策藏进实现——深模块的引擎 |
| [[information-leakage]] | 同一份知识分散在多个模块 |
| [[temporal-decomposition]] | 按时间顺序切模块的陷阱 |
| [[smooth-window-resize]] | 桌面 GUI 平滑窗口缩放：swapchain、WM、事件循环的同步体检 |
| [[rust-gui-ecosystem]] | Rust GUI 生态的多峰现状与 linebender（Druid / Xilem / Vello）路线 |
| [[reactive-ui-rust]] | Rust 下反应式 UI 架构：lens、Elm、Xilem 的假设 |
| [[c-opaque-struct-modules]] | C 语言下的不透明结构模块与伪 friend 技巧（云风） |
| [[c-interface-oop]] | C 语言的接口表 + data 组合式 OOP（云风） |
| [[simple-cpp-mark-sweep-gc]] | 200 行的 C++ 标记清除 GC 玩具（云风） |
| [[c-serialization-metadata]] | 基于自定义元信息的 C 结构序列化与图合并算法（云风） |

## 编程语言基础（wiki/programming-languages/）

SICP 及 Lambda 演算传统的核心概念。

| 文章 | 一句话描述 |
|---|---|
| [[elements-of-programming]] | 编程语言的三要素：原子、组合、抽象 |
| [[substitution-model]] | 纯函数求值的思维工具 |
| [[applicative-vs-normal-order]] | 求值时机的两种设计选择 |
| [[environment]] | 名字→值的 frame chain |
| [[procedural-abstraction]] | 过程作为黑盒 |
| [[lexical-scoping]] | 代码结构决定作用域 |
| [[closure]] | 函数 + 定义时环境 |
| [[recursive-vs-iterative-process]] | 递归语法 vs 递归过程 |
| [[tail-call-optimization]] | 尾调用优化与语言设计分歧 |
| [[higher-order-functions]] | 函数作为一等公民 |
| [[lambda-calculus]] | 计算的通用数学模型 |
| [[order-of-growth]] | 算法增长阶的粗描述 |
| [[fast-exponentiation]] | 分治思想的经典例证 |
| [[probabilistic-algorithms]] | 用概率正确性换可行性 |
| [[functions-as-vectors]] | 函数作为无限维向量：Fourier / 球谐的统一视角 |
| [[cpp-runtime-reflection]] | libclang 元程序生成 C++ 运行时类型表 |
| [[swap-and-pop-removal]] | 无序数组删除的 swap-and-pop 技巧：O(n) → O(1) |

## 计算机体系结构与系统（wiki/computer-systems/）

CAQA + CSAPP 的底层视角。

| 文章 | 一句话描述 |
|---|---|
| [[amdahls-law]] | 并行加速的理论上界 |
| [[flynn-taxonomy]] | 指令流 × 数据流的架构分类 |
| [[cpu-performance-formula]] | CPU Time = IC × CPI / Clock Rate |
| [[latency-vs-throughput]] | 两种性能指标的权衡 |
| [[memory-hierarchy]] | 跨越 5 个数量级的存储分层 |
| [[locality-principle]] | 缓存层次的理论基础 |
| [[aos-vs-soa]] | 内存布局决定 cache 利用率 |
| [[cache-friendliness]] | 让代码与缓存对齐 |
| [[dennard-scaling]] | 晶体管缩放规律的崩塌 |
| [[power-wall]] | 频率停滞的物理原因 |
| [[mttf-reliability]] | 可靠性的量化指标 |
| [[bits-and-context]] | 信息 = 比特 + 上下文 |
| [[compilation-pipeline]] | C 编译的四阶段 |
| [[virtual-memory]] | 进程独立连续地址空间幻觉 |
| [[sse-tricks]] | 跨代 SSE/SSE2 的非正交性补洞技巧 |
| [[adaptive-arithmetic-coding]] | 二元自适应模型 = 多通道 IIR 滤波器，rANS 让多元复活 |
| [[non-cryptographic-hash]] | 现代非加密哈希演进与 Burst codegen 差异 |
| [[rapidhash]] | wyhash 后继的极简 64 位哈希函数 |
| [[compiler-interference-analysis-bug]] | MSVC 把两个活跃临时量塞到同一栈槽的 codegen bug |
| [[linear-allocator]] | O(1) 推指针式分配器，帧内临时数据的默认选择 |
| [[cuda-memory-hierarchy]] | CUDA kernel 可见的 5 种内存：register/local/shared/global/constant |
| [[faster-math-functions]] | 无 libm 场景下手写 sin/cos/exp/pow——minimax 多项式，不是 Taylor |
| [[fearless-simd]] | Rust 下可移植 SIMD 的双层 trait 方案与 runtime 选档难题 |
| [[calling-conventions-x86]] | x86 32 位 cdecl / stdcall / fastcall 三路汇编 diff |
| [[linux-graphics-stack-dri]] | Linux 图形栈 DRI/DRM/KMS 的命名迷雾与真实分层 |
| [[malloc-wrapper-debug]] | 给 malloc 加壳：狗牌、泄漏检测与 __FILE__/__LINE__ 定位 |

## 游戏引擎（wiki/game-engines/）

Game Engine Architecture（Jason Gregory）的核心概念。

| 文章 | 一句话描述 |
|---|---|
| [[game-engine]] | 什么是游戏引擎 |
| [[data-driven-architecture]] | 引擎 vs 游戏专用软件的分水岭 |
| [[soft-real-time]] | 偶尔违反时限是可接受的 |
| [[engine-layering]] | 单向依赖是第一纪律 |
| [[unity-vs-unreal]] | 两种引擎设计哲学 |
| [[engine-evolution]] | 从 BSP 到 Lumen/Nanite |
| [[gknext-renderer]] | gameknife 2024 年启动的 Vulkan 实时光追开源引擎，YearOne 总结 |
| [[gkengine]] | gameknife 2013–2015 的跨平台独立引擎，CryEngine 风格，gkNextEngine 的前身 |
| [[game-physics-engine]] | 约束式刚体物理引擎的三段流水线：broadphase、collision detection、sequential impulse resolution |
| [[collision-detection-gjk-epa]] | 凸几何碰撞检测三件套：GJK 判相交、EPA 补 contact、MPR 一步到位 |
| [[component-entity-data-binding]] | 组件实体模型中的 I/O 端口式数据绑定（Evan Todd 2011） |
| [[game-engine-vfs]] | 游戏引擎虚拟文件系统：Linux VFS 简化版与 auto fallback |

## 实时渲染（wiki/rendering/）

Real-Time Rendering + Custom SRP 的渲染管线知识。

| 文章                                    | 一句话描述                                                              |
| ------------------------------------- | ------------------------------------------------------------------ |
| [[rendering-pipeline]]                | 四阶段的瓶颈驱动并行系统                                                       |
| [[bottleneck-analysis]]               | 找瓶颈只优化瓶颈                                                           |
| [[tbdr-vs-imr]]                       | 两种 GPU 架构对比                                                        |
| [[draw-call]]                         | CPU 状态 setup 是主成本                                                  |
| [[culling]]                           | 分层过滤的 CPU 剔除                                                       |
| [[batching]]                          | 减少 DrawCall 或状态切换                                                  |
| [[mvp-transform]]                     | 三矩阵变换链                                                             |
| [[coordinate-spaces]]                 | Model/World/View/Clip/NDC/Screen                                   |
| [[z-buffer]]                          | 每像素深度缓冲                                                            |
| [[z-fighting]]                        | 深度精度不足的闪烁                                                          |
| [[reversed-z]]                        | 利用 float 精度分布改善远平面                                                 |
| [[perspective-correct-interpolation]] | 透视校正插值                                                             |
| [[rasterization]]                     | 三角形 → fragment                                                     |
| [[aliasing]]                          | 走样与反走样                                                             |
| [[msaa-ssaa]]                         | 两种超采样对比                                                            |
| [[triangle-primitives]]               | 三角形为什么是基本图元                                                        |
| [[fragment-shader]]                   | 每 fragment 的着色                                                     |
| [[early-z-late-z]]                    | 早期/晚期深度测试                                                          |
| [[hsr-tbdr]]                          | TBDR 特有的精确隐面消除                                                     |
| [[alpha-blending]]                    | 半透明混合的顺序依赖                                                         |
| [[stencil-buffer]]                    | 8-bit 模板缓冲的低成本效果                                                   |
| [[overdraw]]                          | 过度绘制的代价与对策                                                         |
| [[deferred-rendering]]                | G-Buffer + 统一光照 pass                                               |
| [[color-space]]                       | RGB 值无意义——色彩空间才赋予意义                                                |
| [[alpha-compositing]]                 | Porter-Duff over 与预乘 α                                             |
| [[pinhole-camera]]                    | 虚拟相机的物理本体与 cos⁴ 暗角                                                 |
| [[thin-lens-model]]                   | 焦距 / 光圈 / 景深 / bokeh 的物理来源                                         |
| [[local-tonemapping]]                 | 局部色调映射的动机与方法谱                                                      |
| [[exposure-fusion]]                   | Mertens Laplacian 金字塔分尺度融合算法                                       |
| [[laplacian-pyramid]]                 | 多分辨率图像分解的基础工具                                                      |
| [[iir-filter-deconvolution]]          | 递归滤波器精确反演卷积模糊                                                      |
| [[poisson-disk-sampling]]             | 渐进 Poisson 采样序列与渲染用途                                               |
| [[gpu-printf-debugging]]              | 用 UAV append buffer 实现 shader printf                               |
| [[unorm-float-conversion]]            | UNORM8 → float32 的精确两乘法构造                                          |
| [[sampling-theorem-sinc]]             | sinc 是无穷节点 Lagrange 插值的极限                                          |
| [[pineda-edge-rasterization]]         | 1988 年的边方程算法是现代 GPU 光栅化的根                                          |
| [[hierarchical-rasterization]]        | 用 tile 角点上下界提前剔除空块                                                 |
| [[triangle-setup]]                    | 光栅化前为边方程算常量的硬件阶段                                                   |
| [[compute-vs-raster-points]]          | 朴素 compute shader 比硬件点光栅化快 1.5-10×                                 |
| [[image-resampling-filters]]          | Bilinear / Bicubic / Mitchell-Netravali 与半 texel 偏移考古              |
| [[cached-shadowmaps]]                 | 级联阴影的帧间相干性缓存                                                       |
| [[temporal-antialiasing]]             | TAA 的 jitter + reprojection + rectification 全流程                    |
| [[motion-vectors]]                    | 屏幕空间运动矢量——所有 temporal 技术的基础                                        |
| [[taa-history-rectification]]         | color clamping 与 depth/stencil/velocity rejection 的组合拳             |
| [[tiled-light-prepass]]               | ROTR Foundation 引擎的 thin G-Buffer + 二次几何提交方案                       |
| [[hbao-interleaved-sampling]]         | 把 HBAO 拆成 16 个 4×4 块并行、再 blur 合并的 cache-friendly trick             |
| [[depth-aware-upsampling]]            | 用 stencil 分派 simple/complex shader 的半分辨率 upsample                  |
| [[fizzle-lod-fading]]                 | 用 discard 噪声替代 alpha blending 的 LOD 过渡方案                           |
| [[volumetric-fog-froxels]]            | frustum-aligned 3D 格网上的 compute-based 体积光流水线                       |
| [[spectral-rendering]]                | 光谱渲染：把 RGB 三元组换成波长积分的现代实时方案                                        |
| [[fourier-srgb-spectral-upsampling]]  | Fourier sRGB：sRGB 纹理到反射率谱的 BC1 可压缩上采样                              |
| [[hero-wavelength-spectral-sampling]] | 波长分层抖动 + 光源谱 CDF LUT 的 MC 采样策略                                     |
| [[spectral-brdf]]                     | 「base color + 纯白」两个权重把 PBR BRDF 改造成光谱 BRDF                         |
| [[polynomial-root-finding-gpu]]       | GLSL 里的 bracketed Newton bisection 实现与高度优化                         |
| [[register-spilling-avoidance]]       | shader 寄存器溢出的识别与系统化规避手册                                            |
| [[projected-solid-angle-sampling]]    | 球形面光源 + 漫反射表面的实时零方差采样（cut disk 分解）                                 |
| [[environment-probe-placement]]       | 反射探针辅助放置：候选生成 + 相似度聚类 + 美术挑选                                       |
| [[quasi-monte-carlo]]                 | 确定性点列换近线性收敛的 QMC 基础                                                |
| [[stratified-sampling]]               | 分层采样：便宜的负相关方差缩减                                                    |
| [[low-discrepancy-sequence]]          | Halton / Sobol 等 QMC 常用点列                                          |
| [[greedy-voxel-meshing]]              | Minecraft 风 voxel 世界的经典网格化算法                                       |
| [[voxel-ambient-occlusion]]           | mesh 阶段烘焙四级 AO 的免费方案                                               |
| [[compact-vertex-format]]             | 每顶点 8 字节的位打包技巧                                                     |
| [[spherical-harmonics]]               | 球面上的 Fourier 基：L2 压掉整张 diffuse envmap                              |
| [[jump-flooding-algorithm]]           | GPU 距离场：对数趟指数步长的 3×3 洪填                                            |
| [[oklab-color-space]]                 | 两次矩阵乘一次立方根得到的感知均匀色彩空间                                              |
| [[3d-rotation-math]]                  | Euler / Axis-Angle / 四元数：3D 旋转的数学形式                                |
| [[layered-grid-noise]]                | 黄金角旋转 + 多层 shift/scale 的廉价伪随机散布                                    |
| [[shadow-mapping-basics]]             | Shadow mapping 入门：hard / soft / bias / PCF / Phong                 |
| [[microfacet-brdf]]                   | $D\,F\,G$ 微表面 BRDF + 多次散射能量补偿                                      |
| [[physically-based-shading]]          | PBR 着色的整体框架与 SIGGRAPH course 脉络                                    |
| [[normal-map-blending]]               | Reoriented Normal Mapping：最短弧四元数混合法线贴图                             |
| [[occlusion-culling]]                 | HZB 查询 vs SPU 软光栅：两种动态遮挡剔除方案                                       |
| [[hierarchical-z-buffer]]             | max-downsample 的 Z 金字塔：保守遮挡查询                                      |
| [[d3d12-resource-binding]]            | D3D12 的描述符、堆、资源状态跨线程管理四件套                                          |
| [[needlets]]                          | 球面 wavelet 基，SH 遮挡振铃问题的替代方案                                        |
| [[procedural-rendering-ps2]]          | PS2 VU + DMA chain 的过程式几何管线                                        |
| [[display-edid-colorspace]]           | 从 EDID 读出显示器原生 primaries + 白点                                      |
| [[custom-srp]]                        | Catlike Coding 教程系列                                                |
| [[scriptable-render-pipeline]]        | Unity 的可编程渲染管线                                                     |
| [[render-graph]]                      | SRP 的声明式编排系统                                                       |
| [[color-lut]]                         | color grading 查找纹理                                                 |
| [[debug-visualization]]               | Rendering Debugger 集成                                              |
| [[gpu-image-editor-brush]]            | GPU 图像编辑器的缩放平移 + fragment shader 笔刷（Papaya vs GIMP）                |
| [[gpu-hazard-tracking]]               | D3D12/Vulkan 为何要求用户自己声明 barrier                                    |
| [[gpu-fence-timeline-semaphore]]      | GPU→CPU 单调计数器作为资源生命周期基础设施                                          |
| [[buffer-renaming]]                   | 老驱动的隐式 buffer 版本化与现代 API 的拆除                                       |
| [[frame-profiler-overlay]]            | 帧内性能剖析器浮层：即开即看的一帧耗时分解                                              |
| [[volumetric-video-playback]]         | 体积视频（全息视频）在 WebXR 跨设备回放的工程实践                                       |
| [[shaping-functions]]                 | step/smoothstep/lerp/sin/frac 等着色器塑形函数与时间动画                        |
| [[planar-mapping]]                    | 用顶点位置的两个分量直接当 UV：最简单的程序化 UV 生成                                     |
| [[texture-dissolve]]                  | 纹理驱动的 clip 溶解 VFX + HDR 边缘发光                                       |
| [[sdf-2d-primitives]]                 | 2D SDF 基元（圆、矩形）、空间变换与可视化                                           |
| [[sdf-ray-marched-shadows]]           | 用 SDF sphere-trace 做 2D 软阴影：iq 单行技巧的完整拆解                           |
| [[draw-procedural-gpu]]               | Unity Graphics.DrawProcedural：GPU-driven 渲染的最小入口                   |
| [[urp-volume-post-processing]]        | URP 基于体积的后处理系统（PPv3）的架构与使用                                         |
| [[blit-render-feature]]               | 在 URP 无扩展点时通过 ScriptableRendererFeature 做自定义全屏后处理                  |
| [[uv-manipulation-nodes]]             | Shader Graph 中 Tiling/Offset、Rotate、Flipbook、Polar 等 UV 操作节点       |
| [[sampler-filter-wrap-modes]]         | 纹理采样器的 Point/Linear/Trilinear 与 Repeat/Clamp/Mirror 的语义与陷阱         |
| [[crt-shader-effects]]                | 把复古 CRT 拆解为 5 个正交 shader trick 的 breakdown                         |
| [[scene-color-depth-nodes]]           | Shader Graph 里 Scene Color / Scene Depth 节点的跨管线行为与深度相交技术           |
| [[particle-custom-vertex-streams]]    | 通过 TEXCOORD 把 AgePercent / StableRandom / Custom Data 传进 shader    |
| [[shader-vector-math-primer]]         | Shader 需要的那点向量数学：dot/cross/normalize 的几何直觉                         |
| [[unity-grabpass-blur]]               | Unity GrabPass + 可分离 Gaussian blur 的入门实现与教学取舍                      |
| [[texture-encoded-state]]             | 把 per-pixel 状态（时间戳/强度）编码进纹理通道供 shader 消费                           |
| [[diamond-square-noise]]              | Diamond-Square 有状态噪声与 compute shader 加速实现                          |
| [[deferred-grass-shader]]             | 延迟管线下的草地方案：alpha cutout + tessellation + geometry shader           |
| [[diffuse-lighting-lambertian]]       | Lambert 漫反射：所有光照模型的共同基座与 Unity 的两条实现路径                             |
| [[unity-surface-shaders]]             | Unity 内建管线的 Surface Shader 抽象：填 surf 函数，Unity 生成所有变体               |
| [[shaderlab-hlsl-basics]]             | URP shader 的 ShaderLab + HLSL 两层结构最小骨架                             |
| [[retro-rendering-techniques]]        | PS1/N64 复古渲染清单：顶点吸附、色深量化、3-point 采样、vertex lit                     |
| [[dither-alpha-clipping]]             | 用 Bayer 矩阵 discard 伪造半透明，规避 alpha blending 的排序地狱                   |
| [[spectral-zucconi-rainbow]]          | Branchless 的波长→RGB 拟合（Zucconi 改进 GPU Gems bump 方案）                 |
| [[diffraction-grating-shader]]        | CD-ROM 彩虹反射：grating 方程 + 从 UV 算切向 + spectral_zucconi6              |
| [[fast-translucency-wraplight]]       | Barré-Brisebois / Frostbite 2 的廉价假 SSS：反向光 + subsurface distortion |
| [[volumetric-raymarching-intro]]      | Volumetric raycasting 到 raymarching：把 cube 当 portal 做体积渲染          |
| [[journey-sand-specular]]             | Journey 沙丘高光分解：Fresnel rim + Blinn-Phong ocean specular            |
| [[visibility-buffer]]                 | 用 thin-gbuffer + 反查替代传统 G-Buffer，化解高 overdraw 代价                   |
| [[hybrid-raytracing-pipeline]]        | VB primary + 短距离硬件光追 secondary + cache 远场                          |
| [[bindless-rendering]]                | CPU 只组织 GPU 只索引，让着色器自由访问任意资源                                       |
| [[analytical-antialiasing]]           | 已知形状数学方程时，在 shader 里按 SDF 淡出一像素的反走样                                |
| [[metal-api-overview]] | Metal 的对象模型：device/queue/buffer/encoder/library/pipeline-state |
| [[metal-shading-language-basics]] | MSL 函数限定符、属性限定符与插值语义的最小讲义 |
| [[cametal-layer-drawable]] | CAMetalLayer / CAMetalDrawable——iOS 上 swapchain 的 Core Animation 版本 |
| [[prebaked-corner-occlusion]] | SSAO 之前的角落遮蔽：lightmap 烘焙、UE1 的 bug 成为 feature、Sims 4 手贴 AO mesh |
| [[painted-foliage-bent-planes]] | Diablo 3 两张三角形 + hand-painted alpha 做细剪影树，固定相机反哺美术技巧 |
| [[normal-decal-edge-blending]] | Fallout 3 / CryEngine 的 decal 壳技巧：把破损边缘从主 mesh 解耦到一层薄几何 |
| [[chromatic-aberration-post]] | 三通道 UV 偏移后处理：真实色差 vs 数字 glitch，Teleglitch / Deadlight 案例 |
| [[color-banding]]                     | 色带根源 + Jimenez 一行 GLSL dither + 大厂去带方案横评                            |
| [[perceptual-colormaps]]              | matplotlib 感知均匀 colormap 烘成 .cube 1D LUT 给 DaVinci Resolve |
| [[tangent-free-normal-mapping]] | 用 `dFdx`/`dFdy` 在 pixel shader 里构造 TBN，免顶点存切线 |
| [[shader-prototyping-tools]] | FX Composer / RenderMonkey / Unity / SharpDX 原型工具横评 |
| [[sharpdx-assimp-pipeline]] | C# + D3D11 的 XNA 式原型：SharpDX + Assimp 模型加载 |
| [[conservative-depth]] | `SV_DepthGreaterEqual` / `[earlydepthstencil]`：两条 Early-Z 救援通道 |
| [[virtualized-volume-textures]] | Karis：2D 虚拟纹理和 SVO 思路扩展到 irradiance volume |
| [[tiled-light-culling]] | Karis：把 specular cone + 能量守恒引入 tile 级光源剔除 |
| [[sparse-shadows-cone-tracing]] | Karis 2012：diffuse 走 shadow map，远 specular 走 cone trace——UE5 Lumen 的起点笔记 |
| [[instant-radiosity-vpl]] | Instant Radiosity 与虚拟点光源（RSM 版） |
| [[parallax-corrected-cubemap]] | 视差修正 cubemap 与非专烘焙 cubemap 的 BoxScale 修正 |
| [[vertex-vector-interpolation-artifact]] | 归一化 view/light 向量在大三角形上的插值陷阱 |
| [[dual-depth-buffer-thickness]] | Min 混合在单 pass 里求物体厚度的 ShaderX6 技巧 |
| [[deferred-alpha-lighting]] | Deferred 渲染下给透明物打光的四条路 |
| [[moment-shadow-mapping]] | 四阶矩 + Hausdorff 矩问题闭式解的可过滤硬阴影；2016 扩展到体积/软阴影/半透明 |
| [[trigonometric-moment-transient-imaging]] | 三角矩问题闭式解把 AMCW lidar 的瞬态成像推到瞬态视频级速度 |

## 经典案例（wiki/examples/）

APoSD 中反复出现的标杆与反面案例。

| 文章 | 一句话描述 |
|---|---|
| [[unix-io]] | 5 个系统调用隐藏几十万行实现的深模块标杆 |
| [[java-io]] | 三件套 + 显式 buffering 的 classitis 病例 |
| [[garbage-collector]] | 接口为零的极限深模块 |

## 游戏开发（wiki/game-development/）

APoSD 框架在 Unity/游戏引擎开发中的应用。

| 文章 | 一句话描述 |
|---|---|
| [[unity-complexity-patterns]] | Unity 项目中的复杂性典型模式 |
| [[classitis-in-games]] | Manager 癌症与事件系统滥用 |
| [[resource-system-design]] | 资源系统的信息隐藏战场 |
| [[ecs]] | ECS 作为深模块与显式依赖的案例 |
| [[rendering-api-depth]] | 渲染 API 的浅 vs 深对照 |
| [[unity-procedural-mesh]] | Unity Mesh API：vertices + triangles + winding order 的最小闭环 |
| [[kinematic-character-controller]] | Unity DOTS 下 kinematic 角色控制器的设计与 edge case |
| [[a-star-pathfinding]] | A* 与动态环境下的寻路取舍，g(n) 是游戏性的入口 |
| [[composite-command-pattern]] | 命令模式与 Serial / Parallel 复合命令：跨帧执行的可组合工作单元 |
| [[meshes-of-navigation-recast]] | 导航网格与 Recast 的体素化生成管线 |

## 人物（wiki/people/）

| 文章 | 一句话描述 |
|---|---|
| [[john-ousterhout]] | APoSD 作者，斯坦福 CS 教授 |
| [[jasper-flick]] | Catlike Coding 作者，Unity 教程作者 |
| [[jason-gregory]] | Naughty Dog 引擎工程师，GEA 作者 |
| [[sussman-abelson]] | SICP 作者，Scheme 发明人 |
| [[hennessy-patterson]] | CAQA 作者，RISC 图灵奖得主 |
| [[bartosz-ciechanowski]] | ciechanow.ski 作者，交互式可视化大师 |
| [[bartosz-wronski]] | Bart Wronski，前 Sony Santa Monica / Google Pixel HDR+ |
| [[fabian-giesen]] | Fabian "ryg" Giesen，RAD/Epic 程序员，The ryg blog 作者 |
| [[aras-pranckevicius]] | 立陶宛图形工程师，前 Unity，现 Blender VSE 模块负责人 |
| [[angelo-pesce]] | Angelo Pesce（C0DE517E），图形程序员，长年博客输出思辨性笔记 |
| [[emilio-lopez-ros]] | The Code Corsair 博主，AAA 帧分析与 TAA tutorial 作者 |
| [[christoph-peters]] | Christoph Peters，momentsingraphics.de，矩/傅里叶系数压缩带界信号的图形研究者 |
| [[matthaeus-chajdas]] | Matthäus "Anteru" Chajdas，AMD GPU/编译器方向，anteru.net 博主 |
| [[max-slater]] | Max Slater（thenumb.at），前 Pixar / Activision 图形工程师 |
| [[xor-shader-artist]] | Xor / GM Shaders，Shadertoy + GameMaker 方向的 shader 艺术家与教程作者 |
| [[stephen-hill]] | Selfshadow 博客 / SIGGRAPH PBS course 组织者 / Lucasfilm ILMxLAB |
| [[jeremiah-van-oosten]] | 3dgep.com 作者，Learning DirectX 12 系列教程 |
| [[robin-green]] | 前 Sony SCEA R&D，GDC 2003 SH Lighting: Gritty Details 作者 |
| [[raph-linus]] | Raph Levien，Google Fonts / linebender，Vello / Druid / Xilem 作者 |
| [[apoorva-joshi]] | Apoorva Joshi，前 Activision path tracing，Papaya 开源 GPU 图像编辑器作者 |
| [[jasper-st-pierre]] | Linux 图形栈 / 现代图形 API 长期布道者，出货游戏渲染器工程师 |
| [[harry-alisavakis]] | Harry Alisavakis，Technically Art 博客作者、ShaderQuest 系列教程作者 |
| [[ronja-bohm]] | Ronja Böhm（Ferris Systems），Unity shader 教程作者 |
| [[cyanilux]] | Cyan（@Cyanilux），Unity Shader Graph / URP 教程作者 |
| [[linden-reid]] | Linden Reid，面向初学者的 Unity shader 与程序化几何教程作者 |
| [[steven-sell]] | Steven Sell，Vertex Fragment 博客与 Realms/Beyond the Storm 作者 |
| [[daniel-ilett]] | Daniel Ilett，Unity shader 教程作者与资产包（Snapshot / Retro / Toolbox）开发者 |
| [[alan-zucconi]] | Alan Zucconi，Unity shader 教程作者（彩虹 / 衍射 / SSS / 体积 / Journey） |
| [[gameknife]] | 中国独立引擎开发者，gkEngine 与 gkNextRenderer 作者 |
| [[allen-chou]] | Allen Chou（周明倫），Naughty Dog gameplay programmer，DigiPen 出身，Game Physics Series 作者 |
| [[frost-kiwi]] | Wladislav Artsimovich / Jaruat Frost，以交互式 WebGL 技术博客闻名 |
| [[warren-moore]] | Warren Moore，Metal by Example 博客与同名书作者 |
| [[simon-trumpler]] | Simon Trümpler，simonschreibt.de 作者，技术美术 / Game Art Tricks 博主 |
| [[kostas-anagnostou]] | Interplay of Light 博主，Playground Games 图形工程师 |
| [[people/evan-todd]] | Evan Todd，etodd.io / Lemma / Deceiver 独立开发者 |
| [[brian-karis]] | Epic UE5 Nanite/Lumen 技术负责人，前 Human Head（Prey 2），UE4 Real Shading 作者 |
| [[cloudwu]] | 云风，skynet / ejoy2d 作者，前网易游戏引擎程序员 |

## 源摘要（wiki/sources/）

| 源 | 一句话描述 |
|---|---|
| [[sources/custom-srp-6-1-0]] | Custom SRP 6.1.0 教程摘要 |
| [[sources/aposd-day01]] | APoSD Day 1：Introduction |
| [[sources/aposd-day02]] | APoSD Day 2：复杂性的定义与症状 |
| [[sources/aposd-day03]] | APoSD Day 3：战术 vs 战略编程 |
| [[sources/aposd-day04]] | APoSD Day 4：深模块 |
| [[sources/aposd-day05]] | APoSD Day 5：浅模块之罪与 Classitis |
| [[sources/aposd-day06]] | APoSD Day 6：信息隐藏 |
| [[sources/sicp-day01]] | SICP Day 1：编程的三要素 |
| [[sources/sicp-day02]] | SICP Day 2：过程即黑盒 |
| [[sources/sicp-day03]] | SICP Day 3：递归过程 vs 迭代过程 |
| [[sources/sicp-day04]] | SICP Day 4：增长阶与快速幂 |
| [[sources/sicp-day05]] | SICP Day 5：概率素数判定 |
| [[sources/sicp-day06]] | SICP Day 6：高阶函数 |
| [[sources/rtr-day01]] | RTR Day 1：渲染管线架构 |
| [[sources/rtr-day02]] | RTR Day 2：Application 阶段 |
| [[sources/rtr-day03]] | RTR Day 3：Geometry Processing |
| [[sources/rtr-day04]] | RTR Day 4：Rasterization |
| [[sources/rtr-day05]] | RTR Day 5：Pixel Processing |
| [[sources/rtr-day06]] | RTR Day 6：一帧的完整生命 |
| [[sources/gea-day01]] | GEA Day 1：引擎是什么 |
| [[sources/gea-day02]] | GEA Day 2：引擎演化史 |
| [[sources/caqa-day01]] | CAQA Day 1：量化方法 |
| [[sources/caqa-day02]] | CAQA Day 2：存储层次与可靠性 |
| [[sources/csapp-day01]] | CSAPP Day 1：信息是上下文中的比特 |
| [[sources/ciechanow-color-spaces]] | Ciechanowski：色彩空间三要素与线性域运算 |
| [[sources/ciechanow-alpha-compositing]] | Ciechanowski：Porter-Duff 合成与预乘 α |
| [[sources/ciechanow-cameras-and-lenses]] | Ciechanowski：从针孔到薄透镜的光学推导 |
| [[sources/bartwronski-exposure-fusion]] | Wronski：Exposure Fusion 与局部色调映射 |
| [[sources/bartwronski-iir-deconvolution]] | Wronski：梯度下降学 IIR 滤波器反卷积 |
| [[sources/bartwronski-poisson-sampling]] | Wronski：Poisson 采样生成器 |
| [[sources/bartwronski-csharprenderer-debug]] | Wronski：CSharpRenderer GPU printf 与 surface snapshot |
| [[sources/ryg-exact-unorm8-to-float]] | ryg：UNORM8 → float 的精确转换 |
| [[sources/ryg-sinc-and-polynomial-interpolation]] | ryg：sinc 与多项式插值的关系 |
| [[sources/ryg-sse-mind-the-gap]] | ryg：SSE/SSE2 的非正交性 trick 集 |
| [[sources/ryg-trip-through-graphics-pipeline-2011-part-6]] | ryg：Pineda 算法与硬件光栅化 |
| [[sources/ryg-models-for-adaptive-arithmetic-coding]] | ryg：Oodle LZNA 背后的多元自适应模型 |
| [[sources/aras-rapidhash-unity-port]] | Aras：rapidhash 的 Unity Burst 移植与 XXH3 对比 |
| [[sources/aras-gpu-point-rasterization]] | Aras：硬件点光栅化为何输给朴素 compute shader |
| [[sources/aras-blender-vse-image-filtering]] | Aras：Blender VSE 的图像滤波考古 |
| [[sources/c0de517e-cached-shadowmaps]] | Pesce：远级联阴影缓存的半成品想法 + Mike Day 的完整实现 |
| [[sources/c0de517e-tiled-hardware-speculations]] | Pesce + ryg：TBDR vs IMR 的软件侧推演与硬件侧修正 |
| [[sources/elopezr-rotr-rendering]] | López：Rise of the Tomb Raider 逐帧渲染分析 |
| [[sources/elopezr-taa-holy-trail]] | López：TAA 完整 tutorial（jitter 到 rectification 全流程） |
| [[sources/peters-spectral-rendering-1-spectra]] | Peters：光谱渲染三部曲 Part 1 — 光谱从哪来 |
| [[sources/peters-spectral-rendering-2-real-time]] | Peters：光谱渲染三部曲 Part 2 — 实时路径追踪里的波长 MC 采样 |
| [[sources/peters-gpu-polynomial-roots]] | Peters：GPU 上的多项式实根求解与反寄存器溢出设计 |
| [[sources/peters-projected-spherical-caps]] | Peters & Dachsbacher i3D 2019：球形光源投影立体角的实时采样 |
| [[sources/chajdas-assisted-probe-placement]] | Chajdas：环境探针辅助放置（CWW11 回顾） |
| [[sources/slater-qmc-crash-course]] | Slater：Monte Carlo 速成 Part 5 — Quasi-Monte Carlo |
| [[sources/slater-exile-voxel-rendering]] | Slater：Exile 引擎的体素渲染管线 |
| [[sources/slater-exile-reflection]] | Slater：Exile 引擎的 libclang 元程序反射 |
| [[sources/slater-functions-are-vectors]] | Slater：Functions are Vectors — 函数即无限维向量 |
| [[sources/slater-compiler-bug]] | Slater：MSVC 2019 interference analysis 的栈重叠 codegen bug |
| [[sources/xor-mini-jfa]] | Xor：JFA 在 GPU 上生成距离场 |
| [[sources/xor-mini-oklab]] | Xor：OKLab 感知均匀色彩混合 |
| [[sources/xor-mini-3d-rotation]] | Xor：Euler / Axis-Angle 3D 旋转入门 |
| [[sources/xor-efficient-chaos]] | Xor：黄金角分层网格的廉价伪随机 |
| [[sources/xor-shadowmaps]] | Xor：shadow mapping 完整入门教程 |
| [[sources/selfshadow-multi-faceted-part-2]] | Hill：微表面多次散射补偿 lobe 的推导与 Fms 修正 |
| [[sources/selfshadow-blending-in-detail]] | Hill & Barré-Brisebois：Reoriented Normal Mapping |
| [[sources/selfshadow-pbs-siggraph-2014]] | Hill：SIGGRAPH 2014 PBS 课程导读 |
| [[sources/selfshadow-practical-visibility]] | Hill & Collin：Conviction HZB + Battlefield SPU 软光栅遮挡 |
| [[sources/3dgep-learning-directx12-lesson3]] | van Oosten：D3D12 Lesson 3，资源绑定与状态跟踪封装 |
| [[sources/3dgep-cuda-memory-model]] | van Oosten：CUDA 五种内存 + 矩阵乘 tiling 优化 |
| [[sources/green-sh-lighting-gritty-details]] | Robin Green：SH 光照在 PS2 上的落地回顾 |
| [[sources/green-implementing-needlets]] | Robin Green：Needlet 球面 wavelet 的实现配方 |
| [[sources/green-faster-math-functions]] | Robin Green：GDC 2002/2003 Faster Math Functions tutorial 回顾 |
| [[sources/green-display-edid-colorspace]] | Robin Green：用 PowerShell + WMI 抽 EDID 色度 |
| [[sources/green-procedural-rendering-ps2]] | Robin Green：GDC 2001 PS2 过程式几何 demo 回顾 |
| [[sources/raphlinus-smooth-resize-test]] | Raph：把窗口拖拽抖动当作 GUI 架构体检 |
| [[sources/raphlinus-rust-2021-gui]] | Raph：Rust GUI 生态现状、Druid 定位、收敛难题 |
| [[sources/raphlinus-fearless-simd]] | Raph：Rust 下可移植 SIMD 的愿景与双层 trait 探索 |
| [[sources/apoorvaj-calling-conventions]] | Joshi：cdecl/stdcall/fastcall 三路汇编 diff |
| [[sources/apoorvaj-zooming-and-panning]] | Joshi：Papaya GPU 图像编辑器笔刷与缩放的性能拆解 |
| [[sources/jasper-how-to-write-a-renderer]] | Jasper：现代图形 API 渲染器的三条轴线（draw call / render pass / data upload） |
| [[sources/jasper-dri-linux-graphics-stack]] | Jasper：拆开 DRI/DRM/KMS/libdrm/wl_drm 的命名迷雾 |
| [[sources/playcanvas-profiler]] | PlayCanvas Profiler 发布公告：帧耗时分解 + 启动时间轴 |
| [[sources/playcanvas-volumetric-video]] | PlayCanvas 集成 MRCS 体积视频到 WebXR AR/VR 的项目复盘 |
| [[sources/halisavakis-shaderquest-shaping-functions]] | Alisavakis：ShaderQuest 第六篇，着色器塑形函数入门 |
| [[sources/ronja-planar-mapping]] | Ronja：用世界坐标 xz 生成 UV 的三阶段演进 |
| [[sources/ronja-texture-dissolve]] | Ronja：纹理驱动的 clip 溶解 + HDR 边缘发光 |
| [[sources/ronja-2d-sdf-basics]] | Ronja：2D SDF 基元、变换作用在采样点上、fwidth 抗锯齿 |
| [[sources/ronja-2d-sdf-shadows]] | Ronja：SDF sphere-tracing 软阴影的 `min(d/t)` 单行技巧 |
| [[sources/ronja-draw-procedural]] | Ronja：DrawProcedural + StructuredBuffer 的 GPU-driven 入门 |
| [[sources/cyan-urp-post-processing]] | Cyan：URP 后处理（Volume + Blit Render Feature） |
| [[sources/cyan-uv-based-nodes]] | Cyan：Shader Graph 的 UV 操作节点总览 |
| [[sources/cyan-retro-crt-shader]] | Cyan：复古 CRT shader 的 5 效果拆解 |
| [[sources/cyan-scene-color-depth]] | Cyan：Scene Color / Scene Depth 节点跨管线行为 |
| [[sources/cyan-particle-custom-vertex-streams]] | Cyan：粒子系统到 Shader Graph 的逐粒子数据通道 |
| [[sources/lindenreid-basic-math-for-shaders]] | Reid：shader 向量数学入门（视觉化 > 抽象符号） |
| [[sources/lindenreid-procedural-geometry-part2]] | Reid：Unity Mesh API 从零构造 cube + winding order |
| [[sources/lindenreid-foggy-window-shader]] | Reid：GrabPass + 可分 blur + 纹理编码时间的可交互雾化窗户 |
| [[sources/vertexfragment-diamond-square-gpu]] | Sell：Diamond-Square 三种实现对比与 GPU 加速复盘 |
| [[sources/vertexfragment-dots-character-controller]] | Sell：Unity DOTS kinematic 角色控制器详细实现 |
| [[sources/vertexfragment-list-removal]] | Sell：C# List.RemoveAt 性能陷阱与 swap-and-pop 解法 |
| [[sources/vertexfragment-deferred-grass]] | Sell：Unity 延迟管线下的 5 阶段草地着色方案 |
| [[sources/danielilett-cel-shading-part-1]] | Daniel Ilett：Cel Shading 系列 1，Lambert 漫反射的 Unity 实现 |
| [[sources/danielilett-your-first-shader]] | Daniel Ilett：Unity 6 + URP 的第一个代码 shader，ShaderLab+HLSL 最小骨架 |
| [[sources/danielilett-retro-terrain-lit]] | Daniel Ilett：Retro Terrain Lit shader 参数与 PS1/N64 复古技术清单 |
| [[sources/danielilett-dither-transparency]] | Daniel Ilett：URP Lit shader 的 Bayer dither 伪透明参数集 |
| [[sources/alanzucconi-improving-rainbow-2]] | Zucconi：branchless 波长→RGB 拟合 `spectral_zucconi(6)` |
| [[sources/alanzucconi-cdrom-diffraction-2]] | Zucconi：CD-ROM 衍射光栅着色器 + 从 UV 推切向 |
| [[sources/alanzucconi-fast-sss-1]] | Zucconi：Barré-Brisebois / Frostbite 廉价假 SSS 移植到 Unity |
| [[sources/alanzucconi-volumetric-rendering]] | Zucconi：体积 raycasting 与 raymarching 入门 |
| [[sources/alanzucconi-journey-sand-specular]] | Zucconi：Journey 沙丘 rim lighting + ocean specular 拆解 |
| [[sources/gameknife-gknextrenderer-yearone]] | gameknife：从 DX11 追赶现代渲染的一年总结 |
| [[sources/gameknife-tbdr-performance-tuning]] | Bruce Merry TBDR 性能调校中译（gameknife 译） |
| [[sources/gameknife-pathfinding-review]] | gameknife：A* 与动态环境寻路的重新审视 |
| [[sources/gameknife-gkengine-features]] | gameknife：gkEngine 2015 年技术特性清单 |
| [[sources/allenchou-game-physics-introduction]] | Allen Chou：约束式刚体物理引擎的流水线概览与术语表 |
| [[sources/allenchou-rusher-2-composite-commands]] | Allen Chou：ActionScript 3 / Rusher 2 框架下 Serial / Parallel 复合命令用法 |
| [[sources/frost-kiwi-luts-in-video-games]] | Frost：1D/3D LUT 在视频游戏中的各种用法（L4D tinting 到 Resolve 调色） |
| [[sources/frost-kiwi-analytical-anti-aliasing]] | Frost：SSAA/MSAA/FXAA/AAA 对比长文与 AAA 实现细节 |
| [[sources/metalbyexample-up-and-running-1]] | Warren Moore：Metal 第 1 篇——清屏到红色 |
| [[sources/metalbyexample-up-and-running-2]] | Warren Moore：Metal 第 2 篇——带色三角形与 MSL 入门 |
| [[sources/metalbyexample-whats-and-wherefores]] | Warren Moore：Metal 的「抽象下界」立场与未来判断 |
| [[sources/simonschreibt-deus-ex-occlusion]] | Simon：Deus Ex 的预烘焙角落遮蔽与 UE1 lightmap bug |
| [[sources/simonschreibt-diablo3-trees]] | Simon：Diablo 3 如何用两张三角形画出细剪影的树 |
| [[sources/simonschreibt-divine-divinity-reflection]] | Simon：Divine Divinity 2D 水面反射的猜测与读者讨论 |
| [[sources/simonschreibt-fallout3-edges]] | Simon：Fallout 3 用 normal decal 壳掩盖低多边形石头的硬边 |
| [[sources/simonschreibt-teleglitch-rgb]] | Simon：Teleglitch 传送器的 RGB 通道独立偏移特效 |
| [[sources/frost-kiwi-color-banding]] | Frost：一行 GLSL dither 消色带 + 五家业界实现横评 |
| [[sources/frost-kiwi-thermal-colormaps]] | Frost：matplotlib colormap → DaVinci Resolve .cube 工具脚本 |
| [[sources/interplay-tools-of-the-trade]] | Anagnostou：shader 原型与调试工具栈总览（2013） |
| [[sources/interplay-depth-testing]] | Anagnostou：D3D11 depth testing 阶段与 Early-Z 救援语义 |
| [[sources/interplay-tangent-free-normal-mapping]] | Anagnostou：Christian Schüler 免 TBN 法线贴图的 FX Composer 实测 |
| [[sources/interplay-unity-as-fxcomposer]] | Anagnostou：Unity 免费版替代 FX Composer 做 shader 原型 |
| [[sources/interplay-sharpdx-model-loading]] | Anagnostou：SharpDX + Assimp 补齐 XNA 式内容管线 |
| [[sources/etodd-meshes-of-navigation]] | Todd：把 Recast 接入 A3P 的 navmesh 管线 |
| [[sources/etodd-refactoring-with-components]] | Todd：端口式的组件数据绑定方案 |
| [[sources/karis-virtualized-volume-textures]] | Karis：把 2D virtual texture 和 SVO 思路搬到 irradiance volume |
| [[sources/karis-tiled-light-culling]] | Karis：tile 级 per-light 剔除加入 specular cone 方向约束 |
| [[sources/karis-sparse-shadows-tracing]] | Karis：next-gen 渲染需要多几何表示 + cone trace，UE5 Lumen 的雏形 |
| [[sources/cloudwu-c-module-interface]] | 云风：C 语言模块化与接口设计 |
| [[sources/cloudwu-cpp-mark-sweep-gc]] | 云风：200 行的 C++ 标记清除 GC |
| [[sources/cloudwu-c-serialization-and-c-oop]] | 云风：C 结构序列化、C OOP 与 protected |
| [[sources/cloudwu-game-engine-vfs]] | 云风：实现一个简单的虚拟文件系统 |
| [[sources/cloudwu-malloc-wrapper]] | 云风：给 malloc 加壳 |
| [[sources/interplay-instant-radiosity-light-prepass]] | Anagnostou：在 light prepass 上跑 Instant Radiosity |
| [[sources/interplay-parallax-corrected-cubemap]] | Anagnostou：用任意 cubemap 做视差修正反射的 hack |
| [[sources/interplay-interpolate-view-light-vectors]] | Anagnostou：大三角形上归一化向量的插值 bug |
| [[sources/interplay-dual-depth-thickness]] | Anagnostou：ShaderX6 厚度技巧的 front/back 分流改进 |
| [[sources/interplay-lighting-alpha-deferred]] | Anagnostou：deferred 下给透明物打光的四条路 |
| [[sources/peters-moment-shadow-mapping]] | Peters & Klein：四阶矩阴影贴图原论文（I3D 2015） |
| [[sources/peters-trigonometric-moment-transient-imaging]] | Peters et al.：三角矩 + AMCW lidar 的快速瞬态成像（SGA 2015） |
| [[sources/peters-beyond-hard-shadows-msm]] | Peters et al.：MSM 扩展到单次散射/软阴影/半透明遮挡（I3D 2016） |

## 元（wiki/meta/）

| 文章 | 一句话描述 |
|---|---|
| [[taste-development]] | 基于 wiki 内容综合出的品味训练方法 |

## 特殊页面

- [[overview]] —— 综合叙事：把主题串起来
- [[log]] —— 所有操作的时间顺序记录
