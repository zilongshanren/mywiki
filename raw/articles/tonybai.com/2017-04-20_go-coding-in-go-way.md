---
title: Go coding in go way
url: https://tonybai.com/2017/04/20/go-coding-in-go-way/
published: '2017-04-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go coding in go way

本篇文章是我在2017年[第三届GopherChina大会](http://tonybai.com/2017/04/18/my-experience-of-gopherchina-2017-as-a-speaker/)上所作talk：”[Go coding in go way](https://tonybai.com/(https:/github.com/bigwhite/talks/blob/master/gopherchina/2017/go-coding-in-go-way-cn.slide))“的改编和展开版，全文如下。

## 一、序

今天我要分享的题目是**“Go coding in go way”**，中文含义就是用**“Go语言编程思维去写Go代码”**。看到这个题目大家不禁要问：究竟什么是[Go语言](https://golang.org/)编程思维呢？关于什么是Go语言变成思维其实并没有官方说法。这里要和大家交流的内容都是基于[Go诞生七年](https://blog.golang.org/7years)多以来我个人对Go的设计者、Go team以及Go主流社区的观点和代码行为的整理、分析和总结。希望通过我的这次“抛砖引玉”，让在座的Gopher们对“Go语言编程思维”有一个初步的认知，并在日常开发工作中遵循Go语言的编程思维，写出idiomatic的Go代码。

## 二、编程语言与编程思维

### 1、大师的观点

在人类自然语言学界有一个很著名的假说：”[萨丕尔-沃夫假说](https://en.wikipedia.org/wiki/Linguistic_relativity)“，这个假说的内容是这样的：

```
语言影响或决定人类的思维方式("Language inuences/determines thought" - Sapir-Whorf hypothesis )
```


说到这个假说，我们不能不提及在2017年初国内上映了一部口碑不错的美国科幻大片《[降临](https://movie.douban.com/subject/21324900/)》，这部片子改编自雨果奖获得者华裔科幻小说家Ted姜的《[你一生的故事](https://book.douban.com/subject/1187842/)》，片中主线剧情的理论基础就是就是“萨丕尔-沃夫假说”。更夸张的是片中直接将该假说应用到外星人语言上，将其扩展到宇宙范畴^_^。片中的女主作为人类代表与外星人沟通，并学会了外星语言，从此思维大变，拥有了预知未来的“超能力”。由此我们可以看出“选择对一门语言是多么的重要”。

奇妙的是，在编程语言界，有位大师级人物也有着与”萨丕尔-沃夫假说”异曲同工的观点和认知。他就是首届图灵奖得主、著名计算机科学家[Alan J. Perlis(艾伦·佩利)](https://en.wikipedia.org/wiki/Alan_Perlis)。他从另外一个角度提出了：

```
“不能影响到你的编程思维方式的编程语言不值得去学习和使用”
A language that doesn't aect the way you think about programming is not worth knowing.
```


### 2、现实中的“投影”

从上述大师们的理论和观点，我们似乎看到了语言与思维之间存在着某种联系。那么两者间的这种联系在真实编程世界中的投影又是什么样子的呢？我们来看一个简单的编程问题：

```
【问题: 素数筛】
问题描述：素数是一个自然数，它具有两个截然不同的自然数除数：1和它本身。 要找到小于或等于给定整数n的素数。针对这个问题，我们可以采用埃拉托斯特尼素数筛算法。
算法描述：先用最小的素数2去筛，把2的倍数剔除掉；下一个未筛除的数就是素数(这里是3)。再用这个素数3去筛，筛除掉3的倍数... 这样不断重复下去，直到筛完为止。
```


![img{512x368}](../../assets/b357c8ba4a559ae1.gif)


算法动图

下面是该素数筛算法的不同编程语言的实现版本。

C语言版本：

```
【sieve.c】
void sieve() {
int c, i,j,numbers[LIMIT], primes[PRIMES];
for (i=0;i<LIMIT;i++){
numbers[i]=i+2; /*fill the array with natural numbers*/
}
for (i=0;i<LIMIT;i++){
if (numbers[i]!=-1){
for (j=2*numbers[i]-2;j<LIMIT;j+=numbers[i])
numbers[j]=-1; /*sieve the non-primes*/
}
}
c = j = 0;
for (i=0;i<LIMIT&&j<PRIMES;i++) {
if (numbers[i]!=-1) {
primes[j++] = numbers[i]; /*transfer the primes to their own array*/
c++;
}
}
for (i=0;i<c;i++) printf("%d\n",primes[i]);
}
```


[Haskell](https://www.haskell.org/)版本：

```
【sieve.hs】
sieve [] = []
sieve (x:xs) = x : sieve (filter (\a -> not $ a `mod` x == 0) xs)
n = 100
main = print $ sieve [2..n]
```


Go语言版本：

```
【sieve.go】
func generate(ch chan<- int) {
for i := 2; ; i++ {
ch <- i // Send 'i' to channel 'ch'.
}
}
func filter(src <-chan int, dst chan<- int, prime int) {
for i := range src { // Loop over values received from 'src'.
if i%prime != 0 {
dst <- i // Send 'i' to channel 'dst'.
}
}
}
func sieve() {
ch := make(chan int) // Create a new channel.
go generate(ch) // Start generate() as a subprocess.
for {
prime := <-ch
fmt.Print(prime, "\n")
ch1 := make(chan int)
go filter(ch, ch1, prime)
ch = ch1
}
}
```


- C版本的素数筛程序是一个常规实现。它定义了两个数组：numbers和primes，“筛”的过程在numbers这个数组中进行(纯内存修改)，非素数的数组元素被设置为-1，便于后续提取；
- Haskell版本采用了函数递归的思路，通过 “filter操作集合”，用谓词(过滤条件）\a -> not $ a
`mod`

x == 0；筛除素数的倍数，将未筛除的数的集合作为参数传递归递给下去； - Go版本的素数筛实现采用的是goroutine的并发组合。程序从2开始，依次为每个素数建立一个goroutine，用于作为筛除该素数的倍数。ch指向当前最新输出素数所位于的筛子goroutine的源channel，这段代码来自于Rob Pike的一次关于concurrency的分享slide。

![img{512x368}](../../assets/cd41f51df585fdaa.gif)


### 3、思考

通过上述这个现实中的问题我们可以看到：面对同一个问题，来自不同编程语言的程序员给出了思维方式截然不同的解决方法：C的命令式思维、Haskell的函数式思维和Go的并发思维。这一定程度上印证了前面的假说：编程语言影响编程思维。

[Go语言](http://tonybai.com/tag/go)诞生较晚（2007年设计、2009年发布Go1），绝大多数Gopher(包括我在内)第一语言都不是Go，都是“半路出家”从其他语言转过来的，诸如：[C](http://tonybai.com/tag/c)、C++、[Java](http://tonybai.com/tag/java)、[Python](http://tonybai.com/tag/python)等，甚至是Javascript、[Haskell](http://tonybai.com/tag/haskell)、[Lisp](http://tonybai.com/tag/clisp)等。由于Go语言上手容易，在转Go的初期大家很快就掌握了Go的语法。但写着写着，就是发现自己写的代码总是感觉很别扭，并且总是尝试在Go语言中寻找自己上一门语言中熟悉的语法元素；自己的代码风格似乎和Go stdlib、主流Go开源项目的代码在思考角度和使用方式上存在较大差异。而每每看到Go core team member(比如：rob pike)的一些代码却总有一种醍醐灌顶的赶脚。这就是我们经常说的go coding in c way、in java way、in python way等。出现这种情况的主要原因就是大脑中的原有语言的思维方式在“作祟”。

我们学习和使用一门编程语言，目标就是要用这门语言思维方式去Coding。学习Go，就要用Go的编程思维去写Go代码，而不是用其他语言的思维方式。

### 4、编程语言思维的形成

人类语言如何影响人类思维这个课题自然要留给人类语言学家去破解。但编程语言如何影响编程思维，每个程序员都有着自己的理解。作为一个有着十几年编程经验的程序员，我认为可以用下面这幅示意图来解释一门编程语言思维的形成机制：

![img{512x368}](../../assets/3387d8d9c5e346ec.png)


决定编程语言思维的根本在于这门编程语言的价值观！什么是价值观？个人认为：一门编程语言的价值观就是这门语言的最初设计者对程序世界的认知。不同编程语言的价值观不尽相同，导致不同编程语言采用不同的语法结构，不同语言的使用者拥有着不同的思维方式，表现出针对特定问题的不同的行为（具现为：代码设计上的差异和代码风格上的不同），就像上面素数筛那样。比如：

```
C的价值观摘录：
- 相信程序员：提供指针和指针运算，让C程序员天马行空的发挥
- 自己动手，丰衣足食：提供一个很小的标准库，其余的让程序员自造
- 保持语言的短小和简单
- 性能优先
C++价值观摘录：
- 支持多范式，不强迫程序员使用某个特定的范式
- 不求完美，但求实用（并且立即可用）
```


此外，从上述模型图，我们可以看出思维和结构影响语言应用行为，这是语言应用的核心；同时存在一个反馈机制：即语言应用行为会反过来持续影响/优化语言结构。我们常用冰山表示一个事物的表象与内涵。如果说某种语言的惯用法idiomatic tips或者best practice这些具体行为是露出水面上的冰山头部，那么价值观和思维方式就是深藏在水面以下的冰山的基座。

## 三、Go语言价值观的形成与Go语言价值观

从上述模型来看，编程语言思维形成的主导因素是这门编程语言的价值观，因此我们首先来看一下Go语言价值观的形成以及Go语言价值观的具体内容。

Go语言的价值观的形成我觉得至少有三点因素。

### 1、语言设计者&Unix文化

Go语言价值观形成是与Go的初期设计者不无关系的，可以说Go最初设计者主导了Go语言价值观的形成！这就好比一个企业的最初创始人缔造企业价值观和文化一样。

![img{512x368}](../../assets/3166dc212f010f8f.png)


图中是Go的三位最初设计者，从左到右分别是罗伯特·格瑞史莫、罗伯·派克和肯·汤普逊。Go初期的所有features adoption是需要三巨头达成一致才行。三位设计者有一个共同特征，那就是深受Unix文化熏陶。罗伯特·格瑞史莫参与设计了Java的HotSpot虚拟机和Chrome浏览器的JavaScript V8引擎，罗博·派克在大名鼎鼎的bell lab侵淫多年，参与了Plan9操作系统、C编译器以及多种语言编译器的设计和实现，肯·汤普逊更是图灵奖得主、Unix之父。关于Unix设计哲学阐述最好的一本书莫过于埃瑞克.理曼德(Eric S. Raymond)的《[UNIX编程艺术](https://book.douban.com/subject/1467587/)》了，该书中列举了很多unix的哲学条目，比如：简单、模块化、正交、组合、pipe、功能短小且聚焦等。三位设计者将Unix设计哲学应用到了Go语言的设计当中，因此你或多或少都能在Go的设计和应用中找到这些哲学的影子。

### 2、遗传基因

Go并发模型CSP理论的最初提出者Tony Hoare曾提出过这样一个观点：

```
The task of the programming language designer " is consolidation not innovation ". (Tony Hoare, 1973).
编程语言设计者的任务不是创新，而是巩固。
```


![img{512x368}](../../assets/b5c4eb220bdd1511.png)


和其他语言一样，Go也是站在巨人肩膀上的。这种基因继承，不仅仅是语法结构的继承，还有部分价值观的继承和进一步认知改进。当然不可否认的是Go也有自己的微创新，比如： implicit interface implementation、首字母大小写决定visibility等。虽然不受学院派待见，但把Go的这些微创新组合在一起，你会看到Go迸发出了强大的表现力。

### 3、面向新的基础设施环境和大规模软件开发的诸多问题

有一种开玩笑的说法：Go诞生于C++程序的漫长compile过程中。如果c++编译很快，那么上面的Go语言三巨头也没有闲暇时间一起喝着咖啡并讨论如何设计一门新语言。

面对时代变迁、面对新的基础设施环境、多核多处理器平台的出现，很多传统语言表现出了“不适应”，这直接导致在开发大规模软件过程中出现了各种各样的问题，比如：构建缓慢、依赖失控、代码风格各异、难用且复杂无法自动化的工具、跨语言构建难等。Go的设计初衷就是为了面向新环境、面向解决问题的。虽然这些问题不都是能在语言层面解决的，但这些环境和问题影响了设计者对程序世界的认知，也就影响了Go的价值观。

### 4、Go语言的价值观

在明确了Go价值观的形成因素后，我认为Go语言的价值观至少包含以下几点：

```
- Overall Simplicity 全面的简单
- Orthogonal Composition 正交组合
- Preference in Concurrency 偏好并发
```


用一句话概括Go的价值观（也便于记忆）：

```
Go is about orthogonal composition of simple concepts with preference in concurrency.
Go是在偏好并发的环境下的简单概念/事物的正交组合
```


无论是Go语言设计还是Go语言使用，都受到上述价值观的影响。接下来我们逐个来看一下Go语言价值观主导下的Go语言编程思维，并看看每种编程思维在语言设计、标准库实现以及主流Go开源项目中的应用体现。我将按“价值观” -> “(价值观下的)语言设计” -> “编程思维” -> “编程思维体现”的顺序展开。

## 四、Overall Simplicity

Go的第一个价值观就是”全面简单”。

图灵奖获得者迪杰斯特拉说过：”简单和优雅不受欢迎，那是因为人们要想实现它们需要更努力地工作，更多自律以及领会更多的教育。” 而Go的设计者们恰恰在语言设计初期就将复杂性留给了语言自身的设计和实现阶段，留给了Go core team，而将简单留给了gopher们。因此，Simplicity价值观更多地体现在了Go语言设计层面。 这里简单列举一些：

```
- 简洁、正规的语法：大大降低Go入门门槛，让来自其他语言的初学者可以轻松使用Go语言；
- 仅仅25个keyword：主流编程语言中最简单的，没有之一；
- “一种”代码写法、尽可能减少程序员付出;
- 垃圾回收GC: 降低程序员在内存管理方面的心智负担；
- goroutine：提供最简洁的并发支持；
- constants：对传统语言中常量定义和使用方法做进一步简化；
- interface：纯方法集合，纯行为定义，隐式实现；
- package：Go程序结构层面的唯一组织形式，它将设计、语法、命名、构建、链接和测试都聚于一包中，导入和使用简单。
```


如今，Go语言的简单已经从自身设计扩展到Go应用的方方面面，但也正是由于在语言层面已经足够简单了，因此在应用层面，“简单”体现的反倒不是很明显，更加顺其自然。接下来，我总结整理几个在“全面简单”价值观下形成的Go编程思维，我们一起看一下。

### 1、short naming thought（短命名思维）

在gofmt的帮助下，Go语言一统coding style。在这样的一个情形下，naming成了gopher们为数不多可以“自由发挥”的空间了。但对于naming，Go有着自己的思维：短命名。即在并不影响readablity的前提下，尽可能的用长度短小的标识符，于是我们经常看到用单个字母命名的变量，这与其他一些语言在命名上的建议有不同，比如Java建议遵循“见名知义”的命名原则。

Go一般在上下文环境中用最短的名字携带足够的信息，我们可以对比一下Java和Go：

```
java vs. go
"index" vs. "i"
"value" vs. "v"
```


除了短小，Go还要求尽量在一定上下文中保持命名含义的一致性，比如：在一个上下文中，我们声明了两个变量b，如果第一个b表意为buf，那么后续的b也最好是这个含义。

在命名短小和一致性方面，stdlib和知名开源项目为我们做出表率。我们统计一下Go标准库中标识符使用频率，可以看到大量单字母命名的变量标识符占据top30：

```
cat $(find $GOROOT -name '*.go') | indents | sort | uniq -c | sort -nr | sed 30q
60224 v
42444 err
38012 t
33386 x
33302 i
33277 b
27943 p
25121 s
21228 n
20831 r
20634 _
19236 c
17056 y
12850 f
12834 a
... ...
```


细致分析了一下stdlib中常见短变量名字所代表的含义（见代码后的注释），stdlib在一致性方面做的还是不错的，当然也有例外。

```
[v, k, i]
// loop varible
for i, v := range s {
for k, v := range m {
for v := range r { // channel
// if、switch/case clause varible
if v := mimeTypes[ext]; v != "" {
switch v := ptr.Elem(); v.Kind() {
case v := <-c:
v := reflect.ValueOf(x) // result of reflect.Value()
[t]
t := time.Now() // time
t := &Timer{ // timer
if t := md.typemap[off]; t != nil { // type
[b]
b := make([]byte, n) // bytes slice
b := new(bytes.Buffer) // bytes.Buffer
```


### 2、minimal thought（最小思维)

码农们是苦逼的，每天坐在电脑前一坐就是10多个小时，自己的“业余”时间已经很少了。Go语言的设计者在这方面做的很“贴心”，考虑到为了让男Gopher能有时间撩妹，女Gopher能有时间傍帅哥，Go语言倡导minimal thought，即尽可能的降低gopher们的投入。这种思维体现在语言设计、语言使用、相关工具使用等多个方面。比如：

- 一种代码风格：程序员们再也无需为coding style的个人喜好而争论不休了，节省下来的时间专心做自己喜欢的事情:)
- “一种”代码写法(或提供最少的写法、更简单的写法)：你会发现，面对一个问题，大多数gopher们给出的go实现方式都类似。这就是Go“一种代码写法”思维的直接体现。Go在语法结构层面没有提供给Gopher很大的灵活性。Go is not a “TMTOWTDI — There’s More Than One Way To Do It”。这点与C++、Ruby有着很大不同。
- 显式代码（obvious），而不是聪明(clever)代码：Go提倡显而易见、可读性好的代码，而非充满各种技巧或称为“炫技”的所谓“聪明”代码。纵观stdlib、kubernetes等go代码库，都是很obvious(直观)的go code，clever code难觅踪迹。这样一来，别人写的代码，你可以轻松地看懂（为你节省大量时间和精力）。这也是Go代码中clever code比例远远小于其他主流语言的原因，Go不是炫技的舞台。

C++程序员看到这里是不是在“抹眼泪”，这里并非黑C++，C++的复杂和多范式是客观的，C++98标准和C++17标准的差异甚至可以用“两门语言”来形容，用泛型的代码和不用泛型的代码看起来也像是两门完全不同的语言，这种心智负担之沉重可想而知。

接下来，我们看看minimal thought在语言设计和应用中的体现。

#### 1) “一种”循环: for

Go语言仅仅提供了一种用于“循环逻辑”的关键字：for。在其他语言中的各种用于循环逻辑的关键字，比如while, do-while等，在go中都可以通过for模拟实现。

```
- 常规
for i := 0; i < count; i++ {}
- "while"
for condition { }
- "do-while"
for { // use "for-break" instead
doSomething()
if condition { break }
}
- iterator loop
for k, v := range f.Value {}
- dead loop
for {}
```


#### 2) “一种”constant

前面说过Go设计者是十分体贴的，这种体贴体现在很多不起眼的细节上，比如对传统语言中constant声明和使用的优化。

Go语言中constants只是数字，无论是整型还是浮点型都可以直接写成数字，无需显式地赋给类型：

```
const incomingQueueLength = 25
const (
http2minMaxFrameSize = 1 << 14
http2maxFrameSize = 1<<24 - 1
)
const PI = 3.1415928
const e = 1E6
```


参与计算的constant无需显式算术转换，而是由编译器自动确定语句中constant的承载类型：

```
const a = 10080
var c int32 = 99
d := c + a
fmt.Printf("%T\n", d) //int32
fmt.Printf("%T\n", a) //int
```


#### 3) “一种”错误处理方法

C++之父Bjarne Stroustrup说过：“世界上有两类编程语言，一类是总被人抱怨诟病的，而另外一类是无人使用的”。Go语言自其出生那天起，就因错误处理机制看起来似乎有些过时、有些简单而被大家所诟病，直至今天这种声音依旧存在。因为Go仅仅提供了一种基于值比较的简单的错误处理方法。但就是这样的错误处理方法也恰恰是Go设计者simplicity价值观的体现。Go设计者认为如果像其他一些主流语言那样，将exception的try-catch-finally的机制与语言的控制结构耦合在一起，将势必大大增加语言的复杂性，这与simplicity的价值观是背道而驰的。简单的基于值比较的error处理方法可以让使用者更重视每一个error并聚焦于错误本身。显式地去处理每一个error，让gopher对代码更有自信。并且在这种机制下，错误值和其他类型的值地位是一样的，错误处理代码也是普通代码，并无特殊之处，无特殊化处理，无需增加语言复杂性。

这些年来，gopher们也初步探索出了这种错误处理方法的常见处理模式，我们以stdlib中识别出的error handling模式为例：

**a) 最常见的**

在外部无需区分返回的错误值的情况下，可以在内部通过fmt.Errorf或errors.New构造一个临时错误码并返回。这种错误处理方式可以cover 80%以上情形：

```
callee:
return errors.New("something error")
or
return fmt.Errorf("something error: %s", "error reason")
caller:
if err != nil {... }
```


**b) 导出的Error变量**

当外部需要区分返回的错误值的，比如这里我要进行一个io调用，后续的操作逻辑需要因io调用的返回错误码的不同而异，我们使用导出的error变量：

```
// io/io.go
var ErrShortWrite = errors.New("short write")
var ErrShortBuffer = errors.New("short buffer")
if err := doSomeIO(); err == io.ErrShortWrite { ... }
```


**c) 定义新的错误类型实现定制化错误上下文**

上面的导出Error变量中包含的error context信息和信息形成机制太过简单，当我们要定制error context时， 我们可以定义一个新的Error type。之后通过针对error interface value的type assertion or type switch得到真实错误类型并访问error context：

```
// encoding/json/decode.go
type UnmarshalTypeError struct {
Value string // description of JSON value - "bool", "array", "number -5"
Type reflect.Type // type of Go value it could not be assigned to
Offset int64 // error occurred after reading Offset bytes
Struct string // name of the struct type containing the field
Field string // name of the field holding the Go value
}
func (e *UnmarshalTypeError) Error() string {
... ...
return "json: cannot unmarshal " + e.Value + " into Go value of type " + e.Type.String()
}
if serr, ok := err.(*UnmarshalTypeError); ok {
//use serr to access context in UnmarshalTypeError
... ...
}
```


不过这样的用法并不推荐也并不多见，在stdlib、kubernetes中，虽然都有自定义的exported error type，但是却很少在外部通过type assertion直接访问其内部error context字段，那标准库是怎么判断error差别的呢？

**d) 包含package中error公共行为特征的Error interface type

在标准库中，我们可以发现这样一种错误处理方式：将某个包中的Error Type归类，统一提取出一些公共行为特征，并且将这些公共行为特征(behaviour)放入一个公开的interface type中。以stdlib中的net package为例。net package将包内的所有错误类型的公共特征抽象放入”Error”这个error type中。外部使用时，通过这个公共interface获取具体错误的特征：

```
//net/net.go
type Error interface {
error
Timeout() bool // Is the error a timeout?
Temporary() bool // Is the error temporary?
}
net/http/server.go中的使用举例：
rw, e := l.Accept()
if e != nil {
if ne, ok := e.(net.Error); ok && ne.Temporary() {
... ..
}
... ...
}
```


OpError是net packge中的一个自定义error type , 它实现了Temporary interface, 可以被外部统一用Error的method判断是否是Temporary或timeout error特征：

```
//net/net.go
type OpError struct {
... ...
// Err is the error that occurred during the operation.
Err error
}
type temporary interface {
Temporary() bool
}
func (e *OpError) Temporary() bool {
if ne, ok := e.Err.(*os.SyscallError); ok {
t, ok := ne.Err.(temporary)
return ok && t.Temporary()
}
t, ok := e.Err.(temporary)
return ok && t.Temporary()
}
```


**e) 通过一些公开的error behaviour function对error behaviour进行判断

我们在标准库中还能看到一种判断error behavior的方法，那就是通过一些公开的error behaviour function。比如：os包暴露的IsExist等函数：

```
//os/error.go
func IsExist(err error) bool {
return isExist(err)
}
func IsNotExist(err error) bool { ... }
func IsPermission(err error) bool { ... }
例子：
f, err := ioutil.TempFile("", "_Go_ErrIsExist")
f2, err := os.OpenFile(f.Name(), os.O_RDWR|os.O_CREATE|os.O_EXCL, 0600)
if os.IsExist(err) {
fmt.Println("file exist")
return
}
```


顺便在这里提一下Go关于error type和variable的命名方式：

```
错误类型: xxxError
//net/net.go
type OpError struct { ... }
type ParseError struct { ... }
type timeoutError struct{}
导出的错误变量: ErrXxx
//io/io.go
var ErrShortWrite = errors.New("short write")
var ErrNoProgress = errors.New("multiple Read calls return no data or error")
```


很多人抱怨，当前Go提供的error handling方案让gopher可以很容易地写出如下面所示的不优雅代码：

```
var err error
err = doSomethingA()
if err != nil {
return err
}
err = doSomethingB()
if err = nil {
return err
}
err = doSomethingC()
if err = nil {
return err
}
... ...
```


代码中大量重复着if err!= nil { return err} 这段snippet。但是如果你全面浏览过Go标准库中的代码，你会发现像上面这样的代码并不多见。Rob Pike曾经在《[errors are values](https://blog.golang.org/errors-are-values)》一文中针对这个问题做过解释，并给了stdlib中的一些消除重复的方法：那就是将error作为一个内部状态：

```
//bufio/bufio.go
type Writer struct {
err error
buf []byte
n int
wr io.Writer
}
func (b *Writer) Write(p []byte) (nn int, err error) {
if b.err != nil {
return nn, b.err
}
... ...
}
//writer_demo.go
buf := bufio.NewWriter(fd)
buf.WriteString("hello, ")
buf.WriteString("gopherchina ")
buf.WriteString("2017")
if err := buf.Flush() ; err != nil {
return err
}
```


error handling的具体策略要根据实际情况而定。stdlib面向的”业务域”相对”狭窄”，像bufio.Write可以采用上面的方法解决，但是对于做业务应用的gopher来讲，业务复杂多变，错误处理没有绝对的模式，需根据上下文不同而具体设计。但如果一个函数中上述snippet过多，很可能是这个函数或方法的职责过多导致，重构是唯一出路。

## 五、Orthogonal Composition

正交组合是我总结出来的第二个Go语言的价值观。如果说上一个价值观聚焦的是Go程序提供的各种小概念实体或者说”零件”的话，那么Composition就是在考虑如何将这些”零件”联系到一起，搭建程序的静态骨架。

在Go语言设计层面，Go设计者为gopher提供了正交的语法元素，供后续组合使用，包括：

- Go语言无类型体系(type hierarchy)，类型定义正交独立；
- 方法和类型的正交性: 每种类型都可以拥有自己的method set；
- interface与其实现之间无”显式关联”；

正交性为”组合”策略的实施奠定了基础，提供了前提。Rob Pike曾说过： “If C++ and Java are about type hierarchies and the taxonomy(分类）of types, Go is about composition.”。组合是搭建Go程序静态结构的主要方式。“组合”的价值观贯穿整个语言设计和语言应用：

- 类型间的耦合方式直接影响到程序的结构；
- Go语言通过“组合”构架程序静态结构；
- 垂直组合(类型组合)：Go通过 type embedding机制提供；
- 水平组合：Go通过interface语法进行“连接”。

interface是水平组合的关键，好比程序肌体上的“关节”，给予连接“关节”的两个部分各自“自由活动”的能力，而整体上又实现了某种功能。

### 1、vertical composition thought(垂直组合思维)

传统OO语言都是通过继承的方式建构出自己的类型体系的，但Go语言中并没有类型体系的概念。Go语言通过类型的垂直组合而不是继承让单一类型承载更多的功能。由于不是继承，那么也就没有了所谓“父子类型”的概念，也没有向上、向下转型(type casting)；被嵌入的类型也不知道将其嵌入的外部类型的存在。调用Method时，method的匹配取决于方法名字，而不是类型。

Go语言通过type embedding实现垂直组合。组合方式莫过于以下这么几种：

**a) construct interface by embedding interface**

```
type ReadWriter interface {
Reader
Writer
}
```


通过在interface中嵌入interface type name，实现接口行为聚合，组成大接口。这种方式在stdlib中尤为常用。

**b) construct struct by embedding interface**

```
type MyReader struct {
io.Reader // underlying reader
N int64 // max bytes remaining
}
```


**c) construct struct by embedding struct**

```
// sync/pool.go
type poolLocal struct {
private interface{} // Can be used only by the respective P.
shared []interface{} // Can be used by any P.
Mutex // Protects shared.
pad [128]byte // Prevents false sharing.
}
```


在struct中嵌入interface type name和在struct嵌入struct，都是“委派模式(delegate)”的一种应用。在struct中嵌入interface方便快速构建满足某一个interface的dummy struct，方便快速进行unit testing，仅需实现少数需要的接口方法即可，尤其是针对Big interface时。

struct中嵌入struct，被嵌入的struct的method会被提升到外面的类型中，比如上述的poolLocal struct，对于外部来说它拥有了Lock和Unlock方法，但是实际调用时，method调用实际被传给poolLocal中的Mutex实例。

### 2、small interface thought(小接口思维)

interface是Go语言真正的魔法。前面提到过，interface好比程序肌体的骨架关节，上下连接着骨架部件。interface决定了Go语言中类型的水平组合方式。interface与其实现者之间的关系是隐式的，无需显式的”implements”声明(但编译器会做静态检查)；interface仅仅是method集合，而method和普通function一样声明，无需在特定位置。

在Go语言中，你会发现小接口（方法数量在1~3）定义占据主流。

```
// builtin/builtin.go
type error interface {
Error() string
}
// io/io.go
type Reader interface {
Read(p []byte) (n int, err error)
}
// net/http/server.go
type Handler interface {
ServeHTTP(ResponseWriter, *Request)
}
type ResponseWriter interface {
Header() Header
Write([]byte) (int, error)
WriteHeader(int)
}
```


我统计了一下stdlib、[k8s](http://tonybai.com/tag/kubernetes)和docker里面的interface定义，画出了下面这幅接口个数与接口中method个数关系的折线图：

![img{512x368}](../../assets/70fc0ecf522615c4.png)


小接口方法少，职责单一；易于实现和测试，通用性强(如:io.Reader和Writer)，易于组合(如:io.Reader)。不过要想在业务领域定义出合适的小接口，还是需要对问题域有着透彻的理解的。往往无法定义出小接口，都是由于对领域的理解还不到位，没法抽象到很高的程度所致。

### 3、horizontal composition thought(水平组合思维)

有了小接口，后续主要关注如何通过接口进行“连接”的方式实现水平组合，以解决大问题、复杂的问题。通过interface进行组合的一种常见方法就是：通过接受interface类型参数的普通function进行组合。

以下几种具体形式：

**a) 基本形式**

接受interface value作为参数是水平组合的基本形式：

```
形式：someFunc(interface value parameter)
```


隐式的interface实现会不经意间满足：依赖抽象、里氏替换原则、接口隔离等原则，这在其他语言中是需要很”刻意”的设计谋划的，但在Go interface来看，一切却是自然而然的。

```
func ReadAll(r io.Reader) ([]byte, error)
func Copy(dst Writer, src Reader) (written int64, err error)
```


**b) wrapper function**

形式：接受interface类型参数，并返回与其参数类型相同的返回值

```
// Wrapper function:
func LimitReader(r Reader, n int64) Reader { return &LimitedReader{r, n} }
type LimitedReader struct {
R Reader // underlying reader
N int64 // max bytes remaining
}
func (l *LimitedReader) Read(p []byte) (n int, err error) {}
// Usage:
r := strings.NewReader("some io.Reader stream to be read\n")
lr := io.LimitReader(r, 4)
if _, err := io.Copy(os.Stdout, lr); err != nil {
log.Fatal(err)
}
// Output: some
```


LimitReader是一个wrapper function，它在r的外面再包裹上LimitedReader。通过wrapper function将NewReader和LimitedReader 的两者巧妙的组合在了一起。这样当我们采用包装后的reader去Read时，返回的是受到Limitedreader限制的内容了：即只读取了前面的4个字节：”some”。

**c) wrapper function chain**

