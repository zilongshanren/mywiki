---
tags: [cpp, 异常, raii, noexcept, 析构函数]
date: 2026-04-19
sources: 1
---

# 从析构函数抛出：C++11 起的隐式 `noexcept` 与 `std::terminate`

[[ben-supnik|Supnik]] 2015 年调试的 SASL / OpenAL / El Capitan 崩溃根因（见 [[sasl-context-changer-raii-bug]]）把一个常被忽视的 C++ 演化摆到台面：**C++11 起，析构函数默认 `noexcept`，从析构函数里漏出的异常会无条件触发 `std::terminate`**。

## 规则的两次变化

**C++98**：析构函数里抛异常在**正常执行**中合法。但如果析构是在因别处抛出异常而触发的栈展开过程中被调用（destructor-during-unwinding），第二次异常会直接 `std::terminate`——"两次在飞的异常同时存在"是未定义行为的已知触发器。

**C++11**：`noexcept(...)` 取代了 deprecated 的 `throw()` 动态异常规范，并把**所有析构函数默认 `noexcept(true)`**（除非显式写 `~T() noexcept(false)`，或基类成员析构本身带 `noexcept(false)`）。从被 `noexcept` 标注的函数里漏出异常——调用 `std::terminate`。

两条变化组合起来：C++11 之后，只要析构函数里抛出的异常没在析构内部被 catch，不管是否有外层栈展开，结局都是进程 abort。

## 为什么 El Capitan 上才爆

Supnik 报告的症状是：同一份 Apple OpenAL 代码在 Yosemite 上没事、El Capitan 上 abort。根因**不**是 OS X 本身行为变了——是**Xcode 工具链升级**导致二进制升级到更新的 C++ 运行时。在更老工具链的行为下（Yosemite 的 dylib 里的 OpenAL 实现仍然允许析构里抛出并在外层 `alcDestroyContext` 里 catch），两次异常没并存时还能被外层接住；新工具链下的 OpenAL 动态库把析构里抛出的 `AudioUnits` 错误码直接当成 `noexcept` 违规，abort。

这是一个"C++ ABI/运行时升级导致的隐式行为变化"经典案例——库方没改代码，系统升级后崩。

## 工程启示

**不要从析构抛异常**。几乎没有例外。常见规避手段：

- **析构里 catch 吞掉**：把异常转成 logging 或错误标志位，析构函数本身保持 `noexcept(true)`。OpenAL 那段代码原本的设计就是"析构里 throw AudioUnits 错误码 → 外层 `alcDestroyContext` catch 后返回错误码"——在 C++98 下可行、在 C++11 下必须改成"析构里 catch 并 stash 错误，`alcDestroyContext` 结尾读 stash"。
- **用专门的 `close()` / `Finish()` 成员**：析构只 release 资源不报告错误；真正要确认没出问题的地方，让 client 显式调 `close()` 并检查返回码。这和 [[minimize-points-and-types-of-failure]] 的设计思想一致。
- **`noexcept(false)` 的显式放行**：把析构写成 `noexcept(false)`，恢复 C++98 行为。可行但是黑魔法——所有下游容器、`move` 操作都会被隐性影响（比如 `std::vector<T>` 在扩容时不再能用 move，只能 copy）。

## 相关
- [[sasl-context-changer-raii-bug]] —— 这次调试的直接触发案例
- [[cross-platform-openal-runtime-loader]]
- [[good-software-no-double-check]] —— 别把 `noexcept` 析构当逃生门，真正的错误路径要一次性明确走通
- [[minimize-points-and-types-of-failure]]
- [[ben-supnik]]

## Sources
- [[sources/supnik-sasl-crash-el-capitan]]
