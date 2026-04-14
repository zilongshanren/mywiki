---
tags: [source, 渲染, 光栅化, 齐次坐标, debugging]
date: 2026-04-14
sources: 1
---

# Triangle rasterization in homogeneous coordinates gotcha（Matthäus G. Chajdas / anteru.net）

[[matthaeus-chajdas]] 2010 年 5 月在 anteru.net 上发表的一篇短笔记，记录他在实现 Olano & Greer 1997 年论文 *Triangle scan conversion using 2D homogeneous coordinates* 时遇到的一个**几乎抓不到**的 bug。

## 摘要

齐次坐标三角形光栅化把三个顶点的 `(x, y, w)` 拼成 3×3 矩阵 `M`，求逆得到 `M⁻¹`，三行同时是边方程系数与重心坐标变换。作者偶然把 `M⁻¹` 转置（手写 3×3 伴随矩阵求逆漏写 transpose，或者向量从错的一边乘进矩阵），结果发现：三角形覆盖几何完全正确——**但整个三角形被插值出同一个 z 值**。更阴险的是这个 z 刚好等于某个顶点的 z，所以画 1px 大小的三角形测试时一切正确，bug 只在跨像素插值时出现。作者额外提到这个 bug 难抓的原因：`M` 远非对称，转置不应当还能算出近似正确的值；矩阵 conditioning 普遍很差，让人误以为是数值问题（作者花了不少时间换 inversion 算法、改善条件数）；行 / 列同时被边判别使用，让人误以为矩阵项算对了。修复后的小优化：插值常数 1 对应的那一行不需要做矩阵乘，三个分量加和直接得到 `w`，省下三次乘法。文章配了两张对比截图，一张是 transpose bug 下的色块化深度，一张是修复后线性变化的深度。

## 关键要点

- **bug 表现**：三角形内 z 全部为常数，色块化；但几何与覆盖正确。
- **根本原因**：`M⁻¹` 在某个环节被转置——可能是手写求逆漏 transpose，或向量乘矩阵的方向错了。
- **难抓原因 1**：错值刚好等于某个顶点的 z，pixel-sized 三角形单元测试通过。
- **难抓原因 2**：`M` 不对称，「转置后还正确」反直觉，作者最初怀疑数值稳定性 / conditioning。
- **难抓原因 3**：行 / 列又被边判别用，边判别正确让人误以为矩阵项算对了。
- **修复后微优化**：用 `(x, y, 1)` 乘 `M⁻¹` 算 `w` 时，三个分量求和即可，省 3 次乘。
- **debug 教训**：把 z 渲染成可视化灰度，「平坦色块 vs. 渐变」一眼就分清。
- **被引用论文**：Olano & Greer 1997, *Triangle scan conversion using 2D homogeneous coordinates*。

## 链接到的概念

- [[homogeneous-rasterization-transpose-bug]]
- [[pineda-edge-rasterization]]
- [[triangle-setup]]
- [[perspective-correct-interpolation]]
- [[debug-visualization]]
- [[matthaeus-chajdas]]

## 原文

- 链接：https://anteru.net/blog/2010/triangle-rasterization-in-homogeneous-coordinates-gotcha
- 本地：`raw/articles/anteru.net/2010-05-03_triangle-rasterization-in-homogeneous-coordinates-gotcha.md`
- 配图：`raw/assets/fa46a8aada35c06f.png`（bug 状态），`raw/assets/28f78b03e35c9498.png`（修复后）
