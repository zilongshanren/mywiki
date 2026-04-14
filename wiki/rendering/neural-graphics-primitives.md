---
tags: [渲染, 神经渲染, 机器学习, 压缩, NeRF]
date: 2026-04-14
sources: 1
---

# 神经图形原语（Neural Graphics Primitives）

**神经图形原语** 指用神经网络作为「任意信号」的隐式表示：图像、光场、距离场、体积都可以当成从坐标到值的函数 $f: \mathbb{R}^n \mapsto \mathbb{R}^m$，然后用一个小 MLP 去**故意过拟合**到这个函数上。这样网络本身就成了训练数据的一种有损压缩。

## 过拟合即压缩

普通机器学习把过拟合当敌人，要用正则化换泛化。图形场景反其道而行——既然我们只关心在训练集上重现信号，就让参数全部用来贴合数据。一张 512×512 的 RGB 图需要 768 KB 原始存储，但只要找得到一个参数数目更少、还能复现它的 MLP，这个 MLP 就是该图像的压缩表示。

## 激活函数决定细节上限

把一张图编码进 MLP 最早暴露出的问题是**高频细节**。Slater 在 Max 的实验里对比：

- **ReLU**：输出出现大量折线痕迹，高频差。
- **Sigmoid 输出层**：把 $(-\infty, +\infty)$ 映到 $[0,1]$，比裸 ReLU 明显改善，但仍有线状伪影。
- **Sinusoid**（SIREN 论文）：$f(x) = \sin(\omega_0 x)$ 的周期激活，理论上可微性质极好，但对权重初始化极端敏感——必须按 $\mathcal{U}(-\tfrac{1}{\omega_0}\sqrt{6/\text{fan\_in}}, \cdot)$ 初始化才能收敛。
- **Gaussian**：$f(x) = e^{-x^2/\sigma^2}$，对初始化鲁棒，在训练集外表现出「边缘 clamp 式」的合理外推，是工程友好选项。

## 输入编码比激活更关键

真正让效果起飞的不是激活函数，而是**输入编码**——在全连接层之前加一个固定或可学习的变换。

**位置编码 / Fourier Features**（NeRF 用法）：把标量 $x$ 展开成一列 $(\sin 2^0 x, \cos 2^0 x, \sin 2^1 x, \dots, \sin 2^L x)$ 的高频基。$L$ 越大，能表示的频率越高。两维图像一下子从 2 维输入变成 30 维，ReLU 网络质量出现戏剧性跃升。

**Instant NGP 多分辨率哈希编码**（SIGGRAPH 2022 best paper）：在 $L$ 层分辨率逐层加倍的网格上，把每个网格顶点哈希进一个固定大小的 $T$ 槽哈希表，每槽存 $F$ 个**可学习**参数。查询时对每层做双线性插值、全层拼接，再送进一个很小的 MLP（2 层、64 维就够）。哈希冲突不处理——训练过程会自动找到对冲突鲁棒的编码。其最大贡献是把训练时间从小时级压到秒级，且能 scale 到 gigapixel 图像、体积、SDF、radiance field。

## 应用面

编码的对象不必是图像。只要能写成「坐标 → 值」的函数：

- **Neural SDF**：把 [[raymarching-intro|sphere tracing]] 的 SDF 换成神经网络，用 marching cubes / dual contouring 回到网格；*Spelunking the Deep* 甚至给出神经 SDF 的解析 closest-point / 交点查询。
- **NeRF / 神经辐射场**：把 3D 位置 + 2D 方向映射到 RGB 辐射 + 体密度，再用体积光追生成新视角。
- **Neural Radiance Cache**：实时光追中在线训练一个小网络做辐射缓存，用它估计二次光线——不用递归 path tracing。

## 与经典表示的关系

神经表示是**隐式表示**的一种；图形史上一直在「三角网格 vs 体素 vs 隐式」之间摇摆，神经方法把隐式路线带回聚光灯下。也催生了[可微渲染](https://rgl.epfl.ch/publications)这一整个子领域——通过梯度下降反向恢复几何、材质与光源。

## 相关

- [[spherical-harmonics]] — 另一种「把信号展开成基函数」的古典手法
- [[needlets]] — 带局部性的球面基
- [[functions-as-vectors]] — 把函数视作无限维向量的统一视角
- [[raymarching-intro]]
- [[max-slater]]

## Sources

- [[sources/slater-neural-graphics-primitives]]
