---
title: 在TeX文档中插入源代码
url: https://tonybai.com/2010/12/01/insert-source-code-into-tex-document/
published: '2010-12-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 在TeX文档中插入源代码

近期有了在[TeX](http://tonybai.com/2010/10/18/hello-tex/)文档中插入源代码的需要。TeX的\verbatim可以帮助你保留输入text的原始格式，但用于输入源代码还是显得不够专业。Google了一下发现TeX中支持插入源代码的包也有不少，如[LGrind](http://www.ctan.org/tex-archive/help/Catalogue/entries/lgrind.html)、Listings等。LGrind似乎没有包含在[TeX Live](http://www.tug.org/texlive)的默认安装包中，用apt-get尝试安装LGrind，发现居然要占用近200M的空间，遂放弃之，最后我选择了[Listings](http://www.ctan.org/tex-archive/help/Catalogue/entries/listings.html)宏包。

Listings宏包短小而强大，其典型应用方式如下：

\usepackage{listings}

\lstset{…}

\begin{lstlisting}

#include

int main(int argc, const char *argv[]) {

printf("Hello World!\n");

return 0;

}

\end{lstlisting}

\lstinputlisting{HelloWorld.c}

其中\lstset用于全局设置插入源代码的类型、各种语法元素的样式、边框和行号设置。你的源码只需包裹在\begin{lstlisting}和\end{lstlisting}之间，源码就能按照之前设置的格式显示。\lstinputlisting支持将一个独立的源代码文件load进来，并按\lstset的格式显示。下面是一个插入C语言源码的例子：

\lstset{ language={[ANSI]C},

showspaces=false,

showtabs=false,

tabsize=4,

frame=single,

framerule=1pt,

framexleftmargin=5mm,

framexrightmargin=5mm,

framextopmargin=5mm,

framexbottommargin=5mm,

%numbers=left,

%numberstyle=\small,

basicstyle=\tt,

directivestyle=\tt,

identifierstyle=\tt,

commentstyle=\tt,

stringstyle=\tt,

keywordstyle=\color{blue}\tt }

\begin{lstlisting}

#include

int main(int argc, const char *argv[]) {

printf("Hello World!\n");

return 0;

}

\end{lstlisting}

上面lstset中每种语法元素的style都设置为\tt。说到\tt，就不能不提到西方字母字族的种类，分为serif、sans serif和monospace三类。其中serif来源于荷兰语, "衬线"的意思，又称为Roman，一般用于正文的主字体，感觉很正式，我们常用的"Times New Roman"字体就归于此族; sans serif中的sans来源自法文，意为“非”，这类字体比较平滑，字体较大，适于在标题中使用，如"Arial"字体。monospace是等宽字族，也称为typewriter，程序源代码用此族字体表示更为美观，常见的字体包括Courier New、Lucida Console等。其中\tt指的就是使用monospace字族; \rm表示使用serif字族，\sf则是使用sans serif字族的意思。

确定了字族后，我们可以通过TeX preamble区的字体设置得知具体的字体，如在上面例子中，我们是这么设置字体的：

\setCJKmainfont{WenQuanYi Micro Hei}

\setCJKsansfont{WenQuanYi Micro Hei}

\setCJKmonofont{WenQuanYi Micro Hei}

\setmainfont{Times New Roman}

\setsansfont{Arial}

\setmonofont{Courier New}

CJK相关的字体设置影响的是中文字体，而真正对代码起作用的是后面的英文字体设置。这里我们的mono字体设置为了"Courier New"，这样我们的源码就会以Courier New的形式展现出来。

我更新了之前制作的book和ppt的TeX模板，以支持插入源代码，有意者可[在此下载](http://code.google.com/p/bigwhite-code/)。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

有木有截图啊？