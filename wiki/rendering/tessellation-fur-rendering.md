---
tags: [渲染, tessellation, fur, hair, d3d11, isoline, geometry-shader]
date: 2026-04-14
sources: 1
---

# 用 tessellation 的 isoline 域渲染毛发

**核心想法**：D3D11 的 tessellator 有一个很少被用到的 domain——**isoline**——输出的是 2D UV 点阵（最多 64 条线 × 每条 64 段）。把一个 UV 分量当作"第几根毛"、另一个当作"毛的第几段"，一个三角形就能在 GPU 上一次性生出 64 根 × 64 段的密集毛发，完全不需要 CPU 准备毛几何或者大张顶点缓冲。[[kostas-anagnostou|Kostas Anagnostou]] 2014 年写的一个原型工程展示了这条路径的全部细节。

## D3D11 tessellation 管线速回

tessellation 是 D3D11/OpenGL 4 引入的功能——用固定函数细分单元外加两个可编程 shader（hull / domain）在 GPU 上动态生成新几何。输入叫 **patch**，由若干 **control points** 定义（对三角形 patch 就是 3 个顶点）。管线是三段：

1. **Hull shader**（分两部分）：control-point 子 shader 逐控制点运行、能访问整个 patch；patch-constant 子 shader 逐 patch 运行，**输出 tessellation factors**——告诉 tessellator 每条外边和内部要切多细（三角形 patch 的 factor 是 4 个，外三内一；isoline 是 2 个：detail 和 density）。
2. **Tessellator**（固定函数）：在一个归一化的参考域（三角形 / 四边形 / isoline）上生成新点，输出它们的 UVW 坐标。**tessellator 不知道 patch 是什么**——它只在抽象域上切分。
3. **Domain shader**：接收 tessellator 输出的 UVW 和 hull 输出的控制点，**真正生成新顶点的世界坐标**——通常是 barycentric 插值，如果要做 displacement mapping，也在这里采高度图。

三种 domain：triangle、quad、**isoline**。前两种用来给现成 mesh 加细度（smooth / displacement），isoline 是一个看起来奇怪的选项——它在一个 2D 归一化域上沿一个方向切"线"，沿另一个方向切"段"。对 fur/hair/grass 这种"密集线性几何"来说它简直是量身定做。

## Fur 方案：domain shader 逐毛生长

把 isoline 的 U 分量当作"第几根毛"（0 到 63 之一），V 分量当作"这根毛的第几段"（0 到 63 之一）。每个三角形 patch 在 domain shader 里要做两件事：

1. **决定这根毛从哪里长出来**——用一张 CPU 预生成的**随机 barycentric 坐标表**，以 U 索引，查出三个权重 $(\lambda_1, \lambda_2, \lambda_3)$，乘原三角形的三个顶点得到毛根位置。在 shader 里现场算 hash 也行，但 Anagnostou 把它移到 CPU 是为了减少 shader 成本和带宽。
2. **决定这根毛的第 v 段的位置**——沿毛根所在表面的法线方向向上扩展 $v \cdot \text{segmentLength}$，得到当前段顶点。毛段数通常 4 就够短毛用。

tessellator 最多输出 64 × 64，意味着**一个基础三角形最多 64 根毛**。密度需求高时有两条路：（a）更细的 base mesh，（b）多 pass 渲染——Anagnostou 按三角形面积计算所需毛数，超过 64 就渲染更多 pass。hull shader 还做一件小事：对**整个 patch 背向相机**的情况把 tessellation factor 写成 0，tessellator 会直接跳过整个 patch——这是一种 per-patch 级 backface cull，但要对 silhouette 附近保守。

## Master strand + 插值：模拟只在主毛上做

短毛没有复杂模拟，直接上面的方案就够用。但**长毛 + 风 + 碰撞**需要对每根毛跑模拟，64×64×三角形数级别的毛上跑完整 simulation 不现实。解法：

- **每个三角形顶点保留一根"主毛"**（master strand）——存它的所有段顶点到一个 structured buffer。整个 mesh 的主毛总数 = 顶点数。
- **对主毛做 simulation**——CPU 或 compute shader，对每根主毛做长度约束、重力、风力、碰撞。三角形数量有限，成本可控。
- **domain shader 里插值**——渲染第 $i$ 根毛的第 $v$ 段时，用 barycentric 权重把三根主毛在段 $v$ 上的位置做加权平均。子毛"看起来像被模拟过"，因为它们是三条已被模拟主毛的线性组合。
- **主毛本身也要被渲染**——插值毛的权重覆盖了主毛本身，但主毛不能缺席，否则毛根点会露出。

