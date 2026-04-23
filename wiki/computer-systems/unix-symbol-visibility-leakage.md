---
tags: [unix, linker, dynamic-library, plugin, abi, symbol-visibility]
date: 2026-04-19
sources: 1
---

# Unix 扁平符号命名空间与静态库泄漏

[[ben-supnik]] 2012 年底的一篇长文把 X-Plane 插件系统里一类「一个 plugin 莫名调进另一个 plugin」bug 讲透了——根因是 Unix 链接器用的是**扁平的全局符号命名空间**，这一点和 Windows / 老 Mac 世界完全不同，而 GCC 的默认导出策略又刚好和这件事冲突。

## 扁平命名空间：先到先得

ld（OS X / Linux 通用）的语义是：对一个符号名，**第一个被加载的动态库定义**就是最终定义，后续所有动态库对它的调用都会被路由到第一家。这是一个**进程级的全局单例表**。于是只要两个 plugin 都把 `sasl_done` 标成全局导出，第二个 plugin 调**自己**的 `sasl_done` 时，会跳进第一个 plugin（或者系统 `libsasl2.dylib`）里——随机地爆炸。

对应的反面是：只要符号不是全局的（`hidden` 可见性），它就不可能被覆盖，别人家的全局符号也污染不到你。**"被覆盖"是导出符号才要担心的事。**

## GCC 默认把一切导出

问题在于 GCC 默认 `-fvisibility=default`——**没有特殊标注的函数全部导出**。一个 X-Plane plugin 可能有几千个内部函数，默认状态下全部进入全局表。符号冲突概率随之爆炸。

正确的工程默认应该反过来：`-fvisibility=hidden` + 显式用 `__attribute__((visibility("default")))` 或导出列表点名需要导出的 API 入口。但改默认值不可能，只能每个项目自己记住。

## 静态库泄漏：链接器的意外副作用

更阴险的是**静态库也会把自己的符号泄漏到宿主动态库的导出表**。`.a` 档案本质上是 `.o` 的集合，每个 `.o` 带着自己的可见性属性；当你把 `libpng.a` 静态链进 `myplugin.dylib` 时，只要 `libpng` 的 `.o` 没有刻意用 hidden，它的所有符号就会出现在 `myplugin.dylib` 的导出表里。

Supnik 的经验：`libpng` / `libfreetype` / `libcurl` 这类 `./configure`-based 项目都按「构建共享库」配置导出可见性，做静态库时没人愿意重新审视。结果每个链接它们的 plugin 都在往全局表里偷倒 libpng 符号；两个 plugin 各自带一份不同版本的 libpng，最先加载的那份决定了**大家**用哪个版本——即使你以为自己静态链的是自己那份。

`nm -m`（OS X）或 `objdump -t`（Linux）能查出谁在往外漏。

## 两条可用的工程反制

1. **显式导出清单**（link-time）。传 `-Wl,--version-script=exports.txt`（Linux）或 `-exported_symbols_list exports.symbols`（OS X），列出唯一允许导出的符号名，例如 `_XPlugin*`。链接器会**把其他所有符号强制 hidden**，不管静态库自己怎么标。这招的好处是一刀切，不用对上游库做任何修改。
2. **两层命名空间 / 版本化符号**。OS X 的 two-level namespace（link 时记住符号来自哪个 dylib，运行时只从那个 dylib 拿）是 Windows 语义。Linux 的 glibc 版本化符号（`@@GLIBC_2.0`）更弱但可以缓解 ABI 迁移冲突。X-Plane 的 plugin 系统比这两个机制都更老，所以历史包袱让他们继续绑在扁平命名空间上。

## dlsym 是唯一能绕过命名空间的口子

**唯一的例外**：用 `dlopen` 拿到特定 dylib 的句柄，再 `dlsym(handle, "PluginStart")`——此时查询被限定到那个具体 dylib，不走全局表。这也是为什么 plugin 系统普遍规定一个"入口函数"（`PluginStart`）：宿主 `dlopen` 每个 plugin、`dlsym` 各自的入口；**plugin 之间相互调入口函数时必须也走这条路径**，否则会再次掉进扁平命名空间的陷阱。

## 与相邻话题的联系

与 [[shared-library-soname-versioning]] 一起看能看出 Supnik 的完整观点：Unix 共享库机制在 ABI 层和符号导出层都存在**抽象与实现不匹配**的裂缝，应用作者只能靠显式列表 / dlopen 防御性编程。在 [[cross-platform-openal-runtime-loader]] 里这一思路被推到极致——直接放弃 link-time 绑定，全部运行时查函数指针。对 Unix 历史的背景参考 Drepper 的《How To Write Shared Libraries》。

## 相关

- [[ben-supnik]]
- [[shared-library-soname-versioning]]
- [[cross-platform-openal-runtime-loader]]
- [[function-vs-data-pointer-portability]]
- [[opengl-extension-bucket-strategy]]

## Sources

- [[sources/supnik-static-libs-plugins]]
