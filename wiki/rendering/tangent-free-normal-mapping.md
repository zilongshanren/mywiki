---
tags: [渲染, 法线贴图, 切线空间, 像素着色器]
date: 2026-04-14
sources: 1
---

# 无预计算切线的法线贴图（Tangent-Free Normal Mapping）

传统 normal mapping 依赖**预计算的切线 / 副切线（tangent / bitangent）**：在美术管线里为每个顶点烘焙一对向量，和 normal 一起组成正交的 TBN 矩阵，再由 vertex shader 传给 pixel shader 用来把切线空间的法线转回世界空间。这套方案的代价是**每顶点多两条向量**的存储与带宽，以及 mesh 导出器必须正确生成——实践里两条都很昂贵。

Christian Schüler 在 *ShaderX5* 里给出了一种替代：**在 pixel shader 里用屏幕空间偏导数（`dFdx` / `dFdy`）临时构造 TBN 基**。他后续又把它进一步压缩成几行代码，不再需要顶点里存 T 和 B。[[kostas-anagnostou|Kostas Anagnostou]] 2013 年在 FX Composer 里复现并视觉比较后，觉得足够好用。

## 核心思路

UV 和位置同时是屏幕函数，所以 `dFdx(position)` / `dFdy(position)` 给出世界空间里 UV 方向的切线。让 $p$ 为插值后的世界位置、$uv$ 为插值后的纹理坐标、$N$ 为插值后的法线：

$$
\begin{aligned}
p_x = \partial p/\partial x,\quad p_y = \partial p/\partial y\\
uv_x = \partial uv/\partial x,\quad uv_y = \partial uv/\partial y
\end{aligned}
$$

用反向映射解出切线 $T$ 和副切线 $B$（即在 UV 方向上的世界空间切向量），再和 $N$ 一起做 Gram-Schmidt 正交化得到 TBN，最后把采样到的切线空间法线乘以 TBN 变换到世界空间做光照。全部操作都在 pixel shader 内完成，**顶点缓冲里只需要 position / normal / uv**。

## 代价与权衡

- **节省**：顶点带宽和显存（每顶点少 6–8 个 float）；消除 mesh 导出器生成错误 TBN 的事故源。
- **代价**：pixel shader 里多几条算术指令（几次 derivative、几次叉积 / 点积、一次 normalize）。
- **视觉差异**：Anagnostou 的测试显示两者非常接近；`thetenthplanet.de` 的原作者补充，在 UV 严重畸变处（比如茶壶壶嘴），预计算 TBN 反而会丢细节，像素级算出的 TBN 要更稳。
- **适用面**：**带宽 / 内存比 ALU 更紧**的平台首选；顶点动画 / 过程式 UV 偏移等会破坏预计算 TBN 正确性的情形，几乎必须用这个。
- **注意**：`dFdx`/`dFdy` 需要 2×2 像素 quad，所以不能在 vertex shader 里等价实现——想把 V / L 向量提前变到切线空间再在 vertex shader 做插值那套**快法**，这里用不上。

## 与 [[normal-map-blending]] 的关系

两者都在讨论「法线贴图的现代用法」但在不同层面：这里是**怎么拿到 TBN**，那里是**怎么把两张法线贴图叠起来**。两个优化可以叠加。

## 相关

- [[normal-map-blending]]
- [[fragment-shader]]
- [[compact-vertex-format]] —— 另一个从顶点格式里省字节的角度
- [[microfacet-brdf]]

## Sources

- [[sources/interplay-tangent-free-normal-mapping]]
