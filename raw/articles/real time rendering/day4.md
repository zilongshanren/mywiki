1. **Day 4 · 光栅化 — 从三角形到像素的信息折叠** --- 有一种东西在图形学里被描述得非常克制，以至于你第一次读到它时会觉得「就这？」——
    
    > "Rasterization, also called scan conversion, is thus the conversion from two-dimensional vertices in screen space—each with a z-value and various shading information associated with each vertex—into pixels on the screen."
    
    "从顶点到像素的转换。"就这一句话，背后却藏着整个渲染管线里最根本的哲学问题：**连续世界和离散世界之间的鸿沟**。 这是一个永远无法完美弥合的鸿沟。信息必然丢失。唯一的问题是：你怎么控制丢失的方式和程度？ 理解这一点，你就理解了为什么抗锯齿是一个永恒的问题，为什么 MSAA 和 TAA 的设计思路如此不同，为什么「一个像素」的概念在图形学里比直觉中更复杂。 ---
    
    ## 为什么是三角形？
    
2. 在进入光栅化的机制之前，有一个问题值得多停一秒：**为什么渲染管线的基本图元是三角形，而不是四边形，不是圆，不是任意多边形？** RTR4 并没有在 Ch2 里直接回答这个问题，但答案散布在整本书里，可以被拼出来： **三角形总是平面的。** 三点确定一个平面，不多不少。四边形就不一定了——四个顶点完全可以不共面，这会让着色和插值产生歧义。三角形没有这个问题。 **三角形总是凸的。** 任何凸多边形的内部判断都很简单（点在所有边的同侧），但非凸多边形的内部判断就麻烦得多。三角形是最简单的凸多边形，边数最少，判断最快。 **三角形的插值有唯一解。** 给定三个顶点的属性（颜色、UV、法线），三角形内任意一点的插值结果是唯一确定的——重心坐标（barycentric coordinates）给出了唯一的线性插值。四边形或者更复杂的形状就没有这么干净的解析解。 **三角形易于硬件化。** 固定的三顶点结构让 Triangle Setup 阶段可以做成纯硬件（fixed-function silicon）——RTR4 明确指出这一点。确定性的输入格式 = 确定性的硬件电路设计。 所以三角形不是历史偶然，它是在「简单」和「足够通用」之间找到的最优点。任何更复杂的图元最终都会被拆分成三角形。这是一个 API 层面的设计决定，但背后有扎实的数学支撑。 ---
    
    ## 两个阶段：Triangle Setup 和 Triangle Traversal
    
3. RTR4 把光栅化拆成了两个功能子阶段。
    
    ### Triangle Setup（三角形设置）
    
    这个阶段几乎不被讨论，但它是 Triangle Traversal 的前提。
    
    > "In this stage the differentials, edge equations, and other data for the triangle are computed... Fixed-function hardware is used for this task."
    
    "Edge equations（边方程）"——这是关键词。对于屏幕空间中的一个三角形，我们可以把它的三条边表示成线方程：
    
    `f_i(x, y) = a_i * x + b_i * y + c_i = 0`
    
    三条边方程把二维平面分成了若干区域。一个点在三角形内，当且仅当它在所有三条边方程的同一侧（对于逆时针三角形，就是所有三个方程值都 >= 0）。 这就是后续 Triangle Traversal 用来判断「一个像素是否在三角形内」的核心工具。
    
4. "Differentials（微分）"——这用来计算重心坐标在 x 和 y 方向的变化率，使得 Triangle Traversal 在扫描像素时可以增量式地计算插值，而不是每个像素重新做一次完整的重心坐标计算。这是一个经典的空间换时间的技巧：预计算微分，然后在 Traversal 时用加法替代乘法。
    
