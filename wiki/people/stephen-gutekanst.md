---
tags: [人物, 作者, zig, mach, 游戏引擎]
date: 2026-04-19
sources: 4
---

# Stephen Gutekanst（Emi / emidoots / Hexops）

Zig 社区独立开发者，[[mach-engine|Mach 游戏引擎]] 与图形工具链的作者、`Hexops` 组织维护者。早期以 "Stephen Gutekanst" 署名，近年以 Emi（GitHub handle `emidoots`）为主要身份。白天做一份正常的技术工作，晚上业余建设 Mach，目标是有朝一日能靠做 Mach 和高质量游戏为生。

主张 "software you can love"——工具应该属于使用者本人，而不是被"开源游戏"裹挟的所谓开源。FOSS 是她个人的根。对大厂仓库里夹带私有 blob（如 DirectX 的 `dxil.dll` 签名器）、对 GitHub 被微软 enshittification 都有明确的批评立场，Mach 与 pkgmirror 均已迁到自托管 Forgejo 实例 `code.hexops.org`。

## 主要工作

- [[mach-engine]] — Zig 写的模块化游戏引擎/图形工具包。
- [[mach-nominated-zig-versions]] — 在 Zig nightly 与 stable 之间提供稳定提名版本的工程实践。
- [[sysgpu-webgpu-successor]] — 用 Zig 从零重写的 WebGPU 原生实现，并朝"WebGPU 继任者"方向演化。
- [[mach-dxcompiler-static-build]] — 用 `build.zig` 把微软 DXC 重写成可静态链接、可跨平台交叉编译的库，并[[dxc-dxil-signing|摆脱 dxil.dll 代码签名 blob]]。
- [[zig-package-mirror]] — `pkgmirror` 自托管 Zig 工具链与包镜像，写在 Zig 里。

## 相关

- [[mach-engine]]
- [[sysgpu-webgpu-successor]]
- [[mach-dxcompiler-static-build]]

## Sources

- [[sources/hexops-mach-nominated-zig]]
- [[sources/hexops-mach-v0-3-released]]
- [[sources/hexops-dxcompiler-better-than-microsoft]]
- [[sources/hexops-pkgmirror]]
