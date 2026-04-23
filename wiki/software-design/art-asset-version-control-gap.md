---
tags: [版本控制, 资源管线, art-asset, perforce, git-lfs, 工作流]
date: 2026-04-19
sources: 1
---

# 艺术资产的版本控制：仍然没有理想解

[[ben-supnik|Supnik]] 2015 年写了一篇半咨询半自言自语的帖子：随着 X-Plane 美术团队扩大，GIT + SVN 的组合开始跟不上，他梳理"理想工具应该长什么样"，结果发现市面上**没有一个工具恰好覆盖所有需求**——这个判断十年后仍然大致成立。帖子本身像一面镜子，把艺术资产 VCS 的本质诉求映得很清楚。

## 艺术资产 vs 源码的结构差异

程序员团队和美术团队用的工具不同，不是因为美术"不懂 VCS"，而是**资产的结构性质不同**：

- **源码可合并**——纯文本、行级 diff 成熟、冲突可人工 resolve；
- **艺术资产不可合并**——二进制 blob（.psd / .fbx / .max / .blend），没有通用 diff，两人同时改几乎一定是灾难；
- **资产量级大**——一个 X-Plane 飞机包几十 MB 到几百 MB，几千个飞机 = TB 级存储；
- **只修改少数**——某一刻某个艺术家只在做其中一架飞机，其他几千个对他是"只需要拿到最新就好"。

**关键推论**：源码需要分支 + 合并能力，艺术资产需要**lock + 高速传输 + 只拿需要的子集 + 保留历史版本**，这两套诉求非常不同。

## Supnik 当时的工具对比

| 维度 | SVN（当时 X-Plane 用） | GIT | rsync | Perforce |
|---|---|---|---|---|
| 集中式，美术可理解 | ✓ | ✗ | 无 VCS | ✓ |
| 不复制完整历史 | ✓ | ✗（全仓库 clone） | 无 VCS | ✓ |
| 可子树 checkout | ✓ | ✗（shallow 是近似） | ✓ | ✓ |
| 不浪费磁盘（无 `.svn` / `.git`） | ✗ | ✗ | ✓ | ✓ |
| Lock 原生支持 | 次要 | ✗ | 无 | ✓ |
| 大文件表现 | 中等 | 差（需 LFS/annex） | 优 | 优 |

Supnik 最初抱怨 SVN 慢，后来自测承认 SVN 的**线速度**其实逼近 rsync/GIT——慢的是 GUI 客户端。但 SVN 的"需要 `.svn` 工作目录"这个缺点仍在：即便你只想 get-latest 几千个飞机里的一个，整个 pile 都要留一份 `.svn` 镜像。

## 理想工具："版本控制化的 X-Plane installer"

Supnik 对自己理想解的描述非常具体：

1. **内容可寻址存储**（CAS，像 GIT 的 object DB）在服务器上存每一个资产文件的每一版；
2. **manifest = 本版本应当有的 {文件路径 → hash}** 列表，本身放进任何 VCS（相对小）；
3. 客户端对比本地 manifest 和远端 manifest，**只下载 hash 不匹配的文件**；
4. 不需要保留任何 `.git` / `.svn` 镜像，本地就是**裸的一堆资产文件**（加一份 manifest）。

本质上就是把 X-Plane 的客户端 updater（manifest + HTTP 对象池）加上版本，**为 manifest 本身做版本控制**——文件 blob 是 CAS 不变量，manifest 是版本单位。

这套架构今天在多个产品里有对应物：**Git LFS** 的 pointer + 远端 object store、**Perforce 的 streams/narrow-clone**、**Bitbucket/GitHub 的 LFS 服务端**，思路完全一致。Supnik 写这篇时已经提到 LFS、annex、bigfiles、fat、media 五个候选，"找不到赢家"是彼时的真实状态。

## 评论里给出的主要替代

- **Perforce**：游戏行业事实标准（评论中多人推荐）。地面真值——大文件 + 窄 clone + 权限 + 24/7 支持。代价是闭源、收费、分支心智不如 GIT 灵活。2015 年后 "Helix + Git Fusion" 把 Perforce 后端 + GIT 前端组合起来，对开发团队和美术团队都友好。
- **Git LFS**：开源路径的主流选择。当时仍在起步，今天（2026 年）已是 GitHub / GitLab 默认能力。
- **Git-annex**：早于 LFS，语义更灵活（本地 working copy 可选择哪些内容实际取到本机），但门槛高、依赖 symlink。
- **Dropbox / BitTorrent Sync**：对"小团队 + 合作，一致性要求不硬"是实用绕路；Supnik 自述团队正用 Dropbox 处理非正式传递。
- **Plastic SCM / Alienbrain / Multiverse**：各有市场，通用性弱于 Perforce。

## 为什么"集中式 + lock"在艺术资产里是特性不是 bug

一位评论者把 Perforce 的 centralization + lock 当缺点，Supnik 反驳得非常清楚，值得记住：

- **艺术团队技术光谱分布很宽**——有的能用 GIT，有的只能用最简 GUI。DVCS 的心智模型（branch / merge / rebase / cherry-pick）对某些成员就是认知负担。
- **很多格式无法 merge**——多人同时改同一个 `.psd` 不是可 resolve 的冲突，是"其中一个必然会被舍弃"。Lock **强制沟通前置**——在你开始动之前必须先和下一位候选人碰一下，这本来就是要发生的协调。
- **源码需要分支灵活，资产需要"别同时动"**——两种需要对应两种工具，强行统一反而两边都别扭。

这和 [[stl-not-abstraction-prescription|"抽象不是处方"]] 的精神同根：**"艺术家也应该用 DVCS"是一种对均匀的错误渴望**，真正的解耦是让两种工作流各自保留最佳工具、在同一仓库里通过 Git Fusion / submodule 之类的桥接机制拼起来。

## 关键约束：版本化 + 分支是硬需求

帖子下方有人问："艺术资产真的需要回退旧版本吗？"Supnik 用 X-Plane 的具体场景回应——**两者都要**：

- **版本化**——tip 上的最新 King Air 可能是一个半成品 WIP，出 bug fix 补丁时必须能拉"上次发布过的"版本；
- **分支**——对所有 in-progress 飞机应用一个跨文件的微调（比如 FM 系数重存）时，如果没法分支就得等所有飞机做完当前改动才能上线补丁。

纯 Dropbox 没法满足这两条，这是艺术资产必须有真正 VCS 的底线。

## 什么时候对策是"每个包一个 repo"

评论中一位飞行模拟开发者说他们把每架飞机独立 repo。Supnik 回应 X-Plane 移动端就是所有飞机一个 GIT repo——**被拖死**。每包一 repo 的代价是"meta 层面（包清单、版本管理）还是要你自己写一个"，等于把 Supnik 提的 manifest 方案换皮实现。

## 相关
- [[asset-exchange-format-strategy]]
- [[game-resource-pack-format]]
- [[xlsx-text-versioning]] —— 另一种"把二进制塞进 VCS 之前先搞清楚它能不能 diff"的反面案例
- [[resource-reference-path-vs-guid-vs-name]]
- [[stl-not-abstraction-prescription]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-source-control-art-assets]]
- [[sources/c0de517e-vcs-next-gen]] —— Pesce 2011 给「下一代」艺术资产 VCS 开的 wishlist（CoW 文件系统 + 依赖驱动 sync），是 Supnik 2015 gap 分析的早期前身
