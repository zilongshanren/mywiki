---
tags: [source, unreal-engine, cpp, toolchain, rider]
date: 2026-04-19
sources: 1
---

# Setting up Rider for C++ and Unreal Engine（Tom Looman）

[[tom-looman]] 2026 年 2 月的文章，讲如何在 Windows 下用 JetBrains Rider 作为 Unreal Engine 5 的 C++ IDE，包括必装的 Visual Studio Build Tools 组件版本。

## 摘要

用 Rider 搭 UE5 开发环境最大的坑在于 Rider 本身不自带 C++ 工具链，仍然要装 Visual Studio Build Tools，并且组件版本必须对齐 UE 当前版本的要求。文章针对 UE 5.6 给出一份可复制清单：Windows 11 SDK 10.0.26100.3916+、.NET Framework 4.8.1 SDK+、MSVC v143 v14.38-17.8。配套说明了常见的三条编译错误（"No valid Visual C++ toolchain"、"No available Windows SDKs found"、".NET Framework SDK 4.6+"）和对应修复步骤。然后介绍 Rider 侧配置：直接打开 `.uproject`、在 Unreal Editor 里把 Source Code Editor 设为 "Rider uproject"、安装 RiderLink 到引擎、打开 Windows Defender 排除项。想调试引擎源码要在 Epic Launcher 给引擎勾选 "Editor Symbols for debugging"。最后列了作者的 Rider 偏好设定：开启 Plugins 索引、降低参数弹窗延迟、关 Reader Mode、关 `#include` 折叠、关 Full Line 补全。

## 关键要点

- UE5 C++ 编译依赖很挑版本，Epic 定期拉高最低 SDK/MSVC 版本，装错直接编不过
- UE 5.6 需要 Win 11 SDK 10.0.26100.3916+、.NET 4.8.1 SDK+、MSVC v143 v14.38-17.8
- Rider 用 `.uproject` 打开而不是 `.sln`，让 Rider 自动维护工程结构
- RiderLink 插件装到引擎一端，能让 Rider 看到 Blueprint 对 C++ 变量/函数的覆写
- 调试引擎源码需要额外下载 Editor Symbols（数十 GB）

## 链接到的概念

- [[rider-ue5-setup]]
- [[tom-looman]]

## 原文

- 链接：<https://tomlooman.com/setup-unreal-engine-cpp-rider/>
- 本地：`raw/articles/tomlooman.com/2026-02-13_setting-up-rider-for-c-and-unreal-engine.md`
