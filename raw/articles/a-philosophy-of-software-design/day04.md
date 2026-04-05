# Day 4 · 深模块 — 最重要的设计原则

**APoSD Ch4 | John Ousterhout 最核心的设计洞察**

---

如果你只能从这本书里带走一个概念，那就是今天这个：**深模块（Deep Module）**。

Ousterhout 在斯坦福教了几十年软件设计课，看过无数学生的代码，也看过无数工业级系统的腐化过程。他观察到一个反复出现的模式：程序员把系统拆成一堆小类、小方法、小模块，每个都「职责单一」，每个都「短小精悍」，然后……整个系统变得越来越难以理解。

不是因为某一个类写错了，而是因为接口和接口之间的缝隙积累了无数的复杂性。

这是一个反直觉的结论。今天我们来把它彻底搞清楚。

---

## 一、模块化设计的真正目标

> "In modular design, a software system is decomposed into a collection of modules that are relatively independent. Modules can take many forms, such as classes, subsystems, or services. In an ideal world, each module would be completely independent of the others: a developer could work in any of the modules without knowing anything about any of the other modules."

注意这句话：**开发者在任意一个模块里工作时，不需要了解其他模块**。

这才是模块化的核心价值。不是「拆分」，不是「单一职责」，而是**认知隔离（cognitive isolation）**。

但 Ousterhout 马上承认这个理想是无法完全实现的：

> "Unfortunately, this ideal is not achievable. Modules must work together by calling each others's functions or methods. As a result, modules must know something about each other."

所以现实的目标是：**最小化模块之间的依赖**。

这里有一个关键的思维转变。大多数程序员把模块化理解为「怎么拆分系统」，但 Ousterhout 把它理解为「怎么控制认知成本」。两种理解方式会导致完全不同的设计决策。

按「怎么拆分」思考的人，会根据功能边界来切割——用户管理是一个模块、订单处理是一个模块、支付是一个模块。这没错，但在这个框架内，他们可能会进一步把用户管理拆成用户创建、用户更新、用户查询、用户删除四个类，把每个类再拆成读服务和写服务……

按「怎么控制认知成本」思考的人，会问：**当我在写 A 模块的时候，我需要同时在脑子里装着哪些其他东西？** 这些「其他东西」就是认知成本。好的模块设计让这个成本最小化。

---

## 二、接口是模块的成本，实现是模块的收益

这是整章最核心的比喻，值得反复读：

> "The benefit provided by a module is its functionality. The cost of a module (in terms of system complexity) is its interface. A module's interface represents the complexity that the module imposes on the rest of the system: the smaller and simpler the interface, the less complexity that it introduces."

**功能是收益，接口是成本。**

这个视角非常不寻常。通常我们把接口理解为「提供服务的入口」，是正面的东西。但 Ousterhout 说：**每一个接口方法都是一个负担**，是调用者必须学习的东西，是必须在脑子里维持的知识，是可能出错的地方。

接口的成本包含两种：

**形式化信息（Formal）**：方法签名、参数类型、返回值类型、异常。这些编译器能检查。

**非形式化信息（Informal）**：

> "The informal parts of an interface include its high-level behavior, such as the fact that a function deletes the file named by one of its arguments. If there are constraints on the usage of a class (perhaps one method must be called before another), these are also part of the class's interface."

这些编译器不能检查，只能靠文档和注释。而且：

> "For most interfaces the informal aspects are larger and more complex than the formal aspects."

这句话让我每次看都觉得震撼。一个方法的签名可能只有一行，但它隐含的使用约束、副作用、调用顺序要求、线程安全保证……这些非形式化信息往往比签名本身复杂得多。

所以当你设计模块时，减少接口面积不仅仅是减少方法数量，更是减少调用者需要理解的隐性约定。

---

## 三、深模块是什么

现在来到今天的主角：

> "The best modules are those that provide powerful functionality yet have simple interfaces. I use the term deep to describe such modules."

**深 = 功能强大，接口简单。**

Ousterhout 用矩形来可视化这个概念。矩形的面积代表功能，矩形的宽度（顶边长度）代表接口复杂度。深模块是一个高而窄的矩形——大面积，小宽度。浅模块是一个矮而宽的矩形——小面积，大宽度。

然后他给出了一个我认为是软件史上最美的例子：**Unix I/O**。

