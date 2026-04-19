---
tags: [ui, ux, input, keyboard-shortcuts, accessibility]
date: 2026-04-19
sources: 1
---

# UX 意见清单（Ben UI）

Ben UI 用 RFC 2119 的 must/should/may 级别写下一套游戏与桌面软件 UX 意见。多数不是原创而是对行业 best practice 的重新表述，但清单式的可链接形式让它成为"争论时可以直接甩链接"的参考。

## 按钮

- **Cursor Change（must）**：可交互元素必须让鼠标指针变化。玩家日常上网形成肌肉记忆，游戏里不变就逼玩家"思考"。理想是改成指点手👆，至少要在视觉上与默认指针明显不同。可拖拽换抓手🖐️，可输入文字换 I 光标。
- **Hover 外观变化（must）**：指针移上去按钮必须有显著视觉变化。80% → 90% 透明度这种幅度不算。
- **可点元素必须有视觉上独立的状态**：normal / hover / mousedown / mouseup / disabled 各自可辨。
- **Button is a Verb（must）**：按钮上写动词。不用"Yes / No"，用"Save / Cancel"。玩家应该仅凭按钮文字就能决策，不必回头读上下文。
- **禁用时解释（should）**：灰掉的按钮应能通过 tooltip 或点击给出"为什么被禁用"和"如何恢复"。

## 快捷键

- **Show Shortcuts In-place（must）**：按钮如果有快捷键，必须在按钮内部或 tooltip 里显示，这是让玩家学快捷键最有效的方式。
- **All Buttons can have Shortcuts（must）**：所有屏幕按钮都必须允许设置快捷键。设计师无法预知哪个功能会被高频使用，也无法预知无障碍需求。
- **Default Shortcuts for Common Actions（should）**：使用率 >50% 的动作默认给快捷键。50% 是拍脑袋的阈值，精神是"多数情况下都做的事不该逼玩家鼠标点"。
- **Show Button Activation on Shortcut（must）**：按快捷键时对应按钮要有"确认"反馈动画。
- **Shortcut to Binding Configuration（should）**：悬停按钮时按下某个快捷键应跳转到绑定界面——让"改绑定"和"用绑定"一样顺手。

## 输入

- **D-Pad / 左摇杆 / WASD / 方向键应同义**：菜单导航里，除非有明确理由，四种输入都要能用。
- **修饰键做修饰行为**：Ctrl/Shift/Alt 不该用在单次动作（如切武器），应用在长按型修饰（如 Shift 跑步）。

## 文字

- **到处支持 Markdown**：文字格式化统一用 Markdown 或类似的最小标记。
- **Write for your Audience**：面向儿童的游戏别用"modified"，用"changed"。
- **单行 < 80 字符**：英文阅读最佳每行 50–70 字符。
- **功能性文字一眼看懂**：用加粗、斜体、颜色、🪙 图标高亮关键点。flavor 文本不受此约束。

## 桌面软件

- **允许多实例（must）**：任何桌面应用都应允许多开。GitHub Desktop 强制单窗口切换仓库，丢上下文、无法对比改动。

## 杂项

- **所有东西都可链接**：文件、菜单项、屏幕都应有可复制链接，点击能直接跳过去。例：[Hermes](https://github.com/jorgenpt/Hermes) 为 UE 资产加可点 URL。
- **到处都可评论**：共享创作工作流都应允许加评论。Figma、代码、甚至 Breath of the Wild 的开发阶段允许开发者在游戏世界里插便签。UE 的自定义 data struct 每条都该有 comment 字段。
- **数量 > 20 就要搜索**：选项菜单、File/Edit/Window 下拉菜单，任何超 20 项的集合都必须可搜索（至少纯文本）。
- **Jump to File Location**：界面若对应磁盘文件（日志、存档、截图、设置），必须有"打开所在目录"的快捷方式。软件自己知道路径，别逼用户去翻。

## 价值

这份清单的价值不在每条的新意，而在把模糊的"好体验"拆成可逐条检查、可被链接吐槽的工程规范。配合 [[ui-as-communication]] 里的"传达视角"可以组成一套 UI/UX 自检表。

## 相关

- [[ui-as-communication]]
- [[ben-ui]]

## Sources

- [[sources/benui-ux-opinions]]
