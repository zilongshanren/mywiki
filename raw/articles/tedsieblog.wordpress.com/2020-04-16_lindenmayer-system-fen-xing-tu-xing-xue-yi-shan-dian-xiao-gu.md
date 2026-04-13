---
title: Lindenmayer System 分形圖形學 – 以閃電效果為例
url: https://tedsieblog.wordpress.com/2020/04/16/lindenmayer-system-a-case-study-of-lightning-bolts/
author: Ted Sie
published: '2020-04-16'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

在上一篇文章 [Lindenmayer System 分形圖形學] 中，描述了 Lindenmayer System 分行圖形學的主要概念，此篇文章會在分形圖形學的基礎上加入更多規則，包含**利用中點偏移規則來模擬閃電之字形的部分、利用隨機分支規則來模擬閃電分支的部分、迭代過程優化分支產生規則**，創造出分形閃電效果。

##### 分形閃電效果概念

**1. 中點偏移規則**

每次的迭代過程中，會在線段適合的位置加入一垂直於線段的偏移向量，形成閃電效果的之字形部分。

![](../../assets/ea49dbdc385e8146.png)


![](../../assets/49951f39fd334fe0.png)


![](../../assets/a3af46793b026ff3.png)


![](../../assets/1e1ca45ba949c983.png)


![](../../assets/65968801c6753414.png)


**2. 隨機分支規則**

在每次中點位移規則後，會在新中點位置加入一隨機線段，形成閃電效果的分支部分。

![](../../assets/9e00aaf1bfe34d11.png)


![](../../assets/f9938d6b69bd09b4.png)


![](../../assets/d3b7efed6ae70d24.png)


![](../../assets/a5b4dcecd90a5601.png)


![](../../assets/ad3a8a4b975f6b15.png)


**3. 分支規則優化**

觀察 **2. 隨機分支規則** 步驟可以察覺，若在每一次的迭代過程都產生分支，分支數量會過於發散導致最終的結果變的不可接受。所以在 **2. 隨機分支規則** 上需要加入一些優化調整來改善這個問題。

**a. 機率性產生分支
b. 分支角度的調整
c. 限制每次迭代過程中的分支數量
d. 限制總體的分支數量**

![](../../assets/22cc7a247fac47ea.png)


![](../../assets/6f4df35ae7d37175.png)


![](../../assets/6cacf4c3a9e5d730.png)


![](../../assets/42fb587003d0ee16.png)


![](../../assets/24d3a0455ff82e84.png)


**4. 網格生成**

到目前為止都還在生成線段的步驟，只有線段沒辦法運用在遊戲之中，這邊簡單的取得每個線段的中心點及長度並利用 [GameObject.CreatePrimitive](https://docs.unity3d.com/ScriptReference/GameObject.CreatePrimitive.html) 生成 Quad 網格，最後搭配 GPU Instancing 改善網格過多造成的問題。

![](../../assets/5762ca168271b2b6.jpg)


**5. 網格間隔優化**

觀察 **4. 網格生成** 步驟可以發現，產生出的網格會在交界處出現細小間隔，導致閃電整體出現斷斷續續的情況，可以在線段交界處額外生成網格來改善這個問題。

![](../../assets/01c0926c2172e559.jpg)


![](../../assets/6dbbd7bee6efa92d.jpg)


**6. 閃電效果優化**

目前已完成閃電效果的雛形，不過由於產生的網格大小、顏色太過一致，導致效果整體過於單調且乏味，需要在額外進行一些優化調整。

**a. 網格大小優化**

網格大小優化的主要思路是在迭代過程中紀錄線段間的關係，從而區分出主幹、分支兩部分，並紀錄線段位於分支層級。

**主幹部分**使用線段與閃電終點的距離作為網格大小調整依據，**分支部分**使用分支層級作為網格大小調整依據，最後建立一個 [Animation Curve](https://docs.unity3d.com/ScriptReference/AnimationCurve.html) 來取得對應的網格大小。

**b. 網格顏色優化**

同 **a. 大小優化** 步驟，最後建立一個 [Gradient](https://docs.unity3d.com/ScriptReference/Gradient.html) 來取得對應的網格顏色。

![](../../assets/a043da54563ac808.jpg)


![](../../assets/6259bccd910a724f.jpg)


**8. 最終成果**

![](../../assets/83c8b12f6e3582ff.jpg)


![](../../assets/c58ad8e81993d9be.jpg)


![](../../assets/a1852506976ca11e.jpg)


![](../../assets/e7cf671b657b1064.jpg)


![](../../assets/32f445809c997b73.gif)


##### Patreon

##### 完整原始碼

##### 參考資料

[Drilian’s House of Game Development – Lightning Bolts](http://drilian.com/2009/02/25/lightning-bolts/)

[游戏中雨天效果开发：如何打造“最美下雨天”](https://zhuanlan.zhihu.com/p/111904859)

[移动端天气系统–【下雨】效果之【雷电】的实现和分析](https://zhuanlan.zhihu.com/p/103124702)