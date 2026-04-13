---
title: Chain of Responsibility模式的C实现
url: https://tonybai.com/2011/10/25/implement-chain-of-responsibility-pattern-in-c/
published: '2011-10-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Chain of Responsibility模式的C实现

又是一个行为类的模式，似乎这类模式在使用C语言开发的项目中适应性更强，而另外两类模式创建型和结构型则略显不受待见^_^。

[Chain of Responsibility](http://en.wikipedia.org/wiki/Chain-of-responsibility_pattern)模式（中文名：职责链模式）是一个不算复杂的模式。虽不复杂，但用好了同样可以解决大问题。个人觉得其最大的好处就在于可以动态地重组针对一类对象的处理流程。正是得益于这一优势，它才可以在纷繁芜杂的业务领域站稳脚跟。

我们遇到的问题是这样的：有一类消息需要我们的系统处理，消息在系统入口处需经过种种业务层面上的校验，只有通过所有校验的消息才被允许进入到我们的系统中并被视为合法的消息。针对来自不同企业的消息，系统在入口处的校验规则是不同的，对于信用度较高的企业，系统实施的校验较少；而对于信用度不高的企业或新签约企业来说，其校验规则就相对多些；随着企业的信用度的变化，系统也会自动地调整对其下发消息的校验规则集。

最初关于这个部分的系统伪码大致是这样的：

int check_msg(corp_info, msg) {

if (corp_info->need_check_source) {

if (FAILED == check_source(msg))

return xx;

}

if (corp_info->need_check_destination) {

if (FAILED == check_destination(msg))

return xx;

}

if (corp_info->need_check_priority) {

if (FAILED == check_priority(msg))

return xx;

}

if (corp_info->need_check_content) {

if (FAILED == check_content(msg))

return xx;

}

return 0;

}

在check_msg外部，系统根据企业的信用度设置corp_info中的多个check feature开关，诸如need_check_source、need_check_content等，从而使得check_msg内部可以根据企业的不同feature开关情况，对企业发送的消息实施不同的校验规则。

这里消息校验的请求者与消息校验的处理者具有一定的耦合，另外check_msg中满眼的if语句也让我们的神经为之紧绷！于是我们尝试移除if，尝试降低请求者和执行者之间的耦合。在《[设计模式](http://book.douban.com/subject/1052241)》中我们找到了Chain of Responsibility模式，我们决定试试！

我们首先定义了handler_t接口：

struct handler_t {

void (*set_successor)(struct handler_t *this, struct handler_t *successor);

struct handler_t* (*get_successor)(struct handler_t *this);

int (*handle_request)(struct handler_t *this, void *obj, void *args);

int type; /* handler类型 */

};

接下来，我们根据例子的需要逐个定义该接口的实现：source_checker、destination_checker、priority_checker和content_checker。以source_checker为例：

/* source_checker.h */

struct handler_t* source_checker_new();

void source_checker_destroy(struct handler_t **h);

/* source_checker.c */

struct source_checker_t {

struct handler_t h;

struct handler_t *successor;

};

static void _set_successor(struct handler_t *this, struct handler_t *successor) {

struct source_checker_t *h = (struct source_checker_t*)this;

h->successor = successor;

}

static struct handler_t* _get_successor(struct handler_t *this) {

struct source_checker_t *h = (struct source_checker_t*)this;

return h->successor;

}

static int _handle_request(struct handler_t *this, void *obj, void *args) {

struct source_checker_t *h = (struct source_checker_t*)this;

struct msg_t *msg = (struct msg_t*)obj;

if (校验失败) /* 伪码 */

return FAILED;

printf(“[source_checker]: check msg – [%s]\n”, msg->msg_id);

if (h->successor)

return (h->successor->handle_request(h->successor, obj, args));

return SUCCESS;

}

struct handler_t* source_checker_new() {

struct source_checker_t *h;

h = (struct source_checker_t*)malloc(sizeof(*h));

if (!h) return NULL;

memset(h, 0, sizeof(*h));

h->h.set_successor = _set_successor;

h->h.get_successor = _get_successor;

h->h.handle_request = _handle_request;

h->h.type = SOURCE_CHECKER;

return (struct handler_t*)h;

}

void source_checker_destroy(struct handler_t **h) {

struct source_checker_t *p = (struct source_checker_t*)(*h);

if (p) free(p);

(*h) = NULL;

}

destination_checker、priority_checker和content_checker与source_checker的实现类似，关键在于_handle_request的实现不同。

现在我们就可以在初始化阶段为不同企业组装不同的业务校验流程了，假设我们有两家企业A和B，A企业下发的消息需要进行全部业务校验，而B企业下发的消息仅需进行source check和destination check：

/* A企业消息的业务校验链 */

struct handler_t *A_destination_checker = destination_checker_new();

struct handler_t *A_priority_checker = priority_checker_new();

struct handler_t *A_content_checker = content_checker_new();

struct handler_t *A_msg_checker = source_checker_new();

A_msg_checker->set_successor(A_msg_checker, A_destination_checker);

A_destination_checker->set_successor(A_destination_checker, A_priority_checker);

A_priority_checker->set_successor(A_priority_checker, A_content_checker);

/* B企业消息的业务校验链 */

struct handler_t *B_destination_checker = destination_checker_new();

struct handler_t *B_msg_checker = source_checker_new();

B_msg_checker->set_successor(B_msg_checker, B_destination_checker);

我们可以将msg_checker的放入corp_info中，这样check_msg的新实现如下：

int check_msg(corp_info, msg) {

return corp_info->msg_checker->handle_request(corp_info->msg_checker, (void*)msg, NULL);

}

这样通过A企业下发的消息testAmsg通过check_msg得到的结果是：

[source_checker]: check msg – [testAmsg]

[destination_checker]: check msg – [testAmsg]

[priority_checker]: check msg – [testAmsg]

[content_checker]: check msg – [testAmsg]

而B企业下发的消息testBmsg通过check_msg得到的结果则是：

[source_checker]: check msg – [testBmsg]

[destination_checker]: check msg – [testBmsg]

前面说过动态重组针对某一对象的业务流程是职责链模式一大特点。当某企业信用度发生变化时，该企业对应的checker链也会动态修改。比如当企业A信用度增加时，系统将去除其对应的content check流程，去除过程的实现如下：

struct handler_t *h = A_msg_checker;

struct handler_t *successor = h->get_successor(h);

while (successor) {

if (successor->type == CONTENT_CHECKER) {

h->set_successor(h, successor->get_successor(successor));

break;

}


h = successor;

successor = successor->get_successor(successor);

}

重组校验链后，企业A下发的消息testAmsg通过msg_check得到的结果就变成了：

[source_checker]: check msg – [testAmsg]

[destination_checker]: check msg – [testAmsg]

[priority_checker]: check msg – [testAmsg]

也许大家也看到了职责链模式的缺点，那就是每增加一个业务处理对象就要增加一个handler_t的具体实现，如诸多xx_checker，在C语言开发中这至少需要一个头文件与一个源文件。但职责链模式对降低请求者与处理者之间的耦合，以及支持职责链的动态重组方面还是会给你带来很大帮助的。是否使用这种模式，需要你自己根据实际情况权衡利弊后做出选择。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论