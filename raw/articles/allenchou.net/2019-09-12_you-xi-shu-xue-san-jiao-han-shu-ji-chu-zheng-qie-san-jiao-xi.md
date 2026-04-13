---
title: 遊戲數學：三角函數基礎 – 正切、三角形、與砲彈 | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2019/09/tangent-triangles-cannonballs-chinese/
author: Allen Chou
published: '2019-09-12'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

原始檔案與未來教學更新資訊可於[Patreon](https://www.patreon.com/TheAllenChou)取得

您可於[Twitter](https://twitter.com/TheAllenChou)上追蹤我

本文屬於[遊戲數學](http://allenchou.net/game-math-series/)系列文

[Here](http://allenchou.net/2019/08/tangent-triangles-cannonballs/) is the original English post.

本文之英文原文[在此](http://allenchou.net/2019/08/tangent-triangles-cannonballs/)

**前備教學**

**大綱**

在[上個教學](http://allenchou.net/2019/08/trigonometry-basics-sine-cosine-chinese/)中，我們認識到了兩個基礎三角函數：正弦與餘弦。這次我們要來學習第三個基礎三角函數：正切(tangent)。這三者為三角函數的根基，能夠用來解決遊戲開發過程中會遇到的各種問題。

你將可透過本教學學會：

- 正切函數的幾何意義
- 正弦函數、餘弦函數、與正切函數之間的關係
- 如何用正切函數做出圓滑的入場與退場效果

- 三角形的邊與三角函數之間的關係
- 給定初速與仰角，如何模擬砲彈路徑
- 在發射砲彈前，如何預測砲彈路徑

- 給定水平距離和仰角，如何定位砲彈的目標

![](../../assets/825f655807c2490f.png)

**正切函數的幾何意義**

我們先來看看上個教學中的單位圓，圓上有一點![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


從上個教學中已經得知![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com (X, Y)= (\cos\theta, \sin\theta)](../../assets/669ad390e0febe34.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

**斜率**。

一條線的斜率是其垂直變動與水平變動之間的比率。舉例來說，我們來看看以下線段：

![](../../assets/b34fff32455b8764.png)

從點![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)

![Rendered by QuickLaTeX.com \frac{2}{3}](../../assets/627f54537ffac34d.png)


至於如以下這個”走下坡”的線段：

![](../../assets/a7a2875a50b458e0.png)

其斜率則為![Rendered by QuickLaTeX.com \frac{-2}{3}](../../assets/1d1e638e20df8e10.png)


現在，回到之前的單位圓圖：

我們看到從原點往![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \frac{\sin\theta}{\cos\theta}](../../assets/f9e6e88a475b17d4.png)

![Rendered by QuickLaTeX.com \tan\theta = \frac{\sin\theta}{\cos\theta}](../../assets/75252588076cb604.png)


但那只是個數學式子而已，我們來看看![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


現在只看該切線介於![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


![](../../assets/57a2ee7aa01e50e3.png)

![Rendered by QuickLaTeX.com \angle ABP](../../assets/2322e18a282b421a.png)

![Rendered by QuickLaTeX.com \angle APD](../../assets/501362fc817ef786.png)

![Rendered by QuickLaTeX.com \angle PAB = \angle PAD = \theta](../../assets/a3b87106ce8f51b0.png)

![Rendered by QuickLaTeX.com \overline{AB}](../../assets/01731d67b55d82ca.png)

![Rendered by QuickLaTeX.com A](../../assets/6343987437844d6e.png)

![Rendered by QuickLaTeX.com B](../../assets/fecac56991c2a4c7.png)


接下來，將上圖拆成以下兩個直角三角形：

![](../../assets/704d38a5dd782f60.png)

三角形的內角和為![Rendered by QuickLaTeX.com 180^\circ](../../assets/831c30544c8a897a.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)

![Rendered by QuickLaTeX.com \angle APB](../../assets/194985a69e6859a7.png)

![Rendered by QuickLaTeX.com \angle ADP](../../assets/ebbe60f9f75d0ec5.png)

![Rendered by QuickLaTeX.com 180^\circ - \theta - 90^\circ](../../assets/0f6e06a47b085ff2.png)


當兩個三角形各自的三個角度組合相同，他們便互相為**相似三角形**。意即若將其中一個三角形等比例縮放、旋轉、與翻轉，就有辦法變成跟另外一個三角形一模一樣。

兩個三角形互相為相似三角形時，其中一個三角形的任意兩邊長度比例將會等同於另外一個三角形的對應兩邊長度比例，於是：

![Rendered by QuickLaTeX.com \begin{flalign*} \frac{\overline{BP}}{\overline{AB}} = \frac{\overline{DP}}{\overline{AP}} \end{flalign*}](../../assets/14cd90c5ba3f6d72.png)


已知![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com (\cos\theta, \sin\theta)](../../assets/a390ac661a350c78.png)

![Rendered by QuickLaTeX.com \overline{AB} = \cos\theta](../../assets/8f87b230a143085e.png)

![Rendered by QuickLaTeX.com \overline{BP} = \sin\theta](../../assets/a675e5d40d6ad3bc.png)

![Rendered by QuickLaTeX.com \overline{AP}](../../assets/f8fcf9c44fc38692.png)

![Rendered by QuickLaTeX.com \overline{AP}=1](../../assets/63da667cf2d77044.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \frac{\sin\theta}{\cos\theta} = \frac{\overline{DP}}{1} \end{flalign*}](../../assets/e2c8dfc13592fbd4.png)


我們也知道![Rendered by QuickLaTeX.com \tan\theta = \frac{\sin\theta}{\cos\theta}](../../assets/75252588076cb604.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \tan\theta = \overline{DP} \end{flalign*}](../../assets/15a52a4f57f60b58.png)


我們找到![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)


![](../../assets/c2b3dede1434c7a0.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

*絕對值*這個字眼，因為![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com tan\theta](../../assets/478eee833fe591d2.png)


**正切曲線**

我們已經在上個教學中看過![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/b09117852d9c1c33.png)

現在再把![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)


![](../../assets/966a7142b9ff96d9.png)

請留意![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com [-1, 1]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-96395345c57f8928c42918c656dd1364_l3.png)

![Rendered by QuickLaTeX.com \tan = \frac{\sin\theta}{\cos\theta}](../../assets/fe81b30ffa997615.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com \pi](../../assets/4b60fce59d6919ef.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com 2\pi](../../assets/8536ab24b2361d28.png)


另一值得關注的一點，是此三個函數之間正負號的相互關係。因為![Rendered by QuickLaTeX.com \tan\theta = \frac{\sin\theta}{\cos\theta}](../../assets/75252588076cb604.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)


現在，來試試看把物件的X座標設成正切函數值：

float tan = Mathf.Tan(Rate * Time.time); obj.transform.position = Vector3(tan, 0.0f, 0.0f);

物件從-X方向高速入場、減速、然後又加速往+X方向退場。

我們可以利用這個特性來製作如下的流星效果：

float tan = Mathf.Tan(Rate * Time.time); obj.transform.position = center + moveDirection * tan;

加減速的效果似乎沒有很明顯，那來試著使用![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)


float tan = Mathf.Tan(Rate * Time.time); float tan3 = tan * tan * tan; obj.transform.position = center + moveDirection * tan3;

**三角函數、角度、與三角形**

瞭解了三個基礎三角函數與單位圓的關係之後，，讓我們來探討它們與直角三角形的關係。畢竟這些函數被稱作三角函數，與三角形是關係密切的。

首先，先介紹一些術語，以下是個一角大小為![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/6a395c84bdb60098.png)

兩端為角![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

**鄰邊**(adjacent side)，因為緊鄰![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

**對邊**(opposite side)，因為位於![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

**斜邊**(hypotenuse)。

![](../../assets/4277cca354f62322.png)

以下為三個基礎三角函數與這些**邊長**的關係：

![](http://www.allenchou.net/wp-content/uploads/2019/09/trig-triangle-side-equations.chinese.png)

一時無法記住這些關係的話，可以參考這個視覺記憶法。將![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

**首字母**用草寫如此書寫在三角形的周圍(請原諒我難看的手寫)：

![](../../assets/45eedc11553975c7.png)

書寫一個字母的時候，其對應的函數即為”**第一個擦過的邊**分之**第二個擦過的邊**“：

![](../../assets/948a488dad961366.png)

再來看一次算式：

![](../../assets/e740321431293ff8.png)

不管此直角三角形的大小為何，這些等式恆成立，因為三角形兩邊之比例與各邊的絕對長度是無關的。

若將直角三角形等比例縮放，大小調整為斜邊長度剛好是1，便可把這個直角三角形放入單位圓中，並且與圓周上的一點![Rendered by QuickLaTeX.com P=(X, Y)](../../assets/43f4dd6b0f2b930b.png)


![](../../assets/0fc83ee3bd9f8322.png)

可以發現上述三角函數等式與![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com (X, Y)=(\cos\theta, \sin\theta)](../../assets/6805fba83100c4bd.png)


![Rendered by QuickLaTeX.com \begin{alignat*} \ \sin\theta &= \frac{Y}{1} &&= Y \:\:\:\: \ \cos\theta &= \frac{X}{1} &&= X \:\:\:\: \ \tan\theta &= \frac{Y}{X} &&= \frac{\sin\theta}{\cos\theta} \end{alignat*}](../../assets/4f18870dc35df963.png)


知道了三角函數與直角三角形邊長之間的關係之後，若碰到一角大小為![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


讓我們用![Rendered by QuickLaTeX.com J](../../assets/401c663f919c1f99.png)

**j**acent side)長度，![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)

**s**ite side)長度，![Rendered by QuickLaTeX.com H](../../assets/90b95e98f0a12951.png)

**h**ypotenuse)長度：

![](../../assets/fd3315fdf8743788.png)

若已知斜邊長度![Rendered by QuickLaTeX.com H](../../assets/90b95e98f0a12951.png)

![Rendered by QuickLaTeX.com J = H \cos\theta](../../assets/d60036c596c452d6.png)

![Rendered by QuickLaTeX.com S = H \sin\theta](../../assets/4553e9b8a754a1b3.png)


![](../../assets/f494989ca6bbf1bc.png)

若已知鄰邊長度![Rendered by QuickLaTeX.com J](../../assets/401c663f919c1f99.png)

![Rendered by QuickLaTeX.com S = J \tan\theta](../../assets/312459264f26be6a.png)

![Rendered by QuickLaTeX.com H = \frac{J}{\cos\theta}](../../assets/a628140252396b9c.png)


![](../../assets/2b93873446a413fb.png)

若已知對邊長度![Rendered by QuickLaTeX.com S](../../assets/fd14bbf347776f9d.png)

![Rendered by QuickLaTeX.com J = \frac{S}{\tan\theta}](../../assets/3b533028aa8c84c9.png)

![Rendered by QuickLaTeX.com H = \frac{S}{\sin\theta}](../../assets/085940b003f781ca.png)


![](../../assets/f3d8f3af0f8bb980.png)

**模擬與預測砲彈路徑**

終於到實戰範例的時候了！讓我們來看看，當給定砲彈發射初始速率、發射水平角、與發射仰角，要如何模擬砲彈的行徑，甚至是如何在發射前就預測好完整路徑。

在這之前，先快速地把動力學的專有名詞複習一下。物件在空間中的定位稱為**位置**(position)，物件的位置隨時間之改變率稱為**速度**(velocity – 通常表達為每秒之位置變化)，物件的速度向量長度為**速率**(speed)，物件的速度隨時間之改變率稱為**加速度**(acceleration – 通常表達為每秒之速度變化)。

[尤拉方法](https://en.wikipedia.org/wiki/Euler_method)(Euler Method)是個可以用來模擬物件移動的簡易演算法：針對每個可移動的物件，隨其位置同時保存速度資料。每一次更新(update) – 又稱時間推進(time step)，對物件的速度加上加速度乘以**delta time** (兩次更新之間的時間差)之變化量，在對物件的位置加上速度乘以delta time之變化量：

velocity += acceleration * deltaTime; position += velocity * deltaTime;

欲模擬大約位於地面高度且人體尺寸附近的重力，我們使用一個長度固定且方向往下的向量。以下這個範例使用尤拉方法，模擬一個初始速度向右上方的2D物件行進路線：

若我們在一禎(frame)當中進行多次時間推進，而每過幾次推進便繪製一個小點，就可以畫出物件路徑的預測圖：

velocity = initialVelocity; position = initialPosition; for (int i = 0; i < NumIterations; ++i) { velocity += acceleration * deltaTime; position += velocity * deltaTime; if (i % IterationsPerDot != 0) continue; DrawDot(position); }

現在，令砲彈初始速率(初始速度向量的長度)為![Rendered by QuickLaTeX.com K](../../assets/f6ac230548b6e4a9.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \phi](../../assets/c5571bad897bf9dc.png)

![Rendered by QuickLaTeX.com +Z](../../assets/dd8570719a10e427.png)

![Rendered by QuickLaTeX.com +X](../../assets/d93ba145fc5d93c3.png)


![](../../assets/6b625b6f2e7bdbee.png)

欲計算初始速度，我們需要先計算出相同方向的單位向量(長度為1之向量)，並將其長度乘以![Rendered by QuickLaTeX.com K](../../assets/f6ac230548b6e4a9.png)


下圖顯示![Rendered by QuickLaTeX.com +X](../../assets/d93ba145fc5d93c3.png)

![Rendered by QuickLaTeX.com +Y](../../assets/0977a46715c2053b.png)

![Rendered by QuickLaTeX.com +Z](../../assets/dd8570719a10e427.png)

![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com +Z](../../assets/dd8570719a10e427.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com \phi](../../assets/c5571bad897bf9dc.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)


![](../../assets/8d3c54da8ee7e179.png)

目標是要找出![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)

![Rendered by QuickLaTeX.com K](../../assets/f6ac230548b6e4a9.png)


首先是個水平單位圓圖，含有![Rendered by QuickLaTeX.com +X+](../../assets/26ea0a3876e417b6.png)

![Rendered by QuickLaTeX.com +Z](../../assets/dd8570719a10e427.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/c1862d1ce5111059.png)

再來是個垂直單位圓圖，含有![Rendered by QuickLaTeX.com +Y](../../assets/0977a46715c2053b.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)

![Rendered by QuickLaTeX.com \phi](../../assets/c5571bad897bf9dc.png)


![](../../assets/c9a67b3797d2608a.png)

調整觀看第一個水平單位原圖的角度，找出能夠看到這個令人熟悉的單位圓圖：

![](../../assets/1e2ca3b02e5ba75f.png)

我們之前已經看過這個算法了，![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com +Z](../../assets/dd8570719a10e427.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com +X](../../assets/d93ba145fc5d93c3.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com V_h = (\sin\theta, 0, \cos\theta)](../../assets/9f80d89f88a74aa9.png)


用同樣的視角觀看第二個垂直的單位圓圖：

![](../../assets/574a3d22084701be.png)

同樣的算法，![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)

![Rendered by QuickLaTeX.com V_h](../../assets/efaf292ab5e94d94.png)

![Rendered by QuickLaTeX.com \cos\phi](../../assets/3007bdb5ea502e67.png)

![Rendered by QuickLaTeX.com +Y](../../assets/0977a46715c2053b.png)

![Rendered by QuickLaTeX.com \sin\phi](../../assets/226fa89660a77033.png)

![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)


![Rendered by QuickLaTeX.com \begin{flalign*} V_i &= \cos\phi \cdot V_h + \sin\phi \cdot (0, 1, 0) \\ &= (\cos\phi \sin\theta, \: \sin\phi, \: \cos\phi \cos\theta) \end{flalign*}](../../assets/52b42f6459f9206d.png)


將![Rendered by QuickLaTeX.com V_i](../../assets/8ffb01d982439a7f.png)

![Rendered by QuickLaTeX.com K](../../assets/f6ac230548b6e4a9.png)


![Rendered by QuickLaTeX.com \begin{flalign*} V_i &= K \cdot (\cos\phi \sin\theta, \: \sin\phi, \: \cos\phi \cos\theta) \\ &= (K \cos\phi \sin\theta, \: K \sin\phi, \: K \cos\phi \cos\theta) \end{flalign*}](../../assets/40089914cd52771f.png)


其對應的程式碼如下：

Vector3 ComputeInitialVelocity() { float sinTheta = Mathf.Sin(HorizontalAngle); float cosTheta = Mathf.Cos(HorizontalAngle); float sinPhi = Mathf.Sin(ElevationAngle); float cosPhi = Mathf.Cos(ElevationAngle); return InitialSpeed * new Vector3 ( cosPhi * sinTheta, sinPhi, cosPhi * cosTheta ); }

給定初始速率、水平角、和仰角，能夠算出砲彈發射的初始速度向量，我們便能模擬與預測砲彈路徑：

void FireCannon() { velocity = ComputeInitialVelocity(); obj.transform.position = InitialPosition; } void Update() { float dt = Time.deltaTime; velocity += acceleration * dt; obj.transform.position += velocity * dt; } void DrawTrajectory() { float dt = Time.fixedDeltaTime; Vector3 velocity = ComputeInitialVelocity(); Vector3 position = InitialPosition; for (int i = 0; i < NumIterations; ++i) { velocity += acceleration * dt; position += velocity * dt; if (i % IterationsPerDot != 0) continue; DrawDot(position); }

**放置砲彈目標**

我們能夠發射砲彈了，現在來放置一些目標吧。給定相對於大砲的水平距離與仰角，要如何在正確的位置放置目標？下圖是欲達到的結果，每個目標與大砲的水平(XZ平面上)距離相同，並且水平間隔相等，也就是相對於大砲的水平角間距相等。

![](../../assets/0a35f4faca7d397e.png)

我們已經知道水平角為![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com (\cos\theta, 0, \sin\theta)](../../assets/1c4c6f9824771a57.png)

![Rendered by QuickLaTeX.com D](../../assets/b45ae2142cb26a8a.png)

![Rendered by QuickLaTeX.com (D \cos\theta, 0, D \sin\theta)](../../assets/59c177e62ccfd565.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/7dd82b39b2e6635d.png)

最後一步是求得各目標的Y座標，也就是離地距離。先前已經看過，一個角大小為![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com J](../../assets/401c663f919c1f99.png)

![Rendered by QuickLaTeX.com J \tan\theta](../../assets/deae43e340e71a1f.png)


![](../../assets/2b93873446a413fb.png)

將![Rendered by QuickLaTeX.com J](../../assets/401c663f919c1f99.png)

![Rendered by QuickLaTeX.com D](../../assets/b45ae2142cb26a8a.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \phi](../../assets/c5571bad897bf9dc.png)

![Rendered by QuickLaTeX.com D \tan\phi](../../assets/9fb6fedd4a39b66d.png)


![](../../assets/06dfbe7cab1a4e5a.png)

我們終於能將目標放置在正確的位置了：

float theta = -0.5f * AngleInterval * (NumTargets - 1); float elevationTan = Mathf.Tan(ElevationAngle); foreach (var target in targetArray) { Vector3 horizontalVec = HorizontalDistance * new Vector3 ( Mathf.Sin(theta), 0.0f, Mathf.Cos(theta) ); theta += AngleInterval; Vector3 verticalVec = HorizontalDistance * elevationTan * Vector3.up; target.transform.position = Cannon.position + horizontalVec + verticalVec; }

![](../../assets/825f655807c2490f.png)

我們還沒有討論要如何偵測砲彈是否與目標碰撞，所以砲彈目前會穿過目標：

碰撞偵測(collision detection)非本教學的主題，所以我就很快地帶過球與球之間地碰撞偵測方法。要偵測兩球是否碰撞，就檢查兩球心連線長度是否小於兩球半徑和。若砲彈與目標碰撞，我們便將兩者摧毀。

Vector3 cannonballToTargetVec = target.transform.position - cannonball.transform.position; float cannonballToTargetDist = cannonballToTargetVec.magnitude; if (cannonballToTargetDist < cannonballRadius + targetRadius) { DestroyCannonball(); DestroyTarget(); }

用同樣的方法，我們可以偵測砲彈預測路徑與目標碰撞，提早中止路徑繪製。

然而，這個方法是**離散**(discrete)碰撞偵測，意即當砲彈行進速率夠大時，還是會穿過目標。我們可以用**連續**(continuous)碰撞偵測技巧來解決此問題，但這同樣也不是本教學的範疇，我會在未來的教學中再對其詳加介紹。

**總結**

我們在上個教學中認識了兩個基礎三角函數：正弦與餘弦。於本教學中，我們看到了第三個基礎三角函數 – 正切 – 的幾何意義。我們也學會了正弦、餘弦、與正切對單位圓與直角三角形的關係。

接著，我們將正切函數對角度的作圖與正弦和餘弦的作圖重疊。現在也有能力用正切函數製作圓滑的物件入場與退場效果。

最後，我們學會了當給定初始速率、水平角、和仰角，如何用三個基礎三角函數模擬與預測發射砲彈的路徑。我們也學會了給定相對於大砲的水平距離和仰角，如何放置砲彈目標。

現在我們習得了解決日常遊戲開發問題所必備的三個基礎三角函數。於未來的教學中，我將介紹更多以這些三角函數為基底而衍伸的數學工具，並且會展示其能套用到的實務範例。

若您喜歡這篇教學，請考慮到[Patreon](https://www.patreon.com/TheAllenChou)支持我。感謝！