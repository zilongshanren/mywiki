---
tags: [gui, 窗口系统, 桌面, 同步]
date: 2026-04-14
sources: 2
---

# 平滑窗口缩放（Smooth Window Resize）

**"抓住窗口左边拖动，看右边是否稳定"**——[[raph-linus]] 把这个几秒钟的动作提炼为一项对桌面 GUI 工具包的基础体检。看似微不足道，却是极少数工具包能做到完美的事：它同时踩到 swapchain 呈现模型、窗口管理器协议、事件循环线程模型、布局/绘制时序四个独立的坑。

## 为什么会抖

窗口缩放同时触发两条级联：窗口管理器更新**窗口帧**（标题栏、边框的位置与尺寸），应用更新**窗口内容**（用新尺寸重新布局并绘制）。内容这一侧走的是 3D 图形管线——命令提交给 GPU 之后并不会马上上屏，而是等 swapchain 的"present"时机。稳定窗口下这点异步没人看得见，反而让 CPU / GPU 能并行。一旦窗口帧正在被实时拖动，边框立刻到位而内容晚一两帧，右边缘肉眼可见地抖动。iTerm2 在 resize 时干脆切到软件渲染绕开这个问题。

## macOS 的药方：presentsWithTransaction

Tristan Hume 2019 年总结的配方是：用 `CAMetalLayer` 而不是 `MTKView`，并设 `presentsWithTransaction = YES`。这会让当前帧的 present 被并入 CoreAnimation 的事务提交里，与窗口帧的尺寸变更同一个 commit 点翻转——从用户角度看，边框和内容是"同一帧"就位的。

## Windows 的药方：flip model vs redirection buffer

Windows 的新 flip model 是高性能路径（让 DWM 直接拿到 app 的 swapchain 表面、支持 wait object 做 latency 优化），代价是内容与窗口绘制**去同步化**。旧的 `DXGI_SWAP_EFFECT_SEQUENTIAL` 与 D2D `HwndRenderTarget` 走"redirection buffer"——先把整个窗口内容拷进一块由 DWM 管理的缓冲区，天然与窗口帧同步，所以不抖。

Raph 在 xi-win 里给出的可行配方是**双模式切换**：稳定状态跑 flip model 拿性能，收到 `WM_ENTERSIZEMOVE` 时临时切回 redirection buffer 路径，收到 `WM_EXITSIZEMOVE` 时再切回来。Direct3D 上类似地可以用 sequential 呈现模式代替 flip。

[[raph-linus]] 2018 年在 xi-win 遇到这个问题时做过系统性的尝试并把三条路都走了一遍。**HWND render target** 走老的 redirection buffer 路径——resize 时最平滑，但无法指定 GPU，在 Optimus 混合显卡 + 外接显示器上会出现对角线撕裂。**DXGI_SWAP_EFFECT_SEQUENTIAL** 的好处是可以编程选择 adapter（优先独显），resize 的同步行为和 HWND 接近，代价是 incremental present 退化成全表面拷贝——指定 dirty rect 似乎被忽略。**Flip swap effect** 是官方推荐的「最先进」路径，但它的 present 时机和 WM_SIZE 派发完全没有同步点；他实验出来的近似配方是 Present(SyncInterval=0) 后紧接 DwmFlush，让下一帧对齐到 vsync 之后一点——在高性能组合（独显 + 外接）能工作，在弱组合（集成显卡 + 笔记本屏）失败。他为这个问题开出 2500 美元的悬赏 PR，并坦承愿意为一个令人信服的「做不到」证明付一半赏金。

## 事件循环的同步性

resize 要平滑还要求 event loop 能**同步**派发"draw me at this new size"事件，让应用绘制完这一帧再返回给系统。winit 1.0 为了简化编程模型，把 event loop 放一个线程、app 逻辑放另一个线程，中间靠 channel 通信——对"游戏式管线"是简化，对平滑 resize 却是灾难：没有办法让 app 线程在这次事件里完成绘制。winit 2.0 "event loop 2.0" 在 Windows 上取消了额外线程、允许同步事件，才迈出第一步。Raph 正是因为这个问题才在 [[reactive-ui-rust|Druid]] 里自己写 window creation，不依赖 winit。

## 布局与绘制必须分阶段

immediate mode GUI（如 dear imgui）常用的"layout 和 draw 在同一次调用里完成"做法，实践中往往会借用上一帧的 layout 结果来简化——结果就是**布局比实际尺寸晚一帧**。在窗口平稳时这一帧延迟没人在意，resize 时就是肉眼可见的抖动。正确的做法是：任何一帧的绘制之前，必须先完成一次独立的 layout pass 确定本帧每个 widget 的尺寸与位置，然后再绘制。

## 为什么值得当体检项

没有专门仪器也能复现，拖一下就看见。而它触发的几乎是整条 GUI 栈上最容易被架构师忽略的同步边界：swapchain present 的时机、WM 消息的派发模型、事件循环的线程模型、layout/draw 的分阶段。通不过这个测试，往往意味着架构层某个地方用了"大部分时间够好"的 shortcut。

## 相关

- [[rust-gui-ecosystem]]
- [[reactive-ui-rust]]
- [[raph-linus]]

## Sources

- [[sources/raphlinus-smooth-resize-test]]
- [[sources/raphlinus-smooth-resize-direct2d]]
