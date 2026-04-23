---
tags: [重构, 代码清理, 遗留代码, 工程纪律, yagni, bitsquid]
date: 2026-04-19
sources: 1
---

# 清理烂代码：改良派的操作手册

[[niklas-frykholm|Niklas Frykholm]] 2012 年给出的一份关于"如何处理继承来的一堆烂代码"的实操清单——来源可能是中间件、开源项目、离职同事的模块，或者公司深处那个"没人有时间盯他"的角落里长年累月长出来的东西。

贯穿全文的一个选择：**改良（reform）而非革命（revolution）**。不是说 rewrite 永远不对，而是多数情况下人们会低估现有代码做对了的那些细节，从而选错。

## 0. 先问值不值得清

这是第一个、也是很多人跳过的判断。Niklas 的措辞是"**karate do yes / karate do no**"——要么认领它、清到自己愿意维护，要么就当成别人的，做最小改动解决手头问题。两种都有道理，骑墙是最糟的。

决策因子：

- **你预计要改多少次？**——只一个 bug vs 未来长期 tweak？
- **需要跟上游合并吗？**——开源活跃项目大改会陷入 merge hell。最好就 patch 回去。
- **工作量？**——每天清 100~10000 行，取中位数 1000。3 万行模块 = 一个月。付得起吗？
- **是核心还是外围？**——font rendering / image loading 这类你可能整个换掉，就别清了；核心能力的代码**必须拥有**。
- **有多烂？**——可接受的烂可以留；"12000 行一个函数"这种得动手。

## 1. 拿到一个测试

"严肃清理一段代码意味着弄坏它。"没有测试你根本不知道什么时候坏的。Unit test 最好；不行就用 integration test（跑一关、让角色做特定动作）。跑一次很贵？——**不必每次改动都跑**。配合 source control，每 5 次 commit 跑一遍，发现崩了就二分就是。发现一个测试没捕捉到的问题——把它**加回测试**。

## 2. 用 source control

如果公司的系统烂到不够用，本地 clone 一个 mercurial / git 仓库放进去改。"花一小时学 mercurial，或者 30 小时学 git"——他自己的梗。**大量小 commit** 是清理最重要的节奏。

## 3. 一次只改一小步

两条反面经验：

- 开始重构到一半觉得"顺手把 API 也理顺"——**不要**。先把继承链拆了 commit，然后再动 API。
- 改到一半发现方向错了——**revert**，不要硬改下去。

他的原话："Smart programmers organize the way they work so that they don't have to be that smart."

把"现在的代码 → 你想要的代码"拆成一串小步骤：重命名 → 成员改函数参数 → 重排算法 → …每步独立 commit。

## 4. 不要一边清一边加功能

这是 #3 的推论但值得独立写一条。清理的目标是"不改行为让代码更好"，加功能的目标是"改行为让它更好"——**方向相反**。混着做时你无法判断"我这一步是没改变行为、还是引入了新 bug"。先清干净，**再**在干净基础上加功能。

## 5. 砍掉你不用的功能

清理成本正比于代码量 × 复杂度 × 乱度。**当前不用、可见未来也不用的功能就删掉**。别为"说不定哪天会用到"留着——代码是成本，不是资产。真要用回来，从版本历史里挖。

## 6. 删掉大多数注释

Niklas 对烂代码里的注释评价很低——他列了四类典型：

- **pointless**：`// Set x to 3` + `x = 3;`
- **incomprehensible**：`// Fix for CB (aug)` + 一个魔法数向量
- **sowing fear and doubt**：`// Really we shouldn't be doing this`
- **downright lying**：`// p cannot be NULL here` 后面跟着 `p->...`

读到看不懂或没帮助的——**删**。注释掉的 dead code、`#ifdef` 掉的 dead code，也删（source control 里有）。而且清理会大量重排代码，**老注释多半会被 refactor 变成错的**——"没有单元测试能告诉你注释坏了。"

好的代码需要很少注释，因为变量名 + 清晰的函数边界 + 简单算法 + assert 本身就是文档。

## 7. 干掉 shared mutable state

他认为**这是理解代码最大的障碍**——不是多线程本身难，而是多线程共享 mutable state 才难。分类：

- **全局变量**——是的还要再说一次。但**全局常量没问题**（Pi、`sprintf` 不是罪）。
- **对象本身就是 shared mutable state 的大口袋**——members 多到像 global；懒的程序员"随便塞个 member 让两个 method 通信"。
- **megafunction**——12000 行长函数的"传奇"。局部变量在这种规模下**几乎和全局一样糟**。
- **非 const 的引用 / 指针参数**——悄悄共享。

干预手段：拆函数、拆对象、成员设 private、方法改 const 返结果而非改状态、方法改 static 吃参数而非读成员、彻底去掉对象改纯函数、局部变量加 const、参数加 const。

## 8. 干掉不必要的复杂度

YAGNI——**你不会需要它**。过度工程化的表征：序列化、引用计数、虚接口、抽象工厂、visitor……**支撑结构比业务代码还多**。两种成因：最初雄心比最终实现大得多；程序员读了太多设计模式书，以为重骨架 = 高质量。

反讽的是**这种刚性模型反而适应不了真正的需求变化**——后来的功能只能以 hack / bolt-on / backdoor 的方式塞进来，形成"绝对秩序 + 彻底混乱"的分裂。

实操：砍未使用的功能；简化必要概念、去掉不必要的；移除不必要的抽象、换成具体实现；简化继承层级；若只用一种配置就不要保留配置开关。

## 与作者其他立场的呼应

- 第 7 条和 [[polling-callbacks-events]] 里对 callback / event 的警觉是同一个"action at a distance"担忧的不同面——共享可变状态是静态的、callback/event 是动态的，二者都可怕。
- 第 8 条是 [[tactical-programming]] vs [[strategic-programming]] 的另一写法——但注意 Niklas 的 YAGNI 倾向比 Ousterhout 的 strategic design 更偏实用主义，他对"未来灵活性"的默认态度是**怀疑而非投资**。
- 第 3 条的"一次只改一小步 + 持续 commit"是很多 Bitsquid 工程纪律（[[now-principle-productivity]]）背后的同一肌肉。

## 相关

- [[niklas-frykholm]]
- [[clean-code-critique]]
- [[tactical-programming]]
- [[strategic-programming]]
- [[now-principle-productivity]]
- [[red-flags]] — Ousterhout 的坏气味清单
- [[false-abstraction]]

## Sources

- [[sources/bitsquid-cleaning-bad-code]]
