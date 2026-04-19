---
tags: [source, ui, ux, keyboard-shortcuts, desktop, benui]
date: 2026-04-19
sources: 1
---

# UX Opinions（Ben UI）

[[ben-ui]] 的 UX 意见清单，用 RFC 2119 的 must/should/may 分级写下按钮、快捷键、输入、文字、桌面软件共约二十条设计准则。

## 摘要

作者把自己（自嘲不是 UX 专家）的 UX 意见写成可逐条链接的清单，每条给一句强约束、再给一段说明为何。涵盖：可交互元素必须改变 cursor 和 hover 外观并有视觉独立的五种状态；按钮文字必须是动词；禁用按钮必须解释原因；所有按钮都该能绑快捷键、使用频率 >50% 的动作应默认有快捷键、按快捷键要有按钮确认动画、悬停按钮按快捷键应跳到绑定页；菜单导航四种输入（D-pad、摇杆、WASD、方向键）应同义；修饰键只做修饰型长按动作；文字统一 Markdown、单行 <80 字符、为目标受众写作、功能性文字一眼看懂；桌面软件必须多开；万物可链接、可评论，>20 项必可搜索，所有绑磁盘文件的界面都要能"打开所在目录"。

## 关键要点

- 用 must/should/may 分级，而不是"最佳实践"这种软表述。
- 按钮五态必须视觉独立：normal/hover/mousedown/mouseup/disabled。
- 快捷键体系要闭环：默认显示、可改绑定、使用时有视觉反馈、绑定入口可直达。
- 无障碍冗余：颜色/声音/震动都不能作唯一通道——和 [[ui-as-communication]] 呼应。
- 桌面端三要：多实例、可链接跳转、Jump to File Location。
- 很多条款"不是新意而是反复没人做到"——清单化让团队评审时可以逐项打勾。

## 链接到的概念

- [[ux-opinions-checklist]]
- [[ui-as-communication]]
- [[ben-ui]]

## 原文

- 链接：https://benui.ca/blog/ux-opinions/
- 本地：`raw/articles/benui.ca/2026-01-01_ux-opinions.md`
