---
title: 为函数添加enter和exit级trace
url: https://tonybai.com/2011/07/13/add-enter-and-exit-trace-for-your-function/
published: '2011-07-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 为函数添加enter和exit级trace

日常开发中，我们为了辅助程序调试常常在每个函数的出入口(entry/exit)增加Trace，一般我们多用宏来实现这些Trace语句，例如：

#ifdef XX_DEBUG_

#define TRACE_ENTER() printf("Enter %s\n", __FUNCTION__)

#define TRACE_EXIT() printf("Exit %s\n", __FUNCTION__)

#else

#define TRACE_ENTER()

#define TRACE_EXIT()

#endif

有了TRACE_ENTER和TRACE_EXIT后，你就可以在你的函数中使用它们了。例如：

void foo(…) {

TRACE_ENTER();

… …

TRACE_EXIT();

}

这样你就可以很容易看到函数的调用关系。不过这种手法用起来却不轻松。首先你需要在每个函数中手工加入TRACE_ENTER和TRACE_EXIT，然后再利用XX_DEBUG_宏控制其是否生效。特别是对于初期未添加函数级Enter/Exit Trace的项目，后期加入工作量很大。

不过[Gcc](http://tonybai.com/2006/03/14/explain-gcc-warning-options-by-examples/)给我们提供了另外一种方便的手法：使用GCC的-finstrument-functions选项。-finstrument-functions使得GCC在生成代码时自动为每个函数在入口和出口生成__cyg_profile_func_enter和__cyg_profile_func_exit两个函数调用。我们要做的就是给出一份两个函数的实现即可。最简单的实现莫过于打印出被调用函数的地址了：

/* func_trace.c */

__attribute__((no_instrument_function))

void __cyg_profile_func_enter(void *this_fn, void *call_site) {

printf("enter func => %p\n", this_fn);

}

__attribute__((no_instrument_function))

void __cyg_profile_func_exit(void *this_fn, void *call_site) {

printf("exit func <= %p\n", this_fn);

}

我们将这两个函数放入libfunc_trace.so：gcc -fPIC -shared -o libfunc_trace.so func_trace.c

我们为下面例子添加enter/exit级Trace：

/* example.c */

static void foo2() {

}

void foo1() {

foo2();

}

void foo() {

chdir("/home/tonybai");

foo1();

}

int main(int argc, const char *argv[]) {

foo();

return 0;

}

$ gcc -g example.c -o example -finstrument-functions

$ LD_PRELOAD=libfunc_trace.so example

enter func => 0×8048524

enter func => 0x80484e5

enter func => 0x80484b2

enter func => 0×8048484

exit func <= 0×8048484

exit func <= 0x80484b2

exit func <= 0x80484e5

exit func <= 0×8048524

不过只输出函数地址很难让人满意，根据这些地址我们无法得知到底对应的是哪个函数。那我们就尝试一下将地址转换为函数名后再输出，这方面GNU依旧给我们提供了工具，它就是addr2line。addr2line是[binutils](http://www.gnu.org/s/binutils)包中的一个工具，它可以根据提供的地址在可执行文件中找出对应的函数名、对应的源码文件名以及行数。我们改造一下func_trace.c中的两个函数的实现：

/* func_trace.c */

static char path[PATH_MAX];

__attribute__((constructor))

static void executable_path_init() {

char buf[PATH_MAX];

memset(buf, 0, sizeof(buf));

memset(path, 0, sizeof(path));

#ifdef _SOLARIS_TRACE

getcwd(buf, PATH_MAX);

sprintf(path, "%s/%s", buf, getexecname());

#elif _LINUX_TRACE

readlink("/proc/self/exe", path, PATH_MAX);

#else

#error "The OS has not been supported!"

#endif

}

__attribute__((no_instrument_function))

void __cyg_profile_func_enter(void *this_fn, void *call_site) {

char buf[PATH_MAX];

char cmd[PATH_MAX];

memset(buf, 0, sizeof(buf));

memset(cmd, 0, sizeof(cmd));

sprintf(cmd, "addr2line %p -e %s -f|head -1", this_fn, path);

FILE *ptr = NULL;

memset(buf, 0, sizeof(buf));

if ((ptr = popen(cmd, "r")) != NULL) {

fgets(buf, PATH_MAX, ptr);

printf("enter func => %p:%s", this_fn, buf);

}

(void) pclose(ptr);

}

__attribute__((no_instrument_function))

void __cyg_profile_func_exit(void *this_fn, void *call_site) {

char buf[PATH_MAX];

char cmd[PATH_MAX];

memset(buf, 0, sizeof(buf));

memset(cmd, 0, sizeof(cmd));

sprintf(cmd, "addr2line %p -e %s -f|head -1", this_fn, path);

FILE *ptr = NULL;

memset(buf, 0, sizeof(buf));

if ((ptr = popen(cmd, "r")) != NULL) {

fgets(buf, PATH_MAX, ptr);

printf("exit func <= %p:%s", this_fn, buf);

}

(void) pclose(ptr);

}

在我的Ubuntu 10.04下，我们编译和执行

$ gcc -D_LINUX_TRACE -fPIC -shared -o libfunc_trace.so func_trace.c

$ gcc -g example.c -o example -finstrument-functions

$ LD_PRELOAD=libfunc_trace.so example

$ example

enter func => 0×8048524:main

enter func => 0x80484e5:foo

enter func => 0x80484b2:foo1

enter func => 0×8048484:foo2

exit func <= 0×8048484:foo2

exit func <= 0x80484b2:foo1

exit func <= 0x80484e5:foo

exit func <= 0×8048524:main

关于这个实现，还有几点要说道说道：

首先libfunc_trace.so是[动态链接](http://tonybai.com/2008/02/03/symbol-linkage-in-shared-library/)到你的可执行程序中的，那么如何获取addr2line所需要的文件名是一个问题；另外考虑到可执行程序中可能会调用chdir这样的接口更换当前工作路径，所以我们需要在初始化时就得到可执行文件的绝对路径供addr2line使用，否则会出现无法找到可执行文件的错误。在这里我们利用了GCC的__attribute__扩展：

__attribute__((constructor))

这样我们就可以在main之前就将可执行文件的绝对路径获取到，并在__cyg_profile_func_enter和__cyg_profile_func_exit中直接引用这个路径。

在不同平台下获取可执行文件的绝对路径的方法有不同，像Linux下可以利用"readlink /proc/self/exe"获得可执行文件的绝对路径，而Solaris下则用getcwd和getexecname拼接。

再总结一下，如果你想使用上面的libfunc_trace.so，你需要做的事情有：

1、将编译好的libfunc_trace.so放在某路径下，并export LD_PRELOAD=PATH_TO_libfunc_trace.so/libfunc_trace.so

2、你的环境下需要安装binutils的addr2line

3、你的应用在编译时增加-finstrument_functions选项。

我已经将这个小工具包放到了Google Code上，有兴趣的朋友可以在[这里](http://code.google.com/p/bigwhite-code/)下载完整源码包（20110715更新：支持输出函数所在源文件路径以及所在行号，前提编译你的程序时务必加上-g选项）。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

是否 有办法 记录函数 进入, 退出时候的行号. 因为有时候函数有很多return语句.不知道是那个条件出发 return的. 如果可以这样的话, 跟问题可能会更好很多.

呵呵, 你代码的这一步我也实现了. 问题是:进入和 退出同一个函数的行数是相同的; 因为我们是基于 函数地址去找行号的,是固定床的. 而不是像 __LINE__ 宏一样是动态的.

很不错的技术博客，赞一个