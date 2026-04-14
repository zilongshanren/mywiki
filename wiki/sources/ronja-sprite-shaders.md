---
tags: [source, rendering, shader, unity, sprite, 2d]
date: 2026-04-14
sources: 1
---

# Sprite Shaders（Ronja's Shader Tutorials）

[[ronja-bohm|Ronja Böhm]] 2018 年 4 月发表的系列第 007 篇，把上一篇的 [[alpha-blending|透明 shader]] 扩展成 Unity 里能正确挂在 `SpriteRenderer` 上的 sprite shader。

## 摘要

文章先解释 `SpriteRenderer` 组件在幕后替我们做的事：根据 sprite import 生成带 UV 的 mesh、把 `SpriteRenderer.color` 塞进顶点 color 通道、用 `Sorting Layer` 和管线沟通绘制顺序、Flip X/Y 时通过 180° 旋转实现而不是改 UV。接着指出一个普通透明 shader 挂上去后两个常见问题——flip 后物体消失、Inspector 色变无效——并给出修正：加 `Cull Off` 关掉背面剔除、在 `appdata`/`v2f` 结构里增加 `fixed4 color : COLOR` 并在 fragment 里 `col *= i.color`。文章末尾点出 Unity 官方 sprite shader 还支持 GPU instancing、pixel snap 和外挂 alpha 通道三项 edge case 功能，教学版本为简洁起见略去。

## 关键要点

- `SpriteRenderer` 已经替 shader 作者生成好 mesh 和 UV——shader 只需关心 flip、color、排序这三件。
- Sprite 没有「里外」之分，也不做光照 → `Cull Off` 零代价。
- `SpriteRenderer.color` 走 **顶点色通道**，不是 uniform；shader 要显式读 `COLOR` 语义才能响应。
- Spritesheet / polygon sprite / 动画无需特殊处理，都由 `SpriteRenderer` 准备 mesh 和 UV。
- 官方 sprite shader 的额外功能（pixel snap、instancing、外挂 α）教学版本略去。

## 链接到的概念

- [[sprite-shaders-unity]]
- [[alpha-blending]]
- [[fragment-shader]]

## 原文

- 链接：<https://www.ronja-tutorials.com/post/007-sprite-shaders/>
- 本地：`raw/articles/ronja-tutorials.com/2018-04-13_sprite-shaders.md`
