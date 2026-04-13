---
title: Unity 中用有限状态机来实现一个 AI
url: http://frankorz.com/2018/06/22/finite-state-machine-in-unity/
author: 文章作者 猫冬
published: '2018-06-22'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

最近在阅读《游戏人工智能编程案例精粹（修订版）》，本文是书中第二章的一篇笔记。

有限状态机（英语：Finite-state machine, 缩写：FSM），是一个被数学家用来解决问题的严格形式化的设备，在游戏业中也常见有限状态机的身影。

对于游戏程序员来说，可以用下面这个定义来了解：

一个有限状态机是一个设备（device），或是一个设备模型（a model of a device）。具有有限数量的状态，它可以在任何给定的时间根据输入进行操作，是的从一个状态变换到另一个状态，或者是促使一个输出或者一种行为的发生。一个有限状态机在任何瞬间只能处在一种状态。
——《游戏人工智能编程案例精粹（修订版）》 Mat Buckland

有限状态机就是要把一个对象的行为分解成易于处理的“块”或者状态。拿某个开关来说，我们可以把它分成两个状态：开或关。其中开开关这个操作，就是一次状态转移 ，使开关的状态从“关”变换到“开”，反之亦然。

拿游戏来举例，一个 FPS 游戏中的敌人 AI 状态可以分成：巡逻、侦查（听到了玩家）、追逐（玩家出现在 AI 视野）、攻击（玩家进入 AI 攻击范围）、死亡等，这些有限的 状态都互相独立 ，且要满足某种条件 才能从一个状态转移到另外一个状态。

有限状态机由三部分组成：

存储任务信息的一些状态（states） ，例如一个 AI 可以有探索状态、追踪状态、攻击状态等等。
状态之间的一些变换（transitions） ，转移代表状态的转移，并且描述着状态转移的条件。例如听到了主角的脚步声，就转移到追踪状态。
需要跟随每个状态的一系列行为（actions） 。例如在探索状态，要随机移动和找东西。
下图是只有三种状态的 AI 的有限状态机图示：

优缺点
实现有限状态机之前，要先了解它的优点：

编程快速简单 ：很多有限状态机的实现都较简单，本文会列出三种实现方法。
易于调试 ：因为行为被分成单一的状态块，因此要调试的时候，可以只跟踪某个异常状态的代码。
很少的计算开销 ：几乎不占用珍贵的处理器时间，因为除了 if-this-then-that 这种思考处理之外，是不存在真正的“思考”的。
直觉性 ：人们总是自然地把事物思考为处在一种或另一种状态。人类并不是像有限状态机一样工作，但我们发现这种方式下考虑行为是很有用的，或者说我们能更好更容易地进行 AI 状态的分解和创建操作 AI 的规则，容易理解的概念也让程序员之间能更好地交流其设计。
灵活性 ：游戏 AI 的有限状态机能很容易地由程序员进行调整，增添新的状态和规则也很容易扩展一个 AI 的行为。
有限状态机的缺点是：

当状态过多时，难以维护代码。
《AI Game Development》的作者 Alex J. Champandard 发表过一篇文章《10 Reasons the Age of Finite State Machines is Over》
if-then 实现
这是第一种实现有限状态机的方法，用一系列 if-then 语句或者 switch 语句来表达状态。

下面拿那个只有三个状态的僵尸 AI 举例：

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 public enum ZombieState{ Chase, Attack, Die } public class Zombie : MonoBehaviour { private ZombieState currentState; private void Update () { switch (currentState) { case ZombieState.Chase: if (currentHealth <= 0 ) { ChangeState(ZombieState.Die); } if (PlayerInAttackRange()) { ChangeState(ZombieState.Attack); } break ; case ZombieState.Attack: if (currentHealth <= 0 ) { ChangeState(ZombieState.Die); } if (!PlayerInAttackRange()) { ChangeState(ZombieState.Chase); } break ; case ZombieState.Die: Debug.Log("僵尸死亡" ); break ; } } }

这种写法能实现有限状态机，但当游戏对象复杂到一定程度时，case 就会变得特别多，使程序难以理解、调试。另外这种写法也不灵活，难以扩展超出它原始设定的范围。

此外，我们常需要在进入状态 和退出状态 时做些什么，例如僵尸在开始攻击时像猩猩一样锤几下胸口，玩家跑出攻击范围的时候，僵尸要“摇摇头”让自己清醒，好让自己打起精神继续追踪玩家。

