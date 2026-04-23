---
tags: [source, 游戏开发, 输入处理, 手柄, awesomenauts]
date: 2026-04-19
sources: 1
---

# The Bouncy Stick Problem（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen|Joost van Dongen]] 2011 年 10 月的文章，记录 Awesomenauts 开发中发现的一个硬件级摇杆输入问题和它的单帧阈值解法。

## 摘要

Awesomenauts 为了手感没有做角色转向的中间平滑动画——推杆即转向。玩家时常抱怨"明明一直推右、松手的瞬间角色却朝左转了"，在商店里这意味着"买错道具"。Joost 的同事 Machiel 定位到根因：手柄摇杆松手时弹簧把杆弹回中心，但弹力强到会**越过 0 点**出现反向瞬时值——PS3 / Xbox 360 手柄都有此现象，老手柄更严重（实测 1 → -0.72 的过冲）。因为 Awesomenauts 反应极快、且单帧采样有时恰好落在过冲那一瞬，一帧的负值就被当作"立即反转"执行。加大 deadzone 要覆盖到 0.72 会让游戏只能识别"推到底"；忽略单帧输入意味主动加一帧滞后；帧间平均会糊掉所有输入。最终解：**当单帧摇杆位置变化 |Δ| > 1.05 时忽略该帧**。因为真实玩家一帧内挪不了 1.05，而弹簧过冲几乎必然在一帧内完成（从极端值跨过 0 回到反向）。上线后问题再没复现。

## 关键要点

- **回弹过冲是硬件现象**：弹簧力过强，杆回到 0 时有瞬时越位（PS3/Xbox 360 均有，老手柄更严重）。
- **快响应游戏放大了问题**：慢响应游戏的转向平滑动画天然吸收了单帧噪声；追求零滞后的游戏把它直接显化。
- **三个不可用方案**：扩 deadzone（覆盖 0.72 等于只认极端值）、跳过单帧（主动引入 1 帧滞后）、帧间平均（糊化所有输入）。
- **单帧 Δ 阈值**：|current − previous| > 1.05 则丢弃该帧。依据是"人类一帧内挪不了这么远，弹簧能"。
- **评论区改进**：更精确形式是"跨过符号且 |previous| 大时把 current 置 0"，避免释放状态非极端时的误伤。

## 链接到的概念

- [[gamepad-stick-bounce-filter]]
- [[unity-input-system-multi-gamepad]]
- [[kinematic-character-controller]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/10/bouncy-stick-problem.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-10-29_the-bouncy-stick-problem.md`
