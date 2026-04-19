---
tags: [source, 认证, 安全, webauthn, passkeys]
date: 2026-04-19
sources: 1
---

# Passkeys Are Too Hard（Evan Todd / etodd.io）

[[evan-todd]] 2026 年 4 月的博客，记录实现 WebAuthn / passkeys 时遇到的复杂度——并提出一个"grug-brained"的简化 API 提案。

## 摘要

作者的 TL;DR："WebAuthn 被工程化得太偏执，企业级用例没问题，但要让一般开发者接得起需要一个简化版。"他把痛点集中在**conditional UI** 这个相对较新的特性。

原版 WebAuthn 流：用户点"用 passkey 登录"按钮 → server 生成随机 challenge → 浏览器调 `navigator.credentials.get(challenge)` 签名 → 发给 server 验签。问题是按钮 UX 失败——用户记不住自己在哪里建过 passkey。

Conditional UI 改成 `<input autocomplete="username webauthn">`——聚焦输入框时，浏览器下拉显示可用 passkey。从用户视角是"理应如此"。

**复杂度来自隐私需求**：WebAuthn 威胁模型里网页本身是敌对的，浏览器绝不能让网站知道"这用户是否有 passkey"（否则可跨会话指纹）。所以 conditional UI 下步骤 1-2（server 生成 + 浏览器 await）在页面 load 时就触发——没 passkey 时 await 无限阻塞。叠加 challenge 必须随机生成、不可复用、持久化（防 pre-play / replay），结果是**每个未登录用户访问 login 页都要 server 写一条 challenge 记录到 DB**。一堆衍生问题：过期怎么办？用 `AbortController` 加超时 + while-loop；每次页面加载都往 DB 写？扩缩时顶不住；改成 `localStorage` 缓存只在过期时重发？复杂度继续堆。

作者提出 grug-brained API 提案：registration 返回 JWKS（只含公钥），login 用 `<input>` 的 `change` 事件，`event.token` 是个 JWT——短过期、`iss` = 页面 origin、signed by 选中的 passkey，`fetch` 到 server 验签即登录。不完美但可懂可审计。"miles ahead of passwords，不用苛求 lightyears ahead。"

## 关键要点

- Conditional UI 解决了按钮 UX 但把复杂度转到 server side——challenge 必须为每个访客持久化。
- WebAuthn 的隐私设计（不暴露 passkey 存在）是合理的，但副作用是 async flow 必须绕。
- 过期处理需要 `AbortController` + while-loop；规模时 DB 写路径难以接受。
- 作者提议的 JWT-签名 + origin-bound 方案不满足企业级审计，但足够替代密码。
- 结论是 "passkey 完全取代密码"还需要更简化的 API 层。

## 链接到的概念

- [[passkeys-webauthn]]
- [[magic-link-auth]]

## 原文

- 链接：https://etodd.io/2026/04/06/passkeys-are-too-hard/
- 本地：`raw/articles/etodd.io/2026-04-06_passkeys-are-too-hard.md`