状态变换表
一个用于组织状态和影响状态变换的更好的机制是一个状态变换表 。

当前状态
条件
状态转移
追踪
玩家进入攻击范围
攻击
追踪
僵尸生命值小于或等于0
死亡
攻击
玩家脱离攻击范围
追踪
攻击
僵尸生命值小于或等于0
死亡

这表格可以被僵尸 AI 不间断地查询。使得它能基于从游戏环境的变化来进行状态变换。每个状态可以模型化为一个分离的对象或者存在于 AI 外的函数。提供了一个清楚且灵活的结构。

我们只用告诉僵尸它有多少个状态，僵尸则会根据自己获得的信息（例如玩家是否在它的攻击范围内）来处理规则（转移状态）。

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 public class Zombie : MonoBehaviour { private ZombieState currentState; private void Update () { if (currentHealth <= 0 ) { ChangeState(ZombieState.Die); return ; } if (PlayerInAttackRange()) { ChangeState(ZombieState.Attack); } else { ChangeState(ZombieState.Chase); } } }

内置规则
另一种方法就是将状态转移规则内置到状态内部 。

在这里，每一个状态都是一个小模块，虽然每个模块都可以意识到其他模块的存在，但是每个模块都是一个独立的单位，而且不依赖任何外部的逻辑来决定自己是否要进行状态转移。

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 public class Zombie : MonoBehaviour { private State currentState; public int CurrentHealth { get ; private set ; } private void Update () { currentState.Execute(this ); } public void ChangeState (State state ) { currentState = state; } public bool PlayerInAttackRange () { return result; } } public abstract class State { public abstract void Execute (Zombie zombie ) ; } public class ChaseState : State { public override void Execute (Zombie zombie ) { if (zombie.CurrentHealth <= 0 ) { zombie.ChangeState(new DieState()); } if (zombie.PlayerInAttackRange()) { zombie.ChangeState(new AttackState()); } } } public class AttackState : State { public override void Execute (Zombie zombie ) { if (zombie.CurrentHealth <= 0 ) { zombie.ChangeState(new DieState()); } if (!zombie.PlayerInAttackRange()) { zombie.ChangeState(new ChaseState()); } } } public class DieState : State { public override void Execute (Zombie zombie ) { Debug.Log("僵尸死亡" ); } }

`Update()`

函数只需要根据 `currentState`

来执行代码，当 `currentState`

改变时，下一次 `Update()`

的调用也会进行状态转移。这三个状态都作为对象封装，并且都给出了影响状态转移的规则（条件）。

这个结构被称为状态设计模式（state design pattern） ，它提供了一种优雅的方式来实现状态驱动行为。这种实现编码简单，容易扩展，也可以容易地为状态增加进入 和退出 的动作。下文会给出更完整的实现。

West World 项目
这项目是关于使用有限状态机创建一个 AI 的实际例子。游戏环境是一个古老西部风格的开采金矿的小镇，称作 West World。一开始只有一个挖金矿工 Bob，后期会加入他的妻子。任何的状态改变或者输出都会出现在控制台窗口中。West World 中有四个位置：金矿，可以存金块的银行，可以解除干渴的酒吧，还有家。矿工 Bob 会挖矿、睡觉、喝酒等，但这些都由 Bob 的当前状态决定。

项目在这里：programming-game-ai-by-example-in-unity/WestWorld/

当你看到矿工改变了位置时，就代表矿工改变了状态，其他的事情都是状态中发生的事情。

Base Game Entity 类
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 public abstract class BaseGameEntity { private int m_ID; public static int m_iNextValidID { get ; private set ; } protected BaseGameEntity (int id ) { m_ID = id; } public int ID { get { return m_ID; } set { m_ID = value ; m_iNextValidID = m_ID + 1 ; } } public abstract void EntityUpdate () ; }

Miner 类
MIner 类是从 BaseGameEntity 类中继承的，包含很多成员变量，代码如下：

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 public class Miner : BaseGameEntity { private State m_pCurrentState; private LocationType m_Location; private int m_iGoldCarried; private int m_iMoneyInBank; private int m_iThirst; private int m_iFatigue; public Miner (int id ) : base (id ) { m_Location = LocationType.Shack; m_iGoldCarried = 0 ; m_iMoneyInBank = 0 ; m_iThirst = 0 ; m_iFatigue = 0 ; m_pCurrentState = GoHomeAndSleepTilRested.Instance; } public override void EntityUpdate () { m_iThirst += 1 ; m_pCurrentState.Execute(this ); } }

