# Day 5 · Pixel Processing — 像素的命运

**RTR4 Ch2.5 | 渲染管线的最后裁决者**

---

前四天我们走过了管线的三分之三：CPU 决定渲染什么，顶点在 GPU 里做完了空间变换，光栅化把三角形打碎成了离散的像素。

今天我们到达终点。

Pixel Processing（像素处理）是管线里最后一个你真正能掌控的地方，也是决定画面最终长相的地方。学完这一章你会发现，这里藏着大量移动端性能问题的根源，也藏着一些被严重低估的利器。

---

## 一、Pixel Processing 的两张脸

RTR4 把 Pixel Processing 分成两个子阶段：

**Pixel Shading（像素着色）** 和 **Merging（输出合并）**。

先说清楚这个分法为什么重要。

Pixel Shading 是**可编程的**。你写 Fragment Shader，GPU 执行。这段代码决定了每个像素的颜色——你可以在这里做纹理采样、PBR 光照计算、后处理效果，想干什么干什么。

Merging 是**不可编程的，但高度可配置的**。

> "Unlike the shading stage, the GPU subunit that performs this stage is typically not fully programmable. However, it is highly configurable, enabling various effects."
> — RTR4, Section 2.5.2

这句话值得细嚼。深度测试、模板测试、Alpha 混合——这些都发生在 Merging 阶段，都不是你用代码写的，而是通过 API（`glDepthTest`、`glBlendFunc`、`stencilOp`）配置的。

硬件用固定逻辑来做这些事，因为它们足够简单、足够通用、并且需要极高的吞吐量——每秒要处理数十亿个像素，用可编程着色器来做太贵了。

---

## 二、Fragment Shader：每像素运行的小程序

很多初学者理解 Fragment Shader 的方式是错的。他们把它想成「处理像素的程序」，但这个描述不够准确。

更准确的说法是：**Fragment Shader 是在光栅化阶段生成的每一个 Fragment 上独立运行的程序。**

Fragment 和 Pixel 不是一回事。一个 Pixel（屏幕上的点）可能对应多个 Fragment——在 MSAA 开启时，一个像素可能有 4 个或 8 个采样点，每个都是独立的 Fragment。Fragment Shader 在每个 Fragment 上跑一遍，最终 Merging 阶段把这些 Fragment 合并成最终的 Pixel 颜色。

这不是文字游戏。理解这个区别，你才能理解为什么 MSAA 能在不增加多少着色成本的情况下提升边缘质量——因为 MSAA 多采样的那些点**共享同一次 Fragment Shader 执行**，而不是每个采样点跑一次 Shader。这是 MSAA 和 SSAA（Super Sampling）最本质的区别。

**Fragment Shader 能做什么？**

RTR4 提到了纹理贴图是最重要的技术之一：

> "A large variety of techniques can be employed here, one of the most important of which is texturing."

但这只是冰山一角。现代 Fragment Shader 几乎可以做任何事：

- **PBR 光照计算**：GGX 微表面模型、Fresnel 反射、各向异性高光
- **程序化材质**：Perlin 噪声、Voronoi 图案、数学生成的材质
- **屏幕空间效果**：SSAO、SSR、Depth of Field 的 CoC 计算
- **光线步进（Ray Marching）**：体积云、SDF 字体渲染、距离场效果
- **Alpha Test / Discard**：舍弃不满足条件的 Fragment，让它们不写入帧缓冲

最后一项在移动端尤其重要。RTR4 提到：

> "A discard operation can be inserted into the pixel shader program and any type of computation can be used to trigger a discard. This type of test can be used to ensure that fully transparent fragments do not affect the z-buffer."

`discard` 指令让你可以在 Shader 里主动杀死一个 Fragment。常见于植被、栅栏、Alpha Cutout 的渲染——让 Fragment 要么完全透明要么完全不透明，避免了 Alpha Blending 带来的排序和 Overdraw 问题。

但 `discard` 是有代价的：它会**破坏 Early-Z**。这是后面要重点讲的内容。

---

## 三、Z-Test：可见性问题的工程解法

现在进入 Merging 阶段。

**可见性（Visibility）是 3D 渲染最根本的问题**：当多个三角形投影到同一个像素时，哪一个应该显示？

