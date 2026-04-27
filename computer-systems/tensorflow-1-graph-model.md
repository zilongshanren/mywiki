---
tags: [machine-learning, dataflow, graph-compiler, tensorflow, python, historical]
date: 2026-04-19
sources: 1
---

# TensorFlow 1.x 的计算图模型

> 历史说明：本页描述的是 **TensorFlow 1.x**（2017 年前后）的编程模型。TF 2.x 以 eager execution + `tf.function` 取代了显式 `Session`/`placeholder`，以下 API（`tf.Session`、`tf.placeholder`、`tf.contrib.data`、`feed_dict`、`tf.reset_default_graph` 等）**均已过时**。保留这页的价值在于其**模型层的思想**——把「建图」和「执行」分离——它直接影响了 PyTorch、JAX、XLA、ONNX、Triton，乃至今日所有现代 ML 框架与 shader / 编译器 IR 的设计。

## 两段式编程：build vs run

TF1 程序分成两步：

1. **构图（build graph）**：Python 代码执行一遍，*不做任何数值运算*，只是往一个默认 graph 里添加节点（`tf.constant`、`tf.add`、`tf.layers.conv2d`）。节点输出叫 **tensor**——形状、dtype、名字都是静态的（名字形如 `Add:0`，冒号后是 output index）。
2. **执行（run session）**：把 graph 丢给 `tf.Session`，通过 `sess.run(fetches, feed_dict=...)` 触发实际数值计算。TF 会回溯依赖、只执行必要节点。

关键直觉：*调用 Python 函数不等于执行运算*。`x = tf.add(a, b)` 只是挂了一个 op，没有加法发生；`sess.run(x)` 才真的算。这一拆分让 TF 能做 op fusion、device placement、跨机调度、自动微分——和 shader compilation、CUDA graph、MLIR 里的「捕获后编译」完全同源。

## 三类一等公民

- **Placeholder**——图里的「洞」，每次 `run` 通过 `feed_dict` 灌值；天生就是输入。
- **Variable**——跨 `run` 持久化的状态（权重、step counter），必须显式 `tf.global_variables_initializer()` 初始化；`assign` 本身是一个 op，要显式 fetch 才真的写入。
- **Optimizer**——高层抽象，吃一个 loss tensor，自动在图里加反向传播节点和 `assign` 节点，返回一个 `optimization_step` op；`sess.run` 它就完成一次 SGD/Adam step。

## 数据管道：Dataset API（TF 1.3+）

从 1.3 起 TF 引入函数式味道的 `Dataset` API（灵感接近 LINQ / Haskell）：`from_tensor_slices → shuffle → map → batch → repeat`，整条 pipeline 是 **graph 内的 op**，`map(read_image)` 里拿到的也是 tensor 而非 numpy。`make_one_shot_iterator().get_next()` 把数据当作图的一部分取出来，训练循环里不再需要 `feed_dict`——减少了 Python↔C++ 的序列化开销。这是 [[multi-gpu-training-replication-patterns]] 能做到 near-linear 伸缩的先决条件：数据必须能跟得上所有 device 的消耗速率。

## 保存：checkpoint vs metagraph

TF1 模型分两部分保存：

- **Metagraph**——整张 graph 的 protobuf 序列化。作者的建议明确：**不要依赖它**；与其保存不可读的二进制，不如保存重建该图的 Python 代码。
- **Checkpoint**——变量当前值的快照。训练中断续跑就要带上 optimizer 内部变量（Adam 的 beta、moment），推理时可以 drop 掉。

这个**「代码是 source of truth、数据才是快照」**的设计哲学，今天在大模型时代仍然是正确方向。

## 为何写这一页

这页不是给 2026 年读者教 TF1 的，而是提醒以下几点对今天依然有效：

- **Build/run 分离**是 graph IR 思想的原型，看懂它后再看 XLA、Triton、MLIR、ONNX，都会觉得熟悉。
- **`tf.device` + 设备占位函数**的设计预示了今天 PyTorch FSDP、DeepSpeed 的 device mesh。
- **从 placeholder 到 Dataset**的演进，正是 Python→图内化的一般规律：减少宿主语言边界上的开销，数据尽量常驻 accelerator 侧。

## Sources

- [[sources/schoener-tensorflow-intro]]