Miner 状态
金矿工人有四种状态：

EnterMineAndDigForNugget ：如果矿工没在金矿，则改变位置。在金矿里了，就挖掘金块。
VisitBankAndDepositGold ：矿工会走到银行并且存储他携带的所有天然金矿。
GoHomeAndSleepTilRested ：矿工会回到他的小木屋睡觉知道他的疲劳值下降到可接受的程度。醒来继续去挖矿。
QuenchThirst ：去酒吧买一杯威士忌，不口渴了继续挖矿。
当前状态
条件
状态转移
EnterMineAndDigForNugget
挖矿挖到口袋装不下
VisitBankAndDepositGold
EnterMineAndDigForNugget
口渴
QuenchThirst
VisitBankAndDepositGold
觉得自己存够钱能安心了
GoHomeAndSleepTilRested
VisitBankAndDepositGold
没存够钱
EnterMineAndDigForNugget
GoHomeAndSleepTilRested
疲劳值下降到一定程度
EnterMineAndDigForNugget
QuenchThirst
不口渴了
EnterMineAndDigForNugget

再谈状态设计模式
之前提到要为状态实现进入 和退出 这两个一个状态只执行一次的逻辑，这样可以增加有限状态机的灵活性。下面是威力加强版：

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 public abstract class State { public abstract void Enter (Miner miner ) ; public abstract void Execute (Miner miner ) ; public abstract void Exit (Miner miner ) ; }

这两个增加的方法只有在矿工改变状态时才会被调用。我们也需要修改 `ChangeState`

方法的代码如下：

1 2 3 4 5 6 7 8 9 public void ChangeState (State state ){ m_pCurrentState.Exit(this ); m_pCurrentState = state; m_pCurrentState.Enter(this ); }

另外，每个具体的状态都添加了单例模式 ，这样可以节省内存资源，不必重复分配和释放内存给改变的状态。以其中一个状态为例子：

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 public class EnterMineAndDigForNugget : State { public static EnterMineAndDigForNugget Instance { get ; private set ; } static EnterMineAndDigForNugget () { Instance = new EnterMineAndDigForNugget(); } public override void Enter (Miner miner ) { if (miner.Location() != LocationType.Goldmine) { Debug.Log("矿工：走去金矿" ); miner.ChangeLocation(LocationType.Goldmine); } } public override void Execute (Miner miner ) { miner.AddToGoldCarried(1 ); miner.IncreaseFatigue(); Debug.Log("矿工：采到一个金块 | 身上有 " + miner.GoldCarried() + " 个金块" ); if (miner.PocketsFull()) { miner.ChangeState(VisitBankAndDepositGold.Instance); } if (miner.Thirsty()) { miner.ChangeState(QuenchThirst.Instance); } } public override void Exit (Miner miner ) { Debug.Log("矿工：离开金矿" ); } }

看到这里，大家应该都会很熟悉。这不就是 Unity 中动画控制器 Animator 的功能吗！

没错，Animator 也是一个状态机，有和我们之前实现十分相似的功能，例如：添加状态转移的条件，每个状态都有进入、执行、退出三个回调方法供使用。


我们可以创建 Behaviour 脚本，对 Animator 中每一个状态的进入、执行、退出等方法进行自定义，所以有些人直接拿 Animator 当状态机来使用，不过我们在下文还会为我们的状态机实现扩展更多的功能。

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 public class NewState : StateMachineBehaviour { }

使 State 基类可重用
由于上面四个状态是矿工独有的状态，如果要新建不同功能的角色，就有必要创建一个分离的 State 基类，这里用泛型实现。

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 public abstract class State <T >{ public abstract void Enter (T entity ) ; public abstract void Execute (T entity ) ; public abstract void Exit (T entity ) ; }

状态翻转（State Blip）
这个项目其实有点像模拟人生这个游戏，其中有一点有意思的是，当模拟人生的主角做某件事时忽然要上厕所，去完之后会继续做之前停止的事情。这种返回前一个状态的行为就是状态翻转（State Blip） 。

1 2 3 private State<T> m_pCurrentState;private State<T> m_pPreviousState;private State<T> m_pGlobalState;

`m_pGlobalState`

是一个全局状态，也会在 `Update()`

函数中和 `m_pCurrentState`

一起调用。如果有紧急的行为中断状态，就把这行为（例如上厕所）放到全局状态中，等到全局状态为空再进入当前状态。

