## [2026-04-05] ingest | Custom SRP 6.1.0

收录 Catlike Coding 的 Unity Custom SRP 6.1.0 教程（作者 Jasper Flick）。内容涉及 Camera Target Texture 修复和 Color LUT 调试可视化的实现。创建 5 篇渲染相关 wiki 页。

## [2026-04-05] ingest | APoSD Day 1 Introduction

收录 APoSD 第 1 章 Introduction 的学习笔记。核心观点：软件开发的最大限制是理解系统的能力，不是技术；复杂性是核心敌人；对抗它有消除与封装两条路；软件设计是持续过程。

## [2026-04-05] ingest | APoSD Day 2 复杂性的定义与症状

收录 APoSD 第 2 章的学习笔记。给出复杂性的精确定义（读者视角）、三症状（变更放大、认知负荷、未知的未知）、两根源（依赖、模糊性）、公式 C = Σ(cp × tp)。

## [2026-04-05] ingest | APoSD Day 3 战术 vs 战略编程

收录 APoSD 第 3 章的学习笔记。复杂性的复利性、零容忍纪律、战术龙卷风概念、10-20% 投资原则、Facebook/Google 对照。

## [2026-04-05] ingest | APoSD Day 4 深模块

收录 APoSD 第 4 章前半部分的学习笔记。深模块作为核心正面构造，Unix I/O 和 GC 作为标杆，接口=成本的重新定义，抽象的定义，浅模块的极端案例，与 Clean Code/GoF 的对比。

## [2026-04-05] ingest | APoSD Day 5 浅模块之罪 & Classitis

收录 APoSD 第 4 章后半部分的学习笔记。Classitis 作为系统性疾病，Java I/O vs Unix I/O 的对照，游戏开发中 Manager 癌症和事件系统滥用的典型。

## [2026-04-05] ingest | APoSD Day 6 信息隐藏

收录 APoSD 第 5 章的学习笔记。信息隐藏作为深模块的灵魂，`private` != 信息隐藏，信息泄漏红旗，后门泄漏，时序分解陷阱，「让类稍微大一点」的反直觉推论。

## [2026-04-05] update | 初次编译整个 wiki

从所有 raw 源初次编译出完整 wiki：35 篇概念/案例/人物/源摘要页，加上 overview、index、log。所有内容使用简体中文。目录结构：software-design、examples、game-development、rendering、people、sources。

## [2026-04-05] ingest | SICP Day 1-6

收录 SICP 前 6 天学习笔记：编程三要素、过程抽象、递归 vs 迭代、增长阶、概率素数判定、高阶函数。创建 wiki/programming-languages/ 下 14 篇概念页：elements-of-programming、substitution-model、applicative-vs-normal-order、environment、procedural-abstraction、lexical-scoping、closure、recursive-vs-iterative-process、tail-call-optimization、higher-order-functions、lambda-calculus、order-of-growth、fast-exponentiation、probabilistic-algorithms。发现与 APoSD information-hiding 的直接呼应。

## [2026-04-05] ingest | Real-Time Rendering Day 1-6

收录 RTR 前 6 天学习笔记：渲染管线架构、Application 阶段、Geometry Processing、Rasterization、Pixel Processing、一帧完整生命。创建 wiki/rendering/ 下 19 篇新概念页：rendering-pipeline、bottleneck-analysis、tbdr-vs-imr、draw-call、culling、batching、mvp-transform、coordinate-spaces、z-buffer、z-fighting、reversed-z、perspective-correct-interpolation、rasterization、aliasing、msaa-ssaa、triangle-primitives、fragment-shader、early-z-late-z、hsr-tbdr、alpha-blending、stencil-buffer、overdraw、deferred-rendering。

## [2026-04-05] ingest | Game Engine Architecture Day 1-2

收录 Jason Gregory 的 Game Engine Architecture 前 2 天学习笔记：引擎定义、三角度分析、引擎演化史（BSP → Lumen/Nanite）。创建 wiki/game-engines/ 下 6 篇概念页：game-engine、data-driven-architecture、soft-real-time、engine-layering、unity-vs-unreal、engine-evolution。

## [2026-04-05] ingest | Computer Architecture Day 1-2 & CSAPP Day 1

收录 CAQA 前 2 天与 CSAPP 第 1 天学习笔记：Amdahl 定律、Flynn 分类法、CPU 性能公式、存储层次、局部性原理、AoS vs SoA、Dennard Scaling 崩塌、功耗墙、MTTF 可靠性、信息=比特+上下文、编译四阶段、虚拟内存。创建 wiki/computer-systems/ 下 14 篇概念页。

## [2026-04-05] update | 大规模知识域扩展

从 7 源扩展到 24 源，wiki 文章从 47 扩展到 101 篇。新增 4 个概念类别（programming-languages、computer-systems、game-engines、rendering 大幅扩展）、3 位作者（sussman-abelson、hennessy-patterson、jason-gregory）。更新 index、overview 大幅重写以反映五大主题架构和跨主题连接。更新 ecs、rendering-api-depth 以引入新 sources。

## [2026-04-05] lint | Wiki 健康检查

健康度评分 A-。发现 28 项改进点，分布 6 类：低入链页面（7）、概念缺口（10）、缺失交叉引用（12）、数据缺口（7）、样式一致性（1）、待研究问题（6）。无坏链，无 frontmatter 缺失，无 index 遗漏，无孤儿页。报告见 output/reports/lint-report.md。

## [2026-04-05] query | 如何用这些内容提升品味

用户问如何用本 wiki 提升设计品味。基于 Ousterhout 的 Red Flag 训练、APoSD 各章的品味判断、SICP 的抽象模式、概率算法的工程哲学，综合出五条可执行的品味训练方法 + 30 天练习计划。归档为 wiki/meta/taste-development.md，更新 index。

## [2026-04-14] ingest | Ciechanowski — Color Spaces

收录 Bartosz Ciechanowski 2019 年长文 Color Spaces。创建 wiki/rendering/color-space.md、wiki/people/bartosz-ciechanowski.md、wiki/sources/ciechanow-color-spaces.md，更新 alpha-blending 以指向线性域运算要求。

## [2026-04-14] ingest | Ciechanowski — Alpha Compositing

收录 Bartosz Ciechanowski 2019 年长文 Alpha Compositing。创建 wiki/rendering/alpha-compositing.md（Porter-Duff over 与预乘 α）、wiki/sources/ciechanow-alpha-compositing.md，扩展 alpha-blending 以引用它作为数学推导来源。

## [2026-04-14] ingest | Ciechanowski — Cameras and Lenses

收录 Bartosz Ciechanowski 2020 年长文 Cameras and Lenses。创建 wiki/rendering/pinhole-camera.md（针孔模型 + cos⁴ 暗角）与 wiki/rendering/thin-lens-model.md（焦距 / 光圈 / 景深 / bokeh / 像差），以及 wiki/sources/ciechanow-cameras-and-lenses.md。更新 mvp-transform 以指向虚拟相机的物理本体。

## [2026-04-14] update | Sprint 1 colossal raw batch 规划

盘点 raw/articles/ 实际体量：125 个域名 / 17,360 篇文章，相对现有 24 sources 是 ~700× 的扩展。既定策略：按主题相关性 + 权威度切 sprint 批次，Sprint 1 先闭环跑通 ciechanow.ski 三篇高相关文章的完整 ingest 流程（4 新概念页 / 1 人物页 / 3 source 摘要 / 2 存量页反向链接）。向用户汇报 scope，待其拍板后续 sprint 边界。

## [2026-04-14] update | Multi-Agent Team 拓扑落地

搭建 P9 orchestrator + P8 worker 并行编译 team：3124 行 tiered manifest (tier1 bartwronski/aras-p/fgiesen/ciechanow/etc. 1231 files + tier2 ronja/halisavakis/danielilett/etc. 903 + tier3 unity/playcanvas/etc. 1042)。协议文件 `_prompts/worker-ingest.md` 定义了 staging bundle JSON schema 与冲突规避四条铁律：worker 不得直写 index/log/overview/已存在概念页，所有补强通过 `wiki/.staging/batch-*/bundle.json` 的 `existing_page_patches` 数组提交，orchestrator 串行 apply。registry 快照随 prompt 传入防止 worker 重复创造已有概念。

## [2026-04-14] ingest | Wave-1 Worker A (bartwronski.com ×5)

处理 5 篇 bartwronski.com 技术文章。新增 6 概念页（local-tonemapping、exposure-fusion、laplacian-pyramid、iir-filter-deconvolution、poisson-disk-sampling、gpu-printf-debugging）、1 人物页（bartosz-wronski）、4 source 摘要。跳过 1 篇个人音乐数据分析教程。最大收获是 exposure-fusion 文章，把 Bart Wronski 从 God of War 到 Pixel HDR+ 两段经历串起来，覆盖了一个完整的 LTM 算法家族。

## [2026-04-14] ingest | Wave-1 Worker B (fgiesen.wordpress.com ×5)

处理 5 篇 ryg 博客文章，全部 ingest 无 skip。新增 7 个概念页（unorm-float-conversion, sampling-theorem-sinc, sse-tricks, pineda-edge-rasterization, hierarchical-rasterization, triangle-setup, adaptive-arithmetic-coding）、1 个人物页（fabian-giesen）、5 个 source 摘要。Pineda 算法 / coarse rast / triangle setup 三个相关概念互相 cross-link，并补强了既有 rasterization、rendering-pipeline、triangle-primitives 页面。涉及主题：GPU 数值精度、信号处理、SIMD x86、桌面 GPU 光栅化、自适应熵编码。

## [2026-04-14] ingest | Wave-1 Worker C (aras-p.info ×5)

处理 5 篇 Aras Pranckevičius 文章。3 篇技术性的 ingested（rapidhash 移植、点云硬件 vs compute 光栅化、Blender VSE 图像滤波考古），2 篇 Blender VSE 周年回顾 skipped_offtopic。新增 4 概念页（non-cryptographic-hash, rapidhash, compute-vs-raster-points, image-resampling-filters）、1 人物页（aras-pranckevicius）、3 source 摘要。对 overdraw / alpha-blending / fragment-shader / rasterization / aliasing / draw-call / bottleneck-analysis 七个既有页提交相关链接 patch。

## [2026-04-14] ingest | Wave-2 Worker D (c0de517e.blogspot.com ×5)

处理 Angelo Pesce 的 5 篇博客。Ingest 2 篇技术文：`cached-shadowmaps`（cascaded shadow 的帧间相干性缓存，引自 Mike Day SIGGRAPH 2012）、`tiled-hardware-speculations`（TBDR vs IMR 的软件侧推演，评论区 Fabian Giesen 的硬件侧修正价值极高）。Skip 3 篇：failed-builds（工作流吐槽）、i-support-anita（政治立场）、dos-nostalgia（个人怀旧 + DOS workstation 折腾）。新增 1 概念页（cached-shadowmaps）、1 人物页（angelo-pesce）、2 source 摘要。对 tbdr-vs-imr / hsr-tbdr / deferred-rendering / culling / fabian-giesen 发送增量 patch。

## [2026-04-14] ingest | Wave-2 Worker E (elopezr.com ×5)

处理 5 篇 elopezr.com 文章。新增 8 个概念页（temporal-antialiasing, motion-vectors, taa-history-rectification, tiled-light-prepass, hbao-interleaved-sampling, depth-aware-upsampling, fizzle-lod-fading, volumetric-fog-froxels）、1 个人物页（emilio-lopez-ros）、2 个 source 摘要（ROTR 帧分析、TAA tutorial）。跳过 3 篇：a-real-life-pinhole-camera 是个人旅行随笔且物理内容已被现有 pinhole-camera.md 覆盖；football-simulation 是 2014 原型项目随笔无技术深度；sub-the-fixer 是 Python 字幕修复工具与图形/引擎无关。

## [2026-04-14] ingest | Wave-2 Worker F (momentsingraphics.de ×5)

处理 5 篇 Christoph Peters 的 Moments in Graphics 博客文章。新增 7 个概念页（spectral-rendering, fourier-srgb-spectral-upsampling, hero-wavelength-spectral-sampling, spectral-brdf, polynomial-root-finding-gpu, register-spilling-avoidance, projected-solid-angle-sampling）、1 个人物页（christoph-peters）、4 个 source 摘要。跳过 1 篇非技术博客工具设置文章（2016 Markdeep + WordPress）。光谱渲染三部曲是重点贡献，把光谱渲染从「离线奢侈品」重新框定为实时可用方案，和既有 [[color-space]] 形成自然的升级路径。

## [2026-04-14] ingest | Wave-3 Worker G (anteru.net ×5)

处理 5 篇 anteru.net 文章，仅 1 篇技术内容入库（2025 assisted environment probe placement）。新增 1 概念页 [[environment-probe-placement]]、1 人物页 [[matthaeus-chajdas]]、1 源摘要。跳过 4 篇非技术内容（version numbers 软工随笔 / Deus Ex 3 trailer 观后感 / Ubuntu netplan 运维 / home server 硬件组装）。

## [2026-04-14] ingest | Wave-3 Worker H (thenumb.at / Max Slater ×5)

处理 Max Slater（thenumb.at）的 5 篇全技术长文，全部 ingest 无跳过：QMC 速成第 5 章、Exile 体素渲染管线、Exile libclang 元程序反射、Functions are Vectors（泛函分析视角的 Fourier / 球谐）、MSVC interference analysis codegen bug。新增 10 个概念页（quasi-monte-carlo / stratified-sampling / low-discrepancy-sequence / greedy-voxel-meshing / voxel-ambient-occlusion / compact-vertex-format / spherical-harmonics / functions-as-vectors / cpp-runtime-reflection / compiler-interference-analysis-bug）、1 个人物页（max-slater）、5 个 source summary。对 poisson-disk-sampling / fourier-srgb-spectral-upsampling / sampling-theorem-sinc / compilation-pipeline 四个现有页面添加交叉链接补丁。

## [2026-04-14] ingest | Wave-3 Worker I (mini.gmshaders.com / Xor ×5)

处理 5 篇 Xor 在 GM Shaders Mini 上的 shader 教程：Mini: JFA、Mini: OkLab、Mini: 3D Rotation、Efficient Chaos、GM Shaders: Shadowmaps。新增 5 个概念页（jump-flooding-algorithm、oklab-color-space、3d-rotation-math、layered-grid-noise、shadow-mapping-basics）、1 个人物页（xor-shader-artist）、5 个 source 摘要。向 color-space / cached-shadowmaps / poisson-disk-sampling / mvp-transform 四个已有页补了 `## 相关` 交叉引用。全部 5 篇成功摄入，无 skip。

## [2026-04-14] ingest | Wave-4 Worker J (blog.selfshadow.com / Stephen Hill ×5)

处理 Stephen Hill 5 篇。4 篇成功摄入：multi-faceted part 2（微表面多次散射补偿）、blending in detail（Reoriented Normal Mapping）、PBS SIGGRAPH 2014 导读、practical dynamic visibility（HZB + SPU 软光栅遮挡）。跳过 self-shadow-6 空 syllabus。新增 5 概念页、1 人物页、4 source 摘要，4 条 patch。

## [2026-04-14] ingest | Wave-4 Worker K (3dgep.com ×5)

3dgep.com 5 篇 Ingest 2 / Skip 3：D3D12 Lesson 3、CUDA Memory Model 入库；3D math coord primer 重复、C++ fast-track Part 2 / 16 太入门跳过。新增 3 概念页、1 人物页、2 source，4 条 patch。

## [2026-04-14] ingest | Wave-4 Worker L (basesandframes / Robin Green ×5)

Robin Green *Bases and Frames* 5 篇全部入库：needlets、faster math functions、SH lighting gritty details、EDID colorspace、PS2 procedural rendering。新增 4 概念页、1 人物页 robin-green、5 source 摘要。对 spherical-harmonics 和 color-space 补了交叉引用和 source。注：任务描述误将作者写为 Chris Green，Worker 按原文 frontmatter 正确识别为 Robin Green。

## [2026-04-14] ingest | Wave-5 Worker M (raphlinus.github.io ×5)

处理 5 篇 Raph Levien 博客文章。新增 4 概念页（smooth-window-resize、rust-gui-ecosystem、reactive-ui-rust、fearless-simd）、1 人物页（raph-linus）、3 source 摘要。跳过 2 篇（2022 年终反思、2017 Recurse Center 混合项目清单）——缺乏单一技术主线。引入 linebender 栈（Vello / Druid / Xilem）作为 Rust GUI 生态的锚点，与 sse-tricks 建立 SIMD 跨链。

## [2026-04-14] ingest | Wave-5 Worker N (apoorvaj.io ×5)

处理 5 篇 Apoorva Joshi *apoorvaj.io* 文章：2 入库 + 3 跳过。入库：*The experiment*（x86 32 位 cdecl/stdcall/fastcall 三路汇编 diff）→ [[calling-conventions-x86]]；*Zooming and panning*（Papaya GPU 图像编辑器的 textured quad 缩放 + fragment shader 笔刷）→ [[gpu-image-editor-brush]]。新增 1 人物页 [[apoorva-joshi]]（前 Activision path tracing）、2 source 摘要。跳过：*Cross-platform consistency*（UI 哲学散文）、*Vibe-coding a tax calculator*（Claude Code 工作流随笔）、*Stop over-engineering static websites*（博客 build 工具链）。对 fragment-shader 和 image-resampling-filters 两个既有页各补了一条相关链接。

## [2026-04-14] ingest | Wave-5 Worker O (blog.mecheye.net ×5)

处理 5 篇 Jasper St. Pierre（blog.mecheye.net）文章。新增 4 概念页（gpu-hazard-tracking, gpu-fence-timeline-semaphore, buffer-renaming, linux-graphics-stack-dri）、1 人物页（jasper-st-pierre）、2 source 摘要。跳过 3 篇非技术内容（Shellshock 项目治理、GNOME 3.8 pressure barriers、GNOME invisible borders）。核心收获：Jasper《How to write a renderer for modern graphics APIs》的 draw call / render pass / data upload 三轴规划视角，以及 Linux 图形栈 DRI/DRM/KMS 命名一次性拆清。

## [2026-04-14] ingest | Wave-6 Worker P (blog.playcanvas.com ×5)

处理 5 篇 PlayCanvas 官方博客。3 篇跳过（PLAYHACK 活动营销、团队成员采访、每周 changelog），2 篇技术性足够入库：Profiler 浮层发布与 MRCS 体积视频 WebXR 集成复盘。新增 2 概念页（frame-profiler-overlay, volumetric-video-playback）、2 source 摘要，未新增人物页。

## [2026-04-14] ingest | Wave-6 Worker Q (halisavakis.com ×5)

处理 5 篇 halisavakis.com 文章。吸收 1 篇 ShaderQuest 塑形函数教程，跳过 4 篇 Technically Art 周报（仅为 Twitter 作品集锦）。新增 1 概念页（shaping-functions）、1 人物页（harry-alisavakis）、1 source 摘要。

## [2026-04-14] ingest | Wave-6 Worker R (ronja-tutorials.com ×5)

处理 5 篇 Ronja Böhm 的 Unity shader 教程，全数 ingest，无 skip。新增 5 概念页（planar-mapping、texture-dissolve、sdf-2d-primitives、sdf-ray-marched-shadows、draw-procedural-gpu）、1 人物页（ronja-bohm，Ferris Systems）、5 source 摘要。建立 SDF 线（primitives → shadows）与现有 [[jump-flooding-algorithm]] 形成互补（解析函数 vs 纹理化距离场）。把 [[texture-dissolve]] 与已有 [[fizzle-lod-fading]] 做了意图差异的对比（VFX 演出 vs 隐藏 LOD 切换）。[[draw-procedural-gpu]] 作为 GPU-driven 渲染路径的入门接入 [[custom-srp]] 和 [[compute-vs-raster-points]]。

## [2026-04-14] ingest | Wave-7 Worker S (cyangamedev.wordpress.com ×5)

处理 5 篇 Cyan（@Cyanilux）的 Unity Shader Graph / URP 技术教程，全部 ingest。新增 7 个渲染概念页（urp-volume-post-processing、blit-render-feature、uv-manipulation-nodes、sampler-filter-wrap-modes、crt-shader-effects、scene-color-depth-nodes、particle-custom-vertex-streams）、1 人物页（cyanilux）、5 个 source 摘要。对 scriptable-render-pipeline / fragment-shader / reversed-z / z-buffer / texture-dissolve / harry-alisavakis 7 处存量页面发出 append_to_section 补丁，交叉链接 URP 后处理、Shader Graph 节点、深度相交、粒子 VFX 等主题。

## [2026-04-14] ingest | Wave-7 Worker T (lindenreid.wordpress.com ×5)

处理 5 篇 Linden Reid 博客，按 topicality gate 跳过 2 篇职业建议（how-to-start-a-career-in-games、how-to-be-successful-at-a-game-jam），ingest 3 篇技术教程。新增 4 概念页（shader-vector-math-primer、unity-procedural-mesh、unity-grabpass-blur、texture-encoded-state）、1 人物页（linden-reid）、3 source 摘要。foggy window 一篇拆成 2 个概念页：GrabPass+blur 技术本身放在 [[unity-grabpass-blur]]，而把时间戳编码进纹理通道这一更通用 trick 单独成页 [[texture-encoded-state]]，便于与 GPU 粒子、flow map、[[gpu-image-editor-brush]] 等既有谱系交叉引用。把 [[linden-reid]] 与 [[ronja-bohm]] 在 "面向初学者的 Unity shader 教程作者" 这条线上互相连接。

## [2026-04-14] ingest | Wave-7 Worker U (vertexfragment.com ×5)

处理 5 篇 Steven Sell 的 Vertex Fragment 技术 ramble。1 篇跳过（Beyond the Storm v0.6 游戏 changelog），4 篇入库：Diamond-Square 的 GPU compute 加速、Unity DOTS kinematic 角色控制器、C# List.RemoveAt 的 swap-and-pop 优化、Unity 延迟管线下的草地着色器。新增 4 概念页（diamond-square-noise, kinematic-character-controller, swap-and-pop-removal, deferred-grass-shader）、1 人物页（steven-sell）、4 source 摘要。Patches 挂到 ecs、poisson-disk-sampling、deferred-rendering。

