---
tags: [vector-field, bytecode-vm, sse, data-oriented, simd, particle, physics, bitsquid]
date: 2026-04-19
sources: 1
---

# 向量场的外循环指令 / 内循环数据字节码 VM

[[niklas-frykholm|Niklas Frykholm]] 2012 年为 Bitsquid 设计的风力系统（vector field）核心机制。它解决的问题是：**让一个"在运行时才能确定的函数"`G(p)` 被上万个粒子求值，还要跑到接近 SSE 原生速度**。方案是一个反直觉的字节码 VM 结构——**外层循环遍历字节码指令、内层循环遍历所有数据点**，把"解码 + 跳转"的成本摊薄到几乎为零。

## 问题定义

游戏里"风"要作用于粒子、物理对象、草、旗帜、树等一切。需求上：

- **全局共享状态**：所有系统看同一份风；子系统不能硬耦合
- **每帧 10000+ 次查询**：粒子级 `G(p)` 求值，必须便宜
- **同时容纳全局效应与局部效应**：基础风 + 爆炸 + 通风口 + 漩涡
- **完全数据驱动**：引擎里不能写死"支持 explosion/updraft/whirl 三种"；licensee 要能在数据里加新效应而无需改 C++ 源码

朴素的"把风速存网格"败在内存和更新成本。写死几种 C++ 效应类败在[[data-driven-architecture|数据驱动性]]。写成通用 bytecode 败在"普通字节码比 native 慢 10 倍"——跟游戏每帧几万次求值的预算完全不兼容。

## 三步压价

**Step 1：表达为函数 + 时间折叠**

`F(p, t)` 在任一帧 `t` 固定，于是把系统劈成两层：高层每帧做一次**常量折叠**从 `F(p, t)` 得 `G(p)`，低层只管高速求值 `G(p)`。这把"每粒子一次 `sin(t)`"这类开销压到每帧一次。

**Step 2：叠加 + AABB 裁剪**

```
G(p) = G_0(p) + G_1(p) + ... + G_n(p)
```

每个 `G_i` 是一个带 AABB 的局部效应（爆炸/漩涡/通风口），基础风是 `Vector3(2.1, 1.4, 0)` 这样的常量。每帧用粒子群的 AABB 与每个 `G_i` 的 AABB 求交，剔除无关效应，得到一个**与本帧相关的最小 `G'(p)`**。

**Step 3：大规模向量化 VM**（核心）

正常 bytecode VM 的热路径是：

```
for each query point p:
    for each instruction op:
        decode op
        jump to handler
        execute(p)
```

解码和跳转的成本每点都付一次，所以慢。Frykholm 把两层循环对调：

```
for each instruction op:
    decode op
    jump to handler
    for each query point p (in chunks):
        execute(p)
```

**一条指令的解码开销摊薄到 1024+ 个粒子上**。在他的测试里字节码比 native 只慢 **16%**——比经典字节码快了 8×。这本质上是把 VM 当**解释执行的 SIMD ISA** 来用，跟 GPU warp 的结构同构（同指令多数据）。

## 寄存器、scratch buffer 与分块

选择 register-based 而不是 stack-based：指令数更少，内层循环每次跑得更短。所有变量存 `Vector4I` 数组，利用 SSE。

本地变量（如示例中 `direction`、`lensqr`）必须是**数组**——内层循环要在所有粒子上跑这条指令，每个粒子需要自己的中间值。一个复杂函数带 20 个本地变量、10000 粒子就是 3.2 MB 临时内存，不可预测。

Frykholm 的做法：调用方传一块 `scratch_space`，VM 在它上面切出每条通道的 buffer。**buffer 大小反过来决定一次处理多少粒子**——比如 256K scratch / 8 本地变量 = 每通道 32K = 2K 粒子，10000 粒子切成 5 个 chunk 处理。摊薄指数从"10000"降到"2048"但依然足够大，内存预算却变得**完全可预测**，可以写进引擎 budget。

