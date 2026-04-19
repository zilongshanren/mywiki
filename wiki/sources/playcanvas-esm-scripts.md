---
tags: [source, playcanvas, javascript, esm, 脚本系统]
date: 2026-04-19
sources: 1
---

# Introducing ESM Scripts in PlayCanvas（Lundin / PlayCanvas Blog）

[[mark-lundin|Mark Lundin]] 2025-06-10 发布于 blog.playcanvas.com 的公告：PlayCanvas 把 **ECMAScript Modules** 作为脚本系统的**官方推荐写法**，同时保持 Classic Scripts（2016 年版）的兼容，两种可以在同项目里混用。

## 摘要

PlayCanvas 的 Classic Scripts 时代留下几个结构问题：隐藏全局、script 加载顺序脆弱、跨项目复用只能复制粘贴、IDE 的 auto-complete 和类型推导几乎都失效。ESM Scripts 用标准 `import`/`export` + `.mjs` + class 继承 `Script` 解了这些问题：每个脚本是有作用域的 class，属性靠字段 + `@attribute` JSDoc 声明（替代 `attributes.add(...)` 的运行期软注册），`static scriptName` 把 class 绑到 Editor 的 script 组件。支持 **Import maps** 意味着可以用别名引入 CDN 上的第三方库，把 JS 生态主流的依赖管理带回了 Editor 项目。Editor 针对 ESM 做了更强的 auto-complete 和 inline docs。Classic `.js` 不会被移除，存量项目不强制迁移。

## 关键要点

- **兼容策略**：`.js` → Classic、`.mjs` → ESM，同项目可混用，不强制迁移。
- **最小样板**：`import { Script } from 'playcanvas'` + `export class ... extends Script` + `static scriptName = '...'` + 字段 + JSDoc `@attribute`。
- **Import maps**：别名与 CDN 拉库是 web-native 的依赖管理路径。
- **静态分析收益**：打包器能做 dead code elimination、未来支持 tree-shaking。
- **工具链联动**：Editor 和 VSCode 都能从 class 定义推导 auto-complete；后续的 VSCode Extension 直接吃 ESM 的类型信息。

## 链接到的概念

- [[playcanvas-esm-scripts]]
- [[playcanvas-react-declarative]]
- [[mark-lundin]]

## 原文

- 链接：<https://blog.playcanvas.com/introducing-esm-scripts-in-playcanvas>
- 本地：`raw/articles/blog.playcanvas.com/2025-06-10_introducing-esm-scripts-in-playcanvas-playcanvas-blog.md`
