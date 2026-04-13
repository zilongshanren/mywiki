---
title: 一个关于Vim扩展TAB键的问题
url: https://tonybai.com/2010/09/07/a-problem-about-vim-expand-tab/
published: '2010-09-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一个关于Vim扩展TAB键的问题

今天遇到一个奇怪的问题：明明我在[.vimrc](http://tonybai.com/2010/08/22/reconfigure-vim/)中开启了expandtab选项，但是当我编辑Makefile文件时，敲入的TAB就是无法被[VIM](http://tonybai.com/2010/08/22/reconfigure-vim/)自动转换为四个空格(已经设置tabstop=4，shiftwidth=4)，通过":set expandtab?"查看该选项值也居然是"noexpandtab";编辑其他文件（如.c、.h文件甚至是无扩展名的文件)时expandtab却都是开启的，TAB也可被自动转换，百思不得其解!

最初怀疑是compatible的设置对expandtab产生了影响。打开我的.vimrc，发现我设置的是“set nocompatible”，“compatible”已经被关掉，不会对expandtab产生影响。又想了想，假设受影响，那么所有文件都应该受到影响才对，不应该只有Makefile这类文件受影响。

想到这里，突然开了窍！是不是我开启的文件类型检测导致的呢？我在.vimrc设置了"filetype plugin on"。又看了一下这个设置的相关Manual，虽然没有直接给出答案，但是顺藤摸瓜，我也找到了原因。

因为开启了文件类型检测，Vim在打开或新建一个文件时会自动判断文件的扩展名以确定文件类型，在$VIMRUNTIME/filetype.vim中搜索"Makefile"，可看到如下脚本语句：

" Makefile

au BufNewFile,BufRead *[mM]akefile,*.mk,*.mak,*.dsp setf make

Vim将Makefile划归为"make"类型(setf make)。在$VIMRUNTIME/ftplugin下有一堆xxx.vim文件，我们从中可以找到make.vim，这个文件就是VIM针对make类型文件的设置，在打开或新建make类型文件时被VIM自动加载。

这个make.vim文件中有一行设置如下：

" Make sure a hard TAB is used, required for most make programs

setlocal noexpandtab softtabstop=0

见文知义！果不其然，就是这个问题。又试验了一下，将.vimrc中的“filetype plugin on”注释掉，再打开Makefile文件，TAB就可以被自动转换为四个空格了。

回头一想，VIM针对make类型文件设置了noexpandtab也不无道理，编写过Makefile的朋友都知道，Makefile的基本组成结构就是：

target … : prerequisites …

command

…

…

其中Makefile语法要求command前面必须放置一个TAB！否则解析失败！

这回真相大白了^_^

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

谢谢楼主的文章，学到不少东西。

我用vim写makefile时遇到一个问题，vim仍将tab转成空格。

我试着加上

filetype on

但仍起不了作用。

请问怎么避免vim将tab转换为空格呢？