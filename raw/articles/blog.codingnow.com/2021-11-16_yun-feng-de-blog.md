---
title: 云风的 BLOG
url: https://blog.codingnow.com/2021/11/
published: '2021-11-16'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### C 中访问 Lua 配置表的优化

这两天写代码时用到[之前写的一个对 Lua 配置表的 cache 模块](https://blog.codingnow.com/2021/06/lua_property_cache.html) 。感觉用起来还是不够简洁方便。我今天动手重新设计了一下。

需求是这样的：

项目有非常多的配置信息保存在 Lua 的 （树状层级的）table 中，大部分逻辑代码直接用 Lua 的语法便可直接访问。但是，有少量有性能要求的业务是在 C 中实现的，C function 中也需要读取这些存放在 Lua 中的配置数据。

配置项随着项目开发，变更非常频繁。如果我设计一个小语言，定义出配置表，用代码生成的方式把表项翻译成对应的 C/C++ 结构，再在 C side 根据 Lua 中的数据重建一组 C 数据也未尝不可。这就是 google protobuf 官方采用的方式（用代码生成的方式，根据数据的 schema 构建出 C++ 类，让 C++ 可以方便访问这些数据）。

但我不想搞得这么复杂（浪费？）。大部分业务循环次数很多，而需要读取的配置表象却比较单一（反复取相同的条目）。所以，虽然第一次通过字符串 key 逐级解析 Lua 配置表或许较为低效；但只要在 C side 用一个 cache 模块缓存下高频访问的配置项应该就能解决性能瓶颈。

我采用了一个固定大小的内存块做 hash cache 。key 使用编译时决定的 32bit int 。用宏定义出来。

比如，如果我想读 name 这一项，就定义一个：

PROTOTYPE(name, string)

它表示，有一个配置表项是 "name" ，它的类型是 string 。这个宏会展开为一个 C 函数

`const char * get_name(struct cache *c, const char &key);`


函数的实现也是由宏展开的，实现内部会给 name 分配一个唯一的 id 。

ps. 一开始我用 `__LINE__`

这个宏拼接出一个唯一 id ，只要宏定义不在同一行就不会有冲突。后来发现，现在几乎所有的编译器都支持了 `__COUNTER__`

这个宏，它会帮我生成自增 id 。

需要缓存的值有四种类型：int float bool 和 string 。前三种类型都是 32bit 的，而字符串在 64 位平台上是一个 64bit 指针 const char * 。string 类型非常少见（在 C 代码中几乎不会访问到），如果我简单的用一个 union 类型联合该四种类型会比较浪费。因为这样，每个 hash slot 就需要 4 (key) + 8 (value) 字节。考虑到对 cpu cache 友好的话，我会把 key value 连续存放在一起，这样在 64bit 平台上，再考虑对齐问题，每个 slot 可能需要 16 字节 。

经过一点思考，我发现我只需要把少量的 string 类型存放在连续的两个 slot 中，每个 slot 存放一半就可以了。这样，每个 slot 就只需要 4 + 4 字节即可。

这个 cache 的运作算法是这样的：

通过

`get_xxx`

的 C API 访问 cache ，编译器为 xxx 生成了一个唯一 32bit id 做 key ，以此 key 查询 cache 。如果命中，直接取出 value 项。由于类型信息是编译器决定的，所以可以从 value 的 union 中取出正确的类型。如果 cache miss ，这通过编译器记录的 key string 去 Lua side 查询具体的 value 。这个过程花少稍长的时间是可以接受的。如果在 Lua side 找不到对应项，则抛出 error 不影响 C cache ；找到的话，就更新对应的 C cache 条目。

当对应的项目是字符串时（编译期决定），计算 hash 时元整到偶数序号的 slot 上，认为该处连续的两个 slot 保存着该条目。需要核对两个 slot 对应的 key ，更新对应的 value 。返回结果需要将两个 slot 上的 value 值合并为一个 const char * 返回。


在使用时，需要把 C side 可能用到的配置表项的 key 全部定义在一个 .h 文件中，方便编译器统一生成 id 。key 可以是点分割的字符串，对应 Lua 中的树状多级表。

在 C 中不提供一次读取一个子配置表的 api 。

在 C 中不能迭代配置表。