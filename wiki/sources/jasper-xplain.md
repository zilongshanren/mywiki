---
tags: [source, x11, 图形栈, 交互式教学]
date: 2026-04-14
sources: 1
---

# "Xplain"（Jasper St. Pierre）

[[jasper-st-pierre]] 2013 年 12 月发表于 blog.mecheye.net 的 meta 公告贴，宣布"Xplain"系列——一份用**交互式 Web 演示**讲 X11 的深度科普站正式上线。本篇本身不是技术文，而是项目启动说明；Xplain 的主体内容托管在 <http://magcius.github.io/xplain/article/>。

## 摘要

Jasper 在 [[sources/jasper-linux-graphics-stack|"The Linux Graphics Stack"]]（2012）之后一直想做一份"X11 深度 followup"，但材料太多、他 burn out 了好几次。2013 年末他决定把已经写出来的内容先发出去——再不发"去年写过一篇 Linux Graphics Stack"这句话就要过期了。Xplain 不是博客文，而是一系列独立托管的文章，重点特性是**每篇都带可交互的 JavaScript 演示**：比如让读者真的能在浏览器里用一个 mock Xlib 去拖动窗口、触发 Expose 事件、观察重绘。这个形式决定了它不能做成博客连载——需要更强的排版与代码嵌入控制，于是托管在 GitHub Pages。

发布时第一篇只写了"非常基础的窗口行为"，计划覆盖的主题清单是：window tree、WM 工作原理、COMPOSITE 扩展、RENDER 扩展、焦点管理、输入 grab、selections（clipboard/drag-and-drop 的协议基石）——整个 X11 生态的**结构性**视角。Jasper 自己的定位是：为那些想真正理解 X11 为什么这样设计的人写，而不是"怎么写 X client"的 how-to。

## 关键要点

- **Xplain 是配套项目，不是博客**：独立托管在 `magcius.github.io/xplain`，每篇带可交互 JS 演示（mock Xlib + real DOM）。
- **定位**：面向"想懂 X11 设计意图"的读者，而不是想写 X client 的工程师。
- **计划覆盖主题**：window tree、WM、COMPOSITE、RENDER、focus management、input grabs、selections——基本把 X 协议的结构性关键点都列了。
- **写作形态**：交互式演示（`demo-common.js`）意味着这个系列的表达力强于纯文字博客，也解释了为什么这篇 2013 年的发布公告至今仍被作为 X11 学习的入口指向。
- **持续性风险**：作者自己也承认 burn out 过数次，系列节奏预计"每月一篇"——这是一个由单人维护、交互演示成本高、容易停滞的项目；读者价值和维护负担并不匹配。
- **与 [[sources/jasper-linux-graphics-stack|"The Linux Graphics Stack"]] 的关系**：Xplain 是那篇栈概览的 deep dive 续作，但单独挑了 X11 一块、用"交互式演示"这一新表达媒介重写。

## 链接到的概念

- [[x11-composite-redirection]]
- [[wayland-compositor-model]]
- [[jasper-st-pierre]]

## 原文

- 链接：<https://blog.mecheye.net/2013/12/xplain/>（发布公告）
- 项目：<http://magcius.github.io/xplain/article/>
- 本地：`raw/articles/blog.mecheye.net/2013-12-28_xplain.md`
