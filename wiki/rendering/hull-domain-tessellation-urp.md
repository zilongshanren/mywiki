---
tags: [shader, urp, hlsl, tessellation, hull, domain, vertex-shader]
date: 2026-04-19
sources: 1
---

# Hull / Domain Tessellation 在 URP 的基础用法

Tessellation 是 DX11 / OpenGL 4 时代引入的可编程管线扩展——让 GPU 在 vertex shader 之后、光栅化之前**动态产生新顶点**。URP 支持（但 Shader Graph 不支持，只能手写 HLSL）；HDRP 的 Shader Graph 支持。这页讲 URP 下写 Hull/Domain shader 的**骨架**和几个必须理解的概念——真正的应用场景（[[tessellation-fur-rendering|毛发 isoline]]、displacement 水面、地形细分）都基于同一套骨架。

## 管线三阶段

```
appdata ──▶ vert ──▶ [tessControlPoint] ──▶ hull ──▶
                                               │
                                               ▼
                                        tessellator
                                       (固定功能，读 tessFactors，在
                                        归一化参考域输出 barycentric
                                        坐标的新顶点)
                                               │
                                               ▼
                          [新 tessControlPoint + barycentric]
                                               │
                                               ▼
                                           domain ──▶ [t2f] ──▶ frag
```

- **vert** 依然跑一次 per 原 mesh 顶点——但它**不再输出 clip space 位置**，而输出一个"还未光栅化"的中间结构 `tessControlPoint`（含 world-space position + UV 等），语义用 `INTERNALTESSPOS` 而非 `SV_POSITION`。
- **hull** 分两部分：
  - **control-point 函数**（per 控制点跑一次，本例用 `[patchconstantfunc(...)]` attribute 注册）——接 `InputPatch<tessControlPoint, 3>` 和 `uint id : SV_OutputControlPointID`，常见做法就 `return patch[id]` 原样转发。
  - **patch-constant 函数**（per patch 跑一次）——返回 `tessFactors { float edge[3]:SV_TessFactor; float inside:SV_InsideTessFactor; }`，告诉 tessellator 每条边和中心各切几段。
- **tessellator**（固定功能）——按 factor 在抽象的归一化参考域（三角形 / 四边形 / isoline）上撒新点，输出它们的 barycentric 权重。**它不知道 patch 是什么**，只管几何域。
- **domain** 函数（per 新顶点跑一次）——拿 `SV_DomainLocation` 的 barycentric 权重和原 patch 的 3 个控制点，**自己插值**出新顶点的全部数据（position、uv、normal…）。displacement 数学（wave、高度图采样）**放在这里**，不是 vert 里。

## hull shader 的 5 个 attribute

hull 函数头必须有这 5 个 attribute，缺一报错：

```hlsl
[domain("tri")]                       // tri / quad / isoline
[outputcontrolpoints(3)]              // 输出 patch 大小（通常等于输入）
[outputtopology("triangle_cw")]       // triangle_cw / triangle_ccw / line
[partitioning("integer")]             // integer / fractional_even /
                                      //   fractional_odd / pow2
[patchconstantfunc("patchConstantFunc")]
tessControlPoint hull(
    InputPatch<tessControlPoint, 3> patch,
    uint id : SV_OutputControlPointID)
{
    return patch[id];
}
```

**partitioning 选项**的取舍：

- `integer` —— tessellation factor 取整，细分数之间突变，均匀间距。
- `fractional_even` / `fractional_odd` —— 允许非均匀间距，**支持平滑过渡**（距离淡出场景的首选），向最近的偶数 / 奇数取整。
- `pow2` —— 在 Ilett 的机器上表现和 `integer` 一样，不一定所有硬件都支持。

**outputtopology** 对应常用的前两种三角形 winding（CW 一般是 front face）和 isoline 模式。毛发 / 草这种细线几何用 `"line"` —— 见 [[tessellation-fur-rendering]]。

## patch constant function：告诉 tessellator 切多细

最简版（全 patch 统一 factor）：

