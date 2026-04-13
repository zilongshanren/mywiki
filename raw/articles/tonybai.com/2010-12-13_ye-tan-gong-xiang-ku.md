---
title: 也谈共享库
url: https://tonybai.com/2010/12/13/also-talk-about-shared-library/
published: '2010-12-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 也谈共享库

近两天一直在考量产品安装包改进的事宜。说实话，我们的安装包做得不够"专业"，不仅没有按照各个平台的标准安装包形式(比如redhat的rpm，debian的deb或[solaris](http://tonybai.com/2009/09/10/something-about-installing-solaris-10/)上的pkg包)制作，而且安装包在生产环境中还需要再进行一次链接才能得到最终的可执行程序。这样一来，每次制作安装包都很费时费力(虽然有自动打包脚本)，安装包的"体积"也很是庞大，因为包中要包含所有.o目标文件和一部分自有库以及第三方库的.a文件。

究竟为何还需要在生产环境中重新链接一次，此问题年头已久，之前无人深究，现在也就没有了现成的答案，这次花了些时间查了一下，发现居然是有关共享库的一个问题。关于共享库，我平时接触的不多，工作中更多愿意使用静态库进行静态链接，这样一来实际上我对共享库的了解也不够深刻。

众所周知，静态链接和动态链接各有不足，也各有千秋：

采用静态链接，最终可执行文件的Size会比较大，因为你在可执行文件中包含了一份程序所依赖的库中的符号的代码copy(注意：不是整个静态库的copy)。不过也恰是由于这点，可执行程序被部署到运行环境下后就简单多了，它运行时不需要再依赖任何其他库了，是典型的自我满足型。

而动态链接则与静态链接恰恰相反，由于编译时仅仅是记录了其运行所依赖的共享库的名字而并未真正包含一份库的copy，所以这样的可执行文件的Size都较小，但在运行环境中我们需要先进行一番配置以让链接器能找到可执行程序所依赖的共享库。

但实际工作中，完全的采用静态链接有时是会遇到麻烦的。因为很多OS在默认安装时是不带开发包的，也就是说像libc、libpthread等系统库只提供了共享库版本(如/lib下提供了libc的共享库libc.so.6)，其静态库版本是需要自行下载、编译和安装的(如libc的静态库libc.a在安装后是放在/usr/lib下面的)。所以多数情况下，我们是将两种链接方式混合在一起使用的，至少像libc这样的系统库多是采用动态链接的。

共享库的制作方法很简单，用下面两行代码我们就可以得到一个名为libfoo.so的共享库：

gcc -fPIC -c libfoo.c -o libfoo.o

gcc -shared -o libfoo.so libfoo.o

不过不知道大家是否留意过：在/lib和/usr/lib等集中放置共享库的目录下，你总是会看到诸如下面的情况：

2010-12-10 12:28 libfoo.so -> libfoo.so.0.0.0*

2010-12-10 12:28 libfoo.so.0 -> libfoo.so.0.0.0*

2010-12-10 12:28 libfoo.so.0.0.0*

关于libfoo.so居然有三个文件入口，其中libfoo.so.0.0.0是真正的共享库文件，而其他两个文件入口则是指向libfoo.so.0.0.0的符号链接。为何会出现这个情况呢？这与共享库的命名[惯例](http://tonybai.com/2010/11/15/keep-legacy-conventions-selectively/)和版本管理不无关系。

共享库的惯例中每个共享库都有多个名字属性，包括real name、soname和linker name：

real name – 指的是实际包含共享库代码的那个文件的名字(如上面例子中的libfoo.so.0.0.0)，也是在共享库编译命令行中-o后面的那个参数;

soname – 是shared object name的缩写，也是这三个名字中最重要的一个，无论是在编译阶段还是在运行阶段，系统链接器都是通过共享库的soname(如上面例子中的libfoo.so.0)来唯一识别共享库的。即使real name相同但soname不同，也会被链接器认为是两个不同的库。共享库的soname可在编译期间通过传给链接器的参数来指定，如上例中我们可以通过"gcc -shared -Wl,-soname -Wl,libfoo.so.0 -o libfoo.so.0.0.0 libfoo.o"来指定libfoo.so.0.0.0的soname为libfoo.so.0(在solaris上的命令为"gcc -shared -Wl,-h -Wl,libfoo.so.0 -o libfoo.so.0.0.0 libfoo.o")。ldconfig -n directory_with_shared_libraries命令会根据共享库的soname自动生成一个名为soname的符号链接指向real name文件，当然你也可以通过ln命令自己来创建这个符号链接。另外在linux下我们可通过readelf -d查看共享库的soname(在solaris下可使用dump -Lvp查看)，ldd输出的ELF文件依赖的共享库列表中显示的也是共享库的soname及所在路径。

linker name – 是编译阶段提供给编译器的名字(如上面例子中的libfoo.so)。如果你构建的共享库的real name是类似于上例中libfoo.so.0.0.0那样的带有版本号，那么你在编译器命令中直接使用-L path -lfoo是无法让链接器找到对应的共享库文件的，除非你为libfoo.so.0.0.0提供了一个linker name(如libfoo.so，一个指向libfoo.so.0.0.0的符号链接)。linker name一般在共享库安装时手工创建。

了解了共享库的名称惯例后，我们考虑如何使用这些共享库。使用共享库分为两个阶段，第一个阶段是可执行文件构建阶段。构建阶段我们需要为编译器(实为链接器)提供可执行程序依赖的共享库的位置信息：

如果依赖的共享库放置在链接器搜索的默认目录下(linux下一般依次为/lib和/usr/lib; solaris下依次为/usr/ccs/lib，/lib和/usr/lib)，你可以直接使用-l指定共享库的linker name即可；

如果依赖的共享库在非默认路径下，可使用-L来告知位置，比如gcc -o fooapp fooapp.c -L private_shared_lib_dir -lfoo，与默认目录相比，-L指定的目录优先级更高，另外注意：这里-L的位置信息并不记录在fooapp文件中，也不会对fooapp的执行产生影响；

在Solaris上，通过配置LD_LIBRARY_PATH也可以为编译器指定共享库路径，且其优先级比-L指定的路径更高，不过在Linux上LD_LIBRARY_PATH在编译阶段似乎不起作用。

运行时阶段，链接器同样要确定可执行文件依赖的共享库的位置和版本，不过与编译构造阶段不同，运行时的链接器按如下顺序搜索共享库：

-rpath

链接器优先在可执行文件中记录的rpath路径下搜索。rpath是在编译时传给链接器的路径参数：

linux平台下可使用：gcc -o fooapp fooapp.c -Wl,-rpath -Wl,fooapp_rpath -L foo_so_path -lfoo

solaris下可用：gcc -o fooapp fooapp.c -R fooapp_rpath -L foo_so_path -lfoo

多个路径可用冒号分割。编译成功后，这些信息会被记录在最终文件的RPATH节中，在运行时链接器读取RPATH节并搜索其值对应的目录。ldd 显示的是运行时应用依赖的库及其在运行环境下的确定路径，例如ldd fooapp的结果为：libfoo.so.0 => fooapp_rpath/libfoo.so.0 (0×00458000)

LD_LIBRARY_PATH

如果fooapp_rpath实际并不存在，则链接器会尝试在LD_LIBRARY_PATH配置的路径中查找依赖的共享库。

ldconfig配置的缓存中的路径

如果在rpath和LD_LIBRARY_PATH中依旧没有搜索到libfoo.so，那么链接器将尝试在ldconfig配置缓存中查找。linux平台上使用ldconfig配置搜索路径的方法如下：在/etc/ld.so.conf.d下增加一个自定义的链接器搜索路径配置文件，执行ldconfig更新缓存后生效。

系统默认路径

链接器最后将在默认路径下查找相关共享库，linux和solaris下均为/lib和/usr/lib。

如果在以上路径下依然没有找到libfoo.so，那么fooapp运行将出错。

好了，到目前为止，前面提到安装包的问题的原因也可以解释清楚了，问题就在于使用了-rpath但却没有在生产环境下进行共享库的配置。一旦安装包制作环境下记录到-rpath中的路径在生产环境下无法找到，且生产环境下没有将相关库的路径配置到链接器搜索的路径下，那么安装后的可执行文件执行时就会出错。解决方法有多种，这里就不赘述了。

© 2010, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

LD_LIBRARY_PATH 仅仅是运行是参数，编译时是不起作用的