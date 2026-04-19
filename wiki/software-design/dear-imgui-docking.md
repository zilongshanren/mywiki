---
tags: [imgui, gui, tooling]
date: 2026-04-19
sources: 1
---

# Dear ImGui Docking 分支

[Dear ImGui](https://github.com/ocornut/imgui) 的 [docking 分支](https://github.com/ocornut/imgui/wiki/Docking) 在主干 immediate-mode GUI 的基础上加入：

- 每个 ImGui “window” 可 **拆出浮动** 或 **吸附** 到任意目标
- 支持 multi-viewport，浮动窗口可以真正成为 OS 原生窗口
- 布局按 dock node 树组织，可持久化

[[chris-wellons]] 在构建 [[dcmake]] 时采用这个分支，形容它 “几乎就是一个构造调试器的 UI 工具箱”——因为 Visual Studio 风格的工具窗口浮动/吸附行为本身就是调试器 UX 的核心。

配合 AI 协作的好处：作者指出他以前从未写过 ImGui 代码，但 AI 很擅长生成 ImGui 布局，可以根据粗略描述补细节，甚至预测下一步需求，这对快速构建开发者工具非常有效。

## 相关

- [[dcmake]]

## Sources

- [[sources/nullprogram-dcmake]]
