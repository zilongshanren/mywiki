---
title: Transaction模式的C实现
url: https://tonybai.com/2011/11/04/implement-transaction-pattern-in-c/
published: '2011-11-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Transaction模式的C实现

提到Transaction模式(即事务模式)，很多人会感到陌生。这并不奇怪，在大名鼎鼎的GoF的《[Design Pattern](http://book.douban.com/subject/1052241)》一书中，它仅仅是[Command模式](http://en.wikipedia.org/wiki/Command_pattern)的别名罢了。不过在实际的开发中，我们却经常会遇到可以应用事务模式的场景。本文可以理解成Command模式在事务领域的应用，但这样说有些麻烦，我们莫不如直接称之为Transaction模式。

与前几篇[设计模式C实现系列](http://tonybai.com/tag/设计模式)文章一样，这篇文章也源于对实际问题的思考和总结。这次的问题是这样的：我们的业务系统实现了一个ftp上传文件的功能，其v1版代码的结构简化后大致如下：

int ftp_upload_file(const char *filename, const remote_server_desc *desc) {

int ret;

ret = upload_local_file(filename, desc);

if (ret)

return ret;

ret = remove_local_file(filename);

if (ret)

return ret;

return rename_remote_file(filename, desc);

};

代码的大致流程是这样的：

1、首先调用upload_local_file，将本地文件(比如foo.txt)上传到远程主机(上传后名字为foo.txt.tmp)

2、然后调用remove_local_file，删除本地文件(如foo.txt)

3、最后调用rename_remote_file，对远程主机上的文件进行改名操作(如将foo.txt.tmp改为foo.txt)

正常情况下，这版代码工作的也很好，以下是正常情况下的输出：

upload [foo.txt.tmp] to host [10.10.12.123, incoming/txt] Ok!

remove localfile [foo.txt] Ok!

rename [foo.txt.tmp] to [foo.txt] Ok!

但明眼人都可以看出v1版本代码的问题，那就是对业务异常的处理不够理想，下面列举一些可能出现异常的环节：

1、upload_local_file可能出现异常，返回失败

这时文件也许已经上传成功，我们在退出整个上传流程之前，应该尝试调用remove_remote_file，删除远程主机上的文件，恢复系统状态到上传前状态；

2、remove_local_file可能出现异常，返回失败

此时文件已经上传成功，若不做任何处理而直接退出的话，会导致下次重复上传同名文件而出现覆盖异常。为了防止这一问题的发生，我们在退出整个上传流程之前，应该尝试调用remove_remote_file，删除远程主机上的文件，恢复系统状态；

3、rename_remote_file也可能出现异常，返回失败

此时文件已经上传成功，且本地文件已经被删除，若改名失败而不做任何处理，将会导致已经上传到远程主机上的文件永远不会被处理（因为后缀名为.tmp，远程主机上的处理程序无法识别）。为了应对这一异常，我们应该在退出整个上传流程之前，恢复本地文件，并删除已经上传到远程主机上的文件，以恢复系统状态。

于是，我们就有了v2版代码，见下面：

int ftp_upload_file(const char *filename, const remote_server_desc *desc) {

int ret;

ret = upload_local_file(filename, desc);

if (ret) {

(void)remove_remote_file(filename, desc);

return ret;

}

ret = remove_local_file(filename);

if (ret) {

(void)remove_remote_file(filename, desc);

return ret;

}

ret = rename_remote_file(filename, desc);

if (ret) {

(void)remove_remote_file(filename, desc);

(void)recovery_local_file(filename);

return ret;

}

return ret;

};

这样修改后，若rename出现异常，则执行结果会变为：

upload [foo.txt.tmp] to host [10.10.12.123, incoming/txt] Ok!

remove localfile [foo.txt] Ok!

rename [foo.txt.tmp] to [foo.txt] Failed!

remove [foo.txt.tmp] from host [10.10.12.123, incoming/txt] Ok!

recover localfile [foo.txt] Ok!

程序在出现异常后将系统状态恢复到未操作前，并会在下一次操作中重新尝试。可以看出这是一个典型的事务场景，即整个上传过程是一个不可分割的整体，其中包括的诸多操作要么都做，要么都不做。

一切初看上去都很美！但用优雅设计的尺度细致考量，我们就会发现一些问题：

首先，如果一个事务场景包含的操作序列很多，那代码中的异常处理将是很痛苦的事情，以最后一步操作为例，一旦异常出错，我们就需要显式做N步回退处理，代码必然显得十分繁琐。另外大量的错误码判断，也会引入诸多if，势必使得代码味道较差；

其次，事务操作的具体实现都暴露给调用者，这在调用者与事务实现之间引入耦合，不利于代码的单元测试与调试；

最后，类似的事务场景在系统中存在很多，如果按v2版本的实现方式，那么系统中将会存在大量类似结构的代码，也算是一种重复吧。

我们的解决手段无非还是面向接口和封装变化，于是我们就有了充分参考了Transaction模式解决方法的v3版代码。

/* 通用事务接口 transaction_unit.h */

struct transaction_unit_t {

int (*execute)(struct transaction_unit_t *this, void *arg); /* alias: commit */

int (*unexecute)(struct transaction_unit_t *this, void *arg); /* alias: rollback */

};

/* upload_request.h */

struct upload_request {

char filename[PATH_MAX];

char ip[16];

char path[PATH_MAX];

};

/* ftp_upload_transaction_unit.h */

struct transaction_unit_t* ftp_upload_transaction_unit_new();

void ftp_upload_transaction_unit_destroy(struct transaction_unit_t **tu);

/* ftp_upload_transaction_unit.c */

typedef struct operation_pair operation_pair;

typedef APR_RING_HEAD(operation_pair_head_t, operation_pair) operation_pair_head_t;

struct operation_pair {

APR_RING_ENTRY(operation_pair) link;

int (*do_func)(struct upload_request* r);

int (*undo_func)(struct upload_request* r);

};

struct ftp_upload_transaction_unit_t {

struct transaction_unit_t tu;

operation_pair_head_t ops;

operation_pair *op; /* 记录操作异常所在单元 */

};

struct transaction_unit_t* ftp_upload_transaction_unit_new() {

struct ftp_upload_transaction_unit_t *tu;

tu = (struct ftp_upload_transaction_unit_t*)malloc(sizeof(*tu));

if (!tu) return NULL;

memset(tu, 0, sizeof(tu));

tu->tu.execute = ftp_upload_transaction_execute;

tu->tu.unexecute = ftp_upload_transaction_unexecute;

APR_RING_INIT(&(tu->ops), operation_pair, link);

operation_pair *op = (operation_pair*)malloc(sizeof(*op)); /* 这里省略一些异常处理，下面也是如此 */

op->do_func = upload_local_file;

op->undo_func = remove_remote_file;

APR_RING_ELEM_INIT(op, link);

APR_RING_INSERT_TAIL(&(tu->ops), op, operation_pair, link);

op = (operation_pair*)malloc(sizeof(*op));

op->do_func = remove_local_file;

op->undo_func = recover_local_file;

APR_RING_ELEM_INIT(op, link);

APR_RING_INSERT_TAIL(&(tu->ops), op, operation_pair, link);

op = (operation_pair*)malloc(sizeof(*op));

op->do_func = rename_remote_file;

op->undo_func = NULL;

APR_RING_ELEM_INIT(op, link);

APR_RING_INSERT_TAIL(&(tu->ops), op, operation_pair, link);

return (struct transaction_unit_t*)tu;

}

static int ftp_upload_transaction_execute(struct transaction_unit_t *tu, void *arg) {

struct ftp_upload_transaction_unit_t *this = (struct ftp_upload_transaction_unit_t*)tu;

operation_pair *op = NULL;

int ret = 0;

APR_RING_FOREACH(op, &(this->ops), operation_pair, link) {

if (op) {

if (op->do_func) {

ret = op->do_func(arg);

if (ret) {

this->op = op;

return ret;

}

}

}

}

return ret;

}

static int ftp_upload_transaction_unexecute(struct transaction_unit_t *tu, void *arg) {

struct ftp_upload_transaction_unit_t *this = (struct ftp_upload_transaction_unit_t*)tu;

operation_pair *op = this->op;

if (!op)

return 0;

do {

if (op->undo_func) {

op->undo_func(arg);

}

op = APR_RING_PREV(op, link);

} while(op && (op != APR_RING_SENTINEL(&(this->ops), operation_pair, link)));

return 0;

}

/* main.c */

int ftp_upload_file(struct upload_request *r) {

int ret;

struct transaction_unit_t *tu = ftp_upload_transaction_unit_new();

/* 事务开始 */

ret = tu->execute(tu, (void*)r);

if (ret)

tu->unexecute(tu, (void*)r);

/* 事务结束 */

return ret;

};

int main(int argc, const char *argv[])

{

struct upload_request r = {"foo.txt", "10.10.12.123", "incoming/txt"};

return ftp_upload_file(&r);

}

代码有些长，所以省略了destroy等一些非关键性的实现代码。这里将事务模式的基本接口抽象为transaction_unit，而ftp_upload_transaction_unit则是transaction_unit接口的一个实现，它通过一个环形链表来组织由事务处理函数(do_func)以及对应事务回滚函数(undo_func)组成的操作单元。沿着链表正向遍历，即执行事务处理操作集合；一旦某个事务操作出现异常，便改为沿着链表反向遍历，即执行事务回滚操作集合，这样也就实现了一种具体的事务模式。

注意：这里仅是一种事务模式的实现思路，但其实现是否符合事务的要求还不一定，要给出一个完备的事务实现可并非易事，实现FTP上传事务更非易事。

原本设计模式的C实现系列文章在上一篇《[Chain of Responsibility模式的C实现](http://tonybai.com/2011/10/25/implement-chain-of-responsibility-pattern-in-c/)》之后就应该嘎然而止的，但变化总比计划快，于是就有了这篇文章。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论