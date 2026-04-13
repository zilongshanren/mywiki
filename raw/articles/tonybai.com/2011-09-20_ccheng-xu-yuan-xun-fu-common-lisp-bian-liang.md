---
title: C程序员驯服Common Lisp – 变量
url: https://tonybai.com/2011/09/20/c-programers-tame-common-lisp-series-variables/
published: '2011-09-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# C程序员驯服Common Lisp – 变量

变量是[C语言](http://tonybai.com/tag/C)中最常用的、不可或缺的语言元素。C语言是命令式编程语言（[imperative programming language](http://en.wikipedia.org/wiki/Imperative_programming)），其基本编程方法是基于对内存单元的修改，而变量又恰是对内存单元的抽象表示，比如："int a = 0xff"这行语句告诉我们在内存中有一块大小为4个字节的区域，该区域可以通过a这个变量直接访问，该区域初始时存储的值为0xff。由此看来C语言的主要操作就是变量操作。

C语言中变量的使用有着严格要求：

第一，在使用一个变量之前必须先声明(或定义)这个变量；

第二，变量声明(或定义)时必须显式指出这个变量的数据类型；

最后，变量类型一旦确定，则在其生命周期内不能改变。

这些也是C语言作为静态编译型语言的特质所决定的。下面代码中关于变量使用的语句在C语言中都是不被允许的：

void foo(void) {

printf("%d\n", x); /* x变量未被声明或定义 */

}

void bar(void) {

x;

printf("%d\n", x); /* 未显式指定x的数据类型，变量声明语句不合法 */

}

与C语言不同，[Common Lisp](http://tonybai.com/2011/06/21/hello-common-lisp/)是一门通用的[函数式编程语言](http://en.wikipedia.org/wiki/Functional_programming)，其基本编程方法是基于对函数的求值，并要求尽量避免引入可改变的(mutable)变量和状态。另外再加上Common Lisp还是一门动态类型语言，这些都决定了其在变量的使用方面与C语言有着较大的差异。

一、赋值

在C语言中，我们用等号(=)来为变量进行赋值，如：

int a = 13;

char *str = "hello c";

struct foo f = {1, 5, "foo"};

但Common Lisp程序是基于[S-expressions](http://tonybai.com/2011/09/02/c-programers-tame-common-lisp-series-expressions/)的，等号(=)只是一个相等性比较的逻辑判断谓词(predicate)，无法为变量进行赋值。在Common Lisp中，宏setf才是最通用也是最常使用的赋值方法。setf的语法形式如下：

(setf var-expression value-expression)

例如：

[1]> (setf x 5)

5

[2]> (print x)

5

[3]> (setf x "hello lisp")

"hello lisp"

[4]> (print x)

"hello lisp"

从这个例子中我们可以看出三点与C语言的不同之处：

1、Common Lisp变量在使用前是无需显式声明的(当然显式声明也是可以的哦，详见后面说明);

2、变量无类型信息；

3、变量在运行时可以被赋值为多种类型的值，比如此例中x先被赋值为一个整数，后又被赋值为一个字符串。

C语言的变量是内存单元的直接抽象，但Common Lisp中的变量想必不是这样的，它似乎更像是一个void*指针，被赋值为各种类型的对象地址。没错，其实Common Lisp变量的实质是一个引用(reference)，对这类变量赋值的实质就是将引用与存储了真实值的内存块地址绑定起来，setf这个宏达到的实际效果就是改变了引用与值的绑定关系而已。通过这里我们似乎还可以引伸出一点，那就是Common Lisp中的变量本身并不包含类型信息，相反，值才是类型信息的载体，变量的类型取决于变量所绑定的值的类型。

二、局部变量(Local Variable)

作用域是变量的最重要属性之一。根据变量的作用域不同，在C语言中我们可以将变量简单地划分为全局变量(Global Variable)和局部变量。顾名思义，全局变量就是在程序的所有作用域内均可以访问的变量；局部变量恰与之相反，只是在某一特定作用域才可以访问的变量，比如某一函数或代码块内部。Common Lisp也支持这两种类型的变量，我们先从局部变量说起。

与C类似，Common Lisp的局部变量也是在函数内部或代码块内部定义和使用的。Common Lisp通过let宏定义一个局部变量，let宏的语法形式如下：

(let (var*)

expr1

expr2

… )

其中每个var的语法形式为：(name initial-value)，如果未指定initial-value，则变量初值将被设置为nil。最后一个expr的求值结果将作为let的返回值。例如：

[1]> (defun bar ()

(let ((x 0)) (setf x 4)))

BAR

[2]> (bar)

4

[3]> (print x)

*** – EVAL: variable X has no value

let引入的局部变量x的作用域仅限于bar的内部，在bar外部无法访问到这些变量，变量x的生命周期也是从bar的执行开始，直到bar执行结束为止。

let一次可声明多个局部变量，并可嵌套使用：

[1]> (defun foo ()

(let ((x 1) (y 2))

(print x)

(print y)

(setf x 3)

(let ((z 4))

(print x)

(print z))))

FOO

[2]> (foo)

1

2

3

4

局部变量的默认作用域属于静态作用域(lexical scope或static scope)，静态作用域是指变量的作用域在执行前即可确定下来，每个函数或代码块中的局部变量均可以在当前函数(或代码块)中或其外层函数(或外层代码块)中找到对应的声明或定义。如上例中，函数foo内有两层let嵌套。外层let引入的变量x和y在当前函数内即可找到对应的定义；最里层的let代码块中使用的变量x在外层的foo函数定义中可以找到相应的定义。一旦找到绑定关系，变量的值就不会因执行环境不同而发生变化了。

和C语言类似，如果局部作用域中的不同层次定义了相同名字的局部变量，那么内层的局部变量将遮盖外层的变量，如：

[1]> (defun bar ()

(let ((x 1))

(print x)

(let ((x 11))

(print x)

(setf x (1+ x))

(print x))

(print x)))

BAR

[2]>

1

11

12

1

求值内层x的值时，Common Lisp找到的是最内层的x定义，最内层的变量x当前绑定值为11，我们看到的输出结果也的确是11。在外层，变量x对应的定义为(x <– 1)，这样外层输出的x的值就为1。

前面例子中定义的函数都是不带参数的，这是故意为之，因为下面我要说函数的形式参数。在C语言中，函数的形式参数与函数内的局部变量是等价的，其作用域也仅局限在函数内部。Common Lisp也是这样的，函数的形式参数本身就可以理解为函数内部的局部变量，在函数被求值时，Common Lisp在函数的形式参数与实际参数间建立绑定关系：

[1]> (defun foo (x)

(print x)

(setf x 13)

(print x))

FOO

[2]> (foo 4)

4

13

从例子中我们可以看出foo函数在求值时，形式参数x与实际参数4建立绑定，第一个(print x)输出结果为4；在foo内部，我们利用setf改变了x的绑定关系后，x值变为13；函数foo内部使用的变量x对应的定义就是foo的形式参数。无论日后foo在什么上下文环境下执行，该x对应的定义都是固定的了，如：

[3]> (let ((x 5)) (foo 4))

4

13

与C语言不同的是，Common Lisp还支持动态作用域(dynamic scope)，这种作用域在如今主流编程语言中已经不常见了。与静态作用域相反，具有动态作用域的变量在执行之前无法确定其定义，也就是说变量的定义不取决于其所在函数或代码块定义时的环境，而是取决于其所在函数或代码块执行时所处的上下文环境，因此其定义或者说绑定关系只能在运行时确定。

对于局部变量，Common Lisp通过(declare (special var-name))来显式声明var-name这个变量为动态作用域变量，又称动态变量(dynamic variable)。动态变量理解起来很不容易，但若明白其实现原理，理解起来就相对轻松许多了。每个动态变量都会对应一个全局绑定关系栈(stack)，在某作用域中遇到一个局部变量定义或新绑定，解释器就会将该新绑定关系压入堆栈；当离开该作用域后，绑定关系被弹出栈。这样当试图确定某个变量的绑定关系时，我们可以直接从栈顶获得绑定关系。如果对应该变量的栈为空时，即判定该变量未绑定任何值，解释器会报错。我们再来通过一个例子来加深一下了解吧：

[1]> (defun foo ()

(declare (special x))

(print x))

FOO

[2]> (let ((x 6)) (foo))

*** – EVAL: variable X has no value

我们定义了一个函数foo，在foo中我们声明了x为动态变量。当我们执行(let ((x 6)) (foo))时，解释器提示X没有绑定任何值。这是怎么回事儿呢？我们还是用原理来一步一步分析。

按照执行顺序，解释器先遇到局部变量x的定义，将x与数值6建立绑定，同时确定x为局部变量，但并非动态变量。执行foo时，foo中的变量x为动态变量，解释器为其建立全局绑定关系栈，但是在foo中并没有变量x的定义，所以x对应的全局绑定关系栈为空，导致执行(print x)时出错。

我们修改一下代码：

[1]> (defun foo ()

(declare (special x))

(print x))

FOO

[2]> (let ((x 6)) (declare (special x)) (foo))

6

按照执行顺序，解释器先遇到局部变量x的定义，将x与数值6建立绑定，同时发现x被显式声明为动态变量，解释器为x建立全局绑定关系栈，并将其绑定关系(x <- 6)压入栈；接下来执行foo函数，foo中的变量x为动态变量，且当前已经建立全局绑定关系栈，继续执行(print x)，从栈顶得到绑定关系(x <- 6)，得到求值结果，最后解释器离开该作用域，将绑定关系弹出栈。

三、全局变量

与局部变量对应的是全局变量。全局变量拥有全局作用域，即在一个程序内部的任何地方都可以访问到全局变量。Common Lisp通过defvar或defparameter宏显式定义一个全局变量（虽然这不是必须的）：

[1]> (defvar *x* 13)

*X*

[2]> (print *x*)

13

[3]> (defparameter *y* 14)

*Y*

[4]> (print *y*)

14

defvar与defparameter的语法形式如下：

(defvar var-symbol optional-initial-value

optional-documentation-string)

(defparameter var-symbol initial-value

optional-documentation-string)

defvar与defparameter的不同之处在于声明中可以不为全局变量绑定初值，而defparameter则是严格要求必须为声明中的全局变量绑定初值，比如:

[1]> (defvar *x*)

*X*

[2]> (defparameter *y*)

*** – The macro DEFPARAMETER may not be called with 1 arguments: (DEFPARAMETER *Y*)

局部变量可以显式地被指定为动态变量，全局变量是否可以呢？我们看看下面的例子：

[1]> (defvar *x* 11)

*X*

[2]> (defun foo ()

(print *x*))

FOO

[3]> (foo)

11

[4]> (let ((*x* 13)) (foo))

13

[3]> (foo)

11

从例子中我们看出，全局变量本身似乎就是一个动态变量。我们猜的没错。对于使用defvar或defparameter显式定义的全局变量，Common Lisp同时为其赋予了动态属性，也就是说defvar或defparameter定义的全局变量本身就是一个动态变量。其在动态作用域中的工作原理与上面在局部变量中提到的动态变量的原理是相同的。就拿上面的例子来说：

1) 我们使用defvar定义*x*时，解释器就为*x*建立了全局绑定关系栈，并将绑定关系(*x* <- 11)压入栈；

2) 执行(foo)时，解释器从栈顶得到*x*的当前值为11；

3) 执行(let ((*x* 13)) (foo))时，解释器又将动态变量*x*的新绑定关系(*x* <- 13)压入栈，这样在执行后面的(foo)时，栈顶的绑定关系就为(*x* <- 13)，即执行结果为13；当解释器执行体离开该作用域时，绑定关系(*x* <- 13)从栈中弹出；

