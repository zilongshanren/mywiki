---
tags: [unity, ngui, ui, legacy]
date: 2026-04-19
sources: 4
---

# NGUI 遗留 UI 系统（Unity）

NGUI 是 Unity 早期最流行的第三方 UI 套件，在 Unity 4.6 的 UGUI（Canvas/RectTransform）推出之前几乎是商业项目的默认选择。它把 UI 建立在普通 GameObject 之上，通过 [[draw-call|Draw Call]] 合批、Panel 裁剪和 Atlas 图集三件套来实现高效的 2D UI 渲染。Ted Sie 2016 年的入门系列——UIPanel/UISprite、UIAtlas、Scroll View、Button——正好串起了这套系统的骨架。

## 核心对象模型

- **UI Root**：场景根节点，由 `NGUI → Create → 2D UI` 生成，所有 NGUI 物件都必须挂在它下面。它把虚拟像素坐标系、缩放策略和相机组装到一起。
- **UI Panel**：把若干 widget 合成一次 Draw Call 的容器，同时可作为**裁剪 Mask**（Scroll View 就是一个带可调 Size 的 UIPanel）。
- **UISprite**：从 [[ngui-uiatlas|UIAtlas]] 中取出的一张图片，多个 UISprite 共享 Atlas 即可合并 Draw Call。
- **UITexture**：直接绑一张独立贴图显示，无需走 Atlas；代价是每张 UITexture 大概率独占一次 Draw Call。

## Atlas 与 Draw Call 的关系

Ted Sie 的 Draw Call 初阶文章用几个极简场景把因果关系讲清楚：

- 两个平面共用 `Material_1` → DrawCall = 2（即便材质相同，渲染路径/对象各自一次）。
- 其中一个换成 `Material_2`（Shader 相同但 Material 不同）→ DrawCall = 3，说明**材质实例本身就是拆批的边界**。
- NGUI 场景里有多张 UISprite，但 DrawCall 依然维持在 2——因为它们来自同一个 [[ngui-uiatlas|UIAtlas]]，共享同一个 Material，NGUI 在 UIPanel 层把它们合成一次提交。

这就是 NGUI 把"打图集"奉为第一要务的根本原因，也是老一代 Unity 项目里美术管线与程序性能深度耦合的由来。详细的 Draw Call 成本模型见 [[draw-call]]。

## Button 交互系统

NGUI 把按钮拆成一组可叠加的 `UIButton*` 组件（必须先挂 Collider 才能响应）：

- **UIButton**：基本按钮，支持 Normal/Hover/Pressed/Disabled 四态的颜色与 Sprite 切换，带 On Click 事件槽。
- **UIButtonActivate**：点击后开关目标物件。
- **UIButtonColor**：只切颜色的简化版，编辑器里可以 `Upgrade to a Button` 补全。
- **UIButtonOffset / UIButtonRotation / UIButtonScale**：三个同构的 tween 组件，分别对 Position/Rotation/Scale 做 Hover 与 Pressed 两态插值，带 Duration。
- **UIButtonKeys / UIButtonMessage (Legacy)**：已弃用。

这种"组件叠加"的风格是 Unity 2016 年前的典型做法——UI 反馈不是写在 shader 或 animator 里，而是靠一组小脚本拼出来。放到今天 UGUI 的体系里，这些职责会被合并成 Button + Animator 状态机 + 可选的 DOTween 补间链。

## Scroll View = UIPanel 做 Mask

NGUI 的 Scroll View 不是一个独立控件，而是把 UIPanel 的"裁剪 Size"当 Mask 用：

1. 在 Sprite 上加 Collider + UIScrollView 脚本；
2. `NGUI → Create → Scroll View` 生成容器，把 Sprite 拖进去当子节点；
3. 调容器 UIPanel 的 Size，超出部分被自动剪掉——就是一个可滑动窗口。

这比 UGUI 的 Mask/RectMask2D 更朴素，但也揭示了"Panel 即裁剪域"这一 NGUI 设计决策——它把合批与裁剪绑到同一个容器上，互相约束（过大的裁剪区 = 更大的 overdraw；过小的 Panel = 更多 Panel = 更多 Draw Call）。

## UIAtlas 的日常维护

Atlas Maker 面板支持四类操作：

- **新增 / 更新**：拖图进 UI Atlas，按 Add/Update，按钮文案会根据是否已存在自动切换。
- **导出**：Inspector 里选择 Atlas，勾选要导出的图片，按 Save As 回写成独立 PNG。这对已把零碎源图从工程里剔除的项目非常关键——Atlas 变成了图片的"版本仓库"。
- **移除**：在 Atlas Maker 里按图片旁的 X → Delete。

这套流程暴露了 NGUI Atlas 的本质：它是一个编辑器态工具搭起来的打包流水线，Atlas 本身又被当作资源原始副本使用，和现代 Sprite Atlas / SpriteAtlasV2 的"纯构建产物"理念正好相反。

## 与 UGUI 的对照

| 维度 | NGUI（2016） | UGUI（Unity 4.6+） |
|---|---|---|
| 坐标系 | 普通 Transform | RectTransform |
| 容器 | UIPanel（合批 + 裁剪） | Canvas + RectMask2D |
| 图集 | UIAtlas（编辑器资源） | Sprite Atlas（构建产物） |
| 相机 | UICamera 必须 | Canvas 可选 |
| 交互 | UIButton* 组件家族 | Button + EventSystem |

理解 NGUI 对今天仍然有价值——许多长生命周期项目、保留了 NGUI 管线的手游仍在维护；而它对 Draw Call / Atlas / Panel 的权衡，也是所有 2D UI 系统绕不开的问题。

## 相关

- [[draw-call]] — NGUI 合批的理论基础
- [[ted-sie]]

## Sources

- [[sources/tedsie-ngui-tutorials]]
