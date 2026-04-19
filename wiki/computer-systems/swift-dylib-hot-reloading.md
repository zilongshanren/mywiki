---
tags: [Swift, macOS, 热重载, 动态链接, SwiftUI, 工具链]
date: 2026-04-19
sources: 1
---

# SwiftUI 动态库热重载

Xcode Previews 的替代方案：把 UI 代码编成一个 `.dylib`，宿主 App 用 `dlopen` / `dlsym` 加载并渲染；UI 代码改动后重新编译 dylib，宿主在 1 秒内 swap 进去。Daniel Hooper 的实现只有 **120 行**、不引入第三方依赖，工程结构比 [HotSwiftUI](https://github.com/johnno1962/HotSwiftUI)（dyld interposition + swizzling + 内存补丁）简单得多，缺点是需要主动把工程拆成 library / host 两个 target。与 [[binary-hot-reload|游戏引擎的 DLL 热重载]] 是同一思路，区别在于 Swift 特有的两个坑。

## 两个 Swift 特有障碍

**坑 1：名字粉碎（name mangling）**。Swift 为支持函数重载会把 `createView()` 改名为 `$s9UIPreview10createViewQryF` 这种天书。`nm -g` + `swift demangle` 能看到原名，但直接拿粉碎名去 `dlsym` 会让代码脆化、无法适应改名。

**坑 2：Swift 函数指针是 16 字节**。`dlsym` 返回 8 字节地址，Swift 函数还额外带 8 字节捕获上下文，`unsafeBitCast` 直接挂。

两个坑的统一解法是 `@_cdecl("createView")`：把 Swift 函数按 **C ABI 导出**，既绕过 name mangling（自定义名字），又返回纯 8 字节函数指针。但 C 函数无法返回 `some View` 或任何 Swift 类型——解法是返回 `NSView`（Objective-C 类型可从 C 函数返回），用 `NSHostingView` 把 SwiftUI View 包进去。宿主那边用 `NSViewRepresentable` 再把 `NSView` 桥回 SwiftUI，完成 `SwiftUI → NSView → SwiftUI` 的往返。

```swift
// library.swift
@_cdecl("createView")
public func createView() -> NSView {
    return NSHostingView(rootView: TodoListView(state: AppState()))
}
```

## 触发 dlopen 重新读盘

`dlopen` 对同路径会增加引用计数但 **不重新从磁盘读内容**，所以单改 `UIPreview.dylib` 文件没用。Hooper 的绕法是每次 swap **把 dylib 拷到新路径**，文件名在 `"true.dylib"` / `"false.dylib"` 之间 toggle：

```swift
func openLibrary() -> UnsafeMutableRawPointer? {
    let tmpDylibName = "\(fileNameToggle).dylib"
    try? fm.removeItem(atPath: tmpDylibName)
    try? fm.copyItem(atPath: dylibName, toPath: tmpDylibName)
    fileNameToggle.toggle()
    return dlopen(tmpDylibName, RTLD_LOCAL | RTLD_FIRST)
}
```

检测变化只看文件 mtime——严肃版应该用 FSEvents，但 1 秒轮询对 UI 开发足够。

## 状态跨重载存活

**一旦库 unload，库里 `@Published` 的所有 `AppState` 也消失**——现象是 hot reload 一次，你刚加的 todo 条目就没了。解法是把 state 的**所有权交给宿主**：库只提供 `createState()` 构造一块 opaque 指针交给宿主保管，`createStatefulView(ptr)` 接收这块指针构造 View。

```swift
@_cdecl("createState")
public func createState() -> UnsafeMutableRawPointer? {
    return Unmanaged.passRetained(AppState()).toOpaque()
}

@_cdecl("createStatefulView")
public func createStatefulView(state_ptr: UnsafeMutableRawPointer) -> NSView {
    let state = Unmanaged<AppState>.fromOpaque(state_ptr).takeUnretainedValue()
    return NSHostingView(rootView: TodoListView(state: state))
}
```

宿主只在第一次调一次 `createState`，后续每次 swap 只换 `createView`。这一步解决后，**加/删/编辑** UI 行为代码不会丢 app 内数据。

## 没解决的部分：state 结构变化

和 [[binary-hot-reload]] 中 Max Slater 说的完全一样：**改 state 结构（加字段、改 field 顺序、改类型）会 crash**——旧内存布局 × 新代码解释，几乎肯定对不上。两个缓解：

1. 反射序列化 + 反序列化（没人真做到）；
2. 在 `AppState` 里加一个 `version: Int`，库里看到版本不匹配就丢旧 state 重建——UI 会清空但不崩。

## 相比 Xcode Previews 的增量

- **真实渲染路径**：不是模拟的 `PreviewProvider`，而是 SwiftUI 真 running，所有自定义 NSView、AppKit 组件、IPC、文件 IO 都正常工作；
- **状态真的留着**：Previews 每次都是 fresh render；热重载的 state 在 app 进程里持久；
- **编译时间只包含 library target**：Previews 编译整个模块树，这套只编库，秒级 rebuild。

## 相关

- [[binary-hot-reload]] — 游戏引擎 C++ 版 DLL 热重载，五个通用坑（memory / threads / function pointers / string literals / struct layout）
- [[cpp-runtime-reflection]] — Slater 在 Exile 里为序列化状态写的反射框架，是 struct layout 变化的理论解
- [[linear-allocator]] — 把分配器从宿主传进库是跨重载保持内存的一种选择
- [[daniel-chase-hooper]]

## Sources

- [[sources/hooper-swiftui-hot-reloading]]
