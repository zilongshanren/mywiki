---
tags: [ai-assisted, c, cpp, safety]
date: 2026-04-19
sources: 1
---

# C 对 AI 也不安全——用 C++ 代替

[[chris-wellons]] 的观察（2026 年 3 月）：即便是前沿 AI，在 C 上仍然会反复出内存安全错误；C++ 显著更可靠。

作者在自己的 [[quilt-cpp-ai-driven-clone|Quilt.cpp]]（~9KLoC C++）中只发现三个内存安全 bug：

- 两个 `strtol` 的 null-terminator 问题——本质是 AI 在“写 C 风格”，改用 `std::from_chars` 后问题消失
- 一个 `std::vector::back` 在空 vector 上的冷门分支

而在 C 上他尝试过用 arena allocation、counted string、slice 等更安全的技术指导 AI，结果并不理想——AI 对这些技术“懂但做不到稳定落地”。

作者的结论（写给自己“一贯偏好 C”的读者群）：

> 在 AI 协作时代，选 C 是一个反生产力的决定。

这不是说 C 不安全（那是老生常谈），而是说：AI 对 C++ 标准库（`std::string_view`、`std::span`、`std::from_chars`、`std::filesystem`）更熟练、写出的代码更不容易崩；这在“让 AI 写代码”的新工作流里具有决定性权重。

相关的 steering 技巧：

- 明确告诉 AI “不要直接用 libc”
- 要求使用 `std::from_chars` 而不是 `strtol`
- 用 `_GLIBCXX_DEBUG` 和 sanitizers 建立护栏

## 相关

- [[quilt-cpp-ai-driven-clone]]
- [[vibe-coding-workflow]]

## Sources

- [[sources/nullprogram-ai-programming-quiltcpp]]
