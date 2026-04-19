---
tags: [cross-compile, windows, linux, wine, pkg-config]
date: 2026-04-19
sources: 1
---

# u-config Frankenwine：单二进制双身份 pkg-config

[[chris-wellons]] 的 u-config 是一个零依赖的 pkg-config 重写。在 2026 年 1 月的博文里，他把 u-config 改造成一个 **既是 Windows 原生 pkg-config.exe、又在 Wine 下自动变成 Linux 交叉 pkg-config** 的单二进制，绕开 Debian `x86_64-w64-mingw32-pkg-config` 配置错乱的老问题。

思路脱胎于 Cosmopolitan Libc 的多人格理念，但实现方式更小：仅合并 u-config 现有的两个平台层——Win32 层（Windows API）和 Linux 层（x86-64 inline asm 直接发 syscall，无 libc）。

三个技术支点：

1. **[[wine-linux-syscall|Wine 下发 Linux syscall]]**：Windows 进程在 Wine 下仍然是普通 Linux 进程，可以用 `syscall` 指令绕过 Win32 与内核对话
2. **运行时侦测 Wine**：`GetProcAddress(GetModuleHandleA("ntdll"), "wine_get_version")` 存在 ⇒ 在 Wine
3. **[[unity-build-macro-renaming|Unity build + 宏改名]]**：两个平台层都定义 `os_write/os_mapfile/...`，作者用 `#define os_write win32_write` 配合 `#include` 的手法在不改一行源码的前提下合并

Entry point：

```c
void __stdcall merge_entrypoint() {
    wine_detected = running_on_wine();
    if (wine_detected) {
        // 伪造 Linux 初始栈：argc/argv
        u8 *fakestack[CMDLINE_ARGV_MAX+1];
        c16 *cmd = GetCommandLineW();
        fakestack[0] = (u8 *)(iz)cmdline_to_argv8(cmd, fakestack+1);
        entrypoint((iz *)fakestack);
    } else {
        mainCRTStartup();
    }
}
```

build：`cc -nostartfiles -e merge_entrypoint -o pkg-config.exe main_wine.c`，`-e` 选择新的入口。

还有两个“坑”值得记录：

- **[[lp64-vs-llp64|LP64 vs LLP64]]**：作者早期写 Linux 平台层时用了 `long`（LP64 下 64 位），移植到 Windows（LLP64 下 32 位）时必须改成 `ptrdiff_t`；尝试用宏替换 `long` 又撞上 `long long` 是多 token 这个 C 预处理器的老毛病
- 最终 Debian 下通过 Wine binfmt 运行同一个 exe 得到正确的交叉 sysroot 结果；在 Windows 下则走 w64devkit 路径

## 相关

- [[wine-linux-syscall]]
- [[unity-build-macro-renaming]]
- [[lp64-vs-llp64]]

## Sources

- [[sources/nullprogram-u-config-wine]]
