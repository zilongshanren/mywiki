---
title: 世界读书日：带你走近Go语言编程思维
url: https://tonybai.com/2022/04/23/taking-a-closer-look-at-programming-thinking-in-go/
published: '2022-04-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 世界读书日：带你走近Go语言编程思维

![](../../assets/590d0fb1dd04b53c.jpeg)


[本文永久链接](https://tonybai.com/2022/04/23/taking-a-closer-look-at-programming-thinking-in-go) – https://tonybai.com/2022/04/23/taking-a-closer-look-at-programming-thinking-in-go

经过十几年的演化和发展，Go语言在全世界范围内已经拥有了百万级别的拥趸，在这些开发者当中，除了一部分新入行的编程语言初学者之外，更多的是从其他编程语言阵营转过来的开发者。由于Go语言上手容易，在转Go的初期大家很快就掌握了Go的语法。

但在编写更多Go代码之后，很多人发现自己写的Go代码总是感觉很别扭，并且总是尝试在Go语言中寻找自己上一门语言中熟悉的语法元素。自己的Go代码风格似乎和Go标准库、主流Go开源项目的代码在思考角度和使用方式上存在不小差异，并且每每看到Go核心开发团队的代码时总有一种醍醐灌顶的感觉。出现这种情况的主要原因就是大脑中上一门编程语言的思维方式在“作祟”。

本文将通过[《Go语言精进之路：从新手到高手的编程思想、方法与技巧》](https://item.jd.com/13694000.html)这本书的内容来详细看一看编程语言与编程思维的关系以及Go语言的编程思维究竟是什么，以帮助大家更加深入地理解Go编程。

![](../../assets/e4d665b3ee6269f2.png)


了解Go编程思维之前，我们先看看思维与语言之间究竟有什么联系呢？

### 1.语言与思维——来自大师的观点

在人类自然语言学界有一个很著名的假说——“萨丕尔—沃夫假说”，这个假说的内容是这样的：“**语言影响或决定人类的思维方式**。”

说到这个假说，我们不能不提及在2017年年初国内上映了一部口碑不错的美国科幻大片《降临》，这部片子改编自雨果奖获得者华裔科幻小说家Ted姜的《你一生的故事》。片中主线剧情的理论基础就是“萨丕尔—沃夫假说”。更夸张的是片中直接将该假说应用到外星人语言上，将其扩展到宇宙范畴。片中的女主作为人类代表与外星人沟通，并学会了外星语言，从此思维大变，拥有了预知未来的“超能力”，这也算是语言影响思维的极致表现了。

奇妙的是，在编程语言界，有位大师级人物也有着与“萨丕尔-沃夫假说”异曲同工的观点和认知，他就是首届图灵奖得主、著名计算机科学家艾伦·佩利（Alan J. Perlis），他从另外一个角度提出：“不能影响到你的编程思维方式的编程语言不值得去学习和使用。”

### 2.现实中的“投影”

从上述大师们的理论和观点，我们看到了语言与思维之间存在着某种联系。那么两者间的这种联系在真实编程世界中的投影又是什么样子的呢？我们来看一个简单的编程问题——素数筛：

-
问题描述：素数是一个自然数，它具有两个截然不同的自然数除数：1和它本身。这里的问题是如何找到小于或等于给定整数n的素数。针对这个问题，我们可以采用埃拉托斯特尼素数筛算法。

-
算法描述：先用最小的素数2去筛，把2的倍数剔除掉；下一个未筛除的数就是素数（这里是3）。再用这个素数3去筛，筛除掉3的倍数… 这样不断重复下去，直到筛完为止（算法图示见图1）。


![](../../assets/88c32228ab30e3b6.gif)



下面是该素数筛算法的不同编程语言的实现版本。

#### （1）C语言版本

```
// sieve.c
#include <stdio.h>
#define LIMIT 50
#define PRIMES 10
void sieve() {
int c, i,j,numbers[LIMIT], primes[PRIMES];
for (i=0;i<LIMIT;i++){
numbers[i]=i+2; /*fill the array with natural numbers*/
}
for (i=0;i<LIMIT;i++){
if (numbers[i]!=-1){
for (j=2*numbers[i]-2;j<LIMIT;j+=numbers[i])
numbers[j]=-1; /* 筛除非素数 */
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


#### （2）Haskell版本

```
// sieve.hs
sieve [] = []
sieve (x:xs) = x : sieve (filter (\a -> not $ a `mod` x == 0) xs)
n = 100
main = print $ sieve [2..n]
```


#### （3）Go语言版本

```
// sieve.go
func Generate(ch chan<- int) {
for i := 2; ; i++ {
ch <- i
}
}
func Filter(in <-chan int, out chan<- int, prime int) {
for {
i := <-in
if i%prime != 0 {
out <- i
}
}
}
func main() {
ch := make(chan int)
go Generate(ch)
for i := 0; i < 10; i++ {
prime := <-ch
print(prime, "\n")
ch1 := make(chan int)
go Filter(ch, ch1, prime)
ch = ch1
}
}
```


对比上述的三个语言版本的素数筛算法的实现，我们看到：

-
C版本的素数筛程序是一个常规实现。它定义了两个数组：numbers和primes，“筛”的过程在numbers这个数组中进行（即基于纯内存修改），非素数的数组元素被设置为-1，便于后续提取；

-
Haskell版本采用了函数递归的思路，通过“filter操作集合”，用下面谓词（过滤条件）筛除素数的倍数，将未筛除的数的集合作为参数传递归递给下去；


```
\a -> not $ a `mod` x == 0；
```


- Go版本程序实现了一个并发素数筛，它采用的是goroutine的并发组合。程序从素数2开始，依次为每个素数建立一个goroutine，用于作为筛除该素数的倍数。ch指向当前最新输出素数所位于的筛子goroutine的源channel，这段代码来自于Rob Pike的一次关于并发的分享。Go版本程序的执行过程可以用图2立体的展现出来。

![](../../assets/1a8e9ccff460f162.gif)



### 3.Go语言原生编程思维

通过上述这个现实中的问题我们可以看到：面对同一个问题，来自不同编程语言的程序员给出了思维方式截然不同的解决方法：C的命令式思维、Haskell的函数式思维和Go的并发思维。结合“萨丕尔—沃夫假说”，我们可以得到一个未经理论证实但又确实对现实有影响的推论：**编程语言影响编程思维，或者说每种编程语言都有属于自己的原生编程思维**。

Go语言诞生较晚，大多数Gopher（包括笔者在内）第一语言都不是Go，都是“半路出家”从其他语言转过来的，如C、C++、Java、Python等。每种语言都有自己的原生编程思维。比如：C语言相信程序员，提供了指针和指针运算，让C程序员天马行空的发挥，接近底层的直接内存操作让C程序拥有很高的性能；C++支持多范式（命令式、OO和泛型），虽不强迫程序员使用某个特定的范式，但推荐使用最新代表现代语言发展特色的泛型等高级范式；Python语言更是形成了Pythonic规则来指导Python程序员写出符合Python思维或惯用法的代码。

经验告诉我们但凡属于某个编程语言的高质量范畴的代码，其必定是在这种编程语言原生思维下编写的代码。如果用A语言的思维去编写B语言的代码（比如用OO思维写C代码，用命令式的思维写Haskell代码等），那么你写出的代码多半无法被B语言社区所认可，更难以成为高质量代码的典范。并且，如果沿着这样的方向去学习和实践B语言，那么结果只能是“南辕北辙”，离编写出高质量代码的目标渐行渐远。

那Go原生编程思维究竟是什么呢？一门编程语言的编程思维是由语言设计者、语言实现团队、语言社区、语言使用者在长期的演化和实践中形成的一种统一的思维习惯、行为方式、代码惯用法和风格。Go语言从诞生到现在也近十年多了。经过Go设计哲学熏陶、Go开发团队的引导和教育、Go社区的实践，Go语言也渐渐形成了属于自己的原生编程思维，或者说形成了符合Go语言哲学的Go语言惯用法（idiomatic go）。它们是Go语言的精华，也是构建本书内容的骨架，并值得我们用一本书的规模去详细呈现。因此可以说阅读本书的过程也是学习和建立Go语言原生编程思维的过程。

### 4. 小结

本文详细介绍了编程语言与编程思维之间的联系。我们学习和使用一门编程语言，目标就是要用这门语言的原生思维方式去编写高质量代码。学习Go，就要用Go的原生编程思维去写Go代码，而不是用其他语言的思维方式。掌握Go原生编程思维就是我们通往高质量Go编程的学习方向和必经之路。如果您想要了解更多有关Go编程思维的内容，推荐您详细阅读我的新作《Go语言精进之路：从新手到高手的编程思想、方法与技巧》。

![](../../assets/686fc4f9a8565f62.jpeg)


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