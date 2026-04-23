---
tags: [index]
date: 2026-04-14
sources: 371
---

# 知识库索引

本知识库涵盖**软件设计哲学 · 实时渲染 · 游戏引擎 · 计算机体系结构 · 编程语言基础**五大主题。入口页：[[overview]]。品味训练指南：[[taste-development]]。

## 软件设计（wiki/software-design/）
核心概念与框架，源自 John Ousterhout 的 APoSD。

| 文章 | 一句话描述 |
|---|---|
| [[complexity]] | 复杂性的定义与整体框架，软件设计的核心敌人 |
| [[change-amplification]] | 复杂性症状之一：改动需要触及多处 |
| [[cognitive-load]] | 复杂性症状之二：需要知道太多东西 |
| [[unknown-unknowns]] | 复杂性症状之三：不知道自己不知道（最危险） |
| [[dependencies]] | 复杂性根源之一：代码间的相互牵连 |
| [[obscurity]] | 复杂性根源之二：重要信息不显而易见 |
| [[red-flags]] | 识别设计问题的信号集合 |
| [[tactical-programming]] | 短视的「让它工作」心态 |
| [[strategic-programming]] | 投资心态，优秀设计恰好也能工作 |
| [[tactical-tornado]] | 外部化成本的高产出工程师 |
| [[zero-tolerance]] | 对复杂性增量的日常纪律 |
| [[continuous-design]] | 软件设计是持续过程，不是一次性活动 |
| [[modular-design]] | 模块化的真正目标是认知隔离 |
| [[deep-modules]] | 强大功能 + 简单接口的设计理想 |
| [[shallow-modules]] | 接口复杂度接近实现复杂度的反模式 |
| [[classitis]] | 「类越多越好」的系统性设计疾病 |
| [[interface-vs-implementation]] | 接口是成本，功能是收益 |
| [[abstraction]] | 省略不重要细节的简化视图 |
| [[false-abstraction]] | 省略了重要细节的「简洁」陷阱 |
| [[information-hiding]] | 把设计决策藏进实现——深模块的引擎 |
| [[information-leakage]] | 同一份知识分散在多个模块 |
| [[temporal-decomposition]] | 按时间顺序切模块的陷阱 |
| [[smooth-window-resize]] | 桌面 GUI 平滑窗口缩放：swapchain、WM、事件循环的同步体检 |
| [[rust-gui-ecosystem]] | Rust GUI 生态的多峰现状与 linebender（Druid / Xilem / Vello）路线 |
| [[reactive-ui-rust]] | Rust 下反应式 UI 架构：lens、Elm、Xilem 的假设 |
| [[c-opaque-struct-modules]] | C 语言下的不透明结构模块与伪 friend 技巧（云风） |
| [[c-interface-oop]] | C 语言的接口表 + data 组合式 OOP（云风） |
| [[simple-cpp-mark-sweep-gc]] | 200 行的 C++ 标记清除 GC 玩具（云风） |
| [[c-serialization-metadata]] | 基于自定义元信息的 C 结构序列化与图合并算法（云风） |
| [[ecs-for-rust-ui]] | Rust UI 的「类 ECS」架构：整数 id + state splitting + data flow 对抗借用检查器（Raph Levien 2018）|
| [[data-structure-invariants]] | ryg：每加一条访问路径就多一条不变量——tail-pointer-to-pointer 与 sentinel 节点是清理之法 |
| [[cpp-multi-paradigm-discipline]] | 把 C++ 当语言联邦：团队必须定义子集（云风评 Effective C++ 3rd Item 1） |
| [[strategy-vs-switch]] | Fowler 经典重构：用 Strategy 模式替代类型码驱动的 switch |
| [[type-safety-vs-simplicity]] | 类型安全 vs 代码浅显——云风写完 C++ 版粒子系统后的自我怀疑 |
| [[id-based-lifetime-with-kill-flag]] | ID 索引 + 销毁标记：替代 refcount 的对象生命期管理模式 |
| [[identity-problem-naming]] | Evan Todd：命名的本质是判断两物是否同一 |
| [[automated-test-philosophy]] | 自动化测试的目的是防回归而非找 bug |
| [[ci-cost-optimization-asg]] | 用 Jupyter 把 ASG 调优成最优化题 |
| [[xlsx-text-versioning]] | xlsx 规范化为可 diff 文本格式；文件锁驱动的无插件编辑链路 |
| [[static-site-antiframework]] | 反框架：本机 Pandoc + wrangler 替代 JAMstack VM |
| [[vibe-coding-workflow]] | AI 代理编程工作流：plan mode + per-PR review + 对账测试 |
| [[graphics-programmer-constraints]] | 图形程序员行业的硬约束与世界观 |
| [[clean-code-critique]] | 游戏/图形视角对 clean code 的系统批判 |
| [[future-proofing-tests]] | Ben Supnik 的三问测试：什么时候可以给未来设计 |
| [[cheat-by-solving-less]] | 打败专家靠作弊——只解一个更小的问题 |
| [[good-software-no-double-check]] | Agent 过度防御的新气味，用不变量和静态类型代替重复检查 |
| [[dcmake]] | CMake 的多平台 GUI 调试器 |
| [[cmake-dap-debugger]] | CMake 3.27+ 的 DAP 调试模式 |
| [[dear-imgui-docking]] | Dear ImGui 的 docking 分支 |
| [[intent-vs-state]] | 用户 Intent 作为 source of truth，State 为派生——Wittens 的前端架构观 |
| [[dom-replacement-rethink]] | DOM/CSS/HTML 的系统性批判与替代路径 |
| [[middleware-vs-open-source]] | 独立团队在闭源中间件与开源库之间的取舍守则 |

| [[ai-code-agent-workflow]] | Hooper 的精确 prompt 路线：AI 当键盘替代而非大脑替代 |
| [[experience-as-noise-filter]] | Pesce：经验是噪声过滤器，既筛掉平庸也筛掉天才级的「不可能想法」 |
| [[incremental-rearchitecting]] | Supnik：增量重构替代大重写，以及大重写失败的组织动力学 |
| [[header-as-user-manual]] | Supnik：头文件即用户手册，物理隔离 > 逻辑封装 |
| [[api-fast-path-design]] | Supnik：快/慢路径在 API 上显式拆分（X-Plane dataref 模式）|
| [[no-magic-principle]] | 计算机里没有魔法：debug、学习与教学的基础姿态（Schöner） |
| [[stl-not-abstraction-prescription]] | Supnik：STL 不是抽象（不隐藏细节），而是对实现与性能的精确规定 |
| [[system-decoupling-patterns]] | Bitsquid 解耦四条：防 framework / 高层调度低层 / 允许复制 / ID 引用 |
| [[polling-callbacks-events]] | 低层→高层通知三种方式：优先 poll / callback 必须延迟 / event 别做 global switchboard |
| [[minimal-markup-pipeline]] | Bitsquid 100 行 Ruby：line-list parser + tag-stack generator |
| [[parameter-nodes-intrusive-linked-list]] | 池化数组 + intrusive 链表：变长小集合的 DOD 容器 |
| [[pragmatic-performance-philosophy]] | Frykholm 的务实性能观七条 + 数量级驱动设计 |
| [[crash-on-unexpected-errors]] | Bitsquid：unexpected error 立刻崩，API 对调用方负全责 |
| [[error-context-stack]] | thread-local 作用域变量栈：深层 assert 的现场信息 |
| [[minimize-points-and-types-of-failure]] | expected error 的 API 设计：少失败点 + 函数级 enum + struct 返回 |
| [[warnings-as-errors-strategy]] | warning 治理：升格为 error + deprecation 四档降级 + tool-first 显示 |
| [[now-principle-productivity]] | Bitsquid 五条日常纪律：5 分钟规则、修病根、心流、VCS、build server |
| [[pimpl-vs-pure-virtual]] | Bitsquid：C 不透明指针 / C++ PIMPL / 纯虚抽象类三种隔离方式的工程取舍 |
| [[no-frame-delays-principle]] | Bitsquid 戒律：动作立即生效，禁止延迟一帧引入灰色过渡态 |
| [[async-api-id-tokens]] | 异步 API 的极简设计：ID token + round-robin + implicit API |
| [[cleaning-bad-code]] | Frykholm 9 条：遗留代码清理操作手册（改良优于革命）|
| [[encapsulation-over-polymorphism]] | Supnik 2010：OOP 三要素 90/10/0 启发式，封装才是核心 |
| [[types-h-data-code-separation]] | Bitsquid：types.h 集中数据、函数按功能分组的 header 组织 |
## 编程语言基础（wiki/programming-languages/）
SICP 及 Lambda 演算传统的核心概念。

| 文章 | 一句话描述 |
|---|---|
| [[elements-of-programming]] | 编程语言的三要素：原子、组合、抽象 |
| [[substitution-model]] | 纯函数求值的思维工具 |
| [[applicative-vs-normal-order]] | 求值时机的两种设计选择 |
| [[environment]] | 名字→值的 frame chain |
| [[procedural-abstraction]] | 过程作为黑盒 |
| [[lexical-scoping]] | 代码结构决定作用域 |
| [[closure]] | 函数 + 定义时环境 |
| [[recursive-vs-iterative-process]] | 递归语法 vs 递归过程 |
| [[tail-call-optimization]] | 尾调用优化与语言设计分歧 |
| [[higher-order-functions]] | 函数作为一等公民 |
| [[lambda-calculus]] | 计算的通用数学模型 |
| [[order-of-growth]] | 算法增长阶的粗描述 |
| [[fast-exponentiation]] | 分治思想的经典例证 |
| [[probabilistic-algorithms]] | 用概率正确性换可行性 |
| [[lua-class-pattern]] | Lua 定义类型的几种极简套路；用 `[false]` 隐藏容器元数据 |
| [[functions-as-vectors]] | 函数作为无限维向量：Fourier / 球谐的统一视角 |
| [[cpp-runtime-reflection]] | libclang 元程序生成 C++ 运行时类型表 |
| [[swap-and-pop-removal]] | 无序数组删除的 swap-and-pop 技巧：O(n) → O(1) |
| [[java-vector-math-limitations]] | Java 做向量数学的两个痛点：无运算符重载、无栈分配 |
| [[hamming-code-hat-puzzle]] | 31 人帽子谜题的 Hamming 码最优策略：胜率 31/32 与对称性上界 |
| [[automatic-differentiation]] | autodiff 全景：dual number forward / DAG backward / JAX 梯度即图变换 |
| [[cantor-szudzik-pairing]] | Cantor 与 Szudzik 两种 2D → 1D 配对函数的对比 |
| [[lua-cpp-binding]] | 手写最小的 Lua/C++ 嵌入封装：栈式 API、点路径取值、表遍历、pcall 调函数 |
| [[avoid-unsigned-types]] | 默认避免 C++ unsigned 类型：保住 sanity check 的能力 |
| [[lua-design-philosophy]] | Roberto/Luiz 访谈：Lua 的机制而非法策、有栈协程、可移植性偏执（云风译） |
| [[c-tagged-union-dispatch]] | C 语言用 tagged union 做类型安全的多变体接口分发（云风） |
| [[cycle-detection-floyd-brent]] | Floyd 龟兔与 Brent 变体；Brent 作为迭代加深的一个实例 |
| [[csharp-runtime-script-compilation]] | C# 自身作脚本：CodeDomProvider + AppDomain shadow copy 实现热重载 |
| [[rpp-stl-replacement]] | Slater 的 rpp：Rust 风格 C++20 STL 替代（region 分配器 / brand / 协程 / 反射） |
| [[continuous-probability]] | 连续概率速成：PDF/CDF、期望方差、Markov/Chebyshev、Dirac delta（MC 系列 Part 1） |
| [[sigmoid-functions]] | tanh/erf/倒平方根 sigmoid 的听感、速度与多项式变形近似 |
| [[negative-space-in-programming]] | ryg：程序的形状由「不做什么」决定 |
| [[nested-loop-optimization]] | 嵌套循环性能迷思的基准反驳：Nested 快于 Single 快于 LINQ，可读性优先 |
| [[go-goroutine-channels]] | Go 的 goroutine / chan / select 与 CSP 风格并发 |
| [[lua-incremental-gc]] | Lua 5.1 增量式 GC 的五阶段状态机与双白色乒乓 |
| [[lua-c-api-dylib-proxy]] | 静态链接 Lua 宿主如何挂第三方 C 扩展：运行期代理 DLL 和构建期 extlua 两代方案 |
| [[stackless-vs-stackful-coroutines]] | C++20 协程为何不需要整栈保存 |
| [[coroutine-awaitable-pattern]] | awaitable 与 coroutine 的分工：名词 vs 动词 |
| [[mulberry32-rng]] | 极简 32-bit 确定性 PRNG：Weyl + xor-shift-multiply |
| [[zig-c-abi-boundary]] | Zig 跨 DLL 只有 C ABI：三文件结构 + comptime 分支的绕法 |
| [[header-file-vs-pub-export]] | `pub` 内联标注把维护成本转嫁为消费者阅读成本 |
| [[free-vs-member-functions-performance]] | 2017 年 Klaus 主张的「free function 更快」8 年后被重测：基本是噪声 |
| [[pade-approximants]] | 有理函数逼近 Taylor 级数，介于 Taylor 与 Minimax 之间的中间台阶 |
| [[hash-trie-intrusive]] | 链表节点兼任哈希 trie 的侵入式结构 |
| [[unity-build-macro-renaming]] | C 里用 `#define` + unity build 合并同名符号的平台层 |
| [[web-clipboard-api]] | Web 剪贴板两套 API 的历史分裂：异步严类型白名单 vs Clipboard Events 任意类型，Google Docs / Figma / Web Custom Formats 的三种绕行方案（Alex Harri） |
| [[compressed-trie-pattern-matching]] | 倒序插入 + 子树压缩让 trie 自发泛化出后缀模式匹配，3,600 冰岛名压进 3.27 kB trie（beygla / Alex Harri） |
| [[orthodox-cpp]] | Orthodox C++（C+）：反 Modern C++ 的最小 C++ 子集主张 |

| [[mach-nominated-zig-versions]] | Zig nightly/stable 之间的月度提名版本机制 |
| [[zig-package-mirror]] | pkgmirror：自托管 Zig toolchain 与包镜像服务 |
| [[computational-complexity-theory-intro]] | 计算复杂度理论入门：$\P/\NP/\coNP$ 与多项式时间归约 |
| [[patterna-hexcells-np-vs-conp]] | 逻辑消除游戏的玩法复杂度：推理是 $\coNP$-complete 而非 $\NP$-complete |
| [[optional-static-typing]] | 可选静态类型：AS3/haXe 起手，TypeScript/Python hints 承接 |
| [[method-binding-semantics]] | 方法隐式 vs 显式绑定 `this`，以及对事件系统对称性的影响 |
| [[earley-parser]] | Earley parser：接受任意 CFG 的通用解析算法，最坏 O(n^3) |
| [[cpp-template-value-vs-type-parameter]] | C++ 模板按类型 vs 按值参数化：只有后者能真正内联函数指针 |
| [[static-hash-value-debug-assert]] | 字符串 hash 常量化：硬编码值 + debug 复算断言 |
| [[tiny-expression-language]] | Bitsquid：给美术用的 stack-VM + RPN 表达式求值器，含 shunting-yard 编译与常量折叠 |
| [[string-handling-game-runtime]] | Bitsquid 经验：UTF-8 + 不要 string class + 运行时 hash ID |
| [[lua-light-userdata-bindings]] | Light userdata 绑定：零分配、零 GC、手写类型 marker |
| [[lua-memory-profiling]] | Lua 内存调优：`_G` 遍历盘点 + `lua_Alloc` stack trace + feedback GC |
| [[murmur-hash-inverse]] | MurmurHash2 32/64 位的数学逆运算（乘法逆元 + 逆异或移位）|
| [[schema-driven-xml-parser-generator]] | Patrick Stein 基于 XML schema 的 CLOS 解析器代码生成（tagstack + 自举 + 多后端） |
| [[floating-point-geometric-predicates]] | 点积符号抖动、线线求交条件数爆炸、几何谓词的鲁棒化策略 |
| [[c-bitwise-operator-precedence-history]] | 为何 C 的 `&` 优先级低于 `==`：B/BCPL 的历史包袱 |
| [[lua-runtime-dynamism-tricks]] | Bitsquid 的 Lua 七招：REPL、热重载、API 劫持、动态 profiler、对象枚举 |
## 计算机体系结构与系统（wiki/computer-systems/）
CAQA + CSAPP 的底层视角。

| 文章 | 一句话描述 |
|---|---|
| [[amdahls-law]] | 并行加速的理论上界 |
| [[flynn-taxonomy]] | 指令流 × 数据流的架构分类 |
| [[cpu-performance-formula]] | CPU Time = IC × CPI / Clock Rate |
| [[latency-vs-throughput]] | 两种性能指标的权衡 |
| [[memory-hierarchy]] | 跨越 5 个数量级的存储分层 |
| [[locality-principle]] | 缓存层次的理论基础 |
| [[aos-vs-soa]] | 内存布局决定 cache 利用率 |
| [[cache-friendliness]] | 让代码与缓存对齐 |
| [[dennard-scaling]] | 晶体管缩放规律的崩塌 |
| [[power-wall]] | 频率停滞的物理原因 |
| [[mttf-reliability]] | 可靠性的量化指标 |
| [[bits-and-context]] | 信息 = 比特 + 上下文 |
| [[compilation-pipeline]] | C 编译的四阶段 |
| [[virtual-memory]] | 进程独立连续地址空间幻觉 |
| [[sse-tricks]] | 跨代 SSE/SSE2 的非正交性补洞技巧 |
| [[adaptive-arithmetic-coding]] | 二元自适应模型 = 多通道 IIR 滤波器，rANS 让多元复活 |
| [[non-cryptographic-hash]] | 现代非加密哈希演进与 Burst codegen 差异 |
| [[rapidhash]] | wyhash 后继的极简 64 位哈希函数 |
| [[compiler-interference-analysis-bug]] | MSVC 把两个活跃临时量塞到同一栈槽的 codegen bug |
| [[linear-allocator]] | O(1) 推指针式分配器，帧内临时数据的默认选择 |
| [[cuda-memory-hierarchy]] | CUDA kernel 可见的 5 种内存：register/local/shared/global/constant |
| [[faster-math-functions]] | 无 libm 场景下手写 sin/cos/exp/pow——minimax 多项式，不是 Taylor |
| [[fearless-simd]] | Rust 下可移植 SIMD 的双层 trait 方案与 runtime 选档难题 |
| [[calling-conventions-x86]] | x86 32 位 cdecl / stdcall / fastcall 三路汇编 diff |
| [[linux-graphics-stack-dri]] | Linux 图形栈 DRI/DRM/KMS 的命名迷雾与真实分层 |
| [[malloc-wrapper-debug]] | 给 malloc 加壳：狗牌、泄漏检测与 __FILE__/__LINE__ 定位 |
| [[gcn-wave-occupancy]] | GCN 波前占用率：VGPR 预算、何时重要、何时反而害人 |
| [[gpu-latency-hiding]] | GPU 用 ILP 与 TLP 两条互斥路径隐藏内存延迟 |
| [[meshoptimizer-vertex-codec]] | 非 LZ 的 delta/预测顶点压缩器，在浮点图像上也赢 |
| [[carry-save-adder-pixel-avg]] | 用 CSA 恒等式对 A8R8G8B8 / R5G6B5 做无溢出、可选 rounding bias 的 SWAR 平均 |
| [[gpgpu-transform-feedback-ios]] | 在 OpenGL ES 3.0 Transform Feedback 上榨出 GPGPU 的历史 hack |
| [[nsmutablearray-circular-buffer]] | `__NSArrayM` 其实是循环缓冲 deque，两端 O(1) |
| [[nsdictionary-linear-probing]] | `__NSDictionaryI` = 开放寻址 + 线性探测 + indexed ivars 紧凑存储 |
| [[objc-runtime-internals]] | Modern Obj-C runtime：class cluster / non-fragile ivars / indexed ivars / lazy binding |
| [[binary-hot-reload]] | C++ 二进制热重载：DLL swap + 五道状态归属坑（memory/threads/fnptr/strings/structs） |
| [[rust-disassembly-tour]] | Rust 的 i128/解构/数组/iterator 在 Compiler Explorer 里到底变成了什么汇编 |
| [[x64-platform-tidbits]] | x86-64 C 提升规则坑与 PS3 PPU GCC 的指针 wrap 保守性；结构体 trick |
| [[x11-composite-redirection]] | X11 Expose 模型、COMPOSITE 扩展、Texture-from-Pixmap 与 unredirection 的合成链路 |
| [[wayland-compositor-model]] | Wayland compositor = display server，2000–3000 SLOC 取代 mutter 的 X 同步胶水 |
| [[bytecode-everywhere]] | ACPI / 字体 CFF / TrueType hinting / BPF / DWARF / VDBE——藏在系统里的字节码 VM 考古 |
| [[x11-pointer-barrier]] | XI 2.3 的 pointer barrier pressure：把"推屏幕边"从 timeout 升级为一等公民手势 |
| [[open-addressing-hashtable]] | Robin Hood 线性探测 + backshift 删除：Slater 的哈希表工程对照组 |
| [[undefined-behavior-c-cpp]] | C/C++ 未定义行为的三阵营分析、历史与治理策略（Raph Levien） |
| [[planar-rotation-dct]] | DCT 平面旋转的四种实现与 FMA 时代的优化观 |
| [[ppc-int-float-lhs]] | PPC 整浮点转换的 Load-Hit-Store 停顿与编译器 workaround |
| [[ring-buffer-virtual-stream]] | SPSC 环形缓冲区：数组索引 vs 虚拟流位置 |
| [[windows-bmp-format]] | Windows GDI 位图族考古：DIB / DDB / DIB Section / HBITMAP / stock bitmap |
| [[connection-multiplexer-gateway]] | 游戏服务器 N 对 1 连接汇聚网关的协议与实现 |
| [[snapshot-diff-persistence]] | 用快照差分把 MMO 全量存盘的 IO 压 90% |
| [[zeromq-messaging-patterns]] | ZeroMQ 的 req/rep、pub/sub、push/pull 三种消息模式 |
| [[parquet-vs-csv-json]] | 表格数据存储：为什么 CSV/JSON 都不够好、Parquet 凭什么成为默认 |
| [[insert-zero-bit-in-middle]] | 在值的中间插入 0 bit：`val + (val & top_mask)` 的 bit-twiddling 小品 |
| [[sign-extend-without-shift]] | 不用移位的符号/零扩展：`val - (val & sign_bit) * 2` |
| [[oodle-compression-suite]] | Oodle 三条产品线拆解：Data / Network / Texture，以及 PS5 尺寸缩水的真实原因 |
| [[mysql-charset-migration]] | MySQL 跨十年升级时 GBK → UTF-8 迁移；`--default-character-set=binary` 与混杂编码 dump 处理 |
| [[main-thread-task-injection]] | 给任务调度器开洞让主线程事件回调运行指定 coroutine |
| [[x86-simd-integer-multiplies]] | x86 SIMD 整数乘法指令的硬件演化史 |
| [[intel-13th-14th-gen-clock-degradation]] | Intel 13 / 14 代 CPU 时钟树退化的软件 work-around |
| [[jujutsu-vcs]] | Jujutsu VCS：Git-兼容但把 rewrite history 变成默认工作流 |
| [[magic-link-auth]] | Magic link 登录的陷阱清单（GET 预取、错 tab、phishing、flaky email、rate limit） |
| [[passkeys-webauthn]] | WebAuthn / passkeys 现状：conditional UI 让服务端复杂度陡升 |
| [[good-parallel-computer]] | Raph Levien 的一篇宣言：我们为什么还没有好的并行计算机 |
| [[gpu-queues-vs-dispatch-execution]] | 用队列串联 stages 对比 compute shader dispatch+barrier 模型 |
| [[gb10-memory-subsystem]] | Nvidia/Mediatek GB10（DGX Spark）CPU 侧五层缓存、双簇非对称、LPDDR5X 113 ns 实测 |
| [[cache-coherence-cross-cluster]] | 同簇 vs 跨簇一致性的两级延迟档位（DSU-120 Snoop Unit vs Coherent Fabric） |
| [[chipset-pcie-latency]] | 主板 chipset 对 PCIe 延迟/带宽的 500–900 ns 惩罚横测（AM5/Z890/Z170/AM3+） |
| [[split-lock-x86]] | 跨 cache line 原子操作在 7 代 x86-64 上的惩罚差异；Linux mitigation 的桌面争议 |
| [[llm-generated-c-compiler-perf]] | LLM 写的 C 编译器当压测负载：move elimination 与零延迟 store forwarding 是救生圈 |
| [[mono-jit-pipeline]] | Mono JIT 的五阶段管线与值类型导致的 400 行 `dot4` 之灾 |
| [[pointer-alias-analysis]] | 指针别名分析：几乎所有 load/store/copy 优化的前置条件 |
| [[dead-store-elimination]] | DSE 本质非局部，应集中到单一 pass——don't multiply the hard parts |
| [[gpu-gol-optimization-ladder]] | GPU Game of Life 优化阶梯：PyTorch 223 ms → bitpacked 64-bit CUDA + 多步融合 0.68 ms |
| [[numpy-tile-reshape-trick]] | reshape + transpose 切瓦片：比 for 循环快 1000×，比 scikit-image 快 15× |
| [[benchmark-methodology-end-to-end]] | 小 benchmark 不能代替端到端：矩阵测试、优化打开再测、2% 噪声阈值 |
| [[estrin-scheme]] | 代数重排 Horner 以缩短依赖链，给乱序 CPU 做并行多项式求值 |
| [[system-load-formula]] | 多子系统合成整体负载的公式（inverse product + average 混合） |
| [[vfx-multithreading-patterns]] | VFX 工具链把遗留代码改造成多线程 / 任务化的几类模式（Houdini / Presto / LibEE） |
| [[msi-hash-table]] | Mask-Step-Index 扁平 open addressing 哈希表 |
| [[wasm-pointer-sign-trap]] | Wasm 把整数视作有符号导致的指针截断陷阱 |
| [[wasmtime-py]] | bytecodealliance 的 wasmtime Python 绑定 |
| [[bump-allocator-wasm-guest]] | Wasm guest 端用 bump 分配器代替 malloc |
| [[monocypher-aead]] | Monocypher AEAD 接口及其 Wasm 包装 |
| [[u-config-frankenwine]] | 单个 exe 根据 Wine 检测切换 Windows/Linux 身份 |
| [[wine-linux-syscall]] | Wine 下 Windows 进程直接发 Linux syscall |
| [[lp64-vs-llp64]] | Unix 和 Windows x64 的 64 位数据模型差异 |
| [[fiber-cpp-basics]] | Jiayin Cao：fiber 动机、与 thread/C++20 coroutine 的差异、x64 System V ABI 上的最小实现 |
| [[a-metric-for-memory-fragmentation]] | 用 √Σf² / Σf 打分的内存碎片度量公式 |

| [[segment-array]] | 稳定指针 + 常数时间访问 + arena 友好的增长数组（Hooper / Per Vognsen） |
| [[build-process-visualization]] | 监听 fork/exec/exit 还原构建时间轴（What The Fork） |
| [[swift-dylib-hot-reloading]] | 120 行 Swift：用 dlopen 替代 Xcode Previews |
| [[mcm-gpu-design]] | MCM GPU：跨 die 互连代价、L1.5 缓存、CTA 调度与 first-touch 页映射 |
| [[cpu-gpu-platform-security-features]] | AMD/Intel/Nvidia 平台安全栈对比：SEV/SME/MxGPU vs TXT/CSME vs Falcon |
| [[electromigration-voltage-degradation]] | Black's Equation 与静态 OC vs 动态 Boost 的电压退化风险 |
| [[zen2-microarchitecture]] | AMD Zen 2 分支预测器、非调度 FP 队列与 L2 缓存的设计分析 |
| [[branch-predictor-design]] | CPU 分支预测器设计：预测惩罚、精度与前端带宽的权衡 |
| [[cpu-scheduler-design]] | CPU 后端调度器：统一 vs 分布式调度队列、非调度溢出缓冲 |
| [[gpu-memory-hierarchy-latency]] | GPU 多级缓存延迟实测：RDNA 2 vs Ampere vs 历代 Nvidia |
| [[tensorflow-1-graph-model]] | TF 1.x 两段式建图/执行模型——现代 ML 框架与 graph IR 的思想原型（历史页） |
| [[multi-gpu-training-replication-patterns]] | 多 GPU 训练的 tower + average-gradients 模板，对应今天的 DDP / all-reduce |
| [[deep-learning-uncertainty]] | DL「uncertainty」的分类学：calibration、parameter vs predictive、risk、MC dropout 质疑 |
| [[custom-allocator-interface]] | Bitsquid Allocator：抽象接口 + subsystem proxy + assert-on-leak |
| [[c-cpp-embed-binary-blobs]] | C/C++ 把资源文件嵌入可执行文件的三种做法（xxd、预处理器、`.incbin`） |
| [[function-vs-data-pointer-portability]] | glXGetProcAddressARB 返回函数指针而非 void*：C 标准不保证代码指针与数据指针等宽 |
| [[cgal-exact-arithmetic-mantissa-growth]] | CGAL 无限精度代数在深层构造下的尾数膨胀陷阱与精度重置 |
| [[cgal-arrangement-import-antennas]] | CGAL arrangement 导入脏多边形的三条路径与 antenna 对 toggle / winding 策略的破坏 |
| [[message-queue-thread-ownership]] | 消息队列作为线程所有权原语：数据访问权随消息流动，缩小 interleaving 状态空间 |
| [[external-data-inspector]] | Bitsquid 2011：跨平台外部 watch window 设想与 blob 描述 DSL |
| [[header-hero-compile-analysis]] | Bitsquid 2011：C++ include 图剖析工具与 Blowup Factor 指标 |
| [[link-exe-lnk4099-patch]] | 二进制 patch MSVC link.exe 让 LNK4099 可被 /ignore |
| [[shared-library-soname-versioning]] | Linux SONAME 的 ABI 契约与 OpenAL/X-Plane 翻车案例 |
| [[cross-platform-openal-runtime-loader]] | X-Plane 的 OpenAL 三平台装载：封装层 + dlopen fallback + 自带 LGPL 副本 |
| [[optimization-leverage-ratio]] | 优化杠杆率：局部改善 × 时间占比才是真正收益 |
| [[semaphore-vs-condvar-latency]] | pthread cond var vs semaphore+spinlock：X-Plane worker 唤醒 200→80 µsec |
| [[cas-refcount-lowbit-lock]] | CAS + refcount 的竞态缺口、指针低位当锁的自旋变体、Vyukov differential refcount |
## 游戏引擎（wiki/game-engines/）
Game Engine Architecture（Jason Gregory）的核心概念。

