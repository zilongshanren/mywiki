---
tags: [query, unity, builtin-pipeline, shadow, mobile, mahjong]
date: 2026-04-21
sources: 4
---

# Unity Built-in 管线麻将场景移动端阴影方案

## 约束复核

- 渲染管线：**Built-in（Forward）**。不是 URP/HDRP。
- 目标：移动端中端（骁龙 7xx / A13+）。带宽与填充率吃紧，GPU 不是瓶颈。
- 相机：**固定斜视**，光源方向可一次定死 → 所有阴影方向是**常量**。
- 动态对象：3 个 avatar（骨骼动画，动）+ 少量正在被摸/打的牌。
- 静态对象：牌墙、已成型的副露、河牌池（一旦摆放就不动）。
- 需要投影的组合：
  - avatar 身体 → 桌面/地面
  - avatar 手臂 → 牌面
  - 单张牌 → 桌面
- **不需要**：牌对牌互相投影（牌墙自阴影）。

## 顶层设计：四层 shadow 混合

因为相机和光源都固定，所有"不变"的阴影都能预烘焙或缓存。场景可以拆成 4 条独立路径，各自用最便宜的手段：

| 投影关系 | 方案 | 运行时成本 |
|---|---|---|
| 牌墙 / 副露 → 桌面（静态） | **一次性离线烘焙**到 RenderTexture（或 lightmap 通道） | 0（采样表面贴图时顺带读一次） |
| 河牌池新牌 → 桌面（偶发增量） | 摸/打时往同一张 RT **Blit 一张牌影 sprite** | 1 draw call / 次打牌 |
| avatar 身体 → 桌面/地面 | **平面投影阴影**（render-to-texture + 斜投影矩阵） | 3 × 小 RT 渲染 + 3 × 贴地 quad |
| avatar 手臂 → 牌面 | 同上共享 RT，采样投到"牌顶平面"（虚拟 receiver plane） | 共用上一步的 RT |

这套组合的**底层逻辑**是：**把静态部分全吃成贴图，把动态部分压到最低分辨率**。Built-in 自带的 shadow map 全部关掉（`QualitySettings.shadows = Disable`），省掉 shadow caster pass、级联、PCF 过滤。

## 方案细节

### 1. 桌面共享 shadow RT（核心抓手）

在桌面那个正方形平面上挂一张 `RenderTexture`（建议 `1024×512` 或按桌子尺寸比例，R8 格式即可——只要一个通道记"阴影强度"）。

**启动时一次烘焙**：

- 关闭所有 avatar 和动态牌，打开所有静态几何（牌墙、副露位）
- 用一个正交相机从光照方向朝下拍摄，深度/黑度直接写入 RT
- 保存为这局游戏的"底图"

**桌面 shader 改动**：表面材质多采一次这张 RT（用 world XZ 转 UV），阴影区域乘 0.35 左右的暗化系数。**一次额外 texture lookup，TBDR 架构下几乎零成本**（桌面像素反正要被写一次）。

### 2. 河牌池增量烘焙

每次打一张牌落到河里，把**预先做好的一张牌影 sprite**（一个带柔边的黑色矩形贴图，64×96 左右）通过 `Graphics.Blit` 叠加到上面那张 RT 上对应 UV 位置。一帧一次、只在"有新牌"时触发。

预先做牌影 sprite 的原因：所有 136 张牌轮廓几乎一样（只差 0 / 副露区别），用一张贴图复用就够了。形变可以靠 `Graphics.Blit` 的 material 里做旋转/倾斜 UV。

这条路是 [[cached-shadowmaps]] 思想的简化版：**静态缓存 + 动态 splat**，只不过 splat 的不是 3D caster 而是一张 2D sprite。

### 3. avatar 身体 → 桌面/地面：平面投影阴影

Built-in 管线有个很老但很对路的技术：**Planar Projected Shadow**。步骤：

1. 每个 avatar 建一个 `Camera`（或用 `CommandBuffer`），从光源方向拍摄骨骼 mesh 到一张 `128×128` 或 `256×256` 的 RT
2. 在桌面/地面上贴一块 quad，材质用这张 RT 作为 alpha mask，颜色用半透明黑
3. quad 用"**斜投影矩阵**"（shadow matrix）把 mesh 投到 receiver 平面——3 行代码，网上随处可搜（关键 API：`Matrix4x4` 构造 + `Graphics.DrawMesh`）

