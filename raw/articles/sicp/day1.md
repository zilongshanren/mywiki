1. **Day 1 · The Elements of Programming — 编程的三要素** SICP 的第一页就扔出了一个看似平淡实则深刻的观察：
    
    > "Every powerful language has three mechanisms for combining simple ideas to form more complex ideas: **primitive expressions**, which represent the simplest entities the language is concerned with, **means of combination**, by which compound elements are built from simpler ones, and **means of abstraction**, by which compound elements can be named and manipulated as units."
    
    原子表达式、组合手段、抽象手段。三样东西。就这三样。 你可能觉得这太基础了——谁不知道变量、表达式、函数？但 SICP 说的不是"语法要素"，它说的是一种**认识论框架**：你用任何编程语言写的任何程序，归根到底都是在做这三件事。理解这一点，你就获得了一把跨越所有编程语言的钥匙。 ---
    
    ### 三要素不是 Scheme 的特性，而是编程的本质
    
    让我们把这个框架映射到你熟悉的世界： **C++ 的三要素：**
    
2. - 原子：`int`、`float`、`+`、`*` 等内置类型和操作
    - 组合：表达式 `a + b * c`、函数调用 `f(g(x))`、类的组合
    - 抽象：`函数`、`class`、`template`、`namespace`
    
    **Unity C# 的三要素：**
    
    - 原子：基本类型、Unity API 调用（`Transform.position`、`Physics.Raycast`）
    - 组合：`MonoBehaviour` 的组合、`GameObject` 的层次结构、`GetComponent<T>()` 的链式调用
    - 抽象：方法、类、接口、泛型、`ScriptableObject`
    
    **Shader 的三要素：**
    
    - 原子：`float4`、`tex2D()`、`dot()`、`mul()`
    - 组合：表达式组合（`saturate(dot(N, L) * atten + ambient)`）
    - 抽象：函数、`#include`、`SubShader`/`Pass` 的分层
    
    有趣的是，每种语言在这三个维度上的"表达力"是不同的。Lisp（Scheme）的组合和抽象手段极其统一——一切都是表达式，一切都可以传递。C++ 在这方面就分裂得多——函数、类、模板是三套不同的抽象机制，各有各的规则和限制。这不是好坏的判断，而是一种**设计权衡的审视**。 当你评价一门语言的时候，不要问"它有什么功能"，要问"它在这三个维度上分别提供了什么？它们之间有没有不一致的地方？"
    
3. ---
    
    ### 命名：最简单也最被低估的抽象
    
    SICP 用 `define` 引入命名：
    
    `(define pi 3.14159) (define radius 10) (define circumference (* 2 pi radius))`
    
    这看起来 trivial，但 Abelson 和 Sussman 在这里埋了一个深刻的点：
    
    > "It should be clear that the possibility of associating values with symbols and later retrieving them means that the interpreter must maintain some sort of memory that keeps track of the name-object pairs. This memory is called the **environment**."
    
    **环境**（environment）这个概念在第一章看起来只是"变量存储"，但到了第三章它会成为理解闭包、作用域链、甚至面向对象编程的核心工具。SICP 的教学设计精妙就在这里——它在第一章轻描淡写地引入一个概念，到后面你才发现这个概念有多重要。
    
4. 在游戏开发中，"环境"的概念无处不在。Unity 的 `SerializeField` 把变量暴露到 Inspector——这就是一种"环境可视化"。Shader 中的 `uniform` 变量从 CPU 端绑定到 GPU 端——这是跨硬件的"环境传递"。理解"环境"不只是"变量存在的地方"，而是"计算所依赖的上下文"，你对很多设计问题的思考会更清晰。 ---
    
    ### 代换模型：你的第一个思维工具（以及它为什么会被推翻）
    
    SICP 引入了**代换模型**（substitution model）来解释计算过程：
    
    `;; 定义 (define (square x) (* x x)) (define (sum-of-squares x y) (+ (square x) (square y)))  ;; 求值 (sum-of-squares 3 4) ;; 第一步：展开 sum-of-squares (+ (square 3) (square 4))`
    
5. `;; 第二步：展开 square (+ (* 3 3) (* 4 4)) ;; 第三步：计算 (+ 9 16) ;; 结果 25`
    
    代换模型的核心思想：**把函数调用替换为函数体，把参数替换为实际值，然后计算**。这在数学上叫做"β-归约"（beta reduction），是 Lambda Calculus 的基本操作。 这个模型简单、直觉、够用——对于纯函数来说。 但 SICP 在这里已经埋下了伏笔：代换模型**不能处理赋值**。当你写 `(set! x (+ x 1))` 时，x 的值取决于"什么时候"求值，而代换模型假设的是"x 的值是固定的"。这个矛盾在第三章会全面爆发，届时代换模型会被**环境模型**取代。 这里有一个深刻的教训：**好的思维工具是有适用范围的**。代换模型不是错的，它只是适用于没有副作用的世界。当你引入状态（赋值），你需要一个更强大的模型。
    
6. 在游戏开发中，这种"模型升级"随处可见：
    
    - 单线程模型足以理解简单游戏 → 多线程后你需要理解竞态条件
    - 单帧渲染足以理解前向渲染 → 延迟渲染后你需要理解 G-Buffer 和多 pass 管线
    - 同步调用足以理解本地 API → 网络同步后你需要理解时序和一致性
    
    **每一次"模型升级"都是认知的阶跃，而 SICP 在第一章就为你示范了这个过程。** ---
    
    ### Applicative Order vs Normal Order：一个改变编程范式的选择
    
    SICP 在 1.1.5 节讨论了两种求值顺序： **Applicative order（应用序）**：先求值参数，再应用函数。这是大多数语言（C、Java、Python、C#）的选择。
    
    `scheme`
    
