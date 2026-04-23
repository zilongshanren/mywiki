---
tags: [opengl, opengl-es, 2d, instancing, vbo, ui, mobile]
date: 2026-04-19
sources: 1
---

# 画一堆动态 2D 四边形的若干姿势

"画一串位置每帧都变的 2D 四边形"——UI、文本渲染、粒子、2D 游戏——[[ben-supnik]] 2013 年把所有可行路径列成一道菜谱，特别强调**移动端（iPhone GLES 2.0）才是这场权衡真正有意义的地方**。桌面端 OpenGL 已经足够快，大多数情况下"profile 先于优化"比选哪条路径重要。

## 前提：一次 draw call 的 setup 远比一个 quad 昂贵

无论走哪条路，**必须先把所有 quad 合进一个 VBO、指向同一张 texture atlas**。不然别的优化都是徒劳——切 VBO 或切 texture 的 CPU 代价远高于画单个 quad。

有个陷阱值得单独记：**即使只是在同一个 VBO 里改 base pointer**，驱动也得把 vertex format 和指针整套重新校验——`glVertexPointer` 的实际成本远比名字看起来大。所以哪怕只是攒成一个 VBO、一次 draw 画一批，就已经是好几档性能。

## 路线 A：uniform 矩阵栈（朴素，不要用）

每 quad 一次 `glRotate/glTranslate`（或 GL2.0 core 里自己改 current matrix uniform）。问题老调重弹：uniform 改一次等价于一次 draw call 上限 1 个 quad，**uniform state 的重建 + 传输远远贵过 24 次 MAD**——典型的"让 GPU 做点简单活、让驱动做一堆脏活"的颠倒。只有当 quad 很少且单个 quad 里顶点很多（比如几千个）时才值得走这条。

## 路线 B：CPU 预变换，塞进流式 VBO

**扔掉 hardware transform，CPU 直接把顶点变换到屏幕坐标，每帧推整个 VBO**。

- **赢**：一次 draw call、一个 VBO，驱动压力最小。
- **赢**：不依赖 GL 3.x/4.x 扩展——**GLES 2.0 iPhone 的唯一合理路径**。
- **输**：每帧所有顶点都要推——桌面端占 bus，移动端只占 CPU（GPU 共享内存、没 bus）。
- **中性**：既然反正都要推，**UV 坐标每帧动也不罚钱**，给动态 texture atlas 或动画 UV 留了空间。

Supnik 的判断：**GLES 2.0 下这就是最佳路径**。注意和 uniform 路线对比时的账：就算用 hardware transform，push 一个 4x4 uniform 是 16 float，而一个 quad 的 4 vertex × (pos + uv) 也就 16 float——**传输量相当**，但"一次 draw call 一个 quad"的驱动税由前者独吞。

## 路线 C：桌面版的"聪明"路径——压缩 instance + HW instancing

桌面 GL 3.x 下要压 CPU 带宽和驱动时间又不做 CPU transform，路径是：

1. `glVertexAttribDivisor` 标记 instance 属性（per-instance 读一次）。
2. Instance array 存**压缩过的变换**：如果你的变换只是 translate+2D rotate 没有 scale，**一对 2D offset + (sin, cos) 就够**，shader 里拼回矩阵。UV 变换同理可压。
3. Mesh 本身是一个 4-vertex 静态 quad。

Supnik 留了句**诚实的免责**：X-Plane 桌面上根本没有这种 case 重要到要改，所以他**没实测过 2D quad 的 HW instancing 路径**。桌面上 B 路线已经够快。

## 反路线：geometry shader / primitive ID + UBO/TBO

- **GS blow-up**（一个 instance 顶点 → GS 里展开成 4 顶点 quad）：Supnik 直截了当"um, don't"。评论区一位 voxel 工程师确认了半条命：**短 vertex stride 时 GS 确实赢 instancing**，但 stride 一大就翻盘；关键是大多数 voxel 引擎**最终都撞到 fill rate 上限**，vertex 效率的差别进不到关键路径。
- **UBO / TBO 查表替代 attrib divisor**：能做但 YMMV；Supnik 没发现明显赢面。
- **Immediate mode（glVertexAttrib4f 逐 quad push）**：大概能跑赢 uniform 路线，但跑不赢 CPU transform。适合老代码救急。

## 评论区的补充细节

几个读者把实战经验填回来：

- **VBO 更新策略**的黑盒：single / double / triple buffer？ring buffer？`glMapBuffer(Range)` vs `glBufferData` vs `glBufferSubData`？"只有驱动工程师知道"——实测 iPhone4 到 iPad2 范围差异并不大，挑一个能跑 60fps 的就行（参见 [[vbo-double-buffering-orphaning]] 与 [[glbuffersubdata-serialization]]）。
- **CPU vs GPU transform 的取舍**：iOS CPU 1GHz × NEON，PowerVR GPU 约 200MHz——频率差让"offload 到 GPU"未必是净赢。**哪一边空闲就喂哪一边**。
- **interleaved vs separate**：Supnik 强硬站 **interleaved**（pos0, color0, normal0, pos1...）——GPU 宽总线一次取一行，所有分量都是有用的，cache 最优。例外是"一部分 per-frame 变、一部分 static"，那时分 VBO 并用不同 usage hint（[[triangle-strips-vs-indexed-triangles]] 里同理的 index/vertex 拆分逻辑）。
- **Instruments 的 CPU 侧信号**：当你走上驱动不喜欢的路时，`glDrawXXX` call stack 下会冒出一堆"吓人名字"——这是验证路线是否合适的最强靠谱信号。

## 和 BrickSmith 的对比

Supnik 同期在 [[bricksmith-instancing-pipeline]] 里走的是桌面版 HW instancing（C 路线），因为 BrickSmith 的 mesh 足够大、instance 数足够多；而 iOS 上的 2D UI 从一开始就走 B 路线。**同一个作者把"每 quad 顶点少、每 quad 变化快"和"每 mesh 顶点多、可批量复用"分到两个 rendering 架构**——这是看场景画表的经典样本。

## 相关

- [[ben-supnik]]
- [[bricksmith-instancing-pipeline]]
- [[vbo-double-buffering-orphaning]]
- [[glbuffersubdata-serialization]]
- [[agp-vs-vram-streaming]]
- [[opengl-pinned-memory-vbo-streaming]]
- [[triangle-strips-vs-indexed-triangles]]
- [[sprite-batch-instance-draw]]

## Sources

- [[sources/supnik-streaming-quads]]
