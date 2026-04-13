---
title: 用 Workflow 把知乎答案存到 Instapaper
url: http://frankorz.com/2016/11/05/workflow-of-zhihu-to-instapaper/
author: 文章作者 猫冬
published: '2016-11-05'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

随着 Instapaper 宣布免费，我开始尝试使用这款应用。这款应用很适合我，唯独抓取的时候对知乎支持不太好，有强迫症的我尝试解决它，其中比较有效的方法是：右上角菜单「Safari 打开」-打开阅读器视图-发邮件至 Instapaper 邮箱。但是这依旧有点麻烦了，我后来找到 [Mercury](https://mercury.postlight.com) 这个服务，并用 Workflow 解决了这问题。

### Workflow 特点

- 支持知乎答案抓取（答案太短可能会抓取失败）
- 知乎专栏文章和其他网站直接原生添加到 Instapapaer
- 清除知乎答案内的知乎超链接跳转

### 前提

### 注册 Mercury

Mercury 是一个免费的在线文本解析网站，允许我们提供网址并得到 JSON 格式的解析结果。我们需要使用它们的服务，所以要注册个账号得到 API KEY 来配置 Workflow 使用。

首先进入 [Mercury](https://mercury.postlight.com) ，点击右上角的「SIGN UP FOR FREE」。注册完成并验证邮箱后，就能看到你专属的 API KEY 了。

![](../../assets/dadf7831027d3eb9.jpg)


### 配置 Workflow

你可以在下面获取到我写的 Workflow。

[Workflow V5 下载](https://workflow.is/workflows/946d07f3f3e44ff09fccb59d9fafdb96)

点击「GET WORKFLOW」，应该就能把这 workflow 保存到你应用当中了。

#### 配置 Mercury API KEY 和邮箱

KEY 我们已经拿到了，另外需要的 Instapaper 的邮箱地址可以在 [How to Save](https://www.instapaper.com/save/email) 中找到Instapaper接收邮件的邮箱地址。

![](../../assets/9d06c91610ab7670.jpg)


把 Workflow 往下拉，找到注释，把 KEY 和 Instapaper 接收邮件的邮箱分别填到「Text」框中和「Email Address」框中。

![IMG_0177](../../assets/17b4bfe0e59bf66e.png)


然后把 Workflow 拉到中间，找到绿色的「Ask When Run」圈圈，删除后添加自己用来发邮件的个人邮箱。再往下拉到 Workflow 四分之三的位置，同样配置好个人邮箱。第一次使用 Workflow 的同学需要授权邮箱应用，另外要注意的是邮箱服务器、用户名、密码都确认无误仍然提示 incorrect 的话，直接保存就好了，运行 Workflow 发送邮件无效后再修改。

![IMG_0178](../../assets/2f256340aaf5dec1.png)


Workflow 中共有四次要配置的地方，并且要在 Workflow 应用中对 Instapaper 授权，都配置完毕要在 Workflow 应用中运行一次，获得对新下载的 Workflow 运行的许可。

### 运行

![知乎答案](../../assets/e2c685a26ca96af0.gif)


操作：右上角菜单-**复制链接**-运行 Workflow

### 最后

自己实在等不到知乎官方支持 Instapaper 的那天了，于是写了这个 Workflow 。拿到 Matrix 内测资格后，这个 Workflow 已经是第五个版本了，相对比较完善。如果有什么疑问或者建议，请在评论区指出，我会尽快回复。

另外 Workflow 中对知乎答案的支持都是通过其他服务抓取数据而来，所以抓取时相当于下载一次网络数据，再用邮件发出，对于图片较多的答案或专栏会耗费较多流量。

注意事项：

- Workflow 对当前复制的文字中是否含有「http」判断是否为链接
- 如果不能运行请换其他邮箱测试（确保邮箱的SMTP、IMAP地址、端口号和邮箱密码正确，QQ 邮箱需要生成授权码来当密码使用）
- 运行后会清除当前剪贴板
- 图片越多，发送邮件速度越慢，耗费流量越多
- 已知不支持新浪文章
**该方法需要重新下载网页数据并发邮件，使用的时候请注意流量消耗**- 如果有运行 Workflow 时自动打开应用再运行的现象，尝试重启设备
- Workflow 点击运行后就会在后台运行，不用死等
- 如还是发送空邮件，且以上所有问题都排除了，那就是知乎答案过长，例如
[这篇知乎答案](https://www.zhihu.com/question/22164041/answer/148128347)，导致 Mercury 解析超时…

找到解决方法，马上写博文分享这也是一种强迫症吧哈哈哈(´ ˘ `๑)