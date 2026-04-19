---
tags: [zig, abi, dll, 热重载, 编程语言]
date: 2026-04-19
sources: 1
---

# Zig 的 C ABI 边界问题

Zig 声称要替代 C，但它有一个关乎生产工程的短板：**跨 DLL 边界时只有 C ABI 故事**。[[sebastian-schoener]] 试图把一个 C 写的、大量依赖 [[binary-hot-reload|DLL 热重载]] 的游戏引擎骨架搬到 Zig，撞上了这堵墙。

## DLL 逼出来的两件事

把程序切成 DLL 天然强制两件事：

1. **一个 ABI**。布尔怎么用字节表示、结构体怎么按调用约定传——编译器不再能「每个调用点各自自由选布局」，必须固定一个所有编译单元同意的接口。
2. **关于代码与数据位置的决策**。全局变量不能有两份；每段代码住哪个 DLL 必须明确。

C 在语言层面就给了你 **实现（`.c` 编译单元）vs 接口（`.h` 头文件）** 的天然切分，换进换出「整合单体构建」和「切成若干 DLL」是顺滑的。Zig 在这两件事上都别扭。

## Zig 语言特性全部没有跨 DLL ABI

Zig 对外导出函数时，如果签名里出现它的语言特性类型，会直接报：

```
error: parameter of type '[]const u8' not allowed in function with calling convention 'x86_64_win'
note: slices have no guaranteed in-memory representation
```

`slice` 这种基础类型都没有稳定内存布局。DLL 导出函数的签名事实上只能回退到 C ABI——这就意味着**你用不了 Zig 的 slice、tagged union、error union 等几乎所有「比 C 更好」的部分**。

## Error return trace 在边界处断掉

Zig 的 `!T` 错误返回不是简单的错误码，编译器会隐式线穿额外参数来记录 `error return trace`——一种不用真的 unwind 栈就能拿到的 stacktrace。这东西没 ABI。跨 DLL 时：

- 错误值需要手动映射成 C 错误码
- error return trace 最多停在 DLL 边界

## 没有「头文件」，import 就是并入

C 里 `#include` 会自然分开声明和定义；Zig 里 `@import` 直接把另一个 `.zig` 文件**并入当前编译单元**。默认结果是一个大 monolith。想要真正的分开编译 + 链接，只能走 C ABI 再手动「重新发明头文件」。

## 绕过方案：手写 + 生成的三文件结构

作者的方案是给每个模块拆出三个 `.zig` 文件，辅以代码生成：

- `string.impl.zig` — 实现代码，顶头标注 `export_surface` 列出要导出的函数及其符号名。
- `string.thunks.zig` — **生成**。每个导出项生成一个 `callconv(.c)` 的 C ABI 薄壁，参数一律降级为 `?*anyopaque` 指针，函数体内部把指针解回 slice/struct，调 `impl` 里的真实实现。
- `string.zig` — **半手写半生成**的「头文件」。它由「手写的类型声明、comptime 函数、anytype 泛型」加上工具自动填入的「转发函数」组成。

最关键的 `generated_startsWith` 转发函数用 `comptime link_options.is_dy` 区分：

- 动态链接构建：`@extern` 取 C ABI 符号 `Core_string_startsWith`，把参数 `&s` 做 `toOpaquePtr` 后调过去
- 单体构建：直接 `@import("string.impl.zig")` 调真实实现

**一份 API 定义** 同时覆盖了 DLL 动态链接和全 inline 的单体构建两种形态——所有用户只 `@import("string.zig")`，什么都不用变。

## 类型降级规则

把任意类型转成 C ABI 参数的通用算法只有几条：

- **已经是指针** → 降级为 `?*anyopaque`
- **值类型** → 取地址传，接收方 `loadIndirectValue` 拷回
- **返回值** → 变成 out 参数指针
- **float / int / bool** → 按值传（保持 C ABI 自然行为）
- **Zig error union** → 放弃，签名里禁止出现

## 稳定 ABI vs 「就某个 ABI」

作者承认**他并没有真的解决 ABI 问题**，只是依赖「同一个 Zig 版本 + 同一组选项下，编译器会给出一致的内存布局」。若真需要 **稳定 ABI**（跨版本、可分发给第三方），他说可以给每个导出函数生成专门的 `extern struct` 实例——试过，可行，但仪式感更重。

## 代价与反思

机器还要做 AST 解析才能把 `impl` 上的文档注释搬到「头文件」里；光做反射不够，因为类型别名会把反射搞糊。作者的中段判断：**能工作，但够不够好还在体验中**；更大的教训是 ——「替代或哪怕超越 C」依旧很难，DLL 作为「代码容器」这个用途让一切没有 ABI 故事的语言显得不够格。

## 相关

- [[binary-hot-reload]] — DLL swap 正是逼出 ABI 需求的场景
- [[header-file-vs-pub-export]] — 同作者对 `pub` 内联导出 vs 独立头文件的消费者视角吐槽
- [[calling-conventions-x86]]
- [[sebastian-schoener]]

## Sources
- [[sources/schoener-zig-hot-reload-abi]]
- 相关阅读：[[mach-engine]]、[[mach-nominated-zig-versions]]、[[zig-package-mirror]]——Mach 生态展示了 Zig 在 pre-1.0 阶段做大型多仓库工程的一整套实践
