---
tags: [c-sharp, .net, 脚本系统, 热重载, AppDomain]
date: 2026-04-14
sources: 1
---

# C# 作为脚本：运行时编译与热加载

游戏程序员引入脚本语言（[[lua-cpp-binding|Lua]]、Python、JavaScript）的最大动机是「改一段逻辑、不重启就能看到效果」。但如果母语本来就是 C#，其实可以在 .NET 运行时里**把 C# 自己当脚本用**——用 `CodeDomProvider` 在运行时把脚本源文件编译成 DLL，然后 `Assembly.Load` 进当前进程，调用静态入口。[[people/evan-todd|Evan Todd]] 在 2011 年给 Project Lemma（后来是 Lemma）实现了这套，目标是「保持写同样的 C# 代码、但是能用一个按键重编译并立刻看到效果」。和引入 IronPython 或 Lua 相比，这条路的诱惑是：**没有 marshalling、没有 binding glue、没有性能损失**。

## 整体架构

Todd 让所有脚本继承一个 `ScriptBase` 基类，基类提供静态的 `main` 引用以及 `get(string id)` 之类的便捷工具函数。脚本文件本身只是裸的语句列表，编译时由引擎自动套上 prefix / postfix——一段 `using` + `namespace Lemma.Scripts { public class Script : ScriptBase { public static void Run() { ... } } }`。这样脚本作者写起来像写 Lua，但底层是被 C# 编译器一次性编译成强类型代码。

执行逻辑就是反射拿 `Lemma.Scripts.Script` 类型，把 `main` 字段塞进去，然后调用静态 `Run`：

```csharp
Type t = assembly.GetType("Lemma.Scripts.Script");
t.GetField("main", BindingFlags.Static | BindingFlags.Public)
  .SetValue(null, this.main);
t.GetMethod("Run", BindingFlags.Static | BindingFlags.Public)
  .Invoke(null, null);
```

## 编译与缓存

调用 `CodeDomProvider.CreateProvider("CSharp")` 拿到 C# 编译器，构造 `CompilerParameters` 时关键是 `GenerateInMemory = false` + `OutputAssembly = binaryPath`——这样 DLL 会落盘，下次启动直接 `Assembly.Load` 就能跳过编译。引用集要把当前主程序的 `executingAssembly.Location` 以及它的 `GetReferencedAssemblies()` 全加上，否则脚本里 `using Microsoft.Xna.Framework` 之类的会找不到符号。

## 热重载的两个深坑

### 坑 1：DLL 文件锁

`Assembly.Load` 之后，.NET 运行时会**锁住 DLL 文件**，进程退出前都释放不了。这意味着「重新编译并覆盖原 DLL」直接失败。理论解法是把脚本扔进另一个 `AppDomain`，然后 `Unload(domain)`——但跨 AppDomain 通信需要 marshalling，整个引入 C# scripting 的初衷就被打回原形了。

正解是开启 **shadow copying**：让 .NET 运行时把每个 DLL 复制一份「影子副本」、加载副本而不是原文件，原文件就保持可写。但 shadow copying 这个属性必须在 AppDomain 创建时就指定，主 AppDomain 一旦跑起来就改不了。Todd 的 workaround 是写一个微型 launcher .exe，里头 `new AppDomain` 时把 `setup.ShadowCopyFiles = "true"` 打开，再用 `domain.ExecuteAssembly("Lemma.exe", args)` 在新 domain 里跑游戏：

```csharp
AppDomainSetup setup = new AppDomainSetup();
setup.ShadowCopyFiles = "true";
setup.ApplicationBase = baseDirectory;
AppDomain domain = AppDomain.CreateDomain("", AppDomain.CurrentDomain.Evidence, setup);
domain.ExecuteAssembly(Path.Combine(baseDirectory, "Lemma.exe"), args);
```

### 坑 2：`CodeDomProvider` 不走 shadow copy

更阴险的是 Todd 后来发现 `CodeDomProvider` 编译出来的 DLL **仍然被锁**。原因是 `CodeDomProvider` 内部不是优雅的 .NET wrapper，它实际 fork 了 `csc.exe` 编译器进程，再用 `Assembly.LoadFile`（而不是 `Assembly.LoadFrom`）把结果加载进来——而 `LoadFile` 不会触发 shadow copy。

Todd 的反向利用：**故意不指定 OutputAssembly**。这样编译器会写到一个临时路径，主程序虽然锁住临时文件但不在乎，因为还能从锁定状态读出 DLL 字节流，然后 `File.Copy` 到他真正想要的缓存路径。下次启动时再走标准的 `Assembly.Load`，那次会被正常 shadow copy。

```csharp
CompilerParameters cp = new CompilerParameters {
    GenerateExecutable = false,
    GenerateInMemory = false,
    TreatWarningsAsErrors = false,
};
// 编译后……
File.Copy(cp.OutputAssembly, binaryPath, true);
```

## 和 [[binary-hot-reload|C++ 二进制热重载]] 的对照

C++ 那条路的烦恼是 vtable、字符串字面量、struct 布局、线程栈这五件事会被 unload 抹掉。C# 走 `CodeDomProvider` 的路径绕过了一部分——GC 堆是统一的，托管对象不会因为某个 assembly 失活而被搬迁。但 Todd 也明确承认了一个**遗留代价**：旧脚本 assembly 永远卸不掉，会一直留在内存里，临时 DLL 文件也会锁到游戏退出。他认为这是可以接受的，因为「热重载只在编辑器里用，最终发布时不会反复 recompile」。

## 工程含义

- 选 C# 写脚本 = 拿到了脚本语言的迭代体验，又不必写 binding 层、不必付 marshalling 成本——**前提**是引擎本身就用 .NET。
- 任何「想在运行时换代码」的方案都要正面回答**unload 与文件锁**这两件事。.NET 给的答案是 `AppDomain` + shadow copy，但 `CodeDomProvider` 还有自己的怪癖要绕。
- 整套技术是 [[tools-first-iteration-loop|工具优先]] 哲学的一个具体实例：把「改 → 看」延迟从「重启游戏」压到「按一个键」。

## 相关

- [[binary-hot-reload]]
- [[tools-first-iteration-loop]]
- [[lua-cpp-binding]]
- [[runtime-editor-console-connection]]
- [[people/evan-todd]]

## Sources

- [[sources/etodd-csharp-runtime-compilation]]
