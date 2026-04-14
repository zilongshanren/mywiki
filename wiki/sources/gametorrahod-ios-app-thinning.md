---
tags: [source, game-development, ios, apple, unity]
date: 2026-04-14
sources: 1
---

# มารู้จักกับ App Thinning (ของ Apple)（Sirawat Pitaksarit / Game Torrahod）

Sirawat Pitaksarit 于 2016 年 11 月发在 Game Torrahod 博客上的文章，用泰语快速讲清楚 Apple 在 iOS 9 上推出的 App Thinning 是什么，以及当时 Unity 5.3 如何把它串进 iOS 构建流程。

## 摘要

作者站在 Unity 手游开发者的立场，把 App Thinning 拆成三条机制来解释。**App Slicing** 解决 Universal Binary 把 32-bit/64-bit 以及所有档位的贴图都塞在一起导致下载包巨大的问题——从 iOS 9.0.2 起，App Store 会按设备切片分发，只下发设备用得上的那一份，iPad 与 iPhone 拿到的包因此不再是同一份。**Bitcode** 则把最终编译延后到 Apple 服务端，上传的是类 LLVM IR，体积更大但可以让 Apple 将来用新工具链重新 codegen，省去开发者重打包、重审核的成本。**On-Demand Resources** 把大块可选资源（后续关卡、特定语言素材）托管在 Apple 端，运行时按 tag 拉取，让首包尽量小、降低安装流失率——但只覆盖 iOS，跨平台发布时 Android 仍需自建 CDN。文章体量很小，主要是概念普及 + Unity 5.3 构建面板截图。

## 关键要点

- App Thinning = App Slicing + Bitcode + On-Demand Resources 三件套。
- Slicing 由 App Store 服务端按设备型号切片，开发者仍上传 Universal 包。
- Bitcode 让 Apple 后端在未来重新编译，适合即将停更但想"未来兼容"的游戏。
- ODR 只托管 iOS 侧资源，Android 通常仍要自建资源服务器。
- Unity 5.3 的 iOS 构建面板已内建 App Thinning 开关。

## 链接到的概念

- [[ios-app-thinning]]

## 原文

- 链接：https://gametorrahod.com/app-thinning/
- 本地：`raw/articles/gametorrahod.com/2016-11-10_maaruucchakkab-app-thinning-kh-ng-apple.md`
