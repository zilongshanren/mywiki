---
title: 也谈Configure脚本问题的解决
url: https://tonybai.com/2010/03/19/also-talk-about-solving-the-problem-of-configure-script/
published: '2010-03-19'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈Configure脚本问题的解决

开了一个下午的技术交流会，回到办公室时离下班时间已经不远，天气预报说今晚有暴雪，外面阴沉的天气似乎也证实了这一点。这时一个同事遇到了一个软件包编译的问题，一时无法解决，向我求助。

这是一个[libmemcached](http://tonybai.com/2010/03/15/try-libmemcached/)的编译问题，我们用的是libmemcached 0.34版本，我的同事在[PC Solaris](http://tonybai.com/2009/09/10/something-about-installing-solaris-10/)上执行libmemcached的configure脚本时遇到如下错，Configure脚本提示：

checking for pthread-config… no

configure: error: could not find libpthread

但经过确认系统中明明在/usr/lib下有pthread相关库的存在：

Tony Bai-[~/libmemcached-0.34]526:>ll /usr/lib|grep pthread

lrwxrwxrwx 1 root root 26 2009 9月 10 llib-lpthread.ln -> ../../lib/llib-lpthread.ln

lrwxrwxrwx 1 root root 23 2009 9月 10 llib-lpthread -> ../../lib/llib-lpthread

lrwxrwxrwx 1 root root 25 2009 9月 10 libpthread.so.1 -> ../../lib/libpthread.so.1*

lrwxrwxrwx 1 root root 25 2009 9月 10 libpthread.so -> ../../lib/libpthread.so.1*

又确认了一下用户的环境变量设置，LD_LIBRARY_PATH也包含了这些库的目录。

经验告诉我，这个错误是假象，向上翻Configure的输出结果，的确发现些奇怪的Check结果，如下：

checking for ANSI C header files… no

checking for sys/types.h… no

checking for sys/stat.h… no

checking for stdlib.h… no

checking for string.h… no

checking for memory.h… no

checking for strings.h… no

checking for inttypes.h… no

checking for stdint.h… no

checking for unistd.h… no

第一感觉，这怎么可能呢？这些标准C库头文件居然都Check失败了！在网上用“checking for [ANSI C](http://en.wikipedia.org/wiki/ANSI_C) header files… no”搜了一下，也没有找到很好的答案。

我对Configure了解也不多，但是还是让我发现了config.log这根救命稻草。config.log这个文件详细地记录了Configure的每一步校验的执行内容和结果，其中对于标准C头文件的Check是这样做的：

configure:4827: checking for ANSI C header files

configure:4857: gcc -c -g -O2 -m64 conftest.c >&5

conftest.c:1: sorry, unimplemented: 64-bit mode not compiled in

configure:4864: $? = 1

configure: failed program was:

| /* confdefs.h. */

| #define PACKAGE_NAME "libmemcached"

| #define PACKAGE_TARNAME "libmemcached"

| #define PACKAGE_VERSION "0.34"

| #define PACKAGE_STRING "libmemcached 0.34"

| #define PACKAGE_BUGREPORT "http://tangent.org/552/libmemcached.html"

| /* end confdefs.h. */

| #include

| #include

| #include

| #include

|

| int

| main ()

| {

|

| ;

| return 0;

| }

configure:4995: result: no

再往下看，检测sys/types.h等标准库头文件的错误都是：

conftest.c:1: sorry, unimplemented: 64-bit mode not compiled in

configure:5047: $? = 1

看来并非是系统没有包含标准头文件，而是Configure采用了64-bit编译的方法去测试头文件存在的时候出错。随意创建一个testm64.c的源文件，输入:

/* testm64.c */

int main() {

;

return 0;

}

用gcc -g -m64 testm64.c执行编译，得到与之前相同的错误结果：

testm64.c:1: sorry, unimplemented: 64-bit mode not compiled in

查看Gcc版本，发现是3.4.6，突然恍然大悟，这不是之前发现在Solaris 10 for x86上Gcc 64位编译的[一个问题](http://tonybai.com/2009/11/05/a-64bit-compiling-problem-on-x86-solaris/)吗，在Solaris 10 for x86上如果要进行64位编译，要使用/usr/sfw/bin下的gcc 3.4.3版本，不能用3.4.6版本。

除了更换[Gcc](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)之外，如果你想编译32位版本的话，还可以这样来做：修改Configure脚本，打开Configure，将-m64字样全部删除。这样Configure后编译libmemcached就一切顺利了。

以上关于Configure脚本问题的解决方法，有一定的通用性，因此记之。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

牛