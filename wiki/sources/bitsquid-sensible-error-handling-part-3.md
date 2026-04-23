---
tags: [source, bitsquid, error-handling, warnings, deprecation, tooling]
date: 2026-04-19
sources: 1
---

# Sensible Error Handling: Part 3（Niklas Frykholm / Bitsquid）

三部曲完结篇，讨论 **warning** 的治理。

## 摘要

Warning 的悖论：希望它 hard-to-ignore（别被淹没）又 easy-to-ignore（别占用精力）。Niklas 先分类：**performance**（没 mip 的纹理、300 MB 音频）、**suspicion**（空 glyph 的字体、0 粒子的 effect）、**deprecation**（本该 error 只因历史数据没强制）。最激进主张：**能把 warning 升级为 error 就升级**——error 不容忽视、必须立即修，而 warning 会腐烂。Deprecation 的四档出路按"好→坏"排：(1) 写转换脚本，哪怕只能处理 98% 也能把三周手工压到 2.5 小时；(2) 脚本 override，用新引擎 API 在脚本层重新实现旧函数；(3) doomsday clock——warning 写死到期日变 hard error；(4) 投降但封住新入口——源数据加 `bad_name_is_error` flag，新工具生成的一律打上，老数据继续 warn。另外两条系统性建议：**warning 放在工具里**（编辑对象时最有用、成本最低，不是等运行时飘 console）；**做一个 review 工具**按类别列所有 warning，制作人能勾掉「这个真的 OK」的项；甚至可以"新 warning 默认就是 error，除非显式 silence"。最根本心法：每类 warning 都暗示工具没帮用户表达 intent，改工具比指责用户更有效。

## 关键要点

- Warning 三分类：performance / suspicion / deprecation。
- 升级为 error 是主要战术；deprecation 有四档降级路径。
- 转换脚本要避免二元思维——98% 覆盖率也极有价值。
- Warning 应该在编辑器里与当前编辑对象绑定显示，不是运行时 console。
- Review 工具 + "新 warning 默认 error" 的 idea 非常漂亮。
- 评论里 Niklas 顺带讲了他的 singleton 观：名字假装精致实则全局变量；过度使用（Camera、World 为什么只能有一个？）；必须有显式 create/destroy；ProfilerLogging 这种确实适合，但要有 `setup_global_*` / `shutdown_global_*` 生命期接口。

## 链接到的概念

- [[warnings-as-errors-strategy]]
- [[crash-on-unexpected-errors]]
- [[zero-tolerance]]
- [[intent-vs-state]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/02/sensible-error-handling-part-3.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-02-20_sensible-error-handling-part-3.md`
