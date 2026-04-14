---
tags: [source, unity, shader, 光照, cel-shading, stencil, outline]
date: 2026-04-14
sources: 1
---

# Cel Shading Part 4 - Edge Outlining（Daniel Ilett）

[[daniel-ilett|Daniel Ilett]] 卡通渲染系列第四篇，给 cel shader 加上**漫画式粗描边**。做法是经典的**两 pass + 法线外推 + stencil mask**——Part 4 的价值在于把这个方法完整拆开讲了 stencil buffer 语法的每个关键词。

## 摘要

文章先声明描边的总体思路：**画两遍**。Pass 1 正常画模型，同时把覆盖的所有像素在 stencil buffer 标成一个参考值（例如 `1`）；Pass 2 用一个**把顶点沿法线向外推 `_OutlineSize` 距离**的 vertex shader 重新画一遍模型，fragment shader 输出纯色 `_OutlineColor`，但通过 stencil 测试把 Pass 1 已经占用的像素丢弃——剩下的只有一圈"外扩出来的边缘"。然后作者详细解释 `Stencil { Ref  Comp  Pass  Fail  ZFail }` 每个字段的语义：**Ref** 是参考值；**Comp** 是比较函数（Pass 1 用 `always` 意味着无条件通过写入，Pass 2 用 `notequal` 意味着只在 stencil 不等于 `Ref` 时才渲染）；**Pass** 是 stencil 和 depth 都通过时的行为（Pass 1 用 `replace` 写入参考值，Pass 2 默认 `keep`）；**Fail** 和 **ZFail** 是失败时的行为，两个 pass 都用默认 `keep`。第二 pass 还需要 `ZWrite off  ZTest on` 作为"sanity check"——描边不应该污染深度缓冲，但仍要被前景物体遮挡。

## 关键要点

- **沿法线外推必须在 object space 完成**：`pos = v.vertex + normalize(v.normal) * _OutlineSize`，然后才 `UnityObjectToClipPos(pos)`。如果在 clip space 做，透视除法会让远处的描边变细。
- **Stencil 的 Pass/Fail/ZFail 区别**：`Pass` 指 stencil 和 depth 都通过时；`ZFail` 指 stencil 过了但 depth 没过；`Fail` 指 stencil 没过。cel outline 只关心"stencil 通过然后写 `Ref`"，所以只需要 `Pass replace` + 两个 `keep`。
- 没加 stencil 测试前整个 Ethan 会被 `_OutlineColor` 完全覆盖——因为外推后的 mesh 绝大部分像素都在原模型内部。Stencil 就是为了**从放大版 mesh 里扣掉原模型区域**。
- **Ref 1 是硬编码的临时值**——Part 5 会把它改成 `_ID` 属性以支持多物体共存；这个硬编码在 Part 4 结尾已经埋下伏笔。
- 描边是一个**纯拓扑效果**——它不依赖于光照、不依赖 albedo、不依赖材质，因此和 Part 3 的 bump+fresnel 代码完全解耦，只是在同一个 `.shader` 文件里多一个 pass。

## 链接到的概念

- [[cel-shading-pipeline]]
- [[cel-shader-outline]]
- [[stencil-buffer]]

## 原文

- 链接：https://danielilett.com/2019-06-15-tut2-4-edge-outline/
- 本地：`raw/articles/danielilett.com/2019-06-15_cel-shading-part-4-edge-outlining.md`
