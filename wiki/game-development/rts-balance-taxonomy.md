---
tags: [游戏开发, 游戏设计, 平衡性, rts]
date: 2026-04-19
sources: 1
---

# RTS 平衡性的七种面孔

[[joost-van-dongen|Joost van Dongen]] 在 Swords & Soldiers 开发过程中从专职平衡组（Olivier、Jasper、Fabian、Tom，其中 Olivier 是重度 Starcraft 玩家，长期跟踪 Blizzard 的 patch 笔记）身上学到：**「阵营平衡」只是 RTS 平衡里最显眼的一种**，真实工作至少还要同时顾到六种别的平衡，它们彼此交织，改一处往往同时动到所有。这页把这七种面孔列成一张 checklist，用来在做平衡决策时避免只看单一维度。

## 七种平衡

1. **阵营平衡（faction balance）**。三个阵营单位、法术、魔法资源获取方式都不同，但高水平玩家应该用任一阵营都能赢——胜负取决于操作不是阵营。这是大众默认理解的那种「平衡」。
2. **新手平衡（beginner balance）**。Swords & Soldiers 故意不追求这个：维京最简单上手、中国最难，为的是风味差异。有趣的是**精通难度**的排序和**入门难度**不一致——维京反而精通最难，因为高端策略需要更多单位配合。
3. **战术平衡（balance between tactics）**。一个阵营内部每种单位、每条策略链都应有用武之地；如果只有一套强力打法，游戏会因为对手「知道你下一步」而变得无聊。
4. **地图平衡（map balance）**。一张图上平衡不代表另一张图上也平衡——中国需要塔采魔法所以怕大地图；Ronimo 的应对是**只针对一张标准地图做平衡**（medium 1），其他 9 张图只上线 4 张作为联机可选。
5. **早 vs 晚游戏平衡（early vs late game balance）**。不能让某阵营前期强后期弱——rush 过后胜负已定就变得无聊；但也不能完全一致，否则失去节奏风味。需要的是「谁 rush 更快」有差异但不致命。
6. **趣味平衡（fun in balance）**。「一直出一种兵」哪怕数值上强也应该被砍。反面例子是维京 Frosthammer + Snowstorm + Rage 的三连——需要技巧和时机，操作成功瞬间玩家自己会爽。**强度高不等于好；好是强度高且操作后玩家自觉做了件牛事**。
7. **运气平衡（luck balance）**。Joost 举的例子：中国开局选远程 / 近战 vs 敌方开局构成 50% 胜率的「剪刀石头布」，统计上阵营平衡但全靠猜。运气过高就是无技巧。反面论点：一点点运气对输家是好事（Mario Kart 让初学者偶尔能赢高手），完全移除运气反而让败者心理负担更重。

## 工程含义

- 平衡不是单目标优化，而是**七维向量**上的 Pareto 搜索；改一个数同时扰动七维。
- 把平衡决策拆成「阵营 / 战术 / 地图 / 节奏 / 趣味 / 运气」六条独立 checklist 来审视，比单看胜率表更能发现隐藏破坏。
- 不要贪——**只对一张代表性地图做平衡**，其他地图作为风味而非严格维度。
- Joost 预告：Ronimo 的「秘密新项目」（后来是 Awesomenauts）平衡复杂度远高于 Swords & Soldiers，能不能 hold 住是未知数。

## 相关

- [[determinism-vs-smart-ai-gameplay]] —— Swords & Soldiers 的 AI 决定论设计
- [[planning-over-rng-game-design]] —— RNG 与技巧的权衡
- [[deckbuilder-game-design-patterns]]

## Sources

- [[sources/joostdevblog-rts-balance-faces]]
