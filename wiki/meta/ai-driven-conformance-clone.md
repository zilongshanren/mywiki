---
tags: [ai-assisted, methodology, testing]
date: 2026-04-19
sources: 1
---

# AI 驱动的 Conformance 克隆法

[[chris-wellons]] 在 [[quilt-cpp-ai-driven-clone|Quilt.cpp]] 中总结的一套“用 AI 克隆既有命令行工具”的方法论，同样适用于类似 [eli.thegreenplace 的 pycparser 重写](https://eli.thegreenplace.net/2026/rewriting-pycparser-with-the-help-of-an-llm/) 等场景：

1. **用 AI 生成 conformance 测试套件**——输入是：原版程序、man page、在线文档
2. **用原版实现验证这套测试**（`-DQUILT_TEST_EXECUTABLE`）——保证测试本身正确
3. **用另一组 AI agent 在架构指引下写代码过测试**，配合 sanitizers / debug 模式做护栏
4. **迭代补漏**：人类查 man page / 手工试用，定位测试集漏洞；AI 再补测试 + 对原版验证；多个 agent 并行修复

关键观察：

- AI 在 **可执行的参考实现** 面前非常高效——它能真正“运行 & 比较”，而不是只基于文档猜
- 测试在这里既是质量护栏也是 AI 的“地面实况”，代替了 AI 无法使用调试器的缺失能力
- 与 CMake + CTest 组合尤其契合，因为 AI 对 CMake/CTest 非常熟练
- 因为这种方法高度依赖“对照原版”，所以它特别适合克隆 CLI 工具、协议实现、解析器等“行为可外部观察”的软件；不太适合 UI 或包含大量不可观察副作用的系统

相较传统“按规格写代码”的思路，差别在于：规格太抽象、AI 容易在边界情况上幻觉；有一个可执行参考后，测试可以被自动校准到与真实行为一致，AI 就不再需要“理解”规格，只需要“对齐行为”。

## 相关

- [[quilt-cpp-ai-driven-clone]]
- [[vibe-coding-workflow]]
- [[automated-test-philosophy]]

## Sources

- [[sources/nullprogram-ai-programming-quiltcpp]]
