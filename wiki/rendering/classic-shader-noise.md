---
tags: [渲染, 噪声, shader, 程序纹理, 数学]
date: 2026-04-14
sources: 3
---

# 经典 shader 噪声函数家族

[[xor-shader-artist|Xor]] 的 Mini: Noise 两篇文章把 shader 里最常见的六种噪声函数——hash、value、Perlin、Worley、Voronoi、fractal——放在同一套坐标约定下手写一遍。它们的共同骨架是「把平面划成整数 cell，在每个 cell 内用哈希生成伪随机量，再按插值或距离规则把像素值组合出来」。把这六个函数打包看，比单独学任何一个都更容易理解「噪声」这类程序纹理的共性。

## Hash：一切的起点

所有噪声都需要一个廉价的 **伪随机哈希函数**：输入一个整数坐标，输出一个看起来随机但确定可复现的数。Xor 用的是经典 sine-fract 套路：

```glsl
float hash1(vec2 p) {
    return fract(sin(p.x*0.129898 + p.y*0.78233) * 43758.5453);
}
```

两个关键经验：**magic number 要避免明显的整数比**（否则会出现对角条纹），以及输入维度变了就要换一组魔数或直接用 `mat2` 打包投影。这类 sine-based hash 在现代 GPU 上有已知的 cross-vendor 精度问题，但作为教学和 shader art 够用。真正讲究的场景请看 [[non-cryptographic-hash]] 与 [[pcg3d-hash]]。

Perlin 需要返回向量的 `hash2`（两个魔数对），Worley / Voronoi 也复用它——哈希函数实际上是整个噪声家族的公用基础库。

## Value Noise：哈希 + 双线性插值

**Value noise** 是最直白的做法：把像素 `p` 落到整数 cell `floor(p)`，采样 cell 四角的 hash 值，再按 sub-cell 坐标做双线性插值即可。直接线性插值看起来有棱有角，常用的改良是套一个 **cubic smoothstep** 预处理：

```glsl
vec2 cube = sub*sub*(3.0 - 2.0*sub);
```

这正是 [[shader-color-interpolation|lerp]] 页讨论的 `3x² - 2x³`——在 `t=0,1` 处一阶导数为零，视觉上没有网格化的硬边。高维扩展是指数级的：2D 要 4 次哈希和 3 次 lerp，3D 要 8 次哈希、7 次 lerp，以此类推。

## Perlin Noise：梯度点积版的 value noise

Perlin 把「cell 角上存一个随机值」换成「cell 角上存一个随机方向向量」，然后用 **方向 · (像素位置 − cell 角)** 的点积作为该角的贡献。意义上，每个 cell 角都是一个「随机斜面」，噪声是这些斜面按 sub-cell 坐标混合的结果。效果比 value noise 更自然，因为梯度混合天然避免了 cell 中心的极值点。

Perlin 推荐搭配 **quintic smoothstep** `6t⁵ - 15t⁴ + 10t³`，二阶导也连续，使得梯度场本身光滑（做法线 / 偏微分时不会出现台阶）。Perlin 的输出范围是 `[-√2, +√2]`，归一化到 `[0,1]` 通常乘 0.7 加 0.5。

## Worley Noise：距离场而非插值

**Worley noise**（又叫 cellular noise）走的是另一条路——它压根不做插值，而是**把每个 cell 内随机放一个「特征点」，输出到最近特征点的距离**。为了避免边界上距离跳变，需要遍历 3×3 邻域取最小值。本 wiki 的 [[worley-voronoi-noise]] 页用更多笔墨讲了它的代价、变体（F1 / F2 / F2-F1）以及 Blender 节点里 27 次哈希的工程现实。

Xor 把「F1 距离」作为 Worley 的最简版本介绍，然后演化出——

## Voronoi Noise：按最近 cell ID 上色

**Voronoi noise** 只是在 Worley 的循环里额外记录「最近的 sample_cell」，最后用 `hash1(voronoi_cell)` 给每个 Voronoi 域染一个随机灰度。视觉上是蜂窝或者龟裂图案，每个「细胞」内部颜色恒定。它也是 shader graph 里 Voronoi 节点常见的一个输出通道。

## Fractal Noise：把任意噪声叠成 fBm

**Fractal noise** 不是一种新噪声，而是**把上面任意一种叠若干层**的组合模式——学术圈叫 fractional Brownian motion (fBm)，Xor 直接叫 octave：

```glsl
for (int i = 0; i < oct; i++) {
    noise_sum  += value_noise(p) * weight;
    weight_sum += weight;
    weight     *= per;          // 强度衰减，常用 0.5
    p *= mat2(1.6, 1.2, -1.2, 1.6);  // scale ×2 + 旋转 ~143°
}
return noise_sum / weight_sum;
```