| 文章 | 一句话描述 |
|---|---|
| [[game-engine]] | 什么是游戏引擎 |
| [[data-driven-architecture]] | 引擎 vs 游戏专用软件的分水岭 |
| [[soft-real-time]] | 偶尔违反时限是可接受的 |
| [[engine-layering]] | 单向依赖是第一纪律 |
| [[unity-vs-unreal]] | 两种引擎设计哲学 |
| [[engine-evolution]] | 从 BSP 到 Lumen/Nanite |
| [[gknext-renderer]] | gameknife 2024 年启动的 Vulkan 实时光追开源引擎，YearOne 总结 |
| [[gkengine]] | gameknife 2013–2015 的跨平台独立引擎，CryEngine 风格，gkNextEngine 的前身 |
| [[game-physics-engine]] | 约束式刚体物理引擎的三段流水线：broadphase、collision detection、sequential impulse resolution |
| [[collision-detection-gjk-epa]] | 凸几何碰撞检测三件套：GJK 判相交、EPA 补 contact、MPR 一步到位 |
| [[component-entity-data-binding]] | 组件实体模型中的 I/O 端口式数据绑定（Evan Todd 2011） |
| [[game-engine-vfs]] | 游戏引擎虚拟文件系统：Linux VFS 简化版与 auto fallback |
| [[handle-based-resource-manager]] | C++/Vulkan 引擎里 manager + 32 位不透明句柄 + magic number 校验的资源管理范式 |
| [[game-resource-pack-format]] | 网易资源包 / 补丁格式与新引擎设想（云风） |
| [[scene-graph-matrix-stack-visitor]] | 场景图遍历：矩阵栈 + 访问者模式的组合拳 |
| [[ant-engine]] | 云风自研的移动端 3D 引擎，2024 年开源 |
| [[ltask-scheduler]] | Ant Engine 的低延迟任务调度器，与 skynet 的高吞吐路线对立 |
| [[mobile-energy-optimization]] | 手机游戏达到 60fps 之后如何继续做能耗优化 |
| [[ecs-particle-system-c]] | 云风的 C 版 ECS 粒子系统：属性聚合、cache 友好、分支消除 |
| [[gameplay-layering-object-actor]] | gameplay 三层切分 + Object / Actor 双类，持久化优先级最高 |
| [[immediate-vs-retained-mode]] | 立即模式 vs 保留模式：表现层对接数据模型的两种范式 |
| [[ecs-data-oriented-revert]] | 把 ECS 回归面向数据的原始设计，剥离辅助模块——云风 2024 对 Ant 的反思 |
| [[engine-thin-wrapper-per-genre]] | 按游戏类型做薄封装框架，隔离底层引擎缺陷 |
| [[mod-first-engine-evolution]] | 异星工厂模式：官方扩展即 Mod，核心系统围绕 Mod API 进化 |
| [[agent-state-sync-broadcast]] | Agent 状态同步的广播机制与拷贝优化（云风 Erlang 服务器） |
| [[soluna-2d-engine]] | 云风的 Soluna：面向策略类游戏的 2D 框架 |
| [[playcanvas-engine-2-breaking-changes]] | PlayCanvas Engine 2.0：一次 major bump 的工程学（cruft 清理 + WebGPU 铺路） |
| [[playcanvas-react-declarative]] | PlayCanvas React：把 PlayCanvas ECS 包成 JSX 的声明式 3D 绑定 |
| [[skynet-lua-sharetable-patch]] | skynet 跨 VM 共享函数原型的 Lua patch 与 5.5 external strings 展望 |
| [[playcanvas-esm-scripts]] | PlayCanvas 新脚本系统：`.mjs` + class + `@attribute` JSDoc，替代 Classic Scripts 的 hidden global |
| [[zero-bind-gpu-resource-management]] | Bindless + BDA + PushConstant 实现零绑定的现代 GPU 资源管理 |
| [[slang-shader-language]] | NVIDIA 主推的现代着色器语言：泛型、模块、自动微分 |
| [[ue4-editor-battery-throttle]] | UE4 编辑器电池模式 60 FPS 硬限制与 r.DontLimitOnBattery |
| [[ue4-common-perf-pitfalls]] | Allar 救火现场反复出现的 UE4 工程陷阱清单 |
| [[svelto-ecs]] | 平台无关 C# ECS 框架：group 模型、显式 composition root、ECS-centric 多范式 |
| [[ecs-abstraction-layers]] | Svelto 的 ECS 分层封装方法论：asmdef 单向依赖 + 依赖倒置 + Hollywood Principle |
| [[svelto-filters-api]] | 跨 group 的 entity 子集索引：transient / persistent filter，取代 event / publisher-consumer |
| [[svelto-on-dots]] | Svelto 接管 DOTS 调度、把 DOTS ECS 当作引擎库而非游戏框架 |
| [[ecs-on-gpu-computesharp]] | 用 ComputeSharp 把 Svelto component 存到 GPU buffer、engine 以 compute shader 形式跑 |
| [[native-client-porting]] | AirMech 移植到 NaCl 的工程笔记（archival，可迁移到 Emscripten） |

| [[mach-engine]] | Mach：Zig 写的模块化游戏引擎，核心是标准库式组件 |
| [[scene-graph-unnecessary-in-engine]] | Pesce：3D 引擎不该把场景图当核心，应按 renderable 类型特化 |
| [[game-engines/flashpunk-framework]] | FlashPunk：ActionScript 3 轻量 2D 游戏框架，Entity/World/Grid 架构分析 |
| [[bitsquid-task-scheduler]] | Bitsquid 2010 年的任务调度器：开放表、单依赖 + 子任务、global queue |
| [[offset-based-resource-blobs]] | 用 offset 而非 pointer patch 做二进制资源 blob |
| [[decoupled-tool-engine-json-rpc]] | 工具与引擎解耦：用 JSON 消息走网络协议 |
| [[per-entity-scene-graph]] | Bitsquid：场景图不覆盖整场景，只挂一个 entity 内部 |
| [[dual-mode-gui-bitsquid]] | Bitsquid 用同一 API 同时支持 retained / immediate GUI |
| [[flow-graph-data-oriented-runtime]] | Bitsquid Flow：可视化脚本的数据导向 runtime |
| [[dependency-checker-tool]] | Bitsquid 500 行工具：资源依赖图与 replace/move/copy |
| [[memory-corruption-bug-hunting]] | Bitsquid：release-only / 平台相关 / 低复现率的内存破坏 bug 系统化狩猎流程 |
| [[game-monitoring-event-buffer]] | 游戏监控：TLS event buffer + 在线/离线 visualizer |
| [[id-lookup-table-packed]] | Bitsquid 2011 ID→Object 查找的三级演化：STL / array-with-holes / packed array |
| [[animation-stream-cache-layout]] | Bitsquid 动画数据的流式 cache 布局：active 数组 + 时间排序流 |
| [[platform-specific-resources-property-system]] | Bitsquid property 机制：文件名段统一处理平台/本地化/业务变体 |
| [[ragdoll-velocity-inheritance]] | 角色切 ragdoll 瞬间把动画速度传进物理：last_world 方案与四种候选对比 |
| [[pesce-2010-engine-layer-sketch]] | Pesce 2010 年社区协作引擎分层草图：六层结构 + DevOps 摆首层 |
| [[vector-field-bytecode-vm]] | Bitsquid 向量场：外循环指令 / 内循环数据的向量化字节码 VM |
| [[bitsquid-foundation-library-concept]] | Bitsquid 2012 开源的最小引擎基座：allocator + 反 STL 集合 |
## 实时渲染（wiki/rendering/）
Real-Time Rendering + Custom SRP 的渲染管线知识。

