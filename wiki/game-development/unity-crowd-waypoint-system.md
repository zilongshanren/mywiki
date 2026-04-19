---
tags: [unity, ai, navigation, editor-tool, crowd]
date: 2026-04-19
sources: 1
---

# Unity 人群 Waypoint 系统

开放世界游戏（GTA、看门狗、人中之龙…）里的路人群是烘托世界氛围的重要旁支系统。[[Ted Sie]] 给出一套在 Unity 中实现简易人群模拟的方案，核心是**路径编辑器 + NavMesh**，重点不在 AI 本身，而在 **定制 Scene 视图编辑体验**。

## Waypoint 数据结构

一个完整的 Waypoint 只需记录三类关系：

- **下个 Waypoint**：从"上一个"方向走来时，下一个目标点。
- **上个 Waypoint**：从"下一个"方向走来时，下一个目标点（双向可行走）。
- **路径分支（Branch）**：当人物走到路径尽头或分叉时，决定下一步走哪条路。
- **对齐地面**：一键把 Waypoint 高度投射到地形表面，方便在起伏地形上编辑。

## 定制编辑器四件套

Unity 里"在 Scene 视图里舒服地摆点"靠四个 API：

- `CustomEditor` — 告诉 Inspector 用自定义 Editor。
- `OnInspectorGUI` — 在 Inspector 面板里加提示/按钮/字段。
- `OnSceneGUI` — 拦截 Scene 视图的鼠标/键盘事件。结合 `Event.current` 与 `HandleUtility.GUIPointToWorldRay`，可以做出"按下某键就在鼠标所指地面位置生成 Waypoint"的快速编辑体验。
- `DrawGizmo` — 给 Waypoint 画自定义 Gizmo（带选中态），让路径在场景里可视。

## 人物行为

每个行人的行为配置都很轻：

- `NavMeshAgent` 驱动移动，`SetDestination` 丢目标点。
- `AnimatorOverrideController` 动态换 walk 动画——同一 Animator Controller 下根据不同 AnimationClip 可做出不同步速/体态的行走效果，随机挑一个实现"每个路人走路姿势不一样"。
- 到达 Waypoint 后按 Branch 选择下一个目标点，循环往复。

## 设计重点

系统本身非常简单，但给出的启示是：**游戏世界的"氛围系统"往往不需要复杂 AI，而需要一套好用的编辑工具。** 路径能否被场景美术三分钟摆完，是这类系统能否真正上线的关键。

## 相关

- [[meshes-of-navigation-recast]]
- [[runtime-editor-console-connection]]
- [[unity-complexity-patterns]]
- [[tools-first-iteration-loop]]

## Sources

- [[sources/tedsie-crowd-simulation]]
