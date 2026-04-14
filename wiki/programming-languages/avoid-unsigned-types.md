---
tags: [C++, API设计, 类型系统, 防御性编程, Scott-Meyers]
date: 2026-04-14
sources: 1
---

# 默认避免使用 unsigned 类型

C++ 里 `unsigned int` / `size_t` 这类无符号整型常被滥用——尤其是从 Java 转过来的程序员，因为 Java 没有 unsigned 类型而把它当成「应当存在的工具」，回到 C++ 后到处使用，仿佛只要值「逻辑上不可能为负」就该用 unsigned。[[matthaeus-chajdas]] 在 2010 年的一篇短文里把 Scott Meyers 1995 年 *C++ Report* 专栏里的老论点重新讲了一遍：**绝大多数日常代码应当默认用 signed 类型**，unsigned 留给极少数确实必要的场合。

## 唯二该用 unsigned 的场景

- **interop**：调用一个期待 `unsigned` 的 C API（操作系统 syscall、第三方库），你必须在边界上做转换。但**应当尽量晚转换**，并且转换前对 signed 值做一次 sanity check，而不是早早把全部内部状态都改成 unsigned。
- **I/O 与位模式**：磁盘、网络、序列化场景里，你关心的是**裸 bit pattern** 而不是数值大小；这时 unsigned 是合适的容器，因为有符号右移、溢出行为都是未定义或实现定义的，会污染你对位模式的推理。

## 为什么 unsigned 会让 sanity check 失效

Meyers 与 Chajdas 的核心论点是：**unsigned 类型让「负数检查」永远 false**。一个被广泛引用的例子（Chajdas 用了 `memset` 的变体）：

```cpp
struct Pod {
    unsigned char flags;
    Vector3 coords;  // 而不是 Vector4
};

memset(&pod, 0, sizeof(Pod) - sizeof(Vector4));
```

写代码的人模糊记得 `Pod` 里有一个 `Vector4`，于是用 `sizeof(Pod) - sizeof(Vector4)` 算「该清的字节数」。但实际上 `coords` 是 `Vector3`——`sizeof(Pod) - sizeof(Vector4)` 是个**负值**。

- 如果 `memset` 第三个参数声明为 `size_t`（unsigned），这个负值悄无声息地变成了 `18446744073709551613`——程序会**清掉接近整个地址空间**，立刻段错误，根本无从定位「到底哪一行算错了大小」。
- 如果声明为有符号 `ssize_t`，一个简单的 `assert(size >= 0)` 就能在调用边界拦截，错误信息直接告诉你「size == -3」。

「能 assert 出来的 bug 是好 bug」是这条建议的核心——**unsigned 把可恢复的诊断错误降级成了不可恢复的内存灾难**。

## 你真的会用到那一个 bit 吗

反对意见通常是：「signed 少了一个 bit 的范围，对大缓冲区会不够用啊」。Chajdas 反问：**你真的见过哪一次 `malloc` 或 `fwrite` 调用要分配 / 写入 2³¹ 个元素吗**？32 位机上单次申请 2 GB 已经接近地址空间极限；64 位机上 2⁶³ 元素更是天文数字。**用一个 bit 换全栈的 sanity check 能力，是显然合算的交易**。

## 这条建议不是「无脑用 signed 就安全」

Chajdas 在文末特别强调：**signed 仍然会溢出**，只是溢出后的负值更难被攻击者利用，而且更容易被 `assert` 与 sanitizer 抓到。要写真正稳的算术代码，仍然要主动检查范围、用 `SafeInt` / `__builtin_*_overflow` 这类工具防御中间结果溢出。signed-by-default 是为了**让错误检查变得可能**，而不是为了让错误本身消失。

## 与现代 C++ 与其它语言的呼应

这条 2010 年的建议在后来获得了大量背书：

- Bjarne Stroustrup 与 Herb Sutter 在 C++ Core Guidelines 里写了 `ES.106 Don't try to avoid negative values by using unsigned`，直接引用了 Meyers 的论证。
- Google C++ Style Guide 长期建议**只在位运算与表示溢出语义时用 unsigned**，索引与计数器都用 signed。
- Rust、Swift、C# 等设计较新的语言在标准库里都为「索引 / 长度」选择了**有符号 64 位整数**，间接承认 unsigned size 的代价过高。
- 现代 sanitizer（UBSan signed-integer-overflow、wraparound 检测）让 signed 的「溢出可观测」优势更明显。

C++ 标准库自身 `size_t` 的选择被普遍认为是历史包袱——`std::ssize` 在 C++20 里加入正是对这一债务的迟来修补。

## 相关

- [[red-flags]]
- [[information-leakage]]
- [[matthaeus-chajdas]]

## Sources

- [[sources/anteru-avoid-unsigned-types]]
