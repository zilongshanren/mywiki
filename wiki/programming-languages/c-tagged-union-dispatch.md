---
tags: [c, 接口设计, 类型安全, 联合体, 消息分发]
date: 2026-04-14
sources: 1
---

# C 语言用 tagged union 做类型安全的消息分发

C 语言里要把一个统一的接口接到多种"形参不一致"的下游函数上，常见做法有三种：传 `void *` + 强转、用 va_list、或者像 Win32 那样把所有参数压扁成 `WPARAM` / `LPARAM` 两个 32 位整数。这些做法的共同问题是**全部抹掉了类型信息**，编译器再也帮不了你。[[cloudwu]] 在 2010 年的一篇短文里整理了 X-Window 的另一种做法：在粘合层定义一个**带 type 字段的 union of structs**，让编译器继续替你把关。

## 为什么 C 的"弱类型函数指针"不实用

C89 允许这样写：`void foo();`——参数列表为空意味着"参数未定"，而不是"无参数"，所以 `void foo(int)` 与 `void foo(void *)` 都能"无害"地塞进它，正如所有具体指针类型都能塞进 `void *`。注意这与"严格无参数" `void foo(void)` 不同。这种弱类型函数声明在实践中很少派上用场，因为 C 程序员**没法主动控制函数调用时参数的压栈**——你不可能根据上下文动态决定怎么传参。需要逐级转发参数时，大家用的也是 `va_list`，于是出现了那种为了能被封装而被迫成对提供的接口：`printf` 之外还要有 `vprintf`。

C++ 的回应是用类模拟函数：重载 `operator()` 把对象当函数用，美其名 functor / 仿函数；或者干脆撕掉糖衣，直接用类继承去定义接口。但 C 还有自己的优雅解法。

## XEvent 的做法：union of structs，每一支带 type 头

Xlib 把所有可能的窗口事件（按键、鼠标、曝光、客户端消息……）打包成一个 `XEvent` union，每个分支是独立的 `XKeyEvent / XButtonEvent / XClientMessageEvent` 等 struct，每个 struct 头部都有一个 `type` 字段。事件循环只接收 `XEvent *`，再按 `event.type` 分发到 `event.xkey.keycode` 或 `event.xbutton.x` 等具体字段。比起 Windows 的 `WPARAM` / `LPARAM`，这种写法对 C 程序员"亲合力"大得多，也更**类型安全**——访问字段时编译器仍能查类型，而不是把一切压进两个 32 位整数里。

## 推广：粘合层的统一接口

把这套手法抽象出来，[[cloudwu]] 给的建议是：当你需要粘合多个对外接口形态不一的模块时，

1. 在粘合层里定义一个 union；
2. 把每一组可能的实参列表打包成一个 struct，所有这些 struct 都列入这个 union；
3. 每个 struct 的头部留一个 `type` 字段，便于分发；
4. 粘合层的统一接口收的就是这个 union 的指针。

它的本质是**把"由编译器在调用现场逐个压栈参数"这件事，改由程序员主动填一个结构体**。利用 struct 的成员类型严格性保证了"传参类型安全"，再用 union 的语法把不同的参数组联合成同一种顶层类型，让上层只需要面对一个统一的函数签名。

## 不只是消息：传 struct 比传一堆参数更常见

即便没有"多种参数组"的需求，把一个 struct/union 指针塞给 API 也是 C 接口设计的家常便饭。Berkeley sockets 的 `connect(int, const struct sockaddr *, socklen_t)` 就是同一种思路：不同地址族的 `sockaddr_in / sockaddr_in6 / sockaddr_un` 共享 `sa_family_t` 头部、各自延伸出协议特定字段，调用者按需打包，内核按 `sa_family` 分发。这种"接口形态稳定、参数变体灵活"的 API 模式，正是 [[c-opaque-struct-modules]] 与 [[c-interface-oop]] 之外，C 语言下另一种朴素而有效的"用类型系统兜底"的设计语汇。

## 相关

- [[cloudwu]]
- [[c-opaque-struct-modules]]
- [[c-interface-oop]]
- [[c-serialization-metadata]]
- [[interface-vs-implementation]]
- [[modular-design]]

## Sources

- [[sources/cloudwu-c-tagged-union-dispatch]]
