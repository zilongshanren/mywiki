1. **Day 1 · Architecture — 渲染管线是什么** 渲染管线不是一条流水线。它是一个受瓶颈支配的并行系统。 这是 RTR4 第二章开篇最重要的认知。书里用了一个三明治工厂的比喻：三个工人，一个切面包（20秒），一个加肉（30秒），一个加配料（20秒）。你可能以为总产能是每 20 秒一个三明治，但实际上只能每 30 秒一个——因为加肉的人是瓶颈，其他两个人做得再快也在等他。
    
    > "The pipeline stages execute in parallel, but they are stalled until the slowest stage has finished its task. For example, say the meat addition stage becomes more involved, taking thirty seconds. Now the best rate that can be achieved is two sandwiches a minute. For this particular pipeline, the meat stage is the bottleneck, since it determines the speed of the entire production."
    
    渲染管线的四个阶段也是一样。Application（CPU）、Geometry Processing（GPU）、Rasterization（GPU）、Pixel Processing（GPU）并行执行，但整条管线的帧率取决于最慢的那个阶段。这意味着：**优化不是让每个阶段都更快，而是找到那个最慢的阶段，只优化它。** 优化非瓶颈阶段对帧率的贡献是零。 这四个阶段各自在回答一个问题。RTR4 的原文把这三个问题说得很精确：
    
    > "The geometry processing stage computes what is to be drawn, how it should be drawn, and where it should be drawn."
    
2. 加上 Application 和 Pixel Processing，完整的分工是：
    
    - **Application（CPU）：** 决定「渲染什么」。哪些物体可见？用什么材质？提交多少 Draw Call？CPU 在这里是决策者，它的决策质量直接决定 GPU 有多少无效工作量。一个糟糕的 CPU 阶段会把大量被遮挡的物体也提交给 GPU——GPU 最终会通过深度测试丢弃它们，但已经浪费了带宽和计算。
    - **Geometry Processing（GPU）：** 决定「在哪里渲染」。3D 空间的顶点通过 Model → View → Projection 变换链最终映射到 2D 屏幕坐标。之后裁剪掉视锥外的部分。
    - **Rasterization（GPU）：** 把三角形变成像素。输入是三个顶点，输出是一堆被三角形覆盖的像素位置。这是从连续几何体到离散像素的桥梁。
    - **Pixel Processing（GPU）：** 决定「每个像素什么颜色」。片段着色器在这里执行，深度测试、模板测试、Alpha 混合也在这里完成。
    
    **Functional Stage vs Implementation：一个容易被忽略的区分** RTR4 特别强调了一点：
    
    > "We differentiate between the functional stages shown here and the structure of their implementation. A functional stage has a certain task to perform but does not specify the way that task is executed in the pipeline. A given implementation may combine two functional stages into one unit or execute using programmable cores, while it divides another, more time-consuming, functional stage into several hardware units."
    
    这不是学术上的咬文嚼字，这个区分有真实的工程意义。同一个「功能阶段」在不同硬件上的实现可以完全不同。举个最关键的例子： 在桌面 GPU（NVIDIA/AMD）上，管线是 Immediate Mode Rendering（IMR）：三角形提交后立即逐像素渲染，直接读写显存。Rasterization 和 Pixel Processing 是真正意义上的前后阶段。
    
3. 在移动 GPU（ARM Mali、Qualcomm Adreno、Apple GPU）上，管线是 Tile-Based Deferred Rendering（TBDR）：GPU 先收集一帧内所有三角形的几何信息，按 Tile（通常 16×16 或 32×32 像素）分组，然后在 GPU 片上内存（On-Chip Memory）中完成一个 Tile 的所有渲染，最后一次性写回显存。在 TBDR 下，Rasterization 和 Pixel Processing 不是简单的前后关系——它们在同一个 Tile 内交织执行。 这个架构差异导致了两个完全不同的优化世界：
    
    - IMR 上，Overdraw（同一像素被多次着色）的成本主要是片段着色器的重复计算。
    - TBDR 上，Overdraw 的成本更低（因为 Hidden Surface Removal 可以在着色前剔除被遮挡的像素），但切换渲染目标极其昂贵（需要把当前 Tile 的数据全部刷回显存，清空片上内存，再加载新的 Tile 数据）。
    
    后面 Day 7 会专门深入 TBDR，但现在你需要知道的是：**当有人说「渲染管线是这样工作的」，你要追问一句——在哪种 GPU 上？** 功能描述是通用的，但实现是特定的。 **瓶颈判断法：10 秒定位问题** 知道了管线是瓶颈支配的，下一步是快速判断瓶颈在哪里。有一个简单到令人惊讶的方法： 把渲染分辨率降到一半。 如果帧率明显提升（比如从 40fps 跳到 60fps），说明瓶颈在 GPU 的像素处理阶段（fill-rate limited）——因为分辨率减半意味着需要处理的像素数减少到 1/4。 如果帧率几乎没变化，说明瓶颈在 CPU（CPU bound）或 GPU 的几何阶段——因为像素数量的减少没有帮助，说明管线被更早的阶段卡住了。
    
4. 这个测试 10 秒钟就能做完，但它能帮你避免最常见的优化错误：在 CPU bound 的项目上花三天优化 Shader 复杂度，或者在 fill-rate limited 的项目上花时间减少 Draw Call。两者都是在优化非瓶颈阶段，对帧率的提升为零。 Unity 中怎么做：直接在 Game 窗口右键降低分辨率，或者在代码中设置 `Screen.SetResolution(width/2, height/2, true)`。在 Xcode 或 Snapdragon Profiler 中，也可以通过降低 viewport 来测试。 ---
    
    > 渲染管线的四个阶段不是四个步骤，是四个并行的工人。帧率取决于最慢的那个人。找到他，优化他，忽略其他人。这是性能优化的第一原则。
    
    ---