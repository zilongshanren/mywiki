---
tags: [计算机系统, 构建系统, 包管理, stingray, bitsquid]
date: 2026-04-19
sources: 1
---

# Stingray Package Manager（spm）

`spm` 是 Stingray 自带的一个小型 Ruby 包管理器，负责**把 external artifacts（第三方库、SDK、示例资源）按 commit 精确版本拉到本地**，是 Bitsquid **one-button build** 哲学的一根承重柱。Niklas 在 2016 年 1 月把它单独拿出来写，是因为游戏引擎常年被"一键构建"这件事折磨：新人跑不起来、build farm 一坏就半天、老版本 bug 复现要靠猜环境——`spm` 就是把这些疼点一次性压住的工程产物。

## one-button build 的门槛

目标定义清晰：**一条 console 命令**就能 build 任何 commit 的引擎与工具链；平台（PC/XB1/PS4/iOS/Android/WebGL）、配置（debug / development / release）、选项（Steam / Oculus / AVX）任意组合都得工作。Niklas 给出的理由不是"省几分钟"，而是"少一件要装进大脑的事"——**简单性是首要美德**，越少的环境假设就越少的 context switch。

## spm 的职责

它不管源码（git 管）、不管编译（`cmake` 管），只管**"这个 commit 需要哪几版 artifact，把它们拉下来并铺进本地 lib 目录"**。三条硬约束：

1. **版本按 hash 精确锁定**。某个 git hash 永远对应同一批 artifact hash，build 结果可复现。
2. **最小下载**。artifact 动辄几百 MB（压缩后），只拉当前 target 需要的。
3. **缓存可控**。切分支不能每次重下，但也不能把磁盘塞满——MRU 缓存按时间（"一个月没用的丢"）或按容量（"留最近 10 GB"）裁。

这三条合起来解释了"**为什么 `git-lfs` 不够**"：LFS 不提供按 target 过滤的部分下载，也不提供基于 LRU/size 的本地缓存策略。

## 实现要点

- **artifact 源可插拔**：S3、Artifactory、Git 任选；配置段里写好 bucket/key 即可。
- **命名不唯一**：文件夹名 `luajit-2.1.0-windows` 不含 hash——更可读、切版本时 build script 不用改目录。代价是不能并行装两个版本、`spm` 要自己维护 "文件夹 → 真实 hash" 的索引。Niklas 自评这个选择"不一定对"，但暂时没有压力换。
- **JSON/SJSON 描述**：每个 library 声明 `groups`（`engine`、`editor` 等）、`platforms`、`lib` 目录名、`version` hash、`source` 配置。升级一个库 = 改 hash + check in。
- **组安装**：`spm install-group -p xb1 engine` 只拉 XB1 engine 需要的东西。并行下载 + 命令行进度条。
- **自举**：`cmake` 本身也由 `spm` 安装；但 Ruby、VS、平台 SDK 仍要手装——最后一公里还在。

## 和其他方案的关系

Niklas 明说借鉴了 `npm`、`gem` 的子命令风格（`install` / `uninstall` / `install-group`）。社区评论里有同行（Julien）用 svn 存 artifact 并在 build server 里做下载，省掉了手装步骤，代价是并发访问控制全压在 svn 上。评论里大家共同承认的设计张力是：**unique name vs 可读 name**、**本地缓存 vs build server 缓存**、**bootstrap 多彻底**。

## 和 Bitsquid 整条构建链的关系

- **前端**：`make.rb` 解析命令行（target / config / 选项），算出"本次需要哪些库"，调 `spm`，再调 `cmake`。
- **`spm`**：只负责 artifact 下载 / 缓存 / 解压。
- **`cmake`**：生成 IDE 工程 / 执行编译。

这个三件套是 Niklas 的 **[[page-granular-system-allocator|"小工具协作、各管一块"]]** 组合拳的构建系统版。

## 相关

- [[data-driven-architecture]]
- [[stingray-data-driven-render-config]]
- [[niklas-frykholm]]
- [[page-granular-system-allocator]]

## Sources

- [[sources/bitsquid-stingray-package-manager]]
