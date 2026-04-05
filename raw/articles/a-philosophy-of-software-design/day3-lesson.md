# Day 3 · 复杂性的根源 & 战术 vs 战略编程

昨天我们拆解了复杂性的三个症状：变更放大、认知负荷、未知的未知。今天我们要往下挖一层——**为什么复杂性会自然地、不可阻挡地积累**，以及面对这个趋势，我们应该用什么样的编程心态来应对。

如果昨天的内容是「认识敌人」，今天的内容是「理解敌人的战略，以及我们的反制」。

---

## 第一部分：复杂性是渐进累积的——温水煮青蛙的代码版

Ousterhout 在第二章的最后两节给出了一个简单却令人不安的结论：

> *"Complexity isn't caused by a single catastrophic error; it accumulates in lots of small chunks."*

没有一个工程师是在某一天早上醒来，拍拍脑袋决定「今天我要把整个系统搞乱」的。所有腐烂的代码库，都是在无数个「这次就先这样吧」的决定中一点点堆积起来的。

> *"A single dependency or obscurity, by itself, is unlikely to affect significantly the maintainability of a software system. Complexity comes about because hundreds or thousands of small dependencies and obscurities build up over time. Eventually, there are so many of these small issues that every possible change to the system is affected by several of them."*

这段话里有一个非常残忍的逻辑：**你的每一个单独的「小妥协」，从理性角度看都是合理的**。今天多加一个参数，是为了赶上 milestone；明天用一个 flag 绕过一个边缘情况，是因为正确修复需要三天重构；后天在 Update() 里加一个全局状态的读取，是因为这条路最短。

每一步单独来看，都说得通。但 Ousterhout 说的是：**复杂性有复利效应**。每一个小依赖和小模糊，都不是孤立存在的，它们相互叠加、相互放大，最终形成的混乱远超所有单个决定的总和。

> *"The incremental nature of complexity makes it hard to control. It's easy to convince yourself that a little bit of complexity introduced by your current change is no big deal."*

这就是「温水煮青蛙」的本质：**每一个单独的温度变化都不足以让青蛙跳出去**。但你回头看两年前的代码库和现在的，你会不认识它。

### 游戏项目里的渐进腐化时间线

作为有十年经验的游戏开发者，你一定见过或亲历过这样的过程。让我把它讲得更具体一些。

**第一个迭代（第1个月）**：手游战斗系统起步，`BattleManager` 负责战斗流程，职责清晰，代码一百来行。`PlayerController` 负责玩家输入和状态，`EnemyAI` 负责 NPC 决策，三者通过简单接口通信。一个新人两小时可以看完。

**第四个迭代（第4个月）**：策划加了 Buff/Debuff 系统。时间紧，于是 Buff 的效果直接写进了受影响的每个模块——移速 Buff 写进 `PlayerController`，攻击 Buff 写进伤害计算，防御 Buff 写进受击逻辑。每个地方只加了几行，感觉还好。

**第八个迭代（第8个月）**：现在有二十几种 Buff，它们分散在七个不同的文件里。没有一个开发者知道所有 Buff 的完整行为。策划说「把减速的持续时间从 3 秒改成 2 秒」，你需要搜索整个代码库，因为「减速」的持续时间被硬编码了三处，但你不确定是不是还有第四处。

**第十二个迭代（第12个月）**：`BattleManager` 已经有两千行了。它依赖 UI 系统（因为需要播放一些动画反馈），UI 系统依赖它（因为要显示战斗状态），物理系统有时候需要知道战斗状态（因为某些 Buff 影响碰撞），存档系统需要序列化战斗中的 Buff 列表。没有人能在脑子里装下完整的依赖图了。每次有新需求，所有人都说「这里很复杂，改动有风险」。

**没有一个时刻**是「系统坏掉」的时刻。它就是渐渐地、自然地，从一个清晰的设计腐化成了一个没人敢动的黑盒。

---

### 「零容忍」哲学：为什么必须从第一天就开始

Ousterhout 在第二章结尾预告了第三章的核心药方：

> *"In order to slow the growth of complexity, you must adopt a 'zero tolerance' philosophy, as discussed in Chapter 3."*

「零容忍」听起来很极端，但它背后的逻辑是清晰的：**如果你允许每次「小妥协」，复杂性就会呈指数增长；但如果你在每次妥协的时候都付出修复成本，复杂性就会保持线性**。

这不是完美主义，这是**复利的数学**。

