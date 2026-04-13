---
title: Image Processing Kernel in Unity
url: https://tedsieblog.wordpress.com/2017/07/22/image-processing-kernel-in-unity/
author: Ted Sie
published: '2017-07-22'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

在 Real-Time Rendering Third Edition 的 Image-Based Effects 章節中提到了影像處理技術

而在其中的 Image Processing Kernel 段落中提到了高斯模糊及邊緣檢測

這兩種影像處理技術都有著相似的取樣原理

透過 Convolution Kernel 或 Convolution Matrix 來取樣貼圖的數據

而達到不同的效果


這次收集了許多不同種類的 Kernel

透過 Unity 進行簡單的驗證

將這些 Kernel 的取樣結果記錄下來


#### Identity

![](../../assets/dc3b1744a3ccebc4.png)



#### BoxBlur

![](../../assets/58194ee6a3ca9452.png)



#### Gaussian Blur 3×3

![](../../assets/57741d002f981ea9.png)



#### Sharpen

![](../../assets/d3c7bfde8b182b3d.png)



#### Emboss 3×3

![](../../assets/e3994dbd9614e3b1.png)



#### Edge Enhance

![](../../assets/41d716a68c4250d9.png)



#### Edge Detection 1

![](../../assets/c6113c9d1d5e025d.png)



#### Edge Detection 2

![](../../assets/dd9ce3ec7db298f6.png)



#### Edge Detection 3

![](../../assets/e838b60871285742.png)



#### Gradient Roberts 2×2




![](../../assets/22662d22c0307607.png)



#### Gradient Prewitt 3×3




![](../../assets/7ef6d85781b50351.png)



#### Gradient Sobel 3×3




![](../../assets/ad2671f640665e0a.png)



#### Github


#### 參考資料

[Kernel(image processing)](https://en.wikipedia.org/wiki/Kernel_(image_processing))

[3×3 convolution kernels](http://matlabtricks.com/post-5/3x3-convolution-kernels-with-online-demo#demo)

[8.2. Convolution Matrix](https://docs.gimp.org/en/plug-in-convmatrix.html)

Unity Shader 入門精要, 第12章 螢幕後處理效果, 12.3 邊緣檢測

Nice article, very very useful.

LikeLike