**Day 5 · 浅模块之罪 & Classitis**

先说一个你可能经历过的场景。

你接手了一个老项目，第一天打开代码目录，看到几百个文件，密密麻麻的类名。你打开其中一个，发现它只有二三十行。再打开另一个，又是二三十行。整个 Managers 目录里有三十个 Manager 类，每个 Manager 只做一件"小事"，但你想理解系统怎么工作，你得同时在脑子里维护三十个类的关系图，还要理解它们之间通过事件系统发出的几十条消息通道。

你花了一整天，还是搞不清楚"玩家死亡时究竟发生了什么"。

这就是 Classitis（类炎症）。它的每个单独部件看起来都"整洁"，但放在一起，它是一场认知灾难。

---

## 一、浅模块的本质：接口成本大于收益

> "a shallow module is one whose interface is relatively complex in comparison to the functionality that it provides... It doesn't take much code to manipulate a linked list (inserting or deleting an element takes only a few lines), so the linked list abstraction doesn't hide very many details."
> —— APoSD, Ch4.5

Ousterhout 给浅模块下了一个精确的定义：interface 的复杂度相对于它提供的功能来说过于复杂。「复杂」不是指 interface 有多少个方法，而是**使用这个模块需要理解的东西**有多少——你需要知道它存在、知道它的命名、知道参数语义、知道何时适合用、知道副作用……这些加在一起，就是使用这个模块的「认知税」。

如果这个认知税高于你省下的工作量，这个模块就是浅的，就是有害的。

他举了一个极端案例：

```java
private void addNullValueForAttribute(String attribute) {
    data.put(attribute, null);
}
```

这个方法看起来很「无害」——职责单一，命名清晰，多合理？

但 Ousterhout 的判断是：**"From the standpoint of managing complexity, this method makes things worse, not better. The method offers no abstraction, since all of its functionality is visible through its interface."**

为什么更糟？这个方法提供的「抽象」是零。它的 interface 复杂度和实现复杂度是完全等价的，甚至 interface 端更重——因为还有发现成本和记忆成本。调用者学这个方法，换来的信息量是零，但付出的认知成本是正的。

这里有一个很重要的认知转变：**好的抽象不是把代码分割成更小块，而是让调用者理解更少的东西**。分割是手段，不是目的。当分割之后调用者需要理解的东西变多了，这种分割就是净亏损。

---

## 二、Classitis：一种系统性的设计疾病

> "Classitis stems from the mistaken view that 'classes are good, so more classes are better.' In systems suffering from classitis, developers are encouraged to minimize the amount of functionality in each new class... Small classes don't contribute much functionality, so there have to be a lot of them, each with its own interface. These interfaces accumulate to create tremendous complexity at the system level."
> —— APoSD, Ch4.6

为什么 Classitis 会变成「美德」？

深层问题是对 **Single Responsibility Principle** 的机械理解。SRP 说每个类应该有「一个职责」，但「一个职责」是什么？这是哲学问题，没有客观的技术答案。如果你把「职责」定义得足够窄，任何类都可以被拆成十个「更专注」的类——`FileOpenOperation`、`FileReadOperation`、`FileCloseOperation`……

Ousterhout 指出了 Classitis 的核心危害：**"These interfaces accumulate to create tremendous complexity at the system level."** 你不能只看单个类的复杂度，要看系统整体的接口复杂度。十个简单类的接口总和，可能比一个功能完整的深类的接口复杂得多，而且这个复杂度是分布式的、隐性的，更难理解和维护。

---

## 三、Java I/O vs Unix I/O：两种设计哲学的对决

Java 读取一个序列化文件，你需要这样写：

```java
FileInputStream fileStream = new FileInputStream(fileName);
BufferedInputStream bufferedStream = new BufferedInputStream(fileStream);
ObjectInputStream objectStream = new ObjectInputStream(bufferedStream);
```

三个对象，三层包装。而且你必须记得加 `BufferedInputStream`——因为如果忘了，程序不会报错，一切看起来正常，但 I/O 性能会慢几十倍。

> "It is particularly annoying (and error-prone) that buffering must be requested explicitly by creating a separate BufferedInputStream object; if a developer forgets to create this object, there will be no buffering and I/O will be slow."
> —— APoSD, Ch4.7

