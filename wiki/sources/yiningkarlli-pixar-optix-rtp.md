---
tags: [source, 渲染, optix, interactive-ray-tracing, pixar]
date: 2026-04-19
sources: 1
---

# Pixar OptiX Lighting Preview Demo（Yining Karl Li / Code & Visuals）

[[yining-karl-li]] 2013 年 7 月在 Pixar Research Group 做暑期实习期间的博客短文，记录他参与的项目——一个基于 NVIDIA OptiX、跑在 GPU 上、直接嵌入 The Foundry Katana 里的实时灯光预览工具——在 SIGGRAPH 2013 NVIDIA 展台公开演示。

## 摘要

短篇幅、以「demo 刚亮相」的心情为主，技术细节很少：项目叫 **RTP（Realtime Preview）**，构建在 OptiX 之上，目标是让灯光师在 Katana 里对 Pixar 产线资产做 GPU 路径追踪的交互式灯光预览。demo 由项目 lead Danny Nahmias 完成，得到积极反响，FXGuide 做了专题 podcast。Yining 把自己定位成「只是实习生」，主要开发者是 Danny Nahmias、Phillip Rideout、Mark Meyer 等人。文章唯一的「技术注脚」是后来的编辑：把 Ustream 播放器换成了 Vimeo，因为 Ustream 嵌入会让某些 Chrome 崩溃。

## 关键要点

- RTP 是 Pixar 早期的 GPU 交互灯光预览探索，直接长在 OptiX 上；这条线索日后在 [[hyperion-renderer]] 的 GPU 交互灯光系统（Moana 2 量产部署）上有呼应，但 RTP 本身属于 Pixar，不属于 Disney Animation。
- 文章把 RTP 明确框定为「在 Katana 里」——即 DCC 内嵌的 GPU 预览，而不是独立 viewer；这与今天 RenderMan XPU、Karma XPU 等产品形态同源。
- 这篇是 [[yining-karl-li]] 毕业前在 Pixar 的实习记录，也是他公开博客里最早的「产线级 GPU ray tracing」接触点，为他之后入职 Disney Animation 做 Hyperion 的故事埋下伏笔。
- 除此之外没有实质技术内容；视频链接早已失效，本地文件保存的是文字壳。

## 链接到的概念

- [[hyperion-renderer]]
- [[yining-karl-li]]

## 原文

- 链接：<https://blog.yiningkarlli.com/2013/07/pixar-optix-lighting-preview-demo.html>
- 本地：`raw/articles/blog.yiningkarlli.com/2013-07-27_pixar-optix-lighting-preview-demo.md`
