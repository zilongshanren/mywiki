# Day 1 · 引擎是什么 — 从游戏需求到引擎抽象

> 基于 Jason Gregory《Game Engine Architecture》第3版 Ch1.1-1.2，面向有经验的 Unity 开发者。

---

## 为什么需要引擎？从一个具体问题开始

假设你在 2003 年，没有 Unity，没有 Unreal，你需要做一个第三人称动作游戏。

你需要什么？渲染 3D 场景（矩阵变换、光栅化、纹理采样）；播放角色动画（骨骼蒙皮、关键帧插值）；检测碰撞（AABB、OBB、GJK 算法）；播放音效（缓冲区管理、空间化、混音）；加载资源（文件 I/O、反序列化、GPU 上传）；处理手柄输入（HID 轮询、死区处理、按键映射）；管理内存（避免碎片化、对象池）；网络同步（如果有联机的话）……

每一项都是成千上万行经过验证的代码。更关键的是：你的下一个游戏**也需要这些**。

这就是引擎存在的根本原因。不是"方便"，而是**生存**。

Gregory 在第一章开头就给出了这个朴素但深刻的观察：

> "While game engines vary widely in the details of their architecture and implementation, recognizable coarse-grained patterns have emerged across both publicly licensed game engines and their proprietary in-house counterparts."

游戏之间的共性，远大于差异。

---

## 引擎的三种定义视角

Gregory 给出的形式定义是：

> "A game engine is a software framework designed for the creation and development of video games."

但这个定义太宽泛——Adobe Flash 也可以"创建视频游戏"。更有价值的理解是从三个视角来看引擎是什么。

### 技术层视角：运行时服务集合

从技术上看，引擎是一套运行时基础设施（Runtime Infrastructure），为游戏提供所有通用的底层服务：

```
游戏逻辑层（你写的代码）
    ↓ 调用
引擎服务层
    ├── 渲染系统 ──────────→ GPU API (Metal/Vulkan/D3D12)
    ├── 动画系统 ──────────→ 骨骼变换 + 混合树
    ├── 物理系统 ──────────→ PhysX / Havok / Chaos
    ├── 音频系统 ──────────→ FMOD / Wwise / 原生 API
    ├── 资源管理 ──────────→ 文件 I/O + GPU 内存
    ├── 场景管理 ──────────→ 空间数据结构
    ├── 输入系统 ──────────→ HID → Action Mapping
    └── 脚本/反射 ─────────→ C# / Blueprint / Lua VM
    ↓ 调用
平台抽象层
    ├── Windows (DirectX 12)
    ├── iOS (Metal)
    ├── Android (Vulkan / GLES)
    └── PlayStation (AGC)
```

每一层只和相邻层通信——**循环依赖是引擎设计的死刑**。Gregory 在第 3 章会深入讲这个原则。

Unity 的架构严格遵循这个模型。你写的 MonoBehaviour 是最顶层，它通过 Unity C++ 引擎调用平台 GPU API，你永远不会直接操作 Vulkan 的 VkCommandBuffer。这不是限制，这是**封装**。

但 Unity 和 Unreal 在这个层次结构的实现上有本质差异——我们后面会详细比较。

### 生产层视角：工具链 + 内容管线

引擎不只是运行时。一个没有编辑器的引擎是不完整的。

内容生产管线：

```
内容创作工具          导入处理              运行时格式
──────────           ──────────           ──────────
Maya/Blender  ──→   FBX Import  ──→      Mesh (GPU-ready)
Photoshop    ──→   Texture Import ──→    ASTC / BC7 压缩纹理
Visual Studio ──→  IL2CPP/Burst  ──→     Native Binary
Unity Editor  ──→  Asset Bundle  ──→     .unity / .asset
```

Unity 的真正杀手锏是**编辑器**，不是运行时性能。Scene View 的实时预览、Inspector 的即时参数调整、Play Mode 的零等待迭代——这些功能让一个 5 人团队可以做出 20 年前需要 50 人团队才能做出的游戏。

Unreal Editor 同样强大，但设计哲学不同：Unreal 的 Blueprint 让非程序员直接在编辑器里写游戏逻辑（可视化脚本），Unity 的 Prefab Variant 让非程序员通过数据驱动定制游戏对象。两种方式都对，目标受众不同。

### 经济层视角：风险管理

从商业角度，引擎解决的是**风险问题**：

| 策略 | 技术风险 | 时间成本 | 适合场景 |
|------|---------|---------|---------|
| 自研引擎 | 极高 | 数年 | 大型 AAA 工作室，有独特技术需求 |
| 商业引擎（Unity/UE） | 低 | 数月 | 99% 的游戏项目 |
| 开源引擎（Godot） | 中 | 数月 | 独立游戏，社区支持够用 |

