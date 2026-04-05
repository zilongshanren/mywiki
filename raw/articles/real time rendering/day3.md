1. ## Geometry Processing — 顶点的旅程
    
    > 系列：Real-Time Rendering 4th Edition 精读 | 面向资深客户端程序员
    
    ---
    
    ### 开场白：一个顶点的一生
    
    如果你问我图形学里哪个知识点是"看似简单、细究惊人"的，我会说：MVP 变换。 几乎每个做过 Shader 的人都写过 `mul(UNITY_MATRIX_MVP, v.vertex)`，但真正想清楚"为什么是三个矩阵而不是一个"、"裁剪为什么放在 Clip Space"、"Z 值的精度为什么远处烂"的人，可能不到十分之一。 今天我们把这条路从头走一遍。不是课本式的定义堆砌，而是每一步问"你为什么存在"。 ---
    
2. ## 一、空间序列：每个坐标系存在的理由
    
    RTR4 Ch2.3 原文：
    
    > _"Originally, a model resides in its own model space... Each model can be associated with a model transform so that it can be positioned and oriented."_
    
    顶点的旅程经过六个空间： **Model Space → World Space → View Space → Clip Space → NDC → Screen Space** 但让我换个问法：**如果没有这些中间空间，会发生什么？**
    
    ### 
    
    1. Model Space（模型空间）——为了复用
    
    模型空间是美术建模时的坐标系，原点通常在模型中心或脚底。它存在的理由只有一个：**复用**。 同一把剑的模型数据，可以放在场景里的任意位置、任意朝向。如果不存在模型空间，每把剑都要用世界坐标存储——场景里 100 把剑就需要 100 份顶点数据，而不是 100 个变换矩阵 + 1 份顶点数据。
    
3. 这是数据压缩的基本直觉：**把"变化"和"不变"分离开**。
    
    ### 
    
    2. World Space（世界空间）——为了光照与物理
    
    Model Space 是局部的，物理意义不强。World Space 是第一个有绝对坐标意义的空间。 **这里是光照计算的主场。** 光源位于世界空间的某个位置。方向光的方向是世界空间的向量。点光源的衰减半径是世界单位。**如果你在 View Space 做光照，必须先把光源变换到 View Space——而且每帧相机移动时都要重算。** 所以 World Space 存在的理由是：**它是物理量有意义的第一个空间**，光照、物理碰撞、AI 导航都在这里。
    
    ### 
    
    3. View Space（观察空间）——为了投影简洁
    
    RTR4 原文：
    
    > _"The purpose of the view transform is to place the camera at the origin and aim it, to make it look in the direction of the negative z-axis, with the y-axis pointing upward and the x-axis pointing to the right."_
    
4. View Space 把相机放到原点，朝向 -Z 轴。这一步纯粹是为了让**投影矩阵的数学更简单**。 如果相机在世界空间任意位置和方向，透视投影矩阵的推导会非常复杂。先把相机移到标准位置，投影矩阵就变成了一个固定形式的 4×4 矩阵。 这是"先标准化，再操作"的典型工程思维。
    
    ### 
    
    4. Clip Space（裁剪空间）——为了裁剪一致性
    
    这是最容易被误解的空间。顶点着色器输出的 `gl_Position` 就是 Clip Space 坐标。 **它的存在意义：让裁剪问题变成一个固定问题。**
    
5. RTR4：_"The advantage of performing the view transformation and projection before clipping is that it makes the clipping problem consistent; primitives are always clipped against the unit cube."_ 不管场景多复杂、相机视锥体是什么形状，投影之后所有图元都被裁剪到同一个标准立方体（[-1,1]³ 或 [0,1]³）。这个**统一性**让 GPU 硬件可以用极简的逻辑实现裁剪。我们后面会详细讲为什么不在 World Space 裁剪。
    
    ### 
    
    5. NDC（标准化设备坐标）——透视除法之后
    
    NDC 是透视除法（`x/w, y/w, z/w`）之后的结果。X 和 Y 在 [-1, 1] 范围内，Z 范围取决于 API（OpenGL 是 [-1, 1]，DirectX/Metal/Vulkan 是 [0, 1]）。 NDC 存在的意义：**API 无关的标准化坐标**。不管视口多大，NDC 的范围是固定的。
    
    ### 
    
    6. Screen Space（屏幕空间）——最终像素坐标
    
    视口变换把 NDC 映射到像素坐标。X 和 Y 变成具体的像素位置，Z 值映射到深度缓冲的精度范围。 ---
    
    ## 二、MVP 矩阵为什么不预乘成一个？
    
