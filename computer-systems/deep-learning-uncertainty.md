---
tags: [machine-learning, uncertainty, bayesian, calibration, deep-learning]
date: 2026-04-19
sources: 1
---

# 深度学习里的「不确定性」到底是什么

Sebastian Schöner 2017 年写的一篇思辨文：在产品里谈「模型的不确定性」是个**被严重滥用的词**，不同语境下其实指向完全不同的数学对象。这页把他梳理的分类做一次简明总结。核心结论：**没有任何一个当下的工具能让工程师放心地「知道自己不知道什么」**；与其迷信 uncertainty API，不如把精力花在「收集更能代表部署分布的数据」上。

## 两条路线的分岔

### 路线 A：实务视角（frequentist）

> **我想要的是：网络告诉我它的某个预测对不对的概率。**

形式化成：若网络以 $p$ 的 softmax 分数预测某类，则它确实在 $p$ 比例的时间里命中——这叫 **calibration**。

- **calibrated network**：softmax 输出和实际准确率一致。
- 大型网络**通常 overconfident**（把 0.6 正确率的样本说成 0.95）；小网络反而天然较准。
- 可视化工具：**calibration plot**（softmax 分数 vs 实际准确率），理想是对角线。量化：**ECE（expected calibration error）**。
- calibration 可以用温度 scaling、isotonic regression 等后处理方法修正（见 Guo et al., 2017）。

**calibration 的致命局限**：它只在**训练分布内**有意义。一个只学过「猫 vs 狗」的网络遇到大象，给出的 softmax 本质上是无意义的随机数。任何**从训练集里学出来**的 uncertainty 估计都有这个天花板。

### 路线 B：OOD 检测（实务视角的补救）

既然分布内 calibration 不够，就加一个「这个输入是否 out-of-distribution」的判别器：

- **简单法**：对每类 pre-softmax activation 拟合 Gaussian，输入落在 3σ 外就拒。问题：真实 activation 分布不是 Gaussian；网络还可能把噪声输入映射到正常训练样本的同一表示。
- **softmax thresholding**（Hendrycks & Gympel, 2016）：观察到错分/OOD 样本的 max softmax 确实偏低，直接阈值分。作者评语：*能用，但没有道理能用*——是在吃训练集的一种副产品。
- **autoencoder 重建误差 / GAN discriminator**：把输入分布本身学出来再判别。
- **COOL**（Kardan & Stanley, 2016）：每类给 $\omega$ 个 softmax 单元、训练时 target 为 $\frac{1}{\omega}$，推理时取单元分数的乘积。靠「同类内部多个弱分类器一致」近似 ensemble 而免付 ensemble 的计算代价。

## 路线 B'：Bayesian 视角（principled）

> **我想要的是：既然参数本身是不确定的，把这份不确定传播到预测上。**

Bayesian Neural Network (**BNN**) 里每个权重都不是一个值，而是一个分布：

1. 选先验 $p(w)$（例如各权重独立 $\mathcal{N}(0, 10^{-3})$——显然是错的假设，但是起点）。
2. 由 Bayes 规则得到后验 $p(w \mid x) = \frac{p(x \mid w) p(w)}{p(x)}$；分母 $p(x)$ 是归一化常数，**这正是 Bayesian 推断困难的根源**。
3. 推断（类比 training）后，要预测某输入：从后验采样多组 $w$，跑出多个预测，看分布。

由此出来三个必须分清的量：

- **parameter uncertainty**（参数不确定性）——后验分布的方差。训练数据越多、通常越小。极端：Dirac 分布 = 零参数不确定性。
- **predictive uncertainty**（预测不确定性）——把参数采样投射到输出空间后的方差。**这才是真正想要的量**。低 parameter uncertainty 蕴含低 predictive uncertainty；反之不然（不同参数可能给同一样本相同答案）。
- **risk**——任务本身的固有随机性，比如抛硬币的 50/50。**再完美的模型也消不掉**；[[probabilistic-algorithms]] 框架下经常看到的「信息论下界」。
- **model mismatch**——模型类**根本不包含**真实过程。参数再准、predictive 再小，也只是精准错答。

作者的 insight：**predictive uncertainty = parameter uncertainty + model mismatch 的残留 + task risk**，这三者需要**分开对待**，实务里却常被混为一谈。

## Monte-Carlo Dropout 的争议

**MC dropout**（Gal & Ghahramani, 2015）：把 dropout 当成变分推断的近似，推理时不关 dropout，采样 50–100 次 forward，看分布方差。便宜且易集成，近十年被大量产品直接当 uncertainty API 使用。

Schöner 对此持**高度保留**态度：Ian Osband（DeepMind, 2016）在一个极简例子里发现 MC dropout 的 predictive uncertainty **不随数据增加而下降**——这违反了「Bayesian 后验随数据集中」的基本直觉。Osband 的解读：**MC dropout 近似的是 risk 而不是 parameter uncertainty**。作者的立场：如果你一定要用，至少把 Gal 原论文读完，留意其隐含假设。

## 实务结论

2017 年的作者（直到今天很大程度仍然成立）：

- 没有一个现成工具值得在生产里无脑推荐为「uncertainty 读数」。
- **最可靠的「不确定性」管理不在模型里，在数据里**：收集能代表部署分布的测试集，用测试表现作为决策依据。
- ensemble 仍是工程上最稳的方案，代价就是训多份模型。
- 如果你把「uncertainty」挂在嘴边，先自问你在说 calibration、parameter variance、predictive variance、risk、OOD 中的哪一个。

## Sources

- [[sources/schoener-dl-uncertainty]]