复杂性的渐进性也解释了为什么「等以后有时间再重构」几乎从来不会发生：到了「以后」，复杂性已经严重到修复它需要几个月，而几个月的代价在任何排期里都很难排上去。所以你继续推迟，复杂性继续增长，推迟的代价继续增加，形成一个单向的恶性螺旋。

---

## 第二部分：战术编程——高效率的毒药

第三章是全书最直接的一章。Ousterhout 不讲技术，讲**编程心态**。

战术编程的定义：

> *"In the tactical approach, your main focus is to get something working, such as a new feature or a bug fix."*

听起来很正常，对吗？「让东西工作」不就是程序员的工作吗？

但 Ousterhout 的核心论点是：

> *"The problem with tactical programming is that it is short-sighted."*

短视，这是战术编程的根本问题。当你用「让这个 feature 跑起来」作为唯一目标时，你的决策视野只有当前任务。**你不会去问「五个版本后，这里的设计还合理吗」，你只会问「我怎么最快让这个 bug 消失」**。

接下来发生的事情 Ousterhout 描述得相当精准：

> *"You tell yourself that it's OK to add a bit of complexity or introduce a small kludge or two, if that allows the current task to be completed more quickly... Before long, some of the complexities will start causing problems, and you will begin to wish you hadn't taken those early shortcuts. But, you will tell yourself that it's more important to get the next feature working than to go back and refactor existing code."*

这段话是不是有种对号入座的感觉？「这个 hardcode 先留着，下个版本再处理」——然后下个版本变成了下下个版本，变成了永远。

重构永远在待办列表里，但永远没有优先级。因为**在战术编程的心态下，重构不产出功能，因此不产出价值**。而每次你绕过一个设计问题而不修复它，你就又加了一点复杂性，让下一次绕过变得更必要。

这是一个**系统动力学意义上的死亡螺旋**——不是某个人的失误，而是一种激励结构的必然结果。

---

### 战术龙卷风：最危险的「英雄」

Ousterhout 用了一个绝妙的词描述把战术编程发挥到极致的人：

> *"Almost every software development organization has at least one developer who takes tactical programming to the extreme: a tactical tornado. The tactical tornado is a prolific programmer who pumps out code far faster than others but works in a totally tactical fashion."*

你身边有没有这样的人？他们的特征是：

- 实现速度惊人，deadline 前总能完成任务
- 管理层认为他们是团队里最有产出的人
- 每次 sprint review 他们的 velocity 最高
- 但他们维护的代码是噩梦

> *"Tactical tornadoes leave behind a wake of destruction. They are rarely considered heroes by the engineers who must work with their code in the future. Typically, other engineers must clean up the messes left behind by the tactical tornado, which makes it appear that those engineers (who are the real heroes) are making slower progress than the tactical tornado."*

这是一个非常深刻的管理学洞察：**战术龙卷风的成本是外部化的**。他的速度是真实的，但他的成本由其他工程师和未来的版本承担。在只看短期 velocity 的管理视角里，他看起来是英雄；在长期系统健康的视角里，他是负资产。

在游戏开发里，战术龙卷风特别危险，因为游戏的功能往往在 deadline 前有个「能玩就行」的验收标准。「先能玩，以后再打磨」在外部看是正常的 polish 流程，但在代码层面这往往意味着大量技术债被打包进了下一个迭代。

想象一个战斗系统开发者：他在三天内实现了一套看起来流畅的连击系统，但输入缓冲区是用一个全局 int 数组硬编码的，连击窗口时间写死在七个不同的地方，技能动画通过 `GameObject.Find("Effect_001")` 实时查找。Demo 很漂亮，但两个月后当策划想加第八个连击类型时，没有人能在不引入大量 bug 的情况下改动它。

---

## 第三部分：战略编程——投资心态

Ousterhout 在定义完战术编程的问题之后，给出了应对方案：

> *"Your primary goal must be to produce a great design, which also happens to work. This is strategic programming."*

注意这句话的语序：**「一个优秀的设计，恰好也能工作」**，而不是「一个能工作的代码，然后再考虑设计」。这是一个根本性的优先级翻转。

战略编程要求一种**投资心态**：

> *"Strategic programming requires an investment mindset. Rather than taking the fastest path to finish your current project, you must invest time to improve the design of the system. These investments will slow you down a bit in the short term, but they will speed you up in the long term."*

这里有两种投资：

**主动投资（Proactive Investments）**：在开始写代码之前，花时间寻找更简洁的设计。试几个方案，选最干净的一个。想象系统将来可能需要如何变化，确保设计能灵活应对。写好文档。