优化要点：
- **3 个 avatar 可以共享一张 atlas RT**（`384×128`），三人分列三段，把三次独立 Blit 合成一次 render-to-RT pass
- RT 只需每 2 帧更新一次（骨骼动画 30fps 采样足够，玩家看不出），**省一半带宽**
- 受光方向一旦定死，shadow matrix 是常量，每帧只需更新 avatar world matrix

**为什么不用 blob shadow**（[[blob-shadow-decal-vs-plane|贴地 plane 版]]）？麻将场景 avatar 是坐姿/半身，身体形状是长方形而不是圆形，圆形 blob 识别度差；而且相机是斜视，玩家能看清角色轮廓，假圆圈会显得廉价。**平面投影保留了身体 + 手臂的剪影**，视觉上升一个档次而成本差不多。

### 4. avatar 手臂 → 牌面：复用身体 RT

麻将场景里牌面高度是固定的（桌面上方 ~2cm）。建一个**虚拟 receiver 平面**在这个高度，把同一张 avatar shadow RT 用**另一套 shadow matrix**（投到牌顶平面而非桌面）再采样一次，作用在牌顶材质上。

因为所有牌顶几乎共面（薄片），误差看不出。**不需要 Projector 组件**（Built-in 的 Legacy Projector 对每个受影物体要多画一个 pass，牌多了成本爆炸）。

### 5. 牌根接触阴影（可选加强）

单张牌落在桌面的**接触线**（牌底那条细黑影）不从上面 RT 烘焙出来，而是靠 [[prebaked-corner-occlusion|烘焙在牌模型自身]]：

- 牌的底部两条边用**顶点色**染一点暗色，或者牌的 diffuse 贴图底 1-2 像素压暗
- 零运行时开销，效果立竿见影

这是 Deus Ex 那一套"把接触阴影烘进 asset"的小抄。

## 不建议做的事

- ❌ **开 Built-in 的 Real-time Shadow**：移动端开销显著（shadow caster pass + shadow map sampling），且 avatar 数少的场景完全浪费
- ❌ **用多个 Light + 每 Light shadow map**：built-in 多光源阴影是 per-pixel pass 翻倍
- ❌ **Legacy Projector 铺所有牌**：每张牌多一个 render pass，80 张就是 80 drawcall 翻倍
- ❌ **SSAO / HBAO 类屏幕空间**：中端机划不来，且麻将场景遮挡结构简单，收益低

## 顶层设计图

```
┌─────────────────────── 桌面 Table ───────────────────────┐
│                                                          │
│   A. 启动烘焙：牌墙+副露 → bake → baseShadowRT (1024×512)│
│   B. 摸打牌：discardSprite Blit → baseShadowRT (增量)    │
│   C. 每帧：3 avatar mesh → atlasShadowRT (384×128)       │
│   D. 桌面 shader：sample baseShadowRT + atlasShadowRT    │
│                  用两个 shadow matrix 投影 UV            │
│   E. 牌顶 shader：sample atlasShadowRT 投到牌顶平面      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## 成本预估（中端手机）

| 项 | 每帧成本 |
|---|---|
| baseShadowRT 烘焙 | 启动一次性 |
| atlasShadowRT 更新（3 avatar） | 3 draw + RT 切换，~0.3ms |
| discardSprite Blit | 只在打牌瞬间，<0.1ms |
| 桌面 shader（多 2 次 tex lookup） | 几乎免费（TBDR） |
| 牌顶 shader（1 次 tex lookup） | 几乎免费 |
| **合计** | **<0.5ms / 帧**，60fps 有预算 |

对比：开 Built-in Directional Shadow（Hard）一般要 1-2ms + shadow caster pass 额外几何提交，中端机动辄 2-3ms 跑不满 60fps。

## 相关 wiki

- [[blob-shadow-decal-vs-plane]] — plane vs decal 的通用取舍
- [[selective-shadow-fade-pass-switch]] — 多 shadow pass 拆分思想
- [[cached-shadowmaps]] — 静态缓存 + 动态 splat 的思路源头
- [[prebaked-corner-occlusion]] — 把接触阴影烘进 asset
- [[shadow-mapping-basics]]
- [[tbdr-vs-imr]] —— 移动端 TBDR 下额外 texture lookup 几乎免费的原因

## 落地优先级

1. 第 1 步：**关掉 built-in real-time shadow**，只留平面投影阴影给 3 avatar（拿到最大头的收益）
2. 第 2 步：加牌根接触阴影（顶点色/贴图烘焙，10 分钟工作量）
3. 第 3 步：桌面 shadow RT（静态烘焙 + 增量 Blit）
4. 第 4 步：手臂投牌顶（复用 avatar shadow RT）

前两步就能吃掉视觉上 80% 的阴影感，后两步锦上添花。
