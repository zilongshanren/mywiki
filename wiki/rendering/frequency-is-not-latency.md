---
tags: [渲染, 延迟, 帧率, 感知, 运动模糊, 输入响应]
date: 2026-04-19
sources: 1
---

# FPS ≠ 延迟

[[angelo-pesce|Pesce]] 2011 年的《Tell the internet that you're not a moron》来自一次工业实战：EA《Fight Night Champion》（2011）从前作的 60fps 降到 30fps gameplay（物理仍 120Hz），互联网立刻把它解读为「为了更好的画面而阉割了手感」。文章是 Pesce 的反击，也是一条对大众游戏讨论极常见误解的**纯技术纠正**：

> **Frequency is NOT latency.** 帧率不是延迟。反复三遍。

## 为什么网民的直觉不对

玩家的响应链是：**输入设备采样 → 游戏逻辑 → 渲染 → 呈现**。手感取决于从按下按键到光到眼睛之间**中间过程的总耗时**，即端到端延迟。

60fps 意味着单帧预算 16.7ms，30fps 意味着单帧预算 33.3ms——这只是**最低延迟的下界**，不是延迟本身。现代 3A 游戏普遍在这条链上塞了几帧缓冲：

- **GPU ring buffer**：GPU 永远落后 CPU 至少一帧（要塞命令）。
- **输入采样队列**：为了做手势识别、滑动平均、防抖动，输入可能以 1000Hz / 10000Hz 采样后再被游戏消费。
- **引擎内的 sim / render / jobs / GPU 各级 double buffer**：每一层可能再加一帧——参见 [[frame-pipeline-latency|帧管线缓冲与延迟]]。
- **显示器内部延迟**、**合成器延迟**、**无线手柄传输延迟**。

一个 60fps 的 AAA 游戏，端到端延迟常常在 4-6 帧（≈ 66-100ms）；一个 30fps 的游戏若能压成 2 帧（≈ 66ms），**手感可以和前者接近甚至更好**。

Pesce 在评论区里甩下一句：**「你要是找得到一个 60fps、没有任何缓冲的 AAA 游戏我就信你。」** 这是一个根植于工业现实的反问。

## Fight Night Champion 的实际做法

- **物理 120Hz、游戏逻辑 60Hz、渲染 30Hz**——各层频率**按各自需要**定。物理要小步积分保证响应碰撞；输入要高频采样保证识别细微摇杆动作；渲染 30fps 配上高质量运动模糊反而更「有力量」「更电影感」。
- **运动模糊是 skinned-silhouette-aware 的**——沿骨骼蒙皮的轮廓正确模糊。他们曾在早期截图里用 Photoshop 手工模拟这个效果，发现**还不如真机效果好**。
- 决策是**盲测驱动**的：After Effects 原型（光流 motion blur）→ 引擎内原型 → 内部 + 外部盲测。多数测试者、制作人、甚至后来的玩家在**不知道数字**的情况下更偏好 30fps 版本。
- 但是**公布帧率数字**后，网民立刻倒戈——这就是文章标题的由来：**技术细节不讲清楚，就默认被当白痴。**

## 30fps + motion blur 受欢迎的机制

评论区有人联想到「**soap opera effect**」——24fps 电影被插帧到 60Hz 后观众反而觉得廉价。可能的解释：

1. 观众被 24fps 电影训练得把低帧率当「电影感」。
2. 24-30fps 恰好落在人眼时序整合的**甜点区**，配合正确的运动模糊后反而接近自然感知。

Pesce 没有敲定任何一个解释，但强调他们的运动模糊是 **optical flow** 驱动的、不是简单的时间域插帧——软搜里 soap opera 来自廉价 temporal resampling，与正确的运动模糊是两回事。

## 对工程沟通的延伸：少数字多演示

文章结尾拔高到**工程传播**层面：做了取舍就大方承担——**展示你做了什么、为什么做**，不要只放一个数字就让网民拿着去吵。否则你会被当成白痴，即使你测过玩家更喜欢你的版本。

这条「**数字不是质量，体验才是**」和游戏圈长期的「分辨率优越症」（1080p = 好、900p = 差）、「帧率优越症」同构。Pesce 的立场和 [[stable-fps|稳定帧率优先]] 的工业共识一致——**手感优先于瞬时指标**。

## 和其它文章的关系

- 和 [[frame-pipeline-latency]] / [[threads-buffers-and-latency]] 是**一体两面**：那篇讲「你的引擎到底有几层缓冲」，这篇讲「为什么大众用帧率数字判断手感是错的」。
- 和 [[cpu-gpu-pipelining-input-lag]] 的独立开发者视角呼应：Max Prerendered Frames、fence、VSync 在 2011 年就是显式可调的。
- 和 [[experience-as-noise-filter]] 的精神一致——经验丰富的从业者**不被表面数字拐走**。

## 相关

- [[frame-pipeline-latency]]
- [[cpu-gpu-pipelining-input-lag]]
- [[stable-fps]]
- [[experience-as-noise-filter]]
- [[angelo-pesce]]

## Sources

- [[sources/c0de517e-tell-internet-not-moron]]