## [2026-04-14] ingest | Wave-8 Worker V (danielilett.com ×5)

处理 5 篇 danielilett.com shader 教程与资产包文档。Ingest 4 篇——2 篇真教程（Cel Shading Part 1 的 Lambert 漫反射、Your First Shader 的 URP 代码 shader 骨架）和 2 篇含实质技术的资产包文档（Retro Terrain Lit 的 PS1/N64 复古技术清单、Dither Transparency 的 Bayer dither alpha clipping 参数）。跳过 1 篇纯营销 overview（Snapshot Shaders 2）。新增 5 个渲染概念页（diffuse-lighting-lambertian、unity-surface-shaders、shaderlab-hlsl-basics、retro-rendering-techniques、dither-alpha-clipping）、1 个人物页（daniel-ilett）、4 个 source 摘要。对 fizzle-lod-fading / alpha-blending / shader-vector-math-primer 三个现有页面做了交叉链接补丁。

## [2026-04-14] ingest | Wave-8 Worker W (alanzucconi.com ×5)

处理 5 篇 Alan Zucconi 的经典 Unity shader 教程，全部入库。新增 5 概念页（spectral-zucconi-rainbow、diffraction-grating-shader、fast-translucency-wraplight、volumetric-raymarching-intro、journey-sand-specular）、1 人物页（alan-zucconi）、5 source 摘要。Patches 挂到 spectral-rendering、physically-based-shading、microfacet-brdf、volumetric-fog-froxels、sdf-ray-marched-shadows。

## [2026-04-14] ingest | Wave-8 Worker X (gameknife.github.io ×5)

处理 5 篇 gameknife.github.io 文章。新增 6 个概念页（visibility-buffer、hybrid-raytracing-pipeline、bindless-rendering、gknext-renderer、gkengine、a-star-pathfinding）、1 个人物页（gameknife）、4 个源摘要。给 tbdr-vs-imr、hsr-tbdr、engine-evolution、deferred-rendering 提了 4 条 patch。跳过 1 篇非技术私活随笔。

## [2026-04-14] ingest | Wave-9 Worker Y (allenchou.net ×5)

处理 5 篇 allenchou.net 博客。Ingest 2 篇：Game Physics Introduction（约束式刚体物理引擎三段流水线概览）与 Rusher 2 Composite Commands（命令模式 Serial/Parallel 子命令教程）。跳过 3 篇：Bunnyhill Flash Molehill 演示（技术栈过时且内容单薄）、Joining Naughty Dog's Kennel（career 叙事）、DigiPen 我的游戏学校（school 博文）。新增 3 个概念页（game-physics-engine、collision-detection-gjk-epa、composite-command-pattern）、1 个人物页（allen-chou，Naughty Dog gameplay programmer）、2 个 source 摘要。对 engine-layering / game-engine 做了 ## 相关 交叉链接补丁，对 kinematic-character-controller 做了 source 链接补丁。

## [2026-04-14] ingest | Wave-9 Worker Z (blog.frost.kiwi ×5)

处理 5 篇 blog.frost.kiwi 文章。入库 2 篇图形长文：LUT 在视频游戏里的用途（link to 已有 [[color-lut]]），以及 Analytical Anti-Aliasing（新增概念页）。跳过 3 篇：WaniKani userscript（非技术）、just-a-textbox（个人工作流 HTML）、jo-mpeg-converted-to-c（源码倾倒，无实质技术分析）。新增 1 概念页（analytical-antialiasing）、1 人物页（frost-kiwi）、2 source 摘要。给 color-lut / aliasing / msaa-ssaa / sdf-2d-primitives 打补丁加链接。

## [2026-04-14] ingest | Wave-10 Worker AB (metalbyexample.com ×5)

处理 5 篇 Warren Moore 的 Metal by Example 文章。跳过 2 篇（about-the-author、the-book）纯元信息页。入库 3 篇 Up and Running 系列实质教程，新增 3 concept 页（metal-api-overview、metal-shading-language-basics、cametal-layer-drawable）、1 人物页（warren-moore）、3 source 摘要。最大收获是把 Metal 作为「iOS 上抽象下界」的自我定位补进了 wiki——它与 d3d12-resource-binding 形成一对显式 API 的姊妹章节，与 rendering-api-depth 上的深浅讨论直接呼应。

## [2026-04-14] ingest | Wave-10 Worker AC (simonschreibt.de ×5)

处理 5 篇 simonschreibt.de Game Art Tricks 拆解文（Deus Ex occlusion、Diablo 3 trees、Divine Divinity 2D reflection、Fallout 3 edges、Teleglitch RGB）。新增 4 个概念页（prebaked-corner-occlusion、painted-foliage-bent-planes、normal-decal-edge-blending、chromatic-aberration-post）、1 个人物页（simon-trumpler）、5 个源摘要。给 hbao-interleaved-sampling、normal-map-blending、crt-shader-effects、urp-volume-post-processing、dither-alpha-clipping、fizzle-lod-fading 提了 6 条 patch。5 篇全部保留（Simon 的博客本来就是纯技术美术干货）。

## [2026-04-14] ingest | Wave-10 Worker AD (blog.frost.kiwi ×5)

处理 5 篇 blog.frost.kiwi 文章。新增 2 概念页（color-banding、perceptual-colormaps）、2 source 摘要。跳过 3 篇（joyo-kanji 是日语学习，genshin impact anki deck 是 Anki 牌组分享，tunneling ssh over https 是网络运维）。最大亮点是 color-banding 长文——Jimenez 的一行 Interleaved Gradient Noise + 五家业界去带方案（Valve / Alien: Isolation / ReShade Deband / AE Ramp Scatter / KDE KWin blur + Windows Acrylic）横向拆解，加上一套相机翻拍 16-bit PNG 测屏幕真实位深的零成本自检法。perceptual-colormaps 把 matplotlib viridis 族和 DaVinci Resolve .cube 1D LUT 工作流打通，和 [[color-lut]] 游戏用法形成对称补充。frost-kiwi 人物页与 color-lut/color-space/dither-alpha-clipping 概念页通过 patch 追加相关链接与 source 引用。

## [2026-04-14] ingest | Wave-11 Worker AE (interplayoflight.wordpress.com ×5)

处理 Kostas Anagnostou / Interplay of Light 2013 年前 5 篇技术博客：tools of the trade、depth testing 阶段、tangent-free normal mapping、Unity as FX Composer replacement、SharpDX + Assimp model loading。5 篇全部入库。

新增概念页 4：[[tangent-free-normal-mapping]]、[[shader-prototyping-tools]]、[[sharpdx-assimp-pipeline]]、[[conservative-depth]]。新增人物页 1：[[kostas-anagnostou]]。新增 source 摘要 5：interplay-tools-of-the-trade / interplay-depth-testing / interplay-tangent-free-normal-mapping / interplay-unity-as-fxcomposer / interplay-sharpdx-model-loading。

Patch：[[early-z-late-z]] 补 Conservative Depth 相关链接与新 source；[[normal-map-blending]] 补 tangent-free 优化相关链接。

## [2026-04-14] ingest | Wave-11 Worker AF (etodd.io ×5)

处理 5 篇 etodd.io 2010-2011 早期独立游戏博客。Ingest 2 篇（meshes-of-navigation、refactoring-with-components），skip 3 篇 changelog/vision 文。新增 2 概念页（meshes-of-navigation-recast, component-entity-data-binding）、1 人物页（evan-todd）、2 source 摘要。对 ecs.md、a-star-pathfinding.md 打补丁补相关链接。

## [2026-04-14] ingest | Wave-11 Worker AG (graphicrants.blogspot.com ×5)

处理 5 篇 Brian Karis 的 Graphic Rants 博文。新增 3 概念页（virtualized-volume-textures, tiled-light-culling, sparse-shadows-cone-tracing）、1 人物页（brian-karis，Epic UE5 Nanite/Lumen 负责人）、3 source 摘要。跳过 2 篇：2010 年的 rgbd 帖被作者本人完全标为 hogwash 并删除正文；2011 年的 new-prey-2-screenshot 是宣传截图帖无技术实现内容。2012 年这两篇（tiled-light-culling + sparse-shadows-cone-tracing）是极高价值的 next-gen 渲染架构笔记——十年后 UE5 Lumen 几乎一字不差地实现了其中的核心假设（多几何表示 + cone trace + visibility 独立于光源跨光源共享）。patch 了 5 张已存在页：deferred-rendering / tiled-light-prepass / sdf-ray-marched-shadows / hierarchical-z-buffer / physically-based-shading。

## [2026-04-14] ingest | batch-w12-ah Cloud Wu 2010 H1 ×5

处理 5 篇云风 2010 年上半年博客，全部 ingested（无 off-topic）。主题覆盖 C 模块化/接口 friend 技巧、极简 C++ mark-sweep GC、C 自描述结构序列化、C 接口式 OOP、游戏引擎 VFS、malloc 调试壳。新建 1 人物页 (cloudwu)、6 概念页 (c-opaque-struct-modules, c-interface-oop, simple-cpp-mark-sweep-gc, c-serialization-metadata, game-engine-vfs, malloc-wrapper-debug)、5 source 摘要。向 modular-design / information-hiding / interface-vs-implementation 追加相关链接。

## [2026-04-14] ingest | Wave-12 Worker AI (interplayoflight.wordpress.com ×5)

处理 5 篇 Kostas Anagnostou 2013 年 Interplay of Light 博客的技术短文。全部 ingest。新增 5 概念页（instant-radiosity-vpl, parallax-corrected-cubemap, vertex-vector-interpolation-artifact, dual-depth-buffer-thickness, deferred-alpha-lighting），5 source 摘要。kostas-anagnostou 已存在，通过 add_source_link 补 5 条 Sources 并在『相关』区追加新概念链接。对 deferred-rendering、alpha-blending、tiled-light-prepass、fast-translucency-wraplight 补『相关』交叉链接。

## [2026-04-14] ingest | Wave-12 Worker AJ (momentsingraphics.de Peters papers ×5)

处理 Christoph Peters 博客上的 5 个条目：3 篇论文摘要页（Moment Shadow Mapping I3D 2015、Trigonometric Moment Transient Imaging SGA 2015、Beyond Hard Shadows I3D 2016）全部 ingest；2 篇 meta（about、publication-list）跳过。新增 2 概念页 moment-shadow-mapping、trigonometric-moment-transient-imaging，3 source 摘要。christoph-peters 人物页通过 patch 追加新贡献行与 source 链接；shadow-mapping-basics 追加到 MSM 的相关链接。全部内容围绕 Peters 的「矩方法」统一母题——把带界信号压成几阶矩、用经典矩问题闭式解在 GPU 上重建。

## [2026-04-14] ingest | batch-w13-ak Wronski 2014 系列（SSR / TAA / GCN）

Worker AK 处理 bartwronski.com 2014 年 5 篇，ingest 3 篇（future-of-SSR、temporal-supersampling、GCN latency hiding），跳过 2 篇意见类。新增 4 个概念页：[[screenspace-reflections]]、[[temporal-supersampling]]、[[gcn-wave-occupancy]]、[[gpu-latency-hiding]]；3 个源摘要；给 [[bartosz-wronski]] 增补 3 条 source 与概念引用；给 [[temporal-antialiasing]] 与 [[motion-vectors]] 增补 Wronski 祖师文引用。

## [2026-04-14] ingest | Wave-13 Worker AL (aras-p.info ×5)

处理 5 篇 aras-p.info 文章，ingest 4 篇技术稿、跳过 1 篇 blog list meta 页。新增 5 概念页（pcg3d-hash、worley-voronoi-noise、lossless-float-image-compression、openexr-format、meshoptimizer-vertex-codec）、4 source 摘要；为已存在的 aras-pranckevicius 与 non-cryptographic-hash 补链接与历史背景。

## [2026-04-14] ingest | Wave-13 Worker AM (raphlinus.github.io ×5)

处理 Raph Levien 博客 5 篇。跳过 2017 Recurse 个人项目清单；2018 Direct2D smooth resize 文章作为已有 smooth-window-resize 概念的 Windows 侧深挖，创建 source summary + 概念页补丁，不重复概念页；新增 3 个概念页：gpgpu-string-unescaping（monoid 同态 + parallel prefix scan 并行化状态机）、gpgpu-json-parsing（scan/scatter/sort 绕过栈处理 Dyck 语言）、ecs-for-rust-ui（xi-win-ui 的整数 id + state splitting + data flow 三板斧）。

## [2026-04-14] ingest | batch-w14-an fgiesen.wordpress.com 2010 年系列（细胞纹理 / CSA / 不变量）

Worker AN 处理 fgiesen.wordpress.com 2010 年 5 篇，ingest 4 篇，跳过 1 篇意见类（we-dont-need-new-multimedia-formats）。新增 3 个概念页：[[cellular-texture-generation]]（rendering，ryg Werkkzeug3 细胞纹理离线生成）、[[carry-save-adder-pixel-avg]]（computer-systems，CSA 打包像素平均 SWAR）、[[data-structure-invariants]]（software-design，不变量诞生与清理法）；4 个源摘要（ryg-cellular-textures-1 / -2 / carry-save-adders / data-structures-and-invariants）。[[fabian-giesen]] sources 5→9 并增补概念引用；[[worley-voronoi-noise]] 增补对离线生成篇的交叉引用；[[sse-tricks]] 指向 CSA 打包像素技巧。

## [2026-04-14] ingest | Wave-14 Worker AP (elopezr.com 2014 早期 ×5)

处理 5 篇 Emilio López Ros 2014 年早期博文，全部 ingested。新增 2 概念页（floyd-steinberg-dithering, java-vector-math-limitations）、5 源摘要。emilio-lopez-ros 人物页已存在，追加 5 条 source 链接并在风格段补一段早期 Android / Java 时期的背景。另补丁 dither-alpha-clipping 增加与 Floyd–Steinberg 的对照。

## [2026-04-14] ingest | Wave-15 Worker AQ (Xor GM Shaders Mini ×5)

处理 5 篇 Xor 的 GM Shaders Mini 2022 年 8-9 月文章（texels/pixels、recursive/ping-pong、code golfing、dot product、creative code）。新增 5 个渲染概念页（texel-pixel-conversion, ping-pong-surfaces, shader-code-golfing, vector-dot-product, creative-coding-process）和 5 个 source 摘要。对 xor-shader-artist 人物页追加 5 条贡献；给 diffuse-lighting-lambertian 和 shader-vector-math-primer 补链。无跳过。

## [2026-04-14] ingest | Wave-15 Worker AR (ciechanow.ski 2014 早期 ×5)

处理 5 篇 Bartosz Ciechanowski 2014 年的早期文章——这是他博客刚开始时的硬核低层时期，远早于后来的交互可视化。Exploring GPGPU on iOS（A7 + Transform Feedback 的 GPGPU hack，作者本人已标为 historical reference）、Drawing Bézier Curves（Revolved 应用里的曲线描边三角化，博客上首篇带交互 demo）、Exposing NSMutableArray（`class-dump` + Hopper 逆向出 `__NSArrayM` 是循环缓冲 deque，1.625× 扩容、从不收缩）、Exposing NSDictionary（逆向 `__NSDictionaryI` 发现用 indexed ivars + 线性探测 + 质数 size 表 + 62% 装载率上限）、以及后者的 ARM64 汇编附录页。新增 5 概念页（gpgpu-transform-feedback-ios / bezier-curve-triangulation / nsmutablearray-circular-buffer / nsdictionary-linear-probing / objc-runtime-internals）、5 source 摘要。bartosz-ciechanowski 已存在，仅 patch 风格 + 贡献表 + 相关 + sources。

## [2026-04-14] ingest | Wave-15 Worker AS (halisavakis.com ×5)

处理 halisavakis.com 早期文章 5 篇。新增 3 概念页（bluk-2d-fog-sprite-shader、unity-image-effect-basics、night-time-tint-shader）、3 source 摘要。跳过 2 篇（Sling Toss 隐私政策、Leucos Ludum Dare postmortem）。补丁 harry-alisavakis 人物页与 fragment-shader 概念页的交叉引用。

## [2026-04-14] ingest | Wave-16 Worker AT (danielilett.com Image Effects 0-3)

处理 Daniel Ilett 《Image Effects》系列 part 0-3（共 5 个文件，其中 series-introduction 跳过）。新增 4 概念页：image-effect-colour-transform、depth-texture-silhouette、image-convolution-kernel、separable-gaussian-blur；新增 4 个 source 摘要；给 daniel-ilett、unity-image-effect-basics、shaderlab-hlsl-basics、z-buffer 打补丁添加交叉引用和 source 链接。part 0 作为 shader 基础入门没有单独建概念页，而是补到已有的 shaderlab-hlsl-basics / unity-image-effect-basics。

## [2026-04-14] ingest | Wave-16 Worker AU (ronja-tutorials.com 001-005)

处理 Ronja's Shader Tutorials 2018 基础系列 5 篇（Structure / HLSL / Variables / Basic Shader / Surface Shader Basics）。5 篇全部 ingested，新增 5 个 source 摘要页，0 个新概念页（核心概念 shaderlab-hlsl-basics / unity-surface-shaders / fragment-shader / shader-vector-math-primer / rendering-pipeline / coordinate-spaces 全部已存在）。Patch 到 ronja-bohm 人物页追加 5 来源链接，另外给 4 个概念页各追加对应的 source 链接。

## [2026-04-14] ingest | Wave-16 Worker AV (alanzucconi.com 2012 ×5)

处理 alanzucconi.com 2012 年 5 篇早期博客。仅 ingest 1 篇技术内容（Flixel 2.5 上的 CRT RGB 通道偏移 CPU 实现），新增 1 个 source 摘要 `alanzucconi-flixel-retro-crt` 并 patch 到现有 `crt-shader-effects` 与 `alan-zucconi`。跳过 4 篇非技术：RAPTUS postmortem / RAPTUS 评论汇编 / Indie Games Expo 2012 见闻 / Still time devlog #1。

## [2026-04-14] ingest | Wave-17 Worker AW (thenumb.at Max Slater ×5)

处理 5 篇 thenumb.at Max Slater 长文：4 篇技术 ingest（hot reload / Hamming hats / exponential rotations / autodiff），1 篇 graphics-blogroll 跳过（纯链接列表）。新建 4 概念页（binary-hot-reload, hamming-code-hat-puzzle, exponential-map-rotations, automatic-differentiation）和 4 source 摘要。Patch max-slater 人物页追加 4 source；patch 3d-rotation-math 追加 exp-map 交叉引用与 source。

## [2026-04-14] ingest | Wave-17 Worker AX (lindenreid.wordpress.com Limit Theory procgen ×5)

处理 Linden Reid 2017 年为 Limit Theory 写的 5 篇 CPU 侧程序化几何教程（stellation、extrusion、torus、sphere/ellipsoid、tessellation-triangulation）。按 orchestrator 建议合并成 2 个新概念页：procedural-mesh-primitives（参数化基元：torus + sphere + ellipsoid）和 mesh-warps-and-tessellation（per-face warp 与三角化算法）。新增 5 个 source 摘要；对已有的 linden-reid 人物页和 unity-procedural-mesh 打补丁以添加交叉引用和新 source 链接。linden-reid 的 sources 从 3 更新为 8。

## [2026-04-14] ingest | Wave-17 Worker AY (cyangamedev.wordpress.com ×5)

处理 Cyan 5 篇 Shader Graph / URP 教程：Render Textures、Voronoi、World-space UVs & Triplanar、Orthographic Depth、Watercolour Shader Experiments。新增 4 个概念页（render-textures-unity / triplanar-mapping / orthographic-depth / watercolour-shader-experiments）+ 5 个 source 摘要。Voronoi 一篇与已有 worley-voronoi-noise 重叠（算法和哈希依赖部分），改为 patch 形式追加 Cyan 的 Shader Graph 实现说明 + source link。cyanilux 人物页 sources 5→10。无新人物。

## [2026-04-14] ingest | Wave-18 Worker AZ (3dgep.com Jeremiah ×5)

处理 3dgep.com 上 Jeremiah van Oosten 2011 年发布的 5 篇早期教程：3D 数学入门（向量/矩阵）、DirectX 9 入门、MD5 模型加载、MD5 GPU skinning。新增 2 个概念页（md5-model-format, gpu-skinning-matrix-palette）、5 个 source 摘要；数学 primer 与 D3D9 入门内容与既有页面重叠，仅 patch 不重建。jeremiah-van-oosten 人物页追加 5 条 source 链接与 4 条相关概念。

## [2026-04-14] ingest | Wave-18 Worker BA (vertexfragment.com Steven Sell ×5)

处理 Steven Sell 的 vertexfragment.com 5 篇，跳过 projects portfolio 页，ingest 其余 4 篇：Bresenham 直线、可变长度 Bresenham、Performance Conscious WebGL、Cantor & Szudzik 配对函数。新增 4 概念页（bresenham-lines / variable-length-bresenham / performance-conscious-webgl / cantor-szudzik-pairing）与 4 source 摘要。steven-sell 人物页已存在，仅通过 patch 追加 source 链接。

## [2026-04-14] ingest | Wave-18 Worker BB (blog.mecheye.net 早期 GNOME ×5)

5 篇 2011-2012 年 Jasper St Pierre 关于 GNOME Shell 开关控件、不可见边框、扩展 API 重构、GJS introspection 与 prefs.js 的博客笔记。均为桌面环境 / 插件框架内容，与图形渲染、引擎、系统编程主题无关，全部跳过，未生成任何 wiki 页面。

## [2026-04-14] ingest | Wave-19 Worker BC (eliasdaler.wordpress.com x5)

处理 Elias Daler 博客 5 篇早期文章。Lua+C++ 系列三篇（Part 1/2/2.5）合并为单一概念 [[lua-cpp-binding]]；[[z-order-top-down-2d]] 为独立概念。新增人物 [[elias-daler]]、2 个 source 摘要。跳过 hello 介绍文。

## [2026-04-14] ingest | Wave-19 Worker BE (giordi91.github.io Marco Giordano ×3)

