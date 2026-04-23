---
tags: [parser, grammar, cfg, algorithms]
date: 2026-04-19
sources: 1
---

# Earley Parser

Earley parser 是 Jay Earley 在 1970 年提出的通用 CFG 解析算法，**不对文法形态设限**：可直接处理任意上下文无关文法，包括左递归、歧义、空产生式。相比之下，LL(k) 要求无左递归，LR(k) 虽能容左递归但需预处理生成分析表。

## 时间复杂度

- 一般 CFG：O(n^3)
- 无歧义 CFG：O(n^2)
- 左/右递归的简单文法，以及大多数实际编程语言文法：O(n)

最坏 O(n^3) 在实际工程里很少触达，因为触发它需要刻意构造的歧义爆炸文法。

## 算法骨架

对输入长度 n，维护 n+1 个状态集 S₀…Sₙ。每个状态形如 `(A → α · β, i)`：产生式 A → αβ 的点在 α 之后，`i` 是该状态开始扫描的位置。三种操作：

- **Predict**：点后是非终结符 B，为 S_j 补入所有 `B → · γ, j`
- **Scan**：点后是终结符且匹配输入第 j+1 位，把点推进后放入 S_{j+1}
- **Complete**：遇到点已到末端的完成项，在其起始集 S_i 里找等它的项，把点推进

输入扫完后如果 Sₙ 里有 `S → α ·, 0`，则接受。

## 与歧义的关系

Earley 天然支持歧义：若一个输入有多棵语法树，Sₙ 会同时包含多条完成路径。生产实现（如 Marpa）可直接输出共享森林（SPPF）。对自然语言处理、DSL 的宽松前端这非常有用。

## 工程实现

- **Marpa**（Jeffrey Kegler，Perl+C）：工业强度，改进了 Earley 对歧义森林的表示，性能接近手写 LALR
- **[[boris-the-brave|Boris The Brave]] 的 Axaxaxas**（Python 3.3）：主打易用、无预处理、可 hook；性能非首要目标
- **nearley.js**：JavaScript 版，用在浏览器端 DSL 解析
- **Lark**（Python）：默认 Earley，也可切 LALR

## 什么时候用

- 文法有歧义或会演化 → Earley 的宽松性避免每次改动都要调文法形态
- 输入短小、性能非瓶颈 → O(n^3) 最坏也不怕
- 需要错误恢复、部分解析 → Earley 的状态集天然保留了不完整解析的信息

不建议用 Earley 做大文件的生产解析：此时 LALR/PEG 生成器仍是更稳的选择。

## Sources

- [[sources/boristhebrave-axaxaxas]]
