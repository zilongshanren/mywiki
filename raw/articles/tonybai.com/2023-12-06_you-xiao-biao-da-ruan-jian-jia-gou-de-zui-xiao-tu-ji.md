---
title: 有效表达软件架构的最小图集
url: https://tonybai.com/2023/12/06/a-minimum-set-of-diagrams-for-expressing-software-architecture/
published: '2023-12-06'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 有效表达软件架构的最小图集

![](../../assets/16da01d45b270553.png)


[本文永久链接](https://tonybai.com/2023/12/06/a-minimum-set-of-diagrams-for-expressing-software-architecture) – https://tonybai.com/2023/12/06/a-minimum-set-of-diagrams-for-expressing-software-architecture

无论你是专职的软件架构师，还是在团队内兼职充当软件架构师角色的开发人员，一旦你处在软件架构师这个位置上，你自然就会遇到软件架构设计的三个困惑：

- 如何更深刻地理解业务；
- 如何更正确地取舍(包括技术性和业务性的)；
- 如何更有效地表达软件架构。

以上每个困惑展开来写都够写一本书的。而在这篇文章中，我仅聚焦最后一个困惑，聊聊我心目中表达软件架构的有效方式 — 最小图集(Minimum Diagram Set)。

## 1. 为什么软件架构需要有效表达

众所周知，软件架构承载着系统关键的技术决策和业务约束，指导着复杂软件的构建与演进，是实现软件系统的蓝图。但并不是说有了好的软件架构就一定可以做出好的软件系统，**软件系统最终还是要经由开发人员来实现**。

如果说架构师是软件架构的生产者，那么开发人员可以理解为是软件架构的消费者。但和一件普通商品一样，往往消费者很难Get到产品设计者的全部idea，产品越复杂，消费者Get到的比例越低，于是商品的生产者就会绞尽脑汁地制作产品说明书、功能演示视频等，目的就是想从不同角度更多、更有效的表达自己的商品的特性。对于普通商品而言，消费者Get程度低顶多是少用几个功能特性；但对于架构师生产的“产品”：架构设计成果而言，如果其消费者开发人员Get的程度低，那影响就会很严重，甚至可能会导致软件系统的开发彻底失败。

并且更不幸的是：我们的软件系统都是“复杂产品”。这样，如何表达和解读软件架构，弥合生产者与消费者之间的Gap，让开发者更多更深刻的理解软件架构这件“产品”便成为了架构师的困惑，日常架构设计工作中的难题，也是业界探索的重要课题。

架构设计是架构师与开发者之间的协议，只有有效的、充分的表达，协议才能被共识理解和忠实执行。业界在有效表达软件架构这条路上摸索了很多年，下面简单说说架构设计表达的演进历程。

## 2. 软件架构表达方式演进简史

软件架构表达的目的就是要直观地传达架构设计人员的思想和意图，使开发团队可以达成对架构设计的一致理解，促进各个团队协作，并作为开发人员编写代码以及管理人员推进项目的重要指导与参考。

### 2.1 自然语言描述

在软件工程的早期阶段，软件架构设计通常使用自然语言（如英语）进行描述。架构师会使用文档、规范和书面记录来表达架构设计的概念、原则、结构、组件和交互。然而，自然语言描述存在歧义性、解释性不足、理解起来较慢的问题，可能导致误解和沟通障碍。

### 2.2 图形化表达

人类大脑中传输的信息90%是视觉信息，其处理图形的速度要比处理文字的速度快上万倍。于是随着软件架构的复杂性增加，人们开始采用更直观、更易理解的图形化方法来描述架构设计(并辅以自然语言的文字描述)。

提到图形化表达，最简单的方法就是使用**一支笔+一张白纸**，基于自己“创造”的符号绘制草图(Sketch，以下草图来自c4model.com)：

![](../../assets/25fee6a94cb90073.png)


这种非规范的框线草图虽然提供了灵活性，但付出的代价却是一致性，因为大家都在创造自己的制图符号，而不是使用统一的标准。

### 2.3 结构化的图形表达

结构化图是在设计表达迈向标准化方面走出的重要一步。结构化图包括数据流图、控制流图、层次图、组件图等，用于可视化表示系统的组件、模块、依赖关系和交互流程等(下图中元素来自维基百科)。

![](../../assets/f21605bfe91bf926.png)


作为一种可以直观可视化描述与沟通架构设计的方式，结构化图形成为了表达架构设计的常见方法之一。不过，早期结构化表达的类型有限，无法涵盖所有环节，有的也没有形成标准，为了提高标准化程度，满足架构设计表达的全部需求，人们在二十世纪末推出了大一统的图形化建模语言UML。

### 2.4 [统一建模语言(UML)](https://www.uml.org)

统一建模语言（Unified Modeling Language，UML）是一种通用的标准化、图形化建模语言，广泛用于软件架构和设计的表示，在软件架构表达方法方面具有里程碑意义：

![](../../assets/3a0539a7c7ef3440.jpeg)


UML第一次在规范层面对图形表示进行了标准化，它提供了一组规范化的图形符号，用于描述系统的结构、行为和交互。在那个Rational统一过程（RUP）以及面向对象设计方法如日中天的时代，人们每每进行设计时，言必称使用UML。UML在图形化、标准化表达设计图方面走到了至今为止都无人企及的高峰。

![](../../assets/22f10713b9a6000b.png)


但是，20多年后的今天，UML并没有成为当时标准出品方期望的那个样子，没能成为表达软件系统设计的主流符号系统。也许是**它的复杂性阻碍了有效沟通**，让人们看到它的spec后就“望而却步”了。不过UML并没有死掉，它依然活着，UML规范中的一些图(Diagram)依然被大家常用，比如：[序列图(Sequence Diagram)](https://www.uml-diagrams.org/sequence-diagrams.html)、[用例图(Use Case Diagram)](https://www.uml-diagrams.org/use-case-diagrams.html)、[类图(Class Diagram)](https://www.uml-diagrams.org/class-diagrams-overview.html)等。

![](../../assets/eb3d9d2445968bf8.png)


### 2.5 形式化表达

业界在寻求图形化表达标准化的同时，也有一个分支在寻求用自然语言的“标准化”表达方法，这就是软件架构设计的形式化表达，在这个领域形成的语言被称为[架构描述语言(ADL)](https://en.wikipedia.org/wiki/Architecture_description_language)。ADL提供了一组特定的语法和语义规则，用于定义系统的组件、接口、依赖关系、行为和性能特征。ADL使架构师能够使用精确的语言来表达和分析架构设计，支持自动化的验证和分析工具，在学术研究这个小众领域还是很有受众的。不过，显然在大多数工程化淋雨，形式化表达门槛太高，对于软件架构在团队内快速有效建立共识起不到什么作用。

下面是一些ADL的实现，感兴趣的童鞋可以了解一下：

### 2.6 多视角的表达

有了UML这个前车之鉴后，人们似乎也放弃了在图记号“标准化”之路上的继续探索了，而是回归问题本源：**怎么有效，就怎么来**。

在工程实践中，人们认清了一个事实：**很难在一张大图(Diagram)中进行软件架构设计的有效表达**。于是大家开始采用“盲人摸象”的策略，将一个架构按不同视角表达为不同的图(Diagram)，这样**当开发人员将多个视角形成的图都理解后，也就理解了整个架构设计**。

按照这个多视角表达的思路(也被称为是一种**软件架构建模**思路)，业界先后出现了：

![](../../assets/a1c7c931516bd7e6.png)


逻辑视图（Logical View）关注系统的功能和功能模块，描述系统中各个模块之间的关系、接口和行为。它展示了系统的静态结构和动态行为，以及模块之间的通信和信息流。

进程视图（Process View）描述系统的并发和分布式特性，关注系统中的进程、线程、任务以及它们之间的关系和通信。该视图展示了系统的并发性、性能、可伸缩性等方面。

物理视图（Physical View）描述系统在硬件和软件环境中的部署和分布情况，包括物理设备、网络拓扑、软件组件的部署位置等。它关注系统的部署架构、可靠性、安全性等方面。

开发视图（Development View）关注系统的软件开发过程和组织结构，描述软件模块的组织、构建、测试和部署过程。它展示了软件开发团队的组织结构、开发工具、版本控制等方面。

场景视图（Scenario View）描述系统在特定使用情境下的行为和交互，以用户场景、用例或故事来说明系统的功能和行为。它帮助验证和验证系统架构的正确性和适应性。

C4模型是一种简洁、易于理解的软件架构建模方法，由Simon Brown提出。它通过四个层次的视图来描述软件系统的不同方面，包括语境视图(Context Diagram，这里借鉴了《[程序员必读之软件架构](https://book.douban.com/subject/26248182/)》)一书中对Context的翻译)、容器视图(Container Diagram)、组件视图(Component Diagram)和代码视图(Code Diagram)，如下图所示：

![](../../assets/4b171e6c3d2343f6.png)


语境视图是最高层级的视图，用于描述软件系统与外部实体之间的关系和交互。它展示了系统所处的环境和与外部实体（如用户、其他系统、第三方服务等）的关系，以及它们之间的交互方式。

容器视图关注系统内部的软件容器及其之间的关系和交互。容器可以是物理的、虚拟的或逻辑的，它们承载着系统中的组件或服务。容器可以是应用程序、数据库、消息队列、Web服务等。容器视图描述了系统的主要部件，以及它们之间的依赖关系和通信方式。

组件视图进一步展开容器视图中的组件，描述系统内部的组件及其之间的关系和交互。组件视图展示了系统的模块、类、库或其他可重用的软件单元，并显示它们之间的依赖关系、接口和通信方式。

代码视图是最底层的视图，关注具体的代码实现细节。它用于描述系统中的类、函数、方法等代码单元的结构、关系和实现细节。代码视图可以是面向对象的类图、模块图或其他代码组织结构的表示方式，用于帮助开发人员理解和浏览源代码。

下面示意图可以更直观的展示出语境、容器、组件以及代码之间这种逐渐“展开”的层次关系：

![](../../assets/fd845e11fc82df82.png)


通过C4模型的这四个层次的视图，架构师可以逐渐深入地描述和表达软件系统的不同层次和组成部分，从整体到细节，帮助团队成员和利益相关者更好地理解和沟通软件架构。

Arc42是一种用于软件架构文档化的模板和方法，它提供了一套规范和指导原则来描述软件系统的架构。下面是Arc42的全景图：

![](../../assets/1f0953d884c9dd20.png)


我们看到：Arc42模板也包含了多个视图，每个视图都关注系统架构的不同方面，包括Context、Building Block View、Runtime View以及Deployment View等。

Context View：描述系统与其外部环境之间的关系和交互，强调边界的概念，分为技术Context与业务Context。

部署视图（Deployment View）描述了系统的部署架构和环境，包括物理设备、服务器、网络拓扑以及协议等信息。

构件视图（Building Block View）描述了系统内部的组件、模块、子系统、包等，并展示它们之间的关系和依赖。构件视图是源码结构的概览。

运行时视图（Runtime View）描述了系统在运行时的行为和交互以及具体场景下对其他构件的运行时依赖。使用序列图、状态图等方式可展示系统的运行时行为。

### 2.7 Diagrams As Code

架构设计不是一成不变的，需要不断演进，因此架构视图也需要“与时俱进”的更新。但直接更新图片格式似乎很不方便，也无法在形式上很好的达成一致，于是一些基于[DSL](https://tonybai.com/2022/05/10/introduction-of-implement-dsl-using-antlr-and-go)语法生成架构设计图(Diagram)的工具便涌现了出来，比如：[PlantUML](http://plantuml.com/)、[Structurizr](https://structurizr.com/dsl)、[Mermaid](https://mermaid.live/)等。有了这些工具，架构师便可以使用文本编辑器来“画图”，支持“所见即所得”。并且由于Diagrams As Code(代码即图)，我们可以将架构设计图与版本控制系统很好地集成。

到这里，我们知道了基于多视角+“Diagrams As Code”是目前的主流的架构设计表达和实践方法，那么我们在软件架构表达实践中，究竟选择哪几个视角来表达呢？这个目前没有统一标准。调研了4+1 Views、C4 model以及Arc42后，我这里说说自己日常做架构表达时使用的最小视图集。

## 3. 最小图集

很多读者可能听说或学习过或实践过[金字塔写作](https://book.douban.com/subject/33391219/)，金字塔写作原理是一种用于新闻报道和科技写作的写作方法，它的核心思想是将最重要的信息放在文章的开头，然后逐渐向下展开，提供更多的细节和背景信息。

金字塔写作的优势在于：

- 它可以迅速吸引读者的注意力，让读者在最短时间内了解文章的核心内容；
- 它还可确保信息传递：将最重要的信息放在开头，可以避免读者在阅读过程中错过关键信息或迷失在细枝末节中，确保信息有效地传达给读者；
- 它还具备灵活性和可定制性，不要求严格按照一个固定的结构来组织文章，而是提供了一种基本的思路和原则，可以根据具体情况进行调整和定制，以适应不同的写作需求和读者群体。

我理解，金字塔写作方法之所以能够成功，其本质是站在了读者的角度去思考问题，想读者之所想，做读者之所需。

软件架构表达的目的也是让开发人员快速深入的理解架构，与设计人员达成共识，指导后续软件系统的实现。所以要想形成有效表达，我们就需要像金字塔写作那样**站在开发人员的角度**来考虑架构表达，借鉴金字塔原理，自上而下，先表达最重要的信息，然后逐渐向下展开，避免开发人员在理解过程中错过关键信息或迷失在细枝末节当中。

综合前面介绍的多种Views的方法，我们觉得软件架构表达的起点，即第一个图必须是语境图(Context Diagram)。

### 3.1 语境图(Context Diagram)

语境图表达的是系统最高的抽象层次，是最高视角，全局视角。通过语境图，可以解决开发人员在内心中提出的下面问题：

- 我们构建的（或已经构建的）软件系统是什么(What)？
- 谁会用它？
- 如何融入已有的IT环境？
- 系统的边界是什么？（业务的，技术的)

语境图不会也不应该展示太多细节，它是软件系统设计图的起点。后续的图都是用“放大镜”将我们的系统放大后的细节的表达。当牵涉到理解系统间接口的问题时，语境图还可以为你识别可能需要沟通的人提供了一个起点。

语境图向开发者展现的重点在于软件系统的范围以及与外部的交互行为（用户< – >系统、系统< – >系统等等）。下面是使用[structurizr](https://structurizr.com/dsl)绘制的一个语境图的实例：

![](../../assets/e9ca592521d94f36.png)


语境图中心蓝色的矩形框代表的是我们的软件系统，上方的user、role、actor是我们的软件系统的用户；client是与我们的软件系统交互的系统，是系统到系统交互的一个代表；在我们的软件系统、Inner System1和Inner System2之外有一个虚线框，代表了企业范围；而Inner System1和Inner System2是我们的软件系统在企业内部依赖的系统；同时，我们的软件系统还依赖企业外部的Outer System1和Outer System2。

上述语境图对应的structurizr dsl代码如下：

```
// system context diagrams
workspace {
model {
u = person "User"
r = person "Role"
a = person "Actor"
c = softwareSystem "Client Software System" {
tags "client"
}
enterprise = group "Enterprise A" {
s = softwareSystem "Our Software System" {
tags "server"
}
d1 = softwareSystem "Inner System1" {
tags "dep"
}
d2 = softwareSystem "Inner System2" {
tags "dep"
}
}
d3 = softwareSystem "Outer System1" {
tags "dep"
}
d4 = softwareSystem "Outer System2" {
tags "dep"
}
u -> s "Uses"
r -> s "Uses"
a -> s "Uses"
c -> s "Call"
s -> d1 "Uses"
s -> d2 "Uses"
s -> d3 "Uses"
s -> d4 "Uses"
}
views {
systemContext s {
include *
autoLayout
}
styles {
element "server" {
background #1168bd
color #ffffff
}
element "dep" {
background #e5e4e2
color #000000
}
element "client" {
background #e5e4e2
color #000000
}
element "Person" {
shape person
background #08427b
color #ffffff
}
}
}
}
```


基于语境图，就好比我们站在万米高空一览Our Software System。不过对于架构设计表达来说，这还不够，现在是时候下降高度让视野进入到系统内部去挖掘一些细节了。

### 3.2 容器图(Container Diagram)

在从万米高空的系统全局视角了解了我们的软件系统是什么后，我们将第一次进入到系统内部。我们现在所处的高度是100米，在这个高度上，可以清晰地看到软件系统的整体形态、内部脉络、技术选择、职责分布以及各个部分之间是如何交流的。我们将每个部分称为一个容器(container)。一个容器通常可以表示一个应用/服务或数据存储，如果你的软件系统采用了微服务架构，那么将每个服务作为一个容器通常是可行的。

针对每个容器，我们可以设置它的属性：名字(如Web App、API网关、关系数据库存储、订阅服务等）、实现技术(如mvc等)以及功能性的描述。在容器间的联系上我们可以附加上通信方式(json over http、gRPC、websocket等)。

下面是上面语境图中的My Software System的容器图：

![](../../assets/988b09d425021b97.png)


在这个容器图中，我们看到了系统支持通过Web app和mobile app访问和使用；系统的入口使用了API网关；系统内部分为业务服务和基础服务，基础服务封装了到关系数据库、对象存储(oss)的接口(关系数据库和oss都是技术选择)；业务服务可以调用企业内部服务，亦可调用企业外部服务，并且明确了调用方式。

下面是生成上述容器图的structurizr的代码：

```
// container diagrams
workspace {
model {
u = person "User"
enterprise = group "Enterprise A" {
s = softwareSystem "Our Software System" {
tags "server"
mobileApp = container "Mobile App" {
tags "container"
}
webApp = container "Web App" {
tags "container"
}
apiGw = container "API Gateway" {
tags "container"
}
biz1 = container "Business Service 1" {
tags "container"
}
biz2 = container "Business Service 2" {
tags "container"
}
biz3 = container "Business Service 3" {
tags "container"
}
base1 = container "Base Service 1" {
tags "container"
}
base2 = container "Base Service 2" {
tags "container"
}
base3 = container "Base Service 3" {
tags "container"
}
rds = container "Relational Database system" {
tags "container"
}
oss = container "Object Storage Service" {
tags "container"
}
}
d1 = softwareSystem "Inner System1" {
tags "dep"
}
d2 = softwareSystem "Inner System2" {
tags "dep"
}
}
d3 = softwareSystem "Outer System1" {
tags "dep"
}
d4 = softwareSystem "Outer System2" {
tags "dep"
}
u -> mobileApp "Uses"
u -> webApp "Uses"
mobileApp -> apiGw "Makes API calls to" "JSON/HTTPS"
WEBApp -> apiGw "Makes API calls to" "JSON/HTTPS"
apiGw -> biz1 "Route API calls to" "gRPC"
apiGw -> biz2 "Route API calls to" "gRPC"
apiGw -> biz3 "Route API calls to" "gRPC"
biz1 -> base1 "Inner API calls to" "gRPC"
biz1 -> base2 "Inner API calls to" "gRPC"
biz2 -> base2 "Inner API calls to" "gRPC"
biz2 -> base3 "Inner API calls to" "gRPC"
biz3 -> base3 "Inner API calls to" "gRPC"
base1 -> rds "Reads from and writes to" "Raw SQL"
base1 -> oss "Reads from and writes to" "HTTPS"
base2 -> rds "Reads from and writes to" "Raw SQL"
base3 -> oss "Reads from and writes to" "HTTPS"
biz1 -> d1 "Make API calls to" "HTTP"
biz2 -> d3 "Make API calls to" "HTTP"
biz3 -> d2 "Make API calls to" "HTTP"
biz3 -> d4 "Make API calls to" "HTTP"
}
views {
container s {
include *
autoLayout
}
styles {
element "server" {
background #1168bd
color #ffffff
}
element "container" {
background #1168bd
color #ffffff
}
element "dep" {
background #e5e4e2
color #000000
}
element "Person" {
shape person
background #08427b
color #ffffff
}
}
}
}
```


注：在容器图这个层次上，group关键字没有起作用，导致企业内部服务与外部服务放在一起了。


按照C4 model的思路，接下来我们会再下降高度，来到10米的高空，进入到某个容器的内部。但容器内部的设计在我看来属于详细设计范畴，如果采用的是微服务架构，那么容器内部的设计就相当于某个服务的设计。所以这里，我并未将这部分作为架构表达的必需之图。

### 3.3 序列图(Sequence Diagram)

无论是语境图，还是容器图，从大类来看，都属于静态的结构图。但做过软件系统设计和研发的童鞋都知道，仅有静态的表达还是不够的，不足以传达软件系统的所有信息，我们还需要对动态行为的表达。这就是为什么我将序列图作为软件表达最小图集一份子的原因。

可能有些人将序列图作为需求分析阶段的产物，其实，序列图既可以在需求阶段产生，也可以在架构设计阶段产生。它在不同阶段有不同的应用和目的。

在需求阶段，序列图被用于描述系统的功能需求和行为。它可以帮助分析和定义系统的用例或用户故事，以及系统与外部实体（如用户、其他系统、服务等）之间的交互过程。通过序列图，需求分析人员和开发团队可以更清晰地理解系统的功能需求，并就用户与系统之间的交互进行沟通和确认。

在架构设计阶段，序列图被用于描述系统的结构和组件之间的交互。在这个阶段，序列图通常用于展示系统的运行时行为、组件之间的消息传递和调用关系。架构师使用序列图来验证系统的设计方案，确保系统的各个组件按预期互相协作，并满足功能和性能要求。

这里的序列图，可以对应前面的Arc42的Runtime View，以及C4 model的[Dynamic Diagram](https://c4model.com/#DynamicDiagram)。

序列图也是UML语言中最常被使用的一种Diagram，即便是在UML不那么被提及的今天，我个人也推荐使用[UML的序列图](https://www.uml-diagrams.org/sequence-diagrams.html)来表达，而不推荐用structurizr来画了，structurizr在序列图方面的表达能力还是弱了许多。

你可以用你最喜欢的画图工具来绘制UML序列图（比如我经常用的[drawio](https://www.drawio.com)），也可以选择[plantuml](https://plantuml.com/zh/sequence-diagram)这种基于DSL语法生成序列图的方式来绘制。plantuml对序列图的支持还是非常好的，支持了序列图的大多数元素，可以绘制出非常复杂的图来(下图来自plantuml官网)：

![](../../assets/3ddbca37cbe91362.png)


针对一个复杂的软件系统，我们可能需要针对不同的Container(或更进一步的组件)绘制较多的序列图，至少要覆盖到软件系统各个Container的核心交互流程。

### 3.4 部署图(Deployment Diagram)

无论是C4模型，还是arc42，亦或是UML语言，都包含部署图。在软件架构表达时，准确表达部署设计，对开发人员后续的实现具有很好的指导作用。通过部署图，架构设计人员可以说明静态图中的软件系统和/或容器实例是如何部署到给定部署环境（如生产、暂存、开发等）中的基础设施上的，比如下面这个部署示意图(来自c4model.com)：

![](../../assets/a437b40d927ea828.png)


我们看到部署图中的核心角色是部署节点(Node)，它代表了软件系统/容器实例运行的位置；可能是物理基础设施（如物理服务器或设备）、虚拟化基础设施（如IaaS、PaaS、虚拟机）、容器化基础设施（如Docker容器）、执行环境（如数据库服务器、Java EE Web/应用服务器、Microsoft IIS）等，并且部署节点还可以嵌套。此外，右下角的”x N”表示需要多少个部署节点。

通过部署图还可以表达云基础架构的情况(下图来自c4model.com)，可以包含DNS、负载均衡器以及防火墙等部署的基础设施的节点：

![](../../assets/b15dd445cf1b399f.png)


structurizr对于部署图支持的还不错，还可以像上图那样使用不同公有云提供商特色的Theme来绘制部署图。

到这里，我们已经“凑齐”了表达软件系统架构的最小图集：语境图、容器图、序列图和部署图。我们要学会灵活使用这些图。在软件系统十分复杂的情况下，我们可以将语境图分为[System Landscape diagram](https://c4model.com/#SystemLandscapeDiagram)和多个sub system的语境图，之后以此类推，对于每个sub system做容器图等。

## 4. 最小图集之外的图(可选)

有些公司或组织会将架构设计阶段延伸到container内部，这样对软件系统架构的表达就要延伸到详细设计，甚至是编码阶段时，我们就要考虑下面两个类型的Diagram了：组件图和代码图。

### 4.1 组件图(Component Diagram)

如果容器图阶段，你所在的高度是100米，那么组件图阶段，你将位于高度为10米的空中，这足以让你看清容器中每个组件(Component)的细节。

组件图就是容器内部的设计，它涉及到容器内部各个逻辑组件的结构与组件间的交互。在这个层次，你可以使用你擅长的面向对象设计方法，或者面向契约/接口的设计模式，你也可以使用一些成熟的企业应用设计模式，比如MVC等。

下面是一张组件图示例(来自c4model.com)：

![](../../assets/3390131f255af240.png)


我们看到中间的部分就是API Application这个容器内部的逻辑组件结构与交互情况。有些时候在组件图这一层面，我们甚至可以对照初对应项目中的代码布局结构。

对于组件图中关键组件间的复杂交互流程，可辅以序列图的方式来表达。

此外，组件图可以使用structurizr绘制，语法和语境图、容器图十分相似。

### 4.2 代码图(Code Diagram)

再下降，我们来到离地面1米的高度，我们几乎要躬身入局，参与编码了。通常架构设计不会到达这个阶段，架构师们在100米或10米高度完成任务后，就可以去休息了。

但如果包含这个阶段，我们要给出的便是代码图(Code Diagram)，再直白些，就是UML类图、E-R关系图等，下面是一个示意图：

![](../../assets/20489823889c1de3.png)


这是一个直面开发人员的图，你可以看到编程语言中的那些机制：接口、继承、实现等等，开发人员甚至可以通过工具将这样的uml class图直接转换为项目的骨架代码。

## 4. 小结

本文首先介绍了为什么软件架构需要有效表达，以便开发者更好地理解架构设计。然后回顾了软件架构表达方式的演进历史，从自然语言描述到图形化表达，再到结构化图形表达、UML、形式化表达，最终发展到现在的多视角表达方式。

文章结合笔者实践经验，借鉴多个多视角软件架构模型，提出了最小图集的概念，笔者认为有效表达软件架构最关键的视角有四个，分别是:

- 语境图：描述系统的整体位置和边界
- 容器图：展示系统内部的容器及其关系
- 序列图：呈现容器内组件以及组件之间的交互行为
- 部署图：阐明系统在实际环境中的部署情况

此外，我认为还可根据需要补充组件图和代码图等更细节的视图。这套最小图集能较全面地表达软件系统的静态结构和动态行为，帮助开发者理解架构设计。

总的来说，该文章从工程实践的视角出发，提出了一套行之有效的软件架构表达方法，对于架构设计的团队沟通及实现具有很好的指导意义。

btw，在容器图或组件图设计阶段，如果要完善工程设计，还可以结合具体的接口文档予以表达，比如基于Swagger的API设计文档等。

## 5. 参考资料

- 《
[Software Architecture for Developers](https://book.douban.com/subject/26248182/)》- https://book.douban.com/subject/26248182/ [The C4 model for visualising software architecture](https://c4model.com)– https://c4model.com[Unified Modeling Language Specification](https://www.omg.org/spec/UML)– https://www.omg.org/spec/UML[The Unified Modeling Language](https://www.uml-diagrams.org)– https://www.uml-diagrams.org[Communicating Software Architecture](https://arquisoft.github.io/slides/course2021/EN.ASW.TE03_Documentation.pdf)– https://arquisoft.github.io/slides/course2021/EN.ASW.TE03_Documentation.pdf[arc42](https://arc42.org)– https://arc42.org

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论