5. Triangle Setup 是纯硬件，开发者不可编程也不可配置（除了图元类型）。它就在那里，默默完成自己的工作。
    
    ### Triangle Traversal（三角形遍历）
    
    这是光栅化的主体。
    
    > "Here is where each pixel that has its center (or a sample) covered by the triangle is checked and a fragment generated for the part of the pixel that overlaps the triangle."
    
    注意原文用的词是「fragment（片段）」而不是「pixel（像素）」。这个区分很重要：**一个像素可能对应多个 fragment**（比如 MSAA 时每个像素有多个采样点，每个采样点是一个 fragment），**一个 fragment 最终也不一定变成像素**（深度测试可能把它丢弃）。 Triangle Traversal 做的事情，概念上很简单：
    
    `对屏幕上的每个候选像素:     判断它的采样点是否在三角形内     如果在:`
    
6.         `用重心坐标插值顶点属性（位置、UV、法线、颜色...）         生成一个 fragment，送往 Pixel Shader`
    
    但"扫描哪些候选像素"这个问题的答案影响性能：你不可能把整个屏幕的每个像素都检查一遍。实际上是先算出三角形的 AABB（最小轴对齐包围盒），只扫描 AABB 内的像素。这已经是很大的优化。 还有更精细的优化：**Tile-Based 遍历**。现代 GPU 会把屏幕分成小方块（tile），先判断三角形和 tile 的关系，完全在外的 tile 直接跳过，完全在内的 tile 所有像素直接接受，边界上的 tile 才需要逐像素检查。这个三级判断大幅减少了内部一致性检查的次数。 ---
    
    ## 采样：光栅化的本质哲学
    
    RTR4 描述了三种不同的"insideness（内部性）"判断策略： **Point Sampling（点采样）：** 最简单。以像素中心为采样点，中心在三角形内 = 像素被覆盖。
    
7. 这是最基础的方式，也是走样（aliasing）的直接来源——因为连续的三角形边界被离散的像素网格强行量化了，边界处就出现了锯齿。 **Supersampling / Multisampling（超采样/多采样）：** 每个像素用多个采样点。 SSAA（Super Sampling AA）：整个像素有多个完整的着色计算，每个采样点都跑一次 Fragment Shader，然后平均。质量最好，成本最高。 MSAA（Multi-Sample AA）：每个像素仍然只跑一次 Fragment Shader，但对覆盖判断做多次采样。如果一个三角形覆盖了像素的部分采样点，着色结果会按覆盖比例混合。成本比 SSAA 低得多，但只解决几何边缘的走样，不解决着色内部的高频噪声（比如细密纹理的摩尔纹）。 **Conservative Rasterization（保守光栅化）：** 只要三角形部分覆盖了像素，该像素就被覆盖。 这个模式不是为了抗锯齿——它是为了需要「不遗漏任何几何」的算法设计的。比如：Voxelization（体素化）、Ray Tracing 的 BVH 构建、一些阴影算法。标准光栅化会"漏掉"只覆盖边角的像素，保守光栅化则不会。代价是会产生更多 fragment，但对于某些算法这是必要的。 这三种策略的存在，揭示了一个关键认知：**采样策略是一个设计参数，不是一个"正确答案"**。什么场景用什么采样策略，取决于你需要解决什么问题。 ---
    
    ## 「像素不是小方块」
    
8. 这是图形学里一个著名的认知纠正，来自 Alvy Ray Smith 的一篇经典文章（他是 Pixar 的联合创始人之一）：**A Pixel Is Not A Little Square**。 RTR4 在描述像素坐标时给出了一个细节：
    
