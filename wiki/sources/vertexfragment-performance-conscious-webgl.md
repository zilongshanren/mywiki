---
tags: [source, rendering, webgl, javascript, performance]
date: 2026-04-14
sources: 1
---

# Performance Conscious WebGL（Steven Sell / Vertex Fragment）

[[steven-sell]] 发表于 2019 年 5 月的 ramble，记录他从 OpenGL/D3D 背景转向 WebGL 时，在搭建实例化渲染管线过程中踩到的三个反直觉 JavaScript 性能陷阱。

## 摘要

文章围绕作者的 `webgl-experiments` 项目展开，他的实例化渲染器把上千乃至十几万个对象的材质属性打包到同一个 `Float32Array` 里，每帧更新子块并 `bufferData` 提交。在调试过程中，他发现 JavaScript 这层薄薄的胶水带来三种大型性能惩罚。**第一**，内建的 `Float32Array.set` 比手写 `for` 循环慢约 40%，`while` 循环又略快于 `for`。**第二**，用字符串 `"<material_id>:<mesh_id>"` 作 `Map` 键，在 5 万对象下 `addRenderObject` 要 17ms，直接超出 16.67ms 帧预算；换成 [[cantor-szudzik-pairing|Cantor 配对]]整数 key 后降到 1ms，提升 94%。**第三**，最反直觉的是 `super` 调用本身：15 万对象的 `update` 里仅仅调用一次 `super.update(delta)` 就吃掉约 13ms/帧；换成 `SceneObject.prototype.update.call(this, delta)` 就快约 8ms，直接把更新逻辑内联进子类又省下 5ms。jsperf 数据印证：`super` 约 1370 万 ops/sec，`prototype.call` 约 1.22 亿，直接写在子类里约 1.26 亿——整整慢近一个数量级。共同教训是：JIT 会奖励形状稳定、类型稳定、不绕原型链的代码，这常与优雅的 OO 风格相反。

## 关键要点

- `Float32Array.set` 比手写 for 循环慢约 40%，while 循环再快一点
- 字符串 Map key 的哈希与 GC 开销在高频插入场景下非常昂贵
- 用 Cantor/Szudzik 把两个整数 id 打包成一个 key，Map 插入提速 17×
- `super.method()` 需要运行时解析原型链中的方法位置，无法被 IC 缓存，比 `prototype.call` 慢 9× 左右
- 三条教训共同指向：WebGL CPU 侧提交管线是 JIT 敏感区域，避免类型/形状变化和原型链遍历
- 作者背景是 Direct3D/OpenGL，自认“不是 JS 开发者”，这些陷阱都是他从原生图形界切进来时被硬砸出来的

## 链接到的概念

- [[performance-conscious-webgl]]
- [[cantor-szudzik-pairing]]
- [[steven-sell]]
- [[cache-friendliness]]

## 原文

- 链接：https://www.vertexfragment.com/ramblings/performance-conscious-webgl/
- 本地：`raw/articles/vertexfragment.com/2019-05-08_performance-conscious-webgl.md`
- 代码仓库：https://github.com/ssell/webgl-experiments
