---
tags: [source, 认证, 安全, web]
date: 2026-04-19
sources: 1
---

# Magic Link Pitfalls（Evan Todd / etodd.io）

[[evan-todd]] 2026 年 3 月的博客，列了实现 magic link 登录时容易漏掉的两个非显然陷阱。

## 摘要

作者是做 security 的，接 magic link 时已经知道几条基础：短过期、一次性、64-bit 熵、数据库只存 hash。做到一半才发现两个更具体的坑：

1. **不能让 GET 直接消费 code**——一些邮件客户端会为渲染 link preview 主动发 GET，浏览器对悬停的链接也会 prefetch。结果 code 在用户真正点击前就被"消费"掉。正解：GET 返回一个带"登录"按钮的中间页，用户点按钮才 POST 消费。
2. **登录原 tab 而不是 magic link tab**——手机上点邮件里的链接，默认在邮件 app 内嵌浏览器里打开，登录的是那个临时 webview，用户日用的浏览器没变化。正解：链接只 "mark code as verified"、显示"请回到原来的 tab"；原 tab 每几秒轮询一次 server，verified 就完成登录。这同时支持"用另一台设备（无邮箱）登录"的场景。

作者提了 6-digit 码作为替代，但 20 bit 熵只够低风险场景，不如短随机链接。末尾开放邀请读者补充更多 pitfall——这引出了续篇 [[sources/etodd-more-magic-link-pitfalls]]。

## 关键要点

- 邮件预览 / 浏览器 prefetch 会提前消费 GET——别把登录动作绑 GET。
- 邮件 app 内嵌浏览器和用户日用浏览器是两个 session——别登错 tab。
- 原 tab 轮询模式天然支持跨设备登录（A 设备输邮箱、B 设备收邮件点链接）。
- 6-digit code 是低熵替代，适合"电视登录 / 二因子"而不是主登录。

## 链接到的概念

- [[magic-link-auth]]

## 原文

- 链接：https://etodd.io/2026/03/22/magic-link-pitfalls/
- 本地：`raw/articles/etodd.io/2026-03-22_magic-link-pitfalls.md`
