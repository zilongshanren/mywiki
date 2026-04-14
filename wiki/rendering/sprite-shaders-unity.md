---
tags: [shader, unity, sprite, 2d, 渲染]
date: 2026-04-14
sources: 1
---

# Sprite Shader（Unity）

在 Unity 里给 2D sprite 写自定义 shader 和给 3D 物体写 shader 看起来很像——底层都是一个 vertex + fragment 的 Pass——但 `SpriteRenderer` 组件在幕后替你做了一堆「3D shader 里没有」的事，如果直接把普通的纹理 shader 贴上去，就会发现 **翻转不见、颜色不响应、排序不正确**。这篇整理出最小可用的 sprite shader 和它需要的三个修正。

## SpriteRenderer 做了什么

`SpriteRenderer` 不是简单的 quad：它读 sprite 的 import 设置（包括 polygon outline、pivot、pixels-per-unit），自动生成对应的 mesh 并写好 UV；把 `SpriteRenderer.color` **塞进顶点 color 通道**；按 `Sorting Layer` / `Order in Layer` 通知渲染管线；在开启 Flip X / Y 时 **按 Y 轴旋转 180°** 取而代之，而不是改 UV。最后一点是所有坑的起点——它让 sprite 的背面在 flip 后朝向相机。

## 三个必要修正

在 [[alpha-blending|透明混合]] shader 基础上，sprite 还需要：

1. **`Cull Off`**：Flip X/Y 时 sprite 被旋转到背面，默认的 backface culling 会把它剪掉。2D sprite 没有「里外」之分，也不做光照，所以关掉 culling 零代价。
2. **读取 vertex color**：`SpriteRenderer.color` 和 tint 是通过顶点色传进来的。`appdata` 和 `v2f` 需要一个 `fixed4 color : COLOR`，fragment 里 `col *= i.color` 才能让 Inspector 里改颜色生效。
3. **保持 `Blend SrcAlpha OneMinusSrcAlpha` + `ZWrite Off`**：继承自透明 shader。

```hlsl
SubShader {
    Tags { "RenderType"="Transparent" "Queue"="Transparent" }
    Blend SrcAlpha OneMinusSrcAlpha
    ZWrite Off
    Cull Off
    Pass { ... }
}
```

## 没覆盖的东西

Unity 官方的 sprite shader 还额外支持 **GPU instancing**、**pixel snap**（用 `_PixelSnap` 把顶点对齐到屏幕像素网格，避免亚像素抖动）、**外挂 alpha 通道**（ETC1 压缩无 alpha 时用第二张贴图存 α）。这三项属于 edge case，自己写教学用 shader 时可以忽略；但做商业项目时 pixel snap 在像素美术里几乎是必需的。Spritesheet、polygon sprite、动画等也无需 shader 侧特殊处理——`SpriteRenderer` 生成的 mesh 已经把 UV 和几何都准备好了。

## 相关

- [[alpha-blending]] — sprite shader 的透明基础
- [[fragment-shader]]
- [[bluk-2d-fog-sprite-shader]] —— 一个基于 sprite shader 扩展出的 2D 雾效案例

## Sources

- [[sources/ronja-sprite-shaders]]
