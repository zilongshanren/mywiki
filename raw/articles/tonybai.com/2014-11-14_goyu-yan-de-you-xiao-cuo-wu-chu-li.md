---
title: Go语言的有效错误处理
url: https://tonybai.com/2014/11/14/effective-error-handling-in-go/
published: '2014-11-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言的有效错误处理

中午闲暇翻看[Daniel Morsing](http://morsmachine.dk/)的“[The Go scheduler](http://morsmachine.dk/go-scheduler)”时，发现其另外一篇短文“[Effective error handling in Go](http://morsmachine.dk/error-handling)”，文章不长，但感觉对[Go](http://tonybai.com/tag/go)中错误处理方法总结的还是比较到位的，这里译之供大家参考。

**一、简介**

Go语言受到诟病最多的一项就是其错误处理机制。如果显式地检查和处理每个error，这恐怕的确会让人望而却步。你可以试试这里列出的几个方法，以避免你走入错误处理方法的误区当中去。

**二、****在缩进区处理错误**

当使用Go语言编写代码时，首选下面这样的错误处理方法：

f, err := os.Open(path)

if err != nil {

// handle error

}

// do stuff

而不是下面这样的：

f, err := os.Open(path)

if err == nil {

// do stuff

}

// handle error

按照上面的方法处理错误，处理正常情况的代码读起来就显得通篇连贯了。

**三、定义你自己的error****s**

做好如何正确进行错误处理的第一步就是要了解error是什么。如果你设计实现的包会因某种原因发生某种错误，你的包用户将会对错误的原因很感兴趣。为了满足用户的需求，你需要实现error接口，简单做起来就像这样：

type Error string

func (e Error) Error() string { return string(e) }

现在，你的包用户通过执行一个type assertion就可以知道是否是你的包导致了这个错误：

result, err := yourpackage.Foo()

if ype, ok := err.(yourpackage.Error); ok {

// use ype to handle error

}

通过这个方法，你还可以向你的包用户暴露更多地结构化错误信息：

type ParseError struct {

File *File

Error string

}

func (oe *ParseError) Error() string {//译注：原文中这里是OpenError

// format error string here

}

func ParseFiles(files []*File) error {

for _, f := range files {

err := f.parse()

if err != nil {

return &ParseError{ //译注：原文中这里是OpenError

File: f,

Error: err.Error(),

}

}

}

}

通过这种方法，你的用户就可以明确地知道到底哪个文件出现解析错误了。（译注：从这里看到的go语言error设计之内涵，让我想起了Rob Pike大神的一篇Blog："[少即是级数级的多](http://commandcenter.blogspot.com.au/2012/06/less-is-exponentially-more.html)"）

不过包装error时要小心，当你将一个error包装起来后，你可能会丢失一些信息：

var c net.Conn

f, err := DownloadFile(c, path)

switch e := err.(type) {

default:

// this will get executed if err == nil

case net.Error:

// close connection, not valid anymore

c.Close()

return e

case error:

// if err is non-nil

return err

}

// do other things.

如果你包装了net.Error，上面这段代码将无法知道是由于网络问题导致的失败，会继续使用这条无效的链接。

有一条经验规则：如果你的包中使用了一个外部interface，那么不要对这个接口中方法返回的任何错误，使用你的包的用户可能更关心这些错误，而不是你包装后的错误。

**四、将错误作为状态**

有时，当遇到一个错误时，你可能会停下来等等。这或是因为你将延迟报告错误，又或是因为你知道如果这次报告后，后续你会再报告同样的错误。

第一种情况的一个例子就是bufio包。当一个bufio.Reader遇到一个错误时，它将停下来保持这个状态，直到buffer已经被清空。只有在那时它才会报告错误。

第二种情况的一个例子是go/loader。当你通过某些参数调用它导致错误时，它会停下来保持这个状态，因为它知道你很可能会使用同样地参数再次调用它。

**五、使用函数以避免重复****代码**

如果你有两段重复的错误处理代码，你可以将它们放到一个函数中去：

func handleError(c net.Conn, err error) {

// repeated error handling

}

func DoStuff(c net.Conn) error {

f, err := downloadFile(c, path)

if err != nil {

handleError(c, err)

return err

}

f, err := doOtherThing(c)

if err != nil {

handleError(c, err)

return err

}

}

优化后的实现方法如下：

func handleError(c net.Conn, err error) {

if err == nil {

return

}

// repeated error handling

}

func DoStuff(c net.Conn) error {

defer func() { handleError(c, err) }()

f, err := downloadFile(c, path)

if err != nil {

return err

}

f, err := doOtherThing(c)

if err != nil {

return err

}

}

这就是全部了。就Go语言错误处理而言，我知道的就这么多了。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

good http://tonybai.com/2014/11/14/effective-error-handling-in-go/