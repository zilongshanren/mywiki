---
title: 云风的 BLOG
url: https://blog.codingnow.com/2018/12/
published: '2018-12-18'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### lua 5.4 可能会增加 to-be-closed 特性

如果你有关注 lua 在 github 上的仓库，就会发现，最近一段时间增加了一个新特性：to-be-closed 的 local 变量。

鉴于历史上 lua 每次的大版本开发过程中都会增加很多有趣的特性，却无法保持到版本正式发布。本文也只是介绍一下这个有趣的特性，并不保证它一定会被纳入语言标准。正式的发布版中即使有这个特性，语法上也可能有所不同。

我认为 Lua 加入这个特性的动机是它缺乏 RAII 机制。过去，我们必须用 pcall 来确保一段代码运行完毕，然后再清理相关的资源。这会导致代码实现繁琐，几乎无法正确实施。比如，如果你用 C 函数申请了一块资源，期望在使用完毕后可以清除干净，过去就只能依赖 __gc 方法。但 gc 的时机不可控，往往无法及时清理。如果你把释放过程放在运行过程的末尾，是很难确定整个运行过程中没有异常跳出的可能，那样就无法执行最后的释放流程。

lua 5.4 预计要增加的 to-be-closed 特性，是允许给堆栈上的 local 变量添加一个 to-be-closed 属性。有了这个属性的 local 变量，一旦超出它的作用域，就立刻运行一段相关的代码。这很像是结合了 golang 的 defer 和 C++ 的析构函数。

在 lua 代码中，我们可以使用 local *toclose c = function(errobj) ... end 来将一个 local 变量 c 定义成 to-be-closed 的。这里 c 是一个 function ，在 c 出了作用域后，它就会被调用。这很像 golang 的 defer 。

如果正常出作用域：比如是通过 goto break return 等，函数的参数为 nil ；如果是通过 error 异常跳出，那么 error 对象就会作为第一个参数传入。

这里的 to-be-closed 变量 c 也可以是非 function 类型，这时，触发的就是它的 `__close`

元方法。这很接近 C++ 的析构函数的行为。不过它并不等价于析构函数，因为对象还可以继续被使用。

触发 `__close`

时，会多传一个参数是对象本身。有了这个机制，我们就不再担心 io.open 这种临时打开的文件无法即使关闭了，因为 FILE 对象默认会加上 `__close`

方法，你需要做的是在需要的地方加上 *toclose 声明。

有了 to-be-closed 后，for 迭代器就可以实现的更完备了。for 会将迭代器声明为 to-be-closed 的，像 lfs.dir 这种操作系统目录迭代器，你就不会担心是否能及时关闭目录对象了。因为无论任何原因跳出 for 循环，迭代器的 `__close`

方法都会被调用。

你也有方法阻止 `__close`

方法调用，那就是使用 coroutine 来包装一个运行过程。如果使用 yield 跳出，是不会处罚 `__close`

方法的。新的 coroutine 库增加了 kill 方法来一次性触发所有挂起的 `__close`

并可以让线程对象可复用。

to-be-closed 也可以通过 C API `lua_toclose`

声明。有了这个，我们可以更放心的在 C 代码中申请临时资源，而不必担心某个 api 调用会抛出 error ，导致临时资源没有释放干净。在过去，我们通常是利用 `lua_newuserdata`

来申请临时内存，这往往无法及时回收。