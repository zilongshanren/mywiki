---
title: 遊戲數學：內積、量尺、與彈力球 | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2020/01/dot-product-projection-reflection-chinese/
author: Allen Chou
published: '2020-01-18'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

原始檔案與未來教學更新資訊可於[Patreon](https://www.patreon.com/TheAllenChou)取得

您可於[Twitter](https://twitter.com/TheAllenChou)上追蹤我

本文屬於[遊戲數學](http://allenchou.net/game-math-series/)系列文

[Here](https://www.allenchou.net/2020/01/dot-product-projection-reflection) is the original English post

本文之英文原文[在此](https://www.allenchou.net/2020/01/dot-product-projection-reflection)

**前備教學**

**大綱**

內積是個簡單卻又十分有用的數學工具，它能將兩個向量的長度與方向之間的關係濃縮成一個單一數值。向量能夠應用在計算投影、反射、打光、與許多其他遊戲相關運算。

你將可透過本教學學會：

- 內積的幾何意義
- 如何將一個向量投影到另外一個向量上
- 如何沿任意軸向測量物件的尺寸

- 如何針對一個平面反射一個向量
- 如何模擬彈力球於斜坡上的行進路線

**內積**

假設有兩個向量，![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![](../../assets/ca006afa65a4f411.png)

**內積**(**dot product**)是個數學運算元，它能結合兩個向量而得出一個單一數值。此值即為第一個向量投影於第二個向量上的**有號長度**(**signed magnitude**)乘以第二個向量的長度。可以把投影想成是用個平行光源將第一個向量的影子映照在第二個向量上，且光源方向與第二個向量方向垂直。

![](../../assets/f616aa93297bff95.png)

我們將![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)


若兩向量之間的夾角小於90度，則第一個向量的有號長度為正(即相當於其長度)。若夾角大於90度，則第一個向量的有號長度則為負(其長度加上負號)。

兩向量何者為第一何者為第二，其實並不重要。將兩者的順序調換，內積結果仍然不變。

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a} \cdot \vec{b} = \vec{b} \cdot \vec{a} \end{flalign*}](../../assets/30a60266f5134a4f.png)


若![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)


**內積公式 – 餘弦版**

注意圖中有個直角三角形，令![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)


![](../../assets/c0d24ceaa5b5d56c.png)

記得[本教學](https://allenchou.net/2019/08/trigonometry-basics-sine-cosine-chinese)提到直角三角形的鄰邊長即為斜邊乘上角度![Rendered by QuickLaTeX.com \theta](../../assets/459f4056e3bc49b2.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \lvert \vec{a} \rvert \cos{\theta}](../../assets/01632481cca73a32.png)


![](../../assets/06ff1a16ab0e2cee.png)

兩項量的內積可以表達成兩項量各自的長度與夾角之餘弦值三者相乘，本算式同時也驗證了內積之兩項量前後順序並不影響結果的特性：

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a} \cdot \vec{b} = \lvert \vec{a} \rvert \lvert \vec{b} \rvert \cos{\theta} \end{flalign*}](../../assets/bb77dd5db1cc20d0.png)


若兩項量![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)

![Rendered by QuickLaTeX.com \cos{\theta}](../../assets/d53591b39d48d80f.png)


若兩向量互相垂直(夾角90度)，則內積值為零。若夾角小於90度，則內積值為正。若夾角大於90度，則內積值為負。由此可見，利用兩項量之內積的正負號，便已可粗略知道兩者方向的同異性。

由於![Rendered by QuickLaTeX.com \cos{0^\circ} = 1](../../assets/ee67ca26bc80f572.png)

![Rendered by QuickLaTeX.com \cos{180^\circ} = -1](../../assets/5a773d4879a5183a.png)

![Rendered by QuickLaTeX.com \lvert \vec{a} \rvert \lvert \vec{b} \rvert](../../assets/361752b374aede4b.png)

![Rendered by QuickLaTeX.com - \lvert \vec{a} \rvert \lvert \vec{b} \rvert](../../assets/8c240daa181080fa.png)


## **內積公式 – 分量版**

當我們以三個分量組成一個3D向量的方式表達兩個3D向量時(總共六個浮點數)，兩個向量之夾角並不是馬上就看得出來的。幸好有另外一個不需要用到夾角餘弦的內積計算方式，假設![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a} &= (a_x, a_y, a_z) \\ \vec{b} &= (b_x, b_y, b_z) \end{flalign*}](../../assets/4c9441a5aa027d0b.png)


那麼兩項量之內積值即等於三個軸向的分量各自相乘之後再相加：

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a} \cdot \vec{b} = a_x b_x + a_y b_y + a_z b_z \end{flalign*}](../../assets/8cea86c4e6c61dce.png)