9. > "Given a horizontal array of pixels and using Cartesian coordinates, the left edge of the leftmost pixel is 0.0 in floating point coordinates... The center of this pixel is at 0.5."
    
    像素中心在 0.5，不是 0。这意味着像素是一个**点样本（point sample）**，代表的是该位置的一个采样值，不是一个有面积的方块。 这个区别在实践中非常重要： 当你做纹理采样时，你采样的是某个精确 UV 坐标的值，不是一个区域的平均。 当你在 Shader 里做 `ddx(uv)` / `ddy(uv)` 时，你在计算相邻像素样本之间的差异。 当你理解"像素是点样本"时，很多图形学操作的行为就有了直觉上的解释：为什么需要过滤（filtering）？因为你在用离散的点样本去重建/逼近一个连续的信号。为什么 Mipmap 有效？因为它预计算了不同采样率下的信号降频版本。 "像素是小方块"这个错误认知导致了很多混乱——包括为什么图像缩放后会有品质问题，为什么纹理采样需要各种过滤模式。一旦你把像素理解为点样本，这些问题的答案就变得清晰了。 ---
    
    ## 透视正确插值
    
10. 这是 Triangle Traversal 里一个经常被忽略但实际很关键的步骤：
    
    > "It is also here that perspective-correct interpolation over the triangles is performed."
    
    问题是这样的：我们在屏幕空间（2D）里对顶点属性做线性插值，但顶点属性（UV、法线等）是在**模型空间或世界空间（3D）**里有意义的。 透视投影是一个非线性变换（因为有透视除法 w 的存在）。这意味着，在屏幕空间里均匀分布的像素，在 3D 空间里是**不均匀分布**的——远处的像素对应 3D 中更大的区域。 如果你直接在屏幕空间对 UV 做线性插值，结果会是错误的——纹理会看起来像被"推挤"向远端。这在透视角度很大的时候（比如看一个倾斜的平面）特别明显。 透视正确插值通过在插值前除以 w（然后最后再乘回来）来修正这个问题。公式是：
    
    `// 错误做法（屏幕空间线性插值） uv = lerp(uv0, uv1, t)`
    
11. `// 正确做法（透视正确插值） uv = lerp(uv0/w0, uv1/w1, t) / lerp(1/w0, 1/w1, t)`
    
    现代 GPU 在 Triangle Traversal 阶段自动做这个修正（这就是"perspective-correct interpolation"）。你在 Shader 里直接拿到的插值结果已经是透视正确的，不需要手动处理。 但你需要知道它的存在，因为在某些非标准的插值场景（比如自己写光线追踪，或者在 Compute Shader 里做手动插值）你需要自己实现它。 **一个实用的 Unity/HLSL 细节：** 如果你在 Vertex Shader 输出一个用 `nointerp` 修饰的变量，它会做屏幕空间的线性插值（不透视正确）。默认的插值（无修饰）是透视正确的。这两种插值在什么时候各自有用？`nointerp` 通常用于需要在屏幕空间做线性操作的场景，比如某些后处理效果。 ---
    
    ## 光栅化的同步点身份
    
    RTR4 有一句话揭示了光栅化在整条管线里的特殊地位：
    
12. > "Rasterization can also be thought of as a synchronization point between geometry processing and pixel processing, since it is here that triangles are formed from three vertices and eventually sent down to pixel processing."
    
    **同步点（synchronization point）**——这个词很精准。
    
13. 几何处理阶段的工作单元是**顶点**（vertex）。光栅化之前，GPU 在处理一个个离散的顶点，它们还没有形成完整的图元。 光栅化之后，工作单元变成了**片段**（fragment）。片段是像素级别的，已经知道自己在哪个三角形里，已经插值好了所有顶点属性。 光栅化就是把"顶点流"变成"片段流"的那个转化点。这个变化在数量上可能是戏剧性的：一个三角形（3个顶点）可能产生成千上万个片段（如果三角形很大）；也可能产生 0 个片段（如果三角形太小，被背面剔除，或者完全在视锥外）。 这种数量的不确定性是为什么 GPU 不能简单地为每个三角形预分配固定的计算资源——需要动态调度。 ---
    
    ## 移动端的光栅化：TBDR 的本质
    
    现在谈移动端，因为光栅化在 TBDR（Tile-Based Deferred Rendering）架构下的行为和桌面端 IMR（Immediate Mode Rendering）有根本性的差异。
    
    ### IMR 的工作方式（桌面端：NVIDIA, AMD）
    
    立即渲染模式：每个三角形提交后立即光栅化，立即执行 Fragment Shader，立即写入帧缓冲（如果通过深度测试）。
    
