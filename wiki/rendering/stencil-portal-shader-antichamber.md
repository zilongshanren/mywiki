---
tags: [渲染, unity, shader, 模板缓冲, surface-shader, antichamber]
date: 2026-04-14
sources: 1
---

# 用 Stencil Buffer 做 Antichamber 风格的「窗口可见」物体

《Antichamber》最具标志性的视觉戏法之一是那种「魔方的每一面看到不同物体」的盒子——眼睛贴近左面看见一个球、右面看见一个立方体、上面又是别的东西。它本身没有任何屏幕空间魔法，全部交给一种古老但便宜的硬件机制：[[stencil-buffer|模板缓冲]]。[[harry-alisavakis|Harry Alisavakis]] 在 *My take on shaders* 第八篇里给出最小可用的 Unity Surface Shader 实现，整支技术只用了模板缓冲两条最基本的指令：写入一个引用号，以及在另一物体上比较是否相等。

## 概念骨架：mask 和 object 配对

效果由**两类物体**组成：

1. **Stencil mask**——一块不可见的几何（教程里就是一个平面），它存在的唯一目的是：在它覆盖的屏幕像素上，向模板缓冲写入一个 reference number（比如 1）。它本身不输出颜色、不写深度，只「污染」模板缓冲那一块。
2. **Stencil object**——真正想被看到的几何（球、立方体）。它的渲染条件是「只有当当前像素的模板值等于我的 reference number 时才输出颜色」。换句话说，**它默认不可见，必须透过对应编号的 mask「窗口」才能被看到**。

mask 和 object 用同一个 `_RefNumber` 整型属性配对：编号 1 的 mask 让编号 1 的 object 可见，编号 2 的 mask 让编号 2 的 object 可见。Antichamber 那种「同一位置的盒子，不同面看到不同东西」就是把多组 mask 平面摆在盒子的六个面上、各自分配不同 RefNumber 实现的。

## Stencil Mask shader：把模板写满，不画颜色

```hlsl
Tags { "RenderType"="Opaque" "Queue"="Geometry-100" "ForceNoShadowCasting"="True" }
ColorMask 0
ZWrite off

Stencil {
    Ref [_RefNumber]
    Pass replace
}
```

四条关键设定：

- **`Queue = Geometry - 100`**：必须**在普通几何之前**画。如果 mask 比 stencil object 晚画，那 object 在被绘制时模板还没被写、自然看不见，效果就会失败。这是这类技术最容易踩到的顺序坑。
- **`ColorMask 0`**：丢弃这支 shader 的颜色输出，mask 不应该有任何视觉痕迹。
- **`ZWrite off`**：不写深度。否则 mask 会挡住后面物体的深度测试，破坏遮挡关系。
- **`ForceNoShadowCasting = True`**：mask 只是一个抽象的「窗口」，不应当在场景里投阴影。
- **`Stencil { Ref [_RefNumber] Pass replace }`**：模板测试通过时，把模板缓冲里这个像素写成 `_RefNumber`。

## Stencil Object shader：模板等于 ref 才画

```hlsl
Tags { "RenderType"="Opaque" "ForceNoShadowCasting"="True" }

Stencil {
    Ref [_RefNumber]
    Comp equal
}
```

差别极小：

- **没有 `Queue` 调整**——它和场景里其他普通几何一起画就行，只要在 mask 之后即可。
- **没有 `ColorMask 0` 和 `ZWrite off`**——它需要正常输出颜色和深度，因为它是真实可见的几何。
- **`Stencil { Ref [_RefNumber] Comp equal }`**：模板测试用 `equal`，只在「当前像素的模板值等于 `_RefNumber`」处画，否则丢弃整个像素。这就把它的可见区域**剪裁到了 mask 的形状**。
- **`ForceNoShadowCasting`** 仍然保留：物体本体可见但不写阴影。否则会出现「角色看不到物体，但地面上有它的阴影」的诡异穿帮。Alisavakis 也承认这是这套朴素方案的局限——要让它正常投阴影需要更复杂的两 pass 处理。

## 为什么 Antichamber 效果非常便宜

模板缓冲是 GPU 上的硬件专用通路，每像素 8 bit、和深度测试合并执行，几乎不增加 fillrate 成本——参见 [[stencil-buffer]]。一个「魔方六面看不同物体」的场景只需要：6 个 mask 平面 + N 个 stencil object，每帧的额外开销就是 6 次 mask 写入加上 stencil object 的常规渲染加一次 `equal` 比较。比起用 [[render-textures-unity|RenderTexture]] 或者另开一个相机做局部抠图，这套方案便宜一个数量级。

## 同一族技术能做的其它效果

把这两支 shader 改一改，就能派生出大量经典效果：

- **传送门**：mask 是一个面片，stencil object 是「门后世界」的几何子集。看穿门面才能看到另一边。这正是 [[stencil-buffer]] 一节里提到的传送门用法。
- **X 光视图**：mask 是一个手电筒形状的圆盘，stencil object 是「平时不画、被照射时显形」的内脏 / 骨架几何。
- **「橱窗里的物体」**：mask 是橱窗的玻璃形状，object 是 mask 后面的展品——展品永远不会从橱窗外被看到。
- **遮罩 + GrabPass 复合**：mask 后面的窗口里再叠加 [[unity-grabpass-blur|GrabPass]] 模糊，做磨砂玻璃 / 雾化窗效果。

整支技术的精神和 [[custom-mask-shaders|in-shader 程序化 mask]] 是一致的——都是「用一种廉价的硬件 / 数学机制来限定屏幕上哪一块允许出某个效果」——只是 stencil 让这块区域能被任意几何（而不仅是圆盘 / 圆环）定义。

## 相关

- [[stencil-buffer]] —— 硬件 8 bit per-pixel mask 的基本机制
- [[unity-surface-shaders]] —— 这两支 shader 的模板就是标准 surface shader
- [[render-textures-unity]] —— 用相机做相同效果的更贵替代方案
- [[fragment-shader]]
- [[unity-grabpass-blur]]
- [[harry-alisavakis]]

## Sources

- [[sources/halisavakis-image-effects-stencil-antichamber]]
