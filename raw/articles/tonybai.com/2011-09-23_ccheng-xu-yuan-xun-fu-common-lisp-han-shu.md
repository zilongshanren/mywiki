---
title: C程序员驯服Common Lisp – 函数
url: https://tonybai.com/2011/09/23/c-programers-tame-common-lisp-series-functions/
published: '2011-09-23'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# C程序员驯服Common Lisp – 函数

[Common Lisp](http://tonybai.com/2011/06/21/hello-common-lisp/)是[函数式编程](http://en.wikipedia.org/wiki/Functional_programming)语言，其基本组成单元自然是函数。对Common Lisp函数的理解也是学习Common Lisp语言的关键。另外与C语言以内存单元修改为主要编程方法不同，Common Lisp的主要编程方法是将函数应用于参数。这里我们分别用两种范式风格实现同一个函数，该函数用于取得第n个fibonacci数（n从0开始）：

;; 命令式风格

(defun imperative-fibonacci (n)

(let ((first 0)

(second 1)

(sum 0))

(dotimes (i n)

(progn

(setf sum (+ first second))

(setf first second)

(setf second sum)))

first))

;; 函数式风格

(defun functional-fibonacci (n)

(cond

((= 0 n) 0)

((= 1 n) 1)

(t (+ (functional-fibonacci (- n 1)) (functional-fibonacci (- n 2))))))

对比一下我们可以看出函数式风格代码更加简洁，可读性更强，更易于理解。虽然使用Common Lisp也可以写出[命令式风格](http://en.wikipedia.org/wiki/Imperative_programming)的代码，不过我们强烈建议你使用函数式风格，这才是Common Lisp的首选范式 – 即用自然而然的函数嵌套调用或递归调用，而不是堆砌一些修改变量值的语句。C语言中也有函数，但与Common Lisp语言中函数的区别就在于其内部实现均为对变量的修改操作，就像上面例子中imperative-fibonacci函数定义的那样。

一、定义新函数

Common Lisp使用defun宏来定义一个新函数，其语法形式如下：

(defun function-name (param*)

"Optional documentation string."

expr1

expr2

expr3

… )

其实我在之前的几篇文章以及上面的例子中已经多次用到了defun宏，与C语言的函数原型相比，defun定义的函数缺少了一些类型信息，包括返回值类型信息和参数列表中参数的类型信息。

defun定义的函数在全局作用域可见，即使这个定义是嵌套在另外一个函数定义中的(标准C是不允许函数嵌套定义的)：

[1]> (defun foo (x)

(print x)

(defun bar (y)

(print (1+ y))))

FOO

[2]> (foo 1)

1

BAR

[3]> (bar 2)

3

注意：嵌套在其他函数定义中函数定义，如bar，其生命周期起始于外围函数执行后，例如例子中foo函数未执行前，bar是未定义的。

对于C程序员来说，也许Common Lisp函数定义与C函数定义最大的不同在函数参数列表上。C语言的函数只支持两种参数列表形式：定长参数列表和[变长参数](http://tonybai.com/2008/05/07/also-talk-about-c-variable-length-args/)列表，比如：

int main(int argc, char* argv[]); /* 定长参数列表 */

int printf( const char* format, …); /* 变长参数列表 */

而Common Lisp函数对参数列表的支持更加灵活，参数的类型更加丰富，功能也更为强大。下面我们逐一来看。

Common Lisp函数参数列表默认都是定长的，参数也是必选的(required)，也就是说参数列表中有几个形式参数，你在调用该函数时就需要传入等量的实际参数，不能多，也不能少，例如：

[1]> (defun foo (x y) (print (+ x y)))

FOO

[2]> (foo 1)

*** – EVAL/APPLY: too few arguments given to FOO

[3]> (foo 1 2 3)

*** – EVAL/APPLY: too many arguments given to FOO

[4]> (foo 1 2)

3

除了参数列表的必选参数外，Common Lisp还支持可选参数(Optional Parameter)。参数列表中的可选参数由&optional指定，例如：

(defun foo (a b &optional c d)

(print a)

(print b)

(print c)

(print d))

其中位于&optional后面的c，d为可选参数；如果未显式指定默认值，则其值为NIL。

[1]> (foo 1 2)

1

2

NIL

NIL

我们可以为可选参数指定默认值，例如：

(defun foo (a b &optional (c 10) (d 11))

… …)

[2]> (foo 1 2)

1

2

10

11

可以看出对于指定了默认值的可选参数，如果调用时没有为可选参数传入实际参数，则可选参数将绑定默认值。可选参数的默认值不仅仅可以是常量值，还可以是全局变量或该可选参数左侧的某个必选参数，例如：

(defvar *x* 13)

(defun foo (&optional a b c (d *x*))

… …)

和

(defun foo (&optional a b c (d a))

… …)


如果有必选参数，那可选参数必须放在必选参数的后面，但我们可以将一个函数的所有参数都定义为可选参数，如：

(defun foo (&optional a b (c 10) (d 11))

… …)

在带有可选参数的函数体内我们如何知道该函数被调用时外面是否给可选参数传入实际参数了呢？Common Lisp提供了一个指示器，你可以将该指示器放在可选参数默认值的后面，就像这样：

(defun foo (&optional a b (c 10) (d 11 d-supplied-p))

(print a)

(print b)

(print c)

(print d)

(print d-supplied-p))

如果函数在执行时可选参数绑定了实际参数而不是默认值，则该指示器的值将为T，否则为NIL。

[1]> (foo 1 2 3 4)

1

2

3

4

T

[2]> (foo 1 2)

1

2

10

11

NIL

Common Lisp语言引入可选参数至少有两个用途，一是为了适应某些场合的需求：一些场合的确不需要显式为所有参数传递实际参数；二是我们通过可选参数可以为某些参数显式地设置默认值。

在Common Lisp中，与[C语言变长参数](http://tonybai.com/2008/05/07/also-talk-about-c-variable-length-args/)列表对应的是函数列表中的rest参数。rest参数通过在参数前面的&rest关键字修饰。通过rest参数，我们可以定义出类似format这样接受不定个数参数的函数，例如：

[1]> (defun foo (x y &optional z &rest others)

(print x)

(print y)

(print z)

(mapcar #'print others))

[2]> (foo 1 2 3 4 "hello lisp")

1

2

3

4

"hello lisp"

(4 "hello lisp")

在函数定义内部rest参数是以一个list的形式存在的，例如上面例子中，传入函数体内的参数others的值实际上是(4 "hello lisp")。

我们知道C语言虽然支持变长参数列表，但其参数列表中至少需要有一个必选参数，例如：int printf( const char* format, …)中的format参数是无法省略的；但是Common Lisp就不同，Common Lisp支持完全的变长参数列表，例如：(defun my-add (&rest addends) …)

Common Lisp还提供一种C语言中没有的参数类型 – keyword参数。keyword参数允许你只为参数列表中的某个特定参数传入实际参数，这种能力是rest和optional参数所不具备的。我们可以通过&key来指示keyword参数，如：

[1]> (defun foo (&key x y z)

(print x)

(print y)

(print z))

作为keyword参数，如果在函数调用时没有为其显式赋值，那么该参数的值将为NIL。我们可以通过如下方式为特定的keyword参数赋值：

[2]> (foo :y 2)

NIL

2

NIL

Keyword参数赋值是不用考虑赋值先后的顺序的，例如：

[3]> (foo :z 11 ![:x](../../assets/de60a9c94e98b4bc.gif)


13

NIL

11

对于带有keyword参数的函数，调用该函数时要么不为任何keyword参数传参，要么至少为其中某一个keyword参数传参，不能只为必选参数传参，如：

[1]> (defun foo (&key x y z)

(print x)

(print y)

(print z))

[2]> (foo 1)

*** – FOO: keyword arguments in (1) should occur pairwise

与Optional参数类似，keyword参数也可以指定默认值，也可以通过指示器来标定keyword参数到底是否绑定了外面传入的实际参数，其中默认值既可以是常量也可以是其左侧其他keyword参数组成的表达式，例如：

[1]> (defun foo (&key (x 17) (y 15 y-supplied-p) z)

(print x)

(print y)

(print y-supplied-p)

(print z))

[2]> (foo :z 23)

17

15

NIL

23

在之前有关keyword参数的例子中我们使用的形式参数多以x，y这样的简单名字命名，这些名字虽便于函数定义内部使用，但是对于这个函数的调用者来说，这些名字却没有什么实际含义。keyword参数支持通过别名方式解决这个问题：

[1]> (defun foo (&key ((:name a)) ((:age b)) ((:gender c) "Unknown"))

(print a)

(print b)

(print c))

[2]> (foo :name "tony" :age 29)

"tony"

29

"Unknown"

Common Lisp中函数的返回值默认为函数体中最后执行的那个表达式的求值结果，上面举的例子也都是这种情况。在C语言中我们通过return语句可以从函数体内的任何位置主动退出该函数，在Common Lisp中我们同样可以用return-from达到这一目的，例如：

[1]> (defun foo (x y)

(if (< x 0)

(return-from foo "IIlegal X Value"))

(if (< y 0)

(return-from foo))

(+ x y))

FOO

[2]> (foo 1 2)

3

[3]> (foo -1 2)

"IIlegal X Value"

[4]> (foo 1 -2)

NIL

对于函数而言，return-from的语法形式为：(return-from func-name optional-value)，若不指定返回值，那么默认return-from的返回值为NIL。

二、匿名函数

与C语言不同，Common Lisp支持定义匿名函数，例如：

[1]> (funcall #'(lambda (x) (print (1+ x))) 2)

3

上面例子中这行语句既包含了函数定义，也包含了函数调用。与之前使用defun定义有名函数不同的是，这次我们定义出来的函数没有指定函数名，这种使用lambda关键字定义的函数被称作为匿名函数。

从例子中也可以看出，匿名函数的定义也很简单，其一般形式为：

(lambda (args*) body-form*)

我们也称这种表达式为lambda表达式。lambda表达式定义的匿名函数与有名函数一样，也支持使用optional，rest和keyword参数。

三、高阶函数

函数式编程语言与命令式语言除了在风格方面的不同之外，最大的不同点之一在于函数式语言中函数已经成为了[一等公民](http://en.wikipedia.org/wiki/First-class_citizen)(first-class citizen)，与整型、字符串等原生类型具有同等的地位。更具体地说，函数成为一等公民意味着我们可以像对待整型数、字符串那样将函数当作数据对待：将函数赋值给变量、将函数作为参数传递给其他函数以及将函数作为返回值返回给函数调用者等等。作为C程序员你也许会说这似乎与C语言中的函数指针很类似啊，但别忘了C语言真正原生支持的是类型是指针，而不是函数。

有了一等公民地位的函数，我们就得到了[高阶函数](http://en.wikipedia.org/wiki/Higher-order_function)。高阶函数就是那些接受其他函数为函数或将其他函数作为返回值的函数。例如Common Lisp提供的标准函数sort就接受一个比较函数作为参数：

[1]> (defun integer-over-than (x y) (> x y))

INTEGER-OVER-THAN

[2]> (sort '(5 2 98) (function integer-over-than))

(98 5 2)

[3]> (sort '("hello" "world") (function string>=))

("world" "hello")

标准库中的sort函数接受一个自定义的比较函数作为参数，并在内部将传入的函数应用于参数list。例子中我们没有直接将integer-over-than传给sort，而是使用了(function integer-over-than)。function是Common Lisp提供的一个特殊操作符，将其应用于函数名可以得到该函数名对应的函数对象。比如通过(function foo)，我们可以得到名字为foo的内部函数对象。如果没有foo这个函数定义，解释器会提示"undefined function FOO"。可以看出真正被当作一等公民对待的不是foo这个符号，而是foo这个符号名字背后所对应的那个函数对象，也就是函数在Common Lisp中的内部表示形式。我们在将函数绑定到某个变量或将函数传递给某个函数作为实际参数时，我们都需要使用这个内部函数对象，而不是foo这个符号，例如：

[1]> (sort '(5 2 98) integer-over-than)

*** – EVAL: variable MY-OVER-THAN has no value

[2]> (setf *sort-func* integer-over-than)

*** – EVAL: variable MY-OVER-THAN has no value

[3]> (setf *func* (function my-over-than))

# FUNCTION MY-OVER-THAN (X Y) (DECLARE (SYSTEM::IN-DEFUN MY-OVER-THAN)) (BLOCK MY-OVER-THAN (> X Y))>

Common Lisp提供了一个语法糖用于简化function的使用，即我们可以用#'代替function操作符，比如：#'foo就等价于(function foo)。

那么在接受函数作为参数的函数定义内部我们如何使用函数对象呢？Common Lisp提供了两个函数funcall和apply用来执行函数对象对应的函数。我们先以funcall为例，funcall的语法形式如下：

(funcall function-obj args*)

例如：

[1]> (defun foo (x y) (print (+ x y)))

FOO

[2]> (defun my-add (x y f) (funcall f x y))

MY-ADD

[3]> (my-add 1 2 #'foo)

3

apply与funcall的不同之处在于其接受的参数格式有不同，apply的语法形式如下：

(apply function-obj args* other-args-list)

直观地比较：(apply #'+ '(1 2 3))就等价于(funcall #'+ 1 2 3)，不同的是使用apply需要将各个参数打包到一个list中，或至少保证最后一个参数为list。下面几种调用方式与(apply #'+ '(1 2 3))都是等价的：

(apply #'+ 1 '(2 3))

(apply #'+ 1 2 '(3))

lambda表达式用于定义一个匿名函数，我们同样可以通过#'来获得这个匿名函数对应的函数对象，例如：

#'(lambda (x y) (print (+ x y)))

匿名函数对象可以直接作为实际参数传递给函数，我们也可以通过funcall来直接执行匿名函数，例如：

[1]> (my-add 1 2 #'(lambda (x y) (print (+ x y))))

3

[2]> (funcall #'(lambda (x y) (print (+ x y))) 1 2)

3

以上是推荐的标准用法，下面方法（去掉了lambda前面的#'）虽然也可以达到相同效果，但不推荐使用：

[1]> (my-add 1 2 (lambda (x y) (print (+ x y))))

3

[2]> (funcall (lambda (x y) (print (+ x y))) 1 2)

3

[3]> ((lambda (x y) (print (+ x y))) 1 2)

3

在C语言中我们通过函数指针和回调手法也可以模拟一些高阶函数的行为，这里就不赘述了。

四、闭包(Closure)

市面上有很多编程语言都支持[闭包](http://en.wikipedia.org/wiki/Closure_(computer_science))，比如JavaScript，Python，Perl，Ruby等。这里所说的闭包不是离散数学里的那个闭包，而是编程语言引入的一种机制，目前对于编程语言中的闭包尚未有一个精确的定义，但一般认为闭包是引用了外部作用域(但不是全局作用域)的变量的函数，这个被引用的变量与这个函数一同存在，即使是脱离了定义它们的上下文环境。

Common Lisp支持闭包，关于Common Lisp闭包的一个最典型例子是这样的：

[1]> (setf *fn* (let ((i 0))

#'(lambda () (setf i (+ i 1)))))

#FUNCTION :LAMBDA NIL (SETF I (+ I 1))>

[2]> (funcall *fn*)

1

[3]> (funcall *fn*)

2

[4]> (funcall *fn*)

3

按照之前我们对变量的理解，let引入的i只是一个局部变量，在离开定义的环境后，该变量生命周期将终结。理论上我们三次调用*fn*所对应的你们函数得到的结果应该是相同的才对。但就是由于在let构造的局部作用域内的那个匿名函数引用了外部的变量i，导致变量i可以脱离其原生作用域的束缚，让其生命周期等同于了其内部的那个匿名函数，这个内部的匿名函数就被称为闭包，而那个被引用的外部变量被成为[自由变量](http://en.wikipedia.org/wiki/Free_variables_and_bound_variables)(free variable)。当我们连续调用函数*fn*时，i就像一个全局变量一样，每次值都加一。

引用了自由变量的闭包似乎是终结了自由变量的局部绑定关系，将自由变量从局部作用域环境中取出，并重新放入一个与闭包同生命周期的新作用域。自由变量会常驻内存中，这也是闭包的常用场景之一。闭包的另外一个用途可能就是出于保护自由变量的考虑，让自由变量只有通过闭包函数才能访问到。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

tony大叔写篇宏相关的吧。