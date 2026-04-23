---
tags: [source, machine-learning, tensorflow, deep-learning, historical]
date: 2026-04-19
sources: 1
---

# TensorFlow - An Introduction（Sebastian Schöner）

[[sebastian-schoener]] 2017 年 12 月发表的 TensorFlow 1.3 入门教程，原文是 Jupyter notebook，从安装讲到训练 MNIST CNN、checkpoint 保存、TensorBoard 监控一整套。

## 摘要

教程的价值不在具体 API（TF 1.x 的 `tf.Session`、`placeholder`、`feed_dict`、`tf.contrib.data` 今天全已被 TF 2.x 的 eager + `tf.function` 取代），而在**两段式建图-执行模型**本身的清晰阐释：Python 代码只是往默认 graph 里挂节点（每个 tensor 有静态 shape/dtype/name），`sess.run(fetches, feed_dict)` 时 TF 才回溯依赖实际计算。介绍了图里的三类公民——*placeholder*（图里的洞）、*variable*（跨 run 的持久状态，必须显式初始化）、*optimizer*（自动加反向与 assign 节点）。随后用 MNIST + tf.layers 搭了一个双层 CNN，并展示了 TF 1.3 新增的 Dataset API（`from_tensor_slices → shuffle → map → batch → repeat`，带多线程 `map`），主张用 graph 内的 iterator 取数据来省掉 `feed_dict` 的 Python/C++ 序列化开销。checkpoint（变量值）与 metagraph（图的 protobuf）两种保存机制作者明确建议只存 checkpoint，metagraph 用 Python 源码取代。教程以 TensorBoard summary 收尾。

## 关键要点

- **build graph vs run session**：调 Python 函数 ≠ 运算，只在挂节点；这是所有现代 ML 框架和 graph IR 的思想原型
- 三类一等公民：placeholder（入口）、variable（跨 run 状态）、optimizer（会自动加微分 op）
- Dataset API 让数据流进 graph 内部，Python 边界开销显著下降
- checkpoint 存权重，metagraph 别用——代码才是 source of truth
- TensorBoard 以 summary op 的形式嵌在 graph 里，通过 `FileWriter` 定期 flush

## 陈旧警告

- `tf.Session` / `placeholder` / `feed_dict`：TF 2.x 已移除或隐藏
- `tf.contrib.*` 整个命名空间已被废弃
- `tf.reset_default_graph`、`global_variables_initializer`：eager 模式下不再需要
- Python 2.7 + TF 1.3：早已过时
- 建议把这篇当**思想史**读，不要按 API 抄代码

## 链接到的概念

- [[tensorflow-1-graph-model]]
- [[multi-gpu-training-replication-patterns]]
- [[automatic-differentiation]]

## 原文

- 链接：https://blog.s-schoener.com/2017-12-12-tensorflow-intro/
- 本地：`raw/articles/blog.s-schoener.com/2017-12-12_tensorflow-an-introduction-sebastian-schoner.md`
