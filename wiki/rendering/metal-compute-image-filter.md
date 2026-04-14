---
tags: [渲染, metal, compute-shader, 图像处理, 后处理, gpgpu]
date: 2026-04-14
sources: 1
---

# Metal 计算内核做图像处理（filter 链与 thread grid）

[[warren-moore|Warren Moore]] 的 *Fundamentals of Image Processing in Metal* 把 Metal 的 **compute shader**（`kernel` 函数）落地成一个能链式使用的图像滤镜框架。文章选了两个滤镜做示范——**去饱和**和 **2D Gaussian Blur**——但重点不是滤镜算法，而是"把 GPU 计算当成图像管线中间节点"的工程模式：filter 作为 provider / consumer，通过懒求值串成一条有向图。这一页从它身上拎出在 Metal 里写 image compute 的三个关键模式。

## 模式一：thread grid 与 `thread_position_in_grid`

Compute kernel 的入口参数带一个 `uint2 gid [[thread_position_in_grid]]`——Metal 会调度一个 2D 的 thread grid，让每个 thread 处理一个像素，`gid` 就是当前 thread 在整个 grid 里的 `(x, y)` 坐标。kernel 里直接拿 `gid` 当源像素坐标去读/写纹理：

```metal
kernel void adjust_saturation(
    texture2d<float, access::read>  inTexture  [[texture(0)]],
    texture2d<float, access::write> outTexture [[texture(1)]],
    constant AdjustSaturationUniforms &u       [[buffer(0)]],
    uint2 gid [[thread_position_in_grid]])
{
    float4 inColor = inTexture.read(gid);
    float Y = dot(inColor.rgb, float3(0.299, 0.587, 0.114));    // BT.601 亮度
    float4 gray = float4(Y, Y, Y, 1.0);
    outTexture.write(mix(gray, inColor, u.saturationFactor), gid);
}
```

两个值得记住的细节：

- **`access::read` / `access::write`** 是 texture 模板参数，限制 kernel 能在这个 texture 上做什么操作——Metal 2014 年不支持同一个 texture 同时 read 和 write（后来加了 read_write），所以 filter 必须把**输入 texture 和输出 texture 分开两张**。
- **BT.601 亮度系数 `0.299 / 0.587 / 0.114`** 是把 RGB 压成灰度的标准（人眼对绿最敏感、红次之、蓝最少），三个系数之和为 1。`mix(gray, color, factor)` 是 Metal 标准库的 `lerp`——factor=0 全灰、factor=1 原色。

## 模式二：Threadgroup 的尺寸对齐陷阱

host 侧 dispatch 一次 kernel 要给两个数：每个 threadgroup 里多少线程（通常 8×8 或 16×16）、要多少个 threadgroup。简单写法是：

```objc
MTLSize tgCount = MTLSizeMake(width / 8, height / 8, 1);
```

**当 width/height 不能被 8 整除时**，这个写法会把边缘几行像素跳过。评论区 Philip G 给出的修复是向上取整：

```
tgCount = ((w + tg.w - 1) / tg.w, (h + tg.h - 1) / tg.h, 1)
```

但向上取整又带来**越界读取**：边缘线程的 `gid` 会超出 texture 范围，`read(gid)` 行为未定义，大多数 GPU 返回黑像素，于是边缘会出现一圈黑边——文章里的 gaussian_blur_2d 正是这样。两条出路：kernel 里手动判 `gid.x >= width` 再 early return；或者用 A11 之后支持的 `dispatchThreads:threadsPerThreadgroup:`（**non-uniform threadgroup**）——Metal 会自动让最后一行/一列的 threadgroup 尺寸变小，精确匹配图像维度，无需手动 bounds-check。

## 模式三：Filter 作为 Provider / Consumer 的懒求值链

Warren 把 filter 抽象成一对协议：

```objc
@protocol MBETextureProvider @property id<MTLTexture> texture; @end
@protocol MBETextureConsumer @property id<MBETextureProvider> provider; @end
```

每个 filter **同时实现这两个协议**——读上游的 provider、把自己的内部 texture 暴露给下游。使用方式是声明式链条：

```objc
desaturate.provider = imageProvider;
blur.provider       = desaturate;
imageView.image     = [UIImage imageWithMTLTexture:blur.texture];
```

关键点是**懒求值**：`blur.texture` 的 getter 发现自己 dirty，就向上游 `desaturate.texture` 拉，触发去饱和 kernel；desaturate 再向 `imageProvider` 拉图像；拉完再跑自己的 blur kernel。每个 filter 有一个 `dirty` 标志，在 uniform 参数被修改时置位（自定义 setter 里做），从而在下一次 `texture` 调用时重新 dispatch。这是**Unix 管道那种声明式组合**搬到 GPU 计算上的直接翻译。

实现上所有 filter 共享一个 `MTLCommandQueue`（在 `MBEContext` 里），每个 `applyFilter` 调用都起一个新的 command buffer + compute command encoder + dispatch + commit。因为同一队列里命令是**顺序执行**的，所以上游 filter 写完 texture、下游 filter 再读，**天然有序**，不需要额外 barrier。

## Gaussian 权重作为查找纹理

文章里 Gaussian blur 的另一个有意思的细节是：**预计算的 2D 权重矩阵通过 `MTLPixelFormatR32Float` 纹理而不是 constant buffer 传入**。理由是权重尺寸会变（半径可调），用纹理比用固定大小的 buffer 更灵活；kernel 里以 `weights.read(kernelIndex).rrrr` 取出单通道浮点值。这意味着半径改变时只需要重建这张权重纹理，不用改 shader，也不用改 pipeline state。

当然这个实现没有用 [[separable-gaussian-blur|可分离性]]——2D 卷积被直接写成双重循环 `for(j) for(i)`，每像素采样 `N²` 次。评论区 koby 报告"加一个 saturation filter 就从 60fps 掉到 12fps"——原因也在这里：盲目写 compute 循环比直接在 fragment shader 里做同样的 lerp 慢得多，因为 fragment stage 有光栅化器和 hierarchical Z 这些"免费"帮手。Warren 的回答也承认了这点：**image effect 如果能融合进 fragment shader，就别上 compute kernel**；compute 的价值在于**不适合光栅化表达的计算**（直方图、物理模拟、非 1-to-1 的空间结构）。

## 异步驱动：dispatch_async + job index 版 debounce

UI slider 拖动会产生高频更新，每次都重新跑 filter 链会把主线程卡住。文章用 GCD 做了一个 **job index 去抖**：主线程每次 slider 回调就 `++self.jobIndex` 并记下当前值，然后 `dispatch_async` 到后台队列；后台队列在真正执行前比较 `currentJob != self.jobIndex`——不匹配说明有更新的任务在排队，当前就跳过。这是用"乐观晚比较"替代 cancellation 的经典 trick，代码量极少。

## 相关

- [[metal-api-overview]]
- [[metal-shading-language-basics]]
- [[image-convolution-kernel]] —— 2D 卷积的通用数学
- [[separable-gaussian-blur]] —— Warren 的 kernel 没走的优化路径
- [[color-space]] —— BT.601 亮度系数的背景
- [[warren-moore]]

## Sources

- [[sources/metalbyexample-image-processing]]