Naughty Dog 自研引擎（Uncharted、The Last of Us）的理由是：PS3/PS4 的 Cell 架构极其特殊，通用引擎无法榨取硬件性能的 100%。但这需要一支专门的引擎团队，这是他们作为索尼第一方工作室才有的奢侈。

普通团队选 Unity 或 Unreal，是因为风险可控——**引擎让小团队能做大游戏**。

---

## 游戏是什么？一个被低估的定义

在讲引擎之前，Gregory 先定义了"游戏"。这不是废话，而是让你理解引擎所有设计决策背后的约束。

> "Most two- and three-dimensional video games are examples of what computer scientists would call soft real-time interactive agent-based computer simulations."

分解这个定义：

**Soft real-time（软实时）**：必须在时间约束内完成计算，但不像硬实时系统（心脏起搏器）那样要求绝对保证。帧率掉到 55fps 可以接受，帧率掉到 15fps 玩家会感知到。引擎的所有优化工作——批次合并、剔除、LOD——都是为了满足这个软实时约束。

**Interactive（交互式）**：系统必须实时响应用户输入。这决定了引擎需要一个**主循环（Game Loop）**，而不是批处理系统。

**Agent-based（基于智能体）**：游戏世界由大量独立实体（角色、子弹、道具）组成，每个实体都有自己的状态和行为。这直接解释了为什么引擎需要**对象模型（Object Model）**——Unity 的 GameObject + Component、Unreal 的 AActor + UActorComponent 都是对这个需求的回应。

**Computer simulation（计算机模拟）**：游戏世界是对真实或虚构世界的**数学近似**。物理引擎不追求精确（那是工程仿真），而是追求"看起来对"的近似。Verlet 积分代替精确积分，刚体碰撞用冲量法而非精确求解——这些都是有意识的近似，是游戏引擎和科学计算软件的根本区别。

理解了这个定义，你就理解了为什么引擎要这样设计，而不是那样设计。

---

## 引擎 vs 游戏：最模糊的边界

Gregory 提出了一个让很多人困惑的问题：引擎在哪里结束，游戏在哪里开始？

> "The line between a game and its engine is often blurry. Some engines make a reasonably clear distinction, while others make almost no attempt to separate the two."

他给出了一个关键判断标准：

> "Arguably a data-driven architecture is what differentiates a game engine from a piece of software that is a game but not an engine. When a game contains hard-coded logic or game rules, or employs special-case code to render specific types of game objects, it becomes difficult or impossible to reuse that software to make a different game."

**数据驱动（Data-driven）**是引擎的本质特征。

举个具体例子。假设你写了一个函数：

```csharp
// 不是引擎——游戏逻辑硬编码在渲染代码里
void RenderOrc(Orc orc) {
    DrawMesh(orc.mesh, orc.greenSkinMaterial);
    DrawMesh(orc.weapon, orc.rustyIronMaterial);
    if (orc.isDead) {
        PlayAnimation("orc_death_animation");
    }
}
```

这是游戏代码，不是引擎代码。它硬编码了"兽人"的概念。

而引擎代码是这样的：

```csharp
// 引擎代码——通用，不知道"兽人"是什么
void RenderEntity(Entity entity) {
    foreach (var meshRenderer in entity.GetComponents<MeshRenderer>()) {
        DrawMesh(meshRenderer.mesh, meshRenderer.material);
    }
    
    var animator = entity.GetComponent<Animator>();
    if (animator != null && animator.HasParameter("IsDead")) {
        animator.SetBool("IsDead", entity.IsDead);
    }
}
```

第二段代码对兽人、骑士、龙、NPC、道具都适用——因为它通过数据（Component 配置）而非代码来定义行为。

Unity 的整个设计哲学就是这个：**GameObject 本身是空的容器，所有行为由 Component 的数据配置决定**。

---

## Unity vs Unreal：两种不同的引擎哲学

理解了引擎的本质，就能理解 Unity 和 Unreal 的设计分歧——这不是"谁更好"的问题，而是两种不同哲学的体现。

### Unity 的哲学：引擎是工具，游戏是应用

Unity 的核心设计原则是**极致的灵活性**。

```csharp
// Unity 的 GameObject 是纯粹的空壳
var go = new GameObject("Enemy");

// 没有任何内置行为
// Transform 是 Unity 强制的最小 Component
Debug.Log(go.GetComponents<Component>().Length); // 输出: 1 (只有 Transform)

// 所有行为通过 Component 组合
go.AddComponent<MeshRenderer>();    // 添加渲染
go.AddComponent<BoxCollider>();     // 添加碰撞
go.AddComponent<EnemyAI>();         // 添加 AI 行为
go.AddComponent<AudioSource>();     // 添加音频

// 现在这个 GameObject 是"敌人"——但这个概念由数据定义，不由继承定义
```

