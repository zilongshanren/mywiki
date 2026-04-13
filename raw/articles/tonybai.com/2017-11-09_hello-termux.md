---
title: Hello，Termux
url: https://tonybai.com/2017/11/09/hello-termux/
published: '2017-11-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Hello，Termux

*程序员或多或少都有一颗 Geek(极客)的心^0^。- Tony Bai*

折腾开始。

这一切都源于前不久将手机换成了Xiaomi的[MIX2](https://en.wikipedia.org/wiki/Xiaomi_Mi_MIX_2)。因为青睐开放的系统（相对于水果公司系统的封闭，当然Mac笔记本除外^0^），我长期使用[Android平台](https://en.wikipedia.org/wiki/Android_(operating_system))的手机。但之前被三星Note3手机的“大屏”搞的不是很舒服，这两年一直用5寸及以下的手机，因为单手操作体验良好。MIX2的所谓“全面屏”概念又让我回归到了大屏时代。

除了大屏，现在手机“豪华”的硬件配置也让人惊叹：高通骁龙835，8核，最高主频 2.45GHz；6GB以上的LPDDR4x的双通道大内存，怪不得微软和高通都开始合作生产基于高通ARM处理器的Win10笔记本了，这配置支撑在笔记本上办公+浏览网页绰绰有余。不过对于不怎么玩游戏的我而言，这种配置仅仅用作手机日常功能有些浪费。于是有了“mobile coding”的想法和需求，至少现在是这样想的，冲动也好，伪需求也好，先实现了再说。

## 一、神器Termux，不仅仅是一个terminal emulator

所谓”mobile coding”不仅仅是要通过手机ssh到服务器端进行coding，还要支持在手机上搭建一个dev环境。dev环境这个需求是以往我安装的[ConnectBot](https://github.com/connectbot/connectbot)等ssh client端工具所无法提供的，而其他一些terminal工具，诸如[Terminal Emulator for Android](https://github.com/jackpal/Android-Terminal-Emulator)仅仅提供[一些shell命令](https://github.com/jackpal/Android-Terminal-Emulator/wiki/Android-Shell-Command-Reference)的支持，适合于那些喜爱使用命令行对Android机器进行管理的”administrator”们，但对dev环境的搭建支持有限的。于是神器[Termux](https://termux.com/)登场了。

[Termux](https://github.com/termux/termux-app)是什么？Termux首先是一个Android terminal emulator，可以像那些terminal工具一样，提供基本的shell操作命令；除此之外更为重要的是它不仅仅是一个terminal emulator。Termux提供了一套模拟的[Linux](http://tonybai.com/tag/linux)环境，你可以在**无需root、无需root、无需root**的情况下，像在PC linux环境下一样进行各种Linux操作，包括使用[apt工具](https://en.wikipedia.org/wiki/APT_(Debian))进行安装包管理、定制shell、访问网络、编写源码、编译和运行程序，甚至将手机作为反向代理、负载均衡服务器或是Web服务器，又或是做一些羞羞的hack行为等。

### 1、安装

Termux仅[支持Android 5.0及以上版本](https://github.com/termux/termux-app/issues/6)（估计现在绝大多数android机都满足这一条件）。在国内建议使用[F-Droid](https://f-droid.org/packages/com.termux/)安装Termux（先下载安装F-Droid，再在F-Droid内部搜索Termux，然后点击安装），国内的各种安装助手很少有对这个工具的支持。或是到[apk4fun](https://www.apk4fun.com/apk/74133/)下载Termux的apk包（size非常小）到手机中安装(安装时需要连接着网络)。当前Termux的最新版本为[0.54](https://github.com/termux/termux-app/releases/tag/v0.54)。

在桌面点击安装后的Termux图标，我们就启动了一个Termux应用，见下图：

![img{512x368}](../../assets/5d35296e0cb17cec.jpg)


### 2、Termux初始环境探索

Mix2手机的Android系统使用的是[Android 7.1.1版本](https://www.android.com/phones/)，桌面Launcher用的是[MIUI 9.1](https://en.wikipedia.org/wiki/MIUI)稳定版，默认的shell是[bash](http://tonybai.com/2009/02/27/make-bash-my-default-shell/)。通过Termux，我们可以查看Android 7.1.1.使用的[Linux内核](http://tonybai.com/2012/03/15/linux-kernel-hacking-series-kernel-config-compile-and-install/)版本如下：

```
$uname -a
Linux localhost 4.4.21-perf-g6a9ee37d-06186-g2b2a77b #1 SMP PREEMPT Thu Oct 26 14:55:45 CST 2017 aarch64 Android
```


可以看出[Linux内核](http://tonybai.com/2012/03/15/linux-kernel-hacking-series-kernel-config-compile-and-install/)是4.4.21，采用的CPU arch family是[ARM](https://en.wikipedia.org/wiki/ARM_architecture) [aarch64](https://en.wikipedia.org/wiki/ARM_architecture#AArch64_features)。

我再来看一下Termux提供的常见目录结构：

Home路径：

```
$cd ~/
$pwd
/data/data/com.termux/files/home
//或者通过环境变量HOME获取：
$echo $HOME
/data/data/com.termux/files/home
```


长期使用Linux的朋友可能会发现，这个HOME路径好是奇怪，一般的标准[Linux发行版](https://en.wikipedia.org/wiki/Linux_distribution)，比如[Ubuntu](http://tonybai.com/tag/ubuntu)都是在”/home”下放置用户目录，但termux环境中HOME路径却是一个**奇怪的位置**。在[Termux官方Wiki](https://wiki.termux.com/wiki/Main_Page)中，我们得到的答案是：Termux是一个prefixed system。

这个prefix的含义我理解颇有些类似于我们在使用configure脚本时指定的–prefix参数的含义。我们在执行configure脚本时，如果不显式地给–prefix传入值，那么make install后，包将被install在

标准位置；否则将被install在–prefix值所指定的位置。

prefixed system意味着Termux中所有binaries、libraries、configs都不是放在标准的位置，比如：/usr/bin、/bin、/usr/lib、/etc等下面。Termux expose了一个特殊的环境变量:PREFIX（类似于configure –prefix参数选项)：

```
$echo $PREFIX
/data/data/com.termux/files/usr
$cd $PREFIX
$ls -F
bin/ etc/ include/ lib/ libexec/ share/ tmp/ var/
```


是不是有些似曾相识？但Termux的$PREFIX路径与标准linux的根路径下的目录结构毕竟还[存在差别](https://wiki.termux.com/wiki/Differences_from_Linux)，但有着对应关系，这种对应关系大致是：

```
Termux的$PREFIX/bin <=> 标准Linux环境的 /bin和/usr/bin
Termux的$PREFIX/lib <=> 标准Linux环境的 /lib和/usr/lib
Termux的$PREFIX/var <=> 标准Linux环境的 /var
Termux的$PREFIX/etc <=> 标准Linux环境的 /etc
```


因此，基本可以认为Termux的$PREFIX/就对应于标准Linux的/路径。

### 3、更新源和包管理

Termux的牛逼之处在于它基于debian的[APT包](https://en.wikipedia.org/wiki/APT_(Debian))管理工具进行软件包的安装、管理和卸载，就像我们在Ubuntu下所做的那样，非常方便。

Termux自己[维护了一个源](http://termux.net/)，提供各种专门为termux定制的包：

```
# The main termux repository:
#deb [arch=all,aarch64] http://termux.net stable main
```


同时，[termux-packages项目](https://github.com/termux/termux-packages)为开发者和爱好者提供了构建工具和脚本，通过这些工具和脚本，我们可以将自己需要的软件包编译为可以在termux运行的版本，并补充到Termux的源之中。我大致测试了一下官方这个源还是可用的，虽然初始连接的响应很缓慢。

国内清华大学维护了一个[Termux的镜像源](https://mirror.tuna.tsinghua.edu.cn/help/termux/)，你可以通过编辑 /data/data/com.termux/files/usr/etc/apt/sources.list文件或执行apt edit-sources命令编辑源(在Shell配置中添加export EDITOR=vi后，apt edit-sources才能启动编辑器进行编辑)：

```
# The main termux repository:
#deb [arch=all,aarch64] http://termux.net stable main
deb [arch=all,aarch64] http://mirrors.tuna.tsinghua.edu.cn/termux stable main
```


剩下的操作与Ubuntu上的一模一样，无非apt update后，利用apt install安装你想要的包。目前Termux源中都有哪些包呢？可以通过apt list命令查看：

```
$apt list
Listing... Done
aapt/stable 7.1.2.33-1 aarch64
abduco/stable 0.6 aarch64
abook/stable 0.6.0pre2-1 aarch64
ack-grep/stable 2.18 all
alpine/stable 2.21 aarch64
angband/stable 4.1.0 aarch64
apache2/stable 2.4.29 aarch64
apache2-dev/stable 2.4.29 aarch64
apksigner/stable 0.4 all
apr/stable 1.6.3 aarch64
apr-dev/stable 1.6.3 aarch64
apr-util/stable 1.6.1 aarch64
apr-util-dev/stable 1.6.1 aarch64
apt/stable,now 1.2.12-3 aarch64 [installed]
apt-transport-https/stable 1.2.12-3 aarch64
... ...
zile/stable 2.4.14 aarch64
zip/stable 3.0-1 aarch64
zsh/stable,now 5.4.2-1 aarch64 [installed]
```


查看是否有需要更新的包列表：

```
$apt list --upgradable
```


以安装[golang](http://tonybai.com/tag/go)为例：

```
$apt install golang
....
$go version
go version go1.9.2 android/arm64
```


![img{512x368}](../../assets/24ec77934ad73b0d.jpg)


Termux源中的包似乎更新的很勤奋，[Go 1.9.2](http://tonybai.com/2017/07/14/some-changes-in-go-1-9/)才发布没多久，这里已经是最新版本了，这点值得赞一个！

## 二、开发环境搭建

我的目标是**mobile coding**，需要在Termux上搭建一个dev环境，以[Go](http://tonybai.com/tag/go)环境为例。

### 1、sshd

在搭建和配置阶段，如果直接通过Android上的软键盘操作，即便屏再大，那个体验也是较差的。我们最好通过PC连到termux上去安装和配置，这就需要我们在Termux上搭建一个[sshd server](https://wiki.termux.com/wiki/SSH)。下面是步骤：

```
$apt install openssh
$sshd
```


就这么简单，一个sshd的server就在termux的后台启动起来了。由于Termux没有root权限，无法listen数值小于1024的端口，因此termux上sshd默认的listen端口是8022。另外termux上的sshd server不支持用户名+密码的方式进行登录，只能用免密登录的方式，即将PC上的~/.ssh/id_rsa.pub写入termux上的~/.ssh/authorized_keys文件中。关于免密登录的证书生成方法和导入方式，网上资料已经汗牛充栋，这里就不赘述了。导入PC端的id_rsa.pub后，PC就可以通过下面命令登录termux了：

```
$ssh 10.88.46.79 -p 8022
Welcome to Termux!
Wiki: https://wiki.termux.com
Community forum: https://termux.com/community
IRC channel: #termux on freenode
Gitter chat: https://gitter.im/termux/termux
Mailing list: termux+subscribe@groups.io
Search packages: pkg search <query>
Install a package: pkg install <package>
Upgrade packages: pkg upgrade
Learn more: pkg help
```


其中10.88.46.79是手机的wlan0网卡的IP地址，可以在termux中使用ip addr命令获得:

```
$ip addr show wlan0
34: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 3000
... ...
inet 10.88.46.79/20 brd 10.88.47.255 scope global wlan0
valid_lft forever preferred_lft forever
... ...
```


### 2、定制shell

Termux支持多种[主流Shell](https://wiki.termux.com/wiki/Shells)，默认的Shell是[Bash](http://tonybai.com/tag/bash)。很多开发者喜欢[zsh](https://www.zsh.org/) + [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh)的组合，Termux也是支持的，安装起来也是非常简单的：

```
$ apt install git
$ apt install zsh
$ git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
$ cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
$ chsh zsh
```


与在PC上安装和配置zsh和oh-my-zsh没什么两样，你完全可以按照你在PC上的风格定制zsh的Theme等，我用的就是默认theme，所以也无需做太多变化，顶多定制一下PROMPT(~/.oh-my-zsh/themes/robbyrussell.zsh-theme中的PROMPT变量)的格式^0^。

### 3、安装vim-go

在terminal内进行Go开发，[vim-go](https://github.com/fatih/vim-go)是必备之神器。vim-go以及相关自动补齐、snippet插件安装在不同平台上都是大同小异的，之前写过两篇《[Golang开发环境搭建-Vim篇](http://tonybai.com/2014/11/07/golang-development-environment-for-vim)》和《[vim-go更新小记](http://tonybai.com/2016/09/08/upgrade-vim-go/)》，大家可以参考。

不过这里有一个较为关键的问题，那就是Termux官方源中的vim 8.0缺少了对python和lua的支持：

```
$vim --version|grep py
+cryptv +linebreak -python +viminfo
+cscope +lispindent -python3 +vreplace
$vim --version|grep lua
+dialog_con -lua +rightleft +windows
```


而一些插件又恰需要这些内置的支持，比如[ultisnips](https://github.com/SirVer/ultisnips/issues/707)需要vim自带py支持；[neocomplete](https://github.com/Shougo/neocomplete.vim)又依赖vim的lua支持。这样如果你还想要补齐和snippet特性，你就需要在Termux下面自己编译Vim的源码了（configure时加上对python和lua的支持）。

### 4、中文支持

无论是PC还是Termux使用的都是UTF8的内码格式，但是在安装完vim-go后，我试着用vim编辑一些简单的源码，发现在vim中输入的中文都是乱码。这里通过一个配置解决了该问题：

```
//~/.vimrc
添加一行：
set enc=utf8
```


至于其中的原理，可以参见我N年前写的《[也谈VIM字符集编码设置](http://tonybai.com/2009/09/28/also-talk-about-vim-charset-configuration/)》一文。

## 三、键盘适配

现阶段，写代码还是需要键盘输入的（憧憬未来^0^）。

### 1、软键盘

使用原生自带的默认软键盘在terminal中用vim进行coding，那得多执着啊，尤其是在vim大量使用ESC键的情况下（我都没找到原生键盘中ESC键在哪里:(）。不过Termux倒是很具包容心，为原生软键盘提供了扩展支持：用两个上下音量键协助你输入一些原生键盘上没有或者难于输入的符号，比如（全部的模拟按键列表参见[这里](https://wiki.termux.com/wiki/Touch_Keyboard)）：

```
清理屏幕：用volume down + L 来模拟 ctrl + L
结束前台程序：用volume down + C 来模拟 ctrl + C
ESC：用volume up + E 来模拟
F1-F9: 用volume up + 1 ~ 9 来模拟
```


据网友提示：volume up + Q键可以打开扩展键盘键，包括ESC、CTRL、ALT等，感谢。


这样仅能满足临时的需要，要想更有效率的输入，我们需要[Hacker’s Keyboard](https://github.com/klausw/hackerskeyboard)。顾名思义，Hacker’s Keyboard可以理解为专为Coding(无论出于何种目的)的人准备的。和Termux一样，你可以从[F-droid](https://f-droid.org/packages/org.pocketworkstation.pckeyboard/)安装该工具。启动该app后，app界面上有明确的使用说明，如果依旧不明确，还可以查看这篇图文并茂的文章：《[How to Use Hacker’s Keyboard](https://www.wikihow.com/Use-Hacker%27s-Keyboard)》。默认情况下，横屏时Hacker’s keyboard会使用”Full 5-row layout”，即全键盘，竖屏时，则是4-row layout。你可以通过“系统设置”中的“语言和输入法”配置中对其进行设置，让Hacker’s keyboard无论在横屏还是竖屏都采用全键盘（我们屏幕够大^0^）：

![img{512x368}](../../assets/db551c0e3cb1fc82.jpg)


横屏

![img{512x368}](../../assets/07661b49bf2b0c0b.jpg)


竖屏

Hacker’s Keyboard无法支持中文输入，这点是目前的缺憾，不过我个人写代码时绝少使用中文，该问题忽略不计。

### 2、外接蓝牙键盘

Hacker’s Keyboard虽然一定程度提升了Coding时的输入效率，但也仅是权宜之计，长时间大规模通过软键盘输入依旧不甚可取，外接键盘是必须的。对于手机而言，目前最好的外接连接方式就是蓝牙。蓝牙键盘市面上现在有很多种，我选择了老牌大厂[logitech](https://en.wikipedia.org/wiki/Logitech)的[K480](https://www.logitech.com/en-us/product/multi-device-keyboard-k480)。这款键盘缺点是便携性差点、按键有些硬，但按键大小适中；而那些超便携的蓝牙键盘普遍键帽太小，长时间Coding的体验是个问题。

![img{512x368}](../../assets/6689da7ddd4ace5f.jpg)


Termux对外接键盘的支持也是很好的，除了常规输入，通过键盘组合键Ctrl+Alt与其他字母的组合[实现各种控制功能](https://wiki.termux.com/wiki/Hardware_Keyboard)，比如：

```
ctrl + alt + c => 实现创建一个新的session；
ctrl + alt + 上箭头/下箭头 => 实现切换到上一个/下一个session的窗口；
ctrl + alt + f => 全屏
ctrl + alt +v => 粘贴
ctrl + alt + +/- => 实现窗口字体的放大/缩小
```


不过，外接键盘和Hacker’s keyboard有一个相同的问题，那就是针对Termux无法输入中文。我尝试了百度、搜狗等输入法，无论如何切换（正常在其他应用中，通过【shift + 空格】实现中英文切换）均只是输入英文。

## 四、存储

到目前为止，我们提到的路径都在termux的私有的内部存储(private internal storage)路径下，这类存储的特点是termux应用内部的、私有的，一旦termux被卸载，这些数据也将不复存在。Android下还有另外两种存储类型：shared internal storage和external storage。所谓shared internal storage是手机上所有App可以共享的存储空间，放在这个空间内的数据不会因为App被卸载掉而被删除掉；而外部存储(external storage)主要是指外部插入的SD Card的存储空间。

默认情况下，Termux只支持private internal storage，意味着你要做好数据备份，否则一旦误卸载termux，数据可就都丢失了;数据可以用git进行管理，并sync到云端。

Termux提供了一个名为[termux-setup-storage](https://github.com/termux/termux-packages/blob/master/packages/termux-tools/termux-setup-storage)的工具，可以让你在Termux下访问和使用shared internal storage和external storage；该工具是[termux-tools](https://github.com/termux/termux-packages/tree/master/packages/termux-tools)的一部分，你可以通过apt install termux-tools来安装这些工具。

执行termux-setup-storage(注意：这个命令只能在手机上执行才能弹出授权对话框，通过远程ssh登录后执行没有任何效果)时，手机会弹出一个对话框，让你确认授权：

![img{512x368}](../../assets/1020e2fcda649718.jpg)


一旦授权，termux-setup-storage就会在HOME目录下建立一个storage目录，该目录下的结构如下：

```
➜ /data/data/com.termux/files/home $tree storage
storage
├── dcim -> /storage/emulated/0/DCIM
├── downloads -> /storage/emulated/0/Download
├── movies -> /storage/emulated/0/Movies
├── music -> /storage/emulated/0/Music
├── pictures -> /storage/emulated/0/Pictures
└── shared -> /storage/emulated/0
6 directories, 0 files
```


我们看到在我的termux下，termux-setup-storage在storage下建立了6个符号链接，其中shared指向shared internal storage的根目录，即/storage/emulated/0；其余几个分别指向shared下的若干功能目录，比如：相册、音乐、电影、下载等。我的手机没有插SD卡，可能也不支持（市面上大多数手机都已经不支持了），如果插了一张SD卡，那么termux-setup-storage还会在storage目录下j建立一个符号链接指向在external storage上的一个termux private folder。

现在你就可以把数据放在shared internal storage和external storage上了，当然你也可以在Termux下自由访问shared internal storage上的数据了。

## 五、小结

Termux还设计了支持扩展的Addon机制，支持通过各种Addon来丰富Termux功能，提升其能力，这些算是高级功能，在这篇入门文章里就先不提及了。好了，接下来我就可以开始我的mobile coding了，充分利用碎片时间。后续在使用Termux+k480的过程中如果遇到什么具体的问题，我再来做针对性的解析。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

你好，请问中文支持具体咋弄啊？需要先编译vim吗？可是我编译不过去，找不到.vimrc文件

软键盘情况下，使用中文输入法直接可以输入中文啊。但是hacker’s keyboard无法输入中文；外接硬件蓝牙键盘时无法在termux中输入中文。不知道你所问的中文支持是否是这个意思？

路径是$PREFIX/share/vim

左划长按keyboard会出现快捷键条，把它往左划就能输中文了

SwiftKey 可能是目前唯一一个在 Termux 里面使用外接键盘能输入中文的输入法，但是 SwiftKey 的词库实在是太烂了…而且还记不住用户选的词，太难受了

推荐「手心输入法」，目前最完美的方案（支持蓝牙键盘空格键候选字上屏、支持用数字选择候选字）

注：4 年前（ 2019 年）我在 Google Play Store 给 SwiftKey 评论反馈了上述问题，然而 4 年过去了（现在是 2023 年）依旧没有改善，大厂的产品就是如此的脸皮厚和不好用

手动点赞！

一个新的方法可以使用任意的中文输入法，有点曲线救国

一个新的方法可以使用任意的中文输入法，有点曲线救国 LOL ：在 Termux 里面运行 openssh 的 sshd，再使用 Termius ssh 连接到 127.0.0.1:8022，这样子在 Termius 里面就能使用任意的中文输入法了（包括搜狗、百度等），需要注意的是要先在 Termius `Settings` 里面启用 `Experimental Keyboard Support(Voice input and CJK layout support)` 否则在某些 Android 里面只能使用 `安全键盘` 也就无法输入中文了。

注：同时测试了 Termius 的同类软件 JuiceSSH，发现只有当禁用系统的 `安全键盘` 才能使用除了 `安全键盘` 之外的其他输入法，但违背了安全原则（应该没人想让 搜狗、百度 之类的输入法知道密码的吧 LOL）所以不建议，而且 JuiceSSH 并没有 Termius 上类似 `Experimental Keyboard Support` 的选项

用这个方法还能同时避开 Termux 里面中文显示得很扁的问题，算是一个意外惊喜～

注：等待了那么多年之后，我已经对 SwiftKey 输入法完全不抱任何希望了，最近 SwiftKey 更新的功能主要是 AI 相关的，反而最能提高用户体验的基础功能（例如 空格键 候选字 直接上屏、用户输入的自定义词添加到词库并且优先级更高 等等）是一个都没更新，我只能安慰自己「大公司不当人也不是第一天了」

注：Termux 本身的开发者对「是否支持中文输入」或者「中文文字显示得很扁」等问题也完全不关心，也算是另外一种傲慢了，我看到 Termux GitHub 上相关的 issue 要么被标记「不解决」要么已经 close 掉了

更正一下，Termux 现在支持使用中文输入法了，方法: 在 Termux 的配置文件 `~/.termux/termux.properties` 里面添加 `enforce-char-based-input=true`（或者把这一行最前面的 `# ` 注释去掉），参考 GitHub issue https://github.com/termux/termux-app/issues/1839

手动点赞！

太棒了！！！

大赞博主！

一直想这么干，终于找到门路了

如何使用root，输入SU之后，termux能用的命令全都失效了，变成了普通的终端

termux的初衷就是无需root权限的linux环境模拟。关于root的问题还是参考官方FAQ吧：

https://wiki.termux.com/wiki/FAQ

如果是想获得管理员权限的话可以用tsu命令替换su命令,原来的命令都还能执行. pkg install tsu 就可以,需要手机root,但其实只要你装了oh-my-zsh,会在安装过程中自动获得storage权限,很多目录都可以操作,如果用tsu去改一些高权限的目录文件的话,我觉得非常作死,不如租服务器折腾,主力机还是别这么玩了.

(ps.我编辑了三次,每次都忘了划那个验证条…..然后编辑的内容就全没了,痛苦

那个防止垃圾评论的plugin的确体验较差，不过我的wordpress版本较低，还懒得升级，好的防垃圾评论的插件我还用不了，无奈啊, sorry了。

先将QQ输入法切换到中文，然后连接蓝牙键盘，可输入中文。

实际测试并不能用 QQ 拼音输入法在 Termux 里面使用蓝牙键盘直接输入中文，只能在 Termux 的 Text Input View 里面输入中文