处理 Marco Giordano (giordi91) 的 3 篇博客：Rust 反汇编导览、GPU 驱动草地、句柄式资源管理。全部 ingest，新增 1 人物页（marco-giordano）、3 概念页（rust-disassembly-tour / gpu-driven-grass-tiles / handle-based-resource-manager）、3 source 摘要。新概念页与既有的 deferred-grass-shader / resource-system-design 形成『同题不同解』对照组，双向 patch 交叉链接；另外 patch culling / alan-zucconi / kostas-anagnostou 追加引用。

## [2026-04-14] ingest | Wave-20 Worker BF (momentsingraphics.de ×5, MSM extensions)

处理 5 篇 momentsingraphics.de 上 Christoph Peters 关于 moment shadow mapping 的扩展工作：GDCE 2016 讲座、cubic equation 快速 HLSL 求解、JCGT 2016 demo 发布、JCGT 2017 改进论文、HPG 2017 非线性量化论文。新增 2 个概念页（cubic-equation-solver-hlsl、non-linearly-quantized-msm），5 个源摘要页，并对 moment-shadow-mapping、polynomial-root-finding-gpu、christoph-peters 三页打补丁补全相关与 sources 链接。

## [2026-04-14] ingest | Wave-20 Worker BG (anteru.net 2010 ×5)

处理 anteru.net 2010 年 5 篇早期文章。Ingest 3 篇技术内容：DX11 早期踩坑笔记 → [[directx11-early-pitfalls]]，齐次坐标光栅化转置 bug → [[homogeneous-rasterization-transpose-bug]]（与 [[triangle-setup]] 互链），默认避免 unsigned 类型 → [[avoid-unsigned-types]]。新增 3 个 source 摘要，并为已有的 [[matthaeus-chajdas]] 人物页追加 3 个新作品链接。跳过 XP retail/OEM hack 与 Bazaar VCS 推荐 2 篇（非主题或工具已过时）。

## [2026-04-14] ingest | Wave-20 Worker BH (apoorvaj.io ×5)

处理 apoorvaj.io 5 篇。Ingest 2 篇技术贴：what-is-opengl-loading（X-macro 手写 GL loader 取代 GLEW）、normal-mapping（切线空间 TBN + 视差家族）。新增 2 概念页（opengl-loader, tangent-space-normal-mapping）、2 source 摘要。Skip 3 篇：cross-platform-consistency（按指令重复 skip）、before-we-begin / acknowledgements（meta）。补丁更新 apoorva-joshi 人物页与三张相邻法线贴图概念页。

## [2026-04-14] ingest | Wave-21 Worker BI (blog.codingnow.com 2010-06..10 ×5)

处理云风博客 2010 年 6-10 月 5 个月度归档。Ingest 4 篇：Lua 访谈校译（Roberto/Luiz on Lua 设计哲学、机制 vs 法策、有栈协程、ANSI C 偏执）、C tagged union dispatch（XEvent 风格的类型安全多变体接口）、网易资源包格式（允许空洞、二进制 diff 补丁、新引擎 FAT 风格分块设想）、Effective C++ 3rd Item 1 评注（C++ 当语言联邦、团队必须定义子集）。Skip 2010-09 新西兰南岛自驾游记。新增 4 概念页（lua-design-philosophy, c-tagged-union-dispatch, game-resource-pack-format, cpp-multi-paradigm-discipline）+ 4 source 摘要，补丁更新 cloudwu / lua-cpp-binding / closure / classitis / game-engine-vfs。

## [2026-04-14] ingest | Wave-21 Worker BJ (blog.playcanvas.com ×5)

处理 5 篇早期 PlayCanvas 博客（2012-2013）。4 篇营销/社区公告跳过（引擎介绍、D.E.M.O. FPS 案例、Answers 社区发布、Dungeon Fury 移动版），仅 1 篇 HTML5 游戏开发 API 清单被沉淀——新增 1 概念页 [[html5-game-apis-2012]] + 1 source 摘要 [[sources/playcanvas-html5-game-apis]]。不新增人物页。

## [2026-04-14] ingest | Wave-21 Worker BK (interplayoflight.wordpress.com ×5)

处理 interplayoflight 5 篇。按 P9 指令 skip readings-on-physically-based-rendering（纯 PBR reading list，无新技术内容）。Ingest 4 篇：(1) educational normalised Blinn-Phong—给美术的 PBR 教学 FX Composer shader；(2) branches and texture sampling—HLSL if 分支内 shader-computed uv 触发 compiler flatten 的隐形性能坑；(3) rendering fur using tessellation—D3D11 isoline domain + master strand + Phone Wire AA；(4) SkySaga/Meandros engine tech 总览—token stream + deferred + voxel AO + G-Buffer weather modification + 3D LUT。新增 4 概念页（normalised-blinn-phong-shader, divergent-gradient-in-branches, tessellation-fur-rendering, skysaga-rendering-tech）、4 source 摘要。补丁更新 kostas-anagnostou 人物页和 microfacet-brdf / physically-based-shading / fragment-shader / deferred-rendering / deferred-grass-shader / voxel-ambient-occlusion / greedy-voxel-meshing / color-lut / journey-sand-specular 九张相邻概念页。

## [2026-04-14] ingest | Wave-22 Worker BL (halisavakis.com image-effect series ×5)

处理 halisavakis.com 2017-05 到 2017-06 的 image effect 教程连载 5 篇。新增 2 个概念页（image-effect-mask-blend、合并的 uv-displacement-image-effect），5 个 source 摘要。chromatic-aberration / grabpass 命中已存在概念页（chromatic-aberration-post / unity-grabpass-blur / unity-image-effect-basics），全走 patch。harry-alisavakis 人物页已存在，补 patch 链入新页与 sources。

## [2026-04-14] ingest | Wave-22 Worker BM (bartwronski.com ×5)

处理 bartwronski.com 5 篇。按 P9 指令 skip 两篇 C#/.NET graphics framework 框架发布 / GitHub 迁移公告（无实质技术内容）。Ingest 3 篇：(1) bokeh-depth-of-field-going-insane-part-1—_The Witcher 2_ 的 scatter bokeh DoF，点精灵 + vertex shader 放大 + premultiplied additive，附 C# 重实现的 indexed draw / procedural vertex from ID / double-width atlas 优化；(2) temporal-supersampling-pt-2-ssao-demonstration—AC4 上 temporal SSAO 的 before/after，3 采样图案轮换 + 深度 rejection + 0.9 历史权重，关键点：在 blur **前**做 temporal、Scalable AO 把深度塞进 AO 纹理所以 rejection 免费、动机和 DICE/Epic 不同（追求多样本而非降 flicker）；(3) runtime-editor-console-connection-in-the-witcher-2—Witcher 2 X360 的编辑器-主机实时调参工具链，复用脚本调试网络通道，支持 camera 劫持 / streaming layer / 灯光 add-move / 环境预设 / post-process shader reload，诚实复盘 streaming 工具因实体系统混淆玩法逻辑和视觉表现而失败。新增 2 概念页（scatter-bokeh-dof, runtime-editor-console-connection）、3 source 摘要。补丁更新 bartosz-wronski 人物页（+3 sources, +2 concepts）、temporal-supersampling（AC4 SSAO 细节补充 + new source）、thin-lens-model / chromatic-aberration-post / alpha-blending / draw-procedural-gpu / hbao-interleaved-sampling 五张相邻概念页的相关章节。

## [2026-04-14] ingest | Wave-22 Worker BN (fgiesen.wordpress.com 2010-10 ×5)

处理 5 篇 ryg 2010 年 10 月的技术文章：环检测算法、64 位平台小坑、视锥剔除（两篇合并）、shader 数学化简清单。新增 4 概念页（cycle-detection-floyd-brent、x64-platform-tidbits、view-frustum-culling-ryg、hlsl-derivation-correctness）、5 source 摘要。fabian-giesen 人物页已存在，仅补 5 条 source 链接。frustum 两篇合并成一页是按 P9 指示。

## [2026-04-14] ingest | Wave-23 Worker BO (danielilett.com image effects 4/5/6)

处理 Daniel Ilett Image Effects 系列 Part 4/5/6：Sobel 边缘检测 + 简易 Bloom、NES/SNES/GB 色彩量化 + CRT 扫描线、Kuwahara 油画滤镜。新增 4 个概念页（sobel-edge-detection, bloom-threshold-blur-composite, color-quantization-retro, kuwahara-filter）和 3 个 source 摘要。按指令跳过 Part 7 wrapping-up 与 cel-shading-introduction 两篇 meta 文章。对 daniel-ilett、unity-image-effect-basics、image-convolution-kernel、crt-shader-effects、retro-rendering-techniques 五个既有页面做反向链接 patch。

## [2026-04-14] ingest | Wave-23 Worker BP (ronja-tutorials.com 006-011 ×5)

处理 ronja-tutorials.com 2018-04 到 2018-05 的 shader 系列 006/007/009/010/011 共 5 篇。新增 3 概念页（sprite-shaders-unity、shader-color-interpolation、procedural-checkerboard），5 份 source 摘要。basic-transparency 命中 alpha-blending、triplanar 命中 triplanar-mapping，均走 patch。ronja-bohm 人物页已存在，补 patch 追加 5 个 source 与新概念链接（sources 10→15）。

## [2026-04-14] ingest | Wave-23 Worker BQ (Xor GM Shaders ×5)

处理 5 篇 Xor/mini.gmshaders.com 教程：raymarching、mini-rotation、mini-two-textures、mini-shadertoy、fractal-texturing。新增 4 个概念页（raymarching-intro、two-texture-sampling-tricks、shadertoy-basics、fractal-texturing）和 5 个 source summary。Mini: Rotation 仅打补丁到现有 [[3d-rotation-math]]。对 xor-shader-artist、volumetric-raymarching-intro、sdf-ray-marched-shadows、texel-pixel-conversion 发起交叉链接补丁。

## [2026-04-14] ingest | Wave-24 Worker BR (alanzucconi.com ×5)

处理 5 篇 Alan Zucconi 文章：3 篇跳过（1 篇 devlog + 2 篇游戏期待清单）；2 篇技术文章 ingest。To Voronoi and Beyond 以补丁形式增强已有的 [[worley-voronoi-noise]]（新增 Minkowski 距离插值、brute-force shader 实现、Wellons cone projection 等要点），不新建概念页。How to find the main colours in an image 新建 [[color-quantization-kmeans]] 概念页——与已有的 [[color-quantization-retro]] 形成互补的两种'颜色量化'含义（前者 K-Means 找主色，后者每通道砍级数模仿老主机）。补 [[alan-zucconi]] 人物页的 2 条 source 链接。

## [2026-04-14] ingest | Wave-24 Worker BS (halisavakis.com ×5)

处理 4 篇 halisavakis.com *My take on shaders* 教程：custom-masks part I/II（合并）、shockwave、stencil antichamber。跳过 1 篇 postmortem。新增 3 概念页（custom-mask-shaders、shockwave-effect、stencil-portal-shader-antichamber）和 4 source 摘要。补丁打到 harry-alisavakis、image-effect-mask-blend、uv-displacement-image-effect、stencil-buffer 四页。

## [2026-04-14] ingest | Wave-24 Worker BT (lindenreid.wordpress.com 2017-12 ×5)

Linden Reid 2017 年 12 月的 Unity shader / 程序化几何四连发。新增 3 概念页（procedural-greeble / stylized-water-shader / cel-shader-outline）、4 source 摘要。texture-dissolve 概念已存在，只 patch 加 source 链接。unity-graphics-setup 纯编辑器配置指南跳过。linden-reid 人物页补 4 条 source 链接与「2017-12 Unity Shader 系列」小节。

## [2026-04-14] ingest | Wave-25 Worker BU (c0de517e ×5 all-skip)

批次 batch-w25-bu：全部跳过。4 篇 meta（new-layout、3d-engines-out-there、homework、collaborative-design-experiment），1 篇 small-brdf-visualizer 为作者自述玩具级 HLSL 片段，技术增量不及现有 [[microfacet-brdf]]。

## [2026-04-14] ingest | Wave-25 Worker BV (aras-p.info ×1)

批次 batch-w25-bv：1 篇。Syntonic Dentiforms redux —— Aras 把 2004 年 D3D9 demo 移植到 sokol_gfx（Windows/Linux/Mac/Web），并把原本 216 文件 24k 行的 C++ 抽象重灾区砍成 49 文件 6k 行。新增 1 source 摘要；patch 到 [[classitis]] 与 [[aras-pranckevicius]]。未新建概念页：相关概念均已存在。

## [2026-04-14] ingest | Wave-25 Worker BW (blog.mecheye.net ×5)

处理 5 篇 Jasper St. Pierre 的博文。跳过 1 篇 GNOME Shell Extension 提交指南（非技术）。纳入 The Linux Graphics Stack（2012 栈综述）、Bytecode（ACPI/字体/BPF 字节码考古）、Barriers（XI 2.3 pointer barrier pressure）、Xplain（交互式 X11 科普系列启动公告）。新增 4 概念页（x11-composite-redirection、wayland-compositor-model、bytecode-everywhere、x11-pointer-barrier）、4 source 摘要，并给既有 linux-graphics-stack-dri / jasper-st-pierre 两页打 patch 加相关链接与 Source 列表。

## [2026-04-14] ingest | Wave-26 Worker BX (etodd.io ×5)

处理 5 篇 etodd.io 文章。新增 2 概念页（csharp-runtime-script-compilation, tools-first-iteration-loop）、3 source 摘要。给现有 component-entity-data-binding 追加 Property/Binding/Command 实现细节小节。给 evan-todd 人物页追加新概念与新 source 链接。跳过 2 篇 career/devlog 进度文。

## [2026-04-14] ingest | Wave-26 Worker BY (interplayoflight.wordpress.com ×5)

处理 5 篇 Kostas Anagnostou 技术博客。新增 3 概念页：unity-postprocessing-adventures、unreal-frame-breakdown（3 篇 How Unreal Renders a Frame 合一，sources=3）、gpu-based-occlusion-culling；新增 5 个 source 摘要页。不重建 kostas-anagnostou / deferred-rendering / occlusion-culling / hierarchical-z-buffer / volumetric-fog-froxels / temporal-antialiasing。

## [2026-04-14] ingest | Wave-26 Worker BZ (simonschreibt.de ×5)

处理 5 篇 Simon Trümpler 早期 Game Art Tricks 短文（Teleglitch 视野阴影、cell shading 描边、Deus Ex 布料褶皱、Deus Ex 屏幕扫描线、WoW 热气球 lit sphere）。新增 5 个 rendering 概念页（sprite-outline-8-direction, extruded-wall-shadow-viewcone, animated-parallax-cloth-fold, mipmap-moire-scanline, lit-sphere-matcap-shading）、5 个 source 摘要。simon-trumpler 人物页已存在，追加 sources 与 相关 链接。

## [2026-04-14] ingest | Batch w27-ca Worker (allenchou.net ×5)

处理 5 篇 allenchou.net 早期博客（2011 ActionScript3/Molehill 时期）。建 2 概念页：scene-graph-matrix-stack-visitor（游戏引擎，访问者模式 + 矩阵栈遍历场景图）、strategy-vs-switch（软件设计，Fowler 经典重构）。建 3 source 摘要。allen-chou 人物页已存在，追加三条 source 链接与两条相关概念。shader-primer 与既有 shader-vector-math-primer 主题不冲突（前者讲管线，后者讲向量数学），仅做交叉链接。跳过 2 篇：packing-my-stuff（生活更新）、bunnyhill-interface-design（个人 API 意见稿）。

## [2026-04-14] ingest | Wave-27 Worker CB (metalbyexample.com ×5)

处理 metalbyexample.com 第二批 5 篇，全部 ingest。新增 3 概念页（metal-3d-rendering-pipeline / metal-texture-sampler / metal-compute-image-filter）和 5 source 摘要。linear-algebra 与 mvp-transform / shader-vector-math-primer 重叠，按约束只作 source-only + patch。feature-sets 是短参考文（A7/A8 GPU 能力差异），source-only + metal-api-overview patch。warren-moore 人物页追加五条贡献与新 sources 链接。

## [2026-04-14] ingest | Wave-27 Worker CC (thenumb.at Max Slater ×5)

处理 5 篇 Max Slater 技术长文：Neural Graphics Primitives、Optimizing Open Addressing、Spherical Integration、Oxidizing C++、Monte Carlo Crash Course Part 1 (Continuous Probability)。新增 5 概念页（neural-graphics-primitives, open-addressing-hashtable, spherical-integration, rpp-stl-replacement, continuous-probability）、5 source 摘要。max-slater 人物页已存在，追加 5 source 链接。Part 1 (2025-03-29) 与已有 Part 5 QMC (slater-qmc-crash-course) 独立收录。

## [2026-04-14] ingest | Batch w28-cd（raphlinus.github.io ×5）

处理 5 篇 Raph Levien 博客文章。Ingest 2 篇：UB 分析（新概念 undefined-behavior-c-cpp）与 sigmoid 数学（新概念 sigmoid-functions）；跳过 3 篇（物理书评、职业帖、合成器 devlog）。新增 2 source 摘要、对 raph-linus / faster-math-functions / avoid-unsigned-types 追加交叉引用。

## [2026-04-14] ingest | Wave-28 Worker CE (anteru.net ×5 systems-engineering)

处理 5 篇 anteru.net 2010 年软件工程类文章：reporting compiler bugs、C++ unit testing frameworks revisited、build engineering、Bazaar 2.2 发布、research project 自动化测试。全部跳过：都是 process/opinion/工具新闻，没有图形/引擎/系统/PL 的核心技术内容落点；且 matthaeus-chajdas 人物页已明确只收录 Anteru 的渲染/编译器方向文章。无概念页、无 source 摘要、无 patch。

## [2026-04-14] ingest | Wave-28 Worker CF (bartwronski.com 2014 ×5)

处理 5 篇 Bart Wronski 2014 年博客。Ingest 2 篇：Hair rendering trick(s)（Witcher 3 / Cyberpunk 原型期 4 pass 混合 deferred/forward 头发管线 + Witcher 2 SSS hack）、CSharpRenderer + volumetric fog code（Siggraph 2014 talk 配套开源 froxel 体积雾 compute shader demo 发布公告）。跳过 3 篇：Sony A7 相机评测、Python 科学工具链主观感受、CSharpRenderer 10 月功能 roll-up。新增 1 概念页 hybrid-hair-rendering、2 source 摘要（hair-rendering-tricks, csharprenderer-volumetric-fog）。bartosz-wronski 与 volumetric-fog-froxels 既有页通过 patch 追加 source 链接与交叉引用。

## [2026-04-14] ingest | Wave-29 Worker CG (elopezr.com CLOS2 ×5)

处理 5 篇 elopezr.com：跳过 4 篇（match-3、the-cube、cars 三篇 2014 早期 postmortem 沿袭 w14 先例；replay-system-using-unity 技术密度不足）。Ingest 1 篇：The Rendering of Castlevania: Lords of Shadow 2（2015）——DX9 世代延迟管线 + Valve Ambient Cube + box light 的 AAA 帧拆解。新增 1 概念页（valve-ambient-cube）与 1 源摘要。emilio-lopez-ros 人物页追加 source 链接与文章表条目。

## [2026-04-14] ingest | Wave-29 Worker CH (interplayoflight.wordpress.com ×5)

处理 5 篇 Kostas Anagnostou / Interplay of Light 技术博客：2017 年的 deferred SDF rendering 实验、2018 年 GPU-driven occlusion 系列 Part 2（MultiDraw + LOD）、bgfx 移植、Digital Dragons 大会版 20K 规模化、2018 年 hybrid raytraced shadows + reflections 的 compute shader 实现。全部 ingest 无 skip。新增 3 个概念页（deferred-sdf-rendering / multidraw-indirect-occlusion-culling / hybrid-raytraced-shadows-reflections）与 5 个 source 摘要；对 kostas-anagnostou、gpu-based-occlusion-culling、hybrid-raytracing-pipeline、deferred-rendering、sdf-ray-marched-shadows 5 个既有页面发了 patch。

## [2026-04-14] ingest | batch-w29-ci Daniel Ilett Cel Shading Parts 0/2/3/4/5

处理 Daniel Ilett 2019 年 Cel Shading 系列 5 篇（Part 0 理论 / Part 2 自定义 Lighting / Part 3 bump+fresnel / Part 4 描边 / Part 5 Stencil ID + ramp 纹理）。新增 1 概念页 cel-shading-pipeline（合并 5 部曲为一条完整的 Unity 内建管线卡通渲染流水线）、5 个 source 摘要；为 diffuse-lighting-lambertian、cel-shader-outline、unity-surface-shaders、daniel-ilett 发补丁追加 source 链接与 `[[cel-shading-pipeline]]` 相关条目。未创建新人物页（daniel-ilett 已存在）。

## [2026-04-14] ingest | Wave-30 Worker CJ (halisavakis.com ×5)

处理 Harry Alisavakis 5 篇 shader 教程（dissolve / random-stripes / glitch / ABZÛ portal cards / shader-bits world+screen pos）。新增 4 概念页（random-stripes-mask-shader、glitch-image-effect、abzu-portal-cards-shader、world-screen-space-position-shader）、5 source 摘要；dissolve 篇与已有 texture-dissolve 重合，只补 Cull Off / addshadow 坑点 + burn ramp 实现 + source 链接。harry-alisavakis / coordinate-spaces / custom-mask-shaders / chromatic-aberration-post / uv-displacement-image-effect 追加相关链接补丁。

## [2026-04-14] ingest | Wave-30 Worker CK (alanzucconi.com ×5)

处理 5 篇 alanzucconi.com 2015 年早期文章。新增 1 source 摘要（alanzucconi-shader-intro-unity，Built-in RP 时代 Shader 系列 Part 1），patch 了 alan-zucconi 人物页和 shaderlab-hlsl-basics / unity-surface-shaders 两个概念页的 Sources 段。跳过 4 篇：3 篇 most-anticipated-games 游戏预览合集 + 1 篇 Python/BeautifulSoup 抓取截图的 web scraping 教程。无新概念页、无新人物页。

