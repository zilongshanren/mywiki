---
title: 云风的 BLOG
url: https://blog.codingnow.com/2018/01/
published: '2018-01-31'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### lua 模块管理的一点改进

lua 从 5.2 开始，简化了 5.1 中的模块管理方式，然后一直保持到现在这个样子。

模块用 require 加载，同名模块在一个 vm 中只加载一次，第 2 次开始会返回上次加载的结果。加载模块时会利用 package.path 或 package.cpath 中定义的字符串模板，把模块名转换为文件名，依次尝试打开文件。

我在新项目中，由于整合了不少模块，感觉现有的这套机制有点点不够用。所以我做了一点点小改动，支持了类似 python 的模块管理那样的相对机制。当在一个模块中 require 另一个模块时，会先尝试加载相对路径上的模块，再尝试绝对路径。这样可以方便我们集成独立开始的模块，并放在独立的名字空间中。也方便给模块内置测试子模块。

例如，我独立开发了一个叫 foobar 的模块，它自己有一个子模块叫 foobar.baz ，在集成到系统中时，我希望把它们一起放在 common 名字空间下。使用的时候可以用 require "common.foobar" 来引用。

如果直接用 lua 原生的模块管理机制，我需要修改 foobar 主模块的代码，把里面的 require "foobar.baz" 改成 require "common.foobar.baz" 。同理，如果我不满意 foobar 这个名字，想换名也很麻烦。

所以我希望在新机制下，foobar 的主模块引用自己的子模块 baz，只需要 require "baz" 即可。如果同一目录下有 baz.lua 这个文件，就优先加载它。而外部模块也可以通过 require "foobar.baz" 直接引用这个子模块。

新机制最好可以兼容原生机制，所以不必另起一套模块管理代码。我们要做的只是获取当前模块的名字，在 foobar 主模块中调用 require 时，尝试给参数加上 foobar. 的前缀，引入失败再按原生路径尝试。

好在 lua 原生机制已经把当前模块名作为参数传递进来了。我们只需要实现这么一个函数：

local loaded = package.loaded local searchpath = package.searchpath function import(modname) if modname then local prefix = modname:match "(.*%.).*$" or (modname .. ".") return function(name) local fullname = prefix .. name local m = loaded[fullname] or loaded[name] if m then return m end if searchpath(fullname, package.path) then return require(fullname) else return require(name) end end else return require end end

这个 import 会生成一个模块导入函数，完成以上逻辑。我把这个函数定义成了全局函数，在项目开头就引入。然后，在每个模块的最前面加入这样一行：

local require = import and import(...) or require

如果定义了 import 则用 import 生成一个 require 代替原生版本；否则直接使用原生版本。

另外，我更倾向于用目录来管理模块。即使一个模块只有一个文件，也放在一个单独的目录中。lua 原生模板的约定是 `?/init.lua`

用目录中的 init.lua 作为主模块的入口，我更喜欢 `?/?.lua`

直接用目录名同名文件做主入口。