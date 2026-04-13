---
title: lcut 0.3.0版本发布
url: https://tonybai.com/2012/04/10/lcut-0-3-0-release/
published: '2012-04-10'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# lcut 0.3.0版本发布

[lcut](http://code.google.com/p/lcut)单元测试框架在我的项目中应用已经有一段时间了，项目组的同事对[lcut](http://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/)的使用也是越来越熟悉，这不今天一位同事还提出了一个新需求，需求大致是这样的。

在实际项目中，经常遇到这类情况：

int bar(…) {

int ret;

ret = foo(…);

/* assert ret */

…

ret = foo(…);

/* assert ret */

…

ret = foo(…);

/* assert ret */

…

}

void tc_test_bar_return_ok(lcut_tc_t *tc, void *data) {

LCUT_RETV_RETURN(foo, 0);

LCUT_RETV_RETURN(foo, 0);

LCUT_RETV_RETURN(foo, 0);

LCUT_ARG_RETURN(foo, 1);

LCUT_ARG_RETURN(foo, 1);

LCUT_ARG_RETURN(foo, 1);

LCUT_INT_EQUAL(tc, 0, bar(…));

…

}

我的同事希望lcut能提供一个接口：支持一次调用，设置多次mock obj的返回值或输出参数，使用这样的接口后，上述代码就可以简化为：

void tc_test_bar_return_ok(lcut_tc_t *tc, void *data) {

LCUT_RETV_RETURN_COUNT(foo, 0, 3);

LCUT_ARG_RETURN_COUNT(foo, 1, 3);

LCUT_INT_EQUAL(tc, 0, bar(…));

}

这个需求提的非常好，看起来更像是一种语法糖(

[syntactic sugar](http://en.wikipedia.org/wiki/Syntactic_sugar))，用于简化代码编写。于是乎下午我就为lcut增加了两个有用的宏：LCUT_RETV_RETURN_COUNT和LCUT_ARG_RETURN_COUNT。正如上面所说，这两个宏可在一次调用中多次设置某个mock obj的返回值和输出参数值，两个宏的原型如下：

#define LCUT_RETV_RETURN_COUNT(fcname, value, count) do { \

lcut_mock_obj_return(#fcname, (void*)value, __FUNCTION__, __LINE__, __FILE__, MOCK_RETV, count); \

} while(0);

#define LCUT_ARG_RETURN_COUNT(fcname, value, count) do { \

lcut_mock_obj_return(#fcname, (void*)value, __FUNCTION__, __LINE__, __FILE__, MOCK_ARG, count); \

} while(0);

只是比之前提供的LCUT_RETV_RETURN和LCUT_ARG_RETURN多了一个宏参数count。count用于指出对mocked obj进行多少次返回值或输出参数的设置。

另外当count传入-1时，其语义为无论mocked object被使用多少次，其返回值或输出参数值都是一样的，即使用LCUT_RETV_RETURN_COUNT或LCUT_ARG_RETURN_COUNT时设置的那个值，直到下一次调用这两个宏进行重新设置时，值才会发生变化。例如上面的例子我们也可以改写为：

void tc_test_bar_return_ok(lcut_tc_t *tc, void *data) {

LCUT_RETV_RETURN_COUNT(foo, 0, -1);

LCUT_ARG_RETURN_COUNT(foo, 1, -1);

LCUT_INT_EQUAL(tc, 0, bar(…));

}

这样无论后续再调用多少次bar函数，foo的返回值总是0，输出参数也总是1。

增加了这两个宏后，lcut的版本号也小升了一位，最新版本是

[lcut-0.3.0-rc1](http://lcut.googlecode.com/files/lcut-0.3.0-rc1.tar.gz)，其中还增加了一个针对lcut mock功能的example – mock_test.c。同时Google Code上的[lcut guide](http://code.google.com/p/lcut/wiki/lcut_user_guide_cn)也做了更新，对新增的宏的用法进行了简要说明。就这样，lcut 0.3.0版本算是发布了，后续还会经过内部的细致测试，如果没有什么问题，就会去掉rc。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论