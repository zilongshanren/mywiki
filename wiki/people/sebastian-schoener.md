---
tags: [人物, 作者, 编译器, unity, mono, zig, c++]
date: 2026-04-19
sources: 5
---

# Sebastian Schöner

德国工程师，博客 [blog.s-schoener.com](https://blog.s-schoener.com/)。长期关注 Unity/Mono/IL2CPP 运行时的 codegen 质量、C++ 工程实践、ABI、热重载、Zig 编译器等底层议题。最近的主线工作是「改 Mono 自己让 Unity 游戏在 Mono 上跑得更快」以及 il2cpp 的 postprocessor 工具 `cpp2better`。

## 主要主题

- Unity Mono JIT codegen 改良：值类型（`float4`/`Vector3`）场景下把 400 行冗余汇编压到 20 行
- 指针别名分析、死代码消除等经典编译器优化在嵌入到现成 JIT 时的工程取舍
- Zig 与 C 的 DLL 边界对比：ABI 故事、`pub` vs header、错误返回链
- 二进制热重载（DLL swap）、函数指针、全局状态迁移
- Windows x64 细节、链接器、构建系统

## 相关

- [[mono-jit-pipeline]]
- [[pointer-alias-analysis]]
- [[dead-store-elimination]]
- [[zig-c-abi-boundary]]
- [[header-file-vs-pub-export]]
- [[binary-hot-reload]]
- [[cpp-multi-paradigm-discipline]]

## Sources

- [[sources/schoener-i-miss-header-files]]
- [[sources/schoener-better-mono-codegen]]
- [[sources/schoener-mono-codegen-part-1]]
- [[sources/schoener-mono-codegen-part-2]]
- [[sources/schoener-zig-hot-reload-abi]]
