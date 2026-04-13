---
title: 云风的 BLOG
url: https://blog.codingnow.com/cat2/go_/
published: '2022-08-12'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

这几天认真玩起了 [Go](http://golang.org)。所谓认真玩，就是拿 Go 写点程序，前后大约两千行吧。

据说 Go 的最佳开发平台是 Mac OS ，我没有。其次应该是 Linux 。Windows 版还没全部搞定，但是也可以用了。如果你用 google 搜索，很容易去到一个叫 [go-windows](http://code.google.com/p/go-windows/) 的开源项目上。千万别上当，这是个废弃的项目。如果你用这个，很多库都没有，而且语法也是老的。我在 Windows 下甚至不能正确链接自己写的多个 package 。活跃的 Windows 版是 [gomingw](http://code.google.com/p/gomingw) ，对于 Windows 用户，装一个 mingw32 以后就可以开始玩了。

就三天来实战经历，我喜欢上这门新语言有如下原因：

mix-in 的接口风格。非常接近于[我在用 C 时惯用的面向对象风格](http://blog.codingnow.com/2010/03/object_oriented_programming_in_c.html)。有语法上的支持要舒服多了。以平坦的方式编写函数，没有层次。而后用 interface 把需要的功能聚合在一起。没有继承层次，只有组合功能。

强类型系统。使得犯错误的机会大大降低。正确通过编译，几乎就没有什么 bug 了。而编写程序又有点使用 lua 这种动态语言的感觉，总之，写起来很舒服。

内置的 string / slice 类型，以及 gc 。这是我觉得现代编程必须的东西。手工管理未必有更高的效率，但一定有更多的出错机会。至少，我一直主张有一个方便的 string 不变量的基本类型的（[参见这一篇](http://blog.codingnow.com/2009/08/getter_setter.html)）。

defer 是个有趣使用的东西，用它来实现 RAII 比 C++ 利用栈上对象的析构函数的 trick 方案让人塌实多了。go 在语言设计上是很吝啬新的关键字的。但多出一个关键字 defer ，并用内建函数 panic / recover 来解决许多看似应该用 exception 解决的问题要漂亮的多。

zero 初始化。我一直觉得 C++ 的构造函数特别多余。按我用 C 的惯例，一切数据结构都应该用 0 初始化。所以 C 里有 calloc 这个函数。go 把这点贯彻了。不会再有未定义的数据。

包系统特别的好。而且严格定义了包的初始化过程，即 init 函数。在我自己的 C 语言构建的项目中，实现了几乎一样的机制，甚至也叫 init 。但是有语言层面的支持就是好。对，只有 init 没有 exit 。正合我意。

goroutine 是个相当有用的设计。8 年前，我给 C 实现了 coroutine 库，并用在项目里，并坚信，程序就应该这么写。但是没有语言级的支持，用起来还是很麻烦。goroutine 不仅简化了许多业务逻辑的编写，而且天生就是为并发编程而生的。select/chan 可能是唯一正确的并发编程的模型。Erlang 还是太小众了，而 Go 可以延用 Erlang 的模型，却有着纯正的 C 语言血统，我想会被更多人接受的。虽然 Go 依然可以用共享状态加锁的方案，但不推荐使用。chan 用习惯了，还是相当方便的。

{ 要不要独立占一行的信仰之争终于结束了。还记得前段时间有位同学来 email 指责我开源的代码没有章法。程序写的太乱。他的理由就是，我的 { 都没有独占一行。好了，争论可以结束了。在 Go 里，如果你把 { 从 if/for 语言的行末去掉，放在下一行。编译器是不会让你通过的。（除非你再加一个 ; ）我很欣慰 ;)

我发现我花了四年时间锤炼自己用 C 语言构建系统的能力，试图找到一个规范，可以更好的编写软件。结果发现只是对 Go 的模仿。缺乏语言层面的支持，只能是一个拙劣的模仿。