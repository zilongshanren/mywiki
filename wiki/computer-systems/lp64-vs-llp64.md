---
tags: [c, types, portability]
date: 2026-04-19
sources: 1
---

# LP64 vs LLP64

两种常见的 64 位 C 数据模型：

| 模型  | `int` | `long` | `long long` | 指针 | 典型系统 |
|-------|-------|--------|-------------|------|----------|
| LP64  | 32    | **64** | 64          | 64   | Linux/macOS/BSD 等 Unix |
| LLP64 | 32    | 32     | **64**      | 64   | Windows x64 |

关键差异在 `long`：LP64 下是 64 位、和指针同宽；LLP64 下只有 32 位。

[[chris-wellons]] 在 [[u-config-frankenwine|u-config Frankenwine]] 一文里吐槽说自己最初把 Linux 平台层的 syscall 返回值用 `long` 承接，觉得“这里有 asm 都没跨平台条件编译，能有什么问题”——结果要把它塞进 Windows 二进制时就崩了。

可移植的替代：

- `ptrdiff_t` — 有符号、指针宽
- `size_t` / `ssize_t` — 大小/带符号大小
- `intptr_t` / `uintptr_t` — 能装下指针的整型
- 固定宽度：`int64_t`

注意 C 预处理器不能简单地用 `#define long ptrdiff_t` 替换 `long`，因为 `long long` 是多 token 类型，会连带坏掉。

实践建议：写 syscall 封装、跨 OS 代码时从一开始就用 `ptrdiff_t`，不用 `long`。

## 相关

- [[u-config-frankenwine]]
- [[avoid-unsigned-types]]

## Sources

- [[sources/nullprogram-u-config-wine]]