## [2026-04-14] ingest | Wave-30 Worker CL (fgiesen.wordpress.com ×5)

处理 5 篇 ryg 2010-2011 技术文章：DCT 平面旋转四种实现（planar-rotation-dct）、PPC int→float LHS（ppc-int-float-lhs）、编程的负空间哲学（negative-space-in-programming）、环形缓冲区虚拟流模型（ring-buffer-virtual-stream）、纹理嵌套分块 swizzle 与减-与增量（texture-swizzle-nested-tiling）。全部 ingest，新增 5 概念页 + 5 source 摘要。fabian-giesen 人物页 sources+6 相关 patch；data-structure-invariants / cache-friendliness / complexity 三页 patch 增加交叉引用。

## [2026-04-14] ingest | Wave-31 Worker CM (lindenreid.wordpress.com ×5)

处理 5 篇 Linden Reid 2017-2018 Unity shader 教程。Ingest 3 篇：动画虚线描边（animated-dotted-outline-shader，`sin(distance)` 距离场 + `_Time` 相位平移）、冰晶 shader（ice-shader-unity，Fresnel 边缘 + lazy noise normal + GrabPass 屏幕扭曲）、摆动草丛（waving-grass-shader-vertex-offset，世界空间风场纹理 + sin/cos 顶点位移 + heightFactor）。跳过 tutorials.md 链接索引页。intro-to-procedural-geometry-part-1 与既有 unity-procedural-mesh / procedural-mesh-primitives 高度重叠，只 patch 不新建。linden-reid 人物页追加 Sources 与相关链接；cel-shader-outline patch 引入动画虚线扩展的交叉引用。

## [2026-04-14] ingest | Wave-31 Worker CN (vertexfragment.com ×5)

处理 5 篇 Steven Sell / Vertex Fragment 文章。新增 3 概念页（windows-bmp-format, surface-angle-silhouette, nested-loop-optimization）、4 source 摘要。Sobel outline 作为现有 sobel-edge-detection 的补丁源合入。跳过 1 篇 AWS Lambda DevOps（非技术图形/系统主题）。复用 steven-sell 人物页，通过补丁更新 sources 计数和链接列表。

## [2026-04-14] ingest | Wave-31 Worker CO (mini.gmshaders.com ×5)

处理 5 篇 Xor Mini 系列短文。新增 2 概念页（classic-shader-noise 合并 noise + noise2 两篇、env-mapping-cubemap-shader）与 5 源摘要（xor-mini-interpolation / noise / noise-2 / environments / hlsl）。Mini: Interpolation patch 到 shader-color-interpolation、Mini: HLSL patch 到 shaderlab-hlsl-basics；worley-voronoi-noise、layered-grid-noise、xor-shader-artist 追加交叉引用与源链接。无人物新增、无跳过。

## [2026-04-14] ingest | Wave-32 Worker CP (gameknife.github.io ×5)

处理 5 篇 gameknife.github.io 博客，2 篇 ingested / 3 篇 skipped。新增 1 概念页 dynamic-resolution-scaling（变分辨率渲染：半分辨率 SSAO/shadow mask 边界白边 workaround、0.75× + 锐化补偿、tex2Dlod→tex2Dgrad 陷阱），2 源摘要（gkengine-rendering-optimization / custom-vc100-toolchain）。patch 到 gkengine、people/gameknife、deferred-rendering、bottleneck-analysis。跳过 skill 元页、mu-biao-shi-xing-chen-da-hai（个人目标宣言）、WISDE 婚礼邀请系统。

## [2026-04-14] ingest | Wave-32 Worker CQ (gametorrahod.com ×5)

处理 gametorrahod.com 5 篇泰语博文。仅 1 篇命中主题：新建 [[ios-app-thinning]] 概念页 + gametorrahod-ios-app-thinning 源摘要。其余 4 篇跳过（Nintendo CEO 追忆、Jam Experiment 消费心理学、YouTube H.264 音画偏差小贴士、AWS S3+Route53 个人站托管教程）。

## [2026-04-14] ingest | Wave-32 Worker CR (cloudwu 2010-11 ~ 2011-03)

处理云风 blog 五篇月度归档。4 篇技术全部 ingest：Go 语言初步、梦幻西游服务器 IO 优化、ZeroMQ 模式、Lua 5.1 增量式 GC 源码剖析。新增 5 概念页 (go-goroutine-channels, connection-multiplexer-gateway, snapshot-diff-persistence, zeromq-messaging-patterns, lua-incremental-gc) 与 4 source 摘要。1 篇（2011-01 父亲业委会维权信件）skip 为非技术。cloudwu 人物页追加新源与相关概念。

## [2026-04-14] ingest | Wave-33 Worker CS (danielilett.com ×5)

处理 5 篇 danielilett.com 2024 年教程，4 篇 ingested / 1 篇 skipped。新建 4 概念页（godot-visual-shaders / shader-graph-lighting-primer / mgs-stealth-camo-shader / pokemon-terastallize-shader），4 source 摘要。跳过 games-shaders-tutorials（链接索引页）。Patch 到 daniel-ilett（追加 4 概念 + 4 sources）、scene-color-depth-nodes（stealth camo 作为最短 Scene Color 实战）、hlsl-derivation-correctness（terastallize 是 DDX/DDY 的 practical 样板）、cel-shader-outline（Godot hull outline 的跨引擎等价）、diffuse-lighting-lambertian、cel-shading-pipeline。关键 takeaways：(1) Godot VisualShader 没有 World Position 节点、要用 Varying 机制手搭，但 VisualShaderNodeCustom 的 `_get_global_code()` 比 Unity Custom Function 更强；(2) Shader Graph Lit 图的 roughness↔smoothness 语义翻转是新手陷阱；(3) Scene Color = URP _CameraOpaqueTexture 的『透过物体看背景』骨架；(4) DDX/DDY 叉积在 shader 端重建 flat normal 是不改 mesh 的最便宜方案，Shader Graph 缺 Primitive ID 时只能用贴图烘 Triangle ID 的 workaround。

## [2026-04-14] ingest | Wave-33 Worker CT (mini.gmshaders.com ×5)

处理 5 篇 Xor 的 mini.gmshaders.com 技术短文，全部 ingested。新增 3 个概念页（multiple-render-targets、mipmap-generation-sampling、webgpu-intro），5 个 source 摘要（xor-mini-mrt / xor-mini-noise-3 / xor-mini-mipmaps / xor-mini-webgpu / xor-mini-blur-philosophy）。Noise 3 以 patch 形式延伸 classic-shader-noise 的 Simplex 章节和函数 vs 纹理讨论；Blur Philosophy 以 patch 形式给 separable-gaussian-blur 加了 dos/avoids 清单和 Dual-Kawase 引用。人物页 xor-shader-artist 新增 5 条贡献记录与 source 链接。另 patch 到 deferred-rendering（MRT 关联）、mipmap-moire-scanline（正向反向 mipmap 对照）。

## [2026-04-14] ingest | Wave-33 Worker CU (cloudwu 2024/01-05 ×5)

处理云风 2024 年 1-5 月的月度归档共 5 篇。4 篇围绕 Ant Engine 的技术笔记（开源宣言、VFS 重构设想、ltask 调度器重构、移动端能耗优化与大型场景剔除设想）全部 ingest，5 月那篇个人职业生涯告别信跳过。新增 4 个概念页：ant-engine / ltask-scheduler / mobile-energy-optimization / async-offline-culling，4 个 source 摘要。cloudwu 人物页与 game-engine-vfs 概念页通过 patch 扩写。

## [2026-04-14] ingest | Wave-34 Worker CW (blog.playcanvas.com ×5)

处理 5 篇 PlayCanvas 博客：跳过 2 篇（2024-02 site redesign marketing、2024-04 VSCode setup 教程），整合 3 篇 WebGPU + 3DGS 工程公告。新增 3 概念页（playcanvas-webgpu-editor, supersplat-pwa, gaussian-splatting-web）、1 人物（will-eastcott）、3 source 摘要。对既有 [[webgpu-intro]] 追加 PlayCanvas Editor 落地相关交叉链接与 source 引用。

## [2026-04-14] ingest | Wave-34 Worker CX (interplayoflight.wordpress.com 2024-2025 现代 GPU 5 篇)

处理 5 篇 Kostas Anagnostou 2024-2025 年的高价值现代 GPU 技术文章，全部 ingest。workgraphs 两篇合并为单一概念页 [[d3d12-work-graphs]]；另外三篇各自建页：[[shader-instruction-cost]]、[[meshlets-and-mesh-shaders]]、[[async-compute]]。新建 5 个 source 摘要。通过 patch 扩写 kostas-anagnostou 人物页与 register-spilling-avoidance（后者补充 VGPR 动态下标的 ISA 级别佐证）。4 个新概念、0 个人物、5 个源摘要、6 条 patch、9 条 index 行。

## [2026-04-14] ingest | Wave-35 Worker CY (anteru.net ×5)

处理 5 篇 anteru.net 文章。新增 1 概念页（[[parquet-vs-csv-json]]）与 1 source 摘要（anteru-data-formats-csv-json），对 [[matthaeus-chajdas]] 人物页追加概念 + source 链接。跳过 4 篇：open-source 维护观点、systemd timers 运维、20 年博客回顾、10 年从业回顾。

## [2026-04-14] ingest | Wave-35 Worker CZ (simonschreibt.de ×2 Feb 2025)

处理 simonschreibt.de 2025 年 2 月两篇 VFX 拆解，全部 ingested。新增 2 概念页（[[camera-relative-sun-shadows]]、[[pom-decal-broken-edges]]）与 2 source 摘要。对 [[simon-trumpler]] 人物页追加贡献表与 Sources。关键 takeaway：(1) Anno 1800 把太阳位置锁相机而非世界——演示"物理正确 ≠ 美术正确"的反例；(2) Cyberpunk 墙面是盒子 + overlap mesh + 普通修补 decal + POM decal 的层叠，POM ray-marching 步数随视角衰减是 CDPR 的优化。

## [2026-04-14] ingest | Wave-35 Worker DA (fgiesen.wordpress.com ×3 2024 bit-twiddling / Oodle)

处理 fgiesen 2024 年 3 篇：Inserting a 0 bit in the middle of a value、Zero or sign extend、Oodle Kraken etc. misconceptions，全部 ingested。新增 3 概念页（[[insert-zero-bit-in-middle]]、[[sign-extend-without-shift]]、[[oodle-compression-suite]]）与 3 source 摘要。对 [[fabian-giesen]] 人物页追加 3 概念 + 3 sources。finalize 阶段补写了 3 个缺失的 source summary（worker 之前漏写 bundle）——关键洞察：(1) `x + (x & top_mask)` = 把 mask 命中的位左移 1 位；(2) 补码定义重写符号扩展为 `val - (val & sign_bit) * 2` 免分支；(3) PS5 游戏缩水的真正原因是 Sony 打包工具跨资源去重，非 Kraken 算法本身。

## [2026-04-19] update | Wave-35 finalize

补齐 wave 35 的 index.md / log.md / done.txt 缺失同步（3 worker 共 10 raws 入 done），补写 3 个 ryg source stub。为 wave 36 正式开跑做好闭环。

## [2026-04-19] ingest | Wave-36 Worker DC (blog.codingnow.com 2024-06 ~ 2024-08 ×5)

处理 5 篇云风 blog.codingnow.com 月度存档，ingest 4 篇跳过 1 篇：ECS 粒子系统 C/C++ 对比（2024-06-11）、工人任务分配 + 寻路（2024-07-25）、ID + 销毁标记替代引用计数（2024-08-24）、gameplay 三层架构 + Object/Actor（2024-08-24）；跳过 2024-06-22 个人游戏选题反思。新增 8 概念页（[[ecs-particle-system-c]]、[[type-safety-vs-simplicity]]、[[worker-task-dispatch-priority]]、[[multi-target-pathfinding]]、[[id-based-lifetime-with-kill-flag]]、[[gameplay-layering-object-actor]]、[[immediate-vs-retained-mode]]、[[save-load-driven-data-design]]）、4 source 摘要。cloudwu 人物页通过 patch 追加 4 source + 8 概念与一条关联概念注记。这批标志着云风 2024 年转向独立游戏后，从底层工程转向 gameplay 上层架构的系统梳理。

## [2026-04-19] ingest | Wave-36 Worker DB (danielilett.com Shader Graph Basics Part 7-10 + Mystery Dungeon ×5)

处理 5 篇 danielilett.com 2024 年 Unity Shader Graph 教程与 Mystery Dungeon 素描复刻，全部 ingested。新增 6 概念页（[[fresnel-edge-highlight]]、[[depth-intersection-subgraph]]、[[depth-aware-gaussian-blur]]、[[shader-graph-custom-function-hlsl]]、[[mystery-dungeon-sketch-shadows]]、[[screen-space-shadow-map-urp]]）与 5 source 摘要。Mystery Dungeon 源同时产出 2 概念（素描阴影 pipeline + URP 屏幕空间阴影贴图）。Worker 因 stream idle timeout 未写 bundle.json，P9 按文件 reverse-engineer 合并。

## [2026-04-19] ingest | Wave-36 Worker DD (mini.gmshaders.com 2024-03 ~ 2024-07 ×5)

处理 5 篇 mini.gmshaders.com：Blur Philosophy 2（Xor）、Volume Shadows（Oakleaff 客座）、Radiance Cascades Part 1（Yaazarai 客座）、Vertex Shaders（Xor）、Radiance Cascades Part 2（Yaazarai 客座），全部 ingested。新增 5 概念页（[[bilinear-sample-blur-optimization]]、[[penumbra-hypothesis]]、[[radiance-cascades]]、[[volumetric-fog-raymarch-shadows]]、[[vertex-shader-basics]]）、3 人物页（[[alex-yaazarai]]、[[alexander-sannikov]]、[[oakleaff]]）、5 source 摘要。Radiance Cascades 两部教程合并到同一概念页、各自保留独立 source 摘要。Worker 因 stream idle timeout 未写 bundle.json，P9 按文件 reverse-engineer 合并。

## [2026-04-19] ingest | Wave-37 Worker DE (danielilett.com 2025-10 ×5)

处理 5 篇 Daniel Ilett 2025 年 10 月 Unity 教程，全部 ingested：Zelda Recall 符文复刻、Shader Graph Basics 11（Terrain splatmap + 自动岩石 + 世界扫描）、Holofoil Pokémon 闪卡（stencil parallax + 彩虹条纹）、Shader Graph Basics 12（Fullscreen Graph 后处理）、Shader Code Basics 02（Texture/UV 采样 + SRP Batcher）。新增 8 概念页（[[draw-renderer-list-mask-urp]]、[[terrain-splatmap-shader-graph]]、[[world-scan-shader-effect]]、[[stencil-parallax-card-layers]]、[[holofoil-rainbow-shader]]、[[fullscreen-shader-graph-urp]]、[[hlsl-texture-sampling-basics]]、[[srp-batcher-cbuffer]]）+ 5 source 摘要 + 对 daniel-ilett / stencil-buffer / sobel-edge-detection 的增量补丁。Worker 因 socket 异常中断丢失部分 source 文件，P9 按 bundle 补写 5 个 source stub。

## [2026-04-19] ingest | Wave-37 Worker DF (blog.codingnow.com 2024-09 ~ 2024-11 ×5)

处理 5 篇云风 blog.codingnow.com 月度存档，ingest 3 篇跳过 2 篇：Ant 引擎改进计划（2024-09-03）、最近玩的游戏与确定性规则（2024-09-23）、异星工厂 2.0 太空时代通关复盘（2024-11-29）；跳过 2024-10-25 席德梅尔回忆录 + 卡牌游戏构思与 2024-11-29-2 马山攀岩日记。新增 5 概念（[[ecs-data-oriented-revert]]、[[engine-thin-wrapper-per-genre]]、[[determinism-vs-smart-ai-gameplay]]、[[mod-first-engine-evolution]]、[[single-hub-logistics-model]]）+ 3 source 摘要 + 对 cloudwu / ant-engine / ecs / game-engine-vfs / worker-task-dispatch-priority 的 patch。把云风 2024 下半年"独立做游戏后对引擎取舍的再评估"这条主线串起来。

## [2026-04-19] ingest | Wave-37 Worker DG (mini.gmshaders.com 2024-08 ~ 2025-02 ×5)

处理 5 篇 Xor 的 mini.gmshaders.com 文章（voxels-2 / vis-dev / anti-aliasing / gamma / sdf），全部 ingested。新增 5 概念（[[voxel-map-lut-2d]]、[[programmer-art-vis-dev]]、[[fwidth-derivative-antialiasing]]、[[gamma-correction-srgb]]、[[sdf-operations-shader]]）+ 5 source 摘要 + 对 xor-shader-artist / sdf-2d-primitives / analytical-antialiasing / color-space / voxel-ambient-occlusion 的 patch。voxels-1 (DDA) 尚未入库，voxels-2 暂以文字引用，待后续补 wikilink。

## [2026-04-19] ingest | Wave-38 Worker DH (danielilett.com Godot hologram + Blur Pro ×5)

处理 5 篇 Daniel Ilett 2026 年 Godot 端教程：4 篇 Godot Hologram Shaders 变体（Dot Matrix / Glitch / Gradient / Grid）合并为 1 概念页 [[godot-hologram-shader-effects]] 避免 slug 爆炸，每篇单独出 source 摘要；Blur Shaders Pro 脚本指南作 source-only，patch 到 [[urp-volume-post-processing]]。新增 1 概念 + 5 source。全部 ingested。

## [2026-04-19] ingest | Wave-38 Worker DI (blog.codingnow.com 2024-12 ~ 2025-03 ×5)

云风博客 5 篇：3 篇 skipped（桌游卡牌构筑设计 brainstorm 连载，非工程）、2 篇 ingested——[[agent-state-sync-broadcast]]（Erlang 服务器 40v40 战场下状态同步广播优化，质疑"广播=廉价"假设）+ [[soluna-2d-engine]] + [[sprite-batch-instance-draw]]（Soluna 2D 管线用 instance draw + storage buffer 把 sprite 顶点压到 26 字节）。

## [2026-04-19] ingest | Wave-38 Worker DJ (jendrikillner.com issues 326-330 — all skipped)

5 篇 jendrikillner.com 每周图形编程链接合辑 2024-02-11 ~ 2024-03-10（issues 326-330）全部 skipped_offtopic（link roundup，沿用 wave 34 先例）。

## [2026-04-19] ingest | Wave-39 Worker DK (jendrikillner 331-340 all skipped)

10 篇 jendrikillner Graphics Programming Weekly（2024-03 ~ 05）全部 skipped_offtopic（link roundup，沿用 wave 34/38 先例）。

## [2026-04-19] ingest | Wave-39 Worker DL (cloudwu 2025-04 ~ 2025-07 ×5)

5 篇云风 blog 月度存档：跳 4（Napier 对数史、单人桌游、育儿、尿酸），入 1——读 Milo Yip 译《游戏引擎架构》笔记，补充 2002~04 在大话西游 64M 内存约束下实现的栈式 / 双端 / 帧分配器与网易内部内存管理器比赛往事。新增 1 source + patch [[linear-allocator]] 的「变种」（双端分配器）+ cloudwu/jason-gregory 链接。

## [2026-04-19] ingest | Wave-39 Worker DM (simonschreibt.de ×5)

5 篇 simonschreibt.de：跳 3（newsletter 归档、Cozy Space Survivors 销售复盘、press kit），入 2——Infinity Nikki 单向窗户（back-face culling + 遮挡体积）与 Shadow Breakdown（shadow map + blob + AO decal 三套合奏）。新增 4 概念（[[one-way-window-backface-culling]]、[[shadow-caster-culling-front-back]]、[[selective-shadow-fade-pass-switch]]、[[blob-shadow-decal-vs-plane]]）+ 2 source + patch [[simon-trumpler]] / [[shadow-mapping-basics]]。

## [2026-04-19] ingest | Wave-40 Worker DN (jendrikillner 341-350 all skipped)

10 篇 jendrikillner Graphics Programming Weekly 2024-05 ~ 07（issues 341-350）全部 skipped_offtopic，延续 waves 34/38/39 先例。

## [2026-04-19] ingest | Wave-40 Worker DO (etodd.io 2024-2025 ×5)

Evan Todd 5 篇：3 技术 ingest（CI ASG 优化、identity/naming、100k 测试哲学）+ 2 信仰/艺术随笔 skip。新增 3 software-design 概念（[[identity-problem-naming]]、[[automated-test-philosophy]]、[[ci-cost-optimization-asg]]）+ 3 source + patch evan-todd / change-amplification / false-abstraction / abstraction。

## [2026-04-19] ingest | Wave-40 Worker DP (mini.gmshaders.com Xor 2025 ×5)

5 篇 Xor 2025 年新文（turbulence / reading-math / combining-shaders / common-mistakes / design-choices）全部 ingested。新增 5 rendering 概念 + 5 source + patch xor-shader-artist / creative-coding-process / fractal-texturing / separable-gaussian-blur。

## [2026-04-19] ingest | Wave-41 Worker DQ (jendrikillner 351-360 all skipped)

10 篇 jendrikillner weekly 2024-08 ~ 10（issues 351-360）全部 skipped，沿用 wave 34/38/39/40 先例。

## [2026-04-19] ingest | Wave-41 Worker DR (danielilett Hologram 系列后续 ×5)

5 篇 Ilett Hologram Shaders 产品文档：3 篇 Godot 变体（noise/scanline/uber）+ 2 篇 Unity Pro 移植（basic/dot-matrix-glitch）。全部 ingested。未新建概念页，全部通过 patch 扩写现有 [[godot-hologram-shader-effects]]（4 变体 → 7 变体 + Pro URP/HDRP 移植章节，新增动态分辨率补偿观察）。5 source 摘要。

## [2026-04-19] ingest | Wave-41 Worker DS (cloudwu 2025-07 ~ 2025-09 ×5)

