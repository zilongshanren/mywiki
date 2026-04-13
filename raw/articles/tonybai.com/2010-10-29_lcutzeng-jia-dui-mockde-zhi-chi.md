---
title: lcut增加对mock的支持
url: https://tonybai.com/2010/10/29/lcut-add-mock-support/
published: '2010-10-29'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# lcut增加对mock的支持

记得恰好是在一个月前的今天，我[发布了lcut](http://tonybai.com/2010/09/30/opensource-a-lightweight-c-unit-test-framework/)(轻量级[C语言单元测试框架](http://tonybai.com/2005/11/08/the-design-and-implementation-of-c-unittest-framework/))[0.1.0版本](http://code.google.com/p/lcut/)

。由于发布仓促，文档没能及时跟上。在[stackoverflow](http://stackoverflow.com)的一个[关于单元测试的帖子](http://stackoverflow.com/questions/65820/unit-testing-c-code)

上，一位叫[Craig McQueen](http://craig.mcqueen.id.au/)的朋友也给出了建议："Some documentation would be helpful. Project background and goals, a features list, advantages over existing alternatives, etc would be helpful for people who are checking it out for the first time." 看完这个建议后心里那个汗啊！不过一想到用E文编写文档心里就有些打怵。就这样在这一个月里文档依旧没有改观:(。不过，lcut本身还是有一些进步的，这两天一直规划着为lcut增加[mock](http://tonybai.com/2008/04/12/mock-test-in-c-unit-test/)的支持，今天终于将这个功能加进了lcut，并发布了[lcut-0.2.0-beta](http://code.google.com/p/lcut/)版，欢迎大家试用，并提出意见和建议。

之前在单元测试过程中使用[cmockery](http://tonybai.com/2009/08/22/introduce-cmockery-for-c-unit-test/)中提供的mock功能，cmockery也是lcut的mock功能的直接灵感来源。与cmockery不同的是lcut将对输出参数的mock和对函数返回值的mock区分开来，这样用起来更加直观。

这里用一个简单的例子(完整代码在lcut包product_database_test.c文件中)来说明一下lcut的mock功能如何使用：

/* product_database.c */

int get_total_count_of_employee() {

database_conn *conn = NULL;

int retv = -1;

int total_count = -1;

conn = connect_to_database("tonybai", "tonybai", "mysql");

if (!conn)

return -1;

retv = table_row_count(conn, "EMPLOYEE_TABLE", &total_count);

if (retv < 0)

return -1;

return total_count;

}

/* product_database_test.c */

database_conn *connect_to_database(const char *user,

const char *passwd,

const char *serviceid) {

return (database_conn*)LCUT_MOCK_RETV();

}

int table_row_count(const database_conn *conn,

const char *table_name,

int *total_count) {

(*total_count) = (int)LCUT_MOCK_ARG();

return (int)LCUT_MOCK_RETV();

}

void tc_get_total_count_of_employee_ok(lcut_tc_t *tc, void *data) {

LCUT_RETV_RETURN(connect_to_database, 0×1234);

LCUT_ARG_RETURN(table_row_count, 5);

LCUT_RETV_RETURN(table_row_count, 0);

LCUT_INT_EQUAL(tc, 5, get_total_count_of_employee());

}

被mock的函数多为系统API或执行代价较高的第三方库函数，我们在业务代码更关心的是这些函数的接口行为，而C语言中函数的接口行为表现为：返回值和输出参数。我们需要通过控制被mock函数的接口行为来达到测试我们业务代码的目的，所以我们需要mock这些函数的返回值和输出参数。上面例子中connect_to_database和table_row_count就是两个被mock了的库函数。我们通过LCUT_MOCK_RETV来mock函数的返回值，通过LCUT_MOCK_ARG来mock函数的输出参数。在测试代码tc_get_total_count_of_employee_ok中，我们分别通过LCUT_RETV_RETURN和LCUT_ARG_RETURN来控制前面两个被mock的函数中mock obj的返回值和输出参数: LCUT_RETV_RETURN(connect_to_database, 0×1234)告诉connect_to_database返回(int)0×1234，相应的，LCUT_ARG_RETURN(table_row_count, 5)则告诉table_row_count执行后其输出参数*total_count的值为5。有了这些设定的mock obj我们就可以专注于我们业务层代码的白盒逻辑单元测试了，一旦connect_to_database和table_row_count的外部行为被控制后，业务层的代码get_total_count_of_employee的行为也就是可预期的了，我们用断言测试即可。

由于实现原理限制，如果你的函数输出参数类型或返回值类型为double*/float*，那么这个函数还不能使用lcut的mock功能，否则会编译出错。但绝大多数软件开发领域都很少使用浮点计算，所以lcut的mock还是可以满足大多数需要的。

题外话：

在公司使用代理上网，svn无法直接访问google code，这个问题一直困扰着我，直到今天才知道可以为svn客户端设置代理，设置步骤如下：

-> vi ~/.subversion/servers

-> 增加如下设置：

[global]

http-proxy-host = 你的代理主机域名或ip

http-proxy-port = 端口

http-proxy-username = 你的用户名

http-proxy-password = 你的密码

设置后，svn立马就可以连上google code的svn server了。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论