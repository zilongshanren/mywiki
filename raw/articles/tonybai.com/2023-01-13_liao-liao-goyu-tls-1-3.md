---
title: 聊聊Go与TLS 1.3
url: https://tonybai.com/2023/01/13/go-and-tls13/
published: '2023-01-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 聊聊Go与TLS 1.3

![](../../assets/82e151c6d28d9a2f.png)


[本文永久链接](https://tonybai.com/2023/01/13/go-and-tls13) – https://tonybai.com/2023/01/13/go-and-tls13

除了一些综述类文章和译文，我的文章选题多来源于实际工作和学习中遇到的问题。这次我们来聊聊近期遇到一个问题：**如何加快基于TLS安全通信的海量连接的建连速度**?

TLS(Transport Layer Security)传输安全层的下面是TCP层，我们首先可能会想到的是**优化内核有关TCP握手的相关参数**来快速建立TCP连接，比如：

- net.ipv4.tcp_max_syn_backlog
- net.ipv4.tcp_syncookies
- net.ipv4.tcp_synack_retries
- net.ipv4.tcp_abort_on_overflow
- net.core.somaxconn
- … …

关于Linux内核参数调优，大家可以参考一下极客时间专栏

[《系统性能调优必知必会》]

此外为了加速海量连接的建连速度，提高应用从内核accept连接队列获取连接的速度，我们还可以采用多线程/多goroutine并发Listen同一个端口并并发Accept的机制，如果你使用的是Go语言，可以看看[go-reuseport](https://github.com/libp2p/go-reuseport)这个包。

说完TCP层，那么TLS层是否有可优化的、对建连速度有影响的地方呢？有的，那就是使用TLS 1.3版本来加速握手过程，从而加快建连速度。TLS 1.3是2018年发布的新TLS标准，近2-3年才开始得到主流语言、浏览器和web服务器的支持。那么它与之前的TLS 1.2有何不同呢？Go对TLS 1.3版本的支持程度如何？如何用Go编写使用TLS 1.3的安全通信代码？TLS 1.3建连速度究竟比TLS 1.2快多少呢？

带着这些问题，我们进入本篇正文部分！我们先来简要看看TLS 1.3与TLS 1.2版本的差异。

### 1. TLS 1.3与TLS 1.2的差异

TLS是由互联网工程任务组(Internet Engineering Task Force, [IETF](https://www.ietf.org/))制定和发布的、用于替代SSL的、基于加解密和签名算法的安全连接协议标准，其演进过程如下图：

![](../../assets/dbe4dfe89698fce3.png)


其中TLS 1.0和1.1版本因不再安全，于[2020年被作废](https://www.ietf.org/rfc/rfc8996.html)，目前主流的版本，也是应用最为广泛的是2008年发布的**TLS 1.2版本**(使用占比如下图统计)，而最新版本则是[2018年正式发布的TLS 1.3](https://www.ietf.org/blog/tls13/)，而[TLS 1.3版本的发布](https://datatracker.ietf.org/doc/rfc8446/)也意味着TLS 1.2版本进入“作废期”，虽然实际中TLS 1.2的“下线”还需要很长时间：

![](../../assets/3a9f78b28c28dc01.png)


TLS 1.3与TLS 1.2并不不兼容，在[TLS 1.3](https://datatracker.ietf.org/doc/rfc8446/)协议规范中，我们能看到列出的TLS 1.3相对于TLS 1.2的一些主要改动：

- 去除了原先对称加密算法列表中的非AEAD(Authenticated Encryption with Associated Data)算法，包括3DES、RC4、AES-CBC等，只支持更安全的加密算法。

注：常见的AEAD算法包括：AES-128-GCM、AES-256-GCM、ChaCha20-IETF-Poly1305等。在具备AES加速的CPU（桌面，服务器）上，建议使用AES-XXX-GCM系列，移动设备建议使用ChaCha20-IETF-Poly1305系列。


- 静态RSA和Diffie-Hellman密码套件(cipher suites)已被删除；所有基于公钥的密钥交换机制现在都提供前向安全性。

注：前向安全(Forward Secrecy)是指的是长期使用的主密钥泄漏不会导致过去的会话密钥泄漏。前向安全能够保护过去进行的通讯不受密码或密钥在未来暴露的威胁。如果系统具有前向安全性，就可以保证在主密钥泄露时历史通讯的安全，即使系统遭到主动攻击也是如此。


- TLS 1.2版本的协商机制已被废弃，引入了一个更快的新的密钥协商机制：PSK(Pre-Shared Key)，简化了握手流程(下图是TLS 1.2与TLS 1.3握手流程的对比)。同时在ServerHello之后的所有握手信息现在都被加密了，以前在ServerHello中以明文方式发送的各种扩展信息现在也可以享受加密保护。

![](../../assets/04e497e0cdbefa66.png)


- 增加了一个零往返时间（0-RTT）模式，在恢复连接建立时为一些应用数据节省了一个往返时间。但代价是丧失了某些安全属性。

注：当客户端（例如浏览器）首次成功完成与服务器的TLS 1.3握手后，客户端和服务器都可在本地存储预共享的加密密钥，这称为恢复主密钥。如果客户端稍后再次与服务器建立连接，则可以使用此恢复密钥将其第一条消息中的加密应用程序数据发送到服务器，而无需第二次执行握手。0-RTT模式有一个安全弱点。通过恢复模式发送数据不需要服务器的任何交互，这意味着攻击者（一般是中间人(middle-man)）可以捕获加密的0-RTT数据，然后将其重新发送到服务器，或重放（Replay）它们。解决此问题的方法是确保所有0-RTT请求都是幂等的。


在这些主要变化中，与初次建连速度有关的显然是TLS 1.3握手机制的变化：从2-RTT缩短到1-RTT(如上图所示)。下面我们就用Go作为示例来看看TLS 1.3相对于TLS 1.2在建连速度方面究竟有怎样的提升。

### 2. Go对TLS 1.3的支持

-
Go语言从

[Go 1.12版本](https://tonybai.com/2019/03/02/some-changes-in-go-1-12)开始提供对TLS 1.3的可选支持。在Go 1.12版本下，你通过设置GODEBUG=tls13=1并且不显式设置tls Config的MaxVersion的情况下，便会开启TLS 1.3。这个版本实现中暂不支持TLS 1.3的0-RTT的特性。 -
[Go 1.13版本](https://tonybai.com/2019/10/27/some-changes-in-go-1-13/)默认情况下开启TLS 1.3，你可以使用GODEBUG=tls13=0关闭对TLS 1.3的支持。 -
等到了

[Go 1.14版本](https://tonybai.com/2020/03/08/some-changes-in-go-1-14/)，TLS 1.3成为默认TLS版本选项且无法再用GODEBUG=tls13=0关闭了！不过，通过Config.MaxVersion可以配置要使用的TLS版本。 -
[Go 1.16版本](https://tonybai.com/2021/02/25/some-changes-in-go-1-16)中，在服务端或客户端不支持AES硬件加速的情况下，server端会优先选择其他AEAD的密码套件(cipher suite)，比如ChaCha20Poly1305，而不会选择AES-GCM密码套件。 -
[Go 1.18版本](https://tonybai.com/2022/04/20/some-changes-in-go-1-18)中，client端的Config.MinVersion将默认为TLS 1.2, 以替代原先的默认值TLS 1.0/TLS 1.1。不过你可以通过显式设置客户端的Config.MinVersion来改变这个设置。不过这个改动不影响server端。

了解了这些后，我们来看一个简单的使用Go和TLS 1.3版本的客户端与服务端示例。

### 3. Go TLS 1.3客户端与服务端通信示例

这次我们不去参考Go标准库crypto/tls包的样例，我们玩把时髦儿的：通过AI辅助生成一套基于TLS的client与server端的通信代码示例。[ChatGPT](https://openai.com/blog/chatgpt/)不对大陆开放，我这里用的是[AI编程助手(AICodeHelper)](https://www.aicodehelper.com/)，下面是生成过程的截图：

![](../../assets/5cff568ab3681184.png)


AICodeHelper为我们生成了大部分代码，但是server端代码有两个问题：只能处理一个client端连接和没有生成传入server证书和私钥的代码段，我们基于上面的框架代码做一下修改，得到我们的server和client端代码：

```
server端代码：
// https://github.com/bigwhite/experiments/blob/master/go-and-tls13/server.go
package main
import (
"bufio"
"crypto/tls"
"fmt"
"net"
)
func main() {
cer, err := tls.LoadX509KeyPair("server.crt", "server.key")
if err != nil {
fmt.Println(err)
return
}
config := &tls.Config{Certificates: []tls.Certificate{cer}}
ln, err := tls.Listen("tcp", "localhost:8443", config)
if err != nil {
fmt.Println(err)
return
}
defer ln.Close()
for {
conn, err := ln.Accept()
if err != nil {
fmt.Println(err)
continue
}
go handleConnection(conn)
}
}
func handleConnection(conn net.Conn) {
defer conn.Close()
r := bufio.NewReader(conn)
for {
msg, err := r.ReadString('\n')
if err != nil {
fmt.Println(err)
return
}
println(msg)
n, err := conn.Write([]byte("hello, world from server\n"))
if err != nil {
fmt.Println(n, err)
return
}
}
}
```


```
// https://github.com/bigwhite/experiments/blob/master/go-and-tls13/client.go
package main
import (
"crypto/tls"
"log"
)
func main() {
conf := &tls.Config{
InsecureSkipVerify: true,
}
conn, err := tls.Dial("tcp", "localhost:8443", conf)
if err != nil {
log.Println(err)
return
}
defer conn.Close()
n, err := conn.Write([]byte("hello, world from client\n"))
if err != nil {
log.Println(n, err)
return
}
buf := make([]byte, 100)
n, err = conn.Read(buf)
if err != nil {
log.Println(n, err)
return
}
println(string(buf[:n]))
}
```


为了方便期间，这里使用自签名证书，并且客户端不对服务端的公钥数字证书进行验签(我们无需生成创建CA的相关key和证书)，我们只需要使用下面命令生成一对server.key和server.crt：

```
$openssl genrsa -out server.key 2048
Generating RSA private key, 2048 bit long modulus
..........................+++
................................+++
e is 65537 (0x10001)
$openssl req -new -x509 -sha256 -key server.key -out server.crt -days 3650
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:
State or Province Name (full name) []:
Locality Name (eg, city) []:
Organization Name (eg, company) []:
Organizational Unit Name (eg, section) []:
Common Name (eg, fully qualified host name) []:localhost
Email Address []:
```


关于非对称加密和数字证书方面的详细内容，可以参见我的

[《Go语言精进之路》一书的第51条“使用net/http包实现安全通信”]。

运行Server和Client，这里我使用的是[Go 1.19版本](https://tonybai.com/2022/08/22/some-changes-in-go-1-19)编译器：

```
$go run server.go
hello, world from client
EOF
$go run client.go
hello, world from server
```


我们的示例已经可以正常运行了！那么如何证明示例中的client与server间使用的是1.3版本的TLS连接呢？或者如何查看client与server间使用的是哪个TLS版本呢？

有小伙伴可能会说：用wireshark抓包看，这个可行，但是用wireshark抓tls包，尤其是1.3建连包比较费劲。我们有更简单的方式，我们在开发环境可以通过修改标准库来实现。我们继续往下看。

### 4. server和client端的TLS版本的选择

TLS握手过程由client端发起，从client的视角，当client收到serverHello的响应后便可得到决策后要使用的TLS版本。因此这里我们改造一下crypto/tls/handshake_client.go的clientHandshake方法，在其实现中利用fmt.Printf输出TLS连接相关的信息即可(见下面代码中”====”开头的输出内容)：

```
// $GOROOT/src/crypto/tls/handshake_client.go
func (c *Conn) clientHandshake(ctx context.Context) (err error) {
... ...
hello, ecdheParams, err := c.makeClientHello()
if err != nil {
return err
}
c.serverName = hello.serverName
fmt.Printf("====client: supportedVersions: %x, cipherSuites: %x\n", hello.supportedVersions, hello.cipherSuites)
... ...
msg, err := c.readHandshake()
if err != nil {
return err
}
serverHello, ok := msg.(*serverHelloMsg)
if !ok {
c.sendAlert(alertUnexpectedMessage)
return unexpectedMessageError(serverHello, msg)
}
if err := c.pickTLSVersion(serverHello); err != nil {
return err
}
... ...
if c.vers == VersionTLS13 {
fmt.Printf("====client: choose tls 1.3, server use ciphersuite: [0x%x]\n", serverHello.cipherSuite)
... ...
// In TLS 1.3, session tickets are delivered after the handshake.
return hs.handshake()
}
fmt.Printf("====client: choose tls 1.2, server use ciphersuite: [0x%x]\n", serverHello.cipherSuite)
hs := &clientHandshakeState{
... ...
}
if err := hs.handshake(); err != nil {
return err
}
... ...
}
```


修改完标准库后，我们再来重新运行一下上面的client.go：

```
$go run client.go
====client: supportedVersions: [304 303], cipherSuites: [c02b c02f c02c c030 cca9 cca8 c009 c013 c00a c014 9c 9d 2f 35 c012 a 1301 1302 1303]
====client: choose tls 1.3, server use ciphersuite: [0x1301]
hello, world from server
```


这里我们看一下第一行输出的内容，这里输出的是client端构建clientHello握手包中的内容，展示的是client端支持的TLS版本以及密码套件(cipher suites)，我们看到客户端支持0×304、0×303两个TLS版本，这两个数字与下面代码中的常量分别对应：

```
// $GOROOT/src/crypto/tls/common.go
const (
VersionTLS10 = 0x0301
VersionTLS11 = 0x0302
VersionTLS12 = 0x0303
VersionTLS13 = 0x0304
// Deprecated: SSLv3 is cryptographically broken, and is no longer
// supported by this package. See golang.org/issue/32716.
VersionSSL30 = 0x0300
)
```


而输出的cipherSuites中包含的那些十六进制数则来自下面常量：

```
// $GOROOT/src/crypto/tls/cipher_suites.go
const (
// TLS 1.0 - 1.2 cipher suites.
TLS_RSA_WITH_RC4_128_SHA uint16 = 0x0005
TLS_RSA_WITH_3DES_EDE_CBC_SHA uint16 = 0x000a
TLS_RSA_WITH_AES_128_CBC_SHA uint16 = 0x002f
TLS_RSA_WITH_AES_256_CBC_SHA uint16 = 0x0035
TLS_RSA_WITH_AES_128_CBC_SHA256 uint16 = 0x003c
TLS_RSA_WITH_AES_128_GCM_SHA256 uint16 = 0x009c
TLS_RSA_WITH_AES_256_GCM_SHA384 uint16 = 0x009d
TLS_ECDHE_ECDSA_WITH_RC4_128_SHA uint16 = 0xc007
TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA uint16 = 0xc009
TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA uint16 = 0xc00a
TLS_ECDHE_RSA_WITH_RC4_128_SHA uint16 = 0xc011
TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA uint16 = 0xc012
TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA uint16 = 0xc013
TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA uint16 = 0xc014
TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256 uint16 = 0xc023
TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 uint16 = 0xc027
TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 uint16 = 0xc02f
TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 uint16 = 0xc02b
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 uint16 = 0xc030
TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 uint16 = 0xc02c
TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 uint16 = 0xcca8
TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256 uint16 = 0xcca9
// TLS 1.3 cipher suites.
TLS_AES_128_GCM_SHA256 uint16 = 0x1301
TLS_AES_256_GCM_SHA384 uint16 = 0x1302
TLS_CHACHA20_POLY1305_SHA256 uint16 = 0x1303
... ...
}
```


而从client.go运行结果中的第二行输出可以看出：这次建连，双方最终选择了TLS 1.3版本和TLS_AES_128_GCM_SHA256这个cipher suite。这与前面我们在回顾Go语言对TLS 1.3的支持历史中的描述一致，TLS 1.3是建连版本的默认选择。

那么我们是否可以选择建连时使用的版本呢？当然可以，我们既可以在server端配置，也可以在客户端配置。我们先来看看在Server端如何配置：

```
// https://github.com/bigwhite/experiments/blob/master/go-and-tls13/server_tls12.go
func main() {
cer, err := tls.LoadX509KeyPair("server.crt", "server.key")
if err != nil {
fmt.Println(err)
return
}
config := &tls.Config{
Certificates: []tls.Certificate{cer},
MaxVersion: tls.VersionTLS12,
}
... ...
}
```


我们基于server.go创建了server_tls12.go，在这个新源文件中，我们在tls.Config中增加一个配置MaxVersion，并将其值设置为tls.VersionTLS12，其含义是其**最高支持的TLS版本为TLS 1.2**。这样当我们使用client.go与基于server_tls12.go运行的服务端程序建连时，我们将得到下面输出：

```
$go run client.go
====client: supportedVersions: [304 303], cipherSuites: [c02b c02f c02c c030 cca9 cca8 c009 c013 c00a c014 9c 9d 2f 35 c012 a 1301 1302 1303]
====client: choose tls 1.2, server use ciphersuite: [0xc02f]
hello, world from server
```


我们看到，交互的双方最后选择了TLS 1.2版本，使用的密码套件为0xc02f，即TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256。

同理，如果你想在client端配置最高支持TLS 1.2版本的话，也可以采用同样的方式，大家可以看看本文对应代码库中的client_tls12.go这个源文件，这里就不赘述了。

到这里，一些小伙伴可能有了一个疑问：我们可以配置使用的TLS的版本，那么对于TLS 1.3而言，我们是否可以配置要使用的密码套件呢？答案是目前不可以，理由来自于Config.CipherSuites字段的注释：“Note that TLS 1.3 ciphersuites are not configurable”：

```
// $GOROOT/src/crypto/tls/common.go
type Config struct {
... ...
// CipherSuites is a list of enabled TLS 1.0–1.2 cipher suites. The order of
// the list is ignored. Note that TLS 1.3 ciphersuites are not configurable.
//
// If CipherSuites is nil, a safe default list is used. The default cipher
// suites might change over time.
CipherSuites []uint16
... ...
}
```


tls包会根据系统是否支持AES加速来选择密码套件，如果支持AES加速，就使用下面的defaultCipherSuitesTLS13，这样AES相关套件会被优先选择，否则defaultCipherSuitesTLS13NoAES会被使用，TLS_CHACHA20_POLY1305_SHA256会被优先选择：

```
// $GOROOT/src/crypto/tls/cipher_suites.go
// defaultCipherSuitesTLS13 is also the preference order, since there are no
// disabled by default TLS 1.3 cipher suites. The same AES vs ChaCha20 logic as
// cipherSuitesPreferenceOrder applies.
var defaultCipherSuitesTLS13 = []uint16{
TLS_AES_128_GCM_SHA256,
TLS_AES_256_GCM_SHA384,
TLS_CHACHA20_POLY1305_SHA256,
}
var defaultCipherSuitesTLS13NoAES = []uint16{
TLS_CHACHA20_POLY1305_SHA256,
TLS_AES_128_GCM_SHA256,
TLS_AES_256_GCM_SHA384,
}
```


注：joe shaw曾写过一篇文章

[“Abusing go:linkname to customize TLS 1.3 cipher suites”]，文中描述了一种通过go:linkname定制TLS 1.3密码套件的方法，有兴趣的小伙伴们可以去阅读一下。

### 5. 建连速度benchmark

最后我们再来看看相较于TLS 1.2，TLS 1.3的建连速度究竟快了多少。考虑到两个版本在RTT数量上的差异，即网络延迟对建连速度影响较大，我特意选择了一个ping在20-30ms的网络。我们为TLS 1.2和TLS 1.3分别建立Benchmark Test：

```
// https://github.com/bigwhite/experiments/blob/master/go-and-tls13/benchmark/benchmark_test.go
package main
import (
"crypto/tls"
"testing"
)
func tls12_dial() error {
conf := &tls.Config{
InsecureSkipVerify: true,
MaxVersion: tls.VersionTLS12,
}
conn, err := tls.Dial("tcp", "192.168.11.10:8443", conf)
if err != nil {
return err
}
conn.Close()
return nil
}
func tls13_dial() error {
conf := &tls.Config{
InsecureSkipVerify: true,
}
conn, err := tls.Dial("tcp", "192.168.11.10:8443", conf)
if err != nil {
return err
}
conn.Close()
return nil
}
func BenchmarkTls13(b *testing.B) {
b.ReportAllocs()
for i := 0; i < b.N; i++ {
err := tls13_dial()
if err != nil {
panic(err)
}
}
}
func BenchmarkTls12(b *testing.B) {
b.ReportAllocs()
for i := 0; i < b.N; i++ {
err := tls12_dial()
if err != nil {
panic(err)
}
}
}
```


server部署在192.168.11.10上，针对每个benchmark test，我们给予10s钟的测试时间，下面是运行结果：

```
$go test -benchtime 10s -bench .
goos: linux
goarch: amd64
pkg: demo
cpu: Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz
BenchmarkTls13-8 216 56036809 ns/op 47966 B/op 608 allocs/op
BenchmarkTls12-8 145 82395933 ns/op 26655 B/op 283 allocs/op
PASS
ok demo 37.959s
```


我们看到相对与TLS 1.2，TLS 1.3建连速度的确更快些。不过从内存分配的情况来看，Go TLS 1.3的实现似乎更复杂一些。

### 6. 参考资料

- RFC 8446：The Transport Layer Security (TLS) Protocol Version 1.3 – https://datatracker.ietf.org/doc/rfc8446/
- 前向安全 – https://sunhuachuang.gitbooks.io/sun-note/content/cryptography/forward_backward_secrecy.html

本文涉及的源码可以在[这里](https://github.com/bigwhite/experiments/blob/master/go-and-tls13)下载。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2022年，Gopher部落全面改版，将持续分享Go语言与Go应用领域的知识、技巧与实践，并增加诸多互动形式。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻)归档仓库 – https://github.com/bigwhite/gopherdaily

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论