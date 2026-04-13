---
title: WordPress迁移到Docker容器
url: https://tonybai.com/2014/11/01/migrate-wordpress-into-docker-container/
published: '2014-11-01'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# WordPress迁移到Docker容器

目前的[Blog](http://tonybai.com)托管在同事的一个共享主机上，由于种种原因，这个主机即将无法使用，我只能再次迁移我的[WordPress](http://wordpress.org)，不得不感叹：铁打的Wordpress，流水的主机啊！

这次迁移前，我仔细考量了一番，如何能让以后可能出现的Wordpress迁移最简化呢？虽然现在的迁移也不是特别复杂。我想到了近期研究的 [Docker](http://tonybai.com/tag/docker)。目前很多国外的VPS都已经支持了[Docker](http://docker.com)，我只需要在本地制作好Docker容器导出，再导入目标VPS的Docker中即可完成迁 移。在真正做迁移前，我打算在实验环境下测试一下。以下是将Wordpress迁移到Docker容器的测试过程。

**一、容器准备**

**1、下载镜像**

WordPress主要就是两个部分组成：wordpress程序 + mysql数据库。Docker官方registery提供了Wordpress和MySQL的image，我们可以直接pull使用。考虑到外站速度较 慢，这里我使用了国内镜像站点dockerpool.com提供的镜像了。

sudo docker pull dl.dockerpool.com:5000/wordpress:4.0.0

sudo docker pull dl.dockerpool.com:5000/mysql:5.6.20

考虑到使用phpmyadmin操作mysql数据的方便性，我又找了一个phpmyadmin的image：

sudo docker pull corbinu/docker-phpmyadmin

**2、启动容器**

mysql作为数据库数据存储镜像，在启动是会被wordpress和phpmyadmin link的，这样后两者在各自容器内才能顺利访问mysql服务和数据库。

按顺序启动容器（mysql为最先启动）：

sudo docker run –name **blogmysql** -e MYSQL_ROOT_PASSWORD=root -d dl.dockerpool.com:5000/mysql:5.6.20

sudo docker run –name blogwordpress –link **blogmysql**:mysql -p 80:80 -d dl.dockerpool.com:5000/wordpress:4.0.0

sudo docker run –name blogphpmyadmin -e MYSQL_USERNAME=root –link **blogmysql**:mysql -p 8000:80 -d corbinu/docker-phpmyadmin

三个容器均可以顺利启动。mysql数据库的访问方式是root/root。wordpress默认为80端口，phpmyadmin用8000端口访问，你可以试试http://localhost:80和http://localhost:8000。

$ sudo docker ps

CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES

a30540120b5d corbinu/docker-phpmyadmin:latest "/bin/sh -c phpmyadm 5 seconds ago Up 3 seconds 0.0.0.0:8000->80/tcp blogphpmyadmin

a88c456bf840 dl.dockerpool.com:5000/wordpress:4 "/entrypoint.sh apac 37 seconds ago Up 35 seconds 0.0.0.0:80->80/tcp blogwordpress

1b6f84f428e3 dl.dockerpool.com:5000/mysql:5.6.20 "/entrypoint.sh mysq 45 seconds ago Up 44 seconds 3306/tcp blogmysql

访问phpmyadmin，使用root/root登录后，我们可以看到主页上得数据库信息：

Database server

Server: 172.17.0.2 via TCP/IP

Server type: MySQL

Server version: 5.6.20 – MySQL Community Server (GPL)

Protocol version: 10

User: root@172.17.0.4

Server charset: UTF-8 Unicode (utf8)

Web server

nginx/1.7.1

Database client version: libmysql – 5.6.20

PHP extension: mysqli Documentation

phpMyAdmin

Version information: 4.2.7.1, latest stable version: 4.2.10.1

**3、install wordpress**

第一次通过http://locahost:80访问wordpress，便进入了wordpress安装流程，这个镜像中携带的版本是wordpress 4.0.0。

step1：

选择安装语言：简体中文

step2:

填写站点名称、用户名、密码、邮件等。

安装ok后，你就进入到了Wordpress 4.0.0的管理后台。


**二、迁移**

**1、导出备份**

目前的Blog使用的是DirectAdmin管理面板。通过DirectAdmin我们可以将当前的Wordpress站点整个下载，下载包中包含:

$ls

backup/ domains/

domains/tonybai.com/public_html下就是你的wordpress程序以及相关配置、插件等数据。

backup/xxx.sql就是数据库导出文件。

我们需要将这两部分恢复到Docker中。

**2、数据表导入**

我曾经试过通过WP-DB-Backup导出sql文件，再通过phpmyadmin导入的方法，但WP-DB-Backup导出的sql文件较大（>2M）,无法满足phpmyadmin对导入文件的要求（<=2m)，于是总是失败。之后决定通过mysql直接执行sql脚本导入。

首先通过phpmyadmin在mysql中建立数据库xx_db，编码：utf8_general_ci。

然后将上面的backup/xxx.sql拷贝到blogmysql容器中，比如就放在/root/下。然后通过nscenter进入到blogmysql容器中，切换到/usr/local/mysql/bin下，执行如下命令：

$ ./mysql -u root -p

输入root，进入mysql

在mysql下执行：

mysql > use xx_db

mysql > source /root/xxx.sql

如无意外，数据将顺利导入mysql的xx_db下。

**3、wordpress导入**

通过docker nsenter工具进入blogwordpress容器，进入/var/www目录下：

$ cp -r html html.bak

$ rm -fr html/*

再将上面提到的public_html下面的文件悉数copy到html下。

打开浏览器，输入http://localhost:80，会出现错误提示："您在 wp-config.php 文件中提供的数据库用户名和密码可能不正确，或者无法连接到 localhost 上的数据库服务器"。

我们需要修改wp-config.php中的数据库连接信息。

define('DB_NAME', 'bigwhite_db');

define('DB_USER', 'root');

define('DB_PASSWORD', 'root');

define('DB_HOST', 'mysql');

再次刷新浏览器，依旧无法正确打开。重启blogwordpress容器后,wordpress终于可以打开了，但打开的wordpress管理页面连接 的数据库不对，我的文章并没有出现在文章列表中，这是一个新库。于是通过docker logs查看blogwordpress日志，进入blogwordpress查看wp-config.php的内容，我惊奇的发现：wp- config.php中的DB_NAME被改回'wordpress'了，而没有使用导入的"bigwhite_db"。

多次修改回bigwhite_db并重启容器后，这个值均被改为wordpress。无奈只好通过phpmyadmin删除wordpress库，重新创 建wordpress库并采用同样方法导入xx.sql，使得wordpress这个db与bigwhite_db拥有同样地内容。这回再打开 wordpress，一切尽在眼前。

迁移实验成功！这样我们将迁移后的容器导出，再导入你的支持docker的VPS中，无需任何其余操作即可完成真正的迁移。目前[Digital Ocean](http://www.digitalocean.com/)已经支持了Docker，Aliyun据说也拥抱了Docker。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

你好，对于docker不是很懂。想问个问题，如果修改或者增减docker中wordpress的代码等，需要如何操作呢。重启docker后，是否会重置。

能否出个 docker Let’s Encrypt https的教程