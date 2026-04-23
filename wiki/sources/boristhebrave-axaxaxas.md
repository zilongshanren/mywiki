---
tags: [source, programming-languages, parser, earley]
date: 2026-04-19
sources: 1
---

# Axaxaxas（Boris The Brave / 2015）

[[boris-the-brave]] 2015 年 9 月发布 Axaxaxas——一个 Python 3.3 版本的 **Earley parser**，从一个夭折项目中抽出的能复用部分。文章很短，更像是 release note，但值得记录，因为它点出了 Earley parser 在通用解析器谱系里的定位。

## 摘要

Earley parser 是 1970 年代提出的通用上下文无关文法解析器，能识别任何 CFG，对歧义文法有天然支持；在左/右递归、线性文法上能达到 O(n) 性能，最差情况 O(n^3)。它的主要竞争对手是 LL(k)、LR(k) 这类需要预处理/生成分析表的工具链。Axaxaxas 的设计目标是易用、可定制、无预处理，即拿即用；想跑高性能可以切到 C 写的 **Marpa** 实现。作者没有在文中展开算法细节，只给出 GitHub 与 ReadTheDocs 链接。从 Boris 的整体写作脉络看，这篇是早期程序化生成 / 约束求解兴趣的一个侧面：解析器本质上也是一种对字符串进行结构约束求解的过程，与后来他在 WFC / tileset 的工作有共同味道。

## 关键要点

- Earley parser 接受任意 CFG，包括歧义、左递归；不需要像 LL/LR 那样分文法子集
- 常见文法上线性时间，最坏 O(n^3)；实战里很少触顶
- Axaxaxas 明确不追求高性能，把易用、无预处理、可 hook 作为首要卖点；高性能选 Marpa
- 名字「Axaxaxas」取自博尔赫斯《A God's Script》/Tlön，Boris 喜欢这种有文学气的命名
- 该库停留在 2015 年前后的 Python 3.3，现代使用需注意生态适配

## 链接到的概念

- [[earley-parser]]
- [[boris-the-brave]]

## 原文

- 链接：https://www.boristhebrave.com/2015/09/13/axaxaxas/
- 本地：`raw/articles/boristhebrave.com/2015-09-13_axaxaxas.md`
