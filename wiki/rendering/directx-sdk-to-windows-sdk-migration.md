---
tags: [渲染, DirectX, Windows-SDK, 工程踩坑, 历史, bitsquid]
date: 2026-04-19
sources: 1
---

# June 2010 DirectX SDK 迁到 Windows 8.x SDK

2012 年后 DirectX SDK 被并进 Windows SDK——Microsoft 官宣 *"DirectX SDK 已经是历史"*。但一大批 codebase 仍链着 **June 2010 DirectX SDK**，这层"历史依赖"在升级到 Windows 8.x SDK 时会把几种**隐形依赖**顶出来。[[amandine-coget|Amandine Coget]] 2015 年在 Bitsquid 的迁移记是这类工程的典型账本。

## Gap 清单：三块没被并进去

实际上只有三块组件在 Windows SDK 里缺位：

- **XInput**：手柄输入；
- **XAudio2**：音频；
- **D3DX9Mesh**（及更广的 D3DX 族）：被 DirectX SDK 原生支持的一堆 helper math / mesh / texture utility，新 SDK 里官方宣告退役。

Bitsquid 早已几乎脱离 D3DX，因此 codebase 核心迁移压力不在这里——更隐蔽的坑在"Windows SDK 的设计假设 vs. 老 SDK 时代的默认行为"之间。

## 坑 1：GUID 默认是 `extern`，lib 决定值

DirectX 大量依赖硬编码 GUID（`IID_ID3D11ShaderReflection` 等）。**头文件里默认声明 `extern`**，值从链进来的 lib 取。在项目里留着老 `dxguid.lib` 会让 runtime 拿到和新 SDK 头文件不匹配的 GUID——走到 `QueryInterface` 就 crash。

正确做法：

- **移除 `dxguid.lib`**；
- 在包含 `windows.h` **之前** `#define INITGUID`，让 GUID 以内联常量形式在当前翻译单元里定义。

等价于把"GUID 值由哪份 lib 提供"的隐式依赖改成"由当前头文件本地定义"的显式控制——是迁移期最容易忽略、也最容易一天内白烧的那种 bug。

## 坑 2：`d3dcompiler.dll` 不再免费搭 `System32` 的车

以前装 DirectX SDK runtime 会把 `d3dcompiler_XX.dll` 预置到 `System32`——`LoadLibrary` 走默认搜索路径就能找到。Windows 8.x SDK 不再保证这点；**旧 project 要显式 copy 一份到可执行目录** 作为 install step。这个依赖在开发机上"正好还有旧版 runtime"时毫无症状，只有干净机器或 CI 上才暴露。

## 坑 3：XInput 1.4 是 Windows 8-only

XInput 在 Windows SDK 里有多个版本。**1.4 仅 Windows 8+**；要支持 Win7 minspec：

- 显式链 `XInput9_1_0.lib`（不是 `XInput.lib`）；
- 设置 `_WIN32_WINNT` 到合适的宏值（见 MSDN `sdkddkver.h` 文档）；
- 否则 Win7 runtime 会去 load 不存在的 `XInput1_4.dll`，crash。

Win8 开发工作站完全感觉不到这个 bug，只有 Win7 自动化测试机会挂——"works on my machine"的经典剧本。

## 为什么这份清单值得收藏

这三条坑每一条都对应 C/C++ 项目的一类**隐形依赖**：

1. **`extern` + lib 提供的全局常量**——GUID 的跨版本漂移；
2. **预置 runtime DLL 与搜索路径**——隐式 `System32` 依赖；
3. **`_WIN32_WINNT` 等 SDK 宏对 API 选择的影响**——`#define` 没设对 SDK 会挑错版本的符号。

任何"SDK 换代"类迁移都可以照这三类排雷：**有无 extern 全局常量被多份 lib 提供？有无依赖预置 DLL？是否依赖 `_WIN32_WINNT` 等 feature 宏切换 API 版本？**

## 相关

- [[directx11-early-pitfalls]] — DX11 刚推出时的 API / 驱动 / 文档坑
- [[amandine-coget]]
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-directx-sdk-upgrade]]
