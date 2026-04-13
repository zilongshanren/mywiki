---
title: Go TLS服务端绑定证书的几种方式
url: https://tonybai.com/2023/10/13/multiple-ways-to-bind-certificates-on-go-tls-server-side/
published: '2023-10-13'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go TLS服务端绑定证书的几种方式

![](../../assets/3af5217be58f6b6f.png)


[本文永久链接](https://tonybai.com/2023/10/13/multiple-ways-to-bind-certificates-on-go-tls-server-side) – https://tonybai.com/2023/10/13/multiple-ways-to-bind-certificates-on-go-tls-server-side

随着互联网的发展，网站提供的服务类型和规模不断扩大，同时也对Web服务的安全性提出了更高的要求。[TLS(Transport Layer Security)](https://tonybai.com/2023/01/13/go-and-tls13)已然成为Web服务最重要的安全基础设施之一。默认情况下，[一个TLS服务器通常只绑定一个证书](https://tonybai.com/2015/04/30/go-and-https)，但当服务复杂度增加时，单一证书已然难以满足需求。这时，服务端绑定多个TLS证书就成为一个非常实用的功能。

Go语言中的net/http包和tls包对TLS提供了强大的支持，在密码学和安全专家[Filippo Valsorda](https://filippo.io/)的精心设计下，Go提供了多种TLS服务端绑定证书的方式，本文将详细探讨服务端绑定TLS证书的几种方式，包括绑定单个证书、多个证书、自定义证书绑定逻辑等。我会配合示例代码，了解每种方式的使用场景、实现原理和优缺点。

## 1. 热身：制作证书

为了后续示例说明方便，我们先来把示例所需的私钥和证书都做出来，本文涉及的证书以及他们之间的签发关系如下图：

![](../../assets/4b416c3941dbc211.png)


注：示例使用的自签名根证书。


从图中我们看到，我们证书分为三个层次，最左边是CA的根证书(root certificate，比如ca-cert.pem)，之后是根CA签发的中间CA证书(intermediate certificate，比如inter-cert.pem)，从安全和管理角度出发，真正签发服务器证书的都是这些**中间CA**；最右侧则是由中间CA签发的叶子证书(leaf certificate，比如leaf-server-cert.pem)，也就是服务器配置的服务端证书(server certificate)，我们为三个不同域名创建了不同的服务器证书。

在这里，我们制作上述证书没有使用类似[openssl](https://www.openssl.org)这样的工具，而是通过Go代码生成的，下面是生成上述证书的代码片段：

```
// tls-certs-binding/make_certs/main.go
func main() {
// 生成CA根证书密钥对
caKey, err := rsa.GenerateKey(rand.Reader, 2048)
checkError(err)
// 生成CA证书模板
caTemplate := x509.Certificate{
SerialNumber: big.NewInt(1),
Subject: pkix.Name{
Organization: []string{"Go CA"},
},
NotBefore: time.Now(),
NotAfter: time.Now().Add(time.Hour * 24 * 365),
KeyUsage: x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature | x509.KeyUsageCertSign,
BasicConstraintsValid: true,
IsCA: true,
}
// 使用模板自签名生成CA证书
caCert, err := x509.CreateCertificate(rand.Reader, &caTemplate, &caTemplate, &caKey.PublicKey, caKey)
checkError(err)
// 生成中间CA密钥对
interKey, err := rsa.GenerateKey(rand.Reader, 2048)
checkError(err)
// 生成中间CA证书模板
interTemplate := x509.Certificate{
SerialNumber: big.NewInt(2),
Subject: pkix.Name{
Organization: []string{"Go Intermediate CA"},
},
NotBefore: time.Now(),
NotAfter: time.Now().Add(time.Hour * 24 * 365),
KeyUsage: x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature | x509.KeyUsageCertSign,
BasicConstraintsValid: true,
IsCA: true,
}
// 用CA证书签名生成中间CA证书
interCert, err := x509.CreateCertificate(rand.Reader, &interTemplate, &caTemplate, &interKey.PublicKey, caKey)
checkError(err)
// 生成叶子证书密钥对
leafKey, err := rsa.GenerateKey(rand.Reader, 2048)
checkError(err)
// 生成叶子证书模板,CN为server.com
leafTemplate := x509.Certificate{
SerialNumber: big.NewInt(3),
Subject: pkix.Name{
Organization: []string{"Go Server"},
CommonName: "server.com",
},
NotBefore: time.Now(),
NotAfter: time.Now().Add(time.Hour * 24 * 365),
KeyUsage: x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature,
ExtKeyUsage: []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
IPAddresses: []net.IP{net.ParseIP("127.0.0.1")},
DNSNames: []string{"server.com"},
SubjectKeyId: []byte{1, 2, 3, 4},
}
// 用中间CA证书签名生成叶子证书
leafCert, err := x509.CreateCertificate(rand.Reader, &leafTemplate, &interTemplate, &leafKey.PublicKey, interKey)
checkError(err)
// 生成server1.com叶子证书
leafKey1, _ := rsa.GenerateKey(rand.Reader, 2048)
leafTemplate1 := x509.Certificate{
SerialNumber: big.NewInt(4),
Subject: pkix.Name{
CommonName: "server1.com",
},
NotBefore: time.Now(),
NotAfter: time.Now().Add(time.Hour * 24 * 365),
KeyUsage: x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature,
ExtKeyUsage: []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
DNSNames: []string{"server1.com"},
}
leafCert1, _ := x509.CreateCertificate(rand.Reader, &leafTemplate1, &interTemplate, &leafKey1.PublicKey, interKey)
// 生成server2.com叶子证书
leafKey2, _ := rsa.GenerateKey(rand.Reader, 2048)
leafTemplate2 := x509.Certificate{
SerialNumber: big.NewInt(5),
Subject: pkix.Name{
CommonName: "server2.com",
},
NotBefore: time.Now(),
NotAfter: time.Now().Add(time.Hour * 24 * 365),
KeyUsage: x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature,
ExtKeyUsage: []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
DNSNames: []string{"server2.com"},
}
leafCert2, _ := x509.CreateCertificate(rand.Reader, &leafTemplate2, &interTemplate, &leafKey2.PublicKey, interKey)
// 将证书和密钥编码为PEM格式
caCertPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: caCert})
caKeyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(caKey)})
interCertPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: interCert})
interKeyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(interKey)})
leafCertPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: leafCert})
leafKeyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(leafKey)})
leafCertPEM1 := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: leafCert1})
leafKeyPEM1 := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(leafKey1)})
leafCertPEM2 := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: leafCert2})
leafKeyPEM2 := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(leafKey2)})
// 将PEM写入文件
writeDataToFile("ca-cert.pem", caCertPEM)
writeDataToFile("ca-key.pem", caKeyPEM)
writeDataToFile("inter-cert.pem", interCertPEM)
writeDataToFile("inter-key.pem", interKeyPEM)
writeDataToFile("leaf-server-cert.pem", leafCertPEM)
writeDataToFile("leaf-server-key.pem", leafKeyPEM)
writeDataToFile("leaf-server1-cert.pem", leafCertPEM1)
writeDataToFile("leaf-server1-key.pem", leafKeyPEM1)
writeDataToFile("leaf-server2-cert.pem", leafCertPEM2)
writeDataToFile("leaf-server2-key.pem", leafKeyPEM2)
}
```


运行这个程序后，当前目录下就会出现如下私钥文件(xx-key.pem)和证书文件(xx-cert.pem)：

```
$ls *pem
ca-cert.pem inter-cert.pem leaf-server-cert.pem leaf-server1-cert.pem leaf-server2-cert.pem
ca-key.pem inter-key.pem leaf-server-key.pem leaf-server1-key.pem leaf-server2-key.pem
```


制作完证书后，我们就来看看日常使用最多的**绑定单一TLS证书**的情况。

## 2. 绑定单一TLS证书

做过web应用的读者，想必对绑定单一TLS证书的实现方式并不陌生。服务端只需要加载一对服务端私钥与公钥证书即可对外提供基于TLS的安全网络服务，这里一个echo服务为例，我们来看下服务端的代码：

```
// tls-certs-binding/bind_single_cert/sever/main.go
// 服务端
func startServer(certFile, keyFile string) {
// 读取证书和密钥
cert, err := tls.LoadX509KeyPair(certFile, keyFile)
if err != nil {
log.Fatal(err)
}
// 创建TLS配置
config := &tls.Config{
Certificates: []tls.Certificate{cert},
}
// 启动TLS服务器
listener, err := tls.Listen("tcp", ":8443", config)
if err != nil {
log.Fatal(err)
}
defer listener.Close()
log.Println("Server started")
for {
conn, err := listener.Accept()
if err != nil {
log.Println(err)
continue
}
handleConnection(conn)
}
}
func handleConnection(conn net.Conn) {
defer conn.Close()
// 处理连接...
// 循环读取客户端的数据
for {
buf := make([]byte, 1024)
n, err := conn.Read(buf)
if err != nil {
// 读取失败则退出
return
}
// 回显数据给客户端
s := string(buf[:n])
fmt.Printf("recv data: %s\n", s)
conn.Write(buf[:n])
}
}
func main() {
// 启动服务器
startServer("leaf-server-cert.pem", "leaf-server-key.pem")
}
```


根据TLS的原理，客户端在与服务端的握手过程中，服务端会将服务端证书(leaf-server-cert.pem)发到客户端供后者验证，客户端使用服务器公钥证书校验服务器身份。这一过程的实质是客户端**利用CA证书中的公钥或中间CA证书中的公钥对服务端证书中由CA私钥或中间CA私钥签名的数据进行验签**。

```
// tls-certs-binding/bind_single_cert/client/main.go
func main() {
caCert, err := ioutil.ReadFile("inter-cert.pem")
if err != nil {
log.Fatal(err)
}
caCertPool := x509.NewCertPool()
caCertPool.AppendCertsFromPEM(caCert)
config := &tls.Config{
RootCAs: caCertPool,
}
conn, err := tls.Dial("tcp", "server.com:8443", config)
if err != nil {
log.Fatal(err)
}
defer conn.Close()
// 每秒发送信息
ticker := time.NewTicker(time.Second)
for range ticker.C {
msg := "hello, tls"
conn.Write([]byte(msg))
// 读取回复
buf := make([]byte, len(msg))
conn.Read(buf)
log.Println(string(buf))
}
}
```


![](../../assets/11985ddba241c4e7.png)


这里我们使用了签发了leaf-server-cert.pem证书的中间CA(inter-cert.pem)来验证服务端证书(leaf-server-cert.pem)的合法性，毫无疑问这是会成功的！

```
// server
$go run main.go
2023/10/05 22:49:17 Server started
// client
$go run main.go
2023/10/05 22:49:22 hello, tls
2023/10/05 22:49:23 hello, tls
... ...
```


注：运行上述代码之前，需修改/etc/hosts文件，添加server.com的IP为127.0.0.1。


不过要注意的是，在这里用CA根证书(ca-cert.pem)直接验证叶子证书(leaf-server-cert.pem)会失败，因为根证书不是叶子证书的直接签发者，必须通过验证证书链来建立根证书和叶子证书之间的信任链。

![](../../assets/be9cfa5db5eb0da5.png)


## 3. 证书链

实际生产中，服务器实体证书和根证书分别只有一张，但中间证书可以有多张，这些中间证书在客户端并不一定存在，这就可能导致客户端与服务端的连接无法建立。通过openssl命令也可以印证这一点：

```
// 在make_certs目录下
// CA根证书无法直接验证叶子证书
$openssl verify -CAfile ca-cert.pem leaf-server-cert.pem
leaf-server-cert.pem: O = Go Server, CN = server.com
error 20 at 0 depth lookup:unable to get local issuer certificate
// 证书链不完整，也无法验证
$openssl verify -CAfile inter-cert.pem leaf-server-cert.pem
leaf-server-cert.pem: O = Go Intermediate CA
error 2 at 1 depth lookup:unable to get issuer certificate
// 需要用完整证书链来验证
$openssl verify -CAfile ca-cert.pem -untrusted inter-cert.pem leaf-server-cert.pem
leaf-server-cert.pem: OK
```


为此在建连阶段，服务端不仅要将服务器实体证书发给客户端，还要发送完整的**证书链**(如下图所示)。

![](../../assets/bd7cb420402998a1.png)


证书链的最顶端是CA根证书，它的签名值是自己签名的，验证签名的公钥就包含在根证书中，根证书的签发者（Issuer）与使用者（Subject）是相同的。除了根证书，每个证书的签发者（Issuer）是它的上一级证书的使用者（Subject）。以上图为例，下列关系是成立的：

```
- ca-cert.pem的Issuer == ca-cert.pem的Subject
- inter1-cert.pem的Issuer == ca-cert.pem的Subject
- inter2-cert.pem的Issuer == inter1-cert.pem的Subject
... ...
- interN-cert.pem的Issuer == interN-1-cert.pem的Subject
- leaf-server-cert.pem的Issuer == interN-cert.pem的Subject
```


每张证书包含的重要信息是签发者(Issuer)、数字签名算法、签名值、使用者（Subject）域名、使用者公钥。除了根证书，每个证书（比如inter2-cert.pem证书）被它的上一级证书（比如inter1-cert.pem证书）对应的私钥签名，签名值包含在证书中，上一级证书包含的公钥可以用来验证该证书中的签名值(inter2-cert.pem证书可以用来验证inter1-cert.pem证书中的签名值)。

那么如何在服务端返回证书链呢？如何在客户端接收并验证证书链呢？我们来看下面示例。在这个示例中，客户端仅部署了根证书(ca-cert.pem)，而服务端需要将服务证书与签发服务证书的中间CA证书以证书链的形式返回给客户端。

我们先来看服务端：

```
// tls-certs-binding/bind_single_cert/server-with-certs-chain/main.go
// 服务端
func startServer(certFile, keyFile string) {
// 读取证书和密钥
cert, err := tls.LoadX509KeyPair(certFile, keyFile)
if err != nil {
log.Fatal(err)
}
interCertBytes, err := os.ReadFile("inter-cert.pem")
if err != nil {
log.Fatal(err)
}
interCertblock, _ := pem.Decode(interCertBytes)
// 将中间证书添加到证书链
cert.Certificate = append(cert.Certificate, interCertblock.Bytes)
// 创建TLS配置
config := &tls.Config{
Certificates: []tls.Certificate{cert},
}
// 启动TLS服务器
listener, err := tls.Listen("tcp", ":8443", config)
if err != nil {
log.Fatal(err)
}
defer listener.Close()
log.Println("Server started")
for {
conn, err := listener.Accept()
if err != nil {
log.Println(err)
continue
}
handleConnection(conn)
}
}
```


我们看到：服务端在加载完服务端证书后，又将中间CA证书inter-cert.pem attach到cert.Certificate，这样cert.Certificate中就构造出了一个证书链，而不单单是一个服务端证书了。

我们要注意证书链构造时的顺序，这里按照的是如下顺序构造证书链的：

```
- 服务端证书 (leaf certificate)
- 中间CA证书N
- 中间CA证书N-1
... ...
- 中间CA证书2
- 中间CA证书1
```


如果客户端没有根CA证书 (root certificate)，在服务端构造证书链时，需要将根CA证书作为最后一个证书attach到证书链中。

下面则是客户端验证证书链的代码：

```
// tls-certs-binding/bind_single_cert/client-verify-certs-chain/main.go
func main() {
// 加载ca-cert.pem
caCertBytes, err := os.ReadFile("ca-cert.pem")
if err != nil {
log.Fatal(err)
}
caCertblock, _ := pem.Decode(caCertBytes)
caCert, err := x509.ParseCertificate(caCertblock.Bytes)
if err != nil {
log.Fatal(err)
}
// 创建TLS配置
config := &tls.Config{
InsecureSkipVerify: true, // trigger to call VerifyPeerCertificate
// 设置证书验证回调函数
VerifyPeerCertificate: func(rawCerts [][]byte, verifiedChains [][]*x509.Certificate) error {
// 解析服务端返回的证书链(顺序：server-cert.pem, inter-cert.pem，inter-cert.pem's issuer...)
var issuer *x509.Certificate
var cert *x509.Certificate
var err error
if len(rawCerts) == 0 {
return errors.New("no server certificate found")
}
issuer = caCert
for i := len(rawCerts) - 1; i >= 0; i-- {
cert, err = x509.ParseCertificate(rawCerts[i])
if err != nil {
return err
}
if !verifyCert(issuer, cert) {
return errors.New("verifyCert failed")
}
issuer = cert
}
return nil
},
}
conn, err := tls.Dial("tcp", "server.com:8443", config)
if err != nil {
log.Fatal(err)
}
defer conn.Close()
// 每秒发送信息
ticker := time.NewTicker(time.Second)
for range ticker.C {
msg := "hello, tls"
conn.Write([]byte(msg))
// 读取回复
buf := make([]byte, len(msg))
conn.Read(buf)
log.Println(string(buf))
}
}
// 验证cert是否是issuer的签发
func verifyCert(issuer, cert *x509.Certificate) bool {
// 验证证书
certPool := x509.NewCertPool()
certPool.AddCert(issuer) // ok
opts := x509.VerifyOptions{
Roots: certPool,
}
_, err := cert.Verify(opts)
return err == nil
}
```


从代码可以看到，当正常验证失败或没有使用正常验证的情况下，我们需要将InsecureSkipVerify设置为true才能触发证书链的自定义校验逻辑(VerifyPeerCertificate)。在VerifyPeerCertificate中，我们先用ca根证书校验位于证书链最后的那个证书，验证成功后，用验证成功的证书验证倒数第二个证书，依次类推，知道全部证书都校验ok，说明证书链是可信任的。

服务端绑定一个证书或一套证书链是最简单的，也是最常见的方案，但在一些场景下，比如考虑支持多个域名、证书轮换等，TLS服务端可能需要绑定多个证书以满足要求。下面我们就来看看如何为TLS服务端绑定多个证书。

## 4. 绑定多个TLS证书

这个示例的证书绑定情况如下图：

![](../../assets/77b0dd195eb04caa.png)


我们在服务端部署并绑定了三个证书，三个证书与域名的对应关系如下：

```
- 证书leaf-server-cert.pem 对应 server.com
- 证书leaf-server1-cert.pem 对应 server1.com
- 证书leaf-server2-cert.pem 对应 server2.com
```


注：在/etc/hosts中添加server1.com和server2.com对应的ip均为127.0.0.1。


```
// tls-certs-binding/bind_multi_certs/server/main.go
func main() {
certFiles := []string{"leaf-server-cert.pem", "leaf-server1-cert.pem", "leaf-server2-cert.pem"}
keyFiles := []string{"leaf-server-key.pem", "leaf-server1-key.pem", "leaf-server2-key.pem"}
// 启动服务器
startServer(certFiles, keyFiles)
}
// 服务端
func startServer(certFiles, keyFiles []string) {
// 读取证书和密钥
var certs []tls.Certificate
for i := 0; i < len(certFiles); i++ {
cert, err := tls.LoadX509KeyPair(certFiles[i], keyFiles[i])
if err != nil {
log.Fatal(err)
}
certs = append(certs, cert)
}
// 创建TLS配置
config := &tls.Config{
Certificates: certs,
}
// 启动TLS服务器
listener, err := tls.Listen("tcp", ":8443", config)
if err != nil {
log.Fatal(err)
}
defer listener.Close()
log.Println("Server started")
for {
conn, err := listener.Accept()
if err != nil {
log.Println(err)
continue
}
handleConnection(conn)
}
}
```


我们看到，绑定多个证书与绑定一个证书的原理是完全一样的，tls.Config的Certificates字段原本就是一个切片，可以容纳单个证书，也可以容纳证书链，容纳多个证书也不是问题。

客户端代码变化不大，我们仅是通过下面代码输出了服务端返回的证书的Subject.CN：

```
// tls-certs-binding/bind_multi_certs/client/main.go
// 解析连接的服务器证书
certs := conn.ConnectionState().PeerCertificates
if len(certs) > 0 {
log.Println("Server CN:", certs[0].Subject.CommonName)
}
```


接下来我们通过client连接不同的域名，得到如下执行结果：

```
// 服务端
$go run main.go
2023/10/06 10:22:38 Server started
// 客户端
$go run main.go -server server.com:8443
2023/10/06 10:22:57 Server CN: server.com
2023/10/06 10:22:58 hello, tls
$go run main.go -server server1.com:8443
2023/10/06 10:23:02 Server CN: server1.com
2023/10/06 10:23:03 hello, tls
2023/10/06 10:23:04 hello, tls
$go run main.go -server server2.com:8443
2023/10/06 10:23:08 Server CN: server2.com
2023/10/06 10:23:09 hello, tls
... ...
```


我们看到，由于绑定多个域名对应的证书，程序可以支持访问不同域名的请求，并根据请求的域名，返回对应域名的证书。

## 5. 自定义证书选择绑定逻辑

无论是单一TLS证书、证书链还是多TLS证书，他们都有一个共同特点，那就是证书的绑定是事先已知的，是一种“静态”模式的绑定；有些场景下，服务端在初始化启动后并不会绑定某个固定的证书，而是根据客户端的连接需求以及特定规则在证书池中选择某个匹配的证书。在这种情况下，我们需要使用GetCertificate回调从自定义的证书池中选择匹配的证书，而不能在用上面示例中那种“静态”模式了。

我们来看一个自定义证书选择逻辑的示例，下面示意图展示了客户端和服务端的证书部署情况：

![](../../assets/5ff0c82ad7bb825d.png)


我们主要看一下服务端的代码逻辑变动：

```
// tls-certs-binding/bind_custom_logic/server/main.go
func startServer(certsPath string) {
// 创建TLS配置
config := &tls.Config{
GetCertificate: func(info *tls.ClientHelloInfo) (*tls.Certificate, error) {
// 根据clientHello信息选择cert
certFile := fmt.Sprintf("%s/leaf-%s-cert.pem", certsPath, info.ServerName[:len(info.ServerName)-4])
keyFile := fmt.Sprintf("%s/leaf-%s-key.pem", certsPath, info.ServerName[:len(info.ServerName)-4])
// 读取证书和密钥
cert, err := tls.LoadX509KeyPair(certFile, keyFile)
return &cert, err
},
}
... ...
}
```


我们看到: tls.Config我们建立了一个匿名函数赋值给了GetCertificate字段，该函数的实现逻辑就是根据客户端clientHello信息(tls握手时发送的信息)按照规则从证书池目录中查找并加载对应的证书与其私钥信息。示例使用ServerName来查找带有同名信息的证书。

例子的运行结果与上面的示例都差不多，这里就不赘述了。

利用这种动态的证书选择逻辑，我们还可以实现通过执行外部命令来获取证书、从数据库加载证书等。

## 6. 小结

通过本文的介绍，我们全面了解了在Go服务端绑定单个、多个TLS证书的各种方式。我们首先介绍了生成自签名证书的方法，这为我们的示例程序奠定了基础。然后我们详细探讨了绑定单证书、证书链、多证书、定制从证书池取特定证书的逻辑等不同机制的用法、优劣势和适用场景。同时，在介绍每种用法时，我们都用代码示例进一步解释了这些绑定方式的具体实现流程。

单证书TLS简单易理解，运行性能优异。多证书TLS在提高性能、安全性、便利管理等方面有着重要意义。而自定义证书选取逻辑则更加灵活。通过综合运用各种绑定机制，可以使我们的Go语言服务器端更加强大和灵活。

本文示例所涉及的Go源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/tls-certs-binding)下载。

注：代码仓库中的证书和key文件有效期为一年，大家如发现证书已经过期，可以在make_certs目录下重新生成各种证书和私钥并copy到对应的其他目录中去。


## 7. 参考资料

[《深入浅出 HTTPS：从原理到实战》](https://book.douban.com/subject/30250772/)– https://book.douban.com/subject/30250772/[Certificate chains and cross-certification](https://en.wikipedia.org/wiki/X.509#Certificate_chains_and_cross-certification)– https://en.wikipedia.org/wiki/X.509#Certificate_chains_and_cross-certification

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论