| 文章                                    | 一句话描述                                                              |
| ------------------------------------- | ------------------------------------------------------------------ |
| [[rendering-pipeline]]                | 四阶段的瓶颈驱动并行系统                                                       |
| [[bottleneck-analysis]]               | 找瓶颈只优化瓶颈                                                           |
| [[tbdr-vs-imr]]                       | 两种 GPU 架构对比                                                        |
| [[draw-call]]                         | CPU 状态 setup 是主成本                                                  |
| [[culling]]                           | 分层过滤的 CPU 剔除                                                       |
| [[batching]]                          | 减少 DrawCall 或状态切换                                                  |
| [[mvp-transform]]                     | 三矩阵变换链                                                             |
| [[coordinate-spaces]]                 | Model/World/View/Clip/NDC/Screen                                   |
| [[z-buffer]]                          | 每像素深度缓冲                                                            |
| [[z-fighting]]                        | 深度精度不足的闪烁                                                          |
| [[reversed-z]]                        | 利用 float 精度分布改善远平面                                                 |
| [[perspective-correct-interpolation]] | 透视校正插值                                                             |
| [[rasterization]]                     | 三角形 → fragment                                                     |
| [[aliasing]]                          | 走样与反走样                                                             |
| [[msaa-ssaa]]                         | 两种超采样对比                                                            |
| [[triangle-primitives]]               | 三角形为什么是基本图元                                                        |
| [[fragment-shader]]                   | 每 fragment 的着色                                                     |
| [[early-z-late-z]]                    | 早期/晚期深度测试                                                          |
| [[hsr-tbdr]]                          | TBDR 特有的精确隐面消除                                                     |
| [[alpha-blending]]                    | 半透明混合的顺序依赖                                                         |
| [[stencil-buffer]]                    | 8-bit 模板缓冲的低成本效果                                                   |
| [[overdraw]]                          | 过度绘制的代价与对策                                                         |
| [[deferred-rendering]]                | G-Buffer + 统一光照 pass                                               |
| [[color-space]]                       | RGB 值无意义——色彩空间才赋予意义                                                |
| [[alpha-compositing]]                 | Porter-Duff over 与预乘 α                                             |
| [[pinhole-camera]]                    | 虚拟相机的物理本体与 cos⁴ 暗角                                                 |
| [[thin-lens-model]]                   | 焦距 / 光圈 / 景深 / bokeh 的物理来源                                         |
| [[local-tonemapping]]                 | 局部色调映射的动机与方法谱                                                      |
| [[exposure-fusion]]                   | Mertens Laplacian 金字塔分尺度融合算法                                       |
| [[laplacian-pyramid]]                 | 多分辨率图像分解的基础工具                                                      |
| [[iir-filter-deconvolution]]          | 递归滤波器精确反演卷积模糊                                                      |
| [[poisson-disk-sampling]]             | 渐进 Poisson 采样序列与渲染用途                                               |
| [[gpu-printf-debugging]]              | 用 UAV append buffer 实现 shader printf                               |
| [[unorm-float-conversion]]            | UNORM8 → float32 的精确两乘法构造                                          |
| [[sampling-theorem-sinc]]             | sinc 是无穷节点 Lagrange 插值的极限                                          |
| [[pineda-edge-rasterization]]         | 1988 年的边方程算法是现代 GPU 光栅化的根                                          |
| [[hierarchical-rasterization]]        | 用 tile 角点上下界提前剔除空块                                                 |
| [[triangle-setup]]                    | 光栅化前为边方程算常量的硬件阶段                                                   |
| [[compute-vs-raster-points]]          | 朴素 compute shader 比硬件点光栅化快 1.5-10×                                 |
| [[image-resampling-filters]]          | Bilinear / Bicubic / Mitchell-Netravali 与半 texel 偏移考古              |
| [[cached-shadowmaps]]                 | 级联阴影的帧间相干性缓存                                                       |
| [[temporal-antialiasing]]             | TAA 的 jitter + reprojection + rectification 全流程                    |
| [[motion-vectors]]                    | 屏幕空间运动矢量——所有 temporal 技术的基础                                        |
| [[taa-history-rectification]]         | color clamping 与 depth/stencil/velocity rejection 的组合拳             |
| [[tiled-light-prepass]]               | ROTR Foundation 引擎的 thin G-Buffer + 二次几何提交方案                       |
| [[hbao-interleaved-sampling]]         | 把 HBAO 拆成 16 个 4×4 块并行、再 blur 合并的 cache-friendly trick             |
| [[depth-aware-upsampling]]            | 用 stencil 分派 simple/complex shader 的半分辨率 upsample                  |
| [[fizzle-lod-fading]]                 | 用 discard 噪声替代 alpha blending 的 LOD 过渡方案                           |
| [[volumetric-fog-froxels]]            | frustum-aligned 3D 格网上的 compute-based 体积光流水线                       |
| [[spectral-rendering]]                | 光谱渲染：把 RGB 三元组换成波长积分的现代实时方案                                        |
| [[fourier-srgb-spectral-upsampling]]  | Fourier sRGB：sRGB 纹理到反射率谱的 BC1 可压缩上采样                              |
| [[hero-wavelength-spectral-sampling]] | 波长分层抖动 + 光源谱 CDF LUT 的 MC 采样策略                                     |
| [[spectral-brdf]]                     | 「base color + 纯白」两个权重把 PBR BRDF 改造成光谱 BRDF                         |
| [[polynomial-root-finding-gpu]]       | GLSL 里的 bracketed Newton bisection 实现与高度优化                         |
| [[register-spilling-avoidance]]       | shader 寄存器溢出的识别与系统化规避手册                                            |
| [[projected-solid-angle-sampling]]    | 球形面光源 + 漫反射表面的实时零方差采样（cut disk 分解）                                 |
| [[environment-probe-placement]]       | 反射探针辅助放置：候选生成 + 相似度聚类 + 美术挑选                                       |
| [[quasi-monte-carlo]]                 | 确定性点列换近线性收敛的 QMC 基础                                                |
| [[stratified-sampling]]               | 分层采样：便宜的负相关方差缩减                                                    |
| [[low-discrepancy-sequence]]          | Halton / Sobol 等 QMC 常用点列                                          |
| [[greedy-voxel-meshing]]              | Minecraft 风 voxel 世界的经典网格化算法                                       |
| [[voxel-ambient-occlusion]]           | mesh 阶段烘焙四级 AO 的免费方案                                               |
| [[compact-vertex-format]]             | 每顶点 8 字节的位打包技巧                                                     |
| [[spherical-harmonics]]               | 球面上的 Fourier 基：L2 压掉整张 diffuse envmap                              |
| [[jump-flooding-algorithm]]           | GPU 距离场：对数趟指数步长的 3×3 洪填                                            |
| [[oklab-color-space]]                 | 两次矩阵乘一次立方根得到的感知均匀色彩空间                                              |
| [[3d-rotation-math]]                  | Euler / Axis-Angle / 四元数：3D 旋转的数学形式                                |
| [[exponential-map-rotations]]         | 矩阵指数 / 对数统一四种旋转表示，给出 slerp 等价物与 Karcher mean 平均算法                       |
| [[render-textures-unity]]             | Unity 的 GPU-side 中间贴图：color format 命名规范与 AsyncGPUReadback 异步回读                |
| [[triplanar-mapping]]                 | 三轴平面投影 + 法线加权混合：解决程序化几何 / 大物体的 UV 拉伸                                            |
| [[orthographic-depth]]                | 正交相机的 Scene Depth：buffer 本身线性 + 平台差异 + 深度差/世界坐标重建的正交版                          |
| [[watercolour-shader-experiments]]    | Cyan 的水彩观感三层 shader：mesh + Blit 后处理 + 假 decal                                  |
| [[layered-grid-noise]]                | 黄金角旋转 + 多层 shift/scale 的廉价伪随机散布                                    |
| [[shadow-mapping-basics]]             | Shadow mapping 入门：hard / soft / bias / PCF / Phong                 |
| [[microfacet-brdf]]                   | $D\,F\,G$ 微表面 BRDF + 多次散射能量补偿                                      |
| [[physically-based-shading]]          | PBR 着色的整体框架与 SIGGRAPH course 脉络                                    |
| [[normal-map-blending]]               | Reoriented Normal Mapping：最短弧四元数混合法线贴图                             |
| [[occlusion-culling]]                 | HZB 查询 vs SPU 软光栅：两种动态遮挡剔除方案                                       |
| [[hierarchical-z-buffer]]             | max-downsample 的 Z 金字塔：保守遮挡查询                                      |
| [[d3d12-resource-binding]]            | D3D12 的描述符、堆、资源状态跨线程管理四件套                                          |
| [[needlets]]                          | 球面 wavelet 基，SH 遮挡振铃问题的替代方案                                        |
| [[procedural-rendering-ps2]]          | PS2 VU + DMA chain 的过程式几何管线                                        |
| [[display-edid-colorspace]]           | 从 EDID 读出显示器原生 primaries + 白点                                      |
| [[custom-srp]]                        | Catlike Coding 教程系列                                                |
| [[scriptable-render-pipeline]]        | Unity 的可编程渲染管线                                                     |
| [[render-graph]]                      | SRP 的声明式编排系统                                                       |
| [[color-lut]]                         | color grading 查找纹理                                                 |
| [[debug-visualization]]               | Rendering Debugger 集成                                              |
| [[gpu-image-editor-brush]]            | GPU 图像编辑器的缩放平移 + fragment shader 笔刷（Papaya vs GIMP）                |
| [[gpu-hazard-tracking]]               | D3D12/Vulkan 为何要求用户自己声明 barrier                                    |
| [[gpu-fence-timeline-semaphore]]      | GPU→CPU 单调计数器作为资源生命周期基础设施                                          |
| [[buffer-renaming]]                   | 老驱动的隐式 buffer 版本化与现代 API 的拆除                                       |
| [[frame-profiler-overlay]]            | 帧内性能剖析器浮层：即开即看的一帧耗时分解                                              |
| [[volumetric-video-playback]]         | 体积视频（全息视频）在 WebXR 跨设备回放的工程实践                                       |
| [[shaping-functions]]                 | step/smoothstep/lerp/sin/frac 等着色器塑形函数与时间动画                        |
| [[planar-mapping]]                    | 用顶点位置的两个分量直接当 UV：最简单的程序化 UV 生成                                     |
| [[texture-dissolve]]                  | 纹理驱动的 clip 溶解 VFX + HDR 边缘发光                                       |
| [[sdf-2d-primitives]]                 | 2D SDF 基元（圆、矩形）、空间变换与可视化                                           |
| [[sdf-ray-marched-shadows]]           | 用 SDF sphere-trace 做 2D 软阴影：iq 单行技巧的完整拆解                           |
| [[draw-procedural-gpu]]               | Unity Graphics.DrawProcedural：GPU-driven 渲染的最小入口                   |
| [[urp-volume-post-processing]]        | URP 基于体积的后处理系统（PPv3）的架构与使用                                         |
| [[blit-render-feature]]               | 在 URP 无扩展点时通过 ScriptableRendererFeature 做自定义全屏后处理                  |
| [[uv-manipulation-nodes]]             | Shader Graph 中 Tiling/Offset、Rotate、Flipbook、Polar 等 UV 操作节点       |
| [[sampler-filter-wrap-modes]]         | 纹理采样器的 Point/Linear/Trilinear 与 Repeat/Clamp/Mirror 的语义与陷阱         |
| [[crt-shader-effects]]                | 把复古 CRT 拆解为 5 个正交 shader trick 的 breakdown                         |
| [[scene-color-depth-nodes]]           | Shader Graph 里 Scene Color / Scene Depth 节点的跨管线行为与深度相交技术           |
| [[particle-custom-vertex-streams]]    | 通过 TEXCOORD 把 AgePercent / StableRandom / Custom Data 传进 shader    |
| [[shader-vector-math-primer]]         | Shader 需要的那点向量数学：dot/cross/normalize 的几何直觉                         |
| [[unity-grabpass-blur]]               | Unity GrabPass + 可分离 Gaussian blur 的入门实现与教学取舍                      |
| [[texture-encoded-state]]             | 把 per-pixel 状态（时间戳/强度）编码进纹理通道供 shader 消费                           |
| [[diamond-square-noise]]              | Diamond-Square 有状态噪声与 compute shader 加速实现                          |
| [[deferred-grass-shader]]             | 延迟管线下的草地方案：alpha cutout + tessellation + geometry shader           |
| [[diffuse-lighting-lambertian]]       | Lambert 漫反射：所有光照模型的共同基座与 Unity 的两条实现路径                             |
| [[unity-surface-shaders]]             | Unity 内建管线的 Surface Shader 抽象：填 surf 函数，Unity 生成所有变体               |
| [[shaderlab-hlsl-basics]]             | URP shader 的 ShaderLab + HLSL 两层结构最小骨架                             |
| [[retro-rendering-techniques]]        | PS1/N64 复古渲染清单：顶点吸附、色深量化、3-point 采样、vertex lit                     |
| [[dither-alpha-clipping]]             | 用 Bayer 矩阵 discard 伪造半透明，规避 alpha blending 的排序地狱                   |
| [[spectral-zucconi-rainbow]]          | Branchless 的波长→RGB 拟合（Zucconi 改进 GPU Gems bump 方案）                 |
| [[diffraction-grating-shader]]        | CD-ROM 彩虹反射：grating 方程 + 从 UV 算切向 + spectral_zucconi6              |
| [[fast-translucency-wraplight]]       | Barré-Brisebois / Frostbite 2 的廉价假 SSS：反向光 + subsurface distortion |
| [[volumetric-raymarching-intro]]      | Volumetric raycasting 到 raymarching：把 cube 当 portal 做体积渲染          |
| [[journey-sand-specular]]             | Journey 沙丘高光分解：Fresnel rim + Blinn-Phong ocean specular            |
| [[visibility-buffer]]                 | 用 thin-gbuffer + 反查替代传统 G-Buffer，化解高 overdraw 代价                   |
| [[hybrid-raytracing-pipeline]]        | VB primary + 短距离硬件光追 secondary + cache 远场                          |
| [[bindless-rendering]]                | CPU 只组织 GPU 只索引，让着色器自由访问任意资源                                       |
| [[analytical-antialiasing]]           | 已知形状数学方程时，在 shader 里按 SDF 淡出一像素的反走样                                |
| [[metal-api-overview]] | Metal 的对象模型：device/queue/buffer/encoder/library/pipeline-state |
| [[metal-shading-language-basics]] | MSL 函数限定符、属性限定符与插值语义的最小讲义 |
| [[cametal-layer-drawable]] | CAMetalLayer / CAMetalDrawable——iOS 上 swapchain 的 Core Animation 版本 |
| [[prebaked-corner-occlusion]] | SSAO 之前的角落遮蔽：lightmap 烘焙、UE1 的 bug 成为 feature、Sims 4 手贴 AO mesh |
| [[painted-foliage-bent-planes]] | Diablo 3 两张三角形 + hand-painted alpha 做细剪影树，固定相机反哺美术技巧 |
| [[normal-decal-edge-blending]] | Fallout 3 / CryEngine 的 decal 壳技巧：把破损边缘从主 mesh 解耦到一层薄几何 |
| [[chromatic-aberration-post]] | 三通道 UV 偏移后处理：真实色差 vs 数字 glitch，Teleglitch / Deadlight 案例 |
| [[color-banding]]                     | 色带根源 + Jimenez 一行 GLSL dither + 大厂去带方案横评                            |
| [[perceptual-colormaps]]              | matplotlib 感知均匀 colormap 烘成 .cube 1D LUT 给 DaVinci Resolve |
| [[tangent-free-normal-mapping]] | 用 `dFdx`/`dFdy` 在 pixel shader 里构造 TBN，免顶点存切线 |
| [[shader-prototyping-tools]] | FX Composer / RenderMonkey / Unity / SharpDX 原型工具横评 |
| [[sharpdx-assimp-pipeline]] | C# + D3D11 的 XNA 式原型：SharpDX + Assimp 模型加载 |
| [[conservative-depth]] | `SV_DepthGreaterEqual` / `[earlydepthstencil]`：两条 Early-Z 救援通道 |
| [[virtualized-volume-textures]] | Karis：2D 虚拟纹理和 SVO 思路扩展到 irradiance volume |
| [[tiled-light-culling]] | Karis：把 specular cone + 能量守恒引入 tile 级光源剔除 |
| [[sparse-shadows-cone-tracing]] | Karis 2012：diffuse 走 shadow map，远 specular 走 cone trace——UE5 Lumen 的起点笔记 |
| [[instant-radiosity-vpl]] | Instant Radiosity 与虚拟点光源（RSM 版） |
| [[parallax-corrected-cubemap]] | 视差修正 cubemap 与非专烘焙 cubemap 的 BoxScale 修正 |
| [[vertex-vector-interpolation-artifact]] | 归一化 view/light 向量在大三角形上的插值陷阱 |
| [[dual-depth-buffer-thickness]] | Min 混合在单 pass 里求物体厚度的 ShaderX6 技巧 |
| [[deferred-alpha-lighting]] | Deferred 渲染下给透明物打光的四条路 |
| [[moment-shadow-mapping]] | 四阶矩 + Hausdorff 矩问题闭式解的可过滤硬阴影；2016 扩展到体积/软阴影/半透明 |
| [[trigonometric-moment-transient-imaging]] | 三角矩问题闭式解把 AMCW lidar 的瞬态成像推到瞬态视频级速度 |
| [[screenspace-reflections]] | Wronski 的 SSR 落地复盘：三类先天缺陷与稳定化技术栈 |
| [[temporal-supersampling]] | 把超采样分摊到连续多帧的一般化框架，TAA 是其特例 |
| [[pcg3d-hash]] | GPU 友好的 3D→3D 整数哈希，替换 1997 年的 Jenkins Lookup3 |
| [[worley-voronoi-noise]] | Worley / Voronoi 噪声节点的原理与哈希依赖 |
| [[lossless-float-image-compression]] | 多层浮点图像的无损压缩评测：EXR vs JPEG-XL vs meshoptimizer |
| [[openexr-format]] | OpenEXR 格式、压缩模式与官方库 vs tinyexr 选型 |
| [[gpgpu-string-unescaping]] | 状态机作为 monoid 同态：parallel prefix scan 并行化 JSON 字符串反转义 |
| [[gpgpu-json-parsing]] | Dyck 语言的 scan + scatter + sort 流水线：把 JSON 括号结构搬到 GPU 并绕过栈 |
| [[cellular-texture-generation]] | ryg 的 Werkkzeug3 细胞纹理离线生成：为什么树最慢、spatial subdivision 为什么最快 |
| [[floyd-steinberg-dithering]] | Floyd–Steinberg 误差扩散 dither 与 JVM 上的四步优化 |
| [[texel-pixel-conversion]] | 纹素与像素之间的换算 |
| [[ping-pong-surfaces]] | 两张 surface 跑任意多趟 shader |
| [[shader-code-golfing]] | shader 代码压缩的技巧与等式 |
| [[vector-dot-product]] | 点乘作为条纹 / 衰减 / Lambert 的瑞士军刀 |
| [[creative-coding-process]] | Xor 的灵感 → 原型 → 打磨 → 迭代工作流 |
| [[bezier-curve-triangulation]] | 用切线法线 + hyperbola 段数把 Bézier 曲线描边交给 GPU 三角形 |
| [[bluk-2d-fog-sprite-shader]] | BLUK 风格的距离相关 2D 雾精灵着色器 |
| [[unity-image-effect-basics]] | Unity built-in 管线的 image effect 全屏后处理骨架 |
| [[night-time-tint-shader]] | 饱和/蓝偏/变暗三合一的夜色全屏后处理 |
| [[image-effect-colour-transform]] | 逐像素 RGB 线性变换：灰度、Sepia、色调矩阵 |
| [[depth-texture-silhouette]] | 采样 `_CameraDepthTexture` 按距离着色做剪影/距离雾 |
| [[image-convolution-kernel]] | 图像卷积核的数学骨架与 fragment shader 写法 |
| [[separable-gaussian-blur]] | Box/Gaussian Blur 的可分离优化与多 pass 模板 |
| [[md5-model-format]] | id Software 的纯文本骨骼动画格式（.md5mesh + .md5anim），骨骼蒙皮教学的事实标准 |
| [[gpu-skinning-matrix-palette]] | 矩阵调色板蒙皮：把骨骼变换搬进 vertex shader，每帧只传 palette 不传顶点 |
| [[bresenham-lines]] | 1962 年的整数直线算法，tile-grid 上的经典工具 |
| [[variable-length-bresenham]] | 支持"从起点沿方向走 range 步"的展开版 Bresenham |
| [[performance-conscious-webgl]] | WebGL 实例化渲染中的三个 JS 性能陷阱（Float32Array.set / 字符串 key / super） |
| [[gpu-driven-grass-tiles]] | Marco Giordano：蓝噪声预烘焙 + vertex 扩展 + compute culling + 间接绘制的 GPU 驱动草地方案 |
| [[cubic-equation-solver-hlsl]] | Peters 的 ~30 行 HLSL 三次方程闭式求解（三实根专用，2× Blinn 速度） |
| [[non-linearly-quantized-msm]] | 非线性量化 MSM：64/32 bit + on-chip compute Gaussian filter（HPG 2017） |
| [[directx11-early-pitfalls]] | DX11 早期开发踩坑：tessellation / compute / HLSL 工程笔记 |
| [[homogeneous-rasterization-transpose-bug]] | 齐次坐标三角形光栅化中 setup 矩阵被转置导致的 z 插值 bug |
| [[opengl-loader]] | OpenGL 为何不能静态链接，及手写 X-macro loader 的取舍 |
| [[tangent-space-normal-mapping]] | 切线空间 TBN 推导 + parallax / steep / POM 视差家族 |
| [[normalised-blinn-phong-shader]] | Anagnostou 给美术的归一化 Blinn-Phong 教学 shader：能量守恒 / Fresnel / gloss 线性化 / Toksvig AA |
| [[divergent-gradient-in-branches]] | if 分支里 shader-computed uv 的 tex2D：编译器静默展平、如何修 |
| [[tessellation-fur-rendering]] | D3D11 isoline domain 的 64×64 毛发生成 + master strand 插值 + Phone Wire AA |
| [[skysaga-rendering-tech]] | SkySaga/Meandros 引擎总览：token stream、deferred PBR、voxel AO、G-Buffer 天气、3D LUT |
| [[image-effect-mask-blend]] | 灰度遮罩混合：把全屏后处理限制到画面局部 |
| [[uv-displacement-image-effect]] | UV 位移后处理：冲击波 / 水波 / 折射的统一抽象 |
| [[scatter-bokeh-dof]] | _The Witcher 2_ 的散射式 bokeh 景深：点精灵 + vertex shader 放大 + premultiplied additive 累加 |
| [[view-frustum-culling-ryg]] | ryg 的 AABB-vs-frustum 方法链：从 8 顶点到 SPU ≈24 cycle/box 的 SIMD p/n-vertex |
| [[hlsl-derivation-correctness]] | 写完 shader 数学后的 5 分钟检查单：对称性 / 避角度 / 反三角恒等式 / 避数值微分 |
| [[sobel-edge-detection]] | Sobel-Feldman 算子：屏幕空间边缘检测与 Neon 掩膜 |
| [[bloom-threshold-blur-composite]] | 简易 Bloom 三步：阈值 + 模糊 + 合成，UsePass 跨 shader 复用 |
| [[color-quantization-retro]] | NES/SNES/GB 色彩量化 + 像素化下采样 + FilterMode.Point |
| [[kuwahara-filter]] | Kuwahara 保边非线性滤镜：油画/笔刷风格化 |
| [[sprite-shaders-unity]] | Unity sprite shader：Cull Off + 顶点色 + 透明三件套 |
| [[shader-color-interpolation]] | shader 颜色插值：加法错误、凸组合、`lerp` 与 mask-driven 混合 |
| [[procedural-checkerboard]] | 程序化棋盘：`floor + frac*2` 量化 → 奇偶 → 多维求和 |
| [[raymarching-intro]] | Xor：sphere-assisted ray marching 的 SDF 入门 |
| [[two-texture-sampling-tricks]] | Xor：texture atlas 下的 UV 归一化与跨贴图映射 |
| [[shadertoy-basics]] | Xor：ShaderToy 格式与移植到游戏引擎的清单 |
| [[fractal-texturing]] | Xor：按深度离散缩放并 blend 的一致 LOD 技巧 |
| [[color-quantization-kmeans]] | K-Means 从图像提取 k 个主色 + silhouette 自动选 k |
| [[custom-mask-shaders]] | Alisavakis：in-shader 圆盘 / 圆环 SDF mask 的最小实现 |
| [[shockwave-effect]] | Alisavakis：圆环 mask × UV 位移做 2D 冲击波命中反馈 |
| [[stencil-portal-shader-antichamber]] | Alisavakis：用 stencil buffer 复刻 Antichamber 的「窗口可见」物体 |
| [[procedural-greeble]] | n 边形 polygon extrusion + 随机 length 生成科幻 mesh 表面细节 |
| [[stylized-water-shader]] | camera depth texture 差 + 顶点噪声 sin 波动的卡通水面 |
| [[cel-shader-outline]] | ramp 纹理硬色阶光照 + 法线 extrude + stencil mask 描边 |
| [[unity-postprocessing-adventures]] | Kostas：Unity 低层 API 搭体积光束后处理 pipeline（2015） |
| [[unreal-frame-breakdown]] | Kostas：UE4.17 默认 deferred 管线的 RenderDoc 逐 pass 拆解（三篇合一） |
| [[gpu-based-occlusion-culling]] | Kostas：DX11 GPU-driven HZB + stream compaction + indirect draw 的 retrofit |
| [[sprite-outline-8-direction]] | 八方向位移实现的 2D sprite 描边 |
| [[extruded-wall-shadow-viewcone]] | Teleglitch 式径向外推墙面伪造视野阴影 |
| [[animated-parallax-cloth-fold]] | Deus Ex 风旗——动画 parallax + 低分辨率 noise 伪造布料褶皱 |
| [[mipmap-moire-scanline]] | 故意放弃 mipmap / 用 moiré 伪造 CRT 扫描线 |
| [[lit-sphere-matcap-shading]] | Lit Sphere / MatCap——把光照响应烘进一张球面查找表 |
| [[metal-3d-rendering-pipeline]] | Metal 最小 3D 渲染管线：OBJ + MVP uniform + vertex descriptor + depth state + Blinn-Phong |
| [[metal-texture-sampler]] | Metal 的 MTLTexture / MTLSamplerState 与 MSL constexpr sampler 两种写法 |
| [[metal-compute-image-filter]] | 用 Metal compute kernel 做图像滤镜链（thread_position_in_grid / 懒求值 provider 协议）|
| [[neural-graphics-primitives]] | 神经图形原语：MLP + 位置编码 / Instant NGP 哈希编码把图像/SDF/NeRF 全部写成 coord→value |
| [[spherical-integration]] | 球面积分里的 $\sin\theta$ 从何而来：参数化 + 叉积 + 第一基本形式 |
| [[hybrid-hair-rendering]] | Wronski 的混合 deferred/forward 头发 trick：按 alpha 阈值把发丝拆成实心 + 边缘两段分别处理 |
| [[valve-ambient-cube]] | Valve HL2 的六方向常数环境光，SH 的穷人替代 |
| [[deferred-sdf-rendering]] | Kostas Anagnostou：把 SDF raymarch 结果写进 Unity G-Buffer + SV_Depth，让 SDF 与多边形在 deferred 管线共存 |
| [[multidraw-indirect-occlusion-culling]] | GPU-driven 剔除 Part 2：NVAPI MultiDraw + mesh LOD + programmable vertex fetch + 批量化一切的 DX11 retrofit |
| [[hybrid-raytraced-shadows-reflections]] | Kostas Anagnostou：compute shader 手写 BVH hybrid raytracer 做硬阴影与镜面反射的早期全景实验 |
| [[cel-shading-pipeline]] | Daniel Ilett 5 部曲：Phong 光照 → 量化 diffuse/specular → bump+fresnel → stencil 描边 → ramp 纹理 |
| [[random-stripes-mask-shader]] | `floor + hash + step` 生成行级随机条纹 mask，作为 glitch / CRT 效果的积木 |
| [[glitch-image-effect]] | 两套随机条纹 mask + 波浪位移 + 色差的 Unity glitch 后处理，含单旋钮控制器 |
| [[abzu-portal-cards-shader]] | ABZÛ 里按相机距离 fade 的透明贴片：兼具远景美化和玩家引导 |
| [[world-screen-space-position-shader]] | Unity shader 里拿 worldPos / screenPos 的四种模板（v/f × surface） |
| [[texture-swizzle-nested-tiling]] | 纹理 swizzle 与嵌套分块的「减-与」通用地址增量 |
| [[animated-dotted-outline-shader]] | `sin(distance) + clip` + `_Time` 相位平移的动画虚线描边（Linden Reid） |
| [[ice-shader-unity]] | Fresnel 边缘 + noise-as-normal + GrabPass 扭曲的冰晶 shader（Linden Reid） |
| [[waving-grass-shader-vertex-offset]] | 世界空间采样风场驱动的 sin/cos 顶点位移草叶动画（Linden Reid） |
| [[surface-angle-silhouette]] | 基于 `1 - abs(dot(V, N))` 的延迟管线后处理剪影，兼带 camera-ray 反投影套路 |
| [[classic-shader-noise]] | 经典噪声家族（hash/value/Perlin/Worley/Voronoi/fBm）在同一手写骨架下对比 |
| [[env-mapping-cubemap-shader]] | 无 cubemap 环境下用等距柱状 HDRI 做天空盒与反射的 shader 写法 |
| [[dynamic-resolution-scaling]] | 变分辨率渲染：统一缩放 + stretch blit + 锐化补偿，降像素计算量的经典手段 |
| [[godot-visual-shaders]] | Daniel Ilett 把 Unity Dissolve/Hologram/Hull Outline 迁到 Godot VisualShader，对比两个可视化编辑器的抽象哲学差异 |
| [[shader-graph-lighting-primer]] | Shader Graph Lit 输出栈速览：Base Color/Normal/Metallic/Smoothness/Emission/AO 的槽位含义与贴图陷阱（roughness↔smoothness 翻转）|
| [[mgs-stealth-camo-shader]] | MGS 潜行迷彩复刻：URP Opaque Texture + Scene Color + Simple Noise remap 偏移 Screen Position 的最短『透过物体看背景』骨架 |
| [[pokemon-terastallize-shader]] | Pokémon 太晶化复刻：DDX/DDY 叉积重建 flat normal + 贴图烘 Triangle ID + HSV 随机反射色 |
| [[multiple-render-targets]] | MRT：一次 draw 写多张附件，G-Buffer / Object ID / 自建 depth 的硬件前提 |
| [[mipmap-generation-sampling]] | Mipmap 的 LOD 选择机制与 `texture2D` bias 参数的廉价 blur 用法 |
| [[webgpu-intro]] | WebGPU/WGSL 入门：跨平台 + 显式 pipeline + 原生 compute shader |
| [[async-offline-culling]] | 离线标注 + 异步粗筛 + 渲染精筛的大型场景剔除设计 |
| [[playcanvas-webgpu-editor]] | PlayCanvas Editor 正式支持 WebGPU：视觉一致性优先 + beta 开关 |
| [[supersplat-pwa]] | SuperSplat 0.17.1：compute 重写 2× 加速 + PWA 文件关联 |
| [[gaussian-splatting-web]] | Web 上的 3DGS 工作流：压缩 PLY + SuperSplat + Editor 集成 |
| [[d3d12-work-graphs]] | D3D12 work graphs：GPU 自己生产/消费任务的新管线，含 CPU 端 PSO、launch 模式、与 compute+indirect 的性能对比 |
| [[shader-instruction-cost]] | shader 指令的三类隐藏成本：无原生实现、硬件非等价、外部资源依赖（含 atan2 展开、waterfall loop、LDS bank conflict） |
| [[meshlets-and-mesh-shaders]] | mesh shader 管线 + meshlet 遮挡剔除：数据结构、threadgroup 调参、AS hi-z cull 的 −44% 实测 |
| [[async-compute]] | D3D12 async compute 方法论：pairing 互补性、bubble 风险、pass 重排的免费收益 |
| [[camera-relative-sun-shadows]] | Anno 1800 把太阳锁相机：物理正确 vs 美术正确的构图反直觉 |
| [[pom-decal-broken-edges]] | Cyberpunk 2077 的 POM decal：盒子 + overlap mesh + 视差遮挡贴图装出手凿墙 |
| [[fresnel-edge-highlight]] | Fresnel 节点 + HDR 色 + Bloom：曲面边缘跳出的最便宜方案 |
| [[depth-intersection-subgraph]] | 同一个 DepthIntersection 子图撑起水面泡沫、光柱软交界、护盾接触带 |
| [[depth-aware-gaussian-blur]] | 稀疏高斯核 + depth bilateral：后处理模糊的便宜深度感知版 |
| [[shader-graph-custom-function-hlsl]] | URP Additional Lights：Shader Graph Custom Function 挂 HLSL 的最小闭环 |
| [[mystery-dungeon-sketch-shadows]] | URP post-process 四件套复刻 Mystery Dungeon 素描阴影美术 |
| [[screen-space-shadow-map-urp]] | 屏幕空间阴影贴图替代光源空间采样，方便后处理拿到阴影 mask |
| [[bilinear-sample-blur-optimization]] | 利用双线性插值降采样数：4 样本高斯压到 1 样本的 GLSL 技巧 |
| [[penumbra-hypothesis]] | 阴影软边假设：用光源角大小近似半影替代 PCSS 多采样 |
| [[radiance-cascades]] | Sannikov 的 2D 全局光照：结构化级联 + bilinear merge 替代随机采样 |
| [[volumetric-fog-raymarch-shadows]] | 屏幕空间 raymarch + 级联阴影的体积雾：renormalize viewRay 的经典坑 |
| [[vertex-shader-basics]] | Vertex Shader 何时写、能做什么：2D 游戏里被低估的流水线一半 |
| [[draw-renderer-list-mask-urp]] | URP 自绘 layer mask：`DrawRendererList` + override material + `ShaderTagId` 重绘特定层到自有 RT |
| [[terrain-splatmap-shader-graph]] | Unity terrain 的 `_Control` + `_Splat0..3` 约定在 Shader Graph 的手工复刻 + 法线自动岩石层 |
| [[world-scan-shader-effect]] | 世界空间扫描波：两次 `Step` 夹出圆环 + Emissive + Bloom 的发光扩散 |
| [[stencil-parallax-card-layers]] | Pokémon 卡牌分层 parallax：stencil mask + Render Objects feature 把 layer 按 stencil 掩回画面 |
| [[holofoil-rainbow-shader]] | 宝可梦 holo 闪卡：视角相关彩虹条纹 + Hue 循环 / Color Ramp 双路径 + Holo Mask + Height→Normal |
| [[fullscreen-shader-graph-urp]] | URP Fullscreen Shader Graph + Full Screen Pass Renderer Feature：Shader Graph 直出后处理 |
| [[hlsl-texture-sampling-basics]] | HLSL 纹理采样骨架：`TEXTURE2D` / `SAMPLER` / `_ST` / `TRANSFORM_TEX` / `SAMPLE_TEXTURE2D` |
| [[srp-batcher-cbuffer]] | SRP Batcher 的门票：`CBUFFER_START(UnityPerMaterial)` 把 material 属性封入常量缓冲 |
| [[voxel-map-lut-2d]] | 以 2D 纹理拼接成 3D LUT，在没有 3D texture / SSBO 的引擎里存体素地图 |
| [[programmer-art-vis-dev]] | 程序员美术的视觉打磨清单：色板、分辨率、细节分布、灯光 |
| [[fwidth-derivative-antialiasing]] | 用 `fwidth()` / 手动偏导数做任意连续函数的一像素淡出 AA |
| [[gamma-correction-srgb]] | shader 视角的 sRGB ↔ linear 编解码：γ=2.2 近似与精确公式 |
| [[sdf-operations-shader]] | SDF 的布尔并差交、onion / hollow、镜像平铺、smooth min 修改清单 |
| [[godot-hologram-shader-effects]] | Daniel Ilett 的 Godot 全息着色器：PBR + 顶点/切片 glitch + dot/grid/gradient + fresnel 等变体 |
| [[sprite-batch-instance-draw]] | 用 instance draw + storage buffer 去重 sprite 顶点数据（云风 Soluna） |
| [[one-way-window-backface-culling]] | 利用 back-face culling 做单向窗户：内部可见、外部被遮挡体积包住 |
| [[shadow-caster-culling-front-back]] | shadow map 该用 front-face 还是 back-face 做投射者 —— peter-panning 与 light leak 的抉择 |
| [[selective-shadow-fade-pass-switch]] | 让单个角色的阴影独立淡出：UE Shadow Pass Switch + 多 shadow pass |
| [[blob-shadow-decal-vs-plane]] | Blob 阴影：对齐平面 vs 投影 decal，水面与高度差的取舍 |
| [[turbulence-domain-warping]] | 叠加旋转正弦波在单 pass 伪装流体 / 火焰 |
| [[reading-math-notation-for-shaders]] | shader 作者读数学论文的记号查表 |
| [[shader-combination-strategies]] | 合并 vs 多趟 pass 的 5 项 checklist |
| [[common-shader-pitfalls]] | NaN / 纹理 / mipmap / 精度常见 shader bug |
| [[shader-art-design-principles]] | Xor 的 shader art 五维自查（构图/光/色/纹理/动作） |
| [[supersplat-publish-platform]] | SuperSplat 2025 年从编辑器扩张为编辑-发布-托管-社区平台 |
| [[subpixel-reconstruction-antialiasing]] | Chajdas/McGuire/Luebke 2011：子像素 visibility + 1x shading 的 deferred 抗锯齿 |
| [[tiled-light-trees]] | O'Donnell/Chajdas 2017：tile 内 light BVH + clustered 混合 |
| [[procedural-retro-skybox]] | 低色深 + dither + 双 Worley 程序云的 PSX 风天空盒 |
| [[iridescent-bubble-shader]] | Fresnel × color-ramp × noise flow 的彩虹肥皂泡 + `_CameraTransparentTexture` 折射 |
| [[refractive-glass-shader]] | URP 下用 `_CameraOpaqueTexture` 做折射玻璃，Fresnel 作边缘 & 混合权重 |
| [[mesh-triangle-explosion]] | 三角形按法线 / offset / baked-vertex-color 三种模式向外炸开 + 重力 + 随机偏移 |
| [[stochastic-texture-sampling]] | 每张贴图 3 次随机偏移采样打散 tiling，Heitz-Neyret 思想的轻量实现 |
| [[sog-compression-format]] | SOGS → SOG：3DGS 的 WebP 级压缩，属性图 + PLAS 排序 + WebP 编码，~95% 缩减 |
| [[splat-transform-cli]] | SplatTransform CLI：PLY/SPLAT/KSPLAT/SOG/CSV 互转 + 空间变换 + 多文件合并 + SH 瘦身 |
| [[voronoi-lava-shader]] | Voronoi 到边距离驱动的双层 PBR 混合 shader |
| [[volume-mask-layers]] | URP Volume 后处理的多维 layer/tag/queue mask 机制 |
| [[underwater-post-effect]] | 屏幕空间水下后处理：flow map UV 扭曲 + triplanar/light-aligned caustics |
| [[volume-component-scripting]] | Unity 三管线 Volume 参数 C# 运行时修改 API 对比 |
| [[bc7-solid-color-blocks]] | BC7 mode 5 精确编码 8-bit 纯色块的闭式端点 |
| [[mrsse-hdr-error-metric]] | Oodle Texture BC6H 所用的相对均方误差度量 |
| [[unorm-snorm-hardware-conversion]] | UNORM / SNORM → float 的硬件级实现（LZ + 16-bit adder 足矣） |
| [[density-field-volumetric]] | 体积 raymarch 的密度场与样本累积（additive vs alpha-blend） |
| [[dot-gyroid-noise]] | Gyroid + 黄金角旋转的廉价 aperiodic 3D 噪声 |
| [[radiometry-integral-view]] | 以积分视角（而非 differential）组织辐射度量 |
| [[photometry-luminance]] | Photometric 量、CIE XYZ 与 luminance |
| [[hyperbolic-tangent-shader]] | tanh 在 shader 里的 4 类用法（sigmoid / tonemap / blend / 调试） |
| [[glsl-mix-function]] | mix 的进阶用法：saturation、extrapolation、remap、感知均匀 |
| [[tweet-shader-280-char]] | 280 字符 tweet shader 的思维与技巧 |
| [[fragcoord-shader-editor]] | Xor 的 FragCoord.xyz：浏览器内 shader 调试器 |
| [[spectral-vs-rgb-comparison]] | 各类光源下 RGB vs 光谱渲染的实证对比 |
| [[path-tracing-basics]] | 最小可行 path tracer 的学习路径（Peters workshop + lectures） |
| [[blend-modes-shaderlab]] | ShaderLab Blend 命令、11 个 BlendMode 因子、三种常见混合模式 |
| [[urp-depth-prepass-passes]] | URP 自定义 shader 必补的 DepthOnly / DepthNormals 两个 Pass 及其触发时机 |
| [[urp-render-objects-feature]] | URP Renderer Feature 无代码做 X-ray、物体 mask、透视显隐 |
| [[hull-domain-tessellation-urp]] | URP 下 hull/domain tessellation 基础骨架：5 个 attribute + patch constant + domain barycentric |
| [[noperspective-affine-texture]] | HLSL `noperspective` 关键字与 PSX affine texture warping 的一行切换 |
| [[toon-outline-post-process-modes]] | Toon 描边的六种算法并列：屏幕空间 Sobel / 物体 mask / inverted hull |
| [[gpu-utilisation-holistic-tuning]] | GPU 利用率整体调优：跨 pass 瓶颈配对 + async compute 搭配方法论 |
| [[vertex-shader-export-bottleneck]] | N 卡 VS export 的 ISBE/PE/TRAM 瓶颈，1→10 float4 export 近 3× 成本 |
| [[spatial-hash-rtao-cache]] | 稀疏空间哈希做 RTAO 缓存 + 天然去噪，11.4MB 支持 1M cell 自适应大小 |
| [[mlp-signal-encoding-rendering]] | 小 MLP 作为渲染信号编码器 vs SH：辐亮度赢、辐照度输、BRDF 靠参数化 |
| [[hlsl-cooperative-vectors-tensor-cores]] | HLSL 通用 shader 访问 Tensor core，大 MLP 推理 173× 加速 |
| [[metal-decade-history]] | Apple Metal API 十年演进（2014–2024）双篇回顾 |
| [[hdr-video-edr-metal]] | AVFoundation + Metal HDR 视频管线 + PQ/HLG tonemapping shader |
| [[metal-4-api-redesign]] | Metal 4 的 API 重塑（显式 residency + command allocator + argument table） |
| [[slug-gpu-glyph-rendering]] | Lengyel Slug 算法专利释放后 Metal 上的最小实现（winding + bands + fractional coverage） |
| [[tessellation-approaches-overview]] | Karis 2026：动态 tessellation + 位移的选型路径，为什么 tracing 和 Nanite 簇内放大都不行、最终走 Reyes |
| [[nanite-tessellation-approach]] | UE5.4 Nanite Tessellation 的流水线：ClusterRasterize 扩展 / PatchSplit global shader / PatchRasterize 软光栅 + DS 导数 |
| [[nanite-reyes-comparison]] | Nanite Tessellation 与 Pixar Reyes 的逐点对照：split 同构、dice 从方格换成不规则等边、shading 频率从 object-space 改为像素 deferred material |
| [[variable-sized-work-pattern]] | Karis 从 Nanite Tessellation 抽出的通用并行原语：wave 内 pull-based 变长工作分发，顺便解释 Nanite 软光栅为何快于 HW |
| [[airfoil-lift-physics]] | 升力物理与流体力学入门（Ciechanowski） |
| [[fluid-flow-visualization]] | Eulerian 箭头 × Lagrangian 粒子 × 标量色图的三重表示 |
| [[keplerian-orbits]] | Kepler 轨道与两体问题（Ciechanowski Moon × Zucconi Orbital） |
| [[n-body-gravity-simulation]] | N 体引力的数值积分：Euler / Verlet / symplectic |
| [[moon-phases-tides]] | 月相、潮汐、食——引力梯度与节点几何 |
| [[pca-intro]] | PCA 直觉入门：椭球半轴与特征分解 |
| [[shader-graph-contract]] | Shader graph 的 sink 节点契约（unlit/lit/layered） |
| [[shader-permutation-explosion]] | shader 排列爆炸与 #stutterstruggle |
| [[gpu-data-packing]] | UNORM/SNORM/bitfield/BFE/BFI 的 HLSL + RDNA 实战 |
| [[haze-urp-volumetric-fog]] | Alisavakis HAZE：URP froxel 体积雾商品化实现 |
| [[planar-mirror-rendering]] | 平面镜 stencil + oblique 投影 + 独立 cull |
| [[monte-carlo-integration]] | MC 积分基础：1/√M 与维度无关 |
| [[inversion-sampling-prng]] | PRNG、拒绝、逆变换采样 + Jacobian |
| [[path-tracing-monte-carlo]] | MC 套渲染方程：cosine-weighted、NEE、MIS、RR |
| [[dual-kawase-blur]] | 多级下采样+上采样的主流游戏 UI 模糊算法 |
| [[kawase-blur]] | Masaki Kawase 的四角采样近高斯模糊 |
| [[convolution-separability-blur]] | 把 N×N 卷积拆成两次 1D pass 的可分离性 |
| [[matrix-multiplication-ordering]] | Across-times-down、列/行向量乘法、空间链约定 |
| [[row-major-column-major-packing]] | HLSL/GLSL 矩阵内存打包与 pack_matrix / layout 语义 |
| [[procedural-pool-ball-sdf]] | 用 SDF 条纹+圆环+数字 atlas 程序化生成台球贴图 |
| [[sdf-number-atlas-text]] | 通过 SDF 纹理 atlas + smoothstep 渲染锐利数字 |
| [[ambient-cube-probe-pathtrace-exit]] | AmbientCube 探针作为 PathTracing 提前退出缓存 |
| [[hybrid-voxel-software-raytracing]] | 探针+体素网格替代 BVH 的软件光追近似 |
| [[phacelle-noise]] | Johansen 发明的廉价方向性噪声（cos+sin→单位圆→归一化取相位） |
| [[directional-noise]] | 方向性噪声家族谱系：Voronoi→Gabor→Gavoronoise→clayjohn/Fewes erosion→Phasor/Phacelle |
| [[erosion-filter-procedural]] | 单 pass GPU 侵蚀滤波器：沿梯度叠条纹、多 octave 分叉、fade/frequency 保留峰谷 |
| [[atmospheric-perspective]] | 远山先趋深蓝再变淡，fog trick 的边界与大气散射的替代方案 |
| [[hair-shader-anisotropic]] | Unity Standard BRDF 之上做各向异性发丝（3 档实现与余弦权重函数） |
| [[gb10-gpu-blackwell-igpu]] | GB10 iGPU 是 consumer Blackwell 而非 datacenter（cc 12.1 vs 10.0）；24 MB L2 策略 vs RDNA 四层渐进缓存 |
| [[lighthouse-2-optix]] | Jacco Bikker 在 OptiX 7 / RTX 上开源的实时 GPU 路径追踪框架 |
| [[nvidia-omniverse]] | 以实时路径追踪为核心的 NVIDIA USD 协作平台与演示序列 |
| [[material-light-validation]] | 以 Arnold 离线渲染器为 ground truth 验证 PBR material 与 light 的流程 |
| [[physical-camera-model]] | 用真实相机参数（ISO / 快门 / 焦距 / 光圈）驱动渲染的相机 entity 模型 |


| [[banjo-kazooie-vertex-color-terrain]] | N64 时代把颜色编码进顶点色做 splat 混合的地形风格，Godot/Blender 复刻路径 |
| [[srgb-premultiplied-alpha-compression]] | sRGB × 预乘 alpha × 块压缩的正确顺序 |
| [[poisson-rect-process]] | 无限平面上的无重叠随机矩形：两相过滤 + 分块无关 |
| [[infinite-chunked-procedural-generation]] | 无限世界的分块程序化生成方法论：相位化 + 局部有界依赖 |
| [[l-system-fractals]] | Lindenmayer 系统：公理 + 产生式规则的分形图形生成 |
| [[l-system-lightning-bolts]] | L-system 衍生：分形闪电效果的随机分支与衰减 |
| [[planet-terrain-dem-pipeline]] | Outerra 行星 DEM 管线：SRTM/NasaDEM + fractal resample 实战 |
| [[opengl-draw-call-batching-sweet-spot]] | instanced draw 的 5k-20k 三角形跨厂甜点（Outerra 实测） |
| [[fp64-sincos-minimax]] | GLSL fp64 sin/cos 的 Remez minimax 近似（Outerra） |
| [[vortex-distortion]] | 极坐标下半径相关旋转的 UV 扭曲后处理（漩涡） |
| [[triangle-filtering-pipeline]] | Confetti/The Forge 的 Triangle VB 工程化：三级剔除 + ExecuteIndirect + Forward++ |
| [[ray-tracing-api-debate]] | Wolfgang Engel 2018 年对 DXR 黑盒化的公开质疑与替代路线 |
| [[the-forge-renderer]] | Confetti 开源跨平台渲染框架，Engel 所谓「下一代 GPU Zen」 |
| [[sharpen-filter]] | unsharp mask 锐化后处理：原图加高频残差；Snapshot Shaders Pro 的单参数产品化 |
| [[synthwave-grid-postfx]] | 屏幕像素反推世界坐标后判定到三组正交平面的距离，画出透视正确的无限网格 |
| [[text-adventure-terminal-postfx]] | ASCII 终端风格后处理：cell 平均亮度索引字符图集、bg/fg 双色 lerp |
| [[spirv-parsing-rewriting]] | 手写 SPIR-V 解析器：检测 OpKill、改写 HLSL binding |
| [[mesh-shader-vulkan-hlsl-per-primitive]] | HLSL + Vulkan mesh shader 的 PerPrimitiveEXT 手动 decoration 坑 |
| [[simplified-pipeline-barriers]] | 把 Vulkan 的 stage/access/layout 压成两个引擎侧 enum |
| [[minimalist-rt-acceleration-structures]] | 只用 ray query + TLAS instanceCustomIndex 的 potato RT |
| [[coordinate-system-table]] | 主流引擎 / API / DCC 的 view/world space 轴向与手性对照表 |
| [[vector-quantization-tilemap]] | 向量量化 = 自动生成瓦片表：K-Means 压图到 codebook + tilemap |
| [[pca-image-compression]] | 用 2D PCA 把 RGB 颜色压成连续「二色调色板」的最简实验 |
| [[color-quantization-som]] | 用 1D 自组织映射学调色板，得到有拓扑的 256 色（ScreenToGif 同款） |
| [[moving-basis-decomposition]] | Silvennoinen / Sloan PRT 压缩技术在 2D 图像上的玩具实现，PCA × PVRTC |
| [[hyperion-renderer]] | Disney Animation 自研生产路径追踪器，从 Moana 到 Zootopia 2 的十年演进 |
| [[wavefront-path-tracing]] | 按 bounce 批处理的路径追踪架构，Hyperion / RenderMan XPU 的共同骨架 |
| [[path-guiding-production]] | 把 path guiding 从 PPG 论文铺到影片管线的工程账：Hyperion × OpenPGL 的二代系统 |
| [[ptex-gpu-streaming]] | Disney 的实时 GPU Ptex 纹理流送：小 cache + 激进 LRU + 原始 face 数据流送 |
| [[nested-dielectrics]] | 水-玻璃-环境多层嵌套介质，Schmidt & Budge 2002 的栈式算法与产线扩展 |
| [[rejection-vs-analytical-sampling]] | 单位球内均匀采样：打开 -O1 后拒绝采样反超解析解 |
| [[asin-cg-approximation]] | Nvidia Cg 文档里的 Abramowitz-Stegun 4.4.45 Minimax asin 近似 |
| [[psraytracing]] | 16bpp.net 的 C++ 路径追踪器，各种性能实验的测试床 |
| [[ediz-upscaling-critique]] | Jon Olick：EDIZ 简单上采样方法的五点批判 |
| [[laplacian-structure-aware-error-diffusion]] | Laplacian 结构感知误差扩散，低对比度区 MSSIM +25% |
| [[sift-single-file-library]] | jo_sift.h：专利过期后的 SIFT 单文件 C 库 |
| [[openpbr]] | 开放式 PBR uber-shader 标准（Adobe / Autodesk / ILM） |
| [[neural-materials]] | 神经材质：把复杂离线 shader graph 压进小 MLP |
| [[graphics-api-history]] | 图形 API 从固定管线到 Vulkan/D3D12 的三段式演进（Sawicki 科普） |
| [[pix-api-and-dxdmp]] | GDC 2026：PIX API、.dxdmp 崩溃转储、DebugBreak()、PIX 事件透传驱动 |
| [[dxr-tier-2-clas-ptlas]] | DXR Tier 2.0：CLAS / Cluster Template / Partitioned TLAS |
| [[advanced-shader-delivery]] | Shader Compiler Plugin + Partial Graphics Programs + DirectStorage 1.4 |
| [[pixelate-postfx]] | Pixelate 像素化后处理：空间维度量化，与色阶量化正交 |
| [[radial-blur-postfx]] | Radial Blur：kernel 随径向距离变化的空间变化 blur |
| [[urp-builtin-feature-mapping]] | Built-in RP 与 URP 的 API 一一对照 |
| [[urp-settings-locations]] | URP 设置入口的散落地图 |
| [[urp-shadergraph-fog-strip]] | 给指定 ShaderGraph 材质关掉 URP 雾效 |
| [[shader-variant-stripping]] | Unity 构建期剥 shader 变体（IPreprocessShaders） |
| [[light-prepass-pipeline]] | Wolfgang Engel 的 light pre-pass 三步走管线（Ni No Kuni 2 实例）|
| [[ninokuni-2-line-art]] | MRT + 艺术家数据驱动的角色线稿管线 |
| [[yuv-gbuffer-layered]] | DCS 的 5 层 R8G8 array + YUV albedo GBuffer |
| [[cloudscape-sdf-volumetric]] | SDF 驱动的体积云 cloudscape（DCS 2.7）|
| [[terrain-virtual-node-texture]] | Anno 1800 的 node-texture 地形（763 slice array + bake）|
| [[texture-driven-gpu-particles]] | Anno 1800 的 quad + 时间×粒子动画纹理粒子系统 |
| [[nine-slice-ui]] | 九宫格 UI mesh：角不变形的任意矩形缩放 |
| [[tiny-shading-language]] | Jiayin Cao：四个月写一门 CPU 路径追踪器的着色语言（Flex+Bison+LLVM + closure tree） |
| [[restir-di-math]] | ReSTIR DI 背后的数学：SIR/RIS/WRS、邻居 target function 不同为何无偏、uniform MIS weight 的代价 |
| [[restir-gi-math]] | ReSTIR GI 数学：Primary Sample Space、per-initial-candidate target function、路径 initial candidate 的 GRIS 处理 |
| [[ascii-shape-vector-rendering]] | 字符不是像素：6D 形状向量 + 最近邻 + 双层对比度增强的 ASCII 渲染器（Alex Harri） |
| [[volume-rendering-offline]] | Jiayin Cao：离线渲染中的体积渲染方程推导（补齐 PBRT 跳过的 in-scattering ODE 推导）|
| [[bxdf-unit-test]] | Jiayin Cao：PBRT bsdftest 用 2π 收敛验证 BXDF 正确性 |
| [[anisotropic-microfacet-sampling]] | Jiayin Cao：GGX/Beckmann/Blinn 各向异性 importance sampling 推导与 arctan 值域坑 |
| [[color-science-basics]] | Jiayin Cao：图形工程师的色彩科学基础——从 SPD 到 CIE XYZ 到 Rec.2020 |
| [[sss-practical-implementation]] | Jiayin Cao：SSS 进 path tracer 的工程实践——消 fireflies 三个 trick 与材质系统重构 |
| [[ground-truth-ambient-occlusion]] | GTAO 完整实现：IGN 噪声、temporal reprojection、bent normal、overscan |
| [[use-gpu-reactive-runtime]] | Steven Wittens 的声明式/响应式 WebGPU 运行时 |
| [[render-pass-orchestration]] | Use.GPU 声明式 render pass 编排：well-known names 隐式 wiring、buffer history 一等化 |
| [[mgs-v-fox-engine-frame]] | Fox Engine 一帧全流程解剖（MGS V：小 G-Buffer、双 SSAO、早 tonemap、分级 scatter DoF） |
| [[gather-bokeh-dof]] | Gather 式 bokeh DoF + McIntosh flood-fill，UE4 BokehDOF 的移动端替代（DOOM 2016 技术） |
| [[ue4-reactive-dynamic-resolution]] | UE4.18 前的反应式 dynamic resolution 补丁，基于 GGPUFrameTime 两档跳变 |
| [[d3d12-resource-alignment]] | D3D12 资源对齐的秘密：small alignment、heap alignment、tight alignment |
| [[compute-shader-dispatch-ids]] | HLSL / GLSL compute shader 线程 ID system-value 速查 |
| [[ray-differentials]] | 路径追踪里选 mip level 的工程机制，以及双向路径追踪下 Manuka/Takua 的两种绕过方案 |
| [[ibl-multiple-scattering]] | Fdez-Agüera 2019 的 IBL 多次散射能量补偿 |
| [[split-sum-approximation]] | Karis 2014 的 IBL 镜面积分分解 |
| [[obb-frustum-sat]] | OBB × 视锥的分离轴定理剔除，消除 false negative |
| [[ispc-simd-culling]] | 用 ISPC / AVX2 做 SoA 剔除，10k/0.3ms |
| [[streaming-staging-texture-upload]] | Nabla 的固定大小 staging + 流式格式转换纹理上传 |
| [[frames-in-flight]] | CPU 领先 GPU 录制的机制、timeline semaphore、swapchain 上限 |
| [[circular-separable-dof]] | Kleber Garcia 的复数可分离圆盘 bokeh gather |
| [[dxt-entropy-reduction]] | DXT selection bits 熵压缩：1.51 bpp 的 Firefall 方案 |
| [[dxt-codebooks-sliding-window]] | Zeng 码表与滑窗码表在 DXT 二次压缩中的定位 |

