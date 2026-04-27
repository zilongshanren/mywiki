---
tags: [source, programming-languages, games, survey]
date: 2026-04-27
sources: 1
---

# 2011 年游戏编程语言调查（Angelo Pesce / C0DE517E）

[[people/angelo-pesce]] 发表于 2011 年 5 月的文章，呈现了一次面向游戏开发者的编程语言使用与偏好调查结果（174 份有效回答）。

## 摘要

Pesce 在 2011 年通过 SurveyMonkey 收集了 174 份游戏开发者的问卷，调查现状与未来偏好。结果显示 C++ 仍是主力但颇受抱怨；Lua 是最主流的脚本层；D 语言是唯一出现明显上升趋势的语言（现有 2 票，期望 12 票），说明人们期待一个"更好的 C++"而非彻底不同的范式。专有脚本系统和 DSL 均不受看好，C# 的使用预期保持平稳而非上升。问卷还揭示了 C++ 被选用的核心原因：平台覆盖、直接内存操作、类封装和编译期类型大小确定；而继承、模板、异常处理等特性评价较低。

## 关键要点

- C++/C、Lua、C# 是 2011 年游戏开发三大主流语言，未来预期变化不大
- D 语言是唯一出现明显期望增长的语言，从 2 份增至 12 份
- 专有脚本系统被认为缺乏前景，受访者不愿再在其上投入
- C++ 最大优势：平台支持（86.8%）、原始内存操作、类封装、编译期类型大小
- C++ 最差特性：STL、RTTI、多继承、异常处理、reinterpret_cast
- 渲染最常用命令式/流式范式；AI 适合函数式/声明式；Gameplay 仍以 OO 和事件为主
- Lua 被视为"设计师层语言"，引擎团队知道它、用它，但不一定喜欢它

## 链接到的概念

- [[programming-languages/lua-design-philosophy]]
- [[programming-languages/orthodox-cpp]]
- [[programming-languages/optional-static-typing]]

## 原文

- 链接：https://c0de517e.blogspot.com/2011/05/2011-future-programming-languages-for.html
- 本地：`raw/articles/c0de517e.blogspot.com/2011-05-08_2011-future-programming-languages-for-games-poll.md`
