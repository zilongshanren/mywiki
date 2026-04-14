---
tags: [图像处理, dither, 量化, 误差扩散, 低端设备]
date: 2026-04-14
sources: 1
---

# Floyd–Steinberg 误差扩散 dither

Floyd–Steinberg 是 1976 年提出的经典**误差扩散（error diffusion）dither** 算法，用来把高位深图像量化成低位深调色板时尽量保留视觉质量。它和 [[dither-alpha-clipping]] 里那种"有序 Bayer 阈值"dither 是两种不同的思路：Bayer 用一张**静态阈值矩阵**做像素级 clip，属于 *ordered dither*；Floyd–Steinberg 则是**顺序扫描每一个像素，把量化误差按权重扩散到右下方的邻居**，属于 *error-diffusion dither*。后者在图案均匀度和色带抑制上明显更好，代价是不能并行、天然带顺序依赖。

## 扩散矩阵

Floyd–Steinberg 的权重矩阵是一个固定的 7/3/5/1 （除以 16）分配：

```
          *   7
    3    5    1
```

扫描到当前像素 `(x, y)` 时，先把它量化到目标调色板得到一个误差 `err = original − quantized`；然后把 `err` 按比例加到右邻 `(x+1, y)`、左下 `(x−1, y+1)`、正下 `(x, y+1)`、右下 `(x+1, y+1)` 四个还没处理过的邻居上。这样高频噪声在局部被"打散"，看起来比直接 round 平滑得多。Tanner Helland 的博客列出了这个系列的十一种变体（Jarvis–Judice–Ninke、Stucki、Atkinson 等），核心思路都是换一个不同的扩散 kernel。

## 工程上的细节：为 Android 低端机做优化

[[emilio-lopez-ros|Emilio López Ros]] 在 [[sources/elopezr-dragon-mania|Dragon Mania]] 的开发里遇到一个很窘迫的约束：目标机型 Galaxy Ace 吃不下 32-bit RGBA8888 纹理，必须降到 **16-bit 1555**，还要处理大约 900 张图，最大 1024×512。于是他用 Java 写了一版 Floyd–Steinberg，并做了四层迭代优化，把 512×512 图像的 dither 时间从 47 ms 降到 30 ms、1920×1200 从 104 ms 降到 70 ms。这几步优化很好地总结了"一个算法在 JVM 上怎么被压榨"：

1. **Naive**：双重整型数组 `[RGBA component][pixel]`，干净但慢；
2. **Invert indices**：换成 `[pixel][RGBA component]`，小分辨率下有速度提升，大分辨率反而变慢——典型的 JVM 内存布局/缓存假象；
3. **Padding 消除 if**：把目标数组上下左右各 pad 一行/列，把 Floyd–Steinberg 的 4 个边界 `if (x+1 < imgW)` 全部干掉，越界的误差直接写进 padding 区域事后丢弃——以少量内存换**去掉循环体里的分支**，效果立竿见影；
4. **Scanline alternation**：只分配**两行** scratch buffer，当前行和下一行轮替，扫描完一行就把结果 flush 进最终 buffer。内存从 `imgW × imgH` 降到 `2 × (imgW + padding)`，同时因为 working set 变小而再次轻微提速。

第四版比第一版整体快约 30%，内存消耗"可忽略"。这是一个很典型的"**算法层面早就定了，工程层面还能榨 30%**"的案例——关键动作都是经典的系统级套路：扁平化为 1D 数组、padding 消除分支、scanline 做流式内存复用。相比之下第二步（索引顺序互换）说明在 JVM 上盲目套用"连续内存更友好"的直觉是危险的，尺寸一变结果就反转。

## 和 alpha dither 的对照

误差扩散 dither 和 [[dither-alpha-clipping|alpha dither]] 常被混为一谈，但解决的问题完全不同：

- Floyd–Steinberg 解决的是**颜色量化**（把 8-bit 打到 5-bit 时的色带和精度损失），对象是**颜色通道**，输出仍然是连续像素；
- Dither alpha clip 解决的是**透明度伪装**（把半透明表现成离散 discard），对象是 **alpha 通道**，输出是二值 pass/discard。

两者共享同一个更大的信号处理直觉——**把低频可见的误差搬到高频不可见的频段**——这也是 [[color-banding|颜色色带 dither]] 和 [[taa-history-rectification|TAA blue noise]] 背后的共同道理。

## Sources

- [[sources/elopezr-floyd-steinberg-dithering]]
