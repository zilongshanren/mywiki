---
tags: [工具链, 内容管线, 版本控制, 协作, bitsquid]
date: 2026-04-19
sources: 1
---

# 游戏内容：VCS 还是数据库？

[[niklas-frykholm|Niklas Frykholm]] 在 2010 年写的一篇短思考，直面一个容易被一拍脑袋带过的问题：游戏的美术 / 关卡 / 配置**数据**，应该放 Subversion / Perforce 这样的版本控制系统里，还是像金融系统那样扔进一个中央数据库？他在对照了两边的长短之后选了**留在 VCS**，但承认这选择有「程序员偏见」的成分。

## 数据库路线的诱惑

数据库模式的好处很诱人：

- 不用 commit / update，改动**立刻对所有人可见**；
- 不会有 merge conflict；
- 天然支持**多人同时编辑同一个关卡**。

代价是放弃 VCS 的三项核心能力：

- **责任追溯 / 历史 / 回滚**；
- **branch / tag**；
- **本地工作副本**（可以先改着不提交）。

金融、零售等行业几十年用数据库做重要的协作，没觉得缺什么——但游戏内容的"版本感"更接近代码：做错了要能退，要能拉分支做 demo，要能在本地拿着一份还没提交的东西先调通再 push。

## Frykholm 的选择与理由

他不愿放弃 VCS 的三件事，所以留在 VCS。评论里有同行给出反例——**Criterion 在 Burnout Paradise 上用的是数据库**，而且还在 SQL 上**重写了一套 Perforce 风格的版本控制**，每个用户有本地库，主库中心化，binary 仍然留在 Perforce。能跑，而且 referential integrity 给得特别好（你删不掉别人还在引用的资源）。但 Frykholm 的反驳是：**如果你在数据库上重造 VCS，就像在 VCS 上重造数据库一样糟糕**。

另一位评论者推 CouchDB（JSON + MVCC）——Frykholm 看了一眼说它的版本系统自己也承认"不适合当 revision control"，所以依然不贴合。

## 不放弃 VCS 但要解决协作

留在 VCS 但想要"改动立即对所有人可见"的体验，有两件事要做：

1. **把 editor 绑到 `svn update` / `svn commit`**：每次改动立即 commit，每次打开立即 update，仓库就模拟出了数据库的"即时性"。
2. **把 merge 做透**。Bitsquid 把几乎所有数据都存成 JSON-like 结构，所以只要写一个 **JSON-aware 的三路合并器**，冲突只发生在"两人同时改了同一对象的同一字段"——真实项目里极少见。

这两步做完之后，VCS 就吃掉了数据库几乎全部的协作优势，同时留住了历史 / 分支 / 工作副本。Frykholm 在这篇里给自己开的后续 todo 就是「写个 3-way JSON merger，然后去做协作式关卡编辑器」。

## 延伸思考：referential integrity

评论区最硬的反驳来自"用了就觉得回不去"的 referential integrity——数据库里你删不掉还在被引用的对象，引擎少写一大堆「找 broken reference」的工具。Frykholm 承认这个好处，但认为在 VCS 侧写一个 linter / garbage collector 也能做到：

- 每个对象分一个 GUID；
- 每个属性要么是标量，要么是 GUID（或 GUID 列表）；
- 每个对象一个文件（方便 merge），**三种操作**：create / destroy / change property；
- 删除前检查有没有人引用该 GUID，或做 mark-and-sweep GC 扫孤儿对象。

这套 schema 在 2010 年提出来的时候已经很像后来 Unity ScriptableObject / Unreal Asset 的引用模型了。

## Sources
- [[sources/bitsquid-content-repositories-vs-databases]]
- [[sources/bitsquid-3-way-json-merge]]
- [[sources/bitsquid-new-data-storage-model]]
- [[sources/c0de517e-vcs-next-gen]] —— Pesce 2011：按「源码 / 资产 / 构建产物」三分法来选工具的早期表述
