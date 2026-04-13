---
title: Hexo 博客补丁
url: http://frankorz.com/2016/09/30/Hexo-patch/
author: 文章作者 猫冬
published: '2016-09-30'
source_blog: 萤火之森
source_site: http://frankorz.com/
category: game programming
fetched: '2026-04-13'
---

本博客部分修改内容

注：原文的主题为 Next，现在在使用 Even，所以配置可能有些地方不一样。

### 小建议

`hexo new "标题"`

的时候尽量取英文标题，在文章中再用 `title:`

指定中文标题，这样未来改标题好改，相应文章的多说评论也不会消失。

### Github Pages 中增加 [README.md](http://README.md)

很多朋友的 hexo 博客都是建在 Github 上的，作为一个项目，`README.md`

文件能够在 Github 上介绍博客的一些信息，但是贸然把文件放到 `source`

文件夹中会被 hexo 检测并转为 html 文档，我们在站点配置文件中跳过即可。

1 | skip_render: |

### 网站底部字数统计

安装 hexo-wordcount

`npm install hexo-wordcount --save`


在`（博客主目录）/themes/next/layout/_partials/footer.swig`

中最后加上

1 | <div class="theme-info"> |

更多参考：[hexo-wordcount](https://www.npmjs.com/package/hexo-wordcount)

### 添加文章更新时间

修改`（博客主目录）/themes/next/layout/_macro/post.swig`

文件，在`<span class="post-time">...</span>`

标签后添加

1 | {%if post.updated and post.updated > post.date%} |

![](../../assets/91f91fdbe344eed7.jpg)


根据博客配置文件中的 `language`

参数修改对应的语言配置文件`（博客主目录）/themes/next/languages/zh_Hans.yml`


1 | post: |

修改主题配置文件`（博客主目录）/themes/next/_config.yml`

，增加一行

1 | display_updated: true |

写文章的时候可以直接在文章开头设置更新时间

1 | updated: 2016-10-14 10:53:09 |

没有这参数的话将会显示md文件的修改日期

### 本地搜索

安装 hexo-generator-search

`npm install hexo-generator-search --save`


编辑主目录下站点配置文件`_config.yml`

加入

1 | search: |

### 添加音乐

#### 歌曲

在markdown文件中要添加音乐处加入iframe标签

1 | <iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="http://music.163.com/outchain/player?type=2&auto=0&id=34578162&height=66"></iframe> |

需要居中可以在外添加`<center>`

标签

1 | <center> |

其中id后数字为网易云音乐歌曲id，可以从[Music](http://music.daoapp.io)处搜索歌名，例如搜索`memories`

，我选择了`MEMORIES - 『MEMORIES』- ALAN WALKER`

之后到达 [http://music.daoapp.io/player?song=34578162](http://music.daoapp.io/player?song=34578162) ，song后数字便是歌曲id。另外高度宽度可以自己根据博客样式更改，`auto = 0`

是不自动播放，需要自动播放请改为`auto = 1`

。

你也可以直接从网易云音乐[官网](http://music.163.com/)中搜索到歌曲，再生成外链播放器。有些版权保护的歌曲或歌单不支持生成外链，可以直接像上面的方法一样查 id 改代码即可。

![](../../assets/f97ea68f41c01bcb.jpg)


示例：

#### 歌单

操作和上面一样，搜索后选择歌单，找到id再替换。

1 | <iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=450 src="http://music.163.com/outchain/player?type=0&id=144236857&auto=0&height=430"></iframe> |

示例：

其他高深玩法参考 [163music-APlayer-you-get-docker](https://github.com/YUX-IO/163music-APlayer-you-get-docker)

#### 歌词

要带歌词的话需要用到适用于 Hexo 的 [Aplayer](https://github.com/grzhan/hexo-tag-aplayer)。

如果歌词、音乐文件、音乐图片保存到博客服务器中，请参考上面的链接进去设置 `post asset folders`

，这里用外链做例子。

安装 Aplayer：

`npm install --save hexo-tag-aplayer`


使用：

参数：

`title`

: 音乐标题`author`

: 歌手名`url`

: 音乐文件路径`picture_url`

: 可选，音乐图片路径`narrow`

: 可选，狭窄的样式`autoplay`

: 可选，自动播放，不支持移动浏览器`width:xxx`

: 可选，前缀`width:`

，播放器的宽度 (默认: 100%)`lrc:xxx`

: 可选，前缀`lrc:`

，LRC 文件路径

例子：

建议使用七牛云存文件，直接用文件外链来设置，其中歌词文件内容参照 lrc 格式填写。

![](../../assets/e6b38b940549798c.jpg)


### 添加思维导图

利用之前App store 限免过的iOS版 MindNode，制作完导图之后，选择在MyMindNode上共享。

![IMG_0165](../../assets/c3c37241b4edc829.png)


上传文件后得到网址，打开后选择右上角导出按钮->Embed。

![](../../assets/419545fc5cf69310.jpg)


这里选择宽度和高度，再如添加音乐一样添加iframe标签即可，示例参考：[2016年书单、公开课](http://latias94.github.io/books/) 。

### 本博客动态背景

在 [百度云](https://pan.baidu.com/s/1jIuJ03s) 下载`particle.js`

，并移动到`（博客主目录）/themes/next/source/js/src`

文件夹下。

然后在`（博客主目录）/themes/next/source/layout/_layout.swig`

中的最后`body`

标签上添加

1 | <script type="text/javascript" src="/js/src/particle.js"></script> |

### 控制首页中文章显示量

在要显示的文字后添加`<!--more-->`

，例如本文章：

1 | --- |