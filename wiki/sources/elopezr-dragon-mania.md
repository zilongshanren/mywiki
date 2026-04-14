---
tags: [source, postmortem, 手游优化, android, midp, 纹理打包]
date: 2026-04-14
sources: 1
---

# Dragon Mania（Emilio López Ros / Gameloft）

[[emilio-lopez-ros|Emilio López Ros]] 2014 年写的简短 postmortem，记录他在 Gameloft 时为《Dragon Mania》做性能抢救的经验：一个用 MIDP 老引擎加 Android port 的龙养成+对战游戏，在 Galaxy Ace 上从 3-4 fps 抢到 14-15 fps。

## 摘要

Dragon Mania 是一个"养龙+繁殖+对战"的 tycoon 游戏。作者在开发末期加入团队，负责音频/本地化 bug 修复、**性能优化**和**dither 算法**。游戏沿用了一个 MIDP 时代的老引擎移植版，缺陷非常典型：**每纹理只有 256 色**（迫使引入 dither）、纹理打包效率差、draw call 堆积（~900 张纹理）、龙本身由多个部分组成且系统不允许把同一条龙打包进单张纹理——每只龙每个部位就要一次 draw call。因为在线对战需要预加载所有龙贴图，纹理驻留压力又进一步放大。作者通过"裁剪纹理、减少 OpenGL 调用、能打包就打包、用 [[floyd-steinberg-dithering|Floyd–Steinberg dither]] 掩盖 256 色限制"等几套老套路把帧率从 3-4 fps 抬到 14-15 fps，被团队认为可玩。

## 关键要点

- 老 MIDP 引擎 port 到 Android 带来结构性问题：每纹理 256 色、纹理打包弱、draw call 堆积；
- 约 900 张纹理需要在启动时全部加载（为了避免对战/繁殖时 runtime 卡顿）；
- 龙拆成多个部位导致每条龙就是 N 个 [[draw-call|draw call]]；
- 典型优化清单：剪图、减 GL 调用、尽量 [[batching|texture atlas / batching]]、Floyd–Steinberg 掩盖色深；
- 最终在 Galaxy Ace 上从 3-4 fps 抬到 14-15 fps；
- 故事本身是"在继承一套不允许你动结构的旧引擎时，工程师能做什么"的缩影——和 [[engine-evolution|引擎演化]] 话题呼应。

## 链接到的概念

- [[floyd-steinberg-dithering]]
- [[draw-call]]
- [[batching]]
- [[engine-evolution]]

## 原文

- 链接：https://www.elopezr.com/dragon-mania/
- 本地：`raw/articles/elopezr.com/2014-03-09_dragon-mania.md`
