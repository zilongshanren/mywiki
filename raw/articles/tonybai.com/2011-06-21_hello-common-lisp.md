---
title: Hello，Common Lisp
url: https://tonybai.com/2011/06/21/hello-common-lisp/
published: '2011-06-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Hello，Common Lisp

[Paul Graham](http://www.paulgraham.com)不愧被誉为[Lisp](http://en.wikipedia.org/wiki/Lisp_(programming_language))的超级推手，他的煽动力真的是很强悍。这不才刚刚看完一遍他编写的《[黑客与画家](http://book.douban.com/subject/6021440)》后，我就决定将[Common Lisp](http://en.wikipedia.org/wiki/Common_Lisp)作为今年计划学习的那门新语言，而且从现在就开始。

去年曾囫囵吞枣般的学习过[Haskell](http://tonybai.com/2010/11/14/the-chinese-translation-project-for-programming-in-haskell/)，一门通用且庞大的纯函数式编程语言。在惊叹于Haskell如此与众不同且功能强大的同时，也为Haskell Monad那魔鬼般的蹩脚语法所苦恼，而Monad的引入就是为了隔离副作用，并让你可以利用些过程式命令式语言解决问题的范式。

原以为Common Lisp也是一门函数式编程语言，应该与Haskell很像，但在看了《[ANSI Common Lisp](http://book.douban.com/subject/1456906)》一书后的前几章后我才发现其实不是那么回事儿。Common Lisp设计初衷其实是一门支持多范式的通用语言。除了语法上更接近于函数式编程范式外，你完全可以用Common Lisp写出具有过程式特点的代码（而且看起来也很容易）。另外Common Lisp Object System(CLOS)还给你提供了OO范式的选择。与Haskell相比，对于我这个C程序员来讲，Common Lisp带来思维跳跃似乎更小些，更有利于后续的学习和使用。

与Haskell的强类型和静态类型（即使你不显式指出类型，Haskell也会根据一些上下文的clue推导出类型，如果它发现类有不匹配，那么编译期间就会报错）不同，Common Lisp是动态类型和弱类型的，当然你也可以显式声明类型，但这么做也仅有利于编译器对代码的速度优化，并不能阻止什么。如：

> (declaim (type fixnum count))

> NIL

> (format t count)

*** – EVAL: variable COUNT has no value

> (setf count "hello lisp")

> "hello lisp"

> (format t count)

> hello lisp

> NIL

看到了吧，即使我们显式声明了count为fixnum类型，我们依然可以用字符串为其赋值。

Lisp语法十分简单：万物皆在括号内，无论代码还是数据。Lisp一直因括号泛滥而被诟病，不过对于我来说还好，也许是因为在C语言中也没少使用括号的缘故吧。另外现在的编辑器都支持高亮括号匹配，这样只要你细心些，写代码时基本不会出现因括号不匹配导致的一些问题。

编程语言影响思维习惯，但思维的转变不是一蹴而就的，也就是说用惯了C、Python等语言后，再去学习类似Common Lisp这类语言的确有些困难。遇到某问题时，或多或少还会首先以过程式的思维去考虑。另外Common Lisp也确实不是一门“小语言”，和Haskell一样，Common Lisp也很庞大，这也使得这些语言的学习曲线陡增。


之前一直认为Lisp也是一门解释性的语言，类似Python采用解析器的方式执行，性能不会很快。后来经了解后才得知诸多编译器（如[CLisp](http://clisp.org/)）都是将源代码编译为某种格式的字节中间码，这样不仅性能得到了提升，可移植性还得到了兼顾。当然Lisp性能与C比起来还是要差出至少一个数量级的。Common Lisp的编译器我装了两个：CLisp和[SBCL](http://www.sbcl.org)，目前来看似乎后者的开发更活跃一些。我个人则更多地使用CLisp。

这里必须得承认的是Lisp语言的应用还是比较小众的，甚至很多程序员都没有听说过有Lisp这门语言的存在。在实际商业开发中更是很少见到用Lisp实现的系统，这方面Haskell也有着同样的”感受“。不过近几年Lisp各种方言大有回升之势，Lisper们需要是耐心和时间。如果要想了解如何利用Common Lisp进行一些实际系统的开发，那么你就不能放过Peter Seibel于2005年编写的《[Practical Common Lisp](http://book.douban.com/subject/1456903)》一书。后来出版的《[Real World Haskell](http://book.douban.com/subject/3134515)》想必也是学习Peter Seibel试图为Haskell开发者们找到一条实际应用之道吧。

但有关Common Lisp的入门书，我还是觉得Paul Graham的《Ansi Common Lisp》更适合，另外在这之前可以先拜读一下Paul Graham的文章"[The Roots of Lisp](http://www.paulgraham.com/rootsoflisp.html)"，这将对Lisp的学习大有裨益。

既然本文的主题为Hello，Common Lisp，那最后还是按学习新语言的惯例，在这里向大家展示一下用Common Lisp是如何编写[Hello World](http://en.wikipedia.org/wiki/Hello_world_program)的吧：

;; HelloWorld.lisp

(defun hello-world ()

(format t "hello, world!"))

(hello-world)

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

呵呵 跟樓主一樣也是因為看了黑客與畫家，才打算學習lisp的。目前剛開始也使用的是Clisp，感覺《ANIS Common Lisp》《Land of Lisp》《Practical Common Lisp 》實用的書也就這幾本了。

看得有点神忽！

为了保持示例上下文的一致性，这里貌似

(declaim (type fixnum *count*))

要改为

(declaim (type fixnum count))

*count*和count是不相关的