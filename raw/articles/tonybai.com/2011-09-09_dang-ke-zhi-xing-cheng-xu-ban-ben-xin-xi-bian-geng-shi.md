---
title: 当可执行程序版本信息变更时
url: https://tonybai.com/2011/09/09/when-program-version-changed/
published: '2011-09-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 当可执行程序版本信息变更时

在Unix/Linux上，我们一般可以通过两种方法查看到一个可执行程序的版本信息，以下以[Ubuntu](http://tonybai.com/2011/04/29/feel-experience-after-using-ubuntu-for-one-year/)中的[Gcc](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)为例。

第一种方法：我们可以直接通过程序名字得到版本信息，例如:

$ which gcc

/usr/bin/gcc

$ ls -l /usr/bin/gcc

lrwxrwxrwx 1 root root 7 2010-08-21 00:18 /usr/bin/gcc -> gcc-4.4*

可以看到我用的Gcc的版本号为4.4，但似乎这个版本信息还不够全，只包含了major和minor版本号，还不包括bugfix修订号。

第二种方法，也是最常见的，获得版本信息最为详细的方法，它就是通过-v或–version命令行选项来查看可执行程序的版本号，绝大多数Unix/Linux下的程序都是支持这种方法的。比如：

$ gcc –version

gcc (Ubuntu 4.4.3-4ubuntu5) 4.4.3

可能有人会认为无论是将版本信息放入程序名字中还是在程序内部加上版本信息，都不是神马难事儿，没有必要单写一篇文章来说明。没错，这些的确不是什么困难的事。

在程序名字中放入版本号，通过Gcc命令即可完成：

$ gcc -o foo-1.3.1 foo.c

如果你使用[Makefile](http://tonybai.com/2011/05/19/use-command-line-vars-of-make/)来构建你的程序，你可以这样做：

/* Makefile */

TARGET = foo-1.3.1

all: $(TARGET)

gcc -o $(TARGET) foo.c

而在程序内部加上版本信息的最简单方法莫过于在头文件中定义一个宏，然后在version函数中输出这个宏的内容：

/* version.h */

#define VERSION "1.3.1"

/* version.c */

void version() {

printf("%s\n", VERSION);

}

我相信很多朋友都是如是做的。

如果大家真的都是这样做的，那么问题就出现了："当可执行程序的版本信息发生变更时，我们需要修改两个地方"。又有人会说："修改两个地方也不是很麻烦啊"。没错，但这绝不是吹毛求疵，而是实实在在发生的问题。实际开发中很多开发人员总是只记得修改一处，而忘记了另外一处，这样就导致了两处版本信息的不一致。

我们不能完全依靠开发人员的细心和责任心来消除这一问题，我这里提供一种方法供大家参考：

我们在Makefile中像这样定义一组版本信息相关的变量，最重要的是通过一个外部宏定义FOO_VERSION_INFO将版本内容传递到程序内部：

# Makefile

MAJOR := 1

MINOR := 3

BUGFIX := 1

TARGET := foo-$(MAJOR).$(MINOR)

CFLAGS = -DFOO_VERSION_INFO=\"${MAJOR}.${MINOR}.${BUGFIX}\"

all:

gcc -o $(TARGET) $(CFLAGS) foo.c

/* foo.c */

void version() {

/* 这里直接使用Makefile中定义的FOO_VERSION_INFO宏 */

printf("%s\n", FOO_VERSION_INFO);

}

int main() {

version();

return 0;

}

$ foo-1.3

$ 1.3.1

这样一来，即使版本号发生变更了，我们也只需修改Makefile这一处包含版本信息的文件即可。

很多可执行程序的文件名中并不包含版本信息，像ls。如果是这样的话，一切就变得简单了。但是若像Gcc那样，在程序名以及程序内部都包含有版本信息的，我相信使用这个方法/技巧还是大有裨益的。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论