14. `Triangle 1 → 光栅化 → Fragment Shader → 写帧缓冲 Triangle 2 → 光栅化 → Fragment Shader → 写帧缓冲 ...（顺序执行）`
    
    帧缓冲在显存（VRAM）里。每次读写帧缓冲 = 访问显存 = 带宽消耗。
    
    ### TBDR 的工作方式（移动端：ARM Mali, Apple GPU, Qualcomm Adreno）
    
    分块延迟渲染：屏幕被分成小块（tile，通常 16×16 或 32×32 像素）。 **第一遍（Geometry Pass / Binning Pass）：** 光栅化所有三角形，但不执行 Fragment Shader。只记录每个 tile 里有哪些三角形。 **第二遍（Fragment Pass）：** 每次处理一个 tile，把这个 tile 的帧缓冲数据加载到**片上内存（On-Chip Memory）**，执行所有属于这个 tile 的 fragment，完成后把结果写回主存。
    
15. `所有三角形 → 几何处理 → Binning（分配到 tile）                          ↓ Tile 0: 加载片上内存 → Fragment Shader → 深度测试 → 写主存 Tile 1: 加载片上内存 → Fragment Shader → 深度测试 → 写主存 ...`
    
    ### 为什么这样做有意义？
    
    移动端的核心资源不是算力，而是**带宽和功耗**。每次访问主存（LPDDR）的耗电量远高于使用片上内存（SRAM）。 TBDR 的关键优化：**同一个 tile 内的所有光栅化操作都在片上完成，中间结果从不写到主存**。深度测试、着色、混合——全部在片上内存里发生。只有最终的结果才写回主存。 这对带宽的节省是巨大的。一个典型的移动 GPU 的片上内存带宽是几百 GB/s，而主存带宽只有几十 GB/s。只要能把工作尽量限制在片上，性能就会好很多。
    
    ### TBDR 对光栅化的具体影响
    
16. **Early-Z 在 TBDR 上天然更强：** 因为同一个 tile 内的所有三角形都会被一起处理，GPU 可以在 Fragment Shader 执行前做 Tile-level 的深度测试。被遮挡的 fragment 在着色之前就被丢弃，节省了大量 ALU 计算。这就是为什么 TBDR 在有大量 overdraw 的场景下也能保持较低的功耗。 **MSAA 在 TBDR 上几乎免费：** MSAA 需要存储每个像素的多个采样点。在 IMR 架构下，这意味着更多的帧缓冲读写（更多带宽消耗）。但在 TBDR 上，多个采样点都在片上内存里——每个 tile 处理时的内存是足够的，MSAA 的额外采样点完全在片上完成，不会增加主存带宽。这就是为什么移动端 MSAA 4x 是很合理的默认选择。
    
17. **RT 切换是移动端的杀手：** 如果你在渲染过程中切换 Render Target（比如 Deferred Rendering 的 G-Buffer），TBDR 必须把当前 tile 的结果 flush 到主存，然后重新加载下一个 RT 的数据。每次切换都是一次主存访问。这就是为什么在移动端，Deferred Rendering 的优势会被大量 RT 切换的带宽代价所抵消。
    
    `// 移动端需要尽量避免的模式： // Pass 1: 渲染到 G-Buffer (4 个 RT) // Pass 2: 读 G-Buffer → 渲染到 Light Buffer   // Pass 3: 读 Light Buffer → 最终合成 // 每个 Pass 切换 = 主存 flush + reload  // 移动端友好的模式： // 使用 Framebuffer Fetch (iOS Metal) / Subpass (Vulkan) // 允许下一个 Pass 直接读取片上的上一个 Pass 结果 // 不需要写回主存再读取`
    
    ARM Mali 架构白皮书里有一句话很直接：
    
    > "The single most important performance tip for Mali GPUs: Avoid unnecessary render target switches."
    
