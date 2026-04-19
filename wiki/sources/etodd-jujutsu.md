---
tags: [source, vcs, git, 工作流]
date: 2026-04-19
sources: 1
---

# Should I Switch From Git to Jujutsu（Evan Todd / etodd.io）

[[evan-todd]] 2025 年 10 月的博客，给犹豫是否试 Jujutsu 的人的一个决策框架。

## 摘要

作者把读者分两类：**用 `git rebase` 整理 PR** 的——"你大概率会爱上 Jujutsu，直接跳到 Part Two 看差异点"；**只 commit + sync main** 的——先讲为什么 rebase 有意义：code review 的痛苦大多来自"commit 讲不出故事"（huge refactor / fix tests / appease linter / sync from main × 4 / fix typo），rewrite history 能把这锅乱麻理成"作者能预知未来"的直线叙事。

Part Two 列四条 Jujutsu 和 Git 的核心差异：(1) 没有 staging area，working copy 永远被快照到当前 commit；(2) commit 可变，每个 commit 除了 `hash` 还有不变的 `change ID`；(3) `jj undo` 永远可回退；(4) rewrite history 是 first-class workflow。

然后讲 `jj edit <change>` 的冲突自动传递——Git 里 rebase 往往要在每个 commit 重解同一冲突，Jujutsu 把解完的结果自动 propagate 下去。典型工作流：`jj git fetch` → `jj new main@origin` → 写代码 → `jj bookmark set -r @- my-branch` → `jj git push --allow-new`。Bookmark 是 Jujutsu 对 Git branch 的等价物，但不跟随新 commit 自动前移，得手动 set。

讲 revset 语言：`@`/`@-`/`main@origin`/`bookmark1 bookmark2` 的组合性——"想到什么表达基本都能拼出来"。同仓对其他人就是一条普通 Git 分支；给同 bookmark 多次 edit 后 push 对方看见的是 rebase。

最后是 footgun 清单：(a) **关掉 IDE 的 Git 集成**——Git 写仓被当只读，VSCode 后台自动 Git 操作会让同一 change 被两个 commit 引用（"conflicted" 状态）；(b) submodule 完全不支持、切分支会错位（但 Git submodule 本身也够乱）。

## 关键要点

- 决策分叉：用 rebase → 试 Jujutsu；不用 rebase → 可以不急。
- Jujutsu 不发明新存储，和 Git 共享仓、对别人透明。
- `change ID` 是 commit 的永久身份，hash 会随 rewrite 变。
- Working copy = current commit，取消了 Git 里 index / stash / working tree 的三元区分。
- Rewrite history 是默认工作流，不是"进阶危险操作"。
- Revset DSL 正交性好，组合能力强。
- IDE Git 集成要关、submodule 别指望。

## 链接到的概念

- [[jujutsu-vcs]]

## 原文

- 链接：https://etodd.io/2025/10/02/should-i-switch-from-git-to-jujutsu/
- 本地：`raw/articles/etodd.io/2025-10-02_should-i-switch-from-git-to-jujutsu.md`
