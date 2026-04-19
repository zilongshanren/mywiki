---
tags: [位操作, 二进制补码, c, bit-twiddling]
date: 2026-04-14
sources: 1
---

# 符号/零扩展的无移位做法

把一个窄位宽（比如 11 bit）整数扩展到机器字宽，同时要支持它**既可能是有符号、也可能是无符号**的情况——这是 bit-packed 格式解码里的常见烦恼。[[fabian-giesen]] 在一个含可变位宽字段的编解码器里遇到了这个问题，总结出一个**不依赖位移语义、也不需要分支**的通用写法。

## 传统做法及其问题

教科书式的写法是「左移到容器的符号位，再做算术右移」：

```c
int32 sign_extend(int32 val_11b) {
    int32 t = val_11b << (32 - 11);
    return t >> (32 - 11);
}
```

这个写法在 C/C++ 里问题不少：**左移进符号位**在 C99/C++17 以前要么是未定义、要么是实现定义；算术右移的符号位复制依赖有符号右移的实现；还要显式依赖固定的字宽。C++20 才正式把二进制补码「签署」进语言标准。

## 用补码定义本身重新推导

从补码的定义出发更干净：**N 位补码只是把最高位的「位值」从 +2^(N-1) 改成 -2^(N-1)**，其余低位的位值完全不变。

所以，把一个无符号 11 位整数「解读成」有符号 11 位整数，需要的只是**把最高位的贡献从 +1024 换成 -1024**。这可以写成：

```c
int sign_extend(int val_11b) {
    return (val_11b & 0x3ff) - (val_11b & 0x400);
}
```

低 10 bit 原样保留，bit 10 用 `val & 0x400` 单独抠出来（要么 0、要么 1024），再减掉它——从 +1024 一下子变成 -1024，完美。

更紧的写法是直接算修正量：如果 bit 10 原本贡献了 +1024、应当贡献 -1024，偏差就是 -2048，即「两倍的位值」：

```c
int sign_extend(int val_11b) {
    return val_11b - (val_11b & 0x400) * 2;
}
```

这个写法对容器位宽**零假设**，也不依赖机器是补码（虽然这年头不是补码的机器已经看不见了）。

## 零或符号扩展的统一函数

一旦写成「减去两倍的符号位」的形式，就可以让同一份代码同时处理有符号和无符号，只需传入「符号位在哪」：

```c
int zero_or_sign_extend(int val, int sign_bit) {
    return val - (val & sign_bit) * 2;
}
```

- `sign_bit == 0` → 不做任何修正，得到无符号扩展。
- `sign_bit == (1 << (N-1))` → 最高位翻号，得到有符号扩展。

对于 ryg 当初的场景——头部决定字段是有符号还是无符号——这意味着**解码循环不再需要 if**，是否做符号扩展完全编码进预计算好的 `sign_bit` 常量里。

## Harold Aptroot 的更漂亮变体

评论区里 Harold Aptroot 给出了一个更漂亮的形式：

```c
int zero_or_sign_extend(int val, int sign_bit) {
    return (val ^ sign_bit) - sign_bit;
}
```

验证：

- `sign_bit == 0` 时，XOR 和减法都是恒等。
- `sign_bit != 0` 且原符号位为 0：XOR 把那一位**置 1**，等同于 `val + sign_bit`，然后立刻减回去，净贡献 0。
- `sign_bit != 0` 且原符号位为 1：XOR 把那一位**清零**，等同于 `val - sign_bit`，再减一次，总共减了 `2 * sign_bit`——正是把 `+sign_bit` 换成 `-sign_bit` 的修正量。

## 相关

- [[sse-tricks]] —— SIMD 内的位级技巧集合
- [[insert-zero-bit-in-middle]] —— 同系列的 bit-twiddling 小品
- [[bits-and-context]]
- [[fabian-giesen]]

## Sources

- [[sources/ryg-zero-or-sign-extend]]
