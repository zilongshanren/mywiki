---
tags: [source, cpp, raii, openal, debugging, noexcept]
date: 2026-04-19
sources: 1
---

# SASL Crash on El Capitan - the Gory Details（Ben Supnik / Hacks of Life）

[[ben-supnik]] 2015 年 11 月发表，调查了一条 X-Plane 用户升级 macOS El Capitan 后遭遇的插件崩溃。Supnik 本人的代码里没问题——他仍然花时间复盘，因为两条 bug 的叠加产生了重要的通用教训。

## 摘要

X-Plane 用户升级 El Capitan 后，从 SASL 插件驱动的飞机切换回自带飞机时进程 abort。Supnik 复盘出两条 bug 叠加：**Apple OpenAL** 对"仍有播放声源 + device 唯一 context + 未使用 effect"的 context 销毁，析构里会抛出一个 `AudioUnits` 错误码——在 C++98 行为下被外层 catch，在 El Capitan 带来的 Xcode 工具链升级后因 C++11 的**析构函数隐式 noexcept**而直接 `std::terminate`；**SASL** 的清理代码里 `ContextChanger(sound->context)` 写成了匿名临时对象形式（合法 C++，但立刻构造立刻析构，等于什么都没做），导致清理期间根本没切到自己 context，该销毁的声源没销毁、反而跑去动 X-Plane 的声源——正好踩中 Apple bug 的触发条件。深层原因是 SASL 的 context changer 构造时 `alGetError()` 读了不检查就丢弃，六年没暴露。文末给出三条教训：用 API 返回码做调试期断言、不能以"看起来能跑"代替行为验证、非用户可见代码必须设计出可调试性。

## 关键要点

- C++11 起析构函数默认 `noexcept(true)`——抛出即 terminate
- El Capitan 的 Xcode 工具链升级触发了早已存在但被 catch 住的 OpenAL bug
- `ContextChanger(arg)` 是 legal C++ 语法但构造匿名临时对象——RAII 常见陷阱
- 静默丢弃 `alGetError` / `glGetError` = 永远不会自然暴露的 bug 温床
- OpenAL 规范本身定义模糊，"删除带播放声源的 context"属于无人规定的灰色地带
- 返回码的用途是"debug 期断言"不是"运行时错误处理"
- 不可见的 cleanup 代码必须显式设计 log / assert / test

## 链接到的概念

- [[throwing-destructor-noexcept-terminate]]
- [[sasl-context-changer-raii-bug]]
- [[cross-platform-openal-runtime-loader]]
- [[good-software-no-double-check]]
- [[crash-on-unexpected-errors]]
- [[minimize-points-and-types-of-failure]]
- [[ben-supnik]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2015/11/sasl-crash-on-el-capitan-gory-details.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2015-11-20_sasl-crash-on-el-capitan-the-gory-details.md`