几个经验值：每层把坐标放大 2 倍、每层把权重乘 0.5（persistence），以及**用一个非 90° 倍数的旋转矩阵**——否则相邻 octave 会对齐出栅格感。这与 [[layered-grid-noise]] 里黄金角旋转的动机一模一样：**打破周期性需要无理数角度**。对 Perlin 做 fBm 得到云、烟、山脉；对 Worley 做 fBm 得到岩石和细胞聚类。

## Simplex Noise：把方形 cell 倾斜成三角

[[sources/xor-mini-noise-3|Noise 3]] 补上了 Ken Perlin 的另一发明 **Simplex noise**。Perlin 在 N 维需要 `2^N` 次哈希采样（2D=4，3D=8，4D=16），Simplex 把空间**倾斜成等边三角形网格**后每个点只需 `N+1` 个邻居——2D=3，3D=4，4D=5。做法是：先 `p += F*(p.x+p.y)` 把坐标斜到 rhombus（`F = 0.366025`），`floor(skew)` 拿 cell，`sub = skew - cell`，再按 `sub.x > sub.y` 判断走上三角还是下三角；3 个顶点到采样点的相对位移用权重 `max(0.5 - d², 0)⁴` 做软 falloff，最后按各顶点的梯度做点积求和。2D 场景下 Simplex 的代码复杂度盖过了采样节省——**真正的增益要到 3D/4D 才显现**。Wikipedia 的 Simplex noise 条目有完整常数推导。

## Functions vs Textures：算 or 查？

噪声既可以**现算**（函数式，fragment shader 每像素跑完整公式）也可以**烘焙**（预算到一张纹理然后采样）。Xor 给出的取舍表相当实用：

| 形态 | 优势 | 劣势 |
|---|---|---|
| Functions | 无限范围、动态参数、高精度、任意维度 | 高代价尤其 fractal 多 octave、跨硬件不一致、可能出 artifact |
| Textures | 任意复杂噪声一次预算、多设备一致、可人手编辑 | 动画不便、额外 VRAM、受纹理尺寸限制、需 tileable |

如果选纹理路线就得解决**tileable noise**。技巧非常简单：坚持方形 cell，并在每次 hash 前 `mod(cell, s)`，s 就是 tile 尺寸。value/Perlin/Worley/Voronoi 都适用。Fractal 版不能用 143° 旋转（会破坏方形约束），改用 `p = p.yx * 2.0 + 9.0`——swap + scale + translate——同样能打破 octave 对齐又保住 tileability。`gpu_set_texrepeat(true)` 是这一路线的天然搭档。

## 家族关系速查

| 名字 | 核心操作 | 连续性 | 典型用途 |
|---|---|---|---|
| Hash | 单次伪随机 | 全不连续 | 其他一切的基础 |
| Value | 角点 hash + 插值 | C¹（用 cubic）/ C²（用 quintic） | 简单程序纹理 |
| Perlin | 梯度点积 + 插值 | C² | 云、地形、烟雾 |
| Worley | 到最近点的距离 | C⁰ | 龟裂、岩石、细胞 |
| Voronoi | 最近 cell 的 hash 值 | 分片常数 | 蜂窝、马赛克 |
| Fractal | 任意噪声按 octave 叠加 | 与基噪声一致 | 自然感 = 多频段细节 |

这张表也解释了为什么「Perlin + fBm」成了最广泛的默认组合：梯度法带来高阶连续性，fBm 又补足了多尺度细节，成本还可控。

## 相关

- [[shader-color-interpolation]] — cubic / quintic smoothstep 是插值类噪声的心脏
- [[worley-voronoi-noise]] — 细胞噪声的单独展开，包含 shader graph 节点代价
- [[layered-grid-noise]] — 不用哈希，靠黄金角旋转打破周期的 Xor 自家做法
- [[fractal-texturing]] — 把 fBm 思路从噪声迁移到纹理采样
- [[non-cryptographic-hash]] — sine hash 之外更靠谱的 GPU 哈希
- [[pcg3d-hash]] — 现代 GPU 上 Worley 推荐的哈希
- [[xor-shader-artist]]
- [[fragment-shader]]
- [[mipmap-generation-sampling]] —— 纹理路线的噪声离不开 LOD 和 bias 的配合

## Sources

- [[sources/xor-mini-noise]]
- [[sources/xor-mini-noise-2]]
- [[sources/xor-mini-noise-3]] —— Simplex noise、函数 vs 纹理权衡、tileable noise
