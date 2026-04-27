---
tags: [machine-learning, distributed-training, parallelism, gpu, tensorflow, historical]
date: 2026-04-19
sources: 1
---

# 多 GPU 训练的复制模式

Sebastian Schöner 2017 年的 TF1 多 GPU 教程里提出的几组**与框架无关**的抽象，时至今日仍是 data parallel 训练的骨架——只是今天的 PyTorch DDP、DeepSpeed、Horovod、`torch.distributed` 把同样的机制包装得更干净罢了。

## 切分方向：水平 vs 垂直 vs 复制

并行一个模型至少有两条路：

- **水平切片（horizontal / model parallel）**——不同 device 负责网络的不同层。好处：每个 device 有更多显存放下更大 mini-batch。坏处：切点需要专门设计，流水线难平衡。
- **垂直切片（vertical / replicated training）**——每个 device 都持有**完整模型**，各自跑一块数据。等价于把 mini-batch 扩大到 `N × batch_size`。
- **Schöner 的共识，也是今天的默认**：**replicated 几乎总赢**——加 device 不用重新切模型，代价只是**权重必须在 device 间同步**。

（2017 年后 model parallel 在 175B+ LLM 时代重新重要起来，但那是**除了** data parallel 之上再叠加的维度。）

## 同步方式：in-graph vs between-graph

同一台机器多 GPU 通常用 **in-graph replication**：一个 TF instance，CPU 作 **controller device**（或称 parameter server, PS）存储变量，每个 GPU 做一份模型副本（**tower**）跑前向+反向，gradient 汇回 controller 做平均并应用。

多机则用 **between-graph replication / distributed TF**：每台机器跑独立的 TF instance，显式声明 **cluster spec**：`ps` jobs（参数服务器）+ `worker` jobs；通过 `tf.train.replica_device_setter` 自动把变量放在 PS 上、op 放在 worker 上。

## Tower + 平均梯度模板

这是 TF1 手写多 GPU 训练的经典骨架（在 PyTorch DDP 里被 `all_reduce` 自动接管）：

1. 拿到可用 device 列表。
2. 对每个 device：在对应 `tf.device` 下构造一份模型（**tower**），把 variable 的创建强制路由到 controller（`assign_to_device` 技巧）。第二个 tower 起调用 `variable_scope.reuse_variables()`——**必须共享权重**。
3. 每个 tower 调 `optimizer.compute_gradients(loss)` 得到 `[(grad, var), ...]`，不 apply。
4. 在 controller device 上把所有 tower 的 gradient **逐变量求平均**（`average_gradients`），再调 `optimizer.apply_gradients`。

作者特意指出：**并行不应是「模型的属性」而应是「训练过程的属性」**——这解释了为什么 `minimize` 要拆成 `compute_gradients` + `apply_gradients`：因为并行策略必须知道 optimizer 的结构。这个判断后来成为 PyTorch `DistributedDataParallel` 和 JAX `pmap` 的共同默认。

## 同步 vs 异步

- **同步（sync）**——所有 worker 等齐再更新；等价于 mini-batch 放大 `N` 倍。每个 step 进度慢，但梯度估计更准；需要配合调高 learning rate。
- **异步（async）**——worker 互不等待，各自把 gradient 推给 PS。吞吐更高，但「每个 worker 读到的权重版本略有不同」，在某些任务上会轻微劣化收敛质量。

## 六个 pitfall（与现代训练仍然适用）

- **不会线性加速**——2.7× / 3 GPU 已经算不错；瓶颈通常在梯度聚合、PCIe 传输、CPU 数据预处理。
- **数据必须跟得上**——Dataset 里 `map(..., num_threads=...)` 给足并行度，否则 GPU 挨饿。对应今天的 `torch.utils.data.DataLoader(num_workers=)`。
- **Controller 选 CPU 还是 GPU**——如果 GPU 之间有 peer-to-peer（NVLink / 同一 box），controller 放一张 GPU 上梯度平均更快；否则不如放 CPU。
- **GPU 在等新权重时能干嘛**——如果有 data augmentation，可以预先 augment 下一 batch；`StagingArea` 就是为此发明的。今天的 `prefetch_to_device` 同理。
- **`CUDA_VISIBLE_DEVICES`**——每个 TF instance 默认会抢光所有 GPU 显存，多进程跑必须手动隔离。PyTorch 里同样问题同样对策。
- **distributed 不总是比 in-graph 快**——单机双卡跑 distributed 反而因进程间通信变慢。**single-machine 多卡优先 in-graph，跨机才上 distributed**，大集群的常见套路是「每机 in-graph + 跨机 distributed」两层。

## 与今天的映射

| 2017 TF1 概念 | 2026 对应 |
|---|---|
| tower / replica | DDP rank / JAX pmap axis |
| controller / parameter server | `all_reduce` / ZeRO shard |
| `assign_to_device` + `variable_scope.reuse` | `DDP` 自动广播 + `nn.Parameter` 共享 |
| `average_gradients` | `all_reduce(SUM) / world_size` |
| `MonitoredTrainingSession` | `torch.distributed.elastic` / `lightning.Trainer` |
| `StagingArea` | `prefetch` / `pin_memory` |

思想层几乎没变；工程层被大幅自动化。

## Sources

- [[sources/schoener-tensorflow-multi-gpu]]
