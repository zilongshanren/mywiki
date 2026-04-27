---
tags: [C++, 性能, noexcept, 异常, STL, benchmark, vector-pessimization]
date: 2026-04-27
sources: 1
---

# C++ `noexcept` 关键字的性能影响

`noexcept` 用于声明函数不抛出异常，理论优化路径有二：一是编译器可跳过 stack unwinding 基础设施的建立；二是标准库（如 `std::vector`）会优先使用 move 而非 copy，带来量级级别的差异。

## 实测结论（16bpp PSRayTracing，10 配置 × 370 小时）

- **整体效果接近噪声**：大多数配置下提升或损失均在 ±1–2% 之间，作者认为可以视为 fuzz
- **唯一显著提升**：AMD + Ubuntu + GCC 配置下，Book 1 场景（使用 `std::vector` 做顺序搜索）获得 6–8% 的一致加速
- **原因分析**：这一提升源于 `std::vector` 在有 `noexcept` move constructor 时选择 move 而非 copy（即"vector pessimization"的逆效应）。切换到 BVH 结构后，因为 BVHNode 没有 noexcept move constructor，这一收益消失
- **Intel + Windows + MSVC**：Perlin Sphere 相关场景出现 -10% 的退步，原因不明
- **Apple Silicon**：几乎无任何变化

## Vector Pessimization

标准库的"vector pessimization"是指：当元素类型的 move constructor **不是** `noexcept` 时，`std::vector` 在 reallocation 时会回退到 copy 以保证异常安全。为 move constructor 加上 `noexcept` 可解锁移动语义，有时会带来 25–30% 的 `emplace_back` 加速（见 StackOverflow 案例）。与此相关的高级话题是"vector pessimization"博文（Quuxplusone，2022），以及 `noexcept` 对函数指针/ABI 边界代码生成的影响。

## 代码生成层面

作者通过 `objdump` 对比了 GCC 生成的 x86 汇编，开启/关闭 `noexcept` 后差异仅为一条 `cmp` 指令的操作数顺序，实际代码路径几乎相同。这与常见说法（"编译器优化掉了大量 overhead"）相矛盾。

## 实践建议

- `noexcept` 作为**文档工具**有价值：明确标注函数不会抛出，方便调用方推理
- 作为**性能技巧**：只在 `std::vector`（或其他 move-aware 容器）+ 目标编译器已验证的情况下使用
- 不要"撒胡椒面"地给每个函数加 `noexcept`——它会破坏 throwing assert 等开发工具，并在某些场景引入退步
- 永远先测量，再下结论——参见 [[benchmark-methodology-end-to-end]]

## 与相关页面的关系

- [[cpp-final-keyword-performance]]：相同思路的另一实验，结论高度相似
- [[throwing-destructor-noexcept-terminate]]：`noexcept` 在析构函数上的语义陷阱
- [[undefined-behavior-c-cpp]]：C++ 为性能让步于 UB 的更宏观语境

## Sources

- [[sources/16bpp-noexcept-keyword]]