1 2 3 4 5 6 7 8 9 10 11 12 13 public void StateUpdate (){ if (m_pGlobalState != null ) { m_pGlobalState.Execute(m_pOwner); } if (m_pCurrentState != null ) { m_pCurrentState.Execute(m_pOwner); } }

StateMachine 类
通过把所有与状态相关的数据和方法封装到一个 StateMachine 类中，可以使得设计更为简洁。

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 public class StateMachine <T >{ private T m_pOwner; private State<T> m_pCurrentState; private State<T> m_pPreviousState; private State<T> m_pGlobalState; public StateMachine (T owner ) { m_pOwner = owner; } public void SetCurrentState (State<T> state ) { m_pCurrentState = state; } public void SetPreviousState (State<T> state ) { m_pPreviousState = state; } public void SetGlobalState (State<T> state ) { m_pGlobalState = state; } public void StateMachineUpdate () { if (m_pGlobalState != null ) { m_pGlobalState.Execute(m_pOwner); } if (m_pCurrentState != null ) { m_pCurrentState.Execute(m_pOwner); } } public void ChangeState (State<T> newState ) { m_pPreviousState = m_pCurrentState; m_pCurrentState.Exit(m_pOwner); m_pCurrentState = newState; m_pCurrentState.Enter(m_pOwner); } public void RevertToPreviousState () { ChangeState(m_pPreviousState); } public State<T> CurrentState () { return m_pCurrentState; } public State<T> PreviousState () { return m_pPreviousState; } public State<T> GlobalState () { return m_pGlobalState; } public bool IsInState (State<T> state ) { return m_pCurrentState == state; } }

新人物 Elsa
第二个项目会演示之前的改进。Elsa 是矿工 Bob 的妻子，她会清理小木屋和上厕所（老喝咖啡）。其中 VisitBathroom 状态是用状态翻转实现的，即上完厕所要回到之前的状态。

项目地址：programming-game-ai-by-example-in-unity/WestWorldWithWoman/


消息功能
好的游戏实现趋向于事件驱动。即当一件事情发生了（发射了武器，主角发出了声音等等），事件会被广播给游戏中相关的对象。

整合事件（观察者模式）的状态机可以实现更灵活的需求，例如：一个足球运动员从队友旁边通过时，传球者可以发送一个（延时）消息，通知队友应该什么时候到相应位置来接球；一个士兵正在开枪攻击敌人，忽然一个队友中了流弹，这时候队友可以发送一个（即时）消息，通知士兵立刻救援队友。

Telegram 结构
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 public struct Telegram{ public BaseGameEntity Sender { get ; private set ; } public BaseGameEntity Receiver { get ; private set ; } public MessageType Message { get ; private set ; } public float DispatchTime { get ; private set ; } public Dictionary<string , string > ExtraInfo { get ; private set ; } public Telegram (float time, BaseGameEntity sender, BaseGameEntity receiver, MessageType message, Dictionary<string , string > extraInfo = null ) : this () { Sender = sender; Receiver = receiver; DispatchTime = time; Message = message; ExtraInfo = extraInfo; } }

这里用结构体来实现消息。要发送的消息可以作为枚举加在 `MessageType`

中，DispatchTime 是决定立刻发送还是延时发送的时间戳，ExtraInfo 能携带额外的信息。这里只用两种消息做例子。

1 2 3 4 5 6 7 8 9 10 11 12 public enum MessageType{ HiHoneyImHome, StewReady, }

