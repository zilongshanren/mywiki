---
tags: [tools, designer-workflow, hot-reload, tuning]
date: 2026-04-19
sources: 1
---

# 运行时重载游戏数值（F5 + 结构体指针）

Joost van Dongen 在 Ronimo 的多个项目里反复用一套极简的「数值热重载」：一个纯文本文件装所有设计师可调的数值（Swords & Soldiers 里约 600 个），游戏里把所有读取点都指到同一个 `struct`，开发版本在游戏运行中按 F5 就地重新解析文本并覆盖 struct 字段；所有 gameplay 代码因为拿的是指针/引用而不是拷贝，下一帧就立即用上新值。设计师 alt+tab 出去改数、切回按 F5，不用重启游戏。

关键纪律是**永远不要把 struct 里的值拷贝到局部变量或对象字段里存起来**——一旦复制，热重载就对那份拷贝失效，这是最容易出错的地方。

与此对比，早年 De Blob 试过做游戏内滑条调节 UI，但当可调项扩展到几百个，做滑条比用 Notepad 还费劲，ROI 不划算，最后回归纯文本。评论区指出 Unity 已经用 C# 反射把任意 `public` 字段自动暴露成编辑器参数，效果上是同一思路的引擎级自动化；HLSL 的 UI annotation（min/max/group）也能把 min-max 范围和树形分组写进数据本身。Proun 里 Joost 没要 F5，但做了「每条赛道独立覆盖全体设定」的分层——同一套机制稍加变形就变成关卡特化参数。

结论：把 gameplay 常量集中到一个文件、加载一次就能热替换——这是 Joost 眼里**任何学生作品都应该第一版就做**的工具，成本极低，对设计迭代速度提升巨大。

## 相关
- [[binary-hot-reload]] —— C++ 代码/so 级别的热重载
- [[tools-first-iteration-loop]] —— 工具优先的迭代观
- [[runtime-editor-console-connection]] —— 编辑器与运行时之间的另一种连接形态

## Sources
- [[sources/joostdevblog-all-the-settings]]