| [[gpu-instanced-grass-urp]] | Cyan 的 URP + Shader Graph GPU 实例化草地：RenderMeshIndirect + compute frustum cull + `_VisibleIDs` 两级索引 |
| [[sysgpu-webgpu-successor]] | Mach sysgpu：Zig 写的 WebGPU 原生实现与继任者 |
| [[dxc-dxil-signing]] | DXC/DXIL 工具链与 dxil.dll 专有签名 blob 的历史 |
| [[mach-dxcompiler-static-build]] | 用 build.zig 重写 DXC 的构建系统并跨平台分发 |
| [[gpu-unbiased-path-tracing]] | 2010 年 GPU 非偏置渲染器大爆发：Octane / Arion / V-Ray RT / iray 的平行史 |
| [[otoy-cloud-rendering]] | OTOY 在 AMD RV770 上的早期云渲染/云游戏架构 |
| [[jpeg-codec-pipeline]] | JPEG 编码三段论：YCbCr+chroma 降采样、8×8 DCT 量化、Huffman 熵编码 |
| [[jpeg-xl-format]] | JPEG-XL 编解码格式：可变 DCT、渐进解码与 AVIF/WebP 对比 |
| [[efficient-sparse-voxel-octrees]] | Laine 2010 年 SVO 论文：contour + 紧凑编码 + CUDA 开源 |
| [[variable-size-gather-dof]] | ATI Scheuermann 风格的按 CoC 变采样半径 gather DoF |
| [[fake-hdr-half-brightness]] | 8-bit 渲染目标下以半亮度渲染 + 后期乘 2 伪装 HDR bloom |
| [[number-puzzle-tile-shader]] | Supnik：shader 级瓦片随机化去除纹理重复感 |
| [[sdf-font-atlas-rendering]] | 基于 AngelCode BMFont + distance field 的字体渲染 |
| [[opengl-builtin-attribute-aliasing]] | NVidia 对 GLSL 内置顶点属性与 generic attribute 的别名处理偏离 GL 2.1 规范 |
| [[triangle-strips-vs-indexed-triangles]] | 在索引化时代三角带的 vertex 复用优势大幅缩水，draw call 成本才是瓶颈 |
| [[camera-mapping-2d-to-3d]] | 把 2D 插画投影到粗 3D 几何上做可动画的「活画」（Joost van Dongen / Proun） |
| [[huge-world-coordinate-precision]] | 3D 世界远离原点时 32-bit float 丢位的 3 种应对：整体 transform、双缓冲、局部坐标系 |
| [[texture2dgrad-explicit-derivatives]] | 当 UV 在 shader 里被 fract/swizzle 破坏连续性时，用 texture2DGradARB 手喂原始导数保住 LOD |
| [[uv-precision-derivative-loss]] | 300 km 地形由 vertex shader 投影生成 UV，其导数精度低于一像素，per-pixel tangent space 会错乱 |
| [[alpha-blending-front-to-back]] | 前向 alpha 合成 + 反转 alpha 的 back-to-front 变体（Supnik） |
| [[vbo-double-buffering-orphaning]] | VBO 双缓冲 / orphaning / MapBufferRange 的应用端推导 |
| [[agp-vs-vram-streaming]] | 流式顶点为何驱动常给 AGP system memory 而非 VRAM |
| [[glbuffersubdata-serialization]] | 为什么 glBufferSubData 必然与 in-flight draw 串行化 |
| [[stereoscopic-3d-design]] | 立体 3D 的设计含义：窗口违例、眼距调节、屏幕空间 trick 失效（van Dongen / Proun） |
| [[screen-space-light-shafts]] | God rays / 体积光屏幕空间近似：从像素向太阳走、采样亮度累加（GPU Gems 3 / Proun） |
| [[lightmap-baking-workflow]] | 离线烘 lightmap：V-Ray / 3ds Max 自动 unwrap、area light、skylight、GI（Proun 单赛道 30h） |
| [[colored-sky-sun-lighting]] | 对比色 sun / skylight 的艺术搭配：蓝-黄、橙-青、粉-绿（Proun 三赛道） |
| [[pc-gpu-driver-compat-qa]] | PC 发行的驱动兼容地狱：NPOT 检测、max-vertex-index、shader-cap 说谎、glTexSubImage2D 坑 |
| [[screen-space-curve-tessellation-cutoff]] | 把 Bézier 曲线细分阈值反投影到屏幕像素半径，避免像素内堆叠几十条冗余顶点 |
| [[opengl-extension-bucket-strategy]] | OpenGL 扩展分桶策略与现场调试用的细粒度开关 |
| [[gpu-embarrassingly-parallel-serial-dispatch]] | GPU 天生并行：为何无需应用层并行命令派发 |
| [[premultiplied-alpha-bilinear-ring]] | 预乘 alpha 为何能修复 bilinear filtering 的 tree-ring 杂色晕 |
| [[gpu-sliced-volumetric-shadows-limits]] | GPU sliced shadow 在 flight-sim 云场景下的失败模式：不透明粒子 + 分桶 + popping |
| [[linear-lighting-pipeline]] | 线性光照累积的三种管线路径：shader 内累加 / sRGB framebuffer blend / HDR float RT |
| [[matrix-as-basis-vectors]] | 3x3 矩阵作为基向量：列是 decoder、行是 encoder |
| [[video-codec-licensing-tradeoffs]] | 引擎视频播放的 codec 选型：H.264 / VP8 / Bink / 平台原生 / 不做 |
| [[particle-collision-plane-cache]] | 每粒子自带平面 + 空间哈希缓存 raycast 结果 |
| [[matrix-scale-drift]] | Matrix4x4 里 rotation/scale 共享存储引发的 28 分钟 0.1% 漂移 |
| [[xplane-gbuffer-format]] | Supnik 2010：X-Plane 10 第一版 16 字节 G-Buffer 布局（shadow/shine 浮点打包） |
| [[glsl-compiler-optimization-reliance]] | 用 ShaderAnalyzer 观察驱动编译器，反推 X-Plane 10 shader 组织策略 |
## 经典案例（wiki/examples/）

APoSD 中反复出现的标杆与反面案例。

| 文章 | 一句话描述 |
|---|---|
| [[unix-io]] | 5 个系统调用隐藏几十万行实现的深模块标杆 |
| [[java-io]] | 三件套 + 显式 buffering 的 classitis 病例 |
| [[garbage-collector]] | 接口为零的极限深模块 |

## 游戏开发（wiki/game-development/）
APoSD 框架在 Unity/游戏引擎开发中的应用。

| 文章 | 一句话描述 |
|---|---|
| [[unity-complexity-patterns]] | Unity 项目中的复杂性典型模式 |
| [[classitis-in-games]] | Manager 癌症与事件系统滥用 |
| [[resource-system-design]] | 资源系统的信息隐藏战场 |
| [[ecs]] | ECS 作为深模块与显式依赖的案例 |
| [[rendering-api-depth]] | 渲染 API 的浅 vs 深对照 |
| [[unity-procedural-mesh]] | Unity Mesh API：vertices + triangles + winding order 的最小闭环 |
| [[kinematic-character-controller]] | Unity DOTS 下 kinematic 角色控制器的设计与 edge case |
| [[a-star-pathfinding]] | A* 与动态环境下的寻路取舍，g(n) 是游戏性的入口 |
| [[composite-command-pattern]] | 命令模式与 Serial / Parallel 复合命令：跨帧执行的可组合工作单元 |
| [[meshes-of-navigation-recast]] | 导航网格与 Recast 的体素化生成管线 |
| [[procedural-mesh-primitives]] | Torus / UV-sphere / ellipsoid 的参数化顶点公式与拓扑结构 |
| [[mesh-warps-and-tessellation]] | Stellation、extrusion 与 fan/centroid/triforce 三角化：CPU 侧 per-face 几何算法 |
| [[z-order-top-down-2d]] | 俯视角 2D 游戏的 z-order：静态分层 vs 动态按底边 Y 排序 |
| [[html5-game-apis-2012]] | 2012 年浏览器游戏 API 可用性地图：WebGL / Web Audio / PointerLock / Gamepad / WebSocket |
| [[runtime-editor-console-connection]] | _The Witcher 2_ 的编辑器-主机实时调参工具链：命令式网络协议，美术电视前调光照/色彩 |
| [[tools-first-iteration-loop]] | Evan Todd：内容管线和工具优先级高于一切引擎特性 |
| [[ios-app-thinning]] | Apple 在 iOS 9 上推出的 App Slicing + Bitcode + On-Demand Resources 分发瘦身三件套 |
| [[worker-task-dispatch-priority]] | 矮人要塞风格的工人任务分发：权重相乘的调度模型 |
| [[multi-target-pathfinding]] | 从任务系统需求倒推：单源多目标扩散代替 N 次 A* |
| [[save-load-driven-data-design]] | 以持久化驱动数据模型设计：存档是设计压力测试 |
| [[determinism-vs-smart-ai-gameplay]] | 微操游戏里确定性规则胜过智能 AI：云风从工厂物流与异星工厂 2.0 学到的 |
| [[single-hub-logistics-model]] | 异星工厂太空平台的唯一枢纽模型：上帝视角 + 背包式中转 |
| [[indie-game-dev-rhythm]] | 云风的独立开发方法论：情绪、拆分、重构、代码量 |
| [[paradox-grand-strategy-economy]] | EU5 经济系统：人口/货币/商品三要素与市场中介 |
| [[deckbuilder-game-design-patterns]] | 卡牌构筑游戏设计套路：双卡堆、主动刷牌、需求上升代替战斗 |
| [[planning-over-rng-game-design]] | 规划式游戏设计：dotAGE / Spirit Island / Voidfall 的确定性 + 精算乐趣 |
| [[minecraft-plugin-development]] | Minecraft plugin vs mod vs data pack 的生态与 Paper/Bukkit 工程 |
| [[character-height-variation-problem]] | 角色高度变化的 6 种解法（高跟鞋问题） |
| [[blender-hard-surface-modeling]] | Blender 硬表面建模：crease + bevel weight + harden normals 少顶点出工业硬棱 |
| [[indie-pitching-publishers]] | Joost van Dongen 17 年经验：半年全职 pitch、MeetToMatch、X-factor 与 76 页台账 |
| [[game-idea-generation]] | 避开创意输入同质化：现代艺术馆、博弈论、古建筑作为非游戏灵感源 |
| [[unity-input-system-multi-gamepad]] | Unity 新旧 Input System 对比与多手柄配对踩坑 |
| [[unity-prefabs-as-data]] | 把 Prefab/GameObject 当纯数据容器用，拿到层级 / 组件 / Variant / Nested 四种结构能力 |
| [[unity-ecs-custom-editor-debug]] | Unity ECS 下用 shadow GameObject + CustomEditor 做可写调试 UI |
| [[unity-asset-refactoring]] | Prefab/Scene/Asset 里 MonoBehaviour 字段结构批量重构的四步法 |
| [[umg-user-widget-lifecycle]] | UMG UUserWidget：NativePreConstruct 与蓝图 PreConstruct 顺序 |
| [[dynamic-split-screen]] | 动态分屏：根据玩家距离在单屏 / 分屏间平滑切换 |
| [[unity-crowd-waypoint-system]] | Unity 人群 Waypoint 系统：以 NavMesh 为基础的简易群体行为 |
| [[unity-dots-tween-system]] | Unity DOTS Tween case study：ECS 下缓动动画系统设计 |
| [[rider-ue5-setup]] | Tom Looman：UE5 C++ 的 Rider + VS Build Tools 搭建清单 |
| [[project-orion-action-roguelike]] | Tom Looman 开源 UE5 合作 Roguelike 示例：Action 系统、DoD 投射物、对象池、Significance Manager |
| [[unreal-insights-counters-traces]] | UE Stats System 与 Unreal Insights 双路径埋点：Counter / Cycle Counter / Named Events |
| [[infinite-random-rhombus-tilings]] | Townscaper 替代方案：3 菱汇合点翻转 + 三层错位 chunking，无全局细分、无 chunk 边界 |
| [[ue-observability-stack]] | UE 物理游戏调试工具五档（On-screen → GDT → Visual Logger → ImGui → Ariadne）|
| [[ue-asset-validator-blueprint]] | UE 蓝图资产验证：GeneratedClass + Subobject Data Subsystem |
| [[ui-as-communication]] | Ben UI：UI 作为把想法搬进玩家脑袋的通道，十种传达媒介与优先级 |
| [[ux-opinions-checklist]] | Ben UI：按钮/快捷键/输入/文字/桌面软件的 RFC 2119 级 UX 清单 |

| [[additive-animation-layering]] | 叠加式动画层：1 帧 idle + 长周期 wiggle 的变化手法 |
| [[java-webstart-jar-signing]] | Java Applet/Web Start 分发时的 JAR 签名与 Maven 自动化流程（Gemserk 2010） |
| [[autotile-tileset-layouts]] | 2D autotile 切片布局：Marching Squares / Blob / Sub-blob / Micro-blob 的取舍 |
| [[vcs-vs-database-for-content]] | 游戏内容存 VCS 还是数据库 |
| [[unreal-pawn-playercontroller-pattern]] | Unreal 里 GameMode / Pawn / PlayerController 三件套分离，从 UDK 到 UE5 一脉相承 |
| [[json-3-way-merge]] | Bitsquid：理解 JSON 结构的三路合并，解决内容 merge 冲突 |
| [[guid-object-database-schema]] | Bitsquid：GUID + key-value + 5 种操作，把内容数据库做成无冲突可 diff 的小型 NoSQL |
| [[fixed-3000fps-gameplay-simplicity]] | Proun 用 3000fps 固定步长换碰撞代码简单性 |
| [[motion-sickness-camera-design]] | 无地平线游戏的抗晕眩摄像机：不做 smoothing、载具钉中心 |
| [[variable-timestep-smoothing]] | Bitsquid 变步长时间平滑：11 帧历史去两高两低取 7 均再 lerp |
| [[local-navigation-over-pathfinding]] | A* is Overrated：局部避障比最短路径算法更决定 AI 靠谱感 |
| [[playcanvas-cloud-asset-pipeline]] | PlayCanvas 2013 云端资产管线：浏览器拖入 FBX/COLLADA 即转码 |
| [[ngui-legacy-ui-system]] | NGUI 遗留 UI 系统：UI Root / UIPanel / UIAtlas / Button 家族 |
| [[game-settings-hot-reload]] | F5 热重载 gameplay 数值（struct + pointer，禁止拷贝） |
| [[level-design-without-editor]] | 没有关卡编辑器时的三层做法（Notepad + 模糊地形 + 程序化背景） |
| [[behaviour-tree-game-ai]] | 行为树游戏 AI，Ronimo 三代迭代到去优先级的 if-else 树 |
## 人物（wiki/people/）
| 文章 | 一句话描述 |
|---|---|
| [[john-ousterhout]] | APoSD 作者，斯坦福 CS 教授 |
| [[jasper-flick]] | Catlike Coding 作者，Unity 教程作者 |
| [[jason-gregory]] | Naughty Dog 引擎工程师，GEA 作者 |
| [[sussman-abelson]] | SICP 作者，Scheme 发明人 |
| [[hennessy-patterson]] | CAQA 作者，RISC 图灵奖得主 |
| [[bartosz-ciechanowski]] | ciechanow.ski 作者，交互式可视化大师 |
| [[bartosz-wronski]] | Bart Wronski，前 Sony Santa Monica / Google Pixel HDR+ |
| [[fabian-giesen]] | Fabian "ryg" Giesen，RAD/Epic 程序员，The ryg blog 作者 |
| [[aras-pranckevicius]] | 立陶宛图形工程师，前 Unity，现 Blender VSE 模块负责人 |
| [[angelo-pesce]] | Angelo Pesce（C0DE517E），图形程序员，长年博客输出思辨性笔记 |
| [[emilio-lopez-ros]] | The Code Corsair 博主，AAA 帧分析与 TAA tutorial 作者 |
| [[christoph-peters]] | Christoph Peters，momentsingraphics.de，矩/傅里叶系数压缩带界信号的图形研究者 |
| [[matthaeus-chajdas]] | Matthäus "Anteru" Chajdas，AMD GPU/编译器方向，anteru.net 博主 |
| [[max-slater]] | Max Slater（thenumb.at），前 Pixar / Activision 图形工程师 |
| [[xor-shader-artist]] | Xor / GM Shaders，Shadertoy + GameMaker 方向的 shader 艺术家与教程作者 |
| [[stephen-hill]] | Selfshadow 博客 / SIGGRAPH PBS course 组织者 / Lucasfilm ILMxLAB |
| [[jeremiah-van-oosten]] | 3dgep.com 作者，Learning DirectX 12 系列教程 |
| [[robin-green]] | 前 Sony SCEA R&D，GDC 2003 SH Lighting: Gritty Details 作者 |
| [[raph-linus]] | Raph Levien，Google Fonts / linebender，Vello / Druid / Xilem 作者 |
| [[apoorva-joshi]] | Apoorva Joshi，前 Activision path tracing，Papaya 开源 GPU 图像编辑器作者 |
| [[jasper-st-pierre]] | Linux 图形栈 / 现代图形 API 长期布道者，出货游戏渲染器工程师 |
| [[harry-alisavakis]] | Harry Alisavakis，Technically Art 博客作者、ShaderQuest 系列教程作者 |
| [[ronja-bohm]] | Ronja Böhm（Ferris Systems），Unity shader 教程作者 |
| [[cyanilux]] | Cyan（@Cyanilux），Unity Shader Graph / URP 教程作者 |
| [[linden-reid]] | Linden Reid，面向初学者的 Unity shader 与程序化几何教程作者 |
| [[steven-sell]] | Steven Sell，Vertex Fragment 博客与 Realms/Beyond the Storm 作者 |
| [[daniel-ilett]] | Daniel Ilett，Unity shader 教程作者与资产包（Snapshot / Retro / Toolbox）开发者 |
| [[alan-zucconi]] | Alan Zucconi，Unity shader 教程作者（彩虹 / 衍射 / SSS / 体积 / Journey） |
| [[gameknife]] | 中国独立引擎开发者，gkEngine 与 gkNextRenderer 作者 |
| [[allen-chou]] | Allen Chou（周明倫），Naughty Dog gameplay programmer，DigiPen 出身，Game Physics Series 作者 |
| [[frost-kiwi]] | Wladislav Artsimovich / Jaruat Frost，以交互式 WebGL 技术博客闻名 |
| [[warren-moore]] | Warren Moore，Metal by Example 博客与同名书作者 |
| [[simon-trumpler]] | Simon Trümpler，simonschreibt.de 作者，技术美术 / Game Art Tricks 博主 |
| [[kostas-anagnostou]] | Interplay of Light 博主，Playground Games 图形工程师 |
| [[people/evan-todd]] | Evan Todd，etodd.io / Lemma / Deceiver 独立开发者 |
| [[brian-karis]] | Epic UE5 Nanite/Lumen 技术负责人，前 Human Head（Prey 2），UE4 Real Shading 作者 |
| [[cloudwu]] | 云风，skynet / ejoy2d 作者，前网易游戏引擎程序员 |
| [[elias-daler]] | Elias Daler，独立游戏开发者，Re:creation / Edbr 引擎作者 |
| [[marco-giordano]] | Marco Giordano（giordi91），自研 DX12/Vulkan 引擎作者，博客 A programmer's cave |
| [[will-eastcott]] | PlayCanvas 联合创始人/CEO，WebGPU 与 3DGS 工具链主推者 |
| [[alex-yaazarai]] | Yaazarai / Alex，GameMaker 社区 shader 开发者，Radiance Cascades 两部教程作者 |
| [[alexander-sannikov]] | Grinding Gear Games 图形程序员，Radiance Cascades 算法提出者 |
| [[oakleaff]] | Oakleaff，GameMaker 业余 3D/shader 开发者，volumetric + cascaded shadow 教程 |
| [[mark-lundin]] | PlayCanvas 团队，@playcanvas/react 作者 |
| [[jendrik-illner]] | Jendrik Illner，Graphics Programming Weekly 主理人 |
| [[kris-bamrah]] | PlayCanvas 团队，Editor 开源与 VSCode Extension 公告的作者 |
| [[sirawat-pitaksarit]] | Sirawat Pitaksarit，Unity DOTS / 音频插件开发者（Game Torrahod 博客） |
| [[daniel-pokladek]] | Daniel Pokladek，Unity shader 学习博客 danielpokladek.me 作者 |
| [[rune-skovbo-johansen]] | 丹麦独立开发者/前 Unity 工程师（Eye of the Temple, The Big Forest, Phacelle Noise, Erosion Filter） |
| [[chips-and-cheese]] | Chips and Cheese 集体作者页（CPU/GPU 微架构实测博客） |
| [[chester-lam]] | Chips and Cheese 主笔，缓存/内存/互连延迟带宽实测的主要贡献者 |
| [[sam-lapere]] | Sam Lapere，OTOY / NVIDIA，Ray Tracey 博客作者，GPU 路径追踪长期记录者 |
| [[joost-van-dongen]] | Joost van Dongen，Ronimo 共同创始人（Awesomenauts / Proun），Galaxy Grove CEO |


| [[alfred-baudisch]] | Alfred Reinold Baudisch，巴西 Elixir/Godot indie dev，《Brazilian Street Food Simulator》作者 |
| [[gemserk]] | Gemserk / Ariel Coppes，独立工作室，Unity 工程实战博客 |
| [[ben-supnik]] | Ben Supnik，Laminar Research / X-Plane 图形与引擎程序员 |
| [[nikos-papadopoulos]] | Nikos Papadopoulos（4rknova），图形 / 仿真工具型博客作者 |
| [[boris-the-brave]] | Sylves/WFC 作者，现 Timaeus（SLT / AI Safety）研究员 |
| [[sebastian-schoener]] | Sebastian Schöner，Unity Mono/IL2CPP codegen 改良、Zig/C++ 底层工程 |
| [[michael-allar]] | Michael Allar — UE4 救火顾问、ue4.style 维护者 |
| [[ted-sie]] | Ted Sie，Unity 中文技术博客作者（分形 / DOTS / 群体仿真） |
| [[outerra-team]] | Brano Kemen / Angrypig Kralik —— Outerra 行星引擎双人组 |
| [[sebastiano-mandala]] | Sebastiano Mandalà — Svelto.ECS 作者、Freejam 工程师 |
| [[tom-looman]] | Tom Looman，前 Epic Games，UE C++ 教程与性能优化长期撰稿者 |
| [[wolfgang-engel]] | Confetti 联创、The Forge 主推，ShaderX/GPU Pro/GPU Zen 编辑，Light Pre-Pass 提出者 |
| [[panagiotis-charitos]] | AnKi 3D Engine 作者，anki3d.org 博客作者 |
| [[pekka-vaananen]] | 30fps.net 博主，芬兰独立渲染研究者，擅长 notebook 式图形实验 |
| [[yining-karl-li]] | Disney Animation Hyperion 渲染工程师，Code & Visuals 博主 |
| [[16bpp]] | 16BPP.net 博主，PSRayTracing 作者，靠全矩阵 benchmark 重测 C++ 性能主张 |
| [[jon-olick]] | 前 id Software 程序员，JO JPEG / jo_*.h 单文件库系列作者 |
| [[adam-sawicki]] | AMD D3D12MA / VMA 作者，asawicki.info 博主，DX12 低层与 GPU 内存专家 |
| [[ming-wai-chan]] | Ming Wai Chan（cmwdexint），Unity URP 实用贴士 |
| [[thomas-poulet]] | 图形咨询 + 物理游戏独立开发，帧分析系列作者（blog.thomaspoulet.fr）|
| [[ben-ui]] | benui.ca，UE5 UI/UX 专家，前 Brace Yourself Games Lead Programmer |
| [[chris-wellons]] | Chris Wellons (skeeto)，nullprogram.com，C/Wasm/Windows 底层 |
| [[graphics-guy-notes]] | Jiayin Cao，NVIDIA（前 Naughty Dog），SORT/TSL 作者，Zorah ReSTIR PT 实装参与者 |
| [[alex-harri-jonsson]] | 冰岛软件工程师，博客 alexharri.com 深挖 Web 剪贴板、trie 压缩、ASCII 渲染等细节主题 |
| [[steven-wittens]] | Steven Wittens，acko.net 作者，Use.GPU 创建者，UI 与渲染架构评论家 |
| [[adrian-courreges]] | Adrian Courrèges，frame-analysis 写作范式奠基者；Switch AAA UE4 优化补丁作者 |
| [[branimir-karadzic]] | Branimir Karadžić，bgfx 作者，Orthodox C++ 提出者 |
| [[bruno-opsenica]] | Bruno Opsenica（bruop）：BGFX/DX12 渲染库作者，IBL 与 culling SIMD 实战 |
| [[people/erfan-ahmadi]] | Erfan Ahmadi，Nabla 框架贡献者、The Forge Bokeh DoF UnitTest 作者 |

