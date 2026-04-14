---
tags: [shader, 坐标, 后处理, 入门]
date: 2026-04-14
sources: 1
---

# 纹素与像素之间的换算

**Pixel（像素）**是屏幕空间的单位，**Texel（纹素）**是纹理空间的单位。两者之所以总被混淆，是因为在全屏后处理的最简场景下，它们几乎一一对应；一旦涉及缩放、旋转或多纹理页，就完全是两套坐标系了。理解它们之间的换算是写任何后处理 shader 的基础功。

## 最简换算公式

片元 shader 里拿到的 `v_vTexcoord` 是归一化的纹理坐标，范围 `[0, 1]`。想把它换成"以屏幕像素为单位"的坐标，只需要知道**一个纹素在归一化空间里占多大**——如果当前 surface 覆盖整个房间：

```
u_texel = vec2(1.0 / room_width, 1.0 / room_height);
```

这个 `u_texel` 是从外部传进来的 uniform。然后 shader 里双向换算：

```glsl
vec2 pixel      = v_vTexcoord / u_texel;   // 纹理 → 像素
vec2 new_coords = pixel * u_texel;         // 像素 → 纹理
```

典型用法是后处理放大镜：在像素空间里计算"鼠标到当前像素"的矢量、距离衰减、偏移量，最后再把修正后的像素坐标乘回 `u_texel` 去采样原图。

## 复杂情况要走矩阵

上面的换算只在**最简场景**成立：surface 覆盖整个屏幕、纹理独占一个 texture page（不是图集里的子区域）、鼠标坐标是屏幕相对的。一旦 view 有旋转 / 缩放 / 歪斜，或者纹理是图集的一角而 UV 并非 `[0,1]`，就需要引入[[coordinate-spaces|坐标空间]]的变换矩阵和它们的逆矩阵，否则怎么换都对不上。这也是为什么理解"这是什么空间的单位"永远是 shader debug 的第一步。

## 相关

- [[fragment-shader]]
- [[coordinate-spaces]]
- [[shader-vector-math-primer]]
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-texels-pixels]]