18. 这不是一个优化建议，这是架构特性决定的设计约束。 ---
    
    ## 走样：信息丢失的具体形式
    
    光栅化是采样，采样就有走样。RTR4 后面的章节（Ch5）会深入讨论抗锯齿，但在这里理解走样的根源很重要。 **走样（Aliasing）的信号处理解释：** 三角形的边缘在数学上是无限精细的（它是一条线）。但光栅化用有限分辨率的像素网格来"采样"这个无限精细的边缘——采样率不足以表达原始信号。 根据奈奎斯特定理：要准确采样一个信号，采样率必须至少是信号最高频率的两倍。三角形边缘在理论上有无限高的频率（一个从 0 到 1 的阶跃函数，包含所有频率成分）。任何有限采样率都不够。 结果是：高频信息以错误的低频形式出现——锯齿。 **抗走样方案的共同本质：**
    
19. 所有 AA 方法本质上做的是同一件事——**在采样之前对信号做低通滤波**，去掉超过采样率能表达的高频成分，然后再采样。
    
    - SSAA：提高采样率（治本，但贵）
    - MSAA：对几何边缘的覆盖测试用更高采样率（只治几何锯齿）
    - FXAA：采样后做后处理模糊（最便宜，但会损失细节）
    - TAA：在时间维度上累积多帧的抖动采样（随时间均匀分布的超采样）
    - DLSS/FSR：学习型上采样，从低分辨率重建高分辨率（信号处理 + AI 先验知识）
    
    理解了走样的信号处理本质，你就不会再为"为什么 TAA 会有鬼影"感到困惑——因为 TAA 利用历史帧做时间平均，历史帧里物体不在当前位置，就会产生拖尾。这不是 TAA 的 Bug，这是时间平均本身的代价。 ---
    
    ## 一个值得思考的设计决定
    
    RTR4 在 Ch2.4 开头就讲了像素坐标的约定：
    
    > "While all APIs have pixel location values that increase going from left to right, the location of zero for the top and bottom edges is inconsistent in some cases between OpenGL and DirectX."
    
20. OpenGL：Y 轴向上（左下角是 (0,0)） DirectX：Y 轴向下（左上角是 (0,0)） 这个不一致性是历史遗留问题。OpenGL 跟从数学坐标系惯例（笛卡尔坐标），DirectX 跟从图像/屏幕坐标惯例（从左上角开始）。 这个差异影响：
    
    - Render Texture 的 Y 轴翻转
    - UV 坐标的 V 分量在不同 API 间需要翻转（`v_directx = 1 - v_opengl`）
    - Depth Buffer 的方向约定
    
21. Unity 在不同平台上透明地处理了大部分这类差异，但你在写需要跨平台的着色器或者处理 RenderTexture 时，仍然需要了解这个差异的存在。 ---
    
    ## 实战：光栅化的可见性
    
    最后谈一个实际问题：**三角形的哪面被光栅化？** 默认情况下，GPU 会剔除背面三角形（Back-face Culling）——如果三角形的顶点在屏幕空间是顺时针排列的（右手系中），说明它是背面朝着你的，不会被光栅化。 这个判断发生在光栅化阶段之前，但严格说是 Triangle Setup 的一部分。剔除背面是"免费"的优化——不需要额外工作，只是不生成那些三角形的 fragment。
    
    `// Unity Shader 里控制剔除： Cull Back   // 剔除背面（默认） Cull Front  // 剔除正面（用于某些特效，比如渲染体积阴影）`
    
