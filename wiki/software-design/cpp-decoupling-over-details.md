---
tags: [c++, 软件设计, 解耦, 模块化, 代码评审, 游戏引擎]
date: 2026-04-19
sources: 1
---

# 活过 C++：解耦才是唯一重要的事

[[angelo-pesce|Pesce]] 2011 年《Surviving C++》的核心论断：**软件项目最重要的单一质量是「可被修改的能力」**。代码要改、硬件要换、设计要翻、玩家口味要跳——那门能让你**轻松动刀**的语言就是好语言；越动越难动的代码就是烂代码，和任何具体条款无关。

Pesce 前面多篇文章都在骂 C++ 本身的缺陷（默认值烂、`friend`、异常、RTTI、模板晦涩），这一篇他换立场：**既然 C++ 不会消失，就研究怎么和它共处**。

## 为什么不能依赖「官方 C++」

和 [[cpp-multi-paradigm-discipline|C++ 多范式纪律]] 的观察一致——没有团队用纯标准 C++ 开发：每个工作室都先把语言砍成一个**子集**，再用宏 / 代码生成 / 库补回缺失的东西（内存管理、序列化、反射、热重载）。所以「工程上的 C++」其实是一门**工作室方言**，通过代码评审和可配置的 lint 工具强制执行。Pesce 2011 年初尝试在 etherpad 上众包这样一套游戏方言，就是 [[sources/c0de517e-survive-cpp-guidelines-experiment]] 的由来。

## 规范条款大多只管「长相」

Pesce 把众包结果看完后反而**失望**：大多数规则只是「减少每分钟的 WTF 数」的美学规则，不改变项目寿命。真正影响生死的只有一件事：**模块之间的耦合面**。

> 如果问题是局部的、被好的抽象藏起来，后面的实现细节就怎么写都行，顶多差一个数量级；但耦合没处理好，整个项目就会慢慢石化成无法修改的大理石雕像。

这与 [[system-decoupling-patterns|Bitsquid 解耦四条]] 的立场完全同构——只是 Pesce 从 C++ 侧、Frykholm 从引擎架构侧谈同一件事。

## 「见到这种代码就该警觉」闪卡

文章下半段是一张**视觉 flashcard**：看到某种写法 → 脑子里应该闪过哪些质疑。条目不长，但每一条都冲着**依赖面管理**：

- **`Foo.h`**——这里面每一个声明都真的要被外部看到吗？能不能分「模块自用 include」和「对外 include」两套目录？是否可以走 PIMPL / 抽象接口？**导出具体类型还是契约？** 有没有在没有两三个真实使用者的情况下提前抽象？
- **`#include`（尤其在头文件里）**——能否用前向声明？这条依赖是静态（模板 / 内联 / 类型）还是动态（接口 / 函数指针）？静态依赖核心库、动态依赖其它模块是默认推荐。
- **`a_type* Foo(...)` 返回裸指针**——谁拥有、谁销毁、什么时候？要不要热重载？要不要改成 [[handle-based-resource-manager|句柄]]？返回的是类型层级里最浅的那一层吗？
- **`class Foo : public Bar` 非接口继承**——如果 `Bar` 不是纯抽象接口，你就同时把 `Foo` 锁在 `Bar` 的接口 **和** 内存布局上。More Effective C++ Item 33：**non-leaf class 应当是 abstract 的**；否则用组合而不是继承。
- **类里的成员函数**——能不能写成外部函数？尤其是私有成员函数——它对头文件的可见性比它该有的还大，不如做成实现文件里的 static 自由函数。
- **`static` 全局**——多模块链接会不会出多份？线程访问安全吗？

这张清单的内核和 [[red-flags|red flags]] / [[minimize-points-and-types-of-failure|最小化失败面]] 精神一致：把抽象经验压缩成**模式匹配反射**，方便在评审或阅读时秒级触发。

## 「不要提前抽象」作为黄金法则

闪卡里反复出现的一条是：**没有两三个真实使用点就不要泛化，没有两三个真实依赖就不要抽象。代码应该去适应情境，不是去预测情境**。这和 [[strategic-programming]] vs [[tactical-programming]] 的讨论同根——Pesce 从模块边界侧反对投机性设计，Ousterhout 从投资回报侧推荐战略性设计，中间的张力在于**抽象的时机**，不在于要不要抽象。

## 落地练习

Pesce 在附言里给的「自测」：**挑一个输入输出清楚的小模块，试着把它拆进 DLL；或者试着用别的语言重写一遍。拆得动 → 项目健康；拆不动 → 就是有问题。** 这是一个可执行、不带道德评判的耦合检测法——比任何风格检查都更有信息量。

## 相关

- [[cpp-multi-paradigm-discipline]] —— 云风 / Meyers 的「C++ 是语言联邦」与团队子集论
- [[system-decoupling-patterns]] —— Frykholm 从引擎架构侧的同一立场
- [[red-flags]]
- [[minimize-points-and-types-of-failure]]
- [[pimpl-vs-pure-virtual]]
- [[header-as-user-manual]]
- [[strategic-programming]] / [[tactical-programming]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-surviving-cpp]]