6. 这个问题我在面试中问过很多人，大多数人的回答是"不知道"或者给一个错误的理由。 **正确答案是：有时候你需要中间结果。** 具体来说： **光照计算需要世界空间或观察空间的顶点位置**。Phong 光照模型需要知道顶点到光源的方向，而这个计算发生在 World Space 或 View Space——不是在 Clip Space，也不是在 NDC。 如果你把 MVP 预乘成一个矩阵，顶点着色器的输入直接跳到 Clip Space，就**丢失了 World Space 的位置信息**。
    
    `// Unity C# 示例：理解 MVP 矩阵分解 using UnityEngine;  public class MVPDebugger : MonoBehaviour {`
    
7.     `// 展示 MVP 矩阵不能简单合并的场景     [Header("调试 MVP 各阶段坐标")]     public Transform targetObject;     public Light pointLight;      void Update()     {         if (targetObject == null) return;                  Camera cam = Camera.main;         if (cam == null) return;          // 获取各个矩阵         Matrix4x4 M = targetObject.localToWorldMatrix;   // Model → World         Matrix4x4 V = cam.worldToCameraMatrix;            // World → View`
    
8.         `Matrix4x4 P = cam.projectionMatrix;               // View → Clip         Matrix4x4 MVP = P * V * M;                        // 预乘版本                  // 顶点在模型空间的原点         Vector4 localPos = new Vector4(0, 0, 0, 1);                  // 逐步变换         Vector4 worldPos  = M * localPos;    // 世界空间：用于光照计算         Vector4 viewPos   = V * worldPos;    // 观察空间：可用于某些效果`
    
9. Vector4 clipPos = P * viewPos; // 裁剪空间：用于裁剪  
    // 预乘版本（跳过中间步骤） Vector4 clipPosFast = MVP * localPos; // 直接到 Clip Space  
    // 光照计算示例：必须用世界空间位置 if (pointLight != null) { Vector3 lightDir = (pointLight.transform.position - (Vector3)worldPos).normalized; float NdotL = Mathf.Max(0, Vector3.Dot(targetObject.up, lightDir));  
    // 关键：lightDir 和 NdotL 的计算需要 worldPos // 如果只有 clipPosFast，我们无法做这个计算 Debug.Log($"World Pos: {worldPos}, NdotL: {NdotL:F3}"); }  
    // 透视除法：Clip → NDC
    
10. Vector3 ndcPos = new Vector3( clipPos.x / clipPos.w, clipPos.y / clipPos.w, clipPos.z / clipPos.w );  
    Debug.Log($"Clip: {clipPos}, NDC: {ndcPos}, w={clipPos.w:F3}"); } }
    
    `**其他需要中间结果的场景：**  - **法线变换**需要在 World Space 或 View Space 完成，再传给光照计算 - **Shadow Map 采样**需要 World Space 位置转换到光源的 View/Clip Space - **屏幕空间效果**（SSAO、SSR）需要重建 World/View Space 位置`
    
11. `- **顶点动画**（如骨骼蒙皮）发生在 Local Space，动画结果才经过 MVP  当然，对于简单的无光照 Shader（UI、纯色、粒子），预乘 MVP 是合理的优化——减少顶点着色器的矩阵乘法次数。但"默认预乘"是错误的工程习惯。  ---  ## 三、裁剪为什么在 Clip Space，不在 World Space？  这个设计决策包含了非常深刻的工程智慧。  ### 问题的本质  在 World Space 做裁剪，你需要对一个任意形状的视锥体（frustum）做图元裁剪。视锥体的六个面方向各不相同，每个面都要做线段-平面求交——而且相机移动时这六个平面的方程每帧都在变。  在 Clip Space 做裁剪，所有图元都被裁剪到 [-1,1]³ 的标准立方体。六个裁剪面的方程是固定的：`
    
12. -w ≤ x ≤ w -w ≤ y ≤ w  
    -w ≤ z ≤ w（OpenGL） 0 ≤ z ≤ w（DirectX）
    
    `RTR4 原文点出了核心：  > *"The use of a projection matrix means that the transformed primitives are clipped against the unit cube. The advantage... is that it makes the clipping problem consistent; primitives are always clipped against the unit cube."*  ### 硬件视角`
    
