---
tags: [source, Swift, macOS, 热重载, SwiftUI]
date: 2026-04-19
sources: 1
---

# Hot Reloading Is Better Than SwiftUI Previews（Daniel Hooper）

[[daniel-chase-hooper]] 2025 年 10 月的长文（14 分钟），用 120 行 Swift 代码实现一个比 Xcode Previews 更好的 SwiftUI 迭代循环，核心是把 UI 编译成 dylib、主 app 用 `dlopen` / `dlsym` 加载并 swap。

## 摘要

Xcode Previews 每次都 fresh render、且在大模块上编译慢。作者的替代方案：把 UI 代码放进一个 dynamic library，宿主 App 监视文件 mtime，改变就重新加载并换 View。实现中遇到两个 Swift 专属麻烦：**name mangling**（Swift 给每个函数起天书名以支持重载）和 **16 字节函数指针**（Swift 函数带 8 字节捕获上下文）。统一解法是 `@_cdecl("createView")` 以 C ABI 导出，返回 `NSView`（Objective-C 类型才能从 C 函数返回），再用 `NSHostingView` 包裹 SwiftUI View；宿主用 `NSViewRepresentable` 桥回 SwiftUI。`dlopen` 同路径会复用、不重读磁盘，绕法是每次 swap 把 dylib 拷到 `"true.dylib"` / `"false.dylib"` 交替。state 跨重载存活的方案是让宿主持有 `AppState` 的 opaque 指针，`createStatefulView(ptr)` 在新 View 里 revive——与 [[binary-hot-reload|游戏引擎 DLL 热重载]] 完全同构。改 state 结构会崩，用 version 字段识别后重建 state 兜底。

## 关键要点

- `dlopen`+`dlsym` 是整个机制核心，120 行 Swift 无第三方依赖
- Swift 两大坑：name mangling、16 字节函数指针；`@_cdecl` 一次解决
- C 函数无法返回 Swift 的 `some View`——返回 `NSView`（Obj-C 可从 C 返回）
- `dlopen` 对同路径不重读磁盘——文件名在 `true.dylib` / `false.dylib` 间 toggle
- State 跨重载存活：宿主持有 opaque 指针，`createState` 与 `createStatefulView` 分工
- Struct 布局变化无解，加 `version` 字段失配时重建而不是崩溃
- 相比 HotSwiftUI，不需要 dyld interposition / swizzling / 安装第三方 app；代价是工程要拆 library / host 两 target

## 链接到的概念

- [[swift-dylib-hot-reloading]]
- [[binary-hot-reload]]
- [[cpp-runtime-reflection]]
- [[linear-allocator]]

## 原文

- 链接：<https://danielchasehooper.com/posts/hot-reloading-swiftui/>
- 本地：`raw/articles/danielchasehooper.com/2025-10-13_hot-reloading-is-better-than-swiftui-previews.md`
