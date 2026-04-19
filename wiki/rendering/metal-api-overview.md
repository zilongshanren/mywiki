---
tags: [渲染, metal, apple, 图形api, 显式api]
date: 2026-04-14
sources: 5
---

# Metal API 概览（Device / Queue / Buffer / Encoder / Pipeline）

**Metal** 是 Apple 2014 年随 iOS 8 推出的低层图形 + 计算 API，定位与 Vulkan / DirectX 12 同代——用「**显式对象图**」替代老 OpenGL 的「全局 context + 状态机」。[[warren-moore|Warren Moore]] 的 *Up and Running with Metal* 系列用两篇文章就把整条最小渲染链路展开一遍，这一页把其中的核心对象按「生命周期」从长到短串起来。

## 一句话定位

> Metal 是你在 iOS 上能接触到的**最低一层**图形抽象。

但它**仍然是抽象**：如果完全去掉抽象，就不会有 `MTLLibrary` / `MTLCommandEncoder` 这种东西——你会直接往 buffer 里写机器码、直接往环形队列里写 GPU 指令。存在这些对象，说明 Metal 在「硬件寄存器」和「你写的代码」之间仍然留了一层 driver。Warren 在 *The Whats and Wherefores of Metal* 里把这一点讲得非常明白。

## 对象家族

Metal 的公开类型**大量使用 Objective-C 协议**（`id<MTLDevice>`、`id<MTLCommandQueue>` 等）——调用方只看接口，具体实现交给各代 GPU 驱动。

### 长寿对象（app 生命周期，只建一次）

- **`MTLDevice`**：对 GPU 的抽象句柄，通过 `MTLCreateSystemDefaultDevice()` 获取，是所有其它对象的工厂。
- **`MTLCommandQueue`**：命令队列，app 内通常只需一条。
- **`MTLLibrary`**：一组编译后的 shader 函数（见 [[metal-shading-language-basics]]）。默认 library `[device newDefaultLibrary]` 来自 Xcode 编译期打进 app bundle 的 `.metal` 文件。
- **`MTLRenderPipelineState`**：由 `MTLRenderPipelineDescriptor`（vertex function + fragment function + color attachment pixel format）产生，内部包含**编译并链接后的 shader program**——创建很昂贵，应当为每一种 shader 组合只建一次，长期持有。

### 帧生命周期（每帧重建）

- **`MTLCommandBuffer`**：一帧要提交的命令集合，`[queue commandBuffer]`。
- **`MTLRenderCommandEncoder`** / `MTLComputeCommandEncoder` / `MTLBlitCommandEncoder`：把「设 pipeline state / 绑 vertex buffer / 画三角形」这类高层命令**编码成**写进 command buffer 的低层 GPU 指令。调用 `endEncoding` 后方可再开下一个 encoder。
- **`MTLRenderPassDescriptor`**：描述一次 render pass 的 load / store 行为与 clear color、附带 color / depth / stencil attachment。[[hsr-tbdr|Apple GPU 是 TBDR 架构]]，load / store action 在这里尤其重要——决定 tile memory 是否需要 resolve 回 DRAM。

### 资源对象

- **`MTLBuffer`**：无类型字节缓冲，`newBufferWithBytes:length:options:`。与 CPU 共享的内存区域由 `MTLResourceOptions` 决定（Shared / Managed / Private）。
- **`MTLTexture`**：1D/2D/3D 图像，也可以是 slice 数组。framebuffer 其实就是一个 [[cametal-layer-drawable|CAMetalDrawable]] 背后的 2D texture。

### Feature set：按 GPU 家族分层的能力查询

