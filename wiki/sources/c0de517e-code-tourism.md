---
tags: [source, 学习方法, 代码阅读, 工程文化]
date: 2026-04-19
sources: 1
---

# Code Tourism（Angelo Pesce / C0DE517E）

[[angelo-pesce]] 2011 年 1 月的短文，提出把「读别人的代码」当成和「画家逛画廊」同等级的学习方式，并呼吁开源项目与公司提供「code tours」这种导览基础设施。

## 摘要

Pesce 以 Paul Graham 的 _Hackers and Painters_ 和 Raymond 的 _The Cathedral and the Bazaar_ 为引，指出「编程 = 艺术」这个类比常被提，但我们的**学习过程**却远不如艺术家系统——画家除了动手，还会**系统地研习前人作品**，程序员一旦变得有经验就倾向丢掉这个动作。

他提议**code galleries**：开源项目应在 wiki 里专门开「入口页」列出值得一读的主路径、主要函数、精彩片段——像旅游局的 sightseeing 指南。他举 Linux 内核相关的 Stack Overflow 问答作样本，并指出 boost 这类项目天然「旅游友好」，而别的代码库（他用意大利的 Naples 作比喻）宝藏多但对游客不友好，更需要导览。

这个实践对公司内部也成立——Pesce 自己每到新项目就会写一份渲染主流程的 wiki 导览。他进一步提议把「精彩代码片段陈列馆」做成日常实践：由 lead / TD 在代码评审时摘录值得欣赏的片段、附短评。

评论区多为赞同，并补充：开源本身才是 code tourism 的前提、每个软件项目都应做成「可交互的书」。

## 关键要点

- **对照画家教育**：画家有参考 / 草图 / 构图 / 细化，对应读论文 / 探索式编程 / 设计 / 自顶向下编码——但画家还有「研习前人作品」这一环，程序员经常缺失。
- **两个障碍**：自命不凡 + 读懂陌生代码的前期成本高、事先不知道里面有什么。
- **Code galleries 的建议**：wiki 入口页、主路径导览、精彩片段陈列，让读代码有明确的起点。
- **内部同样适用**：Pesce 自己做的渲染主流程 wiki 导览就是 code tourism 的模板。
- **和 [[code-as-art-manifesto|code rights]] 的关系**：那篇是「代码该是艺术」，这篇是「艺术需要美术馆 / 美术史」——教育学侧的补充。
- **反对只做 kata**：引 Atwood 的 _ultimate code kata_，但反对把学习完全压缩为自己做练习题——读别人的代码同等重要。

## 链接到的概念

- [[code-tourism-practice]]
- [[code-as-art-manifesto]]
- [[angelo-pesce]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/01/code-tourism.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-01-11_code-tourism.md`
