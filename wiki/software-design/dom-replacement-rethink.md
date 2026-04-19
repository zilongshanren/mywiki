---
tags: [software-design, ui, web, dom, css]
date: 2026-04-19
sources: 1
---

# DOM / CSS / HTML 的根本性重构

[[steven-wittens]] 在 *HTML is Dead, Long Live HTML* 里用整篇文章解释一件事：浏览器中间层（DOM、CSS、SVG、HTML）已经不适合今天的任何使用场景——既不是好的文档引擎，也不是好的应用 UI 工具包——但外面没人有动力去 greenfield 掉它。他的诊断尖锐，提出的替代方向也具体。

## DOM 肥胖

在 Chrome 下 `document.body` 有 350+ 个 key；`document.body.style` 的 CSS 属性有 660 个。property 与 method 界线模糊，很多 getter 会触发 just-in-time 回流。Web Components 本应是原生的组件化方案，但引入了 Shadow DOM 的嵌套与 scoping，API 过度笨重，社区只当作"解释型"存在。真正的 achilles heel 是 DOM 的 SGML/XML 血统让所有东西都是 stringly-typed；React 之类写成 XML 只是*看上去*像，实际数据流远比 DOM 干净——所以大家早就不在 DOM 里放 state。

## CSS 是 inside-out 优先

Wittens 给 CSS 提供了一个很清楚的 mental model：很多人把 CSS 当 constraint solver，于是碰到 `height: 100%` 的嵌套 div 一头雾水。真相是两遍：先 outside-in 把父约束下传，再 inside-out 让子内容撑开父容器。HTML 天然是 inside-out（段落撑开页面），outside-in 要你从 `body { height: 100% }` 一路显式下传，这就是"垂直居中难"的根源。

CSS3 flex 让两种模式更对称，但引入了"先 speculative layout 再 fit"的递归依赖——父容器的 speculative layout 需要把子容器完整布一遍才知道自然尺寸，嵌套深时存在理论上的指数爆炸。`contain: size` / `will-change` / `flex-basis` 这些构造的存在正是为了"关掉过度文档化的默认语义"，揭示底下的 layer-oriented 本质。Wittens 的评价：这种 "subtractive API + containment hint" 是 subtractive design 的反例，应该直接正面暴露 outside-in / inside-out 作为两种容器类型。

CSS 其实是两套东西缝在一起：基于继承的富文本样式系统（`<b>` 的 font-size 向下继承） + 无继承只 containment 的 block/inline 布局系统（border 不会向下继承）。混在同一语法里是历史错误。

## SVG 与 CSS 的错位

SVG 原生嵌入 DOM 能动态生成形状和图标，但既非 CSS 的子集也非超集：`transform` 语义略有差异、坐标全部字符串化、hit-testing 能力比 CSS 强（多边形）但其他方面又弱于 CSS。CSS 获得的圆角/渐变/clipping mask 能力是 SVG-envy，但达不到 SVG 的层级；而 CSS 又缺 polygonal hit-testing 和 graphical layer effects。选哪个渲染某个元素依赖一系列奇葩的 trade-off，而二者最终都只是矢量。

几个有代表性的"卡住在 v1"的 feature：

- `text-ellipsis` 只能对单行截断，整段落不行；检测被截断的文字极难，API 根本不够
- `position: sticky` 设计上是为此而生，但"无条件 sticky"需要荒谬的嵌套 hack
- `z-index` 是绝对数值，没有相对 Z——每个项目最后都有一份 `z-index-war.css`

## "HTML in Canvas" 是个坏答案

[WICG html-in-canvas 提案](https://github.com/WICG/html-in-canvas/tree/main)允许把 HTML 绘入 `<canvas>`，但要求元素必须是 canvas 的后代才能参与 layout/styling/accessibility，hit-testing 靠 2D 矩形回调。Wittens 的吐槽：3D 用法只能装饰？放 dropdown 怎么办？为了定制*外观*却要接管一个元素整棵子树的*全部*交互？这是"把 canvas 和 CSS filter/shader 的合流做不出来，只好让你从 DOM 兜一圈回去"。

真正驱动"canvas 做复杂 UI"的需求——virtualization、just-in-time layout/styling、custom gesture/hit-testing、visual effects——全都是"DOM 做不到的事"，把 DOM 当 black box 预渲染反而绕回起点。canvas 自身的 achilles heel 也没被解决：没有系统字体、没有 text layout API，要自己实现 Unicode word split 才能换行。

## 替代路径

Wittens 不空谈，给了具体方向：

- 把 DOM 里"HTML 片段作为 composite value"这件事真正公开化，而非继续背着 20 年遗产
- 新表面在 DOM 之外开，而不是硬修 DOM
- view tree / render tree 的区分是真实的；problem 是 view tree 到底该长什么样，以及被 lower 成什么——目前"被 lower 成一坨 legacy 碎片"是隐形的

他推自己的 [[use-gpu-reactive-runtime|Use.GPU]] [HTML-like renderer](https://usegpu.live/demo/layout/display) 作为存在性证明：完整的 X/Y flex 模型，复杂度和代码量一小部分；垂直居中 trivial；div 上直接挂 shader；语义 HTML、CSS cascade 全不存在，layout 才是 first-class。"单人能做出来，90% 覆盖率，剩下 10% 我也知道。"

另有现实的推动力：Servo、Ladybird 等替代浏览器有最干净的实现、最核心的优先级；Spectre 把 `SharedArrayBuffer` 多线程基本打死了，重新设计 DOM 顺便解决 multi-origin / 多进程隔离可以让浏览器厂商有理由投入。Mozilla 崩溃、Tauri 在 origin isolation 上没做好，生态缺一个有品味的推动者。

## 相关

- [[use-gpu-reactive-runtime]]
- [[intent-vs-state]]
- [[reactive-ui-rust]]

## Sources

- [[sources/acko-html-is-dead]]
