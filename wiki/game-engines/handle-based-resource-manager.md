---
tags: [资源管理, 引擎架构, 句柄, 内存池, aposd]
date: 2026-04-14
sources: 1
---

# 基于句柄的资源管理器

这是 [[marco-giordano]] 在自研 Vulkan/DX12 引擎里长期使用的资源系统范式。它和 [[resource-system-design]] 讨论的"Unity RAII / Addressables"是同一个问题——"怎么在引擎里管一张纹理、一个 mesh、一个着色器"——但走的是完全不同的一条路：**不返回指针，不返回带引用计数的智能对象，只返回一个 32-bit 的不透明句柄**，所有操作通过 manager + handle 的组合完成。

## 范式的两条支柱

1. **句柄是不透明、可平凡复制的小整数**，而不是资源指针。拷贝它不涉及所有权，也不会触发引用计数更新。
2. **所有资源逻辑都集中在对应类型的 manager 里**（TextureManager、BufferManager、ShaderManager…），不 encapsulate 在资源对象内部。资源对象是被动的数据结构。

## 句柄的内部结构

Marco 的典型句柄就是一个简单结构：

```cpp
struct TextureHandle final {
    uint32_t handle;
    bool isHandleValid() const { return handle != 0; }
};
```

32 位里的分段是 **低 16 位索引 + 高 16 位 magic number**。索引直接作为 manager 内部 memory pool 的 slot 下标，magic number 用作版本验证。他是用模板工具函数做掩码 + 移位提取的，也可以换 C 的 bitfield，但 Marco 十几年前就自己写了，一直没动。

```cpp
template <typename T>
inline uint32_t getIndexFromHandle(const T h) {
    constexpr uint32_t standardIndexMask = (1 << 16) - 1;
    return h.handle & standardIndexMask;
}
```

思路来自《Game Programming Gems》里的一章，后来又被 Andre Weissflog 的 ["Handles are the better pointers"](https://floooh.github.io/2018/06/17/handles-vs-pointers.html) 重新 crystalize 成完整的设计哲学。

## Manager 的数据布局

以 Vulkan 纹理为例，manager 内部存储的 `VkTexture2D` 大致是：

```cpp
struct VkTexture2D {
    const char *name;
    VkImage image;
    VkDeviceMemory deviceMemory;
    VkImageView view;
    VkDescriptorImageInfo srv;
    VkImageLayout imageLayout;
    VkFormat format;
    uint32_t width : 16;
    uint32_t height : 16;
    uint32_t mipLevels : 16;
    uint32_t magicNumber : 16;   // 这里！
    // ...
};
```

关键字段是那个 `magicNumber` —— **资源数据自己也存了一份 magic**，和句柄里那份要对得上。

加载一张纹理：

```cpp
TextureHandle handle = textureManager->load(pathOnDisk);
// ...
textureManager->bindTexture(handle, slot);
```

bind 的时候：

```cpp
VkFormat getTextureFormat(const TextureHandle &h) const {
    assertMagicNumber(h);                            // debug 期校验
    const uint32_t idx = getIndexFromHandle(h);
    const VkTexture2D &data = m_texturePool.getConstRef(idx);
    return data.format;
};
```

`assertMagicNumber` 在 release 下默认会被编译没，也可以强制保留。

## 为什么不用 unordered_map

最朴素的"句柄 → 数据"映射可以走 `std::unordered_map<uint32_t, VkTexture2D>`。Marco 明确反对：hash + 碰撞处理在热路径上太贵。他改用 **自写的定容量 memory pool**，句柄里的索引就是池中 slot 下标，读取是 O(1) 的直接寻址。这种取舍和 [[linear-allocator]] 的精神一致——放弃通用性换确定性能。

## Dangling handle 与 magic number

Memory pool 的 slot 会被回收重用，这就产生"悬垂句柄"的经典问题：句柄指向 slot 10，但原来的 albedo 已经被 free，现在那里躺着一张 roughness。magic number 就是解决这个的：每创建一个资源就把 manager 内部的计数器 +1，把当时的计数写进资源自己的 `magicNumber` 字段，**同时**也写进返回给用户的句柄高 16 位。`assertMagicNumber` 就是比较这两个数是否相同。

计数器 16 位，理论上会 wrap around 后发生 magic 碰撞，Marco 的判断是"概率足够低，不值得处理；如果担心就扩到 32/24 位"。

## 为什么这套比 OOP + 指针好

Marco 列了几点（和 [[information-hiding|信息隐藏]] / [[deep-modules|深模块]] 的精神一致）：

- **所有权不再是问题**：句柄本身不拥有资源，随便拷贝不漏内存，释放只通过 manager 做（显式或在退出时批量）。
- **分配集中**：所有同类资源都在同一个 manager / 同一个 pool 里，改一次池的实现（换成 stack allocator、环形缓冲、延迟释放…）整个引擎的纹理分配策略都换了，调用方完全无感。这正是 [[information-hiding]] 的价值——资源是怎么被存的，外面不该知道。
- **API 抽象的主要工具**：Marco 的引擎同时跑 DX12 和 Vulkan，两个后端返回的都是 `TextureHandle`，底层结构体（`VkTexture2D` / `D3D12Texture2D`）完全不需要暴露给调用方。句柄天然是一个 handle-based BRI（backend-agnostic resource interface）。
- **实现成本不高**：和 OOP 写法相比代码量相近，甚至更少（没有 ctor/dtor/拷贝/移动 的一大套）。

相较之下，[[resource-system-design]] 讨论的 Unity `Addressables` / `AssetReference` 也是同样的问题、同样的思路——**把资源的生命周期与表示全部藏到系统后面，上层只拿一个轻量句柄**。两者在抽象层级上是对应的，区别只在实现语言与运行时。

## 相关
- [[resource-system-design]] —— Unity / C# 侧对同一问题的 RAII / Addressables 回答
- [[information-hiding]] / [[deep-modules]] —— 句柄 + manager 是这两个原则在引擎里最干净的体现
- [[linear-allocator]] —— 池式存储的基础构件
- [[game-engine-vfs]] —— 资源管线的上游（文件系统抽象）
- [[engine-layering]]
- [[id-based-lifetime-with-kill-flag]] — 云风在 skynet 2.0 里用 id + 销毁标记替代 refcount 的变体，哲学一致但面向 actor 并发
- [[id-lookup-table-packed]] — Bitsquid 同思想的三种实现细节与权衡
- [[hot-swap-pointer-patching]] —— Pesce 2011 列出的四种备选方案（指针 patch / GC / 置换表 / 列表扫描），解释为什么工业界没选它们

## Sources

- [[sources/giordi91-handle-resource-management]]