## bytecode 格式与高阶 DSL

格式极简：`(op)(result)(arg1)(arg2)`，每字段 4 字节。**不做 pack**——因为解码成本已经被摊薄，压榨字节数不带来收益。代价是 2-arity 指令需要 4 个变体覆盖"寄存器 vs 常量"的组合，4-arity 指令需要 16 个变体——Frykholm 选择让变体爆炸，因为把常量/寄存器 dispatch 放进 handler 内部反而让内层循环变慢。

人写的时候用类 [[slang-shader-language|HLSL]] 的 DSL：

```hlsl
const float4 center = float4(0,10,0,0);
struct vf_in  { float4 position : CHANNEL0; float4 wind : CHANNEL1; };
struct vf_out { float4 wind : CHANNEL1; };
void whirl(in vf_in in, out vf_out out) {
    float4 r = in.position - center;
    out.wind = in.wind + speed * cross(up, r) / dot(r,r) * radius;
}
```

编译器用**递归下降解析整体结构**、**shunting yard 处理每个表达式**，直接从 value stack 生成 bytecode，临时通道用完即回收。没用 Lex/Yacc——Frykholm 偏好避免额外预编译步骤。

常量走**运行时 patch**：编译时记录 `(hashed_name, bytecode_offset)` patch 列表，gameplay 代码 `VectorField.add(field, "whirl", {radius = 10})` 动态修改这些 offset 处的 Vector4 常量，不用重编译 bytecode。副作用是编译期无法做完整常量折叠（patch 后的一遍 fold 还没实现）。

## 与 GPU 的关系

"外循环指令、内循环数据"正是 GPU warp 的执行模型。Frykholm 刻意选类 HLSL 语法就是留着 GPU 后路：只要某个效应 GPU 能跑就把同一份 DSL 编过去。2012 年 CPU 版的存在理由有二：**GPU 回读延迟**让物理这种 feedback loop 用不上 GPU；**动态拼 bytecode**（按本帧裁剪出的 `G'`）在 GPU 上的开销较大。

## 物理接入的两个工程经验

- **只对 awake actor 施加风力**：否则风让物理世界永不休眠，CPU 费光。代价是"睡着的叶子在爆炸里纹丝不动"。解法是显式 `wake_actors(aabb)` API，放爆炸效果前先叫醒一片物体。
- **Rotation 走 drag 点抬高的 hack**：drag force 本身无转动分量（物理正确），但视觉上需要"叶子被风吹到旋转"。把 drag 作用点抬到质心上方制造力臂。不追求物理正确，追求视觉可信——这与 [[ragdoll-velocity-inheritance]] 是一脉的工程哲学。

## 性能数据

- **20000 粒子 @ 0.4 ms**（单线程，SSE Vector4）
- **字节码比 native 慢 16%**（chunk ≥ 1024 时解码成本可忽略）
- 水平扩展到多线程接近线性

## 与其它字节码设计的对照

- 传统 [[bytecode-everywhere|字节码解释器]]（Lua、Python、ACPI AML）都是 per-instruction per-data，不做外内循环对调——它们的输入数据通常是标量、没有"同一段代码跑 10000 遍"的结构
- [[flow-graph-data-oriented-runtime|Flow 可视化脚本]]在 Bitsquid 后来的演化里走的是 **blob + switch dispatch**，也偏向把 dispatch 成本压低，但不做 vector-wide 展开
- **GPU compute shader**：同形结构的硬件化——Frykholm 这套可以理解为"CPU 上的 compute dispatch"

## 相关

- [[niklas-frykholm]]
- [[bytecode-everywhere]] —— 被忽视的无身份字节码
- [[data-driven-architecture]]
- [[aos-vs-soa]] —— scratch buffer 按通道切正是 SoA 布局
- [[slang-shader-language]] —— DSL 同源
- [[flow-graph-data-oriented-runtime]]
- [[ragdoll-velocity-inheritance]]

## Sources

- [[sources/bitsquid-vector-fields]]
