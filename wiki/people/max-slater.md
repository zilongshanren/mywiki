---
tags: [人物, 作者, 图形程序员, 渲染, 数学]
date: 2026-04-14
sources: 14
---

# Max Slater

**Max Slater**（博客 [thenumb.at](https://thenumb.at/)，GitHub: `TheNumbat`）是一位图形学/系统方向的工程师，曾在 **Pixar**、**Activision** 等做渲染相关工作，也参与过卡内基梅隆大学 15-462 计算机图形学课程（Scotty3D）。他的博客风格是「把数学写到能看懂、把工程写到能复现」的长文。

## 风格

- **数学教学类长文**：多篇是按教材章节铺陈——先定义，后推导，然后配交互 demo。*Monte Carlo Crash Course*、*Functions are Vectors* 是典型代表，后者拿到了 3Blue1Brown 的 Summer of Math Exposition 3 荣誉奖。
- **「从零写一个 X」类工程文**：Exile 项目（C 风格 C++ 写的体素引擎）贡献了一系列硬核技术笔记——reflection 元编程、voxel 渲染管线、hot reload 系统。
- **把编译器 bug 拆到汇编级别**：遇到奇怪 bug 就 godbolt + 汇编 diff，Compiler Bug 那篇是把一个 MSVC stack 重叠问题挖到「x86 指令少分配了 4 KB 栈」的程度。
- **以数学工具拆实时渲染**：光谱渲染、QMC、球谐——他愿意从泛函分析讲起再落到 GPU。

## 对本 wiki 的贡献
| 文章 | 贡献的概念 |
|---|---|
| Monte Carlo Crash Course – Quasi-Monte Carlo | [[quasi-monte-carlo]]、[[stratified-sampling]]、[[low-discrepancy-sequence]]、[[poisson-disk-sampling]] |
| Functions are Vectors | [[functions-as-vectors]]、[[spherical-harmonics]] |
| Exile: Voxel Rendering Pipeline | [[greedy-voxel-meshing]]、[[voxel-ambient-occlusion]]、[[compact-vertex-format]] |
| Exile: Reflection | [[cpp-runtime-reflection]] |
| A Compiler Bug | [[compiler-interference-analysis-bug]] |
| Monte Carlo Crash Course – Exponentially Better Integration | [[monte-carlo-integration]] |
| Monte Carlo Crash Course – Sampling | [[inversion-sampling-prng]] |
| Monte Carlo Crash Course – Case Study: Rendering | [[path-tracing-monte-carlo]] |

## 相关
- [[quasi-monte-carlo]]
- [[functions-as-vectors]]
- [[greedy-voxel-meshing]]
- [[cpp-runtime-reflection]]
- [[compiler-interference-analysis-bug]]
- [[monte-carlo-integration]]
- [[inversion-sampling-prng]]
- [[path-tracing-monte-carlo]]

## Sources
- [[sources/slater-qmc-crash-course]]
- [[sources/slater-functions-are-vectors]]
- [[sources/slater-exile-voxel-rendering]]
- [[sources/slater-exile-reflection]]
- [[sources/slater-compiler-bug]]
- [[sources/slater-exile-hot-reloading]]
- [[sources/slater-hamming-hats]]
- [[sources/slater-exponential-rotations]]
- [[sources/slater-autodiff]]
- [[sources/slater-neural-graphics-primitives]]
- [[sources/slater-optimizing-open-addressing]]
- [[sources/slater-spherical-integration]]
- [[sources/slater-oxidizing-cpp]]
- [[sources/slater-continuous-probability]]
- [[sources/slater-mc-integration]]
- [[sources/slater-mc-sampling]]
- [[sources/slater-mc-rendering]]
