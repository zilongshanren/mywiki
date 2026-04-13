---
title: 搭建你自己的Go Runtime metrics环境
url: https://tonybai.com/2017/07/04/setup-go-runtime-metrics-for-yourself/
published: '2017-07-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 搭建你自己的Go Runtime metrics环境

自从[Go 1.5](http://tonybai.com/2015/07/10/some-changes-in-go-1-5/)开始，每次[Go release](https://golang.org/dl), Gopher [Brian Hatfield](https://twitter.com/brianhatfield)都会将自己对新版Go的runtime的性能数据（与之前Go版本的比较）在twitter上晒出来。就连Go team staff在世界各地做speaking时也在slide中引用Brian的图片。后来，Brian Hatfield将其用于度量runtime性能数据的代码打包成library并放在github上[开源了](https://github.com/bmhatfield/go-runtime-metrics)，我们也可以使用这个[library](https://github.com/bmhatfield/go-runtime-metrics)来建立我们自己的Go Runtime metrics设施了。这里简要说一下搭建的步骤。

## 一、环境与原理

Brian Hatfield的go-runtime-metrics library实现的很简单，其runtime data来自于Go runtime package中的MemStats、NumGoroutine和NumCgoCall等。被测试目标程序只需要import该library即可输出runtime states数据：

```
import _ "github.com/bmhatfield/go-runtime-metrics"
```


go-runtime-metrics library将启动一个单独的[goroutine](http://tonybai.com/2017/06/23/an-intro-about-goroutine-scheduler/)，并定时上报runtime数据。目前该library仅支持向[statsD](https://github.com/etsy/statsd)输出数据，用户可以通过配置将statsD的数据导入[graphite](http://graphiteapp.org/)并使用graphite web查看，流程如下图：

![img{512x368}](../../assets/ab9b72d34f7258b8.png)


本次实验环境为[ubuntu](http://tonybai.com/tag/ubuntu) 16.04.1：

```
$ uname -rmn
tonybai-ThinkCentre-M6600s-N000 4.4.0-83-generic x86_64
```


## 二、搭建步骤

### 1、安装go-runtime-metrics library

我们直接go get就可以下载go-runtime-metrics library：

```
$ go get github.com/bmhatfield/go-runtime-metrics
```


我们编写一个目标程序：

```
//main.go
package main
import (
"flag"
"log"
"net/http"
"os"
_ "github.com/bmhatfield/go-runtime-metrics"
)
func main() {
flag.Parse()
cwd, err := os.Getwd()
if err != nil {
log.Fatal(err)
}
srv := &http.Server{
Addr: ":8000", // Normally ":443"
Handler: http.FileServer(http.Dir(cwd)),
}
log.Fatal(srv.ListenAndServe())
}
```


我的ubuntu主机上安装了四个go版本，它们分别是go 1.5.4、go 1.7.6、go 1.8.3和go1.9beta2，于是我们分别用这四个版本的server作为被测程序进行go runtime数据上报，以便对比。

```
$ GOROOT=~/.bin/go154 ~/.bin/go154/bin/go build -o server-go154 main.go
$ GOROOT=~/.bin/go174 ~/.bin/go174/bin/go build -o server-go174 main.go
$ GOROOT=~/.bin/go183 ~/.bin/go183/bin/go build -o server-go183 main.go
$ GOROOT=~/.bin/go19beta2 ~/.bin/go19beta2/bin/go build -o server-go19beta2 main.go
$ ls -l
-rwxr-xr-x 1 tonybai tonybai 6861176 7月 4 13:49 server-go154
-rwxrwxr-x 1 tonybai tonybai 5901876 7月 4 13:50 server-go174
-rwxrwxr-x 1 tonybai tonybai 6102879 7月 4 13:51 server-go183
-rwxrwxr-x 1 tonybai tonybai 6365648 7月 4 13:51 server-go19beta2
```


### 2、安装、配置和运行statsD

[statsD](https://github.com/etsy/statsd)这个工具用于收集统计信息，并将聚合后的信息发给后端服务（比如：graphite）。statsD是采用js实现的服务，因此需要安装[nodejs](https://nodejs.org/en/)、[npm](https://www.npmjs.com/)和相关modules：

```
$ sudo apt-get install nodejs
$ sudo apt-get install npm
```


接下来，我们将statsD项目clone到本地并根据exampleConfig.js模板配置一个我们自己用的goruntimemetricConfig.js（基本上就是保留默认配置）:

```
// goruntimemetricConfig.js
{
graphitePort: 2003
, graphiteHost: "127.0.0.1"
, port: 8125
, backends: [ "./backends/graphite" ]
}
```


启动statsD:

```
$ nodejs stats.js goruntimemetricConfig.js
3 Jul 11:14:20 - [7939] reading config file: goruntimemetricConfig.js
3 Jul 11:14:20 - server is up INFO
```


启动成功！

### 3、安装、配置和运行graphite

[graphite](https://github.com/graphite-project)是一种存储时序监控数据，并可以按用户需求以图形化形式展示数据的工具，它包括三个组件：

whisper是一种基于file的时序数据库格式，同时whisper也提供了相应的命令和API供其他组件调用以操作时序数据库；

carbon用于读取外部推送的metrics信息，进行聚合并写入db，它还支持缓存热点数据，提升访问效率。

graphite-web则是针对用户的图形化系统，用于定制展示监控数据的。

Graphite的安装和配置是略微繁琐的，我们一步一步慢慢来。

#### a) 安装graphite

```
$sudo apt-get install graphite-web graphite-carbon
whisper将作为依赖自动被安装。
```


#### b) local_settings.py

graphite的主配置文件在/etc/graphite/local_settings.py，文件里面有很多配置项，这里仅列出有关的，且本次生效的配置：

```
// /etc/graphite/local_settings.py
TIME_ZONE = 'Asia/Shanghai'
LOG_RENDERING_PERFORMANCE = True
LOG_CACHE_PERFORMANCE = True
LOG_METRIC_ACCESS = True
GRAPHITE_ROOT = '/usr/share/graphite-web'
CONF_DIR = '/etc/graphite'
STORAGE_DIR = '/var/lib/graphite/whisper'
CONTENT_DIR = '/usr/share/graphite-web/static'
WHISPER_DIR = '/var/lib/graphite/whisper'
LOG_DIR = '/var/log/graphite'
INDEX_FILE = '/var/lib/graphite/search_index' # Search index file
DATABASES = {
'default': {
'NAME': '/var/lib/graphite/graphite.db',
'ENGINE': 'django.db.backends.sqlite3',
'USER': '',
'PASSWORD': '',
'HOST': '',
'PORT': ''
}
}
```


#### c) 同步数据库

接下来执行下面两个命令来做database sync(同步)：

```
$ sudo graphite-manage migrate auth
.. ....
Operations to perform:
Apply all migrations: auth
Running migrations:
Rendering model states... DONE
Applying contenttypes.0001_initial... OK
Applying contenttypes.0002_remove_content_type_name... OK
Applying auth.0001_initial... OK
Applying auth.0002_alter_permission_name_max_length... OK
Applying auth.0003_alter_user_email_max_length... OK
Applying auth.0004_alter_user_username_opts... OK
Applying auth.0005_alter_user_last_login_null... OK
Applying auth.0006_require_contenttypes_0002... OK
$ sudo graphite-manage syncdb
Operations to perform:
Synchronize unmigrated apps: account, cli, render, whitelist, metrics, url_shortener, dashboard, composer, events, browser
Apply all migrations: admin, contenttypes, tagging, auth, sessions
Synchronizing apps without migrations:
Creating tables...
Creating table account_profile
Creating table account_variable
Creating table account_view
Creating table account_window
Creating table account_mygraph
Creating table dashboard_dashboard
Creating table events_event
Creating table url_shortener_link
Running deferred SQL...
Installing custom SQL...
Running migrations:
Rendering model states... DONE
Applying admin.0001_initial... OK
Applying sessions.0001_initial... OK
Applying tagging.0001_initial... OK
You have installed Django's auth system, and don't have any superusers defined.
Would you like to create one now? (yes/no): yes
Username (leave blank to use 'root'):
Email address: xx@yy.com
Password:
Password (again):
Superuser created successfully.
```


这里我们创建一个superuser：root，用于登录graphite-web时使用。

#### d) 配置carbon

涉及carbon的配置文件如下，我们保持默认配置不动：

```
/etc/carbon/carbon.conf（内容太多，这里不列出来了）
/etc/carbon/storage-schemas.conf
[carbon]
pattern = ^carbon\.
retentions = 60:90d
[default_1min_for_1day]
pattern = .*
retentions = 60s:1d
[stats]
pattern = ^stats.*
retentions = 10s:6h,1min:6d,10min:1800d
```


carbon有一个cache功能，我们通过下面步骤可以将其打开：

```
打开carbon-cache使能开关：
$ vi /etc/default/graphite-carbon
CARBON_CACHE_ENABLED=true
启动carbon-cache：
$ sudo cp /usr/share/doc/graphite-carbon/examples/storage-aggregation.conf.example /etc/carbon/storage-aggregation.conf
$ systemctl start carbon-cache
```


#### e) 启动graphite-web

graphite-web支持多种主流web server，这里以[apache2](http://tonybai.com/tag/apache)为例，graphite-web将mod-wsgi方式部署在apache2下面：

```
$sudo apt-get install apache2 libapache2-mod-wsgi
$ sudo service apache2 start
$ sudo a2dissite 000-default
Site 000-default disabled.
$ sudo service apache2 reload
$ sudo cp /usr/share/graphite-web/apache2-graphite.conf /etc/apache2/sites-available
$ sudo a2ensite apache2-graphite
Enabling site apache2-graphite.
To activate the new configuration, you need to run:
service apache2 reload
$ sudo systemctl reload apache2
```


由于apache2的Worker process默认以www-data:www-data用户权限运行，但数据库文件的访问权限却是：_graphite:_graphite：

```
$ ll /var/lib/graphite/graphite.db
-rw-r--r-- 1 _graphite _graphite 72704 7月 3 13:48 /var/lib/graphite/graphite.db
```


我们需要修改一下apache worker的user：

```
$ sudo vi /etc/apache2/envvars
export APACHE_RUN_USER=_graphite
export APACHE_RUN_GROUP=_graphite
```


重启apache2生效！使用Browser打开：http://127.0.0.1，如无意外，你将看到下面graphite-web的首页：

![img{512x368}](../../assets/1a778c5ee234a9ad.png)


## 三、执行benchmarking

这里我将使用[wrk](https://github.com/wg/wrk)这个http benchmarking tool分别对前面的四个版本的目标程序(server-go154 server-go174 server-go183 server-go19beta2)进行benchmarking test，每个目标程序接收10分钟的请求：

```
$ ./server-go154
$ wrk -t12 -c400 -d10m http://127.0.0.1:8000
$ ./server-go174
$ wrk -t12 -c400 -d10m http://127.0.0.1:8000
$ ./server-go183
$ wrk -t12 -c400 -d10m http://127.0.0.1:8000
$ ./server-go19beta2
$ wrk -t12 -c400 -d10m http://127.0.0.1:8000
```


## 四、结果展示

用浏览器打开graphite-web，在左边的tree标签下以此打开树形结构：Metrics -> stats -> gauges -> go -> YOUR_HOST_NAME -> mem -> gc -> pause，如果顺利的话，你将会在Graphite Composer窗口看到折线图，我们也以GC pause为例，GC pause也是gopher们最为关心的：

![img{512x368}](../../assets/487df2f2ff137bb0.png)


通过这幅图（左侧坐标轴的单位为nanoseconds），我们大致可以看出：

Go 1.5.4的GC pause约在600μs左右；

Go 1.7.4的GC pause约在300μs左右；

Go 1.8.3和Go 1.9beta2的GC pause基本都在100μs以下了。Go 1.9的GC改进似乎不大。不过这里我的程序也并不足够典型。

其他结果：

Go routines number：

![img{512x368}](../../assets/249cb32802686b20.png)


GC count：

![img{512x368}](../../assets/7fda7de2164388e6.png)


memory allocations：

![img{512x368}](../../assets/68f7777d1216f55a.png)


除了查看单个指标曲线，你也可以通过graphite-web提供的dashboard功能定制你要monitor的面板，这里就不赘述了。

## 五、参考资料

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论