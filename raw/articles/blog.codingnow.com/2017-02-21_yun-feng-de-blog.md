---
title: 云风的 BLOG
url: https://blog.codingnow.com/2017/02/
published: '2017-02-21'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 绕过 c api 直接访问 lua 表

今天试了一下一个想法：绕过 lua 提供的 C API 直接去访问 lua 的表结构，提供在性能及其重要的环境高效访问数据结构的方法。

例如：我们需要在 lua 和 C 中共享一个 vector 3 结构，有两种实现方法：一、把 C struct 实现为 lua 中的 userdata ，然后给 userdata 加上 metatable 以供 lua 中访问内部数据；二、在 lua 中使用一个 table 实现这个 vector3 结构，类似 { x = 0.0 , y = 0.0, z = 0.0 } 这样；然后在 C 里通过 c api (`lua_rawget/lua_gettable/lua_getfield`

) 来访问里面的数据。

前一种方法会导致在 Lua 中访问成本加大、而后一种方法增加的是 C 中访问数据的成本。如果我们只在少数性能敏感的地方通过 C 去操作数据结构，那么第二种方法看起来更简单灵活一些。这样，不需要 C 介入的地方，是没有额外开销的。毕竟、通过 metamethod 索引 userdata 的成本比直接索引一个普通的 table 要重的多。

但是、第二种方法会导致 C 访问数据的成本较大。我们采用 C 代码去处理 vector 数据结构，一定是考虑到性能热点，在语言边界上损失性能感觉不太划算。我觉得或许可以采取一个技巧来加快它。

对于标准的 Lua 实现，构造好的 hash 表，在不添加新 key 的前提下，读写已有的 key ，value 所在的 slot 是不变的。如果我们能记住 slot 的位置，那么就可以绕过 hash 过程、也不需要把 key （这里是一个 string）压栈，直接读写值了。

而且，对于同一个 `lua_State`

从一个空表开始，按一致的次序写入相同的 key ，内部数据结构也一定相同。我们可以利用这一点，为同类结构一次性生成索引表。

我写了一小段代码验证我的想法，感觉是可行的：[https://gist.github.com/cloudwu/09fca725cb9177d809790b6a7ecdac20](https://gist.github.com/cloudwu/09fca725cb9177d809790b6a7ecdac20) 。

你可以先创建一个 4 个 slot 的 hash 表，key 分别是 x y z `__vector`

。这第 4 个 key `__vector`

是一个标记，表示这是个规整过的数据结构，x y z 都是浮点数，且一定在固定的 slot 里。

`void vector_init(lua_State *L, struct vector_offset *vo)`

可以用来生成 slot 号的结构 `struct vector_offset`

。每个 `lua_State`

只用生成一次，然后就可以永久保存在 C 的数据结构中。

然后我们用 `vector_get`

可以获得内部数据结构 Table * ，这个结构定义在 lobject.h 中，是一个内部 h 文件，这里可以借用一下。之后，就可以用宏 X Y Z 去访问这个 Table * 了。

`vector_get`

中，会检查指定的 table 是否是规整化的 vector 结构，如果不是，就把 x y z 三项读出来，清空 table ，再写回去，并填上 `__vector`

标记。此处检查 `__vector`

标记是个很轻量的操作。

这个方案适用于 Lua 5.3 ，我没有在老版本的 Lua 上试过，但想必也是可以用的。它的好处是不需要修改任何 Lua 的实现代码、只需要引入 Lua 本身的内部 h 文件即可。所以利用这组 api 实现的 lua 库是可以和其它库兼容共存的。