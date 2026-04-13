---
title: 云风的 BLOG
url: https://blog.codingnow.com/2017/10/
published: '2017-10-31'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

前两年有同学给我推荐了 [BGFX](https://github.com/cloudwu/bgfx) 这个库，第一眼被它吸引是它的口号："Bring Your Own Engine/Framework" style rendering library 。这动不动就说自己是 3d engine 的时代，好好做好一个渲染库，仅仅做好渲染库，是多难得的一件事情。

今年国庆节的时候，偶然间我又翻到这个仓库，居然作者一直在更新。坚持了五年，一直在维护这么个小玩意，让我对这个项目多了点信心。节后我饶有兴趣的研究了一下它的代码。

现在我觉得，这个库的设计思想非常对我的胃口，核心部分几乎没有多余的东西：数据计算、平台 API 支持、数据持久化格式支持、等等都没有放在核心部分。它仅仅只做了一件事：把不同平台的图形 API ：Direct X 、OpenGL 等等整合为一套统一的接口，方便在此基础上开发跨平台的 3d 图形程序。不同平台的 3d api 的差异，正是 3d 游戏开发中最脏最累的活了。

虽然 BGFX 已经有人写了 lua binding 库，但我觉得不太合我意：封装的不是很 lua 化，就是简单的 C api 包装，而且 api 覆盖也不全面。

我花了半个月的时间，重新制作了一套 lua 封装。

因为 BGFX 仅仅是渲染库，并不负责创建窗口，获取输入消息。所以我另外整合了 iup 作为窗口框架的支持。因为 iup 已经有很好的原生界面的支持，我在改写 BGFX 自带的 examples 时，就放弃了使用原本例子中用到的 imgui ，转而直接使用 iup 。

在逐个改写 BGFX 自带的例子的过程中，我了解了 bgfx 的架构和 api 设计思路，结合我对 lua 的使用经验，封装为类似但不完全一致的 lua api 。

比如原本 bgfx 的 C/C++ 接口用 `VertexDecl::begin`

`VertexDecl::add`

`VertexDecl::end`

等一组 api 来构建顶点结构。这是因为 C/C++ 语言本身不太适合描述这类数据。但 lua 有很灵活的数据结构支持，故而只需要一个 api 就可以搞定。

又比如 C/C++ 中用位操作组合预定义的宏来组合整数 flags 是一种常见手法，但是在 lua 中即不那么直观、也未必高效。换成字符串描述就会更好。

C++ 可以重载同名函数、可以把函数调用参数的最后几个设置默认值；而 Lua 则更加灵活，只要类型不同，默认值不一定限制在调用参数的最后几个。

Lua 有一些缺陷：不方便直接操作内存。这回导致直接翻译那些 BGFX 中和内存地址有关，例如更新动态 buffer 这种 API 便不适用了，需要找到合适的方法来封装。

我在做这项封装工作的流程中采用的是挑选有代表性的 example 翻译成 lua 版本。在人工转译的过程中，会发现依赖 BGFX 的 C/C++ API ，就随之实现这些 API 的 lua 封装版本。所以这个封装库是随着转译 examples 逐渐增加而逐步完善的。


我目前的工作环境是 windows 10 64bit ，使用 mingw64 编译器。虽然理论上这是一个跨平台库，我是用的 iup 也是跨平台的。但是目前我尚未有精力去折腾多平台的构建脚本。

有兴趣玩一下，却搞不定编译的同学可以直接下载我编译好的动态库版本。只需要写 lua 脚本就可以试用了。[github 仓库在这里](https://github.com/cloudwu/lua-bgfx)。 我在 [release](https://github.com/cloudwu/lua-bgfx/releases) 页面上传了我自己编译好的二进制文件。

注意：直接行对行改写的 lua 版本的 example 有时会很低效，尤其是需要做大量数学运算的，例如 02 metaballs 这个例子就比 C 版本慢很多。如果需要兼顾效率，需要重新按 lua 的风格重新组织代码，并把重度计算的地方用 C 写一个库去计算供 lua 调用。

不过大多数 example 运行起来会发现性能和 C/C++ 版本相差无几，完全可以实用。对于做原型，尝试新的图形算法来说，lua 带来的开发便利性无可比拟。