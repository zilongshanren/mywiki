---
tags: [渲染, 次表面散射, 深度, alpha混合, 单pass技巧]
date: 2026-04-14
sources: 1
---

# 双深度缓冲厚度估计（Dual Depth Buffer Thickness）

[[fast-translucency-wraplight|Barré-Brisebois 的假 SSS]] 需要一个「物体厚度」输入来调节背光强度。原论文建议**离线**把厚度烘焙成纹理或顶点属性——简单但静态，无法处理流体、头发、烟雾这类动态体积。一个自然的动态替代方案是跑两次几何渲染：一次只写背面深度、一次只写正面深度，然后像素相减。能用，但要提交两遍几何。

**Dual depth buffer** 是 Christopher Oat 与 Thorsten Scheuermann 在 *ShaderX6* 里给出的 **单 pass** 方案。核心思路一行就能说清：**关掉 cull、开 `Min` 混合，在 R 通道写 `depth`，在 G 通道写 `1 - depth`，厚度 = `(1 - G) - R`**。

## 为什么 Min 混合能同时求两个极值

GPU 的固定功能混合里，`Min` 操作把 source 和 destination 逐通道取最小值。配合**关闭背面剔除**，一个物体的正面和背面像素都会写入同一个目标像素：
- **R 通道** 用 `Min` 收敛到所有覆盖它的 fragment 中**最小的** depth——也就是**最近的正面**。
- **G 通道** 因为写的是 `1 - depth`，`Min` 反而保留了**最大的 depth**——也就是**最远的背面**。

对同一像素读出来后：`maxDepth - minDepth = (1 - G) - R`，这就是像素处物体沿视线的**厚度**。一整件事在一个 draw call、一个 render target 里搞定。

depth 可以走线性、也可以走透视除法后的 `z/w`。后者的厚度会随观察距离变化——既可能是 feature 也可能是 bug。

## 复杂实心物体上的失效

对于**体积模糊**的物体——雾、毛发、体积粒子——这套方法工作得很漂亮。但对**有复杂内部层次**的实心物体（典型例子：一个身前站了几片叶子的雕像），它会**过估计厚度**：从相机视角看，叶片的正面是最近的，雕像的背面是最远的，中间的雕像身体被当成连续实体，叶子「穿透」了雕像。在背光透射的假 SSS 里，这种过估计表现为叶子的位置在雕像身上变暗——一个不该出现的阴影洞。

## Front/Back 分流的改法

Kostas 的优化是**区分**正面与背面，分别写入不同通道：

```glsl
if (frontfacing) return float4(depth, 1.0, 0, 1);
else             return float4(1.0,   depth, 0, 1);
```

混合依旧是 `Min`：
- **R 通道**只会被正面写入（背面写的是 `1.0`，比任何合法 depth 都大），所以 R 保留**最近正面**深度。
- **G 通道**反过来，只会被背面写入，Min 保留**最近的背面**深度——注意是「最近」而不是「最远」，这正是关键区别。

厚度 = `G - R` = **沿视线第一段正实体的厚度**。结果是叶片不再影响雕像上的雕像像素（因为雕像像素的正面是雕像自己，叶片没写到它的 R；背面也是雕像自己，叶片没写到它的 G），阴影洞消失了。

代价是你丢掉了「跨越多段实体的累加厚度」——也就是说这个版本假设物体是「单段实心」的，对于多层透明体（玻璃瓶里装水里浮冰）依然会低估。工程上是一笔值得的 trade：Barré-Brisebois 的假 SSS 本来也只用到厚度的第一段，精细分层不是它的目标。

## 相关

- [[fast-translucency-wraplight]] — Barré-Brisebois 假 SSS 的厚度消费者
- [[alpha-blending]] — Min 也是一种 blend operation
- [[z-buffer]]
- [[early-z-late-z]]
- [[kostas-anagnostou]]

## Sources

- [[sources/interplay-dual-depth-thickness]]