Unity 的这种设计来自组合（Composition）优于继承（Inheritance）的软件工程原则。你不需要继承一个 `Enemy` 基类，只需要组合出你想要的行为。

**优势**：
- 极度灵活，任何对象可以在运行时添加/删除 Component
- 易于原型开发，拖拽 Component 即可
- 非程序员（设计师）也能在 Inspector 中配置行为

**代价**：
- 大量 Component 之间的 `GetComponent<T>()` 调用有性能开销
- 每帧调用所有 MonoBehaviour 的 `Update()` 是 O(n) 遍历
- 内存布局（AoS，Array of Structures）对 CPU Cache 不友好

这就是为什么 Unity 推出了 DOTS（Data-Oriented Technology Stack）——它是在承认传统 GameObject 架构的局限性。

### Unreal 的哲学：引擎是框架，游戏是引擎的子集

Unreal 的核心设计原则是**功能完整性**。

```cpp
// Unreal 的 AActor 自带大量内置功能
class AEnemy : public AActor {
public:
    // 内置 Tick 机制
    virtual void Tick(float DeltaTime) override;
    
    // 内置网络复制（Replication）
    UPROPERTY(Replicated)
    float Health;
    
    // 内置序列化（SaveGame/LoadGame）
    UPROPERTY(SaveGame)
    int32 KillCount;
    
    // 内置 Actor 生命周期
    virtual void BeginPlay() override;
    virtual void EndPlay(EEndPlayReason::Type EndPlayReason) override;
};

// AActor 自带的功能：
// - Tick（每帧更新）✓
// - 网络复制 ✓
// - 序列化 ✓
// - Actor 层级（Attach/Detach）✓
// - Tag 系统 ✓
// - 可见性控制 ✓
// 在 Unity 中这些都需要额外的 Component！
```

**优势**：
- 开箱即用的网络复制、序列化、GC
- UClass/UObject 反射系统支持蓝图可视化编程
- 更接近"生产就绪"的状态

**代价**：
- 编译时间极长（UHT 生成反射代码 + C++ 编译）
- 学习曲线陡峭
- 灵活性不如 Unity（基类太"重"）

### 关键差异对比

| 维度 | Unity | Unreal |
|------|-------|--------|
| 对象模型 | GameObject（空壳）+ Component | AActor（功能丰富）+ UActorComponent |
| 脚本语言 | C#（托管，GC） | C++（原生）+ Blueprint（可视化） |
| 反射系统 | C# CLR 反射 | UHT 生成（编译时） |
| 网络 | 第三方（Netcode/Mirror） | 内置（深度集成） |
| 渲染管线 | Built-in / URP / HDRP（多路径） | 延迟渲染为主（单路径） |
| 移动端 | 优先支持，优化工具完善 | 可用但移动端专项支持弱于 Unity |
| 开源程度 | 不开源 | C++ 源码完全开放 |

---

## Runtime Engine Architecture：引擎的完整地图

Gregory 在 §1.6 给出了一张完整的运行时引擎架构图。这张图是理解整本书的导航地图。

层次从下到上：

```
Target Hardware
    ↓
Device Drivers
    ↓
OS + Graphics API (DirectX 12 / Metal / Vulkan)
    ↓
Third-Party SDKs (PhysX, FMOD, Lua)
    ↓
Platform Independence Layer (PAL)
    ↓
Core Systems
    ├── Memory Management
    ├── Math Library
    ├── Data Structures & Algorithms
    └── Logging & Profiling
    ↓
Resource Manager
    ├── Asset Pipeline
    ├── Streaming
    └── GPU Upload
    ↓
Rendering Engine
    ├── Visibility System
    ├── LOD System
    ├── Material System
    └── Lighting & Shadows
    ↓
Animation System
    ├── State Machine
    ├── IK
    └── Skinning
    ↓
Physics & Collision
    ├── Broad Phase
    ├── Narrow Phase
    └── Solver
    ↓
Audio System
    ├── Mixer
    ├── 3D Spatialization
    └── Streaming
    ↓
Gameplay Foundation
    ├── Game Object Model
    ├── Event System
    └── Scripting
    ↓
Game-Specific Systems
    ├── Weapons System
    ├── Level System
    └── Objectives System
    ↓
Game Code (Your Code)
```

**关键原则**：上层依赖下层，下层不依赖上层。违反这个原则会导致循环依赖——系统A依赖系统B，系统B依赖系统A——从此代码无法独立测试、无法复用、无法重构。

