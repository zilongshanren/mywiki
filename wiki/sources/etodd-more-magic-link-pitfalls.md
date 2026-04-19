---
tags: [source, 认证, 安全, web, phishing]
date: 2026-04-19
sources: 1
---

# More Magic Link Pitfalls（Evan Todd / etodd.io）

[[evan-todd]] 2026 年 3 月末的续篇，回应读者在 Lobsters 上对上一篇的批评，把 magic link 的陷阱扩到了更难的层面：phishing、flaky email、rate limit。

## 摘要

四条补充：

1. **Magic link 烦**——这是最多读者的吐槽，翻译过来是"想用密码管理器"。作者承认合理，并决定同时实现 [[passkeys-webauthn|passkeys]]——比密码好、对 phishing 免疫；但不能完全替代 magic link，因为普通用户搞不清 passkey 怎么跨设备跨浏览器同步。
2. **Phishing**——"登录原 tab"模式有个攻击面：钓鱼 server 拿用户输入的邮箱向真 server 发起登录、同时轮询真 server 等"verified"；用户收到真邮件、点击链接、钓鱼 server 的 session 被 verified → 拿到真 auth cookie。切成 6 位码也救不了（用户会回去钓鱼站把码贴进去）。和 password phishing 同等严重。作者的缓解：邮件里展示 **IP + 地理位置 + UA**（"有人在 Smalltown KS 从 Chrome on macOS 登录"），让用户肉眼核对；配合 passkey（对 phishing 天生免疫）作为主方案。
3. **Email flaky + hash 的冲突**——"只存 hash"意味着重发需要重新生成 code，但如果第一封邮件最终到了、第二封没到，用户点第一封进不来（因为业务流程已经废了第一码）。作者修正：**改成加密存而不是 hash**，加"重发"按钮，重发的是同一个 code。承认之前的 hash 要求有 cargo-cult 成分——"no plaintext credentials" 作为简单规则好，但 magic link code 的威胁模型和长期密码不一样。
4. **Rate limit**——按 IP + 按账号各限 5 个 pending auth。IP 限制在 NAT/大出口 IP 场景会误伤（卡塔尔那种全国一个出口 IP 的极端例外），但大多数情况下工作；账号限制可能被恶意者用来 DoS，作者没见过实例，欢迎读者补充经验。

## 关键要点

- 想要密码管理器用户体验 → 上 passkeys（对 phishing 免疫），但仍保留 magic link 做兜底。
- Magic link 的 phishing 易感性和 password 同等——6 位码无法改善。
- 邮件里展示登录请求的 IP / 地理 / UA 是可接受的缓解，最终靠 passkeys 闭环。
- Hash 要求是过度 cargo-cult：magic link code 短期存活、不是长期凭证，加密 + 支持重发更实用。
- Rate limit 双维度（IP + 账号），账号维度会被恶意者利用但实际很少。

## 链接到的概念

- [[magic-link-auth]]
- [[passkeys-webauthn]]

## 原文

- 链接：https://etodd.io/2026/03/31/more-magic-link-pitfalls/
- 本地：`raw/articles/etodd.io/2026-03-31_more-magic-link-pitfalls.md`
