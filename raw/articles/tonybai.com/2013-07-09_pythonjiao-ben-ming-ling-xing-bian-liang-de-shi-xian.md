---
title: Python脚本命令行变量的实现
url: https://tonybai.com/2013/07/09/an-implementation-of-python-commandline-variables/
published: '2013-07-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Python脚本命令行变量的实现

我们知道Make工具是支持[命令行变量](http://tonybai.com/2011/05/19/use-command-line-vars-of-make/)的，这种手段为我们提供了很好的灵活性，我们可以通过敲入不同的命令行参数来决定Makefile脚本的行为。

make [variable1=value1 variable2=value2 ... ... ]。

#

# Makefile

#

CMODE = 64-bit

ifeq ($(CMODE), 64-bit)

CFLAGS += -m64

endif


all:

gcc $(CFLAGS) -o foo foo.c

$> make

gcc -m64 -o foo foo.c

$> make CMODE=32-bit

gcc -o foo foo.c

近期我们的一个Python脚本工具也有类似的需求了，但Python脚本原生并不支持这种命令行变量，我们来看看是否可以利用Python提供的机制实现一种可以满足我们需求的命令行变量。

我们的期望结果如下：

$> foo.py fruit=apple

# foo.py

flag = '' #这个定义可以有，也可以没有，如果有，可以理解为默认值

….

if flag == 'apple':

….

elif flag == 'orange':

….

elif flag == 'banana':

….

else:

….

Python是动态语言，提供了注入eval、exec等在运行时执行代码的能力。我们要实现命令行变量的机制，离不开这些能力的支持。eval用于求值表达式，而x=y是语句，我们只能用exec。

【#1】

import sys

if __name__ == '__main__':

c = len(sys.argv)

if c <= 1:

print "found zero command variable"

exit(0)

exec(sys.argv[1])

if fruit == 'apple':

print 'this is apple'

elif fruit == 'oracle':

print 'this is orange'

elif fruit == 'banana':

print 'this is banana'

else:

print 'other fruit'

$> foo.py fruit=apple

Traceback (most recent call last):

File "./foo.py", line 18, in <module>

exec(sys.argv[1])

File "<string>", line 1, in <module>

NameError: name 'apple' is not defined

上面的例子执行后，提示'apple'没有定义。执行foo.py fruit="apple"得到的也是同样的错误。从内部输出来看，无论是fruit=apple还是fruit="apple"，exec的参数始终都 是fruit=apple，导致exec抱怨apple这个符号没有定义。

我们打开一个Python命令行交互窗口，做如下测试：

$> python

Python 2.7.3 (default, Aug 1 2012, 05:14:39)

[GCC 4.6.3] on linux2

Type "help", "copyright", "credits" or "license" for more information.

>>> exec("fruit=apple")

Traceback (most recent call last):

File "<stdin>", line 1, in <module>

File "<string>", line 1, in <module>

NameError: name 'apple' is not defined

>>> exec("fruit='apple'")

>>> fruit

'apple'

>>> exec("num=1")

>>> num

1

通过这个小实验可以看出，我们不能将命令行参数直接原封不动的传给exec，我们要对其进行一下加工，加工的效果如下：

fruit=apple => fruit='apple'

num=1 => num=1

【2】

import sys

def __convert(source):

(var, sep, val) = source.partition("=")

if val.isdigit():

return source

return var + "=" + "\'" + val + "\'"

if __name__ == '__main__':

c = len(sys.argv)

if c <= 1:

print "found zero command variable"

exit(0)

exec( __convert(sys.argv[1]))

if fruit == 'apple':

print 'this is apple'

elif fruit == 'orange':

print 'this is orange'

elif fruit == 'banana':

print 'this is banana'

else:

print 'other fruit'

__convert函数对命令行的参数做了转换，对于数值类的var直接原封不动的返回，否则对于值为字符串的var，将其val用''包裹起来后返回。我们来测试一下新程序：

$> foo.py fruit=apple

this is apple

$> foo.py fruit=orange

this is orange

$> foo.py fruit=watermelon

other fruit

从输出结果来看，我们的预期是达到了^_^。上面的程序只是示例性质的，Python的exec具有运行时执行动态代码的能力，我们在获得这种强大能力的 同时，也面临着巨大的风险。一旦恶意代码从外部传入被exec执行，将带来严重的后果。因此对于exec要执行的代码务必要预先进行必要的形式校验。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

像gunicorn加载配置python格式的配置文件用的就是exec