由于wrapper function返回值类型与parameter类型相同，因此wrapper function可以组合一个chain，形式如下：

```
形式：wrapperFunc(wrapperFunc(wrapperFunc(...)))
```


我们定义一个wrapper function：CapReader，用于将从reader读取的数据变为大写：

```
func CapReader(r io.Reader) io.Reader {
return &capitalizedReader{r: r}
}
type capitalizedReader struct {
r io.Reader
}
func (r *capitalizedReader) Read(p []byte) (int, error) {
n, err := r.r.Read(p)
if err != nil {
return 0, err
}
q := bytes.ToUpper(p)
for i, v := range q {
p[i] = v
}
return n, err
}
```


将多个wrapper function串在一起：

```
s := strings.NewReader("some io.Reader stream to be read\n")
r := io.TeeReader(CapReader(io.LimitReader(s, 4)), os.Stdout)
b, _ := ioutil.ReadAll(r) //SOME
fmt.Println(len(b)) //4
```


可以看到例子中，我们将TeeReader、CapReader、LimitedReader、strings Reader等组合到了一起，实现了读取前四个字节，将读取数据转换为大写并输出到标准输出的功能。

**d) adapter function type **

adapter function type是一个辅助水平组合实现的“工具”。adapter function type将一个普通function转换为自己的类型，同时辅助快速实现了某个“one-method” interface。 adapter function type的行为模式有些像电影中的“僵尸” – 咬别人一口就可以将别人转化为自己的同类。最著名的僵尸类型莫过于http.HandlerFunc了：

