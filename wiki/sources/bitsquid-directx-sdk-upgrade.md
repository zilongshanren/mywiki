---
tags: [source, 渲染, DirectX, Windows-SDK, bitsquid, 工程踩坑]
date: 2026-04-19
sources: 1
---

# Upgrading the DirectX SDK（Amandine Coget / Bitsquid）

[[amandine-coget|Amandine Coget]] 2015 年 6 月 11 日的入职一个月记——把 Bitsquid 从已被废弃的 *June 2010 DirectX SDK* 切到 Windows 8.x SDK 的全过程。六步流水账属于典型的"旧 SDK 退役、新 SDK 未完全等价"期过渡工程。

## 摘要

Step 1 侦察：MSDN 明确说 DirectX SDK 已并进 Windows SDK，真正剩下 gap 的只有 **XInput、XAudio2、D3DX9Mesh** 三块——codebase 早已几乎脱离 D3DX。minspec 还得留在 Windows 7，[MSDN 专文](http://blogs.msdn.com/b/chuckw/archive/2012/11/14/directx-11-1-and-windows-7.aspx)给出 Windows 8.x SDK 在 Win7 上可用的限制细节。

Step 2 切路径、同时把 June 2010 SDK 留作 XAudio2 / D3DX9Mesh 的 fallback——看似只剩几个编译错，直到运行时 crash 在 `ID3D11ShaderReflection` 上。

Step 3 GUID 惊魂：DirectX 大量依赖硬编码 GUID，**默认 GUID 是 `extern` 变量、值由 lib 提供**。之前没拆掉的 `dxguid.lib` 是老版本，链接后 `IID_ID3D11ShaderReflection` 拿到了错的值——引用了一天误以为是错误 include。正确做法是 **移除 `dxguid.lib` + `#define INITGUID` 再包含 `windows.h`**，让 GUID 以 inline 常量形式参与编译。

Step 4 `d3dcompiler`：之前一直默默依赖 `System32` 里的这个 DLL——SDK 装了它自然在——现在新版不保证，project 里得显式 `copy` 一份作为 install step。

Step 5 XInput：SDK 里 XInput 1.4 是 Windows 8 only。要在 Win7 上跑必须显式链 `XInput9_1_0.lib` 并把 `_WIN32_WINNT` 设到对应值——否则 Win7 上 runtime crash 去找不存在的 `XInput1_4.dll`。作者的 Windows 8 workstation 感觉不到，只有 Win7 自动化测试机会挂。

Step 6 Profit——渲染组还要真正压测。

这类笔记的价值不在具体 bug，而在**把"一个平台 SDK 被折腾掉一代"时 C/C++ 项目要对付的几种隐藏依赖**整理成一条可对照的清单：依赖 `System32` 预置 DLL、依赖旧 lib 的 GUID 定义、依赖 `_WIN32_WINNT` 隐式 API 选择。

## 关键要点

- June 2010 DirectX SDK → Windows 8.x SDK 迁移：只剩 XInput / XAudio2 / D3DX9Mesh 三块 gap
- Windows 8.x SDK 在 Windows 7 上可用（参见 MSDN chuckw 专文）
- **GUID 默认是 `extern` 变量**，值由 lib 提供——链旧 `dxguid.lib` → `IID_*` 错值 crash
- 解：移除 `dxguid.lib` + `#define INITGUID` 再 `#include <windows.h>`（内联定义 GUID）
- `d3dcompiler.dll` 过去靠 `System32` 搭便车——新版要 project 显式 copy install step
- XInput 1.4 是 Windows 8 only；Win7 必须链 `XInput9_1_0.lib` 且设 `_WIN32_WINNT`
- 开发机是 Win8、CI 是 Win7——"在我机器上能跑"的典型样本
- 类型：[[directx11-early-pitfalls|DX 早期踩坑]]之外另一种"SDK 换代"层面的隐形依赖

## 链接到的概念

- [[directx-sdk-to-windows-sdk-migration]]
- [[directx11-early-pitfalls]]

## 原文

- 链接：https://bitsquid.blogspot.com/2015/06/when-i-joined-bitsquid-month-ago.html
- 本地：`raw/articles/bitsquid.blogspot.com/2015-06-11_upgrading-the-directx-sdk.md`
