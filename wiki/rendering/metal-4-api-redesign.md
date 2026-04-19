---
tags: [metal, api, apple, 显式资源管理, 并发]
date: 2026-04-19
sources: 1
---

# Metal 4 API 重塑

Metal 4（2025 / iOS 26 / macOS 26）不是版本号例行跳，而是一次核心 API 的重写。哲学从 **fire-and-forget command buffer + 隐式 residency** 改为 **concurrent by default + 显式资源生命期管理**。新类型统一带 `MTL4` 前缀，旧类型部分保留部分被彻底换掉。[[warren-moore|Warren Moore]] 的 getting-started 教程覆盖了从 Metal 3 光栅管线迁移必须理解的变化。

## 变化速览

| Metal 3 及以前 | Metal 4 |
|---|---|
| `MTLCommandQueue.makeCommandBuffer()` | `MTLDevice.makeCommandBuffer()` + `MTL4CommandAllocator` |
| Command buffer 隐式管理命令内存 | Command allocator **显式**管理，必须池化轮用 |
| Command buffer 保活引用资源 | Command buffer **不保活**——应用负责 |
| 资源 residency 隐式 | 必须走 `MTLResidencySet`（唯一路径） |
| 隐式 argument table（setBuffer/setTexture on encoder） | `MTL4ArgumentTable` 是**显式对象** |
| `MTLFunction` 实例 + device-based 编译 | Function descriptor + `MTL4Compiler` |
| Pipeline 描述符带 depth attachment | 只在 pass descriptor 带 depth |
| Dispatch semaphore 做帧节流 | `MTLSharedEvent` + `signalEvent/waitUntilSignaledValue` |

## Function Descriptor

```swift
let fd = MTL4LibraryFunctionDescriptor()
fd.name = "fragment_main"
fd.library = library

// Specialized（function constants）
let sfd = MTL4SpecializedFunctionDescriptor()
sfd.functionDescriptor = fd
sfd.constantValues = constants
```

## MTL4Compiler 接管编译

```swift
let compilerDesc = MTL4CompilerDescriptor()
let compiler = try device.makeCompiler(descriptor: compilerDesc)
let pipeline = try compiler.makeRenderPipelineState(descriptor: rpDesc)
```

支持 pipeline serialization，启动加速。

## Render pipeline 差异

```swift
let rpDesc = MTL4RenderPipelineDescriptor()
rpDesc.vertexFunctionDescriptor = vfd
rpDesc.fragmentFunctionDescriptor = ffd
rpDesc.colorAttachments[0].pixelFormat = .bgra8Unorm
rpDesc.colorAttachments[0].blendingState = .enabled  // enum 替代 bool
```

Depth attachment 不再在 pipeline descriptor 里指定——pass descriptor 里说。

## Residency Set：唯一 resident 路径

```swift
let rsDesc = MTLResidencySetDescriptor()
rsDesc.initialCapacity = 16
let rs = try device.makeResidencySet(descriptor: rsDesc)
rs.addAllocation(texture)
rs.commit()
commandQueue.addResidencySet(rs)   // 或 commandBuffer.useResidencySet(rs)
```

"resident = 所有已挂载 residency set 的并集"。不挂 residency set = 资源不保证可用。

## Argument Table：显式绑定对象

```swift
let atDesc = MTL4ArgumentTableDescriptor()
atDesc.maxBufferBindCount = 16
atDesc.maxTextureBindCount = 16
let argTable = try device.makeArgumentTable(descriptor: atDesc)

argTable.setTexture(texture.gpuResourceID, index: 0)
argTable.setAddress(buffer.gpuAddress + UInt64(offset), index: 0)

encoder.setArgumentTable(vertexArgTable, stages: .vertex)
encoder.setArgumentTable(fragArgTable, stages: .fragment)
```

- Texture 绑 **64-bit gpuResourceID**
- Buffer 绑 **64-bit gpuAddress**，offset 直接加到 address
- Argument table state 每次 draw 被**拷贝**，不需要池化或 sticky 管理

## Command Allocator：按帧池化

```swift
// 初始化时建一个池子，3~4 个轮用
let allocator = device.makeCommandAllocator()

// 每帧
allocator.reset()
commandBuffer.beginCommandBuffer(allocator: allocator)
// encode...
```

Allocator 在 GPU 执行完前不能复用——要么等 frame fence，要么用 `MTLSharedEvent` 等 N 帧前的工作完。

## 提交和呈现：四步

```swift
commandQueue.waitForDrawable(drawable)
commandQueue.commit([commandBuffer])
commandQueue.signalDrawable(drawable)
drawable.present()
```

## Events 替代 Dispatch Semaphore

```swift
let event = device.makeSharedEvent()
// 帧 N 编码前等 N-3 完
event.wait(untilSignaledValue: N-3, timeoutMS: 1000)
// 帧 N 编码后推进
commandQueue.signalEvent(event, value: N)
```

## 迁移建议

作者和一个评论里的 Godot 开发者都说"Metal 4 是个大迁移"。务实做法：

- 显式生命期 / residency / command memory 管理上升为应用层职责
- 如果现有引擎已经在做 bindless / 手动 hazard tracking，迁移相对自然
- 否则**建议彻底新写 driver 层而不是渐进改**（Godot 4.x 方案）

## 相关

- [[metal-decade-history]]
- [[metal-api-overview]]
- [[bindless-rendering]]
- [[d3d12-resource-binding]]
- [[gpu-hazard-tracking]]
- [[warren-moore]]

## Sources

- [[sources/metalbyexample-metal-4-basics]]
