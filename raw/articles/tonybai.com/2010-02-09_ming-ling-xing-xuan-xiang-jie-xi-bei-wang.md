---
title: 命令行选项解析-备忘
url: https://tonybai.com/2010/02/09/parse-command-line-options/
published: '2010-02-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 命令行选项解析-备忘

翻看一本关于[Shell方面的书](http://www.douban.com/subject/3519360/)，有一章节对命令行选项的讲解比较详细，这里总结了一下：

命令行选项分类：

1、无命令行选项(option)

如：mv file1 file2；

在命令后名显示增加一个'-'，也是一种显式无option的表达。比如：mv – file1 file2

2、有命令行选项，但无Option参数

如：rm -f file1

rm -f -r dir1

无参数的option可组合在一起表达，如：rm -fr dir1

3、有命令行选项，且带命令行参数

如：gcc -o test test.c

4、长命令行选项(long options)

如：gcc –help

因为很少自己处理main()，所以似乎还从未写过解析复杂命令行选项的代码。复杂的命令行选项的解析还是蛮复杂的，但是不要自己发明轮子。GNU的标准库给我们提供了两个良好的接口getopt和getopt_long，而且在[GNU C Manual](http://www.gnu.org/s/libc/manual/)中有很好的例子供参考。但getopt的[那个例子](http://www.gnu.org/s/libc/manual/html_node/Example-of-Getopt.html#Example-of-Getopt)是有bug的，某些情况cvalue值始终为NULL，会[dump core](http://tonybai.com/2006/09/06/be-careful-of-the-trap-of-overflow/)(在Solaris下)。

初级文章，记之以备忘。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论