---
tags: [source, game-design, simplicity, twitch, racing, proun]
date: 2026-04-19
sources: 1
---

# Proun's game design（Joost van Dongen / Joost's Dev Blog，2011-06-19）

[[joost-van-dongen]] 在 Proun 发布前一周撰文，回应 trailer 下「就两个按键够深度吗」的质疑，系统讲了 Proun 的 gameplay 设计原则。

## 摘要

Proun 的核心设计约束是**极简**：「要解释给玩家的东西越多，设计越糟」。两按键（左/右绕电缆旋转）是唯一输入。和 Super Crate Box、Super Meat Boy 同属**快速重试的 twitch 玩法**，但单赛道略长。深度由四层叠加挑战构成：难度档位（最高档 4 倍速）、**旋转减速机制**（绕得越少越快，鼓励贴障碍飞）、**可充能 boost**（12 秒不撞换 2 秒加速）、**Ghost 模式**（与所有历史回放同场竞速）。Joost 特别复盘了最早版本的设计错误——存在「确定性最优通关」（一路加速不撞），导致达到后玩家无事可做；后续所有机制都是为了**让最优路线永远差一点、可追求**。极简核心顺带带来触达性红利：非硬核玩家、festival 观众、儿童都能上手。

## 关键要点

- 「Easy to learn, hard to master」是与极简美术呼应的硬约束。
- 存在「可达成的完美」是 skill-based 游戏的设计失败——必须人为加入让最优解持续漂移的机制。
- Ghost 模式不仅与最佳时间比，**和所有历史时间比**才真正好玩。
- Twitch 玩法的关键是**重试循环的短平快**——Proun 的重试比 Super Meat Boy 略长一个单位，但仍在「快速再来一次」的范畴内。
- 极简核心自带触达性，不必为儿童 / 非玩家额外设计。

## 链接到的概念

- [[easy-to-learn-hard-to-master]]
- [[joost-van-dongen]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/06/prouns-game-design.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-06-19_proun-s-game-design.md`
