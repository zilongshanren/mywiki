---
tags: [渲染, metal, apple, core-animation, swapchain]
date: 2026-04-14
sources: 2
---

# CAMetalLayer 与 Drawable（Metal 的 swapchain）

**`CAMetalLayer`** 是 Core Animation 提供的一种特殊图层，作为 [[metal-api-overview|Metal]] 与 iOS / macOS UI 系统之间的胶水。它扮演的角色等价于 OpenGL 里的 default framebuffer、D3D / Vulkan 里的 swapchain：**帮 app 拿到「当前帧要往哪张 texture 里画」的引用，并在画完后把它交还给窗口系统去上屏**。[[warren-moore|Warren Moore]] 在 *Up and Running with Metal, Part 1* 里用这一个对象把 UIKit、Core Animation、Metal 三条链路首尾相接。

## 为什么需要一种特殊的 layer

iOS 上任何 `UIView` 的可见内容都**来自它背后的 `CALayer`**。要让一个普通 UIView 承载 Metal 绘制结果，有两个 idiom：

1. 在 `UIView` 子类里覆写 `+layerClass`，返回 `[CAMetalLayer class]`——Warren 的示例采用此法。
2. 直接持有一个 `CAMetalLayer` 作为自有子层。

无论哪种，这个 layer 必须被告知**两件事**：

```objc
_metalLayer.device      = MTLCreateSystemDefaultDevice();
_metalLayer.pixelFormat = MTLPixelFormatBGRA8Unorm;
```

- **`device`**：哪颗 GPU 负责往这张 layer 里写——没有它，后续从 layer 拿到的 texture 就没法被任何 pipeline state 使用。
- **`pixelFormat`**：颜色通道顺序 / 位宽。`BGRA8Unorm` 是 iOS 原生的默认选项。

## 一次 drawable 的借还

每一帧的开头，app 向 layer 问要一个**可绘制对象**：

```objc
id<CAMetalDrawable> drawable = [self.metalLayer nextDrawable];
id<MTLTexture>      texture  = drawable.texture;
```

`CAMetalDrawable` 协议几乎就是「一张 texture + 一个 present 钩子」的轻包装：

- `drawable.texture` 是这一帧要被当作 framebuffer 的 2D texture
- 画完之后调用 `[commandBuffer presentDrawable:drawable]` 告诉 Core Animation：「这帧我画完了，准备上屏」

然后 `[commandBuffer commit]` 把整条 command buffer 推给 GPU。GPU 执行完后，Core Animation **把这张 texture 的内容合成到屏幕上**——注意是**合成**，所以它会像任何 `CALayer` 一样参与窗口系统的层级合成、圆角、旋转、动画。这是 iOS swapchain 比桌面平台「深」的地方。

`nextDrawable` 背后有一个小的 drawable 环形池。如果上一帧还没显示完，它会阻塞直到有一张可用——这是 Metal app 的天然帧节流点。

## DrawableSize 与 Retina 踩坑

评论区最高频的问题是：**画面模糊** 或者 **只占屏幕四分之一**。原因是 `CAMetalLayer` 的 `drawableSize`（以物理像素为单位）**不会**自动跟 view 的 point-size 联动；要手动设置：

```objc
- (void)setFrame:(CGRect)frame {
    [super setFrame:frame];
    CGFloat scale = self.window ? self.window.screen.scale
                                 : UIScreen.mainScreen.scale;
    CGSize size = self.bounds.size;
    size.width  *= scale;
    size.height *= scale;
    self.metalLayer.drawableSize = size;
}
```

这件小事暴露了 `CAMetalLayer` 的一个本质：**drawable 是像素级的底层存储，而 layer 的 frame 是 point 级的布局单位**。API 故意不自动桥接，留给你去选到底按哪个分辨率渲染——这对 dynamic resolution scaling 反而是好事。

## macOS 上的 NSView 差异

macOS 上 `NSView` **默认不是 layer-backed** 的。Warren 在评论里回答过：要先 `setWantsLayer:YES`，然后在 `makeBackingLayer` 里返回 `CAMetalLayer`——`+layerClass` 的 iOS 模式在 macOS 上不通。

## 和「swapchain」的等价性

把几个平台的术语对齐一下会更清楚：

| 平台 | swapchain 对象 | 取帧 | 提交 |
|---|---|---|---|
| Metal (iOS) | `CAMetalLayer` | `nextDrawable` | `presentDrawable:` |
| D3D12 | `IDXGISwapChain` | `GetCurrentBackBufferIndex` | `Present(...)` |
| Vulkan | `VkSwapchainKHR` | `vkAcquireNextImageKHR` | `vkQueuePresentKHR` |

Metal 的版本把 swapchain 藏进了 Core Animation——好处是**UI 合成免费**，坏处是 drawable 生命周期与 CA 的实现细节绑定在一起（比如 `framebufferOnly` 默认为 YES，影响你能否把 drawable.texture 当作普通纹理采样）。

## 相关

- [[metal-api-overview]]
- [[metal-shading-language-basics]]
- [[smooth-window-resize]] —— 桌面 swapchain 与 WM 的同步话题
- [[gpu-fence-timeline-semaphore]]
- [[rendering-pipeline]]
- [[warren-moore]]

## Sources

- [[sources/metalbyexample-up-and-running-1]]
- [[sources/metalbyexample-up-and-running-2]]
