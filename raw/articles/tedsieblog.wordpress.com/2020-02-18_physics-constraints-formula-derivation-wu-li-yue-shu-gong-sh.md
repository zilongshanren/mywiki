---
title: Physics Constraints Formula Derivation – 物理約束公式推導
url: https://tedsieblog.wordpress.com/2020/02/18/physics-constraints-formula-derivation/
author: Ted Sie
published: '2020-02-18'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

衝量


作用力


質量、轉動慣量


約束條件



衝量是作用在物體上的力在時間上的累積


牛頓第二運動定律


經由牛頓第二運動定律可以得知 P 與 F 的關係，進而求出速度變化量


由於約束衝量 or 作用力並不會對整個系統做功

所以可以得知


將約束條件微分並通則化


雅可比矩陣，列矩陣


物體速度、角速度


由做功與約束條件可得知衝量與雅可比矩陣之間的關係


在約束條件中加入偏重


計算速度變化量後重新導入約束條件

即可求得 值



將新速度套入 JV 公式即可求得


定義 有效質量 Effective Mass



最終可以求得 拉格朗日乘數 Lagrange Multiplier



每幀的速度、角速度變化量即為


參考資料

[TheAllenChou/unity-physics-constraints](https://github.com/TheAllenChou/unity-physics-constraints)

[Game Physics – Equality Constraints & Solver](http://myselph.de/gamePhysics/equalityConstraints.html)