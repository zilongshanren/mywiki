---
title: 当 Go 还在追求极简时，C++ 26 却又加了四大“史诗级”新特性
url: https://tonybai.com/2026/03/31/go-minimalism-vs-cpp26-epic-new-features/
published: '2026-03-31'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 当 Go 还在追求极简时，C++ 26 却又加了四大“史诗级”新特性

![](../../assets/0e5cc7ea6a575455.png)


[本文永久链接](https://tonybai.com/2026/03/31/go-minimalism-vs-cpp26-epic-new-features) – https://tonybai.com/2026/03/31/go-minimalism-vs-cpp26-epic-new-features

大家好，我是Tony Bai。

在这个 Go、Zig 等“小而美”新语言颇受青睐的时代，如果你去技术社区里问一句：“C++ 这门语言怎么样？”

你大概率会得到一堆充满戏谑的回答：“太复杂了，别学”、“从入门到放弃”、“面试造火箭，工作拧螺丝”。

C++，这门诞生于上世纪 80 年代的编程语言，似乎早已被贴上了“老旧、臃肿、极其反人类”的标签。在很多新生代开发者眼里，它就像一头步履蹒跚的史前巨兽，理应被时代所淘汰。

**但就在前天（2026年3月29日），这头“史前巨兽”不仅没有倒下，反而亮出了它那足以撕裂天空的獠牙。**

C++ 标准委员会主席、C++ 界的“教父级”人物 **Herb Sutter** 亲自在博客上宣布：[C++26 标准的技术工作，已正式完成！](https://herbsutter.com/2026/03/29/c26-is-done-trip-report-march-2026-iso-c-standards-meeting-london-croydon-uk/)

Herb Sutter 还用极其兴奋的口吻将其定义为**“自 C++11 以来最具冲击力的一次发布”**。而这次更新的核心，是四个被他称为“Fab Four”（神奇四侠）的史诗级新特性。

当我耐着性子看完全部内容后，我脑子里只剩下四个字：**叹为观止。**

当 Go 语言的开发者还在为“是否要给语言增加一个三元表达式”，或[泛型方法](https://tonybai.com/2026/01/24/go-generics-finally-supports-generic-methods)而激烈辩论时，C++ 却反其道而行之，给自己又加装了四门“宇宙级”的重型武器。这到底是 C++ 吹响的绝地反击号角，还是压垮骆驼的最后一根稻草？

今天，我们就来硬核扒开 C++26 这四大“金刚”，看看它们到底有多强，以及它们将如何影响将来程序员对编程语言的选择。

![](../../assets/62fe59bc4741053d.png)


## 第一门重炮：反射（Reflection）——“代码生成代码”的终极魔法

Herb Sutter 将**反射**放在了四大特性之首，并称之为“自模板（Templates）发明以来 C++ 最重要的升级”。

什么是C++ 的反射？简单来说，**就是让代码在编译期拥有了“自我审视”和“自我创造”的能力。**

![](../../assets/5a5e78fb7f04a10e.png)


在 C++26 之前，如果你想实现一个通用的 JSON 序列/反序列化库，你必须写大量重复的模板代码，或者用各种丑陋的宏来“欺骗”编译器。

但在 C++26 中，你可以像这样写出充满“神性”的代码（代码示意）：

![](../../assets/85b158fdcffcfbf2.png)


这段代码，在编译的时候就能根据编译时的输入(test.json)自动分析JSON构造，并生成编译时用于计算的一个新类型。**这在 Go 语言里，需要借助 reflect 包在运行时（Runtime）以牺牲性能为代价才能做到。而 C++，直接在静态编译期（Compile-time）零成本搞定了！**

Herb Sutter 将其形容为“C++ 的十年火箭引擎”。这意味着，未来 C++ 社区将涌现出无数极其强大、但又极其复杂的元编程（Metaprogramming）库。C++ 的学习曲线，将再次被拉到一个新的高度。

## 第二道防线：内存安全（Memory Safety）——“只需重编，安全自来”

如果说反射让 C++ 的上限变得更加遥不可及，那么内存安全的提升，则是 C++ 在向 Go 和 Rust 的核心优势区发起的正面冲锋。

C++ 常年被诟病的核心痛点是什么？**内存不安全**。悬垂指针、未初始化变量读取（导致[未定义行为](https://tonybai.com/2026/03/16/go-language-eliminated-undefined-behavior-truth-investigation)）……这些噩梦困扰了 C++ 程序员几十年。

C++26 给出了一个极其诱人的承诺：**你的老代码一行都不用改，只要用 C++26 模式重新编译，就能自动获得大幅度的安全提升！**

这主要来源于两个方面的改进：

**消灭未初始化变量的 UB**：在 C++26 中，读取未初始化局部变量不再是“未定义行为（Undefined Behavior）”。这意味着困扰无数新手的、极其诡异的程序崩溃，将成为历史。**“加固”的标准库**：Google 和 Apple 已经将它们内部经过“加固（Hardened）”的标准库实现贡献给了 C++26。这意味着，当你使用 std::vector, std::string 等容器时，大量的边界检查会自动开启。

Herb Sutter 引用了 Google 的内部数据：

“仅在 Google，这项技术就已经修复了超过 1000 个 Bug，预计每年可以预防 1000 到 2000 个新 Bug 的产生，并将整个生产环境的段错误（Segfault）率降低了 30%。”


这简直是在对 Go 说：**“你用 GC 换来的那点可怜的安全性，我 C++ 现在也能做到了，而且依然是零成本的！”**

## 第三把利剑：契约（Contracts）——代码里的“法律条文”

如果你写过 Go，你一定对满屏的 if param == nil { return errors.New(…) } 感到厌烦。这种防御性编程，虽然有效，但极其啰嗦。

C++26 正式引入了语言级的[契约编程](https://tonybai.com/2025/12/13/from-eiffel-contract-to-go-interface)。

你可以像签合同一样，为你的函数制定严格的法律条文：

![](../../assets/f18fbffe278bdaf7.png)


这些 pre 和 post 是编译器和运行时可以理解并强制执行的“法律”。如果调用者违反了前置条件，程序可以在开发阶段就立刻崩溃并给出明确的报错，而不是等到数据被污染后才在某个奇怪的地方爆炸。

虽然 Go 社区也在讨论类似的泛型断言，但 C++26 已经先行一步，将其做成了语言标准。

## 第四个引擎：std::execution——C++ 的“亲儿子”协程模型

在 C++20 中，虽然引入了 co_await 协程，但它只是一个语法糖，并没有提供一个统一的调度框架。

C++26 终于补上了这块短板，正式推出了 **std::execution**，也被称为 **Sender/Receiver 模型**。

这是一个极其强大、统一的异步模型框架。它让你能以一种声明式的方式，去描述、组合和调度复杂的并发任务流。

下面是一段使用std::execution的代码示例：

```
// This is an example of a custom algorithm for starting work
// without allocations. This algorithm is also available in
// <exec/start_now.hpp>. (Users that don't write custom sender
// algorithms will not need to use receivers or call connect
// or start.)
template <stdexec::sender_in<stdexec::empty_env> Sender>
struct start_now {
start_now(Sender sndr)
: _op(stdexec::connect(std::move(sndr), _sink_rcvr())) {
stdexec::start(_op);
}
private:
// start_now is implemented in terms of this custom receiver,
// which is used to discard Sender's results.
struct _sink_rcvr {
using receiver_concept = stdexec::receiver_t;
void set_value(auto&&...) noexcept {}
void set_error(auto&&) noexcept {}
void set_stopped() noexcept {}
};
stdexec::connect_result_t<Sender, _sink_rcvr> _op;
};
int main() {
// A run loop is a fifo queue of work and a loop to execute the
// work. It needs to be driven by calling its .run() member fn.
stdexec::run_loop ctx;
auto event_loop = ctx.get_scheduler();
// Create two tasks that cooperatively multitask.
auto task1 = stdexec::just()
| stdexec::then([]{ std::puts("hello from task 1! suspending..."); })
| stdexec::continue_on(event_loop) // suspend
| exec::repeat_n(5)
| stdexec::then([]{ std::puts("task 1 is done!"); });
auto task2 = stdexec::just()
| stdexec::then([]{ std::puts("hello from task 2! suspending..."); })
| stdexec::continue_on(event_loop) // suspend
| exec::repeat_n(8)
| stdexec::then([]{ std::puts("task 2 is done!"); });
// Start both tasks. This enqueues them for execution on the run loop.
auto op1 = start_now(stdexec::start_on(event_loop, std::move(task1)));
auto op2 = start_now(stdexec::start_on(event_loop, std::move(task2)));
ctx.finish(); // tell the run loop to stop when the queue is empty
ctx.run(); // tell the run loop to start executing work in the queue
}
```


这可以被看作是 C++ 对 Go 的 Goroutine + Channel 模型，以及 Rust 的 async/await + tokio 模型的终极回应。

它让 C++ 开发者第一次拥有了一套语言原生的、能够轻松编写“无数据竞争（Data-race-free by construction）”并发程序的“亲儿子”工具。

## 小结：一场没有退路的豪赌

反射、安全、契约、并发。C++26 的这四大金刚，每一个都足以在其他语言中引发一场大地震。

我们看到的是一头苏醒的巨兽。它没有选择像 Go 那样“断舍离”，也没有像 Rust 那样“偏执于安全”，而是极其贪婪地选择了：**“我全都要！”**

它既想要极致的表达能力和零成本抽象（反射、模板），又想要与 Rust 媲美的内存安全（加固标准库），还想要不输 Go 的并发表达力（std::execution）。

C++26 给老兵们提供了前所未有的强大武器，但也把本就陡峭的学习曲线，又向上抬升了一个令人惊叹的高度，宇宙第一复杂的编程语言，实至名归！

当 Go 的开发者还在为“是否要加个三元表达式”而争论不休时，C++ 已经头也不回地奔向了“万神殿”。

或许，编程语言的终局，真的不是“大一统”，而是“两极分化”：一极是像 Go 一样追求极致简单的“工程师语言”；而另一极，则是像 C++ 这样，专为那 1% 的、追求极致性能和控制力的“宗师级”开发者准备的、布满荆棘的封神之路。

**C++26，欢迎来到神的世界，也欢迎来到神的炼狱。**

## 参考资料

- https://herbsutter.com/2026/03/29/c26-is-done-trip-report-march-2026-iso-c-standards-meeting-london-croydon-uk/
- https://herbsutter.com/2025/06/21/trip-report-june-2025-iso-c-standards-meeting-sofia-bulgaria/
- https://herbsutter.com/2024/07/02/trip-report-summer-iso-c-standards-meeting-st-louis-mo-usa/
- https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p2996r13.html
- https://www.youtube.com/watch?v=7z9NNrRDHQU
- https://www.youtube.com/watch?v=oitYvDe4nps

**今日互动探讨：**

看完 C++26 的这四大“神仙”特性，你是感到兴奋，还是感到了深深的绝望？你觉得 C++ 的这种“大而全”的演进路线是对的，还是 Go 的“小而美”更代表未来？

欢迎在评论区分享你的看法！

还在为“复制粘贴喂AI”而烦恼？我的新专栏 **《 AI原生开发工作流实战》** 将带你：

- 告别低效，重塑开发范式
- 驾驭AI Agent(Claude Code)，实现工作流自动化
- 从“AI使用者”进化为规范驱动开发的“工作流指挥家”

扫描下方二维码，开启你的AI原生开发之旅。

![](../../assets/305ffd23f32ce780.png)


你的Go技能，是否也卡在了“熟练”到“精通”的瓶颈期？

- 想写出更地道、更健壮的Go代码，却总在细节上踩坑？
- 渴望提升软件设计能力，驾驭复杂Go项目却缺乏章法？
- 想打造生产级的Go服务，却在工程化实践中屡屡受挫？

继《[Go语言第一课](http://gk.link/a/10AVZ)》后，我的《[Go语言进阶课](http://gk.link/a/12yGY)》终于在极客时间与大家见面了！

我的全新极客时间专栏 《[Tony Bai·Go语言进阶课](http://gk.link/a/12yGY)》就是为这样的你量身打造！30+讲硬核内容，带你夯实语法认知，提升设计思维，锻造工程实践能力，更有实战项目串讲。

目标只有一个：助你完成从“Go熟练工”到“Go专家”的蜕变！ 现在就加入，让你的Go技能再上一个新台阶！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2026, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论