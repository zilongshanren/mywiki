---
tags: [data-structures, hash-table, c]
date: 2026-04-19
sources: 1
---

# MSI 哈希表

MSI（Mask-Step-Index）哈希表是 [[chris-wellons]] 在 2022 年提出、在 2025 年底“Linked lists, revisited”中再次展示的一种扁平 open addressing 哈希表，结构极简：

```
typedef struct {
    Env **slots;
    int exp;   // 槽数是 2^exp
} EnvTable;
```

三要素：

- **mask** — 槽数为 2 的幂，索引即 `i & mask`
- **step** — 从 hash 高位取一个奇数做 double hashing 的步长：`(hash >> (64 - exp)) | 1`
- **index** — 初始 `i = hash`，每次 `i = (i + step) & mask`

作为步长与 mask 互素（奇数与 2^exp），保证能走遍所有槽。装载因子阈值由 `(1<<exp) - (1<<(exp-3)) < len` 控制，约 7/8。

在博文的用法中，MSI 表并不直接存储键值，而是 **在已有链表之上索引链表节点**（slots 存 `Env *`）。优点：

- **非侵入**：链表节点完全不变，可以在同一链表上建多张索引（比如分别按 key 和 value 长度）
- **常数时间查询**
- **仍是多映射**：查找只检测空 slot 停止条件，iterator 可以继续拿下一个同 key 命中

代价：列表扩张时需要重建更大的表。适合“构建一次，大量查询”的场景。

## 相关

- [[hash-trie-intrusive]] — 同作者的另一种索引形式，侵入但无需 resize
- [[open-addressing-hashtable]]
- [[non-cryptographic-hash]]

## Sources

- [[sources/nullprogram-linked-list-intrusive-index]]
