---
tags: [source, bitsquid, javascript, 热重载, 原型]
date: 2026-04-19
sources: 1
---

# Hot Reloadable JavaScript, Batman!（Niklas / Bitsquid）

[[niklas-frykholm|Niklas]] 2016 年 1 月在 Bitsquid Blog 上发的一篇小品文——把浏览器 JavaScript 当作最便宜的原型环境，顺手写了个 30 行左右的**最小化热重载机制**。一半是技术 note，一半是"为什么 productivity software 都不好用"的吐槽。

## 摘要

Niklas 承认 JavaScript 有一堆 WTF（`"0" == false`、每个函数又是构造器又是方法、`hasOwnProperty` 污染等等）——但作为**原型和 demo 环境**它赢了所有对手：自带 UI、2D/3D 绘图、debugger、REPL、跨平台、"做完发个链接就能给人看"。他越用越发现 JavaScript 取代了他以前用 Visio / Excel / Photoshop 的很多场景：画流程图、做 slide、画折线图——"用程序做而不是产出软件做更有趣"。

文章的核心 trick：**动态往 `<head>` 塞 `<script>` 节点就会触发求值**，之后 `removeChild` 不影响已执行的代码。所以一个 30 行的 `require(s)` + `setInterval(reload, 250)` 就实现了"文件改了就热重载"的体验。作者甚至特地用 `?t=performance.now()` 绕缓存、用 `window.has_reload` 守卫避免 interval 自乘"蒸发宇宙"。状态保留靠 `window.state = window.state || {}`；Safari / Chrome 对 `class` 重定义行为不一致要用 `var Rect = class {}` 这种 workaround。

结尾是典型 Niklas 吐槽：他说自己下一份 slide deck 要**直接用 JavaScript 写**不用 Remark.js——"frameworks? I don't need no stinking frameworks"。

## 关键要点

- 动态添加再移除 `<script>` 节点仍然会 eval——heat reload 的技术底座就是这个。
- `?t=performance.now()` 做 cache-busting；file watcher 的复杂度作者懒得要。
- `window.state` pattern 跨 reload 保留状态，对 slide page / demo 参数都够用。
- 浏览器差异：Chrome 不允许重复 `class Foo {}`，改写成 `var Foo = class {}` 可解。
- **Bitsquid 式工程哲学**：能用最糙的 polling 跑通整个反馈环就不要 file watcher；能用 30 行代码做成就不要框架。
- 副线吐槽：PowerPoint / Visio / Excel 都很烂，markdown / canvas / remark.js 更好用；程序员应该把"sysadmin 式编程"的时间降到最低。

## 链接到的概念

- [[javascript-hot-reload-dom-script]]
- [[live-editing-taxonomy-2010]]
- [[binary-hot-reload]]
- [[niklas-frykholm]]

## 原文

- 链接：https://bitsquid.blogspot.com/2016/01/hot-reloadable-javascript-batman.html
- 本地：`raw/articles/bitsquid.blogspot.com/2016-01-31_hot-reloadable-javascript-batman.md`