Anagnostou 承认他的短毛 demo 里并不需要主毛插值——他写这一段是为了展示完整思路。

## 从"线"到"可见几何"：geometry shader 补宽度

tessellator 通过 isoline domain 产出的是**线 primitive**（line list / line strip）——没有厚度，光栅化出来就是一像素宽的细丝，远看极其破碎。要有体积感必须加宽度。

最便宜的做法是一个 geometry shader：每拿到一段线的两个端点，沿**垂直于视线 × 线方向**的轴扩展 $\pm w/2$，生成两个三角形组成的 quad。宽度 $w$ 可以是屏幕空间常数（每根毛 1–2 像素）或世界空间常数。这是 billboard 式展开——毛总是对着相机，风吹草动时整根毛也保持宽度。

## 细几何的走样噩梦

毛发 / 草这种"亚像素细线"是渲染里最难 AA 的几何之一。Anagnostou 的 demo 没有 geometric AA 时画面近乎不能看——动起来更差。解法分两层：

- **MSAA x4** 是下限，肉眼能看出明显提升；x8 边际收益很小，x4 是甜点。
- **远距离的毛断裂**用 Emil Persson 的 **Phone Wire AA**：把细线宽度 clamp 到一个最小值（防止它变得比一个像素还细），用"clamp 前后的差"做 alpha 淡出。Anagnostou 试了——**alpha sort 在 fur 密度下做不稳定**，alpha blending 路径放弃了，但**最小宽度 clamp** 这半个技巧留了下来，单靠它整体观感已经有明显改善。

屏幕空间 AA（FXAA / SMAA）对这种细几何帮不上大忙——它们识别不出亚像素断裂。几何 AA 必须在 rasterization 阶段发生。

## 数据流：只用一个顶点的 vertex buffer

这个方案有个欺骗性的细节：**vertex buffer 只存一个顶点**（占位、位置不重要），**index buffer 长度 = 三角形数**。真正的 mesh 数据、主毛数据、随机 barycentric 表**全部**通过 structured buffer 传进去，domain shader 靠 SV_PrimitiveID 和 tessellator 产出的 UV 去索引这些 buffer。这是一个有点"hack"的数据流设计：用最小的 vertex buffer 骗光栅化管线"以为有东西要渲染"，实际几何全部由 shader 生成。现代的做法会更激进——用 [[draw-procedural-gpu|DrawProcedural / multi-draw indirect]] 根本不走 vertex buffer，由 compute 生成 indirect args 再发绘制调用。2014 年的 D3D11 这条路还没普及，tessellator 就是当时最接近"GPU 生成几何"的方案。

## 草地迁移

把同一个 pipeline 换 shading 就能渲染草——isoline 产点方式、domain shader 的"毛根 + 段顶点"结构对草同样适用，只是 shading 里从 anisotropic rim 换成 diffuse 色带。这说明这个方案的骨架（"在归一化 2D 域上生成密集 1D 几何"）足够通用。现代工业做法里草更多走 [[deferred-grass-shader|alpha cutout + tessellation + geometry shader 的 triangle 路径]] 或 [[gpu-driven-grass-tiles|compute-driven indirect draw]]——前者属于同一时代的另一个解法，后者是 2020 年前后的 GPU-driven 范式。Anagnostou 的 isoline 方案在概念上更干净，但 geometry shader 在现代硬件上是一等性能坑，生产项目不会把 geometry shader 放到热路径上。

## 相关
- [[deferred-grass-shader]] — alpha cutout + triangle tessellation 的并行解法
- [[gpu-driven-grass-tiles]] — GPU-driven indirect draw 的现代替代方案
- [[draw-procedural-gpu]] — 去掉 vertex buffer 的更激进数据流
- [[fragment-shader]] — 对应毛段的 shading 阶段
- [[msaa-ssaa]] — 为什么细几何一定要几何 AA
- [[kostas-anagnostou]]
- [[hull-domain-tessellation-urp]] —— URP 下 hull/domain tessellation 的基础骨架：5 个 hull attribute、patch constant function、domain 里的 barycentric 插值、距离淡出公式

## Sources

- [[sources/interplay-fur-tessellation]]
