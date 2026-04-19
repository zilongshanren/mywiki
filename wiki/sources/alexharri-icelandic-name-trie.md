---
tags: [source, trie, 压缩, 自然语言, 数据结构]
date: 2026-04-19
sources: 1
---

# Compressing Icelandic name declension patterns into a 3.27 kB trie（Alex Harri / alexharri.com）

[[alex-harri-jonsson]] 于 2025 年 8 月的长文，讲述冰岛人名格变库 [beygla](https://github.com/alexharri/beygla) 如何用压缩 trie 把 3,600 个名字的规则塞进 3.27 kB，并对未见名字保持低错误率。

## 摘要

冰岛语名词有四格（主/宾/与/属），数据库里名字永远以主格存储，在界面里需要按句法替换成正确格的形式。作者用 Árnastofnun 公开的 K-format 词形数据配合已批准名字清单抽出约 3,600 条四元组，把每组用最长公共前缀拆成 `"ur,,i,ar"` 这样的后缀编码，把名字**倒序**插入 trie，使共享相同尾缀的名字落入同一子树。然后递归压缩：若子树所有叶值相同，合并为单节点。10,284 节点降到 1,588，非叶节点压掉 95%+。lookup 逻辑修改为「返回路径上最后一个有值节点」，使得压缩 trie 变成后缀模式匹配器——对未见名字也能推断变格模式。在 363,314 冰岛人的真实分布上综合错误率约 0.34%。再加一层「兄弟叶合并」将尺寸从 4.01 kB 降到 3.27 kB。作者总结「规律性 + 全面性」两个前提，并反思为追求体积而牺牲正确性并不划算，司法系统用的 `beygla/strict` 反而更应是默认。

## 关键要点

- **倒序插入**让同后缀名字落同子树，是启用压缩的前提。
- **子树压缩**在有/无反例上给出截然不同结果——`"Baldur"` 的存在使 `dur` 子树不被误压。
- 压缩 trie 不仅省空间，还**自发泛化**出后缀模式匹配能力。
- **兄弟叶合并**是纯尺寸优化，不改查找语义，`findChild` 改成 key 子串包含即可。
- 作者实务反思：`beygla/strict` 10 kB 换 100% 正确，在司法/正式场景应是默认；酷不是交付标准。

## 链接到的概念

- [[compressed-trie-pattern-matching]]
- [[alex-harri-jonsson]]

## 原文

- 链接：https://alexharri.com/blog/icelandic-name-declension-trie
- 本地：`raw/articles/alexharri.com/2025-08-02_compressing-icelandic-name-declension-patterns-into-a-3-27-k.md`
