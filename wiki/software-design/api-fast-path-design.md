---
tags: [api设计, 性能, opengl, x-plane]
date: 2026-04-19
sources: 1
---

# API 快速路径设计

[[ben-supnik]] 在 2010 年从 OpenGL 驱动与 X-Plane SDK 两边同时提炼出的 API 设计原则：**设计 API 时关心「最快的路径能不能被挡住」，实现 API 时关心「默认行为对总体性能影响如何」**。两个问题不要混着回答。

## 驱动端的经典矛盾

客户端可能写出冗余调用：

```c
glEnable(GL_TEXTURE_2D);
glDrawArrays(GL_TRIANGLES, 0, 51);
glEnable(GL_TEXTURE_2D);   // 多余
glDrawArrays(GL_TRIANGLES, 108, 51);
```

驱动面对两种策略：

1. **检查冗余**：每次 `glEnable` 先比对当前状态，若无变化直接返回。对粗心客户端节省昂贵 state change，对仔细客户端多一次 1-bit 比较。
2. **不检查**：粗心客户端变慢，仔细客户端享受最快路径。

Supnik 的立场是：**不在乎选哪种，但必须公开宣告哪条路径快、哪条不快**——让客户端有办法写出最快路径。模糊的文档会让两类客户端都输。

注意：真实工程里「冗余 detect」很难做。X-Plane 只绘制屏幕可见内容，前一帧 drawn 的状态依赖相机角度，状态机快照几乎每次都不同——纯表面的状态缓存能省的调用远比想象的少。

## 客户端的正面例子：X-Plane dataref

X-Plane SDK 的 `dataref` 是把「一次性贵操作」和「高频快操作」显式拆成两个 API 的典型：

- `XPLMFindDataRef(name)`：字符串 → opaque handle，**官方标注为「慢」**。客户端应该在初始化期查一次、缓存 handle，不要放在 per-frame 循环里。
- `XPLMGetDataf(handle)` / `XPLMSetDataf(handle, v)`：通过 handle 读写数据，**官方标注为「快」**。Sandy 和 Ben 会盯这条路径的代码开销，故意不做校验。

这里有两个设计决策：

1. **把慢和快拆成不同函数名**——而不是「同一个函数，内部看情况走 fast path」。拆开能让客户端在代码里看出性能等级，也避免编译器无法优化的动态分支。
2. **快路径故意不做校验**。传错 handle 会导致不确定行为（包括崩溃），但好写的插件不会被糟糕插件拖累性能。失败模式 Supnik 用 nasal demons 一句话描述完毕：不保证任何特定错误行为。

这是一种**质量分层 SLA**：API 承诺了快路径有多快，但要求调用者遵守契约（handle 有效、调用时序合理）。和「零额外成本抽象」是同源思路。

## 语言层的残留：switch fall-through

Supnik 把 C 的 `switch` fall-through 也归入「为了快路径保留了不安全语义」的例子。现代编译器大半能把 fall-through 还原，但 C 诞生于 70 年代编译器装不下内存的年代，语法本身承载的是**「如果程序员不明写最优代码，就不会有最优代码」**这条前提。今天很多语言（Go、Rust）默认禁止 fall-through，是性能不再需要、安全更值钱的换权。

## 与 API 演进的关系

API 是合约。一旦公开声明「这条路径快」，升级实现时就不能悄悄加校验或缓存层。Supnik 做 `dataref` 时当年 find 实际是线性的，但因为声明了「慢」，客户端都缓存了 handle；后来升级成对数时间，客户端代码不需要动、也没有人突然发现「怎么比以前快了」。**文档契约比实现契约更长久**。

## 相关
- [[information-hiding]]
- [[rendering-api-depth]]
- [[strategic-programming]]
- [[cheat-by-solving-less]]
- [[opengl-ext-vs-arb-fast-path-leak]] —— 驱动内部 fast path 条件的 if 瀑布反面案例

## Sources

- [[sources/supnik-fast-paths]]
