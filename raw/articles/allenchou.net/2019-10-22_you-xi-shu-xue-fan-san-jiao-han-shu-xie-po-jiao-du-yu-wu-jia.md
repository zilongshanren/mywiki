---
title: 遊戲數學：反三角函數、斜坡角度、與物件面向 | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2019/10/inverse-trig-chinese/
author: Allen Chou
published: '2019-10-22'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

原始檔案與未來教學更新資訊可於[Patreon](https://www.patreon.com/TheAllenChou)取得

您可於[Twitter](https://twitter.com/TheAllenChou)上追蹤我

本文屬於[遊戲數學](http://allenchou.net/game-math-series/)系列文

[Here](http://www.allenchou.net/2019/10/inverse-trig/) is the original English post

本文之英文原文[在此](http://www.allenchou.net/2019/10/inverse-trig/)

**前備教學**

**大綱**

我們已經認識了三個基礎三角函數：正弦、餘弦、與正切。現在我們要來看看它們的**反函數**、以及如何將其利用於遊戲開發。

你將可透過本教學學會：

- 三個基礎三角函數的反函數
- 如何從給定的斜率算出斜坡的角度

- 反三角函數的定義域與值域
- 特殊的方便反三角函數
**atan2** - 如何使物件面相滑鼠游標

**反函數**

一個函數能被視為一個黑盒子，能夠將給定的輸入值轉換成特定的輸出值。若一個函數![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

![Rendered by QuickLaTeX.com x](../../assets/4a5eb3d3e5b045d0.png)

![Rendered by QuickLaTeX.com y](../../assets/450e84e6a4b5edb0.png)

![Rendered by QuickLaTeX.com y = f(x)](../../assets/d77c2906dbd29d1d.png)

![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

![Rendered by QuickLaTeX.com y](../../assets/450e84e6a4b5edb0.png)

![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

**反函數**，寫成![Rendered by QuickLaTeX.com f^{-1}](../../assets/c745738d6228b43c.png)


換句話說，若對一個函數![Rendered by QuickLaTeX.com f](../../assets/0704573ab0e20391.png)

![Rendered by QuickLaTeX.com x](../../assets/4a5eb3d3e5b045d0.png)

![Rendered by QuickLaTeX.com y](../../assets/450e84e6a4b5edb0.png)

![Rendered by QuickLaTeX.com y = f(x)](../../assets/d77c2906dbd29d1d.png)

![Rendered by QuickLaTeX.com f^{-1}](../../assets/c745738d6228b43c.png)

![Rendered by QuickLaTeX.com y](../../assets/450e84e6a4b5edb0.png)

![Rendered by QuickLaTeX.com x](../../assets/4a5eb3d3e5b045d0.png)

![Rendered by QuickLaTeX.com x = f^{-1}(y)](../../assets/f38aa98dc7409b9a.png)


舉例來說，一個將輸入值**加一**的函數，其反函數為一個將輸入值**減一**的函數。讓我們將前者寫成![Rendered by QuickLaTeX.com Add1(x)](../../assets/709b89728c15e452.png)

![Rendered by QuickLaTeX.com Sub(1)](../../assets/e08dd1860cdc42f7.png)

![Rendered by QuickLaTeX.com x=2](../../assets/9a535d89ab250d82.png)

![Rendered by QuickLaTeX.com Add1(x)](../../assets/709b89728c15e452.png)


![Rendered by QuickLaTeX.com \begin{flalign*} y = Add1(2) = 3 \end{flalign*}](../../assets/14222a0631079a2a.png)


當我們把![Rendered by QuickLaTeX.com Add1(2)](../../assets/09eec53bd922889c.png)

![Rendered by QuickLaTeX.com y=3](../../assets/aa808b09cc1ef481.png)

![Rendered by QuickLaTeX.com Sub(y)](../../assets/5f9bfb139ba86536.png)

![Rendered by QuickLaTeX.com x=2](../../assets/9a535d89ab250d82.png)


![Rendered by QuickLaTeX.com \begin{flalign*} x = Sub1(3) = 2 \end{flalign*}](../../assets/e1d829ac4d98513f.png)


**反三角函數**

我們已經知道三角函數的輸入值是角的大小，然後其輸出值是個實數。若將三角函數的輸出值作為輸入值餵入它們的反函數，反函數將會輸出原本三角函數輸入的角(單位為**弳度**)。舉例來說，已知![Rendered by QuickLaTeX.com \sin\frac{\pi}{2} = 1](../../assets/517f620245cc5eaa.png)

![Rendered by QuickLaTeX.com \sin^{-1}1 = \frac{\pi}{2}](../../assets/e684aa67dcd730d6.png)


反三角函數有特殊的名字。![Rendered by QuickLaTeX.com \sin^{-1}](../../assets/7f51f326d5904549.png)

**arcsine**。同樣地，![Rendered by QuickLaTeX.com cos^{-1}](../../assets/5554394ff92918e9.png)

![Rendered by QuickLaTeX.com tan^{-1}](../../assets/be9d0fb7e2f42803.png)

**arccosine**和**arctangent**。於Unity中，呼叫反三角函數的方式如下：

float sinAngle = Mathf.Asin(sinValue); // arcsine float cosAngle = Mathf.Acos(cosValue); // arccosine float tanAngle = Mathf.Atan(tanValue); // arctangent

**斜坡角度**

現在來看個簡單的範例。給定遊戲場景中一斜坡的垂直變量和水平變量，要如何算出斜坡的角度？畫成以下的示意圖，又如何從垂直變量![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com H](../../assets/90b95e98f0a12951.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/b560c156ab7eb34c.png)

目標是用![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com H](../../assets/90b95e98f0a12951.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com V](../../assets/3a07f0d2c6ca11a2.png)

![Rendered by QuickLaTeX.com H](../../assets/90b95e98f0a12951.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \tan\theta = \frac{V}{H} \end{flalign*}](../../assets/4f5016468dd3ee3c.png)


接著，我們便可藉由將![Rendered by QuickLaTeX.com \frac{V}{H}](../../assets/15098bb515667137.png)

![Rendered by QuickLaTeX.com \tan^{-1}](../../assets/1eac89c2a029a376.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \theta = \tan^{-1}\frac{V}{H} \end{flalign*}](../../assets/1fb9b2f647f2a6af.png)


從另一個角度來看，上述等式可以看成是更之前的等式兩邊值各輸入反正切函數的結果。一般來說，![Rendered by QuickLaTeX.com f^{-1}(f(x))](../../assets/87147348e28ce36a.png)

![Rendered by QuickLaTeX.com x](../../assets/4a5eb3d3e5b045d0.png)

![Rendered by QuickLaTeX.com f(f^{-1}(y))](../../assets/62a94f7b59ce96af.png)

![Rendered by QuickLaTeX.com y](../../assets/450e84e6a4b5edb0.png)


![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

[先前的教學](http://allenchou.net/2019/08/trigonometry-basics-sine-cosine-chinese/)所提到，可以將其乘上![Rendered by QuickLaTeX.com \frac{180}{\pi}](../../assets/84b185e1a825b906.png)


於是，現在我們可以做個簡單的互動程式，讓使用者移動一個點，該點與原點形成一個斜坡，並且用該點的座標![Rendered by QuickLaTeX.com (X, Y)](../../assets/20a6cdca242db178.png)


這是程式碼：

Vector3 point = p.transform.position; // compute slope angle in radians float angleRad = Mathf.Atan(point.y / point.x); // convert to degrees // Mathf.Rad2Deg is a constant equal to 180.0f / Pi float angleDeg = angleRad* Mathf.Rad2Deg; text = angleDeg + "°";

**定義域與值域**

使用反三角函數時，了解其**定義域**(domain)與**值域**(range)是非常重要的。

一個函數的定義域是所有有效輸入值的集合，而其值域則為所有可能的輸出值的集合。

舉例來說，![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com [-1, 1]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-96395345c57f8928c42918c656dd1364_l3.png)

![Rendered by QuickLaTeX.com [0, 10)](../../assets/372bff49385780c2.png)


反函數的定義域與值域分別就是其對應函數的值域和定義域吧？對反三角函數來說，事實並非如此。

三角函數是週期函數，這表示不同的輸入值可以對應到同一個輸出值。對正弦函數與餘弦函數來說，甚至同一個週期內的不同輸入值也有可能對應到同一個輸出值。

讓我們再用![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \sin\frac{\pi}{2}](../../assets/c206c4977b549dcf.png)

![Rendered by QuickLaTeX.com \sin\frac{5\pi}{2}](../../assets/600a57d5fde6b1d2.png)

![Rendered by QuickLaTeX.com \sin^{-1}1](../../assets/28dd9b69dffd964f.png)

![Rendered by QuickLaTeX.com \frac{\pi}{2}](../../assets/fb4adb336c085ad9.png)

![Rendered by QuickLaTeX.com \frac{5\pi}{2}](../../assets/79933e887ef34138.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)


![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com [-1, 1]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-96395345c57f8928c42918c656dd1364_l3.png)

![Rendered by QuickLaTeX.com \sin^{-1}x](../../assets/617d5e481ebb6b34.png)

![Rendered by QuickLaTeX.com \cos^{-1}x](../../assets/f9efbcca7770ab29.png)

![Rendered by QuickLaTeX.com [-1, 1]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-96395345c57f8928c42918c656dd1364_l3.png)

![Rendered by QuickLaTeX.com \sin^{-1}x](../../assets/617d5e481ebb6b34.png)

![Rendered by QuickLaTeX.com \cos^{-1}x](../../assets/f9efbcca7770ab29.png)

![Rendered by QuickLaTeX.com [\frac{-\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9774586f3753f3cf9ff0dc4a325ab8c8_l3.png)

![Rendered by QuickLaTeX.com [0, \pi]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-2a4bfe6466ef28b78e984d6d1442a1ba_l3.png)

![Rendered by QuickLaTeX.com \pi](../../assets/4b60fce59d6919ef.png)


所以![Rendered by QuickLaTeX.com \sin^{-1}1](../../assets/28dd9b69dffd964f.png)

![Rendered by QuickLaTeX.com \frac{\pi}{2}](../../assets/fb4adb336c085ad9.png)

![Rendered by QuickLaTeX.com [\frac{-\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9774586f3753f3cf9ff0dc4a325ab8c8_l3.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)


接著來看![Rendered by QuickLaTeX.com \tan^{-1}x](../../assets/5556d89e8d9563b1.png)

![Rendered by QuickLaTeX.com \tan\theta](../../assets/7db77412f46d5e1e.png)

![Rendered by QuickLaTeX.com \tan^{-1}x](../../assets/5556d89e8d9563b1.png)

![Rendered by QuickLaTeX.com \tan^{-1}x](../../assets/5556d89e8d9563b1.png)

![Rendered by QuickLaTeX.com [\frac{-\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9774586f3753f3cf9ff0dc4a325ab8c8_l3.png)

![Rendered by QuickLaTeX.com \sin^{-1}x](../../assets/617d5e481ebb6b34.png)


**方便的Atan2函式**

假設於2D平面上有個點![Rendered by QuickLaTeX.com P=(P_x, P_y)](../../assets/5daa083b44a2c4e5.png)

![Rendered by QuickLaTeX.com P_x > 0](../../assets/dc7cdc0ad30cc85b.png)

![Rendered by QuickLaTeX.com P_y > 0](../../assets/db65c9cbbc32a7ba.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com +X](../../assets/d93ba145fc5d93c3.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


![](../../assets/d2651ff0474ce7cd.png)

我們知道![Rendered by QuickLaTeX.com \tan\theta = \frac{P_y}{P_x}](../../assets/8830b2889b322bca.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \theta = \tan^{-1}\frac{P_y}{P_x}](../../assets/bba1f2628a808a8e.png)

![Rendered by QuickLaTeX.com P_x](../../assets/72c34ba1ade40d99.png)

![Rendered by QuickLaTeX.com P_y](../../assets/93a6993515ec6215.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com [0, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-d1fd87d1f660fa4bc822942855f1726f_l3.png)

![Rendered by QuickLaTeX.com [-\frac{\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7acc7e9164fd8c9bce79d25371045b45_l3.png)


上述計算的程式碼如下：

float angle = Mathf.Atan(p.y / p.x);

那麼如果![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P_x > 0](../../assets/dc7cdc0ad30cc85b.png)

![Rendered by QuickLaTeX.com P_y < 0](../../assets/89c3666522523a26.png)

![Rendered by QuickLaTeX.com \frac{P_y}{P_x}](../../assets/cebf49cfeccffff7.png)

![Rendered by QuickLaTeX.com \tan^{-1}\frac{P_y}{P_x}](../../assets/ea66b1bd5a77642a.png)

![Rendered by QuickLaTeX.com [\frac{-\pi}{2}, 0]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1f29f195f2dea4f7e5d0cfb2b3fcef74_l3.png)

![Rendered by QuickLaTeX.com [-\frac{\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7acc7e9164fd8c9bce79d25371045b45_l3.png)


![](../../assets/ad5522a269070f85.png)

但當![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P_x < 0](../../assets/b949a23d550b1e81.png)

![Rendered by QuickLaTeX.com P_y > 0](../../assets/db65c9cbbc32a7ba.png)

![Rendered by QuickLaTeX.com \frac{P_y}{P_x}](../../assets/cebf49cfeccffff7.png)

![Rendered by QuickLaTeX.com P_2=(P_{2x}, P_{2y})](../../assets/5cdc6027719e5189.png)

![Rendered by QuickLaTeX.com \frac{P_{2y}}{P_{2x}}](../../assets/6b8b05298debb862.png)

![Rendered by QuickLaTeX.com P_4=(P_{4x}, P_{4y})](../../assets/9b2536dbb626658a.png)

![Rendered by QuickLaTeX.com \frac{P_{4y}}{P_{4x}}](../../assets/a1cdf71fa1faa0fa.png)

![Rendered by QuickLaTeX.com (P_{2x}, P_{2y}) = (-P_{4x}, -P_{4y})](../../assets/a956dba7ede7ce21.png)


下圖中的兩點![Rendered by QuickLaTeX.com P_2](../../assets/509d0e95df32a230.png)

![Rendered by QuickLaTeX.com P_4](../../assets/7c9ee61a5b4042ff.png)

![Rendered by QuickLaTeX.com \frac{P_{2y}}{P_{2x}} = \frac{P_{4y}}{P_{4x}}](../../assets/f7f4fcbddee770b8.png)


![](../../assets/2fad48e3d0c7fe69.png)

於上圖中，可以看到第一象限中的點![Rendered by QuickLaTeX.com P_1](../../assets/777e18c079fee59b.png)

![Rendered by QuickLaTeX.com P_3](../../assets/d959e4b624cccb47.png)

![Rendered by QuickLaTeX.com P_2](../../assets/509d0e95df32a230.png)

![Rendered by QuickLaTeX.com P_4](../../assets/7c9ee61a5b4042ff.png)

**銳角**(小於90度之角)都相等。

座標比例![Rendered by QuickLaTeX.com \frac{P_{2y}}{P_{2x}}](../../assets/6b8b05298debb862.png)

![Rendered by QuickLaTeX.com \frac{-P_{2y}}{-P_{2x}}](../../assets/4afbc1a39bc1aa6a.png)

![Rendered by QuickLaTeX.com \frac{P_{4y}}{P_{4x}}](../../assets/a1cdf71fa1faa0fa.png)

![Rendered by QuickLaTeX.com \frac{P_{2y}}{P_{2x}}](https://allenchou.net/wp-content/ql-cache/quicklatex.com-ec63408f54c1974f212fec553769087c_l3.png)

![Rendered by QuickLaTeX.com \tan^{-1}\frac{P_{4y}}{P_{4x}}](../../assets/d25d8c6f89160686.png)


當我們將![Rendered by QuickLaTeX.com \frac{P_{2y}}{P_{2x}}](../../assets/6b8b05298debb862.png)

**頓角**(大於90度的角)，而非紅色的負銳角。算角度的時候，一般都是從+X方向開始計算。

![](../../assets/2e3caa86f066cc39.png)

欲達此目的，我們須將在合併![Rendered by QuickLaTeX.com P_{x}](../../assets/72d0960b6391476f.png)

![Rendered by QuickLaTeX.com P_{y}](../../assets/cc01d06dd0eac8b7.png)

![Rendered by QuickLaTeX.com P_{x}](../../assets/72d0960b6391476f.png)

![Rendered by QuickLaTeX.com P_{y}](../../assets/cc01d06dd0eac8b7.png)

![Rendered by QuickLaTeX.com [-\frac{\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-7acc7e9164fd8c9bce79d25371045b45_l3.png)


// range of this function is (-pi, pi] float FixedUpAtan(float py, float px) { if (px > 0.0f) // normal, no fix-up needed { // "normal" // py > 0.0f : first quadrant // py < 0.0f : fourth quadrant return Mathf.Atan(py / px); } else if (px < 0.0f) // fix-up needed { if (py > 0.0f) // second quadrant return Math.PI + Mathf.Atan(py / px); else if (py < 0.0f) // third quadrant return -Math.PI + Mathf.Atan(py / px); else // angle on negative X axis return 2.0f * Mathf.PI; } else // infinity { if (py > 0.0f) return 0.5f * Mathf.PI; // ratio is positive infinity else if (py < 0.0f) return -0.5f * Mathf.PI; // ratio is negative infinity else return 0.0f; // degenerate input (the origin) } }

這程式碼看起來有點分量，不過幸運的是，幾乎任何程式語言的標準數學函示庫內都已經有個方便的**atan2**函數，其值域![Rendered by QuickLaTeX.com (-\pi, \pi]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1a2076e8b5cb430a7530c947d8828532_l3.png)

**atan2**函數參數順序可能有所不同，不過就我所看過的大部分都是Y先X後。

我常常看到一個對**atan2**函數的誤解，說它只是反正切函數的另外一個替代方案，與正切函數提供的功能沒有差異，這其實是錯的。反正切函數只接受單一輸入值，並且其值域為只涵蓋180度的![Rendered by QuickLaTeX.com [\frac{-\pi}{2}, \frac{\pi}{2}]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-9774586f3753f3cf9ff0dc4a325ab8c8_l3.png)

**atan2**函數接收**兩個**輸入值(![Rendered by QuickLaTeX.com P_y](../../assets/93a6993515ec6215.png)

![Rendered by QuickLaTeX.com P_x](../../assets/72c34ba1ade40d99.png)

![Rendered by QuickLaTeX.com (-\pi, \pi]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-1a2076e8b5cb430a7530c947d8828532_l3.png)


**使物件於3D空間中面相滑鼠游標**

最後，讓我們來看看一個經典範例：使物件面向滑鼠游標。

首先，找出滑鼠游標下的射線(ray)與代表地面的平面(plane)之交點。然後，將一個物件定位於該交點，做出該物件於3D空間中跟著滑鼠游標移動的效果。這個物件就是我們的面相目標。

Camera cam = Camera.current; Vector3 mouse= Input.mousePosition; Ray ray = cam.ScreenPointToRay(mouse); float rayDist; plane.Raycast(ray, out rayDist); sphere.position = ray.GetPoint(rayDist);

接下來，讓我們再度使用[彈彈特效工具包](https://assetstore.unity.com/packages/tools/particles-effects/boing-kit-dynamic-bouncy-bones-grass-water-and-more-135594)中的熟面孔：幽浮兔。當沒有被套用任何旋轉的時候，她的正面是+X方向，而她的左邊則是+Z方向。最終目標是要讓她的正面面向目標。

![](../../assets/54574d2d8321a11a.png)

以幽浮兔為原點，計算面向目標相對於她的座標：

Vector3 coord = sphere.transform.position - ufoBunny.transform.position;

現在來將X軸與連接幽浮兔和面向目標的線段之間的角度標記為![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/52acccf095b69268.png)

我們之前已經看過，在這情況下要如何計算![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

**atan2**函數：

float thetaRad = Mathf.atan2(coord.z, coord.x); // in radians

現在回顧一下這張圖：

![](../../assets/d2651ff0474ce7cd.png)

圖中的是XY平面，隨著![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)


現在我們有了旋轉軸與旋轉角度，我們終於可以建構代表該旋轉的**四元數**(quaternion)。未來將會有專門介紹四元數的教學，當下我們只需要知道四元數是Unity用來表示物件旋轉的資料格式。

float thetaDeg = thetaRad * Mathf.Rad2Deg; // in degrees float axis = Vector3.down; // (0, -1, 0) == -Y axis Quaternion rot = Quaternion.AngleAxis(thetaDeg, axis); ufoBunny.transform.rotation = rot;

這是最終結果：

註：Unity本身已提供如`Quaternion.LookRotation`

與`Transform.LookAt`

等輔助函式，能用來達到相同的效果。不過，本教學的目的在於幫助理解反三角函數。

**總結**

透過本教學，我們認識了反三角函數、它們與其相對應的三角函數之間的關係、以及它們的定義域與值域。

另外，我們知道了反正切函數的值域並沒有涵蓋完整的360度範圍，而**atan2**此方便函數的值域則有涵蓋360度範圍。

最後，我們學會了如何使用**atan2**函數製作經典的使物件面相滑鼠游標的效果。

若您喜歡這篇教學，請考慮到[Patreon](https://www.patreon.com/TheAllenChou)支持我。感謝！