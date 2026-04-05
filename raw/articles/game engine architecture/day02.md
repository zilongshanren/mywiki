# Day 2 · 引擎演化史 — 从 id Tech 到 Unreal Engine 5

> 基于 Jason Gregory《Game Engine Architecture》第3版 Ch1.3-1.5

---

## 历史是最好的架构师

1993 年，id Software 发布了 Doom。这个游戏改变了整个游戏产业，但更深远的影响不在于游戏本身，而在于一个商业决策：John Carmack 决定把引擎代码授权给其他工作室使用。**游戏引擎作为独立商品，从这里正式诞生。**

Gregory 在 §1.5 回顾这段历史时写道：

> "The first 3D first-person shooter (FPS) game is generally accepted to be Castle Wolfenstein 3D (1992). Written by id Software of Texas for the PC platform, this game led the game industry in a new and exciting direction. id Software went on to create Doom, Quake, Quake II and Quake III. All of these engines are very similar in architecture, and I will refer to them as the Quake family of engines."

但历史的真正转折点不是 Wolfenstein 3D，而是 **Quake（1996）**——第一个真正意义上可授权的 3D 引擎。id Software 不只卖游戏，还把引擎代码卖给其他开发者。Ritual Entertainment 用它做了 Sin，Valve 用它的精神后代做了 Half-Life，Half-Life 的引擎又演变出了 Counter-Strike。

这条技术谱系图，是理解今天整个游戏引擎市场的起点。

理解这段历史，你就理解了为什么今天 Unity 和 Unreal 是两种截然不同的产品——它们从不同的历史脉络中演化出来，携带着不同的技术"DNA"。

---

## 第一代：BSP 引擎时代（1992-1999）

id Tech 1（Doom 引擎）和 id Tech 2（Quake 引擎）代表了第一代 3D 引擎的技术范式。核心技术是 **BSP Tree（Binary Space Partitioning，二叉空间划分树）**。

### BSP Tree 是什么

BSP Tree 的核心思想是把三维场景划分成一系列凸多边形区域，用二叉树组织，从而在 O(log n) 的时间复杂度内解决"摄像机能看到什么"这个问题。

工作原理：

```
场景几何 → 选择一个分割平面 → 把场景分成前面和后面两部分
                                    ↓
                            对每个部分继续递归分割
                                    ↓
                       直到每个节点只包含一个凸多边形区域

渲染时（从摄像机位置出发）：
  if 摄像机在分割平面的前面:
    先渲染后面的子树（远离摄像机）
    然后渲染当前节点
    再渲染前面的子树（靠近摄像机）
  else:
    顺序反过来
```

这个算法的精妙之处在于：它天然保证了从后往前的渲染顺序，避免了 Z-buffer 在当时硬件性能下的开销，同时实现了高效的可见性剔除。

### BSP 的天然局限

BSP 对**室内封闭场景**效果极好。Quake 的地图是走廊、房间、地下基地——这不是设计选择，是**技术约束**。

BSP Tree 在室外开阔场景上完全失效，原因如下：

```
室外场景的问题：
1. 地形是无限延伸的，无法用少量分割平面表达
2. 天空没有"背面"，无法剔除
3. 视距远，BSP 无法有效减少需要渲染的多边形数量
4. 动态物体（角色、车辆）破坏了 BSP 的静态假设
```

这就是为什么第一代 3D FPS 游戏都是室内场景——技术决定了游戏类型，而不是反过来。

Gregory 特别推荐了一件事：

> "If you own the Quake and/or Quake II games, you can actually build the code using Microsoft Visual Studio and run the game under the debugger using the real game assets from the disk. This can be incredibly instructive. You can set breakpoints, run the game and then analyze how the engine actually works by stepping through the code. I highly recommend downloading one or both of these engines and analyzing the source code in this manner."

Quake 源码至今仍是学习引擎开发的最佳教材之一。代码量小、逻辑清晰、没有过度抽象。对于想理解"引擎是怎么工作的"的工程师，这是最直接的路径。

---

## 第二代：Portal 引擎时代（1998-2006）

Unreal Engine 1（1998）和 Quake III（1999）开始了第二个技术时代。这一代引擎的核心突破：**放弃纯 BSP，引入 Portal 系统 + 可见性预计算（PVS，Potentially Visible Set）**。

### Portal + PVS 系统

Portal 系统的思路更接近人类的直觉：把场景划分为"房间"（Sector），房间之间的开口是"门洞"（Portal）。

预计算阶段：
- 从每个房间的每一点出发，通过所有可能的 Portal 序列，计算能看到哪些其他房间
- 把这个可见性信息存储为 PVS（Potentially Visible Set）

