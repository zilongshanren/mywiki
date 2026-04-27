---
tags: [source, hacksoflife, 软件设计, 发布, 估时, 项目管理]
date: 2026-04-27
sources: 1
---

# Klingons Do Not Release Software（Ben Supnik / The Hacks of Life）

[[ben-supnik|Ben Supnik]] 发表于 2019 年 10 月的文章，回应 Brent Simmons 关于软件发布 ETA 的感慨，阐释软件估时为何天然困难，以及缩减范围才是真正的解法。

## 摘要

Simmons 把应用开发比作"用生锈的钉子赤手在龙卷风中建造有史以来第一栋房子"。Supnik 将这个直觉做了理论化：根本原因在于**软件的可复用性**——每个值得做的功能，在你的团队历史上都是第一次做这类事情。X-Plane 的飞机内容制作（建模、UV、动画）有稳定的工作量参考，因为任务类型固定；但软件功能没有这个性质，Vulkan 移植做完就永远不会再做第二次。

Simmons 说"软件发布的唯一原因是人们不停工作直到准备好"，Supnik 认为这只说对了一半。另一条真实路径是：**压缩范围，让它只包含已经完成的部分**。"准备好"是动态定义，会随市场条件和实现过程中对需求的重新认识而变化。如果软件在你意识到之前已经"准备好了"，就会发生 Klingon 软件现象——它逃出去，留下一路血迹。

## 关键要点

- 软件功能天然不可重复，每个功能都是首次，没有已知工作量参照
- 内容制作（3D、音频等）可以有稳定估时，软件功能不行
- 缩减范围是压缩交付时间的唯一有效手段，"不停工作直到完成"不是
- "ready"是动态的，能识别已完成最小集合并及时交付，才是成熟的项目判断力
- 过于复杂的"Klingon release"是项目管理失控的结果

## 链接到的概念

- [[software-release-estimation]]
- [[always-shippable-game]]
- [[unknown-unknowns]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2019/10/klingons-do-not-release-software.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2019-10-29_klingons-do-not-release-software.md`
