---
tags: [source, version-control, asset-pipeline, perforce, git-lfs, workflow]
date: 2026-04-19
sources: 1
---

# Source Control for Art Assets - This Must Exist（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015 年 12 月一篇半咨询帖——随着 X-Plane 美术团队扩大，GIT + SVN 组合开始吃力，Supnik 梳理"理想工具应有的形态"后发现市场上没人完全覆盖。

## 摘要

帖子把艺术资产 VCS 的本质诉求和源码 VCS 清晰对照：源码可合并、艺术资产不可合并；资产量级大（TB 级），但单次只动少数——"只拿需要的子集"才是刚需。Supnik 原本用 SVN 管资产，抱怨慢，后自测承认 SVN 线速度其实足够，真正痛点是"哪怕只想 get-latest 一架飞机也要保留整个 pile 的 `.svn` 镜像，磁盘 2×"。他尝试把 GIT 硬塞进来失败——对大二进制的根本假设错。他的理想模型：服务端是**内容可寻址对象池**（像 GIT object DB），每版本对应一个 **manifest**（文件路径→hash），manifest 放进 any VCS，客户端按 manifest 下载缺的对象，本地**不保留任何 VCS 元数据镜像**——本质是"版本控制化的 X-Plane installer"。评论区集中推荐 Perforce（游戏行业事实标准，支持大文件 + 窄 clone + 权限）和 Git LFS（当时仍年轻，今天已主流）。Supnik 明确反驳"集中式 + lock 是缺点"——对艺术资产是**特性**，因为多人同时改同一个 `.psd` 只会有一方被牺牲，lock 强制前置沟通。他也给出版本化 + 分支都是硬需求的 X-Plane 具体场景：tip 上的 WIP 不能阻塞旧版 bug fix、要能给"所有 in-progress 飞机"批量应用跨文件改动。

## 关键要点

- 源码与艺术资产需要不同 VCS 工具——不是"美术不懂 VCS"
- 艺术资产关键需求：lock、大文件、子树只拿、保留历史、不留 `.svn` / `.git` 镜像
- "VCS 化的 installer"≈ manifest-first + 内容可寻址对象池——Git LFS 的后来形态
- Perforce 是游戏行业事实标准；代价是闭源收费、分支不如 GIT 灵活
- Git Fusion / GitSwarm：Perforce 后端 + GIT 前端桥接，同一仓库两种工作流
- "集中式 + lock"对无法 merge 的二进制是 feature 不是 bug
- 版本化 + 分支都是硬需求：旧版 bug fix、跨文件批量改
- Dropbox 可以当"throw-over-the-wall"的补充通道，但不是 VCS 替代

## 链接到的概念

- [[art-asset-version-control-gap]]
- [[asset-exchange-format-strategy]]
- [[game-resource-pack-format]]
- [[xlsx-text-versioning]]
- [[resource-reference-path-vs-guid-vs-name]]
- [[stl-not-abstraction-prescription]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2015/12/source-control-for-art-assets-this-must.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-12-10_source-control-for-art-assets-this-must-exist.md`
