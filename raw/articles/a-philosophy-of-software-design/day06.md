**Day 6 · 信息隐藏 — 深模块的灵魂**

---

如果你只能从《A Philosophy of Software Design》这本书里带走一个概念，我希望那个概念是**信息隐藏（Information Hiding）**。

不是因为它听起来高大上，而是因为它几乎是所有「深模块」背后真正的发动机。昨天我们讲了深模块 vs 浅模块的区别，讲了接口要窄、实现要深。但「如何做到深？」——这个问题的答案就是今天的主角：信息隐藏。

Ousterhout 的原话是：

> "The most important technique for achieving deep modules is information hiding. The basic idea is that each module should encapsulate a few pieces of knowledge, which represent design decisions. The knowledge is embedded in the module's implementation but does not appear in its interface."

翻译成人话：**每个模块应该把某些知识藏起来，这些知识代表了设计决策。这些决策活在实现里，不应该出现在接口上。**

---

## 一、「知识」是什么？

Ousterhout 用了一个特别的词：**knowledge**（知识）。不说「数据」，不说「变量」，不说「算法」，而说知识——因为他想强调的是：**真正需要隐藏的，是设计决策本身**。

比如你写一个游戏里的存档系统，你做了一个决策：存档文件用 JSON 格式。这个决策是一种「知识」——关于文件长什么样、怎么序列化、怎么反序列化。

如果你把这个知识藏在 `SaveSystem` 类的实现里，外面的代码不知道也不在乎是不是 JSON，那你就完成了信息隐藏。有一天你决定把 JSON 换成 Protocol Buffers，只需要改 `SaveSystem` 的内部实现，其他系统完全不受影响。

> "Information hiding reduces complexity in two ways. First, it simplifies the interface. Second, information hiding makes it easier to evolve the system. If a piece of information is hidden, there are no dependencies on that information outside the module, so a design change will affect only the one module."

信息隐藏有两个好处：**简化接口**，以及**让系统更容易演进**。第二个好处在长期项目里价值极大——每次「存档格式」这个知识只在一个地方，修改成本是 O(1)；如果它泄漏到了十几个系统里，每次改动都是一场噩梦。

---

## 二、`private` 关键字 ≠ 信息隐藏

这是今天最容易踩的坑，也是很多人根本没意识到自己踩进去了。

> "Hiding variables and methods by declaring them private isn't the same thing as information hiding. Information about the private items can still be exposed through public methods such as getter and setter methods."

**`private` 是访问控制（Access Control）。信息隐藏是设计哲学（Design Philosophy）。**

**反例：有 `private`，但没有信息隐藏**

```csharp
public class CharacterStats : MonoBehaviour
{
    private Dictionary<string, float> _stats;

    public Dictionary<string, float> GetStats()
    {
        return _stats;  // 返回内部字典的直接引用
    }
}
```

`_stats` 字段是私有的，但通过 `GetStats()` 方法，你把**整个内部实现暴露了出去**——调用方现在知道这个类内部用 `Dictionary<string, float>` 存属性，可以直接往字典里塞任意值破坏所有不变量。

这就是 HTTPRequest 案例的精髓：
- **`getParams()` 返回 `Map<String, String>`** → 浅模块，暴露内部实现
- **`getParameter(String name)` 返回 `String`** → 深模块，隐藏内部实现

**正例：真正的信息隐藏**

```csharp
public class CharacterStats : MonoBehaviour
{
    private Dictionary<string, float> _stats;

    public float GetStat(string statName)
    {
        return _stats.TryGetValue(statName, out float value) ? value : 0f;
    }

    public void SetStat(string statName, float value)
    {
        if (!_stats.ContainsKey(statName))
            throw new ArgumentException($"Unknown stat: {statName}");
        _stats[statName] = Mathf.Max(0, value);  // 在这里加业务约束
    }
}
```

调用方不知道内部是字典还是数组还是别的什么。哪天把 `Dictionary` 换成 `float[]` 提升性能，接口完全不用变。

---

## 三、信息泄漏（Information Leakage）：最危险的红旗

> "Information leakage is one of the most important red flags in software design. If you encounter information leakage between classes, ask yourself 'How can I reorganize these classes so that this particular piece of knowledge only affects a single class?'"

信息泄漏发生在：**一份知识（一个设计决策）同时存在于多个模块里**。当它的实现改变时，所有拥有这份知识的模块都必须跟着改。

### 显式泄漏

