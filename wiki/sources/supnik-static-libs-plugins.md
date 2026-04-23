---
tags: [source, unix, linker, plugin, abi]
date: 2026-04-19
sources: 1
---

# Static Libraries and Plugins: Global Pain（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2012-12-13 的长文，把 X-Plane plugin 系统踩到的一类"插件莫名调进另一个插件"bug 讲透：Unix 链接器的扁平全局符号命名空间 + GCC 默认 `visibility=default` + 静态库符号泄漏，三件事叠起来就是地雷阵。

## 摘要

Unix 风格的 `ld`（OS X / Linux 通用）把所有动态库的导出符号塞进一张**进程级的平表**，同名符号只第一个被加载的那份生效。一个 plugin 把内部函数 `sasl_done` 标成全局，被系统 `libsasl2.dylib` 先占，后加载的 plugin 调"自己的" `sasl_done` 时随机跳进 dylib——崩溃。GCC 默认把一切导出扩大了出事面，而 `.a` 静态库的 `.o` 文件会带着自己的可见性属性被链接器泄漏到宿主动态库的导出表——链接 libpng.a 很可能把整个 libpng 的符号泄漏出去，两个 plugin 各带一份不同版本时更加灾难。工程解法是**显式导出清单**（`--version-script` / `-exported_symbols_list`）或 OS X 的 two-level namespace；dlopen + dlsym 是唯一能绕过扁平命名空间安全点名 plugin 入口的机制。

## 关键要点

- Unix 动态库符号是进程级单例表，先到先得
- GCC 默认 `-fvisibility=default` 把一切导出
- 静态库链接进 dylib 会泄漏 `.o` 里的全局符号
- libpng/libfreetype/libcurl 都按 shared-library 配置导出可见性，做静态链接时漏得到处都是
- `nm -m`（OS X）/ `objdump -t`（Linux）能看到谁在漏
- 显式导出列表（linker）一刀切最省心
- dlopen + dlsym 是 plugin 入口唯一安全的路径

## 链接到的概念

- [[unix-symbol-visibility-leakage]]
- [[shared-library-soname-versioning]]
- [[cross-platform-openal-runtime-loader]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2012/12/static-libraries-and-plugins-global-pain.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2012-12-13_static-libraries-and-plugins-global-pain.md`
