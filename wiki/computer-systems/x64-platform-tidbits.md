---
tags: [x86-64, ppc, 编译器, c++, 性能]
date: 2026-04-14
sources: 1
---

# 64 位平台上的两个小坑：C 提升规则与 PPC 指针包装

ryg 在一篇短文里记下了两个「只有看了汇编才会发现」的 64 位平台性能坑。它们根源一样——**C/C++ 的类型提升规则假设 int 就是寄存器宽度**——但表现形式一个在 x86-64 上，一个在 PS3 的 PPU GCC 上。

## 坑 1：x86-64 上的地址计算莫名多一条指令

看这段代码：

```c
U32 offset = ...;
U8 *ptr = base + (offset & 0xffff) * 4;
```

直觉上编译器应该生成 1 条 and 加一条 `base+index*4` 寻址。实际编译出的是：

```
movzx eax, ax     ; 等价于 and eax, 0xffff（更小）
shl   eax, 2      ; *4 在 32 位里做
add   rax, rcx    ; base + 结果
```

为什么？因为 `(offset & 0xffff) * 4` 整体按 C 的算术转换规则在 `unsigned int`（32 位）里计算——而 x86-64 的硬件寻址模式等价于在 64 位里做 `*4`，在存在溢出的情况下二者不等价。哪怕这个例子里显然不可能溢出，优化器也没敢做这一步推断。

修法非常简单：显式把一边升到 64 位——`base + U64(offset & 0xffff) * 4` 或乘以 `4ull` / `(size_t)4`。

延伸思考：`int` 保留 32 位是为了兼容大量历史代码，但 C 的提升规则**隐式假设 int 是原生寄存器宽度**。只要 `int` 与指针宽度不匹配，这类坑就会反复出现。

> 评论区补充：x86-64 上，任何 32 位或更小的目的操作数写入都会**隐式清零寄存器的高 32 位**（避免引入部分寄存器写造成的依赖链），所以 `movzx eax, ax` 之后 `rax` 的高位自然是 0。这是 x86-64 指令集有意的设计选择。唯一的例外是单字节形式的 `xchg eax, eax`（操作码 `0x90`，现在被当作真正的 NOP），它不清零高位。

## 坑 2：PS3 的 PPU GCC 把 32 位指针当 64 位指针用

PS3 的 Cell PPU 虽然是 64 位 PowerPC，但整机只有 256 MB RAM + 256 MB GPU 显存，用 64 位指针纯属浪费。问题在于 GCC **假设（几乎）所有地址计算都可能溢出**，于是手动做计算再把高 32 位清掉，不肯使用 PPC 内建的寻址模式。

```c
U32 *p = ...;
*++p = x;
*++p = y;
```

理想的 PPC 汇编只有 2 条：

```
stw  r9, 4(r8)       ; *(p+1) = x
stwu r10, 8(r8)      ; *(p+2) = y; p += 2
```

而 GCC 实际生成 6 条：先 `addi` 两次，再 `clrldi` 两次把高 32 位抹掉，最后才写内存。**指令数 3 倍，寄存器压力也更高**（多占了两个临时寄存器）。

ryg 发现 GCC 唯一肯相信「指针不会包装」的场景是**结构体成员访问**。于是 PS3 渲染命令缓冲里那种「连续写 N 个 U32 出去」的代码可以这样伪装成结构体：

```c
struct CommandData { U32 w0, w1, w2, w3, w4, w5, w6, w7; };
CommandData *cmd_out = (CommandData *) cmd;
cmd_out->w0 = foo; cmd_out->w1 = bar;
cmd_out->w2 = blah; cmd_out->w3 = blub;
cmd = &cmd_out->w4;
```

换来和手写汇编相当的代码质量。ryg 说当时改 PS3 渲染代码、仅靠这一类低层优化就拿到了 10% 以上的加速。

## 教训

1. 在**有序执行**（in-order）CPU 上调优时，读编译出的汇编是 non-negotiable 的——在 C/C++ 层面你根本看不到这类问题。
2. C/C++ 的算术转换规则是**机器无关**的抽象，但一旦 `int` 宽度和寄存器宽度对不上，抽象开始漏。
3. 溢出语义的保守假设会让编译器放弃大量本可以做的折叠；当场景实际不需要溢出时，用类型或结构体「指导」编译器放心合并。

## 相关

- [[calling-conventions-x86]]
- [[avoid-unsigned-types]]
- [[cpp-multi-paradigm-discipline]]
- [[fabian-giesen]]

## Sources

- [[sources/ryg-64-bit-tidbits]]
