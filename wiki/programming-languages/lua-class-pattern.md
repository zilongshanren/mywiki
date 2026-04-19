---
tags: [lua, oop, 元表, 封装, api-design]
date: 2026-04-19
sources: 1
---

# Lua 中定义类型的极简套路

[[cloudwu]] 在 2025 年 8 月的一篇笔记里整理了自己用 Lua 定义类型的几种常用写法，核心立场一贯：**元表足够用、不要在 Lua 上再造一层 C++ 式的 class 系统**。

## 最小套路

一个类型本质上是一张方法表加上以自身做 `__index` 的元表：

```lua
local object = {}; object.__index = object
local function new_object(self) return setmetatable(self or {}, object) end
function object:get(what) return self[what] end
```

这么写足够朴素，熟了以后可以直接散落在各模块文件里，依赖 Lua 的模块机制找到 `new_object`，不必额外封装。

## 只在需要"类型注册表"时才做封装

如果希望通过一个类名映射表找到所有定义过的类型，可以抽一个 `class` 模块：`class[name]` 读取时自动创建一张方法表、元表，以及一个 `__call` 让 `class.set { ... }` 即为构造。进一步还可以让 `class "set"` 等价于 `class.set`，留一个便于搜索的文本模式。

这个封装的边界非常克制：它**只**解决命名注册与默认构造，不试图做继承、属性访问控制或类型检查。和 C++/Java 的 class 语义完全不是一回事。

## 容器类型与元数据：四种写法的取舍

当类型是一个容器（例如 set，需要带 `n` 这种元数据），有四种写法，分别对应不同的侵入度：

1. **元数据放在 `self.container` 旁**：`self.container` 是真正的集合，`self.n` 是计数。优点简单，缺点是访问集合元素要写 `obj.container[k]`。
2. **元数据以 `_n` 这种前缀混入 `self`**：集合数据直接放在 `self` 上，迭代时要额外剔除 `_` 开头字段，用 `obj.x` 比 `obj.container.x` 自然。
3. **元数据外置到 ephemeron table (`__mode = "k"` 的弱表 SET)**：`SET[object] = {...}`，借 Lua 5.2 引入的 ephemeron 特性让元数据随对象被 GC。`pairs(obj)` 干干净净看不到元数据，代价是每次访问元数据多一层查表。
4. **用 `[false]` 作为元数据 key**：Lua 中 `false` 是合法 key，而业务上几乎不会用 `false` 当键。存一个 `[false] = 0` 即为计数，`#obj` 通过 `__len` 暴露。迭代时只需 `if k then ... end` 剔除。

写法 4 是这篇笔记的新技巧：**不引入弱表、不引入下划线约定，用一个天然不冲突的 key 藏住元数据**。缺点也明白：只适合元数据少、且确实不需要 `false` 做合法键的场景。多个元数据时可以让 `[false] = {}` 套一张子表。

## 让容器"假装"就是 table

如果追求让 `pairs(obj)` 的行为和纯 table 完全一致，可以再加一层 `__pairs` 过滤掉 `false`；把这个模式打包成 `class.container "set5"`，并且允许直接覆盖默认构造函数（例如 `class.set5()` 返回一个已带 `[false] = 0` 的实例）。到这一步，类型使用者看到的就是一个普通的 table，但拿到了 `#obj`、`pairs` 干净、`setmetatable(.., class)` 注册等一揽子好处。

## 设计取向

这几种写法都刻意避开了 "模拟一门面向对象语言"。云风的选择是：

- **元表是工具，不是架构**——用它解决具体的封装、构造、迭代问题，不要反过来被它驱动。
- **暴露 vs 隐藏是一个连续谱**——从方案 1 到方案 4 对应"元数据暴露程度"的逐级降低，选择点在于调用方用得舒不舒服，而不是"哪个更 OO"。
- **优先选本地技巧**——`[false]` 作为 key 比引入弱表或下划线约定都更轻量，宁可让适用面窄一些，也要简单。

这套思路跟 [[lua-design-philosophy]]、[[information-hiding]]、[[interface-vs-implementation]] 都是同一脉络：用最少的机制解决问题，别替使用者提前做"以后也许会扩展"的决定。

## Sources

- [[sources/cloudwu-lua-class-pattern]]