Unity 的架构大体遵循这个层次。你的 `MonoBehaviour` 是最顶层，它调用 `Physics.Raycast()`（物理层），后者调用 PhysX（第三方 SDK），后者调用 OS 的内存分配和 CPU 指令。你永远不会跳层调用——这是引擎封装的价值。

---

## 性能视角：为什么 Unity 的 Component 系统有瓶颈

理解了引擎架构，就能理解一些 Unity 开发者日常困惑的性能问题。

```csharp
// Unity 每帧的更新流程（简化）
void EngineUpdate() {
    // 1. 遍历所有 GameObject
    foreach (var go in AllGameObjects) {
        // 2. 对每个 GameObject，遍历其所有 Component
        foreach (var component in go.Components) {
            // 3. 调用 MonoBehaviour 的 Update()
            if (component is MonoBehaviour mb && mb.enabled) {
                mb.Update();
            }
        }
    }
}
```

这个流程的问题：
- **内存不连续**：GameObject 和 Component 散布在堆内存各处，遍历时 CPU Cache Miss 率高
- **虚函数开销**：每次 `Update()` 调用都是虚函数，有间接跳转开销
- **无法 SIMD**：数据不连续，无法用 SIMD 指令批量处理

而 Unity DOTS/ECS 的方案：

```csharp
// DOTS ECS：按 Component 类型组织内存，而不是按 Entity 组织
// 所有 Transform 连续存储
// 所有 Velocity 连续存储
// System 批量处理，SIMD 友好

[BurstCompile]
public partial struct MoveSystem : ISystem {
    public void OnUpdate(ref SystemState state) {
        // 内存连续，Burst 编译器自动 SIMD
        foreach (var (transform, velocity) in 
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<VelocityComponent>>()) {
            transform.ValueRW.Position += velocity.ValueRO.Value * SystemAPI.Time.DeltaTime;
        }
    }
}
```

DOTS 的速度可以比传统 MonoBehaviour 快 10-100 倍——不是因为 C# 更快了，而是因为**内存访问模式对 CPU Cache 更友好**。

Gregory 在 Ch4（Parallelism）会深入讲 Cache 的重要性，这里先有个概念。

---

## 一个值得深思的问题：引擎到底是谁的

Gregory 在 §1.3 提到了一个微妙的观点：

> "No studio makes a perfectly clear separation between the game and the engine, which is understandable considering that the definitions of these two components often shift as the game's design solidifies."

引擎和游戏的边界是动态的。在开发《The Last of Us》时，Naughty Dog 不断地在"这是引擎功能"和"这是游戏功能"之间移动边界——直到游戏发布，这个边界才算稳定。

对于 Unity 开发者来说，这意味着：你的 MonoBehaviour 可能今天是"游戏代码"，但如果它足够通用，明天就可以成为"引擎级别"的可复用 Component。

好的工程师的工作，就是不断把"游戏代码"提炼成"引擎代码"——让可复用的部分越来越多，让项目特定的代码越来越薄。这是一种持续重构的过程，也是区分高级开发者和普通开发者的分水岭。

---

## 延伸阅读

- **GEA 原文** §1.1-1.6 — Jason Gregory（本章全部内容）
- **Game Programming Patterns** — Robert Nystrom（引擎常用设计模式，免费在线版）
- **Unity DOTS Documentation** — Unity 官方（数据导向设计的 Unity 实现）
- **Unreal Engine Source Code** — GitHub（Epic Games，C++ 源码完全开放）

---

## 🎯 今日测验

**Q1（概念）：** Gregory 说"数据驱动架构是区分游戏引擎与'只是一个游戏的软件'的关键特征"。请用你自己项目中的一个具体例子，说明某段代码是"游戏代码"还是"引擎代码"，以及怎样改造能让它成为"引擎级别"的可复用代码。

**Q2（应用）：** Unity 的传统 GameObject + MonoBehaviour 架构和 DOTS/ECS 架构，在内存布局上有什么本质区别？如果你有一个场景里有 10000 个敌人每帧需要更新位置，两种架构在 CPU Cache 利用上会有什么不同表现？

**Q3（品味）：** Naughty Dog 选择自研引擎而不是使用 Unreal Engine，Unity 选择用 C# 而 Unreal 用 C++。这些选择背后是什么样的 trade-off 逻辑？如果你是一个 10 人的独立团队，做一款移动端动作游戏，你会做什么选择，理由是什么？

> 回复本条消息作答，你的回答会影响明天 Day 2 的内容深度和方向。

---

📅 **明天 Day 2：** 引擎演化史 — 从 id Tech 到 Unreal Engine 5
📊 **进度：** Day 1/30 | Phase 1: 引擎基础
