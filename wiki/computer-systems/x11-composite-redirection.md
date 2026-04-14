---
tags: [x11, 图形栈, 窗口系统, compositing, linux]
date: 2026-04-14
sources: 1
---

# X11 Composite、Redirection 与 TFP

现代 Linux 桌面上那些"窗口半透明、缩放、3D 切换"效果背后的底座，是 X11 的 **COMPOSITE 扩展** 加上 **Texture from Pixmap**。但要理解它们为什么长这样，需要先回到 80 年代 X11 初生时的"Expose 模型"。

## Expose 模型：窗口是"丢失的"

当年内存很贵，X server 无法为每个窗口都保留完整像素内容。X11 的解决方案是：**窗口是 lossy 的**。当用户把一个窗口从另一个窗口上方拖走、露出了一块原本被遮挡的区域，X server 会给被遮挡的程序发一个 `ExposeEvent`，程序自己负责重画那一块。这就是为什么 Windows 或 Linux 上崩溃或卡死的程序在被拖动的其他窗口"擦过"之后会留下一片灰色残影——程序没法响应 Expose，那块像素就永远空在那里。Windows 桌面本身也是一个普通程序，它卡住时你能在整个屏幕上"擦出条纹"，这是这个模型最戏剧化的后果。

## Redirection：让窗口变 lossless

内存便宜之后，现代 X server 可以为每个窗口分配一张专属的 pixmap、让窗口绘制不落到 front buffer，而是落到这张后端 pixmap 上——这叫 **redirection**。被 redirect 之后，窗口在屏幕上其实是"看不见"的，必须靠 compositor 把所有 pixmap 合成到屏幕上才能看到。

## COMPOSITE 扩展与 COW

让这件事成为可能的是 [COMPOSITE 扩展](http://www.x.org/releases/X11R7.7/doc/compositeproto/compositeproto.txt)。它提供两件东西：第一，控制"哪些窗口被 redirect"；第二，一块叫 **Composite Overlay Window (COW)** 的特殊大窗口，compositor 独占，用来做最终合成输出。COW 永远是整个屏幕大小、不能被 redirect、在 X 的窗口列表里不可见——它是 X server 特意给 compositor 留的一个后门。

## Texture from Pixmap (TFP)

compositor 要想用 OpenGL 把窗口 pixmap 合成到 COW 上，必须能把 pixmap 当成 GL 纹理用。X 的 GL 扩展 **TFP**（Texture from Pixmap）做的就是这件事：给 GL 程序一个 "X Pixmap == GL Texture" 的零拷贝视图。Compiz、GNOME Shell、mutter 等现代 compositor 都以 TFP 为基础把每个窗口纹理贴到一个 actor 上，然后用 GL 矩阵把它画回 COW。

这是"合成"的物理含义——你在屏幕上看到的每个窗口都是一个**贴图**，点击事件其实是点在 actor 后面的真 X11 窗口上。把 actor 缩到一半，你会惊讶地发现点击位置和窗口显示位置对不上了：在 GNOME Shell 的 Looking Glass 里跑 `global.get_window_actors().forEach(function(w) { w.scale_x = w.scale_y = 0.5; })` 就能亲手触发这个错位。

## AIGLX 的历史位置

在开源栈还没有内核级 GEM/TTM buffer 管理的年代，每次把窗口 pixmap 拿给 GL 硬件用都要拷贝一次。为避开这个拷贝，早期走的是 **AIGLX**（Accelerated Indirect GLX）——把 OpenGL 放在 CPU 上跑，省掉进 GPU 的那次拷贝。Compiz 时代就用它。DRI2 和现代 TFP 成熟后 AIGLX 就退休了。

## Unredirection：全屏游戏的直通车

每帧把所有窗口 pixmap 采样一遍并不免费。所以绝大多数 compositor 都会对"盖满整个屏幕"的窗口做 **unredirection**——临时关掉它的 redirection，让它像 90 年代那样直接画 front buffer，跳过合成路径。这是全屏游戏能跑 60 FPS 的关键：看起来像个历史残留的 fallback，其实是现代渲染路径的性能逃生口。

## 与 [[wayland-compositor-model]] 的对比

Wayland 把 display server 与 compositor 合并后，这一整套"让 X server 保留窗口状态、compositor 再去 X server 拉 pixmap"的 dance 就不需要了：compositor 自己就是 server，client 直接把 buffer 交给 compositor，compositor 想怎么画怎么画，也不会再出现"actor 位置和 X server 认为的窗口位置不同步"这种 illusion。

## 相关

- [[linux-graphics-stack-dri]]
- [[wayland-compositor-model]]
- [[x11-pointer-barrier]]
- [[jasper-st-pierre]]

## Sources

- [[sources/jasper-linux-graphics-stack]]
