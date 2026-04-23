---
tags: [source, machine-learning, uncertainty, bayesian, calibration]
date: 2026-04-19
sources: 1
---

# A few thoughts on uncertainty in Deep Learning（Sebastian Schöner）

[[sebastian-schoener]] 2017 年 12 月发表的思辨长文，把"deep learning 里的 uncertainty"这个被滥用的词拆成实务与 Bayesian 两条线，并表达了对 MC dropout 的保留态度。

## 摘要

作者先提出**实务视角**的 uncertainty：工程师通常想要"网络说 p 的把握则 p 比例的时候答对"——这正是 **calibration**。calibration plot 呈对角线即理想，大网络通常 overconfident，小网络反而准；可用温度 scaling 等后处理修正（Guo et al., 2017）。但 calibration 只在训练分布内有效，遇 out-of-distribution（OOD）完全失灵。他综述了若干 OOD 检测思路：对 pre-softmax activation 拟 Gaussian 后 3σ 拒识（太粗）、max-softmax thresholding（Hendrycks & Gimpel 2016，"能用但没道理能用"）、autoencoder 重建误差 / GAN discriminator、Kardan & Stanley 的 COOL 架构（每类 $\omega$ 个单元）。随后切到 **Bayesian 视角**：BNN 对每个权重放分布，由 Bayes 规则得后验 $p(w \mid x) = p(x \mid w)p(w)/p(x)$，预测时采样权重看输出分布；由此区分出**四个必须分清的量**——parameter uncertainty（后验方差）、predictive uncertainty（投射到输出空间的方差，才是真正想要的）、risk（任务本身的固有随机性，如抛硬币）、model mismatch（模型类不含真实过程）。最后花大篇幅讨论 **MC dropout**（Gal & Ghahramani 2015）：推理时不关 dropout、采样多次看方差。作者引 Osband 2016 指出一个极简例子里 MC dropout 的 predictive uncertainty **不随数据增加下降**，怀疑它近似的是 risk 而非 parameter uncertainty。结论：没有一个现成工具值得在生产里当 uncertainty API 使用；**最可靠的做法是把功夫花在收集能代表部署分布的测试数据上**。

## 关键要点

- "uncertainty" 至少五义：calibration / parameter variance / predictive variance / risk / OOD，不能混用
- calibration **只在训练分布内**有意义
- OOD 检测方法多，但大多是训练副产品的副产品，作者对大多数持怀疑态度
- **parameter uncertainty ≠ predictive uncertainty**；低 parameter 蕴含低 predictive，反之不真
- **risk** 是任务固有随机性，再完美的模型也去不掉
- **model mismatch**：参数再准、模型类错了也只是精准错答
- MC dropout 流行但可疑：Osband 的例子说明它可能近似 risk 而非 Bayesian 后验
- 产品里最好的不确定性管理是**数据集代表性**，不是 uncertainty API

## 链接到的概念

- [[deep-learning-uncertainty]]
- [[probabilistic-algorithms]]

## 原文

- 链接：https://blog.s-schoener.com/2017-12-20-uncertainty-in-dl/
- 本地：`raw/articles/blog.s-schoener.com/2017-12-20_a-few-thoughts-on-uncertainty-in-deep-learning-sebastian-sch.md`
