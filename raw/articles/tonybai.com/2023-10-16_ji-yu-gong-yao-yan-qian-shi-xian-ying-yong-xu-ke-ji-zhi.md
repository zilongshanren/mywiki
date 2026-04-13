---
title: 基于公钥验签实现应用许可机制
url: https://tonybai.com/2023/10/16/implementation-of-app-licensing-based-on-verifying-sign-by-pubkey/
published: '2023-10-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 基于公钥验签实现应用许可机制

![](../../assets/6822d5b659fdf735.png)


[本文永久链接](https://tonybai.com/2023/10/16/implementation-of-app-licensing-based-on-verifying-sign-by-pubkey) – https://tonybai.com/2023/10/16/implementation-of-app-licensing-based-on-verifying-sign-by-pubkey

随着互联网的普及以及应用的快速发展，商业软件的订阅模式变得越来越流行。软件公司开始提供基于订阅的服务，用户每月或每年支付费用以获取软件的使用权。这种模式使用户可以更灵活地选择服务期限，并且软件公司可以持续提供更新和技术支持。随着“软件定义汽车”的到来，这种模式在智能网联汽车领域也逐渐流行开来！

一些需要私有化部署在客户现场的toB商业软件的公司也在探索这种订阅许可证模式，但与toC的软件不同，toB软件系统由于部署在客户数据中心中，如何有效地管理软件授权成为一个关键问题。传统的通过注册码或者登录供应商服务器进行软件授权存在诸多不便(甚至不可行)，而利用公钥基础设施实现许可证签发和验证可以很好地解决这个问题。

本文就来探讨一下如何利用公钥证书验签的方式实现应用许可机制，在这套机制中，软件供应商负责设计许可证格式对许可证进行签名，并将证书分发给客户。客户只需要利用供应商提供的方法将证书导入系统或更新许可证即可，系统可自动识别许可证的有效性与并加载信息的变更。这种方式无需客户每次连接服务器就可以离线验证许可，既方便且安全，同时也可防止许可证被盗用或篡改。

## 1. 方案原理

基于公钥验签实现许可证验证机制的原理并不复杂，如果你对非对称加密有初步了解，你就能理解下图中的方案工作流程：

![](../../assets/7ae91f28e06a6d54.png)


从图中可以看到，基于公钥验签的许可证验证利用了公钥加密的不对称结构让签发方(软件厂商)和验证方(客户)拥有不对等的密钥。

首先，许可证的签发方(软件厂商)需要为某个客户生成一对公钥(证书)和私钥，私钥需要严格保密，公钥(证书)可以公开，将伴随软件安装包一并分发给客户。

签发方(软件厂商)根据客户购买的服务或产品信息生成许可证文件，其中包含客户标识、授权信息等，然后使用其私钥对该许可证文件内容进行数字签名，形成带签名的许可证。

客户收到许可证后，已安装到客户现场的应用会用公钥对许可证的签名进行验证，验证能够证明该许可证确实来自该签发方，且内容完整无篡改。许可证初次导入、续期或变更时，应用都会对许可证的签名进行验证。整个验证过程是离线脱机的，无需连接签发服务器。

验证成功后，许可证生效。应用会使用许可证中携带的授权信息对应用的行为进行控制与约束。

下面我们用一个Go实现的示例来演示一下这个方案。

## 2. 许可证格式设计

我们先来为示例程序设计一个许可证。

许可证的格式设计直接影响到许可证的生成、分发和验证等流程的顺利进行。许可证文件中需要**包含能够识别客户与软件信息的字段**，如客户名称、客户ID、软件名称、版本号等，其中**客户ID、版本号等信息要与内置于分发给客户的应用中的信息一致**，在构建应用时可以通过类似下面的命令将客户ID、版本号等信息写入给客户定制的应用程序：

```
$go build -ldflags "-X main.version=$(version)" -o xxx
```


这些内容可以与许可证中的内容比对，防止许可证被不同客户滥用。

同时许可证还需要包含授权范围信息，如授权类型(试用版或正式版)、授权期限、业务相关的限制授权(比如：最大接入连接数量等)等，这决定了客户可以享受的软件使用权限。

以上的客户与软件信息和授权范围信息被称为许可证的**有效载荷**。

最后，许可证还要包含签名信息，以防止许可证文件被非法修改。签名信息通常是的**对有效载荷信息的摘要进行运算后的结果**。有了签名信息后，许可证就算制作完成了，并可以分发给客户导入到系统中。

统一格式的许可证文件便于厂商生成，也便于客户侧系统的解析与验证。

下面是我们为示例设计的license文件(.lic)的例子：

```
{
"license": {
"id": "01234567890",
"vendor": "XYZ Company",
"issuedTo": "DDD Company",
"issuedDate": "2023-10-01T00:00:00Z",
"expirationDate": "2024-09-30T23:59:59Z",
"product": "My App",
"version": "1.0",
"licenseType": "Enterprise",
"maxConnections": 1000
},
"signature": {
"algorithm": "SHA256withRSA",
"value": "Cm73yXxA7g0JOWel9xIZtyYOqAcFUnrOectrnI3jX9iQC9NVt61CuZogFdm72uPO5o+h4NhFEy0Lymgt29XFWEEVqrUnZuNRZee5W3UXsPC5vkhVt414Co5rsXuFFV/2UDFt36sF7rp30H53H/M7TCUF0spEfx+ybilS4xC5AjCPC4/1G7swQ2zCVvBfvQXhZkz953DdgMD3sBsqU2i0mMPbMHGGH6J6wXoHjCC6VQ0e3azVTVhiA40kxo5/uI0+ENOo559NIiPaZiAkgZgiuRFybJFk5Ib705BuaNHw6HfRk5DnxmWF/852cv32hT7it0is77p0wGODACkNkPL7YQ=="
}
}
```


接下来我们就基于这个license文件的设计来制作一个许可证并签发。

## 3. 许可证的制作与签发

### 3.1 生成客户专用的私钥和公钥证书

为了给客户制作许可证，我们需要为客户生成一对专用的私钥和公钥证书，这个过程与[《Go TLS服务端绑定证书的几种方式》](https://tonybai.com/2023/10/13/multiple-ways-to-bind-certificates-on-go-tls-server-side)一文中的证书制作步骤一致，我们来看一下生成私钥和公钥证书的代码：

```
// app-licensing/make_certs/main.go
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
// 生成叶子证书模板,CN为DDD Company
leafTemplate := x509.Certificate{
SerialNumber: big.NewInt(3),
Subject: pkix.Name{
Organization: []string{"DDD Company"},
CommonName: "ddd.com",
},
NotBefore: time.Now(),
NotAfter: time.Now().Add(time.Hour * 24 * 365),
KeyUsage: x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature,
ExtKeyUsage: []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
SubjectKeyId: []byte{1, 2, 3, 4},
}
// 用中间CA证书签名生成叶子证书
leafCert, err := x509.CreateCertificate(rand.Reader, &leafTemplate, &interTemplate, &leafKey.PublicKey, interKey)
checkError(err)
// 将证书和密钥编码为PEM格式
caCertPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: caCert})
caKeyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(caKey)})
interCertPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: interCert})
interKeyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(interKey)})
leafCertPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: leafCert})
leafKeyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(leafKey)})
// 将PEM写入文件
writeDataToFile("ca-cert.pem", caCertPEM)
writeDataToFile("ca-key.pem", caKeyPEM)
writeDataToFile("inter-cert.pem", interCertPEM)
writeDataToFile("inter-key.pem", interKeyPEM)
writeDataToFile("ddd-cert.pem", leafCertPEM)
writeDataToFile("ddd-key.pem", leafKeyPEM)
}
```


我们分别生成了CA根、中间CA以及用于DDD Company许可证签发的专用key(ddd-key.pem)和公钥证书(ddd-cert.pem)，执行上述代码后，我们将在目录下看到如下文件：

```
// app-licensing/make_certs
$go run main.go
$ls
ca-cert.pem ddd-cert.pem go.mod inter-key.pem
ca-key.pem ddd-key.pem inter-cert.pem main.go
```


### 3.2 制作许可证文件

有了ddd-key.pem后，我们就可以来制作专供DDD Company的许可证了。我们建立make_lic目录，将ddd-key.pem拷贝到该目录下。

下面是用于生成许可证文件的main函数代码片段(忽略了一些错误处理)：

```
// app-licensing/make_lic/main.go
// 1. 建立对应license和Signature的结构体类型
type License struct {
ID string `json:"id"`
Vendor string `json:"vendor"`
IssuedTo string `json:"issuedTo"`
IssuedDate string `json:"issuedDate"`
ExpirationDate string `json:"expirationDate"`
Product string `json:"product"`
Version string `json:"version"`
LicenseType string `json:"licenseType"`
MaxConnections int `json:"maxConnections"`
}
type Signature struct {
Algorithm string `json:"algorithm"`
Value string `json:"value"`
}
func main() {
keyData, _ := os.ReadFile("ddd-key.pem") // 加载私钥
block, _ := pem.Decode(keyData)
if block == nil || block.Type != "RSA PRIVATE KEY" {
log.Fatal("failed to decode PEM block containing private key")
}
priKey, err := x509.ParsePKCS1PrivateKey(block.Bytes)
if err != nil {
log.Fatal(err)
}
// 2. 填充license的各个字段的值
var license License
license.ID = "01234567890"
license.Vendor = "XYZ Company"
license.IssuedTo = "DDD Company"
license.IssuedDate = "2023-10-01T00:00:00Z"
license.ExpirationDate = "2024-09-30T23:59:59Z"
license.Product = "My App"
license.Version = "1.0"
license.LicenseType = "Enterprise"
license.MaxConnections = 1000
// 3. 将各个字段连接后sha256摘要
data := []string{
license.ID,
license.Vendor,
license.IssuedTo,
license.IssuedDate,
license.ExpirationDate,
license.Product,
license.Version,
license.LicenseType,
strconv.Itoa(license.MaxConnections),
}
payload := strings.Join(data, "")
hash := sha256.Sum256([]byte(payload))
// 4. 用私钥对摘要签名
signed, _ := rsa.SignPKCS1v15(rand.Reader, priKey, crypto.SHA256, hash[:])
// 5. 对签名结果base64编码
signedB64 := base64.StdEncoding.EncodeToString(signed)
// 6. 生成signature对象
signature := Signature{
Algorithm: "SHA256withRSA",
Value: signedB64,
}
// 7. 序列化为json
fullLicense := map[string]interface{}{
"license": license,
"signature": signature,
}
jsonData, _ := json.MarshalIndent(fullLicense, "", " ")
// 8. 保存为.lic文件
os.WriteFile("ddd-company.lic", jsonData, 0644)
}
```


我们看到main函数制作许可证文件的步骤有很多，这里用下面这幅示意图来直观的说明一下：

![](../../assets/5fbec31b6e81e732.png)


证书的输入是有效载荷，包括客户与软件信息(比如ID、Product)、授权信息(比如IssueTo、IssuedDate、ExpirationDate等)、业务授权相关信息(比如MaxConnections等)。

我们将这些输入信息按声明顺序做字符串排列，并对获得的最终字符串做Sha256的单向散列得到摘要信息(摘要长度固定，运算速度较快)。

摘要信息是私钥签名的操作对象。签名后的信息转换为base64编码，最后存入许可证文件中。

这个许可证制作完毕后，就可以分发给客户了。客户拿到许可证，导入到系统中，这时系统就会对导入的许可证进行验证。下面我们就接着来看看如何使用伴随系统一起分发的公钥证书对许可证进行验签。

## 4. 许可证的验证

对许可证验证的过程和步骤可以用下面示意图来表示：

![](../../assets/eec5e130a42374db.png)


我们看到：图中verify signature有三个输入：公钥、从许可证文件中读取的经过base64 decode后的签名值(signature value)和基于许可证中字段计算出的摘要值。使用公钥对signature value进行运算得到的摘要值与基于许可证中字段计算出的摘要值如果一致，则说明验签成功。

基于图中流程，我们给出该示例验签部分的代码实现：

```
// app-licensing/verify_lic/main.go
func main() {
// 1. 加载公钥证书,提取公钥
certData, _ := os.ReadFile("ddd-cert.pem")
block, _ := pem.Decode(certData)
cert, _ := x509.ParseCertificate(block.Bytes)
pubKey := cert.PublicKey.(*rsa.PublicKey)
// 2. 解析许可证文件
licData, err := os.ReadFile("ddd-company.lic")
if err != nil {
panic(err)
}
var license License
var signature Signature
err = json.Unmarshal(licData, &struct{ License *License }{&license})
if err != nil {
panic(err)
}
err = json.Unmarshal(licData, &struct{ Signature *Signature }{&signature})
if err != nil {
panic(err)
}
// 3. 生成签名摘要
data := []string{
license.ID,
license.Vendor,
license.IssuedTo,
license.IssuedDate,
license.ExpirationDate,
license.Product,
license.Version,
license.LicenseType,
strconv.Itoa(license.MaxConnections),
}
payload := strings.Join(data, "")
hash := sha256.Sum256([]byte(payload))
// 4. 使用公钥验签
signValue, _ := base64.StdEncoding.DecodeString(signature.Value)
err = rsa.VerifyPKCS1v15(pubKey, crypto.SHA256, hash[:], signValue)
if err != nil {
fmt.Println("Invalid signature:", err)
} else {
fmt.Println("Signature verified")
}
}
```


## 5. 小结

本文介绍了如何利用数字签名和公钥基础设施实现软件许可证的安全可靠验证。通过设计许可证格式，包含客户标识、授权范围等关键信息，并添加软件供应商的数字签名，可以生成包含授权信息和不可篡改性的许可证文件。许可证签发方持有私钥对证书内容进行签名，而客户侧部署的系统则持有厂商的公钥来验证签名的有效性。整个流程无需连接签发服务器即可完成验证。这种模式解决了传统方式的诸多访问控制难题，实现了可靠、安全、便捷的分布式许可证验证方式。

当然我们也需要注意一些该机制的潜在问题，如私钥保护、公钥可信传递等。同时当有人将系统和许可证做整体复制时，这个方案也无法限制住这种非授权使用(只能等待许可证过期)。

最后，软件厂商可以按产品、客户来管理私钥和签发的证书(如下图所示)：

![](../../assets/c8b0fa828840276c.png)


本文示例所涉及的Go源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/app-licensing)下载。

注：代码仓库中的证书和key文件有效期为一年，大家如发现证书已经过期，可以在make_certs目录下重新生成各种证书和私钥并copy到对应的其他目录中去。


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