Z-Buffer 算法是它的工程解：

> "A z-buffer is the same size and shape as the color buffer, and for each pixel it stores the z-value to the currently closest primitive."

算法本质极其简单——
- 渲染一个 Fragment 时，计算它的深度值 z
- 和 Z-Buffer 里这个像素存储的当前最小深度 z_min 比较
- 如果 z < z_min：这个 Fragment 更靠近相机，更新颜色缓冲和 Z-Buffer
- 如果 z >= z_min：这个 Fragment 被挡住了，丢弃

```
for each primitive:
    for each fragment (x, y, z) covered:
        if z < zbuffer[x][y]:
            zbuffer[x][y] = z
            colorbuffer[x][y] = shade(fragment)
```

RTR4 指出：这个算法是 O(n) 的（n 是图元数量），允许图元以任意顺序渲染，并且工作于任何能计算 z 值的图元。

听起来完美。但有两个重要的注意点。

**第一：Z-Buffer 不能直接处理半透明物体。**

> "However, the z-buffer stores only a single depth at each point on the screen, so it cannot be used for partially transparent primitives."

这句话是透明物体渲染复杂性的根源。Z-Buffer 每个像素只记录一个深度——「当前最近的表面」。但透明物体需要「看穿」——你需要同时知道表面本身的颜色和它后面的颜色。Z-Buffer 做不到这点，所以透明物体必须单独处理，必须从远到近排序渲染，必须在所有不透明物体渲染完毕之后才渲染。

**第二：Early-Z vs Late-Z 的性能差距是量级级别的。**

标准的管线流程是：Fragment Shader 执行 → 然后做 Z-Test。这叫做 **Late-Z**。

问题在于：Fragment Shader 可能非常复杂（100+ ALU 指令），但如果这个 Fragment 最终被 Z-Test 判定为「被遮挡」——所有的 Fragment Shader 计算都白费了。

所以现代 GPU 会做 **Early-Z**：在 Fragment Shader 执行**之前**就做深度测试。如果 Fragment 被遮挡，直接丢弃，Fragment Shader 完全不执行。

这在 Overdraw（多个物体重叠在同一像素）严重的场景里是巨大的性能节省。

但 Early-Z 有三个破坏条件：

1. **Fragment Shader 里有 `discard` 指令**：如果 Shader 可能主动丢弃 Fragment，GPU 就不能提前判断这个 Fragment 到底会不会存在——必须等 Shader 执行完再做 Z-Test
2. **Fragment Shader 修改深度值（`gl_FragDepth` / `SV_Depth`）**：如果 Shader 会改写深度，提前用几何深度做测试就不正确了
3. **Alpha Test（旧 API 的 alpha test，或者用 discard 实现的 Alpha Cutout）**：同第一条，GPU 不知道哪个 Fragment 会被丢弃

这就是为什么「使用 `discard` 的 Shader 性能更差」——不仅仅是因为 `discard` 本身的开销，而是因为它关闭了 Early-Z，所有 Overdraw 都变成了真实的着色开销。

**在移动端，这个问题尤其严重。**

移动端 GPU（Mali、Adreno、PowerVR）都采用 TBDR（Tile-Based Deferred Rendering）架构。TBDR 在 Tile 粒度做 Early-Z（或更强的 Hidden Surface Removal），能消除 Tile 内所有被遮挡的 Fragment 的着色计算。但一旦场景里有大量 `discard`（比如草、树叶的 Alpha Cutout），TBDR 的优化就大打折扣。

游戏开发中一个经典的陷阱：美术觉得草地很漂亮，加了大量 Alpha Cutout 植被。移动端帧率直接砍半——原因不只是三角形数量，而是 Early-Z 失效导致的 Overdraw 着色爆炸。

解决方法之一：**把 Alpha Cutout 的草换成不透明的几何体**（低模，但布局合理），在中远距离替代 Alpha Cutout。这是很多 AA 游戏实际使用的技巧。

---

## 四、Stencil Buffer：被低估的多面手

Z-Buffer 大家都懂，但 Stencil Buffer（模板缓冲）是一个经常被初学者忽略的工具。

RTR4 的描述：

