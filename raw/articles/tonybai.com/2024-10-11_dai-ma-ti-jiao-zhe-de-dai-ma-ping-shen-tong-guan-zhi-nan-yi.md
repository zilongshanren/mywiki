---
title: 代码提交者的代码评审通关指南[译]
url: https://tonybai.com/2024/10/11/the-cl-author-guide-to-getting-through-code-review/
published: '2024-10-11'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 代码提交者的代码评审通关指南[译]

![](../../assets/061b8ddc2969a19d.png)


[本文永久链接](https://tonybai.com/2024/10/11/the-cl-author-guide-to-getting-through-code-review) – https://tonybai.com/2024/10/11/the-cl-author-guide-to-getting-through-code-review

Google在软件工程领域对IT界做出了卓越的贡献，从《[Google软件工程](https://book.douban.com/subject/35838155/)》，到[Google Style Guides](https://google.github.io/styleguide/)，再到[The Change Author’s Guide](https://google.github.io/eng-practices/review/developer/)。这些实践参考不仅提升了软件工程的标准，也为全球IT行业的发展提供了宝贵的资源和指导。由于Go是Google开源的，其cl review基本上是遵循了Google内部的标准和实践，可以帮助开发人员更快地完成审核并获得更高质量的结果。因此在这篇文章中，我翻译一下The Change Author’s Guide，供大家参考。

The Change Author’s Guide分为三部分，由于每一部分篇幅都不多，这里就放在一起了。本次翻译是基于[Google Engineering Practices Documentation](https://github.com/google/eng-practices)的commit 3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c进行的。

注：Google内部使用的术语CL代表“变更列表(changelist)”，指的是一个自包含的更改，该更改已经提交到版本控制系统或正在进行代码评审。其他组织通常称之为“变更”、“补丁”或“拉取请求(PR)”。


## 1. 编写良好的CL描述

CL描述是变更的公开记录，重要的是它能够传达以下信息：

- 做了
**什么**变更？这应该总结主要的变化，使读者在不需要阅读整个CL的情况下了解正在发生的变化。 **为什么**要做出这些变更？作为作者，你在做出这个变更时有什么背景？以及你做出的那些在源代码中无法反映出来的决策？等等。

CL描述将成为我们版本控制历史的一部分，未来可能会被数百人阅读。

未来的开发人员将根据描述搜索你的CL。未来某人可能因为对其相关性有模糊的记忆而寻找你的变更，但没有具体细节。如果所有重要信息都在代码中而非描述中，他们将更难找到你的CL。

而且，在他们找到CL后，是否能够理解**为什么**做出这个变更？阅读源代码可能会揭示软件在做什么，但可能不会揭示其存在的原因，这可能会使未来的开发人员更难知道他们是否可以移动[切斯特顿的栅栏(Chesterton’s fence)](https://abseil.io/resources/swe-book/html/ch03.html#understand_context)。

译注：切斯特顿的栅栏是一种启发式方法，由G.K.切斯特顿提出，旨在告诫人们在改变任何系统之前，应先了解该系统存在的原因和功能，否则可能会造成更大的问题。


一个编写良好的CL描述将帮助这些未来的工程师——有时，也包括你自己！

### 1.1 第一行(first line)

- 简短总结所做的内容。
- 使用完整句子，以命令的形式书写。
- 后面跟一个空行。

CL描述的**第一行**应该是对具体做了什么的简短总结，后面跟一个空行。这是出现在版本控制历史摘要中的内容，因此应该提供足够的信息，使未来的代码搜索者无需阅读你的CL或其整个描述就能理解你的CL实际上做了什么，或与其他CL的不同之处。也就是说，第一行应该独立存在，让读者更快地浏览代码历史。

尽量保持第一行简短、重点突出且切中要点。清晰性和对读者的实用性应是最重要的。

按照传统，CL描述的第一行应该是一个完整的句子，并以命令形式书写（即祈使句）。例如，应该说“Delete the FizzBuzz RPC and replace it with the new system.”，而不是“Deleting the FizzBuzz RPC and replacing it with the new system.”，不过，你不必将其余的描述写成祈使句。

### 1.2 主体信息要丰富

第一行应该是简短且重点突出的摘要，而其余的描述应详细说明并包括读者理解变更列表所需的任何补充信息。它可能包括对正在解决的问题的简要描述，以及为什么这是最佳方法。如果该方法有任何不足之处，应该指出。如果有相关信息也要列出，包含背景信息，如错误编号、基准测试结果和设计文档链接等。

如果你包含外部资源的链接，请考虑由于访问限制或保留政策，未来读者可能无法看到这些链接。在可能的情况下，包含足够的上下文，以便审查者和未来读者理解CL。

即使是小的CL也值得关注细节。将CL放在上下文中。

### 1.3 不好的CL描述

“Fix bug”是一个不充分的CL描述。什么bug？你做了什么来修复它？其他类似的不好的描述包括：

- “Fix build.”
- “Add patch.”
- “Moving code from A to B.”
- “Phase 1.”
- “Add convenience functions.”
- “kill weird URLs.”

其中一些都是取自真实的CL描述。虽然简短，但它们没有提供足够的有用信息。

### 1.4 良好的CL描述

以下是一些好的CL描述示例。

#### 1.4.1 功能变更

示例：

```
RPC: Remove size limit on RPC server message freelist.
Servers like FizzBuzz have very large messages and would benefit from reuse. Make the freelist larger, and add a goroutine that frees the freelist entries slowly over time, so that idle servers eventually release all freelist entries.
```


第一行描述了CL实际做了什么。其余的描述谈论了正在解决的问题、为什么这是一个好的解决方案以及有关具体实现的更多信息。

#### 1.4.2 重构

示例：

```
Construct a Task with a TimeKeeper to use its TimeStr and Now methods.
Add a Now method to Task, so the borglet() getter method can be removed (which was only used by OOMCandidate to call borglet's Now method). This replaces the methods on Borglet that delegate to a TimeKeeper.
Allowing Tasks to supply Now is a step toward eliminating the dependency on Borglet. Eventually, collaborators that depend on getting Now from the Task should be changed to use a TimeKeeper directly, but this has been an accommodation to refactoring in small steps.
Continuing the long-range goal of refactoring the Borglet Hierarchy.
```


第一行描述了CL做了什么以及这是如何与过去不同的。其余的描述谈论了具体实现、CL的背景、解决方案并不理想以及可能的未来方向。它还解释了为什么这个变更被做出。

#### 1.4.3 需要一些上下文的小CL

示例：

```
Create a Python3 build rule for status.py.
This allows consumers who are already using this as in Python3 to depend on a rule that is next to the original status build rule instead of somewhere in their own tree. It encourages new consumers to use Python3 if they can, instead of Python2, and significantly simplifies some automated build file refactoring tools being worked on currently.
```


第一句描述了实际的变更。其余的描述解释了为什么这个变更被做出，并给审查者提供了大量的上下文信息。

### 1.5 使用标签(tags)

标签是手动输入的label，可用于对CL进行分类。这些标签可能由工具支持，也可能只是团队惯例。

例如：

- “[tag]“
- “[a longer tag]“
- “#tag”
- “tag:”

使用标签是可选的。

添加标签时，考虑它们是否应该在CL描述的主体中或第一行中。限制在第一行中使用标签的数量，因为这可能会模糊内容。

以下是带标签和不带标签的示例：

```
// Tags are okay in the first line if kept short.
[banana] Peel the banana before eating.
// Tags can be inlined in content.
Peel the #banana before eating.
// Tags are optional.
Peel the banana before eating.
// Multiple tags are acceptable if kept short.
#banana #apple: Assemble a fruit basket.
// Tags can go anywhere in the CL description.
> Assemble a fruit basket.
>
> #banana #apple
```


```
// Too many tags (or tags that are too long) overwhelm the first line.
//
// Instead, consider whether the tags can be moved into the description body
// and/or shortened.
[banana peeler factory factory][apple picking service] Assemble a fruit basket.
```


### 1.6 生成的CL描述

有些CL是由工具生成的。只要有可能，它们的描述也应该遵循此处的建议。也就是说，它们的第一行应该简短、重点突出且独立，CL描述主体应包含有助于审查者和未来代码搜索者理解每个CL效果的信息细节。

### 1.7 提交CL前审查描述

CL在审查过程中可能会发生重大变化。在提交CL前审查CL描述是值得的，可以确保描述仍然真实反映CL的内容。

## 2. 小型CL

### 2.1 为什么要写小型的CL？

小而简单的CL有以下优点：

- 审查速度更快。审查者更容易找到几分钟的时间来审查小CL，而不是腾出30分钟的时间来审查一个大CL。
- 审查更彻底。 对于大变更，审查者和作者往往会因大量详细评论反复交换而感到沮丧，有时甚至会错过或忽略重要点。
- 引入错误的可能性更小。由于你所做的更改较少，因此你和审查者更容易有效地推理CL的影响，并查看是否引入了错误。
- 被拒绝时浪费的工作更少。 如果你写了一个巨大的CL，然后审查者表示整体方向错误，你就浪费了很多工作。
- 更容易合并。 处理一个大CL需要很长时间，因此在合并时会遇到许多冲突，你将不得不频繁合并。
- 更容易设计良好。 完善小变更的设计和代码质量要比完善大变更的所有细节容易得多。
- 审查阻塞更少。 发送自包含的整体变更部分允许你在等待当前CL审查时继续编码。
- 回滚更简单。 大CL更可能涉及在初始CL提交和回滚CL之间更新的文件，从而增加回滚的复杂性（中间的CL可能也需要回滚）。

请注意，审查者有权仅因为变更过大而直接拒绝你的变更。通常，他们会感谢你的贡献，但会要求你以某种方式将其拆分为一系列较小的变更。在你已经编写完变更后拆分它可能会花费很多时间，或者需要大量时间来争论审查者为什么应该接受你的大变更。因此，最好一开始就写小型CL。

### 2.2 多小算小？

一般而言，CL的合适大小是**一个自包含的变更**。这意味着：

- CL进行最小变更，只解决
**一件事**。这通常只是一个功能的一部分，而不是一次性完成整个功能。一般来说，最好宁可编写太小的CL，也不要编写太大的CL。与你的审核者合作找出可接受的尺寸。 - CL应该包含相关的测试代码。
- 审查者理解CL所需的一切（除未来开发外）都应包含在CL中，比如本CL的描述、现有代码库或他们已经审查过的CL。
- 系统在CL被检查入库后仍能良好工作，适用于其用户和开发人员。
- CL不应小到其含义难以理解。如果你添加了一个新的API，应该在同一个CL中包含对该API的使用方法，以便审查者更好地理解API将如何使用。这也能防止未使用的API被提交。

没有关于“过大”的硬性规则。100行通常是合理的CL大小，而1000行通常被认为过大，但这取决于审查者的判断。变更涉及的文件数量也会影响其“大小”。在一个文件中的200行变更可能是可以接受的，但变更分布在50个文件中的话通常会被认为过大。

请记住，尽管你从开始编写代码的那一刻起就与代码密切相关，审查者通常没有上下文。对你来说合适大小的CL可能对审查者来说会是难以接受的。若有疑问，写比你认为需要的更小的CL。审查者很少抱怨收到的CL太小。

### 2.3 大型CL什么时候可以？

在某些情况下，大变更并不那么糟糕：

- 通常可以将删除整个文件视为仅一行变更，因为审查者审核它所花费的时间很少。
- 有时，大CL是由你完全信任的自动重构工具生成的，审查者的工作只是验证并确认他们确实想要这个变更。这些CL可以更大，尽管上述一些注意事项（例如合并和测试）仍然适用。

### 2.4 高效地编写小型CL

如果你编写了一个小型CL，然后等待审查者批准它，再写下一个CL，那么你将浪费很多时间。因此，你需要找到一种方法，在等待审查时不会阻塞自己。这可能涉及同时处理多个项目，找到愿意立即可用的审查者，进行面对面审查，进行配对编程，或者以某种方式拆分你的CL，以便你能够立即继续工作。

### 2.5 拆分CL

如果存在多个相互依赖的CL时，我们通常有必要在深入编码之前从高层次考虑如何拆分和组织这些CL。

除了使你作为作者更容易管理和组织CL外，这也让你的代码审查者更容易，从而使你的代码审查更高效。

以下是将工作拆分为不同CL的一些策略。

#### 2.5.1 将多个变更堆叠在一起

拆分CL的一种方法是编写一个小CL，发送审查，然后立即开始编写一个基于第一个CL的另一个CL。大多数版本控制系统都允许你以某种方式做到这一点。

#### 2.5.2 按文件拆分

另一种拆分CL的方法是按文件分组，这些文件需要不同的审查者，但其他方面是自包含的变更。

例如：你发送一个CL用于对protocol buffer修改，另一个CL用于对使用该proto的代码的更改。你必须在code CL之前提交proto CL，但它们可以同时接受审查。如果这样做，你可能想通知两组审查者你编写的另一个CL，以便他们了解你的变更的上下文。

另一个例子：你发送一个CL用于代码变更，另一个用于使用该代码的配置或实验；如果有必要，这也更容易回滚，因为配置/实验文件有时比代码变更更快地推送到生产环境。

#### 2.5.3 横向拆分

考虑创建共享代码或存根，以帮助隔离技术栈各层之间的变更。这不仅有助于加快开发速度，还鼓励层之间的抽象。

例如：你创建了一个计算器应用程序，其中有客户端、API、服务和数据模型层。共享的proto signature可以将服务层和数据模型层相互抽象。类似地，API存根可以将客户端代码的实现与服务代码分开，使它们能够独立演进。类似的思路也可以应用于更细粒度的函数或类级别的抽象。

#### 2.5.4 纵向拆分

与分层的横向方法相对应，你可以将代码拆分为更小、全栈、垂直的功能。这些功能中的每一个都可以独立并行实现。这使得一些轨道能够继续前进，而其他轨道则在等待审查或反馈。

回到我们在横向拆分所举的计算器示例。你现在想支持新的运算符，如乘法和除法。你可以通过将乘法和除法实现为独立的纵向特性或子功能来拆分，尽管它们可能有一些重叠，例如共享按钮样式或共享验证逻辑。

#### 2.5.5 横向和纵向拆分

为了进一步发展，你可以结合这些方法并制定一个实施计划，其中每个单元都是独立的CL。从模型（底部）开始，逐渐推进到客户端：

![](../../assets/b8b4a1bac2f9a441.png)


### 2.6 将重构与功能变更分开

通常最好将重构与功能变更或错误修复分开。例如，移动和重命名一个类应该与修复该类中的错误放在不同的CL中。这样，审查者更容易理解每个CL引入的变更。

不过，小的清理工作，例如修复局部变量名称，可以包含在功能变更或错误修复CL中。开发人员和审查者需判断何时重构的规模过大，以至于将其包含在当前CL中会使审查更加困难。

### 2.7 将相关的测试代码放在同一个CL中

CL应该包括相关的测试代码。请记住，这里的“小”指的是CL应该聚焦且不是单纯的行数问题。

所有谷歌的变更都需要测试。

添加或更改逻辑的CL应该伴随新的或更新的测试，以验证新行为。纯重构CL（不打算改变行为）也应有测试覆盖；理想情况下，这些测试已经存在，但如果没有，你应添加它们。

独立的测试修改可以先放入单独的CL，类似于重构准则。这包括：

- 用新测试验证预先存在的提交代码。

确保重要逻辑被测试覆盖。增加对受影响代码后续重构的信心。例如，如果你想重构没有测试覆盖的代码，提交测试CL可以在提交重构CL之前可以验证受测行为在重构前后是否保持不变。

- 重构测试代码（例如，引入助手函数）。
- 引入更大的测试框架代码（例如，集成测试）。

### 2.8 不要破坏构建

如果你有多个相互依赖的CL，你需要找到一种方法，在每个CL提交后确保整个系统保持正常工作。否则，你可能会在CL提交之间破坏所有同事的构建，影响大家几分钟（或在稍后的CL提交中出现意外问题时，甚至更长时间）。

### 2.9 无法做到足够小

有时你会遇到CL必须很大的情况。这种情况很少发生。练习编写小CL的作者几乎总能找到将功能分解为一系列小变更的方法。

在编写大CL之前，请考虑是否可以先进行仅重构的CL，以便为更干净的实现铺平道路。与你的团队成员交谈，看看是否有人对如何将功能实现为小CL发表看法。

如果所有这些选项都失败（这应该非常少见），那么请提前获得审查者的同意，以审核大CL，以便他们对即将到来的内容有所警觉。在这种情况下，预计审查过程会比较漫长，要警惕不要引入错误，并更加细致地编写测试。

## 3. 如何处理审查者的意见

当你将代码提交（CL）发送审查时，审查者可能会对你的代码提出多个意见。以下是一些处理审查者意见的有用建议。

### 3.1 不要把它视为针对个人

审查的目标是维护我们的代码库和产品的质量。当审查者对你的代码提出批评时，请将其视为他们试图帮助你、代码库和谷歌的一种方式，而不是对你或你能力的个人攻击。

有时，审查者可能会感到沮丧，并在评论中表达这种沮丧。虽然对于审查者来说，这不是一个好的做法，但作为开发人员，你应该对此有所准备。问问问自己：“审查者想要向我传达的建设性意见是什么？”然后按照他们实际所说的那样进行操作。

**绝不要对代码审查意见做出愤怒的回应。** 这是一种严重违反职业礼仪的行为，将在代码审查工具中留下永久记录。如果你太愤怒或烦恼而无法友好地回应，请离开电脑一段时间，或做些其他事情，直到你冷静下来再礼貌地回复。

一般来说，如果审查者没有以建设性和礼貌的方式提供反馈，请当面与他们解释。如果无法面对面或视频通话，那么可以私下发一封邮件给他们。以友好的方式解释你不喜欢的地方以及希望他们做出怎样的改变。如果他们在这次私人讨论中以非建设性的方式回应，或者没有达到预期效果，请酌情上报给你的经理。

### 3.2 修正代码

如果审查者表示他们不理解你代码中的某些内容，你的第一反应应该是澄清代码本身。如果代码无法澄清，请添加代码注释，解释代码存在的原因。如果某个注释似乎没有意义，你再在代码审查工具中做解释。

如果审查者不理解你的某段代码，未来其他读者也可能无法理解。写一条在代码审查工具中的回应并不能帮助未来的代码读者，但澄清代码或添加代码注释则能帮助他们。

### 3.3 协作思考

编写代码变更（CL）可能需要大量工作。最终将其发送审查，感觉一切都完成了，可能会很令人满意，但收到要求更改的评论时也可能会感到沮丧，尤其是当你不同意这些评论时。

在这样的时刻，请花点时间退后一步，考虑审查者是否提供了有价值的反馈，能帮助代码库和谷歌。你首先要问自己，“我理解审查者所要求的吗？”

如果你无法回答这个问题，请向审查者寻求澄清。

然后，如果你理解评论但不同意，重要的是要协作思考，而不是对抗性或防御性思考：

```
Bad: “No, I’m not going to do that.”
```


```
Good: "I went with X because of [these pros/cons] with [these tradeoffs]
My understanding is that using Y would be worse because of [these reasons].
Are you suggesting that Y better serves the original tradeoffs, that we should
weigh the tradeoffs differently, or something else?"
```


请记住，** 礼貌和尊重始终应放在首位**。如果你不同意审查者的观点，请寻找协作的方式：寻求澄清、讨论优缺点，并解释为什么你处理事情的方法更适合代码库、用户和/或谷歌。

有时，你可能知道一些审查者不知道的关于用户、代码库或CL的信息。在适当的地方修复代码，并与审查者进行讨论，提供更多上下文。通常，你可以根据技术事实与审查者达成某种共识。

### 3.4 解决冲突

解决冲突的第一步始终是尝试与审查者达成共识。如果无法达成共识，请参阅[代码审查标准](https://google.github.io/eng-practices/review/reviewer/standard.html)，其中提供了在这种情况下应遵循的原则。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论