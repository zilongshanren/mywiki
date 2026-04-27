---
tags: [testing, rendering, ray-tracing, integration-testing, graphics]
date: 2026-04-27
sources: 1
---

# 渲染器集成测试

离线渲染器和实时渲染器都面临同一个测试问题：怎么知道代码改动没有破坏渲染结果？与通用软件不同，渲染器的「正确性」是一张图，不是一个返回值。这就让测试框架设计有了独特的约束和工具选择。

## 确定性是可测性的前提

测试的基础假设是：**给定相同输入，渲染器总输出完全相同的像素**。这要求渲染器做到彻底确定性——包括多线程下的 RNG 控制、浮点运算的平台一致性、场景数据与 RNG 的解耦（避免一个优化意外改变了另一个子系统的随机序列）。[[psraytracing]] 专门把场景布局 RNG 与渲染 RNG 分开，以保证优化的可测试性。

只要确定性成立，**像素级对比**就是可靠的回归测试手段。

## idiff：逐像素比较工具

[OpenImageIO](https://openimageio.readthedocs.io/) 的 `idiff` 命令行工具是图形测试领域的标准工具：给定两张图，输出 PASS / FAILURE，并可选输出差异热图（`-abs -o diff.jpg`）。

```bash
# 通过案例
idiff reference.png current.png   # → PASS, 退出码 0

# 失败案例（输出均方误差、峰值 SNR、异像素统计）
idiff reference.png modified.png  # → FAILURE, 退出码 2
```

`idiff` 的互补工具是 [Perceptual Image Diff](http://pdiff.sourceforge.net/)：引入人类视觉系统模型，判断两张图是否「感知相同」，适合评估近似算法（如三角函数近似）的视觉误差是否在可接受范围内。

## 测试脚本设计

典型的测试脚本分三步走：

1. **生成测试用例**：用 `itertools.product()` 枚举参数组合（分辨率 × 采样数 × 场景 × RNG 种子……），随机采样一个子集（如每场景 10 个），保存为 CSV。全量枚举通常不可行——17000 个组合跑完需要数天。

2. **Reference run**：用当前已知正确的构建生成所有测试用例的渲染图，作为基准存储（不提交渲染图到代码库，只提交 CSV——几十 KB vs 数百 MB）。

3. **Test run**：每次代码改动后重跑，用 `idiff` 逐一与基准对比；同时记录渲染耗时（纳秒），追踪性能回归。

## 集成测试 vs 单元测试

对渲染器而言，集成测试比单元测试更实用的原因在于：

- 渲染器的「正确性」是端到端的整体行为，很难分解成独立的单元断言
- 继承已有代码时，往往不了解局部实现的预期，但知道整体应该输出什么
- 单元测试在追踪回归发生的精确位置时有优势，可以按需为新增函数或修复的 bug 补写

参见 [[automated-test-philosophy]] 中对集成测试优先策略的更普适讨论。

## 性能测试的位置

正确性测试和性能测试可以复用同一个运行框架：每次渲染记录耗时并存入结果 CSV，可以跨构建对比。注意性能测试要求单次运行不并行多测试用例（否则相互争抢 CPU 导致时间不可比），而正确性测试可以并行跑多个场景。这两个模式应该可配置切换。

## 相关

- [[automated-test-philosophy]]
- [[benchmark-methodology-end-to-end]]
- [[psraytracing]]

## Sources

- [[sources/16bpp-methods-of-testing]]
