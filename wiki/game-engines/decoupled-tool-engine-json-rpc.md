---
tags: [工具链, 引擎架构, ipc, 迭代速度, bitsquid]
date: 2026-04-19
sources: 1
---

# 工具与引擎解耦：JSON over Socket

[[niklas-frykholm|Niklas Frykholm]] 2010 年这篇给 Bitsquid 的工具架构定了两条看似矛盾的目标：

1. **工具必须用真正的引擎做可视化**——所见即所得，"工具里看到的"和"游戏里跑的"必须像素级一致；
2. **工具不得强耦合引擎**——工具要能用任意语言（C#、Ruby、Lua、Python……）、任意 UI 风格、任意开发节奏来写。

目标 1 通常导致 "monolithic mega-editor"——引擎和编辑器链在一起编译。Bitsquid 的解法是把两者拆成**两个进程、用网络通信**。

## 架构核心

**工具和引擎之间没有直接 link**。工具发 JSON 消息给引擎，引擎发 JSON 回工具：

```json
{
  "type": "message",
  "level": "info",
  "system": "D3DRenderDevice",
  "message": "Resizing swap chain: 1626 1051"
}
```

所有交互都走这条通道：

- **Lua 调试器**：工具发"设断点 / lua 文件 + 行号"消息；引擎在命中时发回一条。任何人都能接上这套协议写自己的调试器；
- **Profiler**：引擎每帧把 profile sample 打包成一条消息发出去；
- **脚本命令**：工具发 `"ParticleEditorSlave:test_effect('fx/grenade/explosion')"` 这样的 Lua 脚本 string，引擎的 slave 脚本就按收到的指令操作场景。

## 可视化：子窗口嵌入

工具创建一个窗口，把**窗口句柄**发给引擎。引擎在那个窗口下创建**子窗口**，在里面跑自己的 swap chain 渲染。工具端看起来就是编辑器里嵌了一块「活着的游戏画面」，但实际上是引擎进程渲的。

后续规划里还提到 **VNC 风格** 的远程渲染——引擎把 framebuffer 通过网络送到工具端——这样编辑器可以直接连**主机**，美术就在编辑器里看主机上的画面（对 console 开发尤其重要）。和 [[runtime-editor-console-connection|runtime editor-console connection]] 的思路完全一致，只是 Bitsquid 早了好几年。

## Slave 脚本：工具的引擎侧入口

每个工具启动引擎时带一个特殊的 Lua 脚本，叫 slave script。粒子编辑器用 `particle_editor_slave.lua`，预先搭好默认场景（相机 / skydome / 灯光）；工具发来的命令由 slave 脚本解释执行。**slave 脚本通常很小**——粒子编辑器那个只有 120 行。

这把"工具特有的场景 / 交互逻辑"从引擎 core 里剥离出去，放到可以跟着工具一起演化的 Lua 脚本里。

## 数据分层：generic vs runtime

工具只看 **generic data**（人读、可扩展、向后兼容，Bitsquid 选 JSON）；引擎内部用 **runtime data**（快、紧凑、平台相关、随时可以被优化掉）。工具永远不用关心 runtime 格式长什么样。

当数据改动后：

1. 工具触发 data compiler：其实就是引擎本身加 `-compile` flag 启动（**所以数据编译器永远和引擎同步**，改了 runtime 格式就会自动触发 full recompile）；
2. compiler 只重编 dirty 的那部分数据；
3. 编译完后工具发消息让引擎 reload 那个资源——改动瞬间生效。

两种编译模式：**regular**（文件散落）用于开发，**bundled**（全塞进一个 gzip 包，按访问顺序排好）用于发布。对 nav mesh / lightmap 这类昂贵构建 Frykholm 倾向**同一格式、manual rebuild**，而不是"低精度模式"——因为"美术看到的和最终游戏长得不一样"是致命事。

## 为什么不是 monolithic editor

- **工具实现完全自由**：可以 C#、Ruby、Python，也可以让 licensee 自己写小脚本对某个管线做 batch 操作（比如"把所有植被贴图减一级 MIP"）；
- **引擎数据格式可以随便改**——只要 data compiler 跟着改了即可，工具不需要动；
- 想要"紧耦合"的特定情况（比如粒子编辑器里嵌一个材质编辑器），可以**有选择地**共享代码——不像 monolithic editor 那样是默认被绑死的。

## 一个工程约束：编译只在 Win32 dev 构建里

Frykholm 为了防止"引擎不小心读到未 build 的 generic 数据"，在 main 里写死：

```c
#if defined(WIN32) && defined(DEVELOPMENT)
  if (flags.compile()) {
      compile(generic_data_folder, runtime_data_folder);
      exit();
  }
#endif
run(runtime_data_folder);
```

编译流程只在 Win32 开发构建里出现；release 构建和 console 构建根本看不到 `compile()` 这个分支，防止人"偷懒留未优化数据"。

## 相关

- [[tools-first-iteration-loop]] — 为什么工具链优先级该高于新特性
- [[runtime-editor-console-connection]] — 更后期的引擎做一样的事（跨 PC-主机）
- [[binary-hot-reload]] / [[csharp-runtime-script-compilation]] — 缩短"改 → 看"延迟的相关技术
- [[offset-based-resource-blobs]] — Bitsquid 的 runtime 数据格式本身

## Sources

- [[sources/bitsquid-our-tool-architecture]]
