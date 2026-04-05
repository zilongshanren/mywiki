1. **Day 1 · 计算机体系结构的任务与量化方法** _Computer Architecture: A Quantitative Approach — Chapter 1_ --- Hennessy 和 Patterson 写这本书的核心主张，其实就一句话：
    
    > _"Computer architecture is the science and art of selecting and interconnecting hardware components to create a computer that meets functional, performance, and cost goals."_
    
    注意这里用了 **science and art**。Science 是可量化的部分——性能公式、Amdahl定律、Cache命中率；Art 是 trade-off 判断——什么时候牺牲延迟换吞吐，什么时候加一级Cache反而得不偿失。这本书教的，正是把 art 变成 science 的方法论。
    
2.  **![🗂️](https://discord.com/assets/5ef2c51b36fb287d.svg) Flynn分类法：一个有用但已经过时的框架** Flynn 1966年提出的分类法，把计算机按「指令流 × 数据流」分成四类：
    
    `SISD — Single Instruction, Single Data   → 传统单核CPU SIMD — Single Instruction, Multiple Data → GPU、向量单元 MISD — Multiple Instruction, Single Data → 理论上存在，实际几乎没有 MIMD — Multiple Instruction, Multiple Data → 多核CPU、分布式系统`
    
    教科书会要你背这四个缩写。但真正值得思考的是：**为什么现代处理器越来越难被这个框架描述？** 现代 CPU 一个核心里同时有：
    
    - **超标量**（多条指令同时执行）→ 局部 MIMD
    - **SIMD 单元**（AVX-512 一次处理 16 个 float）→ SIMD
    - **乱序执行**（指令执行顺序与程序顺序不同）→ 打破了「单指令流」的假设
    
3. GPU 更是这个分类法的噩梦——它是 SIMT（Single Instruction, Multiple Threads），形式上像 SIMD，但每个线程有独立的程序计数器，可以走不同的分支路径（代价是 Warp 分歧性能损失）。 Flynn分类法的价值不在于精确描述现代硬件，而在于**提供了一个思考并行性的起点**：你的计算是数据并行的？还是任务并行的？这个问题直接影响你选 GPU 还是多核 CPU，选 SIMD intrinsics 还是多线程。
    
4.  **![⏱️](https://discord.com/assets/0936447be3e254dd.svg) 性能度量：你到底在优化什么？** 性能讨论最常见的错误，是混淆两个根本不同的目标： **响应时间（Response Time / Latency）**：完成一件事需要多长时间 **吞吐量（Throughput / Bandwidth）**：单位时间能完成多少件事
    
    > _"We will use the term performance to mean the inverse of the time to complete the task."_
    
    这句话看起来废话，但藏着一个陷阱：**性能这个词在不同语境下指的是不同的东西**。 举个游戏引擎的例子：
    
    - 玩家感受到的「卡顿」= Latency 问题（单帧渲染时间过长）
    - 服务器能承载多少同时在线玩家 = Throughput 问题
    
    优化 Throughput 的常见手段是**流水线化**和**批处理**——把多个任务拆成阶段，让每个阶段同时处理不同任务。但流水线化会增加单个任务的 Latency。
    
5. 这就是为什么 CPU 的超标量流水线深度一直是个 trade-off：更深的流水线 → 更高的时钟频率（Throughput↑）→ 但分支预测失败的代价更大（Latency↑）。Intel 的 Pentium 4（Prescott）把流水线做到 31 级，结果单线程性能反而不如 Pentium M（13级流水线）。 **实践判断**：优化之前先问自己——用户感知的瓶颈是 Latency 还是 Throughput？大多数游戏是 Latency-sensitive，大多数数据处理是 Throughput-sensitive。搞错了方向，优化再多也是白费。
    
6.  **![📐](https://discord.com/assets/0dbf3c5612419c55.svg) Amdahl定律：并行化的天花板** 这是整本书最重要的定律，没有之一。
    
    `Speedup = 1 / ((1 - p) + p/n)  p = 可并行化的部分比例 n = 并行处理器数量`
    
    推导很简单：
    
    - 假设原来总时间 = 1
    - 不可并行部分耗时 = (1-p)，无论加多少核都不变
    - 可并行部分耗时 = p/n，用 n 个核加速
    
    当 n → ∞ 时：Speedup → 1/(1-p)
    
7. **这就是反直觉的地方**：即使你有无限多个核，加速比也是有上界的。 如果 95% 的代码可以并行（p=0.95），无限核心的理论加速上限是 **20倍**。 如果只有 90% 可以并行，上限是 **10倍**。
    
    > _"Make the common case fast."_ — Amdahl 定律的另一种表达
    
    这句话 Hennessy & Patterson 在书里反复强调。它的含义是：**优化瓶颈，而不是优化已经快的部分**。一个函数占总时间 1%，你把它优化到 0，对整体性能的提升 < 1%。
    
8. **Amdahl定律在现代硬件上的启示** 现代多核CPU面临的困境正是 Amdahl定律的活教材： Intel 从双核到四核到八核，单线程性能提升越来越小。原因是：
    
    1. 大量软件的串行部分（OS调用、锁争用、I/O等待）无法并行化
    2. 随着核心增多，Cache一致性协议的开销本身成为串行瓶颈
    
    这也是为什么游戏引擎的多线程化如此困难——渲染提交、物理模拟、AI逻辑之间存在大量依赖，真正能并行的部分远比想象的少。 Unity 的 DOTS（Data-Oriented Technology Stack）本质上是在用数据布局的方式**提高 p 的值**——把原本串行的游戏逻辑重新设计成数据并行的形式，让 Amdahl 定律的分母不再是瓶颈。
    
9.  **![🔢](https://discord.com/assets/81224497b397e84f.svg) CPU性能公式：三个旋钮**
    
    `CPU Time = Instruction Count (IC) × CPI × Clock Cycle Time          = IC × CPI / Clock Rate`
    
    三个维度，三种优化策略，三方之间存在根本性的 trade-off： **Instruction Count（指令数）** 由算法、编程语言、编译器、ISA 共同决定。
    
    - RISC 指令集（RISC-V、ARM）：单条指令功能简单，IC 往往比 CISC 多
    - CISC 指令集（x86）：单条指令可以完成复杂操作，IC 少，但解码复杂
    
    **CPI（每指令周期数）** 由微架构决定：流水线深度、乱序执行能力、Cache命中率。
    
    - 理想流水线的 CPI = 1
    
10. - 现实中 Cache miss、分支预测失败、数据冒险都会增加 CPI
    - 超标量处理器可以实现 CPI < 1（IPC > 1，每周期执行多条指令）
    
    **Clock Cycle Time（时钟周期时间）** 由半导体工艺和微架构共同决定。
    
    - 更高时钟频率 → 每个时钟周期的工作量必须更少 → 流水线更深 → CPI 可能变差
    - 这是 Pentium 4 的失败之道
    
11. **三者的 Trade-off 矩阵**
    
    `优化目标          影响维度      可能的代价 ───────────────────────────────────────── 编译器优化         IC↓          CPI 可能变差（指令重排复杂度） 更复杂的ISA        IC↓          CPI↑（解码复杂，流水线难深） 乱序执行           CPI↓         电路复杂，功耗↑，时钟频率↓ 更深的流水线       时钟↑         CPI↑（分支预测失败代价↑） 更大的Cache        CPI↓（间接）  面积↑，访问延迟↑（L1变慢）`
    
    **品味判断**：RISC-V 为什么在嵌入式和学术界大受欢迎？因为它砍掉了几十年历史包袱，把 IC、CPI、Clock 三者的 trade-off 做到了一个更合理的平衡点。x86 的 CISC 指令集在现代实现里，实际上内部会被译码成类 RISC 的微操作（µops）——所以 CISC 的「IC少」优势，在现代实现里已经大幅缩水。
    
12. ### open clawAPP _—_ Yesterday at 07:27
    
     **![💡](https://discord.com/assets/2aa9dc22c1984b01.svg) 今日 Big Picture** 体系结构领域最重要的思维方式，我认为是**量化思维**： 不说「Cache大一些更好」，说「从 L1 32KB 扩到 64KB，命中率从 94% 提升到 96%，平均 CPI 改善 0.3，但 L1 访问延迟从 4 周期变为 5 周期，对于这个 workload，净收益是 +8% 性能」。 这门课会反复训练你这种思维：任何设计决策都有 trade-off，任何优化都有适用条件。学完这本书，你应该对「这个设计在什么条件下是好的，在什么条件下会失败」有清晰的判断。
    
    > _"The fundamental job of architects is to design systems that not only work functionally, but are fast, cheap, and power-efficient — and these goals are usually in conflict."_
    
    ---
    
    ##  ![🎯](https://discord.com/assets/8683903b8675f909.svg) 今日测验
    
    **Q1（概念）：** Amdahl定律告诉我们，如果一个程序有 80% 可以并行化，使用 4 个处理器的理论加速比是多少？用 8 个呢？为什么继续增加处理器的收益会递减？ **Q2（应用）：** 你正在优化一个游戏引擎，发现渲染线程占总帧时间 70%，其中 Drawcall 提交占 40%、Shader 编译占 30%。根据 Amdahl定律，你应该优先优化哪个？如果 Drawcall 提交可以 100% 并行化，Shader 编译只能 50% 并行化，4核下哪个收益更大？
    
13. **Q3（品味）：** 有人说「CPU 主频越高越好」，有人说「核心数越多越好」。根据 CPU 性能公式和 Amdahl定律，你怎么看这两个说法？什么样的 workload 适合高频单核，什么适合多核？