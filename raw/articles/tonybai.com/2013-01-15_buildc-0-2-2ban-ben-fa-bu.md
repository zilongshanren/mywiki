---
title: buildc 0.2.2版本发布
url: https://tonybai.com/2013/01/15/buildc-0-2-2-release/
published: '2013-01-15'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# buildc 0.2.2版本发布

随着[buildc](http://code.google.com/p/buildc)在项目中的深入使用，开发和测试人员都提出了不少良好意见，让我们有些应接不暇了，这次的版本更新也是为了满足这些意见和建议。 由于忙于应对这些眼前的需求，原本0.3.0的改进计划也被推迟了一些。

[buildc 0.2.2](http://buildc.googlecode.com/files/buildc-0.2.2.tar.gz)版本包含了两个主要修正。

* 增加了–ignore-error命令行选项

自从buildc cache相关命令严格区分–cmode=32-bit还是64-bit后，用户在使用过程中出现了一些新情况。比如某开发人员A负责两个子系统 subsys1和subsys2的开发，这两个子系统分别用到了lib1和lib2。subsys1是一个64bit系统，依赖lib1；而 subsys2是一个32bit系统。依赖lib2。这样开发人员A在自己的开发环境下要管理和缓存lib1和lib2。管理lib1时，用到的 是buildc cache update –cmode=64-bit命令，而管理lib2时，用到的是buildc cache update –cmode=32-bit命令。这时如果内部的二进制库服务器上没有lib1的32bit版本或者没有lib2的64bit版本，buildc cache相关命令就会执行失败。为了临时解决这个问题，我们增加了–ignore-error命令行选项，这样即便lib1无32bit版本 或者lib2无64bit版本，buildc cache相关命令执行不会失败，开发人员A开发环境下的subsys1和subsys2的构建也会顺利完成。

关于这个问题，后续期待在buildc 0.3.0版本或后续版本得到更好的解决。

* 增加buildc pack source –component=[src|deps|all]命令

通常情况下，我们是不需要在生产环境下做任何编译操作的。但有些特殊情况下，我们不得不将源码拿到生产环境下进行编译。之前使用buildc进行 源码构建的工程拿到生产环境下进行编译极为不便，因为生产环境下没有buildc环境，也没有依赖库的cache，因此我们的运维人员提出这样的 需求：提供一份可在生产环境下进行编译的source包。为了满足这一需求，我们针对setup工程进行了完善，对buildc的pack命令做 了扩充，使得buildc pack支持source打包。

buildc pack source支持三个component参数：src、deps和all。src意为源码包，包中只包含工程源码；deps是打依赖包，及包中包含的都是 工程依赖的对应平台的第三方库的二进制版本；all则是src和deps的合体，是一个全量的，在目标环境可直接编译的包。

buildc pack source输出的目标包内结构大致如下：

target-package/

– deps/

– lib1/

– 1.1.0/

– x86_64_linux/

– proj_name

– configure

– Make.rules

– Makefile

– ….

前面说过，这个包在目标环境是直接可编译的，你只需执行：

$>./configure

$> make

在制作目标包时，buildc pack source命令就已经将Make.rules中的各种库的依赖信息按照目标包的结构做了调整。执行configure是为了根据目标环境对 Make.rules做最后的调整。

另外源码包仅携带对应目标平台的第三方库的版本，不会将所有平台的版本都带上。当然这样有利有弊。优点在于源码包的size不会很大；缺点在于， 如果生产环境有许多种平台的话，我们需要为每个平台准备一份源码包。

BTW，现在的buildc基本上由我们组的小兄弟wtz1989227一个人维护，包括buildc的[manual](http://code.google.com/p/buildc/wiki/buildc_user_guide)更新，这次的更新也都是他一 个人的工作成果。小声的说一句：wtz1989227接触Python也为时不多，因此代码方面还有较大的改进提高余地。

© 2013, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论