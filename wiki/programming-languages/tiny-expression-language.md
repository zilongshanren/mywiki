---
tags: [expression-language, stack-vm, rpn, bytecode, bitsquid, tooling]
date: 2026-04-19
sources: 1
---

# 小型表达式语言

游戏引擎里有一类场景需要**把一行数学表达式交到美术手里**：粒子发射器的出射速度想写成 `sin(t) + 0.1 * cos(10*t)`，动画播放速度想跟着某个 controller 变量，物理里搞个龙卷风的力场……这些都是一行式的需求，不值得为之上一门完整脚本语言（Lua / JS），但**又必须比 magic number 多一点表达力**。[[niklas-frykholm|Niklas Frykholm]] 2011 年给 Bitsquid 做的解法是一个极小的**栈式虚拟机 + RPN 字节码**——既轻到可以在热路径上大量求值，又简单到美术不用学语法。

## 为什么不直接用 Lua

一行表达式的求值开销必须**小于表达式本身的计算量**，否则在粒子这种"每帧跑几万次"的地方就被 overhead 吃掉。Lua / JS / Python 都带着解释器、GC、栈帧生命周期这些东西，适合做"整段逻辑"，不适合做"一格求值"。另一方向是硬编码几个预设函数——但那就把设计师锁回了枚举。Expression language 是中间的那一档：比 Lisp 简单，比 Forth 简单，**在语法上就是一个计算器**，只能写一行没有副作用的数学式。

## Stack-based VM + RPN

底层用**栈机**（[[bytecode-everywhere|bytecode]] 那条路）。表达式 `sin(t) + 0.1 * cos(10 * t)` 经由 [shunting-yard](https://en.wikipedia.org/wiki/Shunting-yard_algorithm) 转换成逆波兰：

```
t sin 0.1 10 t * cos * +
```

然后只需要三类操作码：

- `PUSH_VARIABLE idx` — 把第 `idx` 个变量压栈；
- `PUSH_FLOAT v` — 把立即数压栈（用后续一个 32-bit word 存浮点）；
- `COMPUTE_FUNCTION idx` — 按函数表里第 `idx` 项的 arity 从栈弹元素、算结果、再压回；
- `END` — 结束。

Frykholm 的实现用 32 bit/word，高 8 bit 存 opcode、低 24 bit 存索引，主循环就是一个 switch，没有函数调用帧、没有堆分配。执行时外部传进 `variables[]` 数组，按位置匹配。

## 编译三步走

1. **Tokenize** — 扫描字符串，把 identifier 匹配到变量名表/函数名表、常量（比如 `pi`）直接折进来；
2. **Infix → postfix** — 不走完整 yacc，只用 shunting-yard 的简化版（不支持右结合），把运算符栈按优先级（叠加括号层数）pop 出去；
3. **常量折叠** — RPN 格式的好处之一是常量折叠极其简单：如果 `n` 元函数前面连续 `n` 个都是 `PUSH_FLOAT`，就可以在编译期算掉、塞回一个 `PUSH_FLOAT`。如果整条表达式最后只剩一个 `PUSH_FLOAT`，运行期可以直接 bypass VM。

## 对照：表达式语言在引擎里的地位

这一层放在**数据驱动引擎的"可视化脚本"与"完全硬编码"之间**（见 [[data-driven-architecture]]）。Bitsquid 自己也有 [[flow-graph-data-oriented-runtime|visual scripting]]，但 flow graph 粒度是"每个节点一个操作"，而 expression language 是"一整个单元格里的数学式"——两者互补。Unity Shader Graph 的 `Custom Function` 节点、Unreal 的 Material Expression、Houdini VEX / Mantra 的 snippets 都是这一路线不同强度的实现。

Frykholm 把参考代码发在 bitbucket（后期已迁移），也是这种"极小工具发出来给后人直接抄"的作风。

## 相关

- [[bytecode-everywhere]] — 字节码在引擎里的广义用法
- [[data-driven-architecture]] — 表达式语言是数据驱动的一个维度
- [[flow-graph-data-oriented-runtime]] — Bitsquid 的可视化脚本，粒度比表达式粗一档
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-tiny-expression-language]]
