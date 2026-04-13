---
title: 云风的 BLOG
url: https://blog.codingnow.com/2025/08/
published: '2025-08-26'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 在 Lua 中定义类型的简单方法

我通常用 Lua 定义一个类型只需要这样做：

-- 定义一个 object 的新类型 local object = {}; object.__index = object -- 定义构建 object 的函数 local function new_object(self) return setmetatable(self or {}, object) end -- 给 object 添加一个 get 方法 function object:get(what) return self[what] end -- 测试一下 local obj = new_object { x = "x" } assert(obj:get "x" == "x")

这样写足够简单，如果写熟了就不用额外再做封装。如果一定要做一点封装，可以这样：

local class = {}; setmetatable(class, class) function class:__index(name) local class_methods = {}; class_methods.__index = class_methods local class_object = {} local class_meta = { __newindex = class_methods, __index = class_methods, __call = function(self, init) return setmetatable(init or {}, class_methods) end } class[name] = setmetatable(class_object, class_meta) return class_object end

封装的意义在于：你可以通过上面这个 class 模块定义新的类型，且能通过它用类型名找到所有定义的新类型。而上面的第一版通常用于放在独立模块文件中，依赖 lua 的模块机制找到 `new_object`

这个构建方法。

而封装后可以这样用：

-- 定义一个名为 object 的新类型，并添加 get 方法： local object = class.object function object:get(what) return self[what] end -- 创建新的 object 实例，测试方法 object:get local obj = class.object { x = "x" } assert(obj:get "x" == "x")

如果觉得 `local object = class.object`

的写法容易产生歧义，也可以加一点小技巧（同时提供特殊的代码文本模式，方便日后搜索代码）：

function class:__call(name) return self[name] end -- 等价于 local object = class.object local object = class "object"

如果我们要定义的类型是一个容器该怎么做好？

容器的数据结构有两个部分：容纳数据的集合和容器的元数据。之前，我通常把元数据直接放在对象实例中，把集合对象看作元数据中的一个。

比如定义一个集合类型 set 以及两个方法 get 和 set ：

local set = class "set" function set:new() return self { container = {}, n = 0, } end function set:set(key, value) local container = self.container if value == nil then if container[key] ~= nil then container[key] = nil self.n = self.n - 1 end else if container[key] == nil then self.n = self.n + 1 end container[key] = value end end function set:get(key) return self.container[key] end

真正集合容器在 self.container 里，这里 self.n 是集合的元信息，即集合元素的个数。注意这里集合类型需要有一个构造函数 new ，因为它在构造实例时必须初始化 .n 和 .container 。这里的 set:new 构造函数调用了前面生成的 class.set 这个默认构造行为。

测试一下：注意这里用 class.set:new() 调用了构造函数。它等价于 class.set { container = {}, n = 0 } ，因为 .container 和 .n 属于实现细节，所以不推荐使用。

local obj = class.set:new() obj:set("x", 1) obj:set("y", 2) assert(obj.n == 2) assert(obj:get "x" == 1)

如果使用者要直接访问容器的内部数据结构，它可以用 obj.container 找到引用。但我们可能希望 set 表现得更像 lua table 一样，所以也可能想这样实现：

local set2 = class "set2" function set2:new() return self { _n = 0, } end function set2:set(key, value) if value == nil then if self[key] ~= nil then self[key] = nil self._n = self._n - 1 end else if self[key] == nil then self._n = self._n + 1 end self[key] = value end end -- 测试一下 local obj = class.set2:new() obj:set("x", 1) obj:set("y", 2) assert(obj._n == 2) assert(obj.x == 1)

这个版本去掉了 .container 而直接把数据放在 self 里。所以不再需要 get 方法。为了让元数据 n 区分开，所以改为了 ._n 。

如果规范了命名规则，用下划线区分元数据未尝不是一个好的方法，但在迭代容器的时候会需要剔除它们比较麻烦。所以有时候我们会把元数据外置，这里就需要用到 lua 5.2 引入的 ephemeron table 来帮助 gc 。

local set3 = class "set3" local SET = setmetatable({}, { __mode = "k" }) function set3:new() local object = self() SET[object] = { n = 0 } return object end function set3:set(key, value) if value == nil then if self[key] ~= nil then self[key] = nil SET[self].n = SET[self].n - 1 end else if self[key] == nil then SET[self].n = SET[self].n + 1 end self[key] = value end end function set3:__len() return SET[self].n end -- 测试一下： local obj = class.set3:new() obj:set("x", 1) obj:set("y", 2) assert(#obj == 2) assert(obj.x == 1) -- 迭代 obj 已经看不到元数据了。 for k,v in pairs(obj) do print(k,v) end

由于 ._n 外部不可见，所以我们用 #obj 来获取它。

如果不想用 ephemeron table 管理元数据，是否有什么简单的方法剔除元数据呢？

最近发现另一个小技巧，那就是使用 false 作为元数据的 key ：

local set4 = class "set4" function set4:new() return self { [false] = 0, } end function set4:set(key, value) if value == nil then if self[key] ~= nil then self[key] = nil self[false] = self[false] - 1 end else if self[key] == nil then self[false] = self[false] + 1 end self[key] = value end end function set4:__len() return self[false] end -- 测试一下 local obj = class.set4:new() obj:set("x", 1) obj:set("y", 2) for k,v in pairs(obj) do if k then print(k,v) end end

这个版本几乎和第二版相同，不同的地方只是在于把 ["_n"] 换成了 [false] 。这里只有一个元数据，如果有多个，可以把 [false] = {} 设为一张表。

这样就不需要额外使用弱表，在迭代时也只需要判断 key 是否为真来剔除它。虽然有这么一点点局限，但贵在足够简单。

当然你也可以给它再定义一个 `__pairs`

方法滤掉 false ：

function set4:next(k) local nk, v = next(self, k) if nk == false then return next(self, false) else return nk, v end end function set4:__pairs() return self.next, self end

或者给加一种叫 class.container 的类型创建方法

local function container_next(self, k) local nk, v = next(self, k) if nk == false then return next(self, false) else return nk, v end end function class.container(name) local container_class = class[name] function container_class:__pairs() return container_next, self end return container_class end

如果你不需要 class 提供的默认构造函数，同时不喜欢定义一个新的 new 方法，也可以直接覆盖默认构造函数（同时避免别处再给它增加新的方法）：

local set5 = class.container "set5" function set5:set(key, value) if value == nil then if self[key] ~= nil then self[key] = nil self[false] = self[false] - 1 end else if self[key] == nil then self[false] = self[false] + 1 end self[key] = value end end function set5:__len() return self[false] end function class.set5() return set5 { [false] = 0, } end local obj = class.set5() obj:set("x", 1) obj:set("y", 2) for k,v in pairs(obj) do print(k,v) end