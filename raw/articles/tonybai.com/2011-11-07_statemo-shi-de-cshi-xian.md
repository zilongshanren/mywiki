---
title: State模式的C实现
url: https://tonybai.com/2011/11/07/implement-state-pattern-in-c/
published: '2011-11-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# State模式的C实现

上个周末花了些时间将《[Pro Git](http://progit.org/book/zh)》（Git高手进阶之必读书籍，严重推荐^_^）快速地浏览了一遍，在感叹于[Git](http://git-scm.com)强大的同时，也见识到了Git的复杂。可以肯定的是Git学习曲线远没有学习[Subversion](http://tonybai.com/2011/03/23/also-talk-about-solving-the-svn-conflicts/)那样平坦。比如，Subversion工作目录下的文件只有三种状态：Untracked、Modified和Committed(即Unmodified)；而以Git本地工作目录下则有四种状态：Untracked、Staged、Modified和Committed(即Unmodified)。虽然只多出了一种状态，但感觉其复杂度又上了一个台阶。

Git在这里只是一个引子，我真正要说的还是[设计模式](http://tonybai.com/tag/设计模式)，只不过这个模式对应的例子实现与Git的一个命令相关罢了。这个命令就是Git status。Git status可以根据当前工作目录下文件的不同状态输出不同的提示信息，例如，对于工作目录中处于"未跟踪"状态的文件foo.txt，Git会输出下面信息：

$ git status

# On branch master

#

# Untracked files:

# (use "git add [file]…" to include in what will be committed)

#

# foo.txt

nothing added to commit but untracked files present (use "git add" to track)

而对于工作目录下处于已修改(modified)，但未缓存(unstaged)的文件foo.txt，它的输出就会变成：

$ git status

# On branch master

# Changed but not updated:

# (use "git add [file]…" to update what will be committed)

# (use "git checkout — [file]…" to discard changes in working directory)

#

# modified: foo.txt

#

no changes added to commit (use "git add" and/or "git commit -a")

好了，假如你是负责实现这个功能的C程序员，你会如何来实现它呢？是这样吗：

void git_status(const struct file_t *file) {

switch(file->status) {

case UNTRACKED:

…

case STAGED:

…

case MODIFIED:

…

case COMMITED:

…

default:

…

}

}

对于众多设计模式的忠实粉丝来说，这样的实现势必会"犯众怒"：怎么可以有switch…case呢，怎么可以让git_status与file_t的内部状态值耦合在一起呢？经验告诉我们：遇到问题，找模式！这次的题目似乎给了我们很直观的提示：我们应该用State模式来改造git_status的实现。

首先抽出接口file_state_t。

/* file_state.h */

struct file_state_t {

void (*file_state_func)(struct file_state_t *this, const char *filename, void *arg);

};

接下来，我们给出各位文件状态的实现，包括untracked_file_state、modified_file_state、committed_file_state以及staged_file_state，为了节省篇幅这里谨以untracked_file_state为例：

/* untracked_file_state.h */

struct file_state_t* untracked_file_state_instance();

void untracked_file_state_destroy();

/* untracked_file_state.c */

struct untracked_file_state_t {

struct file_state_t fs;

/* other fields here… */

};

static struct untracked_file_state_t *_untracked_file_state = NULL;

static void dump_untracked_file_state(struct file_state_t *this, const char *filename, void *arg) {

printf("# Untracked files:\n"

"# (use \"git add [file]…\" to include in what will be committed)\n"

"#\n"

"# %s\n"

"nothing added to commit but untracked files present (use \"git add\" to track)\n",

filename);

}

struct file_state_t* untracked_file_state_instance() {

if (!_untracked_file_state) {

_untracked_file_state = (struct untracked_file_state_t*)malloc(sizeof(*_untracked_file_state));

if (!_untracked_file_state) return NULL;

memset(_untracked_file_state, 0, sizeof(*_untracked_file_state));

_untracked_file_state->fs.file_state_func = dump_untracked_file_state;

}

return (struct file_state_t*)_untracked_file_state;

}

void untracked_file_state_destroy() {

if (_untracked_file_state)

free(_untracked_file_state);

_untracked_file_state = NULL;

}

untracked_file_state_t对象的创建方式采用了类似Singleton模式的手法，减少了频繁创建销毁带来的消耗，在后面使用这个state对象时我们会看得更加清楚。其他几个file_state_t接口的实现大同小异，不同的是dump_xx_file_state的实现。

最后，将各个State对象用于模拟Git场景中，我们来看看效果：

/* main.c */

struct file_t {

char filename[PATH_MAX];

struct file_state_t *state;

};

static struct file_t* file_new(const char *filename) {

struct file_t *f = (struct file_t*)malloc(sizeof(*f));

if (!f) return NULL;

memset(f, 0, sizeof(*f));

strcpy(f->filename, filename);

/* 文件的初始状态: Untracked */

f->state = untracked_file_state_instance();

if (!f->state) {

free(f);

return NULL;

}

return f;

}

static void file_status(struct file_t *f) {

f->state->file_state_func(f->state, f->filename, NULL);

}

static void file_add(struct file_t *f) {

f->state = staged_file_state_instance();

}

static void file_commit(struct file_t *f) {

f->state = committed_file_state_instance();

}

static void file_modified(struct file_t *f) {

f->state = modified_file_state_instance();

}

int main(int argc, const char *argv[])

{

struct file_t *f = file_new("foo.txt");

file_status(f);

file_add(f);

file_status(f);

file_commit(f);

file_status(f);

file_modified(f);

file_status(f);

return 0;

}

这个程序的输出结果与预期完全一致。没有了switch…case，没有了实现耦合，这下很多模式Fans怒火可以消消了。不过State模式的这种实现缺点也很明显，那就是一旦状态众多，对应的file_state_t接口实现的数量也就随着增多，从实现角度来看，代码似乎有些散。

从例子中我们可以看出这种State模式的实现是一种行为驱动的状态迁移，这种状态迁移是由State对象的使用者在上下文完成的。

用C语言亲手实现了多个模式后（[Iterator](http://tonybai.com/2010/01/30/implement-iterator-in-c/)、[Observer](http://tonybai.com/2011/10/14/implement-observer-pattern-in-c/)、[Strategy](http://tonybai.com/2011/10/20/implement-strategy-pattern-in-c/)、[Chain of Responsibility](http://tonybai.com/2011/10/25/implement-chain-of-responsibility-pattern-in-c/)和[Transaction](http://tonybai.com/2011/11/04/implement-transaction-pattern-in-c/)），愈来愈觉得其内在的思维方式是一致的。因此以后面对问题也大可不必拘泥于某一种模式，而是要融会贯通，以无招胜有招，路子对了，一切也就水到渠成了。

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论