```
type Handler interface {
ServeHTTP(ResponseWriter, *Request)
}
type HandlerFunc func(ResponseWriter, *Request)
func (f HandlerFunc) ServeHTTP(w ResponseWriter, r *Request) {
f(w, r)
}
// Usage: use HandlerFunc adapts index function to an implemenation type of Handler interface.
func index(w http.ResponseWriter, r *http.Request) {
fmt.Fprintf(w, "Welcome!")
}
http.ListenAndServe(":8080", http.HandlerFunc(index))
```


可以看到通过HandlerFunc，我们可以将普通function index快速转化为满足Handler interface的type。一旦转化ok，便可以通过interface进行组合了。

**e) middleware composition **

middleware这个词的含义可大可小，在Go Web编程中，常常指的是一个满足Handler interface的HandlerFunc类型实例。实质上：

```
middleware = wrapper function + adapter function type
```


我们可以看一个例子：

```
func logHandler(h http.Handler) http.Handler {
return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
t := time.Now()
log.Printf("[%s] %q %v\n", r.Method, r.URL.String(), t)
h.ServeHTTP(w, r)
})
}
func authHandler(h http.Handler) http.Handler {
return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
err := validateAuth(r.URL.Query().Get("auth"))
if err != nil {
http.Error(w, "bad auth param", http.StatusUnauthorized)
return
}
h.ServeHTTP(w, r)
})
}
func main() {
http.ListenAndServe(":8080", logHandler(authHandler(http.HandlerFunc(index))))
}
```


