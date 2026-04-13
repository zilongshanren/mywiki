---
title: 通过实例理解OpenID身份认证
url: https://tonybai.com/2023/12/22/understand-oidc-by-example/
published: '2023-12-22'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解OpenID身份认证

![](../../assets/5cde779b1e0d362c.png)


[本文永久链接](https://tonybai.com/2023/12/22/understand-oidc-by-example) – https://tonybai.com/2023/12/22/understand-oidc-by-example

在《[通过实例理解OAuth2](https://tonybai.com/2023/12/16/understand-oauth2-by-example)》一文中，我们以实例方式讲解了OAuth2授权码模式(Authorization Code)模式的工作原理。实例中的照片冲印服务经过用户(tonybai)的授权后，使用用户提供的code(实则是由授权服务器分配并通过用户的浏览器重定向到照片冲印服务的)到授权服务器换取了access token，并最终使用access token从云盘系统中读取到了用户的照片信息。

不过，拿到了access token的照片冲印服务并不知道这个access token代表的是云盘服务上的哪个用户，要不是云盘服务在照片list接口返回了用户名(tonybai)，照片冲印服务还需要自己为授权给它的用户创建一个临时的用户id标识。当tonybai用户一周后再次访问照片冲印服务时，照片冲印服务还需要再走一次OAuth2授权流程，这对用户的体验并不好。

从照片冲印服务角度来说，它希望在用户第一次使用服务并授权时，就能得到用户身份信息，将用户加入到自己的用户体系中，并通过类似[基于会话的身份认证机制](https://tonybai.com/2023/10/23/understand-go-web-authn-by-example)在用户后续使用服务时自动识别并认证用户身份。这样，既可以避免用户额外单独注册账号的不佳体验，又可以避免用户下次使用服务时繁琐地授权过程。

然而，尽管OAuth 2.0是一个需要用户交互的安全协议，但它终归不是身份认证协议。但很多像照片冲印服务这样的应用还有通过像云盘系统这一的大厂应用进行用户身份认证的强烈需求，于是有很多厂商都制定了各自专用的标准，比如Facebook、Twitter、LinkedIn和GitHub等，但这些都是专用协议，缺乏标准性，开发者要逐一开发和适配。

于是[OpenID基金会](https://openid.net/foundation/)基于OAuth2.0制定了[OpenID Connect(简称OIDC)](https://en.wikipedia.org/wiki/OpenID)这样的开放身份认证协议标准，可以在不同厂商之间通用。

在这篇文章中，我们就来介绍一下基于OpenID的身份认证原理，有了上一篇OAuth2做铺垫，OIDC理解起来就非常容易了。

## 1. OpenID Connect(OIDC)简介

OpenID Connect是一个开放标准，由OpenID基金会于2014年2月发布。它定义了一种使用OAuth 2.0执行用户身份认证的互通方式。由于该协议的设计具有互通性，一个OpenID客户端应用可以使用同一套协议语言与不同的身份提供者交互，而不需要为每一个身份提供者实现一套有细微差别的协议。OpenID Connect直接基于OAuth 2.0构建，并保持了OAuth2.0的兼容性。现实世界中，在多数情况下，OIDC都会与保护其他API的OAuth基础架构部署在一起。

我们在[学习OAuth 2.0](https://tonybai.com/2023/12/16/understand-oauth2-by-example)时，首先了解了该协议涉及的几个实体，如Client、Authorization Server、Resource Server、Resource owner、Protected resouce等，以及它们的交互流程。知道了这些也就掌握了OAuth2的内核。以此为鉴，我们学习OIDC协议，也从了解都有哪些实体参与了协议交互，以及它们的具体交互流程开始。

OpenID Connect是一个协议套件([OpenID Connect Protocol Suite](https://openid.net/developers/how-connect-works/))，涉及Core、Discovery、Dynamic Client Registration等：

![](../../assets/1142cafdcfcf5045.jpg)


不过这里我们仅聚焦[OpenID Connect的core 1.0协议规范](https://openid.net/specs/openid-connect-core-1_0.html)。

就像OAuth2.0支持四种授权模式一样，OIDC基于这四种模式，整合出了三种身份认证类型：

- Authentication using the Authorization Code Flow
- Authentication using the Implicit Flow
- Authentication using the Hybrid Flow

其中Authentication using the Authorization Code Flow这种基于OAuth2授权码流程的身份认证方案应该是使用最为广泛的，本文也将基于这个流程对OIDC进行理解，并赋以实例。

### 1.1 OIDC协议中的实体与交互流程图

下面是OIDC规范中给出的通用的身份认证流程图，这个图是高度抽象的，适合上面三个flow：

![](../../assets/0a55dc63b253267e.png)


通过这个图，我们先来认识参与OIDC流程中的三个实体：

- RP(Relying Party)

图的最左端是一个叫RP的实体，如果对应到OAuth2.0那篇文章中的示例，这个RP对应的就是示例中的照片冲印服务，也就是OAuth2.0中的Client，即需要用户(EU)授权的那个实体。

- OP(OpenID Provider)

OP对应的是OAuth2.0中的Authorization Server+Resource Server，不同的是在OIDC这个特殊场景下，Resource Server中存储的resource就是用户的**身份信息**。

- EU(End User)

EU，顾名思义就是使用RP服务的用户，它对应OAuth2.0中的Resource Owner。

结合这些实体、上面的抽象流程图以及OAuth2授权码模式的交互图，我画一下OIDC基于授权码模式进行身份认证的实体间的交互图，这里我们依旧以用户使用照片冲印服务为例：

![](../../assets/23464c49f12a430d.png)


上图就是一个基于授权码流程的OIDC协议流程，是不是赶脚跟OAuth 2.0中的授权码模式的流程几乎完全一致啊!

唯一的区别就是授权服务器(OP)在返回access_token的同时，还多返回了一个ID_TOKEN，我们称这个ID_TOKEN为ID令牌，这个令牌是OIDC身份认证的关键。

### 1.2 ID_TOKEN的组成

从上图中，我们看到ID_TOKEN与普通的OAuth access_token一起提供给Client(RP)使用，与access_token不同的是，RP是需要对ID_TOKEN进行解析的。那么这个ID_TOKEN究竟是什么呢？在OIDC协议中，ID_TOKEN是一个经过签名的[JWT](http://jwt.io)，

OIDC协议规范规定了该jwt应该包含的字段信息，包括必选的(REQUIRED)与可选的(OPTIONAL)，在这里我们了解下面的必选字段信息即可：

- iss

令牌的颁发者，其值就是身份认证服务（OP）的URL，比如：http://open.my-yunpan.com:8081/oauth/token，不包含问号作为前缀的查询参数等。

- sub

令牌的主题标识符，其值是最终用户(EU)在身份认证服务(OP)内部的唯一且永不重新分配的标识符。

- aud

令牌的目标受众，其值是Client（RP）的标识，必须包含RP的OAuth 2.0客户端ID(client_id)，也可以包含其他受众的标识符。

- exp

过期时间，过期后ID_TOKEN将会失效。其值是一个JSON number，表示从1970-01-01T0:0:0Z开始（以 UTC 度量）到过期日期/时间为止的秒数。

- iat

认证时间，即版本ID_TOKEN的时间，其值是一个JSON number，表示从1970-01-01T0:0:0Z开始（以 UTC 度量）到认证日期/时间为止的秒数。

注：如果客户端(RP)向身份认证服务器(OP)注册过公钥，则可以使用客户端公钥对该JWT进行非对称签名校验，或者可以使用客户端密钥对该JWT进行对称签名。这种方式可以提高客户端的安全等级，因为可以避免在网络上传递密钥。


在上面图中使用access_token获取user_info的环节中，RP可以通过ID_TOKEN中的sub（EU唯一标识符）到授权服务器的userinfo端点换取用户的基本信息，这样在RP自己的页面上展示EU的标识时就不可以不用9XDF-AABB-001ACFE这样的唯一标识符(sub)，而是用TonyBai这样的可理解的字符串了。

注：OpenID Connect使用一个特殊的权限范围值openid来控制对UserInfo端点的访问。OpenID Connect定义了一组标准化的OAuth权限范围，对 应于用户属性的子集，比如profile 、email 、phone 、address等。


了解了OIDC的身份认证流程以及ID_TOKEN的组成后，我们就算对OIDC有个直观的认知了，接下来我们用一个实例来加深一下对OIDC身份认证的理解。

## 2. OIDC实例

如果你理解了《[通过实例理解OAuth2](https://tonybai.com/2023/12/16/understand-oauth2-by-example)》一文中的实例，那么理解本篇文章中的OIDC实例将是轻而易举的事情。前面说过，OIDC建构在OAuth2之上，与OAuth2兼容，因此，这里的OIDC实例也改自OAuth2一文中的实例。

与OAuth2一文实例相比，OIDC实例中去掉了云盘服务(my-yunpan)，仅保留了下面结构：

```
$tree -L 2 -F oidc-examples
oidc-examples
├── my-photo-print/
│ ├── go.mod
│ ├── go.sum
│ ├── home.html
│ ├── main.go
│ └── profile.html
└── open-my-yunpan/
├── go.mod
├── go.sum
├── main.go
└── portal.html
```


其中my-photo-print是照片冲印服务，也是oidc实例中的RP实体，而open-my-yunpan扮演着云盘授权服务，是oidc实例中的OP实体。在编写和运行服务之前，我们同样要先修改一下本机(MacOS或Linux)的/etc/hosts文件：

```
127.0.0.1 my-photo-print.com
127.0.0.1 open.my-yunpan.com
```


注：在演示下面步骤前，请先进入到oidc-examples的两个目录下，通过go run main.go启动各个服务程序(每个程序一个终端窗口)。


### 2.1 用户使用my-photo-print.com照片冲印服务

按照流程，用户首先通过浏览器打开照片冲印服务的首页：http://my-photo-print.com:8080，如下图：

![](../../assets/f338dc748ee877ca.png)


这与OAuth2一文中的实例并无什么差别，该页面也是由my-photo-print/main.go中的homeHandler提供的，它的home.html渲染模板也基本没有变化，因此这里就不赘述了。

当用户选择并点击“使用云盘账号登录”时，浏览器将打开云盘授权服务(OP)的首页(http://open.my-yunpan.com:8081/oauth/portal)。

### 2.2 使用open.my-yunpan.com进行授权，包括openid权限

云盘授权服务的首页还是“老样子”，唯一的差别就是请求的权限包含了一项openid(有my-photo-print的home.html带过来的)：

![](../../assets/098d90cca6646322.png)


这个页面同样由open.my-yunpan.com的portalHandler提供，它的逻辑与oauth2的实例相比没有变化，这里也罗列其代码了。

当用户(EU)填写用户名和密码后，点击“授权”，浏览器便会向云盘授权服务的”/oauth/authorize”发起post请求以获取code，负责”/oauth/authorize”端点的authorizeHandler会对用户进行身份认证，通过后，它会分配code并向浏览器返回重定向的应答，重定向的地址就是照片冲印服务的回调地址：http://my-photo-print.com:8080/cb?code=xxx&state=yyy。

### 2.3 获取access token以及id_token，并用用户唯一标识获取用户基本信息(profile)

这个重定向相当于用户浏览器向http://my-photo-print.com:8080/cb?code=xxx&state=yyy发起请求，为照片冲印服务提供code，该请求由my-photo-print的oauthCallbackHandler处理：

```
// oidc-examples/my-photo-print/main.go
// callback handler，用户(EU)拿到code后调用该handler
func oauthCallbackHandler(w http.ResponseWriter, r *http.Request) {
fmt.Println("oauthCallbackHandler:", *r)
code := r.FormValue("code")
state := r.FormValue("state")
// check state
mu.Lock()
_, ok := stateCache[state]
if !ok {
mu.Unlock()
fmt.Println("not found state:", state)
w.WriteHeader(http.StatusBadRequest)
return
}
delete(stateCache, state)
mu.Unlock()
// fetch access_token and id_token with code
accessToken, idToken, err := fetchAccessTokenAndIDToken(code)
if err != nil {
fmt.Println("fetch access_token error:", err)
return
}
fmt.Println("fetch access_token ok:", accessToken)
// parse id_token
mySigningKey := []byte("iamtonybai")
claims := jwt.RegisteredClaims{}
_, err = jwt.ParseWithClaims(idToken, &claims, func(token *jwt.Token) (interface{}, error) {
return mySigningKey, nil
})
if err != nil {
fmt.Println("parse id_token error:", err)
return
}
// use access_token and userID to get user info
up, err := getUserInfo(accessToken, claims.Subject)
if err != nil {
fmt.Println("get user info error:", err)
return
}
fmt.Println("get user info ok:", up)
mu.Lock()
userProfile[claims.Subject] = up
mu.Unlock()
// 设置cookie
cookie := http.Cookie{
Name: "my-photo-print.com-session",
Value: claims.Subject,
Domain: "my-photo-print.com",
Path: "/profile",
}
http.SetCookie(w, &cookie)
w.Header().Add("Location", "/profile")
w.WriteHeader(http.StatusFound) // redirect to /profile
}
```


这个handler中做了很多工作。首先是使用code像授权服务器换取access token和id_token，授权服务器负责颁发token的是tokenHandler：

```
// oidc-examples/open-yunpan/main.go
func tokenHandler(w http.ResponseWriter, r *http.Request) {
fmt.Println("tokenHandler:", *r)
// check client_id and client_secret
user, password, ok := r.BasicAuth()
if !ok {
fmt.Println("no authorization header")
w.WriteHeader(http.StatusNonAuthoritativeInfo)
return
}
mu.Lock()
v, ok := validClients[user]
if !ok {
fmt.Println("not found user:", user)
mu.Unlock()
w.WriteHeader(http.StatusNonAuthoritativeInfo)
return
}
mu.Unlock()
if v != password {
fmt.Println("invalid password")
w.WriteHeader(http.StatusNonAuthoritativeInfo)
return
}
// check code and redirect_uri
code := r.FormValue("code")
redirect_uri := r.FormValue("redirect_uri")
mu.Lock()
ac, ok := codeCache[code]
if !ok {
fmt.Println("not found code:", code)
mu.Unlock()
w.WriteHeader(http.StatusNotFound)
return
}
mu.Unlock()
if ac.redirectURI != redirect_uri {
fmt.Println("invalid redirect_uri:", redirect_uri)
w.WriteHeader(http.StatusBadRequest)
return
}
var authResponse struct {
AccessToken string `json:"access_token"`
IDToken string `json:"id_token,omitempty"`
ExpireIn int `json:"expires_in"`
}
// generate access_token
authResponse.AccessToken = randString(16)
authResponse.ExpireIn = 3600
now := time.Now()
expired := now.Add(10 * time.Minute)
claims := jwt.RegisteredClaims{
Issuer: "http://open.my-yunpan.com:8091/oauth/token",
Subject: ac.userID,
Audience: jwt.ClaimStrings{user}, //client_id
IssuedAt: &jwt.NumericDate{now},
ExpiresAt: &jwt.NumericDate{expired},
}
if strings.Contains(ac.scopeTxt, "openid") {
// generate id_token if contains openid
mySigningKey := []byte("iamtonybai")
jwtToken := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
authResponse.IDToken, _ = jwtToken.SignedString(mySigningKey)
}
respData, _ := json.Marshal(&authResponse)
w.Write(respData)
}
```


我们看到tokenHandler先是对客户端(client)凭据做了校验，接下来验证code，如果code通过验证，则会分配access_token，并根据scope中是否包含openid决定是否分配id_token，这里我们的权限授权中包含了openid，于是tokenHandler将id_token(一个jwt)一并生成并返回给client。

而拿到access_token和id_token的my-photo-print的oauthCallbackHandler会解析id_token，提取其中的有效信息，比如subject等，并用access_token和id_token中的subject(用户的唯一ID)去授权服务获取用户(EU)的基础身份信息(姓名、主页、邮箱等)，并将用户的唯一ID作为cookie存入用户的浏览器。最后让浏览器重定向到my-photo-print的profile页面。

请注意：这里仅是为了简便起见，生产环境请考虑更为安全的会话机制。


profile页面的处理函数为profileHandler：

```
// oidc-examples/my-photo-print/main.go
// user profile页面
func profileHandler(w http.ResponseWriter, r *http.Request) {
fmt.Println("profileHandler:", *r)
cookie, err := r.Cookie("my-photo-print.com-session")
if err != nil {
http.Error(w, "找不到cookie，请重新登录", 401)
return
}
fmt.Printf("found cookie: %#v\n", cookie)
mu.Lock()
pf, ok := userProfile[cookie.Value]
if !ok {
mu.Unlock()
fmt.Println("not found user:", cookie.Value)
// 跳转到首页
http.Redirect(w, r, "/", http.StatusSeeOther)
return
}
mu.Unlock()
// 渲染照片页面模板
tmpl := template.Must(template.ParseFiles("profile.html"))
tmpl.Execute(w, pf)
}
```


我们看到：该handler首先查找cookie中是否存在用户ID，如果不存在，则重定向到登录页面，如果存在，则取出用户唯一ID，并使用该ID查找用户profile信息，最后展示到web页面上：

![](../../assets/2bb0c26ea77af2e4.png)


到这里，我们看到：这种委托云盘授权服务对my-photo-print的用户进行身份认证并拿到该用户基本信息的机制，就是oidc。

注：一旦拿到云盘授权服务身份认证后的用户信息，RP便可以使用各种身份认证机制来管理EU用户，比如RP可以使用会话管理技术（例如使用会话标识符或浏览器cookie）来跟踪EU的会话状态。如果EU在同一会话期间访问RP应用，RP可以通过会话标识符来识别EU，而无需再次进行身份验证。


## 3. 小结

通过上面的内容，我们对OpenID Connect(OIDC)有了更直观的理解，这里做一个小结:

- OIDC是一套身份认证的开放标准协议，基于OAuth 2.0构建，与OAuth 2.0兼容。
- OIDC协议中主要涉及三个角色：RP(依赖方)、OP(身份提供方)、EU(最终用户)。
- EU通过RP使用OP进行身份认证后，RP可以获得EU的身份信息。整个流程与OAuth 2.0的授权码流程高度相似。
- 关键的差别在于：OP返回的token中除了access_token外，还包含一个ID_TOKEN(JWT格式)。
- RP通过解析ID_TOKEN可以获得EU的唯一标识等信息，并通过access_token进一步获取EU的详细身份信息。
- RP获得EU身份信息后，可以通过各种机制识别和管理EU，无需EU重复身份验证。

总的来说，OIDC利用OAuth 2.0流程进行身份认证，通过额外返回的ID_TOKEN提供EU身份信息，很好地满足了RP对EU身份管理的需求。

文本涉及的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/oidc-examples)下载。

## 4. 参考资料

[OIDC(OpenID Connect) Specification](https://openid.net/specs/openid-connect-core-1_0.html)- https://openid.net/specs/openid-connect-core-1_0.html[利用OAuth 2.0实现一个OpenID Connect用户身份认证协议](https://time.geekbang.org/column/article/262672)- https://time.geekbang.org/column/article/262672

[“Gopher部落”知识星球](https://public.zsxq.com/groups/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

![img{512x368}](../../assets/c4a1500def8561d3.png)


![img{512x368}](../../assets/547482cabd3c0134.png)


![img{512x368}](../../assets/311cf32e055e496a.png)


![img{512x368}](../../assets/f6b41cd44e73c829.jpg)


著名云主机服务厂商DigitalOcean发布最新的主机计划，入门级Droplet配置升级为：1 core CPU、1G内存、25G高速SSD，价格5$/月。有使用DigitalOcean需求的朋友，可以打开这个[链接地址](https://m.do.co/c/bff6eed92687)：https://m.do.co/c/bff6eed92687 开启你的DO主机之路。

Gopher Daily(Gopher每日新闻) - https://gopherdaily.tonybai.com

我的联系方式：

- 微博(暂不可用)：https://weibo.com/bigwhite20xx
- 微博2：https://weibo.com/u/6484441286
- 博客：tonybai.com
- github: https://github.com/bigwhite
- Gopher Daily归档 - https://github.com/bigwhite/gopherdaily

![](../../assets/769fc94e8bba6b65.png)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。

© 2023, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论