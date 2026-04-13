---
title: 以单件方式创建和获取数据库实例
url: https://tonybai.com/2021/02/09/create-and-get-db-access-instance-through-singleton/
published: '2021-02-09'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 以单件方式创建和获取数据库实例

![img{512x368}](../../assets/75dd50370c20fe1b.png)


在屡次的Go用户调查中，使用Go语言进行Web服务/API开发都占据了Go语言用途调查结果的头部位置。下面是知名Go IDE [goland](https://blog.jetbrains.com/go/)的母公司JetBrains最新发布的[Go当前状态报告(2021.2.3)](https://blog.jetbrains.com/go/2021/02/03/the-state-of-go/)中的截图：

![img{512x368}](../../assets/24f2bd3c792bbb9a.png)


开发Web或API服务，难免会与数据库打交道。如今创建数据库实例并访库的技术已经是很成熟了，于是就有了下面这样的程序结构：

![img{512x368}](../../assets/43eb2c519e94042b.png)


上面这个图片中，Web服务中的每个要与数据库进行数据交互的包都是自己创建并使用数据库实例，这显然是一种糟糕的设计，它不仅让每个包都耦合外部的第三方数据包，每个包还担负起管理数据库连接的责任，并且在Web服务的整个项目中，还会存在多处获取数据库连接配置、打开关闭数据库等的重复代码。一旦数据库访问代码发生变化，这些包就都得修改一遍。

那么如何优化呢？一个很自然的想法：将创建数据库实例以及对数据库实例的获取封装到一个包中，其他包无需再关心数据库实例的创建与释放，直接获取和使用实例即可，如下面示意图：

![img{512x368}](../../assets/ac73bc51a4a62757.png)


从这段描述来看，这显然是单件(singleton，亦翻译为单例)这个“创建型”模式的应用场景。在这里我们给出一个用Go实现的以单件方式创建和获取数据库实例的demo。

Go语言标准库提供了sync.Once类型，这让Go实现单件模式变得天然简单了。为了模拟上述场景，我们先来描述一下demo项目的结构：

```
database-singleton
├── Makefile
├── cmd
│ └── main
│ └── main.go
├── conf
│ └── database.conf
├── go.mod
├── go.sum
└── pkg
├── config
│ └── config.go
├── db
│ └── db.go
├── model
│ └── employee.go
├── reader
│ └── reader.go
└── updater
└── updater.go
```


在database-singleton这个repo中：

- pkg/db就是我们将数据库实例的创建和获取封装到单件中的实现；
- pkg/reader和pkg/updater则模拟了两个通过单件获取数据库实例并分别读取和更新数据库的包；
- pkg/config是数据库连接配置的读取包。关于go程序的配置读取方案的一些方案，可以参考我的
[《写Go代码时遇到的那些问题[第1期]》](https://tonybai.com/2018/01/13/the-problems-i-encountered-when-writing-go-code-issue-1st/)一文。

我们从cmd/main/main.go中，可以看到整个程序的运行结构：

```
// github.com/bigwhite/experiments/blob/master/database-singleton/cmd/main/main.go
package main
import (
"log"
"os"
"os/signal"
"sync"
"syscall"
"github.com/bigwhite/testdboper/pkg/config"
"github.com/bigwhite/testdboper/pkg/db"
"github.com/bigwhite/testdboper/pkg/reader"
"github.com/bigwhite/testdboper/pkg/updater"
)
func init() {
err := config.Init()
if err != nil {
panic(err)
}
}
func main() {
var wg sync.WaitGroup
wg.Add(2)
var quit = make(chan struct{})
// do some init from db
_ = db.DB()
go func() {
updater.Run(quit)
wg.Done()
}()
go func() {
reader.Run(quit)
wg.Done()
}()
c := make(chan os.Signal, 1)
signal.Notify(c, syscall.SIGINT, syscall.SIGTERM)
_ = <-c
close(quit)
log.Printf("recv exit signal...")
wg.Wait()
log.Printf("program exit ok")
}
```


简单解释一下上面main.go中的代码：

- 在init函数中，我们读取了用于整个程序的配置信息，主要是数据库的连接信息(ip、port、user、password等)；
- 我们启动了两个独立的goroutine，分别运行reader和updater两个模拟数据库读写场景的包；
- 我们使用quit channel通知两个goroutine退出，并使用sync.WaitGroup来等待两个goroutine的结束(关于goroutine的并发模式的详解，可以参考我的专栏文章
[《Go并发模型和常见并发模式》](https://www.imooc.com/read/87/article/2430)； - 我们使用signal.Notify监听系统信号，并在收到系统信号后做出响应（关于signal包的使用，请参见我的专栏文章
[《小心被kill！不要忽略对系统信号的处理》](https://www.imooc.com/read/87/article/2473)）。

在main函数代码中，我们看到了如下调用：

```
// do some init from db
_ = db.DB()
```


这是在初始化的时候通过单件获取访问数据库的对象实例，但这个不是必须的，只有在初始化需要从数据库读取一些信息时才会用到。

接下来，我们就来看看创建数据库访问实例的单件是如何实现的：

```
// github.com/bigwhite/experiments/blob/master/database-singleton/pkg/db/db.go
package db
import (
"fmt"
"sync"
"time"
"github.com/bigwhite/testdboper/pkg/config"
"github.com/jinzhu/gorm"
_ "github.com/jinzhu/gorm/dialects/mysql"
)
var once sync.Once
type database struct {
instance *gorm.DB
maxIdle int
maxOpen int
maxLifetime time.Duration
}
type Option func(db *database)
var db *database
func WithMaxIdle(maxIdle int) Option {
return func(d *database) {
d.maxIdle = maxIdle
}
}
func WithMaxOpen(maxOpen int) Option {
return func(d *database) {
d.maxOpen = maxOpen
}
}
func DB(opts ...Option) *gorm.DB {
once.Do(func() {
db = new(database)
for _, f := range opts {
f(db)
}
dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8&parseTime=True&loc=Local",
config.Config.Database.User,
config.Config.Database.Password,
config.Config.Database.IP,
config.Config.Database.Port,
config.Config.Database.DB)
var err error
db.instance, err = gorm.Open("mysql", dsn) // database: *gorm.DB
if err != nil {
panic(err)
}
sqlDB := db.instance.DB()
if err != nil {
panic(err)
}
if db.maxIdle != 0 {
sqlDB.SetMaxIdleConns(db.maxIdle)
}
if db.maxLifetime != 0 {
sqlDB.SetConnMaxLifetime(db.maxLifetime)
}
if db.maxOpen != 0 {
sqlDB.SetMaxOpenConns(db.maxOpen)
}
})
return db.instance
}
```


- 首先，上述代码使用sync.Once对象辅助实现单件模式，传给once.Do方法的函数在整个程序生命周期中执行且只执行一次。我们就是在这个函数中创建的数据库访问实例；
- 这里我们使用gorm库承担访问数据库的任务，因此所谓的实例，即gorm.DB类型的指针；
- gorm.DB类型是并发安全的，我们无需考虑单件返回的实例的并发访问问题；
- gorm.DB底层使用的是标准库database/sql维护的
[连接池](https://gorm.io/docs/connecting_to_the_database.html#Connection-Pool)，因此一旦gorm.DB实例建立成功，对连接的维护也全部交由它去处理，我们在业务层无需考虑保活和断连后重连问题； - 这里我们没有将获取单件的函数DB设计为不带参数的函数，而是将其设计为携带可变参数列表的函数，这主要是考虑在初次调用DB函数时，可以对底层的连接池进行设置(MaxIdleConn、MaxLifetime、MaxOpenConn)。其他情况使用时，无需传入任何参数；当然由于返回的是gorm.DB的指针，因此外层也是可以基于该指针自行设置连接池的，但在业务层动态更改连接池属性似乎并不可取；
- 谈到可变参数函数，这里使用了功能选项(functional option)的设计，更多关于Go语言变长参数的妙用，可以参考我的专栏文章
[《变长参数函数的妙用》](https://www.imooc.com/read/87/article/2424)。

接下来，我们再看看reader和updater对单件函数db.DB的使用，以reader为例：

```
// github.com/bigwhite/experiments/blob/master/database-singleton/pkg/reader/reader.go
package reader
import (
"log"
"time"
"github.com/bigwhite/testdboper/pkg/db"
"github.com/bigwhite/testdboper/pkg/model"
)
func dumpEmployee() {
var rs []model.Employee // rs: record slice
d := db.DB()
d.Find(&rs)
log.Println(rs)
}
func Run(quit <-chan struct{}) {
tk := time.NewTicker(5 * time.Second)
for {
select {
case <-tk.C:
dumpEmployee()
case <-quit:
return
}
}
}
```


我们看到，reader的Run函数通过定时器每隔5s读取数据库表employee的内容，并输出。dumpEmployee函数通过db.DB非常容易的获取到访问数据库的实例，再也无需自行管理数据库的打开和关闭操作了。

最后，我们说一下DB连接的释放。我们在上面的代码中并没有看到显式的db连接的释放，因此在这样的程序中，始终都需要访问和操作数据库。释放db连接的时候，也是程序退出的时候，当进程退出，与db之间的连接会自动释放，因此无需再显式释放。

注：对于mysql而言，我们可以通过下面命令查看数据库的当前连接数：


```
mysql> show status like 'Threads%';
+-------------------+-------+
| Variable_name | Value |
+-------------------+-------+
| Threads_cached | 2 |
| Threads_connected | 3 |
| Threads_created | 5 |
| Threads_running | 2 |
+-------------------+-------+
4 rows in set (0.00 sec)
```


以上示例代码可以在[这里](https://github.com/bigwhite/experiments/tree/master/database-singleton) https://github.com/bigwhite/experiments/tree/master/database-singleton 下载 。

### 附录

- mysql安装设置(on ubuntu)

```
// ubuntu 18.04, mysql 5.7.33
安装mysql：
$apt-get install mysql-server mysql-client
查看mysql安装成功与否：
$ps -ef|grep mysql
mysql 23965 1 0 22:55 ? 00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid
设置root密码：
$cat /etc/mysql/debian.cnf
# Automatically generated for Debian scripts. DO NOT TOUCH!
[client]
host = localhost
user = debian-sys-maint
password = xxxxxxxxxx
socket = /var/run/mysqld/mysqld.sock
使用debian-sys-maint/xxxxxxxxxx 登录数据库：
$mysql -u debian-sys-maint -p
Enter password:
Welcome to the MySQL monitor. Commands end with ; or \g.
Your MySQL connection id is 4
Server version: 5.7.33-0ubuntu0.18.04.1 (Ubuntu)
Copyright (c) 2000, 2021, Oracle and/or its affiliates.
Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.
Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
mysql> use mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A
Database changed
mysql> update user set authentication_string=PASSWORD("root123") where user='root';
Query OK, 1 row affected, 1 warning (0.01 sec)
Rows matched: 1 Changed: 1 Warnings: 1
mysql> update user set plugin="mysql_native_password";
Query OK, 1 row affected (0.00 sec)
Rows matched: 4 Changed: 1 Warnings: 0
mysql> flush privileges;
Query OK, 0 rows affected (0.01 sec)
root密码生效：
重启mysql服务后，root密码才能生效。
$systemctl restart mysql.service
```


- demo1数据和employee表的创建

```
>create database demo1;
> CREATE TABLE `employee` (
`id` bigint unsigned NOT NULL AUTO_INCREMENT,
`name` varchar(255) NOT NULL,
`age` int NOT NULL,
`gender` varchar(8) NOT NULL,
`birthday` char(14) NOT NULL,
`email` varchar(255) DEFAULT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```


“Gopher部落”知识星球开球了！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！星球首开，福利自然是少不了的！2020年年底之前，8.8折(很吉利吧^_^)加入星球，下方图片扫起来吧！

![](../../assets/d3fad3142fe3cc39.png)


Go技术专栏“[改善Go语⾔编程质量的50个有效实践](https://www.imooc.com/read/87)”正在慕课网火热热销中！本专栏主要满足广大gopher关于Go语言进阶的需求，围绕如何写出地道且高质量Go代码给出50条有效实践建议，上线后收到一致好评！欢迎大家订阅！目前该技术专栏正在新春促销！关注我的个人公众号“iamtonybai”，发送“go专栏活动”即可获取专栏专属优惠码，可在订阅专栏时抵扣20元哦。

![](../../assets/d8e58987c0d3be58.png)


我的网课“[Kubernetes实战：高可用集群搭建、配置、运维与应用](https://coding.imooc.com/class/284.html)”在慕课网热卖中，欢迎小伙伴们订阅学习！

![img{512x368}](../../assets/e9f90df4cc2580e5.png)


[我爱发短信](https://tonybai.com/)：企业级短信平台定制开发专家 https://tonybai.com/。smspush : 可部署在企业内部的定制化短信平台，三网覆盖，不惧大并发接入，可定制扩展； 短信内容你来定，不再受约束, 接口丰富，支持长短信，签名可选。2020年4月8日，中国三大电信运营商联合发布《5G消息白皮书》，51短信平台也会全新升级到“51商用消息平台”，全面支持5G RCS消息。

著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博：https://weibo.com/bigwhite20xx
- 微信公众号：iamtonybai
- 博客：tonybai.com
- github: https://github.com/bigwhite
- “Gopher部落”知识星球：https://public.zsxq.com/groups/51284458844544

微信赞赏：

![img{512x368}](../../assets/8ac1c4a4c5c59f4e.jpg)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2021, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论