```hlsl
tessFactors patchConstantFunc(InputPatch<tessControlPoint, 3> patch)
{
    tessFactors f = (tessFactors)0;
    f.edge[0] = f.edge[1] = f.edge[2] = _TessellationAmount;
    f.inside  = _TessellationAmount;
    return f;
}
```

**硬件上限** `_TessellationAmount = 64`（Ilett 的机器；多数桌面 GPU 同值）。

**距离淡出** 更实用：每条边中点到 `_WorldSpaceCameraPos` 的距离在 `[fadeStart, fadeEnd]` 区间里线性 remap 到 `[0, 1]`，用它乘 `_TessellationAmount` 得到实际 factor。**最后用 `max(factor, 1)` 兜底**——factor = 0 会让整个 patch 在 tessellator 里被丢掉，mesh 出现空洞。

## domain shader：在新顶点上做真实数学

```hlsl
[domain("tri")]
t2f domain(
    tessFactors factors,
    OutputPatch<tessControlPoint, 3> patch,
    float3 barycentricCoordinates : SV_DomainLocation)
{
    t2f i = (t2f)0;
    float3 posWS = patch[0].positionWS * barycentricCoordinates.x
                 + patch[1].positionWS * barycentricCoordinates.y
                 + patch[2].positionWS * barycentricCoordinates.z;
    float2 uv    = patch[0].uv * barycentricCoordinates.x
                 + patch[1].uv * barycentricCoordinates.y
                 + patch[2].uv * barycentricCoordinates.z;
    // displacement 在这里做（sin wave / 采高度图 / 毛发展开……）
    float y = posWS.y + sin(posWS.x + posWS.z + _Time.y) * _WaveHeight;
    i.positionCS = TransformWorldToHClip(float3(posWS.x, y, posWS.z));
    i.uv         = uv;
    return i;
}
```

**barycentric 权重三个之和恒为 1**。`(1,0,0)` 落在第一个控制点上、`(0.333, 0.333, 0.333)` 在三角形中心。quad 拓扑下坐标变成 `float2`，更像传统 UV。

## 注册：两个 #pragma

ShaderLab 不知道 `hull` 和 `domain` 这两个函数名是什么（即使命名一致）——必须显式告诉编译器：

```hlsl
#pragma vertex vert
#pragma fragment frag
#pragma hull hull
#pragma domain domain
```

## 性能注意

Tessellation 在现代硬件上**不是免费午餐**：每个新顶点都跑一次 domain shader、光栅化出的 fragment 数量也按新拓扑膨胀。典型坑——Ilett 自述曾给客户发过一个把 factor 硬编码在 64 的 shader，性能很难看。实践建议：

- 默认 factor 保守（4–8），给 artist 留空间调。
- 一定配**距离淡出**——远景看不出差异但每 patch 省大半算力。
- patch 级 early-out：背对相机的 patch 把 factor 填 0 让 tessellator 直接跳过（用 backface cull 或 view direction + normal 的简单判断）。

## 和 fur isoline 的关系

[[tessellation-fur-rendering|Kostas Anagnostou 的毛发方案]] 用同样的管线但换 domain：`[domain("isoline")]` + `outputtopology("line")`，把 U/V 两个方向分别当作"第几根毛 / 第几段"，用 domain shader 生成真正的毛几何。管线骨架一模一样，只是 factor 的语义和 domain 里的坐标解释不同。

## 相关
- [[tessellation-fur-rendering]] —— isoline domain 的专项应用
- [[vertex-shader]] —— tessellation 之前的阶段
- [[shaderlab-hlsl-basics]] —— `#pragma` 注册和 CBUFFER 组织
- [[coordinate-spaces]] —— 在哪个空间做 displacement 的取舍
- [[tessellation-approaches-overview]] —— Karis 对 D3D hardware tessellator 拓扑均匀方案的批评：密度均匀比拓扑均匀省 31% 三角形
- [[nanite-tessellation-approach]] —— UE5.4 脱离 D3D tessellator 的软实现

## Sources

- [[sources/danielilett-shader-code-vertex-tessellation]]
- [[sources/graphics-guy-tessellation-dx11]] — Cao 2015：DX11 tessellation 管线三阶段 + partitioning 选项 + crack 成因
