---
tags: [gpgpu, parsing, json, 并行算法, scan, scatter, sort]
date: 2026-04-14
sources: 1
---

# GPGPU 上的 JSON 解析：Dyck 语言的并行化

[[raph-linus]] 2018 年写的一篇 sketch——他自己描述为"还没实现过、手都没碰过 GPU、谁知道会出什么问题"。但思路是漂亮的：把 JSON 里**最硬核的那一块**（括号嵌套结构提取，等价于 [Dyck 语言](https://en.wikipedia.org/wiki/Dyck_language) 解析）拆成一串 **scan + scatter + sort** 的 GPGPU 基本块序列。

这是他上一篇 [[gpgpu-string-unescaping|GPGPU 字符串反转义]] 的自然续集：那篇用 monoid 同态和 prefix scan 证明"状态机可以并行"，这一篇要啃的是"树结构可以并行"。

## 目标：从 `[[][[][][[]]][][]]` 里长出一棵树

输出格式设计得像 Cap'n Proto / FlatBuffers：每个节点一段连续 word——第一个是 child 数、后面依次是 child 的**数组下标**。关键决策是**结果按 BFS 顺序排**，因为 BFS 顺序下同一父节点的兄弟是连续块，这让很多"查父节点"变成"在排好的数组里扫一下"。

## 三件 GPGPU 原语

- **Scan（前缀扫描）**：任何结合二元算子的前缀和推广。
- **Scatter**：给定 `(condition, index, value)`，把 value 写到 `b[index]`——要求 index 无冲突。
- **Sort**：稳定排序，以 depth 为 key。

这三件事在 GPU 上都有成熟的 work-efficient 实现。算法的全部工作就是"把 parsing 翻译成这三件事的组合"。

## 算法流程（pass 粒度）

1. **Count nodes + depth**：输入扫一遍，`[` 映射成 1、`]` 映射成 0，做 exclusive prefix sum 得到每个字符所属的节点 id；再把 `]` 改成 -1 做一次 prefix sum 得到 nesting depth。顺带校验括号是否平衡——最终 depth sum 必须为 0。
2. **Reduce to nodes**：只关心 `[`（节点开头），一次 scatter 把 depth 收集到 `depth[]`。到这一步输入已经浓缩到 per-node 表达。
3. **Sort by depth**：稳定排序，得到每个节点在 BFS 顺序中的位置 `bfs[]`——实际不真的搬数据，只记"从原序到 BFS 序的 permutation"。
4. **Determine first-child → parent**：扫一遍，条件 `depth[i+1] == depth[i] + 1` 代表 i+1 是 i 的第一个孩子，scatter 出 `1par[bfs[i+1]] = bfs[i]`。
5. **Propagate parent links**：一次 scan 把 first-child 的 parent 信息顺延到所有兄弟（因为在 BFS 排序里兄弟是连续的）。同一轮顺便累计每个 parent 的 child 计数。
6. **Scatter child counts**：每当 `parent[i] != parent[i+1]` 意味着第 i 个是最后一个同胞，此时 `nchild[parent[i]] = count[i]`。
7. **Allocate output**：每节点需要 `1 + nchild` 个 word，做一次 prefix sum 得到每个节点的输出起始地址。
8. **Emit**：两次 scatter：一次写 size，一次写 child 下标（child 写进 `alloc[parent[i]] + count[i]`）。

## 为什么绕得过 stack

传统 Dyck parsing 靠栈压/弹——而栈是 GPU 最讨厌的串行数据结构。这个 sketch 的核心洞察是：**parent / child 关系在 BFS 顺序下有平凡结构**（兄弟连续、parent 单调）。只要把结果从 token 顺序"打散 + 重排"成 BFS 顺序，就不需要栈——parent 信息可以靠 scan 向右传播。

## 成本账

- 3 次 scan
- 4 次 scatter
- 1 次 sort

按 Raph 自己的判断，**sort 最贵**；scan 有非常好的 work-efficient 算法，成本可忽略。scatter 吃全局内存带宽，是第二贵的。这个成本结构决定了算法值不值得做——在 parser 吞吐和 CPU SIMD parser（Mison / [pikkr](https://github.com/pikkr/pikkr)）之间的对比里，是否赢取决于 sort 的实际开销。

## 扩展性

这个框架很容易扩展到：

- **String unescaping**：复用 [[gpgpu-string-unescaping|上一篇]] 的 monoid + scan
- **Dictionaries**：key 的 hash 可以完全并行，hash table 构建也还是 scan/scatter
- **更复杂语法**：但文献里的"并行 parsing for general CFG"不见得对 JSON 这种简单语法有优势

## 后续：stack monoid

Raph 2020 年写了一篇 follow-up "The stack monoid" 把这条路继续推——那篇证明了"带栈的 parser"本身也可以表达成一个 monoid，从而仍然可以 parallel scan。这个 sketch 是那篇的种子想法。

## 评价：sketch 不是实现

Raph 本人明确提醒这篇只是 thought experiment："我没实际跑过，也不太清楚 scatter 和 sort 在实战里到底多贵。" 这正是他 blog 写作风格的典型体现——[[raph-linus|把博客当研究笔记]]：先把思路写清楚、放到社区里、再决定要不要花时间实现。

## 相关

- [[gpgpu-string-unescaping]] — 前作，把状态机并行化
- [[raph-linus]]
- [[cuda-memory-hierarchy]]

## Sources

- [[sources/raphlinus-gpu-json-parsing]]
