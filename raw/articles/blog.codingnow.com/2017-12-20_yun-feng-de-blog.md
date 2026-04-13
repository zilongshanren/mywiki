---
title: 云风的 BLOG
url: https://blog.codingnow.com/2017/12/
published: '2017-12-20'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

最近在基于 ECS 模型做一些基础工作。实际操作时有一个问题不太明白，那就是涉及对象 (entity) 集合本身的 System 到底应该怎样处理才合适。

仔细阅读了能找到的关于 ECS 的资料，网上能找到的大多是几年前甚至 10 年前的。关于 ECS 的资料都不断地强调一些基本原则：C 里面不可以有方法（纯数据结构），S 里面不可以有状态（纯函数）。从这个角度看，Unity 其实只是一个 EC 系统，而不是 ECS 系统。从 Unity 中寻找关于 System 的设计模式恐怕并不合适。

重看了一遍暴雪在今年 GDC 上的演讲 Overwatch Gameplay Architecture and Netcode —— 这可能是最新公开的采用 ECS 模式的成功（守望先锋）实践了—— 我想我碰到的基础问题应该在里面都有答案。

从绝大多数资料看来，Entity-Component 是对 C++ 中对象模型的一个反思：基于组合，甚至是运行期组合，而不是继承，去合成对象；System 是对 OO 面向对象设计方法的反思：把方法和数据结构分离，不要把一组方法绑定在对象上，即面向对象所主张的，由对象来处理针对它的不同行为；而是由 System 来处理不同的对象聚合。

采用 ECS 模型是因为过去的 OOP 模型耦合度太高，EC/System 的方式可以用来解耦。

把对象 Entity 拆分为更基础的数据结构单元（Component），让 System 直接作用于 Component 集合而不是对象，的确可以对大部分问题解耦。正如 Wikipedia 页面上的举例：假设有一个绘图 System将迭代所有有物理组件和可视组件的 Entity ，它从可视组件中了解 Entity 的怎样绘制，再从物理组件中了解 Entity 该在哪里绘制。而另一个 System 专门处理碰撞检测，它迭代出所有有物理组件的 Entity ，处理他们的碰撞关系，负责产生碰撞事件，但这个 System 不用关心这些 Entity 是怎么绘制的，也不用知道 Entity 具体是什么东西，碰撞本身会有什么后果。再会有另一个 System 负责 Entity 的血量，血量组件记录了 Entity 的 HP 数据，这个 System 处理碰撞事件，知道当子弹击中怪物后，怪物需要扣血。

这样看都很美好，只是，游戏引擎中，往往还有一个性能相关的需求：剔除。一个 System 需要处理的对象往往是全体对象的一个子集。如果子集远小于全体的话，每帧按 Component 类型去迭代整体就有很大的性能开销。

比如，渲染 System 通常会根据摄像机在场景中的位置，剔除掉场景中的大部分物件。如果我们编写了这么一个剔除的 System ，那么在这个 System 运作之后，后续的其它 System 就不应该在整个世界中迭代可视的 Component ，而应该针对的是剔除后的集合了。

如果忽略 EC 这种基于组合的对象模型和传统 C++ 中基于继承的对象模型的实现上的差异，我们可以把 Component 仅看成是 Entity 身上的一种筛选标签 Label ，ECS 模型其实是为 System 提供了按 Label 筛选出 Entity 集合的能力。那么，我们是不是应该提供一种不太影响处理效率的，动态贴标签和撕标签的能力？空间剔除器可以给 Entity 打上需要渲染的标签，后续的渲染器可以迭代“需渲染”的组件集合。

我在 Overwatch Gameplay Architecture and Netcode 中看不到类似的设计，在我自己的实践中，Label 的想法也有不少问题。所以想了另一种方案。

据说，在守望先锋的引擎中，存在着大量的单件（singleton）组件。相关的 System 只会处理这一个组件，从里面读取数据，或把数据放在其中。我认为、用于 System 间交换数据的事件队列、剔除器的结果、这些都应该是存放在某个单件中。像渲染器这种 System 不必从 Entity 全集中迭代需要渲染的集合，而应该转而从剔除器单件里迭代一个子集。

而剔除器的工作依赖对象本身的状态变化。游戏场景中会有大量的物件，它们的状态几乎不会变化，每帧都迭代一遍是很低效的。最好是只在位置变化时才更新剔除器中的集合。

Wikipedia 页面中也谈到 system 间的通讯问题。某些对象状态改变并不频繁，所以处理需要利用观察者模式来被动触发：

The normal way to send data between systems is to store the data in components. For example, the position of an object can be updated regularly. This position is then used by other systems.

If there are a lot of different infrequent events, a lot of flags will be needed in one or more components. Systems will then have to monitor these flags every iteration, which can become inefficient. A solution could be to use the ovserver pattern. All systems that depend on an event subscribe to it. The action from the event will thus only be executed once, when it happens, and no polling is needed.


我自己在实现的时候给 ECS 框架增加这么一个设施：你可以让一个 System 关注一类 Component 的变化事件。只有这类 Component 变化后，System 才运行 —— 而普通 System 是每帧都运行的。而 Component 的新建和删除都会触发这种变更事件，我还给框架增加了一个方法，可以主动设置一个 Component 变更。同一个 Component 的变更事件在同一帧内只会触发一次。

btw, 如果你有留意 Overwatch Gameplay Architecture and Netcode 演讲，大约在第 4 分钟的时候，他展示了一张系统的结构图，其中 System 有两个方法，一个是 Update ，第二个叫 NotifyComponent ，参数是一个 Component 指针。演讲中并未谈及这个 NotifyComponent 是做什么用的，但我猜想就是做的类似工作。

在我的（基于 Lua 的）实现中，System 每帧都会收到一个变更集合，而不是每个 Component 调用一次 System 的对应函数。这是因为 Lua 中维护集合相对廉价，而函数调用相对昂贵。

这个集合每帧更新。一旦有新建 Component ，或是别的 System 主动触发变更消息，都会添加。一开始，我打算在最后将同帧删除了的 Entity 以及从 entity 中移除了 Component 的部分从集合中去掉，保证 System 遍历集合中的 entity 都是有效的。

后来发现，这种做其实是多余的。因为 System 不仅要关心 component 的变化，更要关心 Component 的消失。比如对于空间管理器来说，一个对象从空间中移除也是重要事件。好在 Entity 我们都用唯一 Id 来引用，即使删除，id 也永不复用。如果只需要在 Entity 删除时也把 id 记在这个集合里，System 自己迭代时，发现一个 Entity id 已经无效了，就说明触发了删除事件。这比单独再设计一个删除事件要简洁的多。

总结：

当 System 需要迭代一组 Entity 对他们中的 Component 做特定操作时，这个集合可以从 EntityAdmin 中用 Component 类别做筛选，也可以从 EntityAdmin 获取一个单件，由单件维护这样的集合。

一个单件中的 Entity 集合由特定的 System 来维护，这个 System 可以订阅指定的 Component 的变更事件。

变更事件包含了 Component 的创建、移除和状态变化，创建和移除事件会随着 Entity 的构建和移除自动产生，状态变化由专有 API 产生；同一帧内，一个 Component 最多只会产生一个变更事件。事件并不区分类别（创建、移除等），由 System 在迭代时自行检查 Entity id 的有效性来判别。