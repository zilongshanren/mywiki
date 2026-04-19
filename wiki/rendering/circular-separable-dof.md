---
tags: [渲染, 后处理, 景深, bokeh, 复数, 可分离卷积, frostbite]
date: 2026-04-19
sources: 1
---

# Circular Separable Depth of Field

Frostbite / EA 的 **Kleber Garcia** 提出的一种圆盘 bokeh [[gather-bokeh-dof|gather]] 算法，在 FIFA 17、NHS、Mass Effect Andromeda、Anthem、Need For Speed Heat 出货。核心卖点是把一个**看起来必须 O(N²) 的 2D 圆盘滤波**写成**两次 1D 可分离 pass**——代价是走一次**复数域（复数卷积 + 傅立叶变换）**的数学推导。

## 为什么"圆盘可分离"反直觉

可分离性的经典反例就是圆盘——圆盘不是外积，按行按列独立卷积合成出来的是方形或十字型。然而如果允许滤波核取**复数**值，通过恰当地选择核心实部 / 虚部权重并在合成阶段做一个线性组合，可以让两次 1D 复数卷积的**幅值响应逼近圆盘**。推导细节在 Garcia 的 [Frostbite 论文](https://github.com/kecho/CircularDofFilterGenerator/blob/master/circulardof.pdf)和 [Olli Niemitalo 的博客](http://yehar.com/blog/?p=1495)里；实践上你可以拿论文给的系数直接塞进 shader。

## 工程管线（Erfan Ahmadi 在 The Forge 里的复现）

- **1/2 分辨率** 上做所有计算（景深本来就只在脱焦区域有意义，半分就够）
- **Near / Far 分开**：两侧 CoC 的聚合逻辑不一样（near 要向相机外 bleed，far 不会）
- **可分离 1D 复数卷积**：一次水平、一次垂直
- **多 pass 合成**：两次卷积 pass + near/far 图层叠回去

Garcia 的论文刻意略过了"最后怎么合成 / 混合"这一段——Ahmadi 自述不得不**自己从头想这块**，这也是他复现时"读代码以外还得读纸上缺的部分"这类工程工作的代表。

## 和 scatter / 其它 gather 路线的关系

The Forge 的 Bokeh DoF UnitTest 并排实现了三种做法：

| 做法 | 数学/采样 | 成本模型 | 代表作 |
|---|---|---|---|
| [[circular-separable-dof|Circular Separable]] | 复数可分离卷积，1/2 分辨率 | O(N) × 两 pass | FIFA 17 系、Anthem、NFS Heat |
| Practical Gather-based ([GPU Zen](https://www.amazon.com/GPU-Zen-Advanced-Rendering-Techniques-ebook/dp/B0711SD1DW)) | 48 样本的圆盘采样，**不可分离** | O(48) × pass | — |
| Single-pass (Dennis Gustafsson, [tuxedo labs](http://blog.tuxedolabs.com/2018/05/04/bokeh-depth-of-field-in-single-pass.html)) | 全分辨率、一次采样 | 一 pass，但采样多得多 | — |

Ahmadi 复现的结论：**Circular Separable 和 Practical Gather-based 性能差不多（都 1/2 分辨率 + 分 near/far）**，而 Single-pass 虽然形式最简单，但强行在全分辨率一 pass 内算完，样本数和带宽都翻倍，反而最慢——它的价值在于**教学友好**和**不需要 MRT / 多分辨率管理**。

和 [[scatter-bokeh-dof|scatter bokeh]]（_The Witcher 2_ 路线）比，它属于 gather 家族，不可能做到任意精灵形状或物理色差；换来的是完全 GPU cache 友好、无 overdraw，适合**主流引擎的生产级 DoF**。

## 为什么很多 AAA 选它

- 1D 可分离，适合手动融合进 [[dual-kawase-blur|Dual Kawase]] / [[separable-gaussian-blur|可分离 Gaussian]] 这条管线的一贯风格
- 形状上是**圆盘**——对现代胶片审美 ok，比六边形自然（见 [[scatter-bokeh-dof]] 里 Wronski 对六边形 bokeh 的抱怨）
- 没有 scatter 的 alpha-blend 堆叠问题，无需定序、无需 premultiplied alpha 的 tricky 处理
- 可以跟 [[gather-bokeh-dof|gather-based]] 一样做 near-field fade / McIntosh 降噪

## 相关

- [[gather-bokeh-dof]]
- [[scatter-bokeh-dof]]
- [[thin-lens-model]]
- [[separable-gaussian-blur]]
- [[convolution-separability-blur]]
- [[the-forge-renderer]]
- [[people/erfan-ahmadi]]
- [[people/wolfgang-engel]]

## Sources

- [[sources/erfan-ahmadi-bokeh-dof-project]]
