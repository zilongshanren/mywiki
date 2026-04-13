---
title: Go与C语言的互操作
url: https://tonybai.com/2012/09/26/interoperability-between-go-and-c/
published: '2012-09-26'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go与C语言的互操作

[Go](http://golang.org)有强烈的[C](http://tonybai.com/tag/c)背景，除了语法具有继承性外，其设计者以及其设计目标都与C语言有着千丝万缕的联系。在Go与C语言互操作([Interoperability](http://en.wikipedia.org/wiki/Language_interoperability))方面，Go更是提供了强大的支持。尤其是在Go中使用C，你甚至可以直接在Go源文件中编写C代码，这是其他语言所无法望其项背的。

在如下一些场景中，可能会涉及到Go与C的互操作：

1、提升局部代码性能时，用C替换一些Go代码。C之于Go，好比汇编之于C。

2、嫌Go内存GC性能不足，自己手动管理应用内存。

3、实现一些库的Go Wrapper。比如Oracle提供的C版本OCI，但Oracle并未提供Go版本的以及连接DB的协议细节，因此只能通过包装C OCI版本的方式以提供Go开发者使用。

4、Go导出函数供C开发者使用(目前这种需求应该很少见)。

5、Maybe more…

**一、Go调用C代码的原理**

下面是一个短小的例子：

package main

// #include <stdio.h>

// #include <stdlib.h>

/*

void print(char *str) {

printf("%s\n", str);

}

*/

import "C"

import "unsafe"

func main() {

s := "Hello Cgo"

cs := C.CString(s)

C.print(cs)

C.free(unsafe.Pointer(cs))

}

与"正常"Go代码相比，上述代码有几处"特殊"的地方：

1) 在开头的注释中出现了C头文件的include字样

2) 在注释中定义了C函数print

3) import的一个名为C的"包"

4) 在main函数中居然调用了上述的那个C函数-print

没错，这就是在Go源码中调用C代码的步骤，可以看出我们可直接在Go源码文件中编写C代码。

首先，Go源码文件中的C代码是需要用注释包裹的，就像上面的include 头文件以及print函数定义；

其次，import "C"这个语句是必须的，而且其与上面的C代码之间不能用空行分隔，必须紧密相连。这里的"C"不是包名，而是一种类似名字空间的概念，或可以理解为伪包，C语言所有语法元素均在该伪包下面；

最后，访问C语法元素时都要在其前面加上伪包前缀，比如C.uint和上面代码中的C.print、C.free等。

我们如何来编译这个go源文件呢？其实与"正常"Go源文件没啥区别，依旧可以直接通过go build或go run来编译和执行。但实际编译过程中，go调用了名为cgo的工具，cgo会识别和读取Go源文件中的C元素，并将其提取后交给C编译器编译，最后与Go源码编译后的目标文件链接成一个可执行程序。这样我们就不难理解为何Go源文件中的C代码要用注释包裹了，这些特殊的语法都是可以被Cgo识别并使用的。

**二、在Go中使用C语言的类型**

1、原生类型

* 数值类型

在Go中可以用如下方式访问C原生的数值类型：

C.char,

C.schar (signed char),

C.uchar (unsigned char),

C.short,

C.ushort (unsigned short),

C.int, C.uint (unsigned int),

C.long,

C.ulong (unsigned long),

C.longlong (long long),

C.ulonglong (unsigned long long),

C.float,

C.double

Go的数值类型与C中的数值类型不是一一对应的。因此在使用对方类型变量时少不了显式转型操作，如Go doc中的这个例子：

func Random() int {

return int(C.random())//C.long -> Go的int

}

func Seed(i int) {

C.srandom(C.uint(i))//Go的uint -> C的uint

}

* 指针类型

原生数值类型的指针类型可按Go语法在类型前面加上*，比如var p *C.int。而void*比较特殊，用Go中的unsafe.Pointer表示。任何类型的指针值都可以转换为unsafe.Pointer类型，而unsafe.Pointer类型值也可以转换为任意类型的指针值。unsafe.Pointer还可以与uintptr这个类型做相互转换。由于unsafe.Pointer的指针类型无法做算术操作，转换为uintptr后可进行算术操作。

