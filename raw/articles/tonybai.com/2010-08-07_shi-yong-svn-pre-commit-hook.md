---
title: 使用svn pre-commit hook
url: https://tonybai.com/2010/08/07/use-svn-pre-commit-hook/
published: '2010-08-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用svn pre-commit hook

一直以来我们对项目代码的提交管理都是粗放型的，即对大家提交代码的时间、频率和提交日志的形式都没有严格的要求，可谓比较随意。主要发现的问题包括：

- 某些提交没有规划，甚至随意增加一些并无太大意义的注释都作一次提交。

- 提交的代码甚至没有经过REVIEW和UT，这样的代码即使内部发布，也会带来后续工作量的严重浪费（测试、发现问题、定位问题、重新fix、重新验证等）；

- 提交日志无实际意义，如commit log为空、commit log没能真实反映出这次提交的真实目的和意义、多次提交却采用同一条提交日志等等；

… …

以上，有些问题是需要通过过程要求改善的，有些问题则可以通过技术手段引导大家去完成，比如对commit log的校验。从[Tim的博客](http://timyang.net)中了解到twiiter内部对每次commit的log都做严格要求，至少必须填写此次代码变动的代码评审人。这个idea很好！这样开发人员每次尝试提交代码时都要想着填写reviewed by xxx。xxx是要对这次提交代码的质量负责任的；绝对禁止提交代码者随意填写上一个并未真实review其代码的人的名字。

使用[SVN](http://subversion.tigris.org)来进行代码版本控制工具的项目可采用svn pre-commit hook来实现对commit log的检查。在SVN服务器侧你的项目repos下有一个hook目录，该目录下存放着一些hook的模板（以.tmpl为后缀名）。各个hook模板中都有对该类型hook的说明，甚至还包括一段代码样例。如果你想使该hook启用，需要将xxx.tmpl改名为xxx，这样你再提交代码时，hook就会被svn server端自动调用。svn的hook其实就可以理解为一个可执行的文件，你可用各种语言（如shell脚本、C、Java、Python、Ruby等）实现hook。svn server端在调用hook时，会按照规定次序给hook传入N个确定含义的命令行参数供hook的实现使用。以pre-commit hook为例，svn server会依次传入REPOS和TXN；其中REPOS存储的是项目repository的路径信息；TXN则是此次提交的一个事务号名称。hook实现的返回值将作为svn server判断是否继续此次提交事务的依据：如果返回0，则svn server继续此次提交事务，否则svn server停止此次提交，并将hook实现中输出到标准错误的信息回送到客户端以作为错误提示。

下面是一个用C语言实现的pre-commit hook的简单例子：

/* pre-commit.c */

/* gcc -o pre-commit pre-commit.c */

int main(int argc, char *argv[]) {

char repos[PATH_MAX];

char txn[64];

memset(repos, 0, sizeof(repos));

memset(txn, 0, sizeof(txn));

strcpy(repos, argv[1]);

strcpy(txn, argv[2]);

/* 只对repos下的特定路径下的文件ci进行log检查 */

if (!filter_repos_subdir(txn, repos)) {

return check_log(txn, repos);

}

return 0;

}

对于一个repos，其下面有些folder中的文件可能并不一定是代码，可能不需要严格执行ci log格式的要求，filter_repos_subdir这个函数就旨在过滤此次提交的各个文件的路径信息：若判断出此次提交的文件路径均是不需要严格执行ci log格式要求的，则后续不作log check。

通过repos和txn两个参数我们如何获取此次提交的文件路径信息呢？svn提供了[svnlook](http://svnbook.red-bean.com/en/1.1/ch09s03.html)工具，我们利用svnlook changed -t txn repos可以获取文件路径信息。

#define SVNLOOK "/usr/local/bin/svnlook"

int filter_repos_subdir(const char *txn, const char *repos) {

FILE *fp;

char buf[PATH_MAX];

char cmd[PATH_MAX];

memset(cmd, 0, sizeof(cmd));

memset(buf, 0, sizeof(buf));

sprintf(cmd, "%s changed -t %s %s", SVNLOOK, txn, repos);

fp = popen(cmd, "r");

if (fp == NULL) {

fprintf(stderr, "%s\n", "popen failed");

return 1;

}

while (fgets(buf, PATH_MAX, fp) != NULL) {

if ((strstr(buf, "dog/") != NULL)

|| (strstr(buf, "cat/") != NULL)

|| (strstr(buf, "tiger/") != NULL) {

memset(buf, 0, sizeof(buf));

continue;

} else {

pclose(fp);

return 1;

}

}

pclose(fp);

return 0;

}

filter_repos_subdir利用popen与shell交互获取svnlook执行后输出的信息，如：

U dog/test1.c

U cat/test2.c

A tiger/test3.c

并对多行信息逐一进行过滤。

check_log与filter_repos_subdir类似，它通过svnlook log -t TXN REPOS获取此次提交的日志信息，并根据日志格式要求对日志进行校验，如发现不合格则返回失败；svn server将停止本次commit事务。

int check_log(const char *txn, const char *repos) {

FILE *fp;

char buf[PATH_MAX];

char cmd[PATH_MAX];

memset(cmd, 0, sizeof(cmd));

memset(buf, 0, sizeof(buf));

sprintf(cmd, "%s log -t %s %s", SVNLOOK, txn, repos);

fp = popen(cmd, "r");

if (fp == NULL) {

fprintf(stderr, "%s\n", "popen failed");

return 1;

}

while (fgets(buf, PATH_MAX, fp) != NULL) {

if (strstr(buf, "reviewed by")) {

pclose(fp);

return 0;

}

memset(buf, 0, sizeof(buf));

}

fprintf(stderr, "%s\n", "请填写此次提交代码的reviewer, log格式:… reviewed by xxx …");

pclose(fp);

return 1;

}

以上这个pre-commit hook demo只是为了说明hook的实现思路，如果你要打造自己的pre-commit hook可能还需要更严谨一些，另外还可加上更多有创意性的idea在里面！其他类型hook的实现思路大致一样，详细内容请参考[svn manual](http://svnbook.red-bean.com/)。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

用起来吧，坚决不是为用而用