wrapper function（如：logHandler、authHandler）内部利用 adapter function type转化了一个普通function，并返回实现了Handler interface的HandlerFunc类型实例。

## 六、Preference in Concurrency

Go语言的第三个价值观是偏好并发。如果说interface和组合决定了程序的静态结构组成的话，那么concurrency则影响着程序在执行阶段的动态运行结构。从某种意义上说，Go语言就是关于concurrency和interface的设计!

并发不是并行(paralell)，并发是关于程序结构的，而不是关于性能的。并发让并行更easy，并且通常性能更好;对于程序结构来说，concurrency是一个比interface组合更大的概念。并发是一种在程序执行层面上的组合：goroutines各自执行特定的工作，通过channels+select将goroutines连接起来。原生对并发的支持，让Go语言更适应现代计算环境。并发的存在鼓励程序员在程序设计时进行独立计算的分解。

在语言层面，Go提供了三种并发原语：

-
goroutines提供

**并发执行**, 它是Go runtime调度的基本单元；goroutine实现了异步编程模型的高效，但却允许你使用同步范式编写代码，降低心智负担；goroutines被动态地多路复用到系统核心线程上以保证所有goroutines的正常运行。 -
channels用于goroutines之间的

**通信和同步**；channel是goroutines间建立联系的主要途径或者说goroutine通过channel耦合/组合在一起，这一点channel的功用有点像Unix pipe。 - select可以让goroutine同时
**协调处理**多个channel操作。

