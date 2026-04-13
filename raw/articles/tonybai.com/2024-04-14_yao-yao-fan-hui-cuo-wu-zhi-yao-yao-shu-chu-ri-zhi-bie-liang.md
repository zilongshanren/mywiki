---
title: 要么返回错误值，要么输出日志，别两样都做
url: https://tonybai.com/2024/04/14/either-return-error-or-log-them-do-not-do-both/
published: '2024-04-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 要么返回错误值，要么输出日志，别两样都做

![](../../assets/8fc1caf673a7f0ff.png)


[本文永久链接](https://tonybai.com/2024/04/14/either-return-error-or-log-them-do-not-do-both) – https://tonybai.com/2024/04/14/either-return-error-or-log-them-do-not-do-both

## 1. 缘起

这周，一个产品团队内进行Go代码评审时，得到了一个结论：所有的if err != nil的地方都应该输出错误日志。然而，这种做法并不是最佳实践，它存在一些问题。

首先，打印过多的错误日志会导致日志文件变得冗长和难以阅读。其次，重复的错误信息会增加冗余。此外，每一层都打印错误日志，一旦错误信息设计不当，可能会导致上下文信息的丢失。

让我们来看一个示例，说明为什么同时输出错误日志和返回错误值会导致问题。假设我们有一个五层的Go函数调用栈，其中最底层的函数level4Function出现了一个错误：

```
package main
import (
"fmt"
"log"
)
func main() {
if err := topFunction(); err != nil {
log.Printf("Error: %v", err)
}
}
func topFunction() error {
err := level1Function()
if err != nil {
log.Printf("topFunction: %v", err)
return err
}
return nil
}
func level1Function() error {
err := level2Function()
if err != nil {
log.Printf("level1Function: %v", err)
return err
}
return nil
}
func level2Function() error {
err := level3Function()
if err != nil {
log.Printf("level2Function: %v", err)
return err
}
return nil
}
func level3Function() error {
err := level4Function()
if err != nil {
log.Printf("level3Function: %v", err)
return err
}
return nil
}
func level4Function() error {
err := fmt.Errorf("something went wrong")
log.Printf("level4Function: %v", err)
return err
}
```


在这个示例中，我们在每个函数中都输出错误日志并返回错误值。我们运行一下这个程序：

```
$go run main.go
2024/04/14 23:10:05 level4Function: something went wrong
2024/04/14 23:10:05 level3Function: something went wrong
2024/04/14 23:10:05 level2Function: something went wrong
2024/04/14 23:10:05 level1Function: something went wrong
2024/04/14 23:10:05 topFunction: something went wrong
2024/04/14 23:10:05 Error: something went wrong
```


当我们运行程序时，日志文件会出现重复的错误信息，并且上下文信息不易于进行链式追踪，因为每个函数只打印了特定错误的信息，而没有提供之前错误的上下文。

## 2. 好的实践技巧

为了解决上述问题，我们需要采用一种更好的实践方法。面向调用层次较深的函数调用栈，我们应该**只在最顶层的函数中输出错误日志，而在下层函数中返回错误值**。但是，我们需要精心构造错误值，以形成基于wrapped error的错误链。

让我们修改示例代码，按照最佳实践进行错误处理：

```
package main
import (
"fmt"
"log"
)
func main() {
if err := topFunction(); err != nil {
log.Printf("Error: %v", err)
}
}
func topFunction() error {
err := level1Function()
if err != nil {
return fmt.Errorf("topFunction: %w", err)
}
return nil
}
func level1Function() error {
err := level2Function()
if err != nil {
return fmt.Errorf("level1Function: %w", err)
}
return nil
}
func level2Function() error {
err := level3Function()
if err != nil {
return fmt.Errorf("level2Function: %w", err)
}
return nil
}
func level3Function() error {
err := level4Function()
if err != nil {
return fmt.Errorf("level3Function: %w", err)
}
return nil
}
func level4Function() error {
err := fmt.Errorf("something went wrong")
return fmt.Errorf("level4Function: %w", err)
}
```


在这个修改后的示例中，我们在每个函数中使用fmt.Errorf+%w将错误包装为一个wrapped error，并将前一层的错误作为参数传递。通过这种方式，我们构建了一个错误链，其中每个错误都包含了之前发生的错误上下文。在最顶层的main函数中，我们使用日志库输出错误日志，下面是示例程序的运行结果：

```
2024/04/14 23:12:16 Error: topFunction: level1Function: level2Function: level3Function: level4Function: something went wrong
```


我们看到：通过这种方法，我们避免了重复的错误日志，并保留了错误的上下文信息，快速定位了根因。当运行修改后的程序时，我们会看到日志文件中只打印了完整的错误链，而不是重复的错误信息。通过调用链和精心设计的错误上下文，我们还可以看到函数调用链，这使得错误的调试和处理变得更加方便和可靠。

关于错误链的使用，大家可以看看我之前撰写的《[Go错误处理：错误链使用指南](https://tonybai.com/2023/05/14/a-guide-of-using-go-error-chain/)》一文。

## 3. 小结

在前面的示例中，我们展示了同时输出错误日志和返回错误值的问题，并介绍了如何使用wrapped error来构建错误链。通过合理地处理错误，我们可以提高代码的可读性和可维护性，同时也有助于快速定位和解决问题。

总之，在编写Go代码时，请记住要么返回错误值，要么输出日志，不要两者都做。通过合理地处理错误，我们可以编写出更可靠、更易于调试的代码。

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论