4) 最后再执行(foo)，栈顶的绑定关系已经变成了(*x* <- 11)，所以(foo)的执行结果又变成了11。

使用setf也可以隐式地引入一个全局变量，但与使用defvar或defparameter显式定义的全局变量不同，setf引入的全局变量并非动态变量：

[1]> (setf *x* 11)

11

[2]> (defun foo ()

(print *x*))

FOO

[3]> (foo)

11

[4]> (let ((*x* 13)) (foo))

11

在使用源文件编写代码的情况下，我们推荐使用defvar或defparameter定义全局变量。

另外不得不提的是动态变量是把双刃剑，动态变量在函数(子程序)层次之间建立一个隐含的关系，减少了参数传递。但同时也降低了程序的可读性，可靠性以及运行性能。

四、常量

C程序员更喜欢使用宏来表示常量，但Common Lisp提供了专门的defconstant宏来定义一个常量，其语法形式如下：

(defconstant var-symbol value

optional-documentation-string)

关于常量的内容很简单，但这里还是要注意以下两点：

1、和全局变量类似，Common Lisp常量也有自己的命名惯例，一般以"+constant-name+"为命名格式，名字两旁各加一个加号(+)，不过这个惯例的受重视程度和遵守程度显然不如全局变量那个;

2、常量的名字不能用于作函数的形式参数，比如：

[1]> (defconstant +y+ 2)

+Y+

[2]> (defun foo (+y+) (print +y+))

*** – FUNCTION: +Y+ is a constant, may not be used as a variable

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论