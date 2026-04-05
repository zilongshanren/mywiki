1. **Day 4 · 增长的代价 — 从直觉到算法** ─── 有一种认知升级，你一旦拥有就无法忽视：**看到一个算法，脑子里会自动估算它的资源消耗随问题规模增长的方式。** 这就是今天的主题。SICP Ch1.2.3-1.2.4 讲的不只是增长阶和快速幂，而是一种**判断计算效率的思维方式**——粗糙但有力，足以在写代码之前就预判结局。 ─── 增长阶：粗糙但有力的度量 SICP 对增长阶的定义精确但不繁琐： "We say that R(n) has order of growth Θ(f(n)), written R(n) = Θ(f(n)) (pronounced 'theta of f(n)'), if there are positive constants k₁ and k₂ independent of n such that k₁f(n) ≤ R(n) ≤ k₂f(n) for any sufficiently large value of n." 注意这里用的是 Θ（Theta），不是 O（Big-O）。区别是：O 只给上界，Θ 同时给上界和下界。SICP 在这里更精确——它说的是资源消耗**恰好**以某个方式增长，不是"至多"。
    
2. 但更重要的是紧跟着的这段话： "Orders of growth provide only a crude description of the behavior of a process." 增长阶是**粗描述**。Θ(n²)、Θ(1000n²)、Θ(3n² + 10n + 17) 的增长阶完全相同。常数系数被抹掉了。 这是一种刻意的简化，不是缺陷。SICP 的用意是：在问题规模足够大的时候，增长的**形状**（线性、对数、指数）远比常数系数重要。一个 O(n) 算法不管常数多大，最终都会在大 n 上胜过 O(n²)。 "For a Θ(n) (linear) process, doubling the size will roughly double the amount of resources used. For an exponential process, each increment in problem size will multiply the resource utilization by a constant factor." 这是增长阶最有用的直觉：
    
    `| 增长阶      | 问题规模翻倍时... | | -------- | ---------- | | Θ(1)     | 不变         |`
    
3. `| Θ(log n) | 增加一个常数     | | Θ(n)     | 翻倍         | | Θ(n²)    | 变成原来 4 倍   | | Θ(2ⁿ)    | 平方！        |`
    
    这个直觉告诉你：如果你的游戏场景里有 1000 个物体，用 O(n²) 的碰撞检测大概要做 100 万次检查；有 2000 个物体就是 400 万次。用 O(n log n) 的方法？1000 → 约 10000，2000 → 约 22000。差了 20 倍。 ─── 快速幂：分治思想的第一次亮相 SICP 用指数计算来演示 O(log n) 算法的力量。 朴素版本是显而易见的：
    
4. `(define (expt b n)   (if (= n 0)        1        (* b (expt b (- n 1)))))`
    
    这是线性递归，Θ(n) 步，Θ(n) 空间（因为有 deferred multiplications 链）。计算 b^1000 需要 1000 次乘法。 迭代版本：
    
    `(define (expt b n)    (expt-iter b n 1)) (define (expt-iter b counter product)   (if (= counter 0)       product`
    
5.       `(expt-iter b (- counter 1) (* b product))))`
    
    还是 Θ(n) 步，但现在是 Θ(1) 空间——状态全在参数里，不需要栈来记住"待完成的乘法"。
    
6. 然后 SICP 给出了真正的洞察：
    
    `(define (fast-expt b n)   (cond ((= n 0) 1)         ((even? n) (square (fast-expt b (/ n 2))))         (else (* b (fast-expt b (- n 1))))))`
    
    关键规则：
    
    - 如果 n 是偶数：b^n = (b^(n/2))²
    - 如果 n 是奇数：b^n = b · b^(n-1)
    
    > "The difference between Θ(log n) growth and Θ(n) growth becomes striking as n becomes large. For example, fast-expt for n = 1000 requires only 14 multiplications."
    
    1000 次 vs 14 次。这不是小优化，这是**量级跃迁**。
    
7. ### 为什么是 O(log n)？
    
    SICP 给出了最直接的解释：
    
    > "Computing b^(2n) using fast-expt requires only one more multiplication than computing b^n. The size of the exponent we can compute therefore doubles (approximately) with every new multiplication we are allowed."
    
    逆向想：每允许多一次乘法，可处理的指数就翻倍。所以处理 n，需要约 log₂(n) 次乘法。 这是分治（divide and conquer）的本质：每次把问题规模减半，所以深度是 log₂(n)。
    
    ### 游戏开发中的直接应用
    
    快速幂不只是理论。你会在很多地方遇到它： **矩阵快速幂**——游戏中骨骼动画里，如果需要计算矩阵的 n 次方（某些程序化动画），可以用同样的分治思想：
    
