---
tags: [版本控制, vcs, git, 工作流]
date: 2026-04-19
sources: 1
---

# Jujutsu：把"重写历史"变成日常

Jujutsu（`jj`）是一套 Git-兼容的版本控制系统。和 Git 共享 commit / 引用存储，所以可以放在现有 Git 仓库上用、对别人看过去就是一条普通 branch。Jujutsu 的主张是：**Git 的数据模型（DAG of commits）优雅，但它的 UI 和操作语义混乱**——Jujutsu 换掉 UI，把一些 Git 里"危险的进阶操作"变成默认流程。

## 四个主要差异

1. **没有 staging area，总是 commit**——working copy 就是当前 commit，任何 `jj` 命令都会先把 working copy 快照到当前 commit。不存在 `git add` 和 `git stash` 的概念。
2. **Commit 是可变的**——因为 working copy 总会覆盖到当前 commit，commit 自然会随时间改变。Jujutsu 为每个 commit 维护 `hash`（和 Git 一致、变化）+ `change ID`（不变的身份），可以追溯同一个 commit "曾经长什么样"。
3. **`jj undo`** 永远能救——几乎任何操作都可回退，不用重新 clone 仓库。
4. **Rewrite history 是 first-class**——`jj edit <change>` 直接跳去编辑任意 commit，冲突自动往后传递、被自动标记"conflicted"，可以先放着继续做别的事。等你准备好时打开冲突文件、删 marker 再 `jj` 一下就搞定。Git 里做 rebase 往往要连锁解决每个 commit 里的同一处冲突；Jujutsu 能把 auto-resolve 往下传。

## 典型工作流

```
jj git fetch
jj new main@origin           # 基于 main 开一个新 commit
# ... 写代码 ... jj 会自动把 working copy 快照到这个 commit
jj new                       # 开始一个新 commit，之前那个固化成历史
jj bookmark set -r @- my-branch   # 把 bookmark（Git branch 等价物）打在上一个 commit
jj git push --allow-new      # 推出去
```

一个关键差异：你**不在 branch 上**，只在某个 commit 上。"branch" 被叫做 **bookmark**，只有手动 `set` 时才会移动——不会像 Git 那样跟着新 commit 自动跑。这意味着 `jj new` 不像 `git commit` 会推进分支头——分支头是你说了算的。

## Revset 语言

Jujutsu 的选择器叫 **revset**，是一套高度正交的小 DSL：`@` = 当前 commit、`@-` = 父、`main@origin` = remote ref、`@-::@` = 一段 range，可以组合嵌套。大多数命令都接受 revset，例如 `jj new bookmark1 bookmark2` = 在两个 bookmark 共同基础上开新 commit（带 merge 意图）。想到什么组合基本都能表达，这是 Git 的 `git rev-list` 语法之外的一套更统一的东西。

## 为什么值得考虑迁移

Evan Todd 给的判断：如果你 **习惯 `git rebase`** 整理 PR，大概率会爱上 Jujutsu——默认工作流就是"你在整理历史"，不需要另学一套 `rebase -i` 命令。如果你 **从不 rebase**，Jujutsu 差别不大，但仍然可以用。

Code review 的大多数痛苦来自"commits 讲不出故事"——杂乱的 "fix tests / appease linter / sync from main / fix typo"。`git rebase` 能整理，但代价是命令心智负担高、容易把仓库搞坏；Jujutsu 把这套操作变成默认流程，外加 `jj undo` 保底。

## 和 Git 的边界处的 footgun

- **关掉 IDE 的 Git 集成**：官方建议把底层 Git 仓当**只读**对待，所有写操作都走 `jj`。VSCode 后台偶尔自动触发 Git 操作，会让 Jujutsu 陷入同一个 change 被两个 commit 引用的"conflicted" 状态。
- **Submodule 不支持**：`jj` 完全忽略 submodules；切换到含 submodule 增删的 commit 会让本地状态永久错位（其实 Git submodule 本身也够乱）。
- Change ID 用的是**不出现在 Git hash 里的字母**——保证不和 commit hash 冲突，通常只需前 2 个字符就能唯一定位。

## 相关

- [[version-control-taste]]
- [[continuous-design]]

## Sources

- [[sources/etodd-jujutsu]]