> "The stencil buffer is an offscreen buffer used to record the locations of the rendered primitive. It typically contains 8 bits per pixel. Primitives can be rendered into the stencil buffer using various functions, and the buffer's contents can then be used to control rendering into the color buffer and z-buffer."

8 bits/pixel，意味着每个像素有一个 0-255 的值。你可以：
- 写入这个值（设置模板）
- 用这个值做测试（只在模板值满足条件时渲染）
- 在测试时递增/递减这个值

这些操作组合起来能实现很多意想不到的效果：

**描边效果（Outline）**：先用正常大小渲染物体写入模板，然后用稍微放大的同样物体渲染——只在模板测试失败（即放大物体比正常物体多出的部分）时渲染描边颜色。

**Shadow Volume（Carmack's Reverse）**：Doom 3 的像素精确实时阴影技术。为每个光源生成阴影体积几何，用 Stencil Buffer 记录阴影体积的正面和背面穿越次数——最终 Stencil 值非零的区域在阴影中。虽然现代项目不再用这个技术，但理解它帮助你理解 Stencil Buffer 的能力上限。

**Portal Rendering**：在 Portal 游戏中，传送门另一侧的世界需要被渲染到屏幕上传送门的形状区域里。做法是把传送门的形状写入 Stencil Buffer，然后在 Stencil 测试通过的区域渲染传送门另一侧的场景。

**SSR 的前处理**：Screen-Space Reflection 中，用 Stencil 标记场景里所有使用反射材质的区域，后续的 SSR Pass 只处理 Stencil 标记的像素——避免对整个屏幕做昂贵的 Ray March。

**Deferred Rendering 的 Light Volume**：渲染点光源时，先用 Stencil 测试检查光源球体的遮挡关系，只对真正被光源影响的像素做着色计算。

Stencil Buffer 几乎没有独立的性能成本——它本来就是 Merging 阶段的一部分。学会用它，你能以接近零成本实现很多效果。

---

## 五、Alpha Blending：美丽的性能杀手

RTR4 提到：

> "It is possible to mix the color currently in the color buffer with the color of the pixel being processed inside a triangle. This can enable effects such as transparency or the accumulation of color samples."

Alpha Blending 的公式很简单：

```
C_final = C_src × α + C_dst × (1 - α)
```

其中 C_src 是当前要渲染的 Fragment 颜色，C_dst 是帧缓冲里已有的颜色，α 是透明度。

但 RTR4 紧接着指出了根本性的限制：

> "The z-buffer stores only a single depth at each point on the screen, so it cannot be used for partially transparent primitives. These must be rendered after all opaque primitives, and in back-to-front order, or using a separate order-independent algorithm."

这一段话解释了透明物体为什么难处理：

**为什么必须从远到近排序？**

Alpha Blending 是有顺序依赖的操作。假设你有两个半透明物体 A（近）和 B（远），你想看到「A 半透明，透过 A 看到 B 半透明，透过 B 看到背景」。

如果先渲染 A 再渲染 B：帧缓冲里先有 A 的颜色，然后 B 和帧缓冲里的 A 混合——结果是 B 在 A 前面，错误。

如果先渲染 B 再渲染 A：帧缓冲里先有 B 的颜色，然后 A 和帧缓冲里的 B 混合——结果是 A 在 B 前面，正确。

所以必须从远到近排序。这引入了 CPU 端的排序开销，而且在粒子系统、半透明网格相互穿插的情况下，「正确排序」甚至没有答案。

**为什么透明物体不写 Z-Buffer？**

如果半透明物体写入 Z-Buffer，它们会遮挡后面的不透明物体——但半透明物体本应让你看穿。所以透明物体通常只做 Z-Test（测试是否被不透明物体挡住），但不做 Z-Write（不更新 Z-Buffer）。

这意味着：透明物体之间不能通过 Z-Buffer 判断遮挡关系，必须靠排序。

**为什么 Overdraw 更严重？**

不透明物体有 Early-Z 保护——如果一个像素已经被近处物体占据，远处物体的 Fragment Shader 可能不需要执行。但透明物体不写 Z-Buffer，所以每一层透明物体都要执行 Fragment Shader、都要做混合操作。10 层半透明粒子重叠 = 10 次 Fragment Shader + 10 次 Alpha Blend，完全没有优化可言。

