---
tags: [minecraft, java, modding, tooling]
date: 2026-04-19
sources: 1
---

# Minecraft 插件开发

Minecraft 社区把「改游戏」分成三条独立路线：**命令方块 / 数据包 / 资源包**（原生能力）、**plugin**（服务器侧，通过 Bukkit API）、**mod**（客户端侧，通过 Forge/Fabric）。三者的能力边界、兼容性、部署方式互不相同，新手常混淆。[[alan-zucconi]] 的 *Minecraft Plugin Development* 给出清晰对比与完整实战。

## 三条路线的分水岭

| 方式 | 在哪跑 | 能改什么 | 客户端要不要装 |
|---|---|---|---|
| 数据包 | 服务器 | Minecraft 命令组合、现有 loot table / recipe | 不用 |
| 资源包 | 两端 | 贴图、模型、音频（替换现有资产） | 要下发 |
| **插件** | 服务器（Spigot/Paper/Purpur） | 监听事件、改伤害、加物品 NBT、新 gameplay | 不用 |
| **mod** | 客户端（Forge/Fabric） | 任何想法，包括新方块、新维度、新渲染 | 要装，且与服务器匹配 |

**关键区别是 NBT 标签**：数据包能造命令组合、触发命令给物品打属性，但**不能让合成配方直接产出带自定义 NBT 的物品**。Zucconi 早期的 *Minecraft Laser Gun* 用「carrot on a stick + Custom Model Data」做的 hack 就是这个限制的绕行方案。要想在合成表里直接造「会发激光的胡萝卜」必须上插件。

## Paper + Bukkit API 工程结构

现代教程几乎全推荐 **Paper**：它是 Spigot 的性能 fork，API 兼容 Bukkit，性能/异步改进明显。IntelliJ 工程的典型骨架：

- `pom.xml`：声明 `io.papermc.paper:paper-api` 依赖；
- `plugin.yml`：声明入口 `main`、`name`、`version`，以及事件处理类；
- 主类继承 `JavaPlugin`，覆写 `onEnable()` / `onDisable()`；
- 事件监听类实现 `Listener` 接口，方法标注 `@EventHandler`；
- 调度器 `Bukkit.getScheduler()` 提供 sync/async 任务。

部署只需把 shaded JAR 丢到服务器的 `plugins/` 目录并重启；客户端完全无感。

## 生态的混乱与收敛

Minecraft 服务端有过 Bukkit → Spigot → Paper → Purpur → Pufferfish 的连环 fork 史（最早的 Bukkit 因版权被 Mojang 摁掉）。现在 90% 的新项目用 Paper 或 Purpur；客户端 mod 侧则两分天下：Forge（老牌、资源丰富）、Fabric（轻量、更新快）。任何教程的第一个决策点都是「你在哪一端写代码」。

## 与其他 wiki 主题的位置

这是本 wiki 里为数不多的**服务端 Java 游戏开发**页面。最近的邻居是 [[game-engine-vfs]]（也关注资源打包）与 [[cloudwu]] 的 MMO 存档/广播系列，但 Minecraft 插件的**事件驱动 + 单服务器**模型和 MMO 的 shard + snapshot 模型不在一个抽象层上。

## Sources

- [[sources/alanzucconi-minecraft-plugin]]
