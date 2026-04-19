---
tags: [unreal-engine, cpp, toolchain, rider]
date: 2026-04-19
sources: 1
---

# 用 Rider 搭建 Unreal Engine 5 C++ 开发环境

用 JetBrains Rider 替代 Visual Studio 来写 Unreal Engine C++ 是常见选择，但是 Rider 本身并不自带 C++ 编译工具链，**仍然需要装一套 Visual Studio 的 Build Tools**，而且必须装对版本——Epic 每隔几个版本就会把 MSVC、Windows SDK、.NET Framework SDK 的最低版本往上顶。[[tom-looman]] 针对 UE 5.6 给出的一份可复制清单是：Windows 11 SDK 10.0.26100.3916+、.NET Framework 4.8.1 SDK+、MSVC v143（v14.38-17.8）。装错版本会直接以编译期错误的形式报出来，典型三条错误信息分别指向这三个组件——文章把每条错误对应的修复步骤都写出来了，可以作为排查表用。

Rider 本身的关键配置有：直接用 `.uproject` 而不是 `.sln` 打开项目（Rider 自动同步工程结构）、在 Unreal Editor 的 Source Code Editor 里把编辑器设为 "Rider uproject"、安装 RiderLink 插件到引擎（查 Blueprint 对 C++ 变量/函数的覆写信息很有用）、把 Windows Defender 排除项打开避免扫描构建输出。

若想调试引擎源码，需要去 Epic Launcher 给对应引擎版本勾选 "Editor Symbols for debugging"，代价是几十 GB 磁盘占用。

作者还给出一些个人偏好设定：开启 Plugins 索引（否则 Enhanced Input、Niagara 等不进 autocomplete）、调低参数弹窗延迟、关闭 Reader Mode（rendered comments）、关闭 `#include` 折叠、关闭 Full Line 补全。

## Sources

- [[sources/tomlooman-rider-ue5-setup]]
