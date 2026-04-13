---
title: 《Understanding and Using C Pointers》要点先睹为快
url: https://tonybai.com/2013/05/28/understanding-and-using-c-pointers-keypoint-preview/
published: '2013-05-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 《Understanding and Using C Pointers》要点先睹为快

*如果你问十个C程序员：你觉得C语言的核心是什么？这十个程序员都会回答：指针。*

指针具备成为C语言核心的两个关键要素：**强大**与**争议**。

* **指针的强大**源自于其天生与机器内存模型的适配。使用指针让代码紧凑，并可获得仅次于汇编代码的执行效率；使用指针可以让C程 序员毫不费力地尽情操纵着内存中的每个byte甚至是bit；使用指针可以为C程序员提供无与伦比的操作灵活性。总之，在C语言中指针几乎是无所 不能的代名词。得指针者得天下，没有指针，C语言将变得平庸。

* 成也指针，败也指针。**指针的争议**之处就在于其在赋予C程序员无比强大的Power的同时，也常常带来无穷的烦恼甚至灾祸，比如 内存问题、调试困难或因指针导致的程序崩溃等。就好比人类社会，做核心人物有争议是难免的，比如足球界有马拉多纳，跳水界有菲尔普斯，斯诺克界有 奥沙利文^_^。

好了，言归正传，我们回到C语言图书上来。目前市面上的C语言书籍，无论国内国外，无论经典还是山寨，基本都是百科大全型，将C语言讲的面面俱 到。比如最近的一本大而全的经典应当属《C Programming , A Modern Approach》，中文版书名为《[C语言程序设计：现代方法](http://book.douban.com/subject/4279678/)》第2版。以至于发展到今天，C语言似乎也没啥可讲的了，新出的C语言书大多是与前辈们雷同 的作品。近两年来也有O'reilly出版的C语言书籍，比如：

*《[Head First C](http://book.douban.com/subject/6919383/)》

*《[21st Century C – C Tips from the New School](http://book.douban.com/subject/11229717/)》

前者是典型的Head First风格的C教程，后者则是另辟蹊径，结合C语言外延（构建、调试、打包、版本控制、面向对象与C、知名C语言开源库等)进行讲解。这两本书虽形式 有变化，但终究脱离不开百科大全型，针对C的核心-指针并未有较多的深入探讨。而市场上专门写指针的书也稀少的很（似乎鬼子国那边有一本，叫什么 《[征服C指针](http://book.douban.com/subject/21317828/)》），唯一的一本书名与指针扯上关系的书《Pointers on C》（中文名“[C和指针](http://book.douban.com/subject/3012360/)”）其实依旧是一本C语言大全。于是乎国外著名出版社O'Reilly今年5月出品了一本专门讲解C语言核心 – **指 针**的书《[Understanding and Using C Pointers](http://book.douban.com/subject/20491037/)》，以满足C程序员深入理解C语言核心并实现进阶的诉求。O'Reilly就是O'Reilly，总是能抓住C语言书籍方面的深度阅读需 求^_^。

《Understanding and Using C Pointers》是个小册子，拢共才200多页，但内容却全部是围绕C语言指针展开的，从最基本的指针声明与操作、C内存模型、动态内存分配，讲到指针 与数组、结构体、字符串的关系，再到最后指针的高级特性：强制转换、Strict Aliasing、线程共享、多态支持等，由浅入深的进行细致的剖析。其作者认为作为C语言核心的指针值得花200页篇幅去讲解，而且期望所有读者在读完 此书后能对C指针有个扎实的理解。总之，这本书对系统C程序员理解C语言的核心-指针是大有裨益的。在其中文版（已经由图灵出版社引进版权了）尚 未出版之前，这里带你先了解以下本书的要点：

**第一章 简介**

*1、指针与内存*

【指针声明语法】

int *pi;

【理解复杂指针声明】

方法：从后向前读，例子：

const int *pci;

pci is a variable pci

pci is a pointer variable *pci

pci is a pointer variable to an integer int *pci

pci is a pointer variable to a constant integer const int *pci

【地址操作符】

pi = #

【输出指针值】

通过%x、%o、%p输出(printf)指针的值，一般使用%p（%p输出结果不一定等同于%x，是与实现有关的）。例子如下：

int num = 0;

int *pi = #

printf("Address of num: %d Value: %d\n",&num, num);

printf("Address of pi: %d Value: %d\n",&pi, pi);

Address of num: 4520836 Value: 0

Address of pi: 4520824 Value: 4520836

【通过间接访问操作符解引用指针】

间接访问操作符*，使用例子如下：

int num = 5;

int *pi = #

printf("%d\n",*pi); // Displays 5

*pi = 200;

printf("%d\n",num); // Displays 200

【指向函数的指针】

void (*foo)(); // 这个变量声明中的foo就是一个指向函数的指针

【Null概念】

null concept

赋值为NULL的指针变量表示该指针不指向任何内存地址。

null pointer constant

null concept的具体支撑实现，其常量值可能是常量值0，也可能不是。依具体实现而定。

NULL macro

在许多标准库实现中，NULL定义如下：#define NULL ((void *)0)，这也是我们对NULL的通常理解。当然这是依Compiler的具体实现而定的。如果编译 器使用非全0位模式实现了NULL，那该编译器就要保证在指针上下文中使用的NULL或0是null pointer。

ASCII NUL

一个全0的字节。

null string

一个不包含任何字符的空字符串。C字符串在最后都放置一个结尾0值。

null statement

只包含一个分号的空语句。

指向void的指针

指向void的指针被成为通用指针，可以用于引用任意类型的数据。它有两个属性：

– 指向void的指针与指向char类型的指针具有相同的内存表示与内存对齐约束。

– void指针永远不等于其他类型指针，两个赋值为NULL的void pointer是相等的。

任何指针都可以被赋给一个void pointer，并且之后还可以被转换回其原来的类型。

int num;

int *pi = #

void* pv = pi;

pi = (int*) pv;


void pointer用于数据指针，而不是函数指针。

全局void pointer或static void pointer在程序启动时被初始化为NULL。

*2、指针大小与类型*

在多数现代平台上，指针的大小都是相同的，与其类型无关。指向char的指针与指向结构体的指针大小相同。

指向函数的指针可能与指向数据类型的指针大小有差异，这要依具体实现而定。


【内存模型】

在不同机器和编译器下，C语言原生类型的大小是不同的。

描述不同数据模型的一般记法：I In L Ln LL LLn P Pn，例如LP64、ILP64、LP32等。


【预定义的指针相关类型】

size_t 用于表示对象的大小的一个安全类型。

ptrdiff_t 用于处理指针运算

intptr_t和uintptr_t 用于存 储指针地址

int num;

intptr_t *pi = #

*3、指针操作符*

【指针运算】

pointer + integer

指针实际移动的字节数 = integer + sizeof(integer_type)

void* pointer的指针运算操作行为是未定义的，依赖Compiler的具体实现。

pointer – integer

指针实际移动的字节树 = integer – sizeof(integer_type)。

pointer1 – pointer2

两个指针所指地址间的差值，常用于判断数组中元素的先后次序。

比较pointers

【指针比较】

指针可以使用标准的比较操作符（> and <）进行比较，可用来判断数组中元素的先后次序。

*4、指针的通常用法*


【多级间接寻址】

双指针(double pointer) – 指向指针的指针。

char *titles[] = {"A Tale of Two Cities",

"Wuthering Heights","Don Quixote",

"Odyssey","Moby-Dick","Hamlet",

"Gulliver's Travels"};

char **bestBooks[3];

bestBooks[0] = &titles[0];

bestBooks[1] = &titles[3];

bestBooks[2] = &titles[5];


间接寻址的级数并没有限制，但过多的级数会让人难以理解。


【常量和指针】

指向常量的指针

const int limit = 500;

const int *pci = &limit;

*pci = 600；/* Error， 我们不能解引用一个常量指针并修改其所指的内存值 */


const int *pci <=> int const *pci;

指向非常量的常量指针

int num;

int *const cpi = #

*cpi = 25; /* 可以解引用常量指针并修改其所指的内存的值 */

int limit;

cpi = &limit; /* Error，我们不能为常量指针重新赋新值 */

const int limit1 = 300;

int *const cpi1 = &limit1; /* Warning: 指向非常量的常量指针被用常量 的地址初始化了 */


指向常量的常量指针

const int limit = 300;

const int *const cpci = &limit; /* 声明后，我们不能通过cpci修改limit，也不能为cpci重新赋值 */

指向“指向常量的常量指针”的指针

const int limit = 300;

const int *const cpci = &limit;

const int *const *pcpci = &cpci;

**第二章 C语言动态内存管理**

在运行时通过函数手工从heap分配和释放内存的过程称为动态内存管理。

*1、动态内存分配*

【使用malloc函数】

int *pi = (int*) malloc(sizeof(int));

*pi = 5;

free(pi);

【内存泄漏】

– 丢失了内存地址

– 没有调用free函数释放内存

* 2、动态分配内存函数*

malloc、realloc、calloc、free

是否对malloc出的内存起始地址进行强制转型

int *p = (int*)malloc(4);

void *pointer可以转换为任意类型指针，没有强制转型也可以。

但显式的强制转型可以通过代码看出意图，并且与C++编译器(包括早期C编译器)兼容


你不能用内存分配函数分配的内存去初始化全局或Static变量。

alloca函数用于在栈上动态分配内存，函数结束时，这块内存自动释放；但alloca不是标准C库函数，移植性差。

C99支持可变长度数组(VLA)，数组声明时的元素个数可以是运行时才能确定值的变量，但数组size一旦在运行时被确定，数组大小就无法再做改变：

void compute(int size) {

char* buffer[size];

…

}

* 3、悬挂指针*

* *被free后依然引用原先内存地址的指针，称为dangling pointer。

悬挂指针可能导致如下问题：

– 如果访问其引用的内存，将导致不可预期的结果

– 如果内存不可访问了，将导致段错误

– 存在潜在的安全风险。

悬挂指针引起的问题调试起来十分困难，以下几种方法用于避免发生悬挂指针问题或快速查找悬挂指针问题：

– free后，设置指针为NULL；

– 编写一个替代free的函数；

– 用特定值填充free的内存块，便于快速定位dangling pointer问题

– 使用第三方工具检查dangling pointer问题

**第三章 指针与函数**

当与函数一起使用时，指针有两个方面发挥重要作用：

– 当指针以参数形式传递给函数时，允许函数修改指针所指内存区域的值，并且这种传递方式更加高效；

– 声明函数指针时，函数的名字被求值为函数的地址。


*1、程序栈和堆*

【程序栈】

栈和堆共享一块内存区域。栈在这块区域的低地址部分，堆在高地址部分。

程序栈用于存放栈帧(stack frame)，栈帧中存放的是函数的参数与local变量。

栈增长方向：向上；堆的增长方向：向下。

【栈帧的组成】

一个栈帧包含如下几个元素：

– 返回地址

– 本地变量

– 函数参数

– 栈指针(Stack pointer)和栈帧指针(base pointer or frame pointer)

Stack pointer和frame pointer用于运行时系统对栈的管理。前者总是指向栈的顶端；后者指向栈帧内的某个地址，比如函数的返回地址；frame pointer辅助程序访问栈帧内的元素。

栈帧的创建，见下面例子：

float average(int *arr, int size) {

int sum;

printf("arr: %p\n",&arr);

printf("size: %p\n",&size);

printf("sum: %p\n",&sum);

for(int i=0; i<size; i++) {

sum += arr[i];

}

return (sum * 1.0f) / size;

}

average的栈帧中沿着栈“向上”的方向，依次推入的是：

– 参数 size、arr （与声明的顺序恰好相反）

– 函数average调用的返回地址

– 本地变量sum（如果有多个本地变量，推入栈的顺序也与变量声明顺序相反）

每个线程通常都在自己的栈中创建栈帧。

*2、指针作为参数和返回值*

C语言的参数是“按值传递”的，包括指针本身，函数内使用的是参数的copy。

在处理大数据结构时，将指针作为参数传递给函数或作为返回值会使得程序执行起来更加高效（只是copy一个指针大小的数据，而不是指针所指向的数据对象大 小）。

另外一个以指针作为函数参数的目的是希望在函数内部对数据进行修改。

当传递一个指向常量的指针给函数时，其意图为不希望函数内部对指针所指的数据进行修改。例如void passingAddressOfConstants(const int* num1, int* num2)，不希望num1所指数据被修改。

将指针作为返回值返回时，应避免以下几个常见问题：

– 返回未初始化的指针

– 返回指向非法地址的指针

– 返回指向函数本地变量的指针

– 返回指针后，没有释放其所指的内存块


如果函数要修改的不是参数中指针所指的数据，而是指针本身所指的内存地址，那么应以double pointer形式作为函数参数：

void allocateArray(int **arr, int size, int value) {

*arr = (int*)malloc(size * sizeof(int));

if(*arr != NULL) {

for(int i=0; i<size; i++) {

*(*arr+i) = value;

}

}

}

int *vector = NULL;

allocateArray(&vector,5,45);

*3、**函数指针*

函数指针就是存放函数地址的指针。

使用函数指针可能导致程序运行变慢（可能感知不到），因为函数指针的使用可能导致CPU无法正确的运用分支预测，导致CPU流水线中断。

【声明函数指针】

函数指针的声明看起来像函数原型，比如：void (*foo)(int i);

程序员应该确保通过函数指针调用函数的正确使用，因为C编译器不会检查是否正确的为函数指针传入正确的参数（类型、顺序以及个数）。

通常我们用typedef声明一个函数指针类型，比如：

typedef void (*funcptr)(int i)；

funcptr fp = foo;

【函数指针强制转型】


一个类型的函数指针可以被强制转为另外一种类型函数指针。

转型后的指针 == 转型前的指针


typedef int (*fptrToSingleInt)(int);

typedef int (*fptrToTwoInts)(int,int);

int add(int, int);

fptrToTwoInts fptrFirst = add;

fptrToSingleInt fptrSecond = (fptrToSingleInt)fptrFirst;

fptrFirst = (fptrToTwoInts)fptrSecond;

printf("%d\n",fptrFirst(5,6));

在函数指针间转换，很可能导致函数调用失败。

**第四章 指针与数组**

*1、数组概述*

数组与指针记法关系紧密，在特定上下文中可以相互替换。

数组内部表示中并没有数组长度信息。


【一维数组】

int vector[5];

一维数组是一个线性结构。数组下标起始于0，终止于(元素个数-1)。

【二维数组】

int matrix[2][3] = {{1,2,3},{4,5,6}};

二维数组使用行和列标识数组元素。这类数组需要被映射到一个一维地址空间中。

在C中，二维数组的第一行放在内存的最开始处，接下来是第二行，…，直到最后一行，这就是所谓的“行主序”。

【多维数组】

int arr3d[3][2][4] = {

{{1, 2, 3, 4}, {5, 6, 7, 8}},

{{9, 10, 11, 12}, {13, 14, 15, 16}},

{{17, 18, 19, 20}, {21, 22, 23, 24}}

};

二维以上的维数的数组称为多维数组，其元素内存分配依旧遵守二维数组那种映射方式。

*2、指针记法(notation)与数组*

指针记法与数组记法在一定场合可以互换，但两者并不完全相同。

数组名单独使用时，我们得到的是数组的地址；该地址等同于数组内第一个元素的地址。

int vector[5] = {1, 2, 3, 4, 5};

int *pv = vector;

int (*pv)[5] = &vector;

vector与&vector不同，前者返回指向一个整型变量的指针（int *），后者返回一个指向整个数组的指针(int[5] *)。

pv[i] <=> *(pv + i)

*(pv + i) <=> *(vector + i)

【指针与数组间的不同】

int vector[5] = {1, 2, 3, 4, 5};

int *pv = vector;

sizeof(vector) = 20 != sizeof(pv)

pv是lvalue，可以被修改而指向不同的地址；比如pv = pv + 1

而vector不能被修改。vector = vector + 1这个表达式是错误的，不过pv = vector + 1是ok的。

【使用malloc创建一维数组】

int *pv = (int*) malloc(5 * sizeof(int));

pv[3] = 10;

可使用realloc改变malloc创建的数组的大小。


3*、传递一维数组*

两种记法：数组记法和指针记法，分别如下：

void displayArray(int arr[], int size);

void displayArray(int* arr, int size);

无论哪种，displayArray函数体内int arr[]或int *arr都将以int *arr方式使用，即数组名退化为指针，sizeof(arr) = 指针长度，而不是数组总长度。

【一维指针数组】


int* arr[5];

for(int i=0; i<5; i++) {

arr[i] = (int*)malloc(sizeof(int));

*arr[i] = i;

}

【指针与多维数组】

多维数组可以看成是由子数组组成的，就好比二维数组的每行都可以看成是一个一维数组。

int matrix[2][5] = {{1,2,3,4,5},{6,7,8,9,10}};

int (*pmatrix)[5] = matrix;

4*、传递多维数组*

void display2DArray(int arr[][5], int rows)；<=>

void display2DArray(int (*arr)[5], int rows)；

上面两个版本是等价的。两个版本都指定了列的值，因为编译器需要知道每行的元素个数。

注意第二个版本不等价于void display2DArray(int *arr[5], int rows)；

在void display2DArrayUnknownSize(int *arr, int rows, int cols)的 函数体实现中，你不能使用arr[i][j]，因为arr并未被声明为二维数组。

*5、动态分配二维数组*

【采用不连续的内存分配方式】

int rows = 2;

int columns = 5;

int **matrix = (int **) malloc(rows * sizeof(int *));

for (int i = 0; i < rows; i++) {

matrix[i] = (int *) malloc(columns * sizeof(int));

}

【采用连续内存分配的方式】

int rows = 2;

int columns = 5;

int **matrix = (int **) malloc(rows * sizeof(int *));

matrix[0] = (int *) malloc(rows * columns * sizeof(int));

for (int i = 1; i < rows; i++)

matrix[i] = matrix[0] + i * columns;

or

int *matrix = (int *)malloc(rows * columns * sizeof(int));

**第五章 指针与字符串**

*1、字符串基础*

字符串：以ASCII结尾'\0'字符结尾的字符序列。

分类：字节字符串(byte string) – char类型字符序列

宽字符串（wide string) – wchar_t 类型字符序列（每个字符16bit or 32bit，依编译器实现而定）

字符串声明：char header[32] or char *header；

【字符串字面量池(String literal pool)】

字符串字面量定义后将被放在字面量池中。这块内存区域存放的是组成字符串的字符序列。当一个字面量多次使用时，通常在字面量池中只存储一份该字符串。这将 降低程序的内存使用量。并且通常情况下，字面量池中的字符串是immutable的。

大多数编译器都提供了编译开关，用于指示是否关闭字符串字面量池，比如Gcc的-fwritable-strings。

【字符串初始化】、

char *header = "Media Player";

or

char header[] = "Media Player";

or

char header[13];

strcpy(header,"Media Player");

or

char *header = (char*) malloc(strlen("Media Player")+1);

strcpy(header,"Media Player");

*2、标准字符串操作*

比较字符串：strcmp

拷贝字符串：strcpy

连接字符串：strcat

*3、传递字符串*

传递简单字符串：

size_t stringLength(char* string) ;

size_t stringLength(char string[]);

传递字符串常量：

size_t stringLength(const char* string);

*4、返回字符串*

返回一个字面量：return "Boston Processing Center"；

动态分配的内存：

char* spaces = (char*) malloc(number + 1);

… …

return spaces;

返回local字符串的地址是危险的。

*5、函数指针与字符串*

**第六章 指针与结构体**

*1、简介*

【如何为结构体分配内存】

结构体的大小往往大于该结构体所有字段大小之和，因为有数据对齐的需求，导致编译器在进行结构体内存分配时进行了padding操作。特定数据类型具有一 定的对齐要求，比如short类型的字段要求其地址能被2整除，而integer类型的字段要求其起始地址能被4整除。

考虑到这些多余分配的内存，你应该谨慎对待如下操作：

– 小心使用指针运算

– 结构体数组的元素间有多余内存空间

【结构体内存释放】

为结构体分配内存时，运行时不会自动为结构体内的指针字段分配内存；同理，释放结构体内存时，运行时也不会自动释放结构体内指针字段所指向的内存。

【避免malloc和free的额外开销】

malloc和free多次重复调用时，会给程序带来额外的开销。一个解决方法就是自己维护一份已分配的结构。需要时，从这个池里取出一份，释放时，直接 返回给池中。如果没有可用的结构时，才考虑新创建一个。

*2、使用指针支持数据结构*

无论是简单还是复杂的数据结构，指针都提供了更加灵活的支持，包括链表、队列、栈以及树等。

**第七章 安全问题以及不当使用指针**


深入理解指针以及其正确的使用方法有利于开发出安全可信赖的应用。

OS引入了一些提升安全的技术，比如 Address Space Layout Randomization和Data Execution Prevention。

【Address Space Layout Randomization (ASLR) ，地址空间布局随机化】

ASLR技术使得程序的数据区域随机布局，数据区域包括：代码、栈、堆。随机的放置这些区域让代码攻击行为很难精确预测特定代码的内存地址并使用它们。

【Data Execution Prevention(DEP)，数据执行保护】

DEP技术会阻止执行非执行数据区域中的代码。在一些攻击中，一些非执行数据区域中的数据被恶意覆写为代码，执行权也被转移到那里。但有了DEP后，这些 恶意代码将无法执行。

*1、指针声明与初始化*

【不正确的指针声明】

int* ptr1, ptr2;

ptr1是指针，但ptr2只是一个整型变量。

正确声明方法：int *ptr1, *ptr2; /* 更好的做法是每行仅声明一个变量 */

下面做法存在同样的问题：

#define PINT int*

PINT ptr1, ptr2;

用typedef就没有问题了：

typedef int* PINT;

PINT ptr1, ptr2;

【使用指针前未初始化】

使用前未做初始化的指针，常称作野指针（wild pointer)：

int *pi;

…

printf(“%d\n”,*pi);

【处理未初始化的指针】

指针脸上没有写自己是否做过初始化^_^。通常有三种方法用于对付未初始化的指针：

– 总是将指针初始化为NULL；

– 使用assert函数

– 使用第三方工具


*2**、指针使用问题*


缓冲区溢出(Buffer overflow)可能由以下原因导致：

– 访问数组元素的时候没有检查下标值

– 做数组指针相关运算时不够谨慎

– 用gets之类的函数从标准输入读取字符串

– 使用strcpy和strcat不当

【测试NULL】

调用malloc后，总是检查返回值是否为NULL。

【误用解引用操作符】

int num;

int *pi;

*pi = &num

【悬挂指针】

【访问数组越界】

char firstName[8] = "1234567";

char middleName[8] = "1234567";

char lastName[8] = "1234567";

middleName[-2] = 'X';

middleName[0] = 'X';

middleName[10] = 'X';

【错误计算数组大小】

当将数组作为参数传递给函数时，务必将函数的Size一并传入，这个Size信息将避免数组访问越界。

【误用sizeof操作符】

int buffer[20];

int *pbuffer = buffer;

for(int i=0; i<sizeof(buffer); i++) {

*(pbuffer++) = 0;

}

sizeof(buffer)=>sizeof(buffer)/sizeof(buffer[0]);

【总是匹配指针类型】

【有界指针(bounded pointer)】

【字符串安全问题】

对strcpy和strcat使用不当，会导致缓冲区溢出。

在C11标准中加入了strcat_s和strcpy_s函数，如果发生缓冲区溢出，它们会返回错误。

【函数指针问题】

不要将函数赋值给签名不同的函数指针，这很可能将导致未定义行为发生。


*3、内存释放问题*

【两次free】

【清除敏感数据】

一个良好的实践是覆写哪些不再需要的敏感数据。

char *name = (char*)malloc(…);

…

memset(name,0,sizeof(name));

free(name);

*4、使用静态分析工具*

比如Gcc -Wall等。

**第八章 其他零碎的知识点**

*1、指针转型*

指针转型有几个原因：

– 访问特定目的的地址

– 分配一个地址代表一个端口

– 决定机器的endianess

【访问特定的地址】

#define VIDEO_BASE 0xB8000

int *video = (int *) VIDEO_BASE;

*video = 'A';

【访问一个端口】

#define PORT 0xB0000000

unsigned int volatile * const port = (unsigned int *) PORT;

*port = 0x0BF4; // write to the port

value = *port; // read from the port

【判断机器的endianess】

int num = 0×12345678;

char* pc = (char*) #

for (int i = 0; i < 4; i++) {

printf("%p: %02x \n", pc, (unsigned char) *pc++);

}

*2、Aliasing、Strict Aliasing和restrict关键字*

两个指针同时指向一块相同的内存地址，这两个指针被称为aliasing。

int num = 5;

int* p1 = #

int* p2 = #

aliasing的使用对编译器生成的代码强加了限制。

如果两个指针引用相同位置，每个指针都可以修改这块地址。当编译器生成读写这块内存的代码时，不总是可以通过将值存储在寄存器中这种办法来优化代 码。对每次引用，将强制使用机器级别的低效load和store操作。

Strict Aliasing：另外一种形式的aliasing。strict aliasing不允许不同类型的指针指向同一块内存区域。下面代码：一个指向整型的指针alias了一个指向float类型的指针了，这违反了Strict Aliasing的规则。

float number = 3.25f;

unsigned int *ptrValue = (unsigned int *)&number;

unsigned int result = (*ptrValue & 0×80000000) == 0;

如果仅仅是符号标志和修饰符不同，是不会影响strict aliasing的，下面的语句是符合Strict aliasing规则的：

int num;

const int *ptr1 = #

int *ptr2 = #

int volatile ptr3 = #

有些场合，相同数据的不同表示是很有用处的，下面一些方法可以避免与Strict aliasing规则冲突：

– 使用Union: 多个数据类型的联合体可以规避strict aliasing

– 关闭strict aliasing ：利用编译器提供的开关将strict aliasing关闭（不建议这么做哦），

比如Gcc提供的一些开关：

-fno-strict-aliasing 关闭strict aliasing

-fstrict-aliasing 打开strict aliasing

-Wstrict-aliasing 针对strict aliasing相关问题给出警告

– 使用char pointer：char pointer可以alias任何对象。

【使用Union实现一个值的多种方式表示】


typedef union _conversion {

float fNum;

unsigned int uiNum;

} Conversion;

int isPositive1(float number) {

Conversion conversion = { .fNum =number};

return (conversion.uiNum & 0×80000000) == 0;

}

由于没有指针，所以不存在违反Strict aliasing的问题。

【Strict Aliasing】

编译器假设多个不同类型的指针不会引用到同一个数据对象，这样在strict aliasing的规则下，编译器才能够实施一些优化。如果假设不成立，那很可能发生意料之外的结果。

即使是两个拥有相同字段，但名字不同的结构体，其对应的指针也不能引用同一个对象。但通过typedef结构体类型指针与原类型指针可以引用同一个数据对象。

typedef struct _person {

char* firstName;

char* lastName;

unsigned int age;

} Person;

typedef Person Employee;

Person* person;

Employee* employee;

【使用restrict关键字】

使用restrict关键字，意即告诉编译器这个指针没有被alias，这样编译器将可以进行优化，生成更为高效的代码。通常的优化方法是缓存这个指针。

不过即便使用了restrict关键字，对编译器来说也只是一个建议，编译器可自行选择是否进行优化。

建议新代码中都要使用restrict关键字。

void add(int size, double * restrict arr1, const double * restrict arr2) {

for (int i = 0; i < size; i++) {

arr1[i] += arr2[i];

}

}

double vector1[] = {1.1, 2.2, 3.3, 4.4};

double vector2[] = {1.1, 2.2, 3.3, 4.4};

add(4,vector1,vector2);

以上是add函数的正确用法。

double vector1[] = {1.1, 2.2, 3.3, 4.4};

double *vector3 = vector1;

add(4,vector1,vector3);

add(4,vector1,vector1);

这个例子中vector3与vector1指向同一份数据，也许add可以正常工作，但这个函数的调用结果并不那么可靠。

标准C库中有多个函数使用了restrict关键字，比如void *memcpy(void * restrict s1, const void * restrict s2, size_t n)等。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

真巧，正好想看这本书

感觉第六章最后数据结构部分作者的二叉查找树插入节点insertTree函数实现有错误