云风 5 篇：3 ingest（[[lua-class-pattern]] Lua 类型定义套路、[[xlsx-text-versioning]] xlsx 文本化版本管理、[[mysql-charset-migration]] 跨十年 MySQL 编码迁移）+ 2 skip（Twitter 合集 + 桌游 Deep Future 笔记）。3 source 摘要。

## [2026-04-19] ingest | Wave-42 Worker DT (jendrikillner 361-370)

10 篇 jendrikillner weekly 2024-10 ~ 12（issues 361-370）全部 skipped，延续 waves 34/38-41 先例。

## [2026-04-19] ingest | Wave-42 Worker DU (danielilett Pro variants ×5)

5 篇 Unity Hologram Shaders Pro 变体（dot-matrix / glitch / gradient / grid / grid-glitch）全部作为 source 摘要，参数对齐已入的 Godot 版，未建新概念页。5 source + patch 到 [[godot-hologram-shader-effects]] Sources。

## [2026-04-19] ingest | Wave-42 Worker DV (blog.playcanvas.com 2024-08 ~ 2025-04 ×5)

5 篇 PlayCanvas 博客全部 ingested。新增 3 概念（[[playcanvas-engine-2-breaking-changes]]、[[playcanvas-react-declarative]]、[[supersplat-publish-platform]]）+ 1 人物（[[mark-lundin]]）+ 5 source。patch 到 [[will-eastcott]]、[[supersplat-pwa]]、[[gaussian-splatting-web]]、[[playcanvas-webgpu-editor]]。三主线：Engine 2.0 major bump 清 cruft 给 WebGPU 腾路；PlayCanvas React JSX 声明式 3D；SuperSplat 2025 三版扩张为完整发布平台。

## [2026-04-19] ingest | Wave-43 Worker DW (jendrikillner 371-378 + 2 special ×10)

10 篇 jendrikillner：9 skip（weekly 371-378 link roundup + gtc-2025 NVIDIA 会议宣传）+ 1 ingest（my-recommended-books，图形程序员推荐书单）。新增 [[jendrik-illner]] 人物页 + [[sources/jendrikillner-recommended-books]]。

## [2026-04-19] ingest | Wave-43 Worker DX (danielilett Hologram Pro noise/scanline/uber + Retro CRT ×5)

5 篇全部 ingested 作 source 摘要。3 Unity Hologram Pro 变体对齐已有 [[godot-hologram-shader-effects]]，patch 补 source 链接。2 Godot Retro Pro CRT 与已有 [[crt-shader-effects]] 技术重合（桶形畸变/RGB 子像素/扫描线/VHS tracking/YIQ 色损），patch 补引用，Post-Process 版的 *Scale In Screen Space* + YIQ 建模 NTSC 磁带色损已在 patch content 点出。

## [2026-04-19] ingest | Wave-43 Worker DY (cloudwu 2025-10~11 ×5)

5 篇云风 2025-10~11：4 ingest（[[indie-game-dev-rhythm]] Deep Future 独立开发复盘、[[paradox-grand-strategy-economy]] EU5 经济系统双源、[[main-thread-task-injection]] 主线程事件循环与 ltask 融合）+ 1 skip（资源包老文重发）。3 新概念 + 4 source + patch cloudwu / soluna-2d-engine / ltask-scheduler。

## [2026-04-19] ingest | Wave-44 Worker DZ (jendrikillner weekly 379-388 all skipped)

batch-w44-dz：10 篇 jendrikillner 周报（issue 379-388，2025-02-16 ~ 2025-04-20）全部按既定先例 skipped_offtopic，均为第三方链接聚合、Jendrik 本人无实质原创分析。

## [2026-04-19] ingest | Wave-44 Worker EA (danielilett.com Retro Shaders Pro variants ×5)

处理 5 篇 Daniel Ilett *Retro Shaders Pro* 变体文档（URP Retro Lit、URP CRT Mesh、URP CRT Post Process、Godot Retro Lit、URP Installation Guide）。Ingest 4 篇为 source 摘要，Skip 1 篇（installation guide 为安装说明，非技术内容）。无新增概念页——内容归入既有 [[crt-shader-effects]]、[[retro-rendering-techniques]]、[[color-quantization-retro]]。URP CRT Post Process 贡献了 Interlaced Rendering、Custom RGB Sliders、Render Pass Event、Custom Luminance/RGB/RGB+Intensity ramp 采样等全屏版独有参数；URP Retro Lit 相比 Terrain 版增加 Surface Options + flat shading + specular + reflection cubemap。

## [2026-04-19] ingest | Wave-44 Worker EB (cloudwu blog 2025-11~12 ×5)

处理 5 篇 blog.codingnow.com 文章：2 篇入库（卡牌构筑游戏设计、skynet 升级 Lua 5.5），1 篇跳过（育儿非技术），2 篇跳过（与已入库内容重复：EU5 游玩笔记已有 cloudwu-eu5-gameplay-notes；id + kill flag 已有 cloudwu-id-lifetime-kill-flag）。新增 2 概念页（deckbuilder-game-design-patterns, skynet-lua-sharetable-patch）与 2 source 摘要。

## [2026-04-19] ingest | Wave-45 Worker EC (jendrikillner weekly 389-398 all skipped)

batch-w45-ec：10 篇 jendrikillner 周报（issue 389-398）按既定先例全部 skipped_offtopic。

## [2026-04-19] ingest | Wave-45 Worker ED (cloudwu blog 2025-12~2026-02 ×7)

处理 7 篇 blog.codingnow.com 文章：3 篇入库（AI 聊游戏设计、单人桌游介绍、AI 辅助读书），4 篇跳过：1 篇与已入库 cloudwu-deckbuilder-games 重复（月份列表页抓取），2 篇是同日单篇文章的另一份抓取（月份列表页 / cat27 分类页），1 篇跑步攀岩日记非技术内容。新增 2 概念页（planning-over-rng-game-design, ai-assisted-reading-workflow）与 3 source 摘要。

## [2026-04-19] ingest | Wave-45 Worker EE (anteru.net papers ×6)

处理 6 篇 anteru.net 论文/项目索引页。Skip 1 篇（consulting.md 服务介绍）。Ingest 5 篇：SpMV Work Graphs (ISCA 2025)、Hybrid Sample-based Surface Rendering (VMV 2012)、Giga-Particle Fluid (HPG 2014)、SRAA (I3D 2011)、Tiled Light Trees (I3D 2017)。新增 2 概念页（subpixel-reconstruction-antialiasing, tiled-light-trees）+ 5 source 摘要。SpMV work graph 作为 d3d12-work-graphs 的 HPC 应用案例，不新建概念页。

## [2026-04-19] ingest | Wave-46 Worker EF (jendrikillner weekly 399-408 all skipped)

batch-w46-ef：10 篇 jendrikillner 周报（issue 399-408）按既定先例全部 skipped_offtopic。

## [2026-04-19] ingest | Wave-46 Worker EG (danielilett Retro Pro skybox/vertex-lit + Shader Toolbox ×10)

处理 10 篇 Ilett URP shader 资产文档。Ingest 9 / Skip 1（retro-shaders-pro-for-urp 概览营销页）。新增 5 概念页（procedural-retro-skybox、iridescent-bubble-shader、refractive-glass-shader、mesh-triangle-explosion、stochastic-texture-sampling）+ 9 source 摘要。关键洞察：Retro Vertex Lit v1.5 合并入 Retro Lit 留为兼容页；`_CameraTransparentTexture` 是 Shader Toolbox pack 层的渲染特性，解决 URP `_CameraOpaqueTexture` 透明互见缺陷；Mesh Explosion 用 BakeFaceColors.cs 预烘三角中心到 vertex color。

## [2026-04-19] ingest | Wave-46 Worker EH (playcanvas blog ×10)

10 篇 blog.playcanvas.com 全部入库。新增 3 概念页（sog-compression-format, splat-transform-cli, playcanvas-esm-scripts）+ 1 人物页（kris-bamrah）+ 10 source 摘要。SOGS→SOG 的迭代史（属性图+PLAS+WebP / Morton / 单文件 `.sog` / WebGPU 压缩端）、SplatTransform CLI、Walk Mode + Streamed LOD 构成 2025 下半年到 2026 初的 3DGS 工具链主线；ESM Scripts 是 PlayCanvas Editor 路径现代化关键。

## [2026-04-19] ingest | Wave-47 Worker EI (jendrikillner weekly 409-418 all skipped)

batch-w47-ei：10 篇 jendrikillner 周报（issue 409-418）按既定先例全部 skipped_offtopic。

## [2026-04-19] ingest | Wave-47 Worker EJ (danielilett Shader Toolbox + Snapshot Shaders 2/Pro ×10)

处理 10 篇 Daniel Ilett 产品文档：Shader Toolbox for URP 的 subgraph library 和 voronoi-lava、Snapshot Shaders 2 的 glitch/masking-layers/outline/underwater 四款 volume effect，以及 Snapshot Shaders Pro 的 scripting guide。跳过 3 篇（两个顶层营销页 + Snapshot 2 install guide）。新增 4 概念页（voronoi-lava-shader、volume-mask-layers、underwater-post-effect、volume-component-scripting）+ 7 source 摘要。patch daniel-ilett 人物页 + urp-volume-post-processing、glitch-image-effect、cel-shader-outline、worley-voronoi-noise、sobel-edge-detection、chromatic-aberration-post 六个既有概念页。

## [2026-04-19] ingest | Wave-47 Batch EK (ryg×5 + Xor×7 + Peters×5)

处理 19 篇跨 3 博客域文章。17 ingested（5 ryg HDR/硬件文 + 7 Xor shader art + 5 Peters path tracing / radiometry / spectral）、2 skipped（ryg `content-creator` 纯观点、Peters `blog.md` 首页索引）。新增 15 个概念页：`x86-simd-integer-multiplies`、`intel-13th-14th-gen-clock-degradation`（computer-systems）；`bc7-solid-color-blocks`、`mrsse-hdr-error-metric`、`unorm-snorm-hardware-conversion`、`density-field-volumetric`、`dot-gyroid-noise`、`radiometry-integral-view`、`photometry-luminance`、`hyperbolic-tangent-shader`、`glsl-mix-function`、`tweet-shader-280-char`、`fragcoord-shader-editor`、`spectral-vs-rgb-comparison`、`path-tracing-basics`（rendering）。17 个 source 摘要。作者页三者皆已存在，通过 patches 扩展贡献表 / 相关 / Sources 三段。

## [2026-04-19] ingest | Wave-48 Worker EL (jendrikillner weekly 419-427 all skipped)

batch-w48-el：10 条全部 skipped_offtopic（周报 419-427 延续先例，gtc-2026.md 验证为 GTC 注册/session 列表非原创技术）。

## [2026-04-19] ingest | Wave-48 Worker EM (Daniel Ilett ×8)

处理 8 篇 Daniel Ilett 文章：Toon Shaders Pro for URP 四件套参数手册 (Toon HLSL / Toon SG / Terrain / Outline Post) + Retro Shaders Pro 作者技术自述 + Shader Code Basics 03-05 (transparency / depth buffer / vertex + tessellation)。新增 6 概念页 (blend-modes-shaderlab, urp-depth-prepass-passes, urp-render-objects-feature, hull-domain-tessellation-urp, noperspective-affine-texture, toon-outline-post-process-modes)、8 源摘要；补 patch 到 cel-shading-pipeline、cel-shader-outline、retro-rendering-techniques、depth-texture-silhouette、tessellation-fur-rendering、shaderlab-hlsl-basics、daniel-ilett。

## [2026-04-19] ingest | Wave-48 Worker EN (cloudwu 2026-02~04 + Kostas 2025-08~2026-02 + Warren Moore 2024~2026)

处理 17 篇英文博客。云风 7 文里实 ingest 2（Star Trek LLM 幻觉、soluna extlua 代理），3 篇月索引 / 目录页重复，1 篇内容与已入库 2025-09-16 xlsx 同文，2 篇育儿数学课 off-topic。Kostas Anagnostou 5 文全 ingest（硬核渲染：GPU 利用率整体调优、VS export 瓶颈实测、spatial hash RTAO、neural rendering MLP、Cooperative Vectors 硬件加速）。Warren Moore Metal by Example 5 文全 ingest（Metal 十年上下篇、HDR 视频管线、Metal 4 入门、Slug 字体渲染 —— 注意 slug.md 不是 WIP 占位而是真文章）。新增 11 个概念页（10 渲染 + 1 编程语言 + 1 meta），12 个 source 摘要，0 个人物页。

## [2026-04-19] ingest | Wave-49 Worker EO (jendrikillner ×8 skip + graphicrants Karis Nanite Tessellation ×5)

Jendrikillner weekly 428–435 按先例一律 skip（link-digest）。Karis 2026 Nanite Tessellation 系列 5 篇全 ingest：新增 4 个概念页（tessellation-approaches-overview / nanite-tessellation-approach / nanite-reyes-comparison / variable-sized-work-pattern）+ 5 source 摘要。Patch brian-karis（增 2026 条目）、hull-domain-tessellation-urp（对照 D3D tessellator）、meshlets-and-mesh-shaders 与 d3d12-work-graphs（交叉 variable-sized-work）。

## [2026-04-19] ingest | Wave-49 Worker EQ (multi-author, 17 ingested / 3 skipped)

处理 20 个原始文件：17 ingested（Ciechanowski airfoil+moon、Zucconi Minecraft/PCA/Orbital、Apoorva Joshi shader-graph-contract/coordinate-spaces/static-site-antiframework/vibe-coding、Elopez-Ros life-and-death/packing-data、Alisavakis HAZE、Trümpler high-heel/Sims-4-mirrors、Slater Monte Carlo 2/3/4）；3 skipped（moon 重复、Technically Art 140/141 bluesky 聚合无点评）。新增 20 概念页 + 17 source 摘要；无新人物页。

## [2026-04-19] ingest | Wave-49 Worker EP-retry (vertexfragment ×5 + gametorrahod ×5 + etodd ×5)

重跑 batch-w49-ep（上批次因 stream idle timeout 全量丢失产出）。处理 15 篇：vertexfragment 4 技术文（polar coord / 云 upsample / URP 体积雾 / BTS v0.7 devlog）+ ramblings index 跳过；gametorrahod 全部 5 篇 DOTS 深度文；etodd 4 篇（Jujutsu / magic link ×2 / passkeys）+ posts index 跳过。新增 3 概念页（jujutsu-vcs, magic-link-auth, passkeys-webauthn）、1 人物页（sirawat-pitaksarit）、13 source 摘要。

## [2026-04-19] ingest | Wave-50 Worker ER (bartwronski + frost.kiwi + mecheye + danielpokladek + gameknife + raphlinus ×6)

处理 6 篇杂锦文章：跳过 Bart Wronski 的 ChatGPT 日常使用随笔（personal workflow，无技术内容）；ingest 5 篇——Frost Kiwi 的游戏模糊算法长文（从 Box/Gaussian 一路推到 Dual Kawase）、Jasper St. Pierre 的矩阵乘法与顺序终极指南、Daniel Pokladek 的 SDF 程序化台球 shader 教程、gameknife 的《现代渲染能有多现代？》（零 bind + Slang + AmbientCube + 混合光追）、Raph Levien 的《I Want a Good Parallel Computer》宣言。新增 13 概念页、1 人物页（daniel-pokladek）、5 source 摘要。

## [2026-04-19] ingest | Wave-51 Worker ES (c0de517e.blogspot.com ×5, all skipped)

5 篇 c0de517e.blogspot.com 文章全部为 redirect stub：blogspot 已停更，所有正文搬迁至 c0de517e.com 新站，本批 raw/ 文件仅残留一行外链与迁移提示，无实质可 ingest 内容。建议后续抓取新站（c0de517e.com/007_impostors.htm、009_website_joy.htm、011_portals.htm、012_peak_tech.htm、013_web.htm）后再重新 ingest Angelo Pesce 2023-2024 的思辨长文。

## [2026-04-19] ingest | Wave-51 Worker EU (runevision / Rune Skovbo Johansen ×3)

处理 blog.runevision.com 最近 8 个抓取，实质 3 篇技术文：2025-10 hair shader + atmospheric perspective 合并贴文、2026-01 Phacelle Noise、2026-03 Fast and Gorgeous Erosion Filter。新增 5 概念页（phacelle-noise / directional-noise / erosion-filter-procedural / atmospheric-perspective / hair-shader-anisotropic）、1 人物页（rune-skovbo-johansen）、3 source 摘要。5 篇是首页/月页/归档页对同一文章的重复抓取，skip_duplicate。

## [2026-04-19] ingest | Wave-51 Worker ET (chipsandcheese.com ×5)

处理 5 篇 chipsandcheese.com（Chester Lam）CPU/GPU 微架构实测分析：GB10 CPU 侧内存子系统、GB10 iGPU（consumer Blackwell）、主板 chipset PCIe 延迟横测、LLM 生成 C 编译器压测微架构（April Fools）、x86-64 split lock 跨 7 平台横测。新增 6 概念页 + 2 人物页（chips-and-cheese collective + chester-lam）+ 5 source 摘要。

## [2026-04-19] update | Manifest prune — 13 off-topic hosts removed

应用户指示剪枝 manifest：直接去掉 game-wisdom.com (3894) + learn-cocos2d.com (1712) + hacks.mozilla.org (1516) + gamasutra.com (1336) 四大巨量非 gfx 站；另清除清晰 off-topic 的 tonybai.com (Chinese Go) + masteringemacs.org (Emacs) + divisbyzero.com (数学) + sea-of-memes.com (Minecraft SEO 垃圾) + blog.eyas.sh (政治) + frgmnts.blog (政治) + claire-blackshaw.com (混杂非技术) + blog.justbilt.com (占位) + circle-group.github.io (学术 ML diffusion)。共 10487 篇移出 manifest，补进 done.txt 标 skipped_offtopic；原 raw/ 文件保留（CLAUDE.md: raw/ 不可修改）。blogs.yaml 同步移除 13 个 entry（312 → 299），防止 feedly-ingest 未来重抓。剩余可处理 5676 篇。

## [2026-04-19] ingest | Wave-52 Worker EV (raytracey.blogspot.com ×5)

处理 5 篇 Sam Lapere（Ray Tracey）博文。Ingest 2 篇：2019 Lighthouse 2（Bikker / OptiX 7 / RTX / blue noise）、2020 Marbles RTX × Omniverse（many-light 实时路径追踪的产品化）。Skip 3 篇：finally.md 怀旧短帖、Omniverse kitchen sink 与 Racer RTX 两篇几乎纯视频的感言贴。新增人物页 sam-lapere、概念页 lighthouse-2-optix / nvidia-omniverse；对 path-tracing-basics / path-tracing-monte-carlo / hybrid-raytracing-pipeline 追加 `## 相关` 交叉引用。

## [2026-04-19] ingest | Wave-52 Worker EW (joostdevblog.blogspot.com ×5)

处理 5 篇 Joost van Dongen 博客文章。3 篇 ingest（Blender 硬表面建模、发行商 pitch 方法论、创意输入多样化），2 篇 skip（Robo Maestro Steam 发售公告与 Galaxy Grove 里程碑博文均为非技术内容）。新增 3 概念页（blender-hard-surface-modeling / indie-pitching-publishers / game-idea-generation）、1 人物页（joost-van-dongen）、3 source 摘要。

## [2026-04-19] ingest | Wave-52 Worker EX-retry (bitsquid.blogspot.com ×5)

Retry of batch-w52-ex (stream watchdog timeout, zero output). 处理 5 篇 Stingray 博客末期 (2017) 技术文章：Entity Index 重构（原型链式 structural sharing）、SSR 重投影（TAA 下的几何解与启发式）、物理 lens flare（Hullin 论文的 Stingray 实现）、Arnold 做 PBR ground truth 的 material/light 验证、entity-based 物理相机。新增 2 概念页（material-light-validation, physical-camera-model）和 5 source 摘要。3 个概念页（entity-index-reconstruction, reprojected-planar-reflection, physically-based-lens-flare）在磁盘上已存在且内容完整——未覆写，仅在 bundle 中以 no-op patch 备案。niklas-frykholm.md 已含全部 5 source 链接，无需修改。

## [2026-04-19] ingest | Wave-53 Worker EY (alfredbaudisch.com ×5)

处理 5 篇 alfredbaudisch.com 源文件。3 篇 /project-style/ 栏目页指向同一个 Godot 复刻 Banjo-Kazooie N64 地形的项目，合并为 1 篇 source summary (`alfredbaudisch-banjo-godot-terrain`)。新增概念页 `banjo-kazooie-vertex-color-terrain` 与人物页 `alfred-baudisch`。2 篇 /tools/{blender,godot}/ 栏目聚合页无独立技术内容，skipped_offtopic。交叉链接到 [[retro-rendering-techniques]] 与 [[terrain-splatmap-shader-graph]]。

## [2026-04-19] ingest | Wave-53 Worker EZ (blog.gemserk.com ×5)

处理 5 篇 Gemserk / Ariel 博客。Ingest 4 篇 Unity 工程实战（新旧 Input System 对比与多手柄配对、Prefab/GameObject 作为纯数据容器、ECS CustomEditor shadow GameObject 调试方案、Prefab/Scene/Asset 的数据结构批量重构）；skip 1 篇 zombie-rockers 游戏展示短文。新增 4 概念页、1 人物页（gemserk）、4 source 摘要。3 个已有页面补充 patch（ecs、save-load-driven-data-design、unity-complexity-patterns）。

## [2026-04-19] ingest | Wave-53 Worker FA (hacksoflife.blogspot.com ×5)

处理 Ben Supnik (X-Plane) 5 篇技术博文：C++20 stackless/stackful 协程辨析、coroutine-as-awaitable、future-proofing 三问、beat-the-experts 作弊法、sRGB×premult×compression 三角。新增 1 人物页（ben-supnik）、5 概念页（stackless-vs-stackful-coroutines、coroutine-awaitable-pattern、future-proofing-tests、cheat-by-solving-less、srgb-premultiplied-alpha-compression）、5 source 摘要。Patches 9 条：补 go-goroutine-channels / linear-allocator / strategic-programming / tactical-programming / false-abstraction / alpha-compositing / alpha-blending / gamma-correction-srgb / bc7-solid-color-blocks 的相关链接。

