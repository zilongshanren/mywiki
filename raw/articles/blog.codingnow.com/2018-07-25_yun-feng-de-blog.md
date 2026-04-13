---
title: 云风的 BLOG
url: https://blog.codingnow.com/2018/07/
published: '2018-07-25'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

我为 3d engine 项目设计的[向量运算库](https://blog.codingnow.com/2018/01/lua_linalg.html) 已经用了一段时间了。[在使用过程中也一直在改进](https://blog.codingnow.com/2018/02/linalg_improvement.html) 。从一开始，我就考虑过，这个库的设计主要考量是减少 lua 和 C 交互间的开销，提高内聚性。而易用性方面，计划再上面再做封装。这段时间继续在想怎样从更自然的表达形式转换到这个库的逆波兰指令流上。

大致的方向有两个：

其一，实现一个小语言，用字符串输入表达式组。

其二，利用 Lua 已有的语法解析设施，把 lua 的一个函数翻译成对应的数学运算指令流。

两者都可以看成是一种 jit 的过程，在第一次运行的时候，做一些翻译工作，把要进行的数学运算打包成 C 代码可以处理的指令流，或翻译成现有数学库支持的指令流；或者，增加一个 lua 源码的预处理流程，在预处理阶段做好编译工作（aot）。

这个需求可以分解成三个问题：

首先，如何把更易用的的源码对接到 lua 原生代码。

其次，如何转换为正确的数学运算指令流。

最后，为以上过程选择 jit 或 aot 集成。

经过考量，我觉得第一个问题，如果使用一点奇技淫巧，可以直接利用 lua 已有的语言设施；这样我们就可以避免自己再设计和实现一个小语言。

假设我们需要计算 a * b * c 。这个过程如果是用常规的方式在 lua 中计算。那么至少会有两次关于乘法的函数调用。向量乘法通常是在 C 中实现的，这就涉及 lua 到 C 的交互。为了易用性考虑，我们重载了 * 操作符，这又设计元方法触发的开销。另外 a * b 的结果是一个临时对象，通常无法及时回收，这也增加 gc 的负担。

如果我们通过某种方式把 a * b * c 打包成一个整体，变成 a b c 三个输入量加上一个运算器对象（可以看成是一个 lambda 表达式对象），那么 lua 和 C 的交互就变成了一次，没有元方法触发的额外开销。运算过程中的临时结果也可以在 C 中消化掉。

但是，这里会有一个问题：如果用原生 lua 代码来书写， a * b * c 中的三个参数存在于代码的上下文中，可以是 local 变量也可以是 upvalue 。而和 C 交互则必须是一个独立的函数。C 函数是无法引用 lua 上下文中的 upvalue 的，必须通过参数传入，最终看起来需要是一个原型为 function (a,b,c) 的 C 函数。

即，按最自然的写法：

...
v = a * b * c
...

如果不修改 lua 本身的解析器扩展语法的话，只能变成大致这个样子：

...
v = lambda(function() return a * b * c end)
...

这里把 a * b * c 放在了一个函数中，交给 lambda 去处理，由 lambda 计算出值。

btw, 当然，稍微修改一下，也可以像 moonscript typescript 等扩展 javascript 语法那样，改在预处理阶段处理。

由于 lua 有完善的 upvalue 支持，这里 a b c 放在一个函数中和之前并无太大区别。但是，问题在于，我们的 lambda 这个模块在处理这个运算函数后，需要产生一个运算器 ，最终需要把运算过程交到 C 里。上面已经谈到 C 函数是无法直接访问 lua 层面的 upvalue 的；所以需要 lambda 把 lua 闭包的值读出来，传递给 C 运算器。

实现细节我们放在文末谈。


下面来谈第二个问题，当我们已知 function () return a * b * c end 这么一个 lambda 函数，如何知道这个函数到底做了什么，怎么翻译成最终 C 运算模块可以处理的运算指令流呢？

这里可以用另一个技巧：

我们可以构建一个专用于分析的数据类型充当 a b c 调用它先运行一次。下面是一段示范代码，实际实现要复杂的多：

local lambda_object_mt = {}
local function lambda_object(name)
return setmetatable({ expression = name }, lambda_object_mt)
end
function lambda_object_mt.__mul(a,b)
return lambda_object(a.expression .. "*" .. b.expression)
end

当我们用 `lambda_object`

构建出一个对象传入计算函数时， * 运算并不会真的计算出值来，而是记录下这个计算过程到 object.expression 里。

如果我们把输入参数都替换成这种对象，运行完该函数，就得到了完整的运算流程。

最终看起来是这样的：

local function lambda(func)
local info = debug.getinfo(func,'u')
local n = info.nups
assert(info.nparams == 0 and not info.isvararg and n > 0)
local func_gen = lambda_gen[n]
local call_lambda = func_gen()
for i = 1, n do
debug.upvaluejoin (call_lambda, i+1, func, i)
end
local dummy = func_gen()
for i = 1, n do
debug.upvaluejoin (func, i, dummy, i)
local name = debug.getupvalue(func, i)
debug.setupvalue(func, i, lambda_object(name))
end
local lambda_object = func()
local lambda_func = gen_lambda(lambda_object.expression)
debug.setupvalue(call_lambda, 1, lambda_func)
return call_lambda
end

这就是篇头提到的生成 lambda 函数的完整过程：首先查到输入函数有几个 upvalue ，然后产生对应的桥接闭包，将 upvalue 绑定上去。然后替换掉该输入函数的参数为 `lambda_object`

，模拟运行一次，得到 expression ; 根据这个 expression 生成 （ `gen_lambda`

）一个运算器。


那个可供 lambda 分析的实际做运算的 function 有什么限制？

首先，它不可以有参数，全部用 upvalue 的形式引用上下文中的变量。而这些变量都必须是数学运算用到的数据类型；所以说，这个函数中是不可以调用外部函数的（即不可以引用 `_ENV`

）。

二元参数可以通过计算的数学运算符号完成，例如 + - * / 等等，一元操作也可以利用一元操作符。

当有些操作无法用数学运算符表意的时候，可以用后缀函数来表达，比如：

a.cross(b) 可以表示 a 和 b 的叉乘；a.normalize 表示对 a 归一化。这类表达我们可以通过重载 `__index`

方法来感知到。

函数中可以使用 local 变量，不局限于用单一表达式。例如 local temp = a * b ; return temp * temp ；但不可以使用条件表达式。


接下来的问题是算法最复杂的部分：如何把上面得到的运算过程编译成指令流？这部分我暂时只考虑了算法，还没有完全实现出来，所以就不贴代码了。

这其实是一个编译过程，但并不是从 AST 树生成代码，而是已知若干运算操作以及次序，得到一串基于堆栈（或基于寄存器）的运算指令流。

我们拿到的是若干一元或多元操作。所有的运算都会生成新的值。没有分支。所以处理起来相对容易。

每个运算都可以看成是多个输入量和一个（也可能有多个）输出量。我们对所有的量编号后，就可以对这些运算操作的依赖关系做一个拓扑排序。即，找到什么运算必须先完成（其结果是后续操作的输入量）。

我们的底层计算模块目前是基于堆栈的，那么，处理一个运算时，先后后续运算是否还要重用其输入。如果输入量是最后一次使用，那么直接把输入量和运算操作压入堆栈即可。该运算操作会 pop 出输入，计算完产生出结果压回堆栈；如果后续操作至少会再使用一次输入量，就先在堆栈上复制一次输入量，再进行上述过程。

最后，我们可以得到一组基于堆栈工作的运算指令流。把这个指令流打包成 C 的数据结构，就可以在之后交由 C 运算器计算了。


我们可以看到，编译计算流程这个事情复杂度很高。如果我们每次都去做的话，肯定反不如直接执行原始的 a * b * c 这段 lua 代码来的快。但实际上，这段计算过程的编译只需要做一次就够了，而后续则只需要绑定需要的参数。

为了解决这个问题需要使用一点奇技淫巧。

由于我们的 lambda 表达式是直接书写在 lua 代码的上下文中的，lua 其实为这段代码生成了唯一的函数原型。每次运行到这里的时候，再将这个原型和 upvalue 一起打包成函数闭包。如果我们可以用函数原型做 key ，cache 住编译过程，就不需要每次都做编译工作了。

不幸的是，我们无法直接用 lua 公开 api 获取函数原型对象。绕过公开 api 直接访问 lua 底层数据结构，可以解决这个问题。我在 [如何让 lua 做尽量正确的热更新](https://blog.codingnow.com/2016/11/lua_update.html) 提到了这个方法，这里再次摘录一下：

static int
lproto(lua_State *L) {
if (!lua_isfunction(L, 1) || lua_iscfunction(L,1))
return 0;
const LClosure *c = lua_topointer(L,1);
lua_pushlightuserdata(L, c->p);
lua_pushinteger(L, c->p->sizep);
return 2;
}

这个函数可以返回一个 lua 闭包中引用的原型对象的指针，我们不会直接使用这个指针引用的内容，只是做 key 用足够了。（提醒一点风险：如果整个代码块被回收，指针可能被复用，通常不太可能发生）

在 lambda 的实现中，我们可以先查询对应的原型是否被翻译过，得到编译好的结果后，将传入的 lua 运算器函数的 upvalue 取出，当成参数传递给编译后的 C 运算函数即可。

如果采用 aot 方案的话，我想可以把 lambda(function() return a * b * c end) 改写成 [[[ a * b * c ]]] ，增加一个预编译阶段，转译成 function() return a * b * c end ，做一次预编译工作，再生成 calc( "xxxx", a, b , c) 。这里 calc 就是最终的 C 运算函数，"xxxx" 是编译后的计算指令流。