* 字符串类型

C语言中并不存在正规的字符串类型，在C中用带结尾'\0'的字符数组来表示字符串；而在Go中，string类型是原生类型，因此在两种语言互操作是势必要做字符串类型的转换。

通过C.CString函数，我们可以将Go的string类型转换为C的"字符串"类型，再传给C函数使用。就如我们在本文开篇例子中使用的那样：

s := "Hello Cgo\n"

cs := C.CString(s)

C.print(cs)

不过这样转型后所得到的C字符串cs并不能由Go的gc所管理，我们必须手动释放cs所占用的内存，这就是为何例子中最后调用C.free释放掉cs的原因。在C内部分配的内存，Go中的GC是无法感知到的，因此要记着释放。

通过C.GoString可将C的字符串(*C.char)转换为Go的string类型，例如：

// #include <stdio.h>

// #include <stdlib.h>

// char *foo = "hellofoo";

import "C"

import "fmt"

func main() {

… …

fmt.Printf("%s\n", C.GoString(C.foo))

}

* 数组类型

C语言中的数组与Go语言中的数组差异较大，后者是值类型，而前者与C中的指针大部分场合都可以随意转换。目前似乎无法直接显式的在两者之间进行转型，官方文档也没有说明。但我们可以通过编写转换函数，将C的数组转换为Go的Slice(由于Go中数组是值类型，其大小是静态的，转换为Slice更为通用一些)，下面是一个整型数组转换的例子：

// int cArray[] = {1, 2, 3, 4, 5, 6, 7};

func CArrayToGoArray(cArray unsafe.Pointer, size int) (goArray []int) {

p := uintptr(cArray)

for i :=0; i < size; i++ {

j := *(*int)(unsafe.Pointer(p))

goArray = append(goArray, j)

p += unsafe.Sizeof(j)

}

return

}

func main() {

… …

goArray := CArrayToGoArray(unsafe.Pointer(&C.cArray[0]), 7)

fmt.Println(goArray)

}

执行结果输出：[1 2 3 4 5 6 7]

这里要注意的是：Go编译器并不能将C的cArray自动转换为数组的地址，所以不能像在C中使用数组那样将数组变量直接传递给函数，而是将数组第一个元素的地址传递给函数。

2、自定义类型

除了原生类型外，我们还可以访问C中的自定义类型。

* 枚举(enum)

// enum color {

// RED,

// BLUE,

// YELLOW

// };

var e, f, g C.enum_color = C.RED, C.BLUE, C.YELLOW

fmt.Println(e, f, g)

输出：0 1 2

对于具名的C枚举类型，我们可以通过C.enum_xx来访问该类型。如果是匿名枚举，则似乎只能访问其字段了。

* 结构体(struct)

// struct employee {

// char *id;

// int age;

// };

id := C.CString("1247")

var employee C.struct_employee = C.struct_employee{id, 21}

fmt.Println(C.GoString(employee.id))

fmt.Println(employee.age)

C.free(unsafe.Pointer(id))

输出：

1247

21

和enum类似，我们可以通过C.struct_xx来访问C中定义的结构体类型。

* 联合体(union)

这里我试图用与访问struct相同的方法来访问一个C的union：

// #include <stdio.h>

// union bar {

// char c;

// int i;

// double d;

// };

import "C"

func main() {

var b *C.union_bar = new(C.union_bar)

b.c = 4

fmt.Println(b)

}

不过编译时，go却报错：b.c undefined (type *[8]byte has no field or method c)。从报错的信息来看，Go对待union与其他类型不同，似乎将union当成[N]byte来对待，其中N为union中最大字段的size(圆整后的)，因此我们可以按如下方式处理C.union_bar：

func main() {

var b *C.union_bar = new(C.union_bar)

b[0] = 13

b[1] = 17

fmt.Println(b)

}

输出：&[13 17 0 0 0 0 0 0]

* typedef

在Go中访问使用用typedef定义的别名类型时，其访问方式与原实际类型访问方式相同。如：

// typedef int myint;

var a C.myint = 5

