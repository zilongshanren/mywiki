---
title: BPF和Go：在Linux中内省的现代方式[译]
url: https://tonybai.com/2020/12/25/bpf-and-go-modern-forms-of-introspection-in-linux/
published: '2020-12-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# BPF和Go：在Linux中内省的现代方式[译]

本文翻译自马可·凯瓦克（Marko Kevac）的[《BPF and Go: Modern forms of introspection in Linux》](https://medium.com/bumble-tech/bpf-and-go-modern-forms-of-introspection-in-linux-6b9802682223)(https://medium.com/bumble-tech/bpf-and-go-modern-forms-of-introspection-in-linux-6b9802682223)。

![img{512x368}](../../assets/eb4f48eddb115d2f.png)


每个人都有自己喜欢的关于魔法的书。对于一个人来说是托尔金，对于另一个人来说是普拉切特，对于第三个人来说，比如我，是马克斯-弗雷。今天我要给大家讲的是我最喜欢的IT魔法：[BPF](http://en.wikipedia.org/wiki/Berkeley_Packet_Filter)以及围绕它的现代基础设施。

BPF目前正处于普及的高峰期。这项技术正在飞速发展，深入到意想不到的地方，并且越来越容易被普通用户所接受。现在几乎每个流行的会议都有关于这个主题的演讲，早在8月份，我就应邀在俄罗斯GopherCon上(GopherCon Russia)做了这方面主题的演讲。

我在这方面有着很好的体验，所以我想和尽可能多的人分享一下。这篇文章将为你介绍为什么我们需要像BPF这样的东西，帮助你了解何时、如何使用它，以及它如何帮助作为工程师的你改善你正在进行的项目。我们还将看看它与Go的一些相关内容。

我真正希望的是，你看完这篇文章后，就像小孩子第一次读完《哈利波特》后的眼睛一样，开始发亮，并且希望你自己亲自去尝试一下这个新“玩具”。

## 一点点的背景

好吧，一个34岁的大胡子，眼神灼灼的告诉你这个魔法是什么？

我们生活在2020年。打开Twitter，你可以读到愤怒的技术人士的推文，他们都在说，今天编写的软件质量太糟糕了，都需要扔掉，我们需要重新开始。有些人甚至威胁要彻底离开这个行业，因为他们实在无法忍受所有东西都坏了，不方便又慢。

![img{512x368}](../../assets/77bf4c032637b036.png)


他们可能是对的：如果不查阅千篇一律的评论，就无法确定原因。但有一点我绝对同意，那就是现代软件堆栈比以往任何时候都要复杂：我们有BIOS、EFI、操作系统、驱动程序、模块、库、网络交互、数据库、缓存、编排器（比如K8s）、Docker容器，最后还有我们自己的带有运行时和垃圾收集的软件。

一个真正的专业人士可能会花上几天时间来为你解释在浏览器中输入google.com之后会发生什么。

要了解你的系统里面发生了什么，是非常复杂的，尤其是在目前，事情出了问题，你正在损失金钱的情况下。正是因为这个问题，才出现了帮你搞清楚系统内部情况的企业。在大公司里，有整整一个部门的福尔摩斯式的侦探，他们只知道在哪里敲敲锤子，在哪里拧紧螺栓就能节省数百万美元。

我喜欢问人们如何在最短的时间内调试突发问题。大多数情况下，人们首先想到的方法是**分析日志**。但问题是，能获取的日志只局限于开发者放在系统中的日志，这是不灵活的。

第二种最流行的方法是**研究度量数据**。最流行的三个研究度量数据的系统都是用Go编写的。度量数据是非常有帮助的，然而，虽然它们确实可以让你看到症状，但它们并不总是能帮助你定义出问题的根本原因。

第三种是所谓的“可观察性”：你可以对系统的行为提出尽可能多的复杂问题，并获得这些问题的答案。由于问题可能非常复杂，所以答案可能需要最广泛的信息，而在问题被提出之前，我们并不知道这些信息是什么。而这意味着，可观察性绝对要求灵活性。

提供一个机会来改变”在飞行中”的日志级别呢？使用调试器，在程序运行时连接到程序，并在不中断程序工作的情况下做一些事情呢？了解哪些查询被发送到系统中，可视化慢速查询的来源，通过pprof看看什么在占用内存，并获得其随时间变化的曲线图？测量一个函数的延迟以及延迟对参数的依赖性呢？我想把所有这些方法都归入**可观察性**这个总称之下。这是一组实用工具、方法、知识和经验，它们结合在一起，给了我们机会，如果不能做到我们想做的所有事情，但至少可以在系统工作时，在系统中“现场”做很多事情。它相当于现代IT界的一把瑞士军刀。

![img{512x368}](../../assets/a13debfbefe3b0d7.png)


但我们如何才能实现这一点呢？市场上已经存在很多类似的工具：有简单的，有复杂的，有危险的并且也有缓慢的。但今天的文章是关于BPF的。

Linux内核是一个事件驱动的系统。实际上，在内核和系统中发生的所有事情，都可以被认为是一组事件。中断是一个事件；通过网络接收一个数据包是一个事件；将处理器的控制权转移到另一个进程是一个事件；运行一个函数是一个事件。

对，所以BPF是Linux内核的一个子系统，它让你有机会编写小程序，这些小程序将在内核响应事件时被运行。这些程序既可以让你知道系统中发生了什么，也可以用于控制系统。

现在让我们来了解一下具体的内容。

## 什么是eBPF？

BPF的第一个版本在1994年问世。你们中的一些人可能会在为tcpdump工具编写简单的规则时遇到过它，该工具用于查看或”嗅探”网络数据包。你可以为tcpdump设置过滤器，所以你不必查看所有的数据包–只查看你感兴趣的数据包。例如，”只查看tcp协议和80端口”。对于每一个经过的数据包，都会运行一个函数来决定你是否需要保存这个特定的数据包。可以有非常多的数据包，所以我们的函数必须要快。事实上，我们的tcpdump过滤器被转化成了BPF函数。下面是一个例子。

![img{512x368}](../../assets/150071b5d0d1d196.png)


最初的BPF代表了一个非常简单的虚拟机，有几个寄存器。但尽管如此，BPF还是大大加快了网络数据包的过滤速度。在当时，这是一个重大的进步。

![img{512x368}](../../assets/99b68210a034e243.png)


2014年，一位非常著名的内核黑客[Alexei Starovoitov](https://www.linkedin.com/in/alexey1/)对BPF的功能进行了扩展。他增加了寄存器的数量和程序允许的大小，增加了JIT编译，并创建了一个用于检查程序是否安全的程序。然而，最令人印象深刻的是，新的BPF程序不仅能够在处理数据包时运行，而且能够响应其他内核事件，并在内核和用户空间之间来回传递信息。

这些变化为使用BPF的新方法提供了机会。一些过去需要通过编写复杂而危险的内核模块来实现的事情，现在可以相对简单地通过BPF来完成。为什么这么好呢？因为在编写模块的时候，任何错误往往都会导致恐慌(panic)，这可不是Go语言中的恐慌(panic)，而是内核恐慌。一旦发生，我们唯一能做的就是重启(操作系统)。

普通的Linux用户突然拥有了一种新的超能力：能够查看”引擎盖下的情况”–这在以前只有核心内核开发者才有，或者说根本就没有人能够做到。这个选项可以和为iOS或Android编写程序的能力相提并论：在旧手机上，这要么是不可能的，要么就是太复杂。

Alexei Starovoitov的新版本的BPF被称为eBPF（e代表扩展：extended）。但现在，它已经取代了所有旧版的BPF用法，并且已经变得非常流行，为了简单起见，它仍然被称为BPF。

## BPF用在哪里？

好了，我们可以将BPF程序附加到哪些事件或触发器上呢，人们又是如何开始使用他们获得的新力量的呢？

目前，触发器主要有两组。

第一组是用于处理网络数据包和管理网络流量的。这是XDP、流量控制事件和其他几个。

以下情况需要这些事件：

-
创建简单但非常有效的防火墙。Cloudflare和Facebook等公司使用BPF程序来过滤掉大量的寄生流量，并对抗最大规模的DDoS攻击。由于处理发生在数据包生命的最早阶段，直接在内核中进行（一个BPF程序有时甚至直接推送到网卡中进行处理），所以巨量的流量可以通过这种方式进行处理。这些事情过去都是在专门的网络硬件上完成的。

-
创建更智能、更有针对性、但性能更强的防火墙–这些防火墙可以检查通过的流量是否符合公司规则，是否存在漏洞模式等。例如，Facebook在内部进行这种审计，而一些项目则对外销售这类产品。

-
创建智能负载均衡器。最突出的例子是Cilium项目，它最常被用作K8s集群中的网格网络。Cilium对流量进行管理，平衡、重定向和分析。而所有这些都是在内核运行的小型BPF程序的帮助下完成的，以响应与网络数据包或套接字有关的这个或那个事件。


这是第一组与网络问题有关的触发器，并能够影响网络通信行为。第二组与更普遍的可观察性有关；这组中的程序大多时候无法影响任何事情，而只能”观察”。这是我比较感兴趣的。

在这组中，有如下触发器。

-
perf events – 与性能和perf Linux剖析器有关的事件：硬件处理器计数器，中断处理，拦截主要/次要内存异常等等。例如，我们可以设置一个处理程序，它将在每次内核需要从swap读取内存页时运行。例如，想象一下，一个显示当前使用swap的程序的工具。

-
tracepoints – 内核源代码中的静态（由开发者定义）位置，你可以通过附加到这些位置来提取静态信息（由开发者早先准备的信息）。在这种情况下，静态似乎是一件坏事，因为我说过，日志的缺点之一是它们只包含程序员最初放在那里的东西。从某种意义上说，这是对的，但tracepoints有三个重要的优点。

- 有相当多的跟踪点散落在内核中最有趣的地方。
- 当它们不 “开启 “时，它们不使用任何资源。
- 它们是API的一部分，它们是稳定的，而且不会改变。这一点非常重要，因为我们将要提到的其他触发器缺乏稳定的API。


例如，想象一下，一个有关显示的工具程序(utility)，由于某种原因，内核没有给它执行的时间。你坐着想知道为什么它这么慢，而pprof却没有什么有趣的东西可以显示。

- USDT – 和tracepoints是一样的，但是是针对用户空间的程序。也就是说，作为一个程序员，你可以把这些位置添加到你的程序中。而且很多大规模的知名程序和编程语言已经采用了这些trace。比如：MySQL，或者PHP和Python等语言。通常它们的默认设置是”关闭”，如果要打开它们，你需要使用–enable-dtrace参数或类似的参数来重建解释器。是的，我们也可以在Go中注册这些类型的跟踪。你可能已经认出了参数名称中的单词
。重点是，这种静态跟踪是由**DTrace**[Solaris操作系统](https://en.wikipedia.org/wiki/Solaris_(operating_system))中诞生的同名系统所推广的。举个例子，想象一下，当一个新的线程被创建时，当一个GC或其他与特定语言或系统有关的东西被启动时，我们都能够觉察到。

这就是另一个层次的魔法开始的地方。

-
Ftrace触发器让我们可以选择在内核的任何功能开始时运行一个BPF程序。完全是动态的。这意味着内核会在你选择的任何内核函数开始执行之前，或者在所有内核函数开始执行之前，调用你的BPF函数–无论哪个，你都可以连接到所有的内核函数，并在输出时获得所有调用的可视化效果。

-
kprobes/uprobes给你提供的东西和ftrace几乎一样，但是你可以选择在内核和用户空间执行一个函数时附加到任何位置。如果在函数中间，有一个变量上的’if’，而你需要为这个变量建立一个值的直方图，那就不是问题了。

-
kretprobes/uretprobes–这里的一切类似于前面的触发器，但可以在内核函数或用户空间的函数返回时触发。这类触发器对于查看函数返回的内容，以及测量执行时间都很方便。例如，你可以查看’fork’系统调用返回的是哪个PID。


关于这一切，我重复一遍，最美妙的事情是，当我们的BPF程序响应这些触发器而被调用后，我们的BPF程序可以好好的 “观察”一下：读取函数的参数，记录时间，读取变量，读取全局变量，进行堆栈跟踪，为以后保存一些东西，将数据发送到用户空间进行处理，和/或从用户空间获取数据或一些其他控制命令进行过滤。太棒了！

我不知道你是怎么想的，但对我来说，这个新的基础架构就像一个我一直想得到的玩具。

## API：如何使用它

好了，马科，你已经说服了我们去看看BPF。现在我们怎么才能仔细看看呢？

让我们看看BPF程序由什么组成，以及如何与它交互。

![img{512x368}](../../assets/c67201fcdaf98512.png)


首先，我们有一个BPF程序，如果它通过验证，将被加载到内核中。在那里，它将被JIT编译器编译成机器代码，并在内核模式下运行，这时附加的触发器(trigger)将被激活。

BPF程序可以选择与第二部分，即与用户空间程序交互。有两种方式可以实现。我们可以向循环缓冲区写，用户空间部分可以从它那里读。我们也可以对键值图(key-value map)进行写和读，也就是所谓的BPF图(BPF map)，相应的，用户空间部分，也可以做同样的事情，这样，它们就可以互相传递信息了。

## 基本用途

最简单的BPF工作方式，但却是你在任何情况下都不应该采用的从头开始的方式，就是用C语言编写BPF程序，然后用Clang编译器，将相关代码编译成虚拟机的代码。然后，我们加载这些代码，直接使用BPF系统调用，与我们的BPF程序进行交互，也使用BPF系统调用。

第一个可用的简化方法是使用libbpf库。这是和内核的源代码一起提供的，可以让你直接使用BPF系统调用。基本上，它提供了方便的包装器来加载代码，以及使用BPF映射(BPF map)来从内核向用户空间发送数据并返回。

## bcc

显然，这对人们来说是远远不够方便的。幸运的是，在iovizor这个品牌下，出现了BCC项目，这让我们的生活变得更加方便。

![img{512x368}](../../assets/b2fd9ad9beccd7e7.png)


基本上，它为我们准备了整个构建环境，让我们可以编写单个的BPF程序，其中С部分会自动构建并加载到内核中，而用户空间部分则可以用Python制作，简单明了。

但是，BCC似乎仍有很多事情很复杂。由于某些原因，人们特别不喜欢用С来写底层那部分。

那些来自iovizor的人也提供了一个工具–bpftrace，它可以让你用类似AWK的简单脚本语言（甚至是单行代码）来编写BPF脚本。

![img{512x368}](../../assets/c2051eccf29ff5a2.png)


Brendan Gregg是生产力和可观察性领域的著名专家，他为可用的BPF工作方式制作了以下的图片。

![img{512x368}](../../assets/941a95b57cb85d18.png)


纵轴显示的是某个工具的易用性，而横轴显示的是它的能力。你可以看到，BCC是一个非常强大的工具，但它并不是超级简单的工具。

## 使用BPF的例子

让我们来看看一些具体的例子，看看我们已经可以使用的这种神奇力量。

BCC和bpftrace都包含了一个”工具”目录，其中包含了大量有趣而有用的即用型脚本。它们也可以作为本地的Stack Overflow使用，你可以从中复制代码块用于自己的脚本。

例如，这里是显示DNS查询延迟的脚本。

```
╭─marko@marko-home ~
╰─$ sudo gethostlatency-bpfcc
TIME PID COMM LATms HOST
16:27:32 21417 DNS Res~ver #93 3.97 live.github.com
16:27:33 22055 cupsd 7.28 NPI86DDEE.local
16:27:33 15580 DNS Res~ver #87 0.40 github.githubassets.com
16:27:33 15777 DNS Res~ver #89 0.54 github.githubassets.com
16:27:33 21417 DNS Res~ver #93 0.35 live.github.com
16:27:42 15580 DNS Res~ver #87 5.61 ac.duckduckgo.com
16:27:42 15777 DNS Res~ver #89 3.81 www.facebook.com
16:27:42 15777 DNS Res~ver #89 3.76 tech.badoo.com
```

16:27:43 21417 DNS Res~ver #93 3.89 static.xx.fbcdn.net
16:27:43 15580 DNS Res~ver #87 3.76 scontent-frt3-2.xx.fbcdn.net
16:27:43 15777 DNS Res~ver #89 3.50 scontent-frx5-1.xx.fbcdn.net
16:27:43 21417 DNS Res~ver #93 4.98 scontent-frt3-1.xx.fbcdn.net
16:27:44 15580 DNS Res~ver #87 5.53 edge-chat.facebook.com
16:27:44 15777 DNS Res~ver #89 0.24 edge-chat.facebook.com
16:27:44 22099 cupsd 7.28 NPI86DDEE.local
16:27:45 15580 DNS Res~ver #87 3.85 safebrowsing.googleapis.com
^C%


一个实时显示DNS查询完成时间的实用工具，例如，你可以抓住一些意想不到的异常值。

下面是一个可以”监视”别人在终端上输入的内容的脚本。

```
╭─marko@marko-home ~
╰─$ sudo bashreadline-bpfcc
TIME PID COMMAND
16:51:42 24309 uname -a
16:52:03 24309 rm -rf src/badoo
```


这种脚本可以用来捕捉”坏邻居”，或者对公司的服务器进行安全审计。

下面是一个输出高级语言函数调用链的脚本。

```
╭─marko@marko-home ~/tmp
╰─$ sudo /usr/sbin/lib/uflow -l python 20590
Tracing method calls in python process 20590... Ctrl-C to quit.
CPU PID TID TIME(us) METHOD
5 20590 20590 0.173 -> helloworld.py.hello
5 20590 20590 0.173 -> helloworld.py.world
5 20590 20590 0.173 <- helloworld.py.world
5 20590 20590 0.173 <- helloworld.py.hello
5 20590 20590 1.174 -> helloworld.py.hello
5 20590 20590 1.174 -> helloworld.py.world
5 20590 20590 1.174 <- helloworld.py.world
5 20590 20590 1.174 <- helloworld.py.hello
5 20590 20590 2.175 -> helloworld.py.hello
5 20590 20590 2.176 -> helloworld.py.world
5 20590 20590 2.176 <- helloworld.py.world
5 20590 20590 2.176 <- helloworld.py.hello
6 20590 20590 3.176 -> helloworld.py.hello
6 20590 20590 3.176 -> helloworld.py.world
6 20590 20590 3.176 <- helloworld.py.world
6 20590 20590 3.176 <- helloworld.py.hello
6 20590 20590 4.177 -> helloworld.py.hello
6 20590 20590 4.177 -> helloworld.py.world
6 20590 20590 4.177 <- helloworld.py.world
6 20590 20590 4.177 <- helloworld.py.hello
^C%
```


下面这个例子显示了Python中程序的调用栈。(译注：原文似乎缺了这块的代码)。

Brendan Gregg 制作了一张图片，它汇集了所有相关的脚本，箭头指向每个实用程序允许你观察的子系统。正如你所看到的，我们已经有了大量的现成的实用程序供我们使用–几乎可以应对任何可能的情况。

![img{512x368}](../../assets/7056b380a28508cd.png)


## 那Go语言呢？

现在我们来谈谈Go。我们有两个基本问题。

- 你能用Go写BPF程序吗？
- 你能分析用Go写的程序吗？

我们按顺序来做。

目前，唯一能够编译成BPF机器(BPF machine)能够理解的格式的编译器是Clang。另一个流行的编译器GСС，但gcc仍然没有BPF后端。而能够编译成BPF的编程语言，只有C语言的一个非常有限的版本(C的子集)。

然而，BPF程序还有第二部分，就是在用户空间。而这可以用Go来编写。

正如我在上面已经提到的，BCC允许你用Python来编写这部分，而Python是该工具的主要语言。同时，在主库中，BCC还支持Lua和C++，而且，在辅库中，它还支持[Go](https://github.com/iovisor/gobpf)。

![img{512x368}](../../assets/7ee82ab990664bc6.png)


这个程序看起来和Python中的程序完全一样。一开始，它有一个字符串，其中的BPF程序是用C语言编写的，然后我们沟通在哪里附加一个给定的程序，我们用某种方式和它进行交互，比如从BPF图中提取数据。

基本上就是这样了。更详细的例子可以在[Github上查看](https://github.com/iovisor/gobpf/tree/master/examples/bcc/bash_readline)。

主要的缺点可能是我们使用的是C库，libbcc或者libbpf，用C库构建一个Go程序远不是一件容易的”事”。

除了iovisor/gobpf之外，我还发现了另外三个最新的项目，可以让你在Go中写出用户层(userland)部分。

- https://github.com/dropbox/goebpf
- https://github.com/cilium/ebpf
- https://github.com/andrewkroh/go-ebpf

Dropbox的版本不需要任何C库，但你需要自己用Clang构建BPF的内核部分，然后用Go程序将其加载到内核中。

Cilium的版本和Dropbox的版本有相同的具体内容。但值得一提的是，最主要的原因是它是由Cilium项目的人做的，这意味着它成功性更大。

第三个项目我出于完整性的考虑而列出了。和前面两个项目一样，它没有外部的C语言依赖，需要用C语言手动构建BPF程序，但看起来，未来的前景不是特别乐观。

其实，我们还应该问一个问题：到底为什么要用Go写BPF程序？因为如果你看BCC或者bpftrace，那么bPF程序占用的代码不到500行。但如果用bpftrace语言写一个小脚本，或者用一点Python，不是更简单吗？我看有两个理由要这么做。

第一个原因是这样的。你确实很喜欢Go，而且更愿意用Go来做所有事情(译注：拿着go这柄锤子，眼中到处都是钉子)。此外，把Go程序从机器迁移到机器上可能更简单：静态链接，简单的二进制，以及所有这些。但事情远没有这么简单，因为我们被绑在一个特定的内核上。我就不说了，否则，我的文章又要长50页了。

第二个原因是这样的。你写的不是一个简单的脚本，而是一个大规模的系统，这个系统内部也使用了BPF。我在Go中甚至有这样一个系统的例子。

![img{512x368}](../../assets/16e58581fdb30c18.png)


Scope项目看起来像一个二进制程序，当它在K8s或其他云的基础设施中运行时，会分析发生的一切，并显示有哪些容器和服务，它们是如何交互的等等。而很多这些都是用BPF完成的。一个有趣的项目。

## 用Go分析程序

如果你还记得，我们还有一个问题：我们能不能用BPF分析用Go编写的程序？我们的第一反应是：”可以，当然可以！” 程序用什么语言编写有什么区别呢？毕竟，它只是编译后的代码，和其他程序一样，在处理器中计算一些东西，疯狂地占用内存，并通过内核与硬件交互，通过系统调用与内核交互。原则上这是正确的，但也有一些细节–这些细节有不同程度的复杂性。

### 传递参数

其中一个细节是，Go不使用大多数其他语言所使用的ABI(application binary interface)。它的工作方式是，”创始人”决定从[Plan 9系统](https://en.wikipedia.org/wiki/Plan_9_from_Bell_Labs)中提取ABI，这是一个他们非常熟悉的系统。

ABI和API一样，是一种接口约定–只是在比特、字节和机器代码的层面上。

我们对ABI的主要内容感兴趣的是它的参数是如何传递给函数的，以及响应是如何从函数中回来的。如果说在标准的ABI x86-64中，处理器的寄存器是用来传递参数和响应的，而在Plan 9 ABI中，堆栈是则是用来实现这个目的的。

Rob Pike和他的团队并没有打算做另一个标准；他们已经为Plan 9系统准备了一个几乎是现成的C编译器–就像2 x 2一样简单–在很短的准备时间内，他们将其改造成了Go的编译器。这就是一个工程师的方法。

然而，实际上这并不是一个如此关键的问题。首先，我们可能很快就会[在Go中看到通过寄存器传递参数](https://github.com/golang/go/issues/18597)，其次，从BPF中获取堆栈参数并不复杂：[sargX别名](https://github.com/iovisor/bpftrace/pull/828)已经被添加到bpftrace中，而[另一个别名](https://github.com/iovisor/bcc/issues/934)很可能在不久的将来出现在BCC中。

更新：自从我做了演讲之后，Go官方甚至还出了一个[关于在ABI中使用寄存器的详细技术草案](https://go.googlesource.com/proposal/+/refs/changes/78/248178/1/design/40724-register-calling.md)。

### 唯一的线程标识符

第二个则是与Go的一个被钟爱的功能有关，即goroutines。测量函数延迟的方法之一是保存函数被调用的时间，得到函数的退出时间，并计算其差值。我们需要保存函数的启动时间以及一个键，这这个键将包含函数的名称和TID（线程ID）。线程ID是需要的，因为同一个函数可以被不同的程序，或者一个程序的不同线程同时调用。

![img{512x368}](../../assets/5fa4a838472f5a93.png)


但是，在Go中，goroutine在系统线程之间移动：前一分钟，一个goroutine在一个线程上执行，后一分钟，在另一个线程上执行。而且，在Go的情况下，我们最好不要将TID放入键中，而是放入GID，即goroutine的ID–但不幸的是，我们无法获得它。从纯技术的角度来看，这个ID确实存在。你甚至可以用肮脏的黑客手段来提取它，因为它可以在堆栈的某个地方被找到，但这样做是被Go核心团队建议严格禁止的。他们认为这是我们永远不会需要的信息。goroutine本地存储也是如此–但这有点跑题了。

### 扩展栈

第三个问题是最严重的问题。它是如此严重，以至于即使我们以某种方式解决了第二个问题，也无法帮助我们测量Go函数的延迟。

大多数读者可能对什么是栈有了很好的理解。这也就是栈，与堆不同，你可以为变量分配内存，而不必考虑释放它们。

但是对于C语言来说，在这种情况下，栈有一个固定的大小。如果我们超过了这个固定大小，就会出现众所周知的堆栈溢出现象。

但在Go中，栈是动态的。在旧版本中，它是通过链接的内存块列表来实现的(即分段栈)。现在，它是一个动态大小的连续块。这意味着，如果分配的内存块对我们来说不够用，我们就扩展当前的内存块。而如果我们不能扩展它，我们就分配一个更大的，并将所有数据从旧的位置移动到新的位置。这一点非常吸引人，并且涉及到安全保证、cgo和垃圾收集等问题，但这是另一篇文章的主题。

要知道，为了让Go能够移动堆栈，它必须处理调用栈，并且处理栈中的所有指针。

而这就是基本的问题所在：uretprobes，用于将bPF探针附加到函数返回中，动态地改变堆栈以整合对其处理程序的调用–这就是所谓的 “蹦床(trampoline)”。而且，在大多数情况下，这改变了栈，这是Go不期望发生的事情，它会导致程序崩溃。糟了!

![img{512x368}](../../assets/0a3eb1d6bab4c76a.png)


顺便说一下，这个故事不是Go独有的。C++的堆栈拆分器在处理异常时也每每崩溃。

这个问题没有解决办法。在这种情况下，像往常一样，双方各自向对方抛出完全有理有据的论点进行指责。

但是，如果你真的需要设置uretprobe，有一个方法可以绕过这个问题。怎么解决？不要设置uretprobe探针。你可以在我们退出函数的所有位置设置一个uprobe。可能有一个这样的位置–或者50个。

![img{512x368}](../../assets/1b4ad868888ba21e.png)


而这也是Go的独特性在我们手中发挥的地方。

通常情况下，这种诡计是行不通的。一个足够聪明的编译器知道如何执行所谓的尾部调用优化，这时，我们不是从函数中返回，而是简单地跳到下一个函数的开始处。这种优化对于Haskell这样的函数式语言来说是至关重要的。如果没有它，你就无法在不发生堆栈溢出的情况下寸步难行。但是，有了这种优化，根本不可能找到我们从函数返回的所有位置。

但具体来说，Go 1.14版本的编译器，还不能进行尾部调用优化。这就意味着，附加到函数的所有显式退出的技巧是可行的，即使它非常笨重。

## 示例

不要认为BPF对Go无用。远非如此。我们可以做所有不涉及上述问题的其他事情。而且我们会这样做的。

让我们来看一些例子。

首先，我们来看一个简单的程序。基本上，它是一个监听8080端口的web服务器，并且有一个HTTP查询的处理程序。处理程序从URL中获取一个名称参数和一个年份参数，进行检查，然后将这三个变量（名称、年份和检查状态）发送给prepareAnswer()函数，然后该函数以字符串的形式准备一个答案。

![img{512x368}](../../assets/381a5db0cb44e3b7.png)


Site check是一个HTTP查询，在通道和goroutines的帮助下，检查会议站点是否工作。prepareAnswer函数只是将所有这些转化为一个可读的字符串。

我们将通过curl的简单查询来触发我们的程序：

![img{512x368}](../../assets/8b802ba83448778c.png)


对于我们的第一个例子，我们将使用 bpftrace 打印所有程序的函数调用。在本例中，我们将对 “main “下的所有函数进行附加。在Go中，所有的函数都有一个符号，其形式如下：包名-点-函数名。我们的包是’main’，函数的运行时是’runtime’。

![img{512x368}](../../assets/46d66946c714cf1e.png)


当我使用curl时，处理程序(handler)、site检查函数和goroutine子函数都会被执行，然后是准备答案函数(prepareAnswer)。很好！

接下来，我不仅要导出那些正在执行的函数，还要导出它们的参数。让我们以函数prepareAnswer()为例，它有三个参数。让我们试着打印两个ints。

让我们拿bpftrace来说，只不过这次不是单行代码，而是一个脚本。让我们将其附在我们的函数上，让我们像我说的那样，为堆栈参数使用别名。

在输出中，我们看到，我们发送了2020，获得了状态200，还发送了一次2021。

![img{512x368}](../../assets/95fa3749da0e719b.png)


但这个函数有三个参数。第一个参数是一个字符串。那么这个参数呢？

我们简单的导出0到3的所有堆栈参数，我们看看会看到什么？一个大数字，一个稍小的数字，还有我们以前的数字2021和200。一开始这些奇怪的数字是什么？

![img{512x368}](../../assets/27a7226e7a858099.png)


这时，熟悉Go的内部结构是很有帮助的。如果说在C语言中，字符串只是一个以零结尾的字节数组，那么在Go语言中，字符串实际是一个结构体，由一个指向字节数组的指针（顺便说一下，这个指针不是以零结尾）和长度组成。

![img{512x368}](../../assets/c893dcfcaf7224ac.png)


但是Go编译器在以参数的形式发送一个字符串时，会将这个结构解开，作为两个参数发送。于是，第一个奇怪的数字确实是我们数组的指针，第二个是长度。

果然：预期的字符串长度是22。

相应地，我们修正一下我们的脚本，以便通过堆栈指针寄存器获得这两个值，以及正确的偏移量，并且，在集成的str()函数的帮助下，我们将其导出为一个字符串。这一切都成功了。

![img{512x368}](../../assets/f2655ae1ad96c51e.png)


我们也来看看运行时(runtime)的情况。例如，我想知道我们的程序启动了哪些goroutines。我知道goroutines是由函数newproc()和newproc1()启动的。我们来附着(attach)一下它们。funcval结构的指针是newproc1()函数的第一个参数。这个只有一个字段，就是函数的指针。

![img{512x368}](../../assets/f9784b7aad48e74f.png)


在这种情况下，我们将使用直接在脚本中定义结构的功能。这比使用偏移量要简单一些。我们已经导出了所有的goroutine，当我们的处理程序被调用时，这些goroutine就会启动。之后，如果我们想获取偏移量的符号名称，那么我们就可以在其中看到我们的checkSite函数。万岁!

![img{512x368}](../../assets/47b07ce4e9b6ae0e.png)


这些例子对于BPF、BCC和bpftrace的功能来说只是沧海一粟。只要对内部工作原理有足够的了解和经验，您就可以从工作程序中获得几乎任何信息，而无需停止或改变它。

## 结论

这就是我想告诉你的全部内容，希望对你有所启发。

BPF是Linux中最时髦、最有前途的领域之一。而且我相信，在未来的几年里，我们会看到更多有趣的东西–不仅是技术本身，还有工具和它的传播。

现在还不算太晚，也不是每个人都知道BPF，所以赶快去学习，成为魔术师，解决问题，帮助你的同事。都说魔术师的招数只有一次。

说到Go，照例，我们的结局很独特。我们总是有一些怪癖，无论是不同的编译器，还是ABI，需要GOPATH，有一个你无法谷歌的名字。但我认为，可以说我们（Go)已经成为一股不可忽视的力量，在我看来，情况只会越来越好。

## 附录（译者添加，原文没有此节)

### 在ubuntu 18.04上安装bpftrace

ubuntu 19.04及以后版本可以直接通过下面命令安装bpftrace：

```
(sudo) apt-get install -y bpftrace
```


但18.04版本的apt官方源中并没有bpftrace。但snap中有：

```
# snap install --devmode bpftrace
2020-12-17T17:21:24+08:00 INFO Waiting for automatic snapd restart...
bpftrace 20201207-1718-v0.11.4 from Colin King (cking-kernel-tools) installed
# snap connect bpftrace:system-trace
# which bpftrace
/snap/bin/bpftrace
Build
version: v0.11.4
LLVM: 7
foreach_sym: no
unsafe uprobe: no
bfd: yes
bpf_attach_kfunc: no
bcc_usdt_addsem: no
bcc bpf_attach_uprobe refcount: no
libbpf: no
libbpf btf dump: no
libbpf btf dump type decl: no
Kernel helpers
probe_read: yes
probe_read_str: yes
probe_read_user: yes
probe_read_user_str: yes
probe_read_kernel: yes
probe_read_kernel_str: yes
get_current_cgroup_id: yes
send_signal: yes
override_return: yes
Kernel features
Instruction limit: -1
Loop support: no
btf: no
Map types
hash: yes
percpu hash: yes
array: yes
percpu array: yes
stack_trace: yes
perf_event_array: yes
Probe types
kprobe: no
tracepoint: yes
perf_event: yes
kfunc: no
```


但通过snap安装的bpftrace有缺陷：

```
# bpftrace -e 'uprobe:/root/test/go/goebpf/testprogram:main.* { printf("%s - %s\n", comm, func); }'
sh: 1: objdump: not found
No probes to attach
```


这个问题在https://github.com/iovisor/bpftrace/issues/1430中有解决方法，那就是从bpftrace官方提供的docker镜像中将无缺陷的bpftrace拷贝出来：

```
# docker pull quay.io/iovisor/bpftrace:master-vanilla_llvm_clang_glibc2.27
master-vanilla_llvm_clang_glibc2.27: Pulling from iovisor/bpftrace
da7391352a9b: Pull complete
14428a6d4bcd: Pull complete
2c2d948710f2: Pull complete
8aeae4c5f345: Pull complete
e3b704c358bf: Pull complete
Digest: sha256:77ded0c887c91a431a1ebe508944eae0ed0fab9c51fc2867146c9b4b347becc7
Status: Downloaded newer image for quay.io/iovisor/bpftrace:master-vanilla_llvm_clang_glibc2.27
quay.io/iovisor/bpftrace:master-vanilla_llvm_clang_glibc2.27
# docker run -v $(pwd):/output quay.io/iovisor/bpftrace:master-vanilla_llvm_clang_glibc2.27 /bin/bash -c "cp /usr/bin/bpftrace /output"
# mv bpftrace /snap/bin <--- 覆盖掉原snap安装的bpftrace
# bpftrace -e 'uprobe:/root/test/go/goebpf/testprogram:main.* { printf("%s - %s\n", comm, func); }'
Attaching 5 probes...
```


### 文中一些go文件的源码

```
// testprogram.go
package main
import (
"fmt"
"log"
"net/http"
"strconv"
)
func main() {
http.HandleFunc("/", handler)
if err := http.ListenAndServe(":8080", nil); err != nil {
panic(err)
}
}
func handler(writer http.ResponseWriter, request *http.Request) {
query := request.URL.Query()
name := query.Get("name")
year_, _ := strconv.ParseUint(query.Get("year"), 10, 32)
year := int(year_)
status := checkSite()
answer := prepareAnswer(name, year, status)
writer.Write([]byte(answer + "\n"))
return
}
//go:noinline
func checkSite() int {
resultChan := make(chan int)
go func() {
resp, err := http.Get("https://www.gophercon-russia.ru")
if err != nil {
log.Fatalf("http get failed: %s\n", err)
}
resultChan <- resp.StatusCode
}()
return <-resultChan
}
//go:noinline
func prepareAnswer(name string, year int, status int) string {
answer := fmt.Sprintf("Hello, %s %d! Website returned status %d.", name, year, status)
return answer
}
```


myscript3.bt：

```
# cat myscript3.bt
uprobe:/root/test/go/goebpf/testprogram:main.prepareAnswer {
$length = reg("sp")+16;
$array = reg("sp")+8;
printf("%s - %s %d %d\n", func, str(*($array), $length), sarg2, sarg3);
}
```


**“Gopher部落”知识星球开球了！**高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


我的Go技术专栏：“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”上线了，欢迎大家订阅学习！

![img{512x368}](../../assets/018ff45f7e150fca.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2020, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论