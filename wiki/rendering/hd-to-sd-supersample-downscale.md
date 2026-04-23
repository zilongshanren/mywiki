---
tags: [渲染, 反走样, 2d, 超采样, 下采样, sd, crt]
date: 2026-04-19
sources: 1
---

# HD 2D 游戏在 SD 电视上的超采样下采样

2D 游戏的美术按 1920×1080 画好，直接跑在 720×576 的 SD CRT 上，**理论上应该更清晰**——毕竟有多余像素可丢。[[joost-van-dongen|Joost]] 在 Swords & Soldiers 和 Awesomenauts 上实测：**"太清晰"反而是问题**。

## 为什么直出更糟

3D 有 mipmap + 实时 AA 在硬件层处理缩放；**2D 游戏的反走样是画在美术里的**——艺术家在 Photoshop 里画好了边缘渐变。当 HD 纹理直接渲染到 SD 屏上：

- **1 像素宽的细节会闪烁**：随着角色移动，这些细节有时落在像素上、有时落在两像素之间。
- **预画的反走样边缘消失**：Photoshop 里做的 edge blend 是给 HD 像素用的，SD 降采样时这些像素被整体跳过，等于丢掉了 AA。

结果是"又糙又噪"——在 CRT 上实际观感比 HD 屏差。

## 解法：HD 内部渲染 + 下采样到 SD

标准的 supersampling 做法——只不过用途反过来：**不是为了超过 native 分辨率，而是为了**稳定地降到 native 分辨率。

流程：

1. 内部渲染到比 SD 高的 offscreen target；
2. 用一个 box/average 过滤下采样到最终 SD 尺寸；
3. 每个屏幕像素取覆盖区域内多个样本的平均。

这样细节不会因为位置错开而闪烁——它们被平均成"略淡"的颜色贡献，而不是完全消失。这是 [[msaa-ssaa|SSAA]] 的使用，但因为 2D 不存在覆盖/深度的复杂性，直接"高分辨率渲染 + box filter"就够。

## 1.5× 已经够了

直觉选 2×（1440×1152）最干净——每个输出像素正好 4 个输入样本。但这**很贵**，以至于早期版本里 SD 模式帧率比 HD 还差。Joost 实测把内部分辨率降到 **1.5×（1080×864）** 已经足够把闪烁压下去，性能余量回来。再降下去就看得出锯齿。

## 为什么不预先在资源层降采样

评论区有人问：何不在加载时把纹理按 SD 分辨率 resample 一次，运行时不用 supersample？Joost 给了三条硬性反对理由：

1. **工作量**：资源用 DDS 存。加载时 resample 意味着 decode DDS → resample → 重新 encode DDS。DDS 编码很微妙（block 参数选择不当会塌画质），要额外引 encode 库。
2. **画质下降**：DDS 压缩对"细节/分辨率"比敏感——砍一半分辨率会把压缩 artifact 放大。动画角色尤其容易显。
3. **加载时间**：200 MB 纹理全走 decode→resample→re-encode 流程要耗可观的加载时间。

而且内存不是问题——HD 版能装下，SD 版当然也能。运行时 supersampling 反倒把流程保持简单（**同一套资源全平台**）。

## 启发

- 2D 项目缩放不是免费的；**美术里的预画 AA 对分辨率敏感**，降采样时会崩。
- "高分辨率渲染 + 下采样"是 2D 反走样里最粗暴也最稳的方式——不需要 shader 改动，box filter 就够。
- 选 1.5× 这种非整倍过采样常被忽视，但它在性能/质量曲线上有个甜点。整数倍采样看起来理论干净，但实际往往用不起。
- 这个模式也适用于**高分辨率原美术下到中低端手机**，比如 iPad→iPhone 或旧安卓的适配。

## 相关

- [[msaa-ssaa]] —— 全屏 SSAA 是同一技法，用在 3D 管线
- [[temporal-supersampling]] —— 多帧摊分样本的现代替代
- [[aliasing]]
- [[image-resampling-filters]]
- [[dynamic-resolution-scaling]]
- [[joost-van-dongen]]

## Sources

- [[sources/joostdevblog-hd-2d-on-sd]]
