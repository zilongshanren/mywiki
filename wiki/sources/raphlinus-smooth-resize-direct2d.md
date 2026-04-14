---
tags: [source, gui, windows, direct2d, swapchain]
date: 2026-04-14
sources: 1
---

# Smooth resize in Direct2D（Raph Levien 2018）

[[raph-linus]] 2018 年 4 月为 xi-win 前端发的一篇"悬赏征解"——他开出 2500 美元，请任何人提交一个能让 Direct2D 窗口在 resize 时不抖、不撕裂、60fps 的 xi-win PR。这篇文章是这项悬赏的问题描述 + 他自己已经尝试过的所有失败路径的技术分析。几年后他的"smooth resize test"成为一整个 GUI 工具包体检框架，就是从这里出发。

## 摘要

Raph 在 Gigabyte Aero 14（内置 HD 630 + 独显 GTX 1060）+ 外接 4K 显示器的典型多显示器配置下，尝试了三条 Direct2D 窗口呈现路径：**HWND render target**（老 API，resize 最平滑但不支持指定 GPU、在 Optimus 混合显卡上出现对角线撕裂）、**DXGI_SWAP_EFFECT_SEQUENTIAL**（能手动选 GPU 并表现良好，但 incremental present 退化成全表面拷贝）、**Flip swap effect**（新推荐路径，原则上最高性能，但内容翻转和窗口帧尺寸变更没有同步点，拖拽时内容比边框晚一两帧到达）。三条路都只在"显卡 + 显示器匹配 + 渲染开销足够小"的窄缝里接近可用，没有一条通吃所有硬件。他给出的验收标准非常具体：perftest 例子里的旋转动画必须稳定 60fps、拖动窗口左边缘时右上角的对角线要和窗口角稳定贴合——后者就是他后来反复引用的"抓住左边看右边"测试。文章最后也坦承："有可能这件事根本不可能做到"，他愿意为一个令人信服的不可能性证明付一半赏金。

## 关键要点

- **Flip model 的根本矛盾**：swapchain 的 flip 时机和 WM_SIZE 派发是两条独立时间线，操作系统没有提供 primitive 让它们在同一帧完成
- **HWND render target 意外地最平滑**，因为它走老的 redirection buffer 模型——DWM 把整个窗口内容拷进中间缓冲区，天然和窗口帧同步
- **Incremental present 在 SEQUENTIAL swap 下不工作**——似乎总是拷贝整个表面，dirty rectangle 参数被忽略
- **Optimus 对角撕裂**是独立显卡在独立显示器 → 集成显卡 → 主显示器路径上的物理伪影，不是 swapchain 配置能修
- **给 flip model 加 DwmFlush**：PRESENT 之后立刻 DwmFlush 让下一帧对齐到 vsync 之后一点点，在高性能组合（1060 + 外接）能凑出 60fps，但在弱组合（HD 630 + 笔记本屏）失败

## 链接到的概念

- [[smooth-window-resize]] — 这篇悬赏问题是 smooth resize test 的起源（本源文件补充了 Direct2D 侧的 HWND vs Flip vs Sequential 三路径对比细节）
- [[raph-linus]]

## 原文

- 链接：https://raphlinus.github.io/personal/2018/04/08/smooth-resize.html
- 本地：`raw/articles/raphlinus.github.io/2018-04-08_smooth-resize-in-direct2d.md`