| [[daniel-chase-hooper]] | 独立开发者，前 Apple，Principle 作者；C / Swift / 工具链 |
| [[stephen-gutekanst]] | Emi / emidoots，Mach 引擎与 Hexops 作者 |
| [[blueswordm]] | Chips and Cheese 编解码方向撰稿人 |
| [[people/marte-randomtower]] | Marte，Random Tower 博客作者，Flash/AS3 独立游戏开发者 |
| [[nikos-papadopoulos]] | Nikos Papadopoulos（Arkanova），希腊 demoscene / Linux 图形程序员，4rknova.com 站长 |
| [[patrick-stein]] | Patrick Stein（nklein software），Common Lisp / CL-OpenGL 爱好者，TC Lispers 活跃贡献者 |
| [[dave-evans]] | Dave Evans，PlayCanvas 联合创始人，早期博客主力作者 |
## 源摘要（wiki/sources/）
| 源 | 一句话描述 |
|---|---|
| [[sources/custom-srp-6-1-0]] | Custom SRP 6.1.0 教程摘要 |
| [[sources/aposd-day01]] | APoSD Day 1：Introduction |
| [[sources/aposd-day02]] | APoSD Day 2：复杂性的定义与症状 |
| [[sources/aposd-day03]] | APoSD Day 3：战术 vs 战略编程 |
| [[sources/aposd-day04]] | APoSD Day 4：深模块 |
| [[sources/aposd-day05]] | APoSD Day 5：浅模块之罪与 Classitis |
| [[sources/aposd-day06]] | APoSD Day 6：信息隐藏 |
| [[sources/sicp-day01]] | SICP Day 1：编程的三要素 |
| [[sources/sicp-day02]] | SICP Day 2：过程即黑盒 |
| [[sources/sicp-day03]] | SICP Day 3：递归过程 vs 迭代过程 |
| [[sources/sicp-day04]] | SICP Day 4：增长阶与快速幂 |
| [[sources/sicp-day05]] | SICP Day 5：概率素数判定 |
| [[sources/sicp-day06]] | SICP Day 6：高阶函数 |
| [[sources/rtr-day01]] | RTR Day 1：渲染管线架构 |
| [[sources/rtr-day02]] | RTR Day 2：Application 阶段 |
| [[sources/rtr-day03]] | RTR Day 3：Geometry Processing |
| [[sources/rtr-day04]] | RTR Day 4：Rasterization |
| [[sources/rtr-day05]] | RTR Day 5：Pixel Processing |
| [[sources/rtr-day06]] | RTR Day 6：一帧的完整生命 |
| [[sources/gea-day01]] | GEA Day 1：引擎是什么 |
| [[sources/gea-day02]] | GEA Day 2：引擎演化史 |
| [[sources/caqa-day01]] | CAQA Day 1：量化方法 |
| [[sources/caqa-day02]] | CAQA Day 2：存储层次与可靠性 |
| [[sources/csapp-day01]] | CSAPP Day 1：信息是上下文中的比特 |
| [[sources/ciechanow-color-spaces]] | Ciechanowski：色彩空间三要素与线性域运算 |
| [[sources/ciechanow-alpha-compositing]] | Ciechanowski：Porter-Duff 合成与预乘 α |
| [[sources/ciechanow-cameras-and-lenses]] | Ciechanowski：从针孔到薄透镜的光学推导 |
| [[sources/bartwronski-exposure-fusion]] | Wronski：Exposure Fusion 与局部色调映射 |
| [[sources/bartwronski-iir-deconvolution]] | Wronski：梯度下降学 IIR 滤波器反卷积 |
| [[sources/bartwronski-poisson-sampling]] | Wronski：Poisson 采样生成器 |
| [[sources/bartwronski-csharprenderer-debug]] | Wronski：CSharpRenderer GPU printf 与 surface snapshot |
| [[sources/ryg-exact-unorm8-to-float]] | ryg：UNORM8 → float 的精确转换 |
| [[sources/ryg-sinc-and-polynomial-interpolation]] | ryg：sinc 与多项式插值的关系 |
| [[sources/ryg-sse-mind-the-gap]] | ryg：SSE/SSE2 的非正交性 trick 集 |
| [[sources/ryg-trip-through-graphics-pipeline-2011-part-6]] | ryg：Pineda 算法与硬件光栅化 |
| [[sources/ryg-models-for-adaptive-arithmetic-coding]] | ryg：Oodle LZNA 背后的多元自适应模型 |
| [[sources/aras-rapidhash-unity-port]] | Aras：rapidhash 的 Unity Burst 移植与 XXH3 对比 |
| [[sources/aras-gpu-point-rasterization]] | Aras：硬件点光栅化为何输给朴素 compute shader |
| [[sources/aras-blender-vse-image-filtering]] | Aras：Blender VSE 的图像滤波考古 |
| [[sources/c0de517e-cached-shadowmaps]] | Pesce：远级联阴影缓存的半成品想法 + Mike Day 的完整实现 |
| [[sources/c0de517e-tiled-hardware-speculations]] | Pesce + ryg：TBDR vs IMR 的软件侧推演与硬件侧修正 |
| [[sources/elopezr-rotr-rendering]] | López：Rise of the Tomb Raider 逐帧渲染分析 |
| [[sources/elopezr-taa-holy-trail]] | López：TAA 完整 tutorial（jitter 到 rectification 全流程） |
| [[sources/peters-spectral-rendering-1-spectra]] | Peters：光谱渲染三部曲 Part 1 — 光谱从哪来 |
| [[sources/peters-spectral-rendering-2-real-time]] | Peters：光谱渲染三部曲 Part 2 — 实时路径追踪里的波长 MC 采样 |
| [[sources/peters-gpu-polynomial-roots]] | Peters：GPU 上的多项式实根求解与反寄存器溢出设计 |
| [[sources/peters-projected-spherical-caps]] | Peters & Dachsbacher i3D 2019：球形光源投影立体角的实时采样 |
| [[sources/chajdas-assisted-probe-placement]] | Chajdas：环境探针辅助放置（CWW11 回顾） |
| [[sources/slater-qmc-crash-course]] | Slater：Monte Carlo 速成 Part 5 — Quasi-Monte Carlo |
| [[sources/slater-exile-voxel-rendering]] | Slater：Exile 引擎的体素渲染管线 |
| [[sources/slater-exile-reflection]] | Slater：Exile 引擎的 libclang 元程序反射 |
| [[sources/slater-functions-are-vectors]] | Slater：Functions are Vectors — 函数即无限维向量 |
| [[sources/slater-compiler-bug]] | Slater：MSVC 2019 interference analysis 的栈重叠 codegen bug |
| [[sources/xor-mini-jfa]] | Xor：JFA 在 GPU 上生成距离场 |
| [[sources/xor-mini-oklab]] | Xor：OKLab 感知均匀色彩混合 |
| [[sources/xor-mini-3d-rotation]] | Xor：Euler / Axis-Angle 3D 旋转入门 |
| [[sources/xor-efficient-chaos]] | Xor：黄金角分层网格的廉价伪随机 |
| [[sources/xor-shadowmaps]] | Xor：shadow mapping 完整入门教程 |
| [[sources/selfshadow-multi-faceted-part-2]] | Hill：微表面多次散射补偿 lobe 的推导与 Fms 修正 |
| [[sources/selfshadow-blending-in-detail]] | Hill & Barré-Brisebois：Reoriented Normal Mapping |
| [[sources/selfshadow-pbs-siggraph-2014]] | Hill：SIGGRAPH 2014 PBS 课程导读 |
| [[sources/selfshadow-practical-visibility]] | Hill & Collin：Conviction HZB + Battlefield SPU 软光栅遮挡 |
| [[sources/3dgep-learning-directx12-lesson3]] | van Oosten：D3D12 Lesson 3，资源绑定与状态跟踪封装 |
| [[sources/3dgep-cuda-memory-model]] | van Oosten：CUDA 五种内存 + 矩阵乘 tiling 优化 |
| [[sources/green-sh-lighting-gritty-details]] | Robin Green：SH 光照在 PS2 上的落地回顾 |
| [[sources/green-implementing-needlets]] | Robin Green：Needlet 球面 wavelet 的实现配方 |
| [[sources/green-faster-math-functions]] | Robin Green：GDC 2002/2003 Faster Math Functions tutorial 回顾 |
| [[sources/green-display-edid-colorspace]] | Robin Green：用 PowerShell + WMI 抽 EDID 色度 |
| [[sources/green-procedural-rendering-ps2]] | Robin Green：GDC 2001 PS2 过程式几何 demo 回顾 |
| [[sources/raphlinus-smooth-resize-test]] | Raph：把窗口拖拽抖动当作 GUI 架构体检 |
| [[sources/raphlinus-rust-2021-gui]] | Raph：Rust GUI 生态现状、Druid 定位、收敛难题 |
| [[sources/raphlinus-fearless-simd]] | Raph：Rust 下可移植 SIMD 的愿景与双层 trait 探索 |
| [[sources/apoorvaj-calling-conventions]] | Joshi：cdecl/stdcall/fastcall 三路汇编 diff |
| [[sources/apoorvaj-zooming-and-panning]] | Joshi：Papaya GPU 图像编辑器笔刷与缩放的性能拆解 |
| [[sources/jasper-how-to-write-a-renderer]] | Jasper：现代图形 API 渲染器的三条轴线（draw call / render pass / data upload） |
| [[sources/jasper-dri-linux-graphics-stack]] | Jasper：拆开 DRI/DRM/KMS/libdrm/wl_drm 的命名迷雾 |
| [[sources/playcanvas-profiler]] | PlayCanvas Profiler 发布公告：帧耗时分解 + 启动时间轴 |
| [[sources/playcanvas-volumetric-video]] | PlayCanvas 集成 MRCS 体积视频到 WebXR AR/VR 的项目复盘 |
| [[sources/halisavakis-shaderquest-shaping-functions]] | Alisavakis：ShaderQuest 第六篇，着色器塑形函数入门 |
| [[sources/ronja-planar-mapping]] | Ronja：用世界坐标 xz 生成 UV 的三阶段演进 |
| [[sources/ronja-texture-dissolve]] | Ronja：纹理驱动的 clip 溶解 + HDR 边缘发光 |
| [[sources/ronja-2d-sdf-basics]] | Ronja：2D SDF 基元、变换作用在采样点上、fwidth 抗锯齿 |
| [[sources/ronja-2d-sdf-shadows]] | Ronja：SDF sphere-tracing 软阴影的 `min(d/t)` 单行技巧 |
| [[sources/ronja-draw-procedural]] | Ronja：DrawProcedural + StructuredBuffer 的 GPU-driven 入门 |
| [[sources/cyan-urp-post-processing]] | Cyan：URP 后处理（Volume + Blit Render Feature） |
| [[sources/cyan-uv-based-nodes]] | Cyan：Shader Graph 的 UV 操作节点总览 |
| [[sources/cyan-retro-crt-shader]] | Cyan：复古 CRT shader 的 5 效果拆解 |
| [[sources/cyan-scene-color-depth]] | Cyan：Scene Color / Scene Depth 节点跨管线行为 |
| [[sources/cyan-particle-custom-vertex-streams]] | Cyan：粒子系统到 Shader Graph 的逐粒子数据通道 |
| [[sources/lindenreid-basic-math-for-shaders]] | Reid：shader 向量数学入门（视觉化 > 抽象符号） |
| [[sources/lindenreid-procedural-geometry-part2]] | Reid：Unity Mesh API 从零构造 cube + winding order |
| [[sources/lindenreid-foggy-window-shader]] | Reid：GrabPass + 可分 blur + 纹理编码时间的可交互雾化窗户 |
| [[sources/vertexfragment-diamond-square-gpu]] | Sell：Diamond-Square 三种实现对比与 GPU 加速复盘 |
| [[sources/vertexfragment-dots-character-controller]] | Sell：Unity DOTS kinematic 角色控制器详细实现 |
| [[sources/vertexfragment-list-removal]] | Sell：C# List.RemoveAt 性能陷阱与 swap-and-pop 解法 |
| [[sources/vertexfragment-deferred-grass]] | Sell：Unity 延迟管线下的 5 阶段草地着色方案 |
| [[sources/danielilett-cel-shading-part-1]] | Daniel Ilett：Cel Shading 系列 1，Lambert 漫反射的 Unity 实现 |
| [[sources/danielilett-your-first-shader]] | Daniel Ilett：Unity 6 + URP 的第一个代码 shader，ShaderLab+HLSL 最小骨架 |
| [[sources/danielilett-retro-terrain-lit]] | Daniel Ilett：Retro Terrain Lit shader 参数与 PS1/N64 复古技术清单 |
| [[sources/danielilett-dither-transparency]] | Daniel Ilett：URP Lit shader 的 Bayer dither 伪透明参数集 |
| [[sources/alanzucconi-improving-rainbow-2]] | Zucconi：branchless 波长→RGB 拟合 `spectral_zucconi(6)` |
| [[sources/alanzucconi-cdrom-diffraction-2]] | Zucconi：CD-ROM 衍射光栅着色器 + 从 UV 推切向 |
| [[sources/alanzucconi-fast-sss-1]] | Zucconi：Barré-Brisebois / Frostbite 廉价假 SSS 移植到 Unity |
| [[sources/alanzucconi-volumetric-rendering]] | Zucconi：体积 raycasting 与 raymarching 入门 |
| [[sources/alanzucconi-journey-sand-specular]] | Zucconi：Journey 沙丘 rim lighting + ocean specular 拆解 |
| [[sources/gameknife-gknextrenderer-yearone]] | gameknife：从 DX11 追赶现代渲染的一年总结 |
| [[sources/gameknife-tbdr-performance-tuning]] | Bruce Merry TBDR 性能调校中译（gameknife 译） |
| [[sources/gameknife-pathfinding-review]] | gameknife：A* 与动态环境寻路的重新审视 |
| [[sources/gameknife-gkengine-features]] | gameknife：gkEngine 2015 年技术特性清单 |
| [[sources/allenchou-game-physics-introduction]] | Allen Chou：约束式刚体物理引擎的流水线概览与术语表 |
| [[sources/allenchou-rusher-2-composite-commands]] | Allen Chou：ActionScript 3 / Rusher 2 框架下 Serial / Parallel 复合命令用法 |
| [[sources/frost-kiwi-luts-in-video-games]] | Frost：1D/3D LUT 在视频游戏中的各种用法（L4D tinting 到 Resolve 调色） |
| [[sources/frost-kiwi-analytical-anti-aliasing]] | Frost：SSAA/MSAA/FXAA/AAA 对比长文与 AAA 实现细节 |
| [[sources/metalbyexample-up-and-running-1]] | Warren Moore：Metal 第 1 篇——清屏到红色 |
| [[sources/metalbyexample-up-and-running-2]] | Warren Moore：Metal 第 2 篇——带色三角形与 MSL 入门 |
| [[sources/metalbyexample-whats-and-wherefores]] | Warren Moore：Metal 的「抽象下界」立场与未来判断 |
| [[sources/simonschreibt-deus-ex-occlusion]] | Simon：Deus Ex 的预烘焙角落遮蔽与 UE1 lightmap bug |
| [[sources/simonschreibt-diablo3-trees]] | Simon：Diablo 3 如何用两张三角形画出细剪影的树 |
| [[sources/simonschreibt-divine-divinity-reflection]] | Simon：Divine Divinity 2D 水面反射的猜测与读者讨论 |
| [[sources/simonschreibt-fallout3-edges]] | Simon：Fallout 3 用 normal decal 壳掩盖低多边形石头的硬边 |
| [[sources/simonschreibt-teleglitch-rgb]] | Simon：Teleglitch 传送器的 RGB 通道独立偏移特效 |
| [[sources/frost-kiwi-color-banding]] | Frost：一行 GLSL dither 消色带 + 五家业界实现横评 |
| [[sources/frost-kiwi-thermal-colormaps]] | Frost：matplotlib colormap → DaVinci Resolve .cube 工具脚本 |
| [[sources/interplay-tools-of-the-trade]] | Anagnostou：shader 原型与调试工具栈总览（2013） |
| [[sources/interplay-depth-testing]] | Anagnostou：D3D11 depth testing 阶段与 Early-Z 救援语义 |
| [[sources/interplay-tangent-free-normal-mapping]] | Anagnostou：Christian Schüler 免 TBN 法线贴图的 FX Composer 实测 |
| [[sources/interplay-unity-as-fxcomposer]] | Anagnostou：Unity 免费版替代 FX Composer 做 shader 原型 |
| [[sources/interplay-sharpdx-model-loading]] | Anagnostou：SharpDX + Assimp 补齐 XNA 式内容管线 |
| [[sources/etodd-meshes-of-navigation]] | Todd：把 Recast 接入 A3P 的 navmesh 管线 |
| [[sources/etodd-refactoring-with-components]] | Todd：端口式的组件数据绑定方案 |
| [[sources/karis-virtualized-volume-textures]] | Karis：把 2D virtual texture 和 SVO 思路搬到 irradiance volume |
| [[sources/karis-tiled-light-culling]] | Karis：tile 级 per-light 剔除加入 specular cone 方向约束 |
| [[sources/karis-sparse-shadows-tracing]] | Karis：next-gen 渲染需要多几何表示 + cone trace，UE5 Lumen 的雏形 |
| [[sources/cloudwu-c-module-interface]] | 云风：C 语言模块化与接口设计 |
| [[sources/cloudwu-cpp-mark-sweep-gc]] | 云风：200 行的 C++ 标记清除 GC |
| [[sources/cloudwu-c-serialization-and-c-oop]] | 云风：C 结构序列化、C OOP 与 protected |
| [[sources/cloudwu-game-engine-vfs]] | 云风：实现一个简单的虚拟文件系统 |
| [[sources/cloudwu-malloc-wrapper]] | 云风：给 malloc 加壳 |
| [[sources/interplay-instant-radiosity-light-prepass]] | Anagnostou：在 light prepass 上跑 Instant Radiosity |
| [[sources/interplay-parallax-corrected-cubemap]] | Anagnostou：用任意 cubemap 做视差修正反射的 hack |
| [[sources/interplay-interpolate-view-light-vectors]] | Anagnostou：大三角形上归一化向量的插值 bug |
| [[sources/interplay-dual-depth-thickness]] | Anagnostou：ShaderX6 厚度技巧的 front/back 分流改进 |
| [[sources/interplay-lighting-alpha-deferred]] | Anagnostou：deferred 下给透明物打光的四条路 |
| [[sources/peters-moment-shadow-mapping]] | Peters & Klein：四阶矩阴影贴图原论文（I3D 2015） |
| [[sources/peters-trigonometric-moment-transient-imaging]] | Peters et al.：三角矩 + AMCW lidar 的快速瞬态成像（SGA 2015） |
| [[sources/peters-beyond-hard-shadows-msm]] | Peters et al.：MSM 扩展到单次散射/软阴影/半透明遮挡（I3D 2016） |
| [[sources/bartwronski-future-of-ssr]] | Wronski：屏幕空间反射的 Good / Bad / Ugly（AC4 复盘） |
| [[sources/bartwronski-temporal-supersampling]] | Wronski：时域超采样与 TAA 的祖师级长文（AC4 实战） |
| [[sources/bartwronski-gcn-latency-hiding]] | Wronski：GCN 两种延迟隐藏机制与 wave occupancy |
| [[sources/aras-more-hash-function-tests]] | Aras 2016：非加密哈希横向评测（多平台多尺寸） |
| [[sources/aras-voronoi-hashing-osl]] | Aras 2025：Blender Voronoi 节点换 PCG3D 哈希的完整故事 |
| [[sources/aras-lossless-float-image-compression]] | Aras 2025：EXR/HTJ2K/JPEG-XL/meshoptimizer 浮点图像压缩横评 |
| [[sources/aras-openexr-vs-tinyexr]] | Aras 2025：tinyexr vs OpenEXR 官方库的体积、速度、特性对比 |
| [[sources/raphlinus-smooth-resize-direct2d]] | Raph Levien 2018：Direct2D smooth resize 悬赏与三路径失败分析 |
| [[sources/raphlinus-gpu-unescaping]] | Raph Levien 2018：用 monoid 同态把字符串反转义搬到 GPGPU |
| [[sources/raphlinus-ecs-ui-rust]] | Raph Levien 2018：xi-win-ui 的「类 ECS」Rust GUI 架构笔记 |
| [[sources/raphlinus-gpu-json-parsing]] | Raph Levien 2018：scan + scatter + sort 并行解析 Dyck 语言 |
| [[sources/ryg-cellular-textures-1]] | ryg：Werkkzeug3 细胞纹理的四种算法对比（为什么树最慢） |
| [[sources/ryg-cellular-textures-2]] | ryg：空间递归细分算法把细胞纹理生成推到近似 O(|pixels|) |
| [[sources/ryg-carry-save-adders]] | ryg：CSA 恒等式与打包像素的无溢出平均 SWAR 技巧 |
| [[sources/ryg-data-structures-and-invariants]] | ryg：数据结构不变量的诞生与 sentinel / pointer-to-pointer 清理法 |
| [[sources/elopezr-floyd-steinberg-dithering]] | López Ros：Android 上把 Floyd–Steinberg 压榨 30% 的四次迭代 |
| [[sources/elopezr-dragon-mania]] | López Ros：MIDP 老引擎 Android port 从 3 fps 抢救到 15 fps |
| [[sources/elopezr-will-of-flame]] | López Ros：自研 Java Android 引擎的独立射击游戏项目档案 |
| [[sources/elopezr-wof-editors]] | López Ros：Python/wxPython 的关卡+复合实体编辑器 |
| [[sources/elopezr-java-vector-math]] | López Ros：Java 缺运算符重载与值类型，如何毁了向量数学 |
| [[sources/xor-mini-texels-pixels]] | Xor：纹素与像素之间的换算 |
| [[sources/xor-mini-recursive-shaders]] | Xor：多趟 shader 与 ping-pong surface |
| [[sources/xor-mini-code-golfing]] | Xor：shader code golf 技巧与恒等式 |
| [[sources/xor-mini-dot-product]] | Xor：点乘在 shader 里的三种用法 |
| [[sources/xor-mini-creative-code]] | Xor：从虫洞到飓风的 shader creative coding 流程 |
| [[sources/ciechanow-exploring-gpgpu-ios]] | Ciechanowski：在 A7 iOS 上用 Transform Feedback 做 GPGPU 的过时但经典 hack |
| [[sources/ciechanow-drawing-bezier-curves]] | Ciechanowski：Revolved 里 Bézier 曲线描边的 GPU 三角化方案 |
| [[sources/ciechanow-exposing-nsmutablearray]] | Ciechanowski：逆向 `__NSArrayM` 发现它是循环缓冲 deque |
| [[sources/ciechanow-exposing-nsdictionary]] | Ciechanowski：逆向 `__NSDictionaryI` 发现它是 indexed ivars + 线性探测 |
| [[sources/ciechanow-nsdictionary-objectforkey-assembly]] | Ciechanowski：`objectForKey:` 的 60 条 ARM64 汇编逐行译读 |
| [[sources/halisavakis-bluk-2d-fog-sprite]] | Alisavakis：BLUK 视觉风格的 2D 雾精灵着色器拆解 |
| [[sources/halisavakis-image-effects-intro]] | Alisavakis：Unity image effect 入门教程 |
| [[sources/halisavakis-night-time-shader]] | Alisavakis：夜色全屏后处理示例 |
| [[sources/danielilett-image-effects-shader-primer]] | Ilett：Image Effects Part 0 - ShaderLab / HLSL 样板 |
| [[sources/danielilett-image-effects-colour-transforms]] | Ilett：Image Effects Part 1 - 灰度与 Sepia 颜色变换 |
| [[sources/danielilett-image-effects-depth-silhouette]] | Ilett：Image Effects Part 2 - 采样深度纹理做剪影 |
| [[sources/danielilett-image-effects-blurring]] | Ilett：Image Effects Part 3 - Box/Gaussian Blur 与可分离卷积 |
| [[sources/ronja-structure]] | Ronja 001：Shader/SubShader/Pass 层级结构与 ShaderLab 声明式语义 |
| [[sources/ronja-hlsl]] | Ronja 002：HLSL 标量/向量/swizzle/控制流速通，反教条写 if |
| [[sources/ronja-variables]] | Ronja 003：object data / interpolators / uniforms 三种数据来源与语义标签 |
| [[sources/ronja-basic-shader]] | Ronja 004：UnityObjectToClipPos + TRANSFORM_TEX + tex2D 组出第一个 Unlit shader |
| [[sources/ronja-surface-shader-basics]] | Ronja 005：从手写 Unlit 转 Surface Shader，SurfaceOutputStandard 七字段速查 |
| [[sources/alanzucconi-flixel-retro-crt]] | Zucconi：Flixel 2.5 上的 CPU 版 CRT 通道错位后处理（2012） |
| [[sources/slater-exile-hot-reloading]] | Slater：Exile C++ 引擎的 DLL 热重载实现与五道坑 |
| [[sources/slater-hamming-hats]] | Slater：Hamming 码解 31 人帽子谜题的最优策略证明 |
| [[sources/slater-exponential-rotations]] | Slater：用矩阵 exp/log 统一旋转表示与 Karcher mean |
| [[sources/slater-autodiff]] | Slater：autodiff 从零到 JAX 视角，附图像反模糊 demo |
| [[sources/lindenreid-procedural-stellation]] | Reid：把三角形拱成 tetrahedron 做程序化星体 |
| [[sources/lindenreid-procedural-extrusion]] | Reid：沿法线把三角形挤成三棱柱 |
| [[sources/lindenreid-procedural-torus]] | Reid：圆环作为两层嵌套圆的参数方程 |
| [[sources/lindenreid-procedural-sphere-ellipsoid]] | Reid：UV-sphere 与各向异性 ellipsoid 的参数化 |
| [[sources/lindenreid-mesh-tessellation-triangulation]] | Reid：Fan / Centroid / Triforce 三种实用三角化算法 |
| [[sources/cyan-render-textures]] | Cyan：Unity Render Texture 与 AsyncGPUReadback 异步回读 |
| [[sources/cyan-voronoi]] | Cyan：Shader Graph Voronoi 节点拆解与 cell 边缘 Custom Function |
| [[sources/cyan-triplanar-mapping]] | Cyan：World-space UV 与 Triplanar Mapping 的 Shader Graph 实现 |
| [[sources/cyan-orthographic-depth]] | Cyan：正交相机下 Scene Depth 节点的平台差异与深度差/世界坐标重建 |
| [[sources/cyan-watercolour-shader-experiments]] | Cyan：水彩观感的三层 URP shader（mesh + Blit + decal）|
| [[sources/3dgep-math-primer-vectors]] | Jeremiah：3D 数学向量篇——dot/cross/投影分解的几何直觉 |
| [[sources/3dgep-math-primer-matrices]] | Jeremiah：3D 数学矩阵篇——线性 vs 仿射、行列式、正交矩阵的求逆捷径 |
| [[sources/3dgep-directx9-intro]] | Jeremiah：D3D9 入门历史文献，COM 释放语义与 fixed-function 末期形态 |
| [[sources/3dgep-md5-loading-animating]] | Jeremiah：MD5 模型格式解析与 CPU 端骨骼动画完整实现 |
| [[sources/3dgep-md5-gpu-skinning]] | Jeremiah：把 MD5 蒙皮搬到 vertex shader，矩阵调色板算法的早期典范 |
| [[sources/vertexfragment-bresenham-lines]] | Steven Sell：Bresenham 直线算法与 roguelike 动机 |
| [[sources/vertexfragment-variable-length-bresenham]] | Steven Sell：可变长度 Bresenham 及现代 CPU 上的反优化胜出 |
| [[sources/vertexfragment-performance-conscious-webgl]] | Steven Sell：WebGL 中三个反直觉的 JS 性能陷阱 |
| [[sources/vertexfragment-cantor-szudzik-pairing]] | Steven Sell：Cantor 与 Szudzik 配对函数对比 |
| [[sources/eliasdaler-lua-cpp-binding-series]] | Daler：Lua 与 C++ 绑定教程三连（Part 1/2/2.5） |
| [[sources/eliasdaler-z-order-top-down-2d]] | Daler：俯视角 2D 游戏的 z-order 算法 |
| [[sources/giordi91-rust-disassembly-part-1]] | Marco Giordano：Rust 语言特性反汇编导览 |
| [[sources/giordi91-grass-shader]] | Marco Giordano：GPU 驱动瓦片化草地系统 |
| [[sources/giordi91-handle-resource-management]] | Marco Giordano：句柄 + manager 式资源管理 |
| [[sources/peters-msm-gdce2016-talk]] | Peters：GDCE 2016 一小时 MSM 落地讲座 |
| [[sources/peters-cubic-equation-revisited]] | Peters：HLSL 三次方程快速闭式解（2016） |
| [[sources/peters-msm-jcgt2016-demo]] | Peters：MSMDemoV2，带文档的 HLSL shadow demo（2016-09） |
| [[sources/peters-improved-msm-jcgt2017]] | Peters et al.：MSM 三类应用 + 改进（JCGT 2017） |
| [[sources/peters-non-linearly-quantized-msm]] | Peters：非线性量化 MSM 与 on-chip compute filtering（HPG 2017） |
| [[sources/anteru-directx11-hints]] | Chajdas：DirectX 11 早期开发踩坑笔记（tessellation / CS / HLSL） |
| [[sources/anteru-homogeneous-rasterization-gotcha]] | Chajdas：齐次坐标三角形光栅化的转置陷阱与 debug 教训 |
| [[sources/anteru-avoid-unsigned-types]] | Chajdas：默认避免 C++ unsigned 类型（重述 Scott Meyers 论点） |
| [[sources/apoorvaj-opengl-loading]] | Joshi：从零写一个 OpenGL loader 替换 GLEW |
| [[sources/apoorvaj-normal-mapping]] | Joshi：tangent space 法线贴图与 parallax 家族 WebGL demo |
| [[sources/cloudwu-masterminds-lua-chapter]] | 云风：《编程之魂》第七章 Lua 访谈校译稿 |
| [[sources/cloudwu-c-tagged-union-dispatch]] | 云风：C 语言 tagged union 风格的多变体接口 |
| [[sources/cloudwu-resource-pack-format]] | 云风：网易资源包格式回顾与新设计 |
| [[sources/cloudwu-effective-cpp-comments]] | 云风：Effective C++ 3rd Item 1 评注 |
| [[sources/playcanvas-html5-game-apis]] | Evans：2012 年 HTML5 游戏开发 API 可用性清单 |
| [[sources/interplay-normalised-blinn-phong]] | Anagnostou：归一化 Blinn-Phong 的 PBR 教学 shader（2013） |
| [[sources/interplay-branches-texture-sampling]] | Anagnostou：if 分支内 tex2D gradient 的隐形性能坑（2014） |
| [[sources/interplay-fur-tessellation]] | Anagnostou：D3D11 isoline tessellation 渲染 fur 的原型方案（2014） |
| [[sources/interplay-skysaga-rendering]] | Anagnostou：SkySaga Meandros 引擎完整管线总览（2015） |
| [[sources/halisavakis-image-effects-simple-masks]] | Alisavakis：image effect 的灰度遮罩混合 |
| [[sources/halisavakis-image-effects-chromatic-aberration]] | Alisavakis：自写的 RGB 三通道色差后处理 |
| [[sources/halisavakis-image-effects-grabpass]] | Alisavakis：GrabPass 把 image effect 移植到物体上 |
| [[sources/halisavakis-image-effects-simple-displacement]] | Alisavakis：灰度遮罩驱动的 UV 位移与冲击波雏形 |
| [[sources/halisavakis-image-effects-waving-displacement]] | Alisavakis：RG 向量场 + _Time 滚动的水波位移 |
| [[sources/bartwronski-bokeh-insane-pt1]] | Wronski：_The Witcher 2_ 的 scatter bokeh 实现与 2014 年 C# 重实现（2014） |
| [[sources/bartwronski-temporal-ssao]] | Wronski：AC4 上 temporal SSAO 的 before/after 演示与原理解释（2014） |
| [[sources/bartwronski-editor-console-connection]] | Wronski：_The Witcher 2_ X360 编辑器-主机实时调参工具链复盘（2014） |
| [[sources/ryg-cycle-detection]] | ryg：Floyd 与 Brent 环检测；Brent 是迭代加深的实例 |
| [[sources/ryg-64-bit-tidbits]] | ryg：x86-64 C 提升规则坑与 PS3 PPU GCC 的指针包装 |
| [[sources/ryg-view-frustum-culling]] | ryg：AABB-vs-frustum 方法链，从 baseline 到 SPU SIMD |
| [[sources/ryg-frustum-culling-notes]] | ryg：culling 层级设计、cone vs frustum、clip-space 2D bbox 的多用途 |
| [[sources/ryg-finish-your-derivations]] | ryg：写完 shader 数学的 5 分钟检查单，Oren-Nayar 化简为示范 |
| [[sources/danielilett-image-effects-edge-detection-bloom]] | Ilett：Image Effects Part 4 - Sobel 边缘检测 + 简易 Bloom |
| [[sources/danielilett-image-effects-retro-crt]] | Ilett：Image Effects Part 5 - NES/SNES/GB 颜色量化 + CRT 扫描线 |
| [[sources/danielilett-image-effects-kuwahara]] | Ilett：Image Effects Part 6 - Kuwahara 油画滤镜 |
| [[sources/ronja-basic-transparency]] | Ronja：Unity 透明 shader 的 Queue+Blend+ZWrite 三件套 |
| [[sources/ronja-sprite-shaders]] | Ronja：Cull Off + 顶点色让透明 shader 变 sprite shader |
| [[sources/ronja-color-interpolation]] | Ronja：lerp 的凸组合推导与 mask-driven 混合 |
| [[sources/ronja-triplanar-mapping]] | Ronja：手写 triplanar，含法线逆转置矩阵推导 |
| [[sources/ronja-checkerboard-pattern]] | Ronja：floor+frac 量化奇偶生成程序化棋盘 |
| [[sources/xor-mini-raymarching]] | Xor：sphere-traced raymarching 入门 |
| [[sources/xor-mini-rotation]] | Xor：从 2D 三角到 3D 欧拉角的 shader 旋转入门 |
| [[sources/xor-mini-two-textures]] | Xor：GameMaker texture page 与 UV 归一化 |
| [[sources/xor-mini-shadertoy]] | Xor：ShaderToy 移植到 GameMaker 的清单 |
| [[sources/xor-mini-fractal-texturing]] | Xor：按深度离散缩放 UV 的一致细节技巧 |
| [[sources/alanzucconi-to-voronoi-beyond]] | Zucconi：Voronoi 图的距离度量、应用与 Unity shader 朴素实现 |
| [[sources/alanzucconi-main-colours-kmeans]] | Zucconi：用 K-Means + silhouette 从截图里自动提取主色 |
| [[sources/halisavakis-image-effects-custom-masks-i]] | Alisavakis：in-shader 圆盘 mask 的 5 行实现 |
| [[sources/halisavakis-image-effects-custom-masks-ii]] | Alisavakis：把圆盘 mask 改成圆环 mask 的推导 |
| [[sources/halisavakis-image-effects-shockwave]] | Alisavakis：圆环 mask × UV 位移 = 冲击波 |
| [[sources/halisavakis-image-effects-stencil-antichamber]] | Alisavakis：用 stencil buffer 做 Antichamber 风格的「窗口可见」物体 |
| [[sources/lindenreid-procedural-greeble]] | Linden Reid：n 边形 polygon 的 procedural greeble |
| [[sources/lindenreid-stylized-water-shader]] | Linden Reid：Unity 风格化水面 shader |
| [[sources/lindenreid-dissolve-shader]] | Linden Reid：Unity dissolve shader 与多层边缘色 |
| [[sources/lindenreid-cel-shader-outline]] | Linden Reid：Unity cel shader + stencil 描边 |
| [[sources/aras-syntonic-dentiforms-redux]] | Aras 把 2004 年自己的 demo 移植到 sokol_gfx 跨后端并砍掉 classitis 级的抽象 |
| [[sources/jasper-linux-graphics-stack]] | Jasper：Linux 图形栈两条路径 + Wayland 动因综述（2012） |
| [[sources/jasper-bytecode]] | Jasper：ACPI / 字体 / BPF——被藏起来的字节码解释器 |
| [[sources/jasper-barriers]] | Jasper：GNOME 3.8 压力式消息托盘背后的 XI 2.3 pointer barrier pressure |
| [[sources/jasper-xplain]] | Jasper：Xplain 交互式 X11 深度科普系列启动公告 |
| [[sources/etodd-component-binding-behind-the-scenes]] | Todd：Property/Binding/Command 的实现细节 |
| [[sources/etodd-tools-are-everything]] | Todd：工具优先于特性，内容管线决定游戏 |
| [[sources/etodd-csharp-runtime-compilation]] | Todd：C# 运行时编译 + AppDomain shadow copy 热重载 |
| [[sources/interplay-unity-postprocessing]] | Anagnostou：Unity 里的多步体积光束后处理实验（2015） |
| [[sources/interplay-unreal-frame-part1]] | Anagnostou：How Unreal Renders a Frame Part 1（粒子 / Z-prepass / occlusion / HZB / shadow） |
| [[sources/interplay-unreal-frame-part2]] | Anagnostou：How Unreal Renders a Frame Part 2（light grid / volumetric fog / g-prepass / AO / lighting） |
| [[sources/interplay-unreal-frame-part3]] | Anagnostou：How Unreal Renders a Frame Part 3（SSR / 大气 / 透明物 / 折射 / 后处理链） |
| [[sources/interplay-gpu-occlusion-culling]] | Anagnostou：DX11 GPU-based occlusion culling 实验 |
| [[sources/simonschreibt-teleglitch-viewcones]] | Simon：Teleglitch 视野阴影是径向外推的黑色几何 |
| [[sources/simonschreibt-cell-shading]] | Simon：3D shell extrude + 2D 8-direction sprite 描边 |
| [[sources/simonschreibt-deus-ex-folds]] | Simon：Deus Ex 奥运风旗是动画 parallax，不是顶点动画 |
| [[sources/simonschreibt-deus-ex-scanlines]] | Simon：Deus Ex 屏幕扫描线很可能是 mipmap 缺失下的 moiré |
| [[sources/simonschreibt-wow-balloon]] | Simon：WoW 热气球的中心辉光是 Lit Sphere / MatCap shader |
| [[sources/allenchou-matrix-stack-visitor]] | Allen Chou：用访问者模式持有矩阵栈遍历场景图 |
| [[sources/allenchou-shader-primer]] | Allen Chou：Molehill 时代的最小 VS/FS shader 入门 |
| [[sources/allenchou-switch-vs-strategy]] | Allen Chou：blend mode 重构示例（switch → Strategy） |
| [[sources/metalbyexample-linear-algebra]] | Warren Moore：Metal 视角的图形数学支线（Metal Z=[0,1] clip space 等约定）|
| [[sources/metalbyexample-up-and-running-3]] | Warren Moore：Metal 第 3 篇——带 Blinn-Phong 光照的 3D 茶壶 |
| [[sources/metalbyexample-feature-sets]] | Warren Moore：A7/A8 GPU 家族能力差异与 MTLFeatureSet 查询 |
| [[sources/metalbyexample-textures-and-samplers]] | Warren Moore：Metal 纹理与采样器、constexpr sampler 与坐标系翻转 |
| [[sources/metalbyexample-image-processing]] | Warren Moore：Metal compute kernel 做图像滤镜链（saturation + Gaussian blur）|
| [[sources/slater-neural-graphics-primitives]] | Slater：神经图形原语——激活函数谱系 + 位置编码 + Instant NGP 哈希 |
| [[sources/slater-optimizing-open-addressing]] | Slater：开放寻址哈希表 benchmark —— Robin Hood + backshift 胜出 |
| [[sources/slater-spherical-integration]] | Slater：球面积分里 $\sin\theta$ 的直观 + 形式推导 |
| [[sources/slater-oxidizing-cpp]] | Slater：rpp —— Rust 灵感的 C++20 STL 替代与 region 分配器 |
| [[sources/slater-continuous-probability]] | Slater：Monte Carlo 速成 Part 1 — 连续概率基础 |
| [[sources/raphlinus-undefined-behavior]] | Raph Levien：C/C++ 未定义行为的历史、虚拟机模型与治理 |
| [[sources/raphlinus-favorite-sigmoids]] | Raph Levien：数字合成器里的 sigmoid 比较与多项式变形近似 |
| [[sources/bartwronski-hair-rendering-tricks]] | Wronski：Witcher 3 / Cyberpunk 原型期的头发 alpha-test 四 pass 混合管线 + Witcher 2 SSS hack |
| [[sources/bartwronski-csharprenderer-volumetric-fog]] | Wronski：CSharpRenderer 框架更新，附 Siggraph 2014 froxel 体积雾 compute shader demo 代码 |
| [[sources/elopezr-clos2-rendering]] | López Ros：Castlevania LoS2 的 DX9 延迟管线逐 pass 拆解 |
| [[sources/interplay-deferred-sdf-rendering]] | Anagnostou：deferred SDF rendering |
| [[sources/interplay-multidraw-indirect-occlusion]] | Anagnostou：GPU-based occlusion culling Part 2 (MultiDraw + LOD) |
| [[sources/interplay-bgfx-gpu-driven-port]] | Anagnostou：把 GPU-driven 剔除移植到 bgfx |
| [[sources/interplay-digital-dragons-gpu-driven]] | Anagnostou：Digital Dragons 大会版 20K 规模化 profiling |
| [[sources/interplay-hybrid-raytraced-shadows-reflections]] | Anagnostou：compute shader 手写 hybrid raytracer 的硬阴影与反射 |
| [[sources/danielilett-cel-shading-part-0]] | Ilett：Phong 光照家族的四分量理论铺垫 |
| [[sources/danielilett-cel-shading-part-2]] | Ilett：自定义 Lighting 函数 + fwidth/smoothstep 做 diffuse 硬阶与 specular |
| [[sources/danielilett-cel-shading-part-3]] | Ilett：bump map 与 Fresnel rim 光的最小改动接入 |
| [[sources/danielilett-cel-shading-part-4]] | Ilett：沿法线外推 + stencil buffer 的双 pass 描边 |
| [[sources/danielilett-cel-shading-part-5]] | Ilett：Stencil ID 化 + lighting ramp 纹理替换硬阶 |
| [[sources/halisavakis-dissolve-shader]] | Alisavakis：Unity surface shader 版 dissolve，Cull Off + addshadow 坑点 |
| [[sources/halisavakis-random-stripes-mask]] | Alisavakis：一维 hash + step 生成随机条纹 mask 的最小范例 |
| [[sources/halisavakis-glitch-image-effect]] | Alisavakis：条纹 + 波浪 + 色差三件套 glitch + 单旋钮控制器 |
| [[sources/halisavakis-abzu-portal-cards]] | Alisavakis：复刻 ABZÛ 按距离 fade 的 portal card 透明贴片 |
| [[sources/halisavakis-shader-bits-world-screen-pos]] | Alisavakis：Unity shader worldPos / screenPos 的四种写法备忘 |
| [[sources/alanzucconi-shader-intro-unity]] | Zucconi 2015：Unity Built-in RP 下的 Shader 入门骨架（ShaderLab + Cg/HLSL，Surface vs Vertex/Fragment 取舍） |
| [[sources/ryg-planar-rotations-and-dct]] | ryg：DCT 平面旋转四种实现与 FMA 时代的重新定位 |
| [[sources/ryg-more-ppc-compiler-babysitting]] | ryg：Xbox 360 PPC 上 int→float 的 LHS 与编译器盲区 |
| [[sources/ryg-negative-space-in-programming]] | ryg：程序真正的形状是留白决定的 |
| [[sources/ryg-ring-buffers-and-queues]] | ryg：SPSC FIFO 的两种语义与虚拟流的胜利 |
| [[sources/ryg-texture-tiling-and-swizzling]] | ryg：嵌套分块 swizzle 与减-与地址增量 |
| [[sources/lindenreid-animated-dotted-outline]] | Linden Reid：动画虚线描边——sin 距离场 + 时间相位 |
| [[sources/lindenreid-ice-shader-unity]] | Linden Reid：冰晶 shader = Fresnel + lazy normal + GrabPass 扭曲 |
| [[sources/lindenreid-waving-grass-shader]] | Linden Reid：世界空间风场纹理驱动的草叶顶点动画 |
| [[sources/vertexfragment-demystifying-windows-bitmaps]] | Sell：Windows 位图族对象一次理清 |
| [[sources/vertexfragment-surface-angle-silhouette]] | Sell：Unity 后处理 v2 下的表面角剪影 |
| [[sources/vertexfragment-sobel-outline-unity]] | Sell：Unity 后处理下的深度+法线双 Sobel 描边 |
| [[sources/vertexfragment-demonizing-nested-loops]] | Sell：嵌套循环性能迷思的基准反驳 |
| [[sources/xor-mini-interpolation]] | Xor：nearest/linear/cubic 纹理滤波的 GLSL 手写实现 |
| [[sources/xor-mini-noise]] | Xor：hash / value noise / Perlin noise 的手写三步骨架 |
| [[sources/xor-mini-noise-2]] | Xor：Worley / Voronoi / fractal noise 的手写实现与 fBm octave 模板 |
| [[sources/xor-mini-environments]] | Xor：等距柱状 HDRI 纹理做 skybox 与反射（GameMaker 无 cubemap 替代方案） |
| [[sources/xor-mini-hlsl]] | Xor：GLSL ES → HLSL 语法速查（struct+semantic、函数改名、纹理/采样器分离） |
| [[sources/gameknife-gkengine-rendering-optimization]] | gameknife 2013：gkEngine 渲染优化三轮复盘，104→241 FPS |
| [[sources/gameknife-custom-vc100-toolchain]] | gameknife 2015：从 VS2013 剥离出 50 MB 独立 vc100 工具链 |
| [[sources/gametorrahod-ios-app-thinning]] | Sirawat Pitaksarit：Apple App Thinning 三件套速览（Unity 视角） |
| [[sources/cloudwu-go-first-impressions]] | 云风：Go 语言初步与 240 行重写连接网关 |
| [[sources/cloudwu-mmo-io-snapshot-diff]] | 云风：梦幻西游服务器快照差分持久化优化 |
| [[sources/cloudwu-zeromq-patterns]] | 云风：ZeroMQ Guide 读书笔记与游戏服务器架构建议 |
| [[sources/cloudwu-lua-incremental-gc]] | 云风：Lua 5.1 增量式 GC 源码剖析（双白色乒乓） |
| [[sources/danielilett-godot-visual-shaders]] | Daniel Ilett 2024：Godot VisualShader 初体验，Dissolve/Hologram/Hull Outline 三例对比 Unity Shader Graph |
| [[sources/danielilett-shader-graph-lighting-basics]] | Daniel Ilett 2024：Unity Shader Graph Basics Part 6，Lit 图完整输出栈逐槽讲解 |
| [[sources/danielilett-mgs-stealth-camo]] | Daniel Ilett 2024：Shader Graph 复刻 MGS Stealth Camo，Scene Color + 噪声 UV 偏移 |
| [[sources/danielilett-pokemon-terastallize]] | Daniel Ilett 2024：Shader Graph 复刻 Pokémon 太晶化，DDX/DDY flat normal + 贴图烘 Triangle ID |
| [[sources/xor-mini-mrt]] | Xor：GameMaker 下的 Multiple Render Targets，延迟渲染与 Object ID outline |
| [[sources/xor-mini-noise-3]] | Xor：Simplex noise、函数 vs 纹理的取舍、tileable noise |
| [[sources/xor-mini-mipmaps]] | Xor：mipmap 的生成、LOD 选择原理，以及把 bias 参数当廉价 blur 用 |
| [[sources/xor-mini-webgpu]] | Xor：WebGPU 与 WGSL 的 GM 视角入门 |
| [[sources/xor-mini-blur-philosophy]] | Xor：box → Gaussian → kernel → separable 的 blur 演进与 dos/avoids 清单 |
| [[sources/cloudwu-ant-engine-open-source]] | 云风：Ant Engine 开源宣言及自研引擎论证 |
| [[sources/cloudwu-vfs-new-ideas]] | 云风：对 VFS "不变快照" 假设的反思 |
| [[sources/cloudwu-ltask-rewrite]] | 云风：ltask 调度器重构，删掉独占线程服务 |
| [[sources/cloudwu-ant-engine-mobile-optimization]] | 云风：移动端能耗优化与魔兽式场景剔除设想 |
| [[sources/playcanvas-webgpu-editor]] | Eastcott：PlayCanvas Editor 正式支持 WebGPU 的工程公告 |
| [[sources/playcanvas-supersplat-pwa]] | Eastcott：SuperSplat 0.17.1 的 2× 加速与 PWA 化 |
| [[sources/playcanvas-editor-gaussian-splat]] | Eastcott：PlayCanvas Editor 原生集成 3D Gaussian Splat |
| [[sources/interplay-workgraphs-intro]] | Kostas：work graph 入门 + shadow 三级分类实例 |
| [[sources/interplay-workgraphs-performance]] | Kostas：work graph vs compute+indirect 在 SSSR 上慢 3× |
| [[sources/interplay-hidden-shader-cost]] | Kostas：shader 指令 ISA 级别隐藏成本分类 |
| [[sources/interplay-meshlets-mesh-shaders]] | Kostas：mesh shader + AS hi-z 遮挡剔除，St Miguel gbuffer −44% |
| [[sources/interplay-async-compute]] | Kostas：async compute 的 pairing 方法论与 pass 重排收益 |
| [[sources/anteru-data-formats-csv-json]] | Anteru：CSV/JSON 的失败模式与 Parquet 的生态位 |
| [[sources/simonschreibt-anno-1800-shadows]] | Simon：Anno 1800 把太阳锁相机而非世界的构图学 |
| [[sources/simonschreibt-cyberpunk-broken-edges]] | Simon：Cyberpunk 2077 用 POM decal 在盒子墙装出凿痕 |
| [[sources/ryg-insert-zero-bit-middle]] | ryg：一条加法指令就能在值的中间插入一个 0 bit |
| [[sources/ryg-zero-or-sign-extend]] | ryg：用补码定义重新推导不分支的有符号/零扩展 |
| [[sources/ryg-oodle-kraken-misconceptions]] | ryg：澄清 Oodle 三条产品线与 PS5 游戏缩水的真实原因 |
| [[sources/danielilett-shader-graph-custom-lighting]] | Ilett：Shader Graph Basics Part 7，Fresnel + HDR + Bloom 边缘高光 |
| [[sources/danielilett-shader-graph-intersections-1]] | Ilett：Part 8，DepthIntersection 子图的三重用法 |
| [[sources/danielilett-shader-graph-intersections-2]] | Ilett：Part 9，水面泡沫 / 护盾 / 光柱的深度交界美术 |
| [[sources/danielilett-shader-graph-custom-functions]] | Ilett：Part 10，用 HLSL 做 URP Additional Lights 循环 |
| [[sources/danielilett-mystery-dungeon-sketches]] | Ilett：URP post-process 四件套复刻 Mystery Dungeon 素描风 |
| [[sources/cloudwu-ecs-particle-system-c]] | 云风：ECS 粒子系统的 C/C++ 对比与自我怀疑 |
| [[sources/cloudwu-worker-task-pathfinding]] | 云风：工人任务分配系统与寻路需求重审 |
| [[sources/cloudwu-id-lifetime-kill-flag]] | 云风：用 id + 销毁标记替代引用计数的生命期管理 |
| [[sources/cloudwu-gameplay-architecture]] | 云风：gameplay 上层三层 + Object/Actor 架构笔记 |
| [[sources/xor-mini-blur-philosophy-2]] | Xor：Blur Philosophy 2 —— 双线性采样压缩高斯样本数 |
| [[sources/xor-mini-vertex-shaders]] | Xor：Vertex Shader 基础与 2D 游戏的被低估用法 |
| [[sources/oakleaff-volume-shadows]] | Oakleaff：GM 上体积雾 + 级联阴影的屏幕空间 raymarch |
| [[sources/yaazarai-radiance-cascades]] | Yaazarai：Radiance Cascades Part 1 几何直觉 |
| [[sources/yaazarai-radiance-cascades-2]] | Yaazarai：Radiance Cascades Part 2 优化、代码、朴素采样对比 |
| [[sources/danielilett-zelda-recall-rune]] | Ilett：URP 复刻《王国之泪》Recall 时之逆转（mask RT + 噪声擦除 + 边缘检测） |
| [[sources/danielilett-shader-graph-terrains]] | Ilett：Shader Graph Part 11，手工复刻 Terrain splatmap + 自动岩石 + 世界扫描 |
| [[sources/danielilett-holofoil-cards]] | Ilett：URP 宝可梦 holo 闪卡（stencil 分层 parallax + 视角彩虹 + Height→Normal） |
| [[sources/danielilett-shader-graph-post-processing]] | Ilett：Shader Graph Part 12，Fullscreen Graph 做灰度与颜色+法线 outline |
| [[sources/danielilett-shader-code-textures-uvs]] | Ilett：Shader Code 02，`TEXTURE2D`/`SAMPLER`/`_ST`/`TRANSFORM_TEX` + SRP Batcher CBUFFER |
| [[sources/cloudwu-ant-engine-improvement-plan]] | 云风：独立开发三个月后的 Ant 引擎改进计划 |
| [[sources/cloudwu-game-reviews-determinism]] | 云风：最近玩的游戏与确定性规则 vs 智能 AI |
| [[sources/cloudwu-factorio-space-age]] | 云风：异星工厂 2.0 太空时代 300 小时通关复盘 |
| [[sources/xor-mini-voxels-2]] | Xor：GameMaker 中用 2D LUT 纹理存储可编辑体素地图 |
| [[sources/xor-mini-vis-dev]] | Xor：程序员美术的视觉打磨清单 |
| [[sources/xor-mini-anti-aliasing]] | Xor：shader 解析抗锯齿三级——SDF、fwidth、手动导数 |
| [[sources/xor-mini-gamma]] | Xor：shader 里 sRGB / linear 的正确编解码姿势 |
| [[sources/xor-mini-sdf]] | Xor：Signed Distance Field 的用途与修改操作大全 |
| [[sources/danielilett-blur-shaders-pro-scripting]] | Ilett：URP/HDRP/Built-in 三管线通过 Volume API 脚本化访问后处理效果 |
| [[sources/danielilett-hologram-godot-dot-matrix]] | Ilett：Godot 全息 Dot Matrix 变体——屏幕空间点阵覆盖 |
| [[sources/danielilett-hologram-godot-glitch]] | Ilett：Godot 全息 Glitch 变体——顶点抖动 + 水平切片位移 + fresnel |
| [[sources/danielilett-hologram-godot-gradient]] | Ilett：Godot 全息 Gradient 变体——上下双色渐变 + 可选 Unscaled Time |
| [[sources/danielilett-hologram-godot-grid]] | Ilett：Godot 全息 Grid 变体——世界空间三轴网格线 + 可滚动 |
| [[sources/cloudwu-state-sync-broadcast-optimization]] | 云风：Agent 状态同步的广播优化 |
| [[sources/cloudwu-soluna-2d-pipeline]] | 云风：Soluna 2D 渲染管线优化 |
| [[sources/cloudwu-game-engine-memory]] | 云风读《游戏引擎架构》笔记：Console 内存约束下的栈式 / 双端 / 帧分配器与网易内部内存管理器比赛 |
| [[sources/simonschreibt-nikki-one-way-window]] | Simon：Infinity Nikki 单向窗户与相机外 NPC 动画剔除 |
| [[sources/simonschreibt-nikki-shadow]] | Simon：Infinity Nikki 三套阴影系统——shadow map、blob、AO decal 的合奏 |
| [[sources/etodd-waiting-on-tests]] | Evan Todd：CI ASG 冷启动调优 |
| [[sources/etodd-identity-problem]] | Evan Todd：命名即 identity 分区 |
| [[sources/etodd-zero-to-100k-tests]] | Evan Todd：100k 测试之后回看什么是好测试 |
| [[sources/xor-mini-turbulence]] | Xor：叠加旋转正弦波做湍流 |
| [[sources/xor-mini-reading-math]] | Xor：读数学论文的记号字典 |
| [[sources/xor-mini-combining-shaders]] | Xor：合并 shader 的 checklist 与嵌套顺序 |
| [[sources/xor-mini-common-mistakes]] | Xor：shader 常见 bug 清单 |
| [[sources/xor-mini-design-choices]] | Xor：shader art 5 维设计自查 |
| [[sources/danielilett-hologram-godot-noise]] | Ilett Godot 全息 Noise 变体：胶片颗粒噪点层 |
| [[sources/danielilett-hologram-godot-scanline]] | Ilett Godot 全息 Scanline 变体：屏幕/世界空间扫描线 alpha 调制 |
| [[sources/danielilett-hologram-godot-uber]] | Ilett Godot 全息 Uber 变体：三合一 shader + unscaled time |
| [[sources/danielilett-hologram-pro-basic]] | Ilett Hologram Shaders Pro Basic（URP/HDRP 移植） |
| [[sources/danielilett-hologram-pro-dot-matrix-glitch]] | Ilett Hologram Pro Dot Matrix + Glitch：动态分辨率补偿 |
| [[sources/cloudwu-lua-class-pattern]] | 云风：Lua 类型定义与容器元数据藏匿技巧 |
| [[sources/cloudwu-xlsx-version-control]] | 云风：xlsx 文本化以适配 git 工作流 |
| [[sources/cloudwu-mysql-gbk-utf8-migration]] | 云风：跨十年 MySQL 升级的 GBK → UTF-8 迁移复盘 |
| [[sources/danielilett-hologram-pro-dot-matrix]] | Ilett：Hologram Shaders Pro 点阵变体参数手册（Unity） |
| [[sources/danielilett-hologram-pro-glitch]] | Ilett：Hologram Shaders Pro 纯故障变体参数手册（Unity） |
| [[sources/danielilett-hologram-pro-gradient]] | Ilett：Hologram Shaders Pro 渐变变体参数手册（Unity） |
| [[sources/danielilett-hologram-pro-grid]] | Ilett：Hologram Shaders Pro 世界空间网格变体参数手册（Unity） |
| [[sources/danielilett-hologram-pro-grid-glitch]] | Ilett：Hologram Shaders Pro 网格 + 故障组合变体参数手册（Unity） |
| [[sources/playcanvas-engine-2-release]] | Eastcott：PlayCanvas Engine 2.0.0 发布公告 |
| [[sources/playcanvas-react-declarative-3d]] | Lundin：Declarative 3D with React 公告 |
| [[sources/playcanvas-supersplat-2-0-publish]] | Eastcott：SuperSplat 2.0 发布 + Timeline + .ssproj |
| [[sources/playcanvas-supersplat-2-2-video]] | Eastcott：SuperSplat 2.2 视频渲染 + embed + 社区 |
| [[sources/playcanvas-supersplat-viewer-oss]] | Eastcott：SuperSplat Viewer 转 MIT 开源 |
| [[sources/jendrikillner-recommended-books]] | Illner：图形程序员推荐书单（GPU Zen 3/RTR/PBR/FGED/GEA 等） |
| [[sources/danielilett-hologram-pro-noise]] | Unity Hologram Pro：Noise 变体（时间×空间×强度×色彩四参数） |
| [[sources/danielilett-hologram-pro-scanline]] | Unity Hologram Pro：Scanline 变体（贴图调制 alpha，Screen/World 两态） |
| [[sources/danielilett-hologram-pro-uber]] | Unity Hologram Pro：Uber 变体（Scanline+Glitch+Noise 合一） |
| [[sources/danielilett-retro-godot-crt-mesh]] | Godot Retro Pro：CRT Mesh 变体 |
| [[sources/danielilett-retro-godot-crt-post-process]] | Godot Retro Pro：CRT 全屏后处理 + YIQ 磁带色损 |
| [[sources/cloudwu-deepfuture-postmortem]] | 云风：Deep Future 桌游数字化 7 周独立开发复盘 |
| [[sources/cloudwu-eu5-economy]] | 云风：EU5 经济系统（人口/货币/商品/市场/贸易） |
| [[sources/cloudwu-eu5-gameplay-notes]] | 云风：EU5 游玩笔记（开荒/食物/税基） |
| [[sources/cloudwu-main-thread-task-injection]] | 云风：主线程事件循环与 ltask 调度器的融合 |
| [[sources/cloudwu-deckbuilder-games]] | 云风：最近玩的几款卡牌构筑类电子游戏 |
| [[sources/cloudwu-skynet-lua-55]] | 云风：Skynet 升级到 Lua 5.5.0 |
| [[sources/danielilett-retro-godot-retro-lit]] | Ilett：Godot 版 Retro Lit 参数手册，PSX look 最小可用集 |
| [[sources/danielilett-retro-urp-retro-lit]] | Ilett：URP 通用 Retro Lit，含 Surface Options + flat shading + specular/cubemap |
| [[sources/danielilett-retro-urp-crt-mesh]] | Ilett：URP CRT 贴 mesh 变体（CCTV 屏），Tracking Texture RG 双通道编码 |
| [[sources/danielilett-retro-urp-crt-post-process]] | Ilett：URP 全屏 CRT，独有 Interlaced Rendering + Custom RGB Sliders + Render Pass Event |
| [[sources/cloudwu-ai-game-design-chat]] | 云风：和 AI 聊游戏设计 |
| [[sources/cloudwu-solo-boardgames]] | 云风：介绍几款单人桌游（Spirit Island / Voidfall / Friday） |
| [[sources/cloudwu-ai-reading-workflow]] | 云风：用 AI 辅助读英文小说 |
| [[sources/anteru-sraa]] | Chajdas：SRAA I3D 2011 论文页 |
| [[sources/anteru-tiled-light-trees]] | O'Donnell/Chajdas：tiled light trees I3D 2017 论文页 |
| [[sources/anteru-workgraph-spmv]] | Chajdas 等：work graph SpMV ISCA 2025 |
| [[sources/anteru-hybrid-sample-surface]] | Reichl/Chajdas：hybrid 光栅+ray-cast 大 mesh 渲染 VMV 2012 |
| [[sources/anteru-giga-particle-fluid]] | Reichl/Chajdas：亿级粒子流体交互渲染 HPG 2014 |
| [[sources/danielilett-retro-urp-retro-skybox]] | Ilett：Retro Skybox 参数手册，PSX 风天空盒 + 程序云 |
| [[sources/danielilett-retro-urp-retro-vertex-lit]] | Ilett：Retro Vertex Lit 兼容页（v1.5 合并入 Retro Lit） |
| [[sources/danielilett-toolbox-urp-base-lit]] | Ilett：Shader Toolbox Base Lit，URP default Lit 的 clone 作为 pack 基线 |
| [[sources/danielilett-toolbox-urp-bubble]] | Ilett：Bubble shader，Fresnel + color ramp + iridescent noise flow + camera texture |
| [[sources/danielilett-toolbox-urp-dissolve]] | Ilett：Dissolve shader，Plane/Point origin + 附带 DissolvePlane.cs |
| [[sources/danielilett-toolbox-urp-glass]] | Ilett：Glass shader，refractive index + Fresnel + camera opaque/transparent 双源 |
| [[sources/danielilett-toolbox-urp-glitter]] | Ilett：Glitter shader，Voronoi cell 粒子 + Fresnel 门控 + 双色随机 |
| [[sources/danielilett-toolbox-urp-mesh-explosion]] | Ilett：Mesh Explosion shader，三种 expansion mode + BakeFaceColors.cs |
| [[sources/danielilett-toolbox-urp-stochastic-lit]] | Ilett：Stochastic Lit shader，三次随机偏移采样打散 tiling |
| [[sources/playcanvas-sogs-20x-compression]] | Eastcott：PlayCanvas Engine 2.7.5 引入 SOGS，~20× 压缩（属性图 + PLAS + WebP） |
| [[sources/playcanvas-esm-scripts]] | Lundin：PlayCanvas ESM Scripts 发布，`.mjs` + class + import maps |
| [[sources/playcanvas-splat-transform-cli]] | Eastcott：SplatTransform 开源——3DGS 格式转换/变换/过滤/合并/CSV 导出的 CLI |
| [[sources/playcanvas-editor-frontend-oss]] | Bamrah：PlayCanvas Editor Frontend 开源，含 Observer/PCUI/PCUI-Graph/Editor API |
| [[sources/playcanvas-reflct-spotlight]] | Eastcott：Reflct 电商 3DGS viewer 的 three.js → PlayCanvas 迁移（帧率 2×、内存 -80%） |
| [[sources/playcanvas-sog-opensource]] | Eastcott：SOG 正式开源——Morton order + 单文件 `.sog` + WebGPU 压缩端 |
| [[sources/playcanvas-vscode-extension]] | Bamrah：新版 VSCode Extension，Disk-mapped FS + TS 类型 + AI-agent 友好 |
| [[sources/playcanvas-voxelo-spotlight]] | Eastcott：Voxelo UG3D——短视频 → AI 重建 → 3DGS 数字孪生的电商 pipeline |
| [[sources/playcanvas-supersplat-studio]] | Eastcott：SuperSplat Studio 发布——annotations + post effects + tonemapping |
| [[sources/playcanvas-supersplat-walk-lod]] | Eastcott：SuperSplat Walk Mode（voxel collision）+ Streamed LOD（SOG 切片）+ Easy Upload |
| [[sources/danielilett-toolbox-urp-subgraph-library]] | Ilett：Shader Toolbox URP subgraph 节点库（Better Voronoi / Apply Normal Map 等） |
| [[sources/danielilett-toolbox-urp-voronoi-lava]] | Ilett：Voronoi Lava 双层 PBR shader 参数手册 |
| [[sources/danielilett-snapshot2-glitch]] | Ilett：Snapshot 2 Glitch——Offset Texture / Slice Band / Block Artifact 三段 |
| [[sources/danielilett-snapshot2-masking-layers]] | Ilett：Snapshot 2 Masking Layers——Local vs Global mask 机制 |
| [[sources/danielilett-snapshot2-outline]] | Ilett：Snapshot 2 Outline——屏幕空间 DepthNormalsColor 三通道描边 |
| [[sources/danielilett-snapshot2-underwater]] | Ilett：Snapshot 2 Underwater——flow map + triplanar/light-aligned caustics |
| [[sources/danielilett-snapshot-pro-scripting]] | Ilett：Snapshot Pro Scripting Guide——URP / HDRP / Built-in Volume 三管线 API |
| [[sources/ryg-why-those-particular-integer-multiplies]] | ryg：x86 SIMD 整数乘法的硬件演化推测 |
| [[sources/ryg-bc7-optimal-solid-color-blocks]] | ryg：BC7 纯色块两行公式的最优端点 |
| [[sources/ryg-mrsse]] | ryg：Oodle BC6H 的相对均方误差度量 |
| [[sources/ryg-unorm-snorm-hardware-edition]] | ryg：UNORM / SNORM → float 的硬件级实现 |
| [[sources/ryg-oodle-2-9-14-intel-13th-14th-gen]] | ryg：Oodle 2.9.14 对 Intel 13/14 代 CPU 时钟 bug 的 work-around |
| [[sources/xor-functions-tanh]] | Xor：tanh 在 shader 里的数学和用法 |
| [[sources/xor-modeling-the-world-in-280-chars]] | Xor：280 字符 tweet shader 的动机与入门 |
| [[sources/xor-decoding-phosphor]] | Xor：258 字符 Phosphor tweet shader 的逐行拆解 |
| [[sources/xor-volumetric-raymarching]] | Xor：体积 raymarch 的密度场与样本累积 |
| [[sources/xor-functions-mix]] | Xor：mix 函数的进阶用法（saturation / extrapolation / remap） |
| [[sources/xor-dot-noise]] | Xor：gyroid + 黄金角旋转的廉价 aperiodic 3D 噪声 |
| [[sources/xor-fragcoord-editor]] | Xor：FragCoord.xyz shader 编辑器发布 |
| [[sources/peters-path-tracing-workshop]] | Peters：Intel path tracing workshop（GLSL / ShaderToy） |
| [[sources/peters-path-tracing-lectures]] | Peters：TU Delft 硕士 path tracing 讲座 + Vulkan 实现 |
| [[sources/peters-radiometry-1-backwards]] | Peters：从 radiance 起步的辐射度量积分式重构 |
| [[sources/peters-radiometry-2-photometry]] | Peters：光谱量、CIE XYZ 与 photometric 单位 |
| [[sources/peters-spectral-rendering-3-vs-rgb]] | Peters：RGB vs 光谱渲染在多种光源下的实证对比 |
| [[sources/danielilett-toon-shaders-pro-toon]] | Ilett：Toon Shaders Pro 核心 HLSL shader 参数手册 |
| [[sources/danielilett-toon-shaders-pro-toon-graph]] | Ilett：Toon Shader Graph 变体，`CalculateToonLighting` subgraph |
| [[sources/danielilett-toon-shaders-pro-terrain]] | Ilett：Toon Terrain，splatmap + stochastic texturing |
| [[sources/danielilett-toon-shaders-pro-outline-post]] | Ilett：Toon Outline Post Process，六种描边算法 |
| [[sources/danielilett-retro-shaders-pro-breakdown]] | Ilett：Retro Shaders Pro 作者自述，PSX/N64/VHS/CRT 全套实现细节 |
| [[sources/danielilett-shader-code-transparency]] | Ilett：Shader Code Basics 03 — alpha blend / alpha clip / Blend 命令 |
| [[sources/danielilett-shader-code-depth-buffer]] | Ilett：Shader Code Basics 04 — depth buffer / silhouette / prepass / Render Objects |
| [[sources/danielilett-shader-code-vertex-tessellation]] | Ilett：Shader Code Basics 05 — vertex displacement + hull/domain tessellation |
| [[sources/cloudwu-star-trek-captains-chair]] | 云风：ST:CC 桌游卡牌构筑机制拆解 + 两次 Gemini 规则幻觉实录 |
| [[sources/cloudwu-soluna-extlua-proxy]] | 云风：soluna 用 `lua_getextraspace` + 临时 VM 做 Lua C API 代理 |
| [[sources/interplay-gpu-utilisation-holistic]] | Kostas：跨 pass 瓶颈配对和 async compute 搭配方法论 |
| [[sources/interplay-vertex-shader-exports]] | Kostas：N 卡 VS export 瓶颈的 3080 mobile 受控实验 |
| [[sources/interplay-spatial-hash-rtao]] | Kostas：spatial hashing 做 RTAO 缓存的完整实现 + 自适应 cell + age eviction |
| [[sources/interplay-neural-rendering-1-mlp]] | Kostas：小 MLP 在渲染信号上的 compute shader 实测 |
| [[sources/interplay-neural-rendering-2-coopvec]] | Kostas：Cooperative Vectors preview 把 MLP 推到 Tensor core 的 173× 加速 |
| [[sources/metalbyexample-decade-early-years]] | Warren Moore：Metal 2014–2019 演进回顾 |
| [[sources/metalbyexample-decade-modern-era]] | Warren Moore：Metal 2020–2024 演进回顾（核心 raytracing / MetalFX / Vision Pro / residency set） |
| [[sources/metalbyexample-hdr-video]] | Warren Moore：AVFoundation + Metal HDR 视频完整管线教程 |
| [[sources/metalbyexample-metal-4-basics]] | Warren Moore：Metal 4 API 迁移入门 |
| [[sources/metalbyexample-slug]] | Warren Moore：Slug 算法在 Metal 上的最小实现 |
| [[sources/karis-nanite-tessellation-intro]] | Karis：Nanite Tessellation 系列开篇，为什么位移值得做 amplification |
| [[sources/karis-possible-approaches-tessellation]] | Karis：逐一否决 tracing 与 Nanite 簇内放大，滑向 Reyes |
| [[sources/karis-how-to-tessellate]] | Karis：Tessellation Table 离线预计算 + 16bit barycentric 量化，密度均匀 remesh |
| [[sources/karis-nanite-reyes]] | Karis：UE5.4 完整流水线——ClusterRasterize 扩展 / PatchSplit global shader / PatchRasterize 软光栅 + DS 导数链式法则 |
| [[sources/karis-variable-sized-work]] | Karis：wave 内 pull-based 变长工作分发原语，顺便解释 Nanite 软光栅快于 HW 的数据移动论 |
| [[sources/ciechanow-airfoil]] | Ciechanowski：翼型升力与流体可视化 |
| [[sources/ciechanow-moon]] | Ciechanowski：月球、Kepler、潮汐与食 |
| [[sources/alanzucconi-minecraft-plugin]] | Zucconi：Minecraft Paper 插件开发完整教程 |
| [[sources/alanzucconi-pca-intro]] | Zucconi：PCA 程序员视角直觉入门 |
| [[sources/alanzucconi-orbital-mechanics]] | Zucconi：轨道力学长文（Kepler + n-body） |
| [[sources/apoorvaj-shader-graph-contract]] | Joshi：shader graph 的 sink contract 与 Substrate slab |
| [[sources/apoorvaj-coordinate-spaces]] | Joshi：渲染管线坐标空间链速写 |
| [[sources/apoorvaj-static-site-antiframework]] | Joshi：停止过度工程化静态网站 |
| [[sources/apoorvaj-vibe-coding]] | Joshi：Claude Code 两晚做丹麦税计算器 |
| [[sources/elopezr-graphics-programmer-life]] | López-Ros：图形程序员的生与死——行业痛点 opinion piece |
| [[sources/elopezr-art-of-packing-data]] | López-Ros：HLSL/RDNA 视角的 GPU 数据打包手册 |
| [[sources/halisavakis-haze-manual]] | Alisavakis：HAZE URP 体积雾 renderer feature 用户手册 |
| [[sources/simonschreibt-high-heel-problem]] | Trümpler：角色高跟鞋引发的高度问题 |
| [[sources/simonschreibt-sims-4-mirrors]] | Trümpler：Sims 4 镜子的 stencil + culling 工艺 |
| [[sources/slater-mc-integration]] | Slater：Monte Carlo 积分与维度诅咒 |
| [[sources/slater-mc-sampling]] | Slater：PRNG、拒绝、逆变换采样 |
| [[sources/slater-mc-rendering]] | Slater：Monte Carlo 应用到渲染方程（path tracing） |
| [[sources/vertexfragment-polar-coordinates]] | Steven Sell：用极坐标做 BotW 式水圈纹理效果 |
| [[sources/vertexfragment-cloud-upsample]] | Steven Sell：quarter-res + jitter + 时间重投影 的体积云升采样 |
| [[sources/vertexfragment-urp-volumetric-fog]] | Steven Sell：URP 自定义 Pass 里的体积雾 raymarch 实现 |
| [[sources/vertexfragment-bts-v07]] | Steven Sell：Beyond the Storm v0.7 devlog（草地/雾/云改造 + scope 坍缩） |
| [[sources/gametorrahod-enableable-generated-code]] | Sirawat：DOTS Enableable 组件的 Roslyn 生成代码三条路径 |
| [[sources/gametorrahod-chunk-change-version]] | Sirawat：DOTS chunk change version 的六个反直觉陷阱 |
| [[sources/gametorrahod-thinking-in-cache]] | Sirawat：DOTS 的 cache 视角 + Burst 自动向量化拆解 |
| [[sources/gametorrahod-ecs-patterns]] | Sirawat：从 Unity 官方包里扒出的 9 个 ECS 编程模式 |
| [[sources/gametorrahod-audio-random-container]] | Sirawat：Unity 6 AudioResource / AudioRandomContainer 评估笔记 |
| [[sources/etodd-jujutsu]] | Evan Todd：该不该从 Git 迁到 Jujutsu 的决策框架 |
| [[sources/etodd-magic-link-pitfalls]] | Evan Todd：magic link 登录的两个非显然陷阱（GET 预取、错 tab） |
| [[sources/etodd-more-magic-link-pitfalls]] | Evan Todd：magic link 续篇（phishing、flaky email、rate limit） |
| [[sources/etodd-passkeys-are-too-hard]] | Evan Todd：WebAuthn / passkeys conditional UI 的服务端复杂度问题 |
| [[sources/frost-kiwi-video-game-blurs]] | Frost Kiwi：从 Box Blur 一路推到 Dual Kawase |
| [[sources/jasper-matrix-multiplication-guide]] | Jasper：图形 API 矩阵乘法与顺序一次讲透 |
| [[sources/pokladek-procedural-pool-balls]] | Pokladek：用 SDF 程序化生成台球贴图 |
| [[sources/gameknife-modern-rendering-how-modern]] | gameknife：从 OpenGL ES 老兵视角看现代渲染 |
| [[sources/raphlinus-good-parallel-computer]] | Raph Levien：想要一台好的并行计算机 |
| [[sources/runevision-hair-and-atmosphere]] | Johansen: Unity 发丝着色器三档实现 + 日本远山空气透视观察 |
| [[sources/runevision-phacelle-noise]] | Johansen: Phacelle Noise—比 Phasor Noise 便宜一个数量级的方向性噪声 |
| [[sources/runevision-erosion-filter]] | Johansen: Advanced Terrain Erosion Filter—单 pass GPU 过程化山地侵蚀 |
| [[sources/chipsandcheese-gb10-cpu-memory]] | Chester Lam：GB10 CPU 侧内存子系统实测（2025-12） |
| [[sources/chipsandcheese-gb10-gpu]] | Chester Lam：GB10 iGPU（consumer Blackwell）分析（2026-03） |
| [[sources/chipsandcheese-chipset-microbench]] | Chester Lam：主板 chipset 对 PCIe 延迟的影响（2026-03） |
| [[sources/chipsandcheese-ccc-april-fools]] | Chester Lam：LLM C 编译器与微架构救生圈（2026-04 愚人节） |
| [[sources/chipsandcheese-split-locks]] | Chester Lam：x86-64 split lock 跨 7 平台横测（2026-04） |
| [[sources/raytracey-lighthouse-2]] | Lapere：Lighthouse 2，Bikker 基于 OptiX 7 的开源实时路径追踪框架 |
| [[sources/raytracey-marbles-rtx-omniverse]] | Lapere：Marbles RTX 夜景与 Omniverse 上的 many-light 实时路径追踪 |
| [[sources/joostdevblog-where-to-get-original-ideas]] | Joost van Dongen：避开创意输入同质化（Proun 源自 Kandinsky） |
| [[sources/joostdevblog-robo-maestro-modelling-tricks]] | Joost van Dongen：Blender 硬表面建模 crease / bevel weight / harden normals |
| [[sources/joostdevblog-pitching-to-publishers]] | Joost van Dongen：17 年 pitch 经验，MeetToMatch、X-factor、bookkeeping |
| [[sources/bitsquid-rebuilding-entity-index]] | Stingray：Entity Index 的原型链式重构 |
| [[sources/bitsquid-reprojecting-reflections]] | Jp：SSR 在 TAA 下的几何重投影与多候选启发式 |
| [[sources/bitsquid-physically-based-lens-flare]] | Jp：基于 Hullin 论文的物理 lens flare 实现 |
| [[sources/bitsquid-validating-materials-lights]] | Jp：用 Arnold 验证 Stingray PBR material 与 light |
| [[sources/bitsquid-physical-cameras-stingray]] | Jp + Olivier Dionne：Stingray 物理相机（entity-based） |


