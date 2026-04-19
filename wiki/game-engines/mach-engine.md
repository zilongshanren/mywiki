---
tags: [游戏引擎, zig, mach, 模块化, 图形工具包]
date: 2026-04-19
sources: 2
---

# Mach 引擎

Mach 是 [[stephen-gutekanst]] 用 Zig 开发的游戏引擎与图形工具包，目标是做一个真正属于使用者、模块可拆的现代引擎——引擎本身被视为"一套游戏开发的标准库模块"，你可以只用其中任何一部分。它区别于 Unity/Unreal 那种大一统单体的设计：Mach 把自己切成 `mach-core`（窗口、输入、跨平台图形 API）、`mach-sysaudio`（底层音频 I/O）、`mach-sysgpu`（见 [[sysgpu-webgpu-successor]]）、`mach.math`、`mach.gfx.Sprite`、ECS 等十几个互相独立的包。

## core 的定位

`mach-core` 自己的卖点就是 **SDL + OpenGL / GLFW + Vulkan 的现代替代**——只提供窗口、输入和真正跨平台的图形 API。v0.3 时期暂时还靠 GLFW 做桌面后端、用 WebGPU 做图形层，但 Hexops 在推动用 Zig 从零重写这两块，摆脱 C 依赖。`libmach` 则对 core 和引擎层提供 C API，让非 Zig 用户也能接入。

## 模块化的一条实例链

Mach 的"引擎是一套模块"的主张在 v0.3 有了可见化的例子：

- [[ecs-abstraction-layers|ECS]] 作为跨模块耦合的骨架，负责查询/实体构造；
- `mach.math` 是为 Mach 图形约定（矩阵表示、坐标系）量身定制的数学库，附带 ray-triangle intersect；
- `mach.gfx.Sprite` 用 ECS 把几十万 sprite 每个作为独立 entity 带自己的变换矩阵，在 CPU 侧算完再提交，用来端到端压测渲染管线；
- `mach.gfx.Text` 在做但未可用；
- [[sysgpu-webgpu-successor]] 是图形后端；
- [[sysaudio-zig|sysaudio]] 是音频后端。

## 版本节奏与工具链

Mach 的版本节奏主动绑定在 [[mach-nominated-zig-versions]] 上：每年 1 月和 7 月是 Mach release，其余偶数月挑 Zig nightly 当月的快照作为"提名版本"，使 Mach 生态的 40+ 个仓库和下游用户有一个共同的 Zig 基准。发到 v0.3（2024-02）时，这条工作流是 Mach 在 Zig 社区里最重要的协调机制之一。

## 工具链副产品

因为 Mach 自己的 `sysgpu` 需要向 D3D12 发送 shader，Stephen 不得不把微软的 [[dxc-dxil-signing|DirectX Shader Compiler]] 从 10.5k 行的 CMake 屎山重写成 ~1k 行的 `build.zig`，结果副产出了 [[mach-dxcompiler-static-build|mach-dxcompiler]]——一个首次支持 macOS / aarch64 Linux / MinGW 的静态 DXC 分发，全行业意义上的公共基础设施。类似的副产物还有 [[zig-package-mirror|pkgmirror]]，Mach 自己的包镜像服务 `pkg.hexops.org`。

## 相关

- [[stephen-gutekanst]]
- [[sysgpu-webgpu-successor]]
- [[mach-nominated-zig-versions]]
- [[mach-dxcompiler-static-build]]
- [[zig-package-mirror]]

## Sources

- [[sources/hexops-mach-v0-3-released]]
- [[sources/hexops-mach-nominated-zig]]
