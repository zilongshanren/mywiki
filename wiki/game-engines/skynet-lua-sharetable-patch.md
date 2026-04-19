---
tags: [skynet, lua, 虚拟机, 字符串驻留, 共享常量, 字节码]
date: 2026-04-19
sources: 1
---

# Skynet 的 Lua 共享函数原型 patch

[[cloudwu|云风]] 多年来在 [[ltask-scheduler|skynet]] 里维护了一份**修改版 Lua**，允许同一进程内多个 Lua 虚拟机共享函数原型（function prototype）——每个 skynet 服务都是独立 VM，一个大型服务器动辄上千服务，全部独立加载字节码的初始化开销和内存重复都不小。这份 patch 是 skynet 能跑大规模 Lua actor 的关键基础设施之一。

## 难点：短字符串的 interning

Lua 对短字符串做 VM 内部 interning，同一 VM 里相同字面量共享一份内存且比较退化为指针比较（见 [[lua-incremental-gc|lua-incremental-gc]] 的 `FIXEDBIT` 机制）。函数原型里嵌的常量字符串也被 intern 到所属 VM。当要把这些原型**跨 VM 共享**时，就必须解决"外部导入的字符串"和"本 VM intern 池里已有字符串"如何并存——既不能重复 intern（否则共享无意义），又不能让 VM 里用指针比较字符串的代码错失匹配。

这个 patch 的主要工作就在这里——云风 2019 年有篇专文 *字符串比较* 详细记录过算法。副产品是打过 patch 的 VM 还可以跨 VM 共享只读常量表（`skynet.sharetable` 库）。

## Lua 5.5 的 external strings：可以退出 patch 了

Lua 5.5.0（2025 年底发布）引入了 **external strings** 原生特性，用于让字符串内容指向外部内存，字节码加载速度大幅提升，skynet 的多服务启动性能也会从中受益。云风的判断是：**新项目应避免再依赖 `skynet.sharetable`**，理由是想把 skynet 对上游 Lua 的私有 patch 砍掉，减少长期维护成本。换句话说，等 Lua 官方新特性把共享使用场景覆盖到够用程度，就回到干净的上游版本。

## 5.5 其他值得注意的更新

同步升级时，云风列出几处他认为值得 skynet 项目逐步利用的新特性：

- **`global` 关键字**：强制显式声明全局，减少拼写错误引起的难查 bug。skynet 核心暂未使用，计划逐步添加。
- **分代 GC 改为步进式**：老版本的分代 GC 对内存占用大的服务有较大停顿，往往要手动切回步进模式。5.5 之后应该不再需要。
- **`...args` 变长参数语法**：可用 table 形式直接访问变参列表，可以精简一部分 skynet 自身 Lua 代码。

## 升级注意事项

`skynet` 的 5.5 升级基本兼容 5.4，但**必须 `make cleanall`** 才能让 Lua 重新编译——`make clean` 不清理 Lua 的中间文件。另外虽然兼容，充分回归测试是必要的。

## 相关

- [[cloudwu]]
- [[lua-design-philosophy]]
- [[lua-incremental-gc]]
- [[ltask-scheduler]]

## Sources

- [[sources/cloudwu-skynet-lua-55]]
