---
tags: [character, animation, ik, game-development]
date: 2026-04-19
sources: 1
---

# 角色高度变化问题

换鞋、换种族、换体型——任何**改变角色高度**的游戏化需求都会掀翻一整套隐式假设：手—物件接触点、嘴对嘴位置、掩体高度、碰撞体、摄像机 framing。[[simon-trumpler]] 的 *The High Heel Problem* 把业界的处理方式总结成两类六小类。本页是那一对比的抽象化——它不只是「高跟鞋问题」，也适用于 *Dragon's Dogma 2* 的体型互动、*Saints Row* 的性别可换、*Baldur's Gate 3* 的种族混搭、*Monster Hunter* 的武器拿持姿势。

## 两大策略

### 策略 A：正确调高度

**1. Hope for the best**——接受 clipping，让高度真实变化，赌玩家看不出。*Infinity Nikki* 的大多数 contact 动画够模糊、交互够少，clipping 不被察觉。

**2. Manual labor**——per-变体动画：为每种高度组合手动加一套 contact-accurate 动画。*GTA Online* 打高尔夫动画只有平跟版本的漏洞、*Infinity Nikki* 换鞋那一帧的 pose mismatch 都是这条路没做彻底的证据。

**3. Dynamic IK**——运行时用 full-body IK 把手脚 retarget 到实际接触点。现代引擎（UE5、Unity Animation Rigging、CryEngine、Decima）都支持；*Uncharted* 的走路蹭墙、*Infinity Nikki* 的 foot-IK 都是 samples。代价是 IK 配置错会产生离奇姿势。

### 策略 B：找变通

**1. Hide**——鞋筒高到能把脚藏进去，脚位与动画都不用改，视觉上腿变短。

**2. Shorten**——*Sims 4* 的主力解：**小腿骨被缩短**几厘米，髋部不动，角度保持。这不用改任何动画或 IK，但近距离观察会看到膝盖高度异常。

**3. Bend**——脚腕角度扳起（踩尖状态），脚底离地但髋部不变。这保留原 bone layout，适合没有 IK 的老引擎。

## 决策树

```
需要精确手-手 / 嘴-嘴交互？
├── 是
│    ├── 有 full-body IK？ → 3. Dynamic IK
│    └── 无              → 2. Manual per-shoe animations
└── 否
     ├── 美术能接受「鞋筒藏脚」 → B.1 Hide
     ├── 近景不多             → B.2 Shorten lower leg
     └── 想保留真实视觉差      → A.1 Hope for the best（clipping bug 随意）
```

## 被忽视的副作用

- **Competitive 射击的受击判定体**——视觉 10 cm 差可能让玩家有不公平优势；很多 FPS 把 hitbox 固定到「基准高度」与视觉脱钩。
- **摄像机 framing**——对话、cutscene 的相机角度常 hard-coded 到特定角色高度，换鞋后头顶可能飞出画面，或亲吻镜头对不齐嘴。
- **Cover / 潜行**——掩体掩护点按角色高度设计；10cm 差异能让角色暴露。
- **音频 footstep 距离 panning**——头部高度改变了 listener 位置，影响空间音效。

## 相关概念

- [[kinematic-character-controller]]——底层运动模型
- [[scene-graph-matrix-stack-visitor]]——骨骼 hierarchy 的存储
- [[save-load-driven-data-design]]——不同体型的装备数据持久化

## Sources

- [[sources/simonschreibt-high-heel-problem]]
