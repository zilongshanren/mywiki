---
title: 基于svn diff结果的有效代码量统计
url: https://tonybai.com/2010/12/24/an-effectual-method-based-on-svn-diff-for-code-quantity-statistics/
published: '2010-12-24'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 基于svn diff结果的有效代码量统计

很多公司的过程中都有阶段性统计新增或修改的有效代码行数这一环节，这里先不论统计出的结果用于做什么，就统计本身而言，常常存在诸多问题，比如统计过程耗时且繁琐、统计结果中估算成分较大，不精确等。这些问题以前也一直困扰着我们，并且长时间没有想出很好的解决办法。

今天脑子里突然冒出一个想法：能否根据[svn](http://tonybai.com/2010/08/07/use-svn-pre-commit-hook/) diff得到的结果分析出来有效代码量呢？ svn diff的结果一般是这样的，分为几类：

纯新增代码，如：

+void foo() {

+ … …

+}

纯删除代码，如：

-void foo() {

- … …

-}

修改的代码，如：

-void foo(void);

+void foo(int);

我们所要统计的所谓有效代码更多是指纯新增的代码和修改的代码，纯删除的代码可忽略不计。这样一来实际有效代码行数 = 纯新增代码行数 + 修改代码行数；而修改的代码在svn diff结果中体现为一减一加，实际修改行数是等于其+的行数的。也就是说有效代码行数就是svn diff结果中所有前缀为+的行的行数。svn diff输出格式相对规整，通过解析得到这个行数并非难事。最简单的方法就是使用[Shell脚本](http://tonybai.com/2006/05/02/an-introduction-on-unix-shell-scripting/)了。

脚本全部内容这里就不列出来了，[这里](http://code.google.com/p/bigwhite-code/source/browse/trunk/shell_scripts/source-counter?r=24)可以下载。其核心代码只有以下两行：

svn diff -r$start_revision:$end_revision $target $USERNAME $PASSWD > $TEMPFILE

add_lines_count=`grep "^+" $TEMPFILE|grep -v "^+++"|sed 's/^.//'|sed '/^$/d'|wc -l`

首先我们使用svn diff命令将两个修订号之间的差异重定向到一个临时文件中，然后使用grep、sed和wc的组合完成行数的计算：其中首先过滤出以+开头的行，但去除其中+++开头的行，得到的是所有只以一个+开头的行。再利用set 's/^.//'删除每行行首的那个+，用set '/^$/d'删除所有空行，最后利用wc -l计算总行数。

也就是说通过上面脚本运行后得到的有效代码行数是不包括空行的，但是包含注释代码。

有了这个脚本，以后的版本有效代码量统计就相当精确了，而且也无需每个人都参与统计，大大减少了工作量，甚至可以将这个工作做成自动化完成。

现在的我痛恨一切效率低下的个人行为和过程活动！遇到问题坚决改善，绝不姑息^_^。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

也许 svnstat 可以做得更好

我没用过，早已转移到 git 了

按照这种方法 如果提交一个swf文件 就会有问题了

如果提交至版本库中时有这种2进制文件 如何处理呢， 望指教

可能是因为我是把diff的结果用字符串的方式在处理，我用的ruby on rails 不知道怎么调用您写的shell程序呢， 我这样

IO.popen("grep "^+" #{diff}|grep -v "^+++"|sed ‘s/^.//’|sed ‘/^$/d’|wc -l"){ |f| lines= f.gets} diff是diff命令的结果 但是一直有错误 新手望指教

目前我用字符串的方式，不过也是基于diff命令来计算项目成员的代码量 我是在每连续的两个revision都diff一下，然后根据该revision的committer累加到该成员上， 结果可以计算出来，但是计算过程繁琐且慢 不知有没有更好的方法

还想请教一下，项目第一次提交 就是版本1的代码行数怎么计算呢

先取得文件列表，然后用blame命令会不会好点

现在我们遇到一个性能问题，有一次提交，import了很多文件，因为我们是做一个开源项目的二次开发，所以这次提交代码行数有38W行， 用diff统计，刷新一次页面要五分钟，不知道有何优化方法

现在遇到一个问题 当源代码所在的svn url中的文档文件比如doc、ppt、xls这些文件时，在计算代码行数时如果用diff的话，文档里的内容也计算进去了，如何避免呢