---
tags: [source, game-development, java, minecraft, tooling]
date: 2026-04-19
sources: 1
---

# Minecraft Plugin Development（Alan Zucconi）

[[alan-zucconi]] 2024 年 4 月发表的完整教程，把 *Minecraft* 生态里「mod vs plugin vs data pack」的混乱厘清，再以一个可传送罗盘（linked lodestone compass）作玩具例子，手把手走通 IntelliJ + Paper + Bukkit API + bStats 的插件开发流程。

## 摘要

文章第一部分是 Minecraft 改造生态的**地图**。原生 Minecraft 只暴露三种自定义途径：命令方块、数据包、资源包——都受限于 Minecraft 指令语法，不能真正改变游戏规则。想深入就必须走**插件**（服务器侧）或 **mod**（客户端侧）路线。*Spigot / Paper / Purpur* 是一系列修改版服务端，兼容原版客户端但支持插件；*Forge / Fabric* 则在客户端层做深度修改，适合跨度更大的 mod。第二部分进入代码：`pom.xml` 添加 PaperMC 依赖、`plugin.yml` 声明入口类、继承 `JavaPlugin`、监听事件、使用 Bukkit 调度器。第三部分落到玩具例子——读者需要在 craft 事件里检测特定配方、为新罗盘打 NBT tag（数据包做不到的事情）、在右键事件里读取 lodestone 位置做传送。最后一节讲部署：打 shaded JAR、上传到服务器 plugins 目录、用 bStats 收集使用量。

## 关键要点

- **plugin vs mod**：plugin 跑在服务器端、用 Bukkit API、客户端不用装任何东西；mod 改客户端（Forge/Fabric），一般要求服务器也装同样的 mod。
- **NBT 标签是分水岭**：data pack 能造命令组合但不能给物品打任意 NBT 标签，这就是为什么 Zucconi 最早的 *Minecraft Laser Gun* 只能用「carrot on a stick + custom model data」的 hack 路线；要做真正的新物品还是得上 plugin。
- **Paper 是 Spigot 的性能 fork**——几乎所有新教程都首推 Paper，API 与 Spigot 兼容。
- **bStats 集成**——三行代码接入，作者把公开的使用量指标视为对社区贡献的正反馈。

## 链接到的概念

- [[minecraft-plugin-development]]

## 原文

- 链接：https://www.alanzucconi.com/2024/04/17/minecraft-plugin-development/
- 本地：`raw/articles/alanzucconi.com/2024-04-17_minecraft-plugin-development-alan-zucconi.md`
