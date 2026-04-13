---
title: 又遇字节序问题
url: https://tonybai.com/2011/01/21/encounter-byte-order-problem-again/
published: '2011-01-21'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 又遇字节序问题

今天上午处理了一个线上产品的故障。分析来分析去，最后定位问题还是出在[字节序](http://tonybai.com/2005/09/28/also-talk-about-byte-order/)转换的环节上。

其实测试组早在产品上线前就曾报告了这个问题，但是对应的开发人员并未对该问题进行深入地分析，而是有些草率地将该问题归结为客户端模拟器的实现不符合标准。因为这位同事比较资深，所以当时我也没有给予足够关注。

产品今天凌晨上线，9点左右业务量开始增大，这个问题立即就被我们在现场的运维人员发现，还好我们的系统是集群式的，运维同事及时的将线上有问题的版本停掉，用其他服务器支撑起了全部业务，躲过一劫。

我们还是回到这个问题上来。经验告诉我们：严重的问题往往都是由极其简单的错误导致的。这次也不例外！问题的直接原因就是：多调用了一次htonl。的确就是这么简单，但如果继续深入下去，我们还能得到一些收获。

当产品运行在x86服务器上，这个问题就会暴露出来，但是在Sun Sparc服务器上，该产品运行良好。我们分析后的结论是：这是由于在两种体系结构上htonl的实现不同而导致的。

我们先来做个试验，看下面的代码和执行结果：

/* testhtonl.c */

#include "stdio.h"

#include "arpa/inet.h"

int main() {

unsigned int a = 0×12345678;

unsigned int b = htonl(a);

printf("0x%x\n", b);

printf("0x%x\n", htonl(b));


return 0;

}

将上面代码分别在x86和Sparc上编译运行。在x86上([ubuntu](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/) 10.04 Gcc 4.4.3 x86)运行的结果如下：

0×78563412

0×12345678

而在Sparc上([Solaris 10](http://tonybai.com/2009/09/10/something-about-installing-solaris-10/) for Sparc, Gcc 3.4.6)运行的结果如下：

0×12345678

0×12345678

由此我们可以看出，htonl这个接口并不总等价于字节序转换。在Sparc这种Big-endian体系结构的平台上，htonl相当于直接将参数值返回；而在x86这样的little-endian体系结构平台上，htonl则是等价于一个reverse_byte_order接口，每次调用都会把输入参数的byte order倒转后的结果返回。

还回到我们的那个问题中：多调了一次htonl在Sparc平台上没有什么影响；但是在x86平台上，我们得到了相反字节序的结果，导致故障的出现。

这不是我们第一次遇到字节序问题了，不过却是第一次在线上产品中遇到，上一次是在开发过程中遇到的。这次发生的问题并不仅仅是技术上的问题，更多的是在工作的严谨性和工作态度上出现问题了。对我来说，这是一个很值得吸取的教训。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论