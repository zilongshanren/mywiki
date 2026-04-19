---
tags: [source, playcanvas, vscode, 工具链, ai-agent, typescript]
date: 2026-04-19
sources: 1
---

# New PlayCanvas Visual Studio Extension（Bamrah / PlayCanvas Blog）

Kris Bamrah 2025-11-25 发布于 blog.playcanvas.com 的工具公告：新一代 **PlayCanvas VSCode Extension**（GitHub 上 `playcanvas/vscode-extension`），针对从 PlayCanvas Editor 里编辑文本类资产的场景做了大改。

## 摘要

旧版 VSCode 插件更像一个"上传器"——本地写完要手工推到 Editor。新版是一个**实时 sync + 本地镜像**的系统：文本资产在 VSCode 和 PlayCanvas Editor 之间**即时同步**，不需手工 push / refresh；**live collaborators** 显示当前谁也在同一文件里、避免并行冲突；**完整 TypeScript 类型检查 + auto-complete** 覆盖所有 script 类型（这一步得益于 [[playcanvas-esm-scripts|ESM Scripts]] 让 script 变成可静态分析的 class）；最关键的一条——**Disk-mapped file system**：Editor 项目结构被**直接映射到本地磁盘**。这一步解锁了之前插件做不到的场景：**AI 代码 agent 和 assistant 能在本地文件系统上操作 PlayCanvas 项目**。支持 VSCode 和 Cursor。开发体验侧加了代码组织清理、TS 类型强化、调试流程简化、测试套件。

## 关键要点

- **实时同步**：删除了手动 push 步骤，编辑即保存到 Editor。
- **协作可见**：知道谁在同一文件，减少冲突。
- **完整 TS 支持**：基于 ESM Scripts 的 class 结构做静态分析。
- **Disk-mapped FS 是核心解锁点**：AI agent（Cursor / Copilot / Claude Code 等）可以用它作为载体读写 PlayCanvas 项目——把 PlayCanvas 从"Web-only 编辑器"变成"可以被任意本地工具链管控的项目"。
- **支持 Cursor**：明确把 AI 代码编辑器作为一等公民。
- **和 ESM Scripts / Editor frontend 开源的配合**：这三步（ESM 规范化 + Editor 开源 + Disk-mapped VSCode）共同构成"把 PlayCanvas 项目打开给现代 dev 工具链"的完整改造。

## 链接到的概念

- [[playcanvas-esm-scripts]]
- [[playcanvas-webgpu-editor]]

## 原文

- 链接：<https://blog.playcanvas.com/new-playcanvas-visual-studio-code-extension>
- 本地：`raw/articles/blog.playcanvas.com/2025-11-25_new-playcanvas-visual-studio-extension-playcanvas-blog.md`