```c
int open(const char* path, int flags, mode_t permissions);
ssize_t read(int fd, void* buffer, size_t count);
ssize_t write(int fd, const void* buffer, size_t count);
off_t lseek(int fd, off_t offset, int referencePosition);
int close(int fd);
```

五个系统调用。就这五个。

但它们背后隐藏了什么？

> "A modern implementation of the Unix I/O interface requires hundreds of thousands of lines of code, which address complex issues such as:
> - How are files represented on disk in order to allow efficient access?
> - How are directories stored, and how are hierarchical path names processed?
> - How are permissions enforced?
> - How is functionality divided between interrupt handlers and background code?
> - What scheduling policies are used when there are concurrent accesses?
> - How can recently accessed file data be cached in memory?
> - How can a variety of different secondary storage devices be incorporated into a single file system?"

几十万行代码，处理磁盘布局、目录结构、权限系统、中断处理、并发调度、缓存策略、设备抽象……全部隐藏在这五个函数后面。

**这就是深模块的力量。**

作为调用者，你只需要知道：
- `open` 打开文件，返回文件描述符
- `read` 从文件读数据
- `write` 向文件写数据
- `lseek` 调整读写位置
- `close` 关闭文件

你不需要知道文件系统的实现。你不需要知道缓存策略。你不需要知道如何处理并发访问。这些复杂性全部被接口的简洁性「吃掉了」。

更妙的是：

> "Implementations of the Unix I/O interface have evolved radically over the years, but the five basic kernel calls have not changed."

接口几十年不变，但实现可以大幅改进。这是深模块的另一个重要好处——实现的变化不会影响调用者。

---

## 四、垃圾回收——最深的模块

Ousterhout 给出的另一个例子更极端：

> "Another example of a deep module is the garbage collector in a language such as Go or Java. This module has no interface at all; it works invisibly behind the scenes to reclaim unused memory. Adding garbage collection to a system actually shrinks its overall interface, since it eliminates the interface for freeing objects."

**垃圾回收器是接口为零的深模块。**

想想 C/C++ 里的手动内存管理。`malloc` / `free`，或者 `new` / `delete`，或者智能指针的 `release`……这些都是接口。调用者需要理解所有权语义、什么时候该释放、谁负责释放、如果忘了会发生什么。

Java 的 GC 消灭了所有这些接口。你不需要调用任何东西，不需要记任何约定，不需要追踪对象的生命周期。GC 的实现极其复杂（标记清除、分代回收、并发 GC、暂停时间优化……），但这些复杂性对你完全不可见。

这是一个反直觉的洞察：**有时候让模块更深的最好方式，是让它完全没有接口。**

---

## 五、抽象的真正定义

在讨论深模块的时候，Ousterhout 提出了一个对「抽象」的精确定义：

> "An abstraction is a simplified view of an entity, which omits unimportant details."

这里关键词是**「不重要的细节」（unimportant details）**。抽象不是任意的简化，而是有选择地省略不重要的细节。

但「不重要」很难判断。Ousterhout 警告了两种抽象失败的方式：

**第一种：包含了不重要的细节**

接口比必要的更复杂。比如你要实现一个哈希表，但接口里暴露了「当前使用的哈希算法」这个参数——大多数调用者根本不需要知道这个，反而增加了他们的认知负担。

**第二种：省略了重要的细节**

> "An abstraction that omits important details is a false abstraction: it might appear simple, but in reality it isn't."

这更危险。看起来简单，实际上是个陷阱。Ousterhout 举了文件系统缓存的例子：文件系统对外看起来很简单，但如果你是数据库开发者，你必须知道「数据什么时候才真正写到磁盘」——这个细节很重要，如果接口隐藏了它，就是虚假抽象。

这个概念在游戏开发中太常见了。我见过很多「简洁」的资源管理接口：

```csharp
// 看起来很简单
GameObject obj = ResourceManager.Load("prefabs/bullet");
```

但调用者需要不需要管 `obj` 的生命周期？是引用计数还是 GC 管理？调用 `Load` 后资源会不会在下次场景切换时被卸载？如果这些信息在接口里看不到，就是典型的虚假抽象——简单的外表下是一个定时炸弹。

---

## 六、浅模块的罪行

