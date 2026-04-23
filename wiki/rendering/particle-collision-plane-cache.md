---
tags: [粒子系统, 碰撞, 缓存, 哈希, 数据局部性, bitsquid]
date: 2026-04-19
sources: 1
---

# 粒子碰撞：每个粒子带一张平面 + 空间哈希缓存

Bitsquid 2012 年 hack day，[[niklas-frykholm|Niklas Frykholm]] 用一天时间重写了粒子碰撞，核心灵感来自一个 Naughty Dog 的 GDC talk：**不要给整个粒子系统建一个共享碰撞表示，而是让每个粒子自带碰撞模型**。

## 问题的本性

粒子碰撞难是因为两点：

- **两套完全不同的系统（粒子和物理）必须耦合**，还必须在较低层耦合以保证性能——这是一种天然就丑的依赖。
- **效果之间的需求差异巨大**：火花那种"一百个粒子、只要大体弹对就行"和"一个弹壳、落地必须完美"同框存在，同一套机制要兼顾就必定出 tradeoff。

Niklas 之前反复尝试的都是**先切一块世界 slice、再用某种近似表达之**（三角汤、半球集合、高度场）——但每种都有一堆参数要调（slice 多大、细节多深、动态物体何时刷新），某个效果能用的参数到了另一个场景就崩。

## 方案：per-particle plane

新方法极度简化——每个粒子只存一个平面（normal + offset），共 4 个 float：

```cpp
struct Particle {
    Vector3 position;
    Vector3 velocity;
    Color8  color;
    Vector3 collision_plane_normal;
    float   collision_plane_offset;
};
```

实际代码走的是 SoA（[[data-oriented-design|数据导向]]）而不是上面的 AoS。"没有碰撞"的状态也**不需要额外 flag**——把平面放到原点下方足够远就行。

这样每帧的碰撞测试变成一次**点积 + 比较**，trivial 到可以无脑并行、可以外设（off-CPU）执行，因为它只读本粒子的数据，不触碰共享内存。

于是原来一个难问题被拆成两个简单的子问题：

1. 粒子 vs 平面的测试（trivial）
2. 如何为每个粒子找到合适的那个平面

## 找平面：raycast + 命中率上限

理想情况下每个粒子每帧做一次沿速度方向的 raycast。当然做不到。Bitsquid 给效果设计师一个参数——"每帧允许的 raycast 预算"——比如 `1.0` 表示每帧在本效果里随机挑一个粒子做一次 raycast。好处是**工作量均匀分布在效果的整个生命周期**，不像世界 slice 方案在开头有一个大 spike。

物理 raycast 直接走 PhysX，不自己再建近似世界。

## 关键瓶颈：1000 粒子的共享

每帧只给一次 raycast 预算，1000 个粒子等每个都测一遍要 33 秒——早就穿地了。必须让命中结果被邻居复用。

Niklas 的做法是把 "position, direction → plane" 直接**做成一张哈希表**：

```cpp
const float cell_side = 0.5f, cell_height = 2.0f;
int ix = position.x / cell_side;
int iy = position.y / cell_side;
int iz = position.z / cell_height;
uint64 key = HASH_3(ix, iy, iz);
```

`HASH_3` 是跑了 MurmurHash 前三轮的宏。注意 xy / z 用的 cell 不一样——多数场景水平方向几何更丰富。方向量化到 6 档（沿哪条主轴走）：

```cpp
unsigned id;
if (fabsf(dir.x) >= fabsf(dir.y) && fabsf(dir.x) >= fabsf(dir.z))
    id = dir.x > 0 ? 0 : 1;
else if (fabsf(dir.y) >= fabsf(dir.z))
    id = dir.y > 0 ? 2 : 3;
else
    id = dir.z > 0 ? 4 : 5;
key ^= id;
```

存储是 `HashMap<uint64, CollisionPlane>`。顺带一条个人习惯：**他喜欢把复合 key 提前 hash 成 uint64 再塞 HashMap**，这样 HashMap 本身占更少内存、lookup 就是简单取模——这种"预先 flatten"思维在 Bitsquid 很多 subsystem 里都能看到。

粒子出生、每次反弹时都做一次 lookup；raycast 结果写回 cache。cache 超限时直接丢旧的。

## 两层的 cache 层级

评论区的提问点出了一个容易误解的地方："超快的 dot-and-compare 不是真正的碰撞检测，真正的 raycast 才是。" Niklas 的回答是这正是本质——系统是一个**有损的、近似的 cache 层级**：

- **L1**：每个粒子自带的那个平面（读本地数据、dot product）
- **L2**：spatial+direction hash（按量化 cell 查同向邻居的 raycast 结果）
- **L3**：真实物理引擎的 raycast

再往上还可以加一层 world slice，但越加越复杂，Niklas 不认为值得。

## 这样做的代价

已知的几个粒子不会做的事：

- 不能在 V 形凹槽底部静止——任一时刻只看见 V 的一个面。
- 在多面相交的角落行为很差——只有一个 normal 代表不了它。

如果要存多张平面可以修，但 Niklas 的选择是**保持简单、让少数极端情况下粒子穿地**——与方案整体的哲学一致。

## 相关

- [[niklas-frykholm]]
- [[handle-based-resource-manager]] — "raw memory + 索引"思维的另一实例
- [[polling-callbacks-events]] — raycast 预算化 = 主动控制"何时工作"的同一套思路
- [[pragmatic-performance-philosophy]]

## Sources

- [[sources/bitsquid-hack-day-report]]