7. `;; applicative order (sum-of-squares (+ 1 2) (* 2 3)) ;; 先算参数 (sum-of-squares 3 6) ;; 再展开 (+ (square 3) (square 6)) (+ 9 36) 45`
    
    **Normal order（正则序）**：不求值参数，直接展开，直到需要原子值时才计算。
    
    `;; normal order (sum-of-squares (+ 1 2) (* 2 3))`
    
8. `;; 直接展开，不算参数 (+ (square (+ 1 2)) (square (* 2 3))) (+ (* (+ 1 2) (+ 1 2)) (* (* 2 3) (* 2 3))) ;; 现在才计算 (+ (* 3 3) (* 6 6)) (+ 9 36) 45`
    
    注意 normal order 中 `(+ 1 2)` 被计算了**两次**！这就是惰性求值（lazy evaluation）的雏形，也是它的代价。 这个看似学术的区别实际上影响了整个编程语言的设计方向：
    
    - **Haskell** 选择了 normal order（惰性求值），因此可以自然地处理无限数据结构（无限列表），但性能分析变得极其困难
    - **Rust** 选择了 applicative order（严格求值），并通过 `Iterator` trait 的 lazy chain 来获得部分惰性的好处
    - **C#** 的 LINQ 也是惰性的——`Where().Select()` 不会立即执行，直到 `ToList()` 或 `foreach` 触发
    
9. 在游戏开发中，这个选择有直接的工程影响：
    
    `// Unity 中的 applicative order 陷阱 void Update() { // GetComponent 每帧调用？这就是 applicative order 的"急切"—— // 即使这帧根本不需要 rigidbody var rb = GetComponent<Rigidbody>(); if (someRareCondition) { rb.AddForce(Vector3.up); } }  // 惰性风格：只在需要时获取 void Update() { if (someRareCondition) {`
    
10. `GetComponent<Rigidbody>().AddForce(Vector3.up); } }  // 更好的做法：缓存（memoization，SICP 后面会讲） private Rigidbody _rb; void Start() { _rb = GetComponent<Rigidbody>(); } void Update() { if (someRareCondition) { _rb.AddForce(Vector3.up); } }`
    
    **求值时机的选择**——立即计算还是延迟到需要时？——这是编程中反复出现的设计决策。SICP 在第一天就把它放在你面前了。
    
11. ---
    
    ### 组合的力量：为什么 Lisp 的括号不是缺陷而是特性
    
    很多人嘲笑 Lisp 的括号。但 SICP 的第一个深刻 insight 是：**统一的前缀表示法让"组合"变得完全一致。**
    
    `;; 所有操作，统一格式 (+ 1 2) (* 3 4 5) (+ (* 3 (+ (* 2 4) (+ 3 5))) (+ (- 10 7) 6))`
    
    没有运算符优先级的困扰，没有中缀/前缀/后缀的不一致。一切都是 `(操作符 操作数...)`。这意味着：
    
    1. **程序即数据**——代码本身就是列表结构，可以被程序操作（这在第四章会成为核心）
    2. **无歧义嵌套**——任意深度的组合都有明确的解析方式
    
12. 3. **宏系统的基础**——因为代码是数据，你可以写"生成代码的代码"
    
    这个"代码即数据"（homoiconicity）的性质是 Lisp 最深刻的设计决策。在现代语言中，你可以看到它的影子：
    
    - **C# Expression Tree**：`Expression<Func<int, bool>>` 把 lambda 捕获为数据结构
    - **Roslyn 编译器**：C# 代码可以被程序读取、分析、修改、重新生成
    - **Shader Graph / Visual Scripting**：节点图就是一种"代码即数据"的表达方式
    
    但没有一种现代语言达到了 Lisp 在这方面的统一性。这不是因为其他语言不够好，而是因为它们选择了不同的权衡：可读性和类型安全 vs 元编程的极致灵活性。 ---
    
    ### 品味判断：SICP 第一章教你的不是语法
    
    如果你只从第一章带走一个东西，应该是这个： **编程的本质不是语法，是三种行为的组合：构造原子、组合原子、给组合命名。**
    
13. 你每天在 Unity 中写的代码，无论多复杂，都在做这三件事。当你觉得代码变得臃肿、难以理解时，检查这三个维度：
    
    1. **原子够原子吗？** 你的基本单元是否足够简单，每个函数/类只做一件事？
    2. **组合够清晰吗？** 组合的方式是否一致，读起来能自然地"展开"理解？
    3. **抽象够到位吗？** 重复的模式是否已经被命名和封装？
    
    SICP 的牛逼之处在于：它不教你"怎么用 Scheme"，它教你"怎么思考编程"。Scheme 只是一个足够简单的载体，让你能把注意力放在思想上，而不是语法上。 从明天开始，我们进入过程抽象——函数不只是代码的组织单元，它是构建复杂系统的基本砖块。当你理解了函数作为"黑盒"的真正含义，你写代码的方式会发生根本性的改变。 ---
    
    > 编程语言不是工具集，是思维框架。三要素——原子、组合、抽象——是你审视任何语言、任何架构、任何系统的终极透镜。