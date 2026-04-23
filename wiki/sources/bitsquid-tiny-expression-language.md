---
tags: [source, bitsquid, expression-language, stack-vm, rpn]
date: 2026-04-19
sources: 1
---

# A Tiny Expression Language（Niklas Frykholm / bitsquid blog）

[[niklas-frykholm|Niklas Frykholm]] 2011 年 3 月发表于 bitsquid blog 的小工具分享：给美术 / 设计师用的**单行数学表达式求值器**，设计与实现都压到最小。

## 摘要

当美术希望在粒子速度、动画播放速率、物理力场等字段里写一行公式（比如 `sin(t) + 0.1 * cos(10*t)`）时，拉一门完整脚本语言（Lua 之流）太重，预设枚举又太死。Frykholm 的方案是一个**栈式 VM + 逆波兰字节码（RPN）**：把表达式 shunting-yard 转成 RPN，编译成只有 `PUSH_VAR / PUSH_FLOAT / COMPUTE_FUNCTION / END` 四种 opcode 的紧凑 bytecode（32-bit/word，高 8 bit opcode + 低 24 bit 索引），运行期是一个没有函数帧、没有堆分配的 switch 循环。再加上 RPN 格式对**常量折叠**极其友好，纯常数表达式在编译期就被塞成一个 `PUSH_FLOAT`、运行期可直接 bypass VM。源码一度开源在 bitbucket。

## 关键要点

- **表达式语言 ≠ 脚本语言**：只能写一行、无副作用的数学式，是给"cell 粒度的配置"用的；
- **Stack-based VM + RPN** 是最省的实现：opcode 就 4 种，bytecode 32 bit/word，主循环没有任何堆；
- **Shunting-yard 简化版** 足够：不需要完整 yacc，连右结合都可以先不支持；
- **常量折叠**：RPN 里连续 n 个 `PUSH_FLOAT` 紧跟一个 n 元函数，可以在编译期折掉；
- **对象存储**：外部传 `variables[]` 数组，VM 按 index 取值；函数表同理——没有符号表的运行期开销。

## 链接到的概念

- [[tiny-expression-language]]
- [[bytecode-everywhere]]
- [[data-driven-architecture]]
- [[flow-graph-data-oriented-runtime]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2011/03/putting-some-of-power-of-programming.html
- 本地：`raw/articles/bitsquid.blogspot.com/2011-03-13_a-tiny-expression-language.md`
