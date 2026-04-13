---
title: Comment on Button – Button 系列功能講解
url: https://tedsieblog.wordpress.com/2016/07/10/ngui-tutorial-comment-on-button/
author: Ted Sie
published: '2016-07-10'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

這篇要來介紹一下 NGUI 中的 Button 系列腳本

點選 Component → NGUI → Interaction

可以看到有一長串的 NGUI 腳本


在使用 Button 腳本前，須先加入 Collider 至物件上，才可以使用

**Button：基本按鈕動作**


Tween Target： 作用物件

Transition： 狀態轉換時間

Colors： 各種按鈕狀態下的按鈕對應顏色

Normal： 正常顯示

Hover： 滑鼠停留

Pressed： 滑鼠按下

Disabled： 未啟用

Sprites： 各種按鈕狀態下的按鈕對應圖片

Pixel Snap： 切換對應圖片後，Widget 中的 Size 是否重置

On Click： 當按下後要觸發的其他物件腳本

**Button Activate：物件開關**


Target： 作用物件

State： 按下後的物件狀態 ( 勾選為開啟物件、不勾選為關閉物件 )

**Button Color：功能同 Button ，但只有切換按鈕顏色功能**


若按下 Upgrade to a Button ，UIButton Color 自動切換為 UIButton

**Button Keys (Legacy)：舊版 NGUI 功能，不建議使用**

**Button Message (Legacy)：舊版 NGUI 功能，不建議使用**

**Button Offset：按鈕偏移**


Tween Target： 作用物件

Hover： 滑鼠停留時的偏移座標 ( Position )

Pressed： 滑鼠按下時的偏移座標 ( Position )

Duration： 轉換時間

**Button Rotation：按鈕旋轉，同 Button Offset，座標影響變為 Rotation**


**Button Scale：按鈕縮放，同 Button Offset，座標影響變為 Scale**