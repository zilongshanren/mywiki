---
tags: [source, 版本控制, 工作流, 构建系统]
date: 2026-04-19
sources: 1
---

# Version Control for the next-gen?（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 发表于 2011 年 4 月的一条非常短的「头脑风暴」帖，抛出他对下一代主机世代下游戏团队版本控制架构的草图。全文几乎只是一串 bullet，重点在提问而非解答。

## 摘要

Pesce 把团队的数据分成三类，分别给出他当时认为「合理」的工具选型：

- **源码**——用 DVCS，如 Mercurial。（在 git 尚未成为行业默认前，Mercurial 是当时游戏工作室讨论得最多的分布式候选。）
- **艺术资产**——分布式、版本化（copy-on-write）文件系统。他点名 Lustre + ZFS 的组合；同时对 VCS + 依赖追踪系统「只同步当前任务需要的子集」的方案表达兴趣，引用了 Shotgun 和 Tactic 两个制片工具。
- **构建产物**——CI（CruiseControl / Jenkins）机器把测试通过的构建发到分发系统（如 BitTorrent）给团队使用。

评论区补充了一条现在看来颇有前瞻性的建议：把以上全部打进一份带 web GUI 的 VM 镜像，像 GitHub 那样提供 issues / diff / 图像 diff / 讨论 / 任务视图。这基本是后来 Perforce Helix + Swarm、UGS、GitHub 大型仓库等实际演化路径的混合前身。

## 关键要点

- **三类数据分三套工具**的直觉 2011 年已经成型：源码（可合并文本）、资产（二进制大文件）、构建产物（可丢弃但要可追溯）。这个三分法至今仍是 AAA 工作室 VCS 架构的骨架（见 [[art-asset-version-control-gap]]、[[vcs-vs-database-for-content]]）。
- **Mercurial vs git**：2011 年游戏圈对 DVCS 的讨论仍以 Mercurial 为主要候选，几年后 git 才真正吃掉工作室的源码侧。
- **copy-on-write 文件系统做资产存储** 的设想在 2011 年还很前卫，后来 Perforce 的 narrow clone / Git LFS / Plastic SCM / Unreal 的 virtualized assets 走的都是「只同步需要的子集」这条线。
- **依赖驱动的 sync**（参照 Shotgun / Tactic）这条线 2020 年后被 Unreal Horde、Turnkey、各家自研任务系统继承下来。
- 帖子很短，更像是作者公开一份心智模型来邀请讨论，而不是完整方案——典型的 Pesce 博客风格。

## 链接到的概念

- [[angelo-pesce]]
- [[art-asset-version-control-gap]] —— Supnik 2015 梳理「理想艺术资产 VCS」的 gap 分析，是 Pesce 这个 2011 sketch 的完整化
- [[vcs-vs-database-for-content]]
- [[jujutsu-vcs]] —— 现代 DVCS 后继者之一

## 原文

- 链接：https://c0de517e.blogspot.com/2011/04/version-control-for-next-gen.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-04-01_version-control-for-the-next-gen.md`
- 归档重复副本：`raw/articles/c0de517e.blogspot.com/2011-04-01_version-control-for-the-next-gen-2.md`