```csharp
// 发送方
public class NetworkSender {
    public void SendPosition(Vector3 pos) {
        byte[] data = new byte[12];
        BitConverter.GetBytes(pos.x).CopyTo(data, 0);
        BitConverter.GetBytes(pos.y).CopyTo(data, 4);
        BitConverter.GetBytes(pos.z).CopyTo(data, 8);
        socket.Send(data);
    }
}

// 接收方
public class NetworkReceiver {
    public Vector3 ReceivePosition(byte[] data) {
        float x = BitConverter.ToSingle(data, 0);
        float y = BitConverter.ToSingle(data, 4);
        float z = BitConverter.ToSingle(data, 8);
        return new Vector3(x, y, z);
    }
}
```

「位置的序列化格式」这个知识同时藏在两个类里。改成 `half` 精度？两个类都要改。加 timestamp 字段？两个类都要改。

正确做法：把序列化知识集中到一处。

```csharp
public static class PositionSerializer {
    public static byte[] Serialize(Vector3 pos) { ... }
    public static Vector3 Deserialize(byte[] data) { ... }
}
```

### 后门泄漏（Back-door Leakage）：更可怕的那种

> "Suppose two classes both have knowledge of a particular file format (perhaps one reads files in that format and the other writes them). Even if neither class exposes that information in its interface, they both depend on the file format: if the format changes, both classes will need to be modified. Back-door leakage like this is more pernicious than leakage through an interface, because it isn't obvious."

**Back-door leakage 不会出现在任何接口里，但它实实在在地存在。**

地图编辑器例子：`MapExporter` 和 `MapImporter` 的接口都很干净——

```csharp
public void Export(Map map, string path) { ... }
public Map Import(string path) { ... }
```

但两个类的**实现**里，都有关于地图文件格式的知识：文件头、Chunk 编码、实体序列化、版本号……升级地图格式时，两个类都得改。这就是 back-door leakage。

发现这类问题的方法：**问自己，如果 X 改了，有多少个地方需要修改？** 如果答案大于 1，那个 X 对应的知识就泄漏了。

---

## 四、时序分解（Temporal Decomposition）：听起来合理但错误的直觉

> "In temporal decomposition, the structure of a system corresponds to the time order in which operations will occur. When designing modules, focus on the knowledge that's needed to perform each task, not the order in which tasks occur."

**时序分解的核心问题：你按照「事情发生的顺序」来切割模块，而不是按照「谁拥有哪些知识」来切割。**

初始化角色动画系统：读配置文件 → 解析状态 → 创建状态机 → 绑定到 GameObject

用时序分解可能设计成：

```csharp
public class AnimConfigReader { ... }   // 步骤1：读文件
public class AnimConfigParser { ... }   // 步骤2：解析
public class AnimStateMachineFactory { ... }  // 步骤3：创建
```

`AnimConfigReader` 需要知道配置文件的格式（才能把内容正确读入）。`AnimConfigParser` 也需要知道（才能解析字段）。「配置文件格式」这个知识在两个类里同时存在——信息泄漏。

HTTP Server 那个例子更加说明问题：

> "One team used two different classes for receiving HTTP requests; the first class read the request into a string, and the second class parsed the string. Information leakage occurred because an HTTP request can't be read without parsing much of the message; for example, the Content-Length header must be parsed to compute the total request length."

你以为「读」和「解析」是两件事，但 HTTP 协议的结构决定了——**你不解析就没法读完**。Content-Length 在头部，必须先解析头才知道 body 有多长。「读」和「解析」在表面上是时序上的两步，但在知识层面它们是同一件事。

### 资源加载的时序分解陷阱

```csharp
// 错误的时序分解
public class AssetLoader { ... }        // 加载原始字节
public class AssetDecompressor { ... }  // 解压
public class AssetDeserializer { ... }  // 反序列化
```

这三个类都需要了解「资产包的内部格式」。升级格式时三个类都要动。

```csharp
// 正确的知识边界切割
public class AssetBundleReader {
    public Asset Load(string path) { ... }
    // 内部自己处理：读字节→解压→反序列化，全部封装
}
```

书里的结论：

> "information hiding can often be improved by making a class slightly larger."

把本应合并的类强行拆开，只会制造信息泄漏。有时候，让一个类「稍微大一点」，是比拆成两个浅类更好的设计。

---

## 五、实战案例：帧同步消息协议的设计

假设你在做一个局域网多人游戏，消息格式：

```
[4字节：消息总长度][2字节：消息类型][4字节：帧号][N字节：payload]
```

**坏的设计（时序分解）：**

