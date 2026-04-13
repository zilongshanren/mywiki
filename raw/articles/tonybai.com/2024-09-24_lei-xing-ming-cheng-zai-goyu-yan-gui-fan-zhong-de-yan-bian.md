---
title: “类型名称”在Go语言规范中的演变
url: https://tonybai.com/2024/09/24/the-evolution-of-type-name-in-go-spec/
published: '2024-09-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# “类型名称”在Go语言规范中的演变

![](../../assets/a15ad5533ffa1004.png)


[本文永久链接](https://tonybai.com/2024/09/24/the-evolution-of-type-name-in-go-spec) – https://tonybai.com/2024/09/24/the-evolution-of-type-name-in-go-spec

[Go语言规范（The Go Programming Language Specification）](https://go.dev/ref/spec)是Go语言的核心文档，定义了该语言的语法、[类型系统](https://tonybai.com/2022/12/18/go-type-system)和运行时行为。Go语言规范的存在使得开发者在实现Go编译器时可以依赖一致的标准，它确保了语言的稳定性和一致性，特别是在类型系统设计中，Go团队通过规范推动了语言的简洁性、稳定性与可维护性。对于Go开发者而言，Go语言规范也是语法特性使用的参考手册(虽然语言规范读起来比较抽象和晦涩)。

Go语言规范由Google的Go核心开发团队维护和演进，这与[ISO标准的C/C++语言规范](https://isocpp.org/std/the-standard)有所不同。C和C++语言的ISO标准更新较慢，需经过复杂的全球共识和审核流程，而相比之下，Go语言的管理方式就显得更加灵活，也能够迅速适应新需求。

然而，这种灵活性也带来了潜在的弊端。随着新语法特性的引入和演进，一些已有的概念的含义可能会发生变化，导致前后的不一致性，从而让开发者感到困惑。例如，Go中的Type Name(类型名称)就经历了从最初的Named Type，到[Defined Type](https://tonybai.com/2021/12/02/go-has-implicit-type-convertion)和Alias Type，最终又回归到Named Type的过程。

近期Go语言之父之一的Robert Griesemer在Go官博发表了一篇名为”[What’s in an (Alias) Name?](https://go.dev/blog/alias-names)“的文章，其中就对Go spec中Type Name的历史演进做了回顾，这里我们就基于这段回顾对“类型名称(Type Name)”在Go语言规范中的演变做一下简要梳理，希望能帮助大家更好的理解Go。

## 1. Go规范中的Type Name（类型名称）

在Go语言规范中，Type Name是指给定类型的标识符，它为一个类型提供了唯一的名称。Type Name用于识别和引用各种类型，这包括Go内置(也叫预声明Predeclared Type)的基础类型(比如int、string)和用户自定义的类型，比如：

```
var x int // int是基础类型的Type Name
type MyInt int // MyInt是用户定义类型的Type Name
```


你可能会问，Go还有没有类型名称的类型吗？当然有了，有一些特殊的类型没有直接的类型名称。通常，这些类型是**匿名类型(Anonymous Type)**，即它们并没有通过命名来标识，主要的匿名类型包括：

- 字面量定义的复合类型（Composite Literals）

Go支持在代码中使用复合字面量来定义结构体、数组、切片、map等类型，而不为这些类型显式地定义名称。这些类型是在使用时定义的，并没有为其单独声明一个类型名称。

```
var data = struct { Name string; Age int }{"Alice", 30} // 匿名结构体类型
var arr = [5]int{1,2,3,4,5} // 匿名数组类型
var arr = []int{1, 2, 3} // 匿名切片类型
var m = map[string]int{"foo": 1, "bar": 2} // 匿名map类型
```


- 匿名函数类型

Go支持函数作为一等公民，函数本身可以作为类型，当定义匿名函数（即未命名函数）时，这些函数没有类型名称。

```
var f = func() int { //匿名函数类型func() int
return 42
}
```


Type Name是一个广泛的概念，在Go spec中，Go设计者们将其做了细分，比如Named Type、Defined Type等。那么随着Go版本的变化，Go中的Type Name的分类有哪些重要的演进和变化呢，下面我们就重点说明一下Go spec中Type Name分类的三次重要变化。

## 2. 初始阶段：简单而明确的Named Type (2009-2017)

Go 1.0是Go语言的首个正式发布版本，其中确立了类型名称的基础概念。在这一阶段，[Go的类型系统](https://tonybai.com/2022/12/18/go-type-system)已经具备了高度的简洁性和一致性，这也是该语言设计的核心原则之一。

在Go语言的早期阶段(2009-2017)，Go规范就确定了简单明确的Named Type的概念，它指的是通过下面语法定义的类型T：

```
type T existingType
```


这些通过类型声明定义的T被称为Named Type。而这里的existingType可以Predeclared的预声明类型（比如int、string），可以是已存在的Named Type，也可以是前面提到的匿名类型。

通过给现有类型赋予新名称来定义新的类型，与匿名类型等未命名类型形成鲜明对比。这种简单的分类满足了早期Go程序员的需求，为代码组织和类型系统提供了清晰的基础，提升了代码的可读性和模块化。

我们可以用示意图来展示这个阶段的Go类型名称分类：

![](../../assets/e5d59c778fb86543.png)


而Named Type的定义方式也可以用下图表示：

![](../../assets/91114cadb1ac6aac.png)


我们看到，可以基于Predeclare Type、匿名类型以及已存在的Named Type来定义一个新的Named Type。并且，Named Type具有一些专有特性，比如可拥有自己的方法、只与自身类型赋值兼容，不与其底层类型直接兼容（除非进行显式类型转换）等。

## 3. 变革之始：别名类型的引入 (Go 1.9, 2017)

然而，随着[Go 1.9](https://tonybai.com/2017/07/14/some-changes-in-go-1-9)在2017年引入别名类型(Alias Type)，情况开始变得复杂：

```
type T = Q // T为Q类型的别名类型
```


别名类型的引入是为了支持大规模代码库的重构，但它也模糊了Named Type的界限，因为别名也是一个类型名称。

为了应对这一变化，Go团队引入了”Defined Type”的概念以代替界限模糊的Named Type，用以特指通过类型定义(type T Q)创建的新类型。

这样改动后，整个Go类型系统的类型名称分类就变成如下示意图中的状态了：

![](../../assets/1a0843490e47a909.png)


Defined Type定义和Alias Type的定义分别如下：

![](../../assets/b2be75d7c6f3a644.png)


两者看起来差别不大，但只有Defined Type才拥有专有属性，比如可拥有自己的方法、只与自身类型赋值兼容等。我们也可以为Alias Type定义方法，但那个方法属于原类型。

## 4. 泛型时代的到来：概念的重塑 (Go 1.18, 2022)

2022年，[Go 1.18的发布](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)标志着Go语言进入了[泛型时代](https://tonybai.com/2022/03/25/intro-generics)，这一重大特性的引入再次挑战了现有的类型分类方式。

比如类型参数也是类型，它们有名称，与Defined Type一样，两个不同命名的类型参数表示不同的类型。换句话说，类型参数是Named Type，而且它们的行为在某些方面与Go原始的Named Type类似。更重要的是，Go的Predeclare Type（如int、string等）只能通过它们的名称来访问，并且像Defined Type和类型参数一样，如果它们的名称不同，它们也会不同，这样预声明的类型也变成了Named Type。

为了适应泛型，Go规范重新引入了Named Type，并将其范围扩大到包括预声明类型、Defined Type、类型参数以及部分情况下的别名类型。

重新引入Named Type后，Defined Type依然得以保留，整个Go系统类型的最新类型名称分类状态如下图所示：

![](../../assets/eb6863907a95172f.png)


## 5. 当前的权衡

在”[What’s in an (Alias) Name?](https://go.dev/blog/alias-names)“的文章中，Robert还提到了学院派类型系统理论中的Nominal type（名义类型）和Structural type（结构类型)两个概念，虽然Go spec目前完全没有使用这两个概念。

[Nominal type](https://en.wikipedia.org/wiki/Nominal_type_system)，也叫名义类型。这种类型的身份（identity）明确地与其名称相关联。两个类型即使结构完全相同，如果名称不同，也被视为不同的类型。像Go 1.18以后spec中的预声明类型（如int、string等）、Defined types（通过type关键字定义的类型）和类型参数都属于这种类型，这大体与Named Type是重叠的。

而[Structural type](https://en.wikipedia.org/wiki/Structural_type_system)（结构类型）的类型的身份仅取决于其结构或组成，而不依赖于名称。如果两个类型的结构相同，它们就被视为相同的类型，即使它们可能有不同的名称，像Go中的接口类型(在某种意义上)、通过类型字面量创建的类型（如匿名结构体、函数类型等）等都可以归属与这种类型。值得注意的是，指向类型字面量的别名类型（如type AliasName = struct{ … }）也可看作是structural type。

不过Robert也提到了，后续**Go还会继续沿用Named Type、Defined Type等术语**，而不会用这些学院派的类型术语来更新Go spec，这主要有几方面考虑：

- 历史一致性：Go语言从早期就使用了named type、defined type等术语。突然改变可能会导致现有文档、教程和代码库的混乱。
- 概念特殊性：Go的类型系统有其特殊性，不完全符合传统的nominal/structural二分法。例如，Go的接口类型结合了nominal和structural的特性。这么做，也可以避免引起其他语言中该术语用法的混淆。
- 实用性考虑：”named type”、”defined type”等术语在Go的上下文中有明确的含义，直接对应于语言的特定特性和语法结构。这使得它们在讨论Go特定概念时更加实用。

## 6. 小结

本文基于Robert的文章讲述了Go语言类型系统中的类型名称的演变历程。我们回顾了Type Name在Go语言规范中的重要变化，从最初的简单Named Type到后来的Defined Type和Alias Type，再到引入泛型时代后的重新定义Named Type。每一次变化不仅反映了Go语言的不断发展，也展示了Go团队在应对复杂性和保持语言简洁性之间的平衡。

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