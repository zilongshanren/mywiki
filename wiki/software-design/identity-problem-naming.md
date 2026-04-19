---
tags: [命名, 抽象, 技术债]
date: 2026-04-19
sources: 1
---

# Identity Problem —— 判断两物是否同一

[[evan-todd]] 提出的术语，用来重新表述"命名难"这件老生常谈的事。本质上，编程里最难的问题不是取个好名字，而是**决定两个东西到底算同一个东西、还是不同的东西**。名字只是分区的标签。

## 1,000 维空间里的分区

可以把所有代码实体想象成在一个 1,000 维概念空间里的点。给某个东西起名 `Foo`，就是把它扔进 `Foo` 分区；起名 `Bar` 就是扔进 `Bar` 分区。未来别的工程师在做相似需求时，会先搜分区里有没有现成的东西——他们是否会把新东西塞进你划的分区里，完全取决于你给的名字。

这套思路和 [[abstraction]]、[[false-abstraction]] 的讨论一脉相承：抽象就是划分区，坏的抽象就是分区划错了。

## 两种 identity mismatch

技术债务大多由两类错误分区造成：

**一物实为多物（one-to-many mismatch）**：一个字段、一个函数被当作单个概念，但实际上承载了多种含义。StrongDM 那个 `password` 字段——先是 Postgres 密码，然后是 SSH 私钥，再后来是各种凭据——就是典型。换个中性名字如 `EncryptedData` 也只是粉饰。典型征兆是**给函数加布尔参数**：`DoThing(doOtherThing bool)` 几乎总意味着背后其实是两件不同的事。

**多物实为一物（many-to-one mismatch）**：同一段代码复制粘贴了 50 次。该不该 [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) 起来？作者的判据是**试着起名**：如果能给合并后的函数起一个具体、单一的名字如 `CheckPermissions`，那确实该合并；如果只能起 `Initialize` 或 `PrepareFoosAndAddBars` 这种"多件事拼一起"的复合名，则说明 mismatch 在更深层次，盲目 DRY 只是把错误抽象固化下来——这就成了 [[false-abstraction]] 或 [[classitis]] 的温床。

## 与 Conway 定律的交织

identity problem 不只是技术问题，也涉及人类因素：微服务、模块划分几乎总会沿着团队边界自动生长（Conway 定律）。所以"最好的分区"不是纯技术判断，需要对业务、客户、团队结构有深入理解；也因此只能通过持续重构迭代逼近，而不可能一次性设计到位。[[continuous-design]] 与 [[strategic-programming]] 也在讲这件事。

## 相关

- [[abstraction]]
- [[false-abstraction]]
- [[change-amplification]]
- [[modular-design]]
- [[deep-modules]]
- [[continuous-design]]

## Sources

- [[sources/etodd-identity-problem]]
