---
tags: [source, 跨平台, 音频, OpenAL, 动态链接, X-Plane]
date: 2026-04-19
sources: 1
---

# OpenAL on Three Platforms（Ben Supnik / The Hacks of Life）

[[ben-supnik]] 2010 年 11 月的一篇小结，讲 X-Plane 怎么把 OpenAL 在 OS X / Linux / Windows 三个平台上装起来而不给终端用户多余的麻烦。

## 摘要

同一批 client code，三个平台的"runtime 从哪儿来" 完全不同。OS X 自 10.4 起 OpenAL 是系统 framework，直接 link 就行，要支持 10.3.9 再加 weak-link。Linux 一度从 `libopenal.so.0` 跳到 `.so.1` 而且**两者不共存**，团队干脆写一层**自己的 OpenAL 封装**——用 `dlopen` 先试 `.so.1` 再试 `.so.0`，逐符号 `dlsym` 填到内部函数指针表，把 SONAME 差异吸收掉。Windows 没有保证的 runtime：先加载系统目录 `openal32.dll`，失败就 fallback 到**随 app 分发的 LGPL OpenAL Soft 副本**——有硬件加速用厂家，没装 runtime 也有纯软件后备。另外 Windows 上要**让用户在 UI 里选 device**，避开 `alcOpenDevice(NULL)`——这样 Rapture3D 这类第三方 renderer 才有机会被选上。

## 关键要点

- 三平台的"runtime 哪里找"策略统一到**封装层 + 函数指针表**——上层代码永远认自己的 proxy，不 link-time 绑定真实 `.so` / `.dll`；
- Linux：`dlopen` fallback 串起 `.so.1` / `.so.0` 两个 SONAME；
- Windows：系统 `openal32.dll` 优先 + LGPL OpenAL Soft 自带副本兜底；
- Windows 上 default device 对跨 renderer 场景不够用，要在设置面板里列 device。

## 链接到的概念

- [[cross-platform-openal-runtime-loader]]
- [[shared-library-soname-versioning]]
- [[opengl-extension-bucket-strategy]]
- [[function-vs-data-pointer-portability]]

## 原文

- 链接：http://hacksoflife.blogspot.com/2010/11/openal-on-three-platforms.html
- 本地：`raw/articles/hacksoflife.blogspot.com/2010-11-08_openal-on-three-platforms.md`
