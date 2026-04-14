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
