1. **Day 2 · Application Stage — CPU 在干什么** 昨天我们聊了管线的整体架构：一个受瓶颈支配的并行系统。今天深入第一个阶段——Application Stage，也就是 CPU 在渲染管线里扮演的角色。 这个阶段经常被低估。很多人觉得渲染 = GPU 的事，CPU 只是「把数据丢给 GPU」。错了。CPU 是渲染管线的**决策者**，它决定了 GPU 要做多少无效功。 ---
    
    ## CPU 的绝对控制权
    
    RTR4 原文说得非常明确：
    
    > "The developer has full control over what happens in the application stage, since it usually executes on the CPU. Therefore, the developer can entirely determine the implementation and can later modify it in order to improve performance."
    
    注意「full control」和「entirely determine」这两个词。在整条渲染管线里，Application Stage 是**唯一**一个你有完全控制权的阶段。Geometry Processing、Rasterization、Pixel Processing 都在 GPU 上，你只能通过 Shader 和状态设置间接控制。但 CPU 端的逻辑——你说了算。 这意味着什么？**如果你的渲染性能有问题，最高杠杆的优化往往在 CPU 端，而不是 GPU 端。** 因为 CPU 决定了哪些东西要渲染、以什么方式渲染。一个好的裁剪算法可以让 GPU 的工作量减少 90%，这比你在 Shader 里省几条指令有效得多。
    
2. RTR4 也点明了这一点：
    
    > "Changes here can also affect the performance of subsequent stages. For example, an application stage algorithm or setting could decrease the number of triangles to be rendered."
    
    ---
    
    ## CPU 的核心任务：减少 GPU 的无效工作
    
    很多初级开发者对 CPU 端渲染工作的认知是「准备顶点数据，设置 Uniform，调用 Draw Call」。这些确实是 CPU 在做的事，但这是**执行层面**的理解。从**设计层面**看，CPU 的核心任务是： **让 GPU 只做必要的工作。** RTR4 列举了 CPU 端的典型工作：碰撞检测、加速算法、动画、物理模拟。注意这些工作的共同特征——它们都在回答一个问题：**这一帧需要渲染什么？**
    
    > "One process commonly implemented in this stage is collision detection... Acceleration algorithms, such as particular culling algorithms (Chapter 19), are also implemented here, along with whatever else the rest of the pipeline cannot handle."
    
    这里的「acceleration algorithms」和「culling algorithms」就是关键词。裁剪（Culling）不是一个「高级优化技巧」——它是 CPU 的**本分**。如果你不做裁剪，你就是在让 GPU 渲染大量屏幕外的物体，这是纯粹的浪费。
    
3. ### 裁剪的层级关系
    
    实际项目中，裁剪通常是一个多层过滤器：
    
    1. **视锥裁剪（Frustum Culling）**：最基础的。不在相机视锥内的物体直接跳过。成本极低（几个点积运算），收益巨大。每个引擎都有，Unity 的 Camera 组件自动做这件事。
    
    2. **遮挡剔除（Occlusion Culling）**：被其他物体完全遮挡的物体跳过。成本比视锥裁剪高（需要维护遮挡信息），但在室内场景和城市场景中收益极大。Unity 有烘焙式的 Occlusion Culling，UE 有 HZB（Hierarchical Z-Buffer）方案。
    
    3. **距离剔除（Distance Culling / LOD）**：太远的物体要么不渲染，要么用低精度版本。这不仅减少三角形数量，还减少了材质和纹理的复杂度。
    
    4. **贡献剔除（Contribution Culling）**：屏幕上只占几个像素的物体，渲染它的性价比太低，直接跳过。这是最容易被忽视的一层。
    
    在一个典型的开放世界游戏中，场景可能有上百万个物体，但经过这四层过滤后，每帧实际提交给 GPU 渲染的可能只有几千个。**这就是 CPU 的价值。** ---
    
    ## Draw Call 的真实成本
    
4. 说到 CPU 提交渲染命令，就不得不谈 Draw Call。这可能是游戏开发中被误解最多的概念之一。 很多人以为 Draw Call 的成本在 GPU 端——毕竟是 GPU 在「画」。但实际上，**Draw Call 的主要成本在 CPU 端**。 每次 Draw Call，CPU 需要：
    
    - 验证当前的渲染状态是否合法
    - 将渲染命令翻译成 GPU 能理解的指令
    - 如果渲染状态发生了变化（换了 Shader、换了纹理、换了混合模式），还需要执行**状态切换**
    
    状态切换才是真正的杀手。GPU 是一个状态机，每次状态变化都需要刷新管线。在 OpenGL/DX11 时代，驱动需要在每次 Draw Call 时验证整个渲染状态——即使你什么都没改，驱动也不知道你没改，它必须检查。 这就是为什么：
    
    - **合批（Batching）** 如此重要——减少 Draw Call 数量
    - **排序（Sorting）** 如此重要——把相同状态的物体放在一起渲染，减少状态切换
    - **Instancing** 如此重要——一个 Draw Call 渲染多个相同网格的实例
    
    在 Unity 中，SRP Batcher 就是通过将材质属性放入持久化的 Constant Buffer 来避免重复的状态设置。Dynamic Batching 和 Static Batching 则是通过合并网格来减少 Draw Call 数量。GPU Instancing 则是用一个 Draw Call 加一个 Instance Buffer 来渲染多个实例。
    