运行时：
```
1. 找到摄像机所在的房间（O(1)，简单空间查询）
2. 查 PVS 表：这个房间的 PVS 包含哪些其他房间？（O(1) 查表）
3. 只把 PVS 中房间的几何发送给 GPU
4. 结果：GPU 渲染的几何量大幅减少
```

Portal 系统相比纯 BSP 有几个关键优势：
1. 更适合复杂的室内场景（多层楼、不规则房间）
2. PVS 预计算可以在离线阶段完成，不影响运行时性能
3. 与 BSP 组合使用时（Quake III 用的就是 BSP + PVS 混合），效果更好

### Unreal Engine 1 的真正革命：工具链

但 Unreal Engine 1 真正的创新不在渲染技术，而在**工具链**。

Gregory 这样评价 Unreal：

> "The Unreal Engine has become known for its extensive feature set and cohesive, easy-to-use tools."

Unreal Engine 1 是第一个提供完整关卡编辑器（UnrealEd）的商业引擎。关卡设计师不需要写代码，直接在编辑器里：
- 拼接刷子（BSP Brush）构建几何
- 放置 Actor（可交互实体）
- 编写 UnrealScript（内置脚本语言）触发逻辑
- 实时预览

这让游戏内容生产速度提升了一个数量级。用 Unreal Engine 1 开发的游戏：Unreal Tournament、Deus Ex、Medal of Honor、Lineage……

Unity 的成功，很大程度上继承了这个思路：**工具比引擎运行时性能更重要**。一个工具友好的引擎，能让 5 人团队做出 50 人团队才能做出的游戏。

---

## 第三代：可编程 Shader 时代（2004-2012）

**Shader Model 2.0 的出现（DirectX 9，2002）改变了一切。**

在此之前，GPU 渲染管线是固定功能（Fixed Function Pipeline）。你只能打开/关闭光照、选择混合模式，仅此而已。GPU 的每一步计算都是固定的，程序员无法干预。

Shader Model 2.0 让开发者可以**用代码控制 GPU 的每一个像素**。这是一个质的飞跃。

### 这个时代的技术爆炸

可编程 Shader 催生了一系列之前根本不可能实现的渲染技术：

**法线贴图（Normal Mapping）**：在片元着色器中用法线贴图欺骗光照计算，用低多边形模型表现高细节表面。Doom 3（2004）是第一批大规模使用法线贴图的游戏。

**HDR 渲染（High Dynamic Range Rendering）**：把光照计算在高精度浮点缓冲中进行，最后用 Tone Mapping 映射到屏幕显示范围。解决了光照曝光不自然的问题。Far Cry（2004）是 HDR 渲染的早期典范。

**Shadow Mapping**：在 Shader 中实现阴影——把场景从光源视角渲染到深度纹理，然后在正常渲染时查询这个深度纹理判断是否在阴影中。这比之前的模拟阴影（Blob Shadow）精确得多。

**延迟渲染（Deferred Rendering）**：先把场景的几何信息（位置、法线、材质参数）输出到 G-Buffer，然后统一进行光照计算。这样就能支持数十到数百个动态光源，而不是前向渲染下的 4-8 个。

这个时代的代表是 **Unreal Engine 3（2006）**。

### UE3 的 Material Editor：Shader 的民主化

UE3 引入了 Material Editor——一个节点式可视化 Shader 编辑界面。美术人员不需要写 HLSL 代码，通过连接节点就能创建复杂的材质效果。

这是今天 Unity Shader Graph 和 Unreal Material Blueprint 的直接先祖。

从工程角度理解这个创新：

```
传统工作流：
美术提需求 → 程序员写 HLSL Shader → 编译 → 迭代
（每次修改需要程序员介入，迭代速度极慢）

Material Editor 工作流：
美术直接在节点图中调整 → 即时预览 → 无需程序员介入
（迭代速度提升 10x，同时解放程序员）
```

Unity 的 Shader Graph（2018 年引入 SRP 后）正是受此启发。但有趣的是：Unity 一直到 2018 年才有这个功能，而 Unreal 在 2006 年就已经做到了。这 12 年的差距，体现了两家公司不同的优先级排序。

---

## 第四代：实时 GI 时代（2012-至今）

第三代引擎的核心局限：**全局光照必须预计算（光照烘焙，Lightmap Baking）**。

烘焙的代价极高：
- 场景中所有光源必须是静态的（动态光源不参与 GI）
- 大型场景烘焙时间以小时甚至天计算
- 改动一盏灯，需要全图重新烘焙
- 动态物体（角色）无法正确接受静态 GI

这个局限制约了游戏设计——你无法做动态昼夜系统，无法做动态光源驱动的 GI 效果，动态角色永远和静态场景有割裂感。

