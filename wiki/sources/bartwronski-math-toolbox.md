---
tags: [source, math, python, tools, game-programming]
date: 2026-04-27
sources: 1
---

# On Pursuit of Good Free Mathematics Toolbox（Bart Wronski）

[[people/bartosz-wronski]] 发表于 2014 年 1 月的文章，探讨游戏图形程序员在家或出行时需要哪些**免费数学工具**，以及为何 Python + NumPy/SciPy 是 Mathematica 的可行替代品。

## 摘要

作者从图形程序员的工作需求出发：PBR 积分、曲线拟合、函数近似……这些都需要一套方便的数学计算环境。Mathematica 是业界标准（Siggraph Physically Based Shading 课程材料都用它），但有授权费贵、语法陌生、难以与其他工具集成三大缺点。作者推荐 **Python + NumPy + SciPy + Matplotlib** 的组合：NumPy 提供原生代码实现的 n 维数组和线性代数，SciPy 添加优化、数值积分、曲线拟合等高层功能，Matplotlib 做可视化。在 Windows 上用 **WinPython** 发行版可以免安装直接使用，配合 Sublime Text 编辑器写 10–100 行脚本的工作流极为流畅。唯一明显的短板是符号计算（求积分、化简表达式）——sympy 虽然存在但作者当时未深入使用，仍认为 Mathematica 在符号分析上无可替代。

## 关键要点

- NumPy 释放 Python GIL，计算可以轻松多线程；性能与 Matlab/Octave 相当
- SciPy 涵盖 k-means、数值积分、优化、插值、Matplotlib 可视化——一个包搞定图形数学的大多数需求
- WinPython 是 Windows 用户的最佳入门方案：免安装、自带包管理和 Spyder IDE
- 符号分析（积分化简）仍推荐 Mathematica；Python 的 sympy 当时被作者标注为"未验证"
- 作者后续文章会附带 Python 脚本来演示图形数学

## 链接到的概念

- [[faster-math-functions]]

## 原文

- 链接：https://bartwronski.com/2014/01/19/mathematics-toolbox/
- 本地：`raw/articles/bartwronski.com/2014-01-19_on-pursuit-of-good-free-mathematics-toolbox.md`
