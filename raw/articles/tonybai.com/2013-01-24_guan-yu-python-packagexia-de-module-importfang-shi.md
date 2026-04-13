---
title: 关于Python Package下的Module import方式
url: https://tonybai.com/2013/01/24/the-module-import-way-under-python-package/
published: '2013-01-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 关于Python Package下的Module import方式

2012年有一个[目标](http://tonybai.com/2012/01/29/plan-and-design-2012/)我没有达成，那就是深入学习和使用[Python](http://www.python.org)语言。这个目标被其他学习任务和工作无情的抢占了，当然最主要的原因还是我重视不够^_^。

近期恰逢有一些Python工程的开发工作要做，就顺便略微深入地学习了一下Python：看了几本Python的英文大部头，比如《[Learning Python 4th Edition](http://book.douban.com/subject/4082016/)》、《[Python Essential Reference 4th Edition](http://book.douban.com/subject/3273420)》、《[Programming Python 4th Edition](http://book.douban.com/subject/4893005)》、《[Expert Python Programming](http://book.douban.com/subject/3285148)》以及《[The Python standard library by example](http://book.douban.com/subject/6540551)》，看得我有些要吐了^_^。虽然之前用Python开发过[buildc](http://code.google.com/p/buildc)，但自我感觉依旧还是一个Python的绝对beginner，这 次通过这几本书的学习算是对Python有了个较为系统的了解了。

言归正传，今天要探讨的是一个有关Python Package下的Module import的问题，这是我在进行一个Python工程源码组织设计时遇到的。一般来说，我们的工程代码组织形式如下：

py-proj/

main.py

pkg1/

__init__.py

mod1.py

pkg2/

__init__.py

mod2.py

test/

__init__.py

testmod1.py

testmod2.py

工程的dev需求如下：

* 执行main.py(其中import了各个pkg的module)

* 能够单独执行pkg下的某个module

* 兄弟pkg间可以相互import module

* 能够单独执行test下的某个module的test用例

* 能够一次执行test下的所有module的test用例

基于工程的这些dev需求，我们来看一下module import方式的选择。

Python自2.5版本之后支持两种package import方式：absolute import和relative import。不过[Guido van Rossum](http://en.wikipedia.org/wiki/Guido_van_Rossum)在[PEP 8](http://www.python.org/dev/peps/pep-0008/)中明确建议采用absolute import，理由是：more portable和more readable。经过试验，我个人觉得Guido van Rossum的建议是十分中肯的。relative import在不同版本间的支持语义有差别，且在理解方面显得有些复杂。《Learning Python 4th Edition》中花了将近一个小节来讲Package relative import，感觉复杂难懂。虽然relative import能解决一些问题，但感觉投入产出比不高。我们来看看package absolute import能否满足我们的所有工程dev需求。

* 执行main.py

无论当前工作目录（current working directory)是哪个目录，一旦执行main.py，Python就会自动将main.py所在的目录添加到sys.path中去，作为一个 module search path的entry。这样只要工程下的文件都采用了absolute import，Python就可以正确找到并import正确的module。

* 单独执行某pkg下的某个module

我们在dev时有这样的需求：单独执行某个正在编写的module的代码以获得一些执行结果的反馈。不过，以上面例子中的代码结构为例，如果我们进入到 pkg1目录下执行python mod1.py，一旦mod1.py引用了pkg2.mod2，你就会收到如下错误（前提是你使用了absolute import）：

$ python mod1.py

Traceback (most recent call last):

File "mod1.py", line 2, in <module>

import pkg2.mod2

ImportError: No module named pkg2.mod2

因为Python只是将pkg1这个路径加入到module search path中了，这个路径下显然没有pkg2/mod2.py。不过我们可以通过在工程top-level路径下执行"python -m pkg1.mod1"来单独执行mod1的代码，这样absolute import依然生效，不会导致import error。

* 兄弟pkg间可以相互import module

这个与上面的执行方法类似，只要在top-level下通过python -m执行，那么无论pkg层次多深，无论有多少兄弟package，Python总是可以找到正确的module并导入。

* 单独执行test下的某个module的test用例

这有些类似于引用兄弟package的情况。我们通过在顶层路径下执行python -m test.testmod1即可达到此目的。

* 一次执行test下的所有module的test用例

较新的Python版本已经可以自动发现测试用例并执行。我们通过在top-level目录执行python -m unittest discover test即可执行test目录下所有符合unittest包约定要求的单元测试用例文件。在执行这个命令时，Python会将top-level路径以及 test路径都加入到module search path中。

终上，Absolute import可以满足所有需求。虽然有时候absolute import从代码上会看起来有些冗长(通过from … import …能有所缓解)，但在语义理解的简单性和可读性上的优势让我更加倾向于这种方式。另外通常情况下我们是无需重新设置PYTHONPATH，也用不 到.pth文件，更不需在代码里修改sys.path来改变Python的module search path的。

注：以上测试均在[Ubuntu 12.04](http://tonybai.com/2012/12/04/upgrade-ubuntu-to-1204-lts/) LTS Python 2.7.3版本下测试通过。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

最近也打算这么搞了，之前各种改变sys.path实在是太乱了