### Unreal Engine 4（2014-）：渐进式突破

UE4 没有彻底解决动态 GI，但推进了几个关键技术：

**Distance Field Soft Shadows**：用 Mesh Distance Fields（网格距离场）生成软阴影，支持动态物体，比 Shadow Map 更自然。代价是显存开销大。

**Screen Space Ambient Occlusion（SSAO）**：在屏幕空间近似环境遮蔽效果，完全动态。虽然只是近似，但视觉效果比静态 AO Bake 好很多。

**Light Propagation Volumes（LPV）**：体积化的动态 GI 近似，支持动态光源影响 GI。精度有限，但方向正确。

这些都是"在不完美方案和不可能方案之间找工程近似"的典型例子。游戏引擎开发的本质就是这个——在性能预算内，找到最优的视觉近似。

### Unreal Engine 5（2022）：Lumen 的突破

UE5 的 **Lumen** 是游戏引擎历史上第一个在消费级硬件上实用的实时动态全局光照系统。

Lumen 的核心架构（从公开技术文档简化）：

```
两种 GI 来源混合：
1. Screen Space GI（屏幕空间，精度高，覆盖近处）
   ↓
2. World Space GI（基于 SDF 的全局光照，覆盖远处）

World Space GI 的实现：
- Surface Cache：把场景表面的光照信息缓存为"光照地图"
  （不是静态烘焙，而是每帧动态更新的缓存）
- Mesh Distance Fields：每个 Mesh 预生成 SDF，支持快速光线与场景的近似求交
- Final Gather：在 Screen Space 用稀疏采样，查询 Surface Cache 得到 GI 贡献

代价：
- GPU 内存消耗：1-2 GB 额外开销（Surface Cache）
- 移动端不支持（计算量超出移动 GPU 预算）
- 低端 PC 需要降级到 Screen Space only 模式
```

**Nanite（虚拟几何体）** 同样是 UE5 的革命性技术，但解决的是另一个问题：几何细节密度。

```
传统工作流：
美术制作高模（数百万多边形）→ 烘焙法线图 → 运行时用低模
（信息损失不可避免，LOD 切换有跳变感）

Nanite 工作流：
美术直接使用高模（数亿多边形都可以）→ 运行时 Nanite 自动按像素密度
流式化加载，每个像素只用足够的三角面数
（理论上消除了传统 LOD 系统和手工 LOD 烘焙）
```

Nanite 的实现核心是**软光栅化（Software Rasterization）**——当三角面小到一个像素以下时，传统硬件光栅化效率极低，Nanite 用 Compute Shader 自己实现了针对极小三角面的高效光栅化路径。

---

## Unity 的演化：另一条路

理解了 Unreal 的演化，再看 Unity，会发现它们完全是不同的起点和路径。

Gregory 在书中这样介绍 Unity：

> "Unity's primary design goals are ease of development and cross-platform game deployment."

这两句话说明了一切。Unity 从来不是为了顶级画质而生——它是为了**让更多人能做游戏**。

Unity 的演化路径：

```
2005 年：Unity 1.0，只支持 macOS，面向独立开发者
    ↓
2009 年：Unity 2.6，支持 Windows，向移动端扩展
    ↓
2010 年：Unity 3，Asset Store 上线，生态系统爆炸
    ↓
2012 年：Unity 4，Mecanim 动画系统，移动端市场主导
    ↓
2017 年：Unity 2017，Scriptable Render Pipeline 架构
    ↓
2019 年：Unity 2019，URP 稳定，DOTS 预览
    ↓
2021 年：Unity 2021，DOTS 接近稳定，Burst Compiler 成熟
    ↓
2022-今：Unity 2022/2023，ECS 正式发布，但公司战略动荡
```

Unity 在 2022-2023 年经历了重大的公司危机（Runtime Fee 事件，CEO 更换），这让很多开发者重新评估 Godot 和 Unreal。但从技术角度，DOTS/ECS 的方向是正确的——它解决了传统 GameObject 架构在大规模场景下的性能瓶颈。

### Unity 的移动端优势是真实的

不能因为 Unreal 在画质上领先就说 Unity"落后"。

在移动游戏开发中，Unity 的优势是系统性的：

```
渲染优化：
- URP 的 SRP Batcher 大幅减少 CPU SetPass 调用
- GPU Instancing 的自动化程度更高
- 移动端 Tile-Based 架构（TBDR）的针对性优化
- Shader Stripper 自动剔除未使用的 Shader 变体

工具链：
- Unity Profiler + Frame Debugger 的移动端支持更完善
- Android/iOS 的构建流程更简洁
- Asset Bundle + Addressables 的热更新方案更成熟

生态系统：
- 移动端中间件（Firebase、AppLovin、Facebook SDK）几乎全部优先支持 Unity
- 超休闲游戏、Hyper Casual 市场是 Unity 的绝对领地
```

