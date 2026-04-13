---
title: 代码之外的必修课：顶级技术文档风格指南如何提升你的工程效率
url: https://tonybai.com/2025/07/14/writing-style-guide/
published: '2025-07-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 代码之外的必修课：顶级技术文档风格指南如何提升你的工程效率

![](../../assets/00339a8f6cdb2e81.png)


[本文永久链接](https://tonybai.com/2025/07/14/writing-style-guide) – https://tonybai.com/2025/07/14/writing-style-guide

大家好，我是Tony Bai。

作为一名开发者、架构师或运维专家，我们大部分时间都在与代码、系统和架构打交道。然而，我们同样在持续不断地进行另一种形式的“编码”——**沟通编码**。无论是撰写一个清晰的 README.md，提交一份详尽的 Pull Request 描述，编写项目内部的技术文档，还是在社区中回答一个问题，我们都在扮演着“技术作者”的角色。

代码的质量决定了软件能否运行，而**沟通的质量则决定了项目能否高效协作、知识能否有效传承、社区能否健康发展**。一份糟糕的文档，如同晦涩难懂的“面条代码”，会极大地消耗团队的精力和热情。

最近，Redhat公司发布了《[Red Hat Technical Writing Style Guide](https://www.stylepedia.net/style/)》7.1版本。这份指南不仅仅是一系列规则的集合，它更像是一部由顶级开源软件公司沉淀下来的、关于**如何通过清晰沟通来提升工程效率**的哲学。

在这篇文章中，我将提炼其中的一些精髓，探讨那些能直接提升您和团队工程能力的写作原则，供大家参考。

## 写作的“第一性原理”：清晰、精确、用户至上

技术文档的首要目标是传递信息，任何模糊、冗长或模棱两可的表达都是工程效率的天敌。指南强调了几个核心原则：

### 1. 拥抱主动语态，指令明确无误

主动语态让指令更直接、更有力。在指导性文档中，这能显著降低读者的认知负荷。

| 不推荐 (被动语态) | 推荐 (主动语态) |
|---|---|
| Linuxconf can be started by typing … | Type … to start Linuxconf. |
新的配置可以被应用通过重启服务。 |
重启服务以应用新的配置。 |

**对开发者的价值**：当用户（或未来的你）阅读操作手册时，清晰的指令意味着更低的出错率和更快的解决问题速度。

### 2. 杜绝冗余，尊重读者的时间

避免使用不必要的填充词，让每一句话都言之有物。

| 冗余 | 精炼 |
|---|---|
| Perform the installation of the product. | Install the product. |
| This problem is located on the /dev/sda1 partition. | This problem is on the /dev/sda1 partition. |

### 3. 避免歧义：This 指的是什么？

在技术文档中，代词（如 this, that, it）是歧义的重灾区，尤其对于翻译和非母语阅读者。指南建议明确指出代词所指代的的名词。

```
- A site can use these to self-assign a private routable IP address space.
+ A site can use these unique local addresses to self-assign a private routable IP address space.
- This causes SSH to lose the recorded identities.
+ This action causes SSH to lose the recorded identities.
```


**对开发者的价值**：在复杂的配置说明或问题排查指南中，消除代词歧义可以防止因误解而导致的配置错误。

## 为全球化社区而写：包容性与可翻译性

开源项目和现代技术团队本质上是全球化的。我们的文档需要被不同文化背景的人阅读和翻译。

### 1. 使用包容性语言

这是现代技术社区的基石。避免使用可能带有偏见或冒犯性的术语，有助于建立一个更健康、更多元化的社区环境。

**master/slave**-> 推荐使用 primary/replica, controller/worker, leader/follower 等。**whitelist/blacklist**-> 推荐使用 allowlist/denylist 或 blocklist。**性别代词**-> 避免使用 he/she，推荐使用中性的 they（可指代单数）或直接使用第二人称 you。

### 2. 为翻译而设计

糟糕的措辞会给机器翻译和人工翻译带来灾难。一些简单的规则可以极大地提升文档的可翻译性：

**避免使用俚语和行话**：eat your own dogfood (使用自己的产品), boil the ocean (范围过大) 等表达在其他文化中可能完全无法理解。**慎用 may 和 should**：may 可能表示“可能性”或“许可”，should 可能表示“建议”或“期望”。使用 can (可以), might (可能), must (必须) 会更精确。**避免名词堆叠**：Standard system log management configuration 这种连续名词的组合，在翻译时极易出错。可以调整为 Standard configuration of system log management。

## 工程师的文字“代码规范”：一致性与标准化

如同 eslint 或 gofmt 为代码提供规范一样，风格指南为我们的文字提供了“格式化”标准。这能确保整个项目文档风格统一，易于阅读和维护。

### 1. 统一命令语法文档

在展示命令行示例时，保持一致的格式至关重要。

```
# 一个清晰的命令语法示例
$ git clone [username@]hostname:/repository_filename [directory]
```


```
- 使用 $ 表示普通用户，# 表示 root 用户。
- 使用 [] 表示可选参数。
- 使用斜体或描述性词语（如 _filename_）表示 需替换的值。
- 在需要省略输出时，使用 ...output omitted... 标记，而不是随意删减。
```


### 2. 精确描述 UI 元素

当描述用户界面时，精确和简洁是关键。

**直接了当**：不说 Click the Save button，而说 Click**Save**。**名称匹配**：文档中的 UI 元素名称（如按钮、菜单项）应与界面上显示的**完全一致**（包括大小写）。**导航路径**：使用 -> 或 →清晰地表示导航路径，例如：Go to Monitoring → Metrics。

### 3. 避免产品名称的所有格

一个看似微小但能提升专业度的细节：

**不推荐**: Red Hat OpenShift’s Logging operator creates…**推荐**: The Red Hat OpenShift Logging operator creates…

## 总结与展望：将沟通视为工程技艺

《红帽风格指南》带给我们的最大启示是：**清晰、精确、专业的书面沟通不是一种“软技能”，而是工程技艺（Craftsmanship）不可或缺的一部分**。它与编写高质量代码、设计健壮架构同等重要。

下一次，当你准备提交一个 Pull Request、更新一份 README，或撰写一篇技术博客时，不妨尝试运用其中的一两个原则：

- 将一个被动语态的句子改为主动语态。
- 检查是否有模糊的代词 it 或 this 可以被替换。
- 思考一下你使用的术语是否足够包容和全球通用。

投资于沟通，就是投资于整个团队的效率和项目的未来。正如一份优雅的代码令人赏心悦悦目，一份清晰的文档同样能带来极致的工程之美。

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


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论