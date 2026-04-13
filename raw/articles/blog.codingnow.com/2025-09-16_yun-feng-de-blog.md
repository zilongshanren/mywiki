---
title: 云风的 BLOG
url: https://blog.codingnow.com/2025/09/
published: '2025-09-16'
source_blog: 云风的 BLOG
source_site: https://blog.codingnow.com/
category: game programming
fetched: '2026-04-13'
---

### 有惊无险的一次网站系统升级

好消息是：这个 blog 终于是 UTF-8 编码了。前些年老有人问我能不能把 RSS 输出改成 UTF-8 的，很多 RSS 阅读器不支持 gbk ，这次终于改过来了。

事情源于昨天下午的一次脑抽，我把网站机器的操作系统升级了。上次升级还是十多年前，真的是太老旧了。结果升完级一看，php 被强制升到了 7 ，我自己写的一些 php 程序（主要是留言板）坏掉了。

这些个程序是我在 2004 年重构 2002 年的代码完成的；而 2002 年是从网上随便找来的代码基础上改的。我正儿八经学习 PHP 是在 1997 年，2000 年后就没怎么更新 PHP 的知识了。上次网站升级的时候，PHP 从 4 强制升到 5 ，就乱改了一通，勉强让程序可以运行（开了一些兼容模式）。这次再看代码，简直是惨不忍睹。所以我在本地装了个 PHP8 ，打开 PHP 官网，好好学习了一下手册。然后把代码取下来，重新建了个 git 仓库，正儿八经的改了一下。把留言的部分删了，只留下了浏览旧信息的部分，勉强让它继续跑起来。等什么时候有空了，再用 PHP 或 Lua 重新做一个。

Apache 的配置语法变了，一开始 PHP 跑不起来，折腾了一下配置文件就可以了。

最大的麻烦是 MySQL ，这次强制升到了 8 。之前好像是 4 版或更老的版本。我打开 blog 管理后台一看，全是乱码。心想坏了，编码出问题了。Blog 全是静态页面。只在修改时才从数据库读出内容生成一遍静态页面。所以外面看是正常的。我赶紧关掉了 mysql 服务器，以免（有人留言等修改行为）造成二次伤害。

Blog 是在 2005 年建的，数据采用的是 gbk 编码。其实那一年我已知道未来 UTF-8 一定是主流，但脑子里想的是手机流量费用 3 分钱 1 K 。选用 GBK 而不是 UTF 8 可以为自己和读者省钱。记得那年我和有道的负责人周枫闲聊汉字编码问题，他说 GBK 编码还是有意义的，他们当时爬虫爬来的中文数据储存就是用的 GBK ，这样可以节省 1/3 的储存成本。

其实，当年于我更好的方案应该是储存使用 utf-8 ，只在传输层用 GBK ，以后改起来也方便。可惜当年我自我折腾的能力远比不上现在，用了个别人开发的 blog 系统就懒得折腾了。在古旧得 Mysql 数据库中，是不储存文本编码类型的。基本上是你写什么数据编码就存什么。后来升级后，那些没有标注的编码字段就统一标注成了 latin1/latin1*swedish*ci 。但实际我储存的是 gbk ，读出来自然就乱了。

一开始我觉得，这种问题肯定无数人解决过，google 一下就好。我把通讯编码改成 binary ，select 了几段文本，查看二进制表达，确认是 GBK 编码，数据没有（因为升级或后续操作）损坏。打包了一下数据库仓库目录，想着问题总能解决的吧。

我没有正儿八经的用 mysql 开发过，每次用到 mysql ，都是现学现卖。结果 google 了半天没找到解决方案，有点慌了。估计是像我这样跨越 10 年升级的用户太少了。[在 mysql 官网上是这样写的](https://dev.mysql.com/doc/refman/8.4/en/charset-conversion.html)：

A special case occurs if you have old tables from before MySQL 4.1 where a nonbinary column contains values that actually are encoded in a character set different from the server's default character set. For example, an application might have stored sjis values in a column, even though MySQL's default character set was different. It is possible to convert the column to use the proper character set but an additional step is required. Suppose that the server's default character set was latin1 and col1 is defined as CHAR(50) but its contents are sjis values. The first step is to convert the column to a binary data type, which removes the existing character set information without performing any character conversion: ... The next step is to convert the column to a nonbinary data type with the proper character set:


简单说就是，先把文本标注成二进制格式，然后再转为你确定的编码。之后就可以正确转换到 UTF-8 了。

但我试了一下还是搞不定，只好在推特上求助。网友中数据库专家肯定比我这种临时抱佛脚翻手册的强多了。感谢热心网友提供了很多方案，甚至私信教我 mysql 。上面的方案我搞不定是因为有些字段做了索引。需要先扔掉索引，转码完了再重建。虽然有人教我，但我对自己能正确操作 mysql 还是没太大信心。就把仓库拖到本地，本地安装了一套 mysql8 做实验。

最后，结合网友的建议以及我自己的判断。我决定先以 binary 传输格式用 mysqldump 导出数据库（大约 500M），然后再用文本转换的方式替换其中的编码，最后再想办法导回。

mysqldump -u root -p --default-character-set=binary

这里导出命令行一定要加 `--default-character-set=binary`

，否则内码会被当成 latin 而且转换一次，数据是乱的。

一开始觉得挺简单的，查看了导出数据也很完成，不就是 iconv 转换一下么？实际操作发现 iconv 转换有很多错误。如果忽略掉错误，最后就无法导回数据库。我查了一下 dump 文件，发现数据库的数据中居然混杂着一些 utf8 字符串。iconv 无法正确处理这种混杂的编码。而且 mysql 会将部分字符转义，尤其是引号。如果编码转换中除了问题，就有可能吃掉某些引号等有关的格式文本，就变成了错误格式的文件。

所以全文文本替换是有巨大风险的。思来想去，我自己写了个 Lua 程序，最低限度的解析了 dump 文件的词法，只把 binary 字符串挑出来，并对转义符做好转义。将转换过的文本，用自己的代码判断它是 GBK 还是 UTF8 ，挑选出 GBK 交给 iconv 处理，而 UTF-8 则原封不动。最后再将字符串加回转义符，保证符合 mysql 语法。

最终找到了 680 条 UTF-8 文本。我猜测是当年有几天尝试过把 blog 数据转为 UTF-8 编码，又发现不太对劲所以换回来，中间产生的一些混杂编码。

对于转换好的数据，那些字段编码标准还是 latin ，所以用一个简单的文本替换成 utf-8 即可。

sed -i 's/CHARSET=latin1/CHARSET=utf8mb4/g' backup_utf8.sql sed -i 's/COLLATE latin1_swedish_ci/COLLATE utf8mb4_unicode_ci/g' backup_utf8.sql

ps. 在本地 windows 上试验用 source 导入数据库时踩了个小坑。用反斜杠做路径会报错，必须用正斜杠绕开 mysql 的转义。

自此大功告成。

查看系统基本复原后，又连续升级了两个 LTS ，一直升级到 2024 LTS 版本。中间只碰到几个自己动过的软件配置文件问题。简单修一下即可。

估计又有十年可以不折腾它了。