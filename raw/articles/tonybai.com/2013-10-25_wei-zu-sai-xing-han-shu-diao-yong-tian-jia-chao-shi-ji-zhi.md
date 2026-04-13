---
title: 为阻塞型函数调用添加超时机制
url: https://tonybai.com/2013/10/25/add-timeout-to-blocking-function-call/
published: '2013-10-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 为阻塞型函数调用添加超时机制

我们产品中的一个子模块在进行[Oracle](http://tonybai.com/2009/07/31/a-bug-of-oracle-oci-lib/)实时数据库查询时，常常因数据库性能波动或异常而被阻塞在[OCI API](http://tonybai.com/2009/07/31/a-bug-of-oracle-oci-lib/)的调用上，为此我们付出了“惨痛”的代价。说来说去还是我们的程序设计的不够完善，在此类阻塞型函数调用方面缺少微小粒度的超时机制。

调用阻塞多发生在I/O操作（磁盘、网络、低速设备）、第三方API调用等方面。对于文件/网络I/O操作，我们可利用在非阻塞文件描述符上select /poll的超时机制来替代针对阻塞型文件描述符的系统调用；但在第三方API方面，多数时候是无法用select/poll来进行超时的，我们可以选择 另外一种方法：利用setjmp和longjmp的非局部跳转机制来为特定阻塞调用添加超时机制。其原理大致是：**利用定时器(alarm、setitimer)设置超时时间，在SIGALRM的handler中利用longjmp跳到阻塞型调用之前，达到超时跳出阻塞型函数调用的效果**。同时这种方法通用性更好些。

这个机制实现起来并不难，但有些细节还是要考虑周全，否则很容易出错。我们的产品是需要运行在[Linux](http://tonybai.com/tag/Linux)和[Solaris](http://tonybai.com/tag/Solaris)两个平台下的，因此机制的实现还要考虑移植性的问题。下面简要说说在实现这一机制过程中出现的一些问题与解决方法。

**一、第一版**

考虑到阻塞型函数的原型各不相同，且我们的产品中对阻塞调用有重试次数的要求，因此打算将这个机制包装成一个[宏](http://tonybai.com/2008/05/17/examples-for-macro-definition-switch-and-mask/)，大致是这个模样：

#define add_timeout_to_func(func, n, interval, ret, …) \…

其中func是函数名；n是重试的次数；interval是超时的时间，单位是秒；ret是函数成功调用后的返回值，若失败，也是这个宏的返回值。

我们可以像下面这样使用这个宏：

/* example.c */

int

main()

{

#define MAXLINE 1024

char line[MAXLINE];

int ret = 0;

int try_times = 3;

int interval = 1000;

add_timeout_to_func(read, try_times, interval, ret, STDIN_FILENO, line, MAXLINE);

if (ret == E_CALL_TIMEOUT) {

printf("invoke read timeouts for 3 times\n");

return -1;

} else if (ret == 0) {

printf("invoke read ok\n");

return 0;

} else {

printf("add_timeout_to_func error = %d\n", ret);

}

}

add_timeout_to_func中为阻塞型函数添加的超时机制是利用setjmp/longjmp与信号的处理函数合作完成的。

/* timeout_wrapper.h */


#include <setjmp.h> #include <stdarg.h> #include <unistd.h> #include <stdio.h> #include <signal.h> #include <string.h> #include <errno.h> extern volatile int invoke_count; extern jmp_buf invoke_env; void timeout_signal_handler(int sig); typedef void (*sighandler_t)(int); #define E_CALL_TIMEOUT (-9) #define add_timeout_to_func(func, n, interval, ret, ...) \ { \ invoke_count = 0; \ sighandler_t h = signal(SIGALRM, timeout_signal_handler); \ if (h == SIG_ERR) { \ ret = errno; \ goto end; \ } \ \ if (sigjmp(invoke_env) != 0) { \ if (invoke_count >= n) { \ ret = E_CALL_TIMEOUT; \ goto err; \ } \ } \ \ alarm(interval);\ ret = func(__VA_ARGS__);\ alarm(0); \ err:\ signal(SIGALRM, h);\ end:\ ;\ }

/* timeout_wrapper.c */

#include "timeout_wrapper.h"

volatile int invoke_count = 0;

jmp_buf invoke_env;

void

timeout_signal_handler(int sig)

{

invoke_count++;

longjmp(invoke_env, 1);

}

编译运行这个程序，分别在Solaris、Linux下运行，遗憾的是两个平台下都以失败告终。

先说一下在Linux下的情况。在Linux下，程序居然不响应第二次SIGALRM信号了。通过strace也可以看出，当alarm被第二次调用后， 系统便阻塞在了read上，没有实现为read增加超时机制的目的。原因何在呢？我在《[The Linux Programming Interface](http://book.douban.com/subject/4292217/)》一书中找到了原因。原因大致是这样的，我们按照代码的执行流程来分析：

* add_timeout_to_func宏首先设置了信号的handler，保存了env信息(setjmp)，调用alarm设置定时器，然后阻塞在read调用上；

* 1s后，定时器信号SIGALRM产生，中断发生，代码进入信号处理程序，即timeout_signal_handler; Linux上的实现是当进入处理程序时，内核会自动屏蔽对应的信号(SIGALRM)以及此时act.sa_mask字段中的所有信号；在离开 handler后，内核取消这些信号的屏蔽。

* 问题在于我们是通过longjmp调用离开handler的，longjmp对应的invoke_env是否在setjmp时保存了这些被屏蔽的信号呢？ 答案是：在Linux上没有。这样longjmp跳到setjmp后也就无法恢复对SIGALRM的屏蔽；当再次产生SIGALRM信号时，程序将无法处 理，也就一直阻塞在read调用上了。

解决方法：将setjmp/longjmp替换为sigsetjmp和siglongjmp，后面这组调用在sigsetjmp时保存了屏蔽信号，这样在 siglongjmp返回时可以恢复到handler之前的信号屏蔽集合，也就是说SIGALRM恢复自由了。在Solaris 下，setjmp/longjmp是可以恢复被屏蔽的信号的。

再说说在Solaris下的情况。在Solaris下，程序在第二次SIGALRM到来之际，居然退出了，终端上显示：“闹钟信号”。这是因为在 Solaris下，通过signal函数设置信号的处理handler仅是一次性的。在应对完一次信号处理后，信号的handler被自动恢复到之前的处 理策略设置，对于SIGALRM来说，也就是程序退出。解决办法：通过多次调用signal设置handler或通过sigaction来长效设置 handler。考虑到移植性和简单性，我们选择了sigaction。在Linux平台下，signal函数底层就是用sigaction实现的，是简洁版的sigaction，因此它的设置不是一次性的，而是长效的。

**二、第二版**

综上问题的修改，我们有了第二版代码。

/* timeout_wrapper.h */

extern volatile int invoke_count;

extern sigjmp_buf invoke_env;

void timeout_signal_handler(int sig);

typedef void sigfunc(int sig);

sigfunc *my_signal(int signo, sigfunc* func);

#define E_CALL_TIMEOUT (-9)

#define add_timeout_to_func(func, n, interval, ret, …) \

{ \

invoke_count = 0; \

sigfunc *sf = my_signal(SIGALRM, timeout_signal_handler); \

if (sf == SIG_ERR) { \

ret = errno; \

goto end; \

} \

\

if (sigsetjmp(invoke_env, SIGALRM) != 0) { \

if (invoke_count >= n) { \

ret = E_CALL_TIMEOUT; \

goto err; \

} \

} \

\

alarm(interval); \

ret = func(__VA_ARGS__);\

alarm(0); \

err:\

my_signal(SIGALRM, sf); \

end:\

;\

}

/* timeout_wrapper.c */

volatile int invoke_count = 0;

sigjmp_buf invoke_env;

void

timeout_signal_handler(int sig)

{

invoke_count++;

siglongjmp(invoke_env, 1);

}

sigfunc *

my_signal(int signo, sigfunc *func)

{

struct sigaction act, oact;

act.sa_handler = func;

sigemptyset(&act.sa_mask);

act.sa_flags = 0;

if (signo == SIGALRM) {

#ifdef SA_INTERRUPT

act.sa_flags |= SA_INTERRUPT;

#endif

} else {

#ifdef SA_RESTART

act.sa_flags |= SA_RESTART;

#endif

}

if (sigaction(signo, &act, &oact) < 0)

return SIG_ERR;

return oact.sa_handler;

}

这里从《[Unix高级环境编程](http://book.douban.com/subject/1788421/)》中借了一段代码，就是那段my_signal的实现。这样修改后，程序在Linux和Solaris下工作都蛮好的。但目前唯一的缺点就是超时时间粒度太大，alarm仅支持秒级定时器，我们至少要支持毫秒级，接下来我们要换掉alarm。

**三、第三版**

setitimer与alarm是同出一门，共享一个定时器的。不同的是setitimer可以支持到微秒级的粒度，因此我们就用setitimer替换alarm，第三版仅改动了add_timeout_to_func这个宏：

#define add_timeout_to_func(func, n, interval, ret, …) \

{ \

invoke_count = 0; \

sigfunc *sf = my_signal(SIGALRM, timeout_signal_handler); \

if (sf == SIG_ERR) { \

ret = errno; \

goto end; \

} \

\

if (sigsetjmp(invoke_env, SIGALRM) != 0) { \

if (invoke_count >= n) { \

ret = E_CALL_TIMEOUT; \

goto err; \

} \

} \

\

struct itimerval tick; \

struct itimerval oldtick; \

tick.it_value.tv_sec = interval/1000; \

tick.it_value.tv_usec = (interval%1000) * 1000; \

tick.it_interval.tv_sec = interval/1000; \

tick.it_interval.tv_usec = (interval%1000) * 1000; \

\

if (setitimer(ITIMER_REAL, &tick, &oldtick) < 0) { \

ret = errno; \

goto err; \

} \

\

ret = func(__VA_ARGS__);\

setitimer(ITIMER_REAL, &oldtick, NULL); \

err:\

my_signal(SIGALRM, sf); \

end:\

;\

}

至此，一个为阻塞型函数调用添加的超时机制的雏形基本实现完毕了，但要放在产品代码里还需要更细致的打磨。至少目前只是在单进程单线程中跑过，而且要求每个函数中只能调用add_timeout_to_func一次，否则就会有编译错误。

以上完整代码我都放到github上的[experiments repository](https://github.com/bigwhite/experiments)中了，有兴趣的朋友可以下载细看。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

just want to say thank you for your code.

请教一下，当read进行超时处理的时候，是否有下面这样的风险，当read是一个读socket的操作，会陷入内核，将缓冲buff的地址传入内核，这个buff是当前stack frame里面的变量，当超时时候，信号处理函数执行，当前函数执行的stack frame就无效了，但是当read系统调用从内核执行完后会不会写传入进来的buff，但是这个buff可能已经是其他函数的stack fram了，从而导致问题？