---
tags: [source, c, cpp, rust, 未定义行为, 语言标准]
date: 2026-04-14
sources: 1
---

# With Undefined Behavior, Anything is Possible（Raph Levien / raphlinus.github.io）

[[raph-linus]] 发表于 2018 年 8 月的长文，把 C/C++ 「未定义行为」这个话题的历史、本质与社区分裂讲清楚，并对比了其他语言（Java、Rust、modern C++）的应对策略。

## 摘要

Raph 把 C 程序员分成三个阵营：**不可移植 C**（当汇编用）、**半可移植 C**（用 `#ifdef` 处理目标差异，「C 是可移植的汇编」的真实所指）、**标准 C**（语言委员会为了跨平台发明的抽象模型）。标准 C 引入「未定义行为」既是为了吞下平台差异（非 2 的幂字长、ones-complement 算术等），也是为了让严格别名（strict aliasing）等激进优化成为可能。然而委员会把同一把锤子用得过广——连 `x << 64` 这种场景都列为 UB，且新种类多到几乎每段现存 C 代码都不严格符合标准。这意味着真正的计算模型并不是「指针是数字」，而是一个**带类型与有效区间标签的虚拟机**；编译器可以基于这套虚拟机的假设激进优化，结果就是埋在代码库里几年的 UB 在某次编译器升级后突然爆炸。Linus Torvalds 对 union-based aliasing 补丁的那篇 rant 就是这种「半可移植阵营 vs 标准阵营」冲突的缩影。Raph 接着讨论线程：C89 里严格标准子集甚至无法描述线程程序，C11/C++11 的内存模型（借鉴 Java）补回了大部分表达力，但仍不足以表达 Boehm-Demers-Weiser GC、尾递归、协程等高级构造。对 UB 的治理，Raph 建议组合使用 LLVM UBSan + fuzzer、严格编码规范（Thomas Lord 主张把 C 当目标语言）和用代码生成器来产生 C 片段；他认为 Rust 的 safe/unsafe 分离是最可取的方向，modern C++ 虽有进步但无法与真正的安全语言相提并论。他还强调即使换语言也躲不开 UB——几乎所有运行时底层都是 C，FFI 是必经之路；数据竞争曾被分成「良性」和「危险」，但 Hans Boehm 的研究证明良性数据竞争并不存在。

## 关键要点

- **三个阵营**：不可移植 C / 半可移植 C / 标准 C，每一侧的工程实践与直觉完全不同
- **UB 的两个动机**：兼容奇异硬件 & 让优化器在别名分析上有假设可用
- **真正的 C 虚拟机**：指针不是整数，而是「带类型 + 有效区间」的对象，编译器基于这套假设推理
- **UB 目录比你以为的长得多**：有符号溢出、读未初始化、仅计算越界指针、shift 过位宽、类型双关……几乎所有现存程序都违反
- **「缓慢发生的激进变革」**：早期编译器对 UB 手下留情，晚期编译器把 UB 当优化前提——结果是「升级 GCC 代码就爆」
- **`x << 64` 是 UB**：委员会本可定义为 implementation-defined，但他们选择了广义 UB；Raph 认为这是历史失误
- **Friendly C 方言尝试失败**：编译器作者不愿让出优化空间
- **治理手段**：UBSan + fuzzer + 严格编码规范 + 代码生成工具
- **线程与表达力**：C89 无法描述线程程序，C11/C++11 借鉴 Java 内存模型才补回；但 Boehm GC、尾递归、协程仍只能用半可移植 C 写
- **跨语言**：Java 几乎没有 UB（除 JNI），Rust 靠 safe/unsafe 分离精确控制；modern C++ 依靠 RAII + smart pointer 能降低内存问题但对整数溢出、iterator 失效等仍无力
- **即使换语言也躲不开**：运行时底层几乎都是 C，FFI 把 UB 传进高级语言；数据竞争里不存在「良性」一类

## 链接到的概念

- [[undefined-behavior-c-cpp]]
- [[avoid-unsigned-types]]

## 原文

- 链接：https://raphlinus.github.io/programming/rust/2018/08/17/undefined-behavior.html
- 本地：`raw/articles/raphlinus.github.io/2018-08-17_with-undefined-behavior-anything-is-possible.md`
