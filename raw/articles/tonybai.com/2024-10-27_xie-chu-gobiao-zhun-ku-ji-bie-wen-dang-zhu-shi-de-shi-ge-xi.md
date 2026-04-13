---
title: 写出Go标准库级别文档注释的十个细节
url: https://tonybai.com/2024/10/27/ten-details-when-using-documentation-comments/
published: '2024-10-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 写出Go标准库级别文档注释的十个细节

![](../../assets/bf30df3dd836b3a0.png)


[本文永久链接](https://tonybai.com/2024/10/27/ten-details-when-using-documentation-comments) – https://tonybai.com/2024/10/27/ten-details-when-using-documentation-comments

Go语言以其优秀的工具链、“开箱即用”的标准库和相对完善的文档生态而闻名。Go通过代码中的[文档注释(Doc Comments)](https://go.dev/doc/comment)生成相关包、类型、函数以及方法的说明文档。Go标准库中的文档注释不仅为使用者提供了清晰的指引，更为广大Go开发人员树立了高质量技术文档的标杆。

然而，在日常开发中，很多Go开发者往往只注意到文档注释的基本格式要求，而忽略了一些能让文档质量更上一层楼的细节。这些细节虽小，但却是区分专业级别和业余水平代码的重要标志。

在这篇文章中，我就挑出十个在编写Go文档注释时容易被忽视的关键细节，和大家说说，希望能帮助大家提升Go代码文档注释的level。

## 1. 注释缩进的陷阱

很多开发者在写多行注释时会不经意产生缩进问题，例如：

```
// TODO Revisit this design. It may make sense to walk those nodes
// only once. // 错误示例：第二行有缩进
```


这种缩进会使第二行被解析为代码块。正确的做法是保持未缩进：

```
// TODO Revisit this design. It may make sense to walk those nodes
// only once.
```


## 2. 并发安全性说明

对于类型(Type)的文档注释，**默认情况下读者会认为该类型仅适用于单个goroutine**。如果类型支持并发访问，应该显式地明确注释说明：

```
// Regexp is the representation of a compiled regular expression.
// A Regexp is safe for concurrent use by multiple goroutines,
// except for configuration methods, such as Longest.
type Regexp struct {
...
}
```


## 3. 零值行为说明

如果类型支持零值可用或零值具有特殊含义，应当在注释中显式说明：

```
// Buffer is a variable-sized buffer of bytes with Read and Write methods.
// The zero value for Buffer is an empty buffer ready to use.
type Buffer struct {
...
}
```


## 4. 避免实现细节

函数的文档注释应该关注其行为和返回值，而不是实现细节。除非是性能关键的场景需要说明算法复杂度，否则应该避免在注释中描述算法实现：

```
// 好的示例：关注行为
// Sort sorts data in ascending order as determined by the Less method.
// It makes O(n*log(n)) calls to data.Less and data.Swap.
// 不好的示例：暴露实现细节
// Sort uses quicksort algorithm to sort data...
```


## 5. 返回布尔值的函数注释惯例

对于返回布尔值的函数，按惯例最好**使用”reports whether”的描述方式**，避免使用”or not”：

```
// HasPrefix reports whether the string s begins with prefix.
func HasPrefix(s, prefix string) bool
```


## 6. “构造函数”在文档中的位置

Go自身没有构造函数的专有语法，但当一个包中包含返回类型T或指针*T(包括伴随返回一个error的情况)的包顶层函数时，这些函数会被视为“构造函数”。这些**构造函数在godoc中会被显示在T类型的下面**，看起来像是T类型的方法，这的确容易“误导”一些Go新手：

```
$go doc time
... ...
type Duration int64
func ParseDuration(s string) (Duration, error)
func Since(t Time) Duration
func Until(t Time) Duration
... ...
```


在pkg.go.dev中，这些“构造函数”在文档中会自动显示在类型T类型旁边：

![](../../assets/c5dfd656fb4e8761.png)


这意味着我们在写“构造函数”的文档时**应当注意与类型文档的一致性**：

```
// NewReader creates a new Reader reading from r.
// It is similar to NewReaderSize with the default buffer size.
func NewReader(r io.Reader) *Reader
// Reader implements buffering for an io.Reader object.
type Reader struct {
// ...
}
```


## 7. 顶层函数的并发安全性说明

对于顶层函数（包级别的导出函数），**默认情况下是假定它们是并发安全的**，因此不需要显式说明这一点：

```
// 不必要的说明
// Parse parses the regular expression and returns a Regexp object.
// This function is safe for concurrent use. // 这行是多余的
func Parse(expr string) (*Regexp, error)
// 正确的做法
// Parse parses the regular expression and returns a Regexp object.
func Parse(expr string) (*Regexp, error)
```


## 8. 方法的并发安全性说明

与包的顶层函数不同，类型的方法则是默认被认为仅限单个goroutine使用，即不是并发安全的。如果某些方法支持并发调用，应当在方法的文档注释中显式给予说明：

```
// Load returns the value stored in the map for a key.
// It is safe for concurrent use by multiple goroutines.
func (m *Map) Load(key interface{}) (value interface{}, ok bool)
```


## 9. 方法接收器命名一致对文档展示的影响

在编写类型的多个方法时，应该使用统一的接收器(receiver)命名，这样可以提高文档的一致性和可读性，避免不必要的命名变化：

```
// 不好的示例：接收器命名不一致
func (buffer *Buffer) Read(p []byte) (n int, err error)
func (b *Buffer) Write(p []byte) (n int, err error)
func (buf *Buffer) Cap() int
// 好的示例：统一使用b作为接收器名
func (b *Buffer) Read(p []byte) (n int, err error)
func (b *Buffer) Write(p []byte) (n int, err error)
func (b *Buffer) Cap() int
```


通过下图，我们也可以看到一致的方法receiver参数命名在文档中体现出的一致性，这种一致性不仅让文档看起来更专业，也让使用者在阅读文档时能更专注于方法的功能本身，而不是被不同的命名所分散注意力：

![](../../assets/2dec9448712f2ff2.png)


此外，选择方法接收器名称时的建议使用简短的命名（通常是类型名的第一个小写字母，比如上面的b），避免使用this、self等其他语言常用的命名。即使是单个方法，也要遵循这个命名约定，为后续可能的方法扩展做准备。

## 10. 废弃标记的使用

当需要标记某个API为废弃时，应该及时使用”Deprecated:”前缀予以标记，并**提供替代方案**，如下面的strings.Title函数：

```
// Title returns a copy of the string s with all Unicode letters that begin words
// mapped to their Unicode title case.
//
// Deprecated: The rule Title uses for word boundaries does not handle Unicode
// punctuation properly. Use golang.org/x/text/cases instead.
func Title(s string) string {
... ...
}
```


![](../../assets/a5c3f63e71fab90c.png)


这些细节虽小,但都会影响到文档的可读性和代码的可维护性。良好的文档习惯需要在日常编码中持续积累和保持。

Go团队将代码的可读性和可维护性放到至关重要的位置上，而编写高质量的文档注释就是提升代码可读可维护性的重要实践。从注释的缩进、并发安全性说明，到零值行为、构造函数文档等细节，这些看似微小的考量都在传递着重要的信息。通过遵循这些最佳实践，我们不仅能让文档更加清晰易懂，还能帮助团队减少沟通成本，提高开发效率。更重要的是，这些实践能帮助我们培养更专业的编码习惯，写出更加规范的代码，让我们在日常开发中持续积累这些好的习惯，让代码文档更接近Go标准库的专业水准^_^。

要了解更多关于Go文档注释的细节，可以阅读[Go Doc Comments](https://go.dev/doc/comment)。

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