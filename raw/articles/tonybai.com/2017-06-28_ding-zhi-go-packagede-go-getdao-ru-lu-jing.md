---
title: 定制Go Package的Go Get导入路径
url: https://tonybai.com/2017/06/28/set-custom-go-get-import-path-for-go-package/
published: '2017-06-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 定制Go Package的Go Get导入路径

近期Go team的组员[Jaana B. Dogan](https://rakyll.org/)，网名：[rakyll](https://github.com/rakyll/)开源了一个小工具：[Go Vanity URLs](https://github.com/GoogleCloudPlatform/govanityurls)。这个小工具可以帮助你快速为你的[Go](http://tonybai.com/tag/go) package定制Go get的导入路径（同样也是package被使用时的import路径）。

说到go package的go get导入路径，我们最常见和常使用的domain name就是github.com了，比如：beego包的go get导入路径就是 go get github.com/astaxie/beego。我们还经常看到一些包，它们的导入路径很特殊，比如：go get golang.org/x/net、go get gopkg.in/yaml.v2等（虽然net、yaml这些包实际的repo也是存在于github.com上的），这些就是定制化的package import path，它们有诸多好处：

-
可以为package设置

**canonical import path**，即权威导入路径这是在

[Go 1.4](http://tonybai.com/2014/11/04/some-changes-in-go-1-4/)版本中加入的概念。Go package多托管在几个知名的代码管理网站，比如：github.com、bitbucket.org等，这样默认情况下package的import path就是github.com/xxx/package、bitbucket.org/xxx/package等。一旦某个网站关门大吉了，那package代码势必要迁移到其他站点，这样package的import path就要发生改变，这会给package的用户造成诸多不便，比如之前的code.google.com关闭就给广大的gopher带来了很大的“伤害”。canonical import path就可以解决这个问题。package的用户只需要使用package的canonical import path，这样无论package的实际托管网站在哪，对package的用户都不会带来影响。 -
便于组织和个人对package的管理

组织和个人可以将其分散托管在不同代码管理网站的package统一聚合到组织的官网名下或个人的域名下，比如：golang.org/x/net、gopkg.in/xxx等。

-
package的import路径可以更短、更简洁

有些时候，github.com上的go package的import path很长、很深，并不便于查找和书写，通过定制化import path，我们可以使用更短、更简洁的域名来代替github.com仓库下的多级路径。


不过rakyll提供的govanityurls仅能运行于Google的[app engine](https://cloud.google.com/appengine/)上，这对于国内的Gopher们来说是十分不便的，甚至是不可用的，于是这里[fork了rakyll的repo](https://github.com/bigwhite/govanityurls)，并做了些许修改，让[govanityurls](https://github.com/bigwhite/govanityurls)可以运行于普通的vps主机上。

## 一、govanityurls原理

govanityurls的原理十分简单，它本身就好比一个“导航”服务器。当go get将请求发送给govanityurls时，govanityurls将请求中的repo的真实地址返回给go get，后续go get再从真实的repo地址获取package数据。

![img{512x368}](../../assets/0075cd8e742b225d.png)


可以看出go get第一步是尝试获取自定义路径的包的真实地址，govanityurls将返回一个类似如下内容的http应答(针对go get tonybai.com/gowechat请求)：

```
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta name="go-import" content="tonybai.com/gowechat git https://github.com/bigwhite/gowechat">
<meta name="go-source" content="tonybai.com/gowechat ">
<meta http-equiv="refresh" content="0; url=https://godoc.org/tonybai.com/gowechat">
</head>
<body>
Nothing to see here; <a href="https://godoc.org/tonybai.com/gowechat">see the package on godoc</a>.
</body>
</html>
```


## 二、使用govanityurls

关于govanityurls的使用，可以参考其[README.md](https://github.com/bigwhite/govanityurls)，这里以一个demo来作为govanityurls的使用说明。

### 1、安装govanityurls

安装方法：

```
$go get github.com/bigwhite/govanityurls
$govanityurls
govanityurls is a service that allows you to set custom import paths for your go packages
Usage:
govanityurls -host [HOST_NAME]
-host string
custom domain name, e.g. tonybai.com
```


和rakyll提供的govanityurls不同的是，这里的govanityurls需要外部传入一个host参数(比如：tonybai.com)，而在[原版](https://github.com/GoogleCloudPlatform/govanityurls)中这个host是由[google app engine](https://cloud.google.com/appengine/)的API提供的。

### 2、配置vanity.yaml

vanity.yaml中配置了host下的自定义包的路径以及其真实的repo地址：

```
/gowechat:
repo: https://github.com/bigwhite/gowechat
```


上面这个配置中，我们实际上为gowechat这个package定义了tonybai.com/gowechat这个go get路径，其真实的repo存放在github.com/bigwhite/gowechat。当然这个vanity.yaml可以配置N个自定义包路径，也可以定义多级路径，比如：

```
/gowechat:
repo: https://github.com/bigwhite/gowechat
/x/experiments:
repo: https://github.com/bigwhite/experiments
```


### 3、配置反向代理

govanityurls默认监听的是8080端口，这主要是考虑到我们通常会使用主域名定制路径，而在主域名下面一般情况下都会有其他一些服务，比如：主页、博客等。通常我们都会用一个反向代理软件做路由分发。我们针对gowechat这个repo定义了一条[nginx](http://tonybai.com/2016/11/17/nginx-config-hot-reloading-approach-for-kubernetes-cluster) location规则：

```
// /etc/nginx/conf.d/default.conf
server {
listen 80;
listen 443 ssl;
server_name tonybai.com;
ssl_certificate /etc/nginx/cert.crt;
ssl_certificate_key /etc/nginx/cert.key;
ssl on;
location /gowechat {
proxy_pass http://10.11.36.23:8080;
proxy_redirect off;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
}
}
```


这里为了方便，我既在80端口提供http服务，也在443端口提供了https服务。这里的10.11.36.23就是我真正部署govanityurls的host（一台thinkcenter PC）。/etc/nginx/cert.key和/etc/nginx/cert.crt可以通过下面命令生成：

```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/cert.key -out /etc/nginx/cert.crt
CN填tonybai.com
```


注意：修改两个文件的owner权限，将其owner改为nginx worker process的user，我这里是www-data(chown www-data:www-data /etc/nginx/cert.*)。

### 4、测试govanityurls

我在我的mac上修改了一下/etc/hosts，添加一条路由：

```
10.11.36.23 tonybai.com
```


我们来go get tonybai.com/gowechat：

```
$go get -v -insecure tonybai.com/gowechat
Fetching https://tonybai.com/gowechat?go-get=1
https fetch failed: Get https://tonybai.com/gowechat?go-get=1: EOF
Fetching http://tonybai.com/gowechat?go-get=1
Parsing meta tags from http://tonybai.com/gowechat?go-get=1 (status code 200)
get "tonybai.com/gowechat": found meta tag main.metaImport{Prefix:"tonybai.com/gowechat", VCS:"git", RepoRoot:"https://github.com/bigwhite/gowechat"} at http://tonybai.com/gowechat?go-get=1
tonybai.com/gowechat (download)
package tonybai.com/gowechat: no buildable Go source files in /Users/tony/Test/GoToolsProjects/src/tonybai.com/gowechat
$ls /Users/tony/Test/GoToolsProjects/src/tonybai.com/gowechat
LICENSE README.md mp/ pb/ qy/
```


我们可以看到tonybai.com/gowechat被成功get到本地，并且import path为tonybai.com/gowechat，其他包可以按照这个定制的gowechat的导入路径import gowechat package了。

上面例子中，我们给go get传入了一个-insecure的参数，这样go get就会通过http协议去访问tonybai.com/gowechat了。我们试试去掉-insecure，不过再次执行前需先将本地的tonybai.com/gowechat包删除掉。

```
$go get -v tonybai.com/gowechat
Fetching https://tonybai.com/gowechat?go-get=1
https fetch failed: Get https://tonybai.com/gowechat?go-get=1: x509: certificate signed by unknown authority
package tonybai.com/gowechat: unrecognized import path "tonybai.com/gowechat" (https fetch: Get https://tonybai.com/gowechat?go-get=1: x509: certificate signed by unknown authority)
```


虽然我已经关掉了git的http.sslVerify，但go get的执行过程还是检查了server端证书是未知CA签署的并报错，原来这块的verify是go get自己做的。关于httpskey和证书(.crt)的相关知识，我在《[Go和HTTPS](http://tonybai.com/2015/04/30/go-and-https)》一文中已经做过说明，不是很熟悉的童鞋可以移步那篇文章。

我们来创建CA、创建server端的key（cert.key），并用创建的CA来签署server.crt：

```
$ openssl genrsa -out rootCA.key 2048
$ openssl req -x509 -new -nodes -key rootCA.key -subj "/CN=*.tonybai.com" -days 5000 -out rootCA.pem
$ openssl genrsa -out cert.key 2048
$ openssl req -new -key cert.key -subj "/CN=tonybai.com" -out cert.csr
$ openssl x509 -req -in cert.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out cert.crt -days 5000
# ls
cert.crt cert.csr cert.key rootCA.key rootCA.pem rootCA.srl
```


我们将cert.crt和cert.key拷贝到ubuntu的/etc/nginx目录下，重启nginx，让其加载新的cert.crt和cert.key。然后将rootCA.pem拷贝到/etc/ssl/cert目录下，这个目录是ubuntu下存放CA公钥证书的标准路径。在测试go get前，我们先用curl测试一下：

```
# curl https://tonybai.com/gowechat
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta name="go-import" content="tonybai.com/gowechat git https://github.com/bigwhite/gowechat">
<meta name="go-source" content="tonybai.com/gowechat ">
<meta http-equiv="refresh" content="0; url=https://godoc.org/tonybai.com/gowechat">
</head>
<body>
Nothing to see here; <a href="https://godoc.org/tonybai.com/gowechat">see the package on godoc</a>.
</body>
</html>
```


curl测试通过！

我们再来看看go get：

```
# go get tonybai.com/gowechat
package tonybai.com/gowechat: unrecognized import path "tonybai.com/gowechat" (https fetch: Get https://tonybai.com/gowechat?go-get=1: x509: certificate signed by unknown authority)
```


问题依旧！难道go get无法从/etc/ssl/cert中选取适当的ca证书来做server端的cert.crt的验证么？就着这个问题我在go官方发现了一个类似的issue: [#18519](https://github.com/golang/go/issues/18519) 。从中得知，go get仅仅会在不同平台下参考以下几个certificate files：

```
$GOROOT/src/crypto/x509/root_linux.go
package x509
// Possible certificate files; stop after finding one.
var certFiles = []string{
"/etc/ssl/certs/ca-certificates.crt", // Debian/Ubuntu/Gentoo etc.
"/etc/pki/tls/certs/ca-bundle.crt", // Fedora/RHEL 6
"/etc/ssl/ca-bundle.pem", // OpenSUSE
"/etc/pki/tls/cacert.pem", // OpenELEC
"/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem", // CentOS/RHEL 7
}
```


在ubuntu上，/etc/ssl/certs/ca-certificates.crt是其参考的数字证书。因此要想go get成功，我们需要将我们rootCA.pem加入到/etc/ssl/certs/ca-certificates.crt中去，最简单的方法就是：

```
$ cat rootCA.pem >> /etc/ssl/certs/ca-certificates.crt
```


当然，ubuntu也提供了管理根证书的命令update-ca-certificates，可以看其manual学学如何更新/etc/ssl/certs/ca-certificates.crt，这里就不赘述了。

更新后，我们再来go get：

```
# go get -v tonybai.com/gowechat
Fetching https://tonybai.com/gowechat?go-get=1
Parsing meta tags from https://tonybai.com/gowechat?go-get=1 (status code 200)
get "tonybai.com/gowechat": found meta tag main.metaImport{Prefix:"tonybai.com/gowechat", VCS:"git", RepoRoot:"https://github.com/bigwhite/gowechat"} at https://tonybai.com/gowechat?go-get=1
tonybai.com/gowechat (download)
package tonybai.com/gowechat: no buildable Go source files in /root/go/src/tonybai.com/gowechat
```


go get成功！

## 三、小结

- 使用
[govanityurls](https://github.com/bigwhite/govanityurls)可以十分方便的为你的go package定制go get的导入路径； - 一般使用nginx等反向代理放置在govanityurls前端，便于同域名下其他服务的开展；
- go get默认采用https访问，自签署的ca和server端的证书问题要处理好。如果有条件的话，还是用用
[letsencrypt](https://letsencrypt.org/)等提供的免费证书吧。

微博：[@tonybai_cn](http://weibo.com/bigwhite20xx)

微信公众号：iamtonybai

github.com: https://github.com/bigwhite

© 2017, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

这个只能改掉程序本身直接依赖的import path，而依赖包所依赖的import path无法改变是吗？

是的。

公司私有gitlab的端口用的不是标准端口80和443，go get时提示import path中不能包含:这个字符，govanityurls也不能解决吧

可以啊。你可以读一下 我的这篇文章：使用govanityurls让私有代码仓库中的go包支持go get – https://tonybai.com/2017/06/30/go-get-go-packages-in-private-code-repo-by-govanityurls