---
tags: [wine, linux, windows, syscall]
date: 2026-04-19
sources: 1
---

# 在 Wine 下发 Linux Syscall

Wine 运行的 Windows 程序仍然是普通的 Linux 进程，可以像任何其他 Linux 程序一样用 `syscall` 指令与内核对话。gpfault.net 的文章率先指出这一点，[[chris-wellons]] 则用它构造了 [[u-config-frankenwine|u-config 的双身份二进制]]。

x86-64 下的最小 syscall 封装：

```c
ptrdiff_t syscall3(int n, ptrdiff_t a, ptrdiff_t b, ptrdiff_t c) {
    ptrdiff_t r;
    asm volatile (
        "syscall"
        : "=a"(r)
        : "a"(n), "D"(a), "S"(b), "d"(c)
        : "rcx", "r11", "memory"
    );
    return r;
}
ptrdiff_t write(int fd, void *buf, ptrdiff_t len) {
    return syscall3(SYS_write, fd, (ptrdiff_t)buf, len);
}
```

这么做可以完全绕开 glibc——无需考虑 Win32 vs Linux 的 ABI 兼容问题。

Wine 探测的最简方案是检查 `ntdll!wine_get_version` 是否存在：Wine 的 ntdll 实现会导出这个函数，原生 Windows 不会。

适用场景（不限于 u-config）：

- 需要在 Windows 可执行里同时提供两套平台原生实现
- 交叉编译工具链的“宿主 / 目标”身份切换
- Cosmopolitan Libc 已经把这个思路做到极致；本技巧是轻量版

## 相关

- [[u-config-frankenwine]]

## Sources

- [[sources/nullprogram-u-config-wine]]
