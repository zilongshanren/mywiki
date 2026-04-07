---
tags: [计算机系统, csapp, 编译]
date: 2026-04-05
sources: 1
---

# 编译系统四阶段

```
C source → [预处理] → [编译] → [汇编] → [链接] → 可执行文件
```

## 四阶段

| 阶段 | 输入 | 输出 | 职责 |
|---|---|---|---|
| **预处理（Preprocessing）** | .c | .i | 处理 `#include`、`#define`、条件编译 |
| **编译（Compilation）** | .i | .s | C → 汇编；优化决策都在这里 |
| **汇编（Assembly）** | .s | .o | 汇编 → 机器码（几乎机械转换） |
| **链接（Linking）** | .o + 库 | 可执行文件 | 符号解析、地址重定位 |

## 理解编译系统的价值（CSAPP）

> "Understanding how the compiler works enables you to write better programs."

> "Understanding linking helps you avoid insidious and hard-to-find programming errors."

## 优化示例

- **switch → 跳转表（O(1)）** vs if-else 链（O(n)）。
- **Inline expansion**：小函数内联消除调用开销。
- **Dead code elimination**：移除不可达代码。
- **RIP-relative addressing**：位置无关代码（PIC）。

## 对游戏开发的意义

- Unity IL2CPP：C# → IL → C++ → native，多层编译。
- 崩溃栈追踪读懂要懂汇编约定（x86-64 System V ABI）。
- Shader 编译也有类似多阶段：HLSL → DXIL/SPIR-V → GPU-specific 指令。

## 相关

- [[bits-and-context]]
- [[virtual-memory]]

## Sources

- [[sources/csapp-day01]]
