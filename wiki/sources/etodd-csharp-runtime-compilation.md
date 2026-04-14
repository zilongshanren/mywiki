---
tags: [source, c-sharp, .net, 脚本系统, 热重载]
date: 2026-04-14
sources: 1
---

# C# for scripting - runtime compilation（Evan Todd / etodd.io）

[[people/evan-todd|Evan Todd]] 2011 年 12 月的实战笔记，记录他给 Project Lemma（XNA / C# 引擎）实现「C# 自身作为脚本语言」的全过程，重点是**运行时编译 + DLL 热加载 + 解决 .NET 文件锁与 shadow copy 的两个深坑**。

## 摘要

Todd 调研了 IronPython、CSScript、Lua 这些 .NET 脚本方案，但都嫌它们要么慢、要么需要 marshalling、要么 binding 麻烦。他最后选了「直接把 C# 当脚本」：用 `CodeDomProvider.CreateProvider("CSharp")` 在运行时编译脚本源文件成 DLL、`Assembly.Load` 进当前进程、反射调用静态入口。脚本作者只写裸的语句列表，引擎自动套上 `using` + `namespace` + `public class Script : ScriptBase` 的 prefix / postfix。所有脚本继承 `ScriptBase` 基类，能直接拿到主游戏对象引用。

热重载部分是文章的精华。第一个坑：`Assembly.Load` 之后 .NET 锁住 DLL 文件，覆盖不了。开 `AppDomain` 的 shadow copying 能解决，但 shadow copy 必须在 AppDomain 创建时打开——Todd 写了个微型 launcher .exe，先创建一个开了 shadow copy 的 AppDomain，再 `ExecuteAssembly` 在里面跑游戏。第二个坑：发现 `CodeDomProvider` 实际上 fork 出 `csc.exe` 编译再用 `Assembly.LoadFile`，而 `LoadFile` **不走** shadow copy，DLL 还是被锁。Todd 的反向利用：故意不指定 `OutputAssembly`，让编译器写到临时路径——临时文件被锁无所谓，他从锁定状态里读字节流再 `File.Copy` 到他想要的缓存路径，下次启动再正常 `Assembly.Load`（那一次能 shadow copy）。文末承认遗留代价：旧 assembly 永远卸不掉、临时 DLL 锁到游戏退出，他认为可以接受因为热重载只在编辑器里用。

## 关键要点

- C# 自己当脚本 = 拿到脚本迭代体验，又不必写 binding / 不必付 marshalling 成本
- `CodeDomProvider` 编译 C# 到 DLL，`Assembly.Load` 加载，反射调用静态 `Run`
- DLL 锁定问题：必须用 `AppDomain` + shadow copy
- shadow copy 必须在 AppDomain 创建时打开 → 写 launcher .exe 在新 domain 里跑游戏
- `CodeDomProvider` 用 `Assembly.LoadFile` 不走 shadow copy → 不指定 OutputAssembly、让编译器写临时路径、再 File.Copy
- 遗留：旧 assembly 卸不掉、临时 DLL 锁到退出，但「只在编辑器里 recompile」可以接受

## 链接到的概念

- [[csharp-runtime-script-compilation]]
- [[binary-hot-reload]]
- [[tools-first-iteration-loop]]
- [[lua-cpp-binding]]

## 原文

- 链接：https://etodd.io/2011/12/10/c-for-scripting-runtime-compilation/
- 本地：`raw/articles/etodd.io/2011-12-10_c-for-scripting-runtime-compilation.md`