不但簡單，又不需要用到餘弦函數！

Unity提供`Vector3.Dot`

函式，以計算兩個向量之內積：

float dotProduct = Vector3.Dot(a, b);

以下為該函式的一種實作：

Vector3 Dot(Vector3 a, Vector b) { return a.x * b.x + a.y * b.y + a.z * b.z; }

計算向量長度的算式為![Rendered by QuickLaTeX.com \lvert \vec{a} \rvert = \sqrt{a_x^2 + a_y^2 + a_z^2}](../../assets/1ffc13e9c125d080.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \lvert \vec{a} \rvert = \sqrt{\vec{a} \cdot \vec{a}} \end{flalign*}](../../assets/47c0dad126d9c205.png)


記得先前得出的內積算式![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b} = \lvert \vec{a} \rvert \lvert \vec{b} \rvert \cos{\theta}](../../assets/dfac780a221c54ac.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \theta = \cos^{-1}{(\frac{\vec{a} \cdot \vec{b}}{\lvert \vec{a} \rvert \lvert \vec{b} \rvert})} \end{flalign*}](../../assets/a3a8f6fbdce0b37e.png)


若![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \vec{a} \cdot \vec{b} &= \cos{\theta} \\ \theta &= \cos^{-1}{(\vec{a} \cdot \vec{b})} \end{flalign*}](../../assets/df925c56eb58d03e.png)


**向量投影**