Metal 从 iOS 8 GM 开始引入 `MTLFeatureSet` + `[device supportsFeatureSet:]`，用来区分不同 GPU 家族的能力差异。2014 年枚举只有 `GPUFamily1_v1`（A7）和 `GPUFamily2_v1`（A8）两项，差异集中在两点：A7 的 render pass color attachment 上限是 4、A8 提到 8（意味着 A8 才能开完整的 [[deferred-rendering|deferred G-buffer]]）；A8 新增 [ASTC](https://en.wikipedia.org/wiki/Adaptive_Scalable_Texture_Compression) 纹理压缩支持。多年以后这条 API 路径扩展到了 Apple Silicon 的 `GPUFamily9`，功能分层也远不止当年两条——但设计哲学没变：**问能力而不是问型号**，让 app 对未来硬件自然兼容。

Warren 文里提到一个调试小细节：`MTLCreateDefaultSystemDevice` 在 debugger 下返回 `MTLDebugDevice`（带参数 validation 的 wrapper），脱离 debugger 才返回设备特定驱动类如 `AGXG3Device` / `AGXG4PDevice`——这就是 Metal validation 层的实现机制。

## 最小一帧的 7 步骤

1. 问 `CAMetalLayer` 要一个 `CAMetalDrawable`，从中拿到 `texture`（见 [[cametal-layer-drawable]]）
2. 填一个 `MTLRenderPassDescriptor`，把 `colorAttachments[0].texture` 指向这张 texture，选 `loadAction=Clear` / `storeAction=Store` / `clearColor=...`
3. `commandBuffer = [queue commandBuffer]`
4. `encoder = [commandBuffer renderCommandEncoderWithDescriptor:passDescriptor]`
5. `[encoder setRenderPipelineState:...]`，`setVertexBuffer:offset:atIndex:`，`drawPrimitives:...`
6. `[encoder endEncoding]`
7. `[commandBuffer presentDrawable:drawable]; [commandBuffer commit]`

这 7 步就是 Warren 文章里的全部代码，也是所有 Metal 应用的骨架。

## 与 OpenGL / D3D12 的对比

- 相比 **OpenGL ES**：没有全局 context，pipeline state 是显式的 **immutable 对象**而不是「改一个 enum」；[[draw-call]] 在 CPU 侧的 driver overhead 因此大幅降低。
- 相比 **DirectX 12**（见 [[d3d12-resource-binding]]）：Metal 因为只跑在 Apple 自家 SoC 上，可以假设 CPU / GPU 共享内存，省掉 D3D12 的 upload heap / descriptor heap 这套显式同步，API 表面更小。代价是**Metal 的很多模式当搬到 Mac 分立 GPU 上时就失去了部分优势**——这是 Warren 在 2014 年就正确预言的一件事。
- Metal 的**命令编码器三件套**（queue / buffer / encoder）是显式 API 的共通结构，D3D12 的 CommandQueue / CommandList / CommandList Recording、Vulkan 的 VkQueue / VkCommandBuffer / vkCmd\* 全都是一回事。

## 为什么叫「抽象的下界」而不是「没有抽象」

Warren 反复强调：Metal 是**你能选的最低一层**，而非没有抽象。好处是你不再被全局状态机的「怎么 shader 编译失败了」折磨；坏处是你**必须**自己管 pipeline state 的组合爆炸、自己管资源 lifetime、自己管 drawable 的同步。换来的是可预测的 CPU 开销与 iOS 设备上真正能跑满的 GPU 利用率。

## 相关
- [[metal-shading-language-basics]]
- [[cametal-layer-drawable]]
- [[rendering-api-depth]] —— 接口深浅维度上，Metal 和 D3D12 都是浅接口
- [[d3d12-resource-binding]]
- [[hsr-tbdr]]
- [[tbdr-vs-imr]]
- [[draw-call]]
- [[rendering-pipeline]]
- [[warren-moore]]
- [[metal-decade-history]] —— 十年版本演进回顾
- [[metal-4-api-redesign]] —— Metal 4 的 API 重塑（显式 residency + command allocator + argument table）
- [[hdr-video-edr-metal]] —— AVFoundation + Metal HDR 视频管线
- [[slug-gpu-glyph-rendering]] —— 2026 年 Slug 算法在 Metal 上的实现

## Sources

- [[sources/metalbyexample-up-and-running-1]]
- [[sources/metalbyexample-up-and-running-2]]
- [[sources/metalbyexample-whats-and-wherefores]]
- [[sources/metalbyexample-up-and-running-3]]
- [[sources/metalbyexample-feature-sets]]
