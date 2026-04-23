---
tags: [重写, 设计教训, 软件设计, bitsquid]
date: 2026-04-19
sources: 1
---

# 关于重写的四条教训

[[niklas-frykholm|Niklas Frykholm]] 在 Bitsquid 重写 Flow（可视化脚本，见 [[flow-graph-data-oriented-runtime]]）时写下的"四条戒律"，直接来自第一版留下的疤。前提很值得记住：**重写比新写更难**。新系统可以 iterate release、拿用户反馈长大；重写必须"至少和旧版一样好"才敢交付——等于强行退化到瀑布模型。因此第一版的每一个坏决定都成了翻倍的成本。

## 一、别拿字符串当非文本

详见 [[strings-as-identifiers-antipattern]]。字符串只配给用户看/输入，其它场景一律怀疑；**Id / DisplayName 分离**是基本纪律。

## 二、拿不准就 opt-out

系统会在演进中堆积越来越多"看起来有用但总觉得别扭"的特性。Niklas 的经验是：**那种"不 100% 顺眼"的功能，通常后悔的概率极大**，应当先拒绝，等想清楚再加。

反例：Flow 允许在 `Out` 接口的连线上右键菜单设 "Do First / Do Last / Do Normal"，用于控制多条下游的触发顺序。需求是真实的（先生成再引用），但视觉表达从来没找到漂亮方式——Flow graph 变难读。

更优解：用一个**显式的 sequence 节点**，它的多个输出按顺序触发。它把"顺序"这件事**显式可见**——正和第三条教训一致。

## 三、能显式就别隐式

"三行代码搞定一切"的爽感，往往要在之后几年用"看不懂、改不动、换不掉"去偿还。

Flow 第一版大量依赖 C# 反射：节点类型定义就是一个带 `[Category]` 特性的普通 class，字段的 `In/Out/Variable` 前缀通过字符串截取推导语义，序列化也靠反射。结果：

- 类名就是存档 key，改名即破坏兼容。
- 反射不保证字段返回顺序，逼得作者用"真的很丑的 C# hack"来保留声明顺序（以控制连接器顺序）。
- 第一条教训的 ugly string processing 在这里再次出场——连类名解析都带上了字符串魔法。

回头看，**把节点类型写进配置文件、显式列出字段和类型**会省事得多。评论区有人反驳"可以用 `[Attribute]` 做声明式扩展，像 Unity 的 Property Drawer"，Niklas 承认这是一种思路，但担心 `Vector3` 这类基础类上挂太多 "serialization / GUI / view" 属性会混淆职责——基础类就该只负责"是个向量"。

## 四、别走上复杂代码的不归路

真需要复杂的代码只有两类：本质复杂的（如计算几何）、或需要极致速度的。其它场景里，复杂度就是**成本**。

Flow 第一版的"折叠（fold）"——把一组节点收起来显示成一个节点——就是复杂代码的教科书：要建立新节点、要匹配外部连接器名字（受第一条毒害，必须维护 rename 表）、要保存内部结构以便展开……一路走到黑，下一次重写时等于要把这些 complexity 全再造一遍，才能保持行为兼容。

新版做法：**折叠只是视觉**。数据不动，可视化器选择不画内部而已。展开=换视图。整个子系统被"用对抽象"一把删光。

## 打油诗结尾

> That is all, four simple lessons
> to guide your future coding sessions
> now let your code be light and merry
> until its time for Charon's ferry

## 关联

- [[strings-as-identifiers-antipattern]] — 第一条的专页。
- [[simplicity]] / [[strategic-programming]] — "多想一步换一个更简单的抽象" 在 Bitsquid 文化里的长期回响。
- [[continuous-design]] — 评论区 Niklas 的态度："重写时可以顺便做对"，但新写时别先自己挖坑。
- [[no-magic-principle]] — 隐式反射魔法的长期代价。
- [[cleaning-bad-code]] / [[bitsquid-cleaning-bad-code]] — 同源的"别让烂代码一直欠债"主张。

## Sources

- [[sources/bitsquid-four-meditations-bad-design]]
