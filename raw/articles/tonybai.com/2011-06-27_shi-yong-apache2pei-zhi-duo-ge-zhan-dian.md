---
title: 使用Apache2配置多个站点
url: https://tonybai.com/2011/06/27/configure-multiple-websites-with-apache2/
published: '2011-06-27'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用Apache2配置多个站点

部门虽然不是做Web开发的，但是部门内部很多服务器也是使用Apache作为Web Server的。不过一直一来我这边都是用一个Apache Server对应一套Web应用。不过今天有了新的要求：在一个已经部署了一套应用的Apache2上再部署另外一套应用。这也让我不得不深入了解一下Apache的配置。不过还好，过程还是顺利的，这里记下此文意在备忘，如果同时也能给大家带来一些有价值的参考那就再好不过了。

Ubuntu下安装好Apache2后(sudo apt-get install apache)，在任何配置都未做修改的初始情况下，我们看到的与虚拟站点有关的Apache2的初始配置如下：

Apache2主配置文件: /etc/apache2/apache2.conf。其最后两行为：

# Include the virtual host configurations:

Include /etc/apache2/sites-enabled/

显然/etc/apache2/sites-enabled下存放着有关虚拟站点（VirtualHost）的配置。经查看，初始情况下，该目录下包含一个符号连接：000-default -> ../sites-available/default

这里又引出另外一个配置目录：/etcc/apache2/sites-available。这个目录下放置了所有可用站点的真正配置文件，对于Enabled的站点，Apache2在sites-enabled目录建立一个到sites-available目录下文件的符号链接。

/etc/apache2/sites-available下有两个文件：default和default-ssl。000-default链接的文件为default，我们就以default为例，看看一个VirtualHost的配置是啥样的：

ServerAdmin webmaster@localhost

DocumentRoot /var/www


Options FollowSymLinks

AllowOverride None



Options Indexes FollowSymLinks MultiViews

AllowOverride None

Order allow,deny

allow from all


… …

DocumentRoot是这个站点的根目录，这样Apache2启动时会扫描/etc/apache2/sites-enabled中可用的website配置并加载。当用户访问localhost:80时，Apache2就将default站点根目录/var/www下的index.html作为请求的回应返回给浏览器，你就会欣赏到的就是/var/www/index.html这个文件中的内容了。

Apache2的默认站点我们不要去动它。我们新增站点配置来满足我们的要求。到这里我猜测一下你可能有两类需求：

一是如何配置根据访问的域名区分配置不通的站点？

二是在相同域名地址的情况下，如何通过访问不同的端口获得不同的站点？

我们先来看看第一种需求。第一种需求讲的是我要在一个Apache2服务器上配置两个站点：site1.com和site2.com。好，我们可以按照下面步骤来做：

* 建立配置文件

在sites-available中建立两个站点的配置文件site1_com和site2_com：

sudo cp default site1_com

sudo cp default site2_com

编辑这两个配置文件，以site1_com为例：


ServerAdmin webmaster@localhost

ServerName site1.com

DocumentRoot /var/www/site1_com


Options FollowSymLinks

AllowOverride None



Options Indexes FollowSymLinks MultiViews

AllowOverride None

Order allow,deny

allow from all


… …

注意上面配置中：ServerName、DocumentRoot和Directory是我们重点关注的配置点。site1的ServerName为site1.com，根目录为/var/www/site1_com，Directory同DocumentRoot。site2_com也做同样的改动。

* 在sites-enabled目录下建立符号链接：

sudo ln -s /etc/apache2/sites-available/site1_com /etc/apache2/sites-enabled/site1_com

sudo ln -s /etc/apache2/sites-available/site2_com /etc/apache2/sites-enabled/site2_com

* 在/var/www下建立site1_com和site2_com两个目录，然后修改目录所有者：

sudo chown -R www-data site1_com site2_com/

* 在site1_com和site2_com中各自创建一个index.html文件，用于测试使用。

以site1_com下index.html为例，其内容为：Welcome To Site1。

* 重启Apache2(sudo /init.d/apache2 restart)使配置生效。

* 修改/etc/hosts文件，便于测试。

添加如下两行：

127.0.0.1 site1.com

127.0.0.1 site2.com

* 打开浏览器，输入http://site1.com，之后不出意外你就会看到”Welcome to Site1“字样。

第二类需求是希望通过端口号来区分虚拟站点。这个也不难，一些配置方法与上面内容雷同，这里就不详说了。

比如以site2为例：我通过80端口访问site2，可看到"Welcome to Site2”，从8080端口访问site2，则会看到"Welcome to Site2 through 8080"。我们如何配置呢？

* 首先我们得让apache2监听端口8080

修改/etc/apache2/ports.conf，增加两行：

NameVirtualHost *:8080

Listen 8080

* 在/etc/apache2/sites-available/下增加site2_com_8080，并在sites-enabled下建立符号连接。

site2_com_8080的主要配置如下：

ServerAdmin webmaster@localhost

ServerName site2.com

DocumentRoot /var/www/site2_com_8080


Options FollowSymLinks

AllowOverride None



Options Indexes FollowSymLinks MultiViews

AllowOverride None

Order allow,deny

allow from all


… …

在/var/www下建立site2_com_8080目录，方法同上。

重启Apache2，访问http://site2.com:8080，我们将看到“Welcome to Site2 through 8080”。


© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

VirtualHost的配置虽说不难，每次重复也很烦人。

推荐一个叫 virtualhost.sh 的脚本：

http://code.google.com/p/virtualhost-sh/

建立虚拟站点只需

virtualhost.sh site1.com

hosts 的设置还有网站根目录的生成，都给你弄好了，非常方便。