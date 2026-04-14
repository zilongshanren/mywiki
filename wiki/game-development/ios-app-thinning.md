---
tags: [ios, apple, app-distribution, unity, mobile]
date: 2026-04-14
sources: 1
---

# iOS App Thinning（应用瘦身三件套）

App Thinning 是 Apple 从 iOS 9.0.2 起在 App Store 分发链路上加入的一组优化机制，目的是让用户只下载自己设备真正需要的那一份二进制与资源，而不是把 Universal Binary 里所有架构和所有分辨率的素材都拉下来。对 Unity 之类体积容易膨胀的游戏工程尤其重要——Unity 5.3 起已经把相关开关内建到 iOS 构建面板里，大部分情况下开发者不必自己动手拆分。App Thinning 由三条彼此独立又互相配合的机制组成：**App Slicing**、**Bitcode** 和 **On-Demand Resources**。

## App Slicing

Slicing 处理的是"一份包塞进所有架构 / 所有素材"的问题。开发者照旧上传一个 Universal 包，App Store 在服务端按设备型号切片：64-bit iPhone 只下 64-bit 切片，老 iPad 只下它能显示的那一档贴图。例如一份同时塞了 iPad 级高分辨率图与 iPhone 级图的游戏，iPhone 用户就会自动拿到较小的那份，而不再被迫吞下全尺寸素材。前提是用户把系统升到 iOS 9.0.2 以上，否则仍旧拿到完整大包。

## Bitcode

Bitcode 把"最终编译"这一步从开发者机器搬到 Apple 服务器。上传时提交的不是最终机器码，而是接近 LLVM IR 的中间表示，体积会比原始二进制更大（可能多出 100 MB 级别）。好处是：当 Apple 推出新的编译器优化或新指令集支持时，不需要开发者重新打包、重新过审，Apple 就能直接在后端用新工具链重新 codegen 出性能更好的可执行文件。对那些"即将停更但想再坚持几年"的游戏而言，丢一次 Bitcode 版本上去等于给未来几代 iPhone 的编译器升级买了张便车票。

## On-Demand Resources

ODR 针对"首包很小、进入游戏后还要再拉一大包内容"的体验痛点，把大块可选资源托管在 Apple 的 CDN 上，按标签（tag）组织，运行时按需下载。常见用法包括后续关卡、本地化语言素材、只有部分用户会用到的高清包。好处是初次从 Store 下载的体积变小、上架通过率更高，玩家第一次打开时不会被"再等一小时"的二次下载劝退。代价是 ODR 的托管只覆盖 iOS，跨平台发布时 Android 侧通常仍要靠自建的 [[cdn]]（如 AWS S3）另行搭一套资源服务。

## 与引擎构建管线的关系

三件套本质上都在"分发"层做文章，不直接影响运行时渲染或引擎架构，但对资源打包策略有明显牵引：Slicing 鼓励按 variant 组织贴图（不同分辨率、不同压缩格式），ODR 鼓励把大资源拆成可独立下载的 bundle——这和 Unity 的 AssetBundle / Addressables 思路天然契合。整体而言 App Thinning 是 Apple 把"安装包肥胖"问题系统化解决的一次尝试，工程上的收益最终会回流到包体体积、上架转化率和冷启动体验这些面向终端用户的指标上。

## Sources

- [[sources/gametorrahod-ios-app-thinning]]
