---
title: vim-go更新小记
url: https://tonybai.com/2016/09/08/upgrade-vim-go/
published: '2016-09-08'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# vim-go更新小记

自从上一次配置好Mac上的[Golang Vim开发环境](http://tonybai.com/2014/11/07/golang-development-environment-for-vim/)，基本上就没怎么动过。近两年过去了，[Go已经升级到了1.7版本](http://tonybai.com/2016/06/21/some-changes-in-go-1-7/)，[Vim-go](https://github.com/fatih/vim-go)截至目前也已经演化到了[1.8版本](https://github.com/fatih/vim-go/releases/tag/v1.8)了。社区的积极关注和使用，让Vim-go的作者[Fatih Arslan](https://github.com/fatih)备受鼓舞，于是近一年来，积极为vim-go添加新功能，发布新版本，并编写了vim-go的详细[tutorial](https://github.com/fatih/vim-go-tutorial)。这让我动了更新Vim-go版本的念头，于是就有了本篇内容。

已经记不得当初第一次配置vim-go时，vim-go的版本号是多少了。经过近两年的发展，vim-go已然正式成为Vim下Go开发环境的标准Plugin了。Go从当年的[1.4](http://tonybai.com/2014/11/04/some-changes-in-go-1-4/)升级到1.7，相关工具也跟着一起升级，比如oracle变成了[guru](https://github.com/golang/tools/tree/master/cmd/guru)，名字都换了。支持go的编辑器也逐渐增多并日益成熟，从最初[vim](http://tonybai.com/tag/vim)、[liteIDE](https://github.com/visualfc/liteide)，到后来的[eclipse](http://www.eclipse.org/)、[IntelliJ Idea](https://github.com/go-lang-plugin-org/go-lang-idea-plugin)、[atom](https://atom.io/packages/go-plus)、[sublime text](http://www.sublimetext.com/)以及[vscode](https://github.com/microsoft/vscode-go)对golang都提供了支持。这样一来，无论你之前是哪种IDE的拥趸，你都能找到得心应手的环境走入Golang世界。

我个人一直用vim，sublime text3曾经玩过，没玩熟，卸了。目前机器上还装了一份vscode，感觉在IDE领域中，微软的影响力和成熟度不容小觑，vscode + golang extension从入门门槛来看，还是非常低的。即便vim-go进化到1.8版本，仍然不如vscode安装体验来得方便。当然这不全是vim-go的问题，而是vim的设计哲学所致。

无论是vim-go还是vscode golang plugin，都要依赖golang的周边工具，主要包括[gocode](https://github.com/nsf/gocode)、[goimports](https://github.com/golang/tools/tree/master/cmd/goimports)、[guru](https://github.com/golang/tools/tree/master/cmd/guru)、[godef](https://github.com/rogpeppe/godef)、[golint](https://github.com/golang/lint/golint)、[gometalinter](https://github.com/alecthomas/gometalinter)等。在这方面，vim-go提供了安装依赖工具的方法“:GoInstallBinaries”，或在外部通过：vim -c “GoInstallBinaries” -c “qa”安装（在安装vim-go之后）；而vscode则会自动探测其所依赖的工具是否安装，如果没有安装，会在vscode的下方给出提示，点击提示，会安装相应的工具。

BTW，自从近期golang官网：golang.org不用再翻墙后，go get下载golang.org域名下面的各种工具也简单了许多，大陆的Gopher们再也无需担心go package下载的问题了。

升级vim-go之前，建议先备份好.vimrc文件：

```
cp .vimrc .vimrc.bak.20160908
```


vim-go插件安装由很多方法，在vim-go tutorial中，vim-go作者选择了[vim-plug](https://github.com/junegunn/vim-plug)，而没有用之前的vim插件管理工具[vundle.vim](https://github.com/VundleVim/Vundle.vim)，方法都是大同小异：

下载vim-plug：

```
$curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
% Total % Received % Xferd Average Speed Time Time Time Current
Dload Upload Total Spent Left Speed
100 67682 100 67682 0 0 7020 0 0:00:09 0:00:09 --:--:-- 12576
```


安装vim-go：

在.vimrc中填写如下内容：

```
call plug#begin()
Plug 'fatih/vim-go'
```


然后执行”:PlugInstall”即可。

在安装依赖工具期间，发现mac原生自带的vim(macvim，又叫mvim，安装在/usr/local/bin/mvim)版本还是7.3.xx版本，无法满足一些工具的要求，于是通过brew安装vim(安装在/usr/local/Cellar/vim/7.4.2334/bin/vim)，然后通过/usr/bin/vim的一个符号链接连过去即可。

```
$ll /usr/bin|grep vim
lrwxr-xr-x 1 root wheel 38 9 8 16:21 vim@ -> /usr/local/Cellar/vim/7.4.2334/bin/vim
... ...
```


注意，考虑要安装[neocomplete](https://github.com/Shougo/neocomplete.vim)以支持实时completion（补齐），vim需要有lua支持，因此执行brew install时要带上–with-lua参数：

```
brew install vim --with-lua
```


vim-go升级版安装后，可按照vim-go-tutorial中的步骤，体验一下vim-go的强大，同时对.vimrc进行相关配置，并安装缺失的vim插件，比如neocomplete、[UltiSnips](https://github.com/SirVer/ultisnips)等。我针对vim-go 1.8配置好的.vimrc在[这里](https://github.com/bigwhite/experiments/blob/master/vim_scripts/vimrc-for-vimgo-1.8)可以下载到。

具体细节这里就不提了，如果还有哪些细节不清楚或实验没成功，可以回过头参考我那篇《[Golang开发环境搭建-Vim篇](http://tonybai.com/2014/11/07/golang-development-environment-for-vim/)》。

© 2016, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论