22. `Cull Off    // 不剔除（双面材质，树叶等）`
    
    `Cull Off` 会让每个三角形生成两倍的 fragment（因为正反两面都会被光栅化），成本也近似翻倍。这对于大面积的树叶、草地场景要特别注意。 ---
    
    ## 代码：手动实现光栅化
    
    理解原理最好的方式是实现它。一个简化的软件光栅化（用于理解，不用于实际渲染）：
    
    `// 用边函数判断点是否在三角形内 float EdgeFunction(Vector2 a, Vector2 b, Vector2 p) {`
    
23.     `return (p.x - a.x) * (b.y - a.y) - (p.y - a.y) * (b.x - a.x); }  // 光栅化一个三角形到像素缓冲 void RasterizeTriangle(     Vector2 v0, Vector2 v1, Vector2 v2,     Color c0, Color c1, Color c2,     Color[] framebuffer, int width, int height) {     // 计算 AABB     int minX = Mathf.Max(0, Mathf.FloorToInt(Mathf.Min(v0.x, v1.x, v2.x)));     int maxX = Mathf.Min(width-1, Mathf.CeilToInt(Mathf.Max(v0.x, v1.x, v2.x)));     int minY = Mathf.Max(0, Mathf.FloorToInt(Mathf.Min(v0.y, v1.y, v2.y)));     int maxY = Mathf.Min(height-1, Mathf.CeilToInt(Mathf.Max(v0.y, v1.y, v2.y)));`
    
24.     `float area = EdgeFunction(v0, v1, v2);      for (int y = minY; y <= maxY; y++)     {         for (int x = minX; x <= maxX; x++)         {             // 像素中心             Vector2 p = new Vector2(x + 0.5f, y + 0.5f);              // 计算重心坐标             float w0 = EdgeFunction(v1, v2, p);             float w1 = EdgeFunction(v2, v0, p);             float w2 = EdgeFunction(v0, v1, p);              // 判断是否在三角形内（考虑边界处理）`
    
25.             `if (w0 >= 0 && w1 >= 0 && w2 >= 0)             {                 // 归一化重心坐标                 w0 /= area; w1 /= area; w2 /= area;                  // 插值颜色`
    
26. Color color = c0 * w0 + c1 * w1 + c2 * w2; framebuffer[y * width + x] = color; } } } }
    
    ``注意几个细节： 1. **像素中心在 `x + 0.5f`** — 对应 RTR4 的 `c = d + 0.5` 2. **AABB 限制遍历范围** — 实际 GPU 更高效，但原理相同 3. **边函数值的符号** — 决定三角形正面/背面，也决定内/外 4. **重心坐标归一化** — 用于插值  这是理解光栅化机制的最直接方式。真正的 GPU 光栅化加了很多优化（增量计算、Tile 加速、硬件并行），但核心逻辑就是这样。``
    
27. ``---  > 光栅化是一个必然会丢失信息的过程。好的图形程序员不是试图阻止信息丢失，而是控制丢失的方式——让肉眼察觉不到，或者让察觉到的方式是你预期的。  ---  ## 🎯 今日测验  **Q1 (概念)：** 三角形是渲染管线的基本图元，而不是四边形或多边形。用自己的话解释至少三个理由，说明为什么三角形是更好的选择。  **Q2 (应用)：** 你在做一个移动端（Mali GPU）的植被系统，树叶使用双面材质（`Cull Off`）。发现性能下降明显。除了换成单面材质，还有哪些方案可以在保持双面效果的同时降低光栅化成本？请从 TBDR 架构的角度分析。  **Q3 (品味)：** 有人说"MSAA 在移动端已经足够，不需要 TAA"。你同意吗？从 MSAA 和 TAA 各自解决的问题类型、移动端 TBDR 对 MSAA 的特殊友好性、以及 TAA 引入的 Ghosting 问题这三个角度，给出你的分析和判断。  > 回复本条消息即可作答，你的回答会影响明天的推送深度和方向。``