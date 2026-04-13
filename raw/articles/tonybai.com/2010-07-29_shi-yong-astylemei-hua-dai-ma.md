---
title: 使用astyle美化代码
url: https://tonybai.com/2010/07/29/use-astyle-to-beautify-your-code/
published: '2010-07-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用astyle美化代码

昨天一位同事发了一篇小文档，文档中介绍了一种开源格式化代码的工具，名为[Artistic Style](http://astyle.sourceforge.net)(astyle)，功能看起来还是很不错的。之前我写代码时比较注意代码的风格，一直按照自己的思路来美化自己的代码，用的最多的辅助工具就是[Vim](http://tonybai.com/2008/12/30/in-depth-study-vim/)自带的indent功能，对这之外的格式化工具少有涉猎。记得几年前部门曾推广一款名为[checkstyle](http://checkstyle.sourceforge.net/)的Java代码格式规范检查工具，由于当时基本不接触Java，也没有用过。

今天被问及该工具是否可以在组内推广，遂又花心思想了一下。看了同事的介绍文档，感觉astyle还是很实用的，特别是对现存遗留的格式不规范的代码文件，可批量做转换(之前我都是修改哪个源文件时顺便对格式进行美化，浪费了我不少精力) 但是如何能被大家接受和使用起来，这还是一个问题。最开始想到的是让astyle与[svn](http://subversion.tigris.org/)结合在一起，对开发人员保持透明。通过svn hooks来自动完成对代码的格式化。不过细致研究后发现，这样是有问题的。如果在svn server端增加svn pre-commit hook来调用astyle对提交的代码进行格式化，那么这势必可能导致开发人员提交后的server端代码与其Local copy不一致；如果开发人员不知情，后续就会导致进一步的代码不一致问题。另外在svn官方manual中似乎也不推荐在svn pre-commit hook中修改提交的文件内容，好像是会破坏svn commit事务（导致本地和服务器端的一些对文件的统计不一致）。又考虑在客户端svn hook，可查来查去才发现目前只有TortoiseSVN的实现支持客户端hook，遂放弃。

让大家直接执行astyle，显然是高估了大家的执行力了。遂想到还是将astyle与Vim集成在一起吧。

步骤如下：

1、编译artistic style源码，将astyle的可执行程序放到某个目录X下，并将目录X放到path中（ubuntu上可用sudo apt-get install astyle安装）

2、编辑.vimrc，添加一行map ~~ :%! astyle （Shift+F 注：在当前缓冲区用astyle美化缓冲区中的内容，并输出结果到当前缓冲区中）~~

3、定义模板option文件，位置:$HOME/.astylerc

以下是一个.astylerc的例子：

# my astyle options file

–indent=spaces=8

–brackets=attach

–indent-switches

–indent-cases

–indent-labels

–indent-preprocessor

–indent-col1-comments

–pad-oper

–pad-header

–unpad-paren

–add-brackets

–keep-one-line-statements

–align-pointer=name

–mode=c

–min-conditional-indent=0

按照以上方式集成astyle到vim中有一个缺点：就是每次美化都是针对当前缓冲区（一般就是一个文件）。无法做到对某几行或一块区域进行代码美化。

后在stackoverflow上发现有一人提出这样的方案：在.vimrc中增加一行：autocmd BufNewFile,BufRead *.c set formatprg=astyle\ -T4pb。最初以为这样设置是使用astyle替换vim内置的c indent格式化工具，遂照猫画虎配置后用"="命令进行测试，发现无法格式化；遂花时间研读Vim手册，终于发现是我的理解错了。formatprg这个option是与gq命令联系在一起的，而非关联"="命令。以前的确不怎么使用gq命令，而是一直用c indent("=")来做所谓的格式化操作。利用对formatprg这个option的设置可以做到利用外部工具对vim当前文本buffer做格式化的目的。因为之前已经配置了$HOME/.astylerc，所以在.vimrc中增加一行：autocmd BufNewFile,BufRead *.c set formatprg=astyle，去掉了-T4pb这几个参数。

生效.vimrc后使用gq命令对.c文件进行测试，果然有效。gq命令不仅支持对Whole Buffer进行filter，而且可以对单行、多行以及对块文本进行格式化过滤，比如：

NORMAL模式下: gggqG 即对Whole Buffer进行格式化过滤；

gqG 对从当前行到末尾行之间的文本进行格式化过滤；

gq+1 对下一行文本进行格式化过滤；

gqj 对当前行和下一行文本进行格式化过滤；

与Vim结合在一起最大的好处是：astyle被透明的引入到我们日常开发过程中了，你的工作量并未因astyle的引入而增加，反而astyle却提升了你的工作效率，不是吗？

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

一直都是手动调用astyle, 原来可以和vim结合起来, 呵呵

明天要试试~

加载svn client hook里是一个好主意！原先怎么没想到呢。