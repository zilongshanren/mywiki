---
title: 从简单到强大：再次探索Caddy服务器的魅力
url: https://tonybai.com/2024/11/07/exploring-caddy/
published: '2024-11-07'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 从简单到强大：再次探索Caddy服务器的魅力

![](../../assets/f5cc4b500317e21c.png)


[本文永久链接](https://tonybai.com/2024/11/07/exploring-caddy) – https://tonybai.com/2024/11/07/exploring-caddy

[Go语言诞生十多年来](https://tonybai.com/2023/11/11/go-opensource-14-years/)，社区涌现出众多优秀的Web服务器和反向代理解决方案。其中，最引人注目的无疑是[Caddy](https://caddyserver.com/)和[Traefik](https://github.com/traefik/traefik)。这两者都为开发者和系统管理员提供了更简单、更安全的现代化Web服务器和反向代理部署选项。尽管它们的目标略有不同，Caddy最初旨在满足开发者快速搭建反向代理的需求，特别关注配置的简易性，并在后期增加了自动HTTPS和全面的API支持；而Traefik则更强调云原生架构，适合基于微服务的应用，尤其是使用Docker或Kubernetes部署的场景，提供动态服务发现和灵活的路由能力。

我于2015年[首次体验了开源发布的Caddy](https://tonybai.com/2015/06/04/caddy-a-web-server-in-go/)，其超简单的配置确实给我留下了深刻的印象。之后也一直关注着Caddy的发展，Caddy在支持通过[ACME协议](https://datatracker.ietf.org/doc/html/rfc8555)自动为服务的域名获取免费HTTPS证书的功能后，Caddy就被我[部署在自己的VPS上](https://m.do.co/c/bff6eed92687)，为[Gopher Daily](https://gopherdaily.tonybai.com)等站点提供反向代理服务，运行十分稳定。Caddy这一为域名自动获取免费HTTPS证书的功能是其简化站点部署初衷的延续，也为Caddy赢得的广泛的用户和赞誉，并且这一特性不仅使得Caddy在个人项目和小型部署中大受欢迎，也让它在企业级应用中占有一席之地。

近10年后，我打算在这篇文章中再次探索一下Caddy，了解一下如今的Caddy都提供哪些强大的功能特性，为后续更好地使用Caddy做铺垫。

注：Caddy发展了近10年，支持了很多标准特性以及非标准特性(由社区提供，caddy官方不提供保证和support)，这里仅就笔者感兴趣的特性做探索。目前Caddy依靠

[sponsor的赞助]进行着可持续演进，其所有标准功能都是免费的，但其作者[Matt Holt]也会为企业级赞助商进行定制功能开发。

## 1. Caddy的运行方法与基本配置

### 1.1 Caddy的启停

Caddy使用Go开发，因此继承了Go应用部署的一贯特点：**只有一个可执行文件**。将下载的Caddy放到\$PATH路径下，我们就可以在任意目录下执行它了：

```
$caddy version
v2.8.4 h1:q3pe0wpBj1OcHFZ3n/1nl4V4bxBrYoSoab7rL9BMYNk=
$caddy run
2024/10/11 07:56:24.664 INFO admin admin endpoint started {"address": "localhost:2019", "enforce_origin": false, "origins": ["//127.0.0.1:2019", "//localhost:2019", "//[::1]:2019"]}
```


这么启动后，caddy就会作为一个前台进程一直运行着，直到你停掉它。当然，我们也可以使用start命令将caddy作为后台进程启动：

```
$caddy start
2024/10/11 08:32:07.557 INFO admin admin endpoint started {"address": "localhost:2019", "enforce_origin": false, "origins": ["//127.0.0.1:2019", "//localhost:2019", "//[::1]:2019"]}
2024/10/11 08:32:07.557 INFO serving initial configuration
Successfully started Caddy (pid=31215) - Caddy is running in the background
```


使用stop命令可以停到该后台进程：

```
$caddy stop
2024/10/11 08:32:37.043 INFO admin.api received request {"method": "POST", "host": "localhost:2019", "uri": "/stop", "remote_ip": "127.0.0.1", "remote_port": "65178", "headers": {"Accept-Encoding":["gzip"],"Content-Length":["0"],"Origin":["http://localhost:2019"],"User-Agent":["Go-http-client/1.1"]}}
2024/10/11 08:32:37.043 WARN admin.api exiting; byeee!!
2024/10/11 08:32:37.043 INFO admin stopped previous server {"address": "localhost:2019"}
2024/10/11 08:32:37.043 INFO admin.api shutdown complete {"exit_code": 0}
```


### 1.2 使用Caddyfile配置站点信息

不过如此启动后的caddy并没有什么卵用，因为没有任何关于站点的配置信息。但caddy提供了config API（默认使用2019端口），我们可以使用下面方式访问该API：

```
$curl localhost:2019/config/
null
```


由于没有任何配置数据，该接口返回null。Caddy提供了强大的API可以在Caddy运行是动态设置站点配置信息，这个我们后续再说，因为首次使用Caddy时，开发者通常更愿意使用Caddyfile来提供初始配置信息，Caddyfile也是最初caddy开源时唯一支持的配置方式。我们以server1.com为例来看看在本地使用caddy为其建立反向代理有多简单。下面是Caddyfile的内容：

```
server1.com {
tls internal
reverse_proxy localhost:9001
}
```


然后我们基于该Caddyfile启动caddy，如果不显式传入配置文件，caddy默认使用当前目录(cwd)下的Caddyfile作为配置文件：

```
$caddy run
2024/10/11 08:49:36.916 INFO using adjacent Caddyfile
2024/10/11 08:49:36.920 INFO adapted config to JSON {"adapter": "caddyfile"}
2024/10/11 08:49:36.926 INFO admin admin endpoint started {"address": "localhost:2019", "enforce_origin": false, "origins": ["//localhost:2019", "//[::1]:2019", "//127.0.0.1:2019"]}
2024/10/11 08:49:36.928 INFO tls.cache.maintenance started background certificate maintenance {"cache": "0xc0005add80"}
2024/10/11 08:49:36.936 INFO http.auto_https server is listening only on the HTTPS port but has no TLS connection policies; adding one to enable TLS {"server_name": "srv0", "https_port": 443}
2024/10/11 08:49:36.936 INFO http.auto_https enabling automatic HTTP->HTTPS redirects {"server_name": "srv0"}
2024/10/11 08:49:36.964 WARN pki.ca.local installing root certificate (you might be prompted for password) {"path": "storage:pki/authorities/local/root.crt"}
2024/10/11 08:49:37.024 INFO warning: "certutil" is not available, install "certutil" with "brew install nss" and try again
2024/10/11 08:49:37.024 INFO define JAVA_HOME environment variable to use the Java trust
Password:
2024/10/11 08:49:41.629 INFO certificate installed properly in macOS keychain
2024/10/11 08:49:41.629 INFO http enabling HTTP/3 listener {"addr": ":443"}
2024/10/11 08:49:41.632 INFO http.log server running {"name": "srv0", "protocols": ["h1", "h2", "h3"]}
2024/10/11 08:49:41.632 INFO http.log server running {"name": "remaining_auto_https_redirects", "protocols": ["h1", "h2", "h3"]}
2024/10/11 08:49:41.632 INFO http enabling automatic TLS certificate management {"domains": ["server1.com"]}
2024/10/11 08:49:41.656 INFO tls cleaning storage unit {"storage": "FileStorage:/Users/tonybai/Library/Application Support/Caddy"}
2024/10/11 08:49:41.656 INFO autosaved config (load with --resume flag) {"file": "/Users/tonybai/Library/Application Support/Caddy/autosave.json"}
2024/10/11 08:49:41.656 INFO serving initial configuration
2024/10/11 08:49:41.657 INFO tls finished cleaning storage units
2024/10/11 08:49:41.657 INFO tls.obtain acquiring lock {"identifier": "server1.com"}
2024/10/11 08:49:41.676 INFO tls.obtain lock acquired {"identifier": "server1.com"}
2024/10/11 08:49:41.676 INFO tls.obtain obtaining certificate {"identifier": "server1.com"}
2024/10/11 08:49:41.684 INFO tls.obtain certificate obtained successfully {"identifier": "server1.com", "issuer": "local"}
2024/10/11 08:49:41.685 INFO tls.obtain releasing lock {"identifier": "server1.com"}
2024/10/11 08:49:41.686 WARN tls stapling OCSP {"error": "no OCSP stapling for [server1.com]: no OCSP server specified in certificate", "identifiers": ["server1.com"]}
```


这段日志“信息量”很大，我们后面一点点来看。现在我们先验证一下caddy启动后是否能成功访问到server1.com这个“站点”，拓扑图如下：

![](../../assets/2392156042fac436.png)


server1.com的程序如下：

```
// server1.go
package main
import (
"fmt"
"net/http"
)
func handler(w http.ResponseWriter, r *http.Request) {
fmt.Fprintln(w, "hello, server1.com")
}
func main() {
http.HandleFunc("/", handler)
fmt.Println("Server is listening on port 9001...")
if err := http.ListenAndServe("localhost:9001", nil); err != nil {
fmt.Println("Error starting server:", err)
}
}
```


启动server1后，我们使用curl访问server1.com（注：请先将server1.com放入/etc/hosts中，映射到本地127.0.0.1）：

```
$go run server1.go
$curl https://server1.com
hello, server1.com
```


是不是非常简单 – **短短几行配置就能在本地搭建出一个可以测试https站点的环境**！

### 1.3 Caddyfile背后的那些事儿

现在是时候基于上面caddy run之后输出的日志以及Caddyfile的内容来说说caddy的一些运行机制了。

首先，当前版本的Caddy的**默认配置信息格式**已经不再是我们在Caddyfile中看到的那样了，而是改为了json格式。虽然上面我们是基于Caddyfile启动的caddy，但实际上caddy程序会在内部启用caddyfile adapt，将Caddyfile的格式转换为json格式后，再作为配置信息提供给caddy的后续逻辑：

![](../../assets/b003ddf96d3d784a.png)


比如上面的Caddyfile被转换为json后的配置如下：

```
{
"apps": {
"http": {
"servers": {
"srv0": {
"listen": [
":443"
],
"routes": [
{
"handle": [
{
"handler": "subroute",
"routes": [
{
"handle": [
{
"handler": "reverse_proxy",
"upstreams": [
{
"dial": "localhost:9001"
}
]
}
]
}
]
}
],
"match": [
{
"host": [
"server1.com"
]
}
],
"terminal": true
}
]
}
}
},
"tls": {
"automation": {
"policies": [
{
"issuers": [
{
"module": "internal"
}
],
"subjects": [
"server1.com"
]
}
]
}
}
}
}
```


当然caddy也支持直接将该json格式配置作为启动时所需的初始配置文件：

```
$caddy run --config caddy.json
```


即便是基于Caddyfile启动，caddy也会将当前配置自动保存起来(以下是macOS下启动caddy的日志)：

```
2024/10/11 08:49:41.656 INFO autosaved config (load with --resume flag) {"file": "/Users/tonybai/Library/Application Support/Caddy/autosave.json"}
```


注：linux上caddy默认保存config的位置为/var/lib/caddy/.config/caddy/autosave.json。


正如日志中所提到的，下次启动时如果带上了–resume标志位，Caddy会基于自动保存的json配置文件启动！

如果caddy启动时带有–resume标志位，但在指定路径下找不到autosave.json时，它就会基于当前目录下的Caddyfile启动，除非使用–config指定配置文件。

在Caddyfile的server1.com site block中，我们使用[tls directive](https://caddyserver.com/docs/caddyfile/directives/tls)：

```
server1.com {
tls internal
reverse_proxy localhost:9001
}
```


tls directive的值是internal，意味着使用Caddy的内部、本地受信任的CA为本站点生成证书。Caddy会在本地创建自签的CA(默认名字是local)，并会尝试将自建的CA根证书安装到系统信任存储区，当以非特权用户运行Caddy时，可能会让你输入sudo用户的密码。接下来，Caddy就会用该CA为像server1.com这样的域名签发证书了。在macOS的用户的Library/Application Support/Caddy下我们能看到CA相关和为站点域名生成的相关私钥和证书：

```
➜ /Users/tonybai/Library/Application Support/Caddy git:(master) ✗ $tree
.
├── autosave.json
├── certificates
│ └── local
│ └── server1.com
│ ├── server1.com.crt
│ ├── server1.com.json
│ └── server1.com.key
├── instance.uuid
├── last_clean.json
├── locks
└── pki
└── authorities
└── local
├── intermediate.crt
├── intermediate.key
├── root.crt
└── root.key
```


### 1.4 四层代理配置和grpc

日常工作中，除了http/https代理，还有两个最常见的反向代理和负载均衡配置，一个是纯四层的Raw TCP和UDP，另外一个则是RPC(以gRPC最为广泛)。那么Caddy对这两种情况支持的如何呢？我们接下来就来看看。

#### 1.4.1 Raw TCP和UDP

Caddy正式版目前不支持四层反向代理和负载均衡，但通过一些插件可以支持，其中[mholt/caddy-l4](https://github.com/mholt/caddy-l4/)是其中最著名的，这也是由Caddy作者建立的项目，但目前还处于WIP状态，可以体验，但**不建议用于生产环境**。

由于Caddy是Go实现的，[Go对插件实现的方案方面不是很友好](https://tonybai.com/2021/07/19/understand-go-plugin)，Caddy采用了重新编译的方案，但提供了名为[xcaddy的构建工具](https://github.com/caddyserver/xcaddy)可以十分方便的支持带有插件的caddy编译，这也算将Go在编译方面的优势充分利用了起来了。

如果本地已经安装了go，那么安装xcaddy十分方便：

```
$go install github.com/caddyserver/xcaddy/cmd/xcaddy@latest
go: downloading github.com/caddyserver/xcaddy v0.4.2
go: downloading github.com/Masterminds/semver/v3 v3.2.1
go: downloading github.com/google/shlex v0.0.0-20191202100458-e7afc7fbc510
go: downloading github.com/josephspurrier/goversioninfo v1.4.0
go: downloading github.com/akavel/rsrc v0.10.2
```


接下来，我们就以用xcaddy编译带有mholt/caddy-l4插件了，这个过程大约持续1-2分钟吧，主要是下载依赖包耗时较长：

```
$xcaddy build --with github.com/mholt/caddy-l4
2024/10/11 12:31:46 [INFO] absolute output file path: /Users/tonybai/caddy
2024/10/11 12:31:46 [INFO] Temporary folder: /Users/tonybai/buildenv_2024-10-17-1231.4160508500
2024/10/11 12:31:46 [INFO] Writing main module: /Users/tonybai/buildenv_2024-10-17-1231.4160508500/main.go
package main
import (
caddycmd "github.com/caddyserver/caddy/v2/cmd"
// plug in Caddy modules here
_ "github.com/caddyserver/caddy/v2/modules/standard"
_ "github.com/mholt/caddy-l4"
)
func main() {
caddycmd.Main()
}
2024/10/11 12:31:46 [INFO] Initializing Go module
2024/10/11 12:31:46 [INFO] exec (timeout=0s): /Users/tonybai/.bin/go1.23.0/bin/go mod init caddy
go: creating new go.mod: module caddy
go: to add module requirements and sums:
go mod tidy
2024/10/11 12:31:46 [INFO] Pinning versions
2024/10/11 12:31:46 [INFO] exec (timeout=0s): /Users/tonybai/.bin/go1.23.0/bin/go get -d -v github.com/caddyserver/caddy/v2
go: -d flag is deprecated. -d=true is a no-op
go: downloading github.com/caddyserver/caddy v1.0.5
go: downloading github.com/caddyserver/caddy/v2 v2.8.4
go: downloading github.com/caddyserver/certmagic v0.21.3
go: downloading github.com/prometheus/client_golang v1.19.1
go: downloading github.com/quic-go/quic-go v0.44.0
go: downloading github.com/cespare/xxhash v1.1.0
go: downloading go.uber.org/zap/exp v0.2.0
go: downloading golang.org/x/term v0.20.0
go: downloading golang.org/x/time v0.5.0
go: downloading go.uber.org/multierr v1.11.0
... ...
go: added golang.org/x/term v0.20.0
go: added golang.org/x/text v0.15.0
go: added golang.org/x/time v0.5.0
go: added golang.org/x/tools v0.21.0
go: added google.golang.org/protobuf v1.34.1
2024/10/11 12:31:53 [INFO] exec (timeout=0s): /Users/tonybai/.bin/go1.23.0/bin/go get -d -v github.com/mholt/caddy-l4 github.com/caddyserver/caddy/v2
go: -d flag is deprecated. -d=true is a no-op
go: downloading github.com/mholt/caddy-l4 v0.0.0-20241012124037-5764d700c21c
go: accepting indirect upgrade from github.com/google/pprof@v0.0.0-20231212022811-ec68065c825e to v0.0.0-20240207164012-fb44976bdcd5
go: accepting indirect upgrade from github.com/miekg/dns@v1.1.59 to v1.1.62
go: accepting indirect upgrade from github.com/onsi/ginkgo/v2@v2.13.2 to v2.15.0
go: accepting indirect upgrade from golang.org/x/crypto@v0.23.0 to v0.28.0
go: accepting indirect upgrade from golang.org/x/mod@v0.17.0 to v0.18.0
go: accepting indirect upgrade from golang.org/x/net@v0.25.0 to v0.30.0
... ...
go: upgraded golang.org/x/sys v0.20.0 => v0.26.0
go: upgraded golang.org/x/term v0.20.0 => v0.25.0
go: upgraded golang.org/x/text v0.15.0 => v0.19.0
go: upgraded golang.org/x/time v0.5.0 => v0.7.0
go: upgraded golang.org/x/tools v0.21.0 => v0.22.0
2024/10/11 12:32:10 [INFO] exec (timeout=0s): /Users/tonybai/.bin/go1.23.0/bin/go get -d -v
go: -d flag is deprecated. -d=true is a no-op
go: downloading github.com/go-chi/chi/v5 v5.0.12
go: downloading gopkg.in/natefinch/lumberjack.v2 v2.2.1
go: downloading github.com/fxamacker/cbor/v2 v2.6.0
go: downloading github.com/google/go-tpm v0.9.0
... ...
go: downloading github.com/google/certificate-transparency-go v1.1.8-0.20240110162603-74a5dd331745
go: downloading github.com/go-logr/stdr v1.2.2
go: downloading github.com/cenkalti/backoff/v4 v4.2.1
go: downloading github.com/grpc-ecosystem/grpc-gateway/v2 v2.18.0
2024/10/11 12:32:15 [INFO] Build environment ready
2024/10/11 12:32:15 [INFO] Building Caddy
2024/10/11 12:32:15 [INFO] exec (timeout=0s): /Users/tonybai/.bin/go1.23.0/bin/go mod tidy -e
go: downloading github.com/onsi/gomega v1.30.0
... ...
go: downloading golang.org/x/oauth2 v0.20.0
go: downloading cloud.google.com/go/auth/oauth2adapt v0.2.2
go: downloading github.com/google/s2a-go v0.1.7
go: downloading cloud.google.com/go/compute/metadata v0.3.0
go: downloading cloud.google.com/go/compute v1.24.0
go: downloading go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc v0.49.0
go: downloading github.com/googleapis/enterprise-certificate-proxy v0.3.2
2024/10/11 12:32:31 [INFO] exec (timeout=0s): /Users/tonybai/.bin/go1.23.0/bin/go build -o /Users/tonybai/caddy -ldflags -w -s -trimpath -tags nobadger
2024/10/11 12:33:22 [INFO] Build complete: ./caddy
2024/10/11 12:33:22 [INFO] Cleaning up temporary folder: /Users/tonybai/buildenv_2024-10-17-1231.4160508500
././caddy version
v2.8.4 h1:q3pe0wpBj1OcHFZ3n/1nl4V4bxBrYoSoab7rL9BMYNk=
```


编译后得到的caddy放在当前目录下：

```
$./caddy version
v2.8.4 h1:q3pe0wpBj1OcHFZ3n/1nl4V4bxBrYoSoab7rL9BMYNk=
```


为了与原先的caddy做区分，我们将新编译出来的caddy重命名为caddy-with-l4。下面我们就来看一个四层负载均衡的示例，先看一下Caddyfile的配置：

```
{
layer4 {
127.0.0.1:5000 {
route {
proxy localhost:9003 localhost:9004 {
lb_policy round_robin
}
}
}
}
}
```


这个配置非常好理解！如下面示意图，caddy将来自客户端到5000端口的连接按照round robin负载均衡算法分配到后面的两个服务localhost:9003和localhost:9004上：

![](../../assets/709ce09cd889a4a0.png)


看完TCP，我们再来看看UDP的反向代理的例子，我们修改一下Caddyfile：

```
{
layer4 {
udp/127.0.0.1:5000 {
route {
proxy udp/localhost:9005 udp/localhost:9006 {
lb_policy round_robin
}
}
}
}
}
```


这个配置同样非常好理解！如下面示意图，caddy将来自客户端到5000端口的udp连接按照round robin负载均衡算法分配到后面的两个服务localhost:9005和localhost:9006上：

![](../../assets/97b462527b795916.png)


注：关于上面两个tcp和udp的示例的client端和server端的代码，可以在github.com/bigwhite/experiments下的caddy-examples中找到，这里鉴于篇幅，就不贴出来了。


接下来，我们再看看RPC。

#### 1.4.2 RPC

我们以最为流行的[gRPC](https://tonybai.com/2021/09/17/those-things-about-grpc-client)为例，来看看如何配置Caddy，试验拓扑如下：

![](../../assets/a4d0912e11f0f1cb.png)


请提前将rpc-server.com配置到/etc/hosts中，ip为localhost。然后，根据上面拓扑图，我们将Caddyfile更新为下面内容：

```
rpc-server.com {
tls internal
reverse_proxy h2c://localhost:9007 h2c://localhost:9008
}
```


gRPC使用HTTP/2帧，h2c://可以确保后端启用明文HTTP/2。

注：关于gRPC的grpc-client、grpc-server1和grpc-server2的代码，可以在github.com/bigwhite/experiments下的caddy-examples的rpc目录中找到，这里鉴于篇幅，就不贴出来了。


到这里，关于Caddy的运行方法以及针对各种协议的基本配置方法已经初步探索完了，接下来我们再来看一下Caddy的另一个强大的功能：基于API的运行时动态配置。

## 2. 运行时使用API对Caddy进行动态配置

[Caddy提供了admin和config API](https://caddyserver.com/docs/api)，允许我们在运行时动态配置和管理服务器。前面提到过，Caddy默认的API端口和路径是http://localhost:2019/config/。不过，需要注意的是：**通过API设置的路由配置仅存储在内存中，并未持久化**。这意味着当Caddy服务器重启后，如果没有使用–resume恢复autosave.json中的配置，那么之前通过API进行的各种设置将失效。

在Caddy提供的API中，我们最关心的还是与服务器(server)、路由(routes)、处理器(handle)以及匹配器(match)的设置，以下面Caddyfile所表示的https服务器设置为例：

```
server1.com {
tls internal
reverse_proxy localhost:9001
}
server2.com {
tls internal
reverse_proxy localhost:9002 localhost:9012
}
```


该Caddyfile对应的拓扑图如下：

![](../../assets/c9b617fd3d8c61aa.png)


该Caddyfile转换为JSON格式后的配置数据如下：

```
{
"apps": {
"http": {
"servers": {
"srv0": {
"listen": [
":443"
],
"routes": [
{
"handle": [
{
"handler": "subroute",
"routes": [
{
"handle": [
{
"handler": "reverse_proxy",
"upstreams": [
{
"dial": "localhost:9001"
}
]
}
]
}
]
}
],
"match": [
{
"host": [
"server1.com"
]
}
],
"terminal": true
},
{
"handle": [
{
"handler": "subroute",
"routes": [
{
"handle": [
{
"handler": "reverse_proxy",
"upstreams": [
{
"dial": "localhost:9002"
},
{
"dial": "localhost:9012"
}
]
}
]
}
]
}
],
"match": [
{
"host": [
"server2.com"
]
}
],
"terminal": true
}
]
}
}
},
"tls": {
"automation": {
"policies": [
{
"issuers": [
{
"module": "internal"
}
],
"subjects": [
"server1.com",
"server2.com"
]
}
]
}
}
}
}
```


其中，我们关注的服务器(server)、路由(routes)、处理器(handle)和匹配器(match)之间的隶属关系如下图，其他配置将由Caddy自动完成：

![](../../assets/fa99a8363d159d23.png)


接下来，我们就基于这个示例，来看看通过Caddy API如何完成一些常见的站点设置操作。

### 2.1 POST /load

我们先看看整体替换的POST /load接口。通过该接口，我们可以用新的Caddy配置整体覆盖当前生效的Caddy配置，Caddy收到这个请求后，会阻塞住该调用，直到新配置加载完成或加载失败才会返回。如果加载失败，Caddy会回滚之前的配置。与caddy reload命令一样，该接口可以实现不停机更新并生效配置，无论是加载成功还是加载失败回滚。

下面我们修改一下上面json，将server2.com路由中的那个监听9012的upstream server去掉，并保存为caddy-load.json。如果担心自己修改的配置信息不正确，可以在调用接口之前，先用caddy validate对caddy-load.json进行有效性检查：

```
$caddy validate -c caddy-load.json
2024/10/11 02:50:28.649 INFO using config from file {"file": "caddy-load.json"}
2024/10/11 02:50:28.651 INFO tls.cache.maintenance started background certificate maintenance {"cache": "0xc00012dd00"}
2024/10/11 02:50:28.652 INFO http.auto_https server is listening only on the HTTPS port but has no TLS connection policies; adding one to enable TLS {"server_name": "srv0", "https_port": 443}
2024/10/11 02:50:28.652 INFO http.auto_https enabling automatic HTTP->HTTPS redirects {"server_name": "srv0"}
2024/10/11 02:50:28.652 INFO tls.cache.maintenance stopped background certificate maintenance {"cache": "0xc00012dd00"}
Valid configuration
```


然后用下面curl命令调用load接口尝试新配置加载：

```
$curl "http://localhost:2019/load" \
-H "Content-Type: application/json" \
-d @caddy-load.json
```


此时Caddy会输出类似如下日志：

```
2024/10/11 02:53:15.191 INFO admin.api received request {"method": "POST", "host": "localhost:2019", "uri": "/load", "remote_ip": "127.0.0.1", "remote_port": "60898", "headers": {"Accept":["*/*"],"Content-Length":["1968"],"Content-Type":["application/json"],"Expect":["100-continue"],"User-Agent":["curl/7.54.0"]}}
2024/10/11 02:53:15.226 INFO admin admin endpoint started {"address": "localhost:2019", "enforce_origin": false, "origins": ["//[::1]:2019", "//127.0.0.1:2019", "//localhost:2019"]}
2024/10/11 02:53:15.240 INFO http.auto_https server is listening only on the HTTPS port but has no TLS connection policies; adding one to enable TLS {"server_name": "srv0", "https_port": 443}
2024/10/11 02:53:15.240 INFO http.auto_https enabling automatic HTTP->HTTPS redirects {"server_name": "srv0"}
2024/10/11 02:53:15.254 INFO pki.ca.local root certificate is already trusted by system {"path": "storage:pki/authorities/local/root.crt"}
2024/10/11 02:53:15.256 INFO http enabling HTTP/3 listener {"addr": ":443"}
2024/10/11 02:53:15.257 INFO http.log server running {"name": "srv0", "protocols": ["h1", "h2", "h3"]}
2024/10/11 02:53:15.257 INFO http.log server running {"name": "remaining_auto_https_redirects", "protocols": ["h1", "h2", "h3"]}
2024/10/11 02:53:15.257 INFO http enabling automatic TLS certificate management {"domains": ["server1.com", "server2.com"]}
2024/10/11 02:53:15.257 INFO http servers shutting down with eternal grace period
2024/10/11 02:53:15.258 INFO autosaved config (load with --resume flag) {"file": "/Users/tonybai/Library/Application Support/Caddy/autosave.json"}
2024/10/11 02:53:15.258 INFO admin.api load complete
2024/10/11 02:53:15.263 INFO admin stopped previous server {"address": "localhost:2019"}
```


更新后，你可以通过config API或autosaved.json查看变更后的配置，也可以通过测试验证新配置是否生效。

不过，这种整体替换显然更容易失败，如果Caddy代理的站点路由很多，json文件的Size也不可小觑。此外，要维护全量的配置，还要对Caddy的配置有较为系统的了解。在日常维护中，按配置路径更新局部配置更为实用一些，接下来我们就来看看如何基于配置路径管理服务器(server)、路由(routes)、处理器(handle)以及匹配器(match)的设置。

### 2.2 /config/[path]

通过在config后面加上要操作的配置路径，我们可以读取和更新对应路径上的配置信息。

#### 2.2.1 读取特定路径下的配置

使用Http Get请求，可以读取在/config后面的指定路径上的配置。

- 读取全部

```
$curl "http://localhost:2019/config/"
```


- 读取所有服务器(server)配置

```
$curl "http://localhost:2019/config/apps/http/servers"
{"srv0":{"listen":[":443"],"routes":[{"handle":[{"handler":"subroute","routes":[{"handle":[{"handler":"reverse_proxy","upstreams":[{"dial":"localhost:9001"}]}]}]}],"match":[{"host":["server1.com"]}],"terminal":true},{"handle":[{"handler":"subroute","routes":[{"handle":[{"handler":"reverse_proxy","upstreams":[{"dial":"localhost:9002"},{"dial":"localhost:9012"}]}]}]}],"match":[{"host":["server2.com"]}],"terminal":true}]}}
```


- 读取某个服务器(server)的配置

以srv0为例：

```
$curl "http://localhost:2019/config/apps/http/servers/srv0"
{"listen":[":443"],"routes":[{"handle":[{"handler":"subroute","routes":[{"handle":[{"handler":"reverse_proxy","upstreams":[{"dial":"localhost:9001"}]}]}]}],"match":[{"host":["server1.com"]}],"terminal":true},{"handle":[{"handler":"subroute","routes":[{"handle":[{"handler":"reverse_proxy","upstreams":[{"dial":"localhost:9002"},{"dial":"localhost:9012"}]}]}]}],"match":[{"host":["server2.com"]}],"terminal":true}]}
```


- 读取srv0的listen配置

```
$curl "http://localhost:2019/config/apps/http/servers/srv0/listen/"
[":443"]
```


- 读取srv0的所有路由

```
$curl "http://localhost:2019/config/apps/http/servers/srv0/routes/"
[{"handle":[{"handler":"subroute","routes":[{"handle":[{"handler":"reverse_proxy","upstreams":[{"dial":"localhost:9001"}]}]}]}],"match":[{"host":["server1.com"]}],"terminal":true},{"handle":[{"handler":"subroute","routes":[{"handle":[{"handler":"reverse_proxy","upstreams":[{"dial":"localhost:9002"},{"dial":"localhost:9012"}]}]}]}],"match":[{"host":["server2.com"]}],"terminal":true}]
```


路由是一个数组，要读取某个路由，可以使用数组下标，比如：

```
$curl "http://localhost:2019/config/apps/http/servers/srv0/routes/0/"
{"handle":[{"handler":"subroute","routes":[{"handle":[{"handler":"reverse_proxy","upstreams":[{"dial":"localhost:9001"}]}]}]}],"match":[{"host":["server1.com"]}],"terminal":true}
```


- 读取某路由的handle和match

```
$curl "http://localhost:2019/config/apps/http/servers/srv0/routes/0/handle/"
[{"handler":"subroute","routes":[{"handle":[{"handler":"reverse_proxy","upstreams":[{"dial":"localhost:9001"}]}]}]}]
$curl "http://localhost:2019/config/apps/http/servers/srv0/routes/0/match/"
[{"host":["server1.com"]}]
```


我们看到，就像上面这样按配置路径逐步细化，便可以读取到所有对应的配置，遇到数组类型，可以使用下标读取对应的“数组元素”的配置。

接下来，我们再来看看基于路径的配置修改方法。

#### 2.2.2 更新特定路径下的配置

使用Http Post请求，可以创建或更新在/config后面的指定路径上的配置。如果指定路径对应的配置目标为一个数组，则POST会将json作为元素追加到数组中；如果目标是一个对象，则post会基于json信息创建新对象或更新对象。

我们先以apps/http/servers/srv0/listen/这个数组对象为例，为其添加一个新元素”:80″：

```
$curl -H "Content-Type: application/json" -d '":80"' "http://localhost:2019/config/apps/http/servers/srv0/listen"
```


成功之后，我们可以看到listen数组的变化：

```
$curl "http://localhost:2019/config/apps/http/servers/srv0/listen"
[":443",":80"]
```


如果是要更改某个数组元素，我们可以使用PATCH请求，比如将刚刚创建的”:80″改为”:90″：

```
$curl -X PATCH -H "Content-Type: application/json" -d '":90"' "http://localhost:2019/config/apps/http/servers/srv0/listen/1"
$curl "http://localhost:2019/config/apps/http/servers/srv0/listen"
[":443",":90"]
```


如果要删除刚才添加的数组元素，可以使用DELETE请求，根据下标值路径进行删除：

```
$curl -X DELETE "http://localhost:2019/config/apps/http/servers/srv0/listen/1"
$curl "http://localhost:2019/config/apps/http/servers/srv0/listen"
[":443"]
```


下面我们来添加一个srv1对象，与上面的srv0并齐：

```
$curl -H "Content-Type: application/json" -d '{ "listen" : [":444"]}' "http://localhost:2019/config/apps/http/servers/srv1/"
```


创建后，我们得到下面配置：

```
$curl "http://localhost:2019/config/apps/http/servers/" | gojq
{
"srv0": {
"listen": [
":443"
],
"routes": [
... ...
]
},
"srv1": {
"listen": [
":444"
]
}
}
```


但我们不能这么创建：

```
$curl -H "Content-Type: application/json" -d '{ "srv1" : { "listen" : [":444"]}}' "http://localhost:2019/config/apps/http/servers/"
```


这样会覆盖掉servers的全部信息，整个servers信息将变为：

```
$curl "http://localhost:2019/config/apps/http/servers/" | gojq
{
"srv1": {
"listen": [
":444"
]
}
}
```


### 2.3 @id

虽然通过上面指定路径可以获取和更新对应的配置，但我们也看到了Caddy的json的缩进非常深，这给API的调用者带来了心智负担。Caddy提供了一种强大而灵活的方式来快速访问和修改配置中的特定部分，这就是使用@id标识符。通过在配置中为某些元素分配唯一的@id，我们可以直接引用这些元素，而无需指定完整的路径。这在处理复杂配置或需要频繁修改特定部分时特别有用。

在Caddy的配置中，@id可以应用于多个层次的配置元素。具体来说，在apps/http/servers下的各个层次都支持@id，包括但不限于：

- 服务器（server）级别
- 路由（routes）级别
- 处理器（handle）级别
- 匹配器（match）级别

下面让我们通过具体的例子来看看如何在这些不同的层次上使用@id。由于Caddyfile不支持@id，我们将使用新的配置作为示例：

我们建立一个新的json作为Caddy的启动配置文件：

```
{
"apps": {
"http": {
"servers": {
"myserver": {
"@id": "main_server",
"listen": [
":80"
],
"routes": [
{
"@id": "main_route",
"handle": [
{
"@id": "main_handler",
"body": "Hello from main server!",
"handler": "static_response"
}
],
"match": [
{
"@id": "path_matcher",
"path": [
"/api/*"
]
}
]
}
]
}
}
}
}
}
```


我们先看看服务器级别的@id使用。在这里我们为myserver这个服务器赋予了一个新的@id字段，值为main_server，接下来，我们就可以使用下面路径获取和更新该server的配置信息：

```
$curl "http://localhost:2019/id/main_server"
{"@id":"main_server","listen":[":80"],"routes":[{"handle":[{"body":"Hello from main server!","handler":"static_response"}]}]}
$curl "http://localhost:2019/id/main_server/listen"
[":80"]
```


同理，在路由级别，我们也为为其中的一个路由设置了@id字段，值为main_route，通过下面命令便可以获取和更新该路由信息：

```
$curl "http://localhost:2019/id/main_route/"
{"@id":"main_route","handle":[{"@id":"main_handler","body":"Hello from main server!","handler":"static_response"}],"match":[{"@id":"path_matcher","path":["/api/*"]}]}
$curl "http://localhost:2019/id/main_route/handle"
[{"@id":"main_handler","body":"Hello from main server!","handler":"static_response"}]
```


通过handle（处理器）级别的@id，我们同样可以直接访问@id对应的对象的信息：

```
$curl "http://localhost:2019/id/main_handler/"
{"@id":"main_handler","body":"Hello from main server!","handler":"static_response"}
$curl "http://localhost:2019/id/main_handler/body"
"Hello from main server!"
```


最后是通过@id访问matcher：

```
$curl "http://localhost:2019/id/path_matcher/"
{"@id":"path_matcher","path":["/api/*"]}
$curl "http://localhost:2019/id/path_matcher/path"
["/api/*"]
```


我们看到：使用@id方式，我们可以像一个使用指针或传送点那样，直达特定路径下面，而无需一层一层的输入路径信息。在处理大型或复杂的配置时，它为管理员和开发者提供了一种更灵活、更直观的方式来操作Caddy的配置。

## 3. 生产环境的实践与ACME

最后我们来简单说说在生产环境使用Caddy的一些实践方法。

### 3.1 生产环境的Caddy配置方法

前面说了那么多的Caddy配置方法，那么在生产环境究竟应该使用哪种方法来进行Caddy的初始配置、运行时动态配置更新以及配置的持久化呢？

虽然Caddyfile简单，但如果要在生产环境中进行运行时的动态配置更新，json格式才是不二之选，我们首先可以基于标准格式准备一份json的初始配置作为caddy的初始启动配置，这个配置后续就可以不再使用了。

启动caddy时建议使用–resume，初始情况下因为还没有autosaved.json，caddy会基于初始配置启动，之后重启caddy都会基于autosaved.json启动。

而运行时，我们可直接**基于API对caddy的配置进行修改**，所有的修改都会立即生效，而且无需停机，并且配置变更会save到autosave.json中，即便caddy重启，下一次启动时caddy也会加载停机前的最新配置，而这一切都不需要我们干预。

### 3.2 自动HTTPS与ACME

在生产环境使用Caddy，除了其超级简单的配置和相对不错的性能之外，最主要就要用它的自动https，即自动为代理的站点域名从[Let’s Encrypt](https://letsencrypt.org/)或[zerossl](https://zerossl.com/)申请受信任的免费证书，并可以在证书过期前自动更新证书。Caddy是通过[ACME协议](https://en.wikipedia.org/wiki/Automatic_Certificate_Management_Environment)与这两个站点进行交互并获取和维护证书的。

ACME协议是一个用于自动化数字证书管理的协议。它允许服务器或客户端软件自动向证书颁发机构 (CA) 请求、更新和撤销SSL/TLS证书。ACME协议的优势在于减少了人为错误，支持短期证书，提高了证书安全性，同时由于支持自动化，让大规模证书部署和管理成为可能。

该协议最早在2015年由Let’s Encrypt推出，旨在推广HTTPS，并使证书管理自动化和标准化。

ACME的API版本有两个，API v1规范于2016年发布。它支持为完全限定的域名颁发证书，例如example.com或cluster.example.com，但不支持*.example.com等通配符证书。API v2规范于2018年发布，被称为ACME v2，ACME v2不向后兼容v1。v2版本支持通配符域名证书，例如*.example.com。同时新增新的挑战(challenge)类型TLS-ALPN-01。

[IETF在2019年正式将ACME作为标准协议发布(RFC 8555)](https://datatracker.ietf.org/doc/html/rfc8555)。2021年，ACME v1版本废弃，不再提供支持。

ACME协议的主要组件包括客户端、ACME服务器（如Let’s Encrypt或ZeroSSL）、挑战机制（Challenges）以及证书颁发流程。客户端首先向ACME服务器请求证书，**服务器通过挑战机制要求客户端证明对域名的控制权**，验证通过后颁发证书。这里最复杂的就是挑战机制了。

Caddy Server支持以下ACME 挑战机制：

- HTTP Challenge

CA机构执行该挑战时会对候选主机名的A/AAAA记录执行权威DNS查找，然后在端口80上使用HTTP请求一个临时的加密资源。如果CA（证书颁发机构）看到了预期的资源，则会颁发证书。该挑战机制要求端口80必须对外部可访问。在Caddy中，此挑战机制默认启用且无需显式配置。

- TLS-ALPN Challenge

CA机构执行该挑战时会对候选主机名的A/AAAA记录执行权威DNS查找，然后在端口443上使用一个包含特殊ServerName和ALPN值的TLS握手请求临时的加密资源。如果CA看到了预期的资源，则会颁发证书。该挑战机制要求端口443必须对外部可访问。在Caddy中，此挑战机制也是默认启用的，且无需显式配置。

- DNS Challenge

CA机构执行该挑战时会对候选主机名的TXT记录执行权威DNS查找，并查找包含特定值的TXT记录。如果CA看到了预期的值，则会颁发证书。

该挑战机制的优点是无需开放任何端口，并且请求证书的服务器不需要对外部可访问。但需要Caddy配置访问候选主机域名的DNS提供商的凭据(api token)，以便Caddy能够通过api设置（和清除）特殊的TXT记录。如果启用了DNS挑战，默认情况下其他挑战会被禁用。

这三种挑战机制在不同场景下都有各自的优势，Caddy默认启用HTTP和TLS-ALPN挑战，并在需要时会自动选择最成功的挑战类型来使用。同时Caddy也为DNS challenge提供了对各种DNS提供商的插件支持，这些插件可以在[https://github.com/caddy-dns](https://github.com/caddy-dns)中查找。

Go在ACME方面有着广泛的应用，很多标准的[ACME client](https://letsencrypt.org/docs/client-options/#clients-go)以及服务端都是由go实现的，比如[cert-manager](https://github.com/cert-manager/cert-manager)等，甚至包括支撑let’s encrypt自身的服务都是基于Go实现的，即[用于实现CA的boulder开源项目](https://github.com/letsencrypt/boulder)。

## 4. 小结

在本文中，我们深入探索了Caddy服务器的强大功能与简便配置。Caddy以其独特的设计理念，简化了Web服务器和反向代理的搭建过程，尤其是在自动HTTPS证书管理和API支持方面表现突出。通过Caddyfile的简单配置，用户可以迅速部署安全的HTTPS站点，而无需繁琐的步骤。

此外，Caddy的动态配置能力使得在运行时调整服务器设置成为可能，极大提高了灵活性和管理效率。尽管Caddy目前在四层代理和负载均衡的支持上还有待增强，但通过插件的方式也为用户提供了扩展的可能性。

总之，Caddy不仅适合个人项目的快速搭建，也在企业级应用中展现出强大的稳定性和高效性。随着社区的不断发展和支持，Caddy将继续成为开发者和系统管理员的重要工具。

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/caddy-examples)下载。

[Gopher部落知识星球](https://public.zsxq.com/groups/51284458844544)在2024年将继续致力于打造一个高品质的Go语言学习和交流平台。我们将继续提供优质的Go技术文章首发和阅读体验。同时，我们也会加强代码质量和最佳实践的分享，包括如何编写简洁、可读、可测试的Go代码。此外，我们还会加强星友之间的交流和互动。欢迎大家踊跃提问，分享心得，讨论技术。我会在第一时间进行解答和交流。我衷心希望Gopher部落可以成为大家学习、进步、交流的港湾。让我相聚在Gopher部落，享受coding的快乐! 欢迎大家踊跃加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) – https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 – https://github.com/bigwhite/gopherdaily
- Gopher Daily Feed订阅 – https://gopherdaily.tonybai.com/feed

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2024, [bigwhite](https://tonybai.com). 版权所有.

No related posts.

## 评论