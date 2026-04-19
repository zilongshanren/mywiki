---
tags: [benchmark, performance, compiler-optimization, methodology]
date: 2026-04-19
sources: 3
---

# Benchmark 方法论：小样本不能代替端到端

16BPP.net 的作者在四篇连载里反复踩到同一根弦：**一段代码在 microbenchmark 里的表现，放回真实应用里可能彻底反转**。这页总结他从 `final` / `noexcept` / 贪心 vs 解析 / free function / `asin()` 近似一路积累下来的经验规则。

## 规则一：打开优化再测

`-O0` 下测量几乎没有参考价值。最鲜明的案例：[[rejection-vs-analytical-sampling]] 里解析方法在 `-O0` 下快 10~33%，打开 `-O1` 后拒绝采样反超 50%+。编译器内联、常量折叠、把 `sincos` 合并、向量化——这些都只在 `-O2`/`-O3` 才发生，不测就看不见。

## 规则二：矩阵测试

每个结论都要跨 CPU × 操作系统 × 编译器 × 优化级别。作者的标准矩阵：

- **CPU**：Intel i7-10750H / AMD Ryzen 9 6900HX / Apple M1 或 M4
- **OS**：Windows 11 / Ubuntu 24.04 / macOS Sequoia 或 Tahoe
- **编译器**：GCC / Clang / MSVC
- **优化级别**：`-O0`、`-O1`、`-O2`、`-O3`、`-Ofast`（MSVC 对应 `/Od`、`/O1`、`/O2`、`/Ox`、`/Ot` 等）

典型是 48 组合、每组合数百次迭代，跑几小时到几十小时是常事（free function 那篇跑了 78 小时）。产出是 Google Sheet / Jupyter Notebook / CSV，而不是博客里一张柱状图。

## 规则三：先小样本再整合到真实应用

Small benchmark 和 end-to-end 常常不一致：

- **贪心 vs 解析**：microbench 显示拒绝 `-O3` 后快 50%，放回 PSRayTracing 只快几个百分点（因为采样只占总时间一小部分）。
- **free function**：Vec4 小 benchmark 在 clang/Linux/Intel 的 `normalize()` 上看到 15% 速度提升，整合进 Synfig 全仓库 680 个测例跑 78 小时，差距缩到 0.5%——掉进噪声。

> 「一段代码的 benchmark 结果，只有在它被放进一个更大的应用里之后才有意义。」

## 规则四：警惕 outlier 和非确定性

`.sif` 文件有时候第 10 次突然快 50%，并非真实的性能提升。作者用 [Z-score](https://en.wikipedia.org/wiki/Standard_score) 做离群点剔除（阈值 2.0 丢弃约 5% 数据），结果依然飘；用更严的阈值会丢 30% 数据——**数据本身就非平稳**。Synfig 某些测例在 `164ms` 和 `114ms` 之间周期跳动，Z-score、IQR 都救不了它。

现代 CPU 的动态时钟、OS 调度、ASLR、代码对齐、cache 状态都是「computer gremlins」来源。解决方案是**增加样本量**（25 次起、最好 250 次）、取中位数、每次重跑都重启进程；或干脆丢掉这个文件换一个。

## 规则五：别凭汇编判断

`-O3` 下的汇编「几乎不可读」，编译器会内联、重排、把无关函数都 inline 光。作者承认自己「不是汇编专家」，最后还是以**墙上挂钟**为准。「指令更少」不等于「更快」：参见 [[rejection-vs-analytical-sampling]] 里解析版本虽然指令略少，但多了两次 `call` 就输了。

## 规则六：2% 是信号门槛

作者取自 Nicholas Ormrod 的经验值：**小于 2% 的差异直接视为噪声**。他自己测 free function 时用的是「至少 10ms 才算显著差异」（在 150~300ms 级别的 run 上，相当于 3~6%）。

## 规则七：把原始数据挂出来

每篇性能文都附 Google Sheet、Jupyter notebook、benchmark 源码链接。这是 Klaus Iglberger 2017 年那条「Free functions may be faster」主张 8 年后被重新检验的直接原因——**没有数据的性能宣言都是噪声**。作者的私人目标之一就是「让这个风气停下来」。

## 典型反例

- [[free-vs-member-functions-performance]]：8 年旧主张，重测后基本是噪声。
- [[rejection-vs-analytical-sampling]]：数学直觉与编译后性能完全相反。
- [[asin-cg-approximation]]：先走了半年 Taylor / Padé 的弯路，回头发现 Nvidia Cg 文档里躺了 10 多年的 Minimax 公式直接就是最优。

## 相关

- [[rejection-vs-analytical-sampling]]
- [[free-vs-member-functions-performance]]
- [[asin-cg-approximation]]
- [[estrin-scheme]]
- [[cpu-performance-formula]]
- [[faster-math-functions]]
- [[psraytracing]]

## Sources

- [[sources/16bpp-greedy-vs-analytical]]
- [[sources/16bpp-free-functions-hypothesis]]
- [[sources/16bpp-quicker-trig-asin-cg]]
