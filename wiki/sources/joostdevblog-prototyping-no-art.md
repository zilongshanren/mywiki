---
tags: [source, 游戏开发, 原型, 设计方法, 反馈]
date: 2026-04-19
sources: 1
---

# How a lack of art influences prototyping results（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen|Joost van Dongen]] 2011 年 11 月的文章，通过 Awesomenauts 的跳跃蓄力原型实例，讲"原型方法本身不中立——它会塑造结论"。

## 摘要

Awesomenauts 早期用 Swords & Soldiers 的旧角色做占位（没有跳跃动画），设计师希望跳跃有重量感：按键后蓄力 0.5s 起跳、落地后停 0.5s 再能跑。Joost 直接在代码里加两段 pause——抽象机制上这就是最终产品，唯一差别是那 0.5s 里没有动画。实测感觉是"操控延迟"，团队短暂试玩后放弃。他事后反思：问题不是机制烂，而是**原型缺动画**——有动画的 0.5s 里角色屈膝起跳，玩家按键立即有画面反馈；无动画的 0.5s 里玩家按键后屏幕毫无反应，等价于输入延迟。最低成本的修补是 squash & stretch 代码动画；但 Awesomenauts 整体取向就是"立即跳"所以最终仍选择无蓄力，这个决策被认为是正确的即便原型方法"测不准"。文章后半列了同模式的四类坑：无音效、音乐在游戏外播放、无音画的 FPS 枪、占位美术下单位差异化误判。结论：尽早加占位美术和音效（哪怕从别的游戏里扒）胜过纯抽象原型。

## 关键要点

- **没有动画 ≡ 输入滞后**：0.5s pause 有动画是蓄力反馈，无动画是操控延迟。物理时序相同，体验天壤之别。
- **抽象原型不中立**：纯机制原型会系统性低估"反馈依赖型"机制（如 Assassin's Creed 的爬墙、跳跃蓄力）。
- **临时音效比无音效好**：Swords & Soldiers 先用魔兽 3 音效占位，上正式音效时再替换。
- **游戏内同步的音乐感觉完全不同**：音乐试听时必须用游戏内触发，否则判断偏离。
- **FPS 枪的 80/20**：打击感 80% 来自音画，20% 来自数值——无音画的原型测不了枪感。
- **占位美术扭曲单位判断**：Aztec Sun Giant 和 Viking Frost Hammer 抽象数据像，加美术后完全不同。

## 链接到的概念

- [[prototyping-method-bias]]
- [[easy-to-learn-hard-to-master]]
- [[game-idea-generation]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/11/how-lack-of-art-influences-prototyping.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-11-06_how-a-lack-of-art-influences-prototyping-results.md`
