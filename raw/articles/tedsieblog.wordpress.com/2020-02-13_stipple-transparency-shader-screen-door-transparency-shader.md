---
title: Stipple Transparency Shader (Screen-Door Transparency Shader)
url: https://tedsieblog.wordpress.com/2020/02/13/stipple-transparency-shader-screen-door-transparency-shader/
author: Ted Sie
published: '2020-02-13'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

##### 什麼是 Stipple Transparency?

Stipple Transparency 是一種基於螢幕空間的物件渲染方式，透過轉換螢幕空間位置至像素位置計算出閥值，剔除不必要的像素。

隨著物件透明度的上升，逐漸地增加剃除像素的數量。

![](../../assets/a7cd959d63fa1c24.gif)


##### 為什麼需要 Stipple Transparency?

Unity 中預設的透明物件渲染方式是基於 Alpha Blending，由文章 [Unity Game View Overdraw – 在遊戲視窗上顯示 Overdraw](https://tedsieblog.wordpress.com/2020/01/30/unity-game-view-overdraw/) 可得知，當 Render Queue 為 Transparency 時由於物件採取由後到前的方式繪製，所以會有 Overdraw 的情況發生。

且當複數個物件重疊時，會出現本該是一體的物件出現渲染排序的問題，導致透明渲染呈現詭異的結果。

![](../../assets/6539f4e5752e2e74.jpg)


Stipple Transparency 渲染方式則是基於 Alpha Testing，能夠避免 Overdraw、改善渲染排序、提高物件整體性。

##### Stipple Transparency 核心算法

1. 計算螢幕空間位置

o.vertex = UnityObjectToClipPos(v.vertex); o.screenPos = ComputeScreenPos(o.vertex);

2. 定義閥值矩陣

const float4x4 thresholdMatrix = { 1, 9, 3, 11, 13, 5, 15, 7, 4, 12, 2, 10, 16, 8, 14, 6 };

3. 計算對應像素位置

float2 pixelPos = i.screenPos.xy / i.screenPos.w * _ScreenParams.xy;

4. 取得對應閥值

float threshold = thresholdMatrix[pixelPos.x % 4][pixelPos.y % 4] / 17;

5. 剔除像素

clip(_Alpha - threshold);

##### 最終成果

![](../../assets/3d1e598d4a6c8e7a.jpg)


![](../../assets/55a255ae8eec4d83.jpg)


##### 參考資料

[Coding Adventure: Game Idea Generator](https://www.youtube.com/watch?v=--GB9qyZJqg#t=5m25s)

[Unity Stipple Transparency Shader](https://ocias.com/blog/unity-stipple-transparency-shader/)

[Screen-Door Transparency](https://digitalrune.github.io/DigitalRune-Documentation/html/fa431d48-b457-4c70-a590-d44b0840ab1e.htm)