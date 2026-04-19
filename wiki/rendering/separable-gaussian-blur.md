---
tags: [rendering, shader, post-processing, blur, gaussian, unity]
date: 2026-04-14
sources: 3
---

# 可分离 Gaussian Blur（与 Box Blur）

Box Blur 和 Gaussian Blur 都是最常见的全屏模糊后处理，它们有一个共同的关键性质——**可分离（separable）**：一个 N×N 的 2D 卷积等价于先做一次 1×N 横向卷积、再做一次 N×1 竖向卷积。这把单像素的采样数从 N² 降到 2N，对 N=15 来说意味着 225 次 → 30 次，几乎是一个数量级的加速。现代渲染里绝大多数"高质量"的模糊都是基于这条性质 + 额外优化（下采样金字塔、double-Kawase、线性插值采样）实现的。

## Box Blur：最简单的可分离核

Box Blur 的卷积核是全 1 矩阵，数学上可以写成：

```
B(x, y) = 1   for all |x|, |y| ≤ r
```

这显然可以拆成 `B₁(x) = 1` 和 `B₁(y) = 1` 的外积。因此两遍 1D 模糊就能得到正确结果：

```hlsl
// Pass 1 - horizontal
for (int x = -r; x <= r; ++x)
    sum += tex2D(_MainTex, i.uv + float2(_MainTex_TexelSize.x * x, 0));
sum /= _KernelSize;

// Pass 2 - vertical
for (int y = -r; y <= r; ++y)
    sum += tex2D(_MainTex, i.uv + float2(0, _MainTex_TexelSize.y * y));
sum /= _KernelSize;
```

Box Blur 的缺点是在锐边（物体轮廓）上产生可见的"阶梯条纹"——均匀权重让边缘像素被突然包含/剔除。Gaussian 的中心重、边缘轻的权重曲线能把这个问题几乎消除。

## Gaussian：用正态分布做权重

一维 Gaussian 函数：

```
G(x) = 1/(σ√(2π)) · exp(-x² / (2σ²))
```

σ（标准差）控制"山"的宽窄——σ 越大模糊半径越大、权重越平。由于 2D Gaussian 可以写成 `G(x,y) = G(x) · G(y)`，**Gaussian 同样可分离**，所以只需要实现 1D 版本并跑两次 pass。关键细节：

- 因为权重不再是 1，循环里必须同时累加 `kernelSum`，最后用它（而不是 `_KernelSize`）归一化。否则图像会整体变暗——Gaussian 的离散采样和不会精确等于 1。
- kernel 半径 `r` 的选择要匹配 σ——通常 `r ≈ 3σ` 足够，因为 Gaussian 尾巴在 3σ 之外的能量已经小于 0.3%。
- 在 fragment shader 里直接调用 `exp` 和 `sqrt` 每像素算 Gaussian 是可以的，但更高效的做法是在 CPU 侧预计算权重数组上传到 shader。

## Unity 多 Pass 的正确写法

这里有一个新手最容易踩的坑：**在同一个 shader 里声明两个 Pass 并不会自动把 Pass 1 的结果作为 Pass 2 的输入**——`_MainTex` 仍然是原始相机输出。必须在 C# 侧显式管理中间 RT：

```csharp
protected override void OnRenderImage(RenderTexture src, RenderTexture dst) {
    var tmp = RenderTexture.GetTemporary(src.width, src.height, 0, src.format);
    Graphics.Blit(src, tmp, material, 0);   // pass index 0 = horizontal
    Graphics.Blit(tmp, dst, material, 1);   // pass index 1 = vertical
    RenderTexture.ReleaseTemporary(tmp);
}
```

`Graphics.Blit` 的第四个参数指定 pass 索引。临时 RT 一定要 `ReleaseTemporary` 归还池子，否则每帧泄漏。

## 空间变化 σ：Super Mario Odyssey 的边缘模糊

一个有意思的扩展是让 σ 随**到屏幕中心的距离**变化——中心清晰、边缘逐渐糊掉，模拟 SMO 的"注意力聚焦"镜头后处理：

```hlsl
float getSigma(float2 uv) {
    float d = length((uv - 0.5) * 2.0);     // 0 at center, ~1.4 at corner
    return min(d * 1.25, 1.0);
}
// in loop:
float sigma = getSigma(i.uv) * _Spread;
float w = gaussian(x, sigma);
```

