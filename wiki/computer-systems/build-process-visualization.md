---
tags: [构建系统, 性能分析, 可观测性, 工具, 系统调用]
date: 2026-04-19
sources: 2
---

# 构建时序可视化（Build Process Visualization）

一个构建脚本跑 35 秒、还是 3 秒，**差别 95% 来自可视化之前你看不到的部分**：哪些命令在串行跑、哪些本该并行、哪些启动阶段白白空转。Daniel Hooper 为此写了 *What The Fork*（`wtf`）——在 macOS / Linux / Windows 上拦截构建进程树的 `fork` / `exec` / `exit` 系统调用，把每个子进程画成一个色块，按启动时间横排，父子嵌套竖排。用法就是在任何构建命令前加 `wtf`：`wtf make` / `wtf cargo build` / `wtf gradle build` / `wtf zig build` / `wtf -x`（自动对 Xcode 当前工程）。**它与构建系统和语言无关**，因为它只听系统调用。

## 为什么必须听系统调用

构建命令行输出只能看到顶层工具打印的行，看不到**工具再 fork 出来的孙子进程**——clang 会偷偷调 `ld`、CMake 会反复调 `sw_vers` / `xcode-select`、gradle 会起 JVM daemon。要还原真实时间轴，必须从 OS 层面抓 fork/exec/exit：

- macOS：`EndpointSecurity` / DTrace（各有坑）
- Linux：`ptrace` / `eBPF`
- Windows：ETW

每家 API 都难用，但都能拼出一条**事件流**：`(pid, parent_pid, timestamp, cmdline, cwd)` → 可视化为甘特图。这套方法副产品能力：它能 profile 任意派生子进程的程序，不止构建。

## 肉眼能看见的四类问题

Hooper 在真实项目里拿着 `wtf` 就找到了这些：

1. **Cargo 单线程编译依赖**：某开源项目的一个依赖 crate 用 cargo 顺序编译源文件，10 核 M1 上全串行——装上 `wtf` 一眼就看出来，可能能提速 10×。
2. **CMake 的 weird dance 重复 85 次**：CMake 为探测环境会递归调 `cmake→make→make→clang`，中间跑 `xcode-select -print-path` / `sw_vers` 各一遍；同一构建里这套 dance 重复 85 次，每次都重新问一次 OS 版本。
3. **Xcodebuild 尾部空闲**：`xcodebuild` 构建 10 万行 ObjC 工程时，有 6 秒纯启动空转；尾段又经常只剩 1–2 个 clang 在跑。对比 ninja 构建 2.47M 行的 LLVM 只需 0.4 秒就开始 busy，**ninja 充当事实上的速度上限标杆**。
4. **Zig 随机依赖顺序的隐藏风险**：`zig build` 故意随机化依赖编译顺序，以暴露隐藏的顺序假设——但副作用是有时运气好全并行、有时 `curl` 被排到最后单线程拖尾。

## CI 构建是首要受益场景

CI 往往是 **clean build**，本地增量构建里藏不住的浪费在 CI 上会全部暴露。`wtf` 的开发者数据说某用户把 CI 重建时间 35s → 3.3s，10× 加速的量级与上面 Cargo 的例子是一致的——**大多数构建不是代码太多，是并行度没打满 + 每次都重查一次环境**。

## 要实现一个自己的版本

核心工作量在三块：

- **抓事件**：三个平台的系统调用 API 都各有各的坑，`ptrace` 的信号处理尤其繁琐；
- **存时间轴**：事件数量随构建规模线性增长，数量未知、指针要稳定（UI 要直接引用事件）——Hooper 就是因此写了 [[segment-array]] 做后备容器；
- **UI**：进程按父子嵌套画，按启动时间横排，hover 显示 cwd / argv / 耗时。

*What The Fork* 是商业产品化版本（早期 access 收费、买断制），Hooper 强调数据完全留在本机、可保存录像复盘。

## 相关

- [[segment-array]] — wtf 内部用来存事件流的数据结构
- [[ci-cost-optimization-asg]] — 另一个用数据驱动优化构建成本的实例
- [[daniel-chase-hooper]]

## Sources

- [[sources/hooper-build-visualizer]]
- [[sources/hooper-what-the-fork]]
