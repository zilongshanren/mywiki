---
title: 也谈C语言编译器的标准编译阶段
url: https://tonybai.com/2011/07/04/also-talk-about-standard-compile-stage-of-c-compiler/
published: '2011-07-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈C语言编译器的标准编译阶段

了解C编译器的工作流程有助于C程序员解决编译代码过程中出现的问题。市面上凡是讲解得还算全面的[C语言书籍](http://book.douban.com/doulist/549603/)中都或多或少对此有所提及。

让我们在这里来回顾一下C编译器的工作流程！一般C编译器的工作流程大致分为：预编译、编译、生成目标代码（汇编）和连接这四个主要步骤。我们用实例具体描述一下这四个步骤，以最著名的GCC编译器结合helloworld.c文件为例:

/* helloworld.c */

int main() {

printf("hello, world\n");

return 0;

}

使用Gcc编译该源文件，我们看到编译器有如下输出（省略了一些内容）：

$ gcc -v -o helloworld helloworld.c

… …

gcc version 4.4.3 (Ubuntu 4.4.3-4ubuntu5)

COLLECT_GCC_OPTIONS='-v' '-o' 'helloworld' '-mtune=generic' '-march=i486'

/usr/lib/gcc/i486-linux-gnu/4.4.3/cc1 -quiet -v helloworld.c -D_FORTIFY_SOURCE=2 -quiet -dumpbase helloworld.c -mtune=generic -march=i486 -auxbase helloworld -version -fstack-protector -o /tmp/ccgoLMLQ.s

… …

COLLECT_GCC_OPTIONS='-v' '-o' 'helloworld' '-mtune=generic' '-march=i486'

as -V -Qy -o /tmp/ccN9HVdH.o /tmp/ccgoLMLQ.s

… …

COLLECT_GCC_OPTIONS='-v' '-o' 'helloworld' '-mtune=generic' '-march=i486'

/usr/lib/gcc/i486-linux-gnu/4.4.3/collect2 –build-id –eh-frame-hdr -m elf_i386 –hash-style=both -dynamic-linker /lib/ld-linux.so.2 -o helloworld -z relro /usr/lib/gcc/i486-linux-gnu/4.4.3/../../../../lib/crt1.o /usr/lib/gcc/i486-linux-gnu/4.4.3/../../../../lib/crti.o /usr/lib/gcc/i486-linux-gnu/4.4.3/crtbegin.o -L/usr/lib/gcc/i486-linux-gnu/4.4.3 -L/usr/lib/gcc/i486-linux-gnu/4.4.3 -L/usr/lib/gcc/i486-linux-gnu/4.4.3/../../../../lib -L/lib/../lib -L/usr/lib/../lib -L/usr/lib/gcc/i486-linux-gnu/4.4.3/../../.. -L/usr/lib/i486-linux-gnu /tmp/ccN9HVdH.o -lgcc –as-needed -lgcc_s –no-as-needed -lc -lgcc –as-needed -lgcc_s –no-as-needed /usr/lib/gcc/i486-linux-gnu/4.4.3/crtend.o /usr/lib/gcc/i486-linux-gnu/4.4.3/../../../../lib/crtn.o

可以明显看出，Gcc的输出大致分为三段：

首先是调用/usr/lib/gcc/i486-linux-gnu/4.4.3/cc1对源文件helloworld.c进行预编译和编译，生成汇编代码文件/tmp/ccgoLMLQ.s；

然后，汇编器as被启动，编译ccgoLMLQ.s，生成目标代码文件/tmp/ccN9HVdH.o；

最后，链接器collect2将目标文件和一些库文件连接在一起，形成可执行程序helloworld。

简单总结一下就是：

- cc1负责预编译源代码helloworld.c，生成helloworld.i(指代预编译后生成的中间文件，很多编译器为了效率并不使用临时文件，而使用管道等方法)，我们可以通过gcc -E helloworld.c > helloworld.i得到helloworld.i这个文件；

- cc1将helloworld.i作为输入，对预编译后的源文件进行编译，生成汇编代码文件helloworld.s（指代编译后的汇编代码文件）。我们可以通过gcc -S helloworld.c得到helloworld.s文件；

- as负责根据helloworld.s生成目标代码文件helloworld.o，我们可以通过gcc -c helloworld.c来获得helloworld.o；

- collect2负责将目标代码与各种库文件连接，形成最终可执行文件helloworld。

其实以上不是这次重点要谈的。粗略了解了以上流程的确有助于解决编译过程中的问题，但是还不能解决全部，你需要了解更多。关于[链接过程](http://tonybai.com/2007/12/08/those-things-about-symbol-linkage/)，我在博客里曾多次谈过，这里就不说了。as执行的汇编过程基本不会出现问题，这里也不谈，我们这次重点要关注的就是C编译器在预编译和编译过程中的一些细节。

[C标准](http://tonybai.com/2005/07/28/introduction-on-c-standard-overview-series/)(C99)在5.1.1.2小节将C编译器工作流程分成了八个标准阶段，我这里也是结合这八个阶段并按照我的理解做进一步的解释的。在开始之前我们要明确下面这八个阶段中的前七个都是针对一个编译单元/翻译单元的，自始至终你都要牢记这一点。

第一阶段：物理源文件中的多字节字符被映射到源字符集（具体以何种字符编码方式映射与编译器的实现相关）。三字符序列(或称为三字符组)被替换为相应的单字符的内部表示。

标准中的语言总是那么绕口。这里主要说的是编译器读取物理源文件的内容，此时编译器并不知道该源文件中的多字节字符采用的是何种字符集编码方式。以GCC为例，GCC默认源码文件多字节字符的编码为utf8，而GCC其作为内部表示的源字符集默认也是utf8，所以默认情况下，这个阶段GCC不会对源文件中的内容做任何转换。

例如我们有一个内码格式为GBK的名为foo.c的文件：

/* foo.c */

int main() {

printf("中国\n");

}

按照GBK码表，其中的字符串常量"中国"的编码为d6 d0 b9 fa。将该文件传到一个locale为utf8的平台上编译，我们发现GCC并未尝试将GBK转换为其内部表示的编码格式utf8：

$ gcc -E foo.c > foo.i

$ od -x foo.i

我们可以看到foo.i中"中国"二个字的编码依旧为d6 d0 b9 fa。

不过我们可以显式告知编译器源码文件的编码格式，如果其所在OS支持从该编码格式到utf8的转换，则GCC会在第一阶段就进行这个转换：

$ gcc -E foo.c > foo.i -finput-charset='gbk'

这次foo.i中的"中国"二字的编码变成了utf编码：e4 b8 ad e5 9b bd

三字符序列(trigraphs)的替换过程也是在第一阶段进行的，也就是发生在词法分析之前以及识别字符常量和字符串常量中的转义字符之前。我们看看这个例子：

/* trigraphs_test.c */

int main(int argc, const char *argv[]) {

printf("hello??/n");

printf("world\n");

return 0;

}

$ gcc -E trigraphs_test.c > trigraphs_test.i -std=c99

可以看到trigraphs_test.i内容为：

int main(int argc, const char *argv[]) {

printf("hello\n");

printf("world\n");

return 0;

}

三字符序列发生在转义之前，所以printf("hello??/n");在字符串转义过程之前就先进行了三字符序列的替换(否则编译器会报错)，替换成了printf("hello\n");后续在字符串常量转义字符时\n才被当作了换行符处理。

第二阶段：这个阶段比较简单，说白了就是去掉续行符，即所有相邻的'\'和'\n'的组合，将物理源代码的行拼接为逻辑源代码行。

第三阶段：源文件被分解为预处理词法元素(tokens)和空白字符序列（包括注释）。源文件不应该以一个部分预处理词法元素或部分注释结束(例如一个注释不能一半在一个文件中，而另一半在接下来的文件中)。每条注释都被替换成一个空格字符。换行符保留。将非空空白字符序列(诸如空格、TAB键等，除了换行符）保留还是替换为一个空格字符则由编译器的实现决定

这个阶段中预处理器开始执行了词法分析，删除不必要字符，转换字符，为后续处理营造一个干净的环境。

第四阶段：预处理指示符被执行，宏调用被扩展，_Pragma一元操作符表达式被执行。对通用字符名(UCN)进行词法元素连接的行为是未定义的。预处理器从阶段1到阶段4递归地处理源文件中#include预处理指示符中的头文件或源文件。最后所有预处理指示符被删除。

这个阶段预处理器是主力，其结果是我们得到了一个包含了诸多头文件内容的预处理后的编译单元文件，用作后续处理的输入。

第五阶段：字符常量、字符串常量中的源字符集字符或转义字符序列都会被转换为相应的执行字符集中的字符；如果执行字符集中没有对应的字符（除了宽字符null），则转换成什么由编译器的实现确定。

注意与第一阶段不同的是：这个是在foo.i的基础上，也就是说在GCC默认foo.i中的字符都是utf8的基础上，将代码中的字符常量以及字符串常量中的源字符集字符（默认utf8）转换为执行字符集(默认也是utf8)，包括通用字符名(UCN)。

注意UCN也可以看成转义字符序列，在这个阶段被转换为执行字符集，如：

char *a = "\u4e2d\u56fd"; /* 两个ucn字符为'中国' */

我们通过gcc -S得到源文件对应的.s汇编文件，从汇编文件内容可以看到a的内部表示为：

.string "\344\270\255\345\233\275"

即utf编码的'中国'。

另外这里说的字符和字符串串常量，也包括宽字符和宽字符串，其转换为内部表示的过程也在这个阶段进行，例如下面代码：

wchar w[] = L"中国";

该代码进行了一次utf8到宽字符内部表示（GCC为unicode32）的转换。

第六阶段：将相邻两个字符串字面元素连接起来

这个阶段用一个例子就能说明问题，很简单：

char *a = "hello"

" world";

经过编译后，我们可以看到.s文件中关于a的定义：

.string "hello world"

这就相当于将"hello"和" world"连接起来，形成"hello world"。

第七阶段：编译器执行词法分析、语法分析以及语义分析，生成该编译单元对应的目标代码(.o文件)。

第八阶段：Resolve所有外部符号(包括变量和函数)，并将诸多编译单元的.o以及外部库连接成可执行程序。

个人感觉编译阶段中的难点就是几个涉及字符集转换的阶段，如第一个阶段和第五个阶段，不过只要弄清楚编译器是如何做的，相信所有编译问题都可以被轻松解决了。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

不错！学习了！