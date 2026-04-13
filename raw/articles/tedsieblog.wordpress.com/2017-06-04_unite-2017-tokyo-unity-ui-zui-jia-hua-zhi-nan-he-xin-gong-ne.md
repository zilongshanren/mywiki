---
title: 【Unite 2017 Tokyo】Unity UI 最佳化指南和新功能介紹
url: https://tedsieblog.wordpress.com/2017/06/04/unite-2017-tokyo-unity-ui-optimize-guide-and-new-feature/
author: Ted Sie
published: '2017-06-04'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

#### Unity UI 三大分類

1. Visual

Text, Image, RawImage

2. Interactive

Button, Toggle, Slider, etc.

3. Layout

Vertical Group, Content Size Filter, Layout Element, etc.



#### UI 最佳化

UI 最佳化會依賴於每個案例而有所不同

1. 平台（Mobile, Console, VR）

2. UI 類型（2D, 3D, 混合）

3. 遊戲類型（競速、射擊…等）

不同案例有不同的優化方向

並不是所有的優化建議都適用於所有案例


#### UI Batching

批次處理規則

1. 使用相同的 Canvas

2. 使用相同的 Material

3. 使用相同的 Sprite

4. 使用相同的 Mask

5. 擁有相同的 RectTransform Position Z


#### UI Shaders

UI 元件的預設 Shader 為 UI/Default

Build-In Unity Shader Source Code 可以在下列連結下載

[https://unity3d.com/get-unity/download/archive](https://unity3d.com/get-unity/download/archive)


#### TextMesh Pro

TextMesh Pro 最初是由 Stephan Bouchard 開發

並上架到 Asset Store 的一套 UI 插件

前些日子 Unity 宣布 Stephan Bouchard 與 TextMesh Pro 加入的消息

所以 TextMesh Pro 目前是以免費的形式提供給 Unity 開發者使用

[TextMesh Pro Joins Unity](https://blogs.unity3d.com/2017/03/20/textmesh-pro-joins-unity/)


#### The Rebuild Process

Set ‘Dirty’

1. UI Element Layout changes

2. UI Element Graphic changes

只要 UI 元件被設為 Dirty

就會重新計算該 Components 或物件

Unity Profiler Canvas.SendWillRenderCanvases 用來觀察這個進程


#### Unity UI – Source Code

Layout 使用建議

1. 需要更新 UI 佈局時在開啟，不需要時則關閉

2. 減少需要更新的 UI 元件（組合 UI 元件）

3. 建立自己的 Layout Manager 用來管理 Layout 何時更新

4. 用物件池進行管理使 UI 元件能夠重複使用


#### Sub Canvases

當一個 Canvas 為另一個 Canvas 的子物件則為 Sub-Canvas

Sub-Canvas 特性

1. 擁有獨立的環境設定（例如：Pixel Perfect）

2. 需要時可以針對 Sub-Canvas 進行批次處理

3. 能夠獨立 Canvas 所管理的 UI 元件，針對 Canvas 下的子元件進行開關


#### 資料來源

[Unity UI最適化ガイド 〜ベストプラクティスと新機能 – SlideShare](https://www.slideshare.net/UnityTechnologiesJapan/unite-2017-tokyounity-ui)

[Unity UI最適化ガイド 〜ベストプラクティスと新機能 – YouTube](https://www.youtube.com/watch?v=13Qwh2UkFmU&feature=youtu.be)

[Other UI Optimization Techniques and Tips](https://unity3d.com/learn/tutorials/topics/best-practices/other-ui-optimization-techniques-and-tips)

[Unity Best Practices – Optimizing Unity UI](https://unity3d.com/learn/tutorials/topics/best-practices)

感謝分享!

LikeLike