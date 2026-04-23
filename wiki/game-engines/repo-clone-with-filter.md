---
tags: [version-control, mercurial, source-distribution, nda, tooling]
date: 2026-04-19
sources: 1
---

# 带过滤器的仓库克隆（NDA 源码分发）

Bitsquid 引擎以源码方式卖给客户，但内部仓库里混着 PS3、PS4、X360 等平台相关代码，受 NDA 约束不能外泄。早期做法是"打快照 → 跑一个 [[bitsquid-source-censoring-part-2|审查脚本]] 把秘密段替换成空行 → 打包"，这能让发行版编译通过，但也一次性丢掉了历史、分支、变更信息——用户没法查谁在哪次提交引入了 bug，也不能把本地修改干净地 rebase 到主线。[[niklas-frykholm]] 的结论很直接：**分发源码唯一合理的方式是暴露一个 Mercurial/Git 仓库**。

难题在于"既要有历史，又不能把秘密写进历史"。Bitsquid 的做法是一个叫 `hg-clone.rb` 的工具：给定源仓库、目标仓库、过滤程序和目标 revision，它按拓扑序遍历源仓库的每一次提交，把工作区 check out 到那个 revision、在目标仓库目录里跑过滤程序（擦掉秘密代码）、再以同样的作者/日期/分支/提交信息提交到目标仓库。父提交没拷贝过的会递归先拷，只有目标 revision 的祖先才会被转运，所以内部可以安全地维护不该外泄的开发分支——等它合并进 release 分支后，合并提交才会被转运过去。

版本号没法保留——过滤后内容变了，内容哈希就变了。`hg-clone` 的妥协是在目标提交 message 里插一条 `[clonedfrom:116:91fe33c1a569]` 标记，既用来建立 source↔destination revision 的映射，又用来增量判断哪些 revision 已经转运过。还有一个 `--cutoff` 参数可以"遮蔽历史的前半段"——从指定 revision 开始才有历史，更早的父链统一重新父化到 cutoff。

部署形态上有两种：**按客户一库一过滤器**（客户拿到新平台 NDA 就改过滤器；最灵活），或**按 NDA 组合开库**（客户升级到新平台时得换一个仓库，迁移痛苦）。[[niklas-frykholm]] 推荐前者，配一个 cron 把主仓新提交定期克隆过去。这套思路跟 git 里的 `filter-branch`/`filter-repo` 是同宗，只是面向"持续增量发布给外部客户"而不是"一次性重写自己仓库"。

## Sources

- [[sources/bitsquid-source-censoring-part-2]]