因为 σ 是每像素变化的，循环内部必须重新算 Gaussian 权重——CPU 预计算在这里就行不通了，但也只是每像素多几十次 `exp`，对现代 GPU 是可接受的代价。

## 可分离之外：现代做法

直接写"可分离 Gaussian 两遍 pass"是合格的教学版本，但工业界的 Bloom / DOF / Motion Blur 通常会在 Separable Gaussian 之上再叠加两层优化：

- **金字塔下采样**——先把 `_MainTex` 下采样到 1/2、1/4、1/8 分辨率，在低分辨率上跑小半径 Gaussian，再上采样回来。有效半径乘以分辨率比例。
- **Linear sampling trick**——用双线性插值把两个相邻 texel 的采样合并成一次读取，让 N 次采样降到 N/2 次。

这些手段都是基于"Box/Gaussian 是可分离的"这个最根本的前提。

## Xor 的 Blur Philosophy：dos and avoids

[[xor-shader-artist|Xor]] 在 [[sources/xor-mini-blur-philosophy|Blur Philosophy]] 里把多年踩坑沉淀成两张清单。**Dos**：separable 多 pass、kernel 预计算、启用 linear filter（让双线性插值两 texel 合采一次）、在 **linear color space（gamma 正确）** 做 blur、能下采样就下采样——最好按 2 的幂次跳。**Avoids**：尽量少样本（texture fetch 在移动端贵得离谱）、谨慎处理边界（sprite padding 或 wrap mode 二选一）、surface 不要堆——两张 [[ping-pong-surfaces]] 通常够用、循环里不要调 `sin` / `cos`（把昂贵算式提到 loop 外）。他自己坦言之所以写这篇免费科普，是因为早期那版被 ShaderToy/Godot/Construct 到处抄的 Gaussian shader 有错误，必须公开更正——这是开源贡献者的一种补救礼仪。文章最后推了 **[Dual-Kawase blur](https://github.com/XorDev/Dual-Kawase/wiki)**：下采样金字塔 + 极少采样的对数级扩展，半径翻倍只加 2 pass，是当前社区公认最合算的实时大半径模糊方案之一。

## 反面教材：Metal 教程里的不可分离 Gaussian

[[metal-compute-image-filter|Warren Moore 的 image processing 教程]]在 compute kernel 里直接写了双重循环 `for(j) for(i)`——没有用可分离性，每像素 `N²` 次采样。他的 kernel 还把预计算的 2D 权重矩阵做成一张 `MTLPixelFormatR32Float` 的查找纹理传进去，kernel 里 `weights.read(kernelIndex).rrrr` 取出标量权重。灵活性很好（改半径只需重建权重纹理），但性能代价直接——`N=15` 时就是 225 次 texture fetch/像素，和 2×N=30 的可分离版本差了一个数量级。教程的定位是入门而非性能演示，但对读者是个提醒：可分离这条优化路径之所以存在，正是因为「显式写双重循环」的实现是真的会慢。

## 相关
- [[image-convolution-kernel]]
- [[unity-image-effect-basics]]
- [[sampler-filter-wrap-modes]]
- [[unity-grabpass-blur]]
- [[image-effect-colour-transform]]
- [[depth-texture-silhouette]]
- [[shader-combination-strategies]] — 什么时候不走可分离而塞进单 pass
- [[image-resampling-filters]]
- [[laplacian-pyramid]]
- [[mipmap-generation-sampling]] —— `texture2D` 的 bias 参数可作为 blur 的廉价替代或加强剂
- [[ping-pong-surfaces]]
- [[radial-blur-postfx]] —— 空间变化 kernel 强度的分离高斯 blur 变体
- [[sources/danielilett-snapshot-pro-radial-blur]] —— Pro 版 Radial Blur 的两参数实现

## Sources

- [[sources/danielilett-image-effects-blurring]]
- [[sources/metalbyexample-image-processing]]
- [[sources/xor-mini-blur-philosophy]] —— Xor 的 box → Gaussian → kernel → separable 演进，附 dos/avoids 清单和 Dual-Kawase 推荐
