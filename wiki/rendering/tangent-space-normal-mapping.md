---
tags: [渲染, 法线贴图, 切线空间, 凹凸贴图, 视差贴图]
date: 2026-04-14
sources: 1
---

# 切线空间法线贴图与视差家族（Tangent Space Normal Mapping）

法线贴图是**凹凸贴图**（bump mapping）这一大类的核心代表：通过纹理向 shading 模型「注入」表面方向的细节，模拟那些不大到值得做几何、又不小到能被 BRDF 隐含掉的**中尺度**结构。和位移贴图不同，凹凸家族**不修改几何**，只在着色阶段做手脚。[[apoorva-joshi|Apoorva Joshi]] 2017 年在 *Exploring Bump Mapping with WebGL* 里把这一家从最朴素的 normal mapping 到 parallax occlusion mapping 串成一篇 demo 教程，本页整理其中的数学骨架。

## 为什么必须用切线空间

法线贴图把 RGB 通道当作 X / Y / Z 三个分量来存表面法线，常见编码是 `n = tex * 2 - 1`，因此 `(128,128,255)` 对应 $(0,0,1)$。如果这些法线**直接存在世界空间**，物体一旋转所有法线就要重新烘焙，而且形状相同但朝向不同的两个 mesh 也无法共享同一张贴图。解决办法是把法线存在**切线空间**（tangent space）——一组随着 mesh 表面「贴住」的局部基底——再在运行时把它换基到世界空间做光照。

## TBN 与换基

切线空间的三个基向量是**切线 T**、**副切线 B** 和**法线 N**：T 是 UV 中 $u$ 方向的偏导，B 是 $v$ 方向的偏导，二者与 N 一同构成局部坐标架。T、B 通常在 mesh 加载时**逐顶点预计算**并放进 vertex buffer；vertex shader 用模型-视图矩阵的**逆转置**把 T、B 变换到世界空间，再叉积出对应的世界空间 N。

把任意切线空间向量 $V_{ts}$ 搬到世界空间是一次换基乘法：

$$
V_{ws} = \begin{pmatrix} T_x & B_x & N_x \\ T_y & B_y & N_y \\ T_z & B_z & N_z \end{pmatrix} V_{ts}
$$

反方向需要这个矩阵的**逆**。当 mesh UV 没有 shearing、TBN 正交时，矩阵是正交矩阵，**逆等于转置**——这是性能上的关键省略。如果存在 UV shearing，就必须老老实实在 shader 里求逆。

## 哪一空间做光照

光位置在世界空间，法线在切线空间，要算 Lambertian 必须先把它们搬到同一个空间。两个选择：

1. **法线 → 世界空间**：每像素都要做一次 $V_{ws} = M\,V_{ts}$，开销在 fragment shader。
2. **世界向量 → 切线空间**：只在 vertex shader 里把光位置、相机位置、片段位置乘上 $M^{T}$，让它们沿光栅化阶段被插值到 fragment。

第二种通常更便宜，因为变换次数从「片段数」降到「顶点数」，演示代码也走这条路：vertex shader 输出 `ts_light_pos / ts_view_pos / ts_frag_pos`，fragment shader 在切线空间里直接 `dot(light_dir, n)`。这是实时管线里非常典型的「**把贵的换基操作往上推**」优化。

## Parallax 家族：在 normal map 之上加几何错觉

法线贴图对斜视角的弱点是**没有遮挡感**——不论从哪个角度看，凸起后面的纹理都在原位。视差贴图族补这个洞：在采样 albedo / normal **之前**，按 view ray 与 height map 的「交点」对 UV 做一次偏移 $\Delta uv$。

- **Parallax mapping**：$\Delta uv = h \cdot v_{xy} / v_z$，单次采样 + 一阶近似。便宜但深度大或视角斜时会明显漂移。带 offset limiting 的变种 $\Delta uv = h \cdot v_{xy}$ 用更糙的近似换更稳的边缘。
- **Steep parallax mapping**：把深度 $[0,1]$ 切成 $N$ 层，沿 view ray 线性搜索，找到第一个深度值大于当前层深度的点。本质是一次粗糙的 ray-marching，步数越多越准、越贵。痛点是离散步长导致**台阶状 artefact**。
- **Parallax occlusion mapping (POM)**：在 steep 找到交点后，再取**前一层**的深度，把交点位置在两层之间 lerp 出来，相当于把高度场局部当作直线段近似。在中等步数下视觉效果显著好于 steep，是当代「便宜假位移」的常见选择。

更激进的变体（cone step mapping、relaxed cone tracing、true POM）走的是同一条路：把搜索从均匀步长换成更智能的步长。所有 parallax 技术都建立在切线空间法线之上，只是在 normal sampling 前多做一段 UV 修正。

## 与其它法线贴图技术的关系

- [[normal-map-blending]] —— 把两张切线空间法线贴图叠加为一张，关注的是**叠加运算**而不是怎么得到 TBN。
- [[tangent-free-normal-mapping]] —— 用 `dFdx` / `dFdy` 在 fragment shader 里现算 TBN，省掉顶点缓冲里的 T、B，是本页传统方案的优化版。
- [[diffuse-lighting-lambertian]] —— 视差和 normal 都是为 Lambertian / 镜面项**喂角度**用的。

## 相关

- [[apoorva-joshi]]
- [[coordinate-spaces]] —— 切线空间是其中之一，存在的理由同样是「让某个数学更简单」
- [[fragment-shader]]
- [[shader-vector-math-primer]]

## Sources

- [[sources/apoorvaj-normal-mapping]]
- [[sources/c0de517e-normalmaps-everywhere]]
