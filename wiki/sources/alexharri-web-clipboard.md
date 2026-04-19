---
tags: [source, web, clipboard, browser]
date: 2026-04-19
sources: 1
---

# The web's clipboard, and how it stores data of different types（Alex Harri / alexharri.com）

[[alex-harri-jonsson]] 于 2024 年 9 月的文章，解剖 Web 剪贴板两套 API 的历史分裂、数据类型限制与业界绕行方案。

## 摘要

Web 剪贴板并非单一系统：新异步 API（`navigator.clipboard.read/write`）限制数据类型仅 `text/plain`、`text/html`、`image/png`，以规避原生应用被恶意二进制利用；而老派 `ClipboardEvent.clipboardData.setData` 可写任意 MIME 类型，却只在用户触发（`isTrusted`）的 copy/paste 事件里生效。Google Docs 用 `document.execCommand("copy")` 来「伪造」trusted 事件写入自定义类型；Figma 反过来只写标准 `text/html`，把 base64 编码的 Kiwi 二进制 `.fig` 藏进空 span 的 `data-buffer` 属性，实现与原生 App 的双向互操作。Chromium 的 Web Custom Formats (Pickling) 提议让异步 API 支持 `"web application/json"` 前缀并写入标准化 `org.w3.web-custom-format.map`，但非目标里明确声明**不**追求与未更新的原生应用互操作。全文配 Pasteboard Viewer 截图展示各浏览器在 macOS 上写入的自定义格式名，以及 Safari 同源限制、`isTrusted` 行为、`unsanitized` 选项等细节。

## 关键要点

- 异步 API 严格类型白名单 vs Clipboard Events API 任意类型——两套 API 安全模型对称缺陷。
- `execCommand("copy")` 不是「deprecated 就不能用」，它是目前写入任意类型的合法通道；Google Docs 一直在用。
- Figma 的 HTML 偷渡是跨 Web ↔ 原生互拷的实用妥协。
- Web Custom Formats 用 `org.w3.web-custom-format.type-N` + map 表解决类型白名单问题，但仅 Chromium 支持。
- 各浏览器的系统剪贴板行为差异：Chrome 附带 source-url，Firefox 不存，Safari 同源限制。

## 链接到的概念

- [[web-clipboard-api]]
- [[alex-harri-jonsson]]

## 原文

- 链接：https://alexharri.com/blog/clipboard
- 本地：`raw/articles/alexharri.com/2024-09-01_the-webs-clipboard-and-how-it-stores-data-of-different-types.md`
