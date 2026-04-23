---
tags: [source, game-engines, flash, actionscript, 碰撞检测, 教程]
date: 2026-04-19
sources: 1
---

# FlashPunk Hello World (Shooter)（Marte / Random Tower）

[[people/marte-randomtower|Marte]] 发表于 2010 年 1 月的实践文章，在评析 FlashPunk 框架之后动手构建了一个可玩的 Flash 射击 Demo，验证框架的实际可用性。

## 摘要

作者在 FlashDevelop 环境中使用 FlashPunk 框架搭建了一个最小化射击游戏，包含精灵加载、玩家移动（方向键）、射击（Z 键）、基本碰撞检测与响应，以及移动敌人和简单 GUI。核心收获是 FlashPunk 的碰撞 API 极其简洁：一行 `collide("enemy", x, y)` 即可完成碰撞判断，碰撞类型标签（`setCollisionType("test")`）让开发者轻松控制哪些实体之间会相互作用。静态工具类 `FP.world.remove(this)` 让 Entity 自行从 World 中移除，减少了跨系统通信的样板代码。文章附带了完整源码下载，证明框架对初学者的学习曲线确实友好。

## 关键要点

- `collide("type", x, y)` 一行完成碰撞检测，框架隐藏底层碰撞树遍历
- `setCollisionType("label")` 通过字符串标签分组实体，控制碰撞关系
- `FP.world.remove(this)` 静态单例访问 World，Entity 可自我销毁
- 多精灵嵌入（`[Embed]`）直接打包进 SWF，Flash 时代的常见发布模式
- Main.as → HelloWorld（World）→ Player/Enemy/Explosion 的四层类结构清晰示范框架用法
- 关闭 FlashPunk splash logo 只需修改 Main 构造函数最后一个布尔参数

## 链接到的概念

- [[game-engines/flashpunk-framework]]

## 原文

- 链接：https://randomtower.blogspot.com/2010/01/flashpunk-hello-world-shooter.html
- 本地：`raw/articles/randomtower.blogspot.com/2010-01-19_flashpunk-hello-world-shooter.md`
