---
tags: [source, 编译器, x86-64, ppc, c++, ryg]
date: 2026-04-14
sources: 1
---

# 64-bit tidbits（ryg / The ryg blog）

[[fabian-giesen]] 在 2010 年 10 月记下的两个「只有读汇编才会发现」的 64 位平台坑。核心是 **C/C++ 的类型提升规则隐式假设 `int` 就是原生寄存器宽度**，一旦指针比 `int` 宽就会出麻烦。

## 摘要

第一则在 x86-64：`U8 *ptr = base + (offset & 0xffff) * 4;` 本以为只产生一条 and + 一条 `base+index*4` 寻址，实际生成了 `movzx/shl/add` 三条指令。原因是 C 把整个乘法算在 `unsigned int`（32 位）里，而硬件的 `*4` 寻址等价于在 64 位里做——**溢出语义不一致**，所以编译器不敢合并。修法是把一边显式升成 `U64` / `size_t`。第二则在 PS3 的 PPU GCC：GCC 假定所有地址计算都可能溢出，于是手动算 + 用 `clrldi` 抹高 32 位，而不用 PPC 内建寻址；指令数变成 3 倍，寄存器压力也更大。ryg 发现 GCC 唯一肯相信「指针不会 wrap」的情形是**结构体成员访问**——于是可以把 U32 流伪装成 `struct CommandData { U32 w0...w7; }` 来骗编译器生成好代码。ryg 说当年靠这类低级优化在 PS3 渲染代码上拿到 >10% 的加速。评论区补充：x86-64 上任何 32 位或更小的目的操作数写入都**隐式清零高 32 位**，这是设计选择，不是 bug（唯一例外是单字节形式的 `xchg eax, eax`——即 0x90 NOP）。

## 关键要点

- C/C++ 的整数提升规则假设 `int` 宽度 == 寄存器宽度；64 位平台上这个假设已经坏了
- x86-64 上 `(U32 expr) * 4` 不会被合并进 `base+index*4` 寻址，因为 32 位溢出语义和 64 位不一致
- 修法：显式升位 `U64(offset & 0xffff) * 4` 或用 `4ull` / `(size_t)4`
- PS3 PPU GCC 对一般指针不敢省 `clrldi`（清高 32 位），但**对结构体成员访问肯省**
- 把连续的 `U32` 写操作伪装成 `struct CommandData { U32 w0, ..., w7; }`，可以骗 GCC 生成紧凑的 PPC 代码
- x86-64：任何 32 位及更小的目的操作数写入都隐式清零寄存器高 32 位（避免部分寄存器写依赖）
- **结论**：有序 CPU 上调优必须读汇编——源码层面看不到这些问题

## 链接到的概念

- [[x64-platform-tidbits]]
- [[calling-conventions-x86]]
- [[avoid-unsigned-types]]

## 原文

- 链接：https://fgiesen.wordpress.com/2010/10/10/64-bit-tidbit/
- 本地：`raw/articles/fgiesen.wordpress.com/2010-10-10_64-bit-tidbits.md`
