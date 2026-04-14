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
