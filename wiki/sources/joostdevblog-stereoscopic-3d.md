---
tags: [source, rendering, stereoscopic, gui, indie]
date: 2026-04-19
sources: 1
---

# Stereoscopic 3D（Joost van Dongen / Joost's Dev Blog）

[[joost-van-dongen]] 2010 年 11 月发表的文章，借 *Proun* 和 *Swords & Soldiers* 上线 3D 电视的机会讨论**立体 3D 对游戏内容设计的影响**——刻意跳过立体摄像机的数学。

## 摘要

立体 3D 不是一个「渲染开关」，它倒逼一串设计决策：**把显示器当成窗口**——物体可以穿出来，但穿出来的物体不能被屏幕边缘裁切（窗口违例），这条规则直接禁止 FPS 枪贴脸；**眼距是可调参数**，大眼距 = 更震撼但会让敏感玩家头痛；**GUI 分层**要和场景深度对齐——*Swords & Soldiers* 血条贴在士兵深度、地图因为被前景挡只能放到最前面；**屏幕空间 trick 集体失效**——全屏雨 texture 立体下看起来就是贴在眼前的湿玻璃，必须换成真 3D 粒子。意外红利：*Swords & Soldiers* 的 2D 角色在 3D 空间里像纸片剧场，刚好契合它的卡通风。这些约束几年后在 VR 里几乎 1:1 重演。

## 关键要点

- 窗口违例（window violation）：穿出屏幕的物体不能被屏幕边遮挡 → FPS 的枪不能贴近相机
- 眼距（interpupillary distance）是设计变量，不是物理量；过大 = 震撼但头痛
- GUI 深度必须贴合所指向的 gameplay 对象，否则眼球重新聚焦太累
- 屏幕空间 fake（雨、贴图特效）在立体下立刻穿帮
- 2D 角色 + 3D 立体 = cardboard cutout 美学（幸运契合卡通风格）
- 2010 年针对 3DTV 的经验，几乎全部可迁移到现代 VR

## 链接到的概念

- [[stereoscopic-3d-design]]
- [[motion-sickness-camera-design]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/11/stereoscopic-3d.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-11-06_stereoscopic-3d.md`
