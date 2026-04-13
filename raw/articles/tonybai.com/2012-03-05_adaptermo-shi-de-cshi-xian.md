---
title: Adapter模式的C实现
url: https://tonybai.com/2012/03/05/implement-adapter-pattern-in-c/
published: '2012-03-05'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Adapter模式的C实现

[Adapter](http://en.wikipedia.org/wiki/Adapter_design_pattern)(适配器)模式是《[Design Pattern](http://book.douban.com/subject/1052241)》一书中结构类模式集中的第一个模式，也是一个真正被我的同事在产品代码中应用的模式。

Adapter模式也是一个相对容易理解的模式，多数书籍和网络资料在描述这个模式时都使用了一个与电源适配器有关的例子，说不定Adapter模式还真的是源于对电源适配器的再思考和挖掘呢。

我们在重构遗留代码时引入了Adapter模式。遗留系统中存在的问题大致是这样的：按照规范，最初的系统只需要支持一种通信协议，这里把这个协议暂叫做proto_a。后来随着规范的丰富，客户又先后引入了两种协议proto_b和proto_c。前辈们在处理这些需求时偷了一个懒儿，选择了直接copy两份一模一样的业务逻辑代码以应对两个新协议，这样在遗留系统中就形成了一份业务逻辑，三份相同的代码的局面。可想而知，这样的代码结构是多么的不易于后续维护啊。一旦业务逻辑发生一处变化，我们就需要修改三个位置。代码味道那是相当的浓烈。在遗留代码的重构过程中，我们决定尝试用Adapter模式解决这个问题。

我们的目标是：一套业务逻辑，一套业务代码，支持三种不同的协议。还好这三种协议是基于同源设计的(从同一种协议演化而来)，也就是说具备设计统一操作接口的基础，这似乎天生就适合Adapter^_^。

我们首先定义多种协议的统一操作接口：

/* xx_proto_interface.h */

struct xx_proto_i {

int (*xx_proto_login)(void *trans);

int (*xx_proto_logoff)(void *trans);

int (*xx_proto_req)(void *trans, void *req);

int (*xx_proto_resp)(void *trans, int *status );

int (*xx_proto_heartbeat)(void *trans);

};

显然Adapter的引入就是因为proto_a、proto_b和proto_c原生的接口与统一接口有差别，无法直接使用。我们以proto_a为例，增加一个proto_a的Adapter层：

/* xx_proto_a_adapter.h */

#include "xx_proto_interface.h"

#include "proto_a.h"

struct xx_proto_i* get_proto_a_adapter_impl();

/* xx_proto_a_adapter.c */

#include "xx_proto_a_adapter.h"

static int xx_proto_a_login_adapter(void *trans);

static int xx_proto_a_logoff_adapter(void *trans);

static int xx_proto_a_req_adapter(void *trans, void *req);

static int xx_proto_a_resp_adapter(void *trans, int *status );

static int xx_proto_a_heartbeat_adapter(void *trans);

struct xx_proto_a_adapter_t {

struct xx_proto_i impl;

};

struct xx_proto_i* get_proto_a_adapter_impl() {

struct xx_proto_a_adapter_t *p = malloc(sizeof(*p));

if (p == NULL) return NULL;

p->impl.xx_proto_login = xx_proto_a_login_adapter;

p->impl.xx_proto_logoff = xx_proto_a_logoff_adapter;

p->impl.xx_proto_req = xx_proto_a_req_adapter;

p->impl.xx_proto_resp = xx_proto_a_resp_adapter;

p->impl.xx_proto_heartbeat = xx_proto_a_heartbeat_adapter;

return (struct xx_proto_i*)p;

}

static int xx_proto_a_login_adapter(void *trans) {

printf ("proto_a_login\n");

/* 这里使用proto_a的原生接口实现login */

return 0;

}

… …这里省略若干个实现

int xx_proto_a_heartbeat_adapter(void *trans) {

printf ("proto_a_receive_a_heartbeat\n");

/* 这里使用proto_a的原生接口实现heartbeat */

return 0;

}

实际上我们用proto_a的adapter包装(wrap)了proto_a的原生接口，也就是说proto_a的原生协议实现对客户是不可见的。在《设计模式》书中，Adapter模式的别名也叫Wrapper。

客户端是这么来使用协议的，客户端只需要使用统一的xx_proto_i中的接口即可：

#include "xx_proto.h"

#include "xx_proto_a_adapter.h"

#include "xx_proto_b_adapter.h"

#include "xx_proto_c_adapter.h"

int main() {

/* 根据需要我们灵活选择使用proto_a、proto_b或proto_c的adapter实现 */

struct xx_proto_i *p = get_proto_a_adapter_impl();

struct proto_a_trans;

/* some initializations */

… …

p->xx_proto_login(&trans);

p->xx_proto_req(&trans, …);

… …

}

任何事情都是有代价的，从上面可以看出Adapter模式的引用也使得代码变得庞大，很多proto的Adapter接口的实现可能都会是类似的和浅包装的。但与之前的问题相比，这些代价显然要小很多，并且用宏可以做适当改善。

题外话：适度抽象可以使得代码更加清晰，易于改变和维护。但物极必反，过度抽象反倒会让代码的可读性和易维护性下降，特别是在代码中使用了模式等手法时，千万不能沉迷，因为大家在理解你的多层过度抽象上所要付出的代价可能更大。

© 2012, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

抱歉，暂停评论。