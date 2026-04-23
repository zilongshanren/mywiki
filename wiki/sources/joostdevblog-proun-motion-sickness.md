---
tags: [source, game-feel, camera, motion-sickness, proun]
date: 2026-04-19
sources: 1
---

# Designing against motion sickness in Proun（Joost van Dongen / Joost's Dev Blog，2010-10-30）

[[joost-van-dongen]] 在 Proun trailer 上 Kotaku / Gametrailers 之后，面对观众「看着都要吐」的担忧，撰文讲了他为这种 360° 滚转赛车游戏做的抗晕眩摄像机设计。

## 摘要

核心观察：**看别人玩（尤其视频剪辑）远比亲手玩更容易晕**，因为摄像机旋转对玩家自己是由输入主动触发的、前庭有预期，对观众则完全是被动冲击。从这个前提出发，Joost 做了三条反常规决策：（1）**不做任何 camera smoothing**。他在 Ronimo 被砍的 3D 项目里实验过各种 smoothing 方案，发现即便极轻的延迟也让摄像机与输入不同步、视觉-前庭冲突加剧；极端 smoothing 甚至秒晕。Proun 宁可镜头稍硬也绝不加平滑。（2）**飞船始终钉在屏幕正中**，不缩放不环绕——Proun 没有上下也没有地平线，唯一能作为「稳定锚点」的就是玩家载具本身。（3）**摄像机只在玩家输入时旋转**，避免非自愿旋转。实测绝大多数 playtest 玩家能像玩普通 3D 游戏一样玩完 Proun。他列出的摄像机经验来自之前 De Blob、Swords & Soldiers、Ronimo 秘密新作和一个被砍的 3D 项目。

## 关键要点

- 视频 trailer 引发的晕眩担忧常常夸大了实际玩家体验；宣传策略应多推 demo 少推视频。
- 「主动输入触发的摄像机旋转」几乎不会晕，「非自愿的摄像机旋转」是主凶。
- Camera smoothing 在常规第三人称里是美化手段，在无地平线场景里是致晕源。
- 在无上下/无地平线的游戏里，玩家载具必须充当视觉锚点，所以不能绕飞也不能推拉。
- Joost 的判断源自多个项目的摄像机系统经验积累，而非纯 VR 社区内的结论（2010 年 VR 还远未兴起）。

## 链接到的概念

- [[motion-sickness-camera-design]]
- [[joost-van-dongen]]

## 原文

- 链接：http://joostdevblog.blogspot.com/2010/10/designing-against-motion-sickness-in.html
- 本地：`raw/articles/joostdevblog.blogspot.com/2010-10-30_designing-against-motion-sickness-in-proun.md`
