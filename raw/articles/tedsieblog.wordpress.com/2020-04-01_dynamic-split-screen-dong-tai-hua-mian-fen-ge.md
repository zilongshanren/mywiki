---
title: Dynamic Split Screen – 動態畫面分割
url: https://tedsieblog.wordpress.com/2020/04/01/dynamic-split-screen/
author: Ted Sie
published: '2020-04-01'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

##### 前言

在許多遊戲中，隨著遊玩的人數不同，會根據遊戲特性在畫面中加入一些巧思提高玩家的遊玩體驗。

較常見的做法像是**動態調整攝影機位置及範圍**、**角色超出螢幕範圍時加入提示**、**畫面水平分割**、及**畫面垂直分割**…等。

![](../../assets/d37dfb81b55f6b4f.jpg)


[圖片來源](https://www.youtube.com/watch?v=yUhw1VvaFec)

![](../../assets/e5ec1aae5353520f.jpg)


[圖片來源](https://store.steampowered.com/app/386940/Ultimate_Chicken_Horse/?l=schinese)

![](../../assets/0b27d5097d37aed3.img)


[圖片來源](https://cdn.hk01.com/di/media/images/2177856/org/1c35d8360e3b9ce51800b17c69b55293.jpg/bqHCr7b3_9Mzqto2hqPuFuVlZ7cvDWjEgf3ecoH93nI?v=w1920)

![](../../assets/f04d21f8697eece8.jpg)


[圖片來源](https://www.youtube.com/watch?v=qz6XEhHlyuA)

##### 動態畫面分割

一般來說，遊戲如果使用畫面分割的方式來切割畫面，絕大多數都是使用水平分割或垂直分割，玩家在遊玩時可以很清楚的知道自己在畫面中的位置，但對於其他玩家位置及整個場景相對位置的掌握度卻沒有這麼好。

動態畫面分割則是根據角色在場景中的位置來動態分割畫面，讓玩家能夠 **清楚的知道其他玩家位於哪個方位** 及 **了解整個場景的相對關係**。

##### 畫面分割概念流程

![](../../assets/dbcccb373abd95fa.jpg)


![](../../assets/546cba00f0b14116.jpg)


![](../../assets/8230f3ccc2a40889.jpg)


![](../../assets/a17ae6a5b5cabc79.jpg)


![](../../assets/7ed98bf74d190715.jpg)


##### 畫面分割過渡優化

由上述流程建立出來畫面分割功能會在功能開啟時產生頓感，是因為攝影機偏差與中間點在功能切換的瞬間距離過遠，導致在功能切換時，攝影機會在一瞬間在中心點及偏差點之間移動。解決方法相當簡單，只需要在偏差值部分加入根據距離變化的功能即可。

![](../../assets/423ed235e98adb82.gif)


![](../../assets/71c62d58347f16ae.gif)


##### 最終成果

![](../../assets/1f92dd4f3fc6bc86.gif)


##### Patreon

##### 完整原始碼

##### 參考資料

[Math for Game Programmers: Juicing Your Cameras With Math](https://www.youtube.com/watch?v=tu-Qe66AvtY&feature=youtu.be&t=1745)

[Voronoi Split Screen: A Quick Tour by MattWoelk](https://mattwoelk.github.io/voronoi_split_screen_notes/)