| [[sources/alfredbaudisch-banjo-godot-terrain]] | Baudisch：在 Godot Visual Shader 里复刻 Banjo-Kazooie N64 vertex-color 地形并扩展到 runtime dirt paint |
| [[sources/gemserk-new-input-system-ld44]] | Gemserk：Ludum Dare 44 上同时用 legacy 与新 Input System 的复盘 |
| [[sources/gemserk-prefabs-as-data]] | Gemserk：Unity Prefab/GameObject 当纯数据容器用 |
| [[sources/gemserk-custom-editor-ecs]] | Gemserk：给 Unity ECS 世界写 CustomEditor 调试工具 |
| [[sources/gemserk-refactoring-prefab-data]] | Gemserk：Unity Prefab/Scene/Asset 的数据结构批量重构工具 |
| [[sources/supnik-stackless-vs-stackful-coroutines]] | Supnik：C++20 stackless 协程为何够用 |
| [[sources/supnik-coroutine-as-awaitable]] | Supnik：coroutine 本身就是 awaitable |
| [[sources/supnik-future-proof]] | Supnik：YAGNI 不是禁令，三问通过才可 future-proof |
| [[sources/supnik-beat-the-experts]] | Supnik：靠作弊写出比 malloc 更快的分配器 |
| [[sources/supnik-srgb-premultiplied-alpha]] | Supnik：sRGB、预乘 alpha 与块压缩的三角关系 |
| [[sources/4rknova-mulberry32]] | 4rknova：Mulberry32 确定性 PRNG 逐 bit 拆解 |
| [[sources/boristhebrave-poisson-rect-process]] | Boris The Brave：无限平面非重叠随机矩形算法 |
| [[sources/boristhebrave-infinite-grids]] | Boris The Brave：Sylves 无限网格程序化生成入口贴 |
| [[sources/boristhebrave-no-double-check]] | Boris The Brave：好软件不重复自检，agent 时代的新代码气味 |
| [[sources/schoener-i-miss-header-files]] | Schöner：从 Zig `pub` 回望 C header 的消费者价值 |
| [[sources/schoener-better-mono-codegen]] | Schöner：给 Unity Mono 加优化 pass 的商业化公告 |
| [[sources/schoener-mono-codegen-part-1]] | Schöner：Mono 如何把 `dot4` 变成 400 行汇编 |
| [[sources/schoener-mono-codegen-part-2]] | Schöner：LLVM vs 自写 pass、别名分析、DSE 方法论 |
| [[sources/schoener-zig-hot-reload-abi]] | Schöner：Zig 热重载/DLL 场景的 ABI 痛与三文件绕法 |
| [[sources/allar-ue4-firefighter]] | Allar：UE4 救火顾问的团队与工程教训 |
| [[sources/allar-marketplace-unknown-usernames]] | Allar：用 Fiddler 修 Epic Marketplace 评论用户名 bug |
| [[sources/allar-ue4-editor-battery-60fps]] | Allar：UE4 编辑器在电池 / UPS 下被钳到 60 FPS |
| [[sources/allar-umg-native-preconstruct-order]] | Allar：UMG NativePreConstruct 与蓝图 PreConstruct 触发顺序 |
| [[sources/allar-ue4-notification-offset]] | Allar：UE4 通知气泡位置硬编码在 NotificationManager.cpp |
| [[sources/tedsie-dynamic-split-screen]] | Ted Sie：动态分屏实现 |
| [[sources/tedsie-l-system-fractals]] | Ted Sie：L-system 分形图形学 |
| [[sources/tedsie-l-system-lightning-bolts]] | Ted Sie：L-system 闪电小故事 |
| [[sources/tedsie-crowd-simulation]] | Ted Sie：简易人群模拟系统 |
| [[sources/tedsie-dots-tween-system]] | Ted Sie：Unity DOTS tween 系统案例 |
| [[sources/outerra-srtm-30m-evaluation]] | Outerra：SRTM 30m 数据评估与 76/30 甜点 |
| [[sources/outerra-opengl-perf-grass]] | Outerra：procedural grass 的 OpenGL 三角形吞吐测试 |
| [[sources/outerra-opengl-perf-blocks]] | Outerra：building block 的 OpenGL 三角形吞吐测试 |
| [[sources/outerra-fp64-sincos]] | Outerra：GLSL fp64 sin/cos 的 minimax 近似实现 |
| [[sources/outerra-nasadem-comparison]] | Outerra：NasaDEM preliminary 对比 SRTM/Viewfinder |
| [[sources/sebaslab-ecs-abstraction-layers]] | Mandalà：ECS 抽象层与 assembly 级模块封装 |
| [[sources/sebaslab-svelto-filters-api]] | Mandalà：Svelto.ECS 3.3 Filters API 重写，persistent + transient 两档 |
| [[sources/sebaslab-survival-mini-example]] | Mandalà：Svelto.ECS Survival 示例重写，六层 asmdef + filter 取代 event |
| [[sources/sebaslab-svelto-on-dots-update]] | Mandalà：Svelto.ECS 3.4 的 DOTS 1.0 集成，废弃 ECB 改用 batched ops |
| [[sources/sebaslab-ecs-on-gpu-computesharp]] | Mandalà：用 ComputeSharp 把 Svelto ECS 的 component 存到 GPU compute buffer |
| [[sources/danielilett-snapshot-pro-underwater]] | Ilett：Snapshot Pro Underwater——bump + fog 简化版水下后处理 |
| [[sources/danielilett-snapshot-pro-vortex]] | Ilett：Snapshot Pro Vortex——Strength/Center/Offset 三参数极坐标漩涡 |
| [[sources/danielilett-snapshot-pro-world-scan]] | Ilett：Snapshot Pro World Scan——世界空间扫描条带 + ramp 纹理颜色过渡 |
| [[sources/tomlooman-rider-ue5-setup]] | Looman：Rider + UE5 C++ 开发环境搭建 |
| [[sources/tomlooman-project-orion]] | Looman：Project Orion 合作 Roguelike 示例项目总览 |
| [[sources/tomlooman-unreal-insights-counters]] | Looman：给 Unreal Insights 与 Stats System 加 Counters/Traces |
| [[sources/wolfgang-engel-hdr10-tv-setup]] | Engel 2017：LDR demo 上 HDR10 电视翻车 + 标准校准缺位 |
| [[sources/wolfgang-engel-triangle-visibility-buffer]] | Engel 2018：Triangle VB 全管线长文（The Forge 工程化） |
| [[sources/wolfgang-engel-dxr-api-debate]] | Engel 2018：为什么 RT 不该单独立 API |
| [[sources/wolfgang-engel-ray-tracing-without-api]] | Engel 2018：The Forge 跨平台 compute hybrid shadow 落地 |
| [[sources/wolfgang-engel-forge-history]] | Engel 2020：The Forge 历史 + GPU Zen 定位调整 + DXR 回望 |
| [[sources/boristhebrave-gol-cuda-triton]] | Boris The Brave：Game of Life 在 CUDA / Triton 上 120× 提速阶梯 |
| [[sources/boristhebrave-gol-multistep]] | Boris The Brave：shared memory 多步融合再把 GoL 提 2.7×，击穿 DRAM 带宽下限 |
| [[sources/boristhebrave-rhombus-tilings]] | Boris The Brave：无限随机菱形铺砖，三层错位 chunking 消除 Townscaper 边界痕 |
| [[sources/danielilett-snapshot-pro-sharpen]] | Ilett：Snapshot Shaders Pro - Sharpen unsharp mask 单参数 |
| [[sources/danielilett-snapshot-pro-silhouette]] | Ilett：Snapshot Shaders Pro - Silhouette 深度剪影 near/far 双色 |
| [[sources/danielilett-snapshot-pro-snes]] | Ilett：Snapshot Shaders Pro - SNES 每通道色阶量化 |
| [[sources/danielilett-snapshot-pro-synthwave]] | Ilett：Snapshot Shaders Pro - Synthwave 世界空间网格后处理 |
| [[sources/danielilett-snapshot-pro-text-adventure]] | Ilett：Snapshot Shaders Pro - Text Adventure ASCII 终端后处理 |
| [[sources/anki-spirv-parsing-rewriting]] | Charitos：手写 SPIR-V 解析与改写 |
| [[sources/anki-mesh-shader-vulkan-hlsl]] | Charitos：HLSL + Vulkan mesh shader per-primitive 坑 |
| [[sources/anki-gpu-driven-rendering-video]] | Charitos：AnKi GPU-driven 管线视频（占位，待观后回填） |
| [[sources/anki-simplified-pipeline-barriers]] | Charitos：pipeline barrier 的激进裁剪 |
| [[sources/anki-minimalist-ray-tracing]] | Charitos：仅用加速结构的 potato RT |
| [[sources/30fps-coordinate-system-table]] | Väänänen：3D 软件坐标系对照表 |
| [[sources/30fps-image-vq]] | Väänänen：图像向量量化 = 生成瓦片图 |
| [[sources/30fps-pca-colors]] | Väänänen：2D PCA 做 RGB 颜色压缩 |
| [[sources/30fps-som-palette]] | Väänänen：用自组织映射做调色板量化 |
| [[sources/30fps-mbd-images]] | Väänänen：Moving Basis Decomposition 在 2D 图像上的复现 |
| [[sources/30fps-split-tiles]] | Väänänen：NumPy 切瓦片的 reshape + transpose 高速写法 |
| [[sources/yiningkarlli-moana-2]] | Yining Karl Li：Moana 2 与 Hyperion 十年演进 |
| [[sources/yiningkarlli-texture-streaming-siggraph2025]] | Yining Karl Li：SIGGRAPH 2025 GPU Ptex 纹理流送 talk 配文 |
| [[sources/yiningkarlli-path-guiding-siggraph2025]] | Yining Karl Li：SIGGRAPH 2025 Hyperion 二代 path guiding course 配文 |
| [[sources/yiningkarlli-zootopia-2]] | Yining Karl Li：Zootopia 2 水管嵌套介质 + 二代 path guiding 首次大规模部署 |
| [[sources/16bpp-greedy-vs-analytical]] | 16BPP：拒绝采样 vs 解析采样，开 O1 后拒绝胜 |
| [[sources/16bpp-free-functions-hypothesis]] | 16BPP：重测 Klaus 2017「free function 更快」主张 |
| [[sources/16bpp-quicker-trig-asin-cg]] | 16BPP：从 Taylor/Padé 到 Nvidia Cg Minimax + Estrin 的 asin 近似优化历程 |
| [[sources/jonolick-ediz-critique]] | Jon Olick：批判 EDIZ 简单上采样算法 |
| [[sources/jonolick-laplacian-error-diffusion]] | Jon Olick：介绍 Laplacian 结构感知误差扩散 |
| [[sources/jonolick-sift-library]] | Jon Olick：jo_sift.h 单文件 SIFT 库 |
| [[sources/selfshadow-pbs-siggraph-2012]] | Hill：SIGGRAPH 2012 PBS 课程（Disney Principled BRDF 首发） |
| [[sources/selfshadow-pbs-siggraph-2025]] | Hill：SIGGRAPH 2025 PBS 课程（OpenPBR / EON / 神经材质 / GT7 tone mapping） |
| [[sources/asawicki-graphics-apis-yesterday-today]] | Sawicki：DirectX/OpenGL/Vulkan 演进史科普 |
| [[sources/asawicki-system-load-formula]] | Sawicki：整体系统负载公式 + 交互 demo |
| [[sources/asawicki-dx12-gdc-2026-comments]] | Sawicki：GDC 2026 DirectX 12 新特性的应用端点评 |
| [[sources/bartwronski-poisson-gui]] | Wronski：Poisson 采样生成器加 PyQt GUI + 旋转 disk 模式 |
| [[sources/bartwronski-multithreading-vfx-review]] | Wronski：《Multithreading for Visual Effects》书评，VFX 工具链多线程改造 |
| [[sources/danielilett-snapshot-pro-pixelate]] | Ilett：Snapshot Shaders Pro - Pixelate 单参数空间量化 |
| [[sources/danielilett-snapshot-pro-posterize]] | Ilett：Snapshot Shaders Pro - Posterize 三通道独立色阶 + Power Ramp |
| [[sources/danielilett-snapshot-pro-radial-blur]] | Ilett：Snapshot Shaders Pro - Radial Blur kernel 随径向距离变化 |
| [[sources/danielilett-snapshot-pro-scanlines]] | Ilett：Snapshot Shaders Pro - Scanlines 贴图驱动扫描线 |
| [[sources/danielilett-snapshot-pro-sepia-tone]] | Ilett：Snapshot Shaders Pro - Sepia Tone 单 Blend 参数 luminance 棕褐调色 |
| [[sources/danielilett-snapshot-pro-outline-sobel]] | Ilett：Snapshot Pro 基础 color-only Sobel 描边 |
| [[sources/danielilett-snapshot-pro-neon-sobel]] | Ilett：Snapshot Pro Sobel 掩膜 × HSL 提饱和霓虹 |
| [[sources/danielilett-snapshot-pro-outlines-fancy]] | Ilett：Snapshot Pro color+depth+normal 三路 Sobel 合成 |
| [[sources/danielilett-snapshot-pro-oil-painting]] | Ilett：Snapshot Pro Kuwahara 油画后处理 |
| [[sources/danielilett-snapshot-pro-noise-grain]] | Ilett：Snapshot Pro 程序化胶片颗粒，Hermite/Quintic 插值 |
| [[sources/cmwdexint-urp-builtin-feature-mapping]] | cmwdexint：URP 与 Built-in RP 特性映射 |
| [[sources/cmwdexint-urp-settings-locations]] | cmwdexint：URP 设置面板在哪里找 |
| [[sources/cmwdexint-urp-shadergraph-fog-disable]] | cmwdexint：关掉 URP Lit ShaderGraph 的雾效 |
| [[sources/thomas-poulet-ninokuni-2-frame]] | Poulet：Ni No Kuni 2 的 light pre-pass + MRT 线稿帧分析 |
| [[sources/thomas-poulet-dcs-frame]] | Poulet：DCS 2.7 的 YUV GBuffer + SDF cloudscape 帧分析 |
| [[sources/thomas-poulet-physics-tools-ue5]] | Poulet：UE5 物理游戏的五档可观测性工具栈 |
| [[sources/thomas-poulet-anno-1800-frame]] | Poulet：Anno 1800 完整帧分析（自研引擎、forward+MSAA、node-texture 地形、FFT ocean）|
| [[sources/thomas-poulet-blueprint-validation]] | Poulet：UE 蓝图资产验证的两处坑 |
| [[sources/benui-ui-as-communication]] | Ben UI：UI 作为传达，十种媒介与冗余原则 |
| [[sources/benui-ux-opinions]] | Ben UI：must/should/may 级 UX 意见清单 |
| [[sources/nullprogram-linked-list-intrusive-index]] | Wellons：链表 + 侵入 trie + MSI 索引 的渐进叠加 |
| [[sources/nullprogram-python-wasmtime]] | Wellons：用 wasmtime-py 把 Wasm 作为 Python 扩展机制 |
| [[sources/nullprogram-u-config-wine]] | Wellons：单个 exe 在 Windows/Wine 下双身份 pkg-config |
| [[sources/nullprogram-ai-programming-quiltcpp]] | Wellons：转向 AI 协作编码与 Quilt.cpp 案例 |
| [[sources/nullprogram-dcmake]] | Wellons：基于 CMake DAP 的 GUI 调试器 dcmake |
| [[sources/graphics-guy-tsl-shading-language]] | Cao 2021：为离线渲染器 SORT 写 Tiny Shading Language |
| [[sources/graphics-guy-restir-di-math]] | Cao 2022：ReSTIR DI 数学补完（SIR/RIS/WRS/邻居复用/visibility reuse） |
| [[sources/graphics-guy-fiber-cpp-basics]] | Cao 2023：Fiber 基础、与 C++20 coroutine 的对比、x64 最小实现 |
| [[sources/graphics-guy-restir-gi-math]] | Cao 2025：ReSTIR GI 数学（PSS、per-candidate target function、路径 initial candidate），Zorah/RTX 50 背景 |
| [[sources/alexharri-web-clipboard]] | Alex Harri：Web 剪贴板如何存储不同类型数据 |
| [[sources/alexharri-icelandic-name-trie]] | Alex Harri：把冰岛人名格变规则压进 3.27 kB trie |
| [[sources/alexharri-ascii-rendering]] | Alex Harri：ASCII 字符不是像素——形状向量渲染深入 |
| [[sources/graphics-guy-volume-rendering-offline]] | A Graphics Guy：PBRT 体积渲染章节的 in-scattering ODE 推导补齐 |
| [[sources/graphics-guy-pbrt-bxdf-verify]] | A Graphics Guy：PBRT bsdftest 如何验证 BXDF 的数学依据 |
| [[sources/graphics-guy-anisotropic-microfacet-sampling]] | A Graphics Guy：各向异性 GGX/Beckmann/Blinn importance sampling 全推 |
| [[sources/graphics-guy-color-science-basics]] | A Graphics Guy：从 SPD/CIE XYZ 到 Rec.709/sRGB/Rec.2020 的色彩科学地图 |
| [[sources/graphics-guy-sss-practical-tips]] | A Graphics Guy：SORT 集成 PBRT 3rd SSS 的 fireflies 消除与材质重构经验 |
| [[sources/acko-i-is-for-intent]] | Wittens：Intent 作为 source of truth，patch 驱动的前端架构 |
| [[sources/acko-occlusion-with-bells-on]] | Wittens：Use.GPU 0.14 GTAO + render pass 编排实录 |
| [[sources/acko-html-is-dead]] | Wittens：DOM/CSS/HTML 批判与替代路径 |
| [[sources/adrian-transparent-pixels]] | Courrèges：alpha=0 像素的 RGB 值如何污染边缘，flood-fill + 预乘 alpha 双解 |
| [[sources/adrian-mgs-v-graphics-study]] | Courrèges：MGS V / Fox Engine 一帧完整解剖（定制 ReShade 分支绕反调试） |
| [[sources/adrian-ue4-optimized-post-effects]] | Courrèges：UE4 在 Tegra X1 上的三组 drop-in 优化补丁（GatherDOF / half-res SSAO / reactive dynres） |
| [[sources/asawicki-d3d12-resource-alignment]] | Sawicki：D3D12 资源对齐的秘密（2020） |
| [[sources/asawicki-compute-shader-sv-cheat-sheet]] | Sawicki：compute shader system-value 速查（2020） |
| [[sources/asawicki-memory-fragmentation-metric]] | Sawicki：内存碎片度量公式（2022） |
| [[sources/yiningkarlli-pixar-optix-rtp]] | Yining Karl Li：2013 Pixar OptiX Lighting Preview demo 博客 |
| [[sources/yiningkarlli-zootopia]] | Yining Karl Li：Zootopia 与 Hyperion、Chiang 毛发模型初登场 |
| [[sources/yiningkarlli-mipmap-bidirectional]] | Yining Karl Li：Takua 的 camera-based mip level 选择，解 BDPT 下 ray differentials 难题 |
| [[sources/bkaradzic-orthodox-cpp]] | Karadžić：Orthodox C++ 子集主张 |
| [[sources/bkaradzic-open-source-or-it-didnt-happen]] | Karadžić：独立团队的中间件与开源取舍 |
| [[sources/bkaradzic-airmech-native-client]] | Karadžić：AirMech 移植到 Native Client 的工程笔记 |
| [[sources/bruop-ibl-multiple-scattering]] | Bruop：BGFX 中实现 Fdez-Agüera 多次散射 IBL |
| [[sources/bruop-frustum-culling]] | Bruop：AABB 顶点 clip-space 测试 + AVX2 手写 SIMD |
| [[sources/bruop-more-robust-frustum-culling]] | Bruop：SAT 分离轴 + ISPC 实现，修掉 false negative |
| [[sources/erfan-ahmadi-texture-upload-staging]] | Ahmadi：Nabla 流式 staging 纹理上传 |
| [[sources/erfan-ahmadi-frames-in-flight]] | Ahmadi：Frames In Flight 与 timeline semaphore |
| [[sources/erfan-ahmadi-bokeh-dof-project]] | Ahmadi：The Forge 上三种 Bokeh DoF 实现 |
| [[sources/halisavakis-animated-light-cookies]] | Alisavakis：Custom Render Texture 驱动的动画 light cookie 小实验 |
| [[sources/jonolick-wav-one-function]] | Olick：单函数 WAV 写入器（2012 短贴） |
| [[sources/jonolick-dxt-codebooks-sliding-windows]] | Olick：DXT 压缩之码表与滑窗（Part 1） |
| [[sources/jonolick-dxt-part3-transposes]] | Olick：DXT Part 3 transpose（正文不完整） |
| [[sources/jonolick-dxt-part4-entropy]] | Olick：DXT Part 4 熵降维到 1.51 bpp |