8. `Matrix4x4 MatrixPow(Matrix4x4 m, int n) {     if (n == 0) return Matrix4x4.identity;     if (n % 2 == 0) {         var half = MatrixPow(m, n / 2);         return half * half;     }     return m * MatrixPow(m, n - 1); }`
    
    **模运算快速幂**——密码学、随机数生成器：
    
    `// 计算 base^exp % mod，避免大数溢出 long ModPow(long base, long exp, long mod) {`
    
9.     `long result = 1;     base %= mod;     while (exp > 0) {         if (exp % 2 == 1) result = result * base % mod;         exp /= 2;         base = base * base % mod;     }     return result; }`
    
    注意这里用的是**迭代版**快速幂——SICP 的 Exercise 1.16 就是要你实现这个。迭代版利用了"不变量"的思想（invariant quantity）：维持 `result * base^exp` 在每次循环中保持不变。这是 SICP 对"如何设计迭代算法"的深刻洞察。 ---
    
    ## 欧几里得算法：2000 年的优化
    
10. SICP 在 1.2.5 紧接着介绍 GCD，这不是随机的——它是另一个 O(log n) 算法，但来路完全不同：
    
    `(define (gcd a b)   (if (= b 0)       a       (gcd b (remainder a b))))`
    
    三行代码，2300 年历史（欧几里得大约生于公元前 300 年）。 它的正确性基于一个数学事实：
    
11. > "GCD(a,b) = GCD(b,r) where r is the remainder when a is divided by b"
    
    这是因为 a 和 b 的公因数，恰好就是 b 和 (a mod b) 的公因数。 来看 SICP 给的例子：
    
    `GCD(206, 40) = GCD(40, 6)              = GCD(6, 4)              = GCD(4, 2)              = GCD(2, 0) = 2`
    
    5 步就解决了，而朴素的因数分解方法可能要试到 206 的所有因数。
    
    ### Lamé 定理：GCD 与斐波那契的联系
    
    SICP 提到了一个漂亮的定理：
    
12. > "Lamé's Theorem: If Euclid's Algorithm requires k steps to compute the GCD of some pair, then the smaller number in the pair must be greater than or equal to the kth Fibonacci number."
    
    这意味着：最坏情况下（输入是相邻的斐波那契数），欧几里得算法的步数约为 O(log(min(a,b)))。 这个定理本身就是一个品味时刻——**数论中两个看似不相干的概念（GCD 和 Fibonacci）之间存在深刻联系**。好的算法分析往往会揭示这种隐藏的联系。
    
    ### 在游戏开发中哪里用 GCD？
    
    比你想象的多： **纹理分辨率管理**——当你需要把两张不同分辨率的纹理合并时，找 GCD 决定最大公共 tile 尺寸：
    
    `int Gcd(int a, int b) => b == 0 ? a : Gcd(b, a % b);  // 两张纹理 512x768 和 384x512，最大公共块尺寸？`
    
13. `int blockSize = Gcd(Gcd(512, 768), Gcd(384, 512)); // = 128`
    
    **帧率同步**——30fps 和 60fps 的最小公倍数（LCM = a_b/GCD(a,b)）决定了同步周期： ```csharp int Lcm(int a, int b) => a / Gcd(a, b)_ b; int syncPeriod = Lcm(30, 60); // 60，每 60 帧同步一次 ``` **UI 布局**——等比分割屏幕时，用 GCD 找整数分割点。 ---
    
    ## 增长阶的品味判断
    
14. 知道增长阶，但更重要的是**在工程决策中正确使用它**。这里有几个容易犯的错误：
    
    ### 错误一：忽略常数系数
    
    O(log n) 并不总是比 O(n) 快。如果 O(n) 的常数是 1，O(log n) 的常数是 10000，在 n < 10^(10000) 时 O(n) 更快。 在游戏中，如果数组里只有 16 个元素，二分查找的 overhead（分支预测失败、缓存未命中）可能远超线性扫描。 **SICP 在这里是诚实的**：增长阶是粗描述，小规模时常数很重要。
    
    ### 错误二：不考虑缓存行为
    
    一个 O(n²) 的算法如果访问模式是连续的（cache-friendly），可能在实际测试中胜过一个 O(n log n) 但内存跳跃访问的算法。 这在游戏引擎中尤其重要。GPU 的缓存对访问模式极其敏感——这就是为什么 Entity Component System（ECS）架构要求数据连续存储，即使它的某些操作渐近复杂度更高。
    
    ### 错误三：优化错误的地方
    
