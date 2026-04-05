**Day 6 · Through the Pipeline — 一帧的完整生命**

---

我们今天做一件事：**跟一个三角形走完整条管线**。

不是那种教科书式的「首先进入顶点着色器，然后……」，而是真的去感受它——感受数据在每个阶段的形态变化，感受信息在流动中不断被抛弃，感受最终那个像素出现在屏幕上时经历了什么。RTR4 在 Ch2.6 用了一个很好的比喻：跟着一个华夫饼机器的 CAD 模型走完整条管线。我们今天做同样的事，但会挖得更深。

---

> *"Points, lines, and triangles are the rendering primitives from which a model or an object is built. Imagine that the application is an interactive computer aided design (CAD) application, and that the user is examining a design for a waffle maker. Here we will follow this model through the entire graphics rendering pipeline, consisting of the four major stages: application, geometry, rasterization, and pixel processing."*
> — RTR4 Ch2.6

这段话藏着一个极其重要的认知框架：**渲染管线是一条流水线，不是一棵树**。数据从一端进入，在四个大阶段里被依次处理，最后变成屏幕上的颜色。这个线性结构决定了它的性能特征：**整条管线的速度等于最慢那个阶段的速度**。

很多工程师在优化时犯的第一个错误，就是不知道自己的瓶颈在哪。你在优化 Vertex Shader，但瓶颈在带宽；你在削减 DrawCall，但瓶颈在 Fragment Shader 的 overdraw。找到瓶颈，才能做有效的优化。

---

## 第一阶段：Application Stage — CPU 上发生的一切

> *"The application stage must translate the mouse move to a corresponding rotation matrix, then see to it that this matrix is properly applied to the lid when it is rendered."*
> — RTR4 Ch2.6

这段话说的是 Application Stage 的本质：**把人类意图翻译成 GPU 能理解的数据**。

输入处理、物理模拟、动画更新、AI 逻辑、场景管理、Culling、DrawCall 提交——这些都发生在 Application Stage，都在 CPU 上。

### 数据规模的直觉

一帧里到底有多少数据？

**顶点数**：一个中等复杂度角色，大概 10,000 到 50,000 个顶点。一个现代 AAA 游戏场景，可见物体加在一起，大概 **500,000 到 5,000,000 个顶点**。移动端游戏通常控制在 **100,000 到 500,000 个顶点**。这是每帧都要走一遍 Vertex Shader 的数量。

**三角形数**：顶点数和三角形数的比例大概是 1:2（Index Buffer 让三角形共享顶点），所以三角形数大概是顶点数的两倍。一帧 100 万到 1000 万个三角形，是正常水平。

**像素数**：1080p 屏幕有 1920×1080 = **207 万像素**。2K 是 518 万，4K 是 829 万。但真正被 Fragment Shader 处理的像素数，因为 overdraw，可能是这个数字的 3 到 10 倍。

### DrawCall 的本质代价

DrawCall 本身不贵。贵的是**状态切换（State Change）**。每次 DrawCall 之前，GPU 需要知道用什么 Shader、绑定什么 Texture、用什么混合模式……这些 State 的设置和验证，在传统 OpenGL ES 驱动里代价极高。一帧 2000 个 DrawCall 可能没问题，但如果每个都带来大量 State Change，CPU 就会成为瓶颈。

这是 **SRP Batcher** 存在的根本原因。Unity 的 SRP Batcher 不是真正意义上的「合批」——它不减少 DrawCall 数量，它做的是**把不同物体的 Material Property（矩阵、颜色等）统一打包进 CBUFFER，这样多个 DrawCall 可以共享同一套 Shader State，消除 State Change 的代价**。

GPU-Instancing 才是真正减少 DrawCall 数量的技术。两者解决的是不同层面的问题。

---

## 第二阶段：Geometry Processing — 几何数据的变换之旅

> *"In the geometry stage the vertices and normals of the object are transformed with this matrix, putting the object into view space. Then shading or other calculations at the vertices may be computed. Projection is then performed using a separate user-supplied projection matrix, transforming the object into a unit cube's space that represents what the eye sees. All primitives outside the cube are discarded. All primitives intersecting this unit cube are clipped against the cube."*
> — RTR4 Ch2.6

### 坐标系变换链

一个顶点从 CPU 提交到屏幕，经历：

