---
tags: [c++, 未定义行为, 编译器优化, clang, cgal]
date: 2026-04-19
sources: 1
---

# Clang 借空引用 UB 删除整块代码：一次生产事故

[[ben-supnik|Supnik]] 2015 年在 X-Plane RenderFarm（全球场景生成工具）迁到 Clang 的优化构建后吃到一次段错误。GCC 的 `-O2` 正常、Clang 的 `-O0` 正常，**只在 Clang `-O2` 下**整块 `if(pts->buddy == NULL) { … }` 分支被优化器删得一干二净。这是 **post-classical 编译器**把一条「事实上能跑几十年」的 C++ 惯用法直接判定为 UB 并无情利用的一个干净案例。

## 事发代码

`buddy` 是 CGAL 的 `CC_iterator` —— 一个封装裸指针的 smart handle。它与 `nullptr_t` 的比较是这样定义的：

```cpp
template <class DSC, bool Const>
bool operator==(const CC_iterator<DSC, Const> &rhs, nullptr_t) {
    return &*rhs == NULL;   // 拿 bare pointer 再和 NULL 比
}
```

`&*rhs` 的套路是一个 C++ 圈内流传多年的 idiom：通过 `operator*` 取出引用，再用 `&` 变回裸指针。几乎所有存放指针的 wrapper 类都这么抽掉一层皮。

## Clang 的推理

Clang 的静态分析注释原话：**reference cannot be bound to dereferenced null pointer in well-defined C++ code; comparison may be assumed to always evaluate to false.**

它的推导链：

1. 如果 `&*rhs == NULL` 要成立，那么 `&` 前面那个表达式 `*rhs` 必须取到了一个空引用。
2. 把 null pointer 解引用出「空引用」在 C++ 标准里**没有合法解释**——整段代码已经进入 UB 区间。
3. 既然是 UB，编译器可以任意处理。
4. 选一个最简单的处理：**把 `return &*rhs == NULL` 直接等价为 `return false`**。

于是 `pts->buddy == NULL` 编译后就是 `if(false)`，整个维护循环里的关键处理块蒸发。程序跑得更快——只是跑到段错误为止。

## 短期 workaround：两个 handle 比较

改写为 `pts->buddy == CDT::Vertex_handle()`，让 `operator==` 走**双 handle 版本**：

```cpp
bool operator!=(const CC_iterator &rhs, const CC_iterator &lhs) {
    return &*rhs != &*lhs;
}
```

同样有 `&*` on null 的问题——但这次 Clang 在编译期**看不出**哪一边必然是 null，只能保守地退化为一次实打实的裸指针比较。新版 CGAL 的根治做法是用 `operator->()` 直接吐出 bare pointer，绕开「引用」这一层语义。

## 这件事的教训

- **老派 C/C++ 工程师**习惯「UB = 未规定，但在我认识的硬件上行为是确定的」。这个直觉在 GCC 3 时代几乎总是对的，在 GCC 7 / Clang 现代版本下每年都会坏掉几次。[[undefined-behavior-c-cpp]] 把这个缓慢展开的现象讲得更系统。
- **`&*ptr` idiom 不安全**——每一处这种写法都可能在某次 toolchain 升级后被编译器发现并利用。`std::addressof` **也救不了**：`*ptr` 那一步已经 UB 完了，`addressof` 只是晚一点取地址。
- **UBSan + 细分优化级别**是唯一可靠的预警——Supnik 的崩溃原本在 `-O0` 下跑得好好的，这就是 UB 的典型阴险之处：它在优化开关之间跳来跳去。
- **库版本更新并不免费**。Supnik 在评论区被建议「升级到新 CGAL」，他回应：光是让三四个编译器 + 依赖链同时跑通，就够吃掉几天真正的工作时间。

## 相关

- [[undefined-behavior-c-cpp]] — UB 更全景的语言学脉络
- [[compiler-interference-analysis-bug]] — 另一个「优化器越界优化」的生产案例
- [[ben-supnik]]

## Sources

- [[sources/supnik-dangers-super-smart-compilers]]
