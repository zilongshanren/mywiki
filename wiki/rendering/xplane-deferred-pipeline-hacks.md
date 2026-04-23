---
tags: [渲染, 延迟渲染, g-buffer, srgb, 光照, x-plane, 2012]
date: 2026-04-19
sources: 1
---

# X-Plane 10.10 延迟管线：四篇「Deferred Weirdness」合编

[[ben-supnik|Supnik]] 2012-11-16 到 11-19 连着写了四篇，把 X-Plane 10.10 延迟渲染管线重写的整套教训摊开。主题分为四块：光源体积的 **stencil 剔除**被关掉、两次 deferred pass 被**合成一套多 buffer 的缝合怪**、**sRGB 与 linear 两套 blend 方程**必须共存、最后是三种约束叠加的系统性反思。全体论点的底座是：**X-Plane 是平台而不是游戏**——大量第三方旧内容无法要求按 deferred 理论形态重做，工程必须把延迟管线改造成能吃既有资产的形状。

## 1. 把 stencil 光源体积优化关掉

标准套路来自 stencil shadow volume：给延迟光源画真实 3D 包围体（棱锥/立方体），用**双面 stencil** 标记光源体积内部的屏幕区域，再跑一次 shading pass。详细机理见 [[deferred-light-volume-stencil-depth-clamp-hack]]。

Supnik 实测 stencil 优化对 X-Plane **不是胜利**——即便在 Radeon 4870 这种老卡上，也得把相机和光源摆成病态构型才看到正收益。原因是 X-Plane 的负载画像与典型 console FPS/赛车完全不同：

- **几何重、shader 浅**：延迟光源 fill 根本不是瓶颈。瓶颈在顶点带宽——车灯等动态光的体积每帧由 CPU 变换，两遍 stencil pass 要求顶点流两次。
- **光源数多但每盏小**：数万盏街灯每盏只覆盖几像素。stencil 剔除的节省不够弥补 draw call 加倍和 AGP 流式顶点的传输代价（见 [[agp-vs-vram-streaming]]）。
- **美术本身控制得住 overlap**：艺术家避免光源重叠，pre-stencil 的潜在收益被吃掉。

最后 10.10 把 stencil 关掉，顶点吞吐直接减半。下一步候选是把光源体积换成**屏幕空间四边形**，再省一档流式顶点带宽。

## 2. 把两次 deferred pass 合成一套多 buffer 的缝合怪

X-Plane 必须同时画**外部世界**（近/远剪裁跨到百公里）和**内部 3D 座舱**（控件 < 1 米）；单一 24 位深度缓冲装不下这个量级比。历史做法是两遍 forward：外部画完后 clear depth 再画内部。

初版 deferred 直接照搬成「两次完整 deferred pass」——**带宽翻倍，fps 减半**，deferred renderer 本来就 bandwidth-bound。Supnik 考虑过的 non-linear Z：

- **log depth 在 VS 里改 z**：跨越相机平面 `log(z<0)` 未定义，而且 vertex 做的 clip 测试错位。
- **FS 里改 depth**：早期 Z 剔除失效，X-Plane 多处 overdraw 吃不起这个代价。

都不合适。于是保留双 pass depth，但把 deferred 铺开成一张多缓冲、多 stencil 位的**状态机**：

1. G-Buffer、HDR、LDR 三张 RT 共享一张 depth；[[xplane-gbuffer-format|G-Buffer]] 把眼空间深度以 `16F meters` 独立写一通道，depth 可以 clear 而 G-Buffer resolve 不丢位置（走 [[deferred-depth-reuse-tradeoffs|路线 C]]）。
2. 内/外坐标系**眼空间完全一致**，只差 projection 近/远剪裁面——两段可以共用同一套光照数学。
3. 座舱壳先做 depth pre-fill 占住近端 Z，能 pre-occlude 大量云粒子（Z 测试失败直接剔）。
4. 画外部 solid 到 G-Buffer；画热扰 (heat blur) 体积**只写 stencil** 记下被扰动的像素（后续 depth clear 会把深度信息吃掉，stencil 是唯一能存活的通信通道）。
5. 外部 post-G-buffer 的透明/粒子画进 LDR（8-bit 省带宽）；外部光 billboard 画进 HDR。
6. **Clear depth**，画座舱 solid 到 G-Buffer，同时再置另一个 stencil 位标「在座舱内」。
7. 用 depth-fail 重绘热扰体积以**抹掉**被座舱实体挡住的 stencil——相当于**用 stencil 两步把两张深度缓冲上的 depth test 拼起来**。
8. 回到 HDR，对「在座舱」stencil 位画黑 quad，盖掉被内部实体应当遮挡的外部 light billboard。
9. G-Buffer mix-down 到 HDR（加法混合，light billboard 累加仍在 linear 空间）。
10. LDR 里再用 stencil mask 画黑 quad 盖掉被座舱遮挡的外部粒子。
11. 画内部粒子/light 直接到 LDR。

核心设计是**不对任何 surface 做二次 pass**——只 clear depth 一次。代价是 MRT state 切换**非常**多。Supnik 自己承认这是整个管线最丑的点。

