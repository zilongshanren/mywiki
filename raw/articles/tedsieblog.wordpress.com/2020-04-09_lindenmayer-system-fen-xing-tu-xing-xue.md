---
title: Lindenmayer System 分形圖形學
url: https://tedsieblog.wordpress.com/2020/04/09/lindenmayer-system/
author: Ted Sie
published: '2020-04-09'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

Lindenmayer System 簡稱為 L 系統是一種分形圖形學，根據給定的規則進行迭代過程，最終生成擁有特殊結構的圖形，被廣泛的應用在植物生長過程的研究上。

##### 系統結構

L 系統的主要的結構包含**變數**、**常數**、**旋轉角度**、**初始狀態**、**迭代規則**

**變數：**每次疊代過程中，根據迭代規則而改變的參數

**常數：**每次疊代過程中，不會改變的參數

**旋轉角度：**當方向旋轉時所旋轉的角度值

**初始狀態：**疊代次數為零時的初始輸出

**迭代規則：**每次疊代過程中，變數替換的規則

##### 參數定義

A：沿著方向畫一線段

B：沿著方向畫一線段

X：純標記

Y：純標記

[：紀錄當前位置、方向

]：取出上一位置、方向

+：方向順時針旋轉

-：方向逆時針旋轉

##### Algae

變數：A、B

初始狀態：A

迭代規則：

A -> AB

B -> A

![](../../assets/6a1620869f2d10d3.png)


##### Fractal Tree

變數：A、B

常數：[、]、+、-

旋轉角度：45

初始狀態：B

迭代規則：

A -> A[-B]+B

B -> AA

![](../../assets/9fb98574f32c28e8.gif)


##### Cantor Set

變數：A、X

初始狀態：A

迭代規則：

A -> AXA

X -> XXX

![](../../assets/161b64ca16833183.gif)


##### Koch Curve

變數：A

常數：+、-

旋轉角度：90

初始狀態：A

迭代規則：

A -> A-A+A+A-A

![](../../assets/395d36ca9b81cc88.gif)


##### Koch Snowflake

變數：A

常數：+、-

旋轉角度：60

初始狀態：A++A++A

迭代規則：

A -> A-A++A-A

![](../../assets/2491af221495c28f.gif)


##### Sierpinski Triangle

變數：A、B

常數：+、-

旋轉角度：120

初始狀態：A-B-B

迭代規則：

A -> A-B+A+B-A

B -> BB

![](../../assets/896015a16cf1ea6f.gif)


##### Sierpinski Curve

變數：X

常數：A、B、+、-

旋轉角度：45

初始狀態：A–XA–A–XA

迭代規則：

X -> XA+B+XA–A–XA+B+X

![](../../assets/9e5609ed28c7f29d.gif)


##### Sierpinski Square Curve

變數：X

常數：A、+、-

初始狀態：A-XA-A-XA

旋轉角度：90

迭代規則：

X -> XA+A-A+XA-A-XA+A-A+X

![](../../assets/1891e76e56362203.gif)


##### Sierpinski Arrowhead Curve

變數：A、B

常數：+、-

旋轉角度：60

初始狀態：A

迭代規則：

A -> B+A+B

B -> A-B-A

![](../../assets/0348b9bb24871c48.gif)


##### Dragon Curve

變量：X、Y

常數：A、+、-

初始狀態：AX

旋轉角度：90

迭代規則：

X -> X-YA-

Y -> +AX+Y

![](../../assets/c5105dddf2dd31d1.gif)


##### Fractal Plant

變量：X、A

常數：[、]、+、-

旋轉角度：25

初始狀態：X

迭代規則：

X -> A-[[X]+X]+A[+AX]-X

A -> AA

![](../../assets/4b8bc643ca29fa68.gif)


![](../../assets/e83956a615192a87.gif)


##### Patreon

##### 範例原始碼

##### 參考資料

[L-system – Wikipedia](https://en.wikipedia.org/wiki/L-system)

[Koch snowflake – Wikipedia](https://en.wikipedia.org/wiki/Koch_snowflake)

[Sierpiński curve – Wikipedia](https://en.wikipedia.org/wiki/Sierpi%C5%84ski_curve#Arrowhead_curve)