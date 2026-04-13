---
title: C程序员驯服Common Lisp – 入门
url: https://tonybai.com/2011/08/30/c-programers-tame-common-lisp-series-introduction/
published: '2011-08-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# C程序员驯服Common Lisp – 入门

毫无疑问，[Common Lisp](http://tonybai.com/2011/06/21/hello-common-lisp/)是一门庞大且复杂的语言，学习曲线并不平坦。对于一个从未接触过[函数式语言](http://en.wikipedia.org/wiki/Functional_programming)、交互式语言以及动态类型语言的C程序员来说，学习Common Lisp显然是一个很大的挑战。

也许有人会问："[C语言](http://tonybai.com/tag/C/)已经无所不能了，为何还要学习Common Lisp？"在这里我不想说太多冠冕堂皇的话，至少对我而言，理由有三：

一是好奇，在C语言的世界里待得久了，总想探出头来吸几口新鲜空气，这次我选择了Common Lisp；

二是为了变成一名更好的程序员。为何学习Common Lisp就能成为一名更好的程序员呢？这不是我的观点，而是诸多牛人或大师们（包括[Paul Graham](http://paulgraham.com/)、[Peter Norvig](http://norvig.com)以及另外一个Peter：Peter Seibel等）的观点。不过不管你们信不信，反正我是信了。这个观点的关键思想就是一门语言可以影响一个程序员的思维方式。我相信Common Lisp可以给我带来一种不同于以往的新的编程思维方式，这样至少比只有一种思维方式要好，不是吗；

最后，Lisp是一门可编程的编程语言，可以很容易扩展自身并且创造一门新的语言。我无法不动心于如此一门强大的语言。

学习总是需要一些付出的。Jolt大奖得主《[Practical Common Lisp](http://www.gigamonkeys.com/book)》的作者Peter Seibel花了一年的时间放下一切潜心学习Common Lisp并终有所成。我们还有工作，有生活压力，无法像Seibel那样潇洒，但我们依旧可以去学习Common Lisp，循序渐进地学，一步一步来"驯服"Common Lisp这个"猛兽"。"猛兽"被驯服后，才能为你所用，发挥出异常的威力，不是吗？我们需要的仅是恒心和足够的耐心罢了。

"驯服"意味着"学会"，何为学会一门语言？只是知晓语法，看懂代码还远远不够，那些仅仅叫知道或了解或"纸上谈兵"，还谈不上真正地"学会"。古人云："学以致用"，只有在实际中可以灵活自如的使用了，才叫真正的"学会"了。

现在只是开始！这里我会按照C程序员学习C语言的逻辑展开，为了更加贴近C程序员的思维模式，我选择了这种相对平滑的学习方式。也许最初的几篇会让你觉得Common Lisp很像一门[命令式语言](http://en.wikipedia.org/wiki/Imperative_language)^_^！

言归正传！学习一门编程语言之前，最好先弄清楚该语言在当前众多语言中的位置，了解一下它的前世今生，这有助于你对这门语言的认知。不过关于Common Lisp的详细历史这里就不赘述了，在进行下面内容之前，请先阅读一下[维基百科](http://zh.wikipedia.org/wiki/Common_Lisp)，或是读读几本经典Common Lisp书籍（如《[ANSI Common Lisp](http://book.douban.com/subject/1456906/)》、《[On Lisp](http://www.douban.com/subject/1432683/)》以及《Practical Common Lisp》等）中对Common Lisp历史的介绍。

Common Lisp是[Lisp](http://en.wikipedia.org/wiki/Lisp_(programming_language))语言大家族中的一分子，和[Scheme](http://en.wikipedia.org/wiki/Scheme_(programming_language))等一样，它也是一门Lisp方言(Dialect)。与C语言相比，Lisp更加古老，是史上第二古老的编程语言，仅次于[Fortran](http://en.wikipedia.org/wiki/Fortran)。但Common Lisp比C年轻，它是在上世纪80年代诞生的。与C语言普遍采用的"编辑->编译->调试/执行"的工作方式不同，Common Lisp更多采用的是类似于Python、Ruby那样的交互式的解释器工作模式。你在Common Lisp交互环境中就可以完成上述C语言的所有步骤。这种方式目前看来更易于语言的学习（虽然C语言目前也有解释器的实现，如[Ch](http://en.wikipedia.org/wiki/Ch_(computer_programming))，但C程序员似乎更喜欢传统方式）。

目前市面上Common Lisp的实现有很多种，既有商业收费的，也有开源免费的。商业软件这里就不提了，常用的免费开源的主流Common Lisp解释器包括[CLISP](http://www.clisp.org)、[SBCL](http://www.sbcl.org)(Steel Bank Common Lisp)和[Clozure CL](http://clozure.com)。我个人更喜欢使用CLISP，所以后续有关解释器方面的内容更多以CLISP为主。

CLISP支持诸多平台，你可以很容易得到安装包并顺利的完成安装，关于这方面内容这里就不赘述了。打开一个终端（Windows下打开一个命令行窗口)，敲入"clisp"，回车，你就进入到CLISP提供的Common Lisp顶层环境(Top-Level)当中了(若要进入SBCL，敲入sbcl；若要进入Clozure CL，敲入ccl，以上的前提是这些包的可执行程序路径已经加入到你的PATH环境变量中了)，就像这样：

$ clisp

… …

Welcome to GNU CLISP 2.44.1 (2008-02-23) <[http://clisp.cons.org/](http://clisp.cons.org/)>

Copyright (c) Bruno Haible, Michael Stoll 1992, 1993

Copyright (c) Bruno Haible, Marcus Daniels 1994-1997

Copyright (c) Bruno Haible, Pierpaolo Bernardi, Sam Steingold 1998

Copyright (c) Bruno Haible, Sam Steingold 1999-2000

Copyright (c) Sam Steingold, Bruno Haible 2001-2008

Type :h and hit Enter for context help.

[1]> _

对于所谓的"顶层环境"，熟悉Python和Ruby等解释型语言的朋友并不陌生。它就是一个已经加载了标准Common Lisp包的REPL环境。其中REPL是Read-Eval-Print-Loop的缩写。说白了，这就是一个Common Lisp代码的执行环境，你在里面可以输入Common Lisp代码，这些代码可以被直接执行，执行结果也会立刻展现在你的眼前，或如果遇到错误/异常时，你还可以在里面直接进行代码调试。当然了"顶层"还有一个范围(Scope)的概念在里面，用于区分不同变量和函数的作用域。

我们在CLISP中输入一些字符串、字符以及数字以及简单表达式：

[1]> "hello lisp"

"hello lisp"

[2]> #\c

#\c

[3]> 1

1

[4]> (+ 1 2)

3

CLISP对于我们的输入给予了回应：对于字符串、字符(注意Common Lisp的字符表示法很特别，以#\作为前缀，#\c即C语言中的'c')以及数字，CLISP进行了回显（实际上是对输入求值后的结果），对于"(+ 1 2)"这个计算1和2之和的表达式，CLISP给出了求值后的结果。

我们继续输入一个a：

[5]> a

*** – EVAL: variable A has no value

The following restarts are available:

USE-VALUE :R1 You may input a value to be used instead of A.

STORE-VALUE :R2 You may input a new value for A.

ABORT :R3 Abort main loop

Break 1 [6]>

与前面不同的是，这次CLISP给出了错误提示，求值器（evaluator)无法找到a绑定的值，CLISP进入异常处理模式，或称作调试模式。CLISP给出了三种选择：我们选择输入:R3，可以回到top-level主循环；选择输入:R2，则可以为a赋值。

Break 1 [6]> :R2

New A: 5

5

[7]> a

5

SBCL和Clozure CL与CLISP类似，都会有类似的调试模式，退出调试模式的方法参见各自的提示说明即可。

如果要退出CLISP解释器，我们可以输入"(quit)"，注意quit两边的括号也是命令的一部分；在SBCL中，我们可以输入(SB-EXT:QUIT)退出；Clozure CL的退出方法与CLISP相同。

Common Lisp源代码是由一组[S-expressions](http://en.wikipedia.org/wiki/S-Expression)(symbolic expression)构成的。什么是S-expression呢？这个在Common Lisp书籍中很难找到答案，因为S-expression是一种组织数据的结构，并不是Lisp独有的，只是Lisp恰好也采用了这种结构来组织存储Lisp的代码和数据罢了。在维基百科上，S-expression有一个递归的定义："S-expression要么是一个被成为原子(atoms)的单一的数据对象(data object)，要么是一个S-expressions列表(list)。数字、数组、字符串以及符号都是原子"，比如：

[1]> 13

13

[2]> #(1 2 3)

#(1 2 3)

[3]> "hello"

"hello"

[4]> #'length

#

数字'13'、数组'#(1 2 3)'、字符串"hello"以及符号'length'都是原子。

Lisp将代码和数据都存储于S-expressions当中，这是Lisp与其他主流语言的最大区别之一。我们在编写Common Lisp源码时，需要遵循正确的S-expression格式。前面说过Common Lisp解释器就是一个READ-EVAL-PRINT-LOOP环境，这个环境主要由一个Reader和一个Evaluator构成。Reader负责读取源文件中的文本或者我们在提示符后面输入的文本，检查文本格式是否符合S-Expression要求，直到所有文本都符合格式要求，这样解释器就得到了正确的S-expression：

[1]> (+ 1 2))

3

[2]>

*** – READ from … >: an object

cannot start with #\)

通过上面例子可以看出，Reader识别出了不符合S-expression格式的源码文本。

Reader将文本转换为S-expressions后，Evaluator就开始对S-expression进行校验，校验其是否符合Lisp Code的规范形式(Lisp Form)。

下面的例子说明了Evaluator的作用：

[1]> (foo 1 2)

*** – EVAL: undefined function FOO

毫无疑问，(foo 1 2)是一个有效的S-expression，其通过Reader这关是没有问题的。但是当Evaluator对S-expression"(foo 1 2)"进行验证求值时，却发现无法找到函数foo的定义，这行源码不合法。

简单总结Reader和Evaluator的工作流程就是："源码文本"通过Reader转换为有效的"S-expressions"，后者则由Evaluator转换成有效"Lisp Form"并求值得出结果。

[Common Lisp初学者](http://tonybai.com/2011/08/05/some-experience-of-common-lisp-beginner/)常常被那满眼的括号所吓住，不过事实上括号并没有那么"可怕"。括号其实主要是给Common Lisp解释器(Reader和Evaluator)用的，而不是给程序员看的。现今的代码编辑器都很智能，基本上可以消除括号在编程过程中给你带来的影响（要说一点影响没有也不太可能）。

Common Lisp支持多种注释形式。在C语言中我们用'//'进行单行注释([C99标准](http://en.wikipedia.org/wiki/C99)引入)，而Common Lisp的单行注释符号为';'。C语言采用'/*…*/'进行多行注释，Common Lisp使用的是'#|…|#'。Common Lisp还提供了一种大多语言都不具备的注释方式，那就是将注释直接写到紧邻函数定义的参数列表后面的位置上，这样通过Common Lisp提供的工具，我们可以轻松地提取出该函数的注释，并生成代码文档，比如：

[1]> (defun foo (x) "test comments" (+ x 1))

FOO

[2]> (documentation #'foo t)

"test comments"

由于Common Lisp括号众多，一个风格良好的Lisp程序需要通过良好风格的代码缩进来保证，这方面我推荐AI领域大师Peter Norvig若干年前编写的一篇有关优秀Lisp编程风格的文章《[Tutorial on Good Lisp Programming Style](http://norvig.com/luv-slides.ps)》。

很多C程序员可能还是习惯于将代码写到文件中。Common Lisp解释器提供了将你的源文件加载到顶层环境并直接使用其中的定义的方法：

;; foo.lisp

(defun foo (x) "test foo"

(+ x 1))

[1]> (load "foo.lisp")

;; Loading file foo.lisp …

;; Loaded file foo.lisp

T

[2]> (foo 5)

6

利用load函数我们可将你的源文件加载到顶层环境中，并在顶层环境里使用该源文件中定义的函数。

编程语言初学者总喜欢在终端控制台上看到自己编写的程序的输出结果，那样会产生一种奇妙的成就感，程序员们多陶醉于其中。C程序员最常用的就是printf函数了，Common Lisp中也有与printf等价的函数，它就是format。这里不是专门讲解format函数的，下面仅仅列举一些常见的例子，这些例子应该可以满足你在学习语言初期的需求了：

* 输出整型数

(format t "~d" 1000000) ==> 1000000

(format t "~x" 1000000) ==> f4240

(format t "~o" 1000000) ==> 3641100

(format t "~b" 1000000) ==> 11110100001001000000

上面依次是按十进制、16进制、八进制和二进制输出。

* 输出浮点数

(format t "~f" 3.1415) ==> 3.1415

* 输出字符串

(format t "~a" "hello lisp") ==> hello lisp

* 输出字符

(format t "~c" #\c) ==> c

* 输出换行符

以下借用《ANSI Common Lisp》书中的一个例子：

(format nil "Dear ~a, ~% Our records indicate…" "Mr. Malatesta")

==> "Dear Mr. Malatesta,

Our records indicate…"

format函数的第一个参数表示是否输出到"标准输出(*STANDARD-OUTPUT*"，如果传入t，则表示输出到标准输出设备上。第二个参数与C中的printf函数的第一个参数类似，是一个格式串，不同的是格式串中的指示符(directive)由printf中的'%'变成了'~'。

为了让大家更加直观地了解Common Lisp源代码到底是什么样子的，下面将给出一个Common Lisp的例子程序，这个程序用来计算参数字符串中大写字母的总个数：

我们先给出一个命令式风格的实现版本：

;; upper-char-counter.lisp

(defun upper-char-counter (str)

(let ((len (length str)) (result 0))

(do ((i 0 (+ i 1)))

((>= i len) result)

(if (upper-case-p (char str i)) (setf result (1+ result))))))

即使你不懂Common Lisp语法，你也能大致猜测处理这段代码的逻辑，基本上与下面C代码是等价的：

int upper_char_counter(const char *str) {

int result = 0;

int len = strlen(str);

int i = 0;

while (i < len) {

if (str[i] >= ‘A’ && str[i] <= 'Z') {

result++;

}

i++;

}

return result;

}


下面是一个函数式风格的实现版本：

;; upper-char-counter.lisp

(defun upper-char-counter (str)

(count-if #'upper-case-p str))

[1]> (load "upper-char-counter.lisp")

;; Loading file upper-char-counter.lisp …

;; Loaded file upper-char-counter.lisp

T

[2]> (upper-char-counter "a5B6CD!")

3

这个版本的代码显然更加简洁，但理解起来有些难度。函数count-if接受一个函数和一个字符串作为参数，count-if将函数upper-case-p应用于str中的各个字符上，并将返回true(t)的结果个数累加得到最终返回值。

走到这里，我想大家应该对Common Lisp有了一个感性的认识了，至少可以编写一些命令式风格的简单代码或复制一些现存的代码放到顶层环境中执行了。如果真的是这样，那我的目的就达到了^_^。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

拜谢楼主，同样用C后想搞搞Lisp…………

不过一直没入门，楼主给小弟开了门了…………