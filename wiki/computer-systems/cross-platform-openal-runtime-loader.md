---
tags: [跨平台, 音频, 动态链接, dlopen, ABI, OpenAL]
date: 2026-04-19
sources: 1
---

# 跨平台 OpenAL 运行时装载：一条「dlopen fallback + 自带 LGPL 副本」的路径

OpenAL 是 Loki 时代留下来的 3D 音频 API。规范里的接口是稳定的，但**哪里能找到实现** 在三个桌面平台上的策略完全不同。Ben Supnik 2010 年写过 X-Plane 的做法——用**同一份函数指针封装层**把三个平台的差异收纳掉，对上层 client code 来说 `alSourcePlay` 永远是那个 `alSourcePlay`。

## 三平台的装载现状

### OS X：有 framework，但要 weak-link 兜底

OpenAL 从 **OS X 10.4** 起作为系统 framework 出货，link 进 `OpenAL.framework` 即可。如果要支持 10.3.9 这种更老的版本，就 **weak-link** 加一个符号 NULL 检查（运行时判断当前系统是否提供了对应函数），这是 OS X 处理 "新 framework 但要老系统也能跑" 的标准做法。

### Linux：SONAME 从 `.so.0` 跳到 `.so.1` 而且两者不共存

OpenAL 的参考实现 → 被 OpenAL Soft 重写，发行版随之把 `libopenal.so` 的 **SONAME 从 major 0 升到 major 1** 而且**删掉旧的 `.so.0`**。这是 [[shared-library-soname-versioning]] 页里讨论过的那个 ABI 管理争议——"为了清掉一个历史上错误导出的 `alBufferAppendData` 符号，让所有下游强制重编译"。

抱怨没用。X-Plane 的做法是**写一层 OpenAL 封装**——不在 link 时依赖 `-lopenal`，而是启动时用 `dlopen` 试开 `libopenal.so.1`，失败了再试 `libopenal.so.0`，逐个符号 `dlsym` 填进本地函数指针表。核心 spec 里的符号在两边都有，所以单套 `.so` 名字策略就兼容了两个 major。

### Windows：system `openal32.dll` + 自带 LGPL 副本兜底

Windows 没有任何官方来源保证终端用户系统里有 OpenAL runtime。DirectSound 几乎一定有，OpenAL 则不一定。路径是：

1. 先从系统目录 `openal32.dll` 加载（这是 Creative 的"正规"安装点）；
2. 加载失败就 fallback 到**随 app 一起分发的 OpenAL Soft DLL**（LGPL 允许这么做，条件是用户可以替换这份 DLL）。

这样有硬件加速的机器能用到厂家实现，没装 runtime 的机器也有 OpenAL Soft 做纯软件后备。

## 同一份代码：函数指针表 + dlopen/LoadLibrary

三平台收敛到**同一个 OpenAL 封装层**：

- 启动时 `dlopen` / `LoadLibrary` 找到正确的 `.so`/`.dll`；
- `dlsym` / `GetProcAddress` 填函数指针；
- Client code 只认封装层的 `alSourcePlay` 之类的代理函数，不在 link 时直接引用。

Linux 的 dlopen fallback、Windows 的 "system 优先 + 自带副本兜底" 都能用这同一条装载管线表达，因为**唯一真正变的是"打开哪个 `.so`/`.dll`"**——一旦句柄在手，函数指针表填充和调用是一模一样的。OS X 由于有正式 framework，可以走 link-time 路径，只是也兼容封装层的间接调用。

## 多 renderer：给用户选设备的口子

Windows 上进一步复杂：**OpenAL runtime（谁提供 dll）** 和 **renderer（实际出声音的路径，比如 EAX 硬件、Rapture3D、OpenAL Soft 自身）** 是两件事。同一个 dll 背后挂着多个 device，每个 device 对应一种 renderer。

标准做法是**不调用 `alcOpenDevice(NULL)` 默认 device**，而是**在设置面板里列出可用 device 让用户选**——比如玩家买了 Rapture3D 想用它的 HRTF 就该能选上。OS X / Linux 上这个顾虑相对小（系统级音频路由比较可控），所以 default device 可以直接用。

## 这套手法能迁移到哪

更一般的模式：**当平台的"怎么找到某个 API runtime"策略不一致时，把 API 调用全部绕过 link-time 直接走封装层的函数指针**——把差异收在"装载阶段"，上层业务逻辑零改动。同一套思路在 [[opengl-extension-bucket-strategy|OpenGL 扩展加载]]、[[lua-c-api-dylib-proxy|Lua C API dylib 代理]] 上都能看到。代价是放弃 link-time 符号检查，得自己维护函数签名与真实 runtime 匹配。

## 相关
- [[ben-supnik]]
- [[shared-library-soname-versioning]] —— 同一作者同一时期对这次 `.so.0 → .so.1` 升级的 ABI 观点
- [[opengl-extension-bucket-strategy]]
- [[function-vs-data-pointer-portability]]
- [[lua-c-api-dylib-proxy]]
- [[unix-symbol-visibility-leakage]] —— 把 dlopen + dlsym 那条「唯一能绕过扁平命名空间」的定律放回扁平命名空间的底层语义里解释

## Sources

- [[sources/supnik-openal-three-platforms]]