这解释了为什么很多移动端游戏的粒子效果是最大的性能瓶颈——不是因为顶点数量，而是因为透明 Overdraw。

**实际项目中的应对策略：**

1. **能用 Alpha Test 就不用 Alpha Blend**：Alpha Test（`discard`）不需要排序，不产生 Overdraw，代价是边缘锯齿——但这个锯齿在运动中通常可接受
2. **严格控制透明图层深度**：超过 2-3 层的透明叠加要向美术提出警告
3. **粒子系统的特殊优化**：用低分辨率 RT 渲染粒子，然后合成到主帧缓冲——「软粒子」技术既解决了粒子和几何体交界处的硬边，又降低了分辨率从而降低 Overdraw 开销
4. **Order-Independent Transparency（OIT）**：学术上有很多解决方案（Depth Peeling、Weighted Blended OIT），但在移动端几乎不实用

---

## 六、MRT：一次渲染，多个输出

前面说的所有内容都是「渲染到一个颜色缓冲」。但现代 GPU 支持 **MRT（Multiple Render Targets）**：一次渲染，同时写入多个不同的 RT。

这是 **Deferred Rendering** 的技术基础。

在 Deferred Rendering 的 G-Buffer Pass 里，你的 Fragment Shader 同时输出：
- RT0：Albedo（基础颜色）
- RT1：Normal（世界空间法线）
- RT2：Roughness + Metallic（PBR 参数）
- Z-Buffer：深度

然后在 Lighting Pass 里，读取这四张 RT 重建世界空间位置和材质信息，再计算光照。

MRT 的意义在于：**把几何信息和光照信息解耦**。几何 Pass 只跑一次，不管场景里有多少光源。光照 Pass 的开销只和屏幕上被照亮的像素数量有关，不和场景几何复杂度有关。

在光源数量多的场景里，Deferred Rendering 比 Forward Rendering 效率高很多——Forward 是 O(几何复杂度 × 光源数量)，Deferred 是 O(几何复杂度) + O(屏幕像素数 × 光源数量)。

当然 MRT 也有代价：G-Buffer 需要存储大量数据，带宽开销大。对于移动端 TBDR GPU，频繁的 RT 切换是主要瓶颈——所以 Deferred Rendering 在移动端需要非常谨慎地设计。

---

## 七、从 Late-Z 到 Early-Z 到 HSR：优化的层次

不同的 GPU 架构对 Z-Test 有不同级别的优化，这直接影响你写 Shader 的策略。

**桌面 GPU（IMR，Immediate Mode Rendering）**：
- 标准 Late-Z：Fragment Shader → Z-Test
- Early-Z（有条件）：如果 Fragment Shader 没有 `discard` 且不修改深度，GPU 会自动升级到 Early-Z
- Hi-Z（Hierarchical Z）：用深度 Mipmap 做 Tile 级别的粗粒度剔除，进一步减少需要精确测试的 Fragment 数量

**移动端 GPU（TBDR，Tile-Based Deferred Rendering）**：
- 在 Fragment Shader 执行之前，GPU 在 Tile 内部（通常 16×16 像素）做完整的 HSR（Hidden Surface Removal）
- HSR 可以精确确定 Tile 内每个像素的最终可见 Fragment，只对这些 Fragment 执行 Shader
- 理论上可以消除 Tile 内所有 Overdraw 的着色开销
- 但 HSR 要求 Fragment Shader 不能 `discard`、不能写深度——否则降级到类似 Late-Z 的处理

这就是为什么移动端性能分析工具（如 ARM Mobile Studio）会专门报告「Shader 中 discard 的使用率」——高 discard 率是 TBDR 优化失效的直接信号。

一个实际数据点（来自 ARM 开发者文档）：在 Overdraw = 4 的场景（屏幕平均每像素被 4 个三角形覆盖）里：
- 无 discard + TBDR HSR：着色开销接近 1× Overdraw（近似理想）
- 有 discard + TBDR 降级：着色开销接近 4× Overdraw（每层都要执行 Shader）

四倍的性能差距来自一个看似无害的 `if (alpha < 0.5) discard;`。

---

## 八、Double Buffering：不让用户看到「施工现场」

最后说一个简单但重要的概念。

