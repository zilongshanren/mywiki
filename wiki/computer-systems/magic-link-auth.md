---
tags: [认证, 安全, web, 密码学]
date: 2026-04-19
sources: 2
---

# Magic Link 认证：陷阱清单

"Magic link" 指用户填邮箱、收到含一次性链接的邮件、点击即登录的无密码认证方式。看起来简单，但有一堆易错点。[[evan-todd]] 在两篇博客里整理了自己踩过和读者补充的 pitfalls。

## 基础安全线

业内共识的四条：

- **短有效期**（通常 5-15 分钟）。
- **一次性使用**：消费后立即作废。
- **足够熵的秘密码**：至少 64 bit 随机。
- **不要存明文 code**：数据库只存 hash（后来作者部分收回，见下）。

## 陷阱 1：GET 请求会被自动触发

早期实现是"点链接即登录"——即链接的 GET handler 直接消费 code。问题是：邮件客户端为渲染 link preview 会主动发 GET、浏览器对鼠标悬停的链接也会 prefetch。结果 code 在用户真正点击前就被消费掉了。

**正解**：GET handler 返回一个带"登录"按钮的中间页，用户点按钮才真正消费 code（发 POST）。

## 陷阱 2：错 tab 登录

手机上点邮件里的链接，默认在 **邮件 app 的内嵌浏览器** 里打开——被登录的是那个临时 webview，不是用户真正日用的浏览器。

**正解**：链接只 "mark code as verified"，显示"请返回原来的 tab"；原 tab 每几秒轮询一次 server 检查 code 是否已 verify，verified 就完成登录。这同时支持了"在另一台设备上点链接"的场景。

另一个等价方案是发 6-digit 数字码让用户复制粘贴回原 tab——但 6 位熵较低（~20 bit），只适合低风险场景（电视登录、二因子补充）。

## 陷阱 3：Flaky 邮件 + hash 的冲突

"只存 hash" 的副作用：如果第一封邮件没到、第二封到了，第二封的 code 已经废了（因为用户在点第一封前就被业务流程"开始新登录"重新生成了），导致用户怎么都进不来。

作者的修正：**改成加密存储而不是 hash**，加一个"重发邮件"按钮——可以重发同一个 code。是"严格密码学最佳实践"和"实际可用性"之间的权衡。作者坦承早期的 hash 要求有点 cargo-cult——"no plaintext credentials" 作为一条简单规则很好，但 magic-link code 的威胁模型和长期密码不一样。

## 陷阱 4：Phishing 易感性

"登录原 tab"的异步轮询设计有个攻击面：攻击者搭一个伪装域名的钓鱼 server，用户在钓鱼站输入邮箱 → 钓鱼站**拿用户邮箱向真 server 发起登录** + 同时轮询真 server → 用户收到真邮件 → 点击 → 钓鱼 server 的 session 被 verified → 拿到真 cookie。用户看不出异常。

这和 password-login 的 phishing 易感性**一样**（切成 6 位码也不能改善——用户还是会把码交回钓鱼站）。[[passkeys-webauthn|Passkeys]] 是对 phishing 不敏感的方案（challenge 绑 origin）。

**缓解**：邮件里展示登录请求的 **IP + 地理位置 + UA**（"有人在 Smalltown KS 用 Chrome on macOS 登录你账号"），让用户肉眼核对。配合 passkeys 才是防线。

## 陷阱 5：Rate Limiting

不是 magic-link 特有，但常被漏：按 IP 和按账号分别限制 pending auth 数量（比如各 5 个）。

- IP 限制在 NAT 后一堆用户的场景可能误伤，但极少数（卡塔尔那种整国一个出口 IP）之外可接受。
- 账号限制能锁住试图刷码的攻击者，副作用是可能被恶意者用来 DoS 别人的账号——作者没见过实际发生，读者里有没有经验分享欢迎补充。

## 相关

- [[passkeys-webauthn]]
- [[evan-todd]]

## Sources

- [[sources/etodd-magic-link-pitfalls]]
- [[sources/etodd-more-magic-link-pitfalls]]