发送消息
下面是 MessageDispatcher 类，用来管理消息的发送。

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 102 103 104 105 106 107 108 109 110 public class MessageDispatcher { public static MessageDispatcher Instance { get ; private set ; } static MessageDispatcher () { Instance = new MessageDispatcher(); } private MessageDispatcher () { priorityQueue = new HashSet<Telegram>(); } private HashSet<Telegram> priorityQueue; public void Discharge (BaseGameEntity receiver, Telegram telegram ) { if (!receiver.HandleMessage(telegram)) { Debug.LogWarning("消息未处理" ); } } public void DispatchMessage ( float delay, int senderId, int receiverId, MessageType message, Dictionary<string , string > extraInfo ) { BaseGameEntity sender = EntityManager.Instance.GetEntityFromId(senderId); BaseGameEntity receiver = EntityManager.Instance.GetEntityFromId(receiverId); if (receiver == null ) { Debug.LogWarning("[MessageDispatcher] 找不到消息接收者" ); return ; } float currentTime = Time.time; if (delay <= 0 ) { Telegram telegram = new Telegram(0 , sender, receiver, message, extraInfo); Debug.Log(string .Format( "消息发送时间: {0} ，发送者是：{1}，接收者是：{2}。消息是 {3}" , currentTime, sender.Name, receiver.Name, message.ToString())); Discharge(receiver, telegram); } else { Telegram delayedTelegram = new Telegram(currentTime + delay, sender, receiver, message, extraInfo); priorityQueue.Add(delayedTelegram); Debug.Log(string .Format( "延时消息发送时间: {0} ，发送者是：{1}，接收者是：{2}。消息是 {3}" , currentTime, sender.Name, receiver.Name, message.ToString())); } } public void DisplayDelayedMessages () { float currentTime = Time.time; while (priorityQueue.Count > 0 && priorityQueue.First().DispatchTime < currentTime && priorityQueue.First().DispatchTime > 0 ) { Telegram telegram = priorityQueue.First(); BaseGameEntity receiver = telegram.Receiver; Debug.Log(string .Format("延时消息开始准备分发，接收者是 {0}，消息是 {1}" , receiver.Name, telegram.Message.ToString())); Discharge(receiver, telegram); priorityQueue.Remove(telegram); } } }

`DispatchMessage`

函数会管理消息的发送，即时消息会直接由 `Discharge`

函数发送到接收者，延时消息会进入队列，通过 GameManager 游戏主循环，每一帧调用 `DisplayDelayedMessages()`

函数来轮询要发送的消息，当发现当前时间超过了消息的发送时间，就把消息发送给接收者。

处理消息
处理消息的话修改 BaseGameEntity 来增加处理消息的功能。

1 2 3 4 5 6 7 8 9 10 11 12 13 public abstract class BaseGameEntity { public abstract bool HandleMessage (Telegram message ) ; } public class Miner : BaseGameEntity { public override bool HandleMessage (Telegram message ) { return m_stateMachine.HandleMessage(message); } }

StateMachine 代码也要改：

1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 public class StateMachine <T >{ public bool HandleMessage (Telegram message ) { if (m_pCurrentState != null && m_pCurrentState.OnMessage(m_pOwner, message)) { return true ; } if (m_pCurrentState != null && m_pGlobalState.OnMessage(m_pOwner, message)) { return true ; } return false ; } }

State 基类也要修改：

1 2 3 4 5 6 7 8 9 10 public abstract class State <T >{ public abstract bool OnMessage (T entity, Telegram message ) ; }

`Discharge`

函数发送消息给接收者，接收者将消息给他 StateMachine 的 `HandleMessage`

函数处理，消息最后通过 StateMachine 到达各种状态的 `OnMessage`

函数，开始根据消息的类型来做出处理（例如进行状态转移）。

具体实现请看项目代码：programming-game-ai-by-example-in-unity/WestWorldWithMessaging/


这里实现的场景是：

矿工 Bob 回家后发送 HiHoneyImHome 即时消息 给他的妻子 Elsa，提醒她做饭。
Elsa 收到消息后，停止手上的活儿，开始进入 CookStew 状态做饭。
Elsa 进入 CookStew 状态后，把肉放到烤炉里面，并且发送 StewReady 延时消息 提醒自己在一段时间后拿出烤炉中的肉。
Elsa 收到 StewReady 消息后，发送一个 StewReady 即时消息 给 Bob 提醒他饭已经做好了。如果 Bob 这时不在家，命令行将显示 Discharge 函数中的 Warning “消息未处理”。Bob 在家，就会开心地去吃饭。
Bob 收到 StewReady 的消息，状态转移到 EatStew，开始吃饭。
总结
有时候我们可能会用到多个状态机来并行工作，例如一个 AI 有多个状态，其中包括攻击状态，而攻击状态又有不同攻击类型（瞄准和射击），像一个状态机包含另一个状态机这种层次化的状态机 。当然也有其他不同的使用场景，我们不能受限于自己的想象力。

本文根据《游戏人工智能编程案例精粹（修订版）》进行了 Unity 版本的实现，我对有限状态机也有了更清晰的认识。阅读这本书的同时也会把 Unity 实现放到下面的仓库地址中，下篇文章可能会总结行为树的知识，如果没看到请督促我~

项目地址：programming-game-ai-by-example-in-unity

引用