RTR4 提到：

> "To avoid allowing the human viewer to see the primitives as they are being rasterized and sent to the screen, double buffering is used. This means that the rendering of a scene takes place off screen, in a back buffer. Once the scene has been rendered in the back buffer, the contents of the back buffer are swapped with the contents of the front buffer that was previously displayed on the screen. The swapping often occurs during vertical retrace, a time when it is safe to do so."

**Front Buffer** 是正在显示的帧，**Back Buffer** 是正在渲染的下一帧。渲染完成后两者交换（Swap）。

交换发生在「垂直回扫（Vertical Retrace）」时——也就是显示器扫描完一帧准备开始下一帧的间隙。这就是 VSync（垂直同步）的来源。

开启 VSync：只在回扫时交换，画面不会撕裂（Tearing），但帧率被锁定到显示器刷新率的因子（60fps → 60/30/20...）。
关闭 VSync：随时可以交换，帧率可以超过显示器刷新率，但可能撕裂（屏幕显示的一帧里同时有上一帧的上半部分和下一帧的下半部分）。

现代解决方案：**Triple Buffering**（再加一个缓冲区，渲染结果准备好了就写，显示器取时再取最新的，减少撕裂的同时减少帧率降级）；或者 G-Sync/FreeSync 自适应同步（显示器刷新率跟着 GPU 走）。

---

## 九、Pixel Processing 的移动端视角

综合以上内容，从移动端开发者的角度做一个品味总结：

**关于 Fragment Shader：**
- 纹理采样是最贵的操作（相比 ALU 指令），减少采样次数比减少指令数量更有效
- `discard` 要谨慎，它关闭 Early-Z 和 TBDR 的 HSR，Overdraw 代价暴增
- fp16 精度计算在 Mali 和 Adreno 上通常比 fp32 快 2 倍，大量可以降精度的中间值（UV、颜色、法线分量）应该用 half

**关于 Z-Buffer：**
- 不透明物体从近到远渲染（近处先占据 Z-Buffer，远处 Fragment 直接被 Early-Z 丢弃）
- 透明物体最后渲染，从远到近排序
- 在 TBDR 机器上，避免在帧中间切换 RT（会破坏 Tile 的完整性，触发隐式 Resolve）

**关于 Stencil：**
- Stencil 几乎免费，多用
- 描边、UI 遮罩、特殊效果区域标记都是 Stencil 的典型用途

**关于 Alpha Blend：**
- 移动端粒子系统一定要做 Overdraw 预算管理
- 能 Alpha Test 就不 Alpha Blend
- 软粒子（低分辨率 RT 合成）是减少透明 Overdraw 的有效手段

---

## 十、一个完整的 Fragment Shader 示例

最后用代码把今天的概念串联起来：

```hlsl
// Unity HLSL Fragment Shader 示例
// 演示 Alpha Test + Early-Z 友好写法

Shader "RTR4/Day05/AlphaCutout"
{
    Properties
    {
        _MainTex ("Albedo", 2D) = "white" {}
        _Cutoff ("Alpha Cutoff", Range(0, 1)) = 0.5
        _NormalMap ("Normal Map", 2D) = "bump" {}
    }
    
    SubShader
    {
        // 不透明队列：不参与透明物体排序
        // RenderType 标记帮助 Unity 识别这是 Alpha Test 物体
        Tags { "Queue"="AlphaTest" "RenderType"="TransparentCutout" }
        
        Pass
        {
            // 开启深度写入（不透明物体应该写 Z-Buffer）
            ZWrite On
            // 开启深度测试
            ZTest LEqual
            // 不开启 Blend（不需要 Alpha Blending）
            Blend Off
            
            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            
            struct appdata
            {
                float4 positionOS : POSITION;
                float2 uv : TEXCOORD0;
                float3 normalOS : NORMAL;
            };
            
            struct v2f
            {
                float4 positionCS : SV_POSITION;
                float2 uv : TEXCOORD0;
            };
            
            sampler2D _MainTex;
            float _Cutoff;
            
            v2f vert(appdata v)
            {
                v2f o;
                o.positionCS = TransformObjectToHClip(v.positionOS.xyz);
                o.uv = v.uv;
                return o;
            }
            
            half4 frag(v2f i) : SV_Target
            {
                half4 col = tex2D(_MainTex, i.uv);
                
                // Alpha Test：用 clip 而不是 discard（功能相同，但语义更清晰）
                // clip(x) 当 x < 0 时丢弃当前 Fragment
                // 等价于：if (col.a - _Cutoff < 0) discard;
                clip(col.a - _Cutoff);
                
                // 注意：使用了 clip/discard 后，这个 Shader
                // 在 TBDR GPU 上会关闭 HSR 优化
                // 权衡：Alpha Cutout 的视觉效果 vs 性能损失
                
                return half4(col.rgb, 1.0);
                // 注意：我们输出 alpha = 1，因为这是不透明物体
                // 已经通过 clip 筛选，剩下的像素都是「不透明」的
            }
            ENDHLSL
        }
    }
}
```

