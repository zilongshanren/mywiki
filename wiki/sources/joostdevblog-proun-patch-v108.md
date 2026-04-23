---
tags: [source, game-development, pc-porting, gpu-drivers, debugging]
date: 2026-04-19
sources: 1
---

# Proun patch v108 released!（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen]] 发表于 2011 年 9 月的 Proun 补丁复盘文，是 [[pc-gpu-driver-compat-qa]] 的延续案例库。

## 摘要

Proun 发布后三个月 van Dongen 发了 v108 补丁，修了三个 bug，两个属于典型的「显卡驱动说谎」——**ATI Radeon X1xxx 系列（2005）**在 Ogre 查询 Shader Model 3.0 能力时答「是」，但真喂给它复杂 pixel shader 就崩（DOF blur 上中招）；**Intel GMA 3xxx 系列（2006）**走软件模拟跑 vertex shader，`IDirect3D9` 说不支持、`IDirect3DDevice9` 说支持，互相矛盾。解法分别是：给 material 挂「强制用简化 shader」的特定显卡规则；让 Ogre 同时问两个接口并取最宽松答案（Ogre 升级包已修，但 Proun 发行时未敢合）。第三个 bug 是自家数学错误：**求垂直于 cable 方向的向量时用 `cross(dir, [0,1,0])`，当 cable 本身就是 `[0,1,0]` 方向时退化**——Proun 项目开始第一年就埋下，六年后才在 Cubed 用户赛道上稳定复现。

## 关键要点

- ATI X1xxx / X8xx / X9xx、Intel GMA 3xxx 的能力查询都不可信，**只能靠 per-device quirk table 强制降级**。
- 引擎近发行期不要升级——Ogre 的修复存在，Proun 发行时 van Dongen 不敢合入，于是把 bug 带上线。
- `cross(v, up)` 求切平面向量的退化当玩家很少走到该方向时极难触发（估算 1/10000），**用户关卡（Cubed）反而高频踩中**，相当于免费的模糊测试。
- 评论里 GeForce 5 被提起：支持 SM3.0 分支语句、但硬件没有分支，驱动在 shader 编译时做「best-guess」预测——又是另一种说谎方式。
- 结论：**在更多显卡上测，再测。**

## 链接到的概念

- [[pc-gpu-driver-compat-qa]]
- [[joost-van-dongen]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2011/09/proun-patch-v106-released.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2011-09-10_proun-patch-v108-released.md`
