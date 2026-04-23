---
tags: [source, bitsquid, async, api, callbacks, futures]
date: 2026-04-19
sources: 1
---

# A simpler design for asynchronous APIs — bitsquid: development blog

[[niklas-frykholm|Niklas Frykholm]] 2012 年 8 月初的文章，讨论异步 API（leaderboard、web fetch 这类有延时返回）的四种常见设计，逐一批评并指向一个激进的简化方向。

## 摘要

四种设计从差到好：(1) 回调——四宗罪：时机失控、callback 内能做什么不明、context 错位、代码流难读；Niklas 见到 callback 脑子里警钟就响。(2) Request 对象或 C++11 `promise`/`future`——比 callback 好但仍是 OO 过度设计，这些对象"什么都不做只传话"，还要求调用者维护释放，脚本绑定也麻烦。(3) ID token——返回一个 `unsigned`，用一个独立函数查状态。不设 release API。结果用定长 round-robin buffer 保存最近 64 个请求，超限返回 `SSR_NO_INFORMATION`——64 字节换掉所有生命期管理。(4) Implicit API——把"这是异步操作"从 API 语义里彻底抽掉。例子：`void set_score(int)` + `int acknowledged_score()`，用户只关心"设过的"和"服务器确认过的"；或极简的 `const char *fetch(const char *url)`，没拿到返回 NULL，拿到后下一次返回数据、再下一次自动 free。本文的立场和 [[polling-callbacks-events]] 一脉相承：**对象越少越好、状态越显式越好、时机越可控越好**。

## 关键要点

- Callback 的根本问题是"时机、上下文、可安全执行的操作"三不可控。
- Request 对象 / futures 是通过对象化本身把成本堆积给调用者。
- ID token + 定长 ring buffer：64 字节消除所有生命期管理，代价是有上限。
- Implicit API：把 async 当实现细节——用户只看"intent 和 acknowledged state"。
- fetch 例子极端到一个函数搞定：NULL → 请求发起中；非 NULL → 数据；下次调用自动释放。

## 链接到的概念

- [[async-api-id-tokens]]
- [[polling-callbacks-events]]
- [[id-based-lifetime-with-kill-flag]]

## 原文

- 链接：https://bitsquid.blogspot.com/2012/08/a-simpler-design-for-asynchronous-apis.html
- 本地：`raw/articles/bitsquid.blogspot.com/2012-08-04_a-simpler-design-for-asynchronous-apis.md`