13. GPU 的裁剪单元是固定功能硬件（Fixed-Function），它被设计为处理上述固定形式的裁剪条件。这个硬件可以极高效地并行运行，因为裁剪条件永远不变。 如果在 World Space 裁剪，要么需要可编程的裁剪硬件（代价极高），要么每帧把裁剪平面参数传给硬件（也有代价）。
    
    ### 一个隐藏的细节：w 坐标的作用
    
    RTR4 原文：
    
    > _"The fourth coordinate is needed so that data are properly interpolated and clipped when a perspective projection is used."_
    
    在 Clip Space，裁剪条件是 `-w ≤ x ≤ w`，而不是 `-1 ≤ x ≤ 1`。这是因为透视除法还没发生——w 存储了深度信息，裁剪必须在透视除法之前进行，才能正确处理跨越视锥体边界的图元。 如果先做透视除法再裁剪，近平面附近的图元会发生数值问题（近平面上的点 w≈0，导致除法结果不稳定）。 ---
    
    ## 四、透视除法的非线性——Z-fighting 的根源
    
14. 这一节我要重点讲透，因为这是移动端最常见的视觉 Bug 之一的根源，但很多人不理解为什么会发生。
    
    ### 透视投影矩阵对 Z 做了什么
    
    对于 OpenGL 约定的透视投影矩阵，Z 变换的本质是：
    
    `Z_clip = -( (f+n)/(f-n) * Z_view + 2*f*n/(f-n) ) W_clip = -Z_view`
    
    透视除法后：
    
    `Z_ndc = Z_clip / W_clip = (f+n)/(f-n) + 2*f*n/((f-n)*Z_view)`
    
15. 注意这个公式：Z_ndc 是 Z_view 的**倒数函数**，不是线性函数。
    
    ### 用数字说话
    
    假设 near=0.1, far=1000：
    
    - Z_view = -0.1（近平面）→ Z_ndc = -1.0
    - Z_view = -0.2（仅比近平面远一倍）→ Z_ndc ≈ -0.9995
    - Z_view = -500（中间位置）→ Z_ndc ≈ +0.998
    - Z_view = -1000（远平面）→ Z_ndc = +1.0
    
    **约 50% 的深度精度分配给了前 0.2% 的可见距离！** 这就是问题：远处两个物体在 Z_ndc 空间几乎没有差距，一旦差距小于深度缓冲的精度（通常是 24-bit，精度约 1/16777216），深度测试就会随机翻转，产生 Z-fighting。
    
    `// Unity C# 可运行示例：可视化 Z 精度分布`
    
16. `using UnityEngine; using System.Collections.Generic;  public class ZPrecisionVisualizer : MonoBehaviour {     [Header("相机参数")]     public float nearPlane = 0.1f;     public float farPlane = 1000f;     public int depthBits = 24;          [Header("可视化")]     public bool showInGizmos = true;          // 世界空间 Z 到 NDC Z 的转换（OpenGL 约定）     float WorldZtoNDC(float zView, float n, float f)`
    
17.     `{         // zView 是负值（相机看向 -Z）         return -(f + n) / (f - n) - 2 * f * n / ((f - n) * zView);     }          // 计算某个深度处，两个相邻可区分的深度之间的最小间隔（世界单位）     float MinDepthSeparation(float zView, float n, float f)     {         int maxDepthVal = (1 << depthBits) - 1;`
    
