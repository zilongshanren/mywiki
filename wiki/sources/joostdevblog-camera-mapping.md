---
tags: [source, rendering, 2d-to-3d, stylized, camera-mapping]
date: 2026-04-19
sources: 3
---

# Camera Mapping 三连载（Joost van Dongen / Joost's Dev Blog，2010-10）

[[joost-van-dongen]] 2010 年 10 月连续三篇博客，记录他把 2D 插画「投影」到粗 3D 几何上做出可动画的「活画」的实验与经验。

## 摘要

第一篇 *Camera mapping the Evil Pope*（10-03）用 Marlies Barends 的 *Evil Pope* 做案例，展示即便是脸部表情动画也能用 camera mapping 做到。第二篇 *Captain August got camera mapped*（10-10）挑战更硬的题材：Roderick Leeuwenhart 的 webcomic *Captain August*，画面带破碎透视（顶部圆顶不在单一灭点上）和整组物体共用一根粗白描边——camera mapping 都能保留。Joost 的目标是呼应 *Anno 1404* 故事画那种「给静帧插画呼吸感」的效果。第三篇 *Camera mapping tips and tricks*（10-16）总结了五条可操作经验：用 3ds Max 的 Camera map modifier、不用多边形还原物体边缘（交给贴图 alpha）、把原图拆成尽量多的图层（Evil Pope 3 层、August 28 层）、给模型加轻微曲面避免「纸板人」、投影完成后再绑骨骼 / morph 做动画。他最后表示有意把这套方法用到实时 3D 游戏原型里。

## 关键要点

- 传统 camera mapping 多用于环境，Joost 的新意是用它做**角色**。
- 轮廓**必须**来自贴图 alpha，不能靠多边形边缘——polygon 做不出笔触的模糊与锯齿。
- 图层数量 ≈ 建模难度的倒数。layer 越多、手绘补全的被遮部分越多，3D 场景越好搭。
- 加轻微曲面打破「纸板人」效应，但别过度弯曲，否则侧视时笔触被压缩。
- Camera map 完之后骨骼、morph、换小块贴图都自由，不破坏 2D 错觉。
- 这是一种用原画像素直接承担材质的美术工艺折中，代价是摄像机被原画视角锁住。

## 链接到的概念

- [[camera-mapping-2d-to-3d]]
- [[joost-van-dongen]]

## 原文

- 链接：
  - http://joostdevblog.blogspot.com/2010/10/camera-mapping-evil-pope.html
  - http://joostdevblog.blogspot.com/2010/10/captain-august-got-camera-mapped.html
  - http://joostdevblog.blogspot.com/2010/10/camera-mapping-tips-and-tricks.html
- 本地：
  - `raw/articles/joostdevblog.blogspot.com/2010-10-03_camera-mapping-the-evil-pope.md`
  - `raw/articles/joostdevblog.blogspot.com/2010-10-10_captain-august-got-camera-mapped.md`
  - `raw/articles/joostdevblog.blogspot.com/2010-10-16_camera-mapping-tips-and-tricks.md`
