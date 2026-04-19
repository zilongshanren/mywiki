---
tags: [zig, 版本管理, 工具链, mach, 生态协调]
date: 2026-04-19
sources: 2
---

# Mach 提名 Zig 版本

Zig 官方提供两种完全极端的使用方式：**stable**（一年两发，migration 文档齐备、但新特性要等半年以上）和 **nightly**（功能最新，但每天一变，且大规模重构期间可能不稳定）。[[mach-engine|Mach]] 自己长期用 nightly，但它的 40+ Zig 仓库加上无数下游用户承受不起无序漂移，于是 [[stephen-gutekanst]] 把"提名某个 nightly 快照作为 Mach 生态的固定基准"这套实际做法正式化为 **Mach nominated Zig versions**。

## 核心机制

每年 1/7 月是 Mach 的 release 月，偶数月（3、5、6、9、11）从当月 Zig nightly 里挑一个快照提名为 Mach 生态的统一版本，版本号形如 `2024.1.0-mach`，对应某个具体的 Zig nightly commit。提名流程并非挑出来就完事——必须先确认这个 nightly 版本与所有 Mach 仓库兼容后才算定稿。

## 解决的具体痛点

- 更新 Mach 的 Zig 版本等于更新 40+ 个仓库的依赖树，要从依赖底层逐层往上升级代码与 CI，还要让用户跟着升——频率做成月度比起 ad-hoc 更可控。
- Mach 社区里很多人只用一部分 Mach 模块，pull request 堆积时无法逐个合并，因为一次 Zig 升级必须所有仓库同步；提名版本给了一个 "这批 PR 都打哪个 Zig 之上" 的共同锚。
- 跨项目协调：`zig-gamedev` 等第三方也可以对齐 Mach 的提名版本，让生态 Zig 版本互相兼容。Zig nightly 用户也可能"凑巧"兼容。

## 和业界做法的对比

把它放回语言生态光谱：Rust 的 stable/beta/nightly 是时间驱动、6 周一轮；Go 是严格向后兼容；Node.js 的 LTS 是 "长期支持" 但以稳定性为主。Mach 的提名属于第三条路——**nightly 快照打月度戳**——只适合语言本身还在 pre-1.0、释放频率高但生态需要锚点的状态。Zig 未来稳定下来后这一机制的必要性会下降。

## 相关

- [[mach-engine]]
- [[stephen-gutekanst]]
- [[zig-package-mirror]]

## Sources

- [[sources/hexops-mach-nominated-zig]]
- [[sources/hexops-mach-v0-3-released]]
