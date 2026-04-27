---
tags: [渲染, 法线贴图, 凹凸贴图, 切线空间, 着色器]
date: 2026-04-27
sources: 4
---

# Derivative Map（导数贴图）

**Derivative map** 是由 Morten Mikkelsen（Naughty Dog）在论文 *Bump Mapping Unparametrized Surfaces on the GPU* 中提出的一种凹凸映射替代方案。它与 [[tangent-space-normal-mapping|法线贴图]] 的核心区别在于：**不需要预计算切线向量**，只需要表面法线和屏幕空间/UV 空间的偏导数，就能在像素着色器中扰动法线。

## 原理

高度场 $h(u,v)$ 的梯度在平面上是二维向量，而在三维曲面上需要将它投影到表面上，这个投影结果称为**表面梯度**（surface gradient）。扰动后的法线为：

$$
\mathbf{n}' = \mathbf{n} - \nabla_s \beta
$$

其中表面梯度由 $s/t$ 两个方向（可取屏幕空间 $x/y$）的几何偏导数 $\partial\mathbf{p}/\partial x$、$\partial\mathbf{p}/\partial y$ 以及高度偏导数 $\partial h/\partial x$、$\partial h/\partial y$ 共同计算：

$$
\nabla_s\beta = \frac{(\sigma_t \times \mathbf{n})\,\beta_s + (\mathbf{n} \times \sigma_s)\,\beta_t}{\mathbf{n} \cdot (\sigma_s \times \sigma_t)}
$$

取屏幕空间偏导数时，$\sigma_s = \texttt{ddx}(\mathbf{p})$、$\sigma_t = \texttt{ddy}(\mathbf{p})$，高度偏导数同样用 `ddx(h)` / `ddy(h)` 直接得到。

## 实现方案对比

### 方案一：用 `ddx`/`ddy` 实时计算

代价最低，但双线性滤波使得相邻 texel 间梯度恒定，近距离会出现明显块状。HLSL 5.0 可用 `ddx_fine`/`ddy_fine` 缓解，但根本问题是 2×2 像素 quad 的粒度限制。

### 方案二：预计算 UV 空间导数（推荐）

将高度场 $h$ 对 $u$、$v$ 的偏导数预先存入两通道纹理（即 derivative map 本身），运行时在 shader 中用链式法则：

$$
\frac{\partial h}{\partial x} = \frac{\partial h}{\partial u}\cdot\frac{\partial u}{\partial x} + \frac{\partial h}{\partial v}\cdot\frac{\partial v}{\partial x}
$$

将 UV 空间导数转为屏幕空间导数。这样 derivative map 中存储的是**连续可滤波的梯度值**，mipmap 链上的插值也是正确的，视觉质量与 normal map 相当。

## 与 Normal Map 的权衡

| | Derivative Map | Normal Map |
|---|---|---|
| **顶点格式** | 不需要切线向量（节省 ~27% 网格内存） | 需要 T、B 向量 |
| **插值器** | 一个少（传输更窄） | 需要传 T、B 到 pixel shader |
| **ALU** | 多约 5 条指令 | 较少 |
| **纹理采样** | 多 5 条（两组 ddx/ddy + resinfo） | 少 |
| **灵活性** | 只能表示有高度场基础的扰动 | 可表示任意方向 |
| **混合** | 直接相加，天然正确 | 混合算法需特殊处理（见 [[normal-map-blending]]） |
| **实测性能** | 与 normal map 基本持平（AMD 6750M 测试） | 基准 |

实测显示额外的 ALU 指令被减少的插值器带宽大致抵消。

## 已知 Artifact 与调试

1. **方块状块感**：双线性滤波的副作用；用预计算导数贴图可根本解决。
2. **竖向条纹**：Driscoll 2012 年发现原因是**错误的 mipmap 生成**（每级额外引入一列垃圾数据）。与 FXAA 和各向异性滤波叠加后被放大为明显的竖向条纹。修复 mipmap 生成逻辑后消失。
3. **AMD 旧卡滤波精度**：AMD 当代 GPU 对 < 16 bit/通道纹理的滤波质量有问题，导数贴图建议使用 16 bit 通道。
4. **各向异性滤波**：斜视角下细节过多时建议改用三线性滤波。

## 优势场景

- **过程式几何**（无 UV，无切线）：直接在 world space 用 `ddx`/`ddy` 即可。
- **内存敏感平台**：省去切线向量节省的网格内存有实际意义。
- **法线混合**：相比 normal map，derivative map 可以直接相加混合，无需特殊的 RNM 算法。

## 相关

- [[tangent-space-normal-mapping]] — 传统切线空间 normal map，derivative map 的主要替代对象
- [[tangent-free-normal-mapping]] — 另一种在 pixel shader 中临时构造 TBN 的思路
- [[normal-map-blending]] — normal map 混合的专门讨论
- [[fwidth-derivative-antialiasing]] — `dFdx`/`dFdy` 在 shader 中的其他用途
- [[mipmap-generation-sampling]] — mipmap 生成正确性对 derivative map 至关重要
- [[compact-vertex-format]] — 省切线向量是顶点格式压缩的一个方向
- [[rory-driscoll]]

## Sources

- [[sources/rory-derivative-maps]]
- [[sources/rory-derivative-maps-vs-normal-maps]]
- [[sources/rory-derivative-map-artifacts]]
