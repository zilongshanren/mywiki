---
tags: [source, graphics, animation, character, game-art-tricks]
date: 2026-04-19
sources: 1
---

# The High Heel Problem（Simon Trümpler）

[[simon-trumpler]] 2025 年 3 月的「Game Art Tricks」专栏之一。看起来像花边话题——游戏角色穿高跟鞋到底怎么办——但实际是一次横跨**角色骨骼、动画、IK、摄像机、碰撞体**的工程侦察：在高度变化这一个小切口里，把十几款 AAA/独立游戏的不同解法摆到桌面上对比。

## 摘要

问题：角色穿上高跟鞋，**至少变高 10 厘米**。这导致：
- 手—按钮、手—门把手等 contact 点错位；
- 对话中脸部高度错了；
- 潜行时掩体高度不够；
- competitive 游戏里受击判定体变形。

作者把业界解法划分为两大类六小类：

**方案 A：正确调高度**
1. **Hope for the best**——Infinity Nikki 这种非精确交互为主的游戏，直接让角色变高，clipping 问题极少有人注意；
2. **Manual labor**——per-shoe 动画（GTA Online 的打高尔夫动画就只有平跟版本）；
3. **Dynamic IK**——现代引擎的 full-body IK 系统自动把手脚 retarget 到正确位置；Uncharted 的「走路蹭墙」和 Infinity Nikki 的地形 foot IK 都在这条路上。

**方案 B：找变通**
1. **Hide**——鞋筒够高，脚藏进去让腿视觉上变短；
2. **Shorten**（Sims 4 就是这么干的）——小腿直接缩短，髋部不动，小腿与大腿角度维持，但小腿 mesh 短了几厘米——玩家从正常视角几乎看不出；
3. **Bend**——脚不动，脚腕角度扳起，像踩着尖但腿长不变。

最后还有混合策略：碰撞体保持原高度、视觉高度改变，competitive 游戏常采这种——看起来穿了鞋但受击判定不变。

## 关键要点

- **鞋子高度不是换 mesh 这么简单**——要考虑 bone 位置、IK 链、contact animation、camera framing、碰撞体。
- **Sims 4 的 shorten 小腿方案** 是最省事的产业解——玩家几乎察觉不出，动画、摄像机、交互都不用改。
- **IK 系统是个关键分水岭**：支持 full-body IK 的引擎可以用动态方案；老引擎只能靠 per-shoe 动画。
- **per-shoe 动画有漏洞**——GTA Online 打高尔夫只有平跟版本、Infinity Nikki 换鞋的那一帧姿态还没跟上，都是被作者抓到的 bug 样本。

## 链接到的概念

- [[character-height-variation-problem]]

## 原文

- 链接：https://simonschreibt.de/gat/the-high-heel-problem/
- 本地：`raw/articles/simonschreibt.de/2025-03-17_simonschreibt.md`
