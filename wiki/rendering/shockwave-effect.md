---
tags: [渲染, unity, shader, 后处理, vfx, 冲击波]
date: 2026-04-14
sources: 1
---

# 冲击波效果（Shockwave / 径向 UV 位移）

游戏里那种「角色被打中、镜头中心炸开一圈像水波一样向外扩散的扭曲」就是**径向 UV 位移**——本质上是 [[uv-displacement-image-effect|UV displacement]] 和 [[custom-mask-shaders|in-shader 圆环 mask]] 的最小拼接。它的出现频率高得离谱：《Move or Die》的死亡动画、《以撒的结合》的 boss 砸地反馈、几乎任何带「命中力度」的 2D / 3D 游戏都用得上。

## 公式：圆环 mask × 一次重新采样

[[harry-alisavakis|Harry Alisavakis]] 在 *My take on shaders* 第七篇里把它写得几乎令人失望地简单——把 [[custom-mask-shaders|圆环 mask shader]] 的 `circleAlpha` 拿来当位移强度，然后把 `_DisplacementAmount` 乘上去当 UV 偏移：

```hlsl
// 与 ring mask 完全一样的前半段
float dist        = length(float2(i.uv.x - _CenterX, i.uv.y - _CenterY) * float2(_SizeX, _SizeY));
float rd          = _Thickness / 2;
float rc          = _Radius - rd;
float circle      = saturate(abs(dist - rc) / _Thickness);
float circleAlpha = pow(circle, pow(_Hardness, 2));
half  mask        = (_Invert > 0) ? circleAlpha * _Invert : (1 - circleAlpha) * (-_Invert);

// 唯一的新增部分
float2 displ_uv   = i.uv + mask * _DisplacementAmount;
return tex2D(_MainTex, displ_uv);
```

唯一新增的就是最后两行：用 mask 的灰度值乘上一个标量位移量当 UV 偏移，再 `tex2D` 取一次原 framebuffer。圆环外侧的像素 mask 是 0、不动；圆环最暗的中心带 mask 最大、被最大幅度位移；中间过渡。这就是「冲击波」的视觉本质——**只在那一圈窄环上把屏幕揉一下**。注意位移方向是 `(mask, mask)`，不是径向单位向量；之所以看起来还像是从中心向外推，是因为环形 mask 自身就以圆心对称，沿 (1, 1) 方向偏移会自动产生「环上每一点都在向某一侧推像素」的错觉，配合短暂的动画时长，肉眼就把它看成了「水波扩散」。要更物理一点也可以把 `(mask, mask)` 换成 `mask * normalize(uv - center)`，让位移真正沿径向。

## 触发：协程驱动 `_Radius` 从「不可见」到「冲出屏幕」

shader 本身只描述「某一帧的画面长什么样」，要让它**动**起来需要外面有个脚本驱动 `_Radius` 单调变化：

```csharp
void Update() {
    if (Input.GetButtonDown("Fire1")) {
        Vector2 screenPos = new Vector2(
            Input.mousePosition.x / Screen.width,
            Input.mousePosition.y / Screen.height);
        shockWaveMaterial.SetFloat("_CenterX", screenPos.x);
        shockWaveMaterial.SetFloat("_CenterY", screenPos.y);
        StopAllCoroutines();
        StartCoroutine(ShockWaveEffect());
    }
}

IEnumerator ShockWaveEffect() {
    float t = 0;
    while (t < 1) {
        t += Time.deltaTime * 2;
        shockWaveMaterial.SetFloat("_Radius", Mathf.Lerp(-0.2f, 2f, t));
        yield return null;
    }
}
```

几个值得注意的工程细节：

- **从 `-0.2f` 起步**而不是 `0`：让圆环初始时整体在屏幕「外围更外」，避免一开始有半圈可见。
- **结束在 `2f`**：超出屏幕对角线长度，圆环已经完全跑出 [0, 1] UV 范围，自动消失。
- **`StopAllCoroutines()`**：保证连续点击不会让多个冲击波叠加。
- **center 用屏幕坐标 `[0, 1]`**：和 shader 内部 UV 一致，不是像素坐标。

## 美术堆叠：单独看很弱，叠起来很爽

Alisavakis 反复强调单看冲击波很「平」，要变成有力的命中反馈需要堆叠：**屏幕震动 + [[chromatic-aberration-post|色差]] + 短暂的全屏闪白 / 黑场 + 音效**。冲击波本身只是其中一层 UV 扰动，但它是「让屏幕看上去真的被力量击穿了一下」的视觉锚点。

整支 shader 的真正价值不在于代码本身——它真的只是 [[custom-mask-shaders|圆环 mask]] 加一行 [[uv-displacement-image-effect|UV displacement]]——而在于演示了「shader 模块化拼装」的思维：每一层效果（生成遮罩、用遮罩驱动位移、用脚本驱动遮罩参数）都可以独立替换。把圆环换成菱形、把 UV 位移换成模糊半径、把脚本换成物理触发，就能派生出几十种命中反馈变体。

## 相关

- [[custom-mask-shaders]] —— 提供圆环遮罩的来源
- [[uv-displacement-image-effect]] —— 通用的 UV 位移机制
- [[image-effect-mask-blend]] —— mask × 后处理的合成范式
- [[unity-image-effect-basics]] —— 全屏后处理的脚架
- [[chromatic-aberration-post]] —— 常和冲击波一起堆叠的色差
- [[fragment-shader]]
- [[harry-alisavakis]]

## Sources

- [[sources/halisavakis-image-effects-shockwave]]
