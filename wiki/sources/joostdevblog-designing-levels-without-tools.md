---
tags: [source, game-development, level-design, tools, indie]
date: 2026-04-19
sources: 1
---

# Designing levels without tools（Joost van Dongen，2010-12-18）

[[joost-van-dongen]] 2010 年 12 月的回顾，讲 Swords & Soldiers（Ronimo 首作，Wii 主机项目，程序员只有一人）在**没有正式关卡编辑器**的条件下如何把关卡做出来。

## 摘要

全套解法分三层。第一层，核心 gameplay 数据（金矿、塔、地形高度、地形类型）用 Notepad 按行编辑——每行一类信息，游戏本身就在一条线上展开，设计师看文本就够了。第二层，美术想摆 props，就多给几行、每个 prop 一个字符代号，在 Notepad 里按字符布置；虽然「硬核 hacking 风」，但够用。第三层，曲线地形不直接用设计师给的高度——先做邻域模糊让曲线平滑，再靠 tiling 地表贴图里画的小起伏掩盖三角 strip 的数学感，看起来像手绘。视差背景/前景则走「程序化放置」：美术给每层定义元素库（近树、中景山、远山、云），引擎随机布置，美术只能通过「每层密度 0 到满」+「每关两条渐变（背景色 + 大气雾）」来差异化。**代价**是做不出「这一关有座城」的地标级独特性，只能靠渐变和整体氛围遮掩重复感。尽管如此，最终成品拿到了 IGN「Wii 上最好看游戏之一」的评价。后来的 RoniTech 2 补上了完整 in-game 编辑器。

## 关键要点

- 一维 gameplay 数据用行文本 + 字符代号是被严重低估的实用解法。
- 曲线地形 = 设计师手值 → 模糊平滑 → 地表贴图遮掩三角感，三步走。
- 程序化视差背景能掩盖「资产有限」的问题，但换不出独特地标。
- 工具成本换美术自由度的 trade-off 要提前跟美术沟通。

## 链接到的概念

- [[level-design-without-editor]]
- [[tools-first-iteration-loop]]
- [[game-settings-hot-reload]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/12/designing-levels-without-tools.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-12-18_designing-levels-without-tools.md`
