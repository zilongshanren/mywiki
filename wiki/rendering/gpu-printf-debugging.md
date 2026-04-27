---
tags: [渲染, 调试, gpu]
date: 2026-04-14
sources: 1
---

# GPU printf 调试（UAV append buffer 路径）

GPU shader 的「printf 式调试」是图形开发里长期缺失的工具。CPU 程序员可以随手 `printf` 看变量；GPU 程序员通常要么改 shader 把变量编码成颜色写到屏幕，要么挂上 [RenderDoc](https://renderdoc.org/) 这类外部抓帧工具。在迭代密集的 compute shader 上，外部工具的启动开销和「重抓一帧」周期都显得太重。

## 用 UAV append buffer 实现的 printf

DirectX 11 起的 `RWStructuredBuffer` 和 append/consume buffer 提供了一条 hack 路径：

1. CPU 端创建一个固定大小的 `AppendStructuredBuffer<DebugRecord>`（例如 1024 条记录）
2. shader 里在感兴趣的位置 `buf.Append(record)` 写入
3. 帧末把 buffer 拷回 CPU 侧打印，或者作为下一帧的 debug overlay 显示

这套思路不是新的——[c0de517e 早在 2013 年就写过 DX11 GPU printf](http://c0de517e.blogspot.ca/2013/07/dx11-gpu-printf.html)。[[bartosz-wronski|Bart Wronski]] 在 CSharpRenderer 框架里把它做成了「无需写额外代码」的小工具。

## 过滤宏的设计

直接让所有线程都 append 会瞬间溢出 buffer。Wronski 的做法是定义两种过滤宏：

```hlsl
// pixel shader：按屏幕坐标过滤
if (DEBUG_FILTER_VPOS(i.position, 100, 100)) {
    DebugInfo(i.position.xyz, lighting);
}

// compute shader：按 dispatch thread ID 过滤
if (DEBUG_FILTER_TID(dispatchThreadID, 10, 10, 10)) {
    DebugInfo(dispatchThreadID, finalOutValue);
}
```

只有目标像素 / 线程会真正写 buffer。配套的 `DEBUG_FILTER_CHECK_FORCE_*` 宏允许在 UI 里覆盖目标坐标，不需要重编 shader——甚至可以**在 viewport 上点一下，自动用点击位置作为过滤坐标**，对追 NaN 和负值非常实用。

## 与 surface debug snapshots 的关系

UAV printf 适合「把单个/少数像素的具体数值挖出来」。对「想看整张 SSAO buffer」这类需求，更合适的是另一条路径——**surface debug snapshots**：在渲染流程中显式注册某个临时 RT 的快照，框架在 UI 选中时把它复制到一个 debug buffer，避免被后续 pass 覆盖。两者是互补的工具。

```csharp
SurfaceDebugManager.RegisterDebug(context, "SSAOMain", ssaoCurrent);
// SSAO H blur 后
SurfaceDebugManager.RegisterDebug(context, "SSAOBlurH", tempBlurBuffer);
```

## 设计视角

UAV printf 是个典型的「小接口、大功能」的 [[deep-modules|深模块]]：调用者只需写一个 if + Append，下层处理 buffer 管理、回读、UI 集成。它把「我要看这个值」这个心智极轻的需求和它实际涉及的 GPU/CPU 数据流隔离开来。

## 相关
- [[debug-visualization]]
- [[bartosz-wronski]]
- [[register-spilling-avoidance]] — shader 性能悬崖的另一常见来源
- [[polynomial-root-finding-gpu]] — 典型的「溢出杀死性能」案例
- [[sources/supnik-debugging-glsl]] — 2010 年 Ben Supnik 的前 UAV 时代 GLSL printf（写 `gl_FragColor` + shader 热重载）

## Sources

- [[sources/bartwronski-csharprenderer-debug]]
- [[sources/c0de517e-dx11-gpu-printf]]
