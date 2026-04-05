**Day 2 · 存储层次与可靠性基础**

如果你问我 CAQA 这本书最核心的洞见是什么，我会毫不犹豫地回答：**内存层次结构**。不是多核，不是流水线，不是指令集设计。就是这个看似平凡的「金字塔」——它决定了你游戏里每一帧的命运，决定了你的 GBuffer 采样是流畅还是卡顿，决定了你的 GameObject 遍历是丝滑还是像在嚼沙子。

今天我们要啃的是 Ch1 的 1.5 到 1.10，表面上是「可靠性」和「能耗」，但这一切的根基，都绑定在存储层次这个基本事实上。

---

> *"The memory hierarchy takes advantage of the principle of locality."*
> — Computer Architecture: A Quantitative Approach, 6th Edition

这句话是整个体系结构里最值钱的一句话。注意 CAQA 用的是「takes advantage of」——不是「依赖于」，不是「需要」，而是「利用」。这是工程师的措辞：我们设计了这套系统，专门来剥削程序的局部性行为以获取性能。

这有什么意义？意义是：**如果你的程序没有局部性，整个层次结构的努力就白费了**。缓存不会帮你，预取不会帮你。你的游戏引擎如果数据布局混乱，CPU 就会对着漂亮的 L1 Cache 无能为力。

---

## 一、存储层次：一座有价格的金字塔

先把数字放出来：

| 存储层级 | 典型延迟 | 容量规模 |
|----------|----------|----------|
| CPU 寄存器 | 0 cycles | 几十个 64-bit 寄存器 |
| L1 Cache | 1–4 cycles | 32KB – 64KB |
| L2 Cache | 10–25 cycles | 256KB – 1MB |
| L3 Cache | 30–60 cycles | 4MB – 64MB |
| DRAM | 200–300 cycles | 8GB – 128GB |
| NVMe SSD | ~100,000 cycles | 512GB – 8TB |

这个表格要烂熟于心，因为这是所有性能问题的参照系。

当你在 Unity 里写这样的代码：

```csharp
foreach (var enemy in enemies) {
    if (Vector3.Distance(player.position, enemy.transform.position) < attackRange) {
        enemy.TakeDamage(damage);
    }
}
```

如果 `enemies` 是 `List<Enemy>`，而 `Enemy` 是 MonoBehaviour，每个对象在堆上随机散布，每次访问 `enemy.transform.position` 大概率是 cache miss。一次 DRAM 访问 200–300 cycles，500 个怪物就是 10–15 万 cycles 的纯等待。按 3GHz 算是 33–50 微秒。一帧 16ms 的预算里，光怪物遍历就吃掉了这么多。

这不是「过早优化」，这是**架构决策**。

---

## 二、局部性原理：程序行为的根本规律

CAQA 把局部性分成两种：

**时间局部性（Temporal Locality）**：你最近访问过的数据，很快还会再访问。循环里的指令会被反复执行。

**空间局部性（Spatial Locality）**：你访问了某个地址，它附近的数据也很快会被访问。数组遍历是典型。

**Cache miss 的代价是不对称的**：L1 hit 是 1–4 cycles，L2 hit 是 10–25 cycles，DRAM 是 200–300 cycles。从 L2 掉到 DRAM，延迟跳了一个数量级。一次 DRAM miss 的代价，足以抵消大约 100 次 L1 命中。

**Cache miss 的惩罚是主导性的**。你可以把指令优化到极致，但数据布局糟糕，所有优化都淹没在 memory stall 里。

这就是 Unity DOTS 和 Mike Acton 一直鼓吹 **Data-Oriented Design（DOD）** 的根本原因。

传统 OOP 的 AoS（Array of Structures）：

```
[Entity0: pos, vel, health, renderer, collider, ...]
[Entity1: pos, vel, health, renderer, collider, ...]
```

