---
tags: [html5, webgl, browser-games, web-apis, history]
date: 2026-04-14
sources: 1
---

# HTML5 游戏开发 API 地图（2012 年快照）

2012 年前后是浏览器游戏从「Flash/2D canvas」向「硬件加速 3D + 原生级输入音频」过渡的关键节点。彼时的 PlayCanvas 工程师 Dave Evans 在 blog.playcanvas.com 维护了一份「HTML5 API for game developers」清单，按 **渲染 / 音频 / 输入 / 网络 / 存储** 五大块罗列当时游戏开发者最关心的浏览器能力和各家实现进度。这份清单今天读起来是一份有用的时间胶囊：它精确地定义了「做一个能跑在浏览器里的 3D 多人 FPS 到底需要哪些 API 拼起来」。

## 渲染层

- **Canvas 2D** ——所有主流浏览器在 2012 年都已经支持，是早期 HTML5 游戏的唯一渲染出口。
- **WebGL** ——基于 OpenGL ES 2.0 的 3D API，这是整个故事的中心。2012 年 Chrome / Firefox 默认开启，Safari / Opera 需要在开发者菜单里手动启用，IE 完全不支持。PlayCanvas 等引擎正是踩着这个节点把 3D 渲染搬进浏览器的，和 [[performance-conscious-webgl]] 讨论的性能原则一脉相承。
- **Fullscreen API** ——让一个 DOM 元素独占屏幕，是游戏沉浸感的前提。Chrome / Firefox / Safari 已支持，Opera 计划中，IE 没有。

## 音频层

**Web Audio API** 在当时刚刚落地：Chrome / Safari 已支持，Firefox 正在实现（后来跟进），Opera / IE 没有。Web Audio 相较于 `<audio>` 标签的革命性在于提供了低延迟播放 + 效果链（混响、声像、空间音频），这是做动作游戏音效的前提。在 2012 年之前，浏览器游戏音频基本是「播一个 mp3 就不错了」的状态。

## 输入层

这是 2012 年最分裂的一块——几乎每一个 API 都处于「只有 Chrome 能用」的状态：

- **PointerLock** ——捕获鼠标移动而不移动光标，是 FPS 第一人称相机控制的硬需求。只有 Chrome 支持（且需在 `chrome://flags` 打开），Firefox 仅在全屏模式下生效，Safari / Opera / IE 完全没有。
- **Gamepad API** ——硬件手柄输入。Chrome 已支持，Firefox 在开发分支里，其他浏览器没动静。
- **Device Orientation Events** ——从设备加速度计读数据，是移动端倾斜操控的基础。Chrome / Firefox / 移动 Safari 有，桌面 Safari / Opera / IE 没有。
- **getUserMedia / Stream API** ——访问麦克风和摄像头。Chrome / Opera 已支持，Firefox 计划中。
- **键盘** ——当时没有任何标准化方案支持「忽略键盘布局的物理按键」，Mozilla 刚起草了一份提案。这个痛点要等到 `KeyboardEvent.code` 普及之后才真正解决。

## 网络层

- **WebSockets** ——持久双向连接，2012 年是少数在所有浏览器（包括 IE）都已落地的现代 API。PlayCanvas 自己用 Node.js + WebSocket 搭建 D.E.M.O. 多人 FPS 的服务器，是 WebSocket 在游戏领域最早的公开实践之一。
- **WebRTC / PeerConnection** ——对等通信（含音视频聊天）。Chrome 快了但需 flag，Firefox 计划中，其他浏览器尚无踪迹。WebRTC 在多人游戏中真正落地（用 DataChannel 做低延迟游戏协议）要再过好几年。

## 存储层

**Web Storage**（localStorage）和 **Application Cache（离线存储）** 在 2012 年都已经是全浏览器支持。Evans 把 Web Storage 描述为「正确实现的 Cookie」，这是对 Cookie 体积限制和跨请求开销的直白吐槽。离线存储则让「把整个游戏缓存到浏览器里」成为可能。

## 为什么这份清单今天还值得保留

这份 2012 年的清单揭示了几个和今天仍有参照价值的结构性事实：

1. **浏览器游戏是一套 API 拼图，不是一个 API**。要做一个「能跑」的 3D FPS 需要同时依赖渲染（WebGL）、音频（Web Audio）、输入（PointerLock + Gamepad）、网络（WebSocket / WebRTC）、沉浸（Fullscreen），任何一块缺失都要降级。
2. **实现进度极不均匀**。同一年里，WebGL 已经是半标准了，但 PointerLock 还需要 `chrome://flags`——这意味着「2012 年的浏览器 FPS」本质上是只在 Chrome 上能跑的 FPS。Web 游戏开发者必须学会和「某个特性只在某个浏览器的某个版本上可用」的现实共处。
3. **规范跟随实现**。清单里很多 API（PointerLock、Gamepad、Web Audio、WebRTC）当时都是 W3C 或 WHATWG 的 early-stage 草案，浏览器一边实现一边反哺规范。这和 OpenGL / Direct3D 「规范先行」的文化完全不同。

这张表是 [[game-engine]] 和 [[bottleneck-analysis]] 背后的平台前置条件——当 [[gkengine]] / [[gknext-renderer]] 这类原生引擎可以直接调 D3D12 / Vulkan 时，基于浏览器的 3D 引擎需要先把这一整排 API 凑齐，才有资格谈性能优化。

## Sources

- [[sources/playcanvas-html5-game-apis]]