18. float ndcZ = WorldZtoNDC(zView, n, f); float ndcZ_plus1 = ndcZ + 2.0f / maxDepthVal; // NDC 中移动一个精度单位  
    // 反推世界空间 Z 差值 // Z_ndc = (f+n)/(f-n) + 2fn/((f-n) * Z_view) // 求解 Z_view: Z_view = 2fn / ((Z_ndc - (f+n)/(f-n)) * (f-n)) float A = (f + n) / (f - n); float B = 2 * f * n / (f - n);  
    float z1 = -B / (ndcZ - A); // 注意符号（zView 是负值） float z2 = -B / (ndcZ_plus1 - A);  
    return Mathf.Abs(z1 - z2); }  
    void OnGUI() {
    
19. if (!showInGizmos) return;  
    GUILayout.BeginArea(new Rect(10, 10, 500, 600)); GUILayout.Label($"=== Z 精度分析 (near={nearPlane}, far={farPlane}, {depthBits}-bit) ==="); GUILayout.Label("距离相机(m) | 最小可区分深度差(mm)"); GUILayout.Label("-------------------------------------");  
    float[] distances = { 0.5f, 1f, 2f, 5f, 10f, 50f, 100f, 500f, 999f }; foreach (float dist in distances) { if (dist < nearPlane || dist > farPlane) continue; float minSep = MinDepthSeparation(-dist, nearPlane, farPlane); string warning = minSep > 0.01f ? " ![⚠️](https://discord.com/assets/fb6fd920c79bd504.svg)" : ""; GUILayout.Label($" {dist,6:F1}m {minSep * 1000,10:F4}mm{warning}"); }  
    GUILayout.Label("
    
20. ![⚠️](https://discord.com/assets/fb6fd920c79bd504.svg) 超过 10mm 精度损失时容易出现 Z-fighting"); GUILayout.EndArea(); } }
    
    `运行这个脚本，你会看到：**在 near=0.1、far=1000 的配置下，距离相机 500m 处，两个表面必须相差超过几十毫米才能被深度缓冲区分。这就是为什么大地图游戏的远处建筑经常闪烁。**  ### Reversed-Z：品味性的工程优化  标准深度缓冲把近平面映射到 Z=0、远平面映射到 Z=1（DirectX 约定）或 Z=-1~1（OpenGL）。精度集中在近处。  Reversed-Z 反过来：**把近平面映射到 Z=1、远平面映射到 Z=0**。  为什么这能改善精度？这里有两个因素叠加： 1. **浮点数在接近 0 时精度最高**（指数位全为零，尾数精度全用于小数部分）`
    
21. `2. Reversed-Z 把精度从远平面挪向了近平面——而恰好浮点数在接近 0 时精度最好  两者叠加，使得 Reversed-Z 在远处和近处**都有更好的精度分布**。`
    
22. 这是 2015 年后游戏行业的最佳实践，所有新项目都应该默认启用 Reversed-Z。
    
    `// Unity 开启 Reversed-Z（Universal RP 已经默认开启） // 在 Built-in Pipeline 中手动配置 void ConfigureReversedZ() {     // URP 和 HDRP 默认启用 Reversed-Z     // 检查当前状态     bool isReversedZ = SystemInfo.usesReversedZBuffer;     Debug.Log($"Reversed-Z Buffer: {isReversedZ}");          // 在 Shader 中处理 Reversed-Z 兼容     // #if UNITY_REVERSED_Z     //     float depth = 1.0 - rawDepth;  // 还原到 0=近, 1=远     // #else`
    
23.     `//     float depth = rawDepth;     // #endif }`
    
    ─── 五、Screen Mapping：OpenGL vs DirectX 的坐标陷阱 透视除法之后，我们到了 NDC。然后视口变换把 NDC 映射到屏幕像素坐标。 RTR4 原文： _"The x- and y-coordinates of each primitive are transformed to form screen coordinates. The z-coordinate ([−1, +1] for OpenGL and [0, 1] for DirectX) is also mapped to [z1, z2], with z1=0 and z2=1 as the default values."_ 坐标原点在哪里
    
24. 这是一个每年都要坑一批人的问题。
    
    `| API     | Y 轴方向 | 原点位置 | Z 范围    | | ------- | ----- | ---- | ------- | | OpenGL  | 向上    | 左下角  | [-1, 1] | | DirectX | 向下    | 左上角  | [0, 1]  | | Vulkan  | 向下    | 左上角  | [0, 1]  | | Metal   | 向下    | 左上角  | [0, 1]  |`
    
    **OpenGL 的 Y 轴朝上，原点在左下角。DirectX/Vulkan/Metal 的 Y 轴朝下，原点在左上角。** 这个差异不只是理论上的——它在以下场景都会产生 Bug：
    
    1. **Shadow Map 采样**：如果 Shadow Map 用 OpenGL 坐标、但你的 Shader 用 DirectX 假设，阴影会上下翻转
    2. **后处理 UV 坐标**：全屏后处理时 UV 的上下可能倒置
    3. **Render Texture 转屏幕**：在某些平台上需要翻转 Y 坐标
    
25. 4. **离屏渲染到纹理**：纹理坐标和屏幕坐标的对应关系不同
    
    `// Unity C# 示例：跨平台 UV 翻转处理 using UnityEngine; using UnityEngine.Rendering;  public class PlatformUVFix : MonoBehaviour {     // Unity 内置的跨平台 UV 处理宏     // _ProjectionParams.x == 1 → Y轴朝上（OpenGL风格）     // _ProjectionParams.x == -1 → Y轴朝下（DirectX风格）          Material blitMaterial;          void Start()`
    
26.     `{         // 检查平台 UV 翻转需求         // 注意：Unity 会自动处理大多数情况，但自定义管线需要手动处理         bool requiresFlip = SystemInfo.graphicsUVStartsAtTop;`
    
27. Debug.Log($"UV starts at top: {requiresFlip}"); // true = DirectX/Metal/Vulkan 风格（Y向下，原点左上） // false = OpenGL 风格（Y向上，原点左下） }  
    // 在自定义 Blit 时处理 UV 翻转 void SafeBlit(RenderTexture src, RenderTexture dest) { if (blitMaterial == null) return;  
    // 设置 UV 翻转参数 // Unity Shader 中通常用 #if UNITY_UV_STARTS_AT_TOP 宏处理 float flipY = SystemInfo.graphicsUVStartsAtTop ? -1f : 1f; blitMaterial.SetFloat("_FlipY", flipY);  
    Graphics.Blit(src, dest, blitMaterial); }
    
28. // Shader 中的对应处理： // HLSL/GLSL: // #if UNITY_UV_STARTS_AT_TOP // uv.y = 1.0 - uv.y; // 翻转 Y // #endif }
    
    ``**实际项目建议**：在 Unity 中，大多数平台差异由引擎内部处理。但当你写自定义渲染管线（Custom SRP）或者操作原始 RenderTexture 时，务必用 `SystemInfo.graphicsUVStartsAtTop` 检查当前平台，或者使用 Unity 的 `_ProjectionParams` 内置变量。  ---  ## 六、移动端 TBDR 视角：Geometry Stage 有何不同？  如果你只在 PC 上开发，可能觉得几何处理阶段是"理所当然"的。但在移动端 TBDR（Tile-Based Deferred Rendering）架构下，有几个不同之处值得关注。``
    
29. ``### Binning Pass 对几何的影响  在 TBDR 架构（PowerVR、Mali、Apple GPU、Adreno 的部分模式）中，渲染管线多了一个步骤：  1. **Binning Pass**：顶点着色器先运行一遍，把每个三角形分配到它覆盖的 Tile。只输出位置（`SV_Position`），其他 varying 不产生。 2. **Rendering Pass**：逐 Tile 执行，只处理属于这个 Tile 的三角形，片段着色器在片上内存中运行。  这意味着：  **顶点着色器在移动端会被执行两次！**（或者说位置计算会执行两次）  这对几何处理有实际影响： - **避免在顶点着色器做昂贵的计算**（如骨骼蒙皮）——因为它会被执行两次 - Unity 对此的优化：`Unity_INSTANCED_SVP` 等机制，在支持的 GPU 上避免重复执行位置计算``
    
30. `- 骨骼蒙皮应该放到 Compute Shader 预计算，写回 SSBO（Shader Storage Buffer Object），VS 只读取结果`
    
    csharp // Unity C# 示例：移动端骨骼蒙皮优化策略 using UnityEngine; public class MobileSkinningOptimizer : MonoBehaviour { // 检测是否应该用 GPU Skinning void Start() { // 强制开启 GPU 蒙皮（避免 VS 双重执行的问题） // 注意：Unity 的 GPU Skinning 在移动端会使用 Compute Shader 预计算 var animator = GetComponent<Animator>();
    
31. if (animator != null) { // 检查骨骼数量 var smr = GetComponentInChildren<SkinnedMeshRenderer>(); if (smr != null) { int boneCount = smr.bones.Length; Debug.Log($"骨骼数量: {boneCount}");  
    // 移动端建议：骨骼 > 32 时使用 GPU Skinning // Unity 菜单：Player Settings → GPU Skinning if (boneCount > 32) { Debug.LogWarning("建议开启 GPU Skinning 避免 TBDR 下 VS 重复执行骨骼计算"); } } }
    
32. }  
    // TBDR 几何优化核心原则： // 1. 减少 VS 输出的 varying 数量（减少 Binning Pass 数据量） // 2. 避免在 VS 中做复杂计算（会执行两次） // 3. 几何着色器（GS）在移动端几乎完全禁用——不支持或性能极差 // 4. 曲面细分在移动端几乎无用（Binning 阶段处理不了动态拓扑） }
    
    `### Geometry 在 TBDR 中的另一个特点：过度绘制与几何的关系  TBDR 的 HSR（Hidden Surface Removal）可以在片段着色器执行前消除被遮挡的片段。**但这依赖于几何正确提交：不透明物体必须先提交，且不能开 Alpha Test 或 discard。**  如果你的顶点着色器在某些条件下把顶点推到视锥体外（比如错误的裁剪逻辑），可能导致 TBDR 的 Binning 阶段失效，HSR 无法工作。`
    
33. `---  ## 七、整合视角：一帧里 Geometry Stage 的真实成本  理解了每个空间的作用之后，来看实际项目中的成本分配：  **顶点变换的 GPU 成本构成：** - MVP 矩阵乘法：~8 FLOP/顶点（4x4 矩阵乘向量） - 法线矩阵变换：~6 FLOP/顶点 - 切线空间构建（TBN）：~15 FLOP/顶点 - 骨骼蒙皮（4 骨骼）：~50 FLOP/顶点  对于一个有 100k 顶点的场景，每帧顶点变换的计算量约 5~10 MFLOP——对现代 GPU 来说几乎不算什么。**几何阶段的真正瓶颈通常不是 ALU，而是：**  1. **顶点数据带宽**：从显存读取顶点数据的带宽`
    
34. `2. **顶点缓存命中率**：相邻三角形共享顶点，好的 Mesh 索引顺序能提高缓存命中 3. **小三角形效率**：当三角形投影到屏幕上小于 1 个像素时，几何处理成本 >> 片段着色成本（这是 Nanite 要解决的问题）`
    
    csharp // Unity C# 示例：顶点数据带宽优化 using UnityEngine; using UnityEngine.Rendering; public class VertexLayoutOptimizer : MonoBehaviour { // 演示如何减少顶点数据大小 void AnalyzeVertexLayout() { Mesh mesh = GetComponent<MeshFilter>()?.sharedMesh; if (mesh == null) return;
    
35. // 默认的 Unity 顶点：Position(12) + Normal(12) + Tangent(16) + UV(8) = 48 bytes/顶点 // 可以优化到：Position(12) + Normal(4,压缩) + Tangent(4,压缩) + UV(4,fp16) = 24 bytes/顶点  
    Debug.Log($"顶点数量: {mesh.vertexCount}"); Debug.Log($"估算带宽: {mesh.vertexCount * 48 / 1024f:F1} KB/帧（未优化）"); Debug.Log($"估算带宽: {mesh.vertexCount * 24 / 1024f:F1} KB/帧（优化后）");  
    // 在 Unity 2021.2+ 可以使用 VertexAttributeDescriptor 自定义顶点布局 // VertexAttributeDescriptor[] attrs = new VertexAttributeDescriptor[] // { // new VertexAttributeDescriptor(VertexAttribute.Position, VertexAttributeFormat.Float32, 3), // new VertexAttributeDescriptor(VertexAttribute.Normal, VertexAttributeFormat.SNorm8, 4), // 压缩法线 // new VertexAttributeDescriptor(VertexAttribute.TexCoord0, VertexAttributeFormat.Float16, 2), // fp16 UV // }; } }
    
36. `---  ## 八、总结：顶点旅程的设计哲学  把这六个空间串起来，能看到一条清晰的设计思路：  **每个坐标空间都是为了让某个特定操作最方便而设计的。**  - Model Space：让几何数据可复用 - World Space：让物理量有意义（光照、物理） - View Space：让投影矩阵形式简单 - Clip Space：让裁剪问题统一化 - NDC：让坐标独立于视口大小 - Screen Space：让坐标对应实际像素`
    
37. `MVP 矩阵不能随便合并，因为**不同阶段需要不同中间结果**。  裁剪在 Clip Space，因为**统一性使硬件实现极度简单**。  透视除法的非线性是物理投影的必然结果，**Z-fighting 不是 Bug 而是数学规律**——解决方案是 Reversed-Z、合理的 near/far 比值（建议 < 10000:1），或者 Logarithmic Depth。  Screen Mapping 的 OpenGL vs DirectX 差异是**历史遗留问题**，务必在自定义渲染管线中显式处理。`