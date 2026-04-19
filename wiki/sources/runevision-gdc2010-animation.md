---
tags: [source, blog, gdc, animation, unity, uncharted]
date: 2026-04-19
sources: 1
---

# GDC 2010 现场观察：Unity 展台、Limbo 与 Uncharted 动画技术（Rune Skovbo Johansen / blog.runevision.com）

[[rune-skovbo-johansen]] 发表于 2010 年 3 月 14 日的博客，记录了他作为 Unity 员工在 GDC 2010 的参会体验，重点回顾了 Naughty Dog 的 *Player Movement and Animation in Drake's Fortune 1 and 2* 演讲。

## 摘要

文章分四段：Unity 展台几乎每个路人都听说过 Unity；IGF 丹麦团队双双获奖——*Playdead* 的 *Limbo* 拿下两项，*Press Play* 的 Unity 作品 *Max & the Magic Marker* 也拿到一项；Drake's Fortune 动画讲座没有突破性算法，但在细节上有若干实用技巧；最后是回程感言。技术含量集中在第三节：Naughty Dog 的角色动画几乎都可以直接在 Unity 中复现，仅有一项（水平翻转动画以节省内存）是 Unity 当时做不到的。作者强调他们的主要武器是大量的动画混合、部分骨骼混合、加法动画层，外加脚部 IK 修正——这些当年已是 Unity 原生能力。

## 关键要点

- **加法层叠 1 帧 idle**：Drake's Fortune 在 1 帧的静止 pose 上叠一段长周期随机摆动动画，做出多种"不重复"的 idle/walk/run 变体，详见 [[additive-animation-layering]]。
- **部分骨骼动画**：有些动画只作用于骨架的一部分（例如只控制上半身），下半身另行驱动。
- **加法动画（additive）** 也被用于动作变化，节省空间又能叠出复杂行为。
- **脚部 IK**：通过 raycast 求地面高度，调整骨盆根位置，再用 IK 收脚——思路与作者自己的 Unity Locomotion System 一致，只是更简洁。
- **唯一的 Unity 盲点**：Naughty Dog 为省内存会做"水平翻转动画"，当时 Unity 无法原生支持；其余技术在 Unity 里脚本化或配置即可实现。
- **工业背景**：当年 Unity 3 尚未发布，作者在展台预告了即将到来的新特性。

## 链接到的概念

- [[additive-animation-layering]]
- [[rune-skovbo-johansen]]

## 原文

- 链接：https://blog.runevision.com/2010_03_14_archive.html
- 本地：`raw/articles/blog.runevision.com/2010-03-14_runevision-blog-2.md`（另有 `2010-03-14_runevision-blog.md` 为完全相同的月度归档页）

## 备注

同一博客同周期还抓取了两组重复页面：2010-02-04 的 Nordic Game Jam 回顾、2010-02-11 的 Unity 动画 demo 两句话预告，两者均无可提炼的技术内容，本 batch 作 `skipped_offtopic` 处理。
