---
tags: [渲染, 颜色, 色彩管理, shader]
date: 2026-04-14
sources: 1
---

# OKLab 色彩空间

**OKLab** 是 Björn Ottosson 于 2020 年提出的感知均匀色彩空间，目标是用最小的数学代价逼近人眼对**亮度**和**色度**的感知。相比传统 HSV/HSL/CIELab，它的优势是**混合得好**——两色之间的直线插值，看起来是自然、连续的过渡，不会像 sRGB/linear-RGB 那样跌进中间灰或断色。对 shader 作者来说，它几乎是「免费」升级到感知域的一把钥匙：一对 3×3 矩阵加一个立方根就够了。

## 为什么 sRGB 混合不行

在 [[color-space|sRGB]] 或 linear RGB 里把黄色和蓝色各取一半，得到的是中灰：两端明明都带色，中点却失去了色度。原因是 R/G/B 三通道在中点互相抵消，而「红和绿感觉上比蓝更亮」这件事 RGB 完全不反映。即便先做 gamma 校正到 linear RGB 再混合，光度是对了，但**色度轨迹仍是一条穿过灰点的直线**，不符合感知。

## OKLab 的数学

OKLab 用两次 3×3 矩阵乘法加一次立方根就能从 linear RGB 转换过去：

```glsl
vec3 oklab_from_linear(vec3 lin) {
  const mat3 M1 = mat3(...);   // linear RGB → LMS（长/中/短波视锥响应近似）
  const mat3 M2 = mat3(...);   // LMS' → OKLab
  vec3 lms = M1 * lin;
  return M2 * (sign(lms) * pow(abs(lms), vec3(1.0/3.0)));
}
```

`sign(lms)*pow(abs(lms), 1/3)` 是非线性压缩——把 LMS 响应压到感知均匀的量纲。反变换对称，用 `lms*lms*lms` 替回立方根。

输出三个分量的含义：

- **L**（lightness，0-1）——感知亮度。
- **a**（绿-洋红轴，约 -0.5 ~ +0.5）。
- **b**（蓝-黄轴，约 -0.5 ~ +0.5）。

## 使用纪律

OKLab 本身**只接受 linear RGB 输入**，所以管线必须是：

```
sRGB → linear RGB → OKLab → mix/manipulate → linear RGB → sRGB
```

忘了任何一步 gamma 转换都会毁掉 OKLab 的感知性质。

## Inigo Quilez 的优化版 mix

iq 写了一版融合两端 sRGB→OKLab→sRGB 的 `oklab_mix`，把两次 pow 合成一次立方根/立方，并在中点加一点点 `1 + 0.2*a*(1-a)` 的 gain 拉亮——严格说已经不是 OKLab 了，但视觉上更讨喜。这是 shader 社区常见的做法：**先学数学，再微调给眼睛看**。

## 用途

- **渐变 / 过渡动画**：UI、粒子、2D 场景的线性插值瞬间好看很多。
- **调色盘生成**：等间距采样 L/chroma 能拿到真正均匀的色阶。
- **颜色量化**：像 Xor 的量化工具那样，在 OKLab 距离里找「最感知不同」的 N 色代表。
- **无障碍 / 色盲辅助**：OKLab 下的色差更接近人眼感受到的「可区分度」。
- **OKLCh / OKHSV**：Ottosson 还推导了 OKLab 的极坐标变体，可直接替代 HSL 做调色盘。

## 和其它色空间的关系

- 比 CIELab **数学更简单**，不依赖 XYZ、D65 白点适配的一整套历史包袱。
- 比 HSV/HSL **更符合感知**——HSV 的 V 是 max(R,G,B)，和亮度没什么关系。
- 是 [[color-space|色彩空间]]家族的一员，但专注的是「混合/插值时好看」，不是「色域覆盖」。
- 显示前仍需要做 TRC 编码（sRGB gamma），OKLab 本身并不涉及显示输出的 encode 过程。

## 相关

- [[color-space]] — sRGB / linear / gamma 的三要素
- [[color-lut]]
- [[local-tonemapping]]
- [[spectral-rendering]] — 另一条彻底绕开 RGB 的路
- [[xor-shader-artist]]

## Sources

- [[sources/xor-mini-oklab]]
