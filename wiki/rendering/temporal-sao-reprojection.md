---
tags: [渲染, 环境光遮蔽, ssao, sao, temporal, reprojection]
date: 2026-04-19
sources: 1
---

# SAO 的 Temporal Reprojection

Bitsquid 在 2015 年把 Morgan McGuire 的 **[Scalable Ambient Obscurance (SAO)](http://graphics.cs.williams.edu/papers/SAOHPG12/)** 主机版本压到 Xbox One 上 1–1.5 ms 预算的核心手段，是**把 AO 的采样数沿时间分摊**——每帧只打 6–8 tap，但靠跨帧累积把等效采样数撑起来。这是 [[temporal-supersampling|temporal supersampling]] 框架应用到屏幕空间 AO 上的一次具体落地，和 [[hbao-interleaved-sampling|HBAO interleaved sampling]] 属于同一家族的不同路径：后者靠空间 4×4 小 pass + blur 换 cache 友好，前者靠时间轮转换总采样量。

## 采样分布：Halton + Bayer dithered offset

温水煮青蛙的关键是**让 N 帧的 N 组样本在角度空间里尽量互不覆盖**。Jp 的做法：
- **角度方向用 Halton 序列**：首 8 项 base-3 Halton = `{1/3, 2/3, 1/9, 4/9, 7/9, 2/9, 5/9, 8/9}`，乘以 2π 得到 8 个均匀分布的 rotation——跟 Brian Karis 2014 TAA 的 subpixel jitter 是同一套 low-discrepancy 思路（[[low-discrepancy-sequence]]）。
- **半径用 4×4 Bayer 矩阵 dither**：加一个像素位置依赖的 offset，去掉 Halton 本身可能产生的 banding。

## 相似度函数：三项乘积

时域重投影的成败几乎全在 **相似度函数**（"上一帧这个像素还能代表当前表面吗？"）。Jp 把它拆成三项互独立、可单独可视化的 term：

1. **Disocclusion term**（depth similarity）：`saturate(pow(prev_depth/current_depth, 4) + min_similarity)`。这是 Huw Bowles 《Iterative Image Warping》里的相对深度比阈值，对 camera 前后切换和 occluder 移开两种情况都稳。
2. **Velocity term**：`saturate(velocity * scalar)`。**动得越快、历史越不可信**——这是 reprojection 的通用原则。
3. **Dangerous samples term**：这是 SAO 特有的。一个 AO 样本如果 tap 到了**正在运动的物体**上，就算当前像素本身是静止的，AO 值也会随邻居运动而抖——这类 ghost 普通 reprojection 抓不出来。

## Dangerous Samples：把 moving bit 塞进 depth mip

Jp 的最大工程 trick 是：**在 depth buffer 的一个 bit 里编一个 "moving" 标志**，而且当 SAO 下采样 depth mip chain 时**把这位 bit 向下层传递**。于是 SAO 每次 tap 深度顺手就读出了"我采到的邻居是不是在动"——零额外开销。想法出自 Anton Michels 在 Siggraph 2015 *Rendering Techniques in Rise of the Tomb Raider* 里的分享。

然后把这位 term 按 Oliver Mattausch GPU Pro 2 的 "smooth invalidation" 思路**沿时间累积**：

```
samples_similarity = saturate(num_moving_samples * scalar);
samples_similarity *= (LOW_VELOCITY_SIMILARITY - MIN_SIMILARITY);
samples_similarity = lerp(samples_similarity, prev_samples_similarity, 0.9);
samples_similarity = min(samples_similarity, current_samples_similarity);
```

`lerp(..., 0.9)` 是关键——一个 tap 哪怕只有一帧碰到 moving object，整段历史都要被削掉一段时间，而不是立刻恢复。最终相似度是三项的组合：

```
similarity = depth_similarity * LOW_VELOCITY_SIMILARITY - velocity_similarity;
similarity *= (LOW_VELOCITY_SIMILARITY - HIGH_VELOCITY_SIMILARITY);
similarity = saturate(similarity - samples_similarity);
```

## 和 Wronski AC4 的异同

都属于 SSAO + temporal supersampling 家族，但取舍不同：
- **Wronski 的 AC4 SSAO**（[[temporal-supersampling#SSAO 的特殊例子]]）：只靠 depth rejection，3 帧轮换 spiral 图案；他明言"一天就接完"，因为 AO 区域深度本来连续，没有最终帧那种 color ghost。
- **Jp 的 Stingray SAO**：引入了 moving-bit 的 dangerous-samples 机制，专治"静止像素的邻居在动"这类二阶 ghost，代价是要改 depth buffer 编码和 SAO downsample shader。

两种思路**共同证明了 temporal supersampling 是屏幕空间 AO 的标配路径**，只是激进程度不同。

## 相关

- [[temporal-supersampling]]
- [[hbao-interleaved-sampling]]
- [[ground-truth-ambient-occlusion]]
- [[temporal-antialiasing]]
- [[motion-vectors]]
- [[low-discrepancy-sequence]]
- [[niklas-frykholm]]

## Sources

- [[sources/bitsquid-temporal-sao]]
