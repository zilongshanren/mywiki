---
tags: [渲染, 模板缓冲]
date: 2026-04-05
sources: 1
---

# Stencil Buffer（模板缓冲）

**每像素 8 位的测试与写入缓冲**。性能几乎零成本（硬件专用路径），但能实现大量效果。

## 基本操作

- **写入**：shader 输出时写一个 8bit 值。
- **测试**：`stencil_test(stencilRef, stencilValue)` 根据运算符决定是否通过。
- **按位 mask** 允许独立使用每个 bit。

## 经典效果

### 描边（Outline）

1. 第一 pass：正常渲染物体，模板写 1。
2. 第二 pass：渲染**放大版本**，只在模板不是 1 的地方渲染，出现在物体边缘。

### 传送门（Portal）

1. 渲染传送门形状到模板。
2. 在模板通过的地方渲染传送门内容——天然限定屏幕区域。

### Shadow Volume（Carmack's Reverse / Doom 3）

用模板累积阴影体的进出次数，判断像素是否在阴影中。

### Deferred Lighting 的 light volume 剪裁

只在光源影响的像素执行光照 shader。

## 为什么便宜

模板硬件路径专用，和深度测试合并在一起。设计良好时几乎零额外成本。

## 相关
- [[fragment-shader]]
- [[z-buffer]]
- [[early-z-late-z]]
- [[depth-aware-upsampling]] —— stencil 标记深度不连续像素、分派 simple/complex shader 的 ROTR trick
- [[stencil-portal-shader-antichamber]] —— Antichamber 风格「mask + object 配对」的最小 Unity 实现
- [[stencil-parallax-card-layers]] —— Pokémon 卡牌风格的「stencil mask + Render Objects feature + 分层 parallax」URP 实现
- [[deferred-light-volume-stencil-depth-clamp-hack]] —— X-Plane 光源体积 stencil 被远剪裁面切穿时的 depth-clamp 依赖与 vertex-shader Z-clamp 降级

## Sources

- [[sources/rtr-day05]]
