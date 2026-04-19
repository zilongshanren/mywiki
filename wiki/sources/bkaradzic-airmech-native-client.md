---
tags: [source, 跨平台移植, native-client, 浏览器, opengl-es]
date: 2026-04-19
sources: 1
---

# Porting AirMech to Native Client（Branimir Karadžić）

[[branimir-karadzic]] 2012 年 1 月为 Carbon Games 博客写的移植笔记，记录把《AirMech》从原生 Windows 游戏移植到 Google Native Client 的全部工程维度。作者自己在文首标注"technology discussed herein is obsolete"——但这篇笔记作为"**把 AAA 规模原生 C++ 游戏搬进浏览器沙箱**"的拆解样本，迁移到 Emscripten / WebAssembly 时代几乎一比一成立。详见 [[native-client-porting]]。

## 摘要

移植从工具链开始：用 MinGW 先在 Windows 上把 GCC 那一路跑通，再切 NaCl SDK；最大的非技术障碍是闭源物理库不支持 NaCl，不得不切换到开源实现（呼应 [[middleware-vs-open-source]]）。沙箱带来的限制用三个抽象应对：文件访问统一走内存文件（反正游戏本就用 pack）、`pthread_create` 在 Pepper 主回调里起线程跑 `main`、网络 journaling 走 WebSocket 边车。渲染层被迫从 D3D9 出一条 OpenGL ES 2.0 通路，作者评价 GLES2 是"OpenGL 的一次 fresh start"，但 NaCl 跨进程 GPU RPC 会带来 2–3 帧额外延迟，因此 twitch 类游戏不适合。网络上因为 JS 桥只能传 UTF-8，二进制流被迫 Base64 编码（+33%），他们用 BSD socket shim 对业务透明。后端用 Go + WebSocket handler，大约 10 行代码完成集成。

## 关键要点

- 移植的"可迁移拆解"：**工具链 / 依赖 / 文件系统 / 入口 / 渲染 / 网络 / 调试** 七件事。
- 沙箱环境中，**`printf` 是最可靠的跨平台调试器**——当 GDB 只是"威慑策略调试器"时尤其如此。
- GPU 跨进程 RPC = 不可避免的延迟；`glFinish` / `glGetError` 在这种环境下是性能杀手。
- 多渲染后端（D3D9 + GLES2）是覆盖手机到主机的现实路径——这个经验直接催生了 **bgfx**。
- 这篇文章间接展示了"NaCl → Emscripten / WebAssembly"的工程思路是同构的，文化价值大于技术价值。

## 链接到的概念

- [[native-client-porting]]
- [[middleware-vs-open-source]]

## 原文

- 链接：https://bkaradzic.github.io/posts/native-client/
- 本地：`raw/articles/bkaradzic.github.io/2012-01-06_porting-airmech-to-native-client.md`