## 3. sRGB 与 Linear 两套 blend 必须共存

延迟管线在 blend 阶段有一条刚性要求：[[linear-lighting-pipeline|光是加性的，累加必须 linear]]。但 X-Plane 的旧 alpha 资产——玻璃、窗口污渍、远处 3D 对象的 alpha 淡出——全是艺术家按「Photoshop-style 感知合成」做的，**真正需要的是 sRGB blend**。

| 用途 | 必须 Linear | 必须 sRGB |
|---|---|---|
| 累加延迟光 | ✅ | ❌ |
| 累加 light billboard 光晕 | ✅ | ❌ |
| 玻璃/窗口/烟雾 alpha 合成 | ❌ | ✅ |
| G-Buffer 内对 albedo + emissive 两层 alpha blend | ❌ | ✅ |
| 3D 对象 alpha fade with distance（不可绕过 deferred） | ❌ | ✅ |

**G-Buffer 内的 alpha blend 为何必须 sRGB**：延迟渲染里 albedo 和 emissive 是**两张独立的 RT**，而前向渲染里这两者在 shader 里已经合成后再 blend。要让两种路径结果一致，必须保证

```
blend(A_alb, B_alb, α) + blend(A_lit, B_lit, α) = blend(A_alb+A_lit, B_alb+B_lit, α)
```

这条等式**只在 blend 和 addition 发生在同一 color space 时成立**。因此 G-Buffer 的 albedo/emissive 通道只能在 sRGB 空间 blend，之后的 additive light 累加独立在 HDR RT 上走 linear——两套 blend 方程在不同 RT 上共存。

伴随的硬性限制：**不能把 linear additive 效果画进延迟渲染**（必须走 HDR forward 的后 G-Buffer pass）。

alpha 通过 G-Buffer 的局限很现实：每 texel 只有一个材质，所有通道（albedo/emissive/specular/AO/normal）都被 src-alpha blend 出一个**加权平均值**再走一次光照；那是对光照方程"输入"做加权平均，而不是对"输出"做 alpha 合成，物理上不等价，但 set 得住就是胜利。唯一不 blend 的通道是**眼空间 Z**——丁点位移都会让阴影贴图 aliasing，这是 deferred + alpha 的共病（见 [[deferred-alpha-lighting]]）。

Normal 通道能 blend 的前提是用 [[compact-normal-encoding|Lambert azimuthal 2 通道编码]]——线性插值几何上大致对。

## 4. 合起来学到了什么

Supnik 的自嘲总结：deferred renderer 里任意**一条**困难都有成熟解法，但 X-Plane 三条同时全撞上——

1. 超宽 Z 范围要求两次 pass；
2. 旧内容带着 alpha 且无法剔除出 deferred；
3. 必须在同一帧里维护 sRGB 和 linear 两套 blend 方程。

每条单独应付都不难，**三条一起 juggling** 才是工程复杂度的源头。

这种"把新管线硬弯成吃旧内容形状"的束缚来自 X-Plane 的**平台属性**：第三方 content 不同步更新、常年落后引擎若干版本、作者与引擎团队基本无接触。最省事的 deferred 是**先定规矩再收美术**，这条 X-Plane 走不了。所以 Supnik 的「第一条教训」写在第四篇结尾：

> 如果你能做到，试着只给 deferred 管线留一个"硬边角"——往里塞几个 hack 不难，难的是同时 juggling 好几个。

他特意把话补全：这堆复杂的代码是 **success**，因为它同时兑现了 deferred 的收益（大量光源、几何复杂度、soft particle、未来空间），同时兼容遗留内容——代码承压是因为它在办真实的事。

## 相关

- [[deferred-rendering]]
- [[xplane-gbuffer-format]] —— G-Buffer 布局细节，本篇的第 1 条设计选择
- [[deferred-depth-reuse-tradeoffs]] —— 为什么必须走「往 G-Buffer 写 16F 眼空间 Z」的路线 C
- [[deferred-light-volume-stencil-depth-clamp-hack]] —— 被本篇「关掉」的 stencil 优化的机理与 depth-clamp 降级
- [[deferred-alpha-lighting]] —— 延迟下 alpha 的四条方案综述，本篇走第 1 条 + G-Buffer 内 sRGB blend
- [[linear-lighting-pipeline]] —— 三种光照累积路径的分类，本篇是第三种（HDR RT）的受约束变体
- [[srgb-premultiplied-alpha-compression]] —— sRGB / 预乘 / 压缩三角；本篇是同一作者 sRGB 论题的早期版
- [[gamma-correction-srgb]] —— sRGB 编解码数学底
- [[compact-normal-encoding]] —— G-Buffer 内 normal blend 前提
- [[agp-vs-vram-streaming]] —— 顶点带宽瓶颈论据，关掉 stencil 优化的根据
- [[ben-supnik]]
- [[cheat-by-solving-less]] —— 多处选型的共通哲学：不做更大的问题

## Sources

- [[sources/supnik-deferred-weirdness-series]]
