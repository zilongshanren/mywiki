---
title: 也谈C语言对国际化的支持
url: https://tonybai.com/2011/07/01/also-talk-about-the-internationalization-support-in-c/
published: '2011-07-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈C语言对国际化的支持

C语言对国际化的支持由来已久，最初开始于其第一版标准，即C89标准。在C89中我们可以看到用于支持国际化的locale.h、宽字符、宽字符串以及多字节字符(串)。而之后的"C89增补1"标准，即C90标准，以及C95标准又进一步完善了C语言对国际化的支持，增加了wchar.h、 wctype.h以及大量用于操作宽字符(串)和多字节字符(串)的标准库函数。最新一版C语言标准，即[C99](http://tonybai.com/2005/07/28/introduction-on-c-standard-overview-series/)，让C语言对国际化的支持变得更加成熟，对非英语字符集也给予了更好的支持。

C语言支持国际化的核心就是大家所熟知的locale技术。C语言中的locale模型于C90标准中被引入。locale模型使得一些库函数的外部行为依赖于locale设置。这样的好处就是你无需重新编译代码，你发布的应用即可根据locale来满足不同区域人们的文化习惯。locale包含若干个类别，诸如LC_CTYPE、LC_COLLATE等，其中每个类别都会独立影响某些C函数的外部行为。比较常见的诸如日期时间显示方式、货币表示方式等。

例如，LC_TIME影响strftime的外部行为，不同locale情况下strftime输出的结果会有不同，见下面示例：

int main() {

time_t now;

char buf[1024];

setlocale(LC_ALL, ""); /* set locale to current locale, which is "zh_CN.GB18030" */

time(&now);

strftime(buf, sizeof(buf), "%a, %d %b %Y %H:%M:%S GMT", localtime(&now));

printf("%s\n", buf);

setlocale( LC_TIME, "en_US.UTF-8" );

memset(buf, 0, sizeof(buf));

strftime(buf, sizeof(buf), "%a, %d %b %Y %H:%M:%S GMT", localtime(&now));

printf("%s\n", buf);

}

这个程序在我的RedHat上输出的结果如下：

五, 01 7月 2011 10:07:59 GMT

Fri, 01 Jul 2011 10:07:59 GMT

locale另外一个重要的作用就是对[字符集转换](http://tonybai.com/2007/11/03/also-talk-about-char-encoding/)的影响。曾几何时，ASCII字符集曾是计算机上通行的字符集标准，那时的程序员一般根本无需考虑字符集转换。ASCII的好处就是每个字符可以存储在一个字节(8bit)中，其内部表示(Internel Representation)和外部表示(External Representation)是一致的，这样一来，其存储和传输都非常方便。程序内部在内存中对ASCII字符（就是一个字节）的处理（识别字符、计算字符串中字符个数、解析字符串等）也十分简单快捷。不过随着国际化的日益深入，ASCII的缺点便暴露了出来，即其编码集太小了，即便将8个bit都算上，最多也就是256(2的8次方)个字符，这丝毫没有考虑到广大亚洲人民的需要，严重"伤害"了亚洲人民的情感^_^。于是乎亚洲各个国家和地区都纷纷"自己动手，丰衣足食"，制定了适合自己国家民族语言文字的字符集标准（当然了，其他大洲的国家也是这个样子的）。这些新字符集编码在满足本国语言需要的同时，也都兼容ASCII字符集，也就是说都是在ASCII字符集的基础上通过扩展字节个数达到支持更多字符的目的的。由于兼容ASCII，所以这些字符集中字符的表示都是非固定长度的，即在ASCII编码区间内的字符(即ASCII字符)用一个字节表示；超出这个区间，就会用2个或3个或更多的字节表示。这样的字符在C语言中被归类称为"多字节字符(multi-bytes character)"。

多字节字符，有着与ASCII同样的优点，即它们是面向字节的，便于传输和存储。之前用于处理ASCII的字符设备（基于字节的）都可以对多字节字符给予很好的支持。不过多字节字符缺点也同样明显。

首先就是程序内部（在内存中）处理起来十分不便。给定一个存储了某种字符集字符的字节数组，如果你没有对应的解析器，你是无法识别字符边界，无法识别出数组中究竟包含了哪些字符的，更不用说返回字符个数等操作了。针对这一问题，C语言引入宽字符的概念，宽字符集中的字符所占用的字节数是相同的，要么都是2 个字节，要么都是4个字节（3字节不利于计算机内存寻址优化），一般最大就是4个字节了，因为4个字节已经可以涵盖全球已知所有语言的所有字符了。在 GCC中，默认C语言宽字符类型，即wchar_t类型的长度为4。我们在内存中操作宽字符显然要比多字节字符更加容易：每个字符与N字节一一对应，这样对于统计字符个数、解析和识别字符大有裨益。因此在考量了多字节字符和宽字符的特点后，一般我们会使用宽字符作为字符在程序中的内部表示（用在各种内存操作中），而在存储、传输和显示过程中则使用多字节字符。再多罗嗦几句：宽字符为何不适于传输和存储呢？大致有以下三个原因：

- 空间利用率不高，或者说比较浪费空间和带宽

我想这个原因不用过多解释了。如果用4字节的宽字符存储一篇英文文章，那么与多字节字符相比，宽字符要浪费3/4的空间。

- 字节序问题

宽字符一般用2或4个字节表示，这样的字符在存储和传输过程中显然会遇到字节序问题，不同的平台采用不同的字节序，这样对于同一份以宽字符存储的数据来说，可能在不同的平台上得到不同的结果。

- 与已有I/O设备兼容性差

以往的设备都是面向字节设备的，处理ASCII字符以及由ASCII扩展而来的多字节字符问题不大。但对于由两个字节或四个字节组成的宽字符来说，显然有些力不从心了。

其次由于各个国家和地区纷纷独立制定多字节字符标准，导致了不同字符集之间的不兼容。比如：GBK编码中"中"字的编码是D6D0，而BIG5中"中"的编码则是A4A4。这样一来，一些涉及文本处理的程序，比如文本编辑器，就需要花费大量的工作在了不同编码间的相互识别和解析上。这时一些组织站了出来，试图建立可以容纳全球所有语言字符的统一字符集，Unicode/ISO 10646（为方便期间，二者之间的一些差异这里就忽略不计了，以下统称Unicode）因此诞生。Unicode简单来说就是一组标量数字集合，其中每个数字映射地球上的一个唯一字符。以往大家对于Unicode的理解就是用2个字节(Unicode-16，UCS-2)或4个字节(Unicode- 32, UCS-4)进行编码的宽字符。实则不然，这些理解只是其一，因为最初使用2个字节（后来发现2个字节是严重不足的）或4个字节可以一一映射 Unicode字符集合，编码值就是Unicode字符对应的Unicode字符集表中的那个数字。但是用宽字符作为Unicode底层编码的实现方式显然也会遇到上面所说的各种问题；于是乎基于多字节编码的Unicode实现出现了，最著名的莫过于utf8了，当然还有utf16和utf32。没错，utf8字符是一种多字节字符，utf8与unicode表示字符个数的能力上是等同的。Unicode字符可以与utf8字符做一一对应的转换。和其它多字节编码方案一样，utf8也兼容ASCII编码，也是面向字节的，utf8可以完全替代各个国家地区自己制定的那些私有编码方案。事实上，目前 utf8已经是全球字符编码的事实标准（de facto standard）了。

我们现在来实现这样一个程序：它可以在不同locale下输出foo.dat文件中的字符个数和字节个数，其中foo.dat文件中存储的数据的编码方式为locale指定的。我们有两个思路：

1、假设我们拥有所有locale的字符解析库，我们可以将数据从文件中读取出来后，用当前locale对应的字符解析库对数据进行解析，得到字符的个数；

2、利用locale技术，将文件中的数据读取后转换为宽字符，再计算宽字符的个数，即为foo.dat文件中字符的个数。

我们粗略对比以下这两种思路，优劣立见。利用locale技术，你无需了解任何有关目标主机字符编码的细节，也无需自携带规模庞大的字符解析库，另外无需做任何修改即可支持新增的locale配置。下面就是一个利用locale技术进行字节/字符计数的例子（仅仅是个例子哦），这个程序可以在不同locale下输出foo.dat中的字符个数和字节个数：

/* wc.c */

int main(int argc, const char *argv[])

{

int bytes = 0;

int words = 0;

setlocale(LC_ALL, "");

printf("Current locale is %s!\n", setlocale(LC_ALL, NULL));

FILE *fp = NULL;

fp = fopen("foo.dat", "rb");

if (!fp) {

printf("failed to open foo.dat, err: %d\n", errno);

return -1;

}

char mbs_buf[1024];

wchar_t wcs_buf[100];

mbstate_t s;

size_t n;

const char *p;

memset(mbs_buf, 0, sizeof(mbs_buf));

while (NULL != fgets(mbs_buf, 1024, fp)) {

memset(&s, 0, sizeof(s));

memset(wcs_buf, 0, sizeof(wcs_buf));

p = mbs_buf;

n = mbsrtowcs(wcs_buf, &p, sizeof(wcs_buf), &s);

if (n == -1) {

printf("failed to convert multi-bytes character to wide character, err: %d\n", errno);

return -1;

} else {

bytes += strlen(mbs_buf);

words += wcslen(wcs_buf);

}

memset(mbs_buf, 0, sizeof(mbs_buf));

}

printf("bytes = %d\n", bytes);

printf("words = %d\n", words);

fclose(fp);

return 0;

}

分别在具有两个不同locale的账户下制作foo.dat:

cat > foo.dat

中华人民共和国^D (输入Ctrl+D)

在locale为gb18030下的测试结果是:

Current locale is zh_CN.GB18030!

bytes = 14

words = 7

在locale为utf8下的测试结果是:

Current locale is zh_CN.utf8!

bytes = 21

words = 7

在C语言中，除了显式调用库函数在宽字符和多字节字符之间转换外，C语言本身还有一些隐式的转换值得注意。

首先就是宽字符的转换。如果你在源文件中用L"XXX"给一个wchar_t数组赋值，那么Gcc会默认将XXX看成是utf8编码的字符串。如果你的源文件确实是utf8编码的，那么类似wchar_t w[] = L"中国"则相当于编译器做了一次utf8到unicode-32的转换;但是如果你的源码文件不是utf8编码的，比如是gb18030的，那么编译器将提示错误：“converting to execution character set：无效或不完整的多字节字符或宽字符”。这时需要你通过Gcc命令选项显式指定源码字符集类型：-finput-charset='gb18030'。

其次利用%ls输出宽字符串时也需要注意隐式转换，看下面例子：

/* widechar.c, 该文件采用utf8编码 */

int main(int argc, const char *argv[])

{

wchar_t w[] = L"中国";

printf("%ls\n", w);

return 0;

}

编译ok，但执行后发现无法输出“中国"二字。printf在%ls下支持输出宽字符串，但是也是需要显式指定locale的，否则当前LC_ALL就等于"C"，在"C"locale下printf显然无法将宽字符"中国"成功转换为utf8编码并输出。我们稍作修改：

/* widechar.c, 该文件采用utf8编码 */

int main(int argc, const char *argv[])

{

setlocale(LC_ALL, "");

wchar_t w[] = L"中国";

printf("%ls\n", w);

return 0;

}

通过setlocale(LC_ALL, "")将locale指定为用户当前locale，这样我们就可以顺利见到"中国"字样了。printf做了一次宽字符到utf8的转换后，再将utf8字符串打印到控制台上，为我们所见。

最后，C99支持在源码中使用通用字符名(Universal Character Name, UCN)来表示任何扩展字符集中的字符。利用\U或\u来指定一个Unicode字符，但是注意千万不要以为宽字符和\U0000nnnn或\unnnn是等价的。下面这么做是无法达到你的预期的：

wchar_t w = '\u4e2d'; /* 4e2d是"中"字的Unicode编码 */

如果按我们的预期，w中的4个字节应该依次是0×00，0×00，0x4e和0x2d。但经过实际探测，我们得到的却是0×00、0xe4、0xb8和0xad，这恰恰是"中"的utf8编码。而且编译器还在这一行给出了警告：warning: multi-character character constant。这里也是一种隐式转换，使用UCN表示的Unicode字符将首先被按照执行字符集做转换后再作为右值，此时它就和一个多字节字符串无异，所以这里使用char mbs[] = "\u4e2d"才是正确的。我们可以将\u或\U作为转义字符来看待，这样在真正的编译开始之前，当Compiler处理所有转义字符及字符串时，这些字符和字符串将被预先转换为执行字符集中对应的字符，正如\u4e2d被转换为e4b8ad。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论