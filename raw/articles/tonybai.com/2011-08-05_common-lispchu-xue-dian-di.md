---
title: Common Lisp初学点滴
url: https://tonybai.com/2011/08/05/some-experience-of-common-lisp-beginner/
published: '2011-08-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Common Lisp初学点滴

[Common Lisp](http://tonybai.com/2011/06/21/hello-common-lisp/)是一门Interactive语言，比较容易上手。无论你是用[CLISP](http://www.clisp.org)，[SBCL](http://www.sbcl.org)还是[Clozure CL](http://ccl.clozure.com)，你都可以很快地写出一个"[Hello, World](http://bigwhite.blogbus.com/logs/138644306.html)"程序出来。不过千万不要因此低估了Common Lisp，前人的经验表明：Common Lisp是门庞大且复杂的语言，其学习曲线可并不低。要想真正掌握它，需要你有持续的热情、足够的耐心和不断的练习。我接触Common Lisp时间也不长，是个地地道道的初级选手。这段时间看了些书，做了一些练习，这里把我初学Common Lisp过程中的点点滴滴记录下来，以备忘。

俗话说：工欲善其事，必先利其器。Common Lisp开发者们也有着自己一套高效的开发工具。目前无论是在Windows还是在Linux或是其他平台上，最受Lisper们推崇的工具组合是[Emacs](http://www.gnu.org/software/emacs)+ [Slime](http://common-lisp.net/project/slime)(The Superior Lisp Interaction Mode for Emacs)。鼎鼎大名的Emacs这里就不说了，Slime对于很多非Lisp开发者来说是一个陌生的名字，我们可以把它看成是一种专门为Lisper们提供的一个嵌入到Emacs中的IDE，通过它我们可以在Emacs编辑器中直接进行Lisp代码的求值，编译，宏扩展，符号定义的查找，名字的自动补全以及在线文档查询等操作。我平时开发更多使用的是另外一种编辑神器-[VIM](http://http://tonybai.com/2008/12/30/in-depth-study-vim/)，幸运的是已经有人将Slime移植到了Vim下，Slime摇身一变，变成了[Slimv](http://www.vim.org/scripts/script.php?script_id=2531)（The Superior Lisp Interaction Mode for Vim）。由于接触时间较短，我目前尚不确定在功能上Slimv是否完全等同于Slime。不过就目前来看，Slimv的确让Vim下Common Lisp代码的编写变的高效了许多。

Slimv的安装极其简单：将Slimv包下载到你的$HOME/.vim下（这里以Linux下的安装为例），直接解压即可。Slimv首先为Vim提供了一种名为Paredit Mode(.vim/doc/paredit.txt )的编辑模式，这种模式专门针对Lisp代码源文件，诸如以.lisp为后缀名的文件。该编辑模式保证内容中所有括号、方括号以及双引号均平衡出现，即成对匹配。当你敲入"("，该模式会自动补充对应的")"；删除半个括号时，另半个括号也被自动删除。初次使用Paredit mode很不习惯，特别是不知如何在括号的外层再包裹一层括号，也就是将(list 1 2)变为((list 1 2))。每次在(list 1 2)开始处输入"("，都会得到"()(list 1 2)"。后来才在Stackoverflow上觅到答案：原来先输入"\"再输入"("时，Slimv不会自动补充")"，通过这种方式可以在括号的外围再加上一层括号了，在Lisp实际编程过程当中，嵌套括号的情况还是很多的。

打开一个名为xx.lisp的源文件，Slimv就会自动发挥作用。在Vim的命令模式下，敲入",c"，Slimv会自动启动Swank Server，这个Server运行着一个Common Lisp的REPL，接收并处理嵌入在Vim中的Slimv client端发出的求值、编译、调试等请求，保存你在Vim中与REPL的session内容。Slimv同时会在Vim里创建一个REPL窗口，不过这仅是用来等待你的输入，真正的求值等操作是在Swank Server完成的。

Slimv会自动Detect你已安装的Common Lisp实现，在我的已经安装过Clisp和SBCL的系统中，Slimv优先选择了SBCL。 关于Slimv，这里不再多说什么了，因为其作者已经编写了一份很详尽的[Tutorial](http://kovisoft.bitbucket.org/tutorial.html)在这里，有兴趣的朋友可以参考之。

我在读的Common Lisp书籍主要有两本：一本是"[黑客与画家](http://book.douban.com/subject/6021440/)"的作者Paul Graham编写的"[ANSI Common Lisp](http://book.douban.com/subject/1456906/)"，另外一本则是Peter Seibel的"[Practical Common Lisp](http://www.gigamonkeys.com/book/)"(据说该书的中文译本已由[binghe](http://tianchunbinghe.blog.163.com/blog/static/7001201102794634421/)完成)。这一周多来，我快速地浏览了Peter Seibel的"Practical Common Lisp"，除了惊奇于一些之前未曾接触过的特殊语法结构（如Closure）之外，也感叹于Common Lisp的复杂，数不尽的function, macro和special operator让我有些迷失和混淆。另外Peter Seibel自称书中有关macro的例子都很初级，但就是这样初级的macro也是甚难以理解的。关于macro的深入领会，我看只能指望Paul Graham的大作："ANSI Common Lisp"和"on lisp"了。

另外一本名为"[Common Lisp Quick Reference](http://clqr.berlios.de/index.php)"的小书也值得一看，不过更适合Common Lisp老手查阅手册时使用。

浏览完"Practical Common Lisp“后，继续精读"ANSI Common Lisp"，并且对其中的习题也不放过。这些练习估计很初级，不过对于我这个初级选手来说正合适。刚刚看完第二章(Welcome to Lisp)，这里将我的习题答案放到这里，供大家批评指正：

练习1.

(a) 14

(b) (1 5)

(c) 7

(d) (NIL 3)

练习2.

[1]> (cons 'a '(b c))

(A B C)

[2]> (cons 'a (cons 'b (cons 'c nil)))

(A B C)

[3]> (cons 'a (list 'b 'c))

(A B C)

练习3.

[1]> (defun my-fourth (x)

(car (cdr (cdr (cdr x)))))

MY-FOURTH

[2]> (my-fourth '(1 2 3 4 5))

4

练习4.

[1]> (defun my-max (x y)

(if (> x y) x y))

MY-MAX

[2]> (my-max 5 6)

6

[3]> (my-max 7 6)

7

以上方案只适用于整数等适用>进行比较的类型，下面是一个更加通用的版本：

[1]> (defun my-max1 (x y comp_func)

(if (funcall comp_func x y) x y))

MY-MAX1

[2]> (defparameter *cf* (lambda (x y) (if (> x y) t nil)))

*CF*

[3]> (my-max1 5 6 *cf*)

6

[4]> (my-max1 7 6 *cf*)

7

[5]> (defparameter *ccf* (lambda (x y) (if (char> x y) t nil)))

*CCF*

[6]> (my-max1 #\c #\b *ccf*)

#\c

[7]> (my-max1 #\c #\d *ccf*)

#\d

练习5.

(a) enigma函数的功能是找出list中是否有值为nil的元素，如果有，返回T；否则返回nil

(b) mystery函数的功能是返回x在y列表中的位置(下标)

练习6.

(a) x = car

(car (car (cdr '( a (b c) d ) ) ) )

(b) x = or

(or 13 (/ 1 0))

注：短路求值，后一项在13为t的情况下不被求值，避免了divide by 0错误

(c) x = apply

注意funcall与apply的区别

(funcall function arg1 arg2 …)

== (apply function arg1 arg2 … nil)

== (apply function (list arg1 arg2 …))

练习7.

(defun have-list-param-p (x)

(let ((result nil))

(dolist (obj x)

(if (listp obj)

(setf result t)))

result))

[1]> (load "list_param.lisp")

;; Loading file list_param.lisp …

;; Loaded file list_param.lisp

T

[38]> (have-list-param-p '(1 2 3))

NIL

[39]> (have-list-param-p '(1 (2 3) 4))

T

练习8.

(a)

iterative solution:

(defun print_dots (number-of-dots)

(do ((i 1 (+ i 1)))

((> i number-of-dots))

(format t ".")))

recursive solution:

(defun print_dots (number-of-dots)

(let ((i number-of-dots))

(if (> i 1)

(print_dots (- number-of-dots 1)))

(format t ".")))

练习9.

(a) 问题所在：remove返回一个新的lst，原来的lst如果包含nil，则+会提示nil is not a number

修改后：

(defun summit (lst)

(setf lst (remove nil lst))

(apply #'+ lst))

(b) 问题所在：导致无穷递归，提示Program stack overflow. RESET

修改后：

(defun summit (lst)

(if lst (+ (or (car lst) 0) (summit (cdr lst))) 0))


Common Lisp与[Haskell](http://tonybai.com/2010/11/14/the-chinese-translation-project-for-programming-in-haskell/)不同，Common Lisp并非纯函数式编程语言，其中包含了诸多命令式(imperative)的元素，这样对于习惯了命令式编程的初学者来说，在学习过程中就不会感觉到过于剧烈的思维跳跃了。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

lisp学起来麻烦么？几乎没学过编程的小白飘过。

括号外面加括号的方法是，把光标移动到括号上，然后输入 ,W

更简洁的写法：

(defun summit-apply (lst)

(apply #’+ (remove nil lst)))

你的版本有的问题,(nil 1 2 3)直接返回0

(defun summit-rec (lst)

(if lst

(+ (or (car lst) 0) (summit-rec (cdr lst)))

0))

GNU CLISP 2.49和LispWorks 6.0.1中

结果都是0呀，你试试。

(car ‘(nil 1 2 3))结果为nil,所以在你的版本中就直接返回0

不会就如递归的