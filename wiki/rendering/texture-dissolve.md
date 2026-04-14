---
tags: [渲染, shader, vfx, alpha, unity]
date: 2026-04-14
sources: 1
---

# 纹理驱动的溶解效果（Texture Dissolve）

**Texture dissolve** 是一种让网格按照某张纹理的灰度渐进消失的视觉效果：随着参数从 0 到 1 推进，表面越来越大的区域被 `clip` 掉，最后整个模型消失。它是游戏里极常见的 VFX 模板——角色死亡、道具烧蚀、传送进场、幽灵出现，都可以用同一个 shader 骨架生成。和 [[fizzle-lod-fading|fizzle fading]] 不同：fizzle 是为 LOD 切换而生，目标是不被察觉；dissolve 则是**故意让玩家看到**的演出效果。

## 核心公式：clip 的三步

Ronja 的实现只需要三行关键代码：

```hlsl
float dissolve = tex2D(_DissolveTex, i.uv_DissolveTex).r;
dissolve = dissolve * 0.999;                      // 避免纯白永不消失
float isVisible = dissolve - _DissolveAmount;
clip(isVisible);
```

1. 从 dissolve 纹理的单通道读到一个 `[0, 1]` 的遮罩值。通常是一张 Perlin / Worley 噪声。
2. 乘以一个略小于 1 的系数，确保即使 dissolve 纹理里有纯白像素，当参数推到 1 时它们也能被消掉——否则永远残留几个白点。
3. 减去全局的 dissolve 进度 `_DissolveAmount`，把负值的像素喂给 `clip`。HLSL 的 `clip(x)` 等价于「如果 x < 0 就 discard 当前 fragment」。

这个结构最关键的观察是：**dissolve 纹理本身决定了「谁先消失」**。如果纹理是平滑噪声，像水流一样从暗区向亮区溶解；如果是条纹，就像 scanner 扫过；如果是同心圆，就像冲击波扩散。美术只改纹理，不改 shader，就能切出完全不同的演出效果——一个典型的**数据驱动 VFX**。

## 和坐标来源解耦

dissolve 纹理的 UV 可以是：

- **模型原 UV**：最快，但 UV 拉伸的地方 dissolve 也会被拉伸。
- **屏幕空间 UV**：无论模型怎么转，溶解 pattern 都像一层「玻璃膜」固定在屏幕上——适合屏幕空间演出。
- **世界坐标 [[planar-mapping|planar]] / triplanar UV**：最常见的选择，让 pattern 沿世界坐标分布，不被模型变换污染。
- **程序化噪声**：完全不用贴图，直接在 fragment 里合成 Perlin / Worley。省带宽，可完全参数化。

教程里直接用模型 UV，但明确指出可以自由替换——这是 shader 里「采样坐标和采样函数解耦」设计模式的典型例子。

## 边缘发光（Glow Edge）

单纯 `clip` 出来的边界是硬的、没有美术张力。给它加一圈发光边的手法是：在丢弃之前检测「还没被丢，但离丢弃临界很近的像素」，给它们加一份 emission。

```hlsl
float isGlowing = smoothstep(_GlowRange + _GlowFalloff, _GlowRange, isVisible);
o.Emission = _Emission + isGlowing * _GlowColor;
```

注意 `smoothstep` 的两个端点**反向**——第一个参数大于第二个，于是小的 `isVisible` 得到 1，大的得到 0。几何上这是一条从临界点向内渐变的带子：离 clip 边界近 → 100% glow，远 → 0。配合 `[HDR]` 颜色 + bloom post，就能得到「正在烧焦的灰烬边缘」的经典观感。

## 实现细节和坑

- **表面 shader 语法**：教程用的是 Unity 的 `#pragma surface surf Standard fullforwardshadows` surface shader——省去自己写光照的工作量，但代价是代码离底层更远一层。要做精细控制可以换回 vertex/fragment。
- **阴影 pass 同步**：如果 dissolve 影响可见性但阴影 pass 还把整个网格投影出来，就会看到「模型消失了但影子还在」的 bug。Unity 的 surface shader 自动生成的 shadow caster pass 会继承 `clip`——但纯手写的 vertex/fragment shader 需要显式在 shadow caster pass 里重复这个 clip 逻辑。
- **半透明不适用**：`clip` 是二值的，天然配合不透明管线。要真正的淡出（半透明 fade）需要换成 `alpha = smoothstep(...)` 并走 transparent 队列，但那会失去 [[early-z-late-z|early-z]] 等一大批优化——和 fizzle 面对的权衡一样。
- **不透明度精度**：单通道灰度纹理 + float 比较的精度足够平滑，不需要多重采样；边界不会出现锯齿因为 `smoothstep` 把过渡拉开了。

## 相关

- [[fizzle-lod-fading]] —— 同样用 clip/discard，但目标是隐藏而非演出
- [[alpha-blending]]
- [[early-z-late-z]]
- [[fragment-shader]]
- [[planar-mapping]] —— dissolve 纹理的坐标来源之一
- [[layered-grid-noise]] —— 程序化生成 dissolve pattern
- [[particle-custom-vertex-streams]] —— 粒子系统通过 AgePercent 驱动逐粒子 dissolve

## Sources

- [[sources/ronja-texture-dissolve]]
