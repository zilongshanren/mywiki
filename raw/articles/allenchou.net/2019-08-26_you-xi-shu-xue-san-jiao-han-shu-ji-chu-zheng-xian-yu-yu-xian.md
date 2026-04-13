---
title: 遊戲數學：三角函數基礎 – 正弦與餘弦 | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2019/08/trigonometry-basics-sine-cosine-chinese/
author: Allen Chou
published: '2019-08-26'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

原始檔案與未來教學更新資訊可於[Patreon](https://www.patreon.com/TheAllenChou)取得

您可於[Twitter](https://twitter.com/TheAllenChou)上追蹤我

本文屬於[遊戲數學](http://allenchou.net/game-math-series/)系列文

[Here](http://allenchou.net/2019/08/trigonometry-basics-sine-cosine/) is the original English post.

本文之英文原文[在此](http://allenchou.net/2019/08/trigonometry-basics-sine-cosine/)

**大綱**

三角函數為遊戲開發所用到的數學中，非常基礎的工具。也是我選擇它作為本系列首篇教學主題的原因。能夠掌握三角函數的要領，對解決遊戲開發所會遇到的眾多問題非常有幫助。

你將可透過本教學學會：

- 兩個基礎三角函數的幾何意義：正弦函數與餘弦函數
- 比較兩個不同的角單位：角度與弳度
- 正弦與餘弦的基本特性
- 如何使物體沿著圓形移動與排列：

- 如何使物體沿著螺旋路線移動：

- 如何製作簡諧運動效果:

- 如何製作阻尼彈簧運動效果:

- 如何製作鐘擺運動效果:

- 如何製作漂浮運動效果:

**正弦函數與餘弦函數的幾何意義**

讓我們先來看看**單位圓**，即半徑為1且中心位於原點的圓。

![](../../assets/eaaac7db3cc32708.png)

選一個位於此圓上的點![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


這正是正弦(![Rendered by QuickLaTeX.com sin\theta](../../assets/0e4fad291ae6e60e.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com (X, Y)](../../assets/20a6cdca242db178.png)

![Rendered by QuickLaTeX.com (cos\theta, sine\theta)](../../assets/b5769b3ca5d95109.png)


換句話說，![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![Rendered by QuickLaTeX.com \sin](../../assets/9c2a44c14ab4d230.png)

![Rendered by QuickLaTeX.com \cos](../../assets/98a85ef943f513f7.png)

![Rendered by QuickLaTeX.com \sin(\theta)](../../assets/949e34d87281021e.png)

![Rendered by QuickLaTeX.com \cos(\theta)](../../assets/cda467841df79800.png)

![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)


![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com [-1, 1]](https://allenchou.net/wp-content/ql-cache/quicklatex.com-96395345c57f8928c42918c656dd1364_l3.png)


若角![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


若把兩個座標的角對時間作圖並排比較，就能觀察到它們基本上是同一個波浪形狀的週期函數，只是位置相差四分之一週期。

![](../../assets/18d681fedbe297e0.png)

這些函數的週期是![Rendered by QuickLaTeX.com 360^\circ](../../assets/0e2e0f15c6dd959f.png)

![Rendered by QuickLaTeX.com 360^\circ](../../assets/0e2e0f15c6dd959f.png)

![Rendered by QuickLaTeX.com \sin450^\circ](../../assets/110b72ef72cc0801.png)

![Rendered by QuickLaTeX.com \sin90^\circ](../../assets/9bd7559da0ce0d0b.png)

![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)

![Rendered by QuickLaTeX.com 360^\circ](../../assets/0e2e0f15c6dd959f.png)

![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)


**角度與弳度**

傳入三角函數的角參數可以是此兩種單位之一：**角度**(degree)與**弳度**(radian)，弳度又稱弧度，我在校時學的名稱是弳度，所以接下來都將使用弳度稱呼。大部分的人都很孰悉角度符號，如直角90度寫成![Rendered by QuickLaTeX.com 90^\circ](../../assets/f665200c5de23ae0.png)

![Rendered by QuickLaTeX.com \sin90^\circ](../../assets/9bd7559da0ce0d0b.png)

![Rendered by QuickLaTeX.com \sin90](../../assets/6ebc520f1c82e39d.png)

**弳度**。

180**度**等同於![Rendered by QuickLaTeX.com \pi](../../assets/4b60fce59d6919ef.png)

**弳**，![Rendered by QuickLaTeX.com \pi](../../assets/4b60fce59d6919ef.png)

**圓周率**，其代表”圓的周長與直弳的比率”，值大約為3.14。所以1弳大約是![Rendered by QuickLaTeX.com \frac{180^\circ}{\pi} \approx 57.3^\circ](../../assets/10e780b96c29b4c5.png)

![Rendered by QuickLaTeX.com 60^\circ](../../assets/b4b5c2ed05db9651.png)

![Rendered by QuickLaTeX.com \sin1](../../assets/716267115524b1c9.png)

![Rendered by QuickLaTeX.com 0.84](../../assets/ab74ed44b4d08644.png)

![Rendered by QuickLaTeX.com \sin60^\circ \approx 0.87](../../assets/f290eef32a1a19ec.png)


以下為一些常見的角度與弳度的對應值：

![Rendered by QuickLaTeX.com \begin{alignat*} \ 30^\circ &= \frac{\pi}{6} \hspace{10 mm} &45^\circ &= \frac{\pi}{4} \hspace{10 mm} &60^\circ &= \frac{\pi}{3} \\ \ 90^\circ &= \frac{\pi}{2} \hspace{10 mm} &180 ^\circ &= \pi \hspace{10 mm} &360^\circ &= 2\pi \\ \end{alignat*}](../../assets/9d57afb952da39c6.png)


使用Unity開發時，呼叫![Rendered by QuickLaTeX.com \sin](../../assets/9c2a44c14ab4d230.png)

![Rendered by QuickLaTeX.com \cos](../../assets/98a85ef943f513f7.png)

`Mathf.Sin`

和 `Mathf.Cos`

。請注意此兩個函式的參數單位為弳度，所以如果要計算![Rendered by QuickLaTeX.com \cos45^\circ](../../assets/02ffb4a29baf24c0.png)


// 這其實是將45弳傳入餘弦函數！ float cos45Deg = Mathf.Cos(45.0f);

45弳大約是![Rendered by QuickLaTeX.com 2578^\circ](../../assets/253f7cbe48985718.png)

![Rendered by QuickLaTeX.com 360^\circ](../../assets/0e2e0f15c6dd959f.png)

![Rendered by QuickLaTeX.com 58^\circ](../../assets/d073d6de3332ee62.png)

![Rendered by QuickLaTeX.com 2578^\circ](../../assets/253f7cbe48985718.png)

![Rendered by QuickLaTeX.com 45^\circ](../../assets/73d9208cfc67b668.png)


正確的寫法是：

// 將角度轉換成弳度 float cos45Deg = Mathf.Cos(45.0f * Mathf.PI / 180.0f);

或者藉由轉換常數來做角度與弳度的換算：

float cos45Deg = Mathf.Cos(45.0f * Mathf.Deg2Rad);

使用Unity編輯器這類工具時，對使用者來說角度單位比弳度單位還友善，因為大部分的人可以馬上想像![Rendered by QuickLaTeX.com 45^\circ](../../assets/73d9208cfc67b668.png)


使用弳度單位的其中一個好處，是能簡化弧長計算。假設要計算一個對應角為30度( ![Rendered by QuickLaTeX.com \frac{\pi}{6}](../../assets/e03058110d50c28f.png)


![](../../assets/3cd0fd52f9823d30.png)

若使用角度單位，必須先用**半徑**![Rendered by QuickLaTeX.com \times 2 \pi](../../assets/4685f4d37f286ea7.png)

![Rendered by QuickLaTeX.com 30^\circ](../../assets/98401b57c754a8b7.png)

![Rendered by QuickLaTeX.com 360^\circ](../../assets/0e2e0f15c6dd959f.png)


![Rendered by QuickLaTeX.com \begin{flalign*} arc &= radius \times 2\pi \times \frac{30^\circ}{360^\circ} \\ &= 2 \times 2\pi \times \frac{1}{12} \\ &= \frac{\pi}{3} \\ \end{flalign*}](../../assets/5a94d91d9f77df5d.png)


使用弳度單位的話，弧長公式就是單純的**半徑**![Rendered by QuickLaTeX.com \times](../../assets/cb929ab1ad6cbe39.png)

**弳度**：

![Rendered by QuickLaTeX.com \begin{flalign*} arc &= radius \times \frac{\pi}{6} \\ &= 2 \times \frac{\pi}{6} \\ &= \frac{\pi}{3} \\ \end{flalign*}](../../assets/351abe181556d3b9.png)


進一步觀察，便能注意到使用圓周長公式可很容易驗證弳度的弧長公式。一個圓基本上就是對應角為![Rendered by QuickLaTeX.com 2\pi](../../assets/8536ab24b2361d28.png)

![Rendered by QuickLaTeX.com \times 2\pi](../../assets/4edb122c2e48895e.png)


**正弦與餘弦的基本特性**

現在讓我們來看看一些對未來數學推導很有用的正弦與餘弦的特性。

單位圓上的一點之座標為![Rendered by QuickLaTeX.com (cos\theta, sin\theta)](../../assets/9c75288dcd3d852d.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

[畢氏定理](https://en.wikipedia.org/wiki/Pythagorean_theorem)(Pythagorean Theorem)說明，此點座標![Rendered by QuickLaTeX.com (X, Y)](../../assets/20a6cdca242db178.png)

![Rendered by QuickLaTeX.com \sqrt{X^2 + Y^2}](../../assets/e18d7a71dc0f274a.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \sin^2\theta + \cos^2\theta = 1 \\ \end{flalign*}](../../assets/69f922f21ad21c3d.png)


![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)

![Rendered by QuickLaTeX.com \sin^2\theta](../../assets/714cd4302fb2c1ba.png)

![Rendered by QuickLaTeX.com \cos^2\theta](../../assets/112a1883da16f06e.png)

![Rendered by QuickLaTeX.com (sin(\theta))^2](../../assets/26357f8f5a35ecd8.png)

![Rendered by QuickLaTeX.com (cos(\theta))^2](../../assets/3cbf6ded5e59c71f.png)


先前展示過正弦與餘弦的並排作圖比較：

![](../../assets/18d681fedbe297e0.png)

可以觀察到餘弦曲線基本上就是正弦曲線往左移90度(![Rendered by QuickLaTeX.com \frac{\pi}{2}](../../assets/fb4adb336c085ad9.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \sin\theta &= \cos(\theta - \frac{\pi}{2}) \\ \cos\theta &= \sin(\theta + \frac{\pi}{2}) \\ \end{flalign*}](../../assets/44800f18b898b86f.png)


**沿著圓形與螺旋線移動**

現在我們知道![Rendered by QuickLaTeX.com (cos\theta, sin\theta)](../../assets/9c75288dcd3d852d.png)


以下程式碼可使一個物件以固定速率沿著圓周運動：

obj.transform.position = new Vector3 ( Radius * Mathf.Cos(Rate * Time.time), Radius * Mathf.Sin(Rate * Time.time), 0.0f );

以下程式碼則可使12個物件以固定速率沿著圓周運動，並且使各物件之間沿著圓周的間距相等：

float baseAngle = Rate * Time.time + angleOffset; for (int i = 0; i < 12; ++i) { float angleOffset = 2.0f * Mathf.PI * i / 12.0f; aObj[i].transform.position = new Vector3 ( Radius * Mathf.Cos(baseAngle + angleOffset), Radius * Mathf.Sin(baseAngle + angleOffset), 0.0f ); }

將沿圓周移動與Z軸移動結合，便可使物件沿著3D螺旋線移動：

obj.transform.position = new Vector3 ( Radius * Mathf.Cos(Rate * Time.time), Radius * Mathf.Sin(Rate * Time.time), ZSpeed * Time.time );

**簡諧運動**

複習一下上面已經看過的餘弦函數之作圖：

![](../../assets/17b0cb4fdc15a91a.png)

如果把物件的X座標設成餘弦函數值會如何？

float x = Mathf.Cos(Rate * Time.time); obj.transform.position = Vector3(x, 0.0f, 0.0f);

我們將會得到此效果：

這種依正弦曲線/正弦波(sinusoid / sine wave)的運動模式稱為簡諧運動(simple harmonic motion, 簡稱S.H.M.)。

由於上面程式中使用的是餘弦函數，物件的初始X座標是![Rendered by QuickLaTeX.com \cos0=1](../../assets/62c342780e03b8bb.png)

![Rendered by QuickLaTeX.com \sin0=0](../../assets/70a261558956c883.png)


傳入正弦與餘弦函數的角度參數稱為**相位**(phase)。當傳入三角函數的相位為時間的倍數時，大多數人會將此模式寫成![Rendered by QuickLaTeX.com \sin \omega t](../../assets/cb6217bc6a3ee6ec.png)

![Rendered by QuickLaTeX.com t](../../assets/2095d761bc925f10.png)

![Rendered by QuickLaTeX.com \omega](../../assets/a6481661bed5b147.png)

**弳/秒**)。舉例來說，![Rendered by QuickLaTeX.com \sin2\pi t](../../assets/bd68f0b77220d099.png)


那麼將簡 諧 運動乘上個指數遞減的係數會如何？

float s = Mathf.Pow(0.5f, Decay * Time.time); float x = Mathf.Cos(Rate * Time.time); obj.transform.position = Vector3(s * x, 0.0f, 0.0f);

物件將會改行**受阻尼彈簧運動**(damped spring motion)：

**鐘擺運動**

若將沿圓形運動的物件之角度設為正弦曲線又會如何？

float baseAngle = 1.5f * Mathf.PI; // 270度 float halfAngleRange = 0.25f * mathf.PI; // 45度 float c = Mathf.Cos(Rate * Time.time); float angle = halfAngleRange * c + baseAngle; obj.transform.position = new Vector3 ( Radius * Mathf.Cos(angle), Radius * Mathf.Sin(angle), 0.0f );

這時物件將會進行**鐘擺運動**(pendulum motion)：

可以想成是沿圓形運動的角度值本身進行簡 諧 運動。

**漂浮運動**

再來追加一個範例。這是幽浮兔，她是我的Unity彈彈特效工具包[Boing Kit](https://assetstore.unity.com/packages/tools/particles-effects/boing-kit-135594)範例中的角色。

![](../../assets/12cbada0961cf888.png)

來試著將錯開的簡諧運動分別套用到她的X、Y、Z座標：

Vector3 hover = new Vector3 ( RadiusX * Mathf.Sin(RateX * Time.time + OffsetX), RadiusY * Mathf.Sin(RateY * Time.time + OffsetY), RadiusZ * Mathf.Sin(RateZ * Time.time + OffsetZ) ); obj.transform.position = basePosition + hover;

如次便可產生漂浮運動(hover motion)的效果：

漂浮運動的位移可以進一步運來計算傾斜角度。這超出本文的主題範圍，所以我就僅列出程式碼與結果：

obj.transform.rotation = baseRotation * Quaternion.FromToRotation ( Vector3.up, -hover + 3.0f * Vector3.up );

**總結**

本教學結束了！

我們認識到了![Rendered by QuickLaTeX.com \sin\theta](../../assets/7d9b4d65b65dc299.png)

![Rendered by QuickLaTeX.com \cos\theta](../../assets/1a6ed96fe1b2c7a6.png)


我希望這篇教學能幫助你更加了解兩個基本三角函數：正弦函數與餘弦函數。

下一篇教學，我將介紹另一個基本三角函數：正切函數，並且會介紹更多這三個三角函數的應用。

我們下篇教學再見！

若您喜歡這篇教學，請考慮到[Patreon](https://www.patreon.com/TheAllenChou)支持我。感謝！