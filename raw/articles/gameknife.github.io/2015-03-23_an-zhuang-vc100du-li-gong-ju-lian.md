---
title: 安装vc100独立工具链
url: http://gameknife.github.io/tech/2015/03/23/install-vc100-toolchain/
published: '2015-03-23'
source_blog: gameKnife
source_site: http://gameknife.github.io/
category: graphics
fetched: '2026-04-13'
---

# 安装vc100独立工具链

23 Mar 2015#### 前言

这周末花时间尝试研究[制作vc100独立工具链](http://gameknife.github.io/tech/2015/03/21/make-custom-vc100-toolchain/)，功夫不负有心人，事实证明是完全可行的。下面我给出独立工具链的下载地址和安装注意事项。

#### 下载地址

#### 安装注意事项

系统要求：win7+ & 64bit

环境要求：vs2011+ & 没有安装vs2010

安装方法：

- 下载package.zip, 放置于c:\,
- 解压到c:\package, 使得文件install_vc100_toolchain.bat存在于c:\package\install_vc100_toolchain.bat
- 使用
**管理员**身份运行c:\package\install_vc100_toolchain.bat - 等待pause, 按下回车cmd关闭后，安装完成