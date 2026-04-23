---
tags: [source, bitsquid, lua, 语言选型, 脚本语言]
date: 2026-04-19
sources: 1
---

# Why Lua?（Bitsquid, 2013-02）

[[niklas-frykholm|Niklas Frykholm]] 2013 年 2 月的选型解释：为什么 Bitsquid 用 Lua 作脚本语言，而不是 JavaScript / C#。

## 摘要

文章以 Bitsquid 的四条设计原则（Simplicity / Flexibility / Dynamism / Speed）为骨架，一条条证明 Lua 的契合度。**Simplicity**：Lua 整门语言语法放得下一页，标准库和 C API 同样极简；哪怕没有 class，20 行 Lua 就能 DIY 一套。**Flexibility**：Bitsquid 让 Lua 控制整条 gameplay loop，同一份引擎跑出过 War of the Roses、Krater、Showdown、Hamilton 四种截然不同的游戏。**Dynamism**：Lua 能在**所有目标平台**（主机、移动、平板）上热重载**整个程序**，C# 的 Edit & Continue 完全做不到。**Speed**：LuaJIT 2 是当时最快的动态语言实现之一，无 JIT 平台上 LuaJIT 的解释器也够用；C 互操作成本极低，热点随时落回 C。缺点专门成段写：Lua 周边生态差——没有官方调试器、Intellisense、Resharper 式的 IDE。作者认为"生态也是语言体验的一部分"，不承认 "这锅不是 Lua 的"。最后他用一段想法收尾：IDE 可以用**类型推断 + 类型提示注释**给 Lua 加上 autocompletion、重构支持、甚至 squiggly 警告——想留到下次 hack day 做。

## 关键要点

- Bitsquid 的四条设计原则：Simplicity / Flexibility / Dynamism / Speed；Lua 在四条上都 align。
- Lua 的语法完整 EBNF 贴在文里，整段不到 30 行。
- "无 class 无 OO" 不是缺陷——20 行 Lua 能长出 class 或 prototype 系统（[[lua-class-pattern]]）。
- Bitsquid 里 Lua 控制 gameplay loop，不是 extension language；一个引擎支持风格完全不同的四款商业游戏。
- 热重载能力是 Lua 相对 C# 的决定性优势——**所有目标平台**，**整个程序**。
- LuaJIT 是"一个人做到最快动态语言实现"的典范；FFI 让 C 互操作几乎零开销。
- Lua 的弱点在**生态**而非语言：缺官方调试器、IDE 支持、refactoring；Decoda 开源解了一部分。
- 类型推断 + hint 注释可作 Lua IDE 的未来方向，作者有意做个 prototype（见 `-- @type Car -> number` 式标注）。
- 评论里讨论了 Squirrel（Crytek 内部的类 Lua 语言）作为替代：Niklas 认为两者差不多，Lua 胜在历史更久、库更多。

## 链接到的概念

- [[lua-design-philosophy]]
- [[lua-class-pattern]]
- [[lua-cpp-binding]]
- [[lua-incremental-gc]]
- [[lua-runtime-dynamism-tricks]]
- [[optional-static-typing]]
- [[flow-graph-data-oriented-runtime]]
- [[niklas-frykholm]]

## 原文

- 链接：<https://bitsquid.blogspot.com/2013/02/why-lua.html>
- 本地：`raw/articles/bitsquid.blogspot.com/2013-02-19_why-lua.md`