```csharp
public class MessageReader {
    public byte[] ReadNextMessage() {
        // 必须读前4字节才知道总长度——已经隐含地"知道"消息格式了
        byte[] header = new byte[4];
        stream.Read(header, 0, 4);
        int totalLength = BitConverter.ToInt32(header, 0);
        // ...
    }
}

public class MessageParser {
    public GameMessage Parse(byte[] rawData) {
        // 这个类也知道：长度在哪、类型在哪、帧号在哪
        ushort messageType = BitConverter.ToUInt16(rawData, 4);
        int frameId = BitConverter.ToInt32(rawData, 6);
        // ...
    }
}
```

「消息协议格式」这个知识在两个类里都存在。改协议时两个类都得改。

**好的设计（合并知识）：**

```csharp
public class GameMessageReader {
    public GameMessage ReadNextMessage() {
        // 所有关于协议格式的知识，都封装在这里
        byte[] lengthBytes = new byte[4];
        stream.Read(lengthBytes, 0, 4);
        int totalLength = BitConverter.ToInt32(lengthBytes, 0);
        // 继续读、解析、返回结构化对象
        // ...
        return new GameMessage(messageType, frameId, payload);
    }
}
```

调用方只调用 `ReadNextMessage()` 就能得到结构化的 `GameMessage`，完全不知道底层协议。改协议只改一个类。

---

## 六、Code Review 时如何识别信息泄漏

**1. "如果 X 改了，我要改几个文件？"** 如果答案 > 1，那个 X 的知识就泄漏了。

**2. "接口暴露了实现细节吗？"** 接口里有 `Map`、`List`、`byte[]` 这种具体数据结构，或者能看出内部实现的命名（如 `parseJsonConfig()`）——泄漏的迹象。

**3. "这两个类能独立演进吗？"** 如果改 A 必须改 B，找出那个共享的知识，把它集中到一处。

**4. "这个分类是按时间顺序切的，还是按知识归属切的？"** 类名是「XXXLoader / XXXParser / XXXProcessor」这种流水线结构——警惕时序分解陷阱。

---

## 七、游戏开发里的高危区域

- **存档系统**：序列化格式的知识不要泄漏到存档系统之外。UI 层不应该知道存档是 JSON 还是二进制。
- **资源管理**：资源包格式的知识只应该存在于加载器里。上层只管「我要一个 Prefab」。
- **网络协议**：包格式的知识不要泄漏到游戏逻辑层。游戏逻辑应该看到「玩家移动到了(x,y,z)」，而不是「收到了一个 12 字节的 position packet」。
- **配置系统**：Config 文件格式（CSV/JSON/ScriptableObject）的知识不要泄漏到配置数据的使用方。
- **渲染管线**：Shader 的 property binding 方式不要泄漏到上层 Material 管理代码里。

---

## 品味判断

信息隐藏和「封装」这两个词经常被混用，但它们其实是不同层次的概念。

**封装**是一种语言机制：用 `private`/`protected` 限制访问权限。

**信息隐藏**是一种设计哲学：决定哪些知识应该只活在一个地方，不依赖语言机制，而依赖设计者的判断力。

一个优秀的工程师，能用 `public` 字段实现完美的信息隐藏（只要外部不需要知道这个字段是如何产生和使用的）；一个糟糕的工程师，用满了 `private` 也会把内部实现全部通过 getter 漏出去。

**真正的信息隐藏是设计决策的结果，不是语言约束的副产品。**

---

> 信息隐藏的本质不是把变量藏起来，而是把设计决策藏起来——让调用者永远不需要知道你是怎么做到的，只需要知道你能做什么。

---

## 🎯 今日测验

**Q1（概念）：** 解释「`private` 关键字」和「信息隐藏」的区别。为什么一个类里所有字段都是 `private` 的，却仍然可能存在严重的信息泄漏？请举一个例子。

**Q2（应用）：** 你在做一个 Unity 游戏的配置系统，目前代码结构是：`ConfigFileReader`（读 JSON 文件到字符串）→ `ConfigJsonParser`（解析字符串到字典）→ `GameConfig`（持有配置数据）。从今天的理论角度，分析这个设计的问题，并提出改进方案。

**Q3（品味）：** 「让类稍微大一点，可以改善信息隐藏」和「类应该小，职责要单一」这两个原则看起来矛盾。你如何在设计时判断什么时候应该合并，什么时候应该拆分？请结合具体场景分析。

> 回复本条消息即可作答，你的回答会影响明天的推送深度和方向。