## [2026-04-19] ingest | Wave-54 Worker FD (4rknova.com ×5)

处理 5 篇 Nikos Papadopoulos / 4rknova.com 文章。新增 1 概念页（mulberry32-rng）、1 人物页（nikos-papadopoulos）、1 source 摘要。跳过 4 篇：Gaia 天文数据库（领域不匹配）+ 2 篇虚构小说 + 1 个仅含键位表的 demo 页。

## [2026-04-19] ingest | Wave-54 Worker FB (boristhebrave.com ×5)

处理 Boris The Brave（Sylves / WFC 作者）5 篇。Ingest 3 篇：Poisson Rect Process（无限平面非重叠随机矩形的两相过滤算法）、Dealing With Infinite Grids（Sylves 无限网格文档入口指针贴）、Good Software Doesn't Double Check（批评 agent 过度防御式编程，提倡用不变量与静态类型替代重复检查）。跳过 2 篇：Silksong 游戏攻略、NeurIPS 2025 会议游记。新增 3 概念页（poisson-rect-process, infinite-chunked-procedural-generation, good-software-no-double-check）+ 1 人物页（boris-the-brave）+ 3 source 摘要，并给 poisson-disk-sampling / data-structure-invariants / type-safety-vs-simplicity 三页打回链 patch。

## [2026-04-19] ingest | Wave-54 Worker FC (blog.s-schoener.com ×5)

处理 Sebastian Schöner 5 篇技术文章：`i miss header files`（Zig 视角）、`better codegen for Unity games on Mono`（公告）、Mono codegen 学习笔记 part 1 / part 2、`Zig, hot reload, and ABI trouble`。新增 5 概念页（mono-jit-pipeline, pointer-alias-analysis, dead-store-elimination, zig-c-abi-boundary, header-file-vs-pub-export）、1 人物页（sebastian-schoener）、5 源摘要。无跳过。

## [2026-04-19] ingest | Wave-55 Worker FF (cybereality.com x5)

处理 5 篇 cybereality.com 博文，全部 skip：两篇 off-topic（GenAI 音乐视频、3D psy-op 观点），三篇 Degine 引擎进度通告（GDC demo / Q1 progress / Valentine's mocap remaster）标题指向 graphics/OpenGL 但正文为 1-3 段无技术细节的宣传帖。未创建任何 wiki 页面。

## [2026-04-19] ingest | Wave-55 Worker FE (allarsblog.com ×5)

处理 Michael Allar 5 篇 UE4 工程笔记：救火顾问长文、Marketplace JS hack、编辑器电池 60fps、UMG PreConstruct 顺序、通知气泡偏移。新增 1 人物页（michael-allar）、3 概念页（umg-user-widget-lifecycle / ue4-editor-battery-throttle / ue4-common-perf-pitfalls）、5 source 摘要。无跳过。

## [2026-04-19] ingest | Wave-55 Worker FG (tedsieblog.wordpress.com ×5)

处理 5 篇 Ted Sie 中文 Unity 博客。5 全 ingest：动态分屏、L-system 分形、L-system 闪电效果、人群 Waypoint、DOTS Tween case study。新增 5 概念页（dynamic-split-screen / l-system-fractals / l-system-lightning-bolts / unity-crowd-waypoint-system / unity-dots-tween-system）+ 1 人物页（ted-sie）+ 5 source 摘要。（bundle.json 因 API socket 异常未落盘，人工重建 index/log。）

## [2026-04-19] ingest | Wave-56 Worker FH (greyaliengames.com ×5 all skipped)

五篇 greyaliengames.com 月份归档页全部 skip_offtopic：均为 casual 游戏（Shadowhand / Jewel Match / Clutter / Forbidden Solitaire）发行新闻稿与 Jake Birkett 的年度商业/个人 goals 复盘，无渲染、引擎、系统、编程语言等技术内容。

## [2026-04-19] ingest | Wave-56 Worker FI (outerra.blogspot.com ×5)

处理 5 篇 Outerra 行星引擎技术博文（2015-2018）：SRTM 30m 数据评估、NasaDEM preliminary 对比、OpenGL 三角形吞吐测试 grass + blocks、GLSL fp64 sin/cos minimax 近似。新增 3 概念页（planet-terrain-dem-pipeline, opengl-draw-call-batching-sweet-spot, fp64-sincos-minimax），1 人物页（outerra-team），5 源摘要。Patch draw-call.md / faster-math-functions.md / fractal-texturing.md 交叉链接。

## [2026-04-19] ingest | Wave-56 Worker FJ (sebaslab.com ×5)

处理 Sebastiano Mandalà 5 篇 Svelto.ECS 文章：ECS 抽象层与模块封装、Svelto 3.3 Filters API、Survival mini example 重写、Svelto-on-DOTS 3.4 更新、ComputeSharp 实现 ECS-on-GPU。新增 1 人物页（sebastiano-mandala）、5 概念页（svelto-ecs / ecs-abstraction-layers / svelto-filters-api / svelto-on-dots / ecs-on-gpu-computesharp）、5 source 摘要。无跳过。Patch 到 dots-ecs-programming-patterns 与 dots-enableable-components 加入 Svelto 对照链接。

## [2026-04-19] ingest | Wave-57 Worker FK (danielilett.com Snapshot Shaders Pro effects + Toon Shaders Pro top pages ×5)

处理 5 篇 Daniel Ilett 产品文档收尾：Snapshot Shaders Pro 的 underwater / vortex / world-scan 三款 effect 参考文档（ingest），Toon Shaders Pro URP 顶层营销页与 install guide（skip，沿用 w47 对顶层/install 文档一贯处理）。新增 1 概念页 vortex-distortion、3 source 摘要。patch daniel-ilett 人物页 + urp-volume-post-processing、underwater-post-effect、world-scan-shader-effect、chromatic-aberration-post 四个既有概念页。

## [2026-04-19] ingest | Wave-57 Worker fm (tomlooman.com Tom Looman UE5 ×3)

处理 Tom Looman 博客 5 篇文章：ingest 3 篇 UE5 干货（Rider 环境搭建、Project Orion 合作 Roguelike 示例、Unreal Insights Counters/Traces），skip_duplicate 2 篇（all-posts 索引页、contact 联系页）。新增 3 概念页（rider-ue5-setup、project-orion-action-roguelike、unreal-insights-counters-traces）、1 人物页（tom-looman）、3 source 摘要。

## [2026-04-19] ingest | Wave-57 Worker FL (Wolfgang Engel / Diary of a Graphics Programmer ×5)

全 ingest 5 篇 Wolfgang Engel 文章（2017 HDR10 TV setup、2018 Triangle Visibility Buffer 长文、2018 DXR API 之辩、2018 Ray Tracing without API、2020 Catching Up / Forge 历史）。新增 1 人物页 wolfgang-engel，3 概念页 triangle-filtering-pipeline / ray-tracing-api-debate / the-forge-renderer，5 source 摘要。对 visibility-buffer、hybrid-raytraced-shadows-reflections、kostas-anagnostou、color-space、hdr-video-edr-metal 五个现有页做 patch（补充相关链接 + source 引用）。这批把 Confetti / The Forge 这条线完整并入 wiki，和已有的 Kostas Anagnostou / gameknife 两个 VB+hybrid RT 入口形成三角引用。

## [2026-04-19] ingest | Wave-58 Worker FO (boristhebrave.com 2025 混合 ×5)

处理 5 篇 Boris The Brave 2025 文章。新增 2 概念页（gpu-gol-optimization-ladder 把两篇 GoL 加速文合并；infinite-random-rhombus-tilings Townscaper 替代方案）、3 source 摘要。跳过 pure-reason（LLM 预言非技术）与 2026-01-03 infinite-grids（wave 54 已 ingest）。patch boris-the-brave 人物页、infinite-chunked-procedural-generation、cuda-memory-hierarchy 三处已有页面。

## [2026-04-19] ingest | Wave-58 Worker FP (danielilett snapshot-pro ×5: sharpen/silhouette/snes/synthwave/text-adventure)

处理 5 篇 Daniel Ilett *Snapshot Shaders Pro* 产品参考（极短文档）。新增 3 概念页：[[sharpen-filter]]（unsharp mask / 3×3 Laplacian 卷积核）、[[synthwave-grid-postfx]]（屏幕像素反推世界坐标 + 三组正交平面距离判定）、[[text-adventure-terminal-postfx]]（cell 亮度索引字符图集 + fg/bg lerp）。Silhouette 与 SNES 分别复用既有 [[depth-texture-silhouette]] 和 [[color-quantization-retro]]，只追加 source 链接。新增 5 source 摘要。无人物、无跳过。

## [2026-04-19] ingest | Wave-58 Worker FN (anki3d.org ×5)

处理 5 篇 Panagiotis Christopoulos Charitos 在 anki3d.org 的博客（AnKi 3D Engine 作者）：SPIR-V 手动解析改写、Vulkan mesh shader + HLSL PerPrimitiveEXT 坑、GPU-driven 视频、pipeline barrier 简化、土豆级 RT。新增 4 概念页（spirv-parsing-rewriting, mesh-shader-vulkan-hlsl-per-primitive, simplified-pipeline-barriers, minimalist-rt-acceleration-structures）、1 人物页（panagiotis-charitos）、5 source 摘要。Patch 既有 gpu-hazard-tracking / meshlets-and-mesh-shaders / hybrid-raytracing-pipeline 的相关链接。GPU-driven 视频本体只有 Google Slides 链接，博客无可抽取内容，source 页标注为 data gap。

## [2026-04-19] ingest | Wave-59 Worker FQ (30fps.net / Pekka Väänänen ×6)

处理 6 篇 30fps.net notebook / reference：坐标系对照表、VQ 瓦片图、2D PCA 颜色压缩、SOM 调色板量化、MBD 图像版、NumPy 切瓦片加速。新增 6 概念页（coordinate-system-table、vector-quantization-tilemap、pca-image-compression、color-quantization-som、moving-basis-decomposition、numpy-tile-reshape-trick）、1 人物页（pekka-vaananen）、6 source 摘要。对 coordinate-spaces / color-quantization-kmeans / pca-intro 追加相关链接 patch。全 ingest，无跳过。

## [2026-04-19] ingest | Wave-59 Worker FS (blog.yiningkarlli.com ×6)

处理 Yining Karl Li（Disney Animation Hyperion 渲染工程师）博客 6 篇。Ingest 4 篇技术文：Moana 2 / Zootopia 2 / SIGGRAPH 2025 GPU Ptex 纹理流送 / SIGGRAPH 2025 Hyperion 二代 path guiding。跳过 2 篇（个人博客 CSS 重设计、公司内部摄影展）。新增 1 人物页（yining-karl-li）、5 概念页（hyperion-renderer、wavefront-path-tracing、path-guiding-production、ptex-gpu-streaming、nested-dielectrics）、4 source 摘要。给 mipmap-generation-sampling 追加一条交叉引用。

## [2026-04-19] ingest | Wave-59 Worker FR (16bpp.net ×3)

处理 16bpp.net 性能连载 3 篇独立文章 + 2 个月索引重复 + 1 篇 5 天内 follow-up（gotta-go-fast 合并进 quicker-trig）。新增 6 concept（rejection-vs-analytical-sampling、benchmark-methodology-end-to-end、free-vs-member-functions-performance、asin-cg-approximation、estrin-scheme、pade-approximants、psraytracing 共 7 个）+ 1 人物（16bpp）+ 3 source。核心主题：用矩阵 benchmark 重测 C++ 性能老主张，拒绝采样在 -O1 后反超解析解、Nvidia Cg 的 Abramowitz-Stegun asin_cg + Estrin 重写、Synfig 上 free function 对性能无影响。

## [2026-04-14] ingest | Wave-60 Worker FV (jonolick.com ×5)

处理 5 篇 Jon Olick（jonolick.com）文章。3 篇实质：EDIZ 上采样批判、Laplacian 结构感知误差扩散、SIFT 单文件库 jo_sift.h；2 篇 skip_duplicate（home 首页合集、links 外链合集）。新增 3 概念页（ediz-upscaling-critique / laplacian-structure-aware-error-diffusion / sift-single-file-library）、1 人物页（jon-olick）、3 source 摘要。Laplacian 页与既有 floyd-steinberg-dithering 交叉引用。

## [2026-04-19] ingest | Wave-60 Worker FU (blog.selfshadow.com ×5)

处理 5 篇 blog.selfshadow.com 条目（Stephen Hill 的 SIGGRAPH PBS 课程主页）。跳过 2 篇纯 changelog 空壳与 1 篇已在 wiki 中的重复（2014 课程页已存在）。新增 2 个 source 摘要（2012、2025 课程），新增 2 个概念页（openpbr、neural-materials）。Patch stephen-hill 作者页与 physically-based-shading 概念页追加两条 source 链接。

## [2026-04-19] ingest | Wave-60 Worker ft (asawicki.info ×6)

处理 Adam Sawicki 的 6 篇 asawicki.info 原文。3 篇实质技术内容入库（graphics-api history / system load formula / DX12 GDC 2026 long comments），3 篇 skip（home-page 与 RSS 聚合重复；Total Commander 插件公告无技术实体）。新增 1 人物页（adam-sawicki）、5 概念页（graphics-api-history、system-load-formula、pix-api-and-dxdmp、dxr-tier-2-clas-ptlas、advanced-shader-delivery）、3 source 摘要。Patch 到 hlsl-cooperative-vectors-tensor-cores 与 d3d12-work-graphs 做交叉引用。GDC 2026 DX12 公告被 Sawicki 拆成主机级调试工具、ML for DX、Shader Delivery、DirectStorage 1.4、DXR Tier 2 五条线，本批按其中三条独立成页，ML 方向复用既有 Cooperative Vectors 页。

## [2026-04-19] ingest | Wave-61 Worker FX (allenchou.net ×5 all-skipped)

处理 Allen Chou 5 篇博客：3 篇 DigiPen/DigiJam 作品展示页（Photon Bunny / Cooncoaster / Sky Spire）正文仅游戏链接与玩法说明；My Life at Naughty Dog 是办公室生活 brain dump（滑板车、咖喱日、项目代号梗）；GDC Social Tips 是求职社交建议。全部 5 篇 skipped_offtopic，均与 graphics/engine/systems 技术主题无关。allen-chou 人物页保持不变。

## [2026-04-19] ingest | Wave-61 Worker FY (bartwronski.com ×5)

处理 5 篇 Bart Wronski 2014–2020 文章。2 篇入库：Poisson 生成器 GUI 更新（patch 回 [[poisson-disk-sampling]] 和 [[bartosz-wronski]]）、《Multithreading for Visual Effects》书评（新建概念 [[vfx-multithreading-patterns]]）。跳过 3 篇：small-coding-projects（项目名片页，CSharpRenderer / Poisson 均已覆盖）、Lightroom 胶片底片教程（摄影）、articles-index（目录页 skip_duplicate）。

## [2026-04-19] ingest | Wave-61 Worker FW (Daniel Ilett Snapshot Pro 最后 5 effects)

处理 5 篇 danielilett.com 产品参考文档（Pixelate / Posterize / Radial Blur / Scanlines / Sepia Tone）。新增 2 概念页（pixelate-postfx, radial-blur-postfx）、5 source 摘要。Scanlines 链 [[crt-shader-effects]]、Posterize 链 [[color-quantization-retro]]、Sepia 链 [[image-effect-colour-transform]]，均不另建概念。Snapshot Shaders Pro 产品文档系列至此完结。

## [2026-04-19] ingest | Wave-62 Worker FZ (danielilett Snapshot Pro ×5)

处理 5 篇 Daniel Ilett Snapshot Shaders Pro 产品参考页：outline-sobel / neon-sobel / outlines-fancy / oil-painting / noise-grain。全部 ingested，0 跳过。新增 5 source 摘要，0 概念页（算法本身 sobel-edge-detection / kuwahara-filter / toon-outline-post-process-modes / classic-shader-noise / crt-shader-effects 均已有），0 人物（daniel-ilett 已存在）。向 sobel / kuwahara / classic-noise / toon-outline / crt 5 个既有概念页追加 source 链接。

## [2026-04-19] ingest | Wave-62 Worker GA (cmwdexint.com ×5)

处理 5 篇 cmwdexint.com / Ming Wai Chan 的 URP 贴士。Ingest 3 篇（URP↔Built-in 映射、URP 设置入口、ShaderGraph 关雾效 + 变体剥离）。新增 4 概念页（urp-builtin-feature-mapping, urp-settings-locations, urp-shadergraph-fog-strip, shader-variant-stripping）、1 人物页（ming-wai-chan）、3 source 摘要。跳过 2 篇：Stable Diffusion 本地安装、Unity × Spotify Android SDK 集成（偏离 graphics/rendering 主题）。

## [2026-04-19] ingest | Wave-62 Worker GB (blog.thomaspoulet.fr ×5)

处理 Thomas Poulet 博客 5 篇全技术文章：3 篇自研引擎帧分析（Ni No Kuni 2 light pre-pass + 艺术家驱动线稿 / DCS 2.7 YUV GBuffer + SDF cloudscape / Anno 1800 node-texture 地形 + 纹理驱动粒子 + 9-slice UI），1 篇 UE5 物理游戏的五档可观测性工具栈（On-screen → GDT → Visual Logger → ImGui → Ariadne），1 篇蓝图资产验证（GeneratedClass + Subobject Data Subsystem）。新增 1 人物页（thomas-poulet）、9 概念页、5 源摘要；跨链 simonschreibt-anno-1800-shadows、unreal-frame-breakdown、cel-shader-outline、particle-custom-vertex-streams、tiled-light-prepass、unreal-insights-counters-traces。

## [2026-04-19] ingest | Wave-63 Worker GC (benui.ca ×5)

处理 5 篇 benui.ca（Ben UI，UE5 UI 专家）。ingest 2 篇（ui-as-communication、ux-opinions），新增 2 概念页（ui-as-communication、ux-opinions-checklist）、1 人物页（ben-ui）、2 source 摘要。skip 3 篇：ui-resources 纯外链书单、unannounced-project 简历占位、why-i-refuse-to-use-ai 为 AI 观点文（非技术）。

## [2026-04-19] ingest | Wave-63 Worker GE (nullprogram.com ×5)

处理 5 篇 Chris Wellons (nullprogram) 技术博文。每篇对应独立 URL（非首页重复抓取），全部 ingest。新增 16 概念页（链表+trie+MSI 数据结构三件套、Wasm 三件套 wasmtime-py/指针陷阱/bump allocator、Monocypher AEAD、u-config Frankenwine + Wine syscall + unity 宏改名 + LP64/LLP64、AI 协作三件套 Quilt.cpp/conformance 克隆/C 内存安全、dcmake + CMake DAP + Dear ImGui docking）、1 人物页（chris-wellons）、5 source 摘要。

## [2026-04-19] ingest | Wave-63 Worker gd (agraphicsguynotes.com ×5)

处理 Jiayin Cao 博客 5 篇，4 篇 ingest（TSL shading language / ReSTIR DI 数学 / C++ Fiber 基础 / ReSTIR GI 数学）、1 篇 skip（posts 列表页）。新增 4 概念页（tiny-shading-language、restir-di-math、restir-gi-math、fiber-cpp-basics）、1 人物页（graphics-guy-notes）、4 源摘要。覆盖离线渲染语言设计、ReSTIR 家族数学基础、fiber-based job system 三个主题。

## [2026-04-19] ingest | Wave-64 Worker gf (alexharri.com ×5)

处理 5 篇 Alex Harri Jónsson 博客文章。新增 3 概念页（web-clipboard-api、compressed-trie-pattern-matching、ascii-shape-vector-rendering）、1 人物页（alex-harri-jonsson）、3 source 摘要。跳过 2 篇（about-me 首页 + 冰岛开发者薪资/技术调研，后者地区性数据非技术主题）。

## [2026-04-19] ingest | Wave-64 Worker GG (agraphicsguynotes.com ×5)

agraphicsguynotes.com 早期硬核技术文 5 篇全 ingest：2016 离线体积渲染推导、2018 PBRT bsdftest 数学、2018 各向异性 microfacet importance sampling、2018 色彩科学基础、2020 SSS 工程实践。新增 5 概念页（volume-rendering-offline、bxdf-unit-test、anisotropic-microfacet-sampling、color-science-basics、sss-practical-implementation）与 5 source 摘要，patch graphics-guy-notes 人物页追加 sources 链接、microfacet-brdf/color-space/inversion-sampling-prng/path-tracing-basics 互相交叉引用。

## [2026-04-19] ingest | Wave-64 Worker gh (acko.net / Steven Wittens ×5)

处理 5 篇 Steven Wittens（acko.net）文章。3 篇硬技术 ingest：I is for Intent（Intent vs State 架构）、Occlusion with Bells On（Use.GPU 0.14 GTAO）、HTML is Dead（DOM/CSS 批判）。2 篇跳过：Bouquet Residence（CrowdStrike 公关/管理文化评论）、L in LLM Stands for Lying（AI 批评观点文）。新增 1 人物（steven-wittens）、5 概念（intent-vs-state、ground-truth-ambient-occlusion、use-gpu-reactive-runtime、render-pass-orchestration、dom-replacement-rethink）、3 source 摘要。

## [2026-04-19] defer | Wave-65 GI+GJ (bleuje + dolphin-emu ×10, workers stream-idle timeout)

GI (bleuje 5) 和 GJ (dolphin-emu 5) 两个 worker 都在 730s 附近 stream-idle 超时，零 bundle 落盘。暂标 skip 进 done.txt 以避免下轮 /loop 重新选中；内容需后续会话恢复时用更激进 bundle-first 协议单独处理。

## [2026-04-19] defer | Wave-65 GK (adriancourreges ×5, worker stream-idle timeout)

GK (adriancourreges 5) worker 无 staging / 零 bundle（与 GI/GJ 同样 stream-idle 模式）。defer 进 done.txt。

## [2026-04-19] ingest | Wave-65 Worker gk (adriancourreges.com ×5)