**Model Space → World Space**：Model Transform Matrix（Translation、Rotation、Scale）

**World Space → View Space**：View Matrix（相机矩阵的逆）

**View Space → Clip Space**：Projection Matrix。这步做了一件重要事：**把深度值从线性空间变换到非线性 NDC 空间**。

透视投影丢失了什么？View Space 里深度是线性的：相机 1m 和 2m 处深度差均匀。但经过透视除法后，靠近 Near Plane 的区域深度分辨率极高，远处极低。这就是 **Z-fighting 的根源**：两个距离相机很远的平面，NDC 深度值几乎相同，Z-Buffer 无法区分，于是闪烁。

解决方案之一是 **Reversed-Z Buffer**：把深度值翻转，让 1.0 对应近裁剪面，0.0 对应远裁剪面。因为浮点数在接近 0 时精度更高，远处物体的深度精度反而提升了。Unity 在 D3D11/12 和 Metal 上默认启用 Reversed-Z。

### 裁剪：信息的第一次大规模丢弃

Clip Stage：完全在视锥体外的三角形直接丢弃，跨越视锥体边界的三角形需要被裁剪——生成新顶点。这意味着 Clip Stage 可能会**生成新的顶点和三角形**，而不只是删除。

---

## 第三阶段：Rasterization — 三角形变成像素

> *"All the primitives that survive clipping in the previous stage are then rasterized, which means that all pixels that are inside a primitive are found and sent further down the pipeline to pixel processing."*
> — RTR4 Ch2.6

### 覆盖测试与插值

光栅化的 **Coverage Test**：对每个像素，判断它是否在三角形内部。通常在像素中心点做（MSAA 则在多个采样点做）。

判断点是否在三角形内部用**重心坐标（Barycentric Coordinates）**。重心坐标不只用于覆盖测试，还用于**属性插值**：顶点上的颜色、UV、法线，都通过重心坐标插值到每个像素。

关键细节：**透视校正插值（Perspective-Correct Interpolation）**。在屏幕空间直接线性插值顶点属性是不正确的——透视投影拉伸了屏幕空间的距离关系。正确做法是在 **1/w 空间**里线性插值，再除以 1/w 还原。现代 GPU 硬件自动做这个。

### 锯齿：光栅化的信息损失

一个三角形的顶点坐标可以是 (0.3142, 1.7788) 这样的精确浮点数，但光栅化后，只有像素中心在三角形内的像素会被生成，其余子像素信息全部丢失。这就是**锯齿（Aliasing）**的根源。

所有抗锯齿技术本质上都在做同一件事：**试图恢复或近似那些被丢弃的子像素信息**。

- **MSAA**：每个像素内放置多个采样点，分别做覆盖测试，再平均。直接但代价大——Coverage Buffer 和 Depth Buffer 存储量乘以采样倍数，在移动端是沉重的带宽代价。
- **TAA**：利用多帧历史信息，用时间换空间。代价是 Ghost（鬼影）和 Blur，需要 Motion Vector Buffer。
- **DLSS/FSR**：用 AI 或空间算法从低分辨率上采样，质量越来越接近原生分辨率。

---

## 第四阶段：Pixel Processing — 像素的最终命运

> *"The goal here is to compute the color of each pixel of each visible primitive."*
> — RTR4 Ch2.6

### 带宽 vs ALU：现代渲染的核心认知

这是今天最重要的论点。

现代 GPU 有几千到几万个 Shader Core，理论算力以 TFLOPS 衡量。PC 端 RTX 4090 有 82.6 TFLOPS FP32 算力，内存带宽 1008 GB/s。

移动端呢？Apple A17 Pro GPU 约 2.15 TFLOPS，Adreno 740 约 1.0-1.8 TFLOPS，内存带宽只有 **40-60 GB/s**。比 RTX 4090 低了整整一个数量级。

60fps 每帧带宽预算：

- PC 端 RTX 4090：1008/60 ≈ **16.8 GB per frame**
- 移动端 Adreno 730：40/60 ≈ **667 MB per frame**

1440p 渲染，PBR 着色，每像素采样 5-10 张纹理，加上 Shadow Map、IBL……一帧的实际内存访问量很容易超过 500 MB 到 1 GB。移动端的带宽预算几乎要被压榨到极限。

