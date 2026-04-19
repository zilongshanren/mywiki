---
tags: [渲染, post-processing, blur, depth, gaussian, unity]
date: 2026-04-19
sources: 1
---

# 深度感知高斯模糊与稀疏核优化

常规的[[separable-gaussian-blur|可分离高斯模糊]] blur 整张图，对后处理的很多场景是错的：如果你在模糊"屏幕空间阴影 mask"、或者一张"边缘检测结果"，你不希望模糊**跨越物体边界**——跨边界的模糊会让前景物体的阴影/线条"溢出"到后景上，最典型症状是一个角色的轮廓线漏到它后面的墙上。[[daniel-ilett|Daniel Ilett]] 在 2024 年的 Mystery Dungeon sketch shader 里加了两条工程优化来对付这类问题：**depth-aware kernel** 和 **稀疏采样步长**。

## Depth-aware 核：按深度门禁丢样本

核心思路：在 blur 循环里除了采目标纹理，**同时采深度纹理**；如果样本像素和中心像素的深度差超过阈值，就**跳过这个样本**、不计入加权和，也不累加权重。深度接近的邻居才参与模糊，深度差大的邻居被当作"不同物体、不该溢过去"。

```hlsl
float depth = sampleDepth(i.texcoord);
float3 col = 0;
float kernelSum = 0.001;               // 防止除零
for (int x = lower; x <= upper; x += _BlurStepSize) {
    float2 uv = i.texcoord + float2(_BlitTexture_TexelSize.x * x, 0);
    float newDepth = sampleDepth(uv);
    if (newDepth > 0.001 && abs(depth - newDepth) < _DepthSensitivity) {
        float gauss = gaussian(x);
        kernelSum += gauss;
        col += gauss * SAMPLE_TEXTURE2D(_BlitTexture, sampler, uv);
    }
}
col /= kernelSum;                      // 按实际采到的权重归一化
```

两个关键细节：

- **动态归一化**：被丢弃的样本也不计入分母，不然边界处亮度会骤降。`kernelSum` 累计实际贡献的权重，最终 `col / kernelSum` 保证边界像素和内部像素都按"它们各自采到的有效权重"正确归一。
- **`newDepth > 0.001` 过滤天空**：深度等于 0（或非常接近 0）通常是天空或未写入深度的像素，必须跳过否则会在地平线附近留一圈 artifacts。
- **各向同性**：这个技巧在 horizontal 和 vertical 两 pass 都做，两次 pass 共用同一个 `_DepthSensitivity` 阈值。`0.002` 左右是经验值——对应 reversed-Z 下大约几十厘米的物理距离。

## 稀疏核：用 `_BlurStepSize` 跳样本

传统可分离 Gaussian kernel 大小 N 需要 2N 次采样（横竖各一遍）。要做**大半径模糊**（例如 kernel size = 100，用于让阴影"发散"出去很远）这是 200 次采样，即使分离了仍然肉疼。

观察：大半径 Gaussian 的权重分布本身就平滑，**跳着采**一些像素对最终结果的影响在感官上很小，但采样次数能砍一半、四分之一甚至更多。

```hlsl
for (int x = lower; x <= upper; x += _BlurStepSize) {  // 步长 1,2,4,...
    ...
}
```

`_BlurStepSize = 1` 是标准 Gaussian；`= 2` 跳过一半样本、计算量减半；`= 4` 只采 25%。配合权重归一化（因为采样数变了，`kernelSum` 也会变），视觉质量降级很轻微，尤其是 blur 半径本身就大的时候——模糊本来就在"抹平细节"，采样密度稀一点人眼识别不出来。这和数字信号处理里的 **decimation** 是同一套思路：采样少 → 会引入 aliasing，但如果后面还要做大幅度 low-pass（blur 本身就是），aliasing 会被随之压掉。

## 两套优化的互补性

两套优化针对不同资源：

- **Depth-aware** 节省的是**视觉质量**——大 blur 核的主要问题是跨边界溢出，而不是计算量。
- **稀疏步长**节省的是**计算**——大核的主要成本是采样次数。

在大 blur 半径场景（Ilett 的 Mystery Dungeon 阴影延展用到 kernel size 最高 500）两个都开，才既避免溢出、又能跑到交互帧率。

## 代价和限制

- **分支跳过样本**需要 GPU 在 warp 内分歧路径——如果邻居像素的深度分布差异大（例如靠近物体边缘），同一个 warp 里有些线程走分支、有些不走，实际加速会打折扣。但大多数场景里连续屏幕像素的深度是**空间相关**的，divergence 在 blur 这种局部操作里不严重。
- **稀疏采样不是所有 blur 都能用**：对小半径（例如 kernel size ≤ 5）稀疏完 Gaussian 形状就崩了，稀疏的甜区在 50+ 的大核。
- **深度阈值需要场景自适应**：远景物体间深度差大，阈值要放宽；近景要收紧。Ilett 暴露 `extendDepthSensitivity` 作为 volume 参数留给美术调。

## 相关

- [[separable-gaussian-blur]] — 可分离的基本形
- [[bloom-threshold-blur-composite]]
- [[depth-aware-upsampling]] — 姊妹技巧：上采样时用深度做边界保护
- [[image-convolution-kernel]]
- [[mystery-dungeon-sketch-shadows]] — 这套 blur 的具体使用场景
- [[scene-color-depth-nodes]]

## Sources

- [[sources/danielilett-mystery-dungeon-sketches]]