处理 Adrian Courrèges 5 篇。3 篇硬技术全量 ingest：透明像素陷阱、MGS V / Fox Engine 帧分析（2331 draw / 73 RT，定制 ReShade 绕反调试）、UE4 Switch 优化补丁集（GatherDOF / half-res SSAO / reactive dynres；DQ XI S / Pikmin 4 出货采用）。2 篇 skip_duplicate（首页 + graphics-studies 索引）。新增 3 概念页（mgs-v-fox-engine-frame / gather-bokeh-dof / ue4-reactive-dynamic-resolution）、1 人物页（adrian-courreges）、3 source 摘要。给 srgb-premultiplied-alpha-compression / alpha-blending / scatter-bokeh-dof / dynamic-resolution-scaling / unreal-frame-breakdown / thomas-poulet 7 个 patch。

## [2026-04-19] ingest | Wave-66 Worker GM (asawicki.info 早期 ×3)

处理 3 篇 Adam Sawicki 早期 D3D12/compute 文章。新增 3 概念页（d3d12-resource-alignment、compute-shader-dispatch-ids、a-metric-for-memory-fragmentation）、3 source 摘要。人物页 adam-sawicki 追加 3 条 sources 与 2 条相关概念链接。全 ingest 无 skip。

## [2026-04-19] ingest | Wave-66 Worker gn (blog.yiningkarlli.com early ×3)

处理 Yining Karl Li 博客 3 篇早期文章（2013 Pixar OptiX RTP / 2016 Zootopia / 2018 Mipmapping with Bidirectional Techniques）。新增 1 概念页 [[ray-differentials]]（路径追踪里 mip level 选择的工程机制、BDPT 难题、Manuka shade-before-hit 与 Takua camera-based 两种绕过方案）、3 source 摘要，0 人物页（[[yining-karl-li]] 已存在，追加 3 条 source 链接）。补丁同步 hyperion-renderer / mipmap-generation-sampling / wavefront-path-tracing 三页的相关链接。全部 ingest，无 offtopic skip。

## [2026-04-19] ingest | Wave-66 Worker GL (bkaradzic ×3)

处理 3 篇 bkaradzic.github.io 文章（Orthodox C++、AirMech 开源守则、AirMech NaCl 移植）。三篇均 ingest。新增人物页 branimir-karadzic；新增 3 概念页（orthodox-cpp、middleware-vs-open-source、native-client-porting）；新增 3 source 摘要。对 cpp-multi-paradigm-discipline 与 rpp-stl-replacement 做了轻量交叉链接 patch。

## [2026-04-19] ingest | Wave-67 Worker GQ (ronja + lindenreid + themaister index/about ×5)

5 篇全部为 index/about/tutorials 目录页，无实质技术内容，整批 skip。未新增任何 wiki 页。

## [2026-04-19] ingest | Wave-67 Worker GO (bruop.github.io ×3)

Bruno Opsenica 3 篇：IBL 多次散射（BGFX + Fdez-Agüera 2019）+ frustum culling（顶点 clip-space 测试，SIMD 加速）+ more robust frustum（SAT 分离轴，ISPC 实现）。新增 1 人物、3 source、4 概念。

## [2026-04-19] ingest | Wave-67 Worker P (erfan-ahmadi.github.io ×3)

处理 3 篇 Erfan Ahmadi 博客（Nabla / The Forge）：纹理流式上传、Frames In Flight 讲解、Bokeh DoF 三种实现并排比较。新增 1 人物页（erfan-ahmadi）、3 概念页（streaming-staging-texture-upload, frames-in-flight, circular-separable-dof）、3 source 摘要。补丁到 gpu-fence-timeline-semaphore / gather-bokeh-dof / scatter-bokeh-dof / the-forge-renderer / buffer-renaming。

## [2026-04-19] ingest | Wave-68 Worker GT (Kostas 早期 + Warren Moore 视频)

3 篇全部 skip：Kostas 的 About 页 + 博客首帖（hello-world，无技术内容），Warren Moore 2015 视频公告（外链失效，博客无 transcript）。零新增页面。

## [2026-04-19] ingest | Wave-68 Worker GS (halisavakis 早期 portfolio ×3)

处理 3 篇 halisavakis.com 早期 portfolio 贴：animated-light-cookies（2020）—— Unity Custom Render Texture 做动画光斑，内容极薄仅做 source 摘要；pac-tac-atac（2018 GGJ VR 游戏）与 paul-paul（2019 VR 叙事体验）均为纯作品宣传，无技术内容，skip。新增 1 source 摘要，补 1 条 harry-alisavakis Sources 链接。

## [2026-04-14] ingest | Wave-68 Worker gr (jonolick.com DXT 系列 + WAV ×4)

处理 Jon Olick 4 篇：WAV 单函数写入器（2012）、DXT 压缩 Part 1 codebooks/sliding-windows（2013-02）、Part 3 transposes（2013-07，正文抓取不全）、Part 4 entropy（2013-08）。新增 2 概念页（dxt-entropy-reduction, dxt-codebooks-sliding-window）、4 source 摘要。补 jon-olick 人物页 sources 计数 3→7 及相关链接。Part 4 是系列干货：selection bits 占 LZMA 后 75% 体积，用 rate-distortion 降熵把 2.28 bpp 压到 1.51 bpp / MSE 0.64，比 crunch 质量高 4.3×、速度快 16×。

## [2026-04-19] ingest | Wave-69 Worker gu (cyanilux.com ×5)

处理 5 篇 cyanilux.com 文件：1 篇实质技术文（gpu-instanced-grass-breakdown）ingest；4 篇是栏目 index / 法律页（posts / cookies-privacy / breakdowns / tutorials），跳过。新增 1 概念页（gpu-instanced-grass-urp）、1 source 摘要。给 cyanilux 人物页、gpu-driven-grass-tiles、waving-grass-shader-vertex-offset、shader-graph-custom-function-hlsl 打补丁互连。

## [2026-04-19] ingest | Wave-69 Worker GV (danielchasehooper.com ×5)

处理 5 篇 Daniel Chase Hooper 博客。新增 4 概念页（segment-array, build-process-visualization, swift-dylib-hot-reloading, ai-code-agent-workflow）、1 人物页（daniel-chase-hooper）、5 source 摘要。无跳过。与 [[binary-hot-reload]] / [[linear-allocator]] / [[vibe-coding-workflow]] 建立交叉引用。主题横跨 computer-systems（数据结构 / 构建系统 / 动态链接）与 software-design（AI coding agent 工作流）。

## [2026-04-19] ingest | Wave-69 Worker GW (Hexops / Mach / Stephen Gutekanst ×5)

处理 5 篇 devlog.hexops.org，4 篇入库（nominated Zig / Mach v0.3 / mach-dxcompiler / pkgmirror），1 篇跳过（2026s 是 pkgmirror 公告首页快照，重复）。新增 6 概念页（mach-engine, mach-nominated-zig-versions, sysgpu-webgpu-successor, dxc-dxil-signing, mach-dxcompiler-static-build, zig-package-mirror）、1 人物页（stephen-gutekanst）、4 source 摘要。给 webgpu-intro / zig-c-abi-boundary / slang-shader-language 追加交叉引用。

## [2026-04-19] ingest | Wave-70 Worker HB (blog.runevision.com ×5)

blog.runevision.com 早期 2010 年内容：Nordic Game Jam 与 Unity 动画 demo 预告基本为事件通稿，跳过 3 篇；3 月 14 日 GDC 2010 recap 有 Uncharted 动画技术干货，已吸收为 [[sources/runevision-gdc2010-animation]]，并新建 [[additive-animation-layering]] 概念页。另有 1 篇是月度归档页，与 post URL 完全重复，按 skipped_duplicate 处理。

## [2026-04-19] ingest | Wave-70 Worker HA (chipsandcheese.com ×5)

处理 5 篇 chipsandcheese.com 早期文章（2020-12 ~ 2021-01）。4 篇跳过（建站介绍、Nvidia 企业部门传闻、Intel HEDT 路线图回顾、Intel CEO 更替评论）——均无技术实质。1 篇入库：Chester Lam 基于 Nvidia 2017 MCM 论文的 GPU 多 die 架构分析，新增概念页 [[mcm-gpu-design]] 与 source [[sources/chipsandcheese-nvidia-mcm-gpu]]，并补全 Chester Lam / Chips and Cheese 人物页的交叉链接。

## [2026-04-19] ingest | Wave-70 Worker HC (raytracey.blogspot.com 2010 早期 ×5)

处理 5 篇 Sam Lapere 2010 年早期博客。新增 2 概念页（gpu-unbiased-path-tracing, otoy-cloud-rendering）、2 source 摘要。跳过 3 篇纯产品公告（Octane/Arion 一行通告、GDC 嘉宾转载）。更新 sam-lapere 人物页 sources 从 2→4。

## [2026-04-19] ingest | Wave-71 Worker HD (c0de517e.blogspot.com early 2010 ×5)

Pesce 2010 年 1-2 月博客 5 篇：4 篇跳过（工作流/ergonomics meta、链接堆、Fravia 讣告及其重复件），仅 `pitfalls-of-experience` 实质性入库。新增 2 概念页（`experience-as-noise-filter`、`scene-graph-unnecessary-in-engine`）、1 source 摘要，并为 `angelo-pesce` 和 `scene-graph-matrix-stack-visitor` 打补丁（后者增补反面观点链接）。

## [2026-04-19] ingest | Wave-71 Worker HE (blog.s-schoener.com ×5)

处理 5 篇 Sebastian Schöner 早期（2016-2017）博客。2 篇计算复杂度理论系列入库：新增概念 computational-complexity-theory-intro（$\P/\NP/\coNP$/归约入门）+ patterna-hexcells-np-vs-conp（纠正『扫雷是 NP-complete』的普遍误解：玩家实际做的推理问题是 $\coNP$-complete）。跳过 3 篇非技术元内容（博客 landing 索引、ImageMagick 个人速查、Jekyll 搭建记）。Sebastian Schöner 人物页已存在，追加复杂度理论主题、相关链接与 2 条 source 引用。

## [2026-04-19] ingest | Wave-71 Worker HF (chipsandcheese.com ×5)

处理 5 篇 chipsandcheese.com 2021-01 ~ 2021-02 文章。3 篇入库：BlueSwordM 的现代数据压缩系列 part 1（JPEG 编码管线）、Chips and Cheese 集体作者的三家平台安全栈横评、以及 CTR Safety Revisited（聚焦 Black's Equation 电迁移与静态 OC vs 动态 Boost 的电压退化机理）。2 篇跳过：AMD 未来 CPU 文被作者自己 formally retracted 为传闻站立场，无技术内容；CTR 初评被同月跟进的 Safety Revisited 覆盖得更系统，不重复收录。新增概念页 [[jpeg-codec-pipeline]]、[[cpu-gpu-platform-security-features]]、[[electromigration-voltage-degradation]]，新增 [[blueswordm]] 人物页，patch 了 [[chips-and-cheese]]、[[mttf-reliability]]、[[intel-13th-14th-gen-clock-degradation]] 三处交叉链接。

## [2026-04-21] query | Unity Built-in 移动端麻将阴影方案

问题：Built-in 管线、固定斜视、3 avatar、中端手机，如何高性能实现阴影。
答复：output/reports/mahjong-mobile-shadows-builtin.md。核心方案是关掉 built-in real-time shadow，改用分层混合：桌面共享 shadow RT（静态烘焙 + 河牌 Blit 增量），avatar 用平面投影阴影（共享 atlas RT）投到桌面与虚拟牌顶平面，牌根接触阴影烘焙进贴图。参考 [[blob-shadow-decal-vs-plane]] / [[cached-shadowmaps]] / [[prebaked-corner-occlusion]]。

## [2026-04-19] ingest | Wave-72 Worker HG (c0de517e ×5 all-duplicate)

批次 batch-w72-hg：全部跳过。5 篇均为 -2 后缀月度归档副本，内容与无后缀原文完全相同（仅 URL scheme 及 fetched 日期有差异）。原文已在 batch-w14-ao（ergonomy-rant、iphone-ipad-ipod）和 batch-w25-bu（new-layout、small-brdf-visualizer、3d-engines-out-there）中处理并跳过。无新增页面。

## [2026-04-19] ingest | Wave-72 Worker HI (randomtower.blogspot.com ×5)

处理 5 篇 randomtower.blogspot.com 2010 年文章。摄入 2 篇 FlashPunk 技术文章，新增 1 概念页（flashpunk-framework）、1 人物页（marte-randomtower）、2 source 摘要。跳过 3 篇非技术内容（VVVVVV 短评、游戏截图展示、MW2 观感）。

## [2026-04-19] ingest | Wave-72 Worker HH (chipsandcheese.com ×5，2021)

处理 5 篇 chipsandcheese.com 2021 年文章。新增 5 概念页（zen2-microarchitecture、branch-predictor-design、cpu-scheduler-design、jpeg-xl-format、gpu-memory-hierarchy-latency）、3 source 摘要页。跳过 2 篇（6700 XT 发布披露批评 + Rocket Lake 评测方法论批评，无微架构深度内容）。更新 chester-lam 人物页，追加引用 2 篇。

## [2026-04-19] ingest | Wave-73 Worker HL (raytracey.blogspot.com 2010-03/04 ×5)

处理 5 篇 Sam Lapere 2010 年 3-4 月短博。2 篇入库（SVO+Laine 论文、Fermi+OptiX 基准），3 篇跳过（OTOY 新闻稿、Gaiking trailer、Octane 荷兰招聘）。新增 1 概念页 efficient-sparse-voxel-octrees，2 source 摘要；sam-lapere 已有页仅追加 source/相关链接。

## [2026-04-19] ingest | Wave-73 Worker HJ (joostdevblog.blogspot.com ×5)

处理 5 篇 Joost van Dongen 2010 年 Proun 早期博客。ingest 2（景深 + 伪 HDR）、skip 3（开场白/关卡 UX leashing/抽象艺术史随笔）。新增 2 概念页（variable-size-gather-dof, fake-hdr-half-brightness）、2 source 摘要；joost-van-dongen 人物页已存在，仅追加 source 链接。

## [2026-04-19] ingest | Wave-73 Worker HK (hacksoflife.blogspot.com ×5, 2010-01)

处理 Ben Supnik 2010 年 1 月 5 篇文章，全部 topical。新增 4 概念页（incremental-rearchitecting、header-as-user-manual、api-fast-path-design、number-puzzle-tile-shader）、5 source 摘要。ben-supnik 人物页和 gpu-printf-debugging 概念页为 registry 已有页——发 patch。主题覆盖：大重写的组织动力学 + 增量重构、头文件即用户手册、API 快/慢路径显式拆分（X-Plane dataref 模式）、shader 级瓦片随机化、GLSL printf 调试。

## [2026-04-19] ingest | Wave-74 Worker hm (alfredbaudisch.com ×5)

处理 alfredbaudisch.com 早期 dailies 批次（2021-03-11 至 03-15）5 篇。全部不过题材关：sitemap 为纯导航；hello-world 和 dailies-rules 为个人项目自律元帖；#0003 hard-surface + photobash 仅三句“建模难、光光难、photobash 有趣但难”并附截图，无具体技术；#0004 PS1 腊肠狗绑定仅为进度流水帐。同博客后期篇目（Substance Designer 首次、Banjo-Kazooie N64 地形、顶点色 Wash Car 等）如被抓取值得今后单独评估。零新增页面，无 patch。

## [2026-04-19] ingest | Wave-74 Worker HN (blog.gemserk.com ×5)

处理 5 篇 Gemserk 2010 年早期博客。ingest 1（Applet/Webstart JAR 签名与 Maven profile 自动化）、skip 4（博客存档页 / 工作室欢迎帖 / Tower Defense 三行通告 / Jylonwars 两行通告）。新增 1 概念页（java-webstart-jar-signing）、1 source 摘要；gemserk 人物页已存在，仅追加 source 链接。

## [2026-04-19] ingest | Wave-74 Worker HO (boristhebrave.com ×5)

处理 5 篇 Boris The Brave 早期文章。Ingest 3 篇：tileset roundup（autotile 布局综述）、AS3 gems（语言设计）、Axaxaxas（Earley parser 库）。Skip 2 篇：Box2DFlash 2.1a 发布公告、Celtic Knots Blender 插件发布短文，均为无实质内容的 release note。新增概念页 4 张：[[autotile-tileset-layouts]]、[[optional-static-typing]]、[[method-binding-semantics]]、[[earley-parser]]；新增 source 摘要 3 张；对 [[boris-the-brave]] 补 sources: 6 与 4 条相关概念链接。

## [2026-04-19] ingest | Wave-75 Worker HP (bitsquid.blogspot.com ×5 early 2010)

处理 Bitsquid 2010 年 1-4 月 5 篇早期博客。新增 5 概念页（vcs-vs-database-for-content, offset-based-resource-blobs, bitsquid-task-scheduler, sdf-font-atlas-rendering, decoupled-tool-engine-json-rpc）、5 source 摘要。Niklas Frykholm 人物页追加 sources。

## [2026-04-19] ingest | Wave-75 Worker HR (allarsblog.com ×5)

处理 Michael Allar 2010 年 UDK 时代 5 篇。ingest 1 合并 source（Beginning Your Game Part 1+2：GameInfo / Pawn / PlayerController 搭空白工程）、skip 3（M16 建模 / 几何绑定 / dummy 绑定三篇——视频入口页或 3DS Max+ActorX 纯工作流，无泛化价值）。新增 1 概念页（unreal-pawn-playercontroller-pattern）、1 source 摘要；michael-allar 人物页已存在，patch 追加相关链接与 source。

## [2026-04-19] ingest | Wave-75 Worker HQ (blog.s-schoener.com late-2017 ×5)

处理 Schöner 2017 年末 5 篇：ingest 4 篇（no-magic-principle 信条、TF 1.3 入门、TF 多 GPU、DL uncertainty 思辨），skip 1 篇（hi-there blog intro）。新增概念页 4：[[no-magic-principle]]（software-design）、[[tensorflow-1-graph-model]]、[[multi-gpu-training-replication-patterns]]、[[deep-learning-uncertainty]]（全部 computer-systems），TF 两页明确标注 TF 1.x API 已过时、保留的是思想层映射到 DDP/XLA/MLIR 的桥。新增 source 摘要 4 张，对 [[sebastian-schoener]] 更新 sources 7→11、补 ML 主题段与 4 条相关链接。

## [2026-04-19] ingest | Wave-76 Worker HT (c0de517e.blogspot.com 2010-03 ×5)

处理 Angelo Pesce 2010-03 的 5 个文件：1 篇独立 ingest（skin）、1 篇 skipped_offtopic（68000 访问量里程碑 + Amiga 调侃）、1 篇 skipped_offtopic（homework 工作方法论短文，非技术）、2 篇 skipped_duplicate（-2.md archive 副本）。新增 1 份 source 摘要（c0de517e-skin），触及 [[angelo-pesce]] 与 [[sss-practical-implementation]]。

## [2026-04-19] ingest | Wave-76 Worker hu (tedsieblog A* 系列 + Everyplay)

处理 tedsieblog.wordpress.com 5 篇。A* 四篇（intro/node definition/node generate/node sort）合并为单一源摘要 [[sources/tedsie-a-star-tutorial]]，链接到既有 [[a-star-pathfinding]] 概念页；跳过 Everyplay SDK 6 步安装教学（无技术内容、服务 2018 已下线）。无新概念/人物页。

## [2026-04-19] ingest | Wave-76 Worker HS (bitsquid.blogspot.com 2010 Q2-Q3 x5)

处理 5 篇 Bitsquid 2010 年博客。新增 4 概念页（per-entity-scene-graph, json-3-way-merge, guid-object-database-schema, dual-mode-gui-bitsquid）、4 source 摘要；跳过 MotionBuilder exporter（纯 code-drop 无内容）。补强 vcs-vs-database-for-content 与 immediate-vs-retained-mode 两篇的 Sources 与交叉链接。niklas-frykholm 人物页追加 4 条来源。

## [2026-04-19] ingest | Wave-77 Worker HW (hacksoflife.blogspot.com ×5)

处理 Ben Supnik 2010 年 1-2 月 5 篇早期博文。新增 3 概念页（opengl-builtin-attribute-aliasing / cpp-template-value-vs-type-parameter / triangle-strips-vs-indexed-triangles）、4 source 摘要，跳过 1 篇 iPhone 沙盒+Moore's Law 编辑性评论。Patch 更新 ben-supnik 人物页与 draw-call / opengl-draw-call-batching-sweet-spot 两条相关链接。

## [2026-04-19] ingest | Wave-77 Worker HX (joostdevblog.blogspot.com ×5 — Proun 2010-10)

处理 5 篇 Joost van Dongen 2010-10 博客：三篇 camera mapping 合并为 1 source 摘要 + 1 概念页（camera-mapping-2d-to-3d）；碰撞 3000fps trick 与抗晕眩摄像机各自独立成 source+concept。新增 3 概念页、3 source 摘要，给已有 joost-van-dongen 人物页追加 sources 与相关链接。

## [2026-04-19] ingest | Wave-77 Worker HV (bitsquid.blogspot.com ×5)

处理 5 篇 Niklas Frykholm 2010 Q3-Q4 博客。新增 4 概念页（flow-graph-data-oriented-runtime、custom-allocator-interface、static-hash-value-debug-assert、dependency-checker-tool）与 4 source 摘要，对 niklas-frykholm、offset-based-resource-blobs、data-driven-architecture、linear-allocator、malloc-wrapper-debug、non-cryptographic-hash 六个已有页追加补丁。跳过 1 篇（bitbucket-for-bitsquid，纯博客基础设施公告、原文被 SEO 垃圾评论淹没）。

## [2026-04-19] ingest | Wave-78 Worker IA (4rknova.com ×5)

处理 4rknova.com（Nikos Papadopoulos / Arkanova）2012-2013 早期博客 5 篇。2 篇保留：C/C++ 资源嵌入三段论（xxd / `#include`+STRINGIFY / asm `.incbin`）、GLSL Conway 生命游戏（与 [[gpu-gol-optimization-ladder]] 形成 naive vs optimized 对照）。新增 1 概念页（c-cpp-embed-binary-blobs）、1 人物页（nikos-papadopoulos）、2 source 摘要。跳过 3 篇：GNU make -j alias（过薄）、Debian primus NVIDIA Optimus 配置（偏 distro 运维）、demos 页目录（无正文）。

