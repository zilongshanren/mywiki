---
tags: [cpu, 微架构, 后端, 乱序执行, rob, 调度器, 派发停顿]
date: 2026-04-19
sources: 1
---

# 派发停顿分解：前端 vs 后端瓶颈

在乱序核里，rename/allocate 级位于前端（取指 + 解码）与后端（调度 + 执行）之间，是观察瓶颈来自哪一侧最方便的位置。George Cozma 在 Zen 3 上把这一级的两侧指标拆开：

- **Op Queue Empty** 占比：解码器或 [[op-cache-decoded-uop-cache|op cache]] 没能及时把微操作排进 renamer 前面的队列 → 前端瓶颈
- **Dispatch Stall** 占比：renamer 能出货但后端某个资源满 → 后端瓶颈

Zen 3 的实测结果（Cinebench R23、Civ VI、3DMark Timespy、War Thunder、EU4、Linpack）显示：所有负载都是**后端绑定**为主，但 War Thunder / EU4 的前端瓶颈也相当可观（op queue empty 分别达 16.12% 和 14.75%），这与它们本身分支密度高、代码足迹大有关。

## 后端资源的细分

renamer 需要从若干并行池中同时分配条目；任一池子满则停顿。Zen 3 的主要池子：

- **ROB（Reorder Buffer）**——保留所有未退休指令的程序序。在所有 workload 中都是最常见停顿因，占 8–20%。这其实是好事：说明核没先卡在更小的结构上，真的在把 ROB 填到上限，AMD 的队列规模匹配得不错。
- **Load / Store Queue**——存取操作的入口队列，分别占 2–5%。
- **FP 寄存器文件**——Linpack 场景下非常突出（高 FLOP 密度，产生大量 FP 写），Cinebench 次之。
- **INT 调度器 / INT 寄存器文件**——EU4 上略高（2–3.5%），可能因为该游戏大量短依赖链。
- **FP 调度器 / FP flush recovery**——几乎忽略不计。
- **Taken Branch Buffer**——被视为分支预测器的全局历史 checkpoint；EU4 最高也仅 1.57%。

## 前端的间接证据

前端侧除 op queue empty，还能看 [[branch-predictor-design|分支预测器]]：Zen 3 最差 97.29%（War Thunder），误预测率 <0.5%，但因为一次误预测要清空已取指令、还占用后端资源，真实损失远超图中显示。L2 BTB 覆盖不到时解码器自算地址要 ~12 周期惩罚。

L1i miss 也是前端压力的另一侧：IPC <1 的 Timespy/Linpack 可以用后端空转掩盖；CBR23/War Thunder 这类 IPC >1 的场景 L1i miss 会直接传导成前端停顿。

解码器带宽本身几乎不是瓶颈——Zen 3 有 4 路解码器，实测从未超过 2 IPC。

## Zen 4 的改进方向（根据作者推断）

后续从 [[gigabyte-zen4-leak]] 看 AMD 在 Zen 4 将 L2 从 512 KB 翻倍到 1 MB、L2 DTLB 从 2048 扩到 3072 条目，正好对应这里识别的两大痛点：ROB/LDQ/STQ 满常是因为数据没回来，更大更快的 L2 能直接降低这一类 stall；BPU 精度继续优化则压低误预测冲刷。

## 参见

- [[op-cache-decoded-uop-cache]]
- [[branch-predictor-design]]
- [[zen2-microarchitecture]]
- [[cpu-scheduler-design]]

## Sources

- [[sources/chipsandcheese-zen3-bottlenecks]]
