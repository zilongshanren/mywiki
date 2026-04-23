---
tags: [渲染, 延迟, 并行, 引擎架构]
date: 2026-04-19
sources: 1
---

# 帧管线缓冲与延迟

游戏的多级并行化让每一帧都要经过一串**缓冲队列**：模拟 → 渲染 → worker job → GPU。每一层缓冲都是一次**额外延迟**——从玩家按下按键到画面出现的总延迟，大约等于各层 stage 数乘以一帧时长。

[[angelo-pesce|Pesce]] 在 2010 年提了个清单式的小问题：**你的引擎有几帧延迟？** 他自己当时的工程至少三层：sim → render、render → jobs、jobs → GPU，还不算他没管到的子系统。每层 stage 独立 double-buffer，看起来是无痛并行化；但**累加之后，30fps 的游戏很容易吃到 100 ms 输入滞后**。

## 为什么工业界倾向合并 stage

触发这篇笔记的是 Digital Foundry 关于新《极品飞车》的访谈：**下一作要回到单线程、不拆 sim/render 的结构**，因为 30fps 下那一帧 sim-render 缓冲在实机手感里很明显。这呼应了一个更普遍的模式：

- **高帧率 + 多 stage**：每帧代价小，累加几层仍然可接受（60/120fps 下一两帧缓冲 ≈ 16–33 ms）。
- **低帧率 + 多 stage**：每层 33 ms 起步，三层就 100 ms，玩家能感知到。

因此有些 30fps 项目宁可牺牲并行度去换输入响应；而 60fps 目标的项目更敢拆细。更进一步的做法见 [[frames-in-flight]] ——把 flight 深度做成可配置、按平台 / 模式调。

## 衡量延迟的操作手法

- **数 stage**：sim、render、submit、GPU、present、compositor，每一层都问「这个 stage 和下一个 stage 之间有几帧队列？」
- **工具**：帧捕获器 + 输入时间戳 + 拍摄手柄屏幕能直接量出端到端延迟。
- **区分类型**：GPU pipelining（驱动 / compositor 强制的）通常不可控；应用层 sim-render 解耦是可调的；VR / 云游戏还有额外 warp / 编码队列。

## 权衡框架

并行缓冲交易的是**吞吐 / 稳定性 vs 延迟**：

- 拆 stage → 每 stage 预算宽松 → 吞吐稳定、更容易避免掉帧。
- 合 stage → 总延迟下降 → 手感更好，但任一 spike 都撞上 frame deadline。

没有通用正确答案。Pesce 的提问本身是有价值的——大多数工程师**不知道自己引擎实际上有几层延迟**，因为每个子系统的作者只对自己那段负责。先数清楚，再决定要不要砍。

## 相关
- [[frames-in-flight]]
- [[stingray-default-frame-flow]]
- [[mgs-v-fox-engine-frame]]
- [[unreal-frame-breakdown]]
- [[angelo-pesce]]
- [[cpu-gpu-pipelining-input-lag]] —— Joost 2011 从独立开发视角讲 Max Prerendered Frames / fence / VSync
- [[frequency-is-not-latency]] —— Pesce 2011 Fight Night Champion：FPS != 延迟的大众沟通面

## Sources

- [[sources/c0de517e-threads-buffers-and-latency]]
