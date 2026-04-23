---
tags: [source, bitsquid, version-control, tooling, nda]
date: 2026-04-19
sources: 1
---

# Code Share: Source Censoring, Part 2（Niklas Frykholm / Bitsquid, 2013-04-30）

[[niklas-frykholm]] 2013 年 4 月的短文，介绍 Bitsquid 用来"在 NDA 约束下仍给客户提供带历史的源码仓库"的工具 `hg-clone.rb`。

## 摘要

Bitsquid 引擎向客户分发源码，但内部代码含 PS3 / PS4 / X360 等受 NDA 保护的段落。早先的做法是拍快照、跑"审查脚本"把秘密段替换成空行再打包——版本能 build，但丢掉了历史、分支与变更日志，客户既没法 bisect bug 也没法稳定 rebase 本地修改。作者的结论：源码分发唯一合理的形态是一个可 pull 的 Mercurial/Git 仓库。`hg-clone.rb` 就是用来把内部仓库镜像成"过滤后的外部仓库"：按拓扑序遍历源仓库的每个 revision，check out 到工作区，跑过滤程序擦掉秘密，再以原作者/日期/分支/message 提交到目标仓库，只递归转运目标 revision 的祖先，所以秘密开发分支要合并进 release 才会被外传。过滤后版本号无法保留，工具改在 commit message 里插入 `[clonedfrom:rev:hash]` 作为映射标记与增量断点；`--cutoff` 参数还可以截断早期历史。部署上推荐一客户一仓库一过滤器（客户拿到新平台 NDA 时改过滤器最灵活）。

## 关键要点

- 源码分发不该用"快照+censor"，应该是过滤后的 Mercurial/Git 仓库（保留历史、分支、作者）
- `hg-clone.rb`：按祖先递归转运每个 revision，每次提交前跑过滤程序
- 版本哈希无法保留 → 用 `[clonedfrom:rev:hash]` commit marker 做映射和增量判据
- `--cutoff` 可以只暴露从某 revision 起的历史，早期父链统一 reparent 到 cutoff
- 一客户一仓库 + 对应过滤器 比一组合一仓库更容易应对 NDA 升级

## 链接到的概念

- [[repo-clone-with-filter]]

## 原文

- 链接：https://bitsquid.blogspot.com/2013/04/code-share-source-censoring-part-2.html
- 本地：`raw/articles/bitsquid.blogspot.com/2013-04-30_code-share-source-censoring-part-2.md`
