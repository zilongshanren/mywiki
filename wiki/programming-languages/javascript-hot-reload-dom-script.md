---
tags: [javascript, 热重载, 原型, dom, bitsquid]
date: 2026-04-19
sources: 1
---

# JavaScript 最小化热重载（动态 script node + polling）

2016 年 1 月 [[niklas-frykholm]] 在 Bitsquid Blog 上写的一篇小 trick：**不靠 webpack、不靠 budo、不靠任何打包器**，用 30 行左右 JavaScript 就做出了能在浏览器里实时热重载自己代码的原型环境。它的价值不在技术多新，而在**用最裸的浏览器原语把"改文件→立刻看到效果"这件事做成了**——一种非常 Bitsquid 的工程审美。

## 核心招数：往 `<head>` 里塞一个 script 节点就会执行

```javascript
function require(s) {
  var script = document.createElement("script");
  script.src = s + "?" + performance.now();
  script.type = "text/javascript";
  var head = document.getElementsByTagName("head")[0];
  head.appendChild(script);
  head.removeChild(script);   // 立即移除，代码已被 eval，不影响运行
}
```

两个细节值得品：
- `?performance.now()` 作为 query string 绕过浏览器缓存，强制每次都去 fetch 新版本。
- `appendChild` 触发 eval，之后 `removeChild` 不会撤销已发生的求值——DOM 和 JS 的耦合在这里是可拆的。

## Polling 而不是 file watcher

```javascript
function reload() {
  require("index.js");
  render();
}
if (!window.has_reload) {
  window.has_reload = true;
  window.setInterval(reload, 250);
}
```

每 250 ms 无脑重新加载一次 `index.js`。作者自嘲"如果我笔电够强，这个自加载的 interval 会把宇宙蒸发掉"，所以用 `window.has_reload` 守卫确保只挂一次定时器。理论上该用 file watcher + WebSocket，但那"就开始复杂了，我喜欢简单"。这正是 [[niklas-frykholm|Niklas]] 一贯的工程味：**先用最糙的轮询跑通整条反馈环，再谈优化**。

## 重新渲染前要清 DOM

每次 reload 后 `render()` 先清空 `<body>` 再重建 DOM：

```javascript
while (body.hasChildNodes()) body.removeChild(body.lastChild);
```

否则每帧 DOM 节点线性增长——比自增 timer 的"指数级"温和，但仍然不可接受。

## 跨 reload 的状态保留

- 把所有运行时状态挂到 `window.state`：`window.state = window.state || {}`——首次初始化，后续 reload 保留。幻灯片 deck 的当前 slide 编号、游戏 demo 的相机位置，都这么传递。
- 浏览器差异：Safari 允许重复定义 `class Rect {}`，Chrome Canary 报错。改写成 `var Rect = class { ... }` 双方都接受——这恰好揭露了 ES6 `class` 语法糖的不对称性：变量重赋值可以，class 重声明不行。

## 为什么这套能工作

这是[[live-editing-taxonomy-2010|Pesce 2010 热重载分类]]里的 **code hot-swap** 档在动态语言下的最小实现。它之所以简单，是因为 JavaScript 同时满足三个条件：
1. 所有"定义"都是对 window 的赋值——重赋值即热更新。
2. 浏览器自带 JIT、eval、DOM 双缓冲——显示不闪。
3. 脚本通过 DOM 而非文件系统加载——`?t=` 破缓存足够。

在 C++ 里做同样事情需要 DLL 卸载 / 符号 patch / vtable 重绑，工程债多出两个数量级（见 [[binary-hot-reload]]）。

## 用来替代"生产力软件"

文章真正的骚操作不是热重载本身，而是把这套东西用到极致：
- 拿 canvas 画**流程图**代替 Visio；
- 拿 HTML 写**幻灯片**代替 PowerPoint（作者甚至吐槽 PPT 放 video 要退出演讲模式）；
- 直接画折线 / 柱状图代替 Excel 图表。

"用 programming 取代 productivity software"——[[niklas-frykholm|Niklas]] 说这不是为了省时间，是为了**让 time 变得有趣**。

## 相关

- [[live-editing-taxonomy-2010]]
- [[binary-hot-reload]]
- [[game-settings-hot-reload]]
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-hot-reload-javascript]]
