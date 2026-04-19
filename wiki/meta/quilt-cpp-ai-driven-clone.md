---
tags: [ai-assisted, cpp, case-study]
date: 2026-04-19
sources: 1
---

# Quilt.cpp：AI 驱动的源工具克隆

Quilt.cpp 是 [[chris-wellons]] 2026 年 3 月用 AI 协作在约四天内完成的 [Quilt](https://savannah.nongnu.org/projects/quilt) 补丁管理工具 C++ 克隆，一个约 9KLoC（其中测试与非测试各占一半）的单文件 amalgamation，Windows 下 ~1.6MB 独立 EXE，运行速度比原版 Quilt（Bash + Perl + Coreutils）快约 5 倍，内置 diff/patch 实现，唯一的外部依赖是 `$EDITOR`。

项目动机：[w64devkit](https://github.com/skeeto/w64devkit) 长期缺一个源码控制系统（Git 因平台和 build 难以集成）。作者长年想自己写一个 Quilt 克隆但总没时间，AI 把成本降到了能动手的地步。

方法论（详见 [[ai-driven-conformance-clone]]）：

1. 让一个 AI 根据原版 Quilt 的实现、man page、在线文档生成 **conformance 测试套件**，并对原版实现进行验证
2. 让另一个 AI 在作者的架构指引下写代码过这套测试；开 `_GLIBCXX_DEBUG` 和 sanitizers 做护栏
3. 多天迭代：作者比对 Quilt.cpp 与原版 man page，补漏测试 → 多个 agent 并行修复
4. 作者承认“大部分代码没读过”——某种意义上的 vibe-coding，但测试充分

为什么是 C++ 而非作者惯用的 C：在 9k 行 C++ 里只发现三个内存安全错误，两个是 `strtol` 相关的 null-terminator 问题（AI 在“写 C 风格”），作者随即要求它改用 `std::from_chars` 并尽量不调 libc；另一个是 `std::vector::back` 在空 vector 上的冷门分支。同样的工程在 C 上即便配合 arena/counted string 也不行——AI 写不好。

与 git 的互操作：`quilt mail` 输出可直接被 `git am` 接收的 mbox；`git format-patch` 产物可用 `quilt import`。这让 Quilt.cpp 可以作为“没有 Git 的机器”（例如 Windows XP）上的辅助 VCS。

作者承认其可行性高度依赖原版 Quilt 的存在——AI 很擅长“按可执行参考实现对齐”。

## 相关

- [[ai-driven-conformance-clone]]
- [[c-memory-safety-even-for-ai]]
- [[vibe-coding-workflow]]
- [[chris-wellons]]

## Sources

- [[sources/nullprogram-ai-programming-quiltcpp]]
