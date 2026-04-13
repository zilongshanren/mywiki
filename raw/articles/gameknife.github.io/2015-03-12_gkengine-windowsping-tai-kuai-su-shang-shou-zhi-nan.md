---
title: gkENGINE windows平台快速上手指南
url: http://gameknife.github.io/tech/2015/03/12/windows-startup/
published: '2015-03-12'
source_blog: gameKnife
source_site: http://gameknife.github.io/
category: graphics
fetched: '2026-04-13'
---

# gkENGINE windows平台快速上手指南

12 Mar 2015windows平台快速部署分为，部署，编译，运行，打包四个步骤。

### 部署

*部署开发平台，安装和准备平台所需的第三方依赖库以及测试资源*

- 从github / codeplex pull最新版本
**github GIT**[https://github.com/gameknife/gkEngine.git](https://github.com/gameknife/gkEngine.git) -
运行 init_engine_res.bat ，建立引擎目录环境

- 从资源服务器获取depends.7z第三方依赖库和media.7z资源库
**depends.7z**[http://pan.baidu.com/s/1i38C5ud](http://pan.baidu.com/s/1i38C5ud)**media.7z**[http://pan.baidu.com/s/1qWK90Jy](http://pan.baidu.com/s/1qWK90Jy)分别放置于code/thirdparty下和exec/media下

-
运行hand_make_env.bat，部署第三方依赖环境

- 运行hand_make_resource.bat，部署和编译资源

### 编译

*编译gkENGINE*

-
通过code/engine/solution/gkENGINE_vc10.sln打开工程

-
选择Develop Win32编译配置 -
Build Solution

- 等待编译结束，如果全部工程编译成功，则编译完成，否则请到codeplex上提交issue

### 运行

*测试运行*

-
使用exec/bin32/gkLauncher.exe打开，自动进入默认的测试用例模块。

-
模块的配置可以在exec/media/config/startup.cfg中详细配置

-
在测试用例模块中，方向键左右切换主项目类型，上下键切换当前项目，回车键执行测试用例

-
使用exec/bin32/gkStudio.exe打开编辑器，可以进行场景编辑。编辑器代码位于code/editor/gkstudio中


### 打包

*打包为二次运行包，隐藏开发资源，剔除不必要文件，以供发布运行*

-
测试完成后，使用exec/tools/version_task/build_version_pc.bat来打包pc版本的运行包

-
运行包生成完成后，会保存在exec/builds目录下