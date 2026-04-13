---
title: Go编程语言与环境：万字长文复盘导致Go语言成功的那些设计决策[译]
url: https://tonybai.com/2022/05/04/the-paper-of-go-programming-language-and-environment/
published: '2022-05-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go编程语言与环境：万字长文复盘导致Go语言成功的那些设计决策[译]

![](../../assets/ba3f9f4282cd352d.png)


[本文永久链接](https://tonybai.com/2022/05/04/the-paper-of-go-programming-language-and-environment) – https://tonybai.com/2022/05/04/the-paper-of-go-programming-language-and-environment

[美国计算机学会通讯(Communications of the ACM)](https://cacm.acm.org/)期刊2022年5月第65卷第5期将发表一篇有关Go语言的综述类Paper：[《Go编程语言与环境》](https://cacm.acm.org//magazines/2022/5/260357-the-go-programming-language-and-environment/fulltext)，这类综述类文章只有资深的Go核心团队的人才“有资格”写，该文的作者列表印证了这一点，他们是Russ Cox，Robert Griesemer，Rob Pike，Ian Lance Taylor和Ken Thompson，都是Go语言核心团队耳闻能详的人物。

这篇文章是**Go核心团队对10多年来Go演化发展的复盘**，深入分析了那些对Go的成功最具决定性的设计哲学与决策，个人觉得这是Go诞生十多年来最重要的一篇文章。所以我建议Gopher们都能认真读一遍或几遍这篇文章。这里将其翻译为中文，方便大家enjoy it。

原文pdf版在[这里](https://cacm.acm.org/magazines/2022/5/260357-the-go-programming-language-and-environment/pdf)可以下载。

Go是一种编程语言，于2007年底在Google(谷歌)创建，并在2009年11月作为以开放源代码形式发布。从那时起，它就一直被作为一个公共项目运作，有成千上万的个人和几十家公司为Go项目做出过贡献。Go已经成为构建云计算基础设施的一种流行语言。

[Docker（一种Linux容器管理器）]和[Kubernetes（一种容器部署系统）]都是用Go编写的核心云技术。今天，Go是每个主要的云供应商的关键基础设施的基础，[云原生计算基金会(CNCF)]托管孵化的大多数项目都是Go语言实现的。

![](../../assets/782e57755187cfdc.png)


### 主要见解(key insights)

- Go语言尽管没有什么技术上的突出进步，但却有着广泛的应用。并且，Go的成功在于专注于工程软件项目的整体环境。
- Go的做法是不会将语言特性视为比环境特性更重要，例如：谨慎处理依赖关系(译注：尤指最小版本选择MVS)、可规模化(scale)的开发和生产、默认安全的程序、工具辅助的测试和开发、对自动化修改的适应性以及
[长期保证的兼容性](https://go.dev/doc/go1compat)。 [Go 1.18于2022年3月发布](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)，增加了十年来第一个重要的新语言特性：参数化多态性，经裁剪后可以很好地适应Go语言的其他部分(译注：仍然可以保持向后兼容，满足Go1兼容性承诺)。

![](../../assets/4200808010001eca.png)


### 引子

**早期用户被Go所吸引的原因有很多**。首先，一种支持[垃圾回收](https://tonybai.com/2020/03/10/visualizing-memory-management-in-golang/)、静态编译的系统级编程语言，其本身就是不寻常的。其次，Go对[并发(concurrency)和并行(parallelism)](https://tonybai.com/2015/06/23/concurrency-and-parallelism/)的原生支持有助于利用当时正在成为主流的多核机器的优势。再次，自包含的二进制文件(译注：无需依赖目标主机上的C运行库和其他系统库)和简单的[交叉编译](https://tonybai.com/2014/10/20/cross-compilation-with-golang/)简化了部署。最后，[谷歌的名字无疑也是一个亮点](https://tonybai.com/2012/10/08/the-new-age-of-programming-language/)。

但为什么用户会留存下来呢？为什么Go可以越来越流行、越来越受欢迎而同期的其他语言项目却没有呢？我们相信，语言本身只是答案的一小部分。**完整的故事(答案)必须涉及整个Go环境：库、工具、惯例和针对软件工程的整体做法**，它们都对使用Go语言编程提供了支持。我们在语言设计中做出的最重要的决定，就是使Go更适合大规模软件工程，并帮助我们吸引志同道合的开发者。

在这篇文章中，我们研究了我们认为对Go的成功最具决定性的那些设计决策，探讨了它们不仅适用于语言，而且适用于更广泛的环境的原因。然而，要分离并量化出某个具体设计决策的贡献度是很困难的，所以这篇文章不应该被理解为科学分析，而应该被理解为**基于Go过去十年的经验和用户反馈的最佳理解的呈现**。

### 起源(Origins)

**Go是在Google建立大规模分布式系统的经验中产生的**，在一个由成千上万的软件工程师共享的大型代码库中工作。我们希望为这种环境设计的语言和工具能够解决公司和整个行业所面临的挑战。由于开发工作和正在部署的生产系统的规模都很大，挑战因此出现了!

#### 开发规模(Development scale)

在开发方面，谷歌在2007年有大约4000名活跃的用户在一个单一的、共享的、多语言（C++、Java、Python）的代码库中工作。单一的代码库使问题很容易修复，例如，使主网络服务器变慢的内存分配器中的问题。但是在开发一个库的时候，由于很难找到一个包的所有依赖关系，所以很容易在不知不觉中破坏了这个库的一个以前未知的用户。

另外，在我们使用的现有语言中，导入一个库可能导致编译器递归加载所有导入的库。在2007年的一次C++编译中，我们观察到编译器（在#include预处理后）在编译一组总共4.2MB的文件时，居然读取了超过8GB的数据，在一个已经很大的程序上，扩展系数几乎达到2000。如果为编译一个给定的源文件而读取的头文件的数量随着源代码树线性增长，那么整个源树的编译成本就会呈现指数级增长。

为了弥补速度的减慢，我们开始研究一个新的、大规模并行和可缓存的编译系统，它最终成为开源的Bazel编译系统。但是并行性和缓存对于修复低效的系统只能起到这么大的作用了，我们相信语言本身可以做更多的事情来为编译大型程序提供帮助。

#### 生产规模(Production scale)

在生产方面，谷歌正在运行非常大的系统。例如，2005年3月，一个1500颗CPU的Sawzall日志分析系统集群处理了2.8PB的数据。2006年8月，谷歌的388个大表服务集群由24500个独立的tablet服务器组成，其中一组8069个服务器每秒处理了120万个请求。

然而，谷歌和业界其他公司一样，都在努力编写高效的程序，以充分利用多核系统的优势。我们的许多系统不得不在一台机器上运行同一个二进制文件的多个副本，因为现有的多线程支持既笨重又低性能。庞大的、固定大小的线程栈，重量级的栈开关，以及用于创建新线程和管理它们之间交互的笨拙语法，都使得使用多核系统变得更加困难。但很明显，服务器中的cpu核数量只会越来越多。

在这里，我们也相信语言本身可以通过提供轻量级的、易于使用的并发性原语来提供帮助。我们还在这些额外的cpu核中看到了一个机会：垃圾收集器可以在一个专用的核上与主程序并行运行，减少其延迟成本。

为应对这些挑战而设计的编程语言可能是什么样子的呢？Go就是我们针对这一问题的回答。Go之所以受欢迎，部分原因无疑是整个科技行业现在每天都面临这些挑战。云计算供应商使最小的公司也有可能进行非常大的生产部署。虽然大多数公司没有成千上万的员工在写代码，但现在几乎所有的公司都依赖于由成千上万的程序员贡献的大量开源基础设施。

本文的后续部分将研究具体的设计决策是如何解决这些开发和生产的规模化问题的。我们从语言核心本身开始，向外扩展到周围的环境。**我们并不试图对该语言进行完整的介绍**。要想全面详细了解Go语言，请参见[Go语言规范](https://go.dev/ref/spec)或[《Go程序设计语言》](http://www.gopl.io)等书籍。

### 包(Packages)

一个Go程序是由一个或多个可导入的包组成的，每个包包含一个或多个文件。图1中的网络服务器说明了关于Go的包系统设计的许多重要细节。

![](../../assets/e78949b7cadbedd4.png)



该程序启动了一个本地网络服务器（第9行），它通过调用hello函数来处理每个请求，hello函数用消息”hello, world”（第14行）作为响应。

一个包使用显式的import语句导入另一个包（第3-6行），这与许多语言一样，但与C++的#include机制相反。不过，与大多数语言不同的是，Go安排每个导入语句只读取一个文件(译注：仅会读取依赖包对应的.a文件，以fmt为例，读取的是fmt.a)。例如，fmt包的公共API引用了io包的类型：fmt.Fprintf的第一个参数是io.Writer类型的接口值。在大多数语言中，编译器处理fmt包的导入时，也都会加载所有io的符号来满足fmt包的需要，这可能又需要加载额外的包来满足所有io包中符号的需要。依此类推，一条导入语句可能最终要加载并处理几十个甚至几百个包。

Go通过采用与Modula-2语言类似的做法，即：使编译后的fmt包的元数据包含了了解其自身依赖关系所需的一切，例如io.Writer的定义，从而避免了上述这种问题。因此，编译import “fmt”语句时只需读取一个完全描述fmt及其依赖关系的文件(译注：这个文件指fmt.a)。 此外，这种“扁平化”处理是在编译fmt包时一次完成的，避免了每次导入时的多次加载。这种方法使编译器的工作更少，构建速度更快，有助于大规模开发。同时，包的导入循环是不允许的：**即如果fmt包导入了io包，那么io包就不能导入fmt包，也不能导入任何其他导入fmt的包，即使是间接的导入**。这也使得编译器工作进一步减少，保证了一个特定的构建可以被分割为多个单独的包的编译。这也使得增量程序分析成为可能，我们甚至可以在运行测试之前就运行这种分析来捕捉错误。

一个包导入fmt包并不能使io.Writer这个名字对当前这个包可用。如果main包想使用io.Writer这个类型，它必须自己使用import “io”语句导入io包。因此，一旦所有使用fmt限定名称的引用被从源文件中删除– 例如，如果上面例子中fmt.Fprintf的调用被删除，import “fmt”语句就可以安全地从源文件中删除，而无需做进一步分析。这个属性使得自动管理源代码中的导入语句成为可能。事实上，Go不允许未使用的导入，以避免将未使用的代码链接到程序中而产生的可执行文件膨胀。

导入路径是带引号的字符串字面值，这使其解释具有灵活性。一个斜线分隔的路径在import语句中标识了导入的包，但随后源代码使用包声明语句中声明的短标识符来引用包。例如，import “net/http”提供了包的路径，但我们却使用其顶层名称http对其内容进行访问。在标准库之外，包由以域名开头的类似URL的路径来识别，如import “github.com/google/uuid”。我们将在后面对这类包进行更多的介绍。

关于包的最后一个细节，请大家注意fmt.Fprintf和io.Writer这两个名字中的大写字母。Go使用一种**命名惯例**来对C++和Java的public、private和protected概念和关键字进行模拟。首字母为大写字母的名字，如Printf和Writer，是”导出的”（公共的），其他的则不是。基于首字母大小写的、编译器强制执行的导出规则适用于常量、函数和类型等包级标识符；以及方法名和结构字字段名。我们采用这一规则是为了避免在公共API中涉及的每一个标识符旁边都写上一个像export这样的关键字的语法负担。 随着时间的推移，我们已经开始看重这种可以查看标识符是否在包之外可用或仅在内部使用的能力。

### 类型(Types)

Go提供了一套常见的基本类型：布尔(bool)，定长整型，如uint8和int32，非定长整型int和uint（32或64位，取决于机器大小），以及定长浮点类型(float32和float64)和复数类型(complex64和complex128)。Go还类似C语言那样提供了指针、固定大小的数组和结构体类型。Go还提供了一个内置的字符串类型(string)，一个被称为map类型的哈希表，以及称为slice类型的动态大小的数组。大多数Go程序都依赖于这些类型，Go没有其他特殊的容器类型了。

Go没有提供类(class)，但允许将方法(method)绑定到任何类型上，包括结构体、数组、切片、map，甚至是基本类型，如整型。它没有类型层次体系；我们认为继承性往往会使程序在演化过程中更难适应。相反，**Go鼓励类型的组合**。

![](../../assets/f2b4b01b514af5fe.png)


Go通过其接口类型提供面向对象的多态性。就像Java接口或C++的抽象虚拟类一样，Go的接口包含一个方法名称和签名的列表。例如，前面提到的io.Writer接口在io包中的定义如图2所示：

![](../../assets/216a83e74cdce6ea.png)



Write方法接受一个字节切片，并返回一个整数和可能的错误。与Java和C++不同的是，任何Go类型如果拥有与某个接口相同名称和签名的方法集合，就被认为是实现了该接口，而无需额外的显式声明。例如，os.File类型有一个签名相同的Write方法，因此它实现了io.Writer，而没有使用像Java的”implements”进行显式指示。

避免接口和实现之间的显式关联，允许Go程序员定义小型、灵活以及临时性的接口，而不是将它们作为复杂类型层次结构的基础构件。**它鼓励捕捉开发过程中出现的关系和操作，而不是需要提前计划和定义它们**。这对大型程序尤其有帮助，因为在刚开始开发时，最终的结构是很难看清楚的。去除声明实现的簿记，鼓励使用精确的、只有一种或两种方法的接口，如Writer、Reader、Stringer（类似于Java的toString方法）等，这些接口在标准库中被广泛应用。

初次学习Go的开发者常常担心一个类型会意外地实现一个接口。虽然很容易建立起这样的假设，但在实践中，不太可能为两个不兼容的操作选择相同的名称和签名，而且我们从未在实际的Go程序中看到这种情况发生。

### 并发(Concurrency)

当我们开始设计Go语言的时候，多核计算机已经开始广泛使用，但线程在所有流行的语言和操作系统中仍然是一个重量级的概念。创建、使用和管理线程的难度使其不受欢迎，这限制了对多核CPU能力的充分利用。**解决这一矛盾是创建Go的主要动机之一**。

Go语言中原生包含了多个并发控制线程的概念，称为**goroutines**。goroutines在一个共享地址空间中运行，并能被有效地通过多路复用机制调度到操作系统线程上。对阻塞操作的调用，如从文件或网络中读取数据，只阻塞进行该操作的goroutine；该线程上的其他goroutine可能被移到另一个线程中，这样它们就可以在调用者被阻塞时继续执行。goroutine开始时只有几千字节的堆栈(译注：在Linux x86-64上默认是2KB)，它可以根据需要自动调整大小，而无需程序员参与。开发人员在设计程序结构时将Goroutines视作一种丰富的、廉价的原语。对于一个服务器程序来说，拥有数千甚至数百万个goroutines是很平常的，因为它们的使用成本比线程低得多。

例如，net.Listener是一个带有Accept方法的接口，可以监听并返回客户端新发起的网络连接。图3显示了一个接受连接的函数listen，并为每个连接启动一个新的goroutine来运行服务函数。

![](../../assets/55688ad03a43e36a.png)



listen函数主体中的无限for循环（第22-28行）中调用了listener.Accept方法，它返回两个值：连接和一个可能的错误。假设没有错误发生，go语句（第27行）在一个新的goroutine中启动其参数：一个函数调用serve(conn)，这类似于Unix shell命令的后缀&，但在同一个操作系统进程中。要调用的函数及其参数在原goroutine中被求值；这些值被复制以创建新goroutine的初始栈帧。因此，程序为每个新发起的网络连接运行一个独立的serve函数实例。每个serve的调用处理一个给定连接上的所有请求（第37行对handle(req)的调用没有以go为前缀）；每次serve调用都可以阻塞而不影响对其他网络连接的处理。

在Go的内部，Go的实现使用了有效的多路复用操作，比如Linux的epoll，来处理并发的I/O操作，但用户看不到。Go的运行时库**对用户呈现的是阻塞式I/O的抽象**，其中每个goroutine都是顺序执行的，不需要回调，这很容易理解。

在创建了多个goroutine之后，一个程序必须经常在它们之间进行协调。Go提供了**channel原语**，允许goroutine之间进行通信和同步：channel是一个单向的、大小有限的管道，在goroutine之间传输类型化的信息。Go还提供了一个多路选择原语**select**，可以根据某channel上的通信是否可进行来控制执行。这些想法来自Hoare的”通信顺序过程(Communicating Sequential Processes)”和早期的语言实验，特别是Newsqueak、Alef和Limbo。

图4显示了另一个版本的listen，它是为了限制任何时候可处理的连接数量而写的。

![](../../assets/604e775bbc96d4bd.png)



这个版本的listen首先创建了一个名为ch的channel（第42行），然后启动了一个由10个服务端goroutines组成的池（第44-46行），它们接收来自这个单一channel的连接。当新的连接被接受时，listen使用发送语句ch <- conn（第53行）在ch上发送每个连接。一个server执行接收表达式<- ch（第59行）完成了此次channel通信。这里创建的是无缓冲channel(Go默认如此)，ch没有空间来缓冲正在发送的值，所以在10个server忙完前10个连接后，第11个ch <-conn将被阻塞，直到一个server完成对serve函数的调用并执行新的接收。被阻塞的通信操作对Listener产生了隐性的压力，这回阻止Listener接受新的连接，直到前一个连接被处理完。

请注意，这些程序中没有互斥或其他传统的同步机制。在channel上进行的数据值通信可以作为同步的一部分；按照惯例，在channel上发送数据会将所有权从发送方传给接收方。Go有提供互斥、条件变量、信号量和原子操作的库，供低级别互斥或同步使用，但channel往往是更好的选择。根据我们的经验，人们对消息传递–利用通信在goroutine之间转移所有权–的理解比对互斥和条件变量的理解更容易、更正确。早期流行的一句Go箴言是：”**不要通过共享内存来通信，而是通过通信来共享内存**“。

Go的垃圾收集器大大简化了并发API的设计，消除了关于哪个goroutine负责释放共享数据的问题。与大多数语言一样（但与Rust不同），可变数据的所有权不由类型系统静态跟踪。相反，Go集成了TSAN(ThreadSanitizer)，为测试和受限的生产使用提供了一个动态竞态检测器。

### 安全性(Security和Safety)

任何新语言诞生的部分原因都是为了解决以前语言的缺陷，对Go来说，这还包括影响网络软件安全的安全问题。Go删除了在C和C++程序中造成许多安全问题的未定义行为。整数类型不会自动相互强制转型。空指针解引用、越界的数组和切片索引会导致运行时异常。不存在进入栈帧的空悬指针。任何可能超出其栈帧范围的变量，例如在闭包中捕获的变量，将被移到堆中。在堆中也没有空悬的指针；使用垃圾收集器而不是手动内存管理可以消除使用后的错误。当然，Go并没有解决所有问题，有些东西被遗漏了，也许应该被解决。例如，整数溢出本可以被定义为运行时错误，而不是定义为绕过不处理。

由于Go是一种系统级编程的语言(译注：Go最初被设计者们定位为一种系统级编程语言)，它可能需要破坏类型安全的机器级操作，因此它能够将指针从一种类型强制转换为另一种类型，并进行地址运算，但只能通过使用unsafe包及其受限制的特殊类型unsafe.Pointer。必须注意这种对类型系统的违反要与垃圾收集器保持兼容–例如，垃圾收集器必须始终能够识别一个特定的字(word)是一个整数还是一个指针。在实践中，unsafe包很少出现：安全Go是相当有效的。因此，看到import “unsafe”是一个信号，让我们更仔细地检查源文件是否存在安全问题。

Go的安全属性(safety properties)使它比C或C++等语言更适合于编写加密和其他安全关键的代码。一个微不足道的错误，例如一个越界的数组索引，在C和C++中可能会导致敏感数据的泄露或远程执行，但在Go中会引起运行时异常，从而停止程序，大大限制了潜在的影响。Go中有一整套密码学库，包括对SSL/TLS的支持；Go标准库包括一个可用于生产的HTTPS客户端和服务器。事实上，Go的安全性、性能和高质量库的结合使其成为现代安全工作的热门试验场。例如，免费提供的证书授权机构Let’s Encrypt依靠Go来提供生产服务，并在最近跨越了一个里程碑，签发了10亿份证书。

### 完整性(Completeness)

Go在语言、库和工具层面上提供了现代开发所需的核心部分。这就需要小心翼翼地平衡，既要增加足够多的”开箱即用”的功能，又不能增加太多，以至于我们自己的开发过程因为要支持太多的功能而陷入困境。

Go语言提供了内置的字符串、hash map和动态大小的数组等易于使用的数据类型。如前面所述，这些对于大多数Go程序来说已经足够了。其结果是Go程序之间有了更大的互操作性–例如，没有产生竞争性的字符串或hash map的实现来分裂包的生态系统。Go包含的goroutines和channel是另一种形式的完整性。这些功能提供了现代网络程序中所需要的核心并发功能。Go直接在语言中提供这些功能，而不是在库中提供，这样可以更容易地调整语法、语义和实现，使其尽可能地轻量和易于使用，同时为所有用户提供统一的方法。

Go标准库包括一个生产就绪的HTTPS客户端和服务器。对于在互联网上与其他机器互动的程序来说，这一点至关重要。直接满足这一需求可以避免额外的碎片化。我们已经看到了io.Writer接口；任何输出数据流都按惯例实现了这个接口，并与所有其他I/O适配器进行互操作。图1中的ListenAndServe调用可作为另一个例子，它期望有一个http.Handler类型作为第二个参数，其定义如下图5所示。参数http.HandlerFunc(hello)通过调用hello实现了Handler的ServeHTTP方法。该库创建了一个新的goroutine来处理每个连接，就像本文”并发”部分中的Listener例子一样，所以handler可以用简单的阻塞风格来编写，服务器可以自动扩展以同时处理许多连接。

![](../../assets/e1dfe6931687f53f.png)



http包还提供了一个基本的分派器(dispatcher)，它本身就是Handler的另一个实现，它允许为不同的URL路径注册不同的handler。将Handler类型确立为约定俗成的接口，使得许多不同类型的HTTP服务器中间件(middleware)能够被创建并相互操作。我们不需要将所有这些实现添加到标准库中，但我们确实需要建立一个允许它们一起工作的接口。

标准Go发行版还提供了对交叉编译、测试、性能剖析(profiling)、代码覆盖率、[模糊测试](https://tonybai.com/2021/12/01/first-class-fuzzing-in-go-1-18)等的集成支持。测试是另一个领域，在这个领域中，建立关于核心概念的协议–例如什么是测试用例以及如何运行–使得创建的自定义测试库和测试执行环境都能很好地互操作。

### 一致性(Consistency)

我们对Go的一个目标是**让它在不同的实现、执行环境中，甚至在不同的时间内表现出相同的行为**。这种”无聊”的一致性行为使开发人员能够专注于他们的日常工作，并使Go隐退到后台。

首先，Go语言尽可能地规定了一致的结果，即使是错误的行为，如本文的”安全性”部分所讨论的空指针解引用和数组索引越界。这种一致性行为的一个例外是对map的迭代。我们发现，程序员经常不经意地写下依赖于哈希函数的代码，导致在不同的架构或Go实现上出现不同的结果。

为了使程序在任何地方都有相同的表现，一种选择是强制规定一个特定的哈希函数。相反，Go定义了map迭代是非确定的。该实现为每个map使用不同的随机种子，并从哈希表中的一个随机偏移量开始对地图进行每次迭代。其结果是，map在不同的实现中都是不可预知的。代码不能再意外地依赖于实现细节。与此类似，竞态检测器为调度决策增加了额外的随机性，创造了更多的机会来观察竞态行为。

![](../../assets/34645142cb1e1ddf.png)


一致性的另一个方面是在程序的生命周期内的性能。使用传统的编译器而不是Java和Node.js等语言使用的JIT来实现Go的决策，可以在启动时和短生命周期的程序中提供了一致的性能。没有”慢启动”来惩罚每个进程生命周期的前几秒。这种快速启动使Go成为命令行工具（如上一节所述）以及谷歌应用引擎(Google App Engine)等规模化网络服务器的目标。

稳定的性能包括垃圾收集的开销。最初的Go原型使用了一个基本的、停止世界(STW)的垃圾收集器，当然，它在网络服务器中引入了明显的尾部延时。今天，Go使用了一个完全并发的垃圾收集器，暂停时间不到一毫秒，通常只有几微秒，与堆的大小无关。最主要的延迟是操作系统向必须中断的线程传递信号所需的时间。

最后一种一致性是语言和库随着时间的推移而产生的一致性。在Go诞生的前几年，我们在每周的发布中都会对它进行修补和调整。用户在更新到新的Go版本时，常常不得不改变他们的程序。我们提供自动工具以减少开发人员的负担，但手动调整依然是必要的。从2012年发布的Go 1.0开始，我们**公开承诺只对语言和标准库进行向后兼容的修改**，这样程序在编译到较新的Go版本时可以继续运行而不发生变化。这一承诺对业界产生了吸引力，它不仅鼓励了那些长声明周期的工程项目，也鼓励了其他努力，如书籍、培训课程和第三方软件包的繁荣生态系统。

### 工具辅助开发(Tool-Aided Development)

大规模的软件开发需要大量的自动化和辅助工具。从一开始，Go的设计就是为了鼓励这种工具化，并使其易于创建。

开发者对Go的日常体验是通过go命令进行的。与只编译或运行代码的语言命令不同，go命令为开发周期的所有关键部分提供了子命令：go build和go install构建和安装可执行文件，go test运行测试用例，go get添加新的依赖。go命令还提供了对构建细节的编程访问接口，例如软件包图，从而使得新工具的创建更加容易。

其中一个工具是go vet，它可以执行增量的、每次打包的程序分析，可以像缓存编译的对象文件那样缓存，实现增量构建。go vet工具的目的是高精度地识别常见的正确性问题，这样开发人员就有条件地听从它的报告。简单的例子包括在调用fmt.Printf和相关函数时检查格式字符串和参数是否匹配，或者诊断对变量或结构体字段的未用的写入。这些不是编译器错误，因为我们不希望仅仅因为发现了一个新的可能的错误就停止编译旧代码。它们也不是编译器警告；用户要学会忽略这些。将这些检查放在一个单独的工具中，可以让它们在开发者方便的时候运行，而不干扰普通的构建过程。这也使得所有的开发者都可以使用同样的检查，即使是在使用Go编译器的另一种实现，如Gccgo或Gollvm。这种增量方法使这些静态检查足够高效，我们在go test期间自动运行它们，然后再运行测试本身。无论如何，测试是用户在寻找错误，测试报告往往有助于解释实际的测试失败。这个增量框架也可以被其他工具重复使用。

分析程序的工具是很有帮助的，但是编辑程序的工具就更好了，特别是对于程序的维护，很多工具都是乏味的、可自动化运作的。

Go程序源码的标准样式是通过算法定义的。一个名为gofmt的工具将源文件解析为抽象的语法树，然后使用一致的布局规则将其格式化为源代码。**在Go中，在将代码存储到源码控制系统中之前将其格式化被认为是一种最佳做法**。这种方法使数以千计的开发人员能够在一个共享的代码库中工作，而不需要为大括号样式和其他细节进行争论，这些争论常伴随着这种大型项目。更重要的是，工具可以通过对抽象语法形式的操作来修改Go程序，然后用gofmt的printer输出结果。只有实际改变的部分才会被触及，产生的”差异”与人的手写结果是一致的。人和程序可以在同一个代码库中无缝协作。

为了实现这种方法，Go的语法被设计为能够在没有类型信息或任何其他外部输入的情况下解析源文件，而且没有预处理器或其他宏系统。Go标准库提供了一些包，允许工具重新创建gofmt的输入和输出端，同时还有一个完整的类型检查器。

在发布Go 1.0 –第一个稳定的Go版本之前，我们写了一个叫做gofix的重构工具，它就使用这些包来解析源代码、重写抽象语法树，并写出格式良好的代码。例如，当从map中删除一个条目的语法被改变时，我们就使用了gofix。每次用户更新到一个新版本时，他们可以在他们的源文件上运行gofix，自动应用更新到新版本所需的大部分变化。

这些技术也适用于IDE插件和其他支持Go程序员的工具–profiler、调试器、分析器、构建自动程序、测试框架等等的构建。Go的常规语法、既定的算法代码布局惯例以及基于标准库的直接支持，使得这些工具的构建比其他方式要容易得多。因此，Go世界拥有一个丰富的、不断扩展的、可互操作的工具包。

### 库(Libraries)

在语言和工具之后，下一个用户关键体验是可用的Go库。作为一种分布式计算的语言，Go没有提供用于发布Go软件包的中央服务器。相反，每个以域名开始的导入路径都被解释为一个URL（有一个隐含的前导https://），提供远程源代码的位置。例如，导入 “github.com/google/uuid”可以获取托管在相应的GitHub仓库的代码。

托管源代码最常见的方式是指向公共的Git或Mercurial服务器，但私人服务器也同样得到了很好的支持，作者可以选择发布一个静态的文件包，而不是开放对源码控制系统的访问。这种灵活的设计和发布库的便利性创造了一个繁荣的可导入Go包的社区。依靠域名，避免了在扁平的包名空间中急于索取有价值的条目(译注：应该是避免了导入路径冲突的问题)。

仅仅下载软件包是不够的，我们还必须知道要使用哪些版本。Go将包分组为称为**module**的版本单位。一个module可以为它的一个依赖关系指定一个最低要求的版本，但没有其他限制。当构建一个特定的程序时，Go通过选择最大版本来解决竞争的依赖module的所需版本：如果程序的一部分需要某个依赖module的1.2.0版本，而另一部分需要1.3.0版本，Go会选择1.3.0版本–也就是说，Go要求使用语义版本划分，其中1.3.0版本必须是1.2.0的直接替换(译注：1.3.0保持与1.2.0的兼容性)。另一方面，在这种情况下，即使1.4.0版本可用，Go也不会选择它，因为程序中没有任何部分明确要求使用该较新的版本。这个规则保持了构建的可重复性，并最大限度地减少了因意外破坏新版本所引入的变化而造成的潜在风险。

在语义版本管理中，一个module只能在一个新的主要版本中引入有意的破坏性变化，比如2.0.0。在Go中，从2.0.0开始的每个主要版本在其导入路径中都有一个主要版本后缀，比如/v2。不同的主版本和其他不同名字的module一样被分开。这种方法不允许出现钻石依赖性问题，而且在实践中，它可以适应不兼容的情况，也可以适应具有更精细约束的系统。

为了提高从互联网上下载软件包的构建的可靠性和可重现性，我们在Go工具链中运行了两个默认使用的服务：一个是可用的Go软件包的公共镜像，一个是其预期内容的加密签名的透明日志。即便如此，广泛使用从互联网上下载的软件包仍然存在安全和其他风险。我们正在努力使Go工具链能够主动识别并向用户报告有漏洞的软件包。

### 结论(Conclusion)

虽然大多数语言的设计都集中在语法、语义或类型的创新上，但**Go的重点是软件开发过程本身**。Go语言高效、易学、免费，但**我们认为它的成功之处在于它所采取的编写程序的方法，特别是多个程序员在一个共享代码库上工作时**。该语言本身的主要不寻常属性–并发性–解决了2010年代随着多核CPU的广泛应用而出现的问题。但更重要的是，早期的工作为打包、依赖关系、构建、测试、部署和软件开发领域的其他工作任务奠定了基础，这些方面在传统的语言设计中并没有受到应有的重视。

这些想法吸引了志同道合的开发者，他们重视与努力的结果是：容易并发、明确的依赖关系、可扩展的开发和生产、安全的程序、简单的部署、自动代码格式化、工具辅助开发等等。这些早期的开发者帮助普及了Go，并播种了最初的Go包生态系统。他们还推动了该语言的早期发展，例如，将编译器和库移植到Windows和其他操作系统上（最初的版本只支持Linux和MacOS X）。

不是每个人都喜欢–例如，有些人反对该语言省略了继承和泛型等常见功能。但是Go的以开发为中心的理念足够吸引人，也足够有效，以至于社区在保持最初推动Go存在的核心原则的同时，也得到了蓬勃发展。在很大程度上，由于该社区和它所建立的技术，Go现在是现代云计算环境的一个重要组成部分。

自Go第一版发布以来，该语言几乎被冻结。然而，工具已经大大扩展，有了更好的编译器，更强大的构建和测试工具，以及改进的依赖性管理，更不用说支持Go的大量开源工具了。然而，变化正在到来。[2022年3月发布的Go 1.18](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)包含了对语言的真正改变的第一个版本，一个被广泛要求的改变–参数化多态性的第一版实现。我们曾将任何形式的泛型排除在原始语言之外，因为我们敏锐地意识到，它很难设计好，而且在其他语言中，往往是复杂性而非生产力的来源。在Go的第一个十年中，我们考虑了很多设计，但直到最近才找到一个我们认为很适合Go的设计。在坚持一致性、完整性和社区原则的前提下进行如此大的语言变革，将是对该方法的严峻考验。

### 致谢(Acknowledgments)

Go最早的工作从Google的许多同事的建议和帮助中受益匪浅。自公开发布以来，由于Google的Go团队不断扩大，加上大量的开源贡献者，Go不断成长和改进。Go现在是由成千上万的人共同完成的，这里无法一一列举。我们感谢每一个帮助Go发展到今天的人。

### 参考资料(References)

-
Aas, J. and Gran, S. Let’s Encrypt has issued a billion certificates. Let’s Encrypt (2020), https://letsencrypt.org/2020/02/27/one-billion-certs.html.

-
Aas, J., et al. Let’s Encrypt: An automated certificate authority to encrypt the entire web. In Proceedings of the 2019 ACM SIGSAC Conf. on Computer and Communications Security, 2473–2487.

-
Bloch, D. Life on the edge: Monitoring and running a very large Perforce installation. Presented at 2007 Perforce User Conf., https://go.dev/s/bloch2007.

-
Chang, F., et al. Bigtable: A distributed storage system for structured data. In 7th USENIX Symposium on Operating Systems Design and Implementation (2006), 205–218.

-
Cox, R. Introducing Gofix. The Go Blog (2011), https://go.dev/blog/introducing-gofix.

-
Cox, R. The principles of versioning in Go. (2019), https://research.swtch.com/vgo-principles.

-
Cox, R. Surviving software dependencies. Communications of the ACM 62, 9 (Aug. 2019), 36–43.

-
Cox, R. Transparent logs for skeptical clients (2019), https://research.swtch.com/tlog.

-
Cox, R. and Pike, R. Go programming. Presented at Google I/O (2010), https://www.youtube.com/watch?v=jgVhBThJdXc.

-
Crosby, S.A. and Wallach, D.S. Efficient data structures for tamper-evident logging. In Proceedings of the 18th USENIX Security Symp. (2009), 317–334.

-
Donovan, A.A.A. and Kernighan, B.W. The Go Programming Language. Addison-Wesley, USA (2015).

-
Dorward, S., Pike, R., and Winterbottom, P. Programming in Limbo. In IEEE COMPCON 97 Proceedings (1997), 245–250.

-
Geissmann, L.B. Separate compilation in Modula-2 and the structure of the Modula-2 compiler on the personal computer Lilith. Ph.D. dissertation. Swiss Federal Institute of Technology (1983), https://www.cfbsoftware.com/modula2/ETH7286.pdf.

-
Gerrand, A. Go fmt your code. The Go Blog (2013), https://go.dev/blog/gofmt.

-
Go Project. Setting up and using gccgo. (2009), https://go.dev/doc/install/gccgo.

-
Go Project. Go 1 and the future of Go programs. (2012), https://go.dev/doc/go1compat.

-
Go Project. Gollvm, an LLVM-based Go compiler. (2017), https://go.googlesource.com/gollvm/.

-
Go Project. The Go programming language specification. (2021), https://go.dev/ref/spec.

-
Hoare, C.A.R. Communicating Sequential Processes. Prentice-Hall, Inc., USA (1985).

-
Hockman, K. Go Module Proxy: Life of a query. Presented at GopherCon 2019, https://www.youtube.com/watch?v=KqTySYYhPUE

-
Hudson, R.L. Getting to Go: The journey of Go’s garbage collector. The Go Blog (2018), https://go.dev/blog/ismmkeynote.

-
Klabnik, S. and Nichols, C. The Rust Programming Language. No Starch Press, USA (2018).

-
Lam, A. Using remote cache service for Bazel. Communications of the ACM 62, 1 (Dec. 2018), 38–42.

-
Ousterhout, J. Why threads are a bad idea (for most purposes). (1995), https://web.stanford.edu/~ouster/cgi-bin/papers/threads.pdf

-
Pike, R. The implementation of Newsqueak. Software: Practice and Experience 20, 7 (1990), 649–659.

-
Pike, R., Dorward, S., Griesemer, R., and Quinlan, S. Interpreting the data: Parallel analysis with Sawzall. Scientific Programming Journal 13 (2005), 277–298.

-
Preston-Werner, T. Semantic versioning 2.0.0. (2013), https://semver.org/

-
Serebryany, K., Potapenko, A., Iskhodzhanov, T., and Vyukov, D. Dynamic race detection with LLVM compiler: Compile-time instrumentation for ThreadSanitizer. In Runtime Verification, S. Khurshid, and K. Sen (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg (2012), 110–114.

-
Stambler, R. Go, pls stop breaking my editor. Presented at GopherCon 2019, https://www.youtube.com/watch?v=EFJfdWzBHwE.

-
Symonds, D., Tao, N., and Gerrand, A. Go and Google App Engine. The Go Blog (2011), https://go.dev/blog/appengine

-
Winterbottom, P. Alef language reference manual. In Plan 9: Programmer’s Manual Volume 2. Harcourt Brace and Co., New York (1996).


### 作者(Authors)

Russ Cox (rsc@go.dev), Robert Griesemer, Rob Pike, Ian Lance Taylor, and Ken Thompson作为美国加州山景城的谷歌公司的软件工程师创造了Go编程语言和环境。Cox、Griesemer和Taylor继续在Google领导Go项目，而Pike和Thompson已经退休了。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


![img{512x368}](../../assets/617100c3677e1846.jpg)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2022, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论