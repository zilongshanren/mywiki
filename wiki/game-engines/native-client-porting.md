---
tags: [跨平台移植, 沙箱, 浏览器, opengl-es, 历史]
date: 2026-04-19
sources: 1
---

# Native Client 移植笔记（archival）

[[branimir-karadzic]] 在 2012 年记录了把《AirMech》移植到 Google Native Client（NaCl）的过程。Native Client 作为浏览器技术本身已被历史淘汰——这一页不是在推荐它，而是保存一份"把原生 C++ 游戏搬进沙箱浏览器"时会遇到的工程模式，这些模式后来在 Emscripten / WebAssembly 上几乎一比一复现。

## 工具链：先把 GCC 准备好

在 Windows 上用 MinGW 先把 GCC 这一路跑通，是一切非 MS 平台移植的基础——Premake 让加一条 GCC "flavor" 变得便宜。真正的障碍不是编译器，而是**依赖**：闭源的物理库没有 NaCl 版本，于是必须先切到开源实现（见 [[middleware-vs-open-source]]）。之后的移植基本就是 `#ifdef` 化 Windows 特有代码。

意外之处：NaCl 允许写汇编、允许 SSE intrinsics（`-msseX`）——它对原生代码的限制远比想象中少。

## 沙箱带来的抽象

NaCl 模块受和普通网页一样的限制：不能直接访问文件系统、没有传统 `main`（入口是 Pepper API 的回调）。作者的应对是：

- **文件访问抽象为内存文件**——反正游戏本来就用 pack 文件；HTTP 拉下来放到内存里，对上层透明。
- **用 `pthread_create` 在主线程回调里起一个线程跑 `main`**——主线程必须让出给 Pepper，游戏循环不能阻塞它。
- **日志/网络 journaling 这种"要直写磁盘"的用例** 用 WebSocket 把数据发到一个边车服务器处理。

这一套"用间接层把原生游戏塞进沙箱"的模式，和 Emscripten 的虚拟文件系统、主循环回调（`emscripten_set_main_loop`）结构几乎完全一致。

## 渲染：D3D → OpenGL ES 2.0

这是整个移植里最有长期价值的决定。AirMech 原本是 D3D 渲染器，要走浏览器就必须出一条 OpenGL ES 2.0 通路——而 GLES2 与 WebGL 1 是同一个子集。作者评价 GLES2 是"**OpenGL Lite**"：扔掉了桌面 OpenGL 多年积累的 extension 混乱，是 OpenGL 的"一次 fresh start"。

几条工程观察：

- **额外 2–3 帧延迟**——NaCl 的 GPU 调用跨进程通过 RPC 传递，任何依赖 GPU 结果的同步调用（`glFinish`、`glGetError`）都会让游戏阻塞。这也是为什么他们禁用了游戏内鼠标渲染——twitch 类游戏基本不适合 NaCl。
- **跨平台 shader bug**——他们在 Mac 上命中一个 `mat4 → mat2` 强转的 fragment shader bug，Linux/Windows 下都正常。这类"只在一个平台出现"的坑正是统一渲染抽象层（后来的 bgfx）要解决的问题。
- **Chrome 的 GPU 黑名单**——玩家若自行"un-blacklist"，渲染随时会崩。这种"驱动+浏览器+平台"三轴差异是后来 WebGPU 想彻底治掉的。

结果是团队最终同时维护 D3D9 和 GLES2 两套后端，两者覆盖了从手机到当代主机的大部分硬件——这种多后端抽象正是 **bgfx** 的原型思路。

## 网络：走 WebSocket 的代价

NaCl 早期不直接支持 socket，只能通过 JavaScript 桥接 WebSocket，而 JS 桥要求 UTF-8 字符串——于是二进制流被强制 Base64 编码（24 bits → 32 bits，约 +33% 带宽开销）。他们的做法是把 `socket/connect/send/recv` 等 BSD socket 调用 shim 成对 JS 桥接调用，对上层业务透明。作者预言 PPAPI 会很快直接支持 WebSocket——这套 shim 是过渡期的创可贴。

后端用 Go 写，加一个 WebSocket handler 加一段 Base64 编解码大概 10 行代码——这是语言层面"把网络当一等公民"的胜利之一。

## 经验教训的可迁移性

这篇文章的长期价值不在 NaCl——在于它示范了"**把一个 AAA 规模的原生游戏搬进浏览器**"涉及的全部维度：

1. 工具链（换编译器）；
2. 依赖（切开源）；
3. 文件 / 入口（抽象成沙箱友好的形态）；
4. 渲染（加一条 GLES2 / WebGL 后端）；
5. 网络（桥接或重写）；
6. 调试（`printf` 永远是最可靠的跨平台调试器）。

Emscripten / WebAssembly 时代上述每一项都有对应的现代解法，但拆解方式是同一套。

## Sources

- [[sources/bkaradzic-airmech-native-client]]