现在来看反面教材。Ousterhout 给出了一个极端的浅方法例子：

```java
private void addNullValueForAttribute(String attribute) {
    data.put(attribute, null);
}
```

> "The method offers no abstraction, since all of its functionality is visible through its interface. For example, callers probably need to know that the attribute will be stored in the data variable. It is no simpler to think about the interface than to think about the full implementation."

这个方法是负数价值的。它增加了一个接口（调用者需要学习），但没有隐藏任何实现细节（调用者仍然需要知道 `data` 变量的存在）。

> "It even takes more keystrokes to invoke the method than it would take for a caller to manipulate the data variable directly."

直接写 `data.put(attribute, null)` 比调用这个方法还少打几个字。这个「封装」是纯粹的负担。

更重要的是深度的计算：**接口复杂度 ≈ 实现复杂度** 的时候，模块深度接近 0，即使它能「正确工作」，对管理系统复杂性没有任何贡献。

---

## 七、Classitis——一种流行病

这里 Ousterhout 真的生气了。

> "The extreme of the 'classes should be small' approach is a syndrome I call classitis, which stems from the mistaken view that 'classes are good, so more classes are better.'"

Classitis（类癌）是他自己发明的词。他观察到 Java 社区尤其严重地患了这种病：

```java
FileInputStream fileStream = new FileInputStream(fileName);
BufferedInputStream bufferedStream = new BufferedInputStream(fileStream);
ObjectInputStream objectStream = new ObjectInputStream(bufferedStream);
```

读一个序列化文件需要三个对象。这三个对象之间有依赖：你必须按这个顺序创建，前两个创建后几乎不会单独使用。

> "It is particularly annoying (and error-prone) that buffering must be requested explicitly by creating a separate BufferedInputStream object; if a developer forgets to create this object, there will be no buffering and I/O will be slow."

忘记 `BufferedInputStream` 不会有编译错误，也不会有运行时错误，只会悄悄地性能很差。这是信息泄漏（缓冲这个实现细节泄漏到了调用者）和虚假抽象（接口看起来在做 I/O，但实际上你要懂得什么时候需要缓冲）的双重罪行。

反观 Unix I/O：

> "In contrast, the designers of the Unix system calls made the common case simple. For example, they recognized that sequential I/O is most common, so they made that the default behavior. Random access is still relatively easy to do, using the lseek system call, but a developer doing only sequential access need not be aware of that mechanism."

**把常见情况做简单，把不常见情况做可能**。这是接口设计的黄金法则。

注意这里的品味判断：Java I/O 把三种能力（文件访问、缓冲、序列化）分成三个类，是「正交性」设计。这听起来很合理——每个类做一件事，可以自由组合。但问题在于：99% 的情况你都需要缓冲，所以把缓冲单独拆出来不是在提供灵活性，而是在制造陷阱。

---

## 八、在游戏引擎开发中的深模块设计

作为做过 3 年以上引擎开发的人，这个概念你一定有切身体会，只是可能没有这个词汇来描述它。

**渲染系统的深度**

一个好的渲染系统接口应该是什么样的？

```csharp
// 浅的版本（接口泄漏了实现细节）
void SetVertexBuffer(VertexBuffer vb);
void SetIndexBuffer(IndexBuffer ib);
void SetShader(Shader shader);
void SetTexture(int slot, Texture tex);
void SetConstantBuffer(int slot, ConstantBuffer cb);
void DrawIndexed(int indexCount, int startIndex, int startVertex);
```

```csharp
// 深的版本（接口隐藏了渲染状态管理）
void DrawMesh(Mesh mesh, Material material, Matrix4x4 transform);
```

前者暴露了 GPU 编程的所有细节——顶点缓冲、索引缓冲、常量缓冲绑定槽位。每个调用者都需要懂 D3D/Metal 的资源绑定模型。后者隐藏了所有这些，调用者只需要说「在这个位置用这个材质画这个网格」。

Unity 的 `Graphics.DrawMesh` 和 Unreal 的 `DrawRenderState` 都在朝这个方向设计——虽然底层有大量状态管理的复杂性，但暴露给游戏逻辑层的接口是高层次的。

**ECS 的深度**

Unity DOTS 的 ECS（Entity Component System）是另一个有趣的案例。表面上看，ECS 是「浅」的——Entity 只是一个 ID，Component 只是数据，System 只是处理逻辑，三者分离。

