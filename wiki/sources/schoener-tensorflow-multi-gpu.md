---
tags: [source, machine-learning, distributed-training, gpu, tensorflow, historical]
date: 2026-04-19
sources: 1
---

# TensorFlow - Multi GPU Computation（Sebastian Schöner）

[[sebastian-schoener]] 2017 年 12 月发表的 TF1 多 GPU 训练实践教程，内容覆盖单机多卡 **in-graph replication** 和跨机 **distributed TensorFlow**。

## 摘要

文章开篇先把并行化的两个轴拆清楚：**切分方向**（模型水平切片 vs 模型垂直切片/replicated）和**同步机制**（in-graph vs between-graph、synchronous vs asynchronous）。作者站队 replicated training——加设备不改模型，代价只是 gradient 需同步。接着展示单机多 GPU 的 **tower 模板**：controller device（通常 CPU）保存所有 variable，每个 GPU 跑一份 model copy 计算 forward/backward，`compute_gradients` 结果汇到 controller 做平均再 `apply_gradients`。核心工程技巧：`assign_to_device` 回调把 variable 强制路由到 controller、`variable_scope.reuse_variables` 让 tower 共享权重、`tf.layers.*` 里**必须显式命名**否则 scope 不会复用。作者强调并行性**应是训练过程的属性而非模型的属性**——这正是 `minimize` 被拆成 `compute_gradients`/`apply_gradients` 的原因。跨机部分介绍 cluster spec（ps jobs + worker jobs）、`replica_device_setter`、`MonitoredTrainingSession`（包掉 checkpoint/summary/failure recovery）、chief worker 与 master。最后给出 single/2 GPU in-graph/2 worker distributed 的实测吞吐，提醒读者：小模型里通信开销会盖过并行收益，分布式在单机上通常劣于 in-graph。

## 关键要点

- **replicated training** 赢在可组合性，加 device 不改模型
- 单机多卡 → in-graph；跨机 → distributed；大集群常见「两层套」
- **tower 模板**：controller 存变量 + 每卡一份 model + gradient 平均 + apply
- 同步批量 ≈ 等效放大 mini-batch，需要相应调高 lr
- 异步吞吐更高但略劣化收敛
- 吞吐并非线性伸缩（教程实测 2.7×/3 GPU 已不错），常见瓶颈：数据加载、PCIe、CPU aggregate
- `CUDA_VISIBLE_DEVICES` 必须手动隔离，多 TF instance 默认抢光显存
- **StagingArea**：GPU 等新权重时可预取下一批数据（对应今天的 `prefetch_to_device`）

## 陈旧警告

- API 全部是 TF 1.x，今天对应 `torch.distributed`/DDP、`jax.pmap`、`tf.distribute.Strategy`
- `tf.contrib.staging.StagingArea`、`tf.train.MonitoredTrainingSession` 已废弃
- 但**思想层映射仍有效**：tower ≈ rank，gradient 平均 ≈ `all_reduce(SUM)/world_size`

## 链接到的概念

- [[multi-gpu-training-replication-patterns]]
- [[tensorflow-1-graph-model]]
- [[latency-vs-throughput]]

## 原文

- 链接：https://blog.s-schoener.com/2017-12-15-parallel-tensorflow-intro/
- 本地：`raw/articles/blog.s-schoener.com/2017-12-15_tensorflow-multi-gpu-computation-sebastian-schoner.md`
