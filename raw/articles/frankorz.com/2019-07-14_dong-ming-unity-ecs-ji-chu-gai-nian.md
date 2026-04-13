---
title: 洞明 Unity ECS 基础概念
url: http://frankorz.com/2019/07/14/clarify-ecs-basic-concept/
author: 文章作者 猫冬
published: '2019-07-14'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

虽然网络上已经有不少 ECS 文档的汉化，但自己读官方文档的时候也会产生不少疑问，为此通过查询各种资料，写下本文。

本文从 ECS 官方文档出发，加之内存布局结构的讲解，力求读者能够和博主一起吃透 ECS 中的基本概念。同时建议读者可以先读读我的上一篇博文[《Unity DOTS 走马观花》](http://frankorz.com/2019/05/07/simple-talk-unity-dots/#Entity-Component-System)的 ECS 部分，本文不再复述前文已经提到过的相关概念。

# ECS 与 Job System

我认为有必要重申其两者的关系。

- Job System 能帮我们方便地写出线程安全的多线程代码，其中每个任务单元称为 Job。
- ECS，又称实体组件系统。与传统的面向对象编程相比，ECS 是一种基于数据设计的编程模式。
[前文](http://frankorz.com/2019/05/07/simple-talk-unity-dots/#Entity-Component-System)从内存结构分析了 OOP 模式的缺点，也提到了 ECS 是怎么样基于数据的设计内存结构的。

Job System 是 Unity 自带的库，而要使用 ECS 我们需要从 Package Manager 中安装 “Entities” 预览包。这两者虽说完全是两种东西，但是他们能很好地相辅相成：ECS 保证数据线性地排列在内存中，这样通过更高效的数据读取，能有效提升 Job 的执行速度，同时也给了 Burst 编译器更多优化的机会。

# Entities（实体）

在 `World`

中， `EntityManager`

管理所有实体和组件。

当你需要创建实体和为其添加组件的时候， `EntityManager`

会一直跟踪所有独立的组件组合（也就是原型 Archetype）。

## 创建实体

最简单的方法就是在编辑器直接挂一个 `ConvertToEntity`

脚本，在运行时中把 GameObject 转成实体。

![在编辑器中挂脚本，GameObject 会在运行时中转成实体](../../assets/db10a63be0949060.png)


在编辑器中挂脚本，GameObject 会在运行时中转成实体

脚本中，你也可以创建系统（System）并在一个 Job 中创建多个实体，也可以通过 `EntityManager.CreateEntity`

方法来一次生成大量 Entity。

我们可以通过下面四种方法来创建一个实体：

- 用
[ComponentType](https://docs.unity3d.com/Packages/com.unity.entities@0.0/api/Unity.Entities.ComponentType.html)数组创建一个带组件的实体 - 用
[EntityArchetype](https://docs.unity3d.com/Packages/com.unity.entities@0.0/api/Unity.Entities.EntityArchetype.html)创建一个带组件的实体 - 用
[Instantiate](https://docs.unity3d.com/Packages/com.unity.entities@0.0/api/Unity.Entities.EntityManager.html#Unity_Entities_EntityManager_Instantiate_Unity_Entities_Entity_)复制一个已存在的实体和其当前的数据， - 创建一个空的实体然后再为其添加组件

也可以通过下面的方法一次性创建多个实体：

- 用
[CreateEntity](https://docs.unity3d.com/Packages/com.unity.entities@0.0/api/Unity.Entities.EntityManager.html#Unity_Entities_EntityManager_CreateEntity)来创建相同原型（archetype）的实体并填满一个 NativeArray （要多少实体就提前设定好 NativeArray 的长度） - 用
[Instantiate](https://docs.unity3d.com/Packages/com.unity.entities@0.0/api/Unity.Entities.EntityManager.html#Unity_Entities_EntityManager_Instantiate_Unity_Entities_Entity_)来复制一个已存在的实体并填满一个 NativeArray - 用
[CreateChunk](https://docs.unity3d.com/Packages/com.unity.entities@0.0/api/Unity.Entities.EntityManager.html#Unity_Entities_EntityManager_CreateChunk_)来显式创建内存块（Chunks），并且填入自定数量的给定原型的实体

## 增加和移除组件

实体被创建之后，我们可以增加和移除其组件。当我们这样做的时候，相关联的原型（Archetype）将会被改变， `EntityManager`

也需要改变内存布局，将受影响的数据移到新的内存块（new Chunk of memory），同时也会压缩原来内存块中的组件数组。

对实体的修改会带来内存结构的改变。

实体的修改包括：

- 增加和移除组件
- 改变
`SharedComponentData`

的值 - 增加和删除实体

这些操作都不能放到 Job 中执行，因为这些都会改变内存中的数据结构。因此我们需要用到命令（Commands）来保存这些操作，将这些操作存到 `EntityCommandBuffer`

中，然后在 Job 完成后再依次执行 `EntityCommandBuffer`

中储存的操作。

# World（世界）

每一个 `World`

包含一个 `EntityManager`

和一系列的 `ComponentSystem`

。一个世界中的实体、原型、系统等都不能被另外一个世界访问到。你可以创建很多 `World`

，例如通常我们会使用或创建一个负责主要逻辑运算的 simulation `World`

和负责图形渲染的 rendering `World`

或 presentation `World`

。

当我们点击运行按钮进入 **Play Mode** 时，Unity 会默认创建一个 `World`

，并且增加项目中所有可用的 `ComponentSystem`

。我们也可以关闭默认的 `World`

从而自己创建一个。

**Default World creation code**(see file:*Packages/com.unity.entities/Unity.Entities.Hybrid/Injection/DefaultWorldInitialization.cs*)**Automatic bootstrap entry point**(see file:*Packages/com.unity.entities/Unity.Entities.Hybrid/Injection/AutomaticWorldBootstrap.cs*)

# Components（组件）

ECS 中的组件是一种结构，可以通过实现下列接口来实现：

- IComponentData
- ISharedComponentData
- ISystemStateComponentData
- ISharedSystemStateComponentData

`EntityManager`

会组织所有实体中独立的组件组合成不同的**原型（Archetypes）**，还会将拥有同样原型的所有实体的组件（数据）储存到一起，都放到同一个**内存块（Chunks）**中。

如果你为一个实体新增了一个组件，那么其原型就改变了，实体的数据也需要从原来的内存块移到新的内存块，因为只有相同原型的实体数据才会放到相同的内存块中。

一个原型由很多个内存块组成，这些内存块中存的都是拥有相同原型的实体。

![](../../assets/2aab696bea7582bb.png)


## General Purpose Component（普通用途组件）

这里指的是最普通的组件，可以通过实现 `IComponentData`

接口来创建。

`IComponentData`

不存储行为，只储存数据。`IComponentData`

还是一个结构体（Struct）而不是一个类（Class），这意味着被复制时默认是通过值而不是通过引用。

通常我们会用下面的**模式**来修改组件数据：

1 | var transform = group.transform[index]; // Read |

`IComponentData`

结构不包含托管对象（managed objects）的引用，所有`IComponentData`

被存在无垃圾回收的[块内存（chunk memory）](https://docs.unity3d.com/Packages/com.unity.entities@0.0/manual/chunk_iteration.html)中。

你可能还听过一种组件是不包含数据、只用来标记的“Tag”组件（Tag component），其用途也很广，例如我们可以轻易地给实体加标记来区分玩家和敌人，这样系统中能更容易通过组件的类型来筛选我们想要的实体。如果我们给一个内存块（Chunk）中的所有实体都添加"Tag“组件的话，只有内存块中对应的原型会修改，不添加数据，因此官方也推荐利用好”Tag“组件。

See file: /Packages/com.unity.entities/Unity.Entities/IComponentData.cs.

## Shared components（共享组件）

Shared components 是一种特殊的组件，你可以把某些特殊的需要共享的值放到 shared component 中，从而在实体中与其他组件划分开。例如有时候我们的实体需要共享一套材质，我们可以为需要共享的材质创建 `Rendering.RenderMesh`

，再放到 shared components 中。原型中也可以定义 shared components，这一点和其他组件是一样的。

1 | [ ] |

当你为一个实体添加一个 shared components 时， `EntityManager`

会把所有带有同样 shared components 的实体放到一个同样的内存块中（Chunks）。shared components 允许我们的系统去一并处理相似的（有同样 shared components 的）实体。

### 内存结构

![](../../assets/4ad22297574505f1.png)


每个内存块（Chunk）会有一个存放 shared components 索引的数组。这句话包含了几个要点：

- 对于实体来说，有同样
`SharedComponentData`

的实体会被一起放到同样的内存块（Chunk）中。 - 如果我们有两个存储在同样的内存块中的两个实体，它们有同样的
`SharedComponentData`

类型和值。我们修改其中一个实体的`SharedComponentData`

的值，这样会导致这个实体会被移动到一个新的内存块中，因为一个内存块共享同一个数组的`SharedComponentData`

索引。事实上，从一个实体中增加或者移除一个组件，或者改变 shared components 的值都会导致这种操作的发生。 - 其索引存储在内存块而非实体中，因此
`SharedComponentData`

对实体来说是低开销的。 - 因为内存块只需要存其索引，
`SharedComponentData`

的内存消耗几乎可以忽略不计。

因为上面的第二个要点，我们不能滥用 shared components。滥用 shared components 将让 Unity 不能利用好内存块（Chunk），因此我们要避免添加不必要的数据或修改数据到 shared components 中。我们可以通过 Entity Debugger 来监测内存块的利用。

![](../../assets/30539fcc1be980de.png)


拿上一段 RenderMesh 的例子来说，共享材质会更有效率，因为 shared components 有其自己的 `manager`

和哈希表。其中 `manager`

带有一个存储 shared components 数据的自由列表（[freelist](https://zh.wikipedia.org/wiki/%E8%87%AA%E7%94%B1%E8%A1%A8)），哈希表可以快速地找到相应的值。内存块里面存的是索引数组，需要找数据的时候就会从 Shared Component Manager 中找。

### 其他要点

`EntityQuery`

可以迭代所有拥有相同`SharedComponentData`

的实体- 我们可以用
`EntityQuery.SetFilter()`

来迭代所有拥有某个特定`SharedComponentData`

的实体。这种操作开销十分低，因为`SetFilter`

内部筛选的只是 int 的索引。前面说了每个内存块都有一个`SharedComponentData`

索引数组，因此对于每个内存块来说，筛选（filtering）的消耗都是可以忽略不计的。 - 怎么样获取
`SharedComponentData`

的值呢？`EntityManager.GetAllUniqueSharedComponentData<T>`

可以得到在存活的实体中（alive entities）的所有的泛型 T 类型的`SharedComponentData`

值，结果以参数中的列表返回，你也可以通过其重载的方法获得所有值的索引。其他获取值的方法可以参考 /Packages/com.unity.entities/Unity.Entities/EntityManagerAccessComponentData.cs。 `SharedComponentData`

是自动引用计数的，例如在没有任何内存块拥有某个`SharedComponentData`

索引的时候，引用计数会置零，从而知道要删除`SharedComponentData`

的数据 。这一点就能看出其在 ECS 的世界中是非常独特的存在，想要深入了解可以看这篇文章[《Everything about ISharedComponentData》](https://gametorrahod.com/everything-about-isharedcomponentdata/)。`SharedComponentData`

应该尽量不去更改，因为更改`SharedComponentData`

会导致实体的组件数据需要复制到其他的内存块中。

你也可以读读这篇更深入的文章[《Everything about ISharedComponentData》](https://gametorrahod.com/everything-about-isharedcomponentdata/)。

## System state components（系统状态组件）

`SystemStateComponentData`

允许你跟踪系统（System）的资源，并允许你合适地创建和删除某些资源，这些过程中不依赖独立的回调（individual callback）。

假设有一个网络同步 System State，其监控一个 Component A 的同步，则我只需要定义一个 SystemStateComponent SA。当 Entity [有 A，无 SA] 时，表示 A 刚添加，此时添加 SA。等到 Entity [无 A，有 SA] 时,表示 A 被删除（尝试销毁Entity 时也会删除 A）。


[《浅入浅出Unity ECS》]BenzzZX

`SystemStateComponentData`

和 `SystemStateSharedComponentData`

这两个类型与 `ComponentData`

和 `SharedComponentData`

十分相似，不同的是前者两个类型都是系统级别的，不会在实体删除的时候被删除。

### Motivation（诱因）

System state components 有这样特殊的行为，是因为：

- 系统可能需要保持一个基于
`ComponentData`

的内部状态。例如已经被分配的资源。 - 系统需要通过值来管理这些状态，也需要管理其他系统所造成的状态改变。例如在组件中的值改变的时候，或者在相关组件被添加或者被删除的时候。
- “没有回调”是 ECS 设计规则的重要元素。

### Concept（概念）

`SystemStateComponentData`

普遍用法是镜像一个用户组件，并提供内部状态。

上面引用的网络同步的例子中，A 就是用户分配的 `ComponentData`

，SA 就是系统分配的 `SystemComponentData`

。

下面以 FooComponent （`ComponentData`

）和 FooStateComponent（`SystemComponentData`

）做主要用途的示例。前两个用途已经在前面的网络同步例子中呈现过。

#### 检测组件的添加

如果用户添加 FooComponent 时，FooStateComponent 还不存在。FooSystem 会在 update 中查询，如果实体只有 FooComponent 而没有 FooStateComponent,，则可以判断这个实体是新添加的。这时候 FooSystem 会加上 FooStateComponent 组件和其他需要的内部状态。

#### 检测组件的删除

如果用户删除 FooComponent 后，FooStateComponent 仍然存在。FooSystem 会在 update 中查询，如果实体没有 FooComponent 而有 FooStateComponent,，则可以判断 FooComponent 已经被删除了。这时候 FooSystem 会给删除 FooStateComponent 组件和修改其他需要的内部状态。

#### 监测实体的删除

通常 `DestroyEntity`

这个方法可以用来：

- 找到所有由某个实体 ID 标记的所有组件
- 删除那些组件
- 回收实体 ID 以作重用

然而，`DestroyEntity`

无法删除 `SystemStateComponentData`

。

在你删除实体时，`EntityManager`

**不会**移除任何 system state components，在它们没被删除的时候，`EntityManager`

也不会回收其实体的 ID 。这样允许系统（System）在一个实体被删除的时候，去整理内部的状态（internal state），也能清理关联着实体 ID 的相关的资源和状态。实体 ID 只会在所有 `SystemStateComponentData`

被删除的时候才被重用。

## Dynamic Buffers（动态缓冲）

`DynamicBuffer`

也是组件的一种类型，它能把一个变量内存空间大小的弹性的缓冲（variable-sized, “stretchy” buffer）和一个实体关联起来。它内部存储着一定数量的元素，但如果内部所占内存空间太大，会额外划分一个堆内存（heap memory）来存储。

动态缓冲的内存管理是全自动的。与 `DynamicBuffer`

关联的内存由 `EntityManager`

来管理，这样当`DynamicBuffer`

组件被删除的时候，所关联的堆内存空间也会自动释放掉。

上面的解释可能略显苍白，实际上 `DynamicBuffer`

可以看成一个有默认大小的数组，其行为和性能都和 `NativeArray`

（在 ECS 中常用的无 GC 容器类型）差不多，但是存储数据超过默认大小也没关系，上文提到了会创建一个堆内存来存储多的数据。`DynamicBuffer`

可以通过 `ToNativeArray`

转成 `NativeArray`

类型，其中只是把指针重新指向缓冲，不会复制数据。

[【Unity】ECSで配列を格納する Dynamic Buffers](http://tsubakit1.hateblo.jp/entry/2018/11/07/234502) 这篇文章中，作者用`DynamicBuffer`

来储存临近的圆柱体实体，从而更方便地与这些实体交互。

### 定义缓冲

1 | // 8 指的是缓冲中默认元素的数量，例如这例子中存的是 Integer 类型 |

可能有点奇怪，我们要定义缓冲中元素的结构而不是 `Buffer`

缓冲本身，其实这样在 ECS 中有两个好处：

- 对于
`float3`

或者其他常见的值类型来说，这样能支持多种`DynamicBuffer`

。我们可以重用已有的缓冲元素的结构，来定义其他的`Buffers`

。 - 我们可以将
`Buffer`

的元素类型包含在`EntityArchetypes`

中，这样它会表现得像拥有一个组件一样。例如用`AddBuffer()`

方法，可以通过`entityManager.AddBuffer<MyBufferElement>(entity);`

来添加缓冲。

# Systems（系统）

系统负责将组件数据从一个状态（state）通过逻辑处理到下一个状态。例如系统可以根据帧间隔和实体的速度，在当前帧更新所有移动实体的位置。

世界初始化后提供了三个系统组（system groups），分别是 initialization、simulation 和 presentation，它们会按顺序在每帧中执行。

系统组的概念会在下文提到。

## ComponentSystem（组件系统）

`ComponentSystem`

通常指 ECS 实体组件系统中最基本的概念 System，它提供要执行的操作给实体。

`ComponentSystem`

不能包含实体的数据。从传统的开发模式来看，它与旧的 Component 类有点相似，不过 `ComponentSystem`

**只包含方法**。

一个 `ComponentSystem`

负责更新所有**匹配组件类型**的实体。例如：系统可以通过条件过滤来获得所有拥有 Player 标记（Tag）和位置（Translation）的实体，再对获得的一系列 Player 实体进行处理。其中这种条件过滤由 [EntityQuery](https://docs.unity3d.com/Packages/com.unity.entities@0.0/manual/component_group.html) 结构定义。

![](../../assets/b72255ee3631fd43.png)


要注意的是，`ComponentSystem`

只在**主线程**中执行。

我们可以通过继承 `ComponentSystem`

抽象类来定义我们的系统。

See file: /Packages/com.unity.entities/Unity.Entities/ComponentSystem.cs.

## JobComponentSystem（任务组件系统）

前文提到了 ECS 能很好的和 JobSystem 一起合作，那么这个类型就是一个很好的例子。`ComponentSystem`

只在**主线程**中执行，而 `JobComponentSystem`

则能在**多线程**中执行，更能利用多核的优势。

![](../../assets/b79b9914ba918a98.png)


### 自动化的 Job 依赖管理

`JobComponentSystem`

能帮我们自动管理依赖。原理很简单，来自不同系统的 Job 可以并行地读取相同类型的 `IComponentData`

。如果其中一个 Job 正在写（write）数据，那么所有的 Job 就不能并行地执行，而是设定它们的依赖来安排执行顺序。

1 | public class RotationSpeedSystem : JobComponentSystem |

### 怎么运行的？

所有 Jobs 和系统会声明它们会读/写哪些组件类型（ComponentTypes）。JobComponentSystem 返回的 [JobHandle](https://docs.unity3d.com/ScriptReference/Unity.Jobs.JobHandle.html) 依赖句柄会自动注册到 `EntityManager`

中，以及所有包含读或写（reading or writing）信息的类型中。

这样如果一个系统对 Component A 进行写操作而之后另一个系统会对其进行读操作， `JobComponentSystem`

会查询读取（reading）的类型列表，然后传给你一个依赖。依赖包含第一个系统返回的 JobHandle，也就是包含“一个系统对 Component A 进行写操作”这个依赖，并将其作为第二个系统的参数传入。

`JobComponentSystem`

简单地按照需求维护一个依赖链，这样不会对主线程造成影响。但是如果一个非 Job 的 `ComponentSystem`

要存取（access）相同的数据会怎么样呢？因为所有的存取都是声明好的，因此对于所有 `ComponentSystem`

需要进行存取的组件类型（component type）相关联的 Jobs，`ComponentSystem`

都会先自动完成这些相关的 Jobs，再在 `OnUpdate`

中调用依赖。

### 依赖管理是保守的（conservative）和确定性的（deterministic）

依赖管理是保守的。 `ComponentSystem`

只是简单的跟踪所有使用的 `EntityQuery`

，然后基于 `EntityQuery`

存储需要读或写的类型。

当在一个系统中分发多个 Jobs 的时候，依赖必须被发送到所有 Jobs 中，即使不同的 Jobs 可能需要更少的依赖。如果这里被证明有性能问题，那最好的解决方法是将系统一分为二。

依赖管理的手段也是保守的。它通过提供一个非常简单的 API 来允许确定性和正确的行为。

### Sync points（同步点）

![](../../assets/8da6ed530a69cac2.png)


所有结构性的变化都有确切的同步点（hard sync points）。 `CreateEntity`

、`Instantiate`

、 `Destroy`

、 `AddComponent`

、 `RemoveComponent`

、`SetSharedComponentData`

都有一个确切的同步点。这代表所有通过 `JobComponentSystem`

排期的 Jobs 都会在创建实体之前自动完成。

例如，在一帧中间的 `EntityManager.CreateEntity`

可能带来较大的**停滞**，因为所有在世界中的提前排期好的 Jobs 都需要完成。

如果要在游戏中避免上面提到的停滞，可以使用 `EntityCommandBuffer`

。

### Multiple Worlds（多个世界）

所有世界（World）都有自己的 `EntityManager`

，因此 `JobHandle`

依赖句柄的集合都是分开的。一个世界中的确切的同步点（hard sync points）不会影响另外一个世界。因此，对于流式传输和程序化生成的场景，最后在一个世界中创建实体然后移到另一个世界作为一个事务（transaction）并在帧的开始执行。

对于上面的问题可以参考 [ExclusiveEntityTransaction](https://docs.unity3d.com/Packages/com.unity.entities@0.0/manual/exclusive_entity_transaction.html) 和 System update order。

## Entity Command Buffer（实体命令缓冲）

`EntityCommandBuffer`

解决了两个重要问题：

- 在 Job 中无法访问
`EntityManager`

，因此不能通过它来管理实体。 - 当你使用
`EntityManager`

时（例如创建一个实体），你会使所有已被注入的数组和`EntityQuery`

无效。（这里注入的概念大概是指：系统中可以设定某个过滤条件，给过滤条件加上`[inject]`

后，系统会在启动时为这个属性根据条件注入数据，这样就能得到我们想要的数据。会无效是因为你修改了实体数据，那么结果可能会发生改变。）

`EntityCommandBuffer`

的抽象允许我们去把需要对数据的更改（changes）排好队，这个更改可以来自主线程或者 Jobs，这样数据可以晚一点在主线程接受更改，从而将其和获取数据分离开来。

我们有两种方法来使用 `EntityCommandBuffer`

：

- 在主线程 update 的
`ComponentSystem`

子类有一个`PostUpdateCommands`

（其本身是一个`EntityCommandBuffer`

） 可以用，我们只要简单地把变化按顺序放进去即可。在系统的`Update`

调用之后，它会立刻自动在世界（World）中进行所有数据更改。这样可以防止数组数据无效，API 也和`EntityManager`

很相似。

1 | PostUpdateCommands.CreateEntity(TwoStickBootstrap.BasicEnemyArchetype); |

- 对于 Jobs 来说，我们必须从主线程的
`EntityCommandBufferSystem`

中请求一个`EntityCommandBuffer`

，再传到 Job 里面让其调用。 每当`EntityCommandBufferSystem`

进行 update，命令缓冲都会在主线程中重新把更改按创建的顺序执行一遍。这样允许我们集中进行内存管理，也保证了创建的实体和组件的确定性。

### Entity Command Buffer Systems（实体命令缓冲系统）

在一个系统组中，有一个 Entity Command Buffer Systems 运行在所有系统组之前，还有一个运行在所有系统组之后。比较建议的是我们可以用已存在的命令缓存系统（command buffer system）之一，而不用创建自己的，这样可以最小化同步点（sync point）。

### 在 ParallelFor jobs 中使用 EntityCommandBuffers

在 [ParallelFor jobs](https://docs.unity3d.com/Manual/JobSystemParallelForJobs.html) 使用 `EntityCommandBuffer`

存 `EntityManager`

的命令（command）时， `EntityCommandBuffer.Concurrent`

接口能保证线程安全和确定性的回放（deterministic playback）。

1 | // See file: /Packages/com.unity.entities/Unity.Entities/EntityCommandBuffer.cs. |

`EntityCommandBuffer.Concurrent`

的公共方法都会接受一个 `jobIndex`

参数，这样能回放（playback）已经按顺序保存好的命令。 `jobIndex`

作为 ID 必须在每个 Job 中唯一。从性能考虑，`jobIndex`

必须是传进 `IJobParallelFor.Execute()`

的不断增长的 `index`

。除非你真的知道你传的是啥，否则最安全的做法就是把参数中的 `index`

作为 `jobIndex`

传进去。用其他 `jobIndex`

可能会产生正确的结果，但是可能在某些情况下会有严重的性能影响。

1 | namespace Unity.Jobs |

## System Update Order（系统更新顺序）

组件系统组（Component System Groups）其实是为了解决世界（World）中各种 update 的顺序问题。一个系统组中包含了很多需要按照顺序一起 update 的组件系统（component systems），可以来指定它成员系统（member system）的 update 顺序。

和其他系统一样， `ComponentSystemGroup`

也继承自 `ComponentSystemBase`

，因此系统组可以当成一个大的“系统”，里面也用 `OnUpdate()`

函数来更新系统。它也可以被指定更新的顺序（在某个系统的之前或之后更新等，下文会讲），并且也可以嵌入到其他系统组中。

默认情况下， `ComponentSystemGroup`

的 `OnUpdate()`

方法会按照成员系统（member system）的顺序来调用他们的 `Update()`

，如果成员系统也是一个系统组，那么这个系统组也会递归地更新它的成员系统。总体的系统遵循树的深度优先遍历。

1 | // See file: /Packages/com.unity.entities/Unity.Entities/ComponentSystemGroup.cs. |

### System Ordering Attributes（系统顺序属性）

`[UpdateInGroup]`

指定某个系统成为一个`ComponentSystemGroup`

中的成员系统。如果没有用这个属性，这个系统会自动被添加到默认世界（default World）的 SimulationSystemGroup 中。`[UpdateBefore]`

和`[UpdateAfter]`

指定系统相对于其他系统的更新顺序。这两个系统必须在同一个系统组（system group）中，前文说到系统组也可以嵌套，因此只要两个系统身处同一个根系统组即可。- 例子：如果 System A 在 Group A 中、System B 在 Group B 中，而且 Group A 和 Group B 都是 Group C 的成员系统，那么 Group A 和 Group B 的相对顺序也决定着 System A 和 System B 的相对顺序，这时候就不需要明确地用属性标明顺序了。

`[DisableAutoCreation]`

阻止系统从默认的世界初始化中创建或添加到世界中。这时候我们需要显式地创建和更新系统。然而我们也可以把这个系统和它的标记（tag）加到`ComponentSystemGroup`

的更新列表中（update list），这样这个系统会正常地自动更新。

### Default System Groups（默认系统组）

默认世界（default World）包含 `ComponentSystemGroup`

实例的层次结构（hierarchy）。在 Unity Player Loop 中会添加三个根层次（root-level）的系统组。

下图中打开 Entity Debugger，也能看到这三个系统组和其顺序。

![](../../assets/0ceb858e11429240.png)


这三个系统组各司其职， `InitializationSystemGroup`

做初始化工作， `SimulationSystemGroup`

在 Update 中做主要的逻辑运算， `PresentationSystemGroup`

做图形渲染工作。

如果勾选 “Show Full Player Loop” 项，还能看到完整的游戏主循环，以及系统组执行的顺序。

![](../../assets/d42095987367d6fa.png)


下面列表也展示了预定义的系统组和其成员系统：

- InitializationSystemGroup （在游戏循环（Player Loop）的
`Initialization`

层最后 update）- BeginInitializationEntityCommandBufferSystem
- CopyInitialTransformFromGameObjectSystem
- SubSceneLiveLinkSystem
- SubSceneStreamingSystem
- EndInitializationEntityCommandBufferSystem

- SimulationSystemGroup（在游戏循环的
`Update`

层最后 update）- BeginSimulationEntityCommandBufferSystem
- TransformSystemGroup
- EndFrameParentSystem
- CopyTransformFromGameObjectSystem
- EndFrameTRSToLocalToWorldSystem
- EndFrameTRSToLocalToParentSystem
- EndFrameLocalToParentSystem
- CopyTransformToGameObjectSystem

- LateSimulationSystemGroup
- EndSimulationEntityCommandBufferSystem

- PresentationSystemGroup（在游戏循环的
`PreLateUpdate`

层最后 update）- BeginPresentationEntityCommandBufferSystem
- CreateMissingRenderBoundsFromMeshRenderer
- RenderingSystemBootstrap
- RenderBoundsUpdateSystem
- RenderMeshSystem
- LODGroupSystemV1
- LodRequirementsUpdateSystem
- EndPresentationEntityCommandBufferSystem


**P.S. 内容可能在未来有更改**

Multiple Worlds（多个世界）

前文多处提到默认的世界，实际上我们可以创建多个世界。同样的组件系统（component system）的类可以在不同的世界中初始化，而且每个实例都可以处于不同的同步点以不同的速度进行update。

当前没有方法手动更新一个世界中的所有系统，但是我们可以控制哪些系统被哪个世界控制，和它们要被加到哪个现存的世界中。自定义的世界可以通过实现 `ICustomBootstrap`

接口来创建。

### Tips and Best Practices（提示与最佳实践）

- **用
`[UpdateInGroup]`

为你的系统指定一个`ComponentSystemGroup`

系统组。**如果没有用这个属性，这个系统会自动被添加到默认世界（default World）的 SimulationSystemGroup 中。 - **用手动更新循环（manually-ticked）的 ComponentSystemGroups 来 update 在主循环中的系统。**添加
`[DisableAutoCreation]`

阻止系统从默认的世界初始化中创建或添加到世界中。这时候我们可以在主线程中调用`World.GetOrCreateSystem()`

来创建系统，调用`MySystem.Update()`

来 update 系统。如果你有一个系统要在帧中早点或者晚点运行，这种做法能更简单地把系统插到主循环中。 - **尽量使用已存在的
`EntityCommandBufferSystem`

而不是重新添加一个新的。**因为一个`EntityCommandBufferSystem`

代表一个主线程等待子线程完成的同步点（sync point），如果重用一个在每个根系统组（root-level system group）中预定义的 Begin/End 系统，就能节省多个同步点所带来的额外时间间隔（可以回去看同步点小节的示意图，同步点的位置是由最晚执行完的子线程所决定的）。 - **避免放自定义的逻辑到
`ComponentSystemGroup.OnUpdate()`

中。**虽然`ComponentSystemGroup`

功能上和一个组件系统（component system）一样，但是我们应该避免这么做。因为它作为一个系统组，在外面不能马上知道成员系统是否已经执行了 update，因此推荐的做法是只让系统组当一个组（group）来用，而把逻辑放到与其分离的组件系统中，再定好该系统与系统组的相对顺序。

# 最后

自己才刚考完试，所以计划的文章一直拖到现在。ECS 对我而言充满着吸引力，可能有些程序员也会对性能特别执着吧，它就像魔法一样，完全不同的开发模式，还需要我们深入了解内存的结构。尽管 ECS 可能在工作中对我是一种屠龙技，但有些知识啊，学了就已经很开心了~

我的毕业季也到来了，有空的话可能会写写 Demo 把剩下的实践部分补完，当然计划也可能搁浅。不管怎么样，希望本文对 ECS 同好有所帮助，有问题也欢迎在评论指出。