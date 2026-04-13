---
title: 一个基于XeTeX和xeCJK的TeX模板
url: https://tonybai.com/2010/11/02/a-tex-template-based-on-xetex-and-xecjk/
published: '2010-11-02'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一个基于XeTeX和xeCJK的TeX模板

与"Hello World"作为编程入门时迈出的第一步相似，"[Hello TeX](http://tonybai.com/2010/10/18/hello-tex/)"也只是学习博大精深的[TeX](http://en.wikipedia.org/wiki/TeX)的一块儿敲门砖，离真正的实用还差的远。

两周前[开始体验TeX](http://tonybai.com/2010/10/18/hello-tex/)，直到今天才东拼西凑地倒腾出一个够自己使用的且相对实用的基于XeTeX和xeCJK的[小模板](http://code.google.com/p/bigwhite-code)。这里分享一下，希望能给大家带来一些帮助，同时对自己也算作是一个备忘。关于TeX网上[资料](http://www.ctex.org/documents/packages/)很多，这个模板里的东西也都是参考和融会各种资料并试验后总结而成的。如果你是TeX方面的高手，大可不必理会下面内容^_^。

模板分三个部分：文档声明、序言(Preamble)区和正文(Body)区，下面逐个说：

一、文档声明

\documentclass[a4paper,11pt,titlepage]{book}

每个TeX文档必须包含的一个命令，用来指定该文档的类型，这里类型是Book，属性：A4纸张，五号字，标题后新启一页。

二、序言(Preamble)区

\usepackage{fontspec}

\usepackage{xunicode}

\usepackage{xltxtra}

以上是[XeTeX](http://www.tug.org/xetex/)的三个主要宏包，类似于C语言的stdio.h, stdlib.h和string.h似的，一般只要使用XeTeX，就都要包含。

\XeTeXinputencoding "GBK"

采用[GBK字符编码](http://tonybai.com/2007/11/03/also-talk-about-char-encoding/)集，如果你的.tex文件的编码格式是GBK，那么必须包含这行命令，否则xelatex将无法识别.tex文件中的中文字符。另外值得注意的是如果你采用include或input指令来包含其他章节.tex，那么单独章节的.tex文件中也要包含这个命令，否则也会导致xelatex编译出错。

\XeTeXlinebreaklocale "zh"

\XeTeXlinebreakskip = 0pt plus 1pt minus 0.1pt

上面两个命令主要是为了使xelatex在进行中文断行时处理的更美观些。

\usepackage[colorlinks,

linkcolor=black,

citecolor=black]{hyperref}

控制文本中的超链接内容的格式。

\usepackage[top=1.2in,bottom=1.2in,left=1.2in,right=1in]{geometry}

页边距设置，这里无须多说了。

\title{\XeTeX\ 日常使用模板\\（基于GBK编码）}

\author{著：Tony Bai\\

译：Tony Bai\footnote{\url{http://bigwhite.blogbus.com}}}

\date{October, 2010}

以上是封面内容，其中\XeTeX命令定义在xlxtra包中，如果不包含xlxtra，那么xelatex将编译失败。

\usepackage{fancyhdr}

\pagestyle{fancy}

\fancyhf{}

\fancyhead[LE,RO]{\thepage}

\fancyhead[RE]{\leftmark}

\fancyhead[LO]{\rightmark}

\fancypagestyle{plain}{

\fancyhf{}

\renewcommand{\headrulewidth}{0pt}

}

\renewcommand\chaptermark[1]{\markboth{\chaptername~ #1}{}}

\renewcommand\sectionmark[1]{\markright{\thesection~ #1}}

以上是关于页眉页脚设置，基本上是从[latex notes](http://www.tex.ac.uk/tex-archive/info/latex-notes-zh-cn/)中摘录过来，只是最后两行稍作了修改。

\renewcommand{\baselinestretch}{1.25}

设置正文行距。

\usepackage{titlesec}

\titleformat{\chapter}{\centering\huge}{第\thechapter{}章}{1em}{\textbf}

章节格式设置。

% xeCJK设置

\usepackage[slantfont, boldfont, CJKaddspaces]{xeCJK}

\setmainfont{Times New Roman}

\setCJKmainfont{SimSun}

\setCJKfamilyfont{song}{SimSun}

\setsansfont{AR PL UKai CN}

目前用到的唯一与xeCJK相关的地方，也没什么可说的。

\renewcommand{\chaptername}{第{\thechapter}章}

\renewcommand{\contentsname}{目~录}

默认情况下，章节的描述是英文的，比如Chapter 1 xx，这里对\chapter作了重定义，将Chapter n改为中文描述”第n章“。

\usepackage[fleqn]{amsmath}

引用数学公式包，默认公式居左。

三、正文(Body)区

考虑到长文档很大，编译一遍消耗时间较长，这里采用\include命令加载其他子模块的tex文件。

\begin{document}

\maketitle % 生成title

\include{preface} % 序言

\tableofcontents % 生成目录

\setcounter{tocdepth}{3} % 设置目录深度

\include{introduction} % 第一章 导 言

\end{document}

被include的preface.tex和introduction.tex的结构都很简单，以introduction.tex为例：

\XeTeXinputencoding "GBK" % 本文件采用GBK编码

\chapter{导~言}

在这一章节中，…

\section{XX}

在xx

\subsection{XX-1}

在xx-1

\subsection{XX-2}

在xx-2

\section{YY}

在yy

\subsection{YY-1}

在yy-1

再强调一下，如果采用GBK作为.tex文件的内码，那么\XeTeXinputencoding "GBK"这句是必须的，当初被这个问题折磨了半个小时才终于through它。

另外说一下在正文编辑时经常用到的命令：

* 强制对齐

\begin{flushleft}

致谢\\

\end{flushleft}

* 原文照搬

\begin{verbatim}

xxx

\end{verbatim}

如果是内容较短，可以用\verb|xx|。

* 列表

\begin{itemize} or \begin{enumerate}

\item xx

\item yy

\end{itemize} or \end{enumerate}

这个模板还很简单，诸如索引和附录等都还未考虑。另外由于对XeTeX/LaTeX了解仍不是很透彻，所以模板中不免还有诸多问题，这里就事先打个预防针吧^_^。

完整的模板源文件放置在我的[Google code svn库](http://code.google.com/p/bigwhite-code/)里，可选择下载使用。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论