---
tags: [source, 工具链, msbuild, gkengine]
date: 2026-04-14
sources: 1
---

# 制作自定义 vc100 工具链（gameknife, 2015-03）

[[people/gameknife|gameknife]] 发表于 2015 年 3 月的一篇工程小记。[[gkengine|gkEngine]] 依赖 Havok / ToolkitPro 等第三方库锁死在 VS2010（vc100 工具链），但用户多半用 VS2013+。作者用一台纯净 Win7 + 仅装 VS2013 的虚拟机做试验，把 vc100 的 msbuild 与依赖剥离成一个约 50 MB 的独立安装包，让下载 gkEngine 的朋友不必再装一次完整 VS2010。

## 摘要

文章是作者自己解开"为什么别人编不过 gkEngine"这件事的一篇随笔。Visual Studio 的 C++ 编译由 msbuild 驱动，理论上只要把 vc100 需要的 msbuild task、VC/CRT/ATLMFC、Windows SDK v7.0A 等拷贝到正确路径并补全对应注册表项，就能在只装了 VS2013 的机器上通过 "do not upgrade" + "vc100 工具链" 选项走完整编译流程。作者列出了最终需要部署的七条关键路径，包括 `Microsoft.NET/assembly/Microsoft.Build.CppTask.{common,win32,x64}`、`Microsoft Visual Studio 10.0/VC`、`MSBuild/Microsoft.Cpp/v4.0` 工具链、`Microsoft SDKs/Windows/v7.0A` 等；并在 `HKLM\SOFTWARE\Wow6432Node\Microsoft\{MSBuild,VisualStudio,Microsoft SDKs}` 下补注册表项。最终精简到约 50 MB，作者写了 bat 安装脚本打包发布。文末留了个坑：作者只在 Win7 x64 上测过，XP 与 Win7 x86 需要的路径与注册表微调留给愿意试的读者补 wiki。

## 关键要点

- **msbuild 是 VS C++ 构建的真正核心**——一旦把 msbuild task、VC 工具、CRT/ATLMFC、Windows SDK v7.0A 与注册表项凑齐，vc100 就能在没装 VS2010 的机器上独立存在。
- **最小部署清单（7 条）**：
  - `Windows/Microsoft.NET/assembly/Microsoft.Build.CppTask.Common`
  - `Windows/Microsoft.NET/assembly/Microsoft.Build.CppTask.Win32`
  - `Windows/Microsoft.NET/assembly/Microsoft.Build.CppTask.x64`
  - `Program Files (x86)/Microsoft Visual Studio 10.0/VC`
  - `Program Files (x86)/Microsoft Visual Studio 10.0/IDE` 下的若干工具
  - `Program Files (x86)/MSBuild/Microsoft.Cpp/v4.0` 工具链
  - `Program Files (x86)/Microsoft SDKs/Windows/v7.0A`
- **注册表键**：`HKLM\SOFTWARE\Wow6432Node\Microsoft\{MSBuild, VisualStudio, Microsoft SDKs}` 若干项，让 VS2013 的 project upgrade 向导能识别到 vc100 平台工具集。
- **虚拟机快照**驱动整套试验——作者特别夸了一句"有了快照做系统级文件操作就和玩游戏一样"。
- **工程背景**：gkEngine 依赖的 [[gkengine|Havok / ToolkitPro 界面库]]等锁死在 VS2010，导致 `gkHavok / gkHavokAnimation / gkStudio` 无法在高版本 VS 上编译；作者想把这件事一次性解决掉让社区朋友能跑起来。
- **留作开放问题**：XP / Win7 x86 未测；32 位系统可能需要不同的注册表与路径；作者邀请读者补 wiki。

## 链接到的概念

- [[gkengine]]
- [[people/gameknife]]

## 原文

- 链接：<http://gameknife.github.io/tech/2015/03/21/make-custom-vc100-toolchain/>
- 本地：`raw/articles/gameknife.github.io/2015-03-21_zhi-zuo-zi-ding-yi-vc100gong-ju-lian.md`