| [[sources/cyanilux-gpu-instanced-grass]] | Cyan：Unity URP + Shader Graph 的 GPU 实例化草地全流程（含 Unity 6 Instance ID 变化 + `UnityIndirect.cginc` `_Base` 版本踩坑） |
| [[sources/hooper-segment-array]] | Hooper：增长数组 + 稳定指针 + 10 指令 sa_get |
| [[sources/hooper-build-visualizer]] | Hooper：用系统调用监听做构建甘特图 |
| [[sources/hooper-swiftui-hot-reloading]] | Hooper：SwiftUI 热重载 120 行实现 |
| [[sources/hooper-what-the-fork]] | Hooper：What The Fork 产品页 |
| [[sources/hooper-testing-ai-c]] | Hooper：老 C 程序员实测 Claude Code / Opus 4.5 |
| [[sources/hexops-mach-nominated-zig]] | Hexops：Mach 提名 Zig 版本的正式化 |
| [[sources/hexops-mach-v0-3-released]] | Hexops：Mach v0.3 发布（sysgpu / sysaudio / ECS / Sprite） |
| [[sources/hexops-dxcompiler-better-than-microsoft]] | Hexops：比微软自己更好地构建 DXC |
| [[sources/hexops-pkgmirror]] | Hexops：pkgmirror 自托管 Zig 镜像发布 |
| [[sources/runevision-gdc2010-animation]] | Rune Johansen：GDC 2010 现场观察 Uncharted 动画技术 |
| [[sources/chipsandcheese-nvidia-mcm-gpu]] | Chester Lam：从 Nvidia 2017 论文看下一代 MCM server GPU |
| [[sources/raytracey-2010-gpu-renderer-landscape]] | Lapere：2010 GPU 非偏置渲染器的集体觉醒 |
| [[sources/raytracey-otoy-solidworks-cloud]] | Lapere 转载：OTOY RV770 云渲染细节与 SolidWorks 合作 |
| [[sources/c0de517e-pitfalls-of-experience]] | Pesce：经验的陷阱——从 Crysis 深度缓冲 SSAO 反推谈起 |
| [[sources/schoener-intro-computational-complexity]] | Schöner：$\P/\NP/\coNP$/归约 入门 |
| [[sources/schoener-complexity-of-patterna]] | Schöner：Patterna/HexCells/Minesweeper 推理问题是 $\coNP$-complete |
| [[sources/chipsandcheese-jpeg-image-compression-overview]] | BlueSwordM：JPEG 编码管线与前 JPEG 时代回顾 |
| [[sources/chipsandcheese-security-overview]] | Chips and Cheese：AMD/Intel/Nvidia 三家平台安全栈横向对比 |
| [[sources/chipsandcheese-ctr-safety-revisited]] | Chips and Cheese：CTR 安全追踪与电迁移物理复盘 |
| [[sources/randomtower-flashpunk-review]] | Marte：FlashPunk 框架架构分析 |
| [[sources/randomtower-flashpunk-hello-world]] | Marte：FlashPunk Hello World Shooter 实践教程 |
| [[sources/chipsandcheese-zen2-cinebench-analysis]] | Chester Lam：Zen 2 在 CBR15 的微架构优势分析 |
| [[sources/chipsandcheese-image-compression-part2]] | BlueSwordM：JPEG-XL/AVIF/WebP 图像压缩对比（2021 Part 2）|
| [[sources/chipsandcheese-gpu-memory-latency]] | Chester Lam：GPU 多级缓存延迟实测（OpenCL pointer chasing）|
| [[sources/raytracey-svo-path-tracing-update]] | Lapere：Voxelstein 3D + Laine SVO 论文 |
| [[sources/raytracey-fermi-optix-benchmark]] | Lapere：Fermi / OptiX Design Garage 相对 GTX 285 提升 870% |
| [[sources/joostdevblog-dof-blur-proun]] | van Dongen：Proun 的变采样半径景深（2010） |
| [[sources/joostdevblog-overbright-fake-hdr]] | van Dongen：用半亮度渲染在 8-bit 后端伪装 HDR（2010） |
| [[sources/supnik-when-to-rewrite]] | Supnik：何时重写——大重写的失败剧本与增量重构 |
| [[sources/supnik-coding-for-two-audiences]] | Supnik：代码写给编译器和人类两类读者 |
| [[sources/supnik-fast-paths]] | Supnik：API 设计的快/慢路径显式分层 |
| [[sources/supnik-tile-too-far]] | Supnik：number puzzle 瓦片随机化 shader 与 fixed function 壁垒 |
| [[sources/supnik-debugging-glsl]] | Supnik：GLSL printf = 写 gl_FragColor + shader 热重载 |
| [[sources/gemserk-signing-jars-applet-webstart]] | Gemserk：用 maven-webstart-plugin 为 Applet / Webstart 自动签 JAR（2010） |
| [[sources/boristhebrave-tileset-roundup]] | Boris：2D autotile 切片布局综述（Marching Squares/Blob/Sub-blob/Micro-blob） |
| [[sources/boristhebrave-as3-gems]] | Boris：AS3 语言设计中值得借鉴的几个「钻石」 |
| [[sources/boristhebrave-axaxaxas]] | Boris：Python Earley parser 库发布说明 |
| [[sources/bitsquid-content-repositories-vs-databases]] | Frykholm：为什么我们不把内容放数据库 |
| [[sources/bitsquid-the-blob-and-i]] | Frykholm：用 offset 替代 pointer patching 做 blob 资源 |
| [[sources/bitsquid-task-management-practical]] | Frykholm：Bitsquid 任务调度器的实战实现 |
| [[sources/bitsquid-distance-field-angelcode-fonts]] | Frykholm：用 AngelCode BMFont 生成 SDF 字体 |
| [[sources/bitsquid-our-tool-architecture]] | Frykholm：Bitsquid 的工具架构 —— JSON 消息 + 子窗口嵌入 |
| [[sources/allar-udk-beginning-your-game]] | Allar 2010 UDK 入门：搭空白 GameInfo 与 Pawn/PlayerController 子类 |
| [[sources/schoener-no-magic]] | Schöner：No Magic Principle 信条文 |
| [[sources/schoener-tensorflow-intro]] | Schöner：TF 1.3 Jupyter 入门（MNIST CNN + Dataset API） |
| [[sources/schoener-tensorflow-multi-gpu]] | Schöner：TF1 单机多卡 in-graph replication + 跨机 distributed |
| [[sources/schoener-dl-uncertainty]] | Schöner：深度学习里「uncertainty」的五义拆解与 MC dropout 质疑 |
| [[sources/c0de517e-skin]] | Pesce 2010：皮肤渲染 benchmark + Jim Hejl 关于 FN4 屏幕空间 SSS 的评论 |
| [[sources/tedsie-a-star-tutorial]] | Ted Sie：Unity A* 寻路四步实作（Node/Manager/Sort） |
| [[sources/bitsquid-practical-dod-scene-graphs]] | Frykholm：per-entity 场景图为什么不需要优化增删 |
| [[sources/bitsquid-3-way-json-merge]] | Frykholm：写一个能理解 JSON 的三路合并器 |
| [[sources/bitsquid-new-data-storage-model]] | Frykholm：GUID + 属性 + 5 种操作的无冲突数据库草案 |
| [[sources/bitsquid-dual-mode-guis]] | Frykholm：同一 GUI API 两种模式的实现技巧 |
| [[sources/supnik-ive-got-the-blues]] | Supnik：NVidia/Linux 下 gl_Normal 与 attribute 2 的别名 bug |
| [[sources/supnik-templating-functions]] | Supnik：C++ 模板按值参数化函数指针才能内联 |
| [[sources/supnik-devil-in-details]] | Supnik：Stack Overflow 不是免费调试服务——OpenGL bug 的三类 taxonomy |
| [[sources/supnik-to-strip-or-not-to-strip]] | Supnik：为什么 X-Plane 在桌面 GL 上全部用 indexed triangles，放弃三角带 |
| [[sources/joostdevblog-camera-mapping]] | Joost van Dongen：把 2D 插画投影成 3D 动画的三连载（Evil Pope / Captain August / tips）|
| [[sources/joostdevblog-proun-3000fps-collision]] | Joost van Dongen：Proun 把 gameplay 锁在 3000fps 解决碰撞 tunneling |
| [[sources/joostdevblog-proun-motion-sickness]] | Joost van Dongen：Proun 抗晕眩的摄像机设计决策 |
| [[sources/bitsquid-visual-scripting-data-oriented]] | Frykholm：Flow 可视化脚本 runtime 的 blob + switch dispatch 设计 |
| [[sources/bitsquid-custom-memory-allocation]] | Frykholm：Allocator 抽象接口、subsystem proxy、bootstrap 与 assert-on-leak |
| [[sources/bitsquid-static-hash-values]] | Frykholm：字符串 hash 编译期化的三条路线比较 |
| [[sources/bitsquid-dependency-checker]] | Frykholm：500 行依赖图工具，missing/dangling/replace/move/copy |
| [[sources/4rknova-cpp-embed-files]] | 4rknova：C/C++ 嵌入二进制资源的三种做法 |
| [[sources/4rknova-glsl-game-of-life]] | 4rknova：Conway 生命游戏的 GLSL/ShaderToy 实现 |
| [[sources/supnik-stl-not-abstraction]] | Supnik：STL 不是抽象，它是 shortcut |
| [[sources/supnik-scroll-opengl-world]] | Supnik：X-Plane 如何在 32-bit float 下滚动一个真实大小的地球 |
| [[sources/supnik-glxgetprocaddressarb-syntax]] | Supnik：glXGetProcAddressARB 为什么返回函数指针而非 void* |
| [[sources/supnik-change-uv-map-on-fly]] | Supnik：texture2DGradARB 解决 fract-UV 的 LOD 失配 |
| [[sources/supnik-running-out-of-derivative-res]] | Supnik：顶点投影 UV 在 8800 GT 上耗尽导数精度 |
| [[sources/bitsquid-time-step-smoothing]] | Niklas Frykholm：变步长下的 time step smoothing 策略 |
| [[sources/bitsquid-a-is-overrated]] | Niklas Frykholm：A* is Overrated，导航不是寻路 |
| [[sources/bitsquid-managing-coupling]] | Niklas Frykholm：引擎解耦四条原则 |
| [[sources/bitsquid-managing-coupling-part-2]] | Niklas Frykholm：polling / callback / event 三选一的工程取舍 |
| [[sources/bitsquid-tiny-expression-language]] | Frykholm 2011：一个小巧的表达式语言 |
| [[sources/bitsquid-collaboration-and-merging]] | Frykholm 2011：协作的核心是合并，不是数据库 |
| [[sources/bitsquid-extreme-bug-hunting]] | Frykholm 2011：极限 bug 狩猎——只在 release / 只在 PS3 / 不同调用栈 |
| [[sources/bitsquid-universal-undo-copy-paste]] | Frykholm 2011：基于 GUID 对象库 schema 的通用 Undo / Copy / Paste |
| [[sources/supnik-alpha-front-to-back]] | Supnik：前向/后向 alpha blending 的 blend state 推导 |
| [[sources/supnik-double-buffering-vbos]] | Supnik：VBO 双缓冲与 D3D DISCARD / GL orphaning 的对照 |
| [[sources/supnik-agp-vs-vram]] | Supnik：为什么流式 VBO 放 AGP 比 VRAM 更安全 |
| [[sources/supnik-glbuffersubdata]] | Supnik：glBufferSubData 为何会串行化阻塞 |
| [[sources/joostdevblog-stereoscopic-3d]] | van Dongen：立体 3D 的设计含义（2010） |
| [[sources/joostdevblog-sun-rays]] | van Dongen：Proun 的屏幕空间 god-rays（2010） |
| [[sources/joostdevblog-lighting-in-proun]] | van Dongen：Proun 的 lightmap 烘焙流程（2010） |
| [[sources/joostdevblog-coloured-light-proun]] | van Dongen：Proun 的对比色 sun/skylight 艺术选择（2010） |
| [[sources/joostdevblog-pc-dev-horror]] | van Dongen：PC 发行的显卡驱动兼容血泪（2010） |
| [[sources/nklein-cl-opengl-text-cutoff]] | Stein：CL-OpenGL + ZPB-TTF 文本反走样的屏幕空间 cutoff 计算 |
| [[sources/supnik-value-of-granularity]] | Supnik：OpenGL 扩展分桶与细粒度开关 |
| [[sources/supnik-santa-youre-an-idiot]] | Supnik：GPU 已经足够并行，不需要并行命令派发 |
| [[sources/supnik-cgal-mantissa]] | Supnik：CGAL 尾数膨胀与 float round-trip 精度重置 |
| [[sources/bitsquid-flow-followup-qa]] | Frykholm：Flow 文章后续 Q&A（hierarchical grouping / query 节点） |
| [[sources/bitsquid-monitoring-your-game]] | Frykholm：游戏监控系统 TLS event buffer 设计 |
| [[sources/bitsquid-strings-redux]] | Frykholm：UTF-8 everywhere、不要 string class、runtime 用 hash |
| [[sources/bitsquid-lightweight-lua-bindings]] | Frykholm：light userdata 绑定、手写类型 marker、句柄生命周期 |
| [[sources/bitsquid-fixing-memory-issues-lua]] | Frykholm：Lua 内存泄漏定位、GC 预算反馈控制 |
| [[sources/supnik-cgal-arrangements-import]] | Supnik：把脏多边形导入 CGAL arrangement 的策略与 antenna 问题 |
| [[sources/supnik-fear-of-threading]] | Supnik：线程的开发成本与消息队列所有权模式 |
| [[sources/supnik-vbo-really-double-buffered]] | Supnik：driver 视角重新解释 VBO 为什么没法自动双缓冲 |
| [[sources/bitsquid-better-watch-windows]] | Frykholm 2011：跨平台外部 watch window 设想 |
| [[sources/bitsquid-murmur-hash-inverse]] | Frykholm 2011：MurmurHash2 32/64 位 inverse 代码 |
| [[sources/bitsquid-roll-your-own-docs]] | Frykholm 2011：100 行 Ruby 自制文档管线（parser + generator）|
| [[sources/bitsquid-id-lookup-table]] | Frykholm 2011：Managing Decoupling Part 4 — ID Lookup Table |
| [[sources/bitsquid-header-hero]] | Frykholm 2011：Header Hero 工具与 C++ include 瘦身实操 |
| [[sources/nklein-xml-parser-generator]] | Stein：用 Common Lisp 重写 XML Parser Generator，两文合并 |
| [[sources/bitsquid-low-level-animation-part-2]] | Bitsquid：动画流式 cache 布局 + active 数组 |
| [[sources/bitsquid-dod-sound-parameters]] | Bitsquid：声音参数集合的五步 DOD 重构 |
| [[sources/bitsquid-pragmatic-performance]] | Bitsquid：务实性能观七条 + 数量级设计指南 |
| [[sources/bitsquid-platform-specific-resources]] | Bitsquid：property 资源变体系统（平台编译期 + 语言运行期） |
| [[sources/bitsquid-link-exe-lnk4099-patch]] | Bitsquid：patch link.exe 忽略 LNK4099 的 Ruby 脚本 |
| [[sources/supnik-race-condition-debug]] | Supnik：debugger 打印 STL 容器释放线程导致观察到 race |
| [[sources/supnik-openal-linux-part-27]] | Supnik：OpenAL/Linux SONAME 升 major + 删旧 .so 的 ABI 管理翻车 |
| [[sources/supnik-when-good-floating-point-goes-bad]] | Supnik：X-Plane 里点积谓词与线线求交的浮点失效模式 |
| [[sources/supnik-premultiplication-pros-cons]] | Supnik：预乘 alpha 修 tree ring，但 BCn 压缩精度让 X-Plane 转走 alpha test |
| [[sources/supnik-alpha-blending-lets-try-again]] | Supnik：预乘约定下 back-to-front / front-to-back blend state 的对称重推 |
| [[sources/tedsie-a-star-applied]] | Ted Sie 2016-07 A* 应用篇（四文合并）：FindPath 伪代码实作 + 斜向优化 + Line-of-sight 平滑 + Obstacle raycast 判定 |
| [[sources/supnik-gpu-sliced-shadows-fail-clouds]] | Supnik：flight-sim 云为什么不能用 GPU sliced shadow |
| [[sources/supnik-openal-three-platforms]] | Supnik：OpenAL 在 OS X / Linux / Windows 的统一装载策略 |
| [[sources/supnik-finding-mom-and-dad]] | Supnik：C++ 侵入式结构里孩子找父亲的类型系统限制 |
| [[sources/supnik-c-seventies-technology]] | Supnik：C 位运算符优先级的 B/BCPL 历史根源 |
| [[sources/bitsquid-5-tips-programmer-productivity]] | Niklas：五条程序员日常纪律 |
| [[sources/bitsquid-sensible-error-handling-part-1]] | Niklas：unexpected error 立即 crash 的哲学 |
| [[sources/bitsquid-sensible-error-handling-part-2]] | Niklas：expected error 的 API 收敛与错误码回归 |
| [[sources/bitsquid-sensible-error-handling-part-3]] | Niklas：warning 分类与升格为 error 的战术 |
| [[sources/bitsquid-documentation-system-code]] | Niklas：Bitsquid 文档系统代码公开，line-by-line + HTML context 栈 |
| [[sources/playcanvas-cloud-asset-pipeline]] | Evans：PlayCanvas 把资产转码搬进浏览器（2013） |
| [[sources/supnik-gamma-lighting-trilogy]] | Supnik 2010-11 gamma 四连发：color sync + linear lighting + errata + 量化对比实证 |
| [[sources/bitsquid-cutting-the-pipe-qa]] | Niklas 讲座评论区 Q&A：工具 C# / 引擎 C++ / JSON 通信 / 零代码共享 |
| [[sources/bitsquid-pimpl-vs-pure-virtual]] | Niklas 对 C / PIMPL / 纯虚三种接口-实现分离方式的横向评测 |
| [[sources/bitsquid-inheriting-velocity-ragdolls]] | Niklas：ragdoll 切换时速度继承的四种候选与 last_world 选择 |
| [[sources/bitsquid-embracing-dynamism]] | Niklas：Bitsquid 把 Lua 动态性榨到底的七条常见技巧 |
| [[sources/c0de517e-collaborative-engine-design]] | Pesce：2010 年 etherpad 协作引擎架构清单 |
| [[sources/supnik-more-stl-abstraction]] | Supnik：STL 规格内的实现弹性与容器选型 |
| [[sources/supnik-change-of-basis-revisited]] | Supnik：矩阵列即基向量、affine-orthogonal 子集 |
| [[sources/supnik-basis-projection]] | Supnik：矩阵行是 encoder、转置即逆的几何意义 |
| [[sources/supnik-is-1-a-lot]] | Supnik：杠杆率与 Shark profile 上的 X-Plane 9.62 |
| [[sources/supnik-semaphore-vs-condvar]] | Supnik：cond var 重锁开销与 mach semaphore 方案 |
| [[sources/bitsquid-playing-with-video]] | Frykholm 2012：视频 codec 选型——VP8 赢在最 free |
| [[sources/bitsquid-hack-day-report]] | Frykholm 2012：hack day 粒子碰撞重写（每粒子 plane + 空间 hash）|
| [[sources/bitsquid-matrices-rotation-scale-drifting]] | Frykholm 2012：Matrix4x4 scale 漂移与四种修法 |
| [[sources/bitsquid-simpler-async-api]] | Frykholm 2012：异步 API 的 ID token / implicit 激进简化 |
| [[sources/bitsquid-cleaning-bad-code]] | Frykholm 2012：清理烂代码 9 条操作手册 |
| [[sources/tedsie-ngui-tutorials]] | Ted Sie 2016-07 NGUI 入门四讲合并（UIPanel/UISprite + UIAtlas + Scroll View + Button） |
| [[sources/tedsie-draw-call-basics]] | Ted Sie：Draw Call 初步理解（材质实例即批边界） |
| [[sources/supnik-semaphore-nptl]] | Supnik 2010-12：Linux NPTL 把上一篇的 OS X 原语选择问题大多消除 |
| [[sources/supnik-gbuffer-format]] | Supnik 2010-12：X-Plane 10 G-Buffer 格式自述（4 RT / 16 B / 浮点字段打包） |
| [[sources/supnik-fmtt-glsl-edition]] | Supnik 2010-12：X-Plane G-Buffer 的 GLSL `gl_FragData[0..3]` 实现样本 |
| [[sources/supnik-what-oop-isnt]] | Supnik 2010-12：90/10/0 OOP 三要素启发式 + 评论区对实现继承的细化 |
| [[sources/bitsquid-organizing-header-files]] | Frykholm 2012：types.h 集中数据、函数按功能分组的 header 组织方式 |
| [[sources/bitsquid-vector-fields]] | Frykholm 2012 三部曲合并：向量场的外循环指令/内循环数据字节码 VM |
| [[sources/bitsquid-foundation-library]] | Frykholm 2012：Bitsquid Foundation Library 开源发布（MIT / allocator + POD 集合）|
| [[sources/joostdevblog-all-the-settings]] | Joost：600 个 gameplay 数值的 F5 热重载工具 |
| [[sources/joostdevblog-designing-levels-without-tools]] | Joost：Swords & Soldiers 用 Notepad 做关卡 |
| [[sources/joostdevblog-ai-swords-soldiers]] | Joost：Swords & Soldiers AI（行为树两篇合并） |
| [[sources/supnik-glsl-compiler-observations]] | Supnik：AMD ShaderAnalyzer 看到的 GLSL 编译器做了什么没做什么 |
| [[sources/supnik-cas-reference-counting]] | Supnik：CAS+refcount 的低位锁变体与 Vyukov 评论区给的 differential refcount |
| [[sources/supnik-derivatives-two-parts]] | Supnik：GLSL derivative 两连载，UV 不连续 + if 分支内的未定义导数 |
## 元（wiki/meta/）
| 文章 | 一句话描述 |
|---|---|
| [[taste-development]] | 基于 wiki 内容综合出的品味训练方法 |
| [[ai-assisted-reading-workflow]] | AI 辅助阅读：机器直译 + LLM 上下文解释的小说阅读工作流 |
| [[llm-rule-hallucination]] | LLM 在冷门规则 / 新知识上的幻觉模式：自信度与知识边界完全解耦 |
| [[quilt-cpp-ai-driven-clone]] | Wellons 4 天用 AI 克隆 Quilt 的案例 |
| [[ai-driven-conformance-clone]] | 用 AI 克隆既有 CLI 工具的 conformance 测试法 |
| [[c-memory-safety-even-for-ai]] | 为何 AI 协作时代应选 C++ 而非 C |

## 特殊页面

- [[overview]] —— 综合叙事：把主题串起来
- [[log]] —— 所有操作的时间顺序记录