5. **品味判断：** 在移动端，Draw Call 的成本比 PC 端更高。移动端的 GPU 驱动通常更薄（为了省电），状态验证的开销占比更大。经验值——中低端 Android 设备上，Draw Call 超过 200-300 就开始明显影响帧率，而 PC 上可能要到 2000-3000 才会成为问题。 ---
    
    ## Compute Shader：模糊的边界
    
    RTR4 提到了一个重要的变化：
    
    > "Some application work can be performed by the GPU, using a separate mode called a compute shader. This mode treats the GPU as a highly parallel general processor, ignoring its special functionality meant specifically for rendering graphics."
    
    Compute Shader 打破了「CPU 做逻辑、GPU 做渲染」的传统分工。很多原本属于 Application Stage 的工作——粒子模拟、骨骼动画、裁剪计算——现在可以搬到 GPU 上用 Compute Shader 执行。 为什么要搬？因为这些工作的共同特征是**大规模数据并行**。一万个粒子的物理模拟，每个粒子的计算是独立的——这正是 GPU 擅长的工作模式。 但 Compute Shader 不是万能的。它适合的场景有明确的特征：
    
    - 数据量大（几千到几百万个工作单元）
    - 每个工作单元的计算相对简单
    
6. - 工作单元之间没有或很少有依赖关系
    
    如果你的工作是「遍历一棵复杂的空间分割树来做裁剪」，涉及大量分支和不规则的内存访问，那 CPU 可能仍然是更好的选择。这回到了 Day 1 说的：GPU 是数据并行架构，分支和随机访存是它的弱点。
    
    ### 2026 年的现状
    
    Compute Shader 在现代引擎中的使用越来越深入：
    
    - **GPU-Driven Rendering Pipeline**：UE5 的 Nanite 就是典型——裁剪、LOD 选择、集群拆分全在 GPU 上完成
    - **GPU Culling**：Hi-Z Occlusion Culling 在 GPU 上执行，比 CPU 回读深度缓冲快得多
    - **GPU Skinning**：大量角色的骨骼动画在 GPU 上计算
    - **GPU Particles**：现代粒子系统几乎都在 GPU 上运行
    
    这个趋势的本质是：**把 CPU 从「逐物体处理」中解放出来，让它做更高层次的决策。** CPU 不再需要遍历每一个物体来决定是否渲染——它只需要设置好裁剪参数，让 GPU 自己做批量裁剪。 ---
    
    ## 移动端视角：CPU 比你想的更珍贵
    
7. 在 PC/主机开发中，CPU 和 GPU 通常有相对均衡的性能比。但在移动端，情况完全不同。 移动端的 CPU 面临三重压力：
    
    1. **功耗限制**：手机 CPU 的持续性能远低于峰值性能（热降频）
    2. **竞争者多**：游戏逻辑、物理、AI、网络、操作系统服务都在争抢 CPU 时间
    3. **驱动开销大**：OpenGL ES 的驱动在 CPU 端做了大量工作（状态验证、Shader 编译等）
    
    这就是为什么 Vulkan 和 Metal 在移动端的价值比 PC 端更大。它们的核心卖点不是「GPU 更快」——GPU 硬件没变——而是「**CPU 开销更低**」。预编译的 Pipeline State Object、显式的资源管理、多线程命令录制，这些都是在给 CPU 减负。 在 Unity 移动端项目中，太多次性能问题的根源不是 Shader 太复杂，而是 CPU 端被 Draw Call、骨骼动画、物理模拟拖垮。Profiler 的 CPU 时间远超 GPU 时间。**先优化 CPU，再优化 GPU**——这应该是移动端性能优化的第一原则。 ---
    
    ## Application Stage 的输出
    
    RTR4 指出了 Application Stage 最重要的输出：
    
8. > "At the end of the application stage, the geometry to be rendered is fed to the geometry processing stage. These are the rendering primitives, i.e., points, lines, and triangles, that might eventually end up on the screen. This is the most important task of the application stage."
    
    「might eventually end up on the screen」——注意「might」这个词。CPU 提交的图元只是**候选者**，后续的 Geometry Processing 阶段还会做裁剪。但 CPU 端的裁剪越精确，GPU 端需要处理的无效图元就越少。 这也是为什么 CPU 端的空间数据结构（BVH、Octree、BSP Tree 等）如此重要。它们不是「高级话题」——它们是 Application Stage 做好本分工作的必备工具。没有空间数据结构的场景管理，就像没有索引的数据库——可以工作，但在规模上完全不可接受。 ---
    
    > **CPU 不是渲染管线的搬运工，而是决策者。它的每一个决策——渲染什么、不渲染什么、以什么方式渲染——都在塑造 GPU 的工作负载。优化渲染性能，从优化决策开始。**