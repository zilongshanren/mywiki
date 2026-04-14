---
tags: [shader, 纹理, 状态, 动画]
date: 2026-04-14
sources: 1
---

# 在纹理通道里编码状态

RGBA 纹理不必用来存"颜色"——R、G、B、A 四个通道各是一个独立 `float`（在 `TextureFormat.RFloat` 等高精度格式下）。把**非颜色的数值**塞进这些通道，就能让 shader 读到任意 per-pixel 状态，而不用每帧重传 uniform 或上传新 buffer。这是 Linden Reid 的 *Foggy Window Shader* 第 2-3 部分展示的核心 trick：把"玩家鼠标最后一次点在哪个像素、什么时间点的"直接存到一张纹理里，让 shader 自己算淡出。

## 典型工作流

1. **C# 侧**持有一张 `Texture2D`。
2. 用户交互（鼓标点击、粒子命中、AI 决策）时，把事件的**时间戳**或**强度**写进命中像素的某个通道：`texture.SetPixel(x, y, new Color(Time.timeSinceLevelLoad, 0, 0, 1))`。
3. `texture.Apply()` 上传到 GPU。
4. **Shader 侧**在 fragment shader 里 `tex2D(_MouseMap, uv).r` 读回这个时间戳，结合 `_Time.y` 算年龄：

   ```
   age = _Time.y - timeDrawn
   percentMaxAge = saturate(age / _MaxAge)
   ```

5. 用 `percentMaxAge` 驱动任何视觉参数：模糊半径、色调、透明度、位移……

## 为什么比 uniform 更好

Uniform / constant buffer 传的是**全局单值**，per-pixel 的状态只能靠纹理表达。替代方案是 structured buffer + 显式 index（shader model 5+），但代价是：

- 需要自己管理索引到像素的映射；
- 没有 hardware-filtering 的空间插值；
- 不能直接 `RenderTexture` 读写。

纹理方案的好处是**空间查询免费**：相邻像素的状态差异由 `tex2D` 的双线性插值自动处理，做"笔迹扩散""温度场"之类的效果时尤其顺手。

## 精度的陷阱

- 默认 `TextureFormat.RGBA32` 每通道只有 8-bit，存时间戳会迅速溢出（`Time.time` 累加到几秒就炸）。Reid 的教程专门用了 `TextureFormat.RFloat`（32-bit float）才能把 `_Time.y` 原样塞进 R 通道。
- 如果必须用 8-bit 纹理，经典做法是把一个高精度数字拆到多个通道里（RGBA = 32-bit packing），或者只存**相对时间**（`Time.time - lastRefreshTime`）。

## 相关用例谱系

- **Foggy window（Reid）**：R 通道 = 最后触碰时间，驱动 blur 淡出。
- **GPU 粒子**：位置、速度、寿命全部存在 `RenderTexture` 里，用 shader 迭代。
- **Flow map**：RG 通道 = 2D 方向向量，驱动水流/岩浆动画。
- **Thermal / damage map**：持续累计的场强，每帧 decay。
- **[[gpu-image-editor-brush]]**：同类思路——把"笔触状态"塞进纹理。

## 相关

- [[fragment-shader]]
- [[unity-grabpass-blur]] —— 同一篇教程的第 1 部分
- [[gpu-image-editor-brush]]
- [[motion-vectors]]
- [[linden-reid]]

## Sources

- [[sources/lindenreid-foggy-window-shader]]
