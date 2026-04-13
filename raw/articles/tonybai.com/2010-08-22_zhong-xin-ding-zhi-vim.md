---
title: 重新定制VIM
url: https://tonybai.com/2010/08/22/reconfigure-vim/
published: '2010-08-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 重新定制VIM

这周五工作状态实在不好，也许是工作得有些疲劳的缘故。没有了心思工作，那莫不如利用这些时间读读书。在存储电子书的目录中左翻翻右看看，发现了那本久违了的[中文版VIM手册](http://vimdoc.sourceforge.net)，我决定索性打开温习一下，拣一拣那些已经生疏了的但却极其实用的命令。

下班前400多页的手册居然被我走马观花的浏览完了，其间将遇到的觉得实用的且以前不知道的或不常用的命令记录了下来，一共有50多项，其中不乏令我大呼过瘾的能显著提升工作效率的命令^_^。

VIM自从使用以来一直也未曾系统的挖掘过，之前在plugin上下过一些工夫，比如[taglist,cscope](http://tonybai.com/2008/12/30/in-depth-study-vim/)等。特别是VIM的定制文件vimrc没有系统的整理过，这次重温VIM手册，让我有了重新定制VIM的想法。

定制VIM，即编制适合你自己的.vimrc文件，这个文件不需要你一切都从头开始，网上流传着很多极具参考价值的资料，比如说比较出名的被网友戏称为"史上最强vim配置文件"的[amix vimrc](http://amix.dk/vim/vimrc.html)，你完全可以照猫画虎的全部搬过来直接使用，但最好是认真读一读其中的内容，了解每一项配置背后的原理，不懂的就对比一下manual，这样印象也深刻些。

我重新定制的vimrc基本上就是对amix vimrc的裁剪，所以这里也没什么值得列出来的内容。不过对其中的一些配置我倒想在这里说道说道：

1、的使用

在定义映射时，可使用标识,这类似一个trick，在映射转换时被变量mapleader的值替换掉。mapleader是一个特殊变量，如果mapleader没有被显示赋值，其值默认为'\'；

如: nmap w :w!这个键映射，如果之前没有显式给mapleader变量赋值，那么在normal模式下，敲入'\w'即是执行将当前更新写入文件。如果之前设定let mapleader = ","，那保存文件的命令就变成了',w'。

2、vimrc更新自动生效

autocmd bufwritepost *vimrc* source ~/.vimrc

这是一个比较实用的配置，可让你即时看到修改配置后的效果，比如修改colorscheme。

3、编码选项的设定

公司的服务器环境设定的内码都是GBK，这样我们的代码源文件的内码也就都是GBK；但是Ubuntu默认内码是UTF-8，如果不做任何设置用VIM打开这些文件，势必会导致文件中的中文字符显示为乱码。关于[VIM字符编码](http://bigwhite.blogbus.com/logs/47259473.html)的问题曾经在一篇文章中分析过,这里不再细说。用下面的设置可以解决上面提到的问题：

" 自动识别文件的编码格式, 打开已有文件时起作用

set fileencodings=GBK,UTF-8,gb18030,ucs-bom,cp936

" 标识源文件中的数据的内码格式

set fileencoding=GBK

" 标识vim buffer中的数据编码格式

set encoding=UTF-8

这样配置有一个小问题就是对于新建的文件强制设定了采用GBK的内码。

4、比较实用的设置

map / "NORMAL模式下这个命令用起来很舒服

以下是在visual模式下自动对块文字区域加（），{}，[]等的命令

vnoremap $1 `>a)`<i(

vnoremap $2 `>a]`<i[

vnoremap $3 `>a}`<i{

vnoremap $$ `>a"`<i"

vnoremap $q `>a'`<i'

vnoremap $e `>a"`<i"

source $VIMRUNTIME/ftplugin/man.vim "将光标停留在你想查Manual的Word上，normal模式下敲入'\K'即可自动查找这个word的Manual。

VIM太强大，里面存在太多的技巧和奇妙的命令，VIM manual也是常看常新，Ubuntu里的其他编辑器已经都让我卸载了，以让自己更加专注于VIM^_^。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论