但实际上 ECS 框架隐藏了大量复杂性：内存布局优化（相同类型的 Component 连续存储）、作业系统的线程调度、Chunk 的动态分配和碎片整理……从游戏逻辑开发者的视角看，这些全都不可见。

这就是为什么好的 ECS 框架感觉「很深」——你用简单的 `World.CreateEntity()` 和 `EntityManager.AddComponent()` 就能得到高性能的数据导向架构，背后的复杂性完全被框架吸收了。

**资源系统的典型浅模块问题**

我见过很多游戏项目的资源系统设计是这样的：

```csharp
// 调用者需要知道：
// 1. 引用计数的存在
// 2. 需要手动 Retain
// 3. 使用完要手动 Release
// 4. 不 Release 会内存泄漏
// 5. Release 过多会 crash

ResourceHandle handle = ResourceManager.Load("bullet");
handle.Retain();           // 必须手动 retain
// ... 使用 handle ...
handle.Release();          // 必须手动 release
```

和 Java 的 `FileInputStream + BufferedInputStream` 是同一种病——把资源管理的复杂性推给了调用者。

深的资源系统应该是：

```csharp
// RAII 风格，出作用域自动释放
using (var bullet = ResourceManager.Load<GameObject>("bullet"))
{
    // 用 bullet ...
} // 自动 Release，不需要手动管理
```

或者更彻底：用 Unity 的 `Addressables` 系统，资源的加载、缓存、卸载全部由系统管理，调用者只需要一个 `AssetReference`。

---

## 九、与 Clean Code 和 Design Patterns 的对比

这本书和罗伯特·马丁的《Clean Code》在某些观点上直接冲突，值得明说。

**关于「函数应该短小」**

《Clean Code》大力提倡函数要短，有人建议不超过 10 行，最好 5 行以内。

Ousterhout 的反驳：

> "Any method longer than N lines should be divided into multiple methods. This approach results in large numbers of shallow classes and methods, which add to overall system complexity."

他并不是说长方法一定好，而是说**拆分的标准应该是「是否增加了深度」，而不是「是否超过了 N 行」**。

一个 50 行的方法，如果它的逻辑是线性的、自包含的、有清晰的意图，可能比把它拆成 5 个 10 行的方法更好理解。5 个方法意味着 5 个接口，意味着阅读代码时需要在 5 个地方之间跳转。

**关于「单一职责原则」（SRP）**

SRP 说每个类只做一件事。听起来很有道理，但「一件事」的粒度是什么？

Ousterhout 的框架给了 SRP 一个可操作的解释：**一个类的「职责」边界应该由信息隐藏来决定**。如果两个功能共享相同的内部信息（数据结构、算法知识），它们应该在同一个类里。如果强行分开，信息就会泄漏，接口就会变多，系统整体复杂性就会增加。

这比「每个类只做一件事」更精确，也更有实操指导意义。

**关于设计模式**

设计模式（Gang of Four）很多都是「浅模块」的。

Decorator 模式：给对象动态添加功能。但每个 Decorator 都是一个浅模块——它本身功能很少（只是转发加一点点逻辑），却有和被装饰对象相同的接口成本。用多了就是 Classitis。

Strategy 模式：把算法封装成对象。但如果策略类很小，接口成本可能大于算法实现本身的复杂性。

这不是说模式不好，而是说：**模式应该在增加模块深度的时候使用，而不是作为「好的面向对象设计」的通用标志**。

---

## 十、如何判断一个模块是否够深

给你一个实用的启发式方法：

**1. 文档比率测试**

给这个模块的接口写文档，包括所有参数的含义、前置条件、后置条件、异常情况。

如果文档长度接近或超过实现代码长度——这个模块可能太浅了。

Ousterhout 提到了这一点：

> "If the method is documented properly, the documentation will be longer than the method's code."

一个方法，如果文档比代码还长，很可能是浅方法。

**2. 调用者知识测试**

让一个新成员使用你的模块。记录他在使用过程中需要查阅多少额外信息（除了接口本身）。

如果他需要查看实现代码才能正确使用接口——接口里缺少重要信息（虚假抽象或信息泄漏）。