遍历所有实体的 `position` 做物理更新时，每次取进来 64 bytes cache line，只有 12 bytes（Vector3）是需要的，其余 52 bytes 是噪音。**有效利用率 18.75%**。

ECS 的 SoA（Structure of Arrays）：

```
positions:   [pos0, pos1, pos2, pos3, ...]
velocities:  [vel0, vel1, vel2, vel3, ...]
```

同样的 64 bytes cache line，全部都是 `position` 数据，装 5 个 Vector3。**有效利用率接近 100%**。在 10000 个实体的场景里，这个差异直接决定你是 60fps 还是 25fps。

局部性原理在渲染里的另一个直接应用：**纹理 Mipmap**。GPU 做纹理 filter 时，纹理坐标密集则 L1 texture cache 命中率高；纹理坐标稀疏（远处地形透视变形）则 cache miss 飙升，bandwidth 暴涨，帧率下降。Mipmap 的本质就是用预处理的多级分辨率保证空间局部性，让 GPU texture cache 发挥作用。

---

## 三、MTTF、MTTR、MTBF：可靠性的量化语言

CAQA 定义了三个核心指标：

- **MTTF（Mean Time To Failure）**：平均失效时间
- **MTTR（Mean Time To Repair）**：平均修复时间
- **MTBF（Mean Time Between Failures）**：MTBF = MTTF + MTTR

可用性公式：

```
Availability = MTTF / (MTTF + MTTR) = MTTF / MTBF
```

具体数字。假设 NVMe SSD 的 MTTF 是 150 万小时：

```
AFR（Annual Failure Rate）= 1/1,500,000 × 8760 ≈ 0.584%
```

每年约 0.58% 的概率故障。1000 块盘，一年大约 5–6 块会坏。这是数据中心的日常现实。

**三个九 vs 五个九的差距：**

```
99.9%   → 每年停机时间 ≈ 8.76 小时
99.999% → 每年停机时间 ≈ 5.26 分钟
```

差了 100 倍。从三个九做到五个九，需要冗余设计、故障自动切换、热备份——工程复杂度和成本至少上一个数量级。

**跟游戏开发的关联：**

- **游戏服务器 SLA**：「我们要高可用」远不如「我们目标 MTTR < 2 分钟，整体 Availability > 99.99%」有力。
- **游戏存档可靠性**：Dark Souls 的三份轮换存档策略——本质上是降低 MTTR（存档恢复时间），通过冗余提高数据的等效 MTTF。
- **崩溃恢复**：Unity Crash Handler、UE crash reporter，本质是设计系统的 MTTR——让玩家感知到的「修复时间」尽可能短。

服务器内存用 ECC RAM，就是为了在单 bit 翻转时自动纠错，不需要重启——降低 MTTR，提高 Availability。你的开发机通常没有 ECC，所以偶尔内存出错导致的奇怪 bug 难以复现，这是客观存在的风险。

---

## 四、能耗与功耗趋势：芯片设计的物理极限

动态功耗（Dynamic Power）的公式：

```
P_dynamic = α × C × V² × f
```

- **α（switching activity）**：每时钟周期实际翻转的晶体管比例
- **C（capacitance）**：晶体管电容，制程越先进越小
- **V（voltage）**：供电电压，平方项！
- **f（frequency）**：时钟频率

注意 V 是**平方项**——电压减半，动态功耗降低到四分之一。这是 Dennard Scaling 历史上如此神奇的原因：随着制程缩小可以同时降低电压，功耗密度保持恒定。

**Dennard Scaling 的崩溃（约 2004 年）**：

在接近 90nm 以下，**静态功耗（漏电流 Leakage）**开始不可忽视。栅极氧化层越薄，漏电流急剧增大。7nm、5nm 节点上，静态功耗已占芯片总功耗的相当比例。

更严重的是：**无法继续降压**。电压降到阈值以下，晶体管无法可靠开关，产生逻辑错误。这个物理下限直接导致：

```
频率不再能随制程提升而提升
```