**结论：移动端渲染瓶颈，90% 的情况是带宽，不是 ALU。**

这改变了所有的优化决策：

1. **减少纹理采样次数**比优化 Shader 里的 `sin`/`cos` 更重要
2. **降低 Render Scale**（< 1.0 再 Upscale）比算法优化效果更直接
3. **纹理压缩**（ASTC on mobile）不只是省内存，更是省带宽
4. **Mipmap** 通过让远处物体采样更小的 Mip Level，降低缓存 miss 率——本质是带宽优化
5. **Tile-Based Rendering** 是移动 GPU 的架构核心，正是为了解决带宽问题

### Tile-Based Rendering：移动 GPU 的架构智慧

PC 端 GPU（NVIDIA、AMD）通常是 **Immediate Mode Rendering（IMR）**：每个 DrawCall 立即执行，把结果写入 DRAM 里的 Framebuffer。Depth Buffer 和 Framebuffer 的读写都经过完整带宽链路。

移动端 GPU（Mali、Adreno、PowerVR、Apple）几乎全部采用 **Tile-Based Architecture**：

1. **Binning Pass**：把所有三角形的位置信息分配到屏幕各个 Tile（通常 16×16 或 32×32 像素）
2. **逐 Tile 处理**：把一个 Tile 需要的所有数据加载进 GPU 内部的 **On-Chip Tile Buffer**，在片上完成所有渲染计算
3. 最后只做一次 Tile Buffer → DRAM Framebuffer 的写入

On-Chip Memory 的带宽是 DRAM 的 **100 到 200 倍**。整个渲染过程只需要：开始时从 DRAM 读一次几何数据、结束时写一次颜色结果。

**这就是 Tile-Based 的核心：用片上缓存取代 DRAM 读写，在带宽受限环境下实现高效渲染。**

在 Unity 移动端开发里，这意味着：

- **永远不要在中途 ReadBack Framebuffer**：这会强迫 GPU 把 Tile Buffer 写出到 DRAM 再读回，打破片上处理的优势
- **显式声明不需要 Store 的 Buffer**：如果最终不需要 Depth Buffer 内容，告诉 GPU 不要 Store，否则会白白写回 DRAM
- **`loadAction` 和 `storeAction` 在移动端有实质性性能影响**：URP 的 `RenderPassDescriptor` 里这两个参数，在 Tile-Based GPU 上不是摆设

---

## Output Merger：高度可配置，但不完全可编程

Fragment Shader 计算出颜色后，还有最后一关：

- **Depth Test**：比较当前 Fragment 的深度值和 Depth Buffer 里的值
- **Stencil Test**：根据 Stencil Buffer 做条件测试
- **Blending**：把 Fragment 颜色和 Framebuffer 里的颜色按混合方程混合

RTR4 对此的描述是「highly configurable, but not fully programmable」——你可以通过 API 参数选择 Blend 方程、Depth Test 比较函数，但不能在这里运行任意着色器代码。原因是硬件效率：允许完全可编程会导致各种 RAW（Read-After-Write）Hazard，在并行 GPU 上极难处理。

这也是**半透明渲染是持久难题**的原因：Z-Buffer 算法只对不透明物体有效（O(n)，任意顺序）。半透明物体需要从后往前排序（Painter's Algorithm），或使用 OIT（Order-Independent Transparency）——两者都有代价。

---

## Double Buffering：让人类看不到正在渲染的画面

> *"To avoid allowing the human viewer to see the primitives as they are being rasterized and sent to the screen, double buffering is used. This means that the rendering of a scene takes place off screen, in a back buffer. Once the scene has been rendered in the back buffer, the contents of the back buffer are swapped with the contents of the front buffer. The swapping often occurs during vertical retrace, a time when it is safe to do so."*
> — RTR4 Ch2.6

Double Buffering 的逻辑极其简洁：把渲染结果写到 Back Buffer，等 VSync 时与 Front Buffer 对调。显示器永远看到已经完整渲染好的画面，不会出现撕裂（Tearing）。

Triple Buffering 是扩展：三个 Buffer 轮转，允许 GPU 在一个 Buffer 显示、一个等待呈现、一个正在渲染，在 VSync 限制下最大化 GPU 利用率。

---

## 固定管线的终结