如果他面对接口感到困惑，有很多参数不知道怎么填——接口太复杂，可能是浅模块。

**3. 常见情况测试**

对于这个模块最常见的使用场景（80% 的调用），调用者需要处理多少接口？

Unix `open + read + close` 的顺序文件读取只需要三个调用，每个参数都很直观。Java 需要三个对象，而且必须记住缓冲。前者的「常见情况复杂度」远低于后者。

**4. 实现变化测试**

如果你改变了模块的内部实现（比如换了数据结构、优化了算法），调用者代码需要修改吗？

如果需要修改——说明实现细节泄漏到了接口。

---

## 十一、游戏引擎中的深度量化

给你一个具体的量化练习（适合下次做 Code Review 时用）：

```
模块深度 = 功能行数（实现） / 接口行数（文档化的接口）
```

比例越高，模块越深。

```csharp
// 渲染命令缓冲区
public class CommandBuffer
{
    // 接口：3个方法，合计约10行文档
    public void DrawMesh(Mesh mesh, Matrix4x4 matrix, Material material);
    public void SetRenderTarget(RenderTexture rt);
    public void Execute();
    
    // 实现：内部状态管理、命令排序、GPU 同步、内存管理，约500行
}
```

深度 ≈ 500/10 = 50。非常深，好的设计。

```csharp
// 属性包装器（典型浅模块）
public class PlayerHealth
{
    private int _health;
    
    // 接口：2个方法，文档约等于实现
    public int GetHealth() => _health;
    public void SetHealth(int value) => _health = value;
}
```

深度 ≈ 2/4 = 0.5。极浅，这个类应该被质疑是否有存在的必要。

---

## 今日品味总结

**深模块设计的三个原则：**

1. **最小化接口，最大化功能**：每增加一个接口方法，都要问「调用者真的需要控制这个吗，还是模块内部可以有合理默认值？」

2. **常见情况应该是最简单的**：设计接口时，想象最频繁的使用场景，让那个场景的调用代码最简洁。不常见的场景可以更复杂。

3. **实现细节不应该泄漏**：如果调用者需要理解你的实现才能正确使用接口，这个接口的设计是失败的。

**一个判断标准**：好的模块让你「不需要打开实现代码就能自信地使用它」。如果你经常需要看源码才知道怎么用一个 API，这个 API 的设计者欠你一个道歉。

---

> **今日品味结晶：** 接口不是「提供服务的门」，而是「强加给调用者的负担」。每多一个方法、每多一个参数、每多一个需要调用者理解的约定，都是在加重所有使用这个模块的人的认知负荷。深模块设计的本质是一种慷慨——把复杂性留给自己，把简单留给世界。

---

## 🎯 今日测验

**Q1（概念）：** Ousterhout 说「接口是模块的成本，实现是模块的收益」。用你自己的话解释这句话，并举一个你在实际项目中见过的「接口成本高于实现收益」的例子（即浅模块）。

**Q2（应用）：** 你在做一个游戏的 Audio 系统设计，目前有两个方案：
- **方案 A（深）**：`AudioManager.Play(string clipName, float volume = 1.0f)` — 内部自动管理 AudioSource 池、3D 音效的空间化、音量归一化、同一帧多次播放的去重
- **方案 B（浅）**：`AudioSource source = AudioPool.Get(); source.clip = AudioClip.Load(clipName); source.volume = volume; source.spatialBlend = 0; source.Play();`

从「深模块」原则分析，哪个方案更好？方案 A 的深度是否有可能「过头」（隐藏了调用者需要知道的信息）？什么情况下需要同时提供两种接口？

**Q3（品味判断）：** 以下是 Unity UGUI 的 `Text.text` 属性 vs `TextMeshPro` 的 `SetText` 方法：

```csharp
// UGUI Text
text.text = "Score: 100";  // 简单赋值

// TextMeshPro（推荐的性能优化做法）
textMeshPro.SetText("Score: {0}", score);  // 避免字符串拼接
```

从深模块的角度，`SetText` 是更深还是更浅的接口？为什么 TMP 设计了两种方式（`text` 属性赋值 和 `SetText` 方法）？这个设计决策好不好，为什么？

> 回复本条消息即可作答，你的回答会影响明天的推送深度和方向。

---

*Day 4 / 30 · APoSD Coach 模式 · 实时生成*
