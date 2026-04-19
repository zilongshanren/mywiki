---
tags: [source, unity, ai, navigation, editor-tool]
date: 2026-04-19
sources: 1
---

# 简易人群模拟系统（Ted Sie / 阿祥的开发日常）

[[ted-sie|Ted Sie]] 发表于 2020 年 4 月的文章，给出 Unity 下基于 Waypoint + NavMesh 的简易人群系统实作，重点在定制 Scene 视图编辑器。

## 摘要

开放世界里的路人群是氛围关键系统。作者的方案由两部分组成：一是 Waypoint 数据结构（记录上一个/下一个 Waypoint 和 Branch 分支点，附对齐地面功能）；二是配套的 Scene 视图编辑器，用 Unity 的 `CustomEditor / OnInspectorGUI / OnSceneGUI / DrawGizmo` 四件套做出"按键 + 鼠标点击即可在地面生成 Waypoint"的快速编辑体验。行人行为很轻：`NavMeshAgent.SetDestination` 走路径，`AnimatorOverrideController` 随机换 walk 动画实现不同步态。作者的隐含观点：**氛围系统不需要复杂 AI，需要好用的编辑工具**——路径能否在几分钟内摆完决定这类系统能否上线。

## 关键要点

- Waypoint 三要素：下一个、上一个、Branch。
- CustomEditor / OnInspectorGUI / OnSceneGUI / DrawGizmo 组合实现所见即所得编辑。
- `Event.current` + `HandleUtility.GUIPointToWorldRay` 在 Scene 视图做拾取。
- `AnimatorOverrideController` 是做体态多样化的便宜手段。

## 链接到的概念

- [[unity-crowd-waypoint-system]]
- [[meshes-of-navigation-recast]]
- [[runtime-editor-console-connection]]

## 原文

- 链接：https://tedsieblog.wordpress.com/2020/04/23/simple-crowd-simulation-system/
- 本地：`raw/articles/tedsieblog.wordpress.com/2020-04-23_simple-crowd-simulation-system-jian-yi-ren-qun-mo-ni-xi-tong.md`
