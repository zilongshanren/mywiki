---
title: Go包导入与Java的差别
url: https://tonybai.com/2016/09/13/package-import-in-golang-vs-in-java/
published: '2016-09-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go包导入与Java的差别

闲暇时翻阅了近期下载到的电子书[《Go in Practice》](https://book.douban.com/subject/26345890/) ，看到1.2.4 Package Management一节中的代码Demo，感觉作者对Go package导入的说法似乎不够精确：“Packages are imported by their name”(后续的说明将解释不精确的原因)。联想到前几天遇到的一个Java包导入的问题，让我隐约地感觉Java程序员很容易将两种语言的Package import机制搞混淆，于是打算在这里将Golang和Java的Package import机制做一个对比，对于Java转型到Golang的程序员将大有裨益:)。这里的重点在于与Java的对比，关于Golang的Package Import的细节可以参考我之前写过的一篇文章[《理解Golang包导入》](http://tonybai.com/2015/03/09/understanding-import-packages/)。

我们先来看两个功能等价的代码。

```
//TestDate.java
import java.util.*;
import java.text.DateFormat;
public class TestDate {
public static void main(String []args){
Date d = new Date();
String s = DateFormat.getDateInstance().format(d);
System.out.println(s);
}
}
```


和

```
//testdate.go
package main
import (
"fmt"
"time"
)
func main() {
t := time.Now()
fmt.Println(t.Format("2006-01-02"))
}
```


两个程序在Run时，都输出下面内容：

```
2016-9-13
```


我们看到Golang和Java都是用import关键字来进行包导入的：

```
import java.util.Date;
Date d = new Date();
```


vs.

```
import "time"
t := time.Now()
```


咋看起来，Java在package import后似乎使用起来更Easy，使用包内的类和方法时，前面无需再附着Package name，即Date d，而不是java.util.Date d。而Go在导入”time”后，引用包中方法时依然要附着着包名，比如time.Now()。但实质上两种语言在import package的机制上是有很大不同的。

#### 1、机制

虽然都使用import，但import关键字后面的字符串所代表的含义有不同。

Java import导入的是类而不是包，import后面的字符串表示的是按需导入Java Package下面的类，比如import java.util.*； 或导入Package下某个类，比如import java.util.Date。而Go import关键字后面的字符串是包名吗？很多初学者会认为这个就是Go包名，实则不然，Go import后面的字符串实际上是一个包导入路径，这也是Java用”xxx.yyy.zzz”形式而Golang使用”xxx/yyy/zzz”形式的原因。我们用个简单的例子就能证明这一点。我们知道Golang会在\$GOROOT/src + \$GOPATH/src下面导入xxx/yyy/zzz路径下的包，我们在import “fmt”时，实际上导入的是\$GOROOT/src/fmt目录下的包，只是恰好这个下面的包的名字是fmt罢了。如果我们将\$GOROOT/src/fmt目录改名为fmt1，结果会是如何呢？

```
$go build helloworld.go
helloworld.go:3:8: cannot find package "fmt" in any of:
/Users/tony/.bin/go17/src/fmt (from $GOROOT)
/Users/tony/Test/GoToolsProjects/src/fmt (from $GOPATH)
helloworld.go是一个helloworld go源码。
```


之所以出错是因为在\$GOROOT/src下已经没有fmt这个目录了，所以下面代码中的两个fmt含义是不同的（这也解释了Go in practice中关于包导入的说法的不精确的原因）：

```
package main
import "fmt" ---- 这里的fmt指的是$GOROOT/src下的名为"fmt"的目录名
func main() {
fmt.Println("Hello, World") --- 这里的fmt是真正的包名"fmt"
}
```


从上面我们可以看出Go的包名和包的源文件所在的路径的名字并没有必须一致的要求，这也是为什么在Go源码使用包时一定是用packagename.XX形式，而不是packagename.subpackagename.XX的形式了。比如导入”net/http”后，我们在源码中使用的是http.xxx，而不是net.http.xxx，因为net/http只是一个路径，并不是一个嵌套的包名。

之所以看起来导入路径的终段目录名与包名一致，只是因为这是Go官方的建议：Go的导入路径的最后一段目录名(xxx/yyy/zzz中的zzz)与该目录（zzz）下面源文件中的Go Package名字相同。

下面是一个非标准库的包名与导入路径终段名完全不一致的例子：

```
//github.com/pkgtest/pkg1/foo.go
package foo
import "fmt"
func Foo() {
fmt.Println("Foo in pkg1")
}
//testfoo.go
package main
import (
"github.com/pkgtest/pkg1"
)
func main() {
foo.Foo() //输出：Foo in pkg1
}
```


可以看出testfoo.go导入的是”github.com/pkgtest/pkg1″这个路径，但这个路径下的包名却是foo。

Java语言中的包实际以.jar为单位，.jar内部实际上也是以路径组织.class文件的，比如：foo.jar这个jar包中有一个package名为：com.tonybai.foo，foo包中包含类Foo、Bar，那实际上foo.jar内部的目录格式将是：

```
foo.jar
- com/
- tonybai/
- foo/
- Foo.class
- Bar.class
```


但对于Java包的使用者，这些都是透明的。

#### 2、重名

Java中关于包导入(实则是类导入)唯一的约束就是不能有两个类导入后的full name相同，如果存在两个导入类的full name完全相同，Javac在resolve时，要以ClassPath路径的先后顺序为准了，选择最先遇到的那个类。但是在Go中，如果导入的两个路径下的包名相同，那么Go compiler显然是不能允许这种情况的存在的，会给出Error信息。

比如我们在GOPATH下的github.com/pkgtest/pkg1和github.com/pkgtest/pkg2下放置了同名包foo，下面代码将会报错：

```
package main
import (
"github.com/pkgtest/pkg1"
"github.com/pkgtest/pkg2"
)
func main() {
foo.Foo()
}
```


错误信息如下：

```
$go run testfoo.go
# command-line-arguments
./testdate.go:8: foo redeclared as imported package name
previous declaration at ./testfoo.go:7
```


解决这一问题的方法就是采用package alias：

```
package main
import (
a "github.com/pkgtest/pkg1"
b "github.com/pkgtest/pkg2"
)
func main() {
a.Foo()
b.Foo()
}
```


编译执行上面程序将得到下面结果，而不是Error：

```
Foo of foo package in pkg1
Foo in foo package in pkg2
```


© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

平时不会特别注意的问题，确是值得了解的