注意 Ousterhout 用的两个词：**annoying** 和 **error-prone**。因为有 annoying（繁琐），所以容易产生 error-prone（易错）。「忘记加 BufferedInputStream」是那种最危险的错误：不崩溃，不报错，程序照样运行，只是悄悄地慢了几十倍。它可能在开发环境永远不被发现，最后在生产环境的真实用户数据压力下才暴露。

现在对比 Unix 文件 I/O——整个系统只有五个系统调用：

```
open, read, write, lseek, close
```

五个。buffering 是内核默认提供的，你不需要显式请求，不需要知道 buffering 的存在，就自动获得了它的好处。

> "Almost every user of file I/O will want buffering, so it should be provided by default."
> —— APoSD, Ch4.7

这句话体现了完全不同的设计哲学：**为最常见的用例优化，把复杂度内化在实现里，而不是推给每一个调用者**。

---

## 四、游戏引擎里的 Classitis：一种流行病

Classitis 在游戏开发领域是一个非常真实的问题。Unity 的组件系统本身是优雅的，但经常被滥用成 Classitis 的温床。

这种组织结构你一定见过：

```
PlayerMovementManager.cs
PlayerAnimationManager.cs
PlayerInputHandler.cs
PlayerStateManager.cs
PlayerHealthManager.cs
PlayerAbilityManager.cs
PlayerAudioManager.cs
PlayerVFXManager.cs
PlayerUIManager.cs
```

十个 Manager，全都挂在同一个 Player 对象上。每个 Manager 只做「一件事」，看起来职责清晰。

但实际使用时：这些 Manager 之间严重依赖，依赖关系散布在十个文件里，没有一个地方可以整体看清楚。理解「玩家受到伤害时发生什么」，你需要同时打开五个文件，在五个地方找相关代码，然后在脑子里拼出完整的执行链。加一个「受伤时摄像机震动」的功能——应该改哪个 Manager？答案是不明确的。

这就是 Classitis 的症状：系统级接口复杂度远高于模块级接口复杂度的表面简洁。

**对比一个更深的设计：**

```csharp
public class PlayerController : MonoBehaviour
{
    // 公共接口：真正需要外部知道的
    public void TakeDamage(float amount, DamageInfo info);
    public void ApplyForce(Vector3 force, ForceMode mode);
    public void SetMovementEnabled(bool enabled);
    public void UseAbility(AbilityType type);

    public float CurrentHealth { get; }
    public bool IsAlive { get; }
    public PlayerState State { get; }

    public event Action<float, float> OnHealthChanged;
    public event Action<DamageInfo> OnDeath;
}
```

调用者只需要：

```csharp
player.TakeDamage(50f, new DamageInfo { source = DamageSource.Enemy, hitPoint = hitPos });
```

然后 PlayerController 内部协调好所有状态变化——血量、状态机、动画、音效、特效、HUD——调用者不需要知道。这就是深模块的价值。

有人会说：「但 PlayerController 会变得很大！」

是的，可能 500 行，可能 800 行。但行数是假指标，认知负担才是真指标。一个 800 行但 interface 简洁、逻辑内聚的 PlayerController，比十个 80 行但 interface 复杂、依赖分散的 Manager，要容易理解、修改、测试得多。

---

## 五、Event System 的滥用：Classitis 的隐性变体

游戏开发中有一种特别常见的 Classitis 变体：**Event System 的滥用**。

设计意图是好的——用事件解耦各个 Manager，降低直接依赖。但当这个模式被推到极致，你有二三十个 Manager，每个发出若干事件、监听若干事件，整个系统就变成一张巨大的事件网络图。

想知道「玩家死亡时发生什么」？你需要：
1. 找到 `OnPlayerDeath` 事件的所有发出点（可能是多个 Manager）
2. 找到所有监听这个事件的地方——可能散布在十五个文件里
3. 理解这十五个响应的执行顺序（通常不确定）
4. 分析它们之间是否有竞争条件

这是一种特殊的浅模块病：每个 Manager 的 interface 看起来很简洁（「只发一个事件」），但系统整体的 interface 是极度复杂的，而且这个复杂度是**隐性的**——不在任何一个文件里。

更危险的是，这种架构非常脆弱。如果两个模块响应同一事件，而执行顺序有依赖，这个依赖在代码里是看不见的。某次 Unity 更新改变了脚本执行顺序，隐性 bug 就悄悄出现了。

