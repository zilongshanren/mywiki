---
tags: [web, clipboard, browser-api, security]
date: 2026-04-19
sources: 1
---

# Web 剪贴板 API 的分裂与演进

Web 剪贴板长期是一块被历史糊成的胶合层，而不是一个整洁的 API。Alex Harri 的深挖文章把它拆成两条并行线：2017 年引入的异步 `navigator.clipboard` 与始于 Internet Explorer 4 时代（1997 年前后）的 `ClipboardEvent.clipboardData`。两者共存，能力和安全模型完全不同。

## 两套 API 的对称缺陷

异步 Clipboard API（`read` / `write`）随时可用，但**数据类型被严格限制**在 `text/plain`、`text/html`、`image/png` 三种必选 MIME 类型内。尝试写 `application/json` 会直接抛 `Type application/json not supported on write`。规范在 2012–2021 年间曾有 8 项强制写类型、16 项强制读类型，但在 [w3c/clipboard-apis#155](https://github.com/w3c/clipboard-apis/pull/155) 之后被砍到三种——浏览器担心未沾染的二进制数据被写进系统剪贴板后被原生应用的漏洞利用。

老的 `clipboardData.setData(type, value)` 恰好相反：**数据类型可以任意字符串**（这一自由度是从 IE 时代延续下来的「don't break the web」），但只在用户真实触发的复制/粘贴事件里生效——合成事件的 `isTrusted` 为 false，写了也不会落到系统剪贴板。

## 绕过限制的业界方案

- **Google Docs 的 Copy 按钮**：点击时调用 `document.execCommand("copy")`，而不是异步 API。`execCommand("copy")` 会派发 `isTrusted === true` 的 copy 事件，使 handler 中的 `clipboardData.setData` 得以写入任意类型，这就是 Docs 能写 `application/x-vnd.google-docs-document-slice-clip+wrapped` 的奥秘。
- **Figma 的 HTML 偷渡**：只写 `text/plain` 与 `text/html`，在 HTML 里塞两个空 `<span>`，`data-metadata` 存 base64 JSON（fileKey、pasteID），`data-buffer` 存 base64 编码的 [Kiwi 二进制格式](https://github.com/evanw/kiwi) `.fig` 文件。结果是浏览器与原生 Figma App 互拷一个能共用的「HTML 包裹的二进制」。
- **Web Custom Formats (Pickling)**：Chromium 2022 起支持的新方向，在异步 API 中用 `"web application/json"` 前缀表示自定义类型，系统剪贴板上写一个 `org.w3.web-custom-format.map` 映射表 + 若干 `type-0/type-1` 条目，原生 App 需要更新以读取。非目标明确列出「与未更新的原生应用互操作」——这是先前 Raw Clipboard Access 提案被否后的安全折衷。

## 系统剪贴板层的现实

浏览器将自定义数据塞进各自的保留格式：Chrome 写 `org.chromium.web-custom-data` 并附带 `org.chromium.source-url`；Firefox 写 `org.mozilla.custom-clipdata`；Safari 写 `com.apple.WebKit.custom-pasteboard-data` 并额外保存一份完整表示清单，且**只允许同源 tab 互拷**自定义类型。使用 `text/html` 成为跨应用兼容的最大公约数——这是 Figma 方案实用性的底层逻辑。

## 相关

- [[parse-dont-validate]] 的数据结构思想：`ClipboardItem` 接受 key-value map 让非法状态无法表示（Alex 引用 Alexis King）。
- [[sources/alexharri-web-clipboard]]

## Sources

- [[sources/alexharri-web-clipboard]]
