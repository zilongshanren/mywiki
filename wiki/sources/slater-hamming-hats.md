---
tags: [source, 数学, 错误纠正, 线性代数, 谜题]
date: 2026-04-14
sources: 1
---

# Hamming Hats（Max Slater）

[[max-slater|Max Slater]] 2022 年 3 月发表的数学短文，把 CMU 15-251 的经典「31 人帽子谜题」**完全用线性代数和 Hamming 校验矩阵解决**——并证明这套策略达到所有可能策略的理论上界。

## 摘要

谜题：$n$ 人各戴红/蓝帽子（独立公平硬币），互相能看见对方的帽子但看不见自己的；游戏开始后禁止交流，所有人 **同时** 要么宣布自己的颜色要么弃权。**至少一人猜对、且无人猜错** 全员胜。朴素策略（指定一人永远猜红）赢 50%。Slater 用 Hamming $(n, n-r)$ 码（$n = 2^r - 1$）把胜率推到 $\frac{n}{n+1}$，对 $n = 31$ 是 $\approx 96.875\%$。

技术核心是把游戏状态写成 $\mathbb{F}_2$ 上的 $n$ 比特字。每个玩家按编号知道 $n - 1$ 比特，构造两个候选状态（自己戴红 / 戴蓝），分别乘 Hamming 校验矩阵 $H$。文章证明三件事：(1) 任意两个 Hamming codeword 距离 $\ge 3$；(2) Hamming 码 **完美打包**——每个非 codeword 唯一对应一个 1 比特错位的 codeword；(3) 当真实状态不是 codeword 时，恰好一个玩家会发现「翻自己那位 → codeword」并自信宣布正确颜色，其他人弃权——团队赢。当真实状态恰是 codeword 时，所有人误以为「翻自己那位 → 非 codeword」，全员宣布错误颜色——团队输。胜率 = 非 codeword 占比 = $\frac{n \cdot 2^{n-r}}{2^n} = \frac{n}{n+1}$。

最后用「每个玩家在所有状态下猜对/猜错次数相等」的对称性证明：**任何策略** 都满足 $L \ge W / n$，故胜率上界 $\frac{n}{n+1}$——Hamming 策略最优。

## 关键要点

- **每个非 codeword 唯一对应一个最近 codeword**（perfect packing）是 Hamming 码的核心几何性质，胜率证明的关键。
- **校验矩阵的列就是 1..n 的二进制表示**，所以 $Hz$ 直接给出错位 index——这是 Hamming 码 1-bit 纠错能力的来源。
- **「赢局只需一个人对、输局所有人错」** 的「不对称使用错误」是策略上界的本质。
- **Hamming 策略仅在 $n = 2^r - 1$ 时存在**。其他 $n$ 是否「忽略多余玩家、跑次大 Hamming 策略」是开放问题。
- 整个证明完全在 $\mathbb{F}_2$ 上，是「线性代数 + 概率」如何在意想不到的地方相遇的优美样本。

## 链接到的概念

- [[hamming-code-hat-puzzle]]
- [[probabilistic-algorithms]]
- [[fast-exponentiation]]
- [[max-slater]]

## 原文

- 链接：https://thenumb.at/Hamming-Hats/
- 本地：`raw/articles/thenumb.at/2022-03-29_hamming-hats.md`