fmt.Println(a)

// typedef struct employee myemployee;

var m C.struct_myemployee

从例子中可以看出，对原生类型的别名，直接访问这个新类型名即可。而对于复合类型的别名，需要根据原复合类型的访问方式对新别名进行访问，比如myemployee实际类型为struct，那么使用myemployee时也要加上struct_前缀。

**三、Go中访问C的变量和函数**

实际上上面的例子中我们已经演示了在Go中是如何访问C的变量和函数的，一般方法就是加上C前缀即可，对于C标准库中的函数尤其是这样。不过虽然我们可以在Go源码文件中直接定义C变量和C函数，但从代码结构上来讲，大量的在Go源码中编写C代码似乎不是那么“专业”。那如何将C函数和变量定义从Go源码中分离出去单独定义呢？我们很容易想到将C的代码以共享库的形式提供给Go源码。

package main

// #cgo LDFLAGS: -L ./ -lfoo

// #include <stdio.h>

// #include <stdlib.h>

// #include "foo.h"

import "C"

import "fmt“

func main() {

fmt.Println(C.count)

C.foo()

}

我们看到上面例子中通过#cgo指示符告诉go编译器链接当前目录下的libfoo共享库。C.count变量和C.foo函数的定义都在libfoo共享库中。我们来创建这个共享库：

// foo.h

int count;

void foo();

//foo.c

#include "foo.h"

int count = 6;

void foo() {

printf("I am foo!\n");

}

$> gcc -c foo.c

$> ar rv libfoo.a foo.o

我们首先创建一个静态共享库libfoo.a，不过在编译Go源文件时我们遇到了问题：

$> go build foo.go

# command-line-arguments

/tmp/go-build565913544/command-line-arguments.a(foo.cgo2.)(.text): foo: not defined

foo(0): not defined

