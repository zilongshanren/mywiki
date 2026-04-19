---
tags: [unity, urp, shader-graph, 后处理, fullscreen]
date: 2026-04-19
sources: 1
---

# URP Fullscreen Shader Graph

Unity 2022 之前，URP 的后处理扩展点基本不开放——自定义全屏效果必须手写 `ScriptableRendererFeature` + HLSL shader（见 [[blit-render-feature]]）。Unity 2022 加入的 **Fullscreen Shader Graph** + **Full Screen Pass Renderer Feature** 两个东西填上了这个缺口，让后处理可以**纯用 Shader Graph 搭**。Ilett 的 Shader Graph Basics Part 12 给出最小教程。

## 创建路径和 Graph Settings 差异

*Create → Shader Graph → URP → Fullscreen Shader Graph*。和 Lit / Unlit graph 比，Fullscreen graph 的区别：

- **Graph Settings 里多了 Fullscreen 专用选项**（虽然新手教程里用不上）；
- **节点面板多了 `URP Sample Buffer` 节点**（Lit/Unlit graph 用不了这个节点）；
- **支持 Stencil 块**（Lit/Unlit graph 不支持 stencil 设置，这也是 holofoil 卡不得不用 HLSL mask 的原因）；
- **preview 不可用**——Fullscreen graph 的 preview 只能显示空白，得在 Scene View 里看实际效果，开发时有点不友好。

## `URP Sample Buffer` 取数据

这是 Fullscreen graph 的核心采样节点，底部 *Source* 下拉决定读哪张屏幕纹理：

- **Blit Source** —— 当前 **正在被处理的屏幕颜色**。关键区别：这个 source **链式变化**。如果渲染器里挂了多个 Full Screen Pass，后一个 pass 的 `Blit Source` 就是前一个 pass 的输出——这让后处理可以流式叠加。
- **Normal World Space** —— 屏幕法线缓冲，做 outline、lighting 后处理常用。
- **Motion Vectors** —— 运动向量，TAA、运动模糊用。

还有一个 `Scene Color` 节点**不要用**——它是渲染主 pass 之前被 snap 的那张屏幕，不会拿到同一帧内之前的后处理结果，想串联后处理链用 `URP Sample Buffer` / Blit Source 才对。深度信息可以用 `Scene Depth` 节点（这个节点本身在 Lit/Unlit graph 里也存在）。

## 挂到 Renderer

有了 graph 之后：

1. 用这个 graph 创建 Material；
2. 在 URP Renderer Data 上 *Add Renderer Feature → Full Screen Pass*；
3. 把 Material 拖进 feature 的 Pass Material 字段；
4. *Requirements* 里勾上 *Color*（对颜色采样都需要），读法线时加 *Normal*；
5. （可选）起个名字，便于多 feature 区分。

默认 Full Screen Pass 挂上来时会显示一个"颜色反转"效果证明 feature 在工作，换成自己的 material 就生效。多个 feature 按列表顺序串起来——灰度→outline→bloom 可以纯配置堆出来。

## 两个教学例子

Ilett 给出两个极简 graph 作为入门：

- **灰度滤镜**：`URP Sample Buffer(Blit Source)` → `Dot Product` with `(0.212, 0.715, 0.072)` → `Base Color`。这三个系数是 **Rec.709 luminance** 权重（人眼对绿最敏感、蓝最弱），和 [[sobel-edge-detection]] 里 Luminance 函数用的同一套。
- **Outline（color + normal 双梯度）**：
  1. `Screen`.reciprocal 得到 1 像素的 UV 步长；
  2. 四个偏移向量 (left/right/up/down)，各自接 `Tiling And Offset` 到 `Screen Position`；
  3. 四个 `URP Sample Buffer(Blit Source)` 采样邻居；
  4. 水平差 = right − left，垂直差 = up − down；
  5. `Dot(v, v)` 得到平方模长（省一次 sqrt——阈值可以放到平方空间）；
  6. 水平² + 垂直² → `Step(colorThreshold)` → 颜色梯度 0/1；
  7. 把整套复制一份改成 `Normal World Space` source + `normalThreshold` → 法线梯度 0/1；
  8. 两种梯度相加输入 `Lerp(originalColor, outlineColor, t)` → `Base Color`。

这种"平方模长 + Step 阈值"避开 sqrt 的 trick 是 image processing 常见套路——见 [[sobel-edge-detection]] 里 3x3 Sobel 同样的省 sqrt。

## 为什么不总用这条路

Fullscreen Graph 的代价是**一切逻辑走节点图**，对熟练 HLSL 的人来说比手写更慢（节点展开出的代码是保守编译器结果）。真正昂贵或需要精确 register 分配的效果仍建议走 [[blit-render-feature|自己写 ScriptableRenderPass + HLSL]]；但对非引擎工程师、艺术家可编程范围、原型迭代，Fullscreen Graph 的门槛低得多。

## 相关

- [[blit-render-feature]] —— 老的自定义后处理路径
- [[urp-volume-post-processing]]
- [[sobel-edge-detection]]
- [[depth-texture-silhouette]]
- [[shader-graph-custom-function-hlsl]]

## Sources

- [[sources/danielilett-shader-graph-post-processing]]
