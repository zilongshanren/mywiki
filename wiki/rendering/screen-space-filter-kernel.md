---
tags: [渲染, 屏幕空间, 滤波, 阴影, 次表面散射, 后处理]
date: 2026-04-27
sources: 1
---

# 屏幕空间大滤波核（Screen-Space Filter Kernel）

把阴影柔化、GI、皮肤次表面散射、头发光照等需要空间模糊的着色操作**放到屏幕空间**完成，比世界空间或对象空间的对等方案更具扩展性——因为滤波核的开销由屏幕分辨率而非场景复杂度决定。这是[[people/wolfgang-engel|Wolfgang Engel]] 2011 年提出的图形子系统三条设计规则之一（另两条：禁用查找表、均匀误差分布）。

## 为什么要到屏幕空间

随着可用算力的增加而内存带宽的增长陷入瓶颈，在屏幕空间对已有的 G-Buffer 数据做计算比反复读取世界几何更省带宽。后处理管线（[[rendering/deferred-rendering|延迟渲染]] 下的 DoF、MotionBlur、Tone Mapping）是最成熟的案例；更进一步，复杂材质（皮肤、头发）和阴影/GI 滤波也可以在屏幕空间完成——代价是引入一组工程挑战。

## 三个核心挑战

### 1. 基于相机距离缩放采样步长

同一个世界空间半径在不同深度对应截然不同的像素面积。滤波核若使用固定像素步长，近处会欠采样、远处浪费算力。解法是用线性化深度驱动步长：

```hlsl
// 线性化双曲深度，Q = FarClip / (FarClip - NearClip)
float depthLin = (-NearClip * Q) / (Depth - Q);

// 采样步长反比于距离的平方（类光衰减函数）
sampleStep.xy = float2(1.0, texelRatio) * sqrt(1.0 / (depthLin * depthLin * bias));
```

`bias` 是美术可调的缩放参数；`texelRatio`（像素宽高比）保证各向等尺度。

### 2. 各向异性滤波核

对皮肤 SSS 或毛发光照，沿几何表面方向拉伸滤波核能获得更物理正确的结果。通过世界空间法线与视角向量的点积可以估算表面朝向屏幕的程度，取平方根得到一个 \[0, 1\] 的各向异性系数：

```hlsl
float aniso = saturate(sqrt(dot(viewVec, normal)));
```

将这个系数乘进椭圆形滤波核的长轴方向，即在几何法线接近屏幕法线时保持圆形、倾斜时自动压扁。

### 3. 深度差异剔除

宽滤波核不加限制地跨越几何边界会把阴影/GI/SSS 值涂抹到角落之外，产生明显的光晕瑕疵（halo）。标准做法是对每个采样点检验其深度与滤波核中心深度之差：

```hlsl
bool isValidSample = (abs(sampleDepth - centerDepth) < errDepth);
if (isValidSample && isShadow) {
    sumWeightsOK += weight;
    shadowAcc    += sampleShadow * weight;
}
```

`errDepth` 是一个用户可调阈值，决定"跨越几何"的判定灵敏度。被拒绝的采样在权重归一化时剔除，不参与最终值。

## 应用场景

- **阴影柔化（软阴影）**：多点椭球光源的阴影收集器存入屏幕空间后统一滤波
- **屏幕空间 SSS**：皮肤的多散射轮廓函数在屏幕空间 splat
- **屏幕空间头发光照**：沿切线方向的各向异性高光在屏幕空间扩散
- **GI 遮蔽/辐照度模糊**：SSAO、HBAO 的降噪滤波

## 局限

这类方案的本质缺陷是**屏幕空间的信息丢失**：被遮挡的几何无法参与滤波，物体边界处总存在欠采样风险。深度差异剔除只能减轻、不能消除伪影。Engel 自己也把"合理的偏差值"称为"magic value"，说明实践中仍需经验调整。

## 相关

- [[rendering/deferred-rendering]] —— 这类滤波核的典型宿主：G-Buffer 已经存好了法线/深度
- [[rendering/screen-space-shadow-map-urp]] —— 屏幕空间阴影的 URP 实现
- [[rendering/msaa-ssaa]] —— 屏幕空间操作和 MSAA 的交互
- [[people/wolfgang-engel]] —— 提出此规则的作者

## Sources

- [[sources/humus-screen-space-rules]]