**被动投资（Reactive Investments）**：当你在工作中发现设计问题时，**修复它，而不是绕过它**。这是大多数人最难做到的部分，因为修复它比绕过它要花更多时间，而你正在被 deadline 压着。

但 Ousterhout 的核心论点是：**绕过它比修复它长期代价更高**。绕过它会让下一次绕过更必要，直到绕无可绕。

### 战略 vs 战术的生产力曲线

Ousterhout 画了一张图（书中 Figure 3.1），虽然他承认这只是定性描述：

**战术编程**：初期速度快，但复杂性快速累积，生产力逐渐下降。一段时间后，开发速度慢了至少 20%——而且这个趋势不会逆转，只会加剧。

**战略编程**：初期额外花了 10-20% 的时间，但由于复杂性受控，生产力下降缓慢。几个月后，战略编程的生产力开始超过战术编程，并且这个优势会随时间扩大。

用游戏行业的语言说：战术编程是技术债的「分期付款」，看起来现在负担轻，但利率极高，最终还的远比借的多。战略编程是提前还清，看起来现在痛，但长期无债一身轻。

---

### 投资多少？10-20% 原则

一个实际可操作的建议：

> *"I suggest spending about 10–20% of your total development time on investments. This amount is small enough that it won't impact your schedules significantly, but large enough to produce significant benefits over time."*

10-20% 是什么概念？一个两周 Sprint，大概是 1-2 天。这一两天可以用来：

- 为一个新类多想一个设计方案，选更简洁的那个
- 发现某个地方有设计问题，顺手修了
- 给复杂的模块补上清晰的注释
- 把散落在五处的 magic number 提取成命名常量

这些事情单独看都很小。但 Ousterhout 说：

> *"The most effective approach is one where every engineer makes continuous small investments in good design."*

注意是「每个工程师」「持续地」「小投资」。不是一个人偶尔花一周做大规模重构，而是整个团队在每次提交时都留出一点余量用于设计改进。

这就是为什么大规模重构往往效果不佳：你花了三周把系统重构干净，但如果团队的日常习惯没有改变，六个月后它又会腐化回去。**战略编程是文化，不是项目**。

---

## 第四部分：创业公司的反直觉——快速迭代不等于战术编程

游戏行业有很多「快速迭代」的文化，很多团队会用这个作为战术编程的借口：「我们是独立游戏团队，需要快速验证，没时间搞设计」。

Ousterhout 对创业公司的分析非常精辟：

> *"If you are in a company leaning in this direction, you should realize that once a code base turns to spaghetti, it is nearly impossible to fix. You will probably pay high development costs for the life of the product."*

「意面代码」一旦形成，几乎不可能修复——这不是悲观，这是现实。因为修复它需要大规模重构，而大规模重构的成本太高，在任何有商业压力的团队里都排不上优先级。所以它会一直在那里，每次迭代都变得更难动。

然后是 Facebook 的案例：

> *"Facebook is an example of a startup that encouraged tactical programming. For many years the company's motto was 'Move fast and break things.'... Facebook developed a reputation as a company that empowered its employees. Engineers had tremendous latitude... However, Facebook has been spectacularly successful as a company, but its code base suffered because of the company's tactical approach; much of the code was unstable and hard to understand, with few comments or tests, and painful to work with."*

> *"Eventually, Facebook changed its motto to 'Move fast with solid infrastructure' to encourage its engineers to invest more in good design."*

「Move fast and break things」变成「Move fast with solid infrastructure」——这个口号的迭代本身就说明问题：快速移动和好设计不是对立的，战略编程不是慢，它是让你长期跑得快。

更深刻的论点在这里：

> *"Furthermore, the best engineers care deeply about good design. If your code base is a wreck, word will get out, and this will make it harder for you to recruit."*

好工程师不会接受在烂代码库里工作——不是因为矫情，而是因为他们知道在那种环境里做什么都慢，自己的能力也得不到发挥。如果你的代码库是战术编程的结果，你能招到的工程师档次也会往下走，形成另一个恶性循环。

### Google 和 VMware 的对照组

Ousterhout 用 Google 和 VMware 作为战略编程成功的案例：

> *"Google and VMware grew up around the same time as Facebook, but both of these companies embraced a more strategic approach. Both companies placed a heavy emphasis on high quality code and good design... The companies' strong technical cultures became well known in Silicon Valley. Few other companies could compete with them for hiring the top technical talent."*

