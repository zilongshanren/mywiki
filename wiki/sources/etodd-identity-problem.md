---
tags: [source, software-design, naming, abstraction]
date: 2026-04-19
sources: 1
---

# The Identity Problem（Evan Todd, 2024-01）

[[evan-todd]] 在 2024 年 1 月写的随笔，把"命名难"这个老梗重述成一个更基础的问题：**判断两个东西是不是同一个东西**。作者把它命名为"identity problem"，并认为大多数技术债务都是 identity mismatch 造成的。

## 摘要

作者提出：命名难的本质是"身份问题"——你要在一个 1,000 维的概念空间里决定在哪儿划分区。名字只是分区标签，真正重要的是它帮工程师把这个东西和别的区分开。技术债大多源自两种 identity mismatch：**一物实为多物**（one-to-many），以及**多物实为一物**（many-to-one）。

前者的经典例子是 StrongDM 早期只支持 Postgres，加密字段叫 `password`；后来加了 SSH，私钥也塞进去；再后来所有奇奇怪怪的 datasource 都把凭据倒进这个字段。即使改名为 `EncryptedData`，也改不了"代码坚称它是一物，而它其实是多物"这个事实。更隐蔽的信号是当你想给函数加一个 `doOtherThing bool` 标志位——这几乎总意味着背后其实是两个不同的东西。

后者是 50 段几乎一样的代码反复复制粘贴。该不该 DRY 起来？作者的判据是给合并后的函数取名：如果能起个具体名字如 `CheckPermissions`，那确实是一物；如果只能起 `Initialize` 或 `PrepareFoosAndAddBars` 这种复合名，那说明要么是两件事、要么 mismatch 在更深的地方。

最后点出 Conway's law：微服务的分区几乎总会自动贴着团队边界划，人类因素也是 identity problem 的一部分。

## 关键要点

- 命名的本质功能是"划分高维空间"，而不是好听或短。
- 一物实为多物的征兆：想加布尔参数、字段名与实际含义脱节。
- 多物实为一物的征兆：50 处复制粘贴，但 DRY 后只能起模糊名字。
- 能否起一个**具体、单一**的名字，是检验合并是否合理的试金石。
- identity problem 涉及人类因素（Conway's law），需要反复重构而非一次到位。

## 链接到的概念

- [[identity-problem-naming]]
- [[abstraction]]
- [[false-abstraction]]
- [[change-amplification]]
- [[modular-design]]

## 原文

- 链接：https://etodd.io/2024/01/09/the-identity-problem/
- 本地：`raw/articles/etodd.io/2024-01-09_the-identity-problem.md`
