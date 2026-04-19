---
tags: [source, 开源, 中间件, 游戏开发]
date: 2026-04-19
sources: 1
---

# Open source or it didn't happen!（Branimir Karadžić）

[[branimir-karadzic]] 2011 年 9 月为 Carbon Games 博客写下的一篇短文，记录了《AirMech》团队把最后一个闭源库从代码库里剔除的决定，并给出一份独立团队挑选开源库的守则。详见 [[middleware-vs-open-source]]。

## 摘要

文章首先澄清：团队并不意识形态地反对商业中间件，但几乎每一次采用中间件都带来**平台锁定、Logo 强制展示、License 谈判成本、厂商平台支持盲区**这些实实在在的阻力。作为独立团队，自由切换平台的能力本身就是商业资产。他们选开源库也有严格标准：小而专、依赖少、易集成易维护，C 优于 C++（后者常复杂得像是为炫耀 metaprogramming 而写）；且要求库不依赖 `exceptions` 和 `RTTI`（与 [[orthodox-cpp]] 的主张一致）。文章用一个 JSON 库选型做范例：客户端端选 **js0n**（单文件 C、只解析可信来源）而不是 **JSON_Spirit**。作者还提到显卡市场 2011 年已高度收敛，独立团队重做引擎比 1990 年代容易得多——这构成"自研 + 开源"路线的可行性基础。结尾承诺未来会把代码中独立组件以 BSD 2-clause 释出——这个承诺后来兑现为 **bgfx**。

## 关键要点

- "开源"不等于"好"——**小而专、易集成、不强求异常/RTTI** 是筛选守则。
- 中间件真正的代价是**平台自由度**，不是 License 费用。
- C 风格的 C++ 库更容易被用；复杂 C++ 库的复杂度常来自作者的自我表达而非用户需求。
- 显卡硬件与驱动生态的成熟让独立团队自研引擎重新变得现实。
- 这篇文章是 Karadžić 后来所有工程观的"第一性原理"式底稿：守则、品味、选型理由全部在此定调。

## 链接到的概念

- [[middleware-vs-open-source]]
- [[orthodox-cpp]]

## 原文

- 链接：https://bkaradzic.github.io/posts/open-source-or-it-didnt-happen/
- 本地：`raw/articles/bkaradzic.github.io/2011-09-20_open-source-or-it-didn-t-happen.md`
