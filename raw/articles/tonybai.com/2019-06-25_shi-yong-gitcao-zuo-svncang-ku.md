---
title: 使用git操作svn仓库
url: https://tonybai.com/2019/06/25/using-git-with-svn-repo/
published: '2019-06-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用git操作svn仓库

如今，虽然[Git](https://git-scm.com/)已经大行其道，但是仍有很多IT公司和组织依旧在使用集中式的版本控制系统[subversion](https://subversion.apache.org/)，尤其是一些传统软件公司，他们倾向于集中式的联网开发。如果你是一个[Git](https://tonybai.com/tag/git) fans，并且你要是遇到代码仓库依旧是使用[subversion](https://tonybai.com/tag/svn)进行版本控制的情况，你又该如何施展呢？

其实git很早就[支持与subversion repo的互操作](https://git-scm.com/docs/git-svn)了，2011年我就曾写过一篇[《小试git-svn》](https://tonybai.com/2011/01/20/try-git-svn/)的博文，也正是那一年，我第一次使用git操作subversion仓库。

[《小试git-svn》](https://tonybai.com/2011/01/20/try-git-svn/)一文仅是通过文字性描述简要说明了git操作svn repo的基本命令和功能，并未结合实际例子，也缺少直观的图片展示，并且未涉及branch和tag的操作。这里打算再写一篇关于使用git操作svn仓库的文章，相比于前者，我期望该文能更为系统并结合demo图文并茂的把使用git操作svn仓库这个事情讲的更形象和透彻一些。

## 一. 使用git操作svn repo的基本工作流

使用git操作svn repo的多数场景是已经存在一个svn repo，git fans想用git命令与之交互。下图展示了使用git操作这样的svn repo的基本工作流：

![img{512x368}](../../assets/d02901d633c7c29b.png)


下面我们就用一个demo来详细地说明一下这个基本工作流。

### 1. 建立一个svn demo库

自己搭建一个svn server还是比较费力的，我们选择一个在线的svn代码托管SaaS服务：svnbucket.com。我们在svnbucket.com上注册账号并创建一个svn repo：**test-git-svn**，该repo采用标准的项目布局(trunk/branches/tags)：

![img{512x368}](../../assets/ecd336b82e9c52c8.png)


接下来我们就开始git操作svn repo的过程！

### 2. 通过git首次获取svn仓库

git是分布式版本管理工具，无论是git repo还是svn repo，如果要用git操作，那么首先需要获取到repo的所有数据。git提供了svn子命令来操作远程的svn repo库，我们看一下首次获取svn repo信息的过程：

```
$git svn clone svn://svnbucket.com/bigwhite/test-git-svn/
Initialized empty Git repository in /Users/tony/Test/git-svn-test/test-git-svn/.git/
W: +empty_dir: branches
W: +empty_dir: tags
W: +empty_dir: trunk
r1 = 8cfdc2f6059ff06f53c83d64518dcba146722c04 (refs/remotes/git-svn)
Checked out HEAD:
svn://svnbucket.com/bigwhite/test-git-svn r1
creating empty directory: branches
creating empty directory: tags
creating empty directory: trunk
$tree ./test-git-svn
./test-git-svn
├── branches
├── tags
└── trunk
3 directories, 0 files
$cd test-git-svn
$git branch -a
* master
remotes/git-svn
```


可以看到：我们通过git svn clone(注意：不是git clone)将远程server上的svn repo下载到了本地，后续我们就可以在本地host上快乐地使用git管理本地的代码了。

### 3. 从svn repo中同步最新的代码变更

接下来，远程的svn仓库经常会发生了变更，某开发人员向svn仓库提交了一些initial code，比如在trunk下建立git-svn-demo目录，并创建go.mod和main.go：

```
//在svn repo中的trunk/git-svn-demo目录下：
$cat main.go
package main
import "fmt"
func main() {
fmt.Println("git-svn-demo initial version")
}
$cat go.mod
module github.com/bigwhite/git-svn-demo
```


如果我们本地使用svn工具，我们只需在联网的情况下通过svn update命令即可将远程svn repo的最新改动同步到本地working copy中。但在git下，我们不能像git repo同步那样使用git pull来同步，而是需要使用git svn rebase来获取svn repo中的最新更新，并rebase我们的工作目录(working copy)：

```
$git svn rebase
A trunk/git-svn-demo/go.mod
A trunk/git-svn-demo/main.go
r2 = f826b74bfff2799deaafbca81354c38e0862509c (refs/remotes/git-svn)
First, rewinding head to replay your work on top of it...
Fast-forwarded master to refs/remotes/git-svn.
$tree .
.
├── branches
├── tags
└── trunk
└── git-svn-demo
├── go.mod
└── main.go
4 directories, 2 files
```


git svn rebase子命令会根据svn上的revision创建对应的commit，这一命令几乎等效于”svn update”，同样也可能会存在远程svn repo中的代码与git repo冲突的可能性，解决冲突的方法在[《小试git-svn》](https://tonybai.com/2011/01/20/try-git-svn/)中已经做了描述，这里就不赘述了。

### 4. 将代码更新推送到远程svn repo

在这种模式下，本地开发已经完全变成了基于git的开发模式，开发者可以自由地发挥git的各种优势了，再也不用担心本地代码没有版本控制而出现各种“误删除”、“意外覆盖”的情况了。开发测试并提交(只需普通git commit)到local git repo后，最终还是要将这些commit推送到远程的svn repo中。这里我们不能用push，而要用git svn dcommit：

```
// 本地git repo中更新后的main.go
$cat main.go
package main
import "fmt"
func main() {
fmt.Println("git-svn-demo: git-svn dcommit v0")
}
```


先提交到git本地的仓库:

```
$git commit -m"[git svn]: first commit" .
[master be36a7f] [git svn]: first commit
1 file changed, 1 insertion(+), 1 deletion(-)
```


然后再“推送”到远程的svn 仓库：

```
$git svn dcommit
Committing to svn://svnbucket.com/bigwhite/test-git-svn ...
M trunk/git-svn-demo/main.go
Committed r3
M trunk/git-svn-demo/main.go
r3 = e35efbe999cd035b2d5d67886c9a786ef86c681e (refs/remotes/git-svn)
No changes between be36a7f1164b73a994f28ee3b0e0bb711b5ba2ff and refs/remotes/git-svn
Resetting to the latest refs/remotes/git-svn
```


dcommit会将git repo当前branch与远程svn repo中的差异的git commit都提交到svn repo，并为每个git commit生成一个对应的svn revision。这和”git push”很类似。

我们再来本地做两次git commit：

```
$git commit -m"[git svn]: commit #2" .
$git commit -m"[git svn]: commit #3" .
```


dcommit到svn repo：

```
$git svn dcommit
Committing to svn://svnbucket.com/bigwhite/test-git-svn ...
M trunk/git-svn-demo/main.go
Committed r4
M trunk/git-svn-demo/main.go
r4 = c997db60e3d82c97ce8da23b308d611005740844 (refs/remotes/git-svn)
M trunk/git-svn-demo/main.go
Committed r5
M trunk/git-svn-demo/main.go
r5 = 3b6215a3e5ae0659743e1e8063f842448c19147c (refs/remotes/git-svn)
No changes between ee0df22b9f41882518a7c7b975c38924a9422395 and refs/remotes/git-svn
Resetting to the latest refs/remotes/git-svn
```


我们看到git svn为每个commit生成一个对应的svn revision(svn版本号），这里是r4、r5。

## 二. 利用git branch的优势

和svn建立branch的“重量级”操作（文件copy）相比，git的branch创建和切换可谓“超轻量级”。因此在日常使用git中，多数开发者都会充分发挥git branch的优势，通过在不同branch上的操作、分支的merge等来减少对master的并发修改带来冲突的影响。

我们经常使用feature branch或bugfix branch。以feature branch为例，在feature branch上一般会有多个commit。但在merge到master分支时，我们可以选择多种merge策略，或是fast forward，或是多个commit自动合并为一个commit，又或git merge支持–squash策略（即只merge代码到本地Working copy，不commit到git repo，后续可作为一个commit手工提交到git repo）。

我个人在用git操作svn repo库时，在git本地开发中，更倾向于使用git merge –squash的方法，因为在feature branch上，我更喜欢频繁的小变更的提交，导致commit很多。如果这些commit都dcommit到svn库，可能让svn commit history项目过多，有些commit甚至没有比较完善的意义。

我们在上面的demo上演示一下这个过程。

在本地建立新分支：feature-branch-1：

```
$git checkout -b feature-branch-1
Switched to a new branch 'feature-branch-1'
```


在feature-branch-1做两次修改并commit：

```
$git commit -m"add foo" .
[feature-branch-1 d12ca00] add foo
1 file changed, 4 insertions(+)
$git commit -m"add bar" .
[feature-branch-1 160e5ed] add bar
1 file changed, 4 insertions(+)
```


回到master分支，merge feature分支的修改，并合并为本地的一次commit：

```
$git checkout master
Switched to branch 'master'
$git merge feature-branch-1 --squash
Updating 3b6215a..160e5ed
Fast-forward
Squash commit -- not updating HEAD
trunk/git-svn-demo/main.go | 8 ++++++++
1 file changed, 8 insertions(+)
$git commit -m"[git svn]: add foo and bar function" .
[master fe8f153] add foo and bar function
1 file changed, 8 insertions(+)
```


接下来，将这次合并的commit同步到svn repo上：

```
$git svn dcommit
Committing to svn://svnbucket.com/bigwhite/test-git-svn ...
M trunk/git-svn-demo/main.go
Committed r6
M trunk/git-svn-demo/main.go
r6 = 37bbfbdb99cb7331057a05b72dc55b3faf55b645 (refs/remotes/git-svn)
No changes between fe8f153cac62e027ca068fdd55c2bdaa8751aaf8 and refs/remotes/git-svn
Resetting to the latest refs/remotes/git-svn
```


## 三. 通过git为svn库建立branch和打tag

通过git为svn repo建立branch和tag这类操作其实并没有体现出git的优势，因此日常开发人员一般会用svn命令直接操作svn repo，而不是用git svn子命令。但这里我们仍然要介绍一下通过git为svn repo建立branch和tag的方法。

我们先来看看创建branch：

```
$git svn branch feature-branch-1-from-git
Multiple branch paths defined for Subversion repository.
You must specify where you want to create the branch with the --destination argument.
```


我们看到git svn branch命令出错：让我们指定–destination参数，那我们就再来一遍：

```
$git svn branch feature-branch-1-from-git --destination=branches
Unknown branch destination branches
```


依旧报错！似乎git不认识“branches”这个存放branch的目录！要想解决这个问题，我们需要对.git/config中的配置做些变更，添加最后两行：

```
$cat .git/config
[core]
repositoryformatversion = 0
filemode = true
bare = false
logallrefupdates = true
ignorecase = true
precomposeunicode = true
[svn-remote "svn"]
url = svn://svnbucket.com/bigwhite/test-git-svn
fetch = :refs/remotes/git-svn
branches = branches/*:refs/remotes/*
tags = tags/*:refs/remotes/*
```


原先的.git/config中并没有设置branhes和tags的入口。我们再来试一下建立branch：

```
git svn --username=bigwhite branch feature-branch-1-from-git
Copying svn://svnbucket.com/bigwhite/test-git-svn at r8 to svn://svnbucket.com/bigwhite/test-git-svn/branches/feature-branch-1-from-git...
Authorization failed: Unable to connect to a repository at URL 'svn://svnbucket.com/bigwhite/test-git-svn': Can't get password at /usr/local/Cellar/git/2.12.2/libexec/git-core/git-svn line 1200.
```


仍然报错！不过这个错误应该是[git（我使用的是2.12.2版本）的一个bug](https://github.com/git/git/commit/e0688e9b28f2c5ff711460ee8b62077be5df2360)，我们用try-run方式运行的结果却是一切ok的：

```
$git svn --username=bigwhite -n branch feature-branch-1-from-git
Copying svn://svnbucket.com/bigwhite/test-git-svn at r8 to svn://svnbucket.com/bigwhite/test-git-svn/branches/feature-branch-1-from-git...
```


打tag的方式与建立 branch的方式类似：

```
$git svn tag v1.0.0 -n -m "[git svn]: tag v1.0.0" --destination=tags
Copying svn://svnbucket.com/bigwhite/test-git-svn at r5 to svn://svnbucket.com/bigwhite/test-git-svn/tags/v1.0.0...
```


## 四. 小结

git svn子命令是git fans操作svn repo的利器。由于git svn clone svn_repo后的repo就是一个标准的本地git repo，因此我们还可以为该git repo建立remote upstream repo，这样就可以在local git repo、remote git repo以及remote svn repo三者之间进行代码变更的同步了，当然这种场景操作还是蛮复杂的，也相对少见。

个人建议，无论个人还是组织，即便使用svn中心repo，在本地也尽量用git来进行源码版本管理，并通过git svn与中心svn repo互操作。

我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网上线了，感谢小伙伴们学习支持！

[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/

smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

我的联系方式：

微博：https://weibo.com/bigwhite20xx

微信公众号：iamtonybai

博客：tonybai.com

github: https://github.com/bigwhite

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2019, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

找到的为数不多的讲解git svn应用的文章，感谢

不错的文章！就是在git svn clone …时，应该加上 -s 参数（svn采用标准布局时），这样就应该不会出现git svn branch 等会出错的情况了！