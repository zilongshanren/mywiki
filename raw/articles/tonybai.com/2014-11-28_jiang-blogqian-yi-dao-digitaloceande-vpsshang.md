---
title: 将Blog迁移到DigitalOcean的VPS上
url: https://tonybai.com/2014/11/28/migrate-blog-to-digitalocean-vps/
published: '2014-11-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 将Blog迁移到DigitalOcean的VPS上

自从2012年初将Blog[从Blogbus搬出来](http://tonybai.com/2012/02/29/a-new-departure- of-my-blog-move-from-blogbus-to-wordpress/)放到同事代理的虚拟主机上后，Blog运行一直很稳定，我也算 是比较满意。但同事的主机代理生意这两年来每况愈下，这促使他在前些时候做出了在今年年末放弃这门生意的决定，于是我又不得不为Blog另找落脚儿地了。

这次不想再单纯的买Wordpress虚拟主机了，一来功能有限，二来国外的入门级VPS价格已经与虚拟主机价格逐渐缩小，尤其是像 [DigitalOcean](http://www.digitalocean.com)这样的后起之秀，5$/mon的入门级配置VPS基本可以满足我的应用。于是DigitalOcean VPS就成为了我的购买目标。DigitalOcean这两年推广力度大，其Promo code的优惠有时可达20$以上，去年黑色星期五当天就给出了50$的优惠码。于是我期望着今天（2014黑色星期五）DigitalOcean的 50$优惠码能再现江湖。

但事与愿违，当时间走入美国当地时间星期五后，网上哪些所谓50$的Promo code依旧无法正常使用。无奈只能退而求次，使用"SHIPITFAST10"这个10$的优惠码，对于入门级VPS来说，10$也够试用两个月的了。

Digital Ocean VPS的注册和购买流程非常简单，按照官方提示一步一步做即可。这里要注意的是如果选择信用卡支付，务必一次填对信用卡信息，否则account就会短暂 无法使用，你需要fill out一个Form，提交给客服人工验证才能解除对你account的封锁。

接下来就是稍详细的说明Wordpress blog迁移到Digital Ocean VPS的步骤了，希望能对大家有所帮助。

**一、备份WordPress Blog**

网上关于迁移WordPress的方法有许多方案，之前在测试[将WordPress迁移到Docker容器](http://tonybai.com/2014/11/01/migrate-wordpress-into-docker-container/)中时，我采用的是数据表导出导入+WordPress程序覆盖的方式，这次我依旧采用此方法。

现有的Blog用的是[DirectAdmin](http://www.directadmin.com)的后台管理面板，支持全站备份，备份后的文件为：backup-Nov-27-2014-1.tar.gz。这个压缩包中有两个重要的组件（解压后你就可以看到）：

– backup/tonybai_db.sql

– domains/tonybai.com/public_html/


我们要迁移的就是这两个组件。第一个.sql文件就是我们导出的数据库表，需要导入到新主机中的新库中。而第二个则是Wordpress安装后的文件集合，用于直接覆盖目标主机上对应的Wordpress文件包的。

**二、创建Digital Ocean VPS Droplet**

在填写完信用卡，利用优惠码充值账户成功后，就可以创建Droplet了。Droplet是DO的术语，理解成一个VPS实例即可。Droplet的创建 体验不错，DO已经准备好了各种VPS常用的应用组合以及OS供选择。我选择了5$/mon的Ubuntu 14.04 x64 + WordPress的组合，机房选择San Francisco 1。确认后，DO会开始创建Droplet操作，不到1分钟，Droplet就创建完毕了。如果不用ssh key，则VPS的root密码会发到你的注册邮箱中。有了root和密码，我们就可以通过"ssh root@YOUR_VPS_IP"访问你的VPS了。

首次后台登陆VPS，VPS会强制你修改root登陆密码。

**三、初始安装WordPress**

现在我们的VPS上已经安装好了WordPress运行所需要的所有软件了，包括apache2、mysql等。修改/etc/hosts，将自己的域名tonybai.com映射为VPS IP。

访问tonybai.com，WordPress的自安装程序启动，按照[提示](https://www.digitalocean.com /community/tutorials/one-click-install-wordpress-on-ubuntu-14-04-with- digitalocean)一步一步即可安装好Wordpress，这里带的Wordpress是4.0.0版本（注意：我们后续是要覆盖掉这个 WordPress的）。

安装好后，再访问tonybai.com就可以看到默认安装后的一篇example blog了。

现在我们进入tonybai.com/wp-admin页面，Apache弹出一个登陆框，在DO官方文档提到过，/wp-admin初始情况使用了 apache的.htaccess credential保护机制了，我们需要输入用户名密码才能进入wp-admin页面。这个用户名密码就在/root/WORDPRESS里。

**四、导表**

接下来，我们先将backup/tonybai_db.sql导入mysql数据库。

mysql的数据库访问密码在/root/.my.cnf中，用户名是root。

管理mysql我们更多使用phpmyadmin工具，于是通过apt-get install phpmyadmin -y安装一个。

为了通过Web页面访问到phpmyadmin，我们还需执行以下两个步骤：

在/etc/apache2/apache2.conf尾部添加一行：

Include /etc/phpmyadmin/apache.conf

重启apache2：service apache2 restart

之后通过tonybai.com/phpmyadmin访问phpmyadmin工具。登录时使用mysql的root和密码即可。

进入phpmyadmin后，我们可以看到前面的Wordpress安装过程在mysql中建立了名为wordpress的数据库以及名为 wordpress的数据库用户。但我之前的blog使用的数据库用户和数据库并非wordpress，而是tonybai_user和tonybaidb，于是我们需要自己创建 tonybaidb数据库以及tonybai_user这个数据库账号。

创建tonybaidb时，注意使用utf8_general_ci字符集。

创建tonybai_user数据库账户时，注意其权限仅局限于localhost发起的访问以及tonybaidb这个数据库，其密码设置为原blog wp-config.php中的数据库密码。

由于phpmyadmin导入的文件不能超过2M，因此我们只能通过后台导表：

mysql -u root -p

mysql> use tonybai_db

database changed

mysql> source ./tonybai_db.sql

**五、替换Wordpress安装文件**

默认下wordpress安装到了/var/www下。我们需要将domains/tonybai.com/public_html替换掉/var/www目录：

cd /var

mv www www.bak

将domain/tonybai.com/public_html cp到/var/下，改名为www

chown -R www-data www

chgrp -R www-data www

剩下的就是访问tonybai.com即可。

是不是熟悉的页面和风格又展现在你眼前了！

**六、创建SnapShot**

DO提供两种备份方式Snapshot和Backups，其中Snapshot目前还是免费的，但backup服务是要付费的。Snapshot创建的前提是先stop这个Droplet。建议导入blog、访问正常后，马上建立一个Droplet的Snapshot。

**七、其它**

由于是入门型VPS，其内存仅有512M，并且默认情况下Ubuntu 14.04 VPS没有创建Swap，考虑到VPS的高可用性，我们还是需要自己动手创建一些swap空间，以供不时之需，创建步骤很简单，执行下面命令即可：

fallocate -l 512M /swapfile

mkswap /swapfile

swapon /swapfile

swapon -s 查看一下当前swap，可以看到：

Filename Type Size Used Priority

/swapfile file 524284 0 -1

另外调试过程中发现访问tonybai.com/feed出现如下错误：

Forbidden：

You don't have permission to access /feed/ on this server.

Google、Baidu许久才发现真正问题所在：我的旧Blog目录下有一个feed子目录，把这个目录删除即可。

© 2014, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

感觉还不错啊。

速度快吗？

速度感觉不错，感觉比以前的主机快一些。但mysql宕了两次，正在查原因。呵呵。

digitalocean的新加坡机房是坑,不要跳.美国还好. 可能的情况下,还是首选Linode 10$ 很爽

谢谢博主分享的Code，我才充了25$。使用得挺好的，速度挺快，用的是美国的节点。

另外512MB带Ubuntu是不是没有桌面的？我现在用Centos，不是太熟悉。

默认都是server ，不带desktop。不过可以自行安装吧。但远程桌面访问速度估计不快。毕竟是境外主机。