---
tags: [rendering, webgl, javascript, performance, instanced-rendering]
date: 2026-04-14
sources: 1
---

# 讲究性能的 WebGL

WebGL 是一套把 OpenGL ES 搬到浏览器里的接口，没有对应的 WebD3D 可选。因此当图形程序员从 Direct3D 或原生 OpenGL 转向浏览器时，很快就会撞上 JavaScript 的“又无类型又充满隐式代价”的一面——作者 [[steven-sell]] 记录了他搭建实例化渲染管线时遇到的三个最反直觉的性能陷阱。

## `Float32Array.set` 比手写循环慢

在实例化管线里，所有对象的材质参数（`vec3`、`mat4` 等）都打包进同一个 `Float32Array`，每帧需要把子块写进去，再交给 `gl.bufferData` 传到 GPU。直觉上应当用标准提供的 `Float32Array.set(...)` 批量拷贝，毕竟那是“内建的、理应最快”的路径。

实测结果相反：逐元素 `for` 循环手写赋值比 `set` **快约 40%**，而 `while` 循环又略优于 `for`。这与经验相悖，但在 V8 这类 JIT 引擎面前，原生 typed-array 方法的调用栈、参数校验和边界处理成本并不总能被常数折叠消除。对热路径而言，“丑一点”的手写循环反而稳定。

## 字符串作为 `Map` key 的隐性代价

实例化管线按“相同材质 + 相同网格”分组绘制，最直接的 key 写法是拼接一个字符串 `"<material_id>:<mesh_id>"`。直觉告诉你“慢一点点”，实际测出的“一点点”是：**5 万个对象的 `addRenderObject` 就吃掉 17ms**——一帧预算 16.67ms 直接爆掉。

解决方法是给材质和网格分配整数 id，再用一个 [[cantor-szudzik-pairing]] 之类的 pairing function 把这两个整数打包成单个整数 key。同样 5 万对象下 `addRenderObject` 降到 **1ms，提升约 94%**。jsperf 上的直接对比是：字符串 key 约 3500 万 ops/sec，Cantor 整数 key 约 1.1 亿 ops/sec。在高频插入/查找场景下，任何把 key 设计为字符串的方案都应引起警觉。

## `super` 调用的开销

JavaScript 的 class 语法糖背后是原型链，而 `super.xxx(...)` 的语义远比看上去复杂。作者在 15 万个对象的 `update` 里只做了“通过 `super` 前进一个计时器、再调用 `translate`”这点工作，却看到 15ms 的开销。把 `super.update(delta)` 换成 `SceneObject.prototype.update.call(this, delta)` 立即省下 **8ms**；再把父类那一行挪进子类自己，又省下 **5ms**——一次 `super` 调用合计带来 **13ms / 帧**的惩罚。

jsperf 的对比印证了这一点：

- `super`: 1370 万 ops/sec
- `prototype`: 1.216 亿 ops/sec
- self (直接写在子类里): 1.258 亿 ops/sec

`super` 相比直接的 `prototype.call` 慢了近一个数量级。背后的原因是 `super` 需要在运行时解析“当前方法所在类在原型链上的位置”，无法像普通属性那样被内联缓存命中。在非热路径上这点差别可以忽略，但在 N 十万次调用的逐帧循环里就是性能分水岭。

## 一条共同经验

三个陷阱都指向同一个教训：在 [[game-engine]] 的热循环里，不要信任任何“看起来现代、看起来应该被引擎优化好了”的 API。JIT 会奖励**形状稳定、类型稳定、不绕原型链**的代码，它往往和“漂亮的 OO 代码”正好相反。对于 [[gpu-latency-hiding]] 之上运行的 CPU 侧提交管线，这条原则尤其重要——GPU 再闲，CPU 侧的 draw-call 组装慢一帧照样掉帧。

## Sources

- [[sources/vertexfragment-performance-conscious-webgl]]
