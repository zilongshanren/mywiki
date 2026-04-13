---
title: 也谈Go语言编程 – Hello，Go!
url: https://tonybai.com/2012/08/17/hello-go/
published: '2012-08-17'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈Go语言编程 – Hello，Go!

**Go is expressive, concise, clean, and efficient. Its concurrency mechanisms make it easy to write programs that get the most out of multicore and networked machines, while its novel type system enables flexible and modular program construction. Go compiles quickly to machine code yet has the convenience of garbage collection and the power of run-time reflection. It's a fast, statically typed, compiled language that feels like a dynamically typed, interpreted language.**

**– 摘自 Go语言官方站点**

对于一门编程语言最深刻的喜欢莫过于对这门编程语言的设计理念的认同了，[Go语言](http://en.wikipedia.org/wiki/Go_(programming_language))是继[C语言](http://tonybai.com/tag/c)之后又一门让我有如此感觉的编程语言。

初听到这门语言的存在时，我皱了皱眉：怎么起了这么一个名字！绝大多数编程语言都以名词或人名命名(如C、Java、[Python](http://python.org)、[Ruby](http://ruby-lang.org)、 [Haskell](http://haskell.org)、Ada等)，而这门语言却用了一个日常生活中使用极为频繁的动词Go作为名字，这似乎有些太大众化了。不知为何，这个名字总是让 我联想到以前中国农村给小孩子常起的几个名字：二狗、牛娃等^_^。况且之前已经有很多IT产品也以Go作为名字(例 如，Thoughtworks公司出品的敏捷管理工具也叫[Go](http://www.thoughtworks-studios.com/go-agile-release-management))。

不过随着对这门语言的了解的深入，名字已不再是问题了。Go语言对我这个C程序员产生了强大的吸引力，原因如下：

* Go保持了与C语言一脉相承的理念：短小精悍、致力于成为系统编程语言、简洁而熟悉的C语言家族语法、静态编译型语言、保留了指针、运行高效；

* Go填平了C语言与生俱来的为数不少的"坑"；

* Go提升了编译速度，统一了源码组织、构建规范以及编码规范，让程序员更集中精力于问题域；

* Go改进了并发模型，在语言级别原生支持多核平台；

* Go语言起点高，以创新的设计以及甚小的代价兼容了现有主流编程范型(例如OO等)。

因此有人称Go为21世纪的C语言，我觉得不为过。从这篇文章开始，我将和大家一起走入Go语言的世界。

**一、安装Go**

Go语言官方站(从国内访问十分不稳定，时能时不能，原因你懂的)对Go安装有着较为详尽的说明。如果你使用的是Linux、Mac OS或Windows，那你应该可以很顺利地完成Go的安装。Go于今年上旬发布了第一个稳定版本Go 1，目前最新版本是1.0.2，可以从Google Code上的[Go项目](http://code.google.com/p/go)中下载。我的环境为Ubuntu 10.04 32-bit，下载[go1.0.2.linux-386.tar.gz](http://go.googlecode.com/files/go1.0.2.linux-386.tar.gz)后，解压到/usr/local/go下面：

$ ls /usr/local/go

api/ bin/ doc/ include/ LICENSE PATENTS README src/ VERSION

AUTHORS CONTRIBUTORS favicon.ico lib/ misc/ pkg/ robots.txt test/

然后将/usr/local/go/bin添加到你的PATH环境变量中，你就可以在任意目录下执行go程序了：

$ go version

go version go1.0.2

如果你得到上面的输出结果，可以断定你的Go安装成功了！

**二、第一个Go程序 – Hello, Go!**

我们建立一个用于编写Go程序的工作目录go-examples，其绝对路径为/home/tonybai/go-examples。好了，开始 编写我们的第一个Go程序。

我们在go-examples下创建一个文件hellogo.go，其内容如下：

package main

import (

"fmt"

)

func main() {

fmt.Printf("Hello, Go!\n")

}

下面我们来编译该源文件并执行生成的可执行文件：

$ go build hellogo.go

$ ls

hellogo* hellogo.go

$ hellogo

Hello, Go!

通过go build加上要编译的Go源文件名，我们即可得到一个可执行文件，默认情况下这个文件的名字为源文件名字去掉.go后缀。当然我们也 可以通过-o选项来指定其他名字：

$ go build -o myfirstgo hellogo.go

$ ls

myfirstgo* hellogo.go

如果我们在go-examples目录下直接执行go build命令，后面不带文件名，我们将得到一个与目录名同名的可执行文件：

$ go build

$ ls

go-examples* hellogo.go

**三、程序入口点(entry point)和包(package)**

Go保持了与C家族语言一致的风格：即目标为可执行程序的Go源码中务必要有一个名为main的函数，该函数即为可执行程序的入口点。除此之外 Go还增加了一个约束：作为入口点的main函数必须在名为main的package中。正如上面hellogo.go源文件中的那样，在源码第 一行就声明了该文件所归属的package为main。

Go去除了头文件的概念，而借鉴了很多主流语言都采用的package的源码组织方式。package是个逻辑概念，与文件没有一一对应的关系。 如果多个源文件都在开头声明自己属于某个名为foo的包，那这些源文件中的代码在逻辑上都归属于包foo(这些文件最好在同一个目录下，至少目前 的Go版本还无法支持不同目录下的源文件归属于同一个包)。

我们看到hellogo.go中import一个名为fmt的包，并利用该包内的Printf函数输出"Hello, Go!"。直觉告诉我们fmt包似乎是一个标准库中的包。没错，fmt包提供了格式化文本输出以及读取格式化输入的相关函数，与C中的printf或 scanf等类似。我们通过import语句将fmt包导入我们的源文件后就可以使用该fmt包导出(export)的功能函数了(比如 Printf)。

在C中，我们通过static来标识局部函数还是全局函数。而在Go中，包中的函数是否可以被外部调用，要看该函数名的首母是否为大写。这是一种 Go语言固化的约定：首母大写的函数被认为是导出的函数，可以被包之外的代码调用；而小写字母开头的函数则仅能在包内使用。在例子中你也看到了 fmt包的Printf函数其首母就是大写的。

**四、GOPATH**

我们把上面的hellogo.go稍作改造，拆分成两个文件：main.go和hello.go。

/* hello.go */

package hello

import "fmt"

func Hello(who string) {

fmt.Printf("Hello, %s!\n", who)

}

/* main.go */

package main

import (

"hello"

)

func main() {

hello.Hello("Go!")

}

用go build编译main.go，结果如下：

$ go build main.go

main.go:4:2: import "hello": cannot find package

编译器居然提示无法找到hello这个package，而hello.go中明明定义了package hello了。这是怎么回事呢？原来go compiler搜索package的方式与我们常规理解的有不同，Go在这方面也有一套约定，这里面涉及到一个重要的环境变量：GOPATH。我们可以使用go help gopath来查看一下有关gopath的manual。

Go compiler的package搜索顺序是这样的，以搜索hello这个package为例：

* 首先，Go compiler会在GO安装目录(GOROOT，这里是/usr/local/go)下查找是否有src/pkg/hello相关包源码；如果没有则继续；

* 如果export GOPATH=PATH1:PAHT2，则Go compiler会依次查找是否存在PATH1/src/hello、PATH2/src/hello；配置在GOPATH中的PATH1和PATH2被称作workplace；

* 如果在上述几个位置均无法找到hello这个package，则提示出错。

在本例子中，我们尚未设置过GOPATH环境变量，也没有建立类似PATH1/src/hello这样的路径，因此Go compiler显然无法找到hello这个package了。我们来设置一下GOPATH变量并建立相关目录：

$ export GOPATH=/home/tonybai/go-examples

$ mkdir src/hello

$ mv hello.go src/hello

$ go build main.go

$ ls

main* main.go src/

$ main

Hello, Go!

**五、Go install**

我们将main.go移到src/main中，这样这个demo project显得更加合理，所有源码均在src下：

$cd src

$ ls

hello/ main/

Go提供了install命令，与build命令相比，install命令在编译源码后还会将可执行文件或库文件安装到约定的目录下。我们以main目录为例：

$ cd main

$ go install

install命令执行后，我们发现main目录下没有任何变化，原先build时产生的main可执行文件也不见了踪影。别急，前面说过Go install也有一套自己的约定：

* go install(在src/DIR下)编译出的可执行文件以其所在目录名(DIR)命名

* go install将可执行文件安装到与src同级别的bin目录下，bin目录由go install自动创建

* go install将可执行文件依赖的各种package编译后，放在与src同级别的pkg目录下

现在我们来看看bin目录：

$ ls /home/tonybai/go-examples

bin/ src/ pkg/

$ ls bin

main*

的确出现一个bin目录，并且刚刚编译的程序main在bin下面。

hello.go编译后并非可执行程序，在编译main的同时，由于main依赖hello package，因此hello也被关联编译了。这与单独在hello目录下执行install的结果是一样的，我们试试：

$ cd hello

$ go install

$ ls /home/tonybai/go-examples

bin/ pkg/ src/

在我们的workspace(go-examples目录)下出现了一个pkg目录，pkg目录下是一个名为linux_386的子目录，其下面有一个文 件：hello.a。这就是我们install的结果。hello.go被编译为hello.a并安装到pkg/linux_386目录下了。

.a这个后缀名让我们想起了静态共享库，但这里的.a却是Go独有的文件格式，与传统的[静态共享库](http://tonybai.com/2012/04/11/multiple-definitions-of-the-compiling-phase/)并不兼容。但Go语言的设计者使用这个后缀名似乎是希望 这个.a文件也承担起Go语言中"静态共享库"的角色。我们不妨来试试，看看这个hello.a是否可以被Go compiler当作"静态共享库"来对待。我们移除src中的hello目录，然后在main目录下执行go build：

$ go build

main.go:4:2: import "hello": cannot find package

Go编译器提示无法找到hello这个包，可见目前版本的Go编译器似乎不理pkg下的.a文件。[http://code.google.com/p/go/issues/detail?id=2775](http://code.google.com/p/go/issues/detail?id=2775) 这个issue也印证了这一点，不过后续Go版本很可能会支持链接.a文件。毕竟我们在使用第三方package的时候，很可能无法得到其源码，并且在每个项目中都保存一份第三方包的源码也十分不利于项目源码的后期维护。

**六、像脚本一样运行Go源码**

Go具有很高的编译效率，这得益于其设计者对该目标的重视以及设计过程中细节方面的把控，当然这不是本文要关注的话题。正是由于go具有极速的编译，我们才可以像使用运行脚本语言那样使用它。

目前Go提供了run命令来直接运行源文件。比如：

$ go run main.go

Hello, Go!

go run实际上是一个将编译源码和运行编译后的二进制程序结合在一起的命令。但目前go源文件尚不支持作成Shebang Script，因为Go compiler尚不识别#!符号，下面的源码文件运行起来会出错：

#! /usr/local/go/bin/go run

package main

import (

"hello"

)

func main() {

hello.Hello("Go!")

}

$ go run main.go

package :

main.go:1:1: illegal character U+0023 '#'

不过我们可以可借助一些第三方工具来运行Shebang Go scripts，比如[gorun](https://wiki.ubuntu.com/gorun)。

**七、测试Go程序**

前面说过Go起点较高，因此其自身就提供了一个轻量级[单元测试](http://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/)框架包以及运行测试集的命令。

我们用一个例子来说明如何编写包的测试代码以及如何运行这个测试。我们在go-examples/src下建立另外一个目录mymath，mymath目录下mymath包的代码如下：

/* mymath.go */

package mymath

func MyAdd(i int, j int) int {

return i + j

}

要对mymath包进行测试，我们需在同一目录下创建mymath_test.go文件，其中对MyAdd函数的测试代码如下：

/* mymath_test.go */

package mymath

import "testing"

func TestMyAdd(t *testing.T) {

a, b := 4, 2

if x := MyAdd(a, b); x != 6 {

t.Errorf("MyAdd(%d, %d) = %d, want %d", a, b, x, 6)

}

}

在这个文件中我们import了Go提供的标准单元测试包-testing，并且每个测试方法都已Test作为前缀开头。现在我们来运行一下这个测试，在mymath目录下运行go test命令：

$ go test

PASS

ok mymath 0.007s

如果用例出错，我们就可看到下面提示：

$go test

— FAIL: TestMyAdd (0.00 seconds)

mymath_test.go:8: MyAdd(4, 2) = 6, want 6

FAIL

exit status 1

FAIL mymath 0.007s

由上可以看出，Go test也有自己的一些约定：测试源文件的名字必须以_test.go作为结尾；测试代码与被测代码在同一个包中；测试代码要导入testing包；测试 函数要以Test作为前缀，并且测试函数的函数签名必须是这样的：func TestXXX(t *testing.T)。

语言自带对测试的支持的好处是一致性，避免了大家使用不同的测试框架而给阅读、交流和维护带来的不便。

**八、项目源码组织**

有了源码、有了对编译原理的理解、有了测试框架的支持，我们就可以策划项目源码组织形式了。不过Go的诸多约定基本上已经将我们限制在如下结构上：

proj1/

bin/

myapp1*

pkg/

linux_386/

lib1.a

lib2.a

src/

lib1/

lib1.go

lib1_test.go

lib2/

lib2.go

lib2_test.go

… …

myapp1/

main.go # main package source

main_test.go # test source

proj2/

bin/

myapp2*

pkg/

linux_386/

lib3.a

lib4.a

src/

lib3/

lib3.go

lib3_test.go

lib4/

lib4.go

lib4_test.go

… …

myapp2/

main.go # main package source

main_test.go # test source

基于上述结构，我们可将GOPATH设置为proj1_path:proj2_path。

**九、代码风格(coding style)**

Go程序员可以不再纠结于到底使用哪种代码风格，因为Go已经将代码风格做了严格的约定，一旦违反，Compiler直接给出Error。go还提供了fmt命令来协助Go程序员按标准格式化源文件。

从上面例子中我们可以看到Go的几大风格特点是：

* 左大括号'{'一定在函数名或if等语句在同一行

func foo {

}

* 无需显式用分号;将语句分隔(除非是在一行写上多条语句)，因为compiler会替大家在适当位置加入分号的。

i, j := 2, 3

MyAdd(i, j)

if x := MyAdd(a, b); x != 6 {

… …

}

* if、for等后面的表达式无需用小括号括上


if x != 5 {

… …

}

**十、查看文档**

Go的全量文档几乎与Go安装包一起发布。安装Go后，执行godoc –http=:端口号即可启动doc server。打开浏览器，输入http://localhost:端口号即可以看到几乎与Go官方站完全相同的文档页面。

**十一、参考书籍**

Go毕竟是新生代语言，其自身尚不成熟和完善，资料也较少。这里推荐两本市面上比较好的且内容已更新到Go 1的书籍：

* Mark Summerfield的《[Programming in Go: creating applications for the 21st century](http://book.douban.com/subject/7070565)》

* Ivo Balbaert的《[The Way to Go – A Thorough Introduction to the Go Programming Language](http://book.douban.com/subject/10558892/)》

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

Go 是 Google 的前两个字母，so ……

总而言之，这个名字起的不咋地。

Go的前景怎样呢？有google这个强大的后台支持着，我想Go可以走得更远！