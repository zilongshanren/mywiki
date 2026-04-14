---
tags: [linux, 图形栈, 系统, 内核, mesa]
date: 2026-04-14
sources: 2
---

# Linux 图形栈：DRI / DRM / KMS

Linux 的 GPU 栈从 Mesa 到内核的这一段，在命名上是一团糨糊："DRI" 这三个字母被反复复用到完全不同的层次上，新人看文档经常误把一件事当成三件事（或者把三件事误当成一件事）。Jasper St. Pierre 在 2016 年的 [["DRI" 一文|jasper-dri-linux-graphics-stack]] 里一次把这些名字拆开讲清楚，本页做一份中文索引。

## 五个缩写的各自含义

| 名字 | 层次 | 性质 | 含义 |
|---|---|---|---|
| **DRI**（项目名） | 元 | 项目代号 | Direct Rendering Infrastructure——把 Mesa、Xorg、内核粘起来让 Linux 能硬件 3D 的开源工程 |
| **DRM**（内核） | 内核子系统 | ioctl API | Direct Rendering Manager，Linux 内核里的 GPU 控制子系统，路径在 `drivers/gpu/drm/` |
| **DRI driver model**（Mesa 内） | 用户态 | C 内部 API | Mesa OpenGL 实现内部的驱动抽象模型，有 DRI1/DRI2 两代，产物是 `/usr/lib/dri/i915_dri.so` 这种 `.so` |
| **DRI X extension**（X 协议） | X 协议 | 网络协议扩展 | Xorg 的协议扩展，三代：DRI1 / DRI2 / DRI3，用于让 Mesa 把 buffer 交给 X server 上屏 |
| **KMS / DRM mode**（内核） | 内核子系统 | ioctl API | Kernel Mode Setting，DRM 子系统里独立的另一套 API，专门控显示控制器（CRTC / connector / 分辨率 / HDMI） |

**`/dev/dri/card0` 里的 "dri" 是 DRM 子系统**——设备节点沿用项目名是历史遗留，无法改。**Mesa 的 `i915_dri.so` 里的 "dri" 是 driver model**——与内核无关，只是 Mesa 内部 C ABI 命名。

## 同一份代码里两个 DRI 可以共存

Mesa 里有一份 [`loader_dri3_helper.c`](http://cgit.freedesktop.org/mesa/mesa/tree/src/loader/loader_dri3_helper.c)：它是 **DRI2 driver model** 的 helper 代码，用来帮驱动处理 **DRI3 X 协议扩展**。一个文件里的 DRI2 和 DRI3 分别指 Mesa 内部 ABI 的版本和 X 协议的版本，**与彼此无关**，单看数字只会更困惑。

## libdrm：DRM 的用户态包装

[libdrm](http://cgit.freedesktop.org/mesa/drm/) 是用户态库，包装内核 DRM ioctl，让 Mesa 和 X server 共享同一份 buffer 管理代码。大部分 libdrm 代码是薄包装，但也有重型组件，例如 Intel 的 [`intel_bufmgr_gem`](http://cgit.freedesktop.org/mesa/drm/tree/intel/intel_bufmgr_gem.c) 负责 GEM buffer 的 userspace 分配追踪。

## wl_drm：Wayland 的内部重蹈覆辙

Mesa 为了让 Wayland 的 client 和 compositor 之间能交换纹理 buffer，又造了一套私有协议 [`wl_drm`](http://cgit.freedesktop.org/mesa/mesa/tree/src/egl/wayland/wayland-drm/wayland-drm.xml)——Jasper 吐槽它和 DRI3 几乎一模一样。这也是"命名没收敛、同一件事被反复发明"的活例证。

## 为什么大部分 GPU 驱动在用户态

Linux 的图形驱动是**内核态 + 用户态**两半拼出来的：

- **内核态**：处理 command submission、DMA、中断、内存固定——只有它能触碰硬件寄存器。例如 `drivers/gpu/drm/radeon`。
- **用户态**：处理 GLSL→TGSI→机器码编译、state tracking、buffer 管理——跑在 Mesa 里。例如 `r600_dri.so`。

这么切的理由：

1. **安全**：GLSL 编译器是几十万行的大型 C++，不能塞进 kernel。
2. **崩溃隔离**：用户态驱动崩溃只 crash 一个应用，不 panic 内核。
3. **升级灵活**：换驱动不必重启；甚至 `LD_LIBRARY_PATH` 切换就能跑两套版本做 A/B 测试。
4. **调试方便**：崩栈落在用户态，gdb/asan 直接上。

## Gallium3D 与 Intel 的分岔

Mesa 里有一套叫 **Gallium3D** 的驱动 building block 框架，AMD/Nouveau/软件栈等都在用它构建驱动。Intel 选了不走 Gallium，继续走自己的"纯硬编码"驱动栈——理由是 Intel 有足够投入的驱动团队，Gallium 抽象层带来一定性能损耗，对他们是负收益。这给"是否使用通用框架"留下了一个真实世界的反例：不是所有团队都应走框架路线。

## KMS node / render node 的拆分

历史上 DRM 同时承载渲染和显示两套责任，`/dev/dri/card0` 既能跑 GL 又能 modeset。工作正在进行中，把 render 和 KMS 拆成两个不同的设备节点——这样 Wayland compositor 只需要 KMS 权限，而 GL 应用只需要 render 权限，权限最小化更干净。

## 相关

- [[jasper-st-pierre]] —— Linux 图形栈/窗口系统长期贡献者
- [[gpu-hazard-tracking]] —— 用户态 Mesa 驱动本地的状态追踪工作
- [[rendering-api-depth]] —— 驱动 = 典型深模块
- [[x11-composite-redirection]] —— Expose 模型、COMPOSITE 扩展、TFP 与 unredirection
- [[wayland-compositor-model]] —— Wayland 为何把 display server 与 compositor 合并

## Sources

- [[sources/jasper-dri-linux-graphics-stack]]
- [[sources/jasper-linux-graphics-stack]]
