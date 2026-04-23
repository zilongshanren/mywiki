---
tags: [source, bitsquid, 协作, 版本控制, 数据模型]
date: 2026-04-19
sources: 1
---

# Collaboration and Merging（Niklas Frykholm / bitsquid blog）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 3 月基于本地化工具实际落地的一篇设计思考：**协作的本质不是数据库，而是合并**。

## 摘要

游戏项目是高度协作的产物，但大多数工具链仍然停留在"一人一锁"的文件级并发控制——关卡设计尤其难受。Frykholm 在做本地化工具时领悟到：**只要数据能干净地合并，协作就自然好做；合不动，无论后端是中央数据库还是 git 都白搭**。把"所有操作走中央 DB 同步确认"的强一致方案拿掉，换成 async 提交 + 客户端 / 服务端两侧 merge（web 2.0 学到的方式），后端是 DB 还是 VCS 还是 patch 文件都不重要，关键变成 merge 的健壮性。既然关键是合并，那就应该**主动设计数据让它好合并**——传统 line-based 的 diff 是为源代码设计的，但源代码恰恰是最难合的东西；游戏资产反而在结构上"天然好合"。Frykholm 由此导出了一个 **objects-with-properties** 的最小数据模型：每对象一个 GUID、每字段一个字符串 key，值只允许 null/bool/double/vec3/quat/string/blob/GUID/GUID-set；不允许数组（数组重排难合）、只有 set（set 操作天然可合并）；根对象 GUID = 0。所有修改被压到 `create / change_key / add_to_set` 等少数原子操作，合并就变成 change-set 的 append。真冲突的定义被压缩到"同一对象同一 key 被改成不同值"一种情况。

## 关键要点

- **协作 ≠ 中央数据库**；协作 ≈ 合并；任何 async 系统都是 merge territory；
- **line-based diff 为源代码而设计**，但源代码是所有数据里最难合并的——现状是用"对 code 都嫌勉强"的工具在合**比 code 简单得多**的内容数据；
- **要做到内容好合并，先要把数据表达成 objects-with-properties**：GUID 做对象 id（不同机器不会撞）、string 做字段 key（可向后兼容）；
- **砍掉数组、只保留 set**：数组 reorder 合并极难，改用显式 sort_order 字段 + set；
- **一切改动表达成原子操作序列**：合并 = 两串 op 的 append + 冲突消解（相同 guid+key 的不同值）；
- **change set 本身可以就是数据存储格式**——Frykholm 的本地化工具就是这么干的，没上数据库；
- **保留本地未提交状态**的能力很重要（类比 git "half-finished" 代码不应让别人看见）；这也是 lockstep DB 做不到的。

## 链接到的概念

- [[guid-object-database-schema]]（该概念页直接基于此文与前作整合；本文把"协作"视角补完）
- [[json-3-way-merge]]
- [[vcs-vs-database-for-content]]
- [[snapshot-diff-persistence]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2011/03/collaboration-and-merging.html
- 本地：`raw/articles/bitsquid.blogspot.com/2011-03-27_collaboration-and-merging.md`