这就是 **Power Wall（功耗墙）**。2004 年之前，处理器频率每年约增长 40%；2004 年后，单核频率几乎停滞在 3–5 GHz——不是芯片工程师变懒了，是物理不允许。

**多核是无奈之举，也是聪明之举。** 当无法继续提高单核频率时，Intel 和 AMD 转向多核设计。性能的提升从「更快的单线程执行」变成了「更多的并行执行」。但 Amdahl 定律约束了并行的上限：如果代码有 20% 必须串行，即使无穷多核，最大加速比只有 5 倍。这就是为什么现代游戏引擎要精心设计 Job Graph、最小化串行依赖——在跟 Amdahl 定律搏斗。

**能效才是今天的核心指标：**

```
Apple M1 GPU:  2.6 TFLOPS / 15W  ≈ 173 GFLOPS/W
NVIDIA RTX 3090: 35.6 TFLOPS / 350W ≈ 102 GFLOPS/W
```

Apple M1 的能效比优于 RTX 3090。这不是因为魔法，是因为设计哲学一开始就不是追求峰值算力，而是在功耗预算约束下最大化有效吞吐量。

**对手游开发的直接影响：**

1. **不要把 GPU 算力当免费资源**：手机 TDP 约 4–8W，超出就降频（throttling）。精心设计的 120fps 游戏，玩 10 分钟后可能跌到 40fps，因为手机烫手。
2. **DrawCall 和 State Change 有能耗代价**：合并 DrawCall 不只提升帧率，还降低能耗。
3. **Shader 复杂度影响热功耗**：移动端重型 PBR shader 可能导致芯片温度快速上升，触发 throttling，帧率系统性下降。
4. **DVFS 的存在**：均匀的 GPU 负载比忽重忽轻更容易被 DVFS 处理，不容易产生抖动。

---

## 五、三个概念的统一视角

- **存储层次**：解决速度与容量的矛盾，用局部性作为杠杆，把访问延迟压到最低。
- **可靠性指标**：量化系统在时间维度上的可信赖程度——不是「它会不会坏」，而是「坏了多久、多频繁」。
- **能耗趋势**：认识物理约束对架构设计的决定性影响——频率不再免费增长，多核和能效成为新主旋律。

三者的共同点：它们都是**计算机体系结构的约束条件**，不是设计选择。你可以选择编程语言、设计模式、渲染管线；但你无法选择内存访问延迟，无法选择晶体管漏电流，无法选择物理定律给出的能耗公式。

这就是 CAQA 这本书的根本价值：教你认识这些约束，并在约束之内找到最优解。

**不理解这些原理的工程师，是在碰运气；理解了这些原理的工程师，才是在做工程。**

---

> 存储层次利用局部性，可靠性靠时间量化，能耗受物理约束——三根柱子，撑起了整个现代计算机体系结构的大厦，也决定了你每一行游戏代码的命运。

---

## 🎯 今日测验

**Q1（概念）**：MTBF = MTTF + MTTR。如果一块硬盘的 MTTF 是 100,000 小时，MTTR 是 24 小时，计算它的 Availability 和 AFR（Annual Failure Rate）。

**Q2（应用）**：你在 Unity 中写了一个系统，每帧遍历 10,000 个 NPC 并读取每个 NPC 的 `position`、`health`、`state` 字段。当前用的是 `List<NPC>`，NPC 是普通 C# class。请从存储层次和局部性原理的角度，分析性能瓶颈在哪里，并给出基于 DOD 的改造方案。

**Q3（品味）**：Dennard Scaling 在 2004 年前后崩溃，导致处理器从「提升主频」转向「增加核心数」。这个历史转折，对游戏引擎的架构设计（特别是渲染线程模型）产生了哪些深远影响？请结合 Unity 的 Job System 或 UE 的 TaskGraph 谈谈你的理解。

> 回复本条消息即可作答，你的回答会影响明天的推送深度和方向。
