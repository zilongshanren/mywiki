---
title: 组织Golang代码
url: https://tonybai.com/2014/10/21/organize-golang-code/
published: '2014-10-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 组织Golang代码

本月初golang[官方blog](http://blog.golang.org)(需要自己搭梯子)上发布了一篇[文章](http://blog.golang.org/io2014)，简要介绍了近几个月Go在一 些技术会议上（比如Google I/O、Gopher SummerFest等）的主题分享并伴有slide链接。其中David Crawshaw的“[Organizing Go Code](https://talks.golang.org/2014/organizeio.slide#1)”对Golang的代码风格以及工程组 织的最佳实践进行的总结很是全面和到位，这里按Slide中的思路和内容翻译和摘录如下（部分伴有我个人的若干理解）。

**一、包 (Packages)**

**1、Golang程序由package组成**

所有Go源码都是包得一部分。

每个Go源文件都起始于一条package语句。

Go应用程序的执行起始于main包。

package main

import "fmt"

func main() {

fmt.Println("Hello, world!")

}

对小微型程序而言，你可能只需要编写main包内的源码。

上面的HelloWorld程序import了fmt包。

函数Println定义在fmt包中。

**2、一个例子：fmt包**

// Package fmt implements formatted I/O.

package fmt

// Println formats using the default formats for its

// operands and writes to standard output.

func Println(a …interface{}) (n int, err error) {

…

}

func newPrinter() *pp {

…

}

Println是一个导出(exported)函数，它的函数名以大写字母开头，这意味着它允许其他包中的函数调用它。

newPrinter函数则并非导出函数，它的函数名以小写字母开头，它只能在fmt包内部被使用。

**3、包的形态**(Shape)

包是有关联关系的代码的集合，包规模可大可小，大包甚至可以横跨多个源文件。

同一个包的所有源文件都放在一个单一目录下面。

net/http包共由18个文件组成，导出了超过100个名字符号。

errors包仅仅由一个文件组成，并仅导出了一个名字符号。

**4、包的命名**

包的命名应该短小且有含义。

不要使用下划线，那样会导致包名过长;

不要过于概况，一个util包可能包含任何含义的代码；

使用io/ioutil，而不是io/util

使用suffixarray，而不是suffix_array

包名是其导出的类型名以及函数名的组成部分。

buf := new(bytes.Buffer)

仔细挑选包名

为用户选择一个好包名。

**5、对包的测试**

通过文件名我们可以区分出哪些是测试用源文件。测试文件以_test.go结尾。下面是一个测试文件的样例：

package fmt

import "testing"

var fmtTests = []fmtTest{

{"%d", 12345, "12345"},

{"%v", 12345, "12345"},

{"%t", true, "true"},

}

func TestSprintf(t *testing.T) {

for _, tt := range fmtTests {

if s := Sprintf(tt.fmt, tt.val); s != tt.out {

t.Errorf("…")

}

}

}

**二、代码组织(Code organization)**

**1、工作区介绍(workspace)**

你的Go源码被放在一个工作区(workspace)中。

一个workspace可以包含多个源码库(repository)，诸如git，hg等。

Go工具知晓一个工作区的布局。

你无需使用Makefile，通过文件布局，我们可以完成所有事情。

若文件布局发生变动，则需重新构建。

$GOPATH/

src/

github.com/user/repo/

mypkg/

mysrc1.go

mysrc2.go

cmd/mycmd/

main.go

bin/

mycmd

**2、建立一个工作区**

mkdir /tmp/gows

GOPATH=/tmp/gows

GOPATH环境变量告诉Go工具族你的工作区的位置。

go get github.com/dsymonds/fixhub/cmd/fixhub

go get命令从互联网网下载源代码库，并将它们放置在你的工作区中。

包的路径对Go工具来说很是重要，使用"github.com"意味着Go工具知道如何去获取你的源码库。

go install github.com/dsymonds/fixhub/cmd/fixhub

go install命令构建一个可执行程序，并将其放置在$GOPATH/bin/fixhub中。

**3、我们的工作区**

$GOPATH/

bin/fixhub # installed binary

pkg/darwin_amd64/ # compiled archives

code.google.com/p/goauth2/oauth.a

github.com/…

src/ # source repositories

code.google.com/p/goauth2/

.hg

oauth # used by package go-github

…

github.com/

golang/lint/… # used by package fixhub

.git

google/go-github/… # used by package fixhub

.git

dsymonds/fixhub/

.git

client.go

cmd/fixhub/fixhub.go # package main

go get获取多个源码库。

go install使用这些源码库构建一个二进制文件。

**4、为何要规定好文件布局**

在构建时使用文件布局意味着可以更少的进行配置。

实际上，它意味着无配置。没有Makefile，没有build.xml。

在配置上花的时间少了，意味着在编程上可以花更多的时间。

Go社区中所有人都使用相同的布局，这会使得分享代码更加容易。

Go工具在一定程度上对Go社区的建设起到了帮助作用。

**5、你的工作区在哪？**

你可以拥有多个工作区，但大多数人只使用一个。那么你如何设置GOPATH这个环境变量呢？一个普遍的选择是：

GOPATH=$HOME

这样设置会将src、bin和pkg目录放到你的Home目录下。（这会很方便，因为$HOME/bin可能已经在你的PATH环境变量中了）。

**6、在工作区下工作**

CDPATH=$GOPATH/src/github.com:$GOPATH/src/code.google.com/p

$ cd dsymonds/fixhub

/tmp/gows/src/github.com/dsymonds/fixhub

$ cd goauth2

/tmp/gows/src/code.google.com/p/goauth2

$

将下面shell函数放在你的~/.profile中：

gocd () { cd `go list -f '{{.Dir}}' $1` }

$ gocd …/lint

/tmp/gows/src/github.com/golang/lint

$

**三、依赖管理**

**1、在生产环境中，版本很重要**

go get总是获取最新版本代码，即使这些代码破坏了你的构建。

这在开发阶段还好，但当你在发布阶段时，这将是一个问题。

我们需要其他工具。

**2、版本****管理**

我最喜欢的技术：vendoring。

当构建二进制程序时，将你关心的包导入到一个_vendor工作区。

GOPATH=/tmp/gows/_vendor:/tmp/gows

注：

1、在build时，我们通过构建脚本，临时修改GOPATH（GOPATH := ${PWD}/_vendor:${GOPATH}）， 并将_vendor放置在主GOPATH前面，利用go build解析import包路径解析规则，go build优先得到_vendor下的第三方包信息，这样即便原GOPATH下有不同版本的相同第三方库，go build也会优先导入_vendor下的同名第三方库。

2、go的相关工具在执行类似test这样的命令时会忽略前缀为_或.的目录，这样_vendor下的第三方库的test等操作将不会被执行。

当构建库时，将你关心的包导入你的源码库。重命名import为：

import "github.com/you/proj/vendor/github.com/them/lib"

长路径，不过对于自动化操作来说不算什么问题。写一个Go程序吧！

另外一种技术：gopkg.in。提供带版本的包路径：

gopkg.in/user/pkg.v3 -> github.com/user/pkg (branch/tag v3, v3.N, or v.3.N.M)

**四、命名**

**1、命名很重要**

程序源码中充满着各种名字。名字兼具代价和收益。

代价：空间与时间

当阅读代码时，名字需要短时记忆

你只能适应这么多，更长的名字需要占据更多的空间。

收益：信息

一个好名字不仅仅是一个指代对象，它还能够传达某种信息。

使用尽可能最短的名字用于在上下文中携带合理数量的信息。

在命名上花些时间（值得的）。

**2、命名样式**

使用camelCase，不要用下划线。

本地变量名字应该短小，通常由1到2个字符组成。

包名同行是一个小写词。

全局变量应该拥有长度更长的名字。

不要结巴！

使用bytes.Buffer，不要用bytes.ByteBuffer

使用zip.Reader，不要用zip.ZipReader

使用errors.New，不要用errors.NewError

使用r，不用bytesReader

使用i，不用loopIterator

**3、文档化注释**

文档化注释放在导出标示符的声明之前：

// Join concatenates the elements of elem to create a single string.

// The separator string sep is placed between elements in the resulting string.

func Join(elem []string, sep string) string {

godoc工具可以解析出这些注释并将其展示在Web上：

func Join

func Join (a []string, sep string) string

Join concatenates the elements of a to create a single string. The separetor string sep is placed between elements in the resulting string.

**4、写文档化的注释**

文档化的注释应用使用英文句子和段落。

除了为预定义格式进行的缩进外，没有其他特殊格式。

文档化注释应该以要描述的名词开头。

// Join concatenates… good

// This function… bad

包的文档应该放在包声明语句之前：

// Package fmt…

package fmt

在godoc.org上阅读Go世界的文档，比如：

godoc.org/code.google.com/p/go.tools/cmd/vet

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论