---
tags: [渲染, UI, mesh, 九宫格]
date: 2026-04-19
sources: 1
---

# 九宫格 UI（Nine-Slice）

九宫格是 UI 渲染里一个几乎无处不在的小技巧：当一个矩形元素（按钮、面板）需要支持**任意尺寸的非均匀拉伸**、但又要保留**圆角 / 边框细节不变形**时，把 mesh 和贴图都切成 **3×3 = 9 块**分别缩放。[[sources/thomas-poulet-anno-1800-frame|Anno 1800]] 在 Phoenix（Ubisoft 共享的 UI 中间件，Rainbow Six Siege 也用）里用的正是这套。

## 切法

- **四角**：不拉伸，按 1:1 贴贴图原始像素——保证圆角曲率、阴影、内外描边不会变形。
- **上下两边 & 左右两边**：沿一个方向拉伸，另一个方向保持原尺寸。边框花纹沿长轴被 repeat 或 stretch。
- **中心区域**：两个方向都可以拉伸或 tile，通常就是底色/背景图。

实现时有两种等价路线：

1. **Mesh 切九片**：[[thomas-poulet]] 在 Anno 里看到的是**直接把 9 格切进 mesh 里**——mesh 有 9 组三角形，UV 按九宫格映射到贴图对应块。GPU 拿到就直接画，vertex shader 只处理 screen-space 位置。
2. **Shader 做 UV 变换**：单 quad，shader 根据 fragment 位置决定落在哪一格、对应 UV 怎么采。

两种都常见：Anno 的 mesh 版本更直观，拿出来改 slice 边界也方便，劣势是几何面数高（Anno 有 ~500 个 DrawIndexedInstanced，都是 instance count 1 —— instancing 没开，每个 UI 元素一次 draw）。

## 为什么重要

- 解决「非均匀缩放的圆角毁容」问题，几乎是所有 retained-mode UI 都会提供的原语（CSS 的 `border-image`、iOS 的 `UIImage.resizableImage`、Unity 的 Sliced Image、UE 的 `Box / Border` brush）。
- 配合 [[slug-gpu-glyph-rendering|SDF 字体渲染]]，一套 9-slice 背景 + 一套 SDF glyph atlas，就能拼出像素完美、任意分辨率的 UI。

Anno 还在文本渲染上用了**单通道 SDF 字体图集**——覆盖拉丁大小写、希腊、西里尔、俄文、部分符号——`@` 号在图集里占据的空白大得惊人。多通道 SDF（MSDF）能更好地保留尖锐角，Anno 选择了更省的单通道 SDF，在一般 UI 字号下够用。

## Sources

- [[sources/thomas-poulet-anno-1800-frame]]
