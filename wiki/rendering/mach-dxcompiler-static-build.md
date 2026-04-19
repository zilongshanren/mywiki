---
tags: [渲染, 着色器编译, dxc, zig, 构建系统, 跨平台]
date: 2026-04-19
sources: 1
---

# mach-dxcompiler：静态化 DXC 并跨平台分发

`mach-dxcompiler` 是 [[stephen-gutekanst]] 为 [[mach-engine|Mach]] 的 [[sysgpu-webgpu-successor|sysgpu]] 做 D3D12 支持时，顺手把微软 DirectXShaderCompiler 重做了一次——结果成了行业里第一个能在 macOS、aarch64 Linux、Windows MinGW 上离线编 HLSL shader 的 DXC 分发，且 **完全不依赖 [[dxc-dxil-signing|`dxil.dll`]] 这个专有签名 blob**。

## 要解决的三重锁

Mach 想做"离线 shader 编译、不强制下游分发 DXC 重量级依赖"，但微软那边堆了三个锁：

1. **DXC 不支持静态链接**。CMake 文件把几乎所有模块写成 `SHARED`，表面换成 `STATIC` 会出来 ~15 个互相隐式依赖的静态库；试改成 CMake `OBJECT` library 会发现 HLSL 改动引入了跨目录的隐式依赖，"几乎要把整个仓库的 cmake 重写一遍"（作者亲测，最后放弃）。
2. **DXC 的 COM 实现自带 `LoadLibraryW` 自调用**，就算链成单可执行也会跑去动态加载 `dxcompiler.dll` / `dxil.dll`。
3. **`dxil.dll` 是专有签名 blob**，没有 macOS / aarch64 Linux 版本，且你就算自己从源码 build DXC 也不会产出它，见 [[dxc-dxil-signing]]。

## 解法

Stephen 走了最"底"的一条：

**第一步：整个 CMake 系统推掉重写。** ~10.5k 行 CMake 换成 ~1k 行 `build.zig`——只保留 `dxcompiler` 库和 `dxc.exe` CLI。剩下那 1k 行里很大一部分还只是 `git clone` 源码、预编译产物下载、header 生成（部分来自 llvm-tablegen 还没翻完）。

**第二步：fork 微软的 DXC 仓库改 C++。** 在源码里加 `// Mach change start/end` 注释：模拟 `dllmain` 入口点、禁掉依赖 dll 输出的版本信息打印、把动态库符号查找替换成静态绑定的函数指针。

**第三步：搞定 `dxil.dll`。** 作者"不对签名机制做进一步评论"，但 `mach-dxcompiler` 的最终产物里 `dxil.dll` 不再是任何形式的依赖——在 macOS 上用 mach-dxcompiler 编出来的 DXIL bytecode，和 Windows 上官方 DXC 跑出来的 byte-for-byte 等价，在标准 Windows 机器上也能跑。

## 产出的跨平台矩阵

CI 出预编译二进制，覆盖：

- macOS：Apple Silicon (aarch64) + Intel (x86_64)——**史上第一次**
- Linux：glibc + musl，x86_64 + aarch64——aarch64 史上第一次
- Windows：x86_64 + aarch64，含 MinGW/GNU ABI（可能也是史上第一次）

Zig 用户直接 `zig build -Dfrom_source -Dtarget=...` 就能自己交叉编译。库还暴露了小的 C API 和 Zig API，替代微软那个古董 COM 接口。

## 代价与局限

作者自己列的警告：不支持 SPIR-V 输出（Mach 用不到）；SM6.7/6.8 不打算跟；Windows MSVC ABI 的二进制当前构建失败（C binding 的小 bug）；musl Linux 没测过；llvm-tablegen 出来的 generated header 一部分暂时仍来自旧 CMake 流程。并且：只有一个人维护，仓库存在就是为了解决 Mach 自己的问题。

## 启示

这件事让一个老问题的成本重新可算：只要愿意用 `build.zig` 把一个历史悠久的 C++ 项目的构建系统整个替换——而不是"我来修几个 CMakeLists.txt 让它更 portable"——往往比修原 CMake 更便宜、产出的跨平台支持还更广。Zig 的 `zig cc` 工具链直接负责所有 cross-compile 细节，这一点在 2024 年是现代 C/C++ 项目交叉编译里独一份的生产力工具。

## 相关

- [[dxc-dxil-signing]]
- [[sysgpu-webgpu-successor]]
- [[mach-engine]]
- [[stephen-gutekanst]]
- [[webgpu-intro]]

## Sources

- [[sources/hexops-dxcompiler-better-than-microsoft]]
