---
tags: [source, html5, webgl, browser-games, web-apis, playcanvas]
date: 2026-04-14
sources: 1
---

# HTML5 APIs for game developers（Dave Evans / PlayCanvas Blog）

PlayCanvas 工程师 Dave Evans 于 2012 年 8 月在官方博客维护的一份清单，按渲染 / 音频 / 输入 / 网络 / 存储五类列出游戏开发者关心的 HTML5 API 及其各浏览器支持状态。

## 摘要

这是一篇实用主义的「浏览器游戏 API 可用性表格」，出发点是：PlayCanvas 刚用 HTML5 技术栈做完多人 3D FPS demo「D.E.M.O.」，需要帮读者理清「要做一个 3D 浏览器游戏到底依赖哪些 API、哪些浏览器已经支持、哪些还差着」。清单覆盖 Canvas 2D、WebGL、Fullscreen、Web Audio、PointerLock、Gamepad、DeviceOrientation、getUserMedia、WebSocket、WebRTC、Web Storage、Offline Storage 共十余项。每一项都是「Chrome / Firefox / Safari / Opera / IE」五列的支持矩阵。2012 年的结论是：WebGL 和 WebSocket 已经普及，Web Audio 才刚刚落地 Chrome / Safari，而做 FPS 必备的 PointerLock 基本只有 Chrome 能用。文章本身没有架构深度，但它是理解「2012 年为什么浏览器里做游戏这么难」的一张关键地图——做一个能跑的 3D 多人 FPS 要把五六个 early-stage 的 Web API 全部凑齐，任何一个缺位都要降级。Evans 把 Web Storage 戏称为「Cookie done right」，也顺手记下 IE 对 WebGL 当时完全没有支持这一重要事实。

## 关键要点

- 浏览器游戏不是一个 API，而是一套拼图：渲染（[[rendering-pipeline]]）+ 音频 + 输入 + 网络 + 沉浸
- 2012 年 WebGL / WebSocket 已经跨浏览器可用，Web Audio 在 Chrome / Safari 落地
- FPS 必备的 PointerLock 当时只有 Chrome 能用，且需要 `chrome://flags` 开关
- Gamepad API 仅 Chrome 默认开，Firefox 在开发分支；手柄游戏移植面临兼容性鸿沟
- 键盘输入的物理键位标准（后来的 `KeyboardEvent.code`）在 2012 年还只是提案
- 清单按「渲染 / 音频 / 输入 / 网络 / 存储」五类组织，是后来很多 Web 游戏引擎开发者的参考模板

## 链接到的概念

- [[html5-game-apis-2012]]
- [[performance-conscious-webgl]]
- [[rendering-pipeline]]

## 原文

- 链接：https://blog.playcanvas.com/html5-apis-for-game-developers
- 本地：`raw/articles/blog.playcanvas.com/2012-08-19_html5-apis-for-game-developers-playcanvas-blog.md`
