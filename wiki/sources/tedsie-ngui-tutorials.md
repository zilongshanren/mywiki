---
tags: [source, unity, ngui, ui, tutorial]
date: 2026-04-19
sources: 4
---

# NGUI 入门四讲（Ted Sie / 阿祥的开发日常）

[[ted-sie]] 于 2016 年 7 月发表的 NGUI 系列教学四篇合并摘要，覆盖面板建立、图集维护、Scroll View 和 Button 组件家族。目标读者是当年从 Unity 原生 GUI 或第三方 UI 切过来的开发者。

## 摘要

这组文章把 NGUI 的核心工作流串起来：先由 `NGUI → Create → 2D UI` 生成 UI Root 作为所有 UI 的宿主；用 UISprite/UITexture 放图，其中 UISprite 从 UIAtlas 里取图能参与合批；通过 Atlas Maker 完成图集的新增、更新、导出与移除——特别是导出功能让 Atlas 兼具"资源原始副本"角色；Scroll View 本质上是一个把 UIPanel 当 Mask 用的容器，通过调 Size 裁出可滑动窗口；Button 系列则拆成 UIButton（多态色 + Sprite 切换）、ButtonActivate（开关目标）、ButtonColor（仅颜色）、ButtonOffset/Rotation/Scale（三个同构 tween 组件）等一组可叠加小脚本。四篇合起来揭示了 NGUI 的核心设计：**UIPanel 同时负责合批与裁剪，UIAtlas 是 Draw Call 优化的前提**。

## 关键要点

- UI Root 是 NGUI 的根节点，所有 UI 物件必须挂在它下面。
- UISprite 走 Atlas，UITexture 绑独立贴图；前者能合批，后者通常独占一次 Draw Call。
- UIPanel 的 Size 同时决定"裁剪区"和"合批边界"，Scroll View 就是它的一个应用。
- Button 要挂 Collider 才能响应。UIButton 的 Hover/Pressed/Disabled 多态切换支持 Color 与 Sprite 两类。
- UIButtonOffset/Rotation/Scale 三个组件结构完全一致，只是驱动的 Transform 分量不同——是 tween 组件库的一个迷你例子。
- Atlas Maker 的 Add/Update 文案根据图片是否已存在动态切换，Save As 可把 Atlas 里的子图导出回独立 PNG。
- `UIButtonKeys` / `UIButtonMessage` 已标注为 Legacy，不建议使用。

## 链接到的概念

- [[ngui-legacy-ui-system]]
- [[draw-call]]
- [[ted-sie]]

## 原文

- 链接：
  - <https://tedsieblog.wordpress.com/2016/07/10/ngui-tutorial-comment-on-uipanel-and-uisprite/>
  - <https://tedsieblog.wordpress.com/2016/07/10/ngui-tutorial-comment-on-uiatlas/>
  - <https://tedsieblog.wordpress.com/2016/07/10/ngui-tutorial-comment-on-scroll-view/>
  - <https://tedsieblog.wordpress.com/2016/07/10/ngui-tutorial-comment-on-button/>
- 本地：
  - `raw/articles/tedsieblog.wordpress.com/2016-07-10_comment-on-uipanel-and-uisprite-jian-li-ngui-mian-ban-jian-l.md`
  - `raw/articles/tedsieblog.wordpress.com/2016-07-10_comment-on-uiatlas-ngui-tu-ji-xin-zeng-geng-xin-dao-chu-yi-c.md`
  - `raw/articles/tedsieblog.wordpress.com/2016-07-10_comment-on-scroll-view-ke-hua-dong-qu-kuai-scroll-view.md`
  - `raw/articles/tedsieblog.wordpress.com/2016-07-10_comment-on-button-button-xi-lie-gong-neng-jiang-jie.md`