这里有一个很重要的观点：**技术文化是竞争优势**。好的代码库吸引好的工程师，好的工程师维护好的代码库，产品质量和迭代速度都在上升，形成正向飞轮。

这对游戏行业同样适用。顽皮狗（Naughty Dog）、From Software、id Software——这些公司的技术声誉不只是荣誉，它们是招募顶尖工程师的护城河。

---

## 第五部分：把这套框架放进你的日常工作

十年的游戏开发经验意味着你见过大量的代码库、团队文化和技术决策。Ousterhout 的战略 vs 战术框架提供了一个分析这些经验的透镜。

**识别你团队的现状**：你们现在处于哪个象限？「能工作就行，以后重构」是主旋律，还是每次 PR review 都会有设计讨论？你们的代码库是在变好还是在变坏？不是渐进变好，不是不变，就是在变坏。

**识别战术龙卷风**：你的团队里有没有这样的角色？他们的高速度是用什么交换来的？这个问题不是为了批判任何人，而是为了理解系统激励——如果你的 KPI 是 feature 数量，战术编程是理性选择，问题在激励结构，不在个人。

**战略投资的起点**：不需要发动一场「全面重构运动」。从小处开始：下次写新功能前，多想一个设计方案；下次发现一个小设计问题，顺手修了而不是绕过去；下次写完一个复杂函数，写三行注释解释「为什么这样设计」而非「这段代码做了什么」。

这些都是 10-20% 的小投资，但持续做下去，你的代码库会在不知不觉中往好的方向移动。

---

## 结语：这不是「完美主义」，这是复利

有一种对战略编程的错误解读：「Ousterhout 是在要求我们用完美主义标准对待每一行代码」。这是误读。

战略编程的核心不是追求完美，而是**避免不可逆的退化**。每一次战术妥协都在消耗一种资产——代码的可维护性。这种资产一旦耗尽，补充的代价是指数级的。战略编程就是在每次消耗时付出一定成本，保持这个资产不会过度透支。

10-20% 的时间投资听起来不多，但放在系统层面，它是**复利的**。第一个月省掉的设计时间，会在第六个月以认知负荷的形式返还给你，利率是 300%。而你在第一个月多投入的 10%，会在第六个月以更快的开发速度返还，利率也是正的。

Ousterhout 的最后一句话值得每个工程师抄下来：

> *"It's crucial to be consistent in applying the strategic approach and to think of investment as something to do today, not tomorrow. When you get in a crunch it will be tempting to put off cleanups until after the crunch is over. However, this is a slippery slope; after the current crunch there will almost certainly be another one, and another after that."*

「今天的投资，不是明天的事」。等到没有压力的时候再去搞设计，这个时刻永远不会来。裂缝期结束了之后，还有下一个裂缝期，还有下一个。

真正的战略工程师，是在每一个日常的代码提交里，都带着一点点对系统未来的投资。

---

## 🎯 今日测验

**Q1（识别）：** 你正在一个游戏项目的 AI 模块里修一个 bug。修复这个 bug 有两条路：路线 A 是在现有代码里加一个 `if` 判断，五分钟搞定，但会让这个函数的职责更混乱；路线 B 是重新设计这个函数的接口，把边缘情况变成函数签名的一部分，需要两小时，同时需要修改三处调用代码。

现在 milestone 还有一周。Ousterhout 的战略编程框架会如何指导你的决策？什么情况下你应该选路线 A，什么情况下你必须选路线 B？「10-20% 投资」原则在这里如何应用？

**Q2（案例分析）：** 「战术龙卷风」在游戏开发团队里有一个特殊的生存土壤：Game Jam 文化和原型（prototype）驱动开发。设计验证阶段的原型代码，本应在设计通过后扔掉重写；但实际上，很多项目的「原型代码」最终直接进了正式版。

从 Ch3 的分析出发，这个问题的根源在哪里？是个人道德问题、时间管理问题，还是系统激励问题？一个想用战略编程对抗这种文化的技术主程，有哪些具体可行的手段？

**Q3（哲学）：** Ousterhout 说：

> *"Your primary goal must be to produce a great design, which also happens to work."*

这句话和大多数工程实践文化里的「ship first, polish later」是直接对立的。

你在自己的职业经历里，有没有见过「战略编程赢得了短期速度比拼」的案例？或者相反，见过「坚持好设计反而拖累了进度」的失败案例？两者的关键变量是什么——什么条件下战略编程是正确答案，什么条件下战术权衡是合理的？Ousterhout 有没有给出一个边界条件？

> 回复本条消息即可作答，你的回答会影响明天的推送深度和方向。