### 1、concurrency thought(并发思维)

我将“偏好并发”价值观下的思维统称为“并发思维”。并发思维的核心依旧是组合！

采用并发思维进行程序动态结构设计，需要识别和分解出独立的计算单元放入Goroutines执行，并使用channel/select建立Goroutines之间的联系。计算单元的拆解是并发程序设计的重点，拆解没有统一规则，因业务域不同而异，例如：素数筛实现为每个素数建立一个goroutine以筛除素数的倍数。

不过我们可以从建立Goroutines间的“联系”的角度来看一些常见的goroutines间的“关系”模式。我们可以从“退出机制”和“通信联系”两大方面出发考虑。

#### a) “detached” goroutine

所谓分离的goroutine，即不需要关心它的退出，相当于与父goroutine间“无关系”。这类goroutines启动后与其创建者彻底分离(detached)，生命周期与程序生命周期相同。通常，这类goroutine在后台执行一些特定任务，如：monitor、watcher等。其实现通常采用for-select代码段形式；以timer或event驱动。

Go应用中内置的GC goroutine就是这种类型的：

```
// runtime/mgc.go
go gcBgMarkWorker(p) // each P has a background GC G.
func gcBgMarkWorker(_p_ *p) {
gp := getg()
for {
... ...
}
}
```


