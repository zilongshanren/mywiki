---
title: 云风的 BLOG
url: https://blog.codingnow.com/2025/12/skynet_lua_550.html
published: '2025-12-23'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### Skynet 升级到 Lua 5.5.0

Lua 5.5.0 已经正式发布。所以，skynet 的 Lua 版本也随之升级。

skynet 维护了一份修改版的 Lua ，允许在多个虚拟机之间共享函数原型。这可以节省初始化 Lua 服务的时间，减少内存占用。

跨虚拟机共享函数原型最困难的部分是函数原型会引用常量字符串，而 Lua 在处理短字符串时，需要在虚拟机内部做 interning 。所以 skynet 的这个 patch 主要解决的是正确处理被 interning 的短字符串和从外部导入的函数原型中包含的字符串共存的问题。具体方法[记录在这篇 blog 中](https://blog.codingnow.com/2019/06/string_comparison.html)。

这个 patch 的副产品是允许在多个 Lua VM 间共享常量表。打了这个 patch 后，就可以使用 skynet.sharetable 这个库共享只读常量表了。

这次 Lua 5.5 的更新引入了 external strings 这个特性，已经大幅度提升了 Lua 加载字节码的速度。我比较倾向于在未来不再依赖额外的 patch 减少维护成本。所以建议新项目避免再使用共享常量表，减少对 patch 过的 Lua 版本的依赖。

Lua 5.5 基本上兼容 Lua 5.4 ，我认为绝大多数 skynet 项目都不需要特别改动。但在升级后，还是建议充分测试。注意：更新仓库后，需要用 make cleanall 清除 lua 的编译中间文件，强制 Lua 重新编译。直接 make clean 并不清理它们。

Lua 5.5 有几处更新我认为值得升级：

增加了 global 关键字。对减少拼写错误引起的 bug 很有帮助。skynet 自身代码暂时还没有使用，但后续会逐步添加。

分代 GC 的主流程改为步进式进行。过去版本如果采用分代模式，对于内存占用较大的服务，容易造成停顿。所以这类服务往往需要切换为步进模式。升级到 Lua 5.5 后，应该就不需要了。

新的不定长参数语法 ...args 可以用 table 形式访问不定长参数列表。以后可以简化一部分 skynet 中 Lua 代码的实现。


## Comments

Posted by: itt | (9) January 19, 2026 03:45 PM

Posted by: xiazaiall | (8) January 10, 2026 07:16 PM

Posted by: Cloud | (7) January 8, 2026 03:04 PM

Posted by: charles | (6) December 30, 2025 10:52 PM

Posted by: shan | (5) December 26, 2025 09:53 AM

Posted by: Cloud | (4) December 26, 2025 09:35 AM

Posted by: loveyf | (3) December 25, 2025 06:36 PM

Posted by: hanxi | (2) December 25, 2025 06:26 PM

Posted by: will liu | (1) December 23, 2025 05:47 PM