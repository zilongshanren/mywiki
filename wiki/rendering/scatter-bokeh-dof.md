---
tags: [渲染, 后处理, 景深, bokeh, 相机]
date: 2026-04-14
sources: 1
---

# Scatter Bokeh DoF（点精灵散射式景深）

大部分游戏引擎的景深用**gather**（从周边像素收集颜色）：一个 poisson-like 的近似圆盘滤波器，每个输出像素去读 N 个邻居，乘 circle-of-confusion 权重累加。成本正比于 N × 输出像素数，容易和[[separable-gaussian-blur|可分离模糊]]合作，但——**它本质上是"我读邻居"的模糊**，和真实相机的成像机制是反过来的。[[bartosz-wronski|Bart Wronski]] 在 _The Witcher 2_ 里做的另一条路叫 **scatter bokeh**：每个输入像素把自己的颜色**主动撒**到它对应的 bokeh 光斑形状里，用 alpha 混合累加到输出——这是物理上对的那一侧（脱焦的点 → sensor 上的开口形状 = bokeh shape），也因此可以得到任意形状的 bokeh、精细的 near-plane bleeding、以及物理上正确的色差（[[chromatic-aberration-post|chromatic aberration]] 不是拆 RGB 偏移，而是把不同波长缩放成不同大小的光斑）。

## 算法结构

_The Witcher 2_ 版本的完整流程：

1. **Downsample** 到半分辨率的 color + CoC。CoC 从深度和[[thin-lens-model|薄透镜公式]]算。
2. **绘制 quad grid**：每个半分辨率像素一个 quad。vertex shader 里读回对应的 color 和 CoC，按 CoC 把 quad 放大到 bokeh 精灵的目标大小；**不在当前图层的三角形直接移出屏幕杀掉**（far pass 杀近景，near pass 杀远景）。
3. **Pixel shader** 用 bokeh 贴图做形状 mask，按 `1 / spriteSize²` 做能量归一，输出 premultiplied alpha RGBA。**blend 状态用加法 + 预乘 alpha**，所有精灵在目标纹理上累加。
4. **合成**：一次 fullscreen pass，把 far / near / in-focus 三个图层叠回原分辨率 framebuffer。

插入一个有 10 毫秒级开销的 overdraw 炸弹不是开玩笑——在一些含大光斑、近平面覆盖全屏的场景里 GTX Titan 上都跑到过 11 ms。Wronski 诚实地承认这是一个**只上 Ultra 档、只在过场动画里开**的效果，而且美术非常克制地用物理正确的方式（长焦 + 大光圈 + 窄视角 + 单主体）把开销控制在艺术可接受的预算内。

## 为什么要搞这么疯

Wronski 是胶片摄影爱好者，对**六边形 bokeh 深恶痛绝**——现实中所有高端镜头都用多叶片或圆形光圈，就是为了消灭六边形 bokeh。游戏里出现六边形 bokeh 除非是明确要模拟廉价 TV / 相机，否则属于美术理解偏差。他按光圈开口的不同，把"好 bokeh"分成两类：

- **Creamy bokeh**（人像向）：主体外完全化掉，讽刺的是这种"完美"效果**一个 gaussian blur 就能做**。
- **Busy / 有个性的 bokeh**：圆形或环形光斑，Leica / Zeiss 老镜头味，能让背景叶子变成光斑画。需要可以任意形状的 bokeh sprite，gather + 可分离做不出来。

scatter bokeh 主要是为第二类服务的。

## 2014 年重实现里的几个工程点

Wronski 在 [[sources/bartwronski-csharprenderer-debug|C# 框架]]里的开源重实现加了几处优化：

- **indexed draw**，顶点能复用就复用。
- **procedural vertex from vertex ID**——不在 VB 里存位置，shader 里用 SV_VertexID 算出 quad 四个角。对"bandwidth 压爆"的效果，ALU 换 cache miss 几乎永远是划算的。
- **double-width atlas** 取代 MRT / 多 pass：near 平面的 bokeh 画到贴图左半，far 画到右半。避开了[[draw-call|几何着色器]]放大（在早期 DX11 GPU 上 GS 基本没用好过）和多次 vertex fetch。atlas 接缝处偶尔漏一点到邻图层，用 shader mask 或 border 消掉。
- **alpha 合成策略**：加法预乘 + 最后一次除法回到平均，不是严格 ordered alpha，但绝大部分游戏场景里 CoC 差异都不够大到触发可见伪影——这也是 CryEngine 3 / Lost Planet (2007，最早发货的 scatter bokeh) / BF3 的实践共识。

## 和 gather 路线的比较

gather 路线（poisson disk / separable skewed box / Pettineo 的 DX11 "significant bokeh 提取"）在绝大部分项目里**成本收益更好**：

- 带宽主要花在纹理读取上，GPU 擅长。
- 可以做成 [[separable-gaussian-blur|separable]]（六边形用两次偏斜 box blur 叠出来）。
- 不需要 vertex fetch / alpha blend 的 serial 顺序。

scatter 路线只在两个场景下值得考虑：

1. **Bokeh 形状要高自由度**（星形光圈、自定义光环、物理色差）——gather 没法涵盖。
2. **Near-plane bleeding 要干净**——近景脱焦物体需要把自己"撒"到远处才能正确覆盖，gather 反过来做的时候边缘总会留缝。

即使这样，Wronski 本人后续也承认这是一条"疯狂路线"，主要价值是过场质量和实现学习。现代的重新思考见 Wronski 2017 年的 _Separable Bokeh_——把 scatter 问题转成两次可分离 pass，是对同一美学目标的工程让步。

## 相关

- [[thin-lens-model]] — CoC 的物理推导来自这里
- [[chromatic-aberration-post]] — scatter 路线允许做"对的"色差
- [[alpha-blending]] — premultiplied additive 的典型应用
- [[separable-gaussian-blur]] — creamy bokeh 的低成本近似
- [[draw-procedural-gpu]] — procedural vertex from vertex ID
- [[temporal-supersampling]] — Wronski 自己承认 scatter 的半分辨率接缝"除非做时域超采样"才能消掉
- [[bartosz-wronski]]

## Sources

- [[sources/bartwronski-bokeh-insane-pt1]]
