---
tags: [source, mathematica, tools, rendering-research, numerical-methods]
date: 2026-04-27
sources: 1
---

# Wolfram's Mathematica 101（c0de517e / Angelo Pesce）

[[angelo-pesce]] 发表于 2013 年 10 月的文章，为渲染工程师介绍 Mathematica 作为数据探索和渲染公式验证工具的使用方法。

## 摘要

Pesce 将 Mathematica 定位为渲染工程师的"探索环境"：处理测量 BRDF 数据、验证渲染方程数值积分、推导实时渲染近似公式。文章对比了 Python/Matlab/Octave 等替代方案，认为 Mathematica 在文档一致性、CAS 能力和可视化交互（`Manipulate` + Dynamic cells）上有独特价值。语言核心是符号求值树（非 Lisp 的列表，但有同构性），`=` vs `:=` 的即时/延迟求值区别是最重要的"陷阱"。文章包含一套完整速成示例：模式匹配函数定义、列表操作、矩阵运算、数值积分/最小化/求和、并行化以及 `Compile` 的限制。结尾说明 Mathematica 与 LibraryLink/CudaLink/OpenCLLink 的接口可让其充当模板元编程引擎生成 C/CUDA 代码。

## 关键要点

- 渲染工程场景：BRDF 拟合、渲染方程积分近似、实时模型与离线结果对比——CAS 是辅助工具，不是替代数学理解
- `=` 立即求值，`:=` 延迟求值（`HoldAll` 属性）；`Block` 动态作用域，`Module` 词法作用域；`With` 纯替换规则
- `Manipulate` + Dynamic 单元格实现参数化实时可视化，适合调参近似公式
- 性能路径：列表函数（`Map/MapThread/Fold`）远快于过程式循环；`Parallelize` 可直接并行化列表操作；`Compile` 可生成字节码但有函数支持限制
- Python/Anaconda 在免费和生态上有竞争力，Mathematica 的优势在于"一致性打包"

## 链接到的概念

- [[mathematica-for-rendering]]
- [[numerical-methods-rendering]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2013/10/wolframs-mathematica-101.html
- 本地：`raw/articles/c0de517e.blogspot.com/2013-10-06_wolfram-s-mathematica-101.md`
