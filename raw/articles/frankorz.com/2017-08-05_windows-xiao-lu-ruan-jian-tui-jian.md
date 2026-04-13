---
title: Windows 效率软件推荐
url: http://frankorz.com/2017/08/05/recommandation-of-some-efficient-software/
author: 文章作者 猫冬
published: '2017-08-05'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

用了几年苹果电脑之后，最近开始用回 Windows 系统，找到一些十分好用的效率向的工具，同时受 [效率必备，软件推荐](http://www.ituring.com.cn/article/469111) 启发，写篇文章推荐一下。

## ShareX

[ShareX](https://getsharex.com/) 是一款主打捕获屏幕、文件分享、和生产力的开源工具。下面是我用 ShareX 来录制软件界面的 GIF 动图，可以看看其丰富的功能。

![](../../assets/9fd80f50794bf547.gif)


和 QQ 自带的截图功能和国人开发的 Snipaste 不同，ShareX 的截图不仅仅止于截图后进行批注。ShareX 除了支持和 Snipaste 相似的捕捉窗格（活动的窗口、窗口内的元素等）截图功能外，还支持各种后续的动作，形成一个动作链以节省时间。

### 截图

例如截完图后可以打开编辑窗口编辑，同时保存图片到自定的目录和剪贴板等等，自己可以自定义其动作链。建议勾选复制到剪贴板，文后会完成一个利用快捷键完成截图上传的动作链（你也可以直接配置截图完进行上传，看个人习惯）。

![](../../assets/0d0f3290ff893776.png)


### 上传

![](../../assets/31be3a8c58ba6cc9.png)


ShareX 的上传分为图片上传、文字上传和 URL 短链分享。图片可以上传到不同的图床：Imgur、Google Photos、TinyPic 等等，同样的，文件也可以上传到不同的文件共享网站：Dropbox、OneDrive 等，不过软件内置的多是国外的服务。开放性十足的 ShareX 还允许开发者共享自定义上传插件，这些上传插件可以在 [CustomUploaders](https://github.com/ShareX/CustomUploaders) 里找到。

#### 图片上传

由于不同上传的设置类似，这里只写图片上传的一些个人配置。

我自己使用的图床是开放了 API 的 [SM.MS](https://sm.ms/) 图床，这图床背后的大佬就是卖 [t.tt](http://t.tt) 域名给罗永浩的那位，据他说自己的流量多的用不完就拿来做点公益项目…SM.MS 图床的上传插件可以在 [这里](https://github.com/ShareX/CustomUploaders/blob/master/sm.ms.sxcu) 下载，下载后双击即可导入。导入后可以在软件界面的 [上传至…] -> [上传至…设置] -> 左列表最底端的自定义上传者，在目标类型选上 Image uploader 再点更新就能完成上传插件的配置。

![](../../assets/bd9add1cfa0df7ef.png)


接着在 [上传至…] 选项里勾选好对应的上传插件就完成配置了。

![](../../assets/ef00c27813e73de7.png)


#### 上传后的动作

![](../../assets/cbd36e92c11c6a72.png)


与截图后的动作类似，上传后的动作也十分实用，这里我只选了 URL 复制到剪贴板。

### 动作链

目前截图、上传这两动作都已经配置好，可以开始配置快捷键了。

#### 快捷键

![](../../assets/3bf7009d8251fa55.png)


这里我增加了一个从剪贴板上传的快捷键，这样的话 [快捷键截图] -> 截图保存到剪贴板 -> [快捷键上传] -> 剪贴板内的截图上传到相应图床 -> 返回图片 URL 到剪贴板的动作链就完成了。这对于经常在电脑写东西的我来说很实用，在写这篇文章时也利用这软件节省了不少时间。

你可以在 [ShareX 官网](https://getsharex.com/) 进行下载，其文件托管在 github。

## QuickLook

macOS 系统内置了一个好用的功能，就是空格查看文件内容，现在 QuickLook 也为 Windows 提供类似的体验。

### 空格查看 markdown 文件

![](../../assets/7888f0f6d46ad3a1.png)


### 空格查看代码文件

![](../../assets/0ae91b683a1ee1cf.png)


### 空格查看压缩包

![](../../assets/d2cb21d35ae5358e.png)


你可以在 [QuickLook 官网](http://pooi.moe/QuickLook/) 下载安装包，QuickLook 也能在 [Windows 应用商店](https://www.microsoft.com/store/apps/9nv4bs3l1h4s?ocid=badge) 下载。

## Zeal

受 macOS 平台上 Dash 代码 API 文档查询软件的启发，Zeal 是一款免费开源的支持 Windows 和 Linux 系统的代码 API 文档查询软件。

### 丰富的文档

![](../../assets/a241e29f5d493ea5.png)


### 查询关键词

![](../../assets/1b0b8d4ed4634b4d.png)


### 与编辑器联动

开发者为 Atom、VSCode、Jetbrain 全家桶 IDE 等提供了相关的插件，例如 Atom 的 [atom-dash](https://github.com/blakeembrey/atom-dash)，VSCode 的 [Dash](https://marketplace.visualstudio.com/items?itemName=deerawan.vscode-dash)，Jetbrain 全家桶的 [Dash](https://plugins.jetbrains.com/plugin/7351-dash)。

有了这些插件，你可以做到在写 Python 代码的时候，调用快捷键查询 Zeal 中 Python 文档对应的 API。

你可以在 [Zeal 官网](https://zealdocs.org/) 获得 Zeal。

## 结语

上面提到的三款效率软件都是开源并能免费下载使用，现在越发钦佩开源者了~