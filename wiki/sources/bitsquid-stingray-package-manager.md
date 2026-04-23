---
tags: [source, bitsquid, stingray, 构建系统, 包管理]
date: 2026-04-19
sources: 1
---

# Introducing the Stingray Package Manager (spm)（Niklas Frykholm / Bitsquid）

[[niklas-frykholm|Niklas Frykholm]] 2016 年 1 月的一篇工具介绍——把 Stingray 自家用 Ruby 写的包管理器 `spm` 公开讲了一遍。是 Bitsquid **one-button build** 哲学落到外部依赖这一层的具体实现。

## 摘要

开篇解释动机：**一条命令 build 任何 commit、任何平台、任何配置组合**。这件事对新人上手、build farm、bisect、老版本 bug 修复都极关键；更本质的理由是 Niklas 反复强调的——**简单性是编程的首要美德**，少一件装进大脑的事就是大胜利。

`spm` 只负责一件事：**按 hash 精确版本拉 external artifact**。它有三条硬约束：(1) 版本 hash 锁定，同 git commit 必得同 artifact；(2) 最小下载，只拉当前 target 需要的；(3) 本地缓存可按时间或容量裁。这三条合起来是"为什么 `git-lfs` 不够"的回答——LFS 不做 platform filtering 也不做 LRU cache。

实现细节若干：artifact 源可插 S3 / Artifactory / git；artifact 配置写在 JSON / SJSON 文件里（groups / platforms / lib 目录名 / version hash / source 参数）；升级一个库就是改 hash + check in。命名不带 hash（`luajit-2.1.0-windows` 而非 `luajit-2.1.0-windows-y0dqqY...`），代价是不能并行安装多版本、`spm` 要自己维护"文件夹 → hash"映射——Niklas 自评这个决策"不一定对"。`cmake` 本身也由 `spm` 装，bootstrap 进一步；但 Ruby、VS、平台 SDK 仍需手装——最后一公里还没闭合。Bitsquid 构建三件套：`make.rb`（前端）+ `spm`（拉依赖）+ `cmake`（生成工程 + 编译）。

评论区同行（Julien）分享自家版本：用 svn 做 artifact 存储，build server 上跑 → 解决了 SDK / 授权问题，也省掉了手装步骤。大家共同承认的设计张力：**unique name vs 可读 name**、**客户端 cache vs build server cache**、**bootstrap 多彻底**。

## 关键要点

- 目标是 **zero-configuration bootstrap**——一个 sync + 一条命令就能跑；目前卡在 Ruby / VS / 平台 SDK 的最后一公里。
- `spm` 负责 artifact，`make.rb` 负责 orchestrate，`cmake` 负责编译——**职责单一、工具拼接**的构建系统版。
- artifact 版本用 **hash 精确锁定**，保证 build 可复现。
- **MRU 缓存按时间或容量剪枝**——切分支不重下，磁盘不膨胀。
- **文件夹不带 hash** 是风格选择，可读 vs 可并存之间的取舍；`spm` 自己维护 folder → version 索引。
- `cmake` 自举 by `spm`，但 Ruby 和 VS / 平台 SDK 仍要手装——真正的零配置很难，因为授权软件不能放公共 repo。
- `git-lfs` 不能替代：少了 platform filtering 与客户端 LRU。
- 借鉴 `npm` / `gem` 的子命令 UX（`install` / `uninstall` / `install-group`），游戏引擎工具链也可以是"像管理 node_modules 一样管理 console SDK"。

## 链接到的概念

- [[stingray-package-manager]]
- [[data-driven-architecture]]
- [[stingray-data-driven-render-config]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2016/01/introducing-stingray-package-manager-spm.html
- 本地：`raw/articles/bitsquid.blogspot.com/2016-01-20_introducing-the-stingray-package-manager-spm.md`
