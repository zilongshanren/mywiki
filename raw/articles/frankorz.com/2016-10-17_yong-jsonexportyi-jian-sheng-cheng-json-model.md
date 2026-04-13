---
title: 用JSONExport一键生成JSON Model
url: http://frankorz.com/2016/10/17/powerful-jsonexport/
author: 文章作者 猫冬
published: '2016-10-17'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

以前跟着《第一行代码》入门 Android 的时候，学过几个解析 JSON 的方法，一个一个按 key 名找、建对象存等等，解析的工具也很多，以前对 JSON 不熟悉，这也浪费了我很多时间。现在刚入门 iOS 没多久就让我看到神器 JSONExport，解析 JSON 从此只是几行代码的事情~

JSONExport 是一个运行在 macOS 上通过 JSON 字符串转为 model 的开源工具，支持 Java、Objective-C 和 Swift。我发现了这工具之后忍不住用 Charles 到处抓 API 测试，这是后话~

每次学完了都觉得很基础…还是记下来吧…

### 工具

JSONExport 的项目地址在这：[JSONExport](https://github.com/Ahmed-Ali/JSONExport)

不过项目需要自己编译，嫌麻烦的可以直接下载我汉化好的 [JSONExport](https://pan.baidu.com/s/1dE4WX1J) ，如果失效请在评论留言，下面是界面：

![](../../assets/f00365ee5556f456.jpg)


左边把 JSON 字符串放入，右下角选择要生成的 Model 即可。

### 使用

这里我使用[豆瓣图书 Api V2](https://developers.douban.com/wiki/?title=book_v2)的 API 做示范。

根据提供的 API ，假如我想获得十个书名为"ios 开发"的书籍名，可以构建 URL 为`"https://api.douban.com/v2/book/search?count=10&q=ios%20%E5%BC%80%E5%8F%91"`

，在网页中打开获得 JSON 字符串。

遇到的坑：

- JSON 字符串中含有中文可能会被说明“无效 JSON”，转成unicode再放到工具里去用吧，例如：
[在线unicode转中文](http://www.bejson.com/convert/unicode_chinese/)，或者用下图的 Paw。 - Mac App Store 中也有同名工具，应该是别人直接修改原作者后上传的，能够根据 JSON 地址提取 JSON 数据，不过也是一搜中文就闪退。
- JSONExport 没生成正确的 Model 就重启吧。

![](../../assets/8d6d38d8b0bc6a53.jpg)


复制至JSONExport中，右下角按需选择，这里我用 Swift - Struct 做示范。

![](../../assets/f279fc74ca159845.jpg)


之后点右下角保存，把这六个文件拷到项目中就能直接使用了！我们可以直接构建一个 Struct。

`BookInfo.swift`


1 | struct BookInfo { |

这里我只需要图片、标题、isbn13、url和简介，接下来在 ViewController 中新建个方法获取数据，这里用了用 Swift 写的第三方网络库 Just。

1 | let searchUrl = "https://api.douban.com/v2/book/search?count=10&q=ios%20%E5%BC%80%E5%8F%91"//搜索"ios 开发" |

如果 Xcode 自动提示没有提供初始化语句，可以在刚刚的 `BookInfo.swift`

中自动补全代码，再剪切过来用。

![](../../assets/3953b8bb73e0de96.jpg)


运行后可以看到 dump 的数据已经出来了：

![](../../assets/2967a248fd953c2a.jpg)


其实本文到这就差不多了，主要注意 JSON 中数组和这里生成 Model 的关系。最后附上一个小 Demo ，还没加搜索框，没用完解析的数据，将就看吧…_(:ｪ｣∠)_

![](../../assets/8583decf070cb714.jpg)


项目可以参照这里 [Donban-demo-with-JSONExport](https://github.com/Latias94/Donban-demo-with-JSONExport)