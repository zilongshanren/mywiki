---
tags: [source, devops, testing, ci, cost-optimization]
date: 2026-04-19
sources: 1
---

# Waiting on Tests（Evan Todd, 2024-01）

[[evan-todd]] 2024 年 1 月在博客发表的 DevOps 随笔。作者在 [StrongDM](https://strongdm.com) 把自动化测试从零做到 56,343 条的过程中，观察到测试跑得慢才是最大的生产力杀手，于是用一晚上的 Jupyter Notebook 把 CI 的 AWS Auto-Scaling Group 调优问题变成了一道最优化题。

## 摘要

作者先抛出一个反直觉观点：自动化测试**主要价值不是发现 bug**，而是加速开发——所以慢测试就等于自我否定。九月份那次测试运行 11 个并行任务，快的等 5 秒，慢的要等 45 秒，原因是 Auto-Scaling Group 里的热机器只有 4 台，其余任务要等冷启动（克隆 Git 仓库 + 拉 Docker 镜像 + 空的 Go build cache，合计 3 分钟以上）。作者把 ASG 两个旋钮——最小实例数和 idle 超时——建模成优化变量，用 Cloudwatch "Desired instance count" 分钟级数据当输入，在 Jupyter 里用 numpy 数组暴力枚举所有组合，定义"效率 = -(成本 + 冷启动数)"作为目标函数，配合 `ax.imshow()` 画热力图找到最优解。结论出人意料：把最小实例数从 4 提到 11（正好等于最常见测试套件的 job 数），成本几乎不变，冷启动砍半。配合 `c5ad.4xlarge` AMD 机型替换、Docker 镜像合并、S3 缓存 `node_modules`、Buildkite 并行拆 job 等组合拳，测试时长从 12-15 分钟压到 5 分钟以内。

## 关键要点

- 自动化测试的首要价值是"让已经 work 的东西继续 work"，在判断**新**功能是否正确时它的优势比手工 QA 只多一点点。
- 慢测试比少测试更致命：它直接延长开发循环。
- 冷启动成本由 git clone、Docker pull、空编译缓存构成，对 CI 机器尤其贵；本地 SSD 比 EBS 快很多，但要显式挂载。
- "把 ASG 最小实例数拉到最常见测试套件的 job 数"是反直觉但最优的策略——因为你本来就在等最慢那一个 job。
- Jupyter Notebook + 一份 Cloudwatch JSON 导出足够做正经的容量规划，不需要真的去读论文。
- Python 简单暴力枚举：`[[timeout for timeout in range(30)] for min_instances in range(25)]`，每格算一次目标函数，画 heatmap 就能看最优点。
- 分享渠道用 GitHub Gist：代码、数据、图像三合一。

## 链接到的概念

- [[ci-cost-optimization-asg]]
- [[tools-first-iteration-loop]]
- [[latency-vs-throughput]]

## 原文

- 链接：https://etodd.io/2024/01/01/waiting-on-tests/
- 本地：`raw/articles/etodd.io/2024-01-01_waiting-on-tests.md`
