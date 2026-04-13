---
title: 云风的 BLOG
url: https://blog.codingnow.com/2021/07/
published: '2021-07-27'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

最近在公司内做了一次两小时的分享，介绍了一下我最近几年对 ECS 模型的一些想法以及最近在项目中的应用心得。

我分享的主题不叫 ECS ，而用了一个更宽泛的名字 Data oriented design 。因为我不想局限在 Entity Component System 这些具体名词上。[从 wikipedia 上看](https://en.wikipedia.org/wiki/Data-oriented_design) ，DOD 的提出是源于游戏软件对性能的追求，
它主要围绕的都是其数据在内存中的组织形式不同。和 C++ 这类可以直接控制对象内存布局的 OOP 的语言的默认布局相比，DOD/ECS 的数据布局对 CPU Cache 更好友一些，从而可以获得更好的性能。

如果从这个角度看，如果不是用 C/C++ 这些可以直接控制数据内存布局的语言，采用 ECS 的意义很小。

但是，我觉得 ECS 的意义不仅在于此，它的更重要的意义在于在数据层面对业务解耦。从而引导实现者实现内聚度更高的模块。

根据我这几年的经验，我认为，当你从数据组织的角度去看待业务，遵循处理问题的某些特定模式，才能用好 ECS 。如果仅仅是把 object 的指针换成 entity id ，还是依旧 OOP 中的惯例去写业务，只会感觉处处掣肘。ECS 强调了数据组织方式，在这种数据组织方式下，过去一些简单 O(1) 的处理会变得复杂 O(n) ，一些复杂的处理会变得简单。在享受它带来的收益（性能提高、耦合度下降）同时，必须接受一些限制。

在我看来， ECS 模型下，可以认为所有的数据都被放在一张 2D 稀疏表中。

这张表格每一行就是一个 Entity ，每一列就是一类 Component 。每行可以有许多空洞（不是每个 Entity 都具备所有的 Component ；每列同样可以有空洞。

在这个数据模型下，最基本的操作就是遍历：纵向遍历就是枚举同一类 Component 集合中的每一个元素，在遍历到某个 Component 时，可以横向遍历同一行，即同属一个 Entity 的其它 Component 。

注意：在这里，类型是非常重要的元素，我们永远都可以根据 Compoent 的类型找到具体的数据，所以，传统 OOP 中常见的 Singleton 模式就自然消失了。singleton 其实就是上述表中的某个特定列里只有一个元素，我们自然可以 O(1) 去到这个元素。

在新的数据模型下，引用单个 Entity （特定行）是比较困难的，而列（类型）通常是固定的，索引列是非常自然的事。对一列做迭代变得非常廉价。

我们甚至可以用符合条件去拣选出要迭代的集合：例如，同一行中即包含 A 又包含 B 的集合。这非常像数据库的设计，甚至可以设计出这样的条件：拣选出 A = 42 这样的行。我最近实现的 ECS 框架中迭代器 api 定名就是用的 select 。

在 [wikipedia 的 ECS 词条](https://en.wikipedia.org/wiki/Entity_component_system)中也有类似的观点：It is notable that an ECS resembles the design of databases and, as such, can be referred to as "an in memory database"


和很多已有的 ECS 框架不同，我在实现时加入了更多的限制。我相信这些限制可以简化实现，而且能引导使用者去寻找更合适的算法。

- 每个 Entity 都有一个内在 id ，但这个 id 只是实现手段，不对外暴露。不可以用 id 去引用特定 Entity 。
- Entity 必须在构建的时候就决定好它由哪些 Component 的构成，它不可以在后续运行过程中任意增减 Component 。除了后面提到的特例。
- Tag 是一种特殊的 Component ，它不携带数据，只是用来标记一个 Entity ，用来影响 select 的结果集。Tag 可以被动态的 Enable 或 Disable 。（破坏了规则 2 ）
- 允许在一个特定的处理过程中动态的给 Entity 添加一个临时的 Component ，这会破坏规则 2 。这么用必须遵循一个原则：这类临时的 Component 必须按 select 的遍历次序依次添加，所以，不可以在多个 System 中反复添加（那样会破坏次序）。它通常用于 System 间临时传递数据，在后续的某个 System 结束后，将全部清除。
- select 得到的 Component 次序是稳定的，每次都一致，即这些 Entity 的构建次序。
- 如果需要用特定的次序遍历，可以创建一组 sorted tag 的特殊 Tag ，对这个新 Tag 遍历就可以得到特定的次序。但用这种方式遍历时，上面的规则 4 不再适用。且 sorted tag 需要自己维护，没有自动更新的机制。


在这个模型下，删除这个操作变得不那么特殊。删除就是给一个特定的 Entity 加上一个叫 Removed 的 Tag 而已。我们可以在每次 update 的末尾真正删除有这个 Tag 的 Entity 以释放内存。但这只是因为现实世界中内存资源是有限的缘故。如果资源无限，其实我们永远不必真的删除什么数据，只需要在 select 时排除带有 Removed tag 的 Entity 即可。

有了 Removed Tag 后，C++ 的对象模型中的 RAII 机制也变得不那么必要。因为，我们可以在最后 select 出带 Removed Tag 的特定 Component ，集中做析构处理即可。每个模块要做的就是在执行 pipeline 的最后环节统一添加销毁的处理。这会比每个单独的对象独立做析构要健壮的多。

同理，构建新 Entity 也是一样。大多数情况下，我们并不需要（也不适合）让构造的新对象立刻出现在系统中。这个时候，可以先构建一个仅含初始化列表这个 Component 的 Entity 。等下一个 update 开始时，再由一个 system select 出新构建的对象，统一做初始化工作。


Entity 在这个模型下是没有用来做引用的指针或 id 的。处理逻辑只能针对特定集合而不能针对特定的对象。如果要针对制定对象，我想有两种方法：

其一，我们可以对指定对象打上特殊的 tag ，遍历这个 tag 就能得到特定的 Entity 。

其二，增加一个叫 entity id 的 Component 的，在遍历这组 Component 的时候比较具体的 id 值，找到特定的对象。需要使用者明白，这是一个 O(n) 的操作。

但，我们还是留下了一个关键难题：总有需要相互引用数据的需要。比如在 3d engine 中，场景树节点就必须有邻接关系。怎么在这个数据模型下储存一张邻接图？

我的解决方案是，使用一种特殊的 Component 。当一组数据，例如场景树节点，需要被引用时，这个 Component 不再放在和其它 Component 的同一行上。即它自己独立是一个 Entity 。

这类 Component 永不删除，但会被复用。

当一个 Component 永不删除，它在同一列上的位置就是稳定的。我们就可以用它在列上的行号来引用它。我给这类 Component 加上两组 Tag ，一个叫 Live 一个叫 Dead ，这两个 Tag 是互斥的。当 Live 被 Enable 时， Dead 一定是 Disable 的；反之亦然。

如果我们想遍历这类 Component ，就遍历 Live Tag 集合；当创建新对象时，从 Dead 集合挑出第一个复用。删除就是反转一下 Live/Dead Tag 。

其它 Entity 想引用它时，记录下它的 id ，就可以用 O(1) 时间索引到它。

不过，多处引用和解引用的问题还是留给用户。依旧可以用引用计数或标记扫描的技术去解决。框架本身并不对此负责。


这段时间，我基于以上的想法，[实现了一套 Lua/C 的混合 ECS 框架](https://github.com/cloudwu/luaecs)。尚未全部定稿。

这套东西的设计目标是，可以用 Lua 描述和定义所有的数据结构，并由使用者决定某一类 Component 最终是放在 Lua table 中还是 C Struct 里。但无论放在哪里，都从 Lua 自由访问。

Lua 访问 C struct 中的数据会有额外的代价，性能会略逊于访问 Lua table 中的数据。但因为 ECS 的特性，我们都是批量访问一组数据，我的实现让这个代价尽量的小。简单的测试表明，大约有 30% 的性能损失。我觉得可以接受，因为如果用传统的 OOP 的思路将每个 C 对象通过 metatable 映射成 lua full userdata 的话，通常需要承受 3 倍以上的性能损失。

但这换来的好处是：在 C Struct 中的 Component 可以通过 C API 直接访问。处理效率比处理 Lua 中的数据高一到两个数量级。并且它有更紧凑的内部布局，对于大量数据来说，能比放在 Lua table 中，少占用 2 - 5 倍的内存空间。

我会根据使用场合，把需要高频操作的简单数据结构放在 C struct 中。这些数据往往数据量大，但处理业务简单（例如粒子系统），在 Lua 中并不会单独针对特定数据做特殊处理。但 Lua 层面依然可以根据调试需要处理它们。

整个系统是基于它是一个 Lua 库的理念来设计的，是先有了 Lua 的接口才导出必要的 C API ，而不是反过来，先设计出 C Api 再做 Lua binding 。

基于这个理念，C API 仅用来处理那些高频处理的简单数据结构。我没有对 C 暴露出对象的构建、类型的定义等这些特性。也无法直接用 C API 去访问那些储存在 Lua 中的数据结构。因为，动用 C 写 system 的场合是非常少的，即使出现，几乎只需要提供迭代这一个主要特性就够了。