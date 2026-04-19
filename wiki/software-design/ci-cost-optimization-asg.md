---
tags: [ci, devops, 成本优化, autoscaling]
date: 2026-04-19
sources: 1
---

# CI Cost Optimization —— 给 Auto-Scaling Group 调两个旋钮

[[evan-todd]] 2024 年初记录的一次 CI 调优：把 StrongDM 的测试 pipeline 从 12–15 分钟压到 5 分钟以内，方法是把 AWS Auto-Scaling Group（ASG）的配置当成一道最优化题，用 Jupyter Notebook 解出来。

## 问题结构

CI pipeline 跑 11 个并行测试 job。观察一次典型运行：快的 job "Waited 5s" 就开跑，慢的 "Waited 45s"。原因是 ASG 只保持最少 4 台 `c5d.4xlarge` 热机器，其它 job 要等新实例冷启动——clone Git 仓库、pull Docker 镜像、空的 Go build cache 合计 3 分钟以上，且首次运行测试更慢。

关键洞察：反正你要等最慢那一个 job 完成，**快 4 台没用，慢 7 台才是瓶颈**。所以应当扩大热机器数量到最常见测试套件所需的 job 数（= 11）。

## 两个旋钮

ASG 可调两个参数：

- **最小实例数**：常驻机器数量（原值 4）
- **Idle 超时**：没新任务时等待多久再关机（原值 10 分钟）

优化目标同时包含"月度成本"和"冷启动次数"。作者把二者加权（1 美元 = 1 次冷启动）求和再取负号，叫 "efficiency"。

## Jupyter 解法

输入：Cloudwatch "Desired instance count" 分钟级时间序列，导出成 JSON。数据粒度刚好每分钟一条，算成本变成对数组求和乘单价：

```python
on_demand_cost_per_minute = 0.768 / 60.0
monthly_cost = sum(time_series) * on_demand_cost_per_minute * 22.0
```

冷启动数是对相邻差分取正值：

```python
cold_starts = sum(1 if ts[i] < ts[i+1] else 0 for i in range(len(ts)-1)) * 22
```

模拟"最小实例数改成 N"：工作时段的点抬升到至少 N。模拟"超时改成 N 分钟"：每个点取后 N 分钟内的最大值。然后暴力枚举 `min_instances ∈ [0,25)`、`timeout ∈ [0,30)` 的 25×30 网格，每格算一次 efficiency，`ax.imshow()` 画热力图找最优。

## 反直觉结论

最优组合是 **min=11, timeout≈10 分钟**——热机器刚好覆盖最常见测试套件，成本与现状几乎相同，冷启动次数砍半。"比 4 台热机器 + 长超时"和"比 0 热机器 + 超长超时"都更好。事后看理所当然：反正你在等最慢那一个 job，省下几台机器的闲置成本换不回一次冷启动的 3 分钟。

## 其它组合拳

单靠 ASG 还不够，同期作者做了一组并行优化：

- `node_modules` 缓存到 S3（`GOCACHE` 缓存到 S3 反而更慢，放弃）
- 最常见测试套件的 job 从 11 合并到 8
- 最长 job 用 [Buildkite parallelism](https://buildkite.com/docs/tutorials/parallel-builds) 再拆
- Docker 镜像合并瘦身
- 换成 AMD 处理器的 `c5ad.4xlarge`，同性能更便宜
- 发现付了钱的物理 SSD 其实没挂载，一直在走 EBS——修好后测试快了不少

这些合力把测试时长压到 5 分钟以内，直接支持了 [[automated-test-philosophy]] 里的 Goal #2（缩短开发循环）。

## 相关

- [[automated-test-philosophy]]
- [[tools-first-iteration-loop]]
- [[latency-vs-throughput]]
- [[evan-todd]]

## Sources

- [[sources/etodd-waiting-on-tests]]