这不是说 Unreal 在移动端不能用——吃鸡类（PUBG Mobile、和平精英）就是用 Unreal 做的。但移动端的默认选择仍然是 Unity，这有深刻的历史和生态原因。

---

## 技术债务的历史学

从引擎演化史可以学到一个更普遍的工程教训：**每一个技术决策都是有代价的债务，只是还款时间不同。**

BSP Tree 在 1993 年是正确的选择（硬件性能约束下的最优解），但到 1998 年就变成了技术债务——需要用 Portal + PVS 替代。

前向渲染在 2000 年代初是唯一可行的选择，但到 2006 年 UE3 引入延迟渲染时，前向渲染就成了需要偿还的债务（要么跟上，要么在多光源场景下落后）。

Unity 选择 C# 托管语言，在 2005 年降低了开发门槛（债务的收益），但到 2018 年就需要用 DOTS/Burst 来偿还这笔 GC 和 Cache 不友好的债务。

Unreal 选择 C++ + 深度反射系统，带来了极致性能（收益），但也带来了漫长的编译时间和陡峭的学习曲线（这笔债至今仍未还清）。

作为开发者，理解这个历史模式，能帮助你对当前项目中的技术选择有更清醒的认识：**你今天做的每一个架构决策，都是在未来的某个时间点需要偿还的债务。问题不是"要不要借"，而是"借的时候清楚代价，并且计划好还款方式"。**

---

## 代码视角：渲染管线的演化在 Unity 中的体现

理解了引擎演化史，再看 Unity 的渲染管线选择，会清晰很多：

```csharp
// Unity 三套渲染管线的核心差异

// Built-in Pipeline（第二代 Portal 时代的遗产）
// 前向渲染 + Fixed Function lighting（保留了大量遗留 API）
Camera.main.renderingPath = RenderingPath.Forward;
// 支持所有旧平台，但性能优化空间有限

// URP（针对移动端重新设计的前向渲染）
// 完全 Scriptable，通过 Renderer Features 扩展
UniversalAdditionalCameraData urpCameraData = 
    camera.GetUniversalAdditionalCameraData();
urpCameraData.renderType = CameraRenderType.Base;
// 移动端优化：Tile-based rendering friendly，Draw Call 合并更积极

// HDRP（面向高端 PC/主机的延迟渲染）
// G-Buffer: Albedo/BaseColor, Normal, MaterialProperty (Smoothness/Metallic)
// 完整 PBR + 动态 GI + 光线追踪支持
HDAdditionalCameraData hdrpCamera = 
    camera.GetComponent<HDAdditionalCameraData>();
// 代价：移动端不支持，最低硬件要求高
```

这三套管线对应了渲染技术演化的三个时代，Unity 选择全部保留而不是强制迁移——这既是商业策略（向后兼容），也是技术债务（维护三套系统的成本极高）。

---

## 延伸阅读

- **GEA 原文** §1.3-1.5 — Jason Gregory（Quake 到 UE4 的完整历史回顾）
- **Quake 源码** — <https://github.com/id-Software/Quake>（强烈推荐！用 VSCode 打开直接读）
- **Unreal Engine 5 技术博客** — Nanite & Lumen 的技术深度解析（Epic 官方）
- **Digital Foundry 频道** — YouTube，引擎技术的视觉对比分析

---

## 🎯 今日测验

**Q1（概念）：** id Tech（Quake）引擎使用 BSP Tree 解决可见性问题，而 Unreal Engine 1 使用 Portal + PVS。请解释这两种技术各自适合什么样的场景，为什么 BSP Tree 不适合室外开放世界？

**Q2（应用）：** Unity 的前向渲染（URP Forward）和 Unreal 默认的延迟渲染（Deferred）在移动端性能上有什么关键差异？如果你要在一个移动端游戏中支持 20 个动态点光源，两种渲染管线各自的代价是什么，应该怎么选？

**Q3（品味）：** 从今天的引擎演化史来看，每一个技术选择都是有代价的"技术债务"。回顾你参与过的项目，有哪个技术决策是当时"正确"的，但后来变成了需要偿还的债务？这笔债是怎么还的（或者还没还）？

> 回复本条消息作答，你的回答会影响明天的内容深度。

---

📅 **明天 Day 3：** 大型 C++ 软件工程 — 引擎级别的代码组织哲学
📊 **进度：** Day 2/30 | Phase 1: 引擎基础
