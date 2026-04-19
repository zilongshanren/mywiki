---
tags: [data-structures, c, hash-trie]
date: 2026-04-19
sources: 1
---

# 侵入式哈希 Trie

侵入式哈希 trie 是 [[chris-wellons]] 在 2023 年提出、2025 年底的博文里再次演示的一种复合数据结构：把链表节点和哈希 trie 节点合并在同一个 struct 中——链表节点额外持有 `child[2]` 两个子指针，以 64 位 hash 自高到低位逐位选择左右子，构造时沿 hash 路径走到空指针处落下即可。

相比传统 open addressing 哈希表：

- **不需要 resize**：每插入一个节点只是往 trie 里走几步，没有全表重建
- **节点在 [[linear-allocator|arena]] 上分配**：内存紧凑，cache 行为好
- **同一份节点数据既是链表又是哈希 map**：保留源顺序（可 FIFO 遍历），同时 O(log n) 查询
- **天然多映射**：同一 key 多次插入都在树里，用 iterator 顺 hash 路径下降即可找到全部

构造函数要点：

```
Env *new_env(Arena *a, Env **env, Str key, Str value) {
    for (uint64_t h = hash64(key); *env; h <<= 1) {
        env = &(*env)->child[h>>63];
    }
    *env = new(a, 1, Env);
    ...
}
```

每步用 `h>>63` 取最高位选分支，然后把 h 左移一位。树的深度期望是 O(log n)。

适用于嵌入式和 Wasm 这类不欢迎 libc/动态分配的场景——结合 arena，就是一套“无 resize、无释放、无运行时开销”的键值结构。

## 相关

- [[msi-hash-table]] — 同作者的非侵入、扁平的另一种哈希表
- [[linear-allocator]]
- [[open-addressing-hashtable]]

## Sources

- [[sources/nullprogram-linked-list-intrusive-index]]
