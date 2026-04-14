---
tags: [rendering, shader, post-processing, color, unity]
date: 2026-04-14
sources: 1
---

# 夜色全屏后处理：饱和 / 蓝偏 / 变暗的三合一

一种廉价、几乎零资产成本的「白天染成夜晚」全屏后处理配方，[[harry-alisavakis]] 在 *My take on shaders* 系列第二篇用它给他的手游 Sling Toss 做昼夜切换。技术上是一个建立在 [[unity-image-effect-basics]] 骨架上的 [[fragment-shader]]，加一个 `_NightTime ∈ [0.001, 1]` 滑杆做权重。

## 三条色彩操作为何缺一不可

作者的经验是：「变夜晚」这个感觉必须同时做三件事才能骗过眼睛，单独做任何一条都会露馅——

- **只抽饱和**：画面只是变成灰色怀旧照，没有昼夜感
- **只加蓝**：像给照片贴了蓝色玻璃纸，假而平
- **只变暗**：像关灯，物件的色温没变

所以 shader 把三者揉在一起。实现上先用 Unity 内置的 `Luminance(col.rgb)` 算出灰度值 `lum`（按 Rec.601/709 的感知加权），然后 `lerp(col.rgb, fixed3(lum, lum, lum), _NightTime)` 把颜色向灰度推进——这等价于一个手动实现的饱和度滑块。接下来一行表达式同时完成蓝偏和变暗：

```hlsl
return (output + _NightTime * fixed4(0, 0, 0.8, 1)) * (1 - _NightTime);
```

`+ _NightTime * fixed4(0, 0, 0.8, 1)` 把蓝通道线性抬高，`* (1 - _NightTime)` 把整体亮度按权重压低，`_NightTime = 0` 回到白天、`_NightTime = 1` 是全灰 + 蓝染 + 几乎全黑。数学上这个组合并不精确正确（加蓝后又乘系数会轻微调制蓝色的饱和），但在美术调参的范围内效果够好，关键是所有系数都挂在一个权重下，调一根滑杆就能做淡入淡出。

## 实战里的两个细节

**选择性不应用**：Sling Toss 里玩家角色保持原色不受夜色影响，靠的是经典的多相机分层 workaround——把角色放在独立 layer、独立相机，只给环境相机挂这支 image effect。这是 built-in 管线时代做选择性后处理最省事的土法；URP/HDRP 下应改用 Volume 优先级 + Layer Mask 或自定义 pass，因为不能再往 `OnRenderImage` 上挂东西。

**时代痕迹**：原文是 Unity 5.6 时代，代码里用的是 `UnityObjectToClipPos(v.vertex)`，刚好是 Unity 从 `UNITY_MATRIX_MVP` 过渡到推荐宏的节点。把这支 shader 迁移到现代 URP 的主要修改是换头文件、走 [[blit-render-feature]]、加 `UNITY_VERTEX_INPUT_INSTANCE_ID`，核心的三行颜色数学可以原封不动复用。

作为一个教学示例，这支 shader 的价值是把「用 lerp + 一个权重把多个色彩操作参数化」的思路具象化了——同样的模板可以换成「黄昏（橙染 + 弱暗）」「水下（绿染 + 模糊 + 折射）」「恐怖（高对比 + 青染 + 暗角）」等等。

## 相关

- [[unity-image-effect-basics]]
- [[fragment-shader]]
- [[shaderlab-hlsl-basics]]
- [[harry-alisavakis]]

## Sources

- [[sources/halisavakis-night-time-shader]]