## [2026-04-19] ingest | Wave-78 Worker HZ (hacksoflife.blogspot.com 2010-02 ×5)

处理 Ben Supnik 2010 年 2 月的 5 篇 X-Plane 技术短文，全部 ingest。新增 5 概念页：stl-not-abstraction-prescription（软件设计反面案例）、huge-world-coordinate-precision（大世界 float 精度）、function-vs-data-pointer-portability（GLX 函数指针签名）、texture2dgrad-explicit-derivatives（UV 不连续与 LOD）、uv-precision-derivative-loss（vertex projected UV 精度耗尽）。新增 5 source 摘要。对 ben-supnik、false-abstraction、abstraction、coordinate-spaces、fwidth-derivative-antialiasing 打 patch。

## [2026-04-19] ingest | Wave-78 Worker HY (bitsquid.blogspot.com 2010 末/2011 初 ×5)

处理 5 篇 Niklas Frykholm Bitsquid 早期文章：time step smoothing、A* is overrated、C++ coding style（skip：raw 正文为空，全是评论）、managing coupling part 1 & 2。新增 4 概念页：[[variable-timestep-smoothing]]、[[local-navigation-over-pathfinding]]、[[system-decoupling-patterns]]、[[polling-callbacks-events]]；4 source 摘要；对 [[a-star-pathfinding]] 与 [[niklas-frykholm]] 各打一条 append patch。Niklas 的解耦系列与 cloudwu 的 [[id-based-lifetime-with-kill-flag]]、既有 [[handle-based-resource-manager]] 形成交叉引用。

## [2026-04-19] ingest | Wave-79 Worker IB (bitsquid.blogspot.com 2011 Q1-Q2 x5)

处理 5 篇 Niklas Frykholm / bitsquid 2011 年博客。1 篇跳过（仅 GDC 视频外链加 spam）；4 篇入库：表达式语言（新概念 tiny-expression-language）、协作与合并（patch guid-object-database-schema）、极限 bug 狩猎（新概念 memory-corruption-bug-hunting）、通用 Undo/Copy/Paste（patch guid-object-database-schema）。新增 2 概念 + 4 source 摘要。

## [2026-04-19] ingest | Wave-79 Worker IC (hacksoflife 2010-02 ×5)

Ben Supnik 2010 年 2 月连载的 OpenGL VBO / alpha blending 四篇全部 ingest，另跳过 1 篇 Apple Mail multipart MIME 吐槽。新增 4 概念页（alpha-blending-front-to-back, vbo-double-buffering-orphaning, agp-vs-vram-streaming, glbuffersubdata-serialization）+ 4 source 摘要。四篇互相引用，并与已有 [[alpha-blending]] / [[alpha-compositing]] / [[buffer-renaming]] / [[ben-supnik]] 交叉链。

## [2026-04-19] ingest | Wave-79 Worker ID (joostdevblog.blogspot.com ×5 — Proun graphics, 2010-11..12)

处理 5 篇 Joost van Dongen 的 Proun 技术博客（立体 3D、god-rays、lightmap 烘焙、对比色灯光、PC 驱动兼容）。全部 ingest。新增 5 概念页（stereoscopic-3d-design / screen-space-light-shafts / lightmap-baking-workflow / colored-sky-sun-lighting / pc-gpu-driver-compat-qa）、5 source 摘要，patch 已存在的 [[joost-van-dongen]] 人物页（相关 / Sources / sources count 3→8）。

## [2026-04-19] ingest | Wave-80 Worker IG (nklein.com ×5)

处理 5 篇 nklein.com（Patrick Stein，2010-01/02 iPhone dev 时期）。保留 1 篇技术文（CL-OpenGL + ZPB-TTF 矢量字形反走样的屏幕空间 cutoff 自适应细分），跳过 4 篇 iPhone Spelling Toy 里程碑 / 发布公告。新增 1 概念页（screen-space-curve-tessellation-cutoff）、1 人物页（patrick-stein）、1 源摘要。

## [2026-04-19] ingest | Wave-80 Worker batch-w80-if (hacksoflife.blogspot.com ×5)

处理 Ben Supnik 2010-03 ~ 2010-04 共 5 篇。入库 3 篇（OpenGL 扩展分桶策略、GPU 并行性与串行派发、CGAL 尾数膨胀）。跳过 2 篇：constitutional-opposition（Apple SDK 许可证评论）、thank-you-jeeves（C++ 语法小笑话）。新增 3 个概念页、3 个 source 摘要；Supnik 人物页追加相关与 Sources。

## [2026-04-19] ingest | Wave-80 Worker IE (bitsquid.blogspot.com 2011-Q2/Q3 ×5)

处理 Niklas Frykholm 2011 年 5-8 月的 5 篇 Bitsquid 博文。新增 4 概念页（game-monitoring-event-buffer、string-handling-game-runtime、lua-light-userdata-bindings、lua-memory-profiling）+ 5 source 摘要；patch flow-graph-data-oriented-runtime（hierarchical grouping / query 节点 follow-up）、lua-cpp-binding、lua-incremental-gc、static-hash-value-debug-assert 的交叉引用。

## [2026-04-19] ingest | Wave-81 Worker IJ (blog.playcanvas.com 2012 ×5)

处理 PlayCanvas 博客 2012 年 5 篇早期文章，全部低信息量营销/动态贴（博客开张、Google I/O 展台、GitHub 集成、HTML5 观点转载、年度榜单入选），无技术深度，全部 skip。

## [2026-04-19] ingest | Wave-81 Worker II (hacksoflife.blogspot.com Supnik 2010-05~08 ×5)

处理 5 篇 Ben Supnik 博文，3 ingested（cgal-arrangements-import / fear-of-threading / vbo-really-double-buffered），2 skipped（how-does-opengl-work 仅推荐 WWDC 视频；restarting-os-x-window-server macOS 小技巧）。新增 2 概念页（cgal-arrangement-import-antennas, message-queue-thread-ownership）、3 source 摘要。Supnik 人物页 / vbo-double-buffering-orphaning / cgal-exact-arithmetic-mantissa-growth patch 已入栈。

## [2026-04-19] ingest | Wave-81 Worker IH (bitsquid 2011-Q3/Q4 ×5)

处理 5 篇 Niklas Frykholm 博文（watch-window 设想 / MurmurHash2 inverse / 自制 Ruby 文档系统 / ID lookup table 三级演化 / Header Hero 编译时间分析）。新增 5 概念页（external-data-inspector, murmur-hash-inverse, minimal-markup-pipeline, id-lookup-table-packed, header-hero-compile-analysis）、5 source 摘要。人物页 niklas-frykholm 已存在，补充 5 条 source 链接。跨引至 id-based-lifetime-with-kill-flag、handle-based-resource-manager、system-decoupling-patterns、static-hash-value-debug-assert 等既有概念。

## [2026-04-19] ingest | Wave-82 Worker IM (nklein.com Patrick Stein 2010-02~04 ×5)

处理 5 篇 nklein 博文。3 篇跳过：iPhone 拼写 app 两则产品更新（bugfix / 动物美术+翻译）、GIMP 烧焦纸张 Script-Fu 插件。2 篇（2010-03 XML Parser Generator 长文 + 2010-04 两行发布公告）合并为一份 source 摘要 nklein-xml-parser-generator，新增 1 概念页 schema-driven-xml-parser-generator（Common Lisp schema-driven codegen、tagstack SAX、自举、多语言后端），并在 patrick-stein 人物页补链。

## [2026-04-19] ingest | Wave-82 Worker IK (bitsquid 2011 late ×5)

处理 5 篇 2011-Q4 bitsquid.blogspot.com 文章：low-level animation part 2、DOD sound parameters、pragmatic performance、platform-specific resources、patch link.exe LNK4099。新增 5 概念页（animation-stream-cache-layout、parameter-nodes-intrusive-linked-list、pragmatic-performance-philosophy、platform-specific-resources-property-system、link-exe-lnk4099-patch）、5 source 摘要。人物页已存在（niklas-frykholm），仅追加 source 链接。

## [2026-04-19] ingest | Wave-82 Worker IL (hacksoflife.blogspot.com Supnik 2010-09/10 × 5)

处理 5 篇 Ben Supnik 短文。新增 3 概念页（shared-library-soname-versioning, floating-point-geometric-predicates, premultiplied-alpha-bilinear-ring）、5 source 摘要。主题：debugger 打印 STL 触发线程释放看到 race condition；OpenAL Linux SONAME major 升级 + 删除旧 .so 的 ABI 管理错位；X-Plane 里点积几何谓词的浮点脆弱性；预乘 alpha 修复 bilinear tree-ring 但 BCn 压缩精度让 X-Plane 最终选 alpha test；预乘约定下 back-to-front/front-to-back 的对称 blend state 配方。Patch 到 alpha-blending / alpha-blending-front-to-back / alpha-compositing / srgb-premultiplied-alpha-compression / ben-supnik。

## [2026-04-19] ingest | Wave-83 Worker IP (tedsieblog.wordpress.com A* 续作 ×5)

处理 Ted Sie 2016-07-10 A* 五篇续作。4 篇技术文（implement / eight-ways / line-of-sight / obstacle-detection）合并为单一 source 摘要 tedsie-a-star-applied，achievement 篇（纯 Unity wiring 展示）作为 runner 段并入同一摘要。无新概念页，复用既有 [[a-star-pathfinding]]。在 ted-sie 人物页与 a-star-pathfinding 概念页 Sources 段加链。

## [2026-04-19] ingest | Wave-83 Worker IO (hacksoflife.blogspot.com Supnik 2010-10/11 × 5)

处理 5 篇 Ben Supnik 短文，4 篇 ingest、1 篇 skip（mediawiki-modsecurity 纯 WAF 误伤的 sysadmin 记录）。新增 3 概念页（gpu-sliced-volumetric-shadows-limits, cross-platform-openal-runtime-loader, c-bitwise-operator-precedence-history）、4 source 摘要。主题：GPU sliced shadow 算法对 flight-sim 云（偏不透明粒子 + 空间分桶 + 切片方向翻转）的失败模式；OpenAL 三平台装载策略统一成封装层 + dlopen/LoadLibrary fallback + Windows 自带 LGPL 副本；C++ 侵入式结构中 child 找 parent 的类型系统限制（byte offset 不可作为模板参数）；C 位运算符优先级低于比较的 B/BCPL 历史根源——Ritchie 选择不破坏旧代码语义。Patch 到 ben-supnik / shared-library-soname-versioning / cloudscape-sdf-volumetric / parameter-nodes-intrusive-linked-list。

## [2026-04-19] ingest | Wave-83 Worker IN (bitsquid 2012 early x5)

处理 5 篇 2012 年初 Bitsquid Blog：5 Tips + Sensible Error Handling 三部曲 + 文档系统代码公开。新增 5 个 software-design 概念页：crash-on-unexpected-errors、error-context-stack、minimize-points-and-types-of-failure、warnings-as-errors-strategy、now-principle-productivity。新增 5 个 source 摘要。文档系统一文不单建概念页，而是补丁到已有 minimal-markup-pipeline。niklas-frykholm 人物页已存在，追加相关概念与 5 条 source 链接。

## [2026-04-19] ingest | Wave-84 Worker IS (blog.playcanvas.com 2013 ×5)

处理 5 篇 2013 年 PlayCanvas 早期博客。仅保留 1 篇云端资产管线发布公告（Dave Evans, 2013-06），其余 4 篇（meetup / Ludum Dare / 域名搬家 / 招人）SKIP 为社区公告。新增 1 概念页 [[playcanvas-cloud-asset-pipeline]]、1 人物页 [[dave-evans]]、1 source 摘要。

## [2026-04-19] ingest | Wave-84 Worker IR (hacksoflife Supnik gamma trilogy ×5)

处理 Supnik 2010-11 gamma 系列 5 篇：三部曲 + value-of-gamma-compression 合并为单一 source 摘要 supnik-gamma-lighting-trilogy；新增 concept linear-lighting-pipeline（光照累积的三条路径）。跳过 i-hate-c-part-492（纯 CFBundleGetFunctionPointerForName 代码片段，无论述）。补强 ben-supnik / gamma-correction-srgb / color-space / color-banding 之间的交叉链接。

## [2026-04-19] ingest | Wave-84 Worker IQ (bitsquid 2012 Q1/Q2 x5)

处理 5 篇 Bitsquid 2012 年 3–5 月博客：4 篇 ingested、1 篇 skipped（GDC2012 rendering-talks 抓到的全是垃圾评论）。cutting-the-pipe 虽只抓到评论区，但 Q&A 直接点明 Bitsquid 工具/引擎零共享 + JSON 通信取舍，作为 source 页补充到 decoupled-tool-engine-json-rpc。新增 4 概念：pimpl-vs-pure-virtual（对比 C opaque / PIMPL / 纯虚）、ragdoll-velocity-inheritance（last_world 方案）、no-frame-delays-principle（本文顺手立下的 Bitsquid 戒律）、lua-runtime-dynamism-tricks（七条 Lua 动态性用法）。niklas-frykholm 页已存在，补挂 4 条 source 链接与 4 条 相关。

## [2026-04-19] ingest | Wave-85 Worker IV (c0de517e.blogspot.com 2010-03 ×5)

处理 5 篇 Pesce 2010-03 博文：2 篇 monthly-archive 重复（retweeting-2 / the-world-changed-2）skipped_duplicate；retweeting（webtoy 推荐）与 the-world-changed（Web 开发感叹）skipped_offtopic；保留 collaborative-design-experiment——2010 年社区协作产出的六层引擎架构清单。新增 1 概念页 [[pesce-2010-engine-layer-sketch]]、1 source 摘要，给 [[angelo-pesce]] / [[engine-layering]] 挂 cross-link。

## [2026-04-19] ingest | Wave-85 Worker IU (hacksoflife Supnik 2010-11/12 ×5)

处理 Ben Supnik 2010 年末 5 篇：more-stl-abstraction / change-of-basis-revisited / basis-projection / is-1-a-lot / semaphore-vs-condvar。change-of-basis 双篇合并成 matrix-as-basis-vectors 一个概念页（encoder/decoder 双视角）；另新增 optimization-leverage-ratio（Amdahl 的工程化）与 semaphore-vs-condvar-latency（pthread cond var 重锁坑）。stl 续篇 patch 回已有 stl-not-abstraction-prescription。人物页 ben-supnik source count 22→27。

## [2026-04-19] ingest | Wave-85 Worker IT (bitsquid 2012 mid ×5)

处理 bitsquid.blogspot.com 2012-05 到 2012-08 共 5 篇 Niklas Frykholm 文章。新增 5 概念页（video-codec-licensing-tradeoffs, particle-collision-plane-cache, matrix-scale-drift, async-api-id-tokens, cleaning-bad-code）和 5 source 摘要。niklas-frykholm 人物页追加 5 条 source 链接；polling-callbacks-events / clean-code-critique / 3d-rotation-math 各追加一条 cross-link。无跳过。

## [2026-04-19] ingest | Wave-86 Worker IY (tedsieblog.wordpress.com ×5)

处理 Ted Sie 2016-07 的 5 篇 NGUI / Draw Call 入门文章。新增 1 概念页（ngui-legacy-ui-system）、2 source 摘要（tedsie-ngui-tutorials 合并 4 篇 NGUI 教学、tedsie-draw-call-basics 单独成文）。Draw Call 入门篇通过 patch 链进既有 [[draw-call]]。无跳过。

## [2026-04-19] ingest | Wave-86 Worker IX (hacksoflife 2010-12 Supnik ×5)

处理 5 篇 hacksoflife.blogspot.com 2010-12 Supnik 博文：4 篇 ingested，1 篇 skipped_offtopic。`semaphore-follow-up-ntpl` 作为前作 [[semaphore-vs-condvar-latency]] 的 Linux NPTL 跨平台补记，patch 上去并出 1 篇 source 摘要。`gbuffer-format` + `fmtt-glsl-edition` 是 X-Plane 10 第一版延迟管线的 G-Buffer 格式自述与 GLSL 实现样本，新增概念页 [[xplane-gbuffer-format]]（4 RT / 16 字节 / `256×shadow+shine` 浮点字段打包 / 16F 深度行星尺度不足），patch 到 [[deferred-rendering]]、[[multiple-render-targets]]。`what-oop-isnt` 新增概念页 [[encapsulation-over-polymorphism]]（90/10/0 启发式 + 继承三细分 + 评论区 LogicalError/David/Homer 立场），patch 到 [[classitis]]、[[cpp-multi-paradigm-discipline]]。`lisp-isnt-a-language` 只有 5 行 Alan Kay 引用 + 一句粪便吐槽，skipped_offtopic。共 2 概念、4 source 摘要，patch 3 个既有页 + Ben Supnik 人物页。

## [2026-04-19] ingest | Wave-86 Worker IW (bitsquid.blogspot.com 2012 Q3/Q4 ×5)

处理 Bitsquid 2012 年下半年 5 篇：header 组织 1 篇、vector field 三部曲（合并为 1 个 source + 1 个概念）、foundation library 发布 1 篇。新增 3 概念页（types-h-data-code-separation / vector-field-bytecode-vm / bitsquid-foundation-library-concept），3 个 source 摘要。niklas-frykholm 人物页已存在，仅追加 sources。补丁 4 个已有概念（custom-allocator-interface / header-hero-compile-analysis / bytecode-everywhere / header-as-user-manual）。无跳过。

## [2026-04-19] ingest | Wave-87 Worker JB (joostdevblog 2010-12 to 2011-01 ×5)

处理 5 篇 joostdevblog（2010-12 至 2011-01）。4 ingested（AI part1+part2 合并成单 source），1 skipped（endless art styles —— 纯风格taste论，无方法论）。新增 3 概念页：game-settings-hot-reload（F5 struct 指针热重载）、level-design-without-editor（Notepad 关卡 + 程序化背景）、behaviour-tree-game-ai（Ronimo 三代 AI 演进，含 Halo 2 启发、优先级树 vs if-else 树的迭代）；新增 3 source 摘要；更新 joost-van-dongen 人物页。

## [2026-04-19] ingest | Wave-87 Worker JA (hacksoflife / Supnik ×5, 2010-12 ~ 2011-01)

处理 5 篇 Supnik 博客：4 ingested、1 skipped（stupid-cvs-tricks 属 legacy VCS 琐事）。Derivatives I + II 合并到一篇 source summary（同一硬件模型、同一修法族）。新增 2 概念页：[[glsl-compiler-optimization-reliance]]（RV790 编译器观察驱动 X-Plane 10 shader 组织改写）、[[cas-refcount-lowbit-lock]]（CAS+refcount 的经典缺口 + 指针低位自旋锁 + Vyukov differential refcount）。3 source 摘要，Supnik 人物页 source count 27 → 30。Derivatives 内容已由 [[texture2dgrad-explicit-derivatives]] / [[divergent-gradient-in-branches]] 充分覆盖，只补 source link。

## [2026-04-19] ingest | Wave-87 Worker iz (bitsquid.blogspot.com 2012-11~2013-03 ×5)

处理 5 篇 Niklas Frykholm 早期 Bitsquid 博客：formal data-def language、four meditations on bad design、GC vs allocation sizes、Why Lua、object replication migration race。新增 5 概念页（binary-data-definition-language / strings-as-identifiers-antipattern / four-meditations-on-rewrites / page-granular-system-allocator / object-replication-migration-race）+ 5 source summaries。作者页补 5 条相关链接。

## [2026-04-19] ingest | Wave-88 Worker JC (bitsquid.blogspot.com 2013 ×5)

处理 5 篇 bitsquid 2013 博文：4 篇 ingested（gimbal lock / source censoring part 2 / finding nearby stuff / scripted network debugging），1 篇 skipped（gdc-2013-slides 正文已被 SEO 评论垃圾完全吞噬，无任何技术内容）。新增 4 概念页（gimbal-lock-euler-interpolation, repo-clone-with-filter, spatial-hash-grid-linked-list, scripted-network-debugging）、4 source 摘要，niklas-frykholm 人物页追加概念与 source 链接并把 sources 计数 10 → 14。

## [2026-04-19] ingest | Wave-88 Worker JD (hacksoflife 2011-01 to 2011-02 ×5)

处理 5 篇 hacksoflife（Supnik 2011 年 1-2 月）。3 ingested：derivatives-iii（内建导数浮点耗尽 → 算法式导数替换，接 derivatives-two-parts 与 uv-precision-derivative-loss）、is-collada-a-win（DCC 资源交换三路线决策）、g-buffer-normals-revisited（Lambert azimuthal 2 通道法线编码，直接迭代 xplane-gbuffer-format 的 XY + 重建 Z 方案）。2 skipped：losing-javadocs-in-eclipse（作者 Chris 的 IDE 菜单操作步骤，off-topic）、random-wordpress-notes（WP + mod_rewrite 博客托管技巧）。新增 2 概念页：compact-normal-encoding、asset-exchange-format-strategy；新增 3 source 摘要；patch xplane-gbuffer-format（补充 Lambert 后续）、uv-precision-derivative-loss（补充算法式导数）、ben-supnik 人物页。

## [2026-04-19] ingest | Wave-88 Worker JE (joostdevblog 2011-01 to 2011-02 x5)

处理 5 篇 joostdevblog（2011-01-13 至 2011-02-10），全部 ingested。新增 4 概念页：rts-balance-taxonomy（Joost 七种 RTS 平衡面孔）、destroy-recreate-vs-reset（Maarten 的销毁重建替代隐藏重置）、solo-programmer-discipline（独行程序员十条瓷砖格言）、perspective-meta-shapes（Proun 的视角相关 meta-shape 构图）。新增 5 source 摘要；role-of-game-designer 未建独立概念页（与既有 tools-first-iteration-loop 重叠），以 source 摘要形式保留并挂到 tools-first 的 Sources。更新 joost-van-dongen 人物页（sources 11→16）。
