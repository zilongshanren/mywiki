---
tags: [调试, 内存, 工程实践, bitsquid, ps3]
date: 2026-04-19
sources: 1
---

# 内存破坏类 bug 的系统化狩猎

[[niklas-frykholm|Niklas Frykholm]] 2011 年这篇是一份"**submission 前一周、只在 release 构建、只在 PS3、每次崩在不同调用栈、复现率低**"——游戏行业里最让人绝望的那类 bug 怎么抓的工程日志。重点不是某个具体 trick，而是一套**从 symptom 反推 hypothesis、再用受控实验逼近 root cause** 的流程。

## 先做一件事：别慌，写下来

Frykholm 的起手动作是拿一张纸把**关于这个 bug 已知的和不知道的所有事**列出来，想到新的假设就加进去、排除一个就划掉一个。核心判断：**恐惧来自无知**，你越知道得多、bug 越不可怕。不要盯着"怎么修"这个当下根本做不到的事，盯着"我现在能学到一点什么关于它的信息"。

## 从 symptom 读 hypothesis

每一条"看起来很烦"的属性其实都在泄露信息：

- **只在 release 复现** — 很可能是 debug 里某段代码（assertion、memset、额外初始化）**掩盖**了 bug；或者 bug 依赖时序，debug 的慢让它消失；或者是**未初始化变量**在 debug 下被自动清零。
- **只在 PS3 复现** — 大概率在 PS3 专属子系统（SPU、DMA、平台内存）。
- **低复现率** — 依赖随机性，典型就是未初始化内存的随机 bit 或线程调度的非确定性。
- **不同调用栈** — 最强信号：**某个坏系统正在覆盖别人的内存**，被覆盖者挨个在不同位置崩。

把这些拼起来就是一个很可操作的工作假设：**时序或未初始化相关的问题，让某个系统（可能 PS3 专属）越界写到了别人家的内存**。

## 把复现变稳

做实验的前提是能**反复**复现。哪怕只能做到 30%，也把它脚本化跑 20 次——单次看不见和 20 次看不见的置信度完全不同。Frykholm 特别提到：让脚本自动跑的时候，你可以去倒杯茶。这是**把思考和验证解耦**——验证交给机器。

## 受控实验清单

核心方法论是**改一样、看 bug 是否变化**。触发一套工程上常见的"按系统关/开"与"按内存工具切换"：

- **逐系统 disable** — 关声音、关渲染、关 AI，一个个关直到 bug 消失；依赖前提是**引擎是模块化、子系统可独立关**（呼应 [[managing-coupling|管理耦合]]）。
- **git bisect** — 如果 bug 最近才出现，二分版本历史直接锁定 commit。
- **data breakpoint** — 如果每次都踩同一个地址，在那地址放 memory write breakpoint，直接等坏人来签到。
- **看被覆盖的 pattern** — 0x????字节里有没有熟悉的值（某个 struct 的 magic、某个 float 的精度尾部）？能识别出就知道凶手的 family。
- **malloc 填特定 pattern** — 在自定义 allocator（Bitsquid 自己写，见 [[custom-allocator-interface]]）里让 `malloc` 填 `0x00/0xFF/0x12345678`，bug 行为变了就是**未初始化内存**的锅。
- **free 清零 / canary** — 释放时把内存清成 pattern，任何"free 后还在写"的代码会更显眼；或 allocate 时多要几 byte 放 canary pattern，free 时检查，**buffer overflow** 立刻报。
- **disable multi-threading** — 所有系统在同一线程跑，bug 没了就是 race condition。
- **memory verification** — 很多 allocator（dlmalloc 等）都能遍历所有 block 检查 header；每隔 N 帧跑一次，把"什么时候 header 被改坏"压到一个时间区间内，再二分缩小。
- **换 allocator** — 切到 system malloc、dlmalloc、自己的 allocator，把 crash 移位有时能让真凶露出来。
- **切虚拟内存 allocator** — 让可疑子系统走 VMM，release 后的访问直接 page fault，不用等它覆盖到别人家。

## 收束到一个答案

这篇结尾给了个实际案例：测试脚本 + 系统级 disable + 版本回溯把嫌疑锁到"SPU 解压"子系统（新加的、PS3 专属）；把这个系统的 allocation 换成 VMM，坏写立刻抛 DMA 错，一下看到**解压目标 buffer 被 free 之后 SPU 还在 DMA 往里写**——典型的 lifetime race。看一眼代码就修掉。

## 和 Valgrind / ASan 的关系

评论区有人提醒可以跑 Linux build 让 Valgrind 扫（现代工具链里 ASan / MSan 也是）。Frykholm 回复说这对 PC 系统很香，但对 **SPU 代码无效**——这也是主机时代这类方法论必须存在的理由。今天在 PC 上，ASan / MSan / TSan 已经把"填 pattern / canary / clear on free"这些手动招数收进了编译器；但逐系统 disable、git bisect、hypothesis 列表这套**元方法**仍然完全适用。

## 相关

- [[custom-allocator-interface]] — 这些招数的前提：自己的 allocator 接口允许替换 / 插桩
- [[managing-coupling]] — 模块化是"按系统 disable"成立的前提
- [[static-hash-value-debug-assert]] — 另一套类似气质的"debug 时多装一层保险"工程技巧
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-extreme-bug-hunting]]
