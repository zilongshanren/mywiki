---
tags: [lua, 动态语言, 脚本, 调试工具, bitsquid]
date: 2026-04-19
sources: 1
---

# Lua 运行时动态性技巧

C++ 程序员看自己的代码，往往把它当成一堆**固定的类和函数**——编译完了就长这个样。换到 Lua、JavaScript、Python 这样的动态语言，代码本身是**数据**：任何函数都可以在运行时被重新绑定、任何命名空间都可以被遍历。Niklas Frykholm 在 2012 年的这篇博客列出了 Bitsquid 把这条特性榨到底的七招用法，每一招都对调试器和工具链意义重大。

## 把命令行变成游戏控制台

Lua 的 `loadstring` 可以把一段字符串当代码编译并执行。接一个远程 console 面板，美术/策划就能往跑着的游戏里直接打：

```lua
World.spawn_unit("bazooka", Unit.position(player))
Unit.set_data(player, "run_speed", 4.3)
```

这是 [[runtime-editor-console-connection]] 在 Bitsquid 侧的等价实现——把外部工具和运行时用一条命令通道连起来，迭代效率立刻上一个量级。

## 覆盖式热重载

控制台不止能发命令，**还能重新定义函数**。把 `Player.register_kill` 直接在控制台里重新写一遍，之前所有调用方的引用立即指向新版本——不用重启、不用回存档、不用重新进关。

只要全局命名空间的使用有纪律，整份 Lua 代码都能这样被热加载。文件一改，按一个键，运行中的游戏就拿到新逻辑。甚至可以进一步：**脚本报错时不崩游戏，只冻住那个协程**，等程序员修好、重载、继续跑——现场保留所有上下文。

## 劫持引擎 API 做侦查

引擎通过 C 函数暴露的 `World.spawn_unit`、`PhysicsWorld.raycast` 这些 API 在 Lua 里**没有任何特权**，可以像普通 Lua 函数一样被覆盖：

```lua
old_spawn_unit = World.spawn_unit
function World.spawn_unit(type, position)
  if type == "tribble" then
    print_stack_trace()
  end
  old_spawn_unit(type, position)
end
```

这样就能问出"是谁在半夜偷偷 spawn tribble"或者"到底哪里在做昂贵的 raycast"这种传统 profiler 问不出的问题——**在 API 边界上加钩子**，不动业务代码。

## 在脚本里做向后兼容

API 改名之后，通常的办法是全工程 grep 替换。但脚本可以自己写一个"旧名字转调新名字"的胶水层：

```lua
function PhysicsWorld.clear_kinematic(world, actor)
  Actor.set_kinematic(actor, false)
end
```

引擎侧该删就删，外部项目代码不动就继续跑。可以作为**过渡期**的稳态，也可以作为逐步替换的临时桥。Niklas 的态度值得记录：*backwards compatibility is the mother of stagnation*——留的时间太长会积成屎山，但有这个转接层让淘汰旧 API 的阵痛变短。

## 动态插 profiler 探针

在 C 里插 `PROFILE_SCOPE` 必须编译期选点。Lua 可以写一个通用 wrapper：

```lua
function profile(class_name, method_name)
  local f = _G[class_name][method_name]
  _G[class_name][method_name] = function (...)
    Profiler.start(class_name .. "." .. method_name)
    f(...)
    Profiler.stop()
  end
end
```

调 `profile('Player', 'update')` 就把 `Player.update` 包上 profiler scope。优化现场按需插、不需要时再解开，探针分布完全由本次调查决定——这是静态插探针语言做不到的。

## Tab 补全与全对象枚举

Lua 的反射能力还能用来造两样配套工具：

**Tab 补全**：遍历 `_G` 里所有表（类），再遍历每个表里的函数，就得到完整可调用函数列表。人在 console 里不用背 API。

**全对象枚举**：递归遍历 `_G` 和所有 metatable、key、value，能枚举出所有 Lua 可达对象。写一个 `f(o)` 作用于每一个对象，就能做"谁血量是 0"、"每类对象内存占多少"这种跨整个运行时的快速诊断。

## 与手写绑定的搭配

这七招都建立在 Niklas 坚持的一条前提上：**Lua 绑定手写**。每个 `lua_unit_set_position` 就是几行 C 代码——不用自动绑定生成器，因为手写能让 Lua API 脱离 C++ API 的形状，做成更 Lua-idiomatic 的接口，之后重构 C++ 也不必动脚本。详情见 [[lua-cpp-binding]]、[[lua-light-userdata-bindings]]。

## 相关

- [[lua-cpp-binding]] — Bitsquid 手写绑定的做法
- [[lua-design-philosophy]]
- [[lua-class-pattern]]
- [[runtime-editor-console-connection]] — 同一类"把命令通道打通"的工具
- [[binary-hot-reload]] — 代码热加载在 native 侧的难度对照
- [[csharp-runtime-script-compilation]] — 另一门运行时可编译语言的同类实践
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-embracing-dynamism]]