我們已知向量內積的幾何定義，即為一被投影向量之有號長度與另一向量之長度相乘。現在就讓我們來看看如何將一個向量投影到另外一個向量上。令![Rendered by QuickLaTeX.com \vec{c} = {project}_{\vec{b}}(\vec{a})](../../assets/ce16b7dfc4116b5f.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![](../../assets/63c79315691e125f.png)

與![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \frac{\vec{b}}{\lvert \vec{b} \rvert}](../../assets/da576e21adaa434d.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{c}](../../assets/f80e34d6e3bd75fb.png)

![Rendered by QuickLaTeX.com \vec{c}](../../assets/f80e34d6e3bd75fb.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


既然內積![Rendered by QuickLaTeX.com \vec{a} \cdot \vec{b}](../../assets/dce7ac233073ff31.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{c}](../../assets/f80e34d6e3bd75fb.png)

![Rendered by QuickLaTeX.com \vec{a}](../../assets/19de170cb829a9d0.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)

![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \frac{\vec{a} \cdot \vec{b}}{\lvert \vec{b} \rvert} \end{flalign*}](../../assets/3ee40892e3be8a17.png)


將此有號長度乘上單位向量![Rendered by QuickLaTeX.com \frac{\vec{b}}{\lvert \vec{b} \rvert}](../../assets/da576e21adaa434d.png)


![Rendered by QuickLaTeX.com \begin{flalign*} \vec{c} = {project}_{\vec{b}}(\vec{a}) = \frac{\vec{a} \cdot \vec{b}}{{\lvert \vec{b} \rvert}^2} \: \vec{b} \end{flalign*}](../../assets/a4e515813bda8918.png)


由於![Rendered by QuickLaTeX.com {\lvert \vec{b} \rvert}^2 = \vec{b} \cdot \vec{b}](../../assets/7d39973fe8ec11f2.png)


![Rendered by QuickLaTeX.com \begin{flalign*} {project}_{\vec{b}}(\vec{a}) = \frac{\vec{a} \cdot \vec{b}}{\vec{b} \cdot \vec{b}} \: \vec{b} \end{flalign*}](../../assets/7e95adfc2d32ce56.png)


若![Rendered by QuickLaTeX.com \vec{b}](../../assets/7c4189e6504626c8.png)


![Rendered by QuickLaTeX.com \begin{flalign*} {project}_{\vec{b}}(\vec{a}) = (\vec{a} \cdot \vec{b}) \: \vec{b} \end{flalign*}](../../assets/f5d59ae6058c7db4.png)


Unity提供`Vector3.Project`

函式，以計算將一個向量投影至另一向量上：

Vector3 projection = Vector3.Project(vec, onto);

以下為該函式的一種實作：

Vector3 Project(Vector3 vec, Vector3 onto) { float numerator = Vector3.Dot(vec, onto); float denominator = Vector3.Dot(onto, onto); return (numerator / denominator) * onto; }

有時候需要留意一個退化狀況，也就是作為投影目標的向量本身長度為零或近乎零，如此便會造成除以零的運算而導致數值爆炸。單單只用Unity的`Vector3.Project`

函式即有可能會遇到此狀況。

處理此狀況的方法之一，是預先運算作為投影目標的向量長度。若長度太小，則改用另外一個長度夠大的後備向量作為投影目標(如+X單位向量、角色正前方向量等)：

Vector3 SafeProject(Vector3 vec, Vector3 onto, Vector3 fallback) { float sqrMag = v.sqrMagnitude; if (sqrMag > Epsilon) // 與一個極小數相比 return Vector3.Project(vec, onto); else return Vector3.Project(vec, fallback); }

**習題：量尺**

現在來看個向量投影的習題：製作一個任意軸向的量尺，以測量物件延此軸向的尺寸。

我們用個基準點(base)和軸向(axis)代表量尺：

struct Ruler { Vector3 Base; Vector3 Axis; }

欲將一個點投影到量尺上，首先，找出該點對於量尺基準點的相對向量。接下來，將此向量投影至量尺軸向上。最後，將量尺基準點沿著量尺軸向以此向量投影位移，即可得該點於量尺上之投影：

![](../../assets/6f1c339f64a3b9b1.png)

Vector3 Project(Vector3 vec, Ruler ruler) { // 計算相對向量 Vector3 relative = vec - ruler.Base; // 投影 float relativeDot = Vector3.Dot(vec, ruler.Axis); Vector3 projectedRelative = relativeDot * ruler.Axis; // 從基準點位移 Vector3 result = ruler.Base+ projectedRelative; return result; }

名為`relativeDot`

的中介值，基本上即為點之投影與量尺基準點沿著量尺軸向之有號距離，若與軸向相同則為正，若與軸向相反則為負。

計算物件模型中的每一個頂點投影到量尺上的有號距離，取得最小與最大的有號距離，最大值減最小值即為該物件沿著量尺軸向測量出的尺寸。從量尺基準點，位移量尺軸向乘以最小與最大之有號距離，則可得到該物件投影到量尺上的兩個端點。

void Measure ( Mesh mesh, Ruler ruler, out float dimension, out Vector3 minPoint, out Vector3 maxPoint ) { float min = float.MaxValue; float max = float.MinValue; foreach (Vector3 vert in mesh.vertices) { Vector3 relative = vert- ruler.Base; float relativeDot = Vector3.Dot(relative , ruler.Axis); min = Mathf.Min(min, relativeDot); max = Mathf.Max(max, relativeDot); } dimension = max - min; minPoint = ruler.Base+ min * ruler.Axis; maxPoint = ruler.Base+ max * ruler.Axis; }

**向量反射**

接著我們要來看如何計算向量![Rendered by QuickLaTeX.com \vec{v}](../../assets/fe0c58e4e9fa1ad9.png)

![Rendered by QuickLaTeX.com \vec{n}](../../assets/f4d4d2619671dfcd.png)


![](../../assets/e8aacdc36d3f6ee5.png)

我們可將向量拆解成與平面平行的分量![Rendered by QuickLaTeX.com \vec{v}_\parallel](../../assets/939aeedbea4cfe2b.png)

![Rendered by QuickLaTeX.com \vec{v}_\perp](../../assets/1902ddf4c29d8b29.png)


![](../../assets/90426688095a8f46.png)

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{v} = \vec{v}_\parallel + \vec{v}_\perp \end{flalign*}](../../assets/2bb65b210eab5835.png)


垂直分量便是向量投影至平面法向量上的結果，而平行分量則是原本向量減去垂直分量：

![Rendered by QuickLaTeX.com \begin{flalign*} \vec{v}_\perp &= {project}_{\vec{n}}(\vec{v}) \\ \vec{v}_\parallel &= \vec{v} - \vec{v}_\perp \end{flalign*}](../../assets/71dc7da5f40536de.png)


將平行分量方向反轉再加上垂直分量，便可得到向量對平面反射的結果。

![](../../assets/f2459092fab4e31d.png)

令反射為![Rendered by QuickLaTeX.com {reflect}_\vec{n}}(\vec{v}](../../assets/a01dad2dba6a36d8.png)


![Rendered by QuickLaTeX.com \begin{flalign*} {reflect}_{\vec{n}}(\vec{v}) = \vec{v}_\parallel - \vec{v}_\perp \end{flalign*}](../../assets/11fe5bd0e63de87b.png)


若我們將![Rendered by QuickLaTeX.com \vec{v}_\parallel](../../assets/939aeedbea4cfe2b.png)

![Rendered by QuickLaTeX.com \vec{v} - \vec{v}_\perp](../../assets/bca3004e5fba2b1c.png)


![Rendered by QuickLaTeX.com \begin{flalign*} {reflect}_{\vec{n}}(\vec{v}) = \vec{v} - 2\vec{v}_\perp \end{flalign*}](../../assets/c3d51225f5cc9a55.png)


Unity提供`Vector3.Reflect`

函式，以計算向量反射：

float reflection = Vector3.Reflect(vec, normal);

以下為該函式的一種實作：

Vector3 Reflect(Vector vec, Vector normal) { Vector3 perpendicular= Vector3.Project(vec, normal); Vector3 parallel = vec - perpendicular; return parallel - perpendicular; }

而以下為使用另一種向量反射算式之實作：

Vector3 Reflect(Vector vec, Vector normal) { return vec - 2.0f * Vector3.Project(vec, normal); }

**習題：彈力球與斜坡**

現在我們知道如何反射向量，我們便已具備足夠知識，以模擬彈力球於斜坡上的行進路線：

我們將使用於[先前的教學](https://www.allenchou.net/2019/09/tangent-triangles-cannonballs-chinese/)中所提到的尤拉方法(Euler Method)來模擬受重力影響的球之行進路線：

ballVelocity+= gravity * deltaTime; ballCenter += ballVelocity* deltaTime;

欲偵測球與斜坡的碰撞，我們必須知道如何偵測一個球體是否以穿透了一個平面。

球體可用球心與半徑代表，平面可用法向量與平面上之一點代表。令球心為![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com R](../../assets/ab9820595f7b211b.png)

![Rendered by QuickLaTeX.com \vec{n}](../../assets/f4d4d2619671dfcd.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com P](../../assets/c603478e83db650a.png)

![Rendered by QuickLaTeX.com C](../../assets/4ad5461ab20da426.png)

![Rendered by QuickLaTeX.com \vec{u}](../../assets/cd0fea837a52d7bd.png)


![](../../assets/fcb316ffa3c6838d.png)

若球體沒有穿透平面，與平面垂直的![Rendered by QuickLaTeX.com \vec{u}](../../assets/cd0fea837a52d7bd.png)

![Rendered by QuickLaTeX.com \vec{u}_\perp](../../assets/05825d1d8662c6ad.png)

![Rendered by QuickLaTeX.com \vec{n}](../../assets/f4d4d2619671dfcd.png)

![Rendered by QuickLaTeX.com R](../../assets/ab9820595f7b211b.png)


![](../../assets/b2d24696ae6cc040.png)

換句話說，若![Rendered by QuickLaTeX.com \vec{u} \cdot \vec{n} > R](../../assets/f25bd93dec613edf.png)

![Rendered by QuickLaTeX.com R - \vec{u} \cdot \vec{n}](../../assets/a3c4ee7db51b97a2.png)


欲修正球心位置，我們只需要將球體沿著平面法向量![Rendered by QuickLaTeX.com \vec{n}](../../assets/f4d4d2619671dfcd.png)


// 若無穿透，回傳原始球心位置 // 若有穿透，回傳修正後之球心位置 void SphereVsPlane ( Vector3 c, // 球心位置 float r, // 球半徑 Vector3 n, // 平面法向量(單位向量) Vector3 p, // 平面上一點 out Vector3 cNew, // 球心位置輸出 ) { // 原始球心位置為預設值 cNew = c; Vector3 u = c - p; float d = Vector3.Dot(u, n); float penetration = r - d; // 有無穿透? if (penetration > 0.0f) { cNew = c + penetration * n; } }

將球心修正邏輯安排到積分邏輯後面：

ballVelocity += gravity * deltaTime; ballCenter += ballVelocity* deltaTime; Vector3 newSpherePosition; SphereVsPlane ( ballCenter, ballRadius, planeNormal, pointOnPlane, out newBallPosition ); ballPosition = newBallPosition;

球穿透斜面後的位置修正，伴隨著速度向量對著斜面反射，便可模擬球從斜面反彈的效果。

上面的動畫展示的是完全彈性碰撞，且看起來不自然。正常來說，反彈力道會隨著反彈次數因能量消耗而減少，於是球會越彈越低。

一般來說，會用一個單一**彈性**值(**restitution**)來模擬兩物件之間的碰撞。當彈性為100%，則球會完美反彈。當彈性為50%，則球平行於斜面法向量的速度分量會於反彈後減半。彈性即為球平行於斜面法向量的速度分量於碰撞後與碰撞前之比例。以下為將彈性納入考量的向量反射函數：

Vector3 Reflect ( Vector3 vec, Vector3 normal, float restitution ) { Vector3 perpendicular= Vector3.Project(vec, normal); Vector3 parallel = vec - perpendicular; return parallel - restitution * perpendicular; }

此為將彈性納入考量而修改的`SphereVsPlane`

函數：

// 若無穿透，回傳原始球心位置 // 若有穿透，回傳修正後之球心位置 void SphereVsPlane ( Vector3 c, // 球心位置 float r, // 球半徑 Vector3 v, // 球速度 Vector3 n, // 平面法向量(單位向量) Vector3 p, // 平面上一點 float e, // 彈性 out Vector3 cNew, // 球心位置輸出 out Vector3 vNew // 球速度輸出 ) { // 原始球心位置與球速度為預設值 cNew = c; vNew = v; Vector3 u = c - p; float d = Vector3.Dot(u, n); float penetration = r - d; // 有無穿透? if (penetration > 0.0f) { cNew = c + penetration * n; vNew = Reflect(v, n, e); } }

然後將球心位置修正邏輯用完整的反彈邏輯取代：

ballVelocity+= gravity * deltaTime; spherePosition += ballVelocity* deltaTime; Vector3 newSpherePosition; Vector3 newSphereVelocity; SphereVsPlane ( spherePosition , ballRadius, ballVelocity, planeNormal, pointOnPlane, restitution, out newBallPosition, out newBallVelocity; ); ballPosition= newBallPosition; ballVelocity= newBallVelocity;

現在，我們終於能模擬不同彈性的彈力球於斜坡上的行進路線：

**總結**

透過本教學，我們認識了向量內積的幾何意義，以及其算式(餘弦版本與分量版本)。

另外，我們瞭解了如何用內積計算向量投影，和如何用向量投影測量物件沿任意量尺軸向之尺寸。

最後，我們學會了用內積反射向量，及如何用項量反射模擬彈力球於斜坡上的行進路徑。

若您喜歡這篇教學，請考慮到[Patreon](https://www.patreon.com/TheAllenChou)支持我。感謝！