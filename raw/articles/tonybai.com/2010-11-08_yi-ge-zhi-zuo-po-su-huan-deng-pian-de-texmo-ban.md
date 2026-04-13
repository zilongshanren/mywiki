---
title: 一个制作朴素幻灯片的TeX模板
url: https://tonybai.com/2010/11/08/a-tex-template-for-making-plain-ppt/
published: '2010-11-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 一个制作朴素幻灯片的TeX模板

自从有了For book的[中文TeX模板](http://tonybai.com/2010/11/02/a-tex-template-based-on-xetex-and-xecjk/)后，我对[TeX](http://tonybai.com/2010/10/18/hello-tex/)的热情便"继续"一发而不可收拾^_^。上周原本计划为内部的一个交流准备一个PPT，但在开始构思之前却突然想到：是否可以使用TeX完成幻灯片制作呢？Google了一下，果然有成熟解决方案-使用[BEAMER](http://bitbucket.org/rivanvx/beamer/wiki/Home)。

有了[TeX基础](http://tonybai.com/2010/10/18/hello-tex/)后，学习使用Beamer构建幻灯片就显得容易了许多，用TeX创建幻灯片文档与编写普通文档差别并不大。TeX制作的幻灯片文档也是由三个部分组成：文档类声明、Preamble区和正文区。

文档类声明中的选项为beamer，表示我们要创建幻灯片文档。

\documentclass{beamer} % 文档类声明

Preamble区甚至可以复用普通TeX文档中的那些设置，这里不再赘述^_^。

正文区的内容大多与普通TeX文档也类似，只是幻灯片使用frame来组织。每个幻灯片由一组frame构成，而每个frame又包含多个slide。\section和\subsection依然可以在幻灯片中使用，不过我还似乎没有发现他们的实际价值在哪里，所以我在模板中也没有使用它们。但itemize、enumerate以及block在幻灯片制作中的作用却甚是重要。以下是模板正文区内容：

\begin{document}

\begin{frame}

\titlepage

\end{frame}

\begin{frame}

\frametitle{Outline}

\tableofcontents

\end{frame}

\begin{frame}

\frametitle{first frame}

\framesubtitle{usage of itemize}

This is the first frame using \XeTeX~and beamer.

\begin{itemize}

\item xx % first slide of this frame

\item yy % second slide of this frame

\item zz % third slide of this frame

\end{itemize}

\end{frame}

\begin{frame}

\frametitle{second frame}

\framesubtitle{usage of enumerate}

This is the second frame.

\begin{enumerate}

\item xx

\item yy

\item zz

\end{enumerate}

\end{frame}

\begin{frame}

\frametitle{third frame}

\framesubtitle{usage of block}

This is the third frame.

\begin{block}{Advantage}

The obvious disadvantage of this approach is that you have to know LaTeX in order to use Beamer.

\end{block}

\begin{block}{disadvantage}

The advantage is that if you know LaTeX, you can use your knowledge of LaTeX also when creating a presentation, not only when writing papers.

\end{block}

\end{frame}

\end{document}

之所以称之为朴素幻灯片模板，是因为这里并不包含一些很炫的特效。Beamer手册(texdoc beamer)有240多页，相信其中可能会包含如何制作一些特效的内容。

完整的幻灯片模板可从[这里](http://code.google.com/p/bigwhite-code/source/checkout)下载。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论