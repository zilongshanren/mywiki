---
tags: [认证, 安全, web, passkeys, webauthn]
date: 2026-04-19
sources: 1
---

# Passkeys / WebAuthn：为什么"取代密码"还差一段路

Passkeys 是基于 **WebAuthn** 的无密码登录标准——用户端生成一对密钥，私钥存在设备/密码管理器里，公钥发给服务器；登录时服务器发一个随机 challenge，客户端用私钥签名，服务器验签后登录。核心特性是**与 origin 绑定**——钓鱼站拿到 challenge 签出来的东西对真站没用，[[magic-link-auth|magic link]] 的钓鱼攻击面在这里消失。

理论上极好。实际用起来，[[evan-todd]] 的结论是："WebAuthn 是为企业级偏执场景设计的，还没到我这种 **grug-brained** 开发者能随手接入的地步。"

## Conditional UI：更好的默认 UX

原版 WebAuthn 要求用户点一个 "Sign in with passkey" 按钮触发登录。问题是大多数用户早忘了自己在哪个站建过 passkey，按钮 UX 失败了。

**Conditional UI** 改成在 `<input>` 上加一个属性：

```html
<input type="text" autocomplete="username webauthn" />
```

聚焦输入框时浏览器的自动填充下拉里直接列出该站可用 passkey，选一个就登录。对用户来说是无感的——"本来就该这样"。

## 为什么 conditional UI 让服务端变复杂

WebAuthn 的**威胁模型假设网页本身是敌对的**——浏览器绝不能让 `example.com` 在用户主动选 passkey 之前知道"这个浏览器是否为我存过 passkey"。否则网站可以用"是否有 passkey"做跨会话指纹、关联临时账号。这是合理的隐私考虑。

代价是：conditional UI 下步骤 1-2（**server 生成 challenge** + **浏览器 await `navigator.credentials.get()`**）在页面加载时就触发，即使用户根本没 passkey。如果没有，await 就无限阻塞。再加 WebAuthn 的两条额外要求：

- **challenge 必须是服务端随机生成**（防 pre-play 攻击）
- **challenge 不可复用**（防 replay），必须持久化

合起来就是：**服务器必须给每一个未登录用户（哪怕他根本没 passkey）生成并持久化一个随机 challenge**。这立即引出一连串问题：

- challenge 多久过期？过期了 login 页是不是要刷新？→ 需要 `AbortController` + while-loop 在用户选 passkey 时别 timeout。
- 每次页面加载都写一条数据库？→ 缩放陷阱，每个登录表单都往 hot path 上糊了一次写。
- 考虑缓存到 `localStorage` 只有过期才重发？→ 开始绕复杂度越来越高的路。

作者的评价："这是一堆本该简单可审计的东西却被绕成迷宫。"

## 作者希望的 grug-brained API

创建 passkey：

```js
const cred = await navigator.credentials.create({...options})
// 应当直接返回一个 JWKS 文档（只含公钥）
```

登录：

```html
<input type="text" autocomplete="username webauthn" />
```

选中 passkey 时 `<input>` 触发 `change` 事件，`event.token` 是个 **JWT**：短过期、`iss` 是页面 origin、签名来自选中的 passkey。`fetch` 给服务端，验签即登录。**challenge 和会话存储都不需要**——浏览器内部处理完。

这不是完美方案，但"不完美但没人用不起"远胜"完美但门槛劝退"。如果企业真的需要 WebAuthn 原版那套 challenge/reply 可审计性，让他们继续用——大部分人只要一个比密码好得多的东西。

## 和 magic link 的互补

Passkey 不能完全替代 magic link——大多数普通用户不理解"passkey 存哪、怎么带到别的设备/跨品牌浏览器"。作者的现实方案：**magic link + passkey 并存**，passkey 作为钓鱼免疫的主路径、magic link 作为兜底（再配合邮件里的 IP/UA 展示减缓钓鱼）。

## 相关

- [[magic-link-auth]]
- [[evan-todd]]

## Sources

- [[sources/etodd-passkeys-are-too-hard]]
