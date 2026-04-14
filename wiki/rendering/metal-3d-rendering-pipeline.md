---
tags: [渲染, metal, 光照, blinn-phong, 深度测试, vertex-descriptor, 教学]
date: 2026-04-14
sources: 1
---

# Metal 下的最小 3D 渲染管线（OBJ → 光照 → 深度）

[[warren-moore|Warren Moore]] 的 *Up and Running with Metal, Part 3* 把 Metal 的最小渲染链路从 Part 2 的「2D 三角形」升级成「带 Blinn-Phong 光照、可手势旋转的茶壶」。这一跳引入的**四类新对象**——模型资产、uniform 缓冲、vertex descriptor、depth/stencil state——正好构成一条从 [[metal-api-overview|Metal API]] 往 3D 渲染迈出的最小步骤表。这一页把这四件事按从 CPU 资产到 GPU 绑定的顺序串起来。

## 资产：OBJ 模型与 index buffer

文章选的资产是 Utah 茶壶 OBJ。OBJ 格式存顶点位置、法线、纹理坐标、面，以 ASCII 行列出，Warren 写了一个自家的迷你 parser，输出一对连续数组：`vertices`（`Vertex` 结构数组）与 `indices`（uint16 数组）。index buffer 的意义是**复用顶点**——相比直接存 `3 × faceCount` 个顶点，Index 数组只需要存 int16 偏移，能在模型封闭、法线平滑共享时节省大量内存。

评论区补了一个值得记住的反例：**不平滑的 cube 无法通过 index buffer 节省**——6 个面需要 6 组不同法线，每个顶点要出现 3 次才能给三条相邻面提供正确的 `normal`，所以 cube 的 24 个「带法线顶点」恰好没有任何两个相同，indexing 退化成无用功。Index buffer 的收益只出现在**顶点—属性组合**被多次共用的模型上，smoothing group 是典型场景。

## Uniform：modelView / MVP / normalMatrix 三矩阵

Part 2 只需要一个 NDC 下的静态三角形，Part 3 里每一帧都要把旋转角度送进 shader。Warren 把需要每帧更新的数据打进一个 C 侧结构：

```c
typedef struct {
    float4x4 modelViewMatrix;
    float4x4 modelViewProjectionMatrix;
    float3x3 normalMatrix;
} Uniforms;
```

- **`modelViewProjectionMatrix`** 是 [[mvp-transform|MVP]] 的预乘结果，顶点 shader 直接用它把 object-space 位置推到 clip space。
- **`modelViewMatrix`** 保留下来是因为 fragment shader 里的光照要在 **view space** 里做（光源方向和视线方向都以 view space 为基准）——需要 view-space 位置就从这一矩阵出发。
- **`normalMatrix`** 是 `transpose(inverse(modelView))` 的 3×3 上角。普通点位置乘 M 即可，但**法线乘 M 会被非均匀缩放扭歪**——只有 `M⁻ᵀ` 才保留法线垂直性。这条规则本身值得单独记一笔；CPU 侧每帧算 `transpose(inverse(...))` 是可接受的开销，因为只有一次矩阵构造，不是逐顶点计算。

每帧把这个结构拷进一个 `MTLBuffer` 里，在 encoder 上以 `setVertexBuffer:atIndex:1` 和 `setFragmentBuffer:atIndex:0` 绑定，shader 侧就能用 `constant Uniforms &uniforms [[buffer(n)]]` 读到。

## Vertex Descriptor：告诉 Metal 你的顶点长什么样

[[metal-shading-language-basics|MSL]] 里的 `[[stage_in]]` 依赖 CPU 侧显式描述顶点的内存布局。做法是填一个 `MTLVertexDescriptor`：为每个 attribute 指定 `format` / `bufferIndex` / `offset`，再为每个 layout 指定 `stride` 与 `stepFunction`。

Warren 的茶壶用**interleaved 布局**——position 和 normal 连续放在同一个 buffer 里，`stride = sizeof(float) * 8`、normal 的 `offset = sizeof(float) * 4`。为什么首选 interleaved？评论区里 Warren 从 Apple 工程师处转述了原因：**cache coherency**——一个顶点的全部属性物理相邻存放，shader 读完 position 后取 normal 几乎必然命中 L1。把 position / normal / uv 拆到三个独立 buffer（俗称 SoA）在流式生成顶点的场景里有意义，但对离线模型来说会损失局部性。

Vertex descriptor 绑定在 **pipeline state 上**，改变它需要重新创建 pipeline——因此不同 vertex 格式的材质组合数决定了你要维护多少个 pipeline state。

## Depth / Stencil State：让 Z 正确

2D 三角形没有 Z 遮挡问题，3D 场景则必须配一个 `MTLDepthStencilState`：

```objc
MTLDepthStencilDescriptor *desc = [MTLDepthStencilDescriptor new];
desc.depthCompareFunction = MTLCompareFunctionLess;
desc.depthWriteEnabled = YES;
self.depthStencilState = [device newDepthStencilStateWithDescriptor:desc];
```

以及 `setFrontFacingWinding:` 与 `setCullMode:` 两把手——前者告诉 Metal 哪个缠绕方向算正面（Warren 选逆时针 CCW，与右手系一致），后者把背面的三角形裁掉省一次 fragment shader 调用。深度附件本身要在 [[metal-api-overview|`MTLRenderPassDescriptor`]] 的 `depthAttachment` 上配，否则 runtime 会报 `validateDepthStencilState` 的断言失败（评论里正好有人踩过这个坑）。见 [[z-buffer|深度缓冲]] 的通用原理。

## Fragment shader：搬进 view space 的 Blinn-Phong

光照在 fragment shader 里按 [[normalised-blinn-phong-shader|Blinn-Phong]] 的未归一化老版本写：

```metal
float3 ambient = light.ambientColor * material.ambientColor;
float3 N = normalize(vert.normal);
float NdotL = saturate(dot(N, light.direction));
float3 diffuse = light.diffuseColor * material.diffuseColor * NdotL;
float3 specular = 0;
if (NdotL > 0) {
    float3 V = normalize(vert.eye);
    float3 H = normalize(light.direction + V);
    float f = pow(saturate(dot(N, H)), material.specularPower);
    specular = light.specularColor * material.specularColor * f;
}
return float4(ambient + diffuse + specular, 1);
```

两个细节：`saturate` 截断负的 `NdotL`，否则背光面会得到负光；halfway vector **取 `normalize(L + V)` 而不是简单相加除 2**，避免数值不稳定。diffuse 为 0 时主动跳过 specular 计算是个小的分支优化——当面已经背光，specular lobe 就算再尖也没意义。这就是 [[shader-vector-math-primer|向量点乘]] 在真实 shader 里的样子：三次 `dot`、两次 `normalize`、加起来就是一整套 per-pixel lighting。

## 相关

- [[metal-api-overview]] —— 把 Part 3 的新对象塞进 device/queue/encoder 的对象图
- [[metal-shading-language-basics]] —— MSL 函数限定符与 `[[stage_in]]` 的由来
- [[mvp-transform]] —— Uniform 里那三把矩阵的几何含义
- [[shader-vector-math-primer]]
- [[diffuse-lighting-lambertian]] —— `N·L` 的物理解释
- [[normalised-blinn-phong-shader]] —— Blinn-Phong 在 PBR 时代的归一化版本
- [[z-buffer]]
- [[warren-moore]]

## Sources

- [[sources/metalbyexample-up-and-running-3]]
