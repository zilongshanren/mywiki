---
tags: [source, dxc, dxil, hlsl, directx, zig, 构建系统]
date: 2026-04-19
sources: 1
---

# Building the DirectX shader compiler better than Microsoft?（Stephen Gutekanst）

[[stephen-gutekanst]] 2024 年 2 月的长文，讲她为了让 [[mach-engine|Mach]] 的 [[sysgpu-webgpu-successor|sysgpu]] 能在 D3D12 上工作，不得不从头重构微软 [[dxc-dxil-signing|DirectX Shader Compiler]] 的过程——顺手做出了行业内第一个覆盖 macOS / aarch64 Linux / MinGW 的静态 DXC 分发（见 [[mach-dxcompiler-static-build]]）。

## 摘要

文章先梳理 DirectX shader 编译历史：FXC 被弃、DXC 基于 LLVM/Clang 3.7 的微软 fork、DXBC 与 DXIL 的未文档化"文档就是编译器输出"状态。接着点出一堆 WebGPU 实现（Dawn、wgpu、Bevy）的共同困境——DXC 比 FXC 好但要带两个 dll 分发，很多引擎因此默认用 FXC 导致社区普遍无法使用 SM6.0+。作者想摆脱这层 runtime 依赖，于是挑战静态链接：发现 DXC 的 CMake 写死 `SHARED`、COM 实现里有 `LoadLibraryW` 自调用、最大的拦路虎是专有的 `dxil.dll` 代码签名 blob（Windows Developer Mode 外必须有它）。最终作者用 ~1k 行 `build.zig` 替换了 ~10.5k 行 CMake，fork DXC 用 `// Mach change start/end` 注释改 C++，产出 mach-dxcompiler，在 macOS/aarch64 Linux/MinGW 等全部是"史上第一次"支持的平台做 CI 分发，DXIL 输出与 Windows 官方 DXC byte-for-byte 等价。

## 关键要点

- `dxil.dll` 是微软用来控制"哪些 DXIL 能跑"的 gatekeeper，从未开源，覆盖平台少。
- 把一个大型 C++ 项目的 CMake 整个推翻用 `build.zig` 重写，在 Zig + `zig cc` 工具链下反而是最省事的路。
- 作者明确本项目"只有我一个人维护，存在的目的是解决 Mach 自己的问题，用它你依赖我"。
- 文末呼应 Mach 哲学："software you can love"，对"open source 游戏"式的伪开源提出批评。

## 链接到的概念

- [[mach-dxcompiler-static-build]]
- [[dxc-dxil-signing]]
- [[sysgpu-webgpu-successor]]
- [[webgpu-intro]]
- [[stephen-gutekanst]]

## 原文

- 链接：<https://devlog.hexops.org/2024/building-the-directx-shader-compiler-better-than-microsoft/>
- 本地：`raw/articles/devlog.hexops.org/2024-02-09_building-the-directx-shader-compiler-better-than-microsoft.md`
