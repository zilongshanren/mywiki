---
title: 云风的 BLOG
url: https://blog.codingnow.com/2021/09/
published: '2021-09-18'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### Paradox 脚本语言的一点研究

因为一直给群星维护汉化 Mod 的缘故，我花了不少时间去理解 Paradox 的配置脚本语言。

[我认为它用了类 lisp 的语法来描述数据](https://blog.codingnow.com/2017/07/paradox_data_format.html)。用数据去描述游戏逻辑。P 社的游戏都有玩家共建的 Wiki 提供了丰富的资源来[帮助玩家创作 Mod](https://stellaris.paradoxwikis.com/Modding) 。学习它的脚本语言是非常容易的。

最近一段时间，我仔细阅读了 Wiki 中所有关于 Modding 的文章，相比之前零星的了解，算是做了一次系统的学习。

这套脚本语言还是以配置数据为主，但也提供了很多逻辑控制手段，很值得学习。

我以一个游戏程序员的角度去看，在此记录一些有启发的东西。当然，我自己并未用它开发完整的 Mod ，可能理解会有所偏差。

从游戏逻辑控制（官方称为 [Dynamic modding](https://stellaris.paradoxwikis.com/Dynamic_modding) ）的角度，它定义了两个重要的概念：Effect 和 Condition 。它们均以数据列表的形式出现在脚本中，从词法上看，和其它静态数据并无不同。但结合上下文，它们是一段段类似通用语言中的语句段。

Effect 是一段顺序执行的语言段，它的运行伴随着游戏状态的变化；我们可以把一组 Effect 的语句段单独列出来，并起个名字，这被称为 scripted effect 。但我看来，它更像是通用语言中的（有副作用的）函数 。scripted effect 甚至还可以有参数，但没有返回值。

而 Condition 则可以看成是一组类型为布尔量表达式，它的值只能是 true 或 false ，且不会修改游戏的状态。组成 condition 的更小单元叫 trigger ，trigger 也可以被单独定义，被成为 scripted trigger 。它就像一个无副作用，布尔类型的函数。

把有副作用的命令式代码段 effect 和无副作用的条件代码段 condition 分离，可以极大的减少面条班的 if else 逻辑。

我猜想，引擎在实现的时候，还可以对 Condition 的结果做一些 cache ，避免在同一个 game tick 内重复运算。这对群星这种对象繁多、逻辑复杂的策略游戏是有很大的性能收益的。

例如，游戏中 event 的数据结构中，就组合了 effect 和 condition 。

country_event = { id = action.8 hide_window = yes is_triggered_only = yes trigger = { is_country_type = default from = { is_country_type = default } NOT = { has_communications = from } is_hostile = from } immediate = { establish_communications = from fromfrom = { conquer = root set_controller = root } } }

上面这个实例中，就演示了 action.8 这个事件会在 trigger 中定义的 condition 满足的时候，执行 immediate 中定义的 effect 。

第一次看到这段代码，可能很难理解。这里就需要了解另一个重要概念 scope 了。

群星里的对象是被组织在一个个 scope 中的，有 country sector system planet pop fleet ship leader 等等这样的 scope 。每层 scope 都会包含特定的对象以及若干 scope 。

比如星区 sector 这个 scope 中，包含了星区这个对象的各种属性外，还包含了星区内的所有星系 system scope 引用；同样，星系内也有所在星区的 scope 的引用。

这些 scope 如树状层次组织起来。同一个 scope 不只一条脉络。比如，你可以从 国家-星区-星系-星球-人口 最终这个人口的 scope ；同时也可以从 国家-派系-人口 找到它。同一个 scope 可以以不同的分类方式同时存在于多个树中。

每个定义好的 effect 或 trigger 都需要在特定类型的 scope 中运行。比如 habitability 宜居度就是一个只能在星球 planet 这个 scope 中运行的 trigger 。它可以探知某个 pop 在那个 planet 上的宜居度如何。

habitability = { who =value = 0.6 }

这条就是说，在当前星球的 scope 下，针对 who 这个东西的宜居度是否为 0.6 。这里的 value = 0.6 非常有迷惑性，这里的等于号其实是一个比较操作符。上面这一条大致相当于这样一段 lua 代码：

_ENV:habitability(who, function(value) return value == 0.6 end)

我们从当前的环境中取到 habitability 这个函数，把当前环境和 who 这个目标传给它；计算出相对宜居度的 value ，交给 value == 0.6 去判断，得到一个布尔量的结果。

在很多语言中，我们需要写 a:foo(args) 这样去调用一个函数；但在这里不同，需要先进入 a 这个 scope ，再调用 foo ；也就是写成 a = { foo = args } 。

这样做的好处是，在一个 scope 中可以做很多和当前 scope 对象有关的事情，而不必反复的写 scope 本身。这有点像 C++ 中在成员函数中省略 this 的语法。

不过，这里还可以做的更多。比如：

pop = { planet = { habitability = { who = prev value > 0.6 } } }

这读作：判断人口所在星球相对该人口的宜居度是否大于 0.6 。

它可以看成是调用了 pop.planet.habitability 这个函数，只不过按该脚本的语法，我们需要用 pop = {} 和 planet = {} 进入两层 scope 。（再群星 3.0 的更新中，提供了 dot 语法做语法糖，简化过多 scope 层次切换的花括号）。

但和很多别的语言不同。如果是在 Lua 中，你写 pop.planet:habitability() 时，只有 pop.planet 这个对象传递给了 habitability 方法。这还是通过 : 这个语法糖实现的。如果你写 . 的话，这个信息也被扔掉了。

但是，此处却可以用 prev 引用到 pop ，也就是 planet 的上个 scope 层次。（同时也可以用 this 引用当前的层次。）

scope 的设计给了我不少的启发。除了 prev 可以引用前一个层次的 scope 外，还可以用 root 引用最外的层次，以及用 from 引用调用栈的上一个层次。有了这一系列的语法糖，很容易描述对象和对象之间的关系。相比而言，在传统的面向对象语言中，通常只提供一个 this/self 指代自己。而游戏中的大量逻辑是面向多个对象的：有战斗中的对手，有管理层次中的上下级，等等。

trigger 和 effect 段中都可以借助 scope 语法简化很多复杂业务的写法。

比如，可以在 country 的 scope 中写：

any_planet_within_border = { is_planet_class = pc_gaia }

就可以判断当前国家境内是否有至少一个盖娅星球。这个 `any_`

的 trigger 会迭代该 scope 下所有的星球，对每个星球 scope 都执行 `is_planet_class = pc_gaia`

这个 trigger 条件。

还可以在写：

every_owned_planet = { limit = { is_planet_type = pc_continental } … }

用 limit 指定的 condition 筛选出当前国家内所有大陆性气候的星球，做一系列 ... 操作 。