15. 增长阶分析告诉你哪段代码**可能**成为瓶颈。但"可能"不等于"是"。用 profiler 确认热点之前，增长阶分析只是指导方向，不是优化指令。 SICP 引用 Knuth（第三版前言）的话精神是：**premature optimization is the root of all evil**。增长阶帮助你避免显然错误的选择（别在关键路径上用 O(n³)），但不是优化一切的理由。 ---
    
    ## 分治的本质
    
16. 今天涉及的所有算法（快速幂、欧几里得）都有一个共同模式：**把大问题规约到更小的同类问题**。 这就是分治（divide and conquer）的本质。规约的速度决定了最终的复杂度：
    
    - 每次减少一半 → O(log n)
    - 每次减少一个 → O(n)
    - 每次生成两个子问题，各减少一半 → O(n log n)（归并排序）
    - 每次生成两个子问题，每次只减少 1 → O(2^n)（朴素 Fibonacci）
    
    SICP 在第一章就给你建立了这个直觉框架：通过四个递进的例子（阶乘、Fibonacci、快速幂、GCD），你看到了同一类"问题规约"思想如何产生天壤之别的效率。 这个框架会在整本书里反复出现——第 2 章的树操作、第 5 章的寄存器机器，都是分治思想的不同化身。 ---
    
    ## 代码练习：迭代快速幂
    
    SICP Exercise 1.16 的精华版，加上游戏开发的情境：
    
17. `; 迭代快速幂（Scheme） ; 不变量：result * b^n 在每次迭代保持不变 (define (fast-expt-iter b n)   (define (iter b n result)     (cond ((= n 0) result)           ((even? n) (iter (square b) (/ n 2) result))           (else (iter b (- n 1) (* result b)))))   (iter b n 1))`
    
    对应的 C# 版本（游戏引擎实用）：
    
    `// 整数快速幂（适用于动画帧步进、LOD 计算等） static long FastPow(long b, int n) {`
    
18.     `long result = 1;     while (n > 0) {         if ((n & 1) == 1) result *= b;  // n 是奇数         b *= b;                          // b = b²         n >>= 1;                         // n = n/2     }     return result; }  // 浮点快速幂（着色器预计算、概率衰减） static float FastPowf(float b, int n) {     float result = 1.0f;     while (n > 0) {         if ((n & 1) == 1) result *= b;         b *= b;`
    
19.         `n >>= 1;     }     return result; }`
    
    注意 `n & 1` 和 `n >>= 1` 替代了取余和除法——位操作在整数上更快，编译器通常会自动做这个优化，但显式写出来意图更清晰。 ---
    
    > 快速幂告诉你：同一个数学问题，可以有复杂度天壤之别的计算过程。程序员的技能不只是让计算机做事，而是让它以最聪明的方式做。
    
    ---
    
    ##  ![🎯](https://discord.com/assets/8683903b8675f909.svg) 今日测验
    
20. **Q1 (概念)：** Θ(n²) 和 Θ(n log n) 两种增长阶，在 n = 10、n = 1000、n = 10⁶ 时，各自大约需要多少步？从这个对比中，你理解到了什么？ **Q2 (应用)：** 你在写一个 Unity 游戏的寻路系统。每帧需要在 200 个 waypoint 中找到离玩家最近的 3 个点。有两个方案：方案 A 是对所有 waypoint 遍历计算距离（O(n)），方案 B 是提前构建一个空间数据结构（k-d tree，查询 O(log n)）。从增长阶分析的角度，什么情况下方案 A 可能比方案 B 实际更好？什么情况下必须用方案 B？
    
21. **Q3 (代码)：** 用 Scheme 或 C# 实现一个函数 `compose-n`，让 `(compose-n f n)` 返回"将 f 应用 n 次"的函数，即 f∘f∘...∘f (n 次)。要求使用 O(log n) 的方式（类比快速幂的思想）。提示：`(compose-n f 4)` = `compose(compose(f,f), compose(f,f))`