一个更深的设计：把这些逻辑内聚到一个地方，用显式的调用而不是隐式的事件。`PlayerController.TakeDamage` 直接调用需要响应的系统，调用顺序是显式的，逻辑在一个地方可以完整理解。**显式的耦合比隐式的耦合好管理——因为显式的耦合可以在代码里看到、追踪、测试。**

---

## 六、"类应该小"为何如此顽固

**局部视角的诱惑**：当你只看一个类，小类确实清晰。但你很少能只看一个类，你总是在理解系统时看类。我们的直觉在局部层面工作，但设计质量在系统层面衡量。

**Code Review 的激励扭曲**：十行的类，reviewer 一眼看懂。两百行的类，需要花时间真正理解。最安全的 review 意见是「这个类太大了，拆开」——不需要深入理解就可以给出，而且听起来很专业。

**可量化指标的误导**：Cyclomatic complexity、lines per file——这些指标在小类下都好看。但「理解一个功能需要跨越的文件数」才是决定项目长期可维护性的关键因素，很难量化，于是被忽视。

Ousterhout 的贡献在于：他提供了一把不同的尺子。不问「这个类有多大」，而问「这个模块隐藏了多少复杂性」。

---

## 七、什么时候浅模块是合理的

并非所有浅模块都是设计失败。

**边界层的 pass-through** 有时不可避免——在不同抽象层次之间，需要薄薄的适配层做「翻译」，它的职责就是转换，本身不需要隐藏什么复杂性。

**框架强制的结构**：Unity 的 MonoBehaviour 有生命周期约束，有时需要把逻辑分布到不同的 MonoBehaviour 里（`FixedUpdate` 做物理，`LateUpdate` 做相机）。这种拆分是框架决定的，在约束下是合理的。

**测试隔离**：为了让某段逻辑可测试，可能把它提取到小的可注入接口里，即使这个接口很浅。这是有意识的权衡——用结构复杂度换取可测试性。

关键词是**有意识**。如果你创建一个浅模块，你应该清楚知道为什么、代价是什么、这个代价是否值得。

而 Classitis 的危害在于，它通常是**无意识**的——没有想过「这样拆有什么代价」，只是机械遵循「类要小」的教条。这种无意识的分割，累积起来造成系统级的复杂度爆炸。

---

## 八、品味判断：评判设计的问题

评判一个设计好不好，有几个具体问题可以问：

**「理解这个功能，我需要打开几个文件？」** 如果答案是一个，通常是好设计。如果是五个、十个，需要警惕。

**「做一个合理的功能改动，我需要修改几个地方？」** 如果改一个功能需要改七个文件，这个系统的耦合是不健康的。

**「有一个新来的开发者，他需要多久才能理解这个模块的作用？」** 这个心理模型的建立成本，是系统认知负担的直接体现。

真正优秀的系统设计，往往违反我们的第一直觉。一个深模块看起来可能「做了太多事」——这违反了 SRP 的直觉。一个把玩家逻辑都放在一起的 PlayerController 看起来可能「太大了」——这违反了「类应该小」的直觉。但这些「违反直觉」的选择，在实际工程实践中往往更强大。

**重要的不是大小，而是深度。**

---

> 衡量一个模块好坏的真正标准，不是它有多少行代码，而是它帮调用者隐藏了多少他不需要知道的事情。

---

## 🎯 今日测验

**Q1（概念）：** 用自己的话解释「浅模块」和「深模块」的区别。为什么 Ousterhout 认为「类应该小」这个建议是有害的？他反对的是什么，他提倡的是什么？

**Q2（应用）：** 在你现在或曾经参与的 Unity 项目里，找一个 Classitis 的实例——多个小类/Manager 共同完成一件事，但理解起来需要跨越很多文件。用今天的理论分析它的问题，并描述一个更深的设计方案。

**Q3（品味）：** 有两种设计方案：A）一个 `AudioSystem` 类，有 200 行代码，直接引用了 `GameState`、`PlayerController`、`EventBus`，处理所有音效逻辑；B）五个小类 `MusicManager`、`SFXManager`、`VoiceManager`、`AudioEventHandler`、`AudioStateObserver`，通过事件系统相互通信，每个类 30-50 行。哪个设计更好？在什么条件下 A 更好？在什么条件下 B 更好？

> 回复本条消息即可作答，你的回答会影响明天的推送深度和方向。