提示foo函数未定义。通过-x选项打印出具体的编译细节，也未找出问题所在。不过在Go的问题列表中我发现了一个issue(http://code.google.com/p/go/issues/detail?id=3755)，上面提到了目前Go的版本不支持链接静态共享库。

那我们来创建一个动态共享库试试：

$> gcc -c foo.c

$> gcc -shared -Wl,-soname,libfoo.so -o libfoo.so foo.o

再编译foo.go，的确能够成功。执行foo。

$> go build foo.go && go

6

I am foo!

还有一点值得注意，那就是Go支持多返回值，而C中并没不支持。因此当将C函数用在多返回值的调用中时，C的errno将作为err返回值返回，下面是个例子：

package main

// #include <stdlib.h>

// #include <stdio.h>

// #include <errno.h>

// int foo(int i) {

// errno = 0;

// if (i > 5) {

// errno = 8;

// return i – 5;

// } else {

// return i;

// }

//}

import "C"

import "fmt"

func main() {

i, err := C.foo(C.int(8))

if err != nil {

fmt.Println(err)

} else {

fmt.Println(i)

}

}

$> go run foo.go

exec format error

errno为8，其含义在errno.h中可以找到：

#define ENOEXEC 8 /* Exec format error */

的确是“exec format error”。

**四、C中使用Go函数**

与在Go中使用C源码相比，在C中使用Go函数的场合较少。在Go中，可以使用"export + 函数名"来导出Go函数为C所使用，看一个简单例子：

package main

/*

#include <stdio.h>

extern void GoExportedFunc();

void bar() {

printf("I am bar!\n");

GoExportedFunc();

}

*/

import "C"

import "fmt"

//export GoExportedFunc

func GoExportedFunc() {

fmt.Println("I am a GoExportedFunc!")

}

func main() {

C.bar()

}

不过当我们编译该Go文件时，我们得到了如下错误信息：

# command-line-arguments

/tmp/go-build163255970/command-line-arguments/_obj/bar.cgo2.o: In function `bar':

./bar.go:7: multiple definition of `bar'

/tmp/go-build163255970/command-line-arguments/_obj/_cgo_export.o:/home/tonybai/test/go/bar.go:7: first defined here

collect2: ld returned 1 exit status

代码似乎没有任何问题，但就是无法通过编译，总是提示“多重定义”。翻看Cgo的文档，找到了些端倪。原来

*There is a limitation: if your program uses any //export directives, then the C code in the comment may only include declarations (extern int f();), not definitions (int f() { return 1; }).*

似乎是// extern int f()与//export f不能放在一个Go源文件中。我们把bar.go拆分成bar1.go和bar2.go两个文件：

// bar1.go

package main

/*

#include <stdio.h>

extern void GoExportedFunc();

void bar() {

printf("I am bar!\n");

GoExportedFunc();

}

*/

import "C"

func main() {

C.bar()

}

// bar2.go

package main

import "C"

import "fmt"

//export GoExportedFunc

func GoExportedFunc() {

fmt.Println("I am a GoExportedFunc!")

}

编译执行：

$> go build -o bar bar1.go bar2.go

$> bar

I am bar!

I am a GoExportedFunc!

个人觉得目前Go对于导出函数供C使用的功能还十分有限，两种语言的调用约定不同，类型无法一一对应以及Go中类似Gc这样的高级功能让导出Go函数这一功能难于完美实现，导出的函数依旧无法完全脱离Go的环境，因此实用性似乎有折扣。

**五、其他**

虽然Go提供了强大的与C互操作的功能，但目前依旧不完善，比如不支持在Go中直接调用可变个数参数的函数(issue975)，如printf(因此，文档中多用fputs)。

这里的建议是：尽量缩小Go与C间互操作范围。

什么意思呢？如果你在Go中使用C代码时，那么尽量在C代码中调用C函数。Go只使用你封装好的一个C函数最好。不要像下面代码这样：

C.fputs(…)

C.atoi(..)

C.malloc(..)

而是将这些C函数调用封装到一个C函数中，Go只知道这个C函数即可。

C.foo(..)

相反，在C中使用Go导出的函数也是一样。


© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

都是很新鲜的概念。我觉得Go把python对c的利用也学到了。

func CArrayToGoArray(cArray unsafe.Pointer, size int) (goArray []int) {…}这个有更好的实现方案：func CArrayToGoSlice(begin uintptr, size int) []byte { var theGoSlice []byte sliceHeader := (*reflect.SliceHeader)((unsafe.Pointer(&theGoSlice))) sliceHeader.Cap = size sliceHeader.Len = size sliceHeader.Data = begin return theGoSlice}

func CArrayToGoArray(cArray unsafe.Pointer, size int) []int { return (*[1<<30]int)(cArray)[0:size]}

这个不行啊，内存管理要分开

这里提到的C使用GO的例子，最终还是使用GO来编译的C代码，如果GO编译出来的库文件能直接给C使用就好了（似乎不太现实）

bar1.go bar2.go的例子会报错，报错信息如下：

# command-line-arguments

C:\Users\ADMINI~1\AppData\Local\Temp\go-build390401246\b001\_x002.o: In function `bar’:

D:/Go-Work/src/Demo/DemoCGO/main.go:23: undefined reference to `GoExportedFunc’

D:/Go-Work/src/Demo/DemoCGO/main.go:23: undefined reference to `GoExportedFunc’

collect2.exe: error: ld returned 1 exit status

Compilation finished with exit code 2

golang版本是go version go1.11.2 windows/amd64

我用”go1.11.2 darwin/amd64″版本go编译器在macos下重新试了一下该例子，编译和执行都是ok的(不过我没有在windows上试，我没有windows上的go编译环境)：

$go build -o bar bar1.go bar2.go

$ls

bar* bar1.go bar2.go go.mod

$./bar

I am bar!

I am a GoExportedFunc!

func CArrayToGoArray(cArray unsafe.Pointer, size int) []int { return (*[1<<30]int)(cArray)[0:size]}

这个貌似也不是全平台方案

@tony bai 能否给出一个CArrayToGoArray 实现的cgo 例子,

注意这里数组内存是在C 里面malloc， 最后传给了go， 需要go管理生存期。

//extern void MyCMallocArray(int *p, int n);

func CGoMallocArray() []int {

xxxxxx

MyCMallocArray

xxxxxx

}