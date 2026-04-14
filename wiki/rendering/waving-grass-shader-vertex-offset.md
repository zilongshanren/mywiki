---
tags: [渲染, shader, vertex-animation, 植被, unity]
date: 2026-04-14
sources: 1
---

# 摆动草丛 Shader（顶点动画 + 世界空间风场采样）

[[linden-reid]] 2018 年 1 月的这一篇是她 shader 系列里最具代表性的**顶点动画**教程——目标是让整片草地「像风吹过一样」同步波动，但是要注意：每一株草都是独立的 mesh、有各自的本地坐标。如果在**局部空间**里做顶点 offset，每棵草会各走各的波，看不出风是从同一方向吹过的。整篇的设计都是围绕这个问题展开的——**怎么让独立 mesh 共享同一张"风场"**。

## 世界空间采样把风场变成全局函数

答案是把顶点变换到世界空间之后再用 `(x, z)` 去采一张梯度纹理：

```hlsl
float4 worldPos = mul(input.vertex, unity_ObjectToWorld);
float2 samplePos = worldPos.xz / _WorldSize.xz;      // 归一化到 [0,1]
samplePos += _Time.x * _WindSpeed.xz;                 // 沿风向平移采样位置
float windSample = tex2Dlod(_WindTex, float4(samplePos, 0, 0));
```

`_WorldSize` 是一个材质 Property，定义世界坐标范围，除法把世界坐标压缩到 `[0, 1]`——也就是风场纹理的 UV 空间。由于**所有草共用同一个材质和同一组 uniform**，`worldPos.xz / _WorldSize.xz` 对整片草地产生一个连续的标量场，每棵草在这个场上查到的值只取决于它在世界里的位置——**这就是"共享风"的成因**。

梯度纹理需要**左右无缝**（左右边缘像素色值一致），否则 `_Time` 平移采样到边界附近时会跳变、产生明显接缝。这是纹理制作时必须注意的点，shader 代码无法救。

## `frac` 把时间漂移的采样坐标拉回 0-1

`_Time.x * _WindSpeed.xz` 累加后 `samplePos` 很快超出 `[0, 1]`——需要靠 `frac()` 取小数部分让坐标回到 UV 合法范围：

```hlsl
return float4(frac(input.sp.x), 0, 0, 1);   // 调试时可视化 sample 位置
```

这里 Unity 的 `_Time.x = t / 20`（`_Time = (t/20, t, t*2, t*3)`），所以 `_WindSpeed` 通常要设得比较大、让有效速度显著。这是 [[shaping-functions|shaping function]] 的典型应用：`frac` 把递增的线性值转成周期性的锯齿波，等效于在采样空间里让风"无限地往一个方向吹"。

## 顶点位移：用风场值驱动 `sin/cos`

真正让草摆动的一行：

```hlsl
output.pos.z += sin(_WaveSpeed * windSample) * _WaveAmp * heightFactor;
output.pos.x += cos(_WaveSpeed * windSample) * _WaveAmp * heightFactor;
```

`windSample` 作为三角函数的相位——它在空间上连续变化、时间上平移，相当于在每个空间点喂入不同的相位，`sin/cos` 输出的就是连续平滑的波面。`_WaveAmp` 是幅度，`_WaveSpeed` 在这里并不是时间速度而是相位倍频——真正的时间速度是在 `samplePos += _Time.x * _WindSpeed` 那一步完成的。名字有点误导，但算法没错。

## `heightFactor`：让草根不动

一个现实的细节——草根粘在土里、草尖飞得最远。作者用两个 Properties 控制：

```hlsl
float heightFactor = input.vertex.y > _HeightCutoff;   // bool → {0, 1}
heightFactor *= pow(input.vertex.y, _HeightFactor);     // 高度越高幅度越大
```

第一行利用 HLSL 布尔到 float 的隐式转换——低于阈值的顶点拿到 0，草根彻底不动；高于阈值的乘上 `pow(y, k)`——幅度随高度**指数增长**，草尖飞得比中段更远。这精确对应了「现实中越远离根部越柔」的直觉。

评论区补了一个更好的思路：**用 UV 的 U 通道代替顶点 y**。好处是做 GPU instancing 或者 dynamic batching 把多株草合批成一个大 mesh 后，世界空间 y 不再反映"距离根部的距离"，但 UV 里可以预烘焙一个"沿着茎的归一化位置"——做 [[gpu-driven-grass-tiles|GPU 草叶绘制]] 时必须这样处理。

## 光照：ramp 采样复用

草的光照还是 cel shading——`dot(N, L)` 采样一张 ramp 纹理，和 [[cel-shader-outline|她的 cel shader]] 完全同构。顶点动画只改位置不改法线——理论上变形后法线失真，但草是薄片、幅度小、人眼看不出来，所以不重算法线是个常见的偷懒。真正需要重算的是**树叶厚片**或**大位移骨骼**场景。

## 全局风场的通用价值

这个 pattern 的价值远超「草」本身——**把任何全局现象编码进一张纹理，让每个物体在世界空间里对该纹理采样**——是整个风格化 shader 流派的通用方法：

- 风 → 本文的 wind texture
- 海浪 → Gerstner wave texture 或 heightmap
- 区域效果（魔法阵、死亡区） → 俯视图 splat 纹理
- 全局噪声动画（云、雾） → 滚动的 worley/perlin

它对比的是"在 CPU 侧生成每个物体的参数再下发"——后者灵活但带宽低，前者几乎零 CPU 工作量但需要场景整体尺度已知。这是 [[texture-encoded-state|用纹理编码状态]] 的另一种形态：把**空间上连续**的状态烘进纹理，采样替代计算。

## 相关

- [[cel-shader-outline]] —— ramp 光照的直接复用
- [[texture-encoded-state]] —— 把全局状态烘到纹理的通用范式
- [[shaping-functions]] —— `frac / sin / pow` 的塑形
- [[gpu-driven-grass-tiles]] —— GPU 侧的大规模草叶管线
- [[deferred-grass-shader]]
- [[painted-foliage-bent-planes]]
- [[unity-procedural-mesh]]
- [[linden-reid]]

## Sources

- [[sources/lindenreid-waving-grass-shader]]