#### b） “parent-child” goroutine

这类goroutine与detached goroutine正相反，parent需要通知并等待child退出。如果仅通知并等待一个child，我们可以这样做：

```
parent:
quit := make(chan string)
go child(quit)
child:
select {
case c := <-workCh:
// do something
case <-quit:
// do some cleanup
quit<-"done"
}
parent:
quit<-"quit"
<-quit
```


当需要同时通知多个child goroutine quit时，我们可以通过channel close来实现：

```
parent:
quit := make(chan struct{})
for ... {
go child(quit) // several child goroutines
}
child:
select {
case c := <-workCh: // do something
case <-quit: // do some cleanup
return
}
parent:
close(quit)
time.Sleep(time.Second * 30)
```


如果parent要获得child的退出状态值，可以自定义quit channel中的元素类型：

```
type ExitStatus interface {
Status() int
}
type IntStatus int // an adapter
func (n IntStatus)Status() int {
return int(n)
}
quit := make(chan ExitStatus) // for each child goroutine
child:
quit <- IntStatus(2017)
parent:
s := <-quit
fmt.Println(s.Status()) //2017
```


#### c) service handle

一些goroutine在程序内部提供特定service，这些goroutine使用channel作为service handle，其他goroutine通过service handle与其通信。

比如：我们经常使用的time.After返回一个service handle：

