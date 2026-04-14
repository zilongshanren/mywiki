---
tags: [渲染, 噪声, shader, 程序纹理]
date: 2026-04-14
sources: 1
---

# 分层网格噪声（Layered Grid Chaos）

Xor 在 *Efficient Chaos* 里介绍的一种**廉价伪随机**方法：用一张均匀网格配几个「shift + scale + rotate」的变体层叠加，换一种「随机感」——既不是 hash noise，也不是 Worley noise，而是介于两者之间、在 3D 下几乎免费的星空/雨/粒子散布器。核心观察是：**随机性不必靠 hash，只需要打破周期性**。

## 为什么不用 Worley

Worley noise（cell noise，Voronoi 的亲戚）要在 N 维的 3×3×...×3 邻域里采点，复杂度是 `3^N`——2D 要 9 次，3D 要 27 次，4D 要 81 次。对于实时 shader，3D 以上就已经不划算了。Xor 的方法每层只算一次「到当前 cell 中心的距离」，加几层的代价和层数成线性，3D 下没有额外开销。

## 基础：单一网格 + cell-center 距离

先把坐标拆到单位 cell 里，算到 cell 中心的距离，用作点光源的衰减基：

```glsl
vec2 subcell = mod(coord, 2.0) - 1.0;   // 每个 cell 居中到 [-1,+1]
float len = length(subcell);
float att = max(1.0 - len, 0.0) / len;  // 圆形 cutoff + 1/r 衰减
```

单层当然太规则——看起来就像格子状星空。关键是怎么叠多层把格子隐藏掉。

## 三板斧：shift、scale、rotate

对第 `i` 层：

- **Shift**：`p += LAYER_SHIFT * i;` —— 每层平移一个非整数偏移，错开格子位置。
- **Scale**：`p /= 1.0 + LAYER_SCALE * i;` —— 每层放大一点点，让不同层的 cell 尺寸不同，避免所有层共用一个「周期」。
- **Rotate**：用黄金角（golden angle, ≈137.5°）对应的 `mat2` 旋转每层——**这是关键的无理数旋转**，保证任意有限层都不会回到对齐状态：

```glsl
// 黄金角 ≈ 2.39996 rad，对应 mat2：
coord *= mat2(0.22252093, -0.97492791,
              0.97492791,  0.22252093);
```

5 层左右基本看不出任何格子结构。黄金角在自然界里本身就是「最不容易落入重复的角度」（向日葵种子分布、松果的对数螺旋），拿来打破 shader 里的周期性非常合适。

## 保留与应用方向

如果 shader 需要「原始方向」（比如做视差、定向光照），直接旋转坐标会丢掉这个信息。更干净的做法是**把累积的旋转矩阵单独维护**：

```glsl
mat2 orient = mat2(1.0);
// loop:
orient *= gold;
vec2 p = coord * orient;  // 用的时候再乘
```

这样原始 `coord` 保持不变，每层有自己的旋转姿态可以查询。

## 打破剩余规律

肉眼 zoom-out 或者只开 1-2 层时，还会看到沿轴的条纹。Xor 给了两个便宜的修补：

- **正弦 warp**：`p += LAYER_WAVES * sin(p.yx);`——把坐标本身轻度扭曲，`amp=0.2` 就已经把条纹拍没了。
- **随机打洞**：在每层按一个廉价阈值丢掉一部分 cell，避免远看时「每层都铺满」的均质感。

这类技巧的共性：**代价小到可以叠很多次，而不是去追求单层完美**。

## 为什么能在 3D 免费扩展

因为整套流程从没做过邻域采样——每层只算「到本 cell 中心的距离」，cell 的定义天然适配任意维数。把 `vec2` 换成 `vec3`，`mod` 换成 3D mod，一切照旧。对比 Worley 的 `3^N`，这是量级差距。

## 用途

- **星空 / 密度粒子**：Xor 最初写这篇时就是给 GameMaker 的「让它下钱」特效用的。
- **雨、雪、落叶**：每层不同速度和方向，天生有视差层次感。
- **程序纹理背景、远景装饰**。
- **体积噪声**：3D 下仍然廉价，可以做简单的体积雾/云。

## 和其它噪声的关系

- **Value / Perlin / Simplex**：平滑场，不适合点状散布。
- **Worley**：点状散布的正确答案，但维数代价指数级。
- **Hash-based scatter**：每个 cell 用 hash 选子位置，也很便宜；Xor 的方法算是「不靠 hash，只靠几何变换打破周期」的另一条路。

本质上 Xor 展示的是一种**权衡品位**：不追求严格的统计随机性，只追求「眼睛看起来像随机」的视觉效果，同时把每一分成本花在刀刃上。

## 相关

- [[fragment-shader]]
- [[poisson-disk-sampling]] — 追求真正均匀散布的另一条路
- [[non-cryptographic-hash]] — hash 噪声的基础
- [[xor-shader-artist]]
- [[classic-shader-noise]] —— 经典噪声家族（value/Perlin/Worley/Voronoi/fBm）对照；fBm 和本页的黄金角旋转出发点相同：用非对称角打破 octave 对齐

## Sources

- [[sources/xor-efficient-chaos]]
