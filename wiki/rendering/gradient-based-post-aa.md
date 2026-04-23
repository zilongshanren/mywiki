---
tags: [渲染, 反走样, post-aa, 梯度, pixel-bender]
date: 2026-04-19
sources: 1
---

# 梯度驱动的后处理反走样

**梯度驱动 post-AA** 是 [[angelo-pesce]] 在 2011 年发表的一份 DIY 后处理反走样配方——用纯局部算子替代 [[aa-techniques-survey-2011|MLAA]] 的全局模式匹配，以换取在 GPU 上跑得足够快且代码足够短。它不是一个被命名为品牌的算法（后来 FXAA / SMAA 的近亲），但 Pesce 的写法把这类「只看当前像素及其 1-ring 邻域」的后处理 AA 共同骨架浓缩得非常清楚。

## 三段式模板

1. **识别边**：颜色差分还是法线/深度差分？Pesce 给的实战结论是**后者更稳**——color 版容易被 albedo pattern 欺骗。但在他公开的 Pixel Bender 配方里仍用了颜色梯度，因为作为 post-process 滤镜，算子要能对任何输入生效而不依赖 G-Buffer。
2. **拟合基元**：把一条几何基元（直线 / 过像素中心直线 / 曲线）拟合到识别出的边上，得到**长度与方向**。MLAA 的 key property 是能找到横跨多像素的近水平 / 近垂直直线——代价是 pattern matching 的大邻域搜索，2011 年的 DX9 GPU 跑这个逻辑非常吃力。Pesce 方案直接跳过拟合，用**梯度矢量**隐式替代：梯度方向就是边的法线，旋转 90° 即是沿边方向。这个近似只对**曲线与短边**成立。
3. **沿基元混合**：要么区分前景 / 背景并按覆盖度插值（MLAA 路线），要么沿基元**采样再平均**（Pesce 路线）。后者便宜，且避免精确计算基元在像素里的积分。

## Pesce 的 Pixel Bender 配方（2011）

```
// 1. 水平/垂直差分
vb = tex(+1,0) - tex(-1,0);
hb = tex(0,+1) - tex(0,-1);

// 2. Rec. 709 亮度权重投影到标量梯度
vg = dot(vb, (0.2126, 0.7152, 0.0722));
hg = dot(hb, (0.2126, 0.7152, 0.0722));

// 3. 梯度旋转 90° 得到沿边方向
off = (hg, -vg);
offl = length(off);
off /= offl;

// 4. 沿边方向 3-tap 平均
col = (tex(0) + tex(+off) + tex(-off)) / 3;

// 5. 用梯度强度做 blend 权重（阈值 0.25）
blend = saturate(offl / 0.25);
out = lerp(tex(0), col, blend);
```

关键点：**梯度模长既是边检测信号，也是 blend 强度**——弱边不被碰，强边才混合。偏移向量长度 = 1 texel，**没有 sub-pixel 精度**，因此长直线上的阶梯 pattern 不会被消除。

## 和 MLAA 的取舍

Pesce 在 *Dead Rising 2* 无 MSAA 源图上做的直接对比：

| 场景 | MLAA | 梯度滤镜 |
|---|---|---|
| 长椅边（长直线） | 干净 | 明显阶梯残留 |
| 树叶（曲线） | 过度模糊 | 更自然 |
| 角色轮廓（曲线） | 可接受 | 更自然 |
| 金属杆（频繁换向细节） | 糊成一团 | 保留细节 |

**一句话结论**：两者是互补的，不是竞争的。*Force Unleashed II* 公开的做法与 Pesce 的配方类似，MLAA 在长近水平 / 近垂直边上的优势无可替代。

## 在 AA 家族谱系里的位置

- 相对 [[aa-techniques-survey-2011|MLAA / FXAA]]：同属 **post-AA** 档，但 **MLAA = 全局 pattern 匹配**，**FXAA / 本方案 = 局部梯度**。FXAA 在此基础上加了 sub-pixel 偏移与多方向判别，能处理更长的边。
- 相对 [[subpixel-reconstruction-antialiasing|SRAA]]：SRAA 吃 G-Buffer 的 sample 级深度 / 法线来重建几何边，属于 deferred-only 档，信息量大得多。
- 相对 [[temporal-antialiasing|TAA]]：TAA 从时间维度引入外源样本，带宽远高；梯度滤镜彻底无外源。
- **与 MSAA 组合**：Pesce 建议在 MSAA 的 sample 分辨率上先跑 edge filter 再做 downscale——不要先 resolve，否则几何不连续处的信息已被均值掉。ATI HPG'09 paper 给过更完整的方案。

## 局限

- 只看 1-ring 邻域——长直线上看不见「边在哪结束」，必然残留阶梯。
- 颜色梯度容易被 albedo pattern 触发假边——深度 / 法线版更稳但要求 G-Buffer。
- UI / HUD 要 mask 掉——全屏跑的代价和 [[aa-techniques-survey-2011|MLAA 驱动版]] 一样，会误伤已经像素完美的矢量元素。

## 相关

- [[aa-techniques-survey-2011]] —— Supnik 的 AA 五档分类，post-AA 家族归为其中第 4 档
- [[angelo-pesce]]
- [[analytical-antialiasing]]
- [[subpixel-reconstruction-antialiasing]]
- [[temporal-antialiasing]]
- [[msaa-ssaa]]

## Sources

- [[sources/c0de517e-recipe-for-aa]]