对比一下**不友好**的写法（会产生更多问题）：

```hlsl
// 错误示例：透明物体但没有正确设置队列和混合
Shader "RTR4/Day05/WrongTransparent"
{
    SubShader
    {
        // 错误：用 Geometry 队列渲染透明物体
        // 会和不透明物体混排，排序错误
        Tags { "Queue"="Geometry" }
        
        Pass
        {
            // 错误：透明物体开启了 ZWrite
            // 会遮挡后面的透明物体
            ZWrite On
            
            // 开启了混合但没有正确设置队列
            Blend SrcAlpha OneMinusSrcAlpha
            
            HLSLPROGRAM
            // ... 
            // 结果：透明物体和不透明物体互相干扰
            // Z-Buffer 被透明物体污染，后面的透明物体被错误遮挡
            ENDHLSL
        }
    }
}
```

正确的透明物体设置：

```hlsl
Tags { "Queue"="Transparent" "RenderType"="Transparent" }
ZWrite Off        // 不写深度
ZTest LEqual      // 但要做深度测试（被不透明物体遮挡时不渲染）
Blend SrcAlpha OneMinusSrcAlpha  // 标准 Alpha 混合
```

---

## 总结：今天的品味升级

**Pixel Processing 的三个层次理解：**

**Level 1（知道做法）**：Fragment Shader 决定颜色，Z-Test 决定可见性，Blend 做透明混合。

**Level 2（知道为什么）**：Early-Z 比 Late-Z 高效，因为省掉了被遮挡 Fragment 的 Shader 执行；透明物体必须排序，因为 Alpha Blend 是有顺序依赖的；Stencil Buffer 是精确区域控制的利器，成本接近零。

**Level 3（知道什么时候不做）**：`discard` 虽然方便，但在 TBDR 移动端是 HSR 的杀手，用前要评估 Overdraw 的实际成本；Alpha Blend 虽然漂亮，但粒子层叠超过 3 层就要做预算评审；MRT 和 Deferred Rendering 虽然在多光源场景很高效，但移动端的带宽成本让它的适用场景比桌面端窄得多。

---

> **今日品味结晶：** Pixel Processing 不是管线的「终点」，而是性能决战的「战场」。Early-Z、HSR、Overdraw 预算——这些概念的深度掌握，区分了「能用 GPU」和「会用 GPU」的开发者。

---

## 🎯 今日测验

**Q1（概念）：** 解释为什么在 Fragment Shader 中使用 `discard` 会影响渲染性能，在 TBDR 架构的移动端 GPU 上这个影响和桌面端有什么不同？

**Q2（应用）：** 假设你在优化一个移动端游戏，场景里有大量半透明的草地（用 Alpha Blend 实现），在 ARM Mobile Studio 里发现帧率瓶颈在 Fragment Shader 阶段，Overdraw 超过 400%。你会采取哪些策略来优化，优先级如何排序？

**Q3（品味）：** 下面两种实现「角色描边效果」的方案，各有什么 Trade-off？从性能、画质、实现复杂度三个维度分析：
- 方案 A：用 Stencil Buffer + 放大物体的两 Pass 方案
- 方案 B：在 Fragment Shader 里用 Sobel 算子检测法线/深度不连续区域做后处理描边

> 回复本条消息即可作答，你的回答会影响明天的推送深度和方向。

---

*Day 5 / 90 · RTR4 Coach 模式 · 实时生成*
