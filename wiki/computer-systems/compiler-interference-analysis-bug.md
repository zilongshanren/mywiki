---
tags: [计算机系统, 编译器, bug, C++, 优化, 调试]
date: 2026-04-14
sources: 1
---

# 编译器干涉分析 bug（Interference Analysis Bug）

一个在 **MSVC 2019**（cl 19.24）上观察到的代码生成 bug：一个包含 4 KB 数组的小 struct 会被优化器错误地当成「两个生命期不重叠的临时量」，结果**两个活跃的栈临时量被分配到了同一块栈空间**，一个写入把另一个改坏了。Max Slater 在 path tracer 里遇到这个 bug 导致整张图烂掉，下探到汇编才找到根因。

## 最小复现

```cpp
struct data { uint8_t _data[4095] = {}; };
struct container {
    uint8_t type = 1;
    data n;
    static container make() {
        container ret;
        printf("Before: %d\n", ret.type);
        ret.n = data{};
        printf("After: %d\n", ret.type);  // prints 0 instead of 1
        return ret;
    }
    container() {}
    container(const container&) {}
};
void func(container c) {}
int main() { func(container::make()); }
```

`-O2` 下输出 `Before: 1` / `After: 0`。任何以下改动都能「修」好它：

- `_data[4095]` → `_data[4094]` 或更小
- 删除拷贝构造函数
- 删除 `func()` 调用
- 在 `func()` 调用前加一个无关的 `container::make()` 调用

**典型的幽灵 bug 味道**——和具体的大小、调用结构、函数数量耦合。

## 真正的底层原因

用 compiler explorer 对比 19.24（坏）和 19.25（修）的汇编，唯一的差别是**后者多分配了一页栈空间**：

```
-- mov eax, 8224    ; 坏版本
++ mov eax, 12320   ; 修复版本
```

三个临时量 $T1$（`data{}` 的匿名临时）、$T2$（`ret`，最终被 copy-elided 传给 `func`）、$T3$（似乎是 pre-copy-elision 时代的残留）**在坏版本里 $T1$ 和 $T2$ 占用了同一块栈区间 `[32, 4128)`**——这是显然的错误：

- `ret.n = data{};` 把临时 `data{}`（$T1$）写完之后 `memcpy` 到 `ret.n`（$T2$ 的成员），而 $T2$ 里的 `type` 字段又紧挨在 `ret.n` 之前。两个生命期**完全重叠**，写 $T1$ 就是在写 $T2->type`。
- 更糟：`memcpy` 的源和目标在坏版本下是**部分重叠**的（都落在 `[32, 4128)` 内），这本身就是 UB。

修复版本把 $T1$ 和 $T2$ 放到了不同的栈地址：$T1 \in [32, 4127)$、$T2 \in [4128, 8224)$，两者不再冲突。

## 为什么编译器「看错了」

微软确认这是个 **interference analysis**（干涉分析）的错误。猜测根源：

- **RVO / copy elision**：因为拷贝构造被省略，`ret` 和它的调用 site 使用同一块栈；
- **inlining**：`container::make()` 和 `func()` 都被内联进 `main`，临时量的「谁属于谁」信息在 IR 级别已经被压扁；
- 优化器某一步认为 $T1$ 和 $T2$ **alive 的区间不重叠**——可能以为 `ret.n = data{};` 之前 `ret` 的字段还没被真正初始化——因此可以合并两个栈槽。

这种 bug 的特征是**非常特定的大小 / 结构触发**：4 KB 是一个 page 边界，触发优化器某条 heuristic 路径；如果数组小于一个 chkstk chunk，`__chkstk` 不会被调用，分配路径也不同。

## 经验教训

- **只在 `-O2` 下出现的 bug 通常是 UB**——但**不总是**。这一次是编译器的错，不是用户代码的错。
- **Godbolt / compiler explorer 是调试器**：可以跨版本 bisect 汇编输出，直接看「优化器在哪一步开始跑偏」。
- **相信「所有调用的结果」**：在加 printf 拆分到 `ret.type` 是什么被修改之前，没人会怀疑编译器；但一旦 MCVE 在 GCC / Clang 下正确，就该报给 MSVC bug tracker。
- **栈临时量的分配规则** 是 ABI + 优化器的共同产物，对它的心智模型应当包括「临时量也有 live 区间分析」这一层。

## 相关

- [[compilation-pipeline]] — bug 出现在编译阶段的干涉分析 pass 里
- [[virtual-memory]] — 4 KB page 阈值导致 `__chkstk` 路径变化
- [[bottleneck-analysis]] — 通过 bisect 把 bug 定位到汇编 diff 的方法论
- [[max-slater]]

## Sources

- [[sources/slater-compiler-bug]]
