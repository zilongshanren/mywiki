---
title: Unity Geometry Shader Cookbook – Unity 幾何著色器簡介
url: https://tedsieblog.wordpress.com/2019/04/09/unity-geometry-shader-cookbook/
author: Ted Sie
published: '2019-04-09'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

常見的可編程 Shader 有 Vertex Shader 及 Fragment Shader，而 Shader Model 4.0 及 OpenGL 3.2 開始引入了 Geometry Shader 幾何著色器。

用這篇文章來記錄如何在 Unity 中實作 Geometry Shader。


![](../../assets/052e639f19887b22.gif)


##### 執行順序

Rendering Pipeline 中執行順序依次為 Vertex Shader、Geometry Shader 及 Fragment Shader。

**Vertex Shader**

負責逐頂點處理，由於數入的單位是單一頂點，所以無法取得鄰近點、線、面的資料，而 Geometry Shader 就是用來處理這些資料之間的關係。

**Geometry Shader**

負責圖元 (Primitive) 處理，不但能夠取得點、線、面之間的關係，還能進行新增及刪減的動作。

**Fragment Shader**

負責逐像素處理，將經過 Rasterisation 後的像素進行計算。

##### 定義 Geometry Shader 方法

#pragma geometry geom

##### 定義資料結構

//由應用階段到 Vertex Shader 的資料結構 struct a2v { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; //由 Vertex Shader 到 Geometry Shader 的資料結構 struct v2g { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; //由 Geometry Shader 到 Fragment Shader 的資料結構 struct g2f { float4 vertex : SV_POSITION; float2 uv : TEXCOORD0; };

##### 撰寫 Geometry Shader

[maxvertexcount(3)] void geom(triangle v2g input[3], inout TriangleStream<g2f> outStream) { g2f o; for(int i = 0; i < 3; i++) { o.vertex = UnityObjectToClipPos(input[i].vertex); o.uv = input[i].uv; outStream.Append(o); } outStream.RestartStrip(); }

**屬性**

maxvertexcount(number) //設定 Geometry Shader 的最大輸出頂點數

**輸入**

point //點圖元資料 line //線圖元資料 lineadj //線圖元資料，包含鄰近線圖元資料 triangle //面圖元資料 triangleadj //面圖元資料，包含鄰近面圖元資料

**輸出**

PointStream //點 Stream 資料 LineStream //線 Stream 資料 TriangleStream //面 Stream 資料

**Stream 方法**

Append(struct) //新增 Stream 資料 RestartStrip() //使用 TriangleStream 時，需要使用這個方法形成面圖元資料（三點為一面）

##### 實作範例

PointStream/Vertex

![](../../assets/edf04234c01eee71.jpg)


LineStream/Line

![](../../assets/7b876e712c80cd6f.jpg)


TriangleStream/DoNothing

![](../../assets/544a86647cdcea82.jpg)


TriangleStream/ExtrudeVertex

![](../../assets/ec4089047a5ac04d.jpg)


TriangleStream/TriangleAnimation

![](../../assets/d7bef9d586db5178.gif)


TriangleStream/ExtrudePyramid

![](../../assets/bb9888bcaec9e04f.jpg)


TriangleStream/ExtrudePyramidAnimation

![](../../assets/876c7e5e9044bcdf.gif)


TriangleStream/ExtrudeTriangle

![](../../assets/eb5d2158c515618f.jpg)


TriangleStream/ExtrudeTriangleAnimation

![](../../assets/052e639f19887b22.gif)


##### Repository

##### 參考資料

[keijiro/StandardGeometryShader](https://github.com/keijiro/StandardGeometryShader)

[幾何著色器 (Geometry Shader) | 逍遙文工作室](https://cg2010studio.com/2011/06/30/geometry-shader/)

[Unity3D Geomerty Shader – 苍白的茧](http://www.dreamfairy.cn/blog/2016/06/05/unity3d-geomerty-shader/)

## One thought on “Unity Geometry Shader Cookbook – Unity 幾何著色器簡介”