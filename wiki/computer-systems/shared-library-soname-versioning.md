---
tags: [linux, abi, shared-library, 版本]
date: 2026-04-19
sources: 1
---

# Shared Library SONAME 与 ABI 版本

Linux 共享库 `libfoo.so.X.Y.Z` 的 **SONAME（major 版本号）** 是链接器在运行时用来匹配「兼容的同一个库」的标识。语义是：**同一个 SONAME 必须保持 ABI 兼容**——老程序在不重新编译的前提下应当能加载并正常工作。升 major = 宣布 break，下游必须重新编译。

这个约定看似清楚，实操里总有边角。Ben Supnik 在 2010 年的 OpenAL/Linux 事件里遇到一个典型案例：发行版把 `libopenal.so.0` 用完全重写的 `libopenal.so.1` 替换、同时**删除 `libopenal.so.0`**，并要求所有应用重新编译。争议的焦点是：这次 major 升级**是否正当**。

## 扩展机制不应算进 ABI

OpenAL 像 OpenGL 一样有 **extension 机制**：程序在运行时 `GetProcAddress` 拿扩展函数指针，只有当扩展字符串存在时才调用。因此：

- 扩展符号（`_LOKI`、`_EXT` 等）本质上**不属于 link-time ABI**——应用从不依赖它们在 `.so` 导出表里出现。
- 扩展可能随硬件/驱动变化——上一代显卡有、下一代就没了，这是 extension 设计本身允许的。
- 去掉扩展符号**不应**触发 SONAME 升 major。

真正计入 ABI 的只有核心规范里规定的符号。

## "误导出的私货符号"怎么办

OpenAL 那次还有一个 `alBufferAppendData` 符号——历史上曾经作为 streaming 候选，后来从 1.0 规范里删除、挪进扩展，但 **旧实现把它以未装饰的名字导出在了核心里**。这是**原始实现的 bug**：不该出现在 `.so` 导出表里的东西出现了。

新实现要不要为了向后兼容把它补回来？两条路都有道理：

- **不补**：承认老库的导出是错的，走 SONAME 升级让新老并存——`.so.0` 留给老程序、`.so.1` 做正确的事。代价是所有发行版要长期保留两份。
- **补回去**：让应用无感升级，但等于永远背着一个规范外的历史包袱。

Supnik 的遗憾不是哪条路都错，而是**发行版选了最差的组合**：SONAME 升了 major（暗示不兼容），却又**删除旧 `.so`**（不让共存），同时要求应用重新编译。这不是 ABI 管理，是制造混乱。

## 应用端的自保：`dlopen` 双 SONAME

X-Plane 的应对是运行时 `dlopen` 试开 `libopenal.so.0` 或 `libopenal.so.1`——哪个在就用哪个。这对核心 API 兼容的库有效，因为「核心 spec 符号」在两边都有。代价是放弃静态链接和 link-time 检查，并且必须自己写函数指针表。

更一般的教训：当一个生态里 SONAME 升级不严谨时，应用层只能用 `dlopen` 做防御性编程。这也是为什么 [[opengl-extension-bucket-strategy|OpenGL 扩展加载库]]（GLEW / GLAD）早早标准化了。

## 相关
- [[ben-supnik]]
- [[opengl-extension-bucket-strategy]]
- [[function-vs-data-pointer-portability]] —— dlsym/GetProcAddress 返回的函数指针在 POSIX 里的跨类型转换问题
- [[linux-graphics-stack-dri]]
- [[cross-platform-openal-runtime-loader]] —— 同一作者后续写到三平台装 OpenAL 的统一策略，Linux 侧正是 dlopen 双 SONAME fallback

## Sources
- [[sources/supnik-openal-linux-part-27]]
