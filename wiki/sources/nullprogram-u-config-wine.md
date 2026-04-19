---
tags: [source, computer-systems, windows, linux, build-systems]
date: 2026-04-19
sources: 1
---

# Frankenwine：一个二进制同时是 Windows pkg-config 和 Linux 交叉 pkg-config（Chris Wellons / nullprogram）

[[chris-wellons]] 发表于 2026 年 1 月的文章，展示如何让 u-config 的单个 `pkg-config.exe` 在 Windows 上作为原生程序运行，而在 Wine 下自动变身为 Linux 进程直接发 syscall。

## 摘要

作者借鉴了 gpfault.net 上“从 Wine 进程发 Linux syscall”的思路以及 Cosmopolitan Libc 的多重身份理念，把 u-config 现有的 Windows 平台层与 Linux（基于 x86-64 inline asm syscall，非 libc）平台层合并进同一个 EXE。运行时通过 `GetProcAddress(GetModuleHandleA("ntdll"), "wine_get_version")` 检测是否在 Wine 下，分发到对应的 `os_write/os_mapfile/...`。两个平台层都定义了同名函数，作者用 unity build + `#define` 前缀改名技巧分别包装为 `win32_*` 和 `linux_*`。还需处理 Linux 侧假定 LP64 而 Windows 是 LLP64 的类型差异。最终一个 `merge_entrypoint` 根据 `running_on_wine()` 要么调用 `mainCRTStartup`，要么伪造一份 Linux 栈（含 argc/argv）调用 Linux entrypoint。实测在 Debian 下用 Wine binfmt 运行该 exe，能正确走 `/usr/x86_64-w64-mingw32/` 交叉 sysroot；直接在 Windows 下运行同一个 exe 则走 w64devkit 的路径。

## 关键要点

- 侦测 Wine：查 `ntdll!wine_get_version` 导出
- Unity build + `#define os_write win32_write` 可以在不改源码的情况下合并两个同名平台层
- LP64 vs LLP64：Linux 平台层假设 `long` 是 64 位，移植到 Windows 前需改 `ptrdiff_t`
- 伪造 Linux 初始栈传给 entrypoint 即可复用 Linux 平台层
- 这使 Debian 下的交叉 pkg-config 彻底绕开被错误配置的 `x86_64-w64-mingw32-pkg-config`

## 链接到的概念

- [[u-config-frankenwine]]
- [[wine-linux-syscall]]
- [[unity-build-macro-renaming]]
- [[lp64-vs-llp64]]

## 原文

- 链接：https://nullprogram.com/blog/2026/01/19/
- 本地：`raw/articles/nullprogram.com/2026-01-19_null-program.md`