> *"This pipeline resulted from decades of API and graphics hardware evolution... The last example of a major fixed-function machine is Nintendo's Wii, introduced in 2006. Programmable GPUs make it possible to determine exactly what operations are applied in various sub-stages throughout the pipeline."*
> — RTR4 Ch2.6

**Nintendo Wii 是固定功能管线最后的大规模商用产品。2006 年。**

Wii 之前，GPU 每个阶段能做什么是硬件固定的，开发者只能调参数，没有 Shader 可写。光照模型固定是 Blinn-Phong，纹理混合方式固定几种，自定义空间极其有限。

可编程 GPU 带来了革命——不只改变了游戏画面上限，还改变了 GPU 的整个应用场景：从纯粹的图形处理器，演变成今天的 GPGPU，支撑了深度学习的爆炸式发展。

---

## Unity 实战：把管线知识变成工程直觉

**DrawCall 优化，你真正在优化什么？**

很多人说「减少 DrawCall」，但实际上应该分两个层面：

1. **减少 CPU State Setup 代价**：SRP Batcher，通过 CBUFFER 共享 Shader State
2. **减少实际 DrawCall 数量**：GPU Instancing（相同 Mesh + 相同 Material），Static Batching（合并静态物体 Mesh）

**Profile 优先，猜测无效**。Unity Profiler + Frame Debugger 可以告诉你实际的瓶颈在哪：是 CPU DrawCall 提交，是 Vertex Shader ALU，是 Fragment Shader 的纹理采样，还是 Tile-Based GPU 的带宽。不同设备上同一个场景的瓶颈可能完全不同——高端 PC 可能是 Shadow Map 的 Fragment Shader，同一场景在 Android 中端机可能是带宽。

**Overdraw 是移动端的隐形杀手**。UI 层叠、半透明粒子效果、大面积全屏 Post-Processing——这些都会让实际 Fragment 处理量远超屏幕像素数。在 Android GPU Inspector 或 Xcode Metal HUD 里，Overdraw 的可视化往往让人吃惊。

**Shader 优化的正确优先级（移动端）**：
1. 减少纹理采样次数（最高优先级）
2. 使用低精度变量（`half` 而不是 `float`，移动端有硬件加速）
3. 避免条件分支（GPU SIMD 执行，分支导致 warp divergence）
4. 减少数学复杂度（最低优先级，但不是没有价值）

---

## 品味判断

通读 RTR4 Ch2.6 之后，你会发现一件有意思的事：**这一章的例子（华夫饼机器）是刻意选择的一个「普通」例子，而不是游戏里的「酷炫」效果**。

这个选择很有品味。因为管线的原理是普适的——无论渲染的是华夫饼机器还是龙，是一个三角形还是一百万个三角形，数据流经管线的基本结构是相同的。用最简单的例子把原理讲清楚，比用复杂的例子展示神奇效果更重要。

管线知识的真正价值不在于「我知道管线有哪几个阶段」——这个任何人背一遍都能说出来。真正的价值在于：**当你看到一个帧率问题，你脑子里能自动地把问题定位到管线的某个阶段，然后用对应的工具去验证**。这是一种工程直觉，只有在「知识 + 实践」反复迭代之后才能形成。

RTR4 的这章是基础，但它是所有后续章节的骨架。每一个后续章节（Shadow、PBR、Post-Processing、Ray Tracing）都是在这个骨架上展开的。

---

> 一帧不是画出来的，是流出来的——每个阶段都在丢弃信息、压缩信息、变换信息，最终那个像素是整条流水线协作的结果。

---

## 🎯 今日测验

**Q1（概念）：** 「带宽瓶颈比 ALU 瓶颈更常见」这个结论，对于移动端 GPU 来说为什么成立？请从移动 GPU 的硬件参数出发，解释带宽预算如何被消耗掉。

**Q2（应用）：** 假设你在做一个移动端 Unity 游戏，Profile 发现 GPU 时间主要耗在 Fragment Shader 上，但降低 Shader 复杂度没有显著改善。根据今天的内容，你接下来会检查哪几个方向？按优先级排序。

**Q3（品味）：** SRP Batcher 和 GPU Instancing 都被叫做「合批优化」，但它们解决的是完全不同的问题。请解释这两种技术各自针对的是管线的哪个瓶颈，在什么情况下应该用哪个？

> 回复本条消息即可作答，你的回答会影响明天的推送深度和方向。
