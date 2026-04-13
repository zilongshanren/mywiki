---
title: 通过实例理解Web应用用户密码存储方案
url: https://tonybai.com/2023/10/25/understand-password-storage-of-web-app-by-example/
published: '2023-10-25'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解Web应用用户密码存储方案

![](../../assets/7acdfd66afb1b2e1.png)


[本文永久链接](https://tonybai.com/2023/10/25/understand-password-storage-of-web-app-by-example) – https://tonybai.com/2023/10/25/understand-password-storage-of-web-app-by-example

在上一篇文章[《通过实例理解Go Web身份认证的几种方式》](https://tonybai.com/2023/10/23/understand-go-web-authn-by-example)中，我们了解了Web应用的多种身份验证方式。但无论哪种方式，用户初次访问Web应用的注册流程和登录流程是不可避免的，而基于用户名密码的注册流程依旧是当今主流。注册后，Web应用后端是如何保存用户密码的呢？历史上都有哪些存储方案？当今的主流存储方案又是什么呢？在这篇文章中，我们就来说说Web应用的各种密码存储方案的优缺点，并通过实例来理解一下当前的主流存储方案。

## 1. Web应用用户密码存储的重要性

用户密码是访问Web应用的关键，它直接关乎到用户账号和应用数据的安全。

如果用户密码被泄露或破解，将导致严重后果。后果最轻的算是某个用户或某少数用户的账号被盗用了，用户将失去对账号的控制。盗用账号后，攻击者可以获取该用户的私密信息，或进行额外的攻击；如果用户在多个应用重复使用同一密码，那么后果将进一步严重，用户的一系列账号都将受到安全威胁；更为严重的是Web应用存储用户账号信息的数据库被攻破(俗称“脱库”)，攻击者会拿到存储的全部用户账号信息等，如果用户密码存储不当，攻击者可以很容易破译所有用户的密码，并基于这些密码信息做进一步的攻击。

由此可见，Web应用必须非常重视用户密码的存储安全。在当前弱密码和频繁密码泄露成为常态的背景下，Web应用开发者有责任使用安全的密码存储方案，尽力保护用户信息安全，即便在被脱库的最糟糕情况下，也不让攻击者轻易破解出用户的密码，这也关系到应用和企业的信誉。

## 2. 密码存储方案的演进：魔高一尺，道高一丈

Web应用用户密码存储方案的演进历史可以分为以下几个阶段，如图所示：

![](../../assets/3918b2ce8b6ff2ad.png)


下面我们按图中的演进顺序，对各阶段的密码存储方案逐一说明一下。

### 2.1 起始阶段 – 明文存储

早期的Web应用为了实现简单，采用了最简单“粗暴”的用户密码存储方式：明文存储，即直接把用户的密码以纯文本形式存储在数据库中。

显然这种方式的最大优点就是实现简单，验证登录时直接比对明文密码。但这种方式最大的缺点就是**极其不安全**，密码一旦泄露就失去了全部保密性。但当时人们的安全意识较弱，该方案被广泛使用。

### 2.2 弱哈希算法阶段 – MD5和SHA1

随着时间的推移，CPU和GPU性能的提升使得字典破解和穷举攻击更加可行有效，大量密码被泄露的事件引起人们对密码安全的重视，人们更多地认识到明文存储密码的危险性。同时，Web应用的发展也从追求功能和便利，转变为在易用性与安全性之间求平衡。政府和行业协会也开始指定密码存储的最新安全要求的规范和政策，密码学等相关技术的快速发展也为更安全的密码存储提供了前提和支持。

于是人们开始使用MD5、SHA1等单向哈希算法对密码进行处理，只存储密码的哈希值。虽然增加了一定的密码存储的复杂性，但其最大的优点就是在一定程度上放置了明文存储的密码泄露问题。

不过，随着大量使用MD5和SHA-1的应用遭到破解，这些哈希算法的脆弱性暴露无遗。同时彩虹表攻击的出现，让破解者只需要预计算密码哈希表就可以快速破解以弱哈希存储的密码。

于是技术社区以及安全规范都开始提倡和推荐采用更安全的密码存储方案，即采用**加盐方案**。

### 2.3 加盐哈希阶段 – 增加随机盐值

加盐哈希就是在计算密码的哈希值时，在密码字符串前/后面添加一个称为“盐(salt)”的随机字符串，这个随机字符串称为**盐值**，它的作用是增加哈希后密码的随机性。

加盐哈希的步骤大致如下图：

![](../../assets/f778d98a2dbe878d.png)


在用户注册阶段，系统根据用户输入的密码生成在数据库中的哈希密码值：

- 系统首先随机生成一个足够长的随机字符串作为盐值，可以使用密码学安全的随机数生成算法；
- 将盐值与用户输入的原始密码字符串拼接在一起(盐值放在密码的前后均可)；
- 对连接后的字符串计算哈希值，可以使用MD5、SHA-1、SHA256、SHA-512等哈希算法；由于也被证实MD5、SHA-1存在弱点，可以被碰撞攻击，建议至少使用SHA256算法；
- 将盐值和哈希值一起存储在数据库中(可以向图中那样将hashed_password和salt通过:分隔符组合为一个字段后再存储在数据库中)。

验证登录时，系统根据用户名取出盐值，然后将用户输入的密码与盐值组合计算哈希值，与存储的原始哈希值比较，相同则验证成功。

在密码哈希前加入随机字符串(即“盐(salt)”)可以大幅增加了破解难度，同时不同用户如采用相同密码，也可以通过不同的盐在哈希后得到不同的哈希值，这可以有效地防止预计算表的攻击。

不过随着硬件算力的飞速提高，比如GPU、专用ASIC芯片以及云计算资源等，密码破解效率进一步提高，甚至普通人也可利用现成的破解工具和云资源进行密码破解，攻击者门槛大幅降低，简单加盐也已出现不能有效对抗硬件加速破解的情况。

于是人们开始考虑使用一些新哈希算法，这些算法可以大幅提高攻击者付出的时间和资源消耗成本，增加密码破解难度，这就是下面我们要说的慢哈希算法。

### 2.4 慢哈希算法阶段 – Argon2、Bcrypt、Scrypt和PBKDF2

[Argon2](https://www.argon2.com/)、[Bcrypt](http://en.wikipedia.org/wiki/Bcrypt)、[Scrypt](http://www.tarsnap.com/scrypt.html)和[PBKDF2](http://en.wikipedia.org/wiki/PBKDF2)是目前主流的慢哈希算法，它们与SHA256等快速哈希算法的主要差异点如下:

- 计算速度更慢，需要消耗更多CPU和内存资源，从而对抗硬件加速攻击；
- 使用更复杂的算法，组合密码学原语，增加破解难度；
- 可以配置资源消耗参数，调整安全强度；
- 特定优化使并行计算困难；
- 经过长时间的密码学分析，仍然安全可靠。

从这些特点可以知道：这些慢哈希算法更适合密码哈希的原因是可以大幅增加攻击者密码破解的成本，如果这么说大家印象还不够深刻，我们就来量化对比一下，下面是以SHA256和Scrypt两个算法为例做的一个简单的benchmark测试：

```
// web-app-password-storage/benchmark/benchmark_test.go
package main
import (
"crypto/sha256"
"testing"
"golang.org/x/crypto/scrypt"
)
func BenchmarkSHA256(b *testing.B) {
b.ReportAllocs()
data := []byte("hello world")
b.ResetTimer()
for i := 0; i < b.N; i++ {
sha256.Sum256(data)
}
}
func BenchmarkScrypt(b *testing.B) {
b.ReportAllocs()
const keyLen = 32
data := []byte("hello world")
b.ResetTimer()
for i := 0; i < b.N; i++ {
scrypt.Key(data, data, 16384, 8, 1, keyLen)
}
}
```


我们看看输出的benchmark结果是什么样的：

```
$go test -bench .
goos: darwin
goarch: amd64
pkg: demo
... ...
BenchmarkSHA256-8 6097324 195.3 ns/op 0 B/op 0 allocs/op
BenchmarkScrypt-8 26 41812138 ns/op 16781836 B/op 22 allocs/op
PASS
ok demo 2.533s
```


我们看到无论是cpu消耗还是内存开销，Scrypt算法都是SHA256的几个数量级的倍数。

加盐的慢哈希也是目前的**主流的用户密码存储方案**，那有读者会问：这四个算法选择哪个更佳呢？说实话要想对这个四个算法做个全面的对比，需要很强的密码学专业知识，这里直接给结论(当然也是来自网络资料)：建议使用Scrypt或Argon2系列的算法，它们俩可提供更高的抗ASIC和并行计算能力，Bcrypt由于简单高效和成熟，目前也仍十分流行。

不过，慢哈希算法在给攻击者带来时间和资源成本等困难的同时，也给服务端正常的身份认证带来一定的性能开销，不过大多数开发者认为这种设计取舍是值得的。

下面我们就基于慢哈希算法结合加盐，用实例说明一下一个Web应用的用户注册与登录过程中，密码是如何被存储和用来验证用户身份的。

## 3. 加盐哈希存储方案的示例

在这个示例中，我们建立两个html文件：一个是signup.html，用于模拟用户注册；一个是login.html，用于模拟用户登录：

```
// web-app-password-storage/signup.html
<!DOCTYPE html>
<html>
<head>
<title>注册</title>
</head>
<body>
<form action="http://localhost:8080/signup" method="post">
<label>用户名:</label>
<input type="text" name="username"/>
<label>密码:</label>
<input type="password" name="password"/>
<label>确认密码:</label>
<input type="password" name="confirm-password"/>
<button type="submit">注册</button>
</form>
</body>
</html>
// web-app-password-storage/login.html
<!DOCTYPE html>
<html>
<head>
<title>登录</title>
</head>
<body>
<form action="http://localhost:8080/login" method="post">
<label>用户名:</label>
<input type="text" name="username"/>
<label>密码:</label>
<input type="password" name="password"/>
<button type="submit">登录</button>
</form>
</body>
</html>
```


接下来，我们来写这个web应用的后端：一个http server：

```
// web-app-password-storage/server/main.go
package main
import (
"database/sql"
"encoding/base64"
"math/rand"
"net/http"
"strings"
"time"
"golang.org/x/crypto/scrypt"
_ "modernc.org/sqlite"
)
var db *sql.DB
func main() {
// 连接SQLite数据库
var err error
db, err = sql.Open("sqlite", "./users.db")
if err != nil {
panic(err)
}
defer db.Close()
// 创建用户表
sqltable := `
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
hashedpass TEXT
);
`
_, err = db.Exec(sqltable)
if err != nil {
panic(err)
}
http.HandleFunc("/login", login)
http.HandleFunc("/signup", signup)
http.ListenAndServe(":8080", nil)
}
func signup(w http.ResponseWriter, r *http.Request) {
username := r.FormValue("username")
password := r.FormValue("password")
cpassword := r.FormValue("confirm-password")
if password != cpassword {
http.Error(w, "password and confirmation password do not match", http.StatusBadRequest)
return
}
// 注册新用户
salt := generateSalt(16)
hashedPassword := hashPassword(password, salt)
stmt, err := db.Prepare("INSERT INTO users(username, hashedpass) values(?, ?)")
if err != nil {
panic(err)
}
_, err = stmt.Exec(username, hashedPassword+":"+salt)
if err != nil {
panic(err)
}
w.Write([]byte("signup ok!"))
}
func login(w http.ResponseWriter, r *http.Request) {
username := r.FormValue("username")
password := r.FormValue("password")
// 验证登录
storedHashedPassword, salt := getHashedPasswordForUser(db, username)
hashedLoginPassword := hashPassword(password, salt)
if hashedLoginPassword == storedHashedPassword {
w.Write([]byte("Welcome!"))
} else {
http.Error(w, "Invalid username or password", http.StatusUnauthorized) // 401
}
}
// 生成随机字符串作为盐值
func generateSalt(n int) string {
rand.Seed(time.Now().UnixNano())
letters := []rune("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
b := make([]rune, n)
for i := range b {
b[i] = letters[rand.Intn(len(letters))]
}
return string(b)
}
// 对密码进行bcrypt哈希并返回哈希值与随机盐值
func hashPassword(password, salt string) string {
dk, err := scrypt.Key([]byte(password), []byte(salt), 1<<15, 8, 1, 32)
if err != nil {
panic(err)
}
return base64.StdEncoding.EncodeToString(dk)
}
// 从数据库获取用户哈希后的密码和盐值
func getHashedPasswordForUser(db *sql.DB, username string) (string, string) {
var hashedPass string
row := db.QueryRow("SELECT hashedpass FROM users WHERE username=?", username)
if err := row.Scan(&hashedPass); err != nil {
panic(err)
}
split := strings.Split(hashedPass, ":")
return split[0], split[1]
}
```


示例的结构比较清晰，这里提供了两个http handler，一个是signup用于接收用户注册请求，一个是login，用于接收处理用户登录请求。在注册请求时，我们生成用户密码的带盐慢哈希值，与salt一起存入数据库，这里用sqlite代替通用关系型数据库；在login handler中，我们根据username读取数据库中的salt和hashed_password，然后基于请求中的password与salt重新做一遍hash，将得到的结果与数据库中读取的hashed_password比较，相同则说明用户输入的密码正确。

Go官方维护的golang.org/x/crypto为我们提供了高质量的scrypt包，当然crypto下也有bcrypt、argon2和pbkdf2的实现，感兴趣的童鞋可以自行研究。

## 4. 小结

用户密码的安全存储是保障Web应用与用户数据安全的基石。简单的密码存储实践如明文和弱哈希算法存在巨大隐患，而随着计算能力提升，任何weak password都可被轻松破解。为有效保护用户，Web应用必须采取更可靠的密码存储方案。

本文详细介绍了从简单明文、单向哈希到先进的加盐慢哈希的演进历程。我们看到，这是一场与不断增强的攻击手段进行的应对之争。随着硬件计算能力、并行与云计算等技术进步，必须加强密码存储机制的强度。当前，结合随机盐、迭代计算的慢哈希可大幅提高破解难度，是推荐的密码存储安全实践。

当然，密码安全需要持续关注新兴攻击手段，并及时采纳更强大的算法。这不仅是技术问题，也需要整个社区的共同努力，通过提高意识和最佳实践来保护用户。

本文示例所涉及的Go源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/web-app-password-storage)下载。

## 5. 参考资料

[《API安全实战》](https://book.douban.com/subject/36039150/)– https://book.douban.com/subject/36039150/[《API安全技术与实战》](https://book.douban.com/subject/35429043/)– https://book.douban.com/subject/35429043/[保密：系统如何保证敏感数据无法被内外部人员窃取滥用？](https://time.geekbang.org/column/article/334293)– https://time.geekbang.org/column/article/334293

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