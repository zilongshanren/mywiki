---
tags: [工具链, 版本控制, 协作, bitsquid, 数据格式]
date: 2026-04-19
sources: 1
---

# JSON 三路合并

用 XML 或 JSON 存游戏内容最常踩的坑，是 git / Perforce 那种**按行做 diff** 的合并器：它完全不知道"这是层级数据"，会把两个人分别改了不同字段的 commit 合出一份结构错乱的 JSON 来。[[niklas-frykholm|Niklas Frykholm]] 在 2010 年写了一个**理解 JSON 结构的三路合并器**，直接在 VCS 里把 Bitsquid 的内容冲突问题消解掉。

这是他在 [[vcs-vs-database-for-content|"VCS vs 数据库"]] 那篇里给自己开的 todo。

## 核心观察：大部分冲突不是真冲突

打开一个 "content conflict" 对话框往往吓人，但多数时候**不是两个人真的改了同一处**。是合并工具把层级数据当成纯文本、错配了括号缩进，把两边的改动胡乱组合。Frykholm 的判断是——只要合并器认得 JSON 结构，这类假冲突就全部消失。

## 对象 diff：简单情形

忽略数组暂时。两个 JSON object 的 diff 可以表达为一组 `object[key] = value` 操作：

- **新增 key**：相当于把 `null` 改成一个值；
- **删除 key**：相当于把值改成 `null`；
- **修改 key**：普通赋值。

三路合并时，把 base 到左的操作集和 base 到右的操作集合并起来即可。唯一真正冲突的场景是**同一个 object 同一个 key 被左右两边改成了不同的值**——这种才算"真冲突"。对真冲突，Frykholm 的处理方式是 **always pick right**：不弹对话框、不让内容创作者在 WinMerge 里读 JSON，而是挑一边继续，让关卡设计师在**关卡编辑器里**修最后那点问题——用对的工具做对的事。

## 数组：语义依赖于 id

数组是难点。`[1, 2, 3] → [1, 2, 4]` 到底是"最后一个元素从 3 改成 4"，还是"删掉 3 再加 4"？没有额外信息无法区分，而这对三路合并结果的影响不一样：`[1,2,3] / [1,2,4] / [1,2,5]` 可以合成 `[1,2,5]` 也可以合成 `[1,2,4,5]`。

Frykholm 的解法是**给数组元素加 `id` 字段**，通常是 GUID：

```json
[{"x": 1, "id": "a"}, {"x": 2, "id": "b"}, {"x": 3, "id": "c"}]
```

这样数组语义就从"按下标定位"变成"按 id 定位"，id 变了就是删+加，id 不变但字段变了就是 update——两种情况泾渭分明，合并算法可以和 object 合并共用一套框架。没 id 的数组也能合并，但退化到启发式猜测，推荐所有 authored 数组都带 id。

## 与 Bitsquid 的内容管线对接

这个合并器只干一件事，但把它装在 VCS hook 上之后，Bitsquid 能继续走 [[vcs-vs-database-for-content|VCS 内容管线]]，同时吃到接近数据库的无冲突协作体验——这条权衡的成立就是合并器实际上好用。它的思路后来在 [[guid-object-database-schema]] 里被 Frykholm 进一步泛化：如果每个对象都有 GUID、每个改动都能表达成 `create/destroy/change/add_to_set/remove_from_set` 这几种原子操作，合并就彻底变成 set union，真冲突的定义被压到一个 key 级别。

Frykholm 把代码放到了公共域（后来迁到 bitbucket），给后来者一个直接可用的起点。

## 相关
- [[vcs-vs-database-for-content]] — 此合并器是这条路线的 enabler
- [[guid-object-database-schema]] — 把同样思路推到彻底的 schema 设计
- [[snapshot-diff-persistence]]
- [[niklas-frykholm]]
- [[sources/bitsquid-collaboration-and-merging]] — 把同一思路再往前推一步：merging 就是协作本身

## Sources

- [[sources/bitsquid-3-way-json-merge]]
