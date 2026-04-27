---
tags: [rendering, hdr, post-processing, compute-shader, exposure]
date: 2026-04-27
sources: 1
---

# 亮度直方图自动曝光

在物理正确的渲染管线里，场景亮度可能跨越多个数量级（太阳直射面 vs 深阴影），必须在送入 [[tone-mapping|色调曲线]] 前先将亮度缩放到合适范围。**自动曝光**通过计算当前帧的"代表性平均亮度"，按摄影曝光公式推导出线性缩放因子，让色调映射在合理的工作域内运行。

## 为什么用直方图

最简单的方案是对 HDR 帧缓冲做 mip 链，最终 1×1 级别即为几何平均值。但几何平均会被极端亮点（如太阳、灯泡高光）或极端暗区（黑色背景大面积）强烈拉偏，导致曝光不稳定。

**亮度直方图**将场景亮度的对数值量化到 256 个 bin，记录每个 bin 的像素计数，然后计算加权平均，完全忽略最暗的 bin（纯黑/低于阈值的像素，存在 bin 0 中）。这种做法等效于摄影里的"避开死黑区域测光"，结果更稳定，也更容易扩展为中位数或其他统计量。

## GPU 实现（两趟 compute）

### 第一趟：填充直方图

以 16×16 线程组处理 HDR 图像，每线程取一像素，计算亮度 `lum = dot(rgb, vec3(0.2125, 0.7154, 0.0721))`，通过 `log2(lum)` 规范化到 [0, 1] 的对数区间，映射到 bin 1–255（亮度低于阈值归入 bin 0）。线程组内用 **shared memory** 先累加局部直方图，再用 `atomicAdd` 合并到全局 buffer，减少对全局内存的锁争用。

### 第二趟：并行归约求均值

256 个线程各自持有一个 bin 的计数，先用共享内存存储 `count × bin_index`（加权值），再执行经典的**并行归约加和**（每次迭代对半折叠，O(log N) 步完成），把加权总和收拢到 `histogramShared[0]`。最后将分母设为非零像素总数（排除 bin 0 中的纯黑像素），反查对数空间得到实际平均亮度值。

### 时序平滑

为避免相邻帧曝光突变（闪烁感），新计算的平均亮度与上一帧的值做线性插值：`adaptedLum = prevLum + (newLum - prevLum) * timeCoeff`，结果写入一张 1×1 R16F 纹理供后续 pass 读取。`timeCoeff` 控制眼睛适应速度，可以分别设置暗→亮和亮→暗的不同速率，模仿人眼的非对称适应。

## 与曝光公式的衔接

获得平均亮度 `L_avg` 后，通过 Frostbite（Lagarde & de Rousiers 2014）的摄影曝光公式计算 EV：

```
L_max = 78 / (q * S) * N² / t    (q=0.65, S=100, N²/t = EV exposure)
exposure = 1 / L_max
scaled_luminance = L_in * exposure
```

常用简化式 `exposure = 0.18 / L_avg`，把"中灰"映射到 0.18 附近。得到的 `scaled_luminance` 仍未经裁剪，需要 [[tone-mapping]] 曲线进一步压缩。

## 参见

- [[tone-mapping]] — 曝光缩放后的曲线处理
- [[local-tonemapping]] — 全局曝光的局部扩展

## Sources

- [[sources/bruop-exposure-histogram]]