```
//time/sleep.go
func After(d Duration) <-chan Time {
return NewTimer(d).C
}
```


对应的service goroutine就是runtime中的timer service goroutine：

```
// runtime/time.go
func timerproc() {
timers.gp = getg()
for {
... ...
}
}
```


编写此类service goroutine时，需要考虑对于“慢消费者”service goroutine应该如何处置：阻塞还是丢弃。timer service goroutine使用的是buffered channel(size=1)，并在向channel发送消息时通过select做了一个判断。如果channel buffer满了，则丢弃这次timer事件。

如果我们要同时处理来自不同service goroutine的handle，那么可以使用service handles aggregation，见下面例子：

比如：我们从wechat、weibo、短信渠道获取msg：

```
type msg struct {
content string
source string
}
func wechatReceiver() <-chan *msg {
c := make(chan *msg)
go func() {
c <- &msg{"wechat1", sourceWechat}
c <- &msg{"wechat2", sourceWechat}
c <- &msg{"wechat3", sourceWechat}
}()
return c
}
func weiboReceiver() <-chan *msg {...}
func textmessiageReceiver() <-chan *msg {...}
```


我们需要把这些handle聚合起来统一处理，我们通过一个aggregation function来做。对于不固定数量handles的聚合，用goroutine来聚合(非常类似于unix pipe chain)：

```
func serviceAggregation(ins ...<-chan *msg) <-chan *msg {
out := make(chan *msg)
for _, c := range ins {
go func(c <-chan *msg) {
for v := range c {
out <- v
}
}(c)
}
return out
}
c := serviceAggregation(weiboReceiver(), wechatReceiver(), textmessageReceiver())
m := <-c // 获取message并处理
```


对于固定数量handles聚合，用select就可以实现：

```
func serviceAggregation(weibo, wechat, textmessage <-chan *msg) <-chan *msg {
out := make(chan *msg)
go func(out chan<- *msg) {
for {
select {
case m := <-weibo:
out <- m
case m := <-wechat:
out <- m
case m := <-textmessage:
out <- m
}
}
}(out)
return out
}
c := serviceAggregation(weiboReceiver(), wechatReceiver(), textmessageReceiver())
m := <-c // 获取message并处理
```


#### d) dispatch-and-mix goroutines

在“微服务”时代，我们在处理一个请求时经常调用多个外部微服务并综合处理返回结果：

```
func handleRequestClassic() {
r1 := invokeService1()
//handle result1
r2 := invokeService2()
//handle result2
r3 := invokeService3()
//handle result3
}
```


上述例子中的问题是显而易见的：顺序调用、慢、一旦某个service出现异常，返回时间不可预知，可能会导致调用阻塞。

一个优化的方法就是讲将处理请求时对外部的服务调用分发到goroutine中，再汇总返回结果。并且通过设置一个总体超时时间，让调用返回的时间可预知。：

