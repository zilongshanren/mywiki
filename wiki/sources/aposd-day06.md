---
tags: [source, aposd, 软件设计]
date: 2026-04-05
sources: 1
---

# APoSD Day 6 —— 信息隐藏：深模块的灵魂

APoSD 学习推送系列第 6 天，对应第 5 章 Information Hiding (and Leakage)。

## 摘要

**信息隐藏**是达成 [[deep-modules|深模块]] 最重要的技术——每个模块封装一些代表设计决策的「知识」，让它们存在于实现里、不出现在接口上。**`private` 关键字 ≠ 信息隐藏**：私有字段也能通过 getter 把实现漏个干净。**信息泄漏**是最重要的红旗：同一份知识存在于多个模块。**后门泄漏**更隐蔽——不在接口里但在实现里。**时序分解**是常见陷阱——按时间顺序切模块，而不是按知识归属。推论：**有时让类稍微大一点反而更好**。

## 关键要点

- **信息隐藏**：每个模块封装代表设计决策的知识，藏在实现里。
- 两大好处：简化接口、让系统更容易演进。
- **`private` 是访问控制；信息隐藏是设计哲学**——用 public 字段也能做到好的信息隐藏，满屏 private 也能漏个干净。
- HTTPRequest 对照：`getParams()` 返回 Map（浅）vs `getParameter(name)` 返回 String（深）。
- **[[information-leakage|信息泄漏]]是最重要的红旗**——改 X 要改几处，答案 > 1 就漏了。
- **后门泄漏**（Back-door leakage）：不在任何接口里，但两个类实现都依赖同一格式——更阴险。
- **[[temporal-decomposition|时序分解]]** 陷阱：HTTP Reader + Parser 不是两件事，因为读完依赖解析 Content-Length。
- **「information hiding can often be improved by making a class slightly larger」**——反直觉但真实。
- 游戏开发高危区域：存档、资源、网络协议、配置、渲染绑定。

## 链接到的概念

- [[information-hiding]]
- [[information-leakage]]
- [[temporal-decomposition]]
- [[deep-modules]]
- [[change-amplification]]
- [[john-ousterhout]]

## 原文

- 链接到：[[raw/articles/a-philosophy-of-software-design/day06]]
