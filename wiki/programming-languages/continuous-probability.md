---
tags: [数学, 概率, 蒙特卡洛, 随机变量]
date: 2026-04-14
sources: 1
---

# 连续概率速成

**连续概率** 是蒙特卡洛方法的数学前置。把离散世界里的 PMF/求和换成连续世界里的 PDF/积分，看似形式上微调，但概念上发生了一次真正的切换——「单点概率」不再有意义，**密度**取代了**质量**。这个切换是后续 [[quasi-monte-carlo|QMC]]、重要性采样、球面积分、路径追踪等所有内容的起点。

## 从质量到密度

离散随机变量 $X$ 用**概率质量函数**（PMF）$f_X(x) = \mathbb{P}\{X = x\}$ 描述，所有值加起来等于 1。「质量」这个比喻很直白：总质量 = 1，按各个可能结果切分。

连续随机变量 $Z$ 就不能这么干——不可数多的结果，如果每个都给非零概率会得到无限总和，所以**任一特定结果的概率必须为零**。$\mathbb{P}\{Z = 0.5\} = 0$，但 $Z$ 依然要返回*某个*结果。

破解矛盾的办法是把视角从质量换成**密度**。物理意义上，密度是单位体积的质量；这里是「单位结果上的概率」。要得到一段区间 $[z, z+h)$ 的概率，我们计算

$$ f_Z(z) = \lim_{h \to 0} \frac{\mathbb{P}\{z \le Z < z+h\}}{h} $$

这就是**概率密度函数**（PDF）。要得到任意区间的概率，对 PDF 积分即可；积分到整个定义域必须等于 1。

## CDF 是 PDF 的原函数

**累积分布函数**（CDF）$F_Z(z) = \mathbb{P}\{Z < z\}$ 是一个不管离散还是连续都成立的工具。在连续情形下，PDF 恰是 CDF 的导数：$f_Z = F_Z'$，反过来 $F_Z = \int_{-\infty}^z f_Z$。CDF 的重要性体现在**反函数采样**上——想从 $Z$ 采样一次？抽一个 $u \sim U[0,1]$，算 $F_Z^{-1}(u)$ 即可。

## 联合分布与边缘化

二维情况给出**联合 PDF** $f_{X,Y}(x,y)$。对某一维积分可以「边缘化」出另一维的 PDF：$f_X(x) = \int f_{X,Y}(x,y)\,dy$。

两变量**独立**当且仅当 $f_{X,Y}(x,y) = f_X(x)f_Y(y)$，记作 $X \perp Y$。不独立时需要**条件分布**：$f_{Y \vert X=x}(y)$ 描述「已知 $X = x$ 时 $Y$ 的分布」，它不是 $f_{X,Y}$ 的切片本身，而是切片归一化之后的结果。

## 期望：PDF 加权求和

$\mathbb{E}[X] = \int x\,f_X(x)\,dx$。更一般地，对一个函数 $g(X)$：

$$ \mathbb{E}[g(X)] = \int g(x)\,f_X(x)\,dx $$

这一式子是**蒙特卡洛积分的核心**——如果我们想估计 $\int g(x)\,dx$，就人造一个 pdf $p(x)$，把积分改写成 $\mathbb{E}_p\left[\frac{g(X)}{p(X)}\right]$，再取 $N$ 个样本求均值。

**期望是线性的**，对依赖随机变量也成立：$\mathbb{E}[X+Y] = \mathbb{E}[X] + \mathbb{E}[Y]$。这就是为什么路径追踪可以把一整条路径的贡献拆成独立项来估计。

## 方差、协方差与概率上界

**方差** $\mathrm{Var}[X] = \mathbb{E}[(X - \mathbb{E}[X])^2] = \mathbb{E}[X^2] - \mathbb{E}[X]^2$，衡量散布程度。标准差 $\sigma = \sqrt{\mathrm{Var}[X]}$ 是更直观的距离感。

方差**不是**线性的：$\mathrm{Var}[X + Y] = \mathrm{Var}[X] + \mathrm{Var}[Y] + 2\,\mathrm{Cov}[X,Y]$，只有独立变量协方差为 0 时才可加。注意**零协方差不蕴含独立**——它只是线性相关为零。

**Markov 不等式**：对非负 $X$，$\mathbb{P}\{X \ge a\} \le \mathbb{E}[X]/a$。证明只需反证——如果超过这个比例，单独该事件就已让期望超过 $a \cdot \mathbb{E}[X]/a = \mathbb{E}[X]$。

**Chebyshev 不等式**：$\mathbb{P}\{|X - \mu| \ge k\sigma\} \le 1/k^2$，把 Markov 套在 $(X - \mu)^2$ 上立即得到。对更强的 high-probability 界（随机算法里常用）则要看 **Chernoff bound**，它 bound 的是 $e^X$。

## Dirac delta：离散和连续的连接

Dirac delta $\delta(x)$ 不是一个普通函数——它在 $x \ne 0$ 时为零，但满足 $\int\delta = 1$。作用是把**离散分布也装进连续的 PDF 语言**：

$$ f_X(x) = 0.5\,\delta(x) + 0.5\,\delta(x - 1) $$

描述一枚公平硬币。混合分布也可以这么写：「50% 返回 0，否则均匀 $[0,1]$」= $0.5\,\delta(x) + 0.5$（限制在 $[0,1]$ 上）。这套记号在图形学里特别有用——完美镜面 BRDF 本质上就是 delta 分布，把它和漫射项放进同一个积分是靠 delta 才能自洽。

## 定位

本文是 [[max-slater|Max Slater]] *Monte Carlo Crash Course* 的**第一章**，为后续章节做记号与概念铺垫：

- 第 2 章：从期望线性性推出蒙特卡洛估计器、大数律、方差 $\propto 1/N$ 收敛。
- 第 3 章：采样技术（逆变换、拒绝、重要性采样、Metropolis）。
- 第 4 章：渲染积分案例研究。
- 第 5 章：见 [[quasi-monte-carlo]]。

## 相关

- [[quasi-monte-carlo]] — 系列第 5 章，建立在这些基础之上
- [[spherical-integration]] — 同一套变换坐标的语言
- [[probabilistic-algorithms]] — 用概率换可行性
- [[automatic-differentiation]] — 另一篇数学向铺陈风格的 Slater 文
- [[functions-as-vectors]]
- [[max-slater]]

## Sources

- [[sources/slater-continuous-probability]]