```
func handleRequestByDAM() {
c1, c2, c3 := make(chan Result1), make(chan Result2), make(chan Result3)
go func() { c1 <- invokeService1() } ()
go func() { c2 <- invokeService2() } ()
go func() { c3 <- invokeService3() } ()
timeout := time.After(200 * time.Millisecond)
for i := 0; i < 3; i++ {
select {
case r := <-c1: //handle result1
c1 = nil
case r := <-c2: //handle result2
c2 = nil
case r := <-c3: //handle result3
c3 = nil
case <-timeout:
fmt.Println("timed out")
return
}
}
return
}
```


不过这次优化后的程序依旧存在一个问题，那就是一旦timeout，调用返回，但一些在途的请求资源可能没有回收，request无法显式撤回，久而久之，可能导致资源的泄露。于是我们做进一步改进：通过Context显式cancel掉已经向外发起的在途请求，释放占用资源:

```
type service func() result
func invokeService(ctx context.Context, s service) chan result {
c := make(chan result)
go func() {
c1 := make(chan result)
go func() {
c1 <-s()
}
select {
case v := <-c1:
c <-v
case <-ctx.Done():
// cancel this in-flight request by closing its connection.
}
}()
return c
}
func handleRequestByDAM() {
ctx, cf := context.WithCancel(context.Background())
c1, c2, c3 := invokeService(ctx, service1), invokeService(ctx, service2),
invokeService(ctx, service3)
timeout := time.After(200 * time.Millisecond)
for i := 0; i < 3; i++ {
select {
case r := <-c1: //handle result1
case r := <-c2: //handle result2
case r := <-c3: //handle result3
case <-timeout:
cf() // cancel all service invoke requests
return
}
}
return
}
```


优化后的程序的优点：并发、快、返回结果可预知。

## 七、总结

通过这篇文章，我总结了主导Go语言编程思维的三个价值观：

- Overall Simplicity
- Orthogonal Composition
- Preference in Concurrency

阐述了每种价值观主导下的编程思维，并给出了每种编程思维在语言设计、语言应用方面的一些模式和实际例子。

Go最初的设计初衷还有一点，那就是将编程时的fun重新带给Gopher们。但个人觉得只有当你使用Go编程思维去写Go code时，你才能体会到Go设计者的用意，才能让你没有别扭的赶脚，发现自己走在正确的way上，才能真正感到go coding时的fun。

另外，虽然总结出的三个价值观数量不多，但如果能在实际运用中认真践行，却能迸发巨大能量。它会让你应对各种复杂情况、代码设计变得游刃有余、顺利解决各种业务问题。

最后再说说Go 2.0。回到前面的 “编程语言思维的形成”模型，行为总是对结构有反馈的，这将导致结构的持续改变和优化。Go team将于今年8月份发布Go1.9版本，这是一个关键的时间节点。恰好今年的denver的[Gophercon大会](http://www.gophercon.com/)上，[Russ Cox](https://github.com/rsc)将做”the future of go”的演讲，后续是继续1.10还是Go 2.0，让我们拭目以待！不过个人觉得，无论对语言结构改动的需求有多大，Go的价值观都是不会发生改变的。

本文的slide文件可以在[这里](https://github.com/bigwhite/talks/blob/master/gopherchina/2017/go-coding-in-go-way-cn.slide)下载。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

代码显示控件优化下吧，弄的像oschina那样。

时间飞快，转眼年中就要到来，祝你天天愉快！

嗯

带颜色好看点

花了一个下午看完

收获炒鸡大啊

期待

感谢分享！已推荐到《开发者头条》：https://toutiao.io/posts/1fxejm 欢迎点赞支持！

欢迎订阅《GoHackers》https://toutiao.io/subject/1385

我只想默默的拜读您的博客！

从golang 1.0发布之前就关注，最近又重拾golang做项目，整理了一个学习笔记。

https://github.com/sdming/doc/tree/master/golang

很赞！

很赞，学到了好多，想问下这个动态图是用什么软件画出来的？

引用了一位外国gopher的图片：http://divan.github.io/posts/go_concurrency_visualize/

写的很详细，受教了~

今天看了你博客很多文章，收获挺多的

倒数第一个代码段里

invokeService(ctx content.Content, s service)，应该是context吧

嗯，笔误！已经fix. 3ks

感觉go还是会逐渐变厚

有个问题 ，文章最后的

go func() {

c1 := make(chan result)

go func() {

c1 <-s()// 假如s()一直没有返回结果，那这个goroutine会不会结束掉呢

}

select {

case v := <-c1:

c <-v

case <-ctx.Done():

// cancel this in-flight request by closing its connection.

}

}()

s()不返回，goroutine不会结束。但是除非是代码bug，一般来说即便是网络超时，s()也会返回的，可能只是等的时间长了些罢了。

你好，在goroutine里return和runtime.Goexit()有什么区别吗，我试了下return好像不会释放内存?

我对Goexit的理解也仅限于godoc上对Goexit的描述：https://golang.org/pkg/runtime/#Goexit 个人觉得在用户程序中尽量使用return，而不是runtime.Goexit。

是这样的……我做个高并发网络请求，三百并发量，结果做出来的东西内存占用很大，检测goroutine数量上万……我猜测是context造成的

可以profile一下（go tool pprof）内存分配情况 https://golang.org/doc/diagnostics.html

Go语言中constants只是数字

麻烦您 这句话能解释一下吗？

package main

import (

“fmt”

)

const (

a = 1

)

func main() {

var n1 int16 = 5

fmt.Println(n1 + a)

var n2 int32 = 51

fmt.Println(n2 + a)

}

运行这个程序：

$go run testconst.go

6

52

看到了吧，a这个常量的“类型”随着参与运算时的其他操作数的类型而自动变化，不需要显式转型，不会出现Compile error。这算是一个compiler sugar吧。

你好，素数筛那个问题，我试了下用Rob那个Go的代码运行出来，素数到时都筛选出来了，但是总是报死锁错误：all goroutines are asleep – deadlock!，可以解释下吗

那只是一个demo代码，演示的是精妙的素数筛技巧罢了。比如我们要筛出100以内素数，如果在main goroutine执行sieve，当筛选完毕后，所有goroutine都会阻塞在从ch这个channel的send or recv 操作上。因此runtime会报panic。你可以 将sieve放到一个单独的goroutine中运行，就像下面这样：

func main() {

go sieve()

time.Sleep(time.Second * 100)

}