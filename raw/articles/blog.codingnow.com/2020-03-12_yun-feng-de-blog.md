---
title: 云风的 BLOG
url: https://blog.codingnow.com/2020/03/
published: '2020-03-12'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 矩阵 decompose 的一点优化

我们的游戏引擎中，有个重要的功能是将一个矩阵分解成 S 缩放，R 旋转，T 位移三个分量。这里 T 直接取矩阵的第四行即可，代价比较高的是 S 和 R 的分解，其中 R 又取决于 S 的提取。

但是，游戏中大量的矩阵中是不包含缩放的，即 S 分量大多是 (1,1,1) 。一旦不用缩放，又可以简化 R 提取的操作。所以我打算对传统算法做一点优化。在提取 S 的时候多加一次判断，看值是否接近 1 。

计算 S 的方法是将矩阵的前三行当作三个 vector 3 分别取 length 。length 其实是取 dot 然后计算 sqrt。由于大多数情况预测 dot 值很可能为 1 ，那么当 dot 接近 1 的时候，就不必再开方了。

我很好奇判断一个数字是否接近 1 有没有什么技巧可以提高性能，所以我写了三个版本测试。

static inline int equal_one(float f) { union { float f; uint32_t n; } u; u.f = f; return ((u.n + 0x1f) & ~0x3f) == 0x3f800000; // float 1 } #define EPSILON 0.000001f static inline int equal_one_float1(float f) { float v = f - 1.0f; return fabs(v) < EPSILON; } static inline int equal_one_float2(float f) { float v = f - 1.0f; return -EPSILON < v && v < EPSILON; }

后两个版本很常规，区别在于要不要调用 fabs 取绝对值。第一个版本则是针对 float 的 ieee 754 的二进制表示做的，是一个整数运算的版本。

我在 PC 上做了简单的性能测试，第一版和第二版性能几乎一致，而第三版要慢 3 倍。我认为原因在于第三版多了一次比较操作（有分支情况）。而针对 ieee 754 的 float 做 fabs 本质上仅仅是将高位置为 0 ，甚至比整数版 abs 还要快。现代编译器一般都会做此优化。

暂时没有在 arm CPU 上测试。不过如果不开 NEON 的话，arm 的浮点运算将全部导致函数调用，肯定不如第一个版本好。

第一版的缺点是扩展性不足，一旦从 float 换成 double 就要重新编写。