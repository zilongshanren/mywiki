---
title: Observer模式的C实现
url: https://tonybai.com/2011/10/14/implement-observer-pattern-in-c/
published: '2011-10-14'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Observer模式的C实现

[设计模式](http://en.wikipedia.org/wiki/Design_pattern_(computer_science)) (Design Pattern，以下简称DP)的定义有很多种。我个人的理解：DP是人们在软件开发过程中所总结出来的一些典型问题的经验解决方法模板。使用它们可以使我们的代码更易被复用，更易扩展，更好地适应变化以及更便于后期维护。

人们都说设计模式是独立于语言的，但这里的"语言"更多的是指面向对象语言，比如Java、C++、C#、Python和Ruby等。使用面向对象语言(OO)在实现设计模式时更为自然而然。GoF的经典书籍[《Design Patterns》](http://book.douban.com/subject/1052241) 的副标题就是"Elements of Reusable Object-Oriented Software"，显然DP主要针对面向对象的软件开发，书中的内容也主要是用C++表述的。

相比于OO语言，关于[C语言](http://tonybai.com/tag/C/) 等面向过程的语言与设计模式结合使用的资料和例子都甚少，它们就像是走在两条互相平行的马路上的路人，老死不相往来。难道我们真地找不到C与设计模式的交集吗，非也！设计模式强调[高内聚，低耦合](http://tonybai.com/2010/09/17/the-nature-of-some-classical-design-rules/) ，一切面向接口！这种思想其实也有助于C程序员写出更加模块化、更加灵活以及更为优美的代码来。只是用C语言实现后所展现出来的形式与支持继承、多态的OO语言相比可能不是那么自然。

我相信在现实使用C语言的开发过程中，有些C程序员已经在不知不觉中使用了模式的思想，但DP对于多数C程序员还是略显生分的，虽然DP已经诞生10多年了，也许这与C语言诞生在设计模式之前不无关系^_^。

如何在日常开发中融入模式的思想呢？GoF在《Design Patterns》一书的第一章就告诉了我们,大致是一切从问题出发：弄清楚你遇到的问题，浏览模式，找到适合解决你的问题的模式。

言归正传。我们的系统常常有这样的业务情景：某种数据对象发生变化，与其相关的其他数据对象也需要一并做出改变。为了便于理解，这里举一个大家都比较易懂的例子：Tony是一个中国移动全球通(GoTone)用户，他订购了中国移动提供的139邮箱和手机报业务。中国移动有一个系统用于管理全球通用户信息、各种移动业务以及全球通用户的各种业务订购关系。Tony这个人记性不大好，每天丢三落四，同时也经常忘记及时缴纳手机话费，导致系统中Tony这个用户的状态经常在"正常"和"停机"间变来变去。为了防止Tony在停机的状态下依旧可以使用邮箱和手机报业务，移动公司提出了一个新需求：当用户处于"停机"状态时，用户应该无法使用139邮箱和手机报业务。如果你是负责开发这个需求的程序员，你如何在系统中满足这个需求呢？

将客户提出的需求翻译为程序员的行话就是当Tony的用户信息由"正常"变为"停机"时，系统需要同时修改139邮箱订购关系数据和手机报订购关系数据，将两类数据记录中Tony的订购关系由"开通"变为"暂停"；当Tony的用户信息由"停机"变为"正常"时，系统则需要将两类数据记录中Tony的订购关系由"暂停"改为"开通"。总之，当全球通用户信息发生变化时，139邮箱订购关系与手机报订购关系数据就需要随着进行变更。

从例子中已有的描述可以看出，现有的系统内部至少有三套数据集以及相应的数据操作接口，分别是全球通用户数据、139邮箱订购关系数据和手机报订购关系数据，这也是最基本的数据封装与抽象。现在我们就在此基础上来满足新的需求。

很多人首先想到的是修改全球通用户数据操作接口，实现两类订购关系的随动变更。

void update_gotone_customer_state(const char *number, int state) {

/* 根据number查找出对应的用户信息，并更新其state */

… …

/* 新增如下操作 */

update_mailbox_order(number, state);

update_newspaper_order(number, state);

}

我们可以看出这种方法是在全球通用户数据操作接口中直接调用两种订购关系的数据操作接口来修改数据状态，这种方法显然是耦合最高的方法，它在本无耦合的数据对象之间建立了耦合。update_mailbox_order和update_newspaper_order的变化将直接导致update_gotone_customer_state接口的变化。我们也无法独立地对update_gotone_customer_state接口进行单元测试了，除非对新增的两个依赖接口进行[mock](http://bigwhite.blogbus.com/logs/81333872.html) — 显然这种mock是被动的，也是不合理的。

为了去除这一方法引入的耦合，我们可以引入一个新函数来作为用户状态变更时的处理函数，如下：

void gotone_customer_state_switch(const char *number, int state) {

update_gotone_customer_state(number, state);

update_mailbox_order(number, state);

update_newspaper_order(number, state);

}

这种方法依次调用三个数据集各自的操作接口更新用户状态。显然这种方法去除了数据集操作接口之间的耦合，但也存在着另外一个更严重的问题，那就是这种方法难以适应移动业务日新月异的变化。

假定此时用户Tony又订购了一个移动业务 -手机电视，那么如何让手机电视订购关系感知到用户状态的变化呢？你可能会这样来改。

void gotone_customer_state_switch(const char *number, int state) {

update_gotone_customer_state(number, state);

update_mailbox_order(number, state);

update_newspaper_order(number, state);

update_mobiletv_order(number, state);

}

你知道这样的修改意味着什么吗？意味着程序要重新编译，重新发布以及重新部署上线。一个用户新订购了一个业务就带来如此大的变动，这是不能忍受的，不是吗！

关于这类问题，DP给出了一个解决模式，即Observer模式，中文叫作观察者模式。观察者模式中有两个主要元素：主题(Subject)和观察者(Observer)，主题的变更引发诸多相应观察者的随动更新。在这个例子中，全球通用户数据显然是一个Subject，而139邮箱、手机报以及手机电视等业务订购数据则是Observer的角色。

全球通用户数据是一个Subject，但是却是一个具体的Subject，如果让其与139邮箱等具体业务Observer直接关联，势必会像最初的解决方法那样在不同数据对象间引入耦合。DP始终在告诉我们要面向接口，要依赖抽象，所以我们需要建立抽象的Subject和Observer接口来。在C语言中没有interface关键字，也没有abstract class(抽象类)，C语言只有struct和函数指针。将struct和函数指针结合，我们就有了C语言接口的概念：

/* isubject.h */

struct iobserver_t;

struct isubject_t {

void (*attach)(struct isubject_t *subject, struct iobserver_t *observer);

void (*detach)(struct isubject_t *subject, struct iobserver_t *observer);

void (*notify)(struct isubject_t *subject, void *arg);

};

/* iobserver.h */

struct iobserver_t {

void (*update)(void *arg);

};

isubject_t声明了三个函数指针字段，attach用于增加监视这个Subject的Observer的；detach用于卸载监视这个Subject的某个Obsever；而notify则是在Subject发生变化时用于通知各个Observer进行更新的。iobserver_t相对比较简单，只有一个update函数指针字段，该字段指向的函数在Subject发生变化时被调用，完成Observer自身的更新。

isubject_t只是一个抽象的接口，我们还需要isubject_t的一个具体实现，包括attach, detach以及notify等函数的具体实现算法。下面是isubject_t的一个具体实现isubject_imp_t的相关数据类型与操作接口：

/* isubject_imp.h */

struct isubject_t* isubject_imp_new();

void isubject_imp_free(struct isubject_t **subject);

/* isubject_imp.c */

typedef struct _iobserver_t _iobserver_t;

/* 这里用apache apr库中的apr_ring作为存储observers的数据结构 */

typedef APR_RING_HEAD(_iobserver_head_t, _iobserver_t) _iobserver_head_t;

struct isubject_imp_t {

struct isubject_t subject; /* 这里务必将subject放在第一个字段的位置 */

_iobserver_head_t observers;

};

struct isubject_t* isubject_imp_new() {

struct isubject_imp_t *p = NULL;

p = (struct isubject_imp_t*)malloc(sizeof(*p));

if (!p) return NULL;

memset(p, 0, sizeof(*p));

APR_RING_INIT(&(p->observers), _iobserver_t, link);

p->subject.attach = isubject_imp_attach;

p->subject.detach = isubject_imp_detach;

p->subject.notify = isubject_imp_notify;

return (struct isubject_t*)p;

}

static void isubject_imp_attach(struct isubject_t *subject, struct iobserver_t *observer) {

struct isubject_imp_t *p = (struct isubject_imp_t *)subject;

//将observer插入ring，这里代码省略

}

static void isubject_imp_detach(struct isubject_t *subject, struct iobserver_t *observer) {

struct isubject_imp_t *p = (struct isubject_imp_t *)subject;


//将observer从ring中移出，这里代码省略

}


static void isubject_imp_notify(struct isubject_t *subject, void *arg) {

struct isubject_imp_t *imp = (struct isubject_imp_t *)subject;

//遍历ring，调用每个observer的update接口，并传入参数arg，这里代码省略

}

注意以上操作都是面向isubject_t这个接口类型的，而不是isubject_imp_t这个具体类型的，isubject_imp_t对于外部是不可见的。下面我们尝试用Observer模式解决一下上面例子中的问题。

首先建立tony这个用户的subject，并初始化其当前的业务Observer：

struct isubject_t *tony_subj = isubject_imp_new();

struct iobserver_t mailbox_observer = {

.update = update_mailbox_order

};

struct iobserver_t newspaper_observer = {

.update = update_newspaper_order

};

tony_subj->attach(tony_subj, &mailbox_observer);

tony_subj->attach(tony_subj, &newspaper_observer);

恰巧Tony上个月又忘记缴纳话费了，月初Tony的手机被停机了。中国移动的系统进行了Tony这个账户的状态变更操作：

tony_subj->notify(tony_subj, tony_account_info); /* tony_account_info表示Tony的基本账户信息 */

这行代码的执行结果是update_mailbox_order和upudate_newspaper_order被调用，139信箱以及手机报订购关系中有关Tony的订购信息状态变为"暂停"。也许上面的代码还没有让你看到Observer模式的好处，Ok，让我们进行一些变化！

移动为了推广3G业务，允许用户免费试用3个月的手机电视业务。有便宜不能不占，Tony遂订购了手机电视业务。前面的两种方法对于此种情况都无能为例，但采用了Observer模式之后，对于手机电视的订购，系统只需要在相应的处理函数中执行：

struct iobserver_t mobiletv_observer = {

.update = update_mobiletv_order

};

tony_subj->attach(tony_subj, &mobiletv_observer);

这样一来我们无需修改Tony被停机时的处理代码，手机电视订购关系也可以感知到Tony的账户变更。

同样，Tony使用了移动的手机上网套餐，打开手机浏览器，天下信息便可一览无余。于是Tony决定退订有些鸡肋的手机报业务，对于这一退订事件，系统只需要在相应的处理函数中执行：

tony_subj->detach(tony_subj, &newspaper_observer);

可以看到Tony停机的处理无需因手机报退订而做出改变，同时Tony停机也不会导致手机报订购关系数据的变更，这正是我们期望的。

以上是Observer模式的一种C语言实现，同时也解决了我们遇到的实际问题。关于Observer模式的详细描述还是参见GoF的《[Design Patterns](http://book.douban.com/subject/2111801/)》一书吧。用过程式语言实现DP的确不那么自然，但这就是C语言的方式。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论