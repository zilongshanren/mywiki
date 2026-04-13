---
title: Comment on UIAtlas – NGUI 圖集新增、更新、導出、移除
url: https://tedsieblog.wordpress.com/2016/07/10/ngui-tutorial-comment-on-uiatlas/
author: Ted Sie
published: '2016-07-10'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

在上一篇中我們新增了一個圖集

這裡來講解如何對圖集做新增、移除、導出


**圖集新增**

圖集新增的流程和製作圖集的流程大致上一樣

開啟Atlas Maker後將想要新增的圖集拖拉至UI Atlas選項中


選擇想要新增的圖片


按下 Add/Update 後即可新增圖片至圖集中


**圖集更新**

圖集更新的方法跟新增一樣

差別是在選擇圖片後圖集更新的字樣從Add → Update

按下Add/Update後即可更新圖片至圖集中


**圖集導出**

有時候在圖集打包好後

會把多餘的零碎圖片從專案中移除

但如果後來又希望找到同一張圖片來做調整時就會顯得不方便

所以NGUI支援了圖片導出的功能

可以直接從圖集中將選定的圖片導出

選擇想要導出的圖集

接著在Inspector面板中可以看到UIAtlasComponent


選擇想要導出的圖片後按下Save As

就可以將圖片重新導出


**圖集移除**

開啟Atlas Maker面板

將圖集拖拉至UI Atlas選項中

按下想要移除的圖片旁的X按鈕後

點選Delete即可移除