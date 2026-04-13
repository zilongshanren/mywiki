---
title: C程序员驯服Common Lisp – 表达式
url: https://tonybai.com/2011/09/02/c-programers-tame-common-lisp-series-expressions/
published: '2011-09-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# C程序员驯服Common Lisp – 表达式

[Common Lisp](http://en.wikipedia.org/wiki/Common_Lisp)程序由一组表达式构成。在"[入门](http://tonybai.com/2011/08/30/c-programers-tame-common-lisp-series-introduction/)"一文中我提到过：Common Lisp使用[S-expressions](http://en.wikipedia.org/wiki/S-Expression)作为表达式(Expressions)的基本语法格式。S-expressions由原子(atoms)和S-expressions列表组成，或者说原子和列表(List)是组成S-expression的基本元素。复杂的源程序都是由简单的表达式组成的，我们在学习编写实用的Common Lisp程序之前，首先要清楚简单表达式的结构和求值方法。

每个Lisp表达式都可以提交给Common Lisp解释器进行求值，并得到一个求值结果。这里我们从简单的原子说起。

一、原子

原子虽然十分简单，但它也是一种表达式。对于原子而言，其求值结果就是其自身的值。下面我们来看看一些常见的原子以及其求值结果：

(1) 数字(Number)

数字是一种原子，其求值结果即为其自身数值。

* 整型数字

[1]> 13

13

[2]> -4

-4

[3]> 0

0

[4]> #xa ;; 16进制数

10

[5]> #o11 ;; 8进制数

9

[6]> #b011 ;; 二进制数

3

[7]> #24r1n ;; 24进制数

47

最后的#24r1n是一种通用N进制数表示形式，N取值范围为2到36，其表示形式为#Nr…。

* 浮点数

[1]> 3.1415

13

[2]> 365e0

365.0

[3]> 365e-3

0.365

[4]> 365f-3

0.365

[5]> 365d-3

0.365d0

[6]> 0.365e20

3.65E19

标志f表示单精度浮点数，标志d表示双精度浮点数，标志e表示默认采用单精度，与f相同。

* 分数

[1]> 5/6

5/6

* 复数

[1]> #C(1.2 3)

#C(1.2 3)

C(1.2 3)对应的复数为1.2+3i。

(2) 字符(character)

单独的字符也是原子，其求值结果也是其自身值。

下面是一些可见字符：

[1]> #\a

#\a

[2]> #\A

#\A

[3]> #\%

#\%

[4]> #\&

#\&

一些常见的控制字符的形式如下：

[1]> #\newline

#\Newline

[2]> #\tab

#\Tab

[3]> #\backspace

#\Backspace

[4]> #\space

#\Space

[5]> #\escape

#\Escape

(3) 字符串(string)

与[C语言](http://tonybai.com/tag/C/)中的字符串不同，Common lisp中字符串结尾并不包含''。但字符串也是原子，其求值结果依旧是其本身。

[1]> "Hello, Common Lisp!"

"Hello, Common Lisp!"

我们可以字符转义将一些特殊字符放入字符串，比如我们可以在字符串中包含双引号：

[2]> (format t "~A ~%" "He said \"I am going to see Harry Potter!\" and then he left.")

He said "I am going to see Harry Potter!" and then he left.

NIL

不过我们无法通过转义方法将tab字符、回车符、换行符放入字符串，只能通过键盘手工输入：

[3]> "Look, here are tabs and some

returns!

Understand?"

"Look, here are tabs and some

returns!

Understand?"

(4) 布尔类型(bool)

布尔值也是原子，但只有两个可选值：t和nil。t代表true，nil代表false，由于比较简单，这里就不细说了。

(5) 符号(symbols)

与[C语言](http://tonybai.com/tag/C)不同的是，Common Lisp中有一种语法元素称为"符号"。符号有些类似于C语言中的标识符，用来表示Lisp程序中使用的名字，诸如函数和变量的名字，像format，hello-foo, *counter*等。Lisp符号的包容性更强，像+，-等在C中为操作符关键字的字符都可以作为符号。

(a b c) ; 一个包含三个符号的list

(a 2 "bar") ; 这个list包含一个符号，一个数字和一个字符串

(+ (* 2 3) 4) ; 这个list包含一个符号，一个列表以及一个数字

符号的求值比较特殊，如果该符号没有绑定到任何值，解释器会提示错误。如果绑定了值，则显示绑定的值：

[1]> a

*** – EVAL: variable A has no value

The following restarts are available:

USE-VALUE :R1 You may input a value to be used instead of A.

STORE-VALUE :R2 You may input a new value for A.

ABORT :R3 Abort main loop

Break 1 [2]> :r3

[3]> (setf a 5)

5

[4]> a

5

二、列表

在实用程序中，我们很少将原子单独作为表达式，我们更多使用的是List，即列表。之前说过Common Lisp的核心就是List，此List不同于我们以往数据结构中学习的那个List，在Common Lisp中，List是程序和数据的载体，别忘了Lisp是"LISt Processing"的缩写，直译过来Lisp就是List处理语言，这也凸显了List在Lisp语言中的核心地位。

绝大多数情况下，Lisp程序字面上就是一组列表集合。掌握对List进行求值的方法就显得尤为重要了。

我们先从一个简单到不能再简单的List入手：

[1]> (+ 1 2)

3

这个List由三个原子组成，一个符号以及两个数字。Common Lisp解释器会首先检查第一个元素是否是一个符号并且是否是一个绑定了有效函数的符号。如果不符合条件则报错。如果第一个元素是符号且绑定合法函数，如+，那么解释器会将后续的元素作为该函数的参数，并自左向右对参数逐个进行求值。

[1]> (length "hello lisp")

10

[2]> ("foo" 1 2)

*** – EVAL: "foo" is not a function name; try using a symbol instead

The following restarts are available:

USE-VALUE :R1 You may input a value to be used instead.

ABORT :R2 Abort main loop

在(+ 1 2)这个例子中，+是一个符合条件的符号，解释器接下来对1和2这两个原子进行求值，前面提到整数是原子，其求值结果即为自身值，所以解释器将1和2传给+，得到最终结果3。

Common Lisp的解释器对参数的求值是自左向右递归进行的，下面是一个稍复杂的表达式，其详细的求值过程如下：

(+ (- 7 (/ 4 2)) (* 3 4))

-> (+ (- 7 2) (* 3 4))

-> (+ 5 (* 3 4))

-> (+ 5 12)

-> 17

解释器从左向右依次对参数进行求值，解释器遇到函数+的第一个参数(- 7 (/ 4 2))，这显然是也是一个减法表达式，解释器递归地对该表达式进行求值；(- 7 (/ 4 2))表达式的第一个参数7为原子类型，其求值结果为自身值7；第二个参数又是一个除法表达式，解释器再一次进行递归求值，进入(/ 4 2)，这是个简单表达式，其求值结果为2；求值程序回到表达式(- 7 2)，得到求值结果5，至此最外层表达式的第一个参数求值完毕，结果为5；解释器继续对最外层表达式的第二个参数(* 3 4)进行求值，这是个乘法表达式，对该表达式求值结果为12，这样我们的顶层表达式就变成了(+ 5 12)，则最终求值结果就为17。这个过程有点类似于树遍历算法中的深度优先遍历算法。

无论是多么复杂的表达式，Common Lisp解释器的求值方法都是如此的。当然解释器不一定会将函数的所有参数都进行求值，比如：(if t 5 (+ 6 7)这个表达式在if条件为t时，只会求值5这个参数，(+ 6 7)这个表达式不会被求值。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论