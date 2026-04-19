---
tags: [unity, urp, stencil, parallax, renderer-feature, 卡牌]
date: 2026-04-19
sources: 1
---

# Stencil + Render Objects：宝可梦卡牌式分层 parallax

Pokémon TCG Pocket 的 ex 卡有一种「**透过卡牌的边界窗**看到后面一张有景深的背景，前景图随视角动但被卡框截断」的效果——本质是一个**受限视口**：前景 / 背景是真实的三维分层几何，但只允许在**卡牌边框内的像素**上显示。Ilett 用 URP 的 stencil + Render Objects feature 把这件事以低成本拼出来，这条路径也适合任何「impossible window」几何效果。

## 四层几何分工

卡面由四层 quad 组成：

1. **边框**（foreground border）—— 中间挖了一个 alpha-clip 的洞，卡边花纹包围它。正常渲染。
2. **遮罩 mesh**（stencil mask）—— 刚好填进那个洞的透明 quad，**唯一作用是往 stencil buffer 写 1**，不写颜色也不写深度。
3. **前景艺术图**（foreground artwork）—— 透明 quad，放在边框前方一点点。
4. **背景**（background）—— 不透明 quad，放在后方一段距离，**故意做得比窗大**，这样卡旋转时窗里仍然填满背景。
5. 还有一层文字（CardText）平贴边框。

## 阶段 1：Stencil mask shader 写 1

Shader Graph 的 Lit / Unlit 模式**不支持 stencil 设置**（只有 Fullscreen 模式开放），所以 mask 必须手写 HLSL。关键 block：

```
Stencil
{
    Ref [_StencilRef]   // 属性里暴露的 1
    Comp Always         // 测试永远通过
    Pass Replace        // 通过时把 Ref 写进 stencil
    Fail Keep
}
ZWrite Off              // 关键：后面的东西还要能画到这块区域
ColorMask 0             // 完全不写颜色
```

`ZWrite Off` 是必须的——如果 mask 写了深度，前景艺术图会因为 z-test 被剔掉。`ColorMask 0` 保证 mask quad 彻底不影响画面。

## 阶段 2：Render Objects feature 把 layer 按 stencil 读回来

这里是关键的架构决策：**与其让每个前景/背景 shader 都自己读 stencil**（那得改所有 material 的 shader），不如把它们从**正常渲染路径**里抽掉，然后用 URP 的 `Render Objects` Renderer Feature 在 stencil mask 写好之后**补画一次、同时带上 stencil 读**。

- 在 **CardArtwork** 自定义 layer 上放前景 quad + 背景 quad；
- URP Renderer Data 的 *Opaque Layer Mask* / *Transparent Layer Mask* 顶层里**关掉** CardArtwork——它们从此不再走默认不透明/透明 pass；
- 加两个 *Render Objects* Renderer Feature：
  - 第一个：Event = *AfterRenderingOpaques*，Queue = Opaque，Layer Mask = CardArtwork，**Overrides.Stencil.Value = 1，Compare = Equal** —— 等同于"只在 stencil==1 的像素画"，背景 quad 被卡牌窗外的 stencil=0 像素剔除；
  - 第二个：Event = *AfterRenderingTransparents*，Queue = Transparent，同样 stencil=1 equal —— 处理前景艺术图。

## 阶段 3：CardText 单独再一层

文字不希望被前景 artwork 盖住，放在单独的 **CardText** layer，同样从 opaque/transparent layer mask 里摘掉，然后加第三个 Render Objects feature 放在前两个之后（list 越靠下渲染越晚），把文字画在最上面。想稳，可以把这个 feature 的 *Depth Test* 改为 *Always*。

## 为什么不直接在 shader 里写 stencil

能这么做——但**每个参与窗口效果的 material 都得换成自写 stencil 版 shader**，多一套维护路径。Render Objects feature 的好处是**改一次 renderer 配置，现有 shader 全部复用**，这是 URP 2022 以后做"可选视觉叠加"的推荐路径。

## 相关

- [[stencil-buffer]]
- [[stencil-portal-shader-antichamber]] —— 同样的 stencil「绘制→读取」模式，用在门后场景
- [[holofoil-rainbow-shader]] —— 同一教程里下一段讲的彩虹 holo shader，和这套 parallax 组合
- [[blit-render-feature]]

## Sources

- [[sources/danielilett-holofoil-cards]]
