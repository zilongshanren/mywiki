---
title: 云风的 BLOG
url: https://blog.codingnow.com/2019/02/
published: '2019-02-24'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

我们的游戏引擎采用 ECS 框架。最近一年的开发，为 ECS 框架的应用积累了不少经验。我在 blog 上也写过数篇 ECS 相关的东西：

[Lua 下的 ECS 框架](https://blog.codingnow.com/2017/12/lua_ieaae_ecs_oue.html)

[ECS 中的 Entity](https://blog.codingnow.com/2018/11/ecs_entity.html)

最近两个月，结合过去的经验，我们对最初设计的框架做了较大的调整。这主要是源于对框架要解决的事情的更深入的理解，以及在实践过程中针对典型场景总结出来的模式。

首先，我们去掉了 [Lua 实现 ECS 框架的一些技巧](https://blog.codingnow.com/2017/12/lua_ecs_trick.html) 中提到的一些东西：Notify 机制被证明的过于复杂且可以有别的替代方案，这点下面那会展开讲；Component 的方法是多余的，当初加上它更多是因为 OOP 的惯性思维。

最大的改变是对 System 的思考。

System 的存在是为了解耦不同的业务，把引擎要解决的事情分成尽量不相关的部分，并可以用数据驱动其运行流程。

System 不能通过直接调用来传递状态。这是因为 ECS 框架解决的是大批量同类对象做类型的业务，我们希望针对批量对象做 Step A ，全部完成后，再做 Step B 。所以不能在针对单个对象完成 Step A 后立刻调用 Step B 的流程。

System 不能保存中间状态。这也是因为 ECS 框架处理的批量对象而不是单个。

只有加上这些限制，才能做到系统间解耦。但同时也衍生出难题：到底如何控制 System 运作的次序。

最初的设计中，我们对 System 的名字排序，然后针对性的标注有相互次序依赖的 System 的前后次序。可是当 System 数量上去后，这种全局式的描述次序会对使用人造成极大的负担。

由于 System 本身不保存状态，所以我们设计了 Singleton 用于保存 System 的状态，以及充当 System 间数据交换的载体。同时，我为 System 设计了 init 方法，一般用来初始化对应的 Singleton 。这些 Init 方法必须是有序的，这就需要在 System 定义时描述清楚相互依赖关系。利用依赖关系做拓扑排序，不仅仅可以筛选出关联的 System 集合，还可以决定它们的初始化次序。后来，我们发现这些依赖关系不仅可以用于初始化流程，更新过程其实使用这个次序也并非不可。但这也促使我思考，init 流程是否应该是个特殊的东西，还是应该放到一个抽象层中。

对于客户端来说，所有的 System 并非服务于单一事务。例如做渲染的 System 和做物理模拟，动画计算的 System 就是相对独立的事务。它们的更新频率都不相同。还有处理输入设备消息的 System ，如果放在渲染流程中，即每个渲染帧主动去检查是否有输入，看起来也很浪费。

综上所述，我认为我们有必要对 System 分组。不同的组由驱动框架运转的代码编码在不同的地方：例如，外部输入消息产生时，驱动消息处理的 System 组；每个渲染帧驱动渲染更新 System 组；时钟用来驱动每个固定频率的物理帧及动画帧。

其实，我们可以把 System 看成一个无状态的函数对象，它针对某些 Component 处理了某种事务。但它又不仅仅是一个 update 函数，我们还需要定义它们之间的相互依赖关系。从这个角度，init 流程其实只是一个分组而已。这样，一个 System 可以看成是多个函数对象的聚合，每个函数对象处于不同的分组中，而 System 在定义时则描述出和其它 System 的依赖关系，以及对特定 Singleton 的依赖。

Init 这个 System 组只被调用一次，且不应由 World 的创建过程默认驱动，而应该把调用职责交给使用框架的人。这样，使用者就可以灵活的决定在 World 反序列化结束后，所有数据都安置妥当，再驱动 System 的初始化流程。Init 也不再是 ECS 框架的底层概念，而被看成是一个和其它分组平等的概念而已。

Component 的新建和移除也是很多 System 所关心的事情。之前我设计了 Notify 方法来处理它们，但实际用起来并不顺手。我现在认为，应该放在独立的分组里。比如，增加新增对象 System 组和删除对象 System 组。但这会导致对象构建和删除过程的延迟处理，守望先锋的开发团队认为，删除对象可以也最好被延迟处理，但是创建对象最好是及时的。我就这个问题是这样约定的：

创建对象，我们立刻将对象(Entity) 立刻加入 World ，由创建者负责初始化该对象的状态，它有可能被当前帧更新，也可能在下一帧更新；但它和其它对象的交互，是放在下一帧的新建对象 System 组来完成的，例如，该对象被加到物理世界中的过程，就是物理 System 的新建对象函数来添加它；渲染 System 的空间裁剪器也是推迟到下一帧去处理它。

我为新增对象增加了一个 `world:each_new(component_type)`

迭代器，可以迭代出某类 Component 所有新构建的对象，每次迭代后，就自动从新对象集合中移除，也就是说，一个 Component 只会被迭代一次。

对于删除对象，每次调用 world 的 `remove_entity`

删除一个 Entity 或用 `remove_component`

删除 Entity 上的一个 Component ，都可以在后续的 `world:each_removed(component_type)`

中迭代到。和 `each_new`

不同，`each_removed`

可以迭代多次；直到使用者主动调用 `world:clear_removed`

清除。

`world:clear_removed`

其实是一个延迟删除的过程，推荐在每帧固定调用一次。它会清理暂时记住的被清除的 Entity id 集合，还会调用删除的 Component 的析构函数（如果定义了）。


另一个重构的部分是 Component 的类型系统。

我们为 Component 设计一个类型系统主要是为了解决两个主要问题：

作为一个数据驱动框架，我们需要对 World 做序列化和反序列化。编辑器需要持久化编辑出来的 World ，运行时可以从数据文件中读出序列化的结构，序列化必须依赖一个类型系统。

编辑器需要依赖类型系统，通过反射，生成 Component 的编辑控件。


Component 是基于类型系统定义出来的类型的，Component 往往是定义好的类型的组合。

我选择使用 lua 原本的语法来描述类型，目前看起来像这样：

p:type "NAME"
["temp"].a "int" (1)
.b "OBJECT"
[ "private" ].c "id" (0)
.array "int[4]" { 1,2,3,4 }
.any "var" (nil)
.map "int{}" { x = 1, y = 2 }
.color "color"

.name 定义了字段名，紧跟着一个字符串描述了类型，后面可选一个小括号定义出它的默认值。字段名前面还有若干可选的中括号，给该字段加上 tag 。这些 tag 供序列化模块和编辑器做类型反射时参考。