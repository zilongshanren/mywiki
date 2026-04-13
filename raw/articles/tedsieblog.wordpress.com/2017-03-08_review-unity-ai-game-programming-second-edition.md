---
title: 【Review】Unity AI Game Programming – Second Edition
url: https://tedsieblog.wordpress.com/2017/03/08/review-unity-ai-game-programming-second-edition/
author: Ted Sie
published: '2017-03-08'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

在前一陣子的 [FREE LEARNING – FREE TECHNOLOGY EBOOKS](https://www.packtpub.com/packt/offers/free-learning) 活動中，免費取得了這本 [Unity AI Game Programming – Second Edition](https://www.packtpub.com/game-development/unity-ai-game-programming-second-edition)，於是花費了約四天將這本書給吸收完畢，透過這次的文章，紀錄自己對於這本書的理解、分析及評論。


![](https://dz13w8afd47il.cloudfront.net/sites/default/files/imagecache/ppv4_main_book_cover/9781785288272.png)



#### Chapter1 – The Basics of AI in Games

這個章節簡單介紹了 AI 在遊戲中的定位為何，從有限狀態機、感測器、路徑移動、尋路演算、Navigation、群聚效應、行為樹到最後的模糊邏輯都初步介紹了一遍。


#### Chapter2 – Finite State Machines and You

書中這邊所指的 Finite State Machine 是 Unity 所內建的 [Mecanim Animation System](https://docs.unity3d.com/462/Documentation/Manual/MecanimAnimationSystem.html)，藉由 Mecanim 系統去設定 Parameters、States、Transition…等，再配合繼承了 [StateMachineBehaviour](https://docs.unity3d.com/ScriptReference/StateMachineBehaviour.html) 的腳本就可以詳細編輯每一個狀態的細節變化以及傳遞條件。

與一般提到的有限狀態機 [Finite State Machine](https://en.wikipedia.org/wiki/Finite-state_machine) 差異是，Mecanim 系統不只包含了狀態機的邏輯處理部分還附帶處理了 Unity 動畫部分，並結合可視化編輯呈現出狀態轉移的條件及狀態圖，讓非程式人員也能夠享受到編輯狀態機的過程。

![](../../assets/6ab978f43fb11195.png)



#### Chapter3 – Implementing Sensors

感測器在人工智慧中是應用範圍相當廣泛的一個項目，一般提到的感知都會第一時間聯想到人的五官，其中包含了聽覺、視覺、觸覺、嗅覺、味覺，這些感覺都可以經過感測器實作來加以實現，像是視覺感測可以透過基本的視線範圍去進行射線偵測。但是這個章節中卻只實作了透過碰撞器去偵測物體是否在感測器中 [OnTriggerEnter](https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnTriggerEnter.html) 的應用，並沒有針對某種感覺來做相對應感測器的實作，這部分算是相對可惜。


#### Chapter4 – Finding Your Way

這本書中篇幅最大的一個章節，主要在圍繞在路徑跟隨、簡易障礙物避免、尋路演算以及 Unity [Navigation](https://docs.unity3d.com/Manual/Navigation.html) 的實作。

值得一提的是障礙物避免的處理方式，書中先透過射線來判斷移動物體是否會碰撞障礙物，如果碰撞成立就會在移動物體上附加一個額外的移動向量使移動物體產生移動偏移，透過這個方式就可以很簡單的使移動物體繞過障礙物，但是會在某些狀況下產生 Bug ，而書中也沒有提到這一部份。

尋路演算部分，完整的介紹了 A* 演算法的原理、實作過程以及最後實作成果，另外也可以搭配我自己撰寫的 [A* 演算法系列文](https://tedsieblog.wordpress.com/2016/07/08/a-star-algorithm-introduction/)一起服用，可以更加理解 A* 尋路演算法的完整理論。

[Navigation](https://docs.unity3d.com/Manual/Navigation.html) 則是 Unity 所提供的尋路功能，在這個段落中完整介紹了 Navigation 的設定方式，包含了 Baking、NavMeshAgent 以及 Mesh Links。

![](https://docs.unity3d.com/uploads/Main/NavMeshCover.png)



#### Chapter5 – Flocks and Crowds

說明了[群聚效應](https://en.wikipedia.org/wiki/Flocking_(behavior))的三個核心概念，分離、對齊以及凝聚。

分離：透過與其他物件保持一定距離，來避免物件群之間的碰撞。

對齊：與其他物件保持相同的移動方向及速度。

凝聚：與物件群中心保持一定距離。

透過這三個核心概念，就能夠模擬出群體移動的行為，也可以常常在 RTS 類遊戲中看到這個效果的運用，像是紅色警戒、世紀帝國、星海爭霸…等

經典作品。

![](https://i0.wp.com/i.gbc.tw/gb_img/9/002/625/2625149.jpg)


![](https://cdn1-techbang.pixcdn.tw/system/images/298345/original/88dd6cb0750b5d26c3b2127619cbb407.jpg?1443243433)



#### Chapter6 – Behaviour Trees

這個章節說明並實作了行為樹 [Behaviour Tree](https://en.wikipedia.org/wiki/Behavior_tree)

的運作方式，而行為樹的核心概念為節點（Node），搭配節點狀態以及執行條件，就可以透過不同的行為樹狀分支邏輯組合出自己想要的 AI 心智圖。

一般情況下，會將節點狀態分為：成功（Success）、失敗（Failure）及執行中（Running），而節點執行條件則分為：序列（Sequence）及選擇（Selector）。

序列：只要有一子節點狀態失敗，則節點狀態失敗。

選擇：只要有一子節點狀態成功，則節點狀態成功。

而在接觸遊戲人工智慧 AI 時，最常聽到的三個名詞包含了，有限狀態機（FSM）、分層有限狀態機（HFSM） 以及行為樹（Behaviour Tree），這三種名詞都是用來處理遊戲 AI 的運作邏輯。但書中並沒有介紹到分層狀態機，所以這邊先跳過分層狀態機，將有限狀態機與行為樹做一個簡單的比較。

有限狀態機，由複數狀態所組合成的運作機制，透過事件觸發來引起狀態之間的切換，是一種事件觸發型 AI。

行為樹，由樹狀圖的根做為起點，由各個節點中的節點狀態以及節點執行條件來進行邏輯檢測，判斷是否要往分支繼續執行，是一種輪詢型 AI。


#### Chapter7 – Using Fuzzy Logic to Make Your AI Seem Alive

模糊邏輯 [Fuzzy Logic](https://en.wikipedia.org/wiki/Fuzzy_logic)，一般我們在處理邏輯問題時，往往是非零即一，在這種狀況之下會導致 AI 的行為相當容易被玩家看穿，這時候就可以運用模糊邏輯，透過模糊邏輯的應用，就可以打造出更活靈活現的 NPC 及怪物。而書中靈活的運用了一個名為 Bob 的巫師角色來說明模糊邏輯的實際運用情況，藉由模糊邏輯來判斷巫師目前的生命值情況，但這個章節也只是簡單的介紹了模糊邏輯的概念以及基本的實作，並沒有針對這個議題做更深入的研究。

![](../../assets/d10b1a897be78287.png)



#### Chapter8 – How It All Comes Together

最後的章節結合了前面所學的東西，做出了一個可玩遊戲，算是將書中所提到一部分要素做了結合，這部分需要特別研究的議題，就是一個很簡單的概念應用後衍生出的小遊戲。


#### 結語

整體來說，這本 Unity AI Game Programming 算是一本中規中矩的 Unity 相關書籍，透過循序漸進的介紹及實作，讓讀者可以獲取關於人工智慧的相關知識，不過卻往往在一些關鍵的部分點到為止，沒有做更進一步的議題探討、說明及應用，這部分的表現就沒這麼理想。

對於想要專研人工智慧的開發者來說，這本書可以歸類成有空閒時間在快速閱讀的書，但是對於在 Unity 上已經有一定的使用經驗且對 AI 人工智慧有興趣想要嘗試入門的開發者，還是推薦抽空閱讀，可以一次性的獲得人工智慧開發上所需要累積的知識。

## One thought on “【Review】Unity AI Game Programming – Second Edition”