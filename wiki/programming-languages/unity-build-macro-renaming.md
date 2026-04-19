---
tags: [c, build-systems, preprocessor]
date: 2026-04-19
sources: 1
---

# Unity Build + 宏改名合并平台层

在 C 里要让两个平台层实现（它们各自定义了同名的 `os_write`、`os_mapfile` 等函数）共存于同一个二进制，最直接的办法不是重构它们——而是借助 unity build + `#define` 前缀改名，在不改任何一行源码的前提下各自换一件马甲：

```c
#define os_fail    win32_fail
#define os_listing win32_listing
#define os_mapfile win32_mapfile
#define os_write   win32_write
#include "main_windows.c"
#undef  os_write
#undef  os_mapfile
#undef  os_listing
#undef  os_fail

#define os_fail    linux_fail
#define os_listing linux_listing
#define os_mapfile linux_mapfile
#define os_write   linux_write
#include "main_linux_amd64.c"
#undef  os_write
...
```

随后在合并层里提供真正的 `os_*` 函数，基于运行时条件分发：

```c
filemap os_mapfile(os *ctx, arena *a, s8 path) {
    return wine_detected ? linux_mapfile(ctx, a, path)
                         : win32_mapfile(ctx, a, path);
}
```

[[chris-wellons]] 把这种做法形容为 “dirty but effective”。注意事项：

- 只适用于编译单元内部可见的符号；跨翻译单元的符号要改声明头
- C 的多 token 类型名（`long long`、`unsigned int`）对预处理器不友好——无法简单地 `#define long ptrdiff_t` 处理 LP64/LLP64 差异
- 不适合长期维护的合并，但非常适合快速原型和 hack

## 相关

- [[u-config-frankenwine]]

## Sources

- [[sources/nullprogram-u-config-wine]]
