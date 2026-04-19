---
tags: [渲染, vulkan, 资源上传, 内存, nabla, staging-buffer]
date: 2026-04-19
sources: 1
---

# 流式 Staging Buffer 纹理上传

入门教程里教的纹理上传是**一图一 staging**：加载图像 → 开一块和图同大的 `HOST_VISIBLE` buffer → record copy → submit → 等 fence。代码短，但在生产里有三个致命缺陷：

1. **每次都要在 GPU 上分配一块新内存**。`HOST_VISIBLE + DEVICE_LOCAL` 的堆在独显上经常只有 256 MB（历史上 PCIe BAR 的限制），并发用户一多就分配失败。即使用 [VulkanMemoryAllocator](https://gpuopen.com/vulkan-memory-allocator/) 之类池化分配器，这块堆也最先耗尽。
2. **不能预估峰值内存**。一张 MEGA 贴图可能一瞬间把 staging 堆占满，邻居线程 / 子系统直接失败。
3. **格式转换要再开一块 CPU 内存**。JPEG 没有 alpha 通道，而 GPU 想要 `B8G8R8A8`——朴素做法是在 CPU 侧再拷一份转好的图，相当于同一张 MEGA 贴图住三份内存。

Erfan Ahmadi 在 Nabla 里给出的"The Good Way"是一整套**固定大小、流式复用、分批提交**的 staging 机制。

## 核心结构：固定环形 staging + 通用地址分配器

开一块**固定大小**（默认 64 MB）的 `HOST_VISIBLE` 且尽量 `DEVICE_LOCAL` 的 buffer，一辈子只开这一次。上面挂一个 `GeneralpurposeAddressAllocator`——本质是 [[linear-allocator|线性 / 通用分配器]]的 GPU 版本，返回 `(offset, size)`。staging buffer 比贴图大或小都无所谓。

每次上传：

```
needed = 本次 submit 里要塞的最大 slab
got    = 向 GPU allocator 申请 min(needed, 剩余空间)
```

拿到一段地址后按优先级尽量多塞：

1. 先试 **array layers**（cubemap 一面一面来、纹理数组一层一层来）
2. 不够就塞 **slices / depth**（3D 贴图一层一层）
3. 还不够塞 **rows**
4. 还不够塞 **block**（压缩格式的最小单元）

塞到装不下为止 → submit 当前 command buffer → 等 fence 释放这段 staging → 继续写下一批。核心实现是 `ImageRegionIterator`，等价于一个"可暂停、可恢复"的 region 游标，和 submit 的生命周期耦合在一起。

## 为什么能"边拷边转格式"

一张 `R8G8B8` 资产要上传为 `B8G8R8A8`，朴素做法会新开一块转换后的 CPU buffer。Nabla 的优化是：**把 GPU 上 mapped staging memory 伪装成一个 `ICPUBuffer`**，再直接对它跑 Convert / Swizzle / Convolution 之类的 image filter。filter 一边拷 texel，一边按目标 `VkFormat` 编码，**不存在"中间转换内存"**。

这套"void\* → ICPUBuffer → VkBuffer → IFile 互相伪装"的玩法，Ahmadi 在文中直接说 Nabla "supports all kinds of abuse like that"——本质上是把 CPU 和 GPU 的资源抽象统一成"一张 recipe + 一块内存"的组合，不关心内存来自哪。

## 顺手对齐到物理设备

一个 Vulkan conformant 的 staging 实现还要照顾：

- `optimalBufferCopyRowPitchAlignment` 和 `optimalBufferCopyOffsetAlignment` —— 物理设备偏好的拷贝对齐
- 目标队列的 `minImageTransferGranularity` —— 决定能不能只拷一小块
- `nonCoherentAtomSize` —— 若 staging 非 coherent，需要手动 flush / invalidate 到这个粒度

这些常量在入门教程里全部被跳过，但只有照顾全了拷贝吞吐才稳。

## 多线程上传与中途 submit 的接口设计

最棘手的工程细节是"在一次上传里可能会插入多次 submit"。Nabla 给出的权衡：

- **不自己创建 command buffer 和 fence**，由用户传进来、用户自己 submit。
- 用户能挂 waitSemaphores / signalSemaphores —— 但在**中途 submit** 里这些信号量必须**只在最后一批**触发，否则语义错乱。
- 一次 waitSemaphore 只应在第一次 submit 里真正 wait，之后要 **nullify**——因为那个等待已经发生过了。

这种"切成多段 submit 但对外表现为一次上传"的接口难点，和 [[gpu-fence-timeline-semaphore|timeline semaphore]] 的语义直接相关——timeline 的值必须线性前进、不能被"内部 submit"污染。

## 相关

- [[linear-allocator]] —— GPU 地址分配器的底座
- [[gpu-fence-timeline-semaphore]] —— 多 submit 间的同步
- [[frames-in-flight]] —— staging 的"每帧一段"节奏
- [[buffer-renaming]] —— 隐式 API 替你做的那部分
- [[d3d12-resource-binding]] —— D3D12 侧的 UploadBuffer 节奏
- [[people/erfan-ahmadi]]

## Sources

- [[sources/erfan-ahmadi-texture-upload-staging]]
