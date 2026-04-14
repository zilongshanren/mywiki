---
tags: [source, 渲染, metal, compute-shader, 图像处理, gpgpu, 教程]
date: 2026-04-14
sources: 1
---

# Fundamentals of Image Processing in Metal（Warren Moore）

[[warren-moore|Warren Moore]] 2014 年 10 月的 *Metal by Example* 教程，把 Metal 的 `kernel` 函数（compute shader）拿来做图像处理。文章通过一个**可链式组合**的滤镜框架演示两个具体滤镜——**saturation adjustment**（去饱和）与 **2D Gaussian blur**——最终在 iOS 界面上把 slider 实时映射到两个参数。

## 摘要

文章先定义两个协议 `MBETextureProvider` / `MBETextureConsumer`，让每个 filter 既可以作为上游（输出 texture）又可以作为下游（消费 texture），从而以声明式方式把滤镜链起来：`imageProvider → desaturateFilter → blurFilter`。基类 `MBEImageFilter` 管理 compute pipeline state、internal texture 和 dirty 标志——uniform 参数改变时置脏、下次读 `texture` 时触发懒求值重跑 kernel。去饱和 kernel 用 **BT.601 亮度系数 `(0.299, 0.587, 0.114)`** 把 RGB 压成灰度，再用 `mix(gray, color, factor)` 线性插值到半去饱和。Gaussian blur kernel 接收**三张纹理**：`inTexture`（`access::read`）、`outTexture`（`access::write`）和 `weights`（`access::read` 的 `R32Float` 查找表），双重循环 `for(j) for(i)` 读权重与邻域像素做加权求和——**没有利用可分离性**，所以每像素是 `N²` 次采样。host 侧用 `[MTLComputeCommandEncoder dispatchThreadgroups:threadsPerThreadgroup:]` 提交一个 2D 的 threadgroup grid；kernel 里通过 `[[thread_position_in_grid]]` 拿到当前像素坐标 `gid`。UI 层面用 `dispatch_async` + 一个原子 `jobIndex` 做去抖——slider 高频回调时只执行最新那次任务，中间的过期任务自动丢弃。评论区密度非常高，涵盖**threadgroup 尺寸不整除导致边缘丢失**（Philip G 补丁）、**非一致 threadgroup 的替代方案**（A11 之后 `dispatchThreads:threadsPerThreadgroup:`）、**不能对 32-bit float / int texture 做 write 操作**、**把 filtered texture 转回 UIImage 是多余的 CPU 回 roundtrip**（后来 Warren 自己重写了样例直接画 full-screen quad）、以及**把 saturation 滤镜搬到 fragment shader 里从 12fps 回到 60fps** 的性能教训。

## 关键要点

- **Compute kernel 的入口签名三要素**：`texture2d<..., access::read/write>` 参数 + 带 `[[buffer]]` 的 uniform + 带 `[[thread_position_in_grid]]` 的 2D 坐标。
- **`access::read` 和 `access::write` 不能同时用**（2014 年）——输入和输出必须是**两张独立的 texture**，所以 filter 的 internalTexture 模式是必然选择，而不是设计偏好。
- **Threadgroup 分配的对齐陷阱**：`width / tgw` 向下取整会丢边缘；向上取整需要 kernel 内部 bounds check；或者用后来的 `dispatchThreads:threadsPerThreadgroup:`（non-uniform threadgroup）让 Metal 自动处理。
- **权重作为查找纹理传入**：`MTLPixelFormatR32Float` 的单通道 texture 比 buffer 更灵活——半径改变时重建 texture 即可，不用改 pipeline。代价是每次 kernel 调用多一次 texture fetch。
- **Filter chain 的懒求值语义**：dirty 标志 + 取 texture 的 getter → 惰性 dispatch，天然避免无用计算；一个 command queue 内顺序执行又天然保证了上游先于下游，不用 barrier。
- **"能用 fragment shader 就不要用 compute kernel"**：文中 koby 的性能报告是个活教材——saturation 这种 1-to-1 像素映射没必要拉出 compute pipeline，compute 真正的价值是**非 1-to-1 的计算**（直方图、reduction、不规则邻域）。

## 链接到的概念

- [[metal-compute-image-filter]]
- [[metal-api-overview]]
- [[metal-shading-language-basics]]
- [[image-convolution-kernel]]
- [[separable-gaussian-blur]]
- [[warren-moore]]

## 原文

- 链接：https://metalbyexample.com/fundamentals-of-image-processing/
- 本地：`raw/articles/metalbyexample.com/2014-10-14_fundamentals-of-image-processing-in-metal.md`
