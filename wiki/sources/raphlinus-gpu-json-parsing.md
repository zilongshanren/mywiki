---
tags: [source, gpgpu, parsing, json, 并行算法]
date: 2026-04-14
sources: 1
---

# Towards GPGPU JSON parsing（Raph Levien 2018）

[[raph-linus]] 2018 年 5 月的一篇 sketch——他本人坦承"还没实现过、对 GPU 几乎没有实操经验、谁知道会出什么幺蛾子"。文章的价值是算法设计层面的：把 JSON parsing 里最难啃的那一块（括号嵌套结构）拆成纯 scan/scatter/sort 的流水线，**完全绕过栈这个 GPU 天敌**。这是前作 [[sources/raphlinus-gpu-unescaping|String unescaping sketch]] 的自然续集，也是他 2020 年 "The stack monoid" 文章的种子。

## 摘要

任务抽象为 Dyck 语言解析：输入形如 `[[][[][][[]]][][]]`，输出是一棵树的 FlatBuffers 式紧凑表达（每个节点是一段连续 word，首个是 child 数、后面是 child 的数组下标），**按 BFS 顺序排布**。Raph 只允许自己使用三种 GPGPU 原语——scan、scatter、sort——然后把整个 parser 拆成 8 个 pass 的流水线：第一步把 `[`/`]` 映射到 ±1 做 prefix sum 得到 per-char 的 node id 和 nesting depth；然后 scatter 出 per-node 的 depth；稳定 sort by depth 得到每节点的 BFS 位置；扫一遍识别"first child → parent"关系；再一次 scan 把 parent 信息向右传播给所有 sibling（BFS 排序下 sibling 连续）、顺便累计 child 数；scatter 出 per-parent 的 child count；prefix sum 算出每个节点的输出起始地址；最后两次 scatter 写 size 字段和 child 下标。整条管线是 **3 个 scan + 4 个 scatter + 1 个 sort**，其中最贵的是 sort，scan 非常廉价。核心洞察是："parent / child 关系在 BFS 顺序下是平凡结构"——sibling 连续、parent 单调——因此靠 scan 向右传播即可代替栈。

## 关键要点

- **关键创新**：不是改 parser 算法，而是**换输出顺序**（BFS 而非 DFS），让 parent-sibling 关系变成可扫的单调序
- **栈消失了**：传统 Dyck parsing 必须有栈来追踪 nested brackets，这里完全用 scan + scatter 替代
- **cost breakdown**：sort 最贵 → scatter（全局内存带宽）→ scan（基本免费）
- **Scan/scatter 扩展性好**：string unescaping（复用 monoid）、dictionary key hashing、hash table 构建都能套同一个框架
- 作者明确提醒：**这只是思路 sketch，没实际实现**；与 CPU SIMD parser（Mison、pikkr）的对比需要真跑才知道谁赢
- 2020 年的 **"The stack monoid"** follow-up 把"栈 parser 也是 monoid"推到底，完成了这个 sketch 的理论闭环

## 链接到的概念

- [[gpgpu-json-parsing]]
- [[gpgpu-string-unescaping]]
- [[raph-linus]]
- [[cuda-memory-hierarchy]]

## 原文

- 链接：https://raphlinus.github.io/personal/2018/05/10/toward-gpu-json-parsing.html
- 本地：`raw/articles/raphlinus.github.io/2018-05-10_towards-gpgpu-json-parsing.md`
