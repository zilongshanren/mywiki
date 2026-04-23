---
tags: [opengl, instancing, renderer, ldraw, vbo, batching]
date: 2026-04-19
sources: 1
---

# BrickSmith 的新渲染管线：attribute instancing 到 hardware instancing

[[ben-supnik]] 2013 年给开源 LDraw 编辑器 **BrickSmith** 重写了 OpenGL 底层绘制层，是一个结构清晰的真实案例：**如何把 17,000+ 个 lego 砖块每帧推到屏幕上而不炸 draw call**。作为 X-Plane 程序员的他顺手把自家经验翻译成了一个非游戏应用。

## LDraw 数据的特征决定了工程空间

LDraw 格式把模型拆成 push-pop 状态栈 + 基元（line / tri / quad），有两个关键特征：

- **顶点数量才是瓶颈**——LDraw 没有 LOD，lego 砖块按几何精度建模（即使一个 "stud" 只有八角棱柱，一块基础板上也有 1024 个 stud）。
- **颜色继承于栈顶的 "current color"**——一个子零件可能声明"这里涂红色"，也可能声明"填空位"（由上层决定）。

Supnik 在 shader 里用一个小技巧把 current-color 消化掉：**用 RGBA 里 `A=0` + 特殊 RGB 编码表示"从栈里取颜色"**，shader 自己做代换。这样**同一块砖（mesh）不需要按颜色切分**，上层也不用发两批 draw call。

## 三层实例化的演进路径

Supnik 列出了推实例数据的三种方式，逐级替换：

### 1. 朴素：uniform 矩阵

每砖一次 `glPushMatrix/glRotate/glTranslate` → uniform state 变化 → 驱动必须把**整块 uniform buffer**（包括你没动的投影矩阵和光照值）重拷一份给 GPU，途中要么走 PCIe、要么 DMA 进 VRAM。每个 draw call 附带大量驱动工作。**5000 draw call 对实时帧率已经是上限**，但 5000 砖只是一到两个中型 lego 模型——这条路走不通。

### 2. Immediate-mode instancing（attribute instancing）

把 modelview 矩阵塞进**顶点属性**而不是 uniform：`glVertexAttrib4f` 改属性的默认值，走一次 `glDrawArrays` 画一个砖，循环下去。属性是**廉价的 per-vertex default**，切换不走 uniform buffer 重建那条重路径。X-Plane 上测出比 uniform 快 **≈2x**。

### 3. Hardware instancing（攒成一次 draw call）

同样用顶点属性，但用 `glVertexAttribDivisor` 告诉 OpenGL：这些属性**一个 instance 一次** 读，其他顶点属性照常每顶点一次。把一整批砖的 instance 数据（矩阵 + 颜色）打包进一个 VBO，单次 `glDrawArraysInstanced` 画完一整组同款砖。X-Plane 上测出比 attribute instancing 再快 **≈10x**——"超过 10 万个 object 一帧"级别（参见 [[xplane-instancing-2011-numbers]]）。

BrickSmith 的 instance 是 **24 floats**：4x4 矩阵（4 个 vec4 属性）+ RGBA current color + RGBA complement color。

## 为什么 instance buffer 走 STREAM_DRAW

砖 mesh 本身以 `STATIC_DRAW` 驻留 VBO（几乎从不改），但 instance 位置是 `STREAM_DRAW`——因为 BrickSmith 目前每帧重新遍历模型生成砖列表，没有缓存结构（X-Plane 则相反，预计算 object 列表所以用 `STATIC_DRAW`）。100,000 砖 × 24 float = **10 MB/frame**，对现代总线完全够用。注意这份流式 buffer 不用每个 mesh 一份，**全部 instance 合并写进同一条 giant stream buffer**——好处是 map/unmap 一次、少一堆小 VBO（小于一页的 VBO 对驱动是负担，参见 [[vbo-double-buffering-orphaning]]）。

## Drawing dispatch：三桶分流

每帧遍历 scene，draw 请求不立刻执行而是**分桶**：

- **半透明桶**：需要 back-to-front 排序，最后画。CPU 有代价，只对真的有透明的砖做。
- **复杂桶**（texturing、stack 复杂度）：按 part 排序以少切 VBO，但一个砖一个 draw call。
- **简单桶**：合并成 HW instancing，按 part 组织。

这个分桶既体现了 [[alpha-blending-front-to-back]] 的原则，也是早期 render-queue 思路的直接落地。

## 实测：vertex-bound 时代的尽头

新管线在大多数模型上 **≈2x**，CPU 占用从 100% 降到 30-35%——说明瓶颈彻底从 CPU 驱动调用转移到 GPU。但在 39,000 砖（Datsville，~125M 顶点）的极端模型上两者都是 5 fps——此时瓶颈是 **GPU 顶点吞吐本身**（ATI 4870 约 500M vertices/sec，正好吃满）。**没有 LOD 再优化也救不回来**——Supnik 的下一步计划就是 LOD（参见 [[lego-realistic-lighting-brain-dump]] 末尾对这件事的自嘲）。

## 评论区的增量：merged instancing 与 texelFetch 解包

有读者提议**把 mesh 复制 100-1000 份放进同一个 VBO**，用 `gl_InstanceID` + `gl_VertexID` 自己查表、`texelFetch` 从 TBO 解包 8-float 压缩 instance。Supnik 的回应是这套在别的情境有用，但 BrickSmith 的瓶颈是三角形建立（triangle setup），不在 instance 带宽或 draw call 上——548 种唯一砖已经足够大的 batch；试过 TBO vs UBO vs divisor，顶点吞吐基本打平。这呼应了他在 [[xplane-instancing-2011-numbers]] 里给出的**时代基线**：2011-2013 年 instance 数量早已不是瓶颈。

## 相关
- [[ben-supnik]]
- [[xplane-instancing-2011-numbers]]
- [[sprite-batch-instance-draw]]
- [[vbo-double-buffering-orphaning]]
- [[triangle-strips-vs-indexed-triangles]]
- [[alpha-blending-front-to-back]]
- [[draw-call]]
- [[opengl-draw-call-batching-sweet-spot]]
- [[bricksmith-speculative-gpu-occlusion]] —— 2013-08 Supnik 基于本 pipeline 推演的 GPU 遮挡剔除全方案与四条不发车理由

## Sources

- [[sources/supnik-instancing-bricksmith]]
