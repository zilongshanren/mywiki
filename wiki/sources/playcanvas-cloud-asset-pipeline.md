---
tags: [source, playcanvas, asset-pipeline, html5]
date: 2026-04-19
sources: 1
---

# Importing in the Cloud: New Asset Pipeline（PlayCanvas Blog）

[[dave-evans]] 发表于 2013 年 6 月的 PlayCanvas 官方博客文章，宣布浏览器端资产导入管线上线。

## 摘要

文章很短，核心信息是一句话：**PlayCanvas 把资产转码搬到了云端**。开发者不再需要下载安装命令行工具链把美术资产转成 PlayCanvas 格式，只要把 FBX 或 COLLADA 文件拖进浏览器，服务器端完成所有转换。文章以一个 5 分钟演示视频收尾，演示如何把 Mixamo 上的模型和动画在几分钟内送进 PlayCanvas 游戏。这是 2013 年时相当早的"pure web engine"产品判断：如果整个开发循环都在浏览器里完成，asset 流水线就必须 server-side。

## 关键要点

- 2013-06 上线的浏览器端资产导入功能
- 取消本地命令行工具链依赖
- 支持 FBX / COLLADA 直接上传
- 与 [[will-eastcott|Will Eastcott]] 后续推动的 Editor-only workflow 一脉相承
- 云端转码栈实现细节未披露（gap）

## 链接到的概念

- [[playcanvas-cloud-asset-pipeline]]
- [[dave-evans]]
- [[will-eastcott]]

## 原文

- 链接：https://blog.playcanvas.com/importing-in-the-cloud-the-new-asset-pipeline
- 本地：`raw/articles/blog.playcanvas.com/2013-06-21_importing-in-the-cloud-new-asset-pipeline-playcanvas-blog.md`
