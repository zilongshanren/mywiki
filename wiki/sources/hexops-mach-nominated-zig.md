---
tags: [source, zig, mach, 版本管理, 工具链]
date: 2026-04-19
sources: 1
---

# Announcing Mach nominated Zig versions（Stephen Gutekanst / Hexops devlog）

[[stephen-gutekanst]] 2024 年 1 月的文章，正式化了 Mach 引擎"每月从 Zig nightly 里挑一个快照作为 Mach 生态固定基准"的做法，给 Zig stable 和 nightly 之间填了一层"提名版本"。

## 摘要

Zig 当时每年两次 stable release（功能滞后 6 个月以上），nightly 又天天在变。Mach 用 nightly 但更新频率 ad-hoc——每次升 Zig 要动 40+ 个 Zig 仓库，还要拉着整个 Mach 用户群一起动。作者把这件事做成月度节奏：1 月和 7 月是 Mach release，偶数月挑 Zig nightly 提名为"2024.x.0-mach"版本，并确认提名的 Zig 与所有 Mach 仓库都兼容后再定稿。其他 Zig 项目（如 zig-gamedev）也被鼓励对齐到同一个提名版本上，让生态有一个公共的 Zig 基准。Mach 用户因此能比 stable 用户快 2-3 倍拿到 Zig 新功能，又不用承担 nightly 日日漂移的代价。

## 关键要点

- Zig 处在 pre-1.0，stable 与 nightly 的矛盾是生态级问题，不是个人偏好。
- 一次 Zig 升级要从依赖图底部往上推，需要"整个生态同步"能力，不能一家一家 merge。
- 提名 cadence：3、5、6、9、11 月各一次，4、10 月跳过；1、7 月是 Mach release。
- 版本号 `2024.1.0-mach` 映射到具体 Zig nightly commit。
- 不是所有语言都需要这个机制——它的必要性随 Zig 稳定下来会消失。

## 链接到的概念

- [[mach-nominated-zig-versions]]
- [[mach-engine]]
- [[stephen-gutekanst]]

## 原文

- 链接：<https://devlog.hexops.org/2024/announcing-nominated-zig/>
- 本地：`raw/articles/devlog.hexops.org/2024-01-07_announcing-mach-nominated-zig-versions.md`
