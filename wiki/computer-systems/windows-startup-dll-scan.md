---
tags: [Windows, 性能, DLL加载, 开发环境, 安全]
date: 2026-04-27
sources: 1
---

# Windows DLL 加载时的安全扫描延迟

Windows 的若干安全机制会在 DLL 加载时触发扫描或网络请求，在需要加载大量二进制的开发者工具链中可造成严重的启动延迟。

## Smart App Control

Windows 11 的 Smart App Control 是影响最显著的一项：它在系统全新安装时默认启用，对每个首次加载的 exe/dll 文件执行校验，可能将文件发送至 Microsoft 服务器核验。[[adam-sawicki]] 在运行 Unreal Engine 编辑器时遭遇了 5 分钟的首次启动延迟，根因正是此功能——UE5 编辑器需加载约 914 个独立的 exe/dll，网络延迟逐个累积。

**特性说明：**

- 仅在全新 Windows 安装上默认启用；系统升级路径通常不会开启
- 关闭后**不可再开启**（这是 Microsoft 的设计）
- 关闭路径：Windows 设置 → 隐私和安全 → Windows 安全中心 → 应用和浏览器控制 → 智能应用控制

## 调试方法

启动延迟问题通常难以直接定位，以下方法有助于缩小范围：

- **Visual Studio 输出面板**：观察"Loaded … .dll"消息的出现频率，判断是否每个 DLL 加载都在等待
- **Very Sleepy / Concurrency Visualizer**：分析进程调用栈，如果在用户态只看到 `LoadLibrary` 等系统调用而无业务代码，说明阻塞发生在内核态或另一进程
- **多进程并行加载测试**：若单进程内多线程 `LoadLibrary` 无法并行（内部 mutex），而多进程可以，则说明限流在进程级别，指向系统级扫描机制

## 与杀毒软件的区别

Windows Defender 的实时防护（排除目录设置）与 Smart App Control 是两套不同的机制。关闭实时防护或添加排除目录**不会**绕过 Smart App Control。两者需分别处理。

## 相关

- [[build-process-visualization]]
- [[compilation-pipeline]]

## Sources

- [[sources/asawicki-app-startup-5min-fix]]
