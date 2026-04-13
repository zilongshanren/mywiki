---
title: 通过实例理解Web应用授权的几种方式
url: https://tonybai.com/2023/11/04/understand-go-web-authz-by-example/
published: '2023-11-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 通过实例理解Web应用授权的几种方式

![](../../assets/f9ae3a7f08d5d49f.png)


[本文永久链接](https://tonybai.com/2023/11/04/understand-go-web-authz-by-example) – https://tonybai.com/2023/11/04/understand-go-web-authz-by-example

在前面的系列文章中，我们了解了[Go Web应用身份认证的几种方式](https://tonybai.com/2023/10/23/understand-go-web-authn-by-example/)，也知道了该[如何相对安全地存储用户的密码信息](https://tonybai.com/2023/10/25/understand-password-storage-of-web-app-by-example)，最大程度减小在系统数据库被攻破时用户密码信息的泄露程度。

一旦用户通过身份验证，他/她就可以以合法的身份进入到系统中，那么问题来了：**用户进入系统后是否就可以“为所欲为”了呢**？显然不是! 比如我们以普通用户身份登录github，身份验证成功后，我们只能增删改自己账号下的代码仓库数据或读取其他用户的公开仓库(public)数据，我们无法修改和删除其他用户下面的仓库数据，甚至看不到其他用户的私有仓库。Web应用系统(比如github)的这种对用户可以使用什么功能、可以访问和修改哪些数据的管理和控制，就是**授权(Authorization)**，简称为**AuthZ**。

在这篇文章中，我们就结合实例一起来了解一下Web应用都有哪些种授权方式。

## 1. 授权：基于访问控制策略的评估与决策

在[Go Web应用身份认证的几种方式](https://tonybai.com/2023/10/23/understand-go-web-authn-by-example/)一文中，我们简要说明了身份认证(AuthN)与授权(AuthZ)的关系与差异。授权是基于用户身份认证的基础之上的，按时间发生顺序，授权也是发生在身份认证之后的。

授权的目的是**限制合法用户在系统中的操作**，限制未经允许的访问。这让很多人将授权与访问控制(access control)直接划上了等号。其实授权与访问控制的确是密不可分的，但它们之间也不是可以简单划等号的。下面示意图展示了一个Web应用系统中授权与访问控制的关系：

![](https://tonybai.com/wp-content/uploads/understand-go-web-authz-by-example-2.png)


从广义上看，授权和访问控制都属于对系统资源或信息的保护，它们的目的是限制未经授权的访问。从具体来看，访问控制关注的是如何控制主体访问对象，是一种机制或方法，它通常会定义访问模型以及相关访问策略；而授权则关注主体是否有权访问对象，是在已知用户身份以及访问控制策略下对访问请求的评估和决策过程，并得出主体是否具有访问权限的最终结果。

从上图我们也可以看到：授权是建立在访问控制之上的。访问控制定义了授权评估所需的模型、策略、机制和规则，授权则是在这套规则下，评估一个主体对一个对象的操作是否被允许，两者关系密不可分。在实现上，我们通常会联合使用“访问控制”和“授权”这两个概念，对外部更多用**授权**一词作为这个过程的统称。

到这里，我们理解了访问控制与授权的关系 – 访问控制提供了授权评估所需的模型和规则体系。针对不同的应用场景，IT界有几种典型的访问控制模型被提出和使用：

- 访问控制列表（Access Control List，ACL）
- 强制访问控制（Mandatory Access Control，MAC）
- 自主访问控制（Discretionary Access Control，DAC）
- 基于属性的访问控制（Attribute-Based Access Control， ABAC)
- 基于角色的访问控制(Role-Based Access Control， RBAC）

这些模型为我们建立访问策略提供了框架和抽象工具。理解不同访问控制模型的思想和适用场景，可以帮助我们更好地制定系统的安全访问策略。在接下来的内容中，我们会简单介绍这几种访问控制模型，包括它们应用场景、优缺点等。这也将帮助大家建立访问控制和授权评估的整体视角，也可以为后续使用Go语言实现授权控制的实例提供理论基础。

## 2. 访问控制模型

和任何其它IT技术一样，访问控制模型也有着自己的演进历史过程。下面我们沿着模型演进的时间线，逐个认识一下各个模型。

### 2.1 访问控制列表（Access Control List，ACL)

[ACL](https://en.wikipedia.org/wiki/Access-control_list)是最早的访问控制模型，基于ACL的访问控制会直接在被访问对象(也称为客体(O – Object))上设置允许/拒绝访问的主体(S – Subject)列表，最典型的就是Unix/Linux文件系统中文件的访问模型，如下图：

![](../../assets/d2c38e858ce8a3ad.png)


由此可见，这个模型并非专属于Web应用授权。早在上世纪60年代，它就广泛应用在操作系统中文件系统的访问权限管理。在1965年，Multics操作系统第一个实现了基于ACL模型的文件系统访问权限管理。POSIX曾推出ACL标准化草案，但后来放弃。但ACL并未因此受到打击，后来在NFSv4、Windows、Unix等系统中都有实现。之后，ACL被广泛地应用于网络领域，包括路由器、交换机以及防火墙都借助于访问控制列表来有效地控制用户对网络的访问，从而最大程度地保障网络安全。

ACL模型的优点是简单易用，但也存在灵活性差、难于扩展和满足复杂应用场景访问控制要求等不足。

ACL模型在现代Web应用中使用的越来越少，仅用于少数控制对特定资源访问权限的特定场景。例如，在静态文件服务器中，可以通过在文件系统中使用ACL来控制对文件或目录的访问权限。在复杂的现代Web应用领域，一些由ACL发展演化出的更灵活、更具扩展性的模型已经发展起来并走到了前台，比如后续即将要提到的RBAC和ABAC模型。

### 2.2 强制访问控制（Mandatory Access Control，MAC）

[强制访问控制（Mandatory Access Control，MAC）](https://en.wikipedia.org/wiki/Mandatory_access_control)起源于军用的[多级安全](https://en.wikipedia.org/wiki/Multilevel_security)系统，在MAC模型中，系统层强制执行访问控制策略，用户层无法更改。在操作系统领域，我们熟知的Linux的[SELinux](https://www.redhat.com/en/topics/linux/what-is-selinux)和[AppArmor](https://wiki.ubuntu.com/AppArmor)，Windows的[Mandatory Integrity Control](https://en.wikipedia.org/wiki/Mandatory_Integrity_Control)都属于MAC模型的实现。这种模型通常用于需要高度安全的环境，如军事或政府部门。

不过，MAC由于其中心化的强制控制方式，让其灵活性较差，并且实施起来相对复杂，在现代Web应用领域的使用场景有限。我理解这种MAC模型映射到Web应用领域的具体呈现就是“写死”到代码中的访问控制逻辑和授权决策逻辑，这些“系统层”逻辑是所有到达Web应用的请求必经的且无法进行配置和改变的。

一个典型的应用就是对资源根据安全等级进行的强制访问控制：**用户只能访问其安全等级低于或等于自身安全等级的资源**。下面是一个演示性质的代码例子：

```
// authz-examples/mac/main.go
// 定义安全等级
type SecurityLevel int
const (
// 最低安全等级
LevelLow SecurityLevel = iota
// 中等安全等级
LevelMedium
// 最高安全等级
LevelHigh
)
// 定义资源
type Resource struct {
// 资源名称
Name string
// 安全等级
Level SecurityLevel
}
// 定义用户
type User struct {
// 用户名
Name string
// 安全等级
Level SecurityLevel
}
// 定义访问控制策略
func CheckAccess(user User, resource Resource) bool {
// 检查用户的安全等级是否高于或等于资源的安全等级
return user.Level >= resource.Level
}
func main() {
// 创建资源
resource := Resource{
Name: "敏感数据",
Level: LevelHigh,
}
// 创建用户
user := User{
Name: "管理员",
Level: LevelHigh,
}
// 检查访问权限
if CheckAccess(user, resource) {
fmt.Printf("用户[%s]有权访问资源\n", user.Name)
} else {
fmt.Printf("用户[%s]没有权限访问资源\n", user.Name)
}
// 创建用户
user = User{
Name: "访客",
Level: LevelLow,
}
// 检查访问权限
if CheckAccess(user, resource) {
fmt.Printf("用户[%s]有权访问资源\n", user.Name)
} else {
fmt.Printf("用户[%s]没有权限访问资源\n", user.Name)
}
}
```


在这个例子中，我们定义了三个安全等级：LevelLow、LevelMedium和LevelHigh。资源和用户都被分配了安全等级。CheckAccess函数用于执行强制的访问控制策略：即用户只能访问其安全等级低于或等于自身安全等级的资源。

### 2.3 自主访问控制（Discretionary Access Control，DAC）

[DAC模型](https://en.wikipedia.org/wiki/Discretionary_access_control)基于资源所有者对其资源的访问权限进行授予和控制。在DAC模型中，资源的所有者可以自主决定哪些用户或实体可以访问他们的资源，以及对资源的访问权限级别。资源的所有者可以决定将资源设置为公开访问、私有访问或仅限于特定用户或用户组的访问。通过授权用户或实体访问资源，资源的所有者具有灵活性和自主权来管理他们的资源。

很显然，这样的DAC模型具有**较为灵活的优点**，允许资源所有者根据自己的需求和偏好授予和撤销访问权限。这使得资源的访问控制可以针对个体用户进行定制，满足不同用户的需求。同时，DAC模型具备**分散控制**的特征，它将访问控制的决策权下放给资源的所有者，而不是集中在中央管理机构。这样可以减轻管理负担，并且资源的所有者可以更直接地管理和控制自己的资源。

使用自主访问控制（DAC）模型进行访问控制的Web应用的典型例子是文件共享服务，即我们经常说的网盘服务，比如Google Drive、Dropbox或百度网盘等。在这样的应用中，用户可以上传、存储和共享文件。并使用DAC模型，设置文件或文件夹的访问权限，例如私有、只读或读写访问。用户还可以选择将文件或文件夹的访问权限限制为特定的用户或用户组。

另一种使用DAC模型进行访问控制的Web应用示例是社交媒体应用，这类应用允许用户发布和查看帖子，并给每个帖子分配权限以控制其他用户对其的访问权限，权限可以是“公开”、“好友”、“私人”等，

下面是一个DAC模型的演示性质的代码例子：

```
// authz-examples/dac/main.go
type Resource struct {
Name string
Owner string
AccessMap map[string]bool
}
func (r *Resource) GrantAccess(user string) {
r.AccessMap[user] = true
}
func (r *Resource) RevokeAccess(user string) {
r.AccessMap[user] = false
}
func (r *Resource) CanAccess(user string) bool {
access, exists := r.AccessMap[user]
if !exists {
return false
}
return access
}
func main() {
// 创建一个资源
resource := Resource{
Name: "example.txt",
Owner: "alice",
AccessMap: make(map[string]bool),
}
// 授予访问权限给用户
resource.GrantAccess("alice")
resource.GrantAccess("bob")
// 验证访问权限
fmt.Println("alice can access:", resource.CanAccess("alice")) // 输出: true
fmt.Println("bob can access:", resource.CanAccess("bob")) // 输出: true
fmt.Println("eve can access:", resource.CanAccess("eve")) // 输出: false
// 撤销访问权限
resource.RevokeAccess("bob")
// 验证访问权限
fmt.Println("bob can access:", resource.CanAccess("bob")) // 输出: false
}
```


在这个示例中，我们定义了一个Resource结构，包含资源的名称、所有者和访问权限的map。用户可以调用GrantAccess方法授予其他用户对资源的访问权限，RevokeAccess方法则用于撤销用户的访问权限，CanAccess方法用于验证用户是否具有访问资源的权限。通过这个示例，我们也可以看到，MAC模型可以基于一个ACL(比如AccessMap)来实现。

DAC模型那些固有的特点带来的也并不都是好处，也可能给应用带来一定的安全性挑战。比如：由于访问权限由资源的所有者授予，因此可能存在资源所有者授予不当权限的情况。如果资源所有者错误地授予了高权限给不信任的用户或实体，可能会导致安全漏洞。

此外，由于每个资源的所有者可以独立决定访问权限，因此可能会导致系统中存在许多不一致的访问控制策略。这可能增加了管理和维护的复杂性，并且可能导致访问控制规则的碰撞或冲突。

### 2.4 基于角色的访问控制(Role-Based Access Control，RBAC）

按访问控制模型的出现时间看，ACL是一个60后，MAC是一个70后，DAC是一个80后。那90后的代表是哪个模型呢？没错，就是[RBAC](https://en.wikipedia.org/wiki/Role-based_access_control)。

RBAC是访问控制模型中的一种相对较新的模型，它基于角色和权限的概念来管理对资源的访问。在RBAC模型中，访问权限是根据用户的角色进行授权和控制的。

RBAC模型的核心概念包括：

- 角色（Role）

角色代表一组具有相似职责或权限需求的用户，每个角色可以被分配不同的权限，或者说权限是以角色为最小单位分配的。

- 权限（Permission）

权限代表对资源执行特定操作的授权。权限定义了以特定角色进入系统的用户在系统中可以对某些类资源执行的操作，例如读取、写入、删除等。

- 用户（User）

用户是系统中的实体，通过分配角色来获得相应的权限。

下图是一个RBAC模型中用户、角色、权限与资源之间的直观的关系示意图(使用[mermaid](https://mermaid.live/)绘制)：

![](../../assets/eed8659747cf84eb.png)


这个图比较好理解！首先看权限，权限是一个规则，即允许哪个/哪些角色操作哪个/那些资源。以权限P1为例，它允许角色X操作资源R1和资源R2；权限P2则是允许角色Y和角色Z操作资源R2；权限P3则是允许角色Z操作资源R3。用户则会被赋予角色，并继承角色具有的所有权限。

通过上面图示和说明，我们看到：RBAC模型通过将权限分配给角色，而不是直接分配给用户，简化了权限管理，因为只需管理角色的权限，而无需单独管理每个用户的权限。

同时，这种方法也保持了一定的灵活性：通过分配和撤销角色，可以轻松地管理用户的访问权限。当用户的职责或权限需求发生变化时，只需调整其角色分配即可。

在安全性方面，RBAC模型可以减少人为错误和误操作的风险。通过严格控制角色的权限，可以确保用户只能执行他们所需的操作，从而减少潜在的安全漏洞。

基于上述特点，RBAC模型被广泛应用于企业环境中，并满足企业或组织内部的权限管理需求，是当今企业级Web应用的**主流访问控制模型**。

此外，像Github的[Personal Access Token(PAT)](https://github.com/settings/tokens)以及其他互联网Web应用的类似PAT的权限配置也是基于RBAC模型的。使用PAT时，用户可以创建令牌并为其分配特定的范围和权限，这时令牌既是user，也充当了角色(Role)。这些权限可以控制PAT可以访问和执行的操作，例如读取仓库、创建存储库、管理问题等。用户可以根据自己的需求创建多个PAT(Role)，并根据需要撤销或更新它们。下面是github PAT创建和配置的示意图：

![](../../assets/39bdec8b82c30332.png)


不过，RBAC模型虽然是主流模型，但也存在一些问题，比如：

- 静态角色分配

RBAC模型中，角色和权限的分配是静态的，需要预先定义和分配角色。这种固定的角色分配方式难以适应动态变化的访问控制需求。例如，当用户的职责发生变化或需要临时获得额外权限时，RBAC模型需要进行角色重新分配或角色继承的操作，导致管理复杂性增加。

- 角色爆炸问题

在大型组织或系统中，RBAC模型可能涉及大量的角色，以覆盖各种职责和权限。这可能导致角色爆炸问题，即角色数量过多，不易管理和维护。角色之间的关系和权限的粒度也可能变得复杂，增加了配置和管理的复杂性。

- 缺乏细粒度访问控制

RBAC模型的主要限制之一是对访问控制的粒度较粗。RBAC模型通常基于角色来控制访问权限，而忽略了更细粒度的访问控制需求，如基于资源属性、环境上下文等进行访问控制。

- 缺乏动态性和灵活性

RBAC模型的角色和权限分配是静态的，难以适应动态变化的访问控制需求。RBAC模型无法根据实时上下文信息或动态的用户属性来进行访问控制决策，导致难以满足复杂的访问控制策略。

这些问题也促成了**00后的新模型ABAC**的出现，下面我们就来看看ABAC模型。

### 2.5 基于属性的访问控制（Attribute-Based Access Control，ABAC)

[ABAC](https://en.wikipedia.org/wiki/Attribute-based_access_control)，有时也被称为policy-based access control (PBAC)或claims-based access control (CBAC)，是一种基于属性（Attribute）来决定对资源的访问权限的访问控制模型。与“90后”的RBAC模型相比，ABAC模型提供了更细粒度、动态和灵活的访问控制能力。

ABAC模型的核心概念包括如下几个：

- 属性（Attribute）

属性是关于用户、资源、环境或其他上下文信息的特征。属性可以是任意对象，一般有这么几类。访问主体(用户)属性，可以是访问者自带的属性，比如年龄，性别，部门，角色等；动作类属性：比如读取，删除，查看等；被访问对象的属性，比如一条记录的修改时间，创建者等；环境类属性：比如时间信息，地理位置信息，访问平台信息等。属性还可以根据需要进行自定义和扩展。

- 策略（Policy）

策略定义了访问控制规则和条件，用于评估访问请求的属性和上下文信息，并决定是否允许或拒绝访问。策略可以包括属性匹配、逻辑操作、时间条件等。

- 属性策略引擎（Policy Decision Point, PDP）

属性策略引擎是ABAC模型的核心组件，负责评估访问请求的属性和条件，并根据属性和预定义的策略进行逻辑计算，以做出是否允许访问的控制决策。

下面是一个使用ABAC模型在组织内控制对某个文件资源的访问的例子的示意图：

![](../../assets/8037bf41e94b6de7.png)


在这个示例中，用户属性包括用户角色（Role）、用户部门（Department）、用户年龄(Age)；资源属性有文件类型（FileType）、文件所属部门（FileDepartment）。

属性策略引擎(PDP)通过PIP(策略信息点)获取相关属性，并基于策略做出决策。下面是一些策略示例：

```
策略1：仅允许具有"管理员"角色的用户访问任意类型的文件。
策略2：仅允许具有"员工"角色的用户访问属于自己部门的任意类型的文件。
策略3：允许具有"访客"角色的用户访问公共类型的文件。
策略4：允许60岁以上用户访问特定类型的文件。
策略5：不允许访问属于其他部门的文件。
```


图中的PEP(策略执行点)负责接收用户发起的访问请求，并将请求传递给PDP进行决策，确保访问控制策略得到严格执行，以保护资源的安全性和完整性。用户可以是人员、应用程序或其他实体。之后，PEP负责根据访问控制策略的决策结果来执行实际的访问控制。当PDP（Policy Decision Point，属性策略引擎）确定用户是否被授权访问资源后，PEP将根据决策结果来允许或拒绝对资源的访问。PEP还可以记录和监控访问请求和决策结果，用于后续的审计和安全分析。通过记录访问活动，PEP可以提供有关谁、何时以及如何访问资源的详细信息。

ABAC是较新的访问控制模型，相较于它的前辈RBAC来说，它的能力更强大，控制粒度更精细，授权决策动态且灵活，但也更加复杂，需要定义和管理大量的属性和策略。这可能增加了实施和维护的困难。另外，ABAC模型的属性策略引擎需要对访问请求进行属性匹配和逻辑计算，这可能对系统性能产生一定的影响，在引入ABAC模型时，这也是一个需要考虑的因素。

尽管ABAC模型存在一些挑战和复杂性，但它提供了更高级、动态和灵活的访问控制能力让它可以更好地满足复杂的访问控制需求和安全策略，这使得ABAC模型在许多组织和行业中得到广泛应用，包括企业、政府、云计算、物联网等。同时，有许多标准化组织和机构致力于制定ABAC的标准和规范，例如[NIST（美国国家标准与技术研究院）的NGAC](https://www.nist.gov/identity-access-management/policy-machine-and-next-generation-access-control)和[OASIS的XACML（eXtensible Access Control Markup Language）](https://www.oasis-open.org/committees/tc_home.php)，这些标准化努力有助于推动ABAC的统一实施和互操作性。

随着技术的不断进步，ABAC模型也在不断演进和改进。例如，引入了机器学习和人工智能技术来提高决策过程的自动化和智能化。

到这里，我们已经学习了从ACL到ABAC的5种主要访问控制模型，包括它们的发展历史、应用场景、优缺点等，这给我们提供了对不同访问控制模型的全面了解和比较。如今RBAC和ABAC是大家广泛应用的主流模型，接下来，我们就以一个示例来进一步加深这两个模型的理解。我将构建一个简单的公司员工信息管理系统，并在此系统中分别实现基于RBAC和ABAC的访问控制机制，以便通过对比不同实现来直观感受两种模型的区别。

## 3. 一个Web应用的授权实例

下面我们用一个Web应用的授权实例来进一步理解RBAC和ABAC两个广泛使用的访问控制模型。这是一个公司员工信息管理系统授权访问控制的示例，我们先用[casbin](https://github.com/casbin/casbin)以RBAC模型实现该示例，之后使用[Open Policy Agent](https://github.com/open-policy-agent/opa)以ABAC模型再实现一遍该示例。

### 3.1 示例简介

好的，现在给你描述一下这个示例对授权的具体要求。

这是一个公司的员工信息管理系统，系统中定义了几种角色(role)：经理(manager)、员工(employee)、HR和财务(finance)。这些角色可以直接用于RBAC模型中的角色，在ABAC中，它也可以作为主体(subject)的角色属性使用。系统要保护的资源有两个表：员工信息表(employee_info)和员工工资表(employee_salary)，并定义了如下访问控制要求：

- 经理：可以查看和修改所有员工的信息
- 员工：可以查看和修改自己的信息
- HR：可以查看和修改所有员工的信息，可以查看和修改所有员工的工资信息
- 财务：可以查看所有员工的工资信息

这个公司有如下几位不同角色的员工：

- 经理：alice
- 员工：bob
- HR：cathy
- 财务：dan

接下来我们就先来基于RBAC实现该系统的访问控制。

### 3.2 基于RBAC模型的访问控制

根据前面的介绍，RBAC模型是基于角色的访问控制，因此针对上面示例描述，我们需要先定义角色以及为角色分配权限。

casbin使用policy.csv定义角色的权限：

```
// authz-examples/rbac/casbin/policy.csv
p, manager, employee_info, read
p, manager, employee_info, write
p, employee, employee_info, write
p, employee, employee_info, read
p, hr, employee_info, read
p, hr, employee_info, write
p, hr, employee_salary, write
p, hr, employee_salary, read
p, finance, employee_salary, read
```


初看这个文件中的配置数据，很多人不知道是什么意思，这个csv文件中每行的字段含义都要与model.conf对照着看：

```
// authz-examples/rbac/casbin/model.conf
[request_definition]
r = role, obj, act
[policy_definition]
p = role, obj, act
[role_definition]
g = _, _
[policy_effect]
e = some(where (p.eft == allow))
[matchers]
m = g(r.role, p.role) && r.obj == p.obj && r.act == p.act
```


我们看下这个配置文件中的section: policy_definition，我们看到其定义为p = role, obj, act，这里的p就是规则定义，根据这一规则定义，我们可以确定csv中p开头的行中的各段数据的含义，比如：根据“p, manager, employee_info, read”，我们可以得到role=manager，obj=employee_info，act=read，我们用下图再直观总结一下这种对应关系：

![](../../assets/560e8f9d49b076d8.png)


request_definition这个section中定义了请求传入时参数的次序(“r = role, obj, act”)，其要求Go代码中调用casbin.Enforcer.Enforce方法时各个参数的传入次序与之相同(比如: Enforce(“manager”, “employee_info”, “read”))，并指示了传入的参数对应的含义。

matchers这个section中定义了匹配规则，先不看g(r.role, p.role)，“r.obj == p.obj && r.act == p.act”这个很好理解，即当请求(request)中的obj与策略规则(policy)中的obj匹配，且请求中的act与策略规则中的act(动作)匹配时，才认为通过访问控制的校验。

我们结合Go代码来看一下casbin对RABC的实现和使用方法：

```
// authz-examples/rbac/casbin/main.go
package main
import (
"fmt"
"github.com/casbin/casbin/v2"
)
func main() {
users := map[string]string{
"alice": "manager",
"bob": "employee",
"cathy": "hr",
"dan": "finance",
}
e, err := casbin.NewEnforcer("model.conf", "policy.csv")
if err != nil {
panic(err)
}
// 经理alice访问员工信息
ok, err := e.Enforce(users["alice"], "employee_info", "read") // role, obj, act
if err != nil {
panic(err)
}
fmt.Println("manager alice can read employee_info:", ok)
ok, err = e.Enforce(users["alice"], "employee_info", "write")
if err != nil {
panic(err)
}
fmt.Println("manager alice can write employee_info:", ok)
// 员工bob访问自己信息
ok, err = e.Enforce(users["bob"], "employee_info", "write")
fmt.Println("employee bob can write employee_info:", ok)
// HR cathy 访问员工信息
ok, err = e.Enforce(users["cathy"], "employee_info", "write")
fmt.Println("hr cathy can write employee_info:", ok)
ok, err = e.Enforce(users["cathy"], "employee_salary", "write")
fmt.Println("hr cathy can write employee_salary:", ok)
// 财务dan访问工资信息
ok, err = e.Enforce(users["dan"], "employee_salary", "read")
fmt.Println("finance dan can read employee_salary:", ok)
// 员工bob串改薪水信息
ok, err = e.Enforce(users["bob"], "employee_salary", "write")
fmt.Println("employee bob can write employee_salary:", ok)
}
```


这里只是企业内部信息系统的简化实现，正常情况下，员工使用自己的账号登录到系统后，系统就会获知该用户的角色(role)，这里我们用了一个map来存储用户名与角色的映射关系。

我们基于model.conf和policy.csv创建新的Enforcer，然后调用其Enforce方法并按“role, obj, act”次序传入我们要测试的信息。Enforce返回true表示通过了访问控制规则的验证，否则就是没有通过授权验证。

上述代码的输出结果如下：

```
$go run main.go
manager alice can read employee_info: true
manager alice can write employee_info: true
employee bob can write employee_info: true
hr cathy can write employee_info: true
hr cathy can write employee_salary: true
finance dan can read employee_salary: true
employee bob can write employee_salary: false
```


到这里，我们还有一个问题没有解决，那就是casbin的model.conf中role_definition的配置含义以及matchers中g(r.role, p.role)含义。

[casbin关于RBAC的文档](https://casbin.org/docs/rbac)中明确提到了，如果不使用RBAC模型，那么role_definition就是一个可选的配置；如果要使用RBAC模型，那么role_definition下的每一行都是一个独立的RBAC系统，下面的配置拥有两个独立的RBAC系统：g和g2：

```
[role_definition]
g = _, _
g2 = _, _
```


“_, _”表示映射关系中有两方。通常我们只会使用到user和role的映射，因此只用一个RBAC系统即可，即只配置和使用g即可。下面是应用g这个RBAC系统的例子：

```
// policy.csv
p, manager, employee_info, write
g, alice, manager
```


这里的“g, alice, manager”的含义是alice是角色manager中的一员，或alice这个user的角色是manager。当然alice这个位置上不仅可以使用user，也可以使用resource，甚至是role，casbin只是将其看成一个字符串而已。

而matchers中的“g(r.role, p.role)”的含义就是请求(r)中的role在policy文件中能找到对应的role。如果Enforce函数传入的是”manager”，那么只有policy.csv中定义了”manager”这个角色，g(r.role, p.role)的结果才是true。

上述示例并未在policy.csv中使用到这种user到role的映射(基于g这个RBAC系统)，下面我们改造一下示例，我们在policy.csv中保存这种user到role的映射，而不是在go代码中保存，新版policy.csv如下：

```
// authz-examples/rbac/casbin_with_user_in_policy/policy.csv
p, manager, employee_info, read
p, manager, employee_info, write
p, employee, employee_info, write
p, employee, employee_info, read
p, hr, employee_info, read
p, hr, employee_info, write
p, hr, employee_salary, write
p, hr, employee_salary, read
p, finance, employee_salary, read
g, alice, manager
g, bob, employee
g, cathy, hr
g, dan, finance
```


对应的Go代码改造如下：

```
// authz-examples/rbac/casbin_with_user_in_policy/main.go
func main() {
e, err := casbin.NewEnforcer("model.conf", "policy.csv")
if err != nil {
panic(err)
}
// 经理alice访问员工信息
ok, err := e.Enforce("alice", "employee_info", "read") // role, obj, act
if err != nil {
panic(err)
}
fmt.Println("manager alice can read employee_info:", ok)
ok, err = e.Enforce("alice", "employee_info", "write")
if err != nil {
panic(err)
}
fmt.Println("manager alice can write employee_info:", ok)
// 员工bob访问自己信息
ok, err = e.Enforce("bob", "employee_info", "write")
fmt.Println("employee bob can write employee_info:", ok)
// HR cathy 访问员工信息
ok, err = e.Enforce("cathy", "employee_info", "write")
fmt.Println("hr cathy can write employee_info:", ok)
ok, err = e.Enforce("cathy", "employee_salary", "write")
fmt.Println("hr cathy can write employee_salary:", ok)
// 财务dan访问工资信息
ok, err = e.Enforce("dan", "employee_salary", "read")
fmt.Println("finance dan can read employee_salary:", ok)
// 员工bob串改薪水信息
ok, err = e.Enforce("bob", "employee_salary", "write")
fmt.Println("employee bob can write employee_salary:", ok)
}
```


大家看到我们在调用Enforce时，第一个参数传入的不再是role，而是user名字，由于policy.csv中使用g保存了user到role的映射，因此Enforce会在内部将user先替换为映射的role，然后再在policy.csv中找到对应的p定义的role，查看是否满足matchers中“g(r.role, p.role)”规则。

运行上面新示例的结果将于第一个示例一样，这里就不赘述了。

接下来，我们再来看看如何基于ABAC模型实现该公司的员工信息系统的授权。

注：casbin号称也支持ABAC模型，有兴趣的童鞋可以自行基于casbin实现基于ABAC模型的员工信息系统的授权示例。


### 3.3 基于ABAC模型的访问控制

前面介绍ABAC模型时已经提到过，ABAC是基于属性的访问控制，由于我们这个示例比较简单，能用到的user主体属性只有user的角色(role)，这里就基于user的角色来实现访问控制，而作为客体的那两张表，考虑简单起见，这里并未为之定义什么属性。

[OPA（Open Policy Agent）](https://github.com/open-policy-agent/opa)是CNCF基金会下面的一个开源的通用策略引擎，它目前已经从CNCF毕业，也是CNCF目前毕业项目中唯一一个策略引擎。OPA可以用于实现统一的访问控制和策略管理。它提供了一个通用的框架，可用于编写和执行策略，以决定对资源的访问是否被允许。OPA使用一种名为Rego的声明性语言来定义策略。Rego语言简洁而强大，可以表达复杂的访问控制逻辑。它允许开发人员定义规则、条件和约束，以描述访问策略和决策过程。受益于CNCF的支持和资源，OPA获得了更广泛的知名度和认可度。它成为了云原生生态系统中重要的一部分，并与其他CNCF项目和工具进行紧密的集成，如Kubernetes、Envoy、Prometheus等。这种集成加强了整个生态系统的互操作性和一致性，为用户提供了更强大的功能和灵活性。

使用opa实现员工信息系统的ABAC授权，我们需要先使用Rego语言定义出访问控制策略，下面是用Rego定义的员工信息系统的访问控制策略：

```
// authz-examples/abac/opa/policy.rego
package opa.examples
import input as i
# 定义策略
allow {
i.subject.role == "manager"
i.object == "employee_info"
i.action == "read"
}
allow {
i.subject.role == "manager"
i.object == "employee_info"
i.action == "write"
}
allow {
i.subject.role == "employee"
i.object == "employee_info"
i.action == "read"
}
allow {
i.subject.role == "employee"
i.object == "employee_info"
i.action == "write"
}
allow {
i.subject.role == "hr"
i.object == "employee_info"
i.action == "read"
}
allow {
i.subject.role == "hr"
i.object == "employee_info"
i.action == "write"
}
allow {
i.subject.role == "finance"
i.object == "employee_salary"
i.action == "read"
}
```


这个策略配置文件使用的语法借鉴了Go，不过即便你不了解Go语法，你很大概率也能读懂其逻辑，是不是感觉比前面的casbin的model.conf和policy.csv的组合配置更易理解一些呢！我们以一个allow代码块为例：

```
allow {
i.subject.role == "finance"
i.object == "employee_salary"
i.action == "read"
}
```


这个配置块儿的含义就是当输出的请求中的主体的role为”finance”且客体(resouce)为”employee_salary”并且action为”read”时，允许请求访问。其他的section依此理解即可。

下面我们再来看看基于opa实现上述ABAC模型的Go代码：

```
// authz-examples/abac/opa/main.go
package main
import (
"context"
"fmt"
"log"
"github.com/open-policy-agent/opa/rego"
)
func main() {
// Construct a Rego object that can be prepared or evaluated.
r := rego.New(
rego.Query("data.opa.examples.allow"),
rego.Load([]string{"./policy.rego"}, nil),
)
// Create a prepared query that can be evaluated.
query, err := r.PrepareForEval(context.Background())
if err != nil {
log.Fatal(err)
}
inputs := []map[string]interface{}{
{
"name": "alice",
"subject": map[string]string{
"role": "manager",
},
"object": "employee_info",
"action": "read",
},
{
"name": "alice",
"subject": map[string]string{
"role": "manager",
},
"object": "employee_info",
"action": "write",
},
{
"name": "bob",
"subject": map[string]string{
"role": "employee",
},
"object": "employee_info",
"action": "write",
},
{
"name": "cathy",
"subject": map[string]string{
"role": "hr",
},
"object": "employee_info",
"action": "read",
},
{
"name": "cathy",
"subject": map[string]string{
"role": "hr",
},
"object": "employee_info",
"action": "write",
},
{
"name": "dan",
"subject": map[string]string{
"role": "finance",
},
"object": "employee_salary",
"action": "read",
},
{
"name": "bob",
"subject": map[string]string{
"role": "employee",
},
"object": "employee_salary",
"action": "write",
},
}
for _, v := range inputs {
// Execute the prepared query.
rs, err := query.Eval(context.Background(), rego.EvalInput(v))
if err != nil {
log.Fatal(err)
}
if len(rs) > 0 {
fmt.Printf("%s %s can %s %s: %v\n", (v["subject"].(map[string]string))["role"], v["name"],
v["action"], v["object"], rs[0].Expressions[0].Value)
} else {
fmt.Printf("%s %s can %s %s: %v\n", (v["subject"].(map[string]string))["role"], v["name"],
v["action"], v["object"], false)
}
}
}
```


这个例子参考了opa官方的示例，我们先基于policy.rego构建一个rego策略引擎，然后按我们的测试逻辑构建一组input，我将input放入了一个map切片中，然后遍历该切片，对每个input执行Eval，通过Eval返回的结果判断input是否通过了引擎的校验。执行上述示例代码，我们将得到：

```
$go run main.go
manager alice can read employee_info: true
manager alice can write employee_info: true
employee bob can write employee_info: true
hr cathy can read employee_info: true
hr cathy can write employee_info: true
finance dan can read employee_salary: true
employee bob can write employee_salary: false
```


这个和casbin实现的结果是一致的。

通过上面两种模型的实现，我们能达到相同的效果。不过，opa的rego语言的简洁清晰且不乏强大的表达能力还是让人印象深刻的，casbin的配置在理解上要下一番功夫，并且要用好casbin，还必须要深入理解其配置方法和配置项的含义。这两个工具大家可以根据自己的喜好选择最适合你自己的。

以上无论是RBAC，还是ABAC，都是仅由本地单系统参与的授权模型。随着系统规模的扩大，我们可能需要考虑引入第三方授权系统。第三方授权具有方便实现单点登录、用户友好的授权流程、减少密码传播风险、细粒度的授权管理以及第三方应用程序集成等好处。这些好处可以提供更方便、安全和灵活的用户体验，并促进了应用程序之间的互操作性和集成性。

接下来我们就来说说基于OAuth2的第三方授权。

## 4. OAuth2授权框架

### 4.1 什么是第三方授权

在开始理解OAuth2授权框架之前，我们先来简单说说**什么是第三方授权**。为了更好的说明，我先画了一张示意图：

![](../../assets/72dc12d16e6d18ff.png)


结合这张图，我们理解以下第三方授权。第三方授权是指一个实体（第三方，比如图中的C应用），通过获得用户的授权，可以访问另一个实体（服务提供者，比如图中的S应用）的资源(比如用户A的一些个人信息)或执行特定操作。在这种授权模式下，用户授予第三方应用程序(C应用)或服务访问其受保护资源(位于S应用中的用户A的一些个人信息)的权限，而无需直接向第三方实体(比如C应用)共享其凭据（如用户名和密码）。

第三方授权的典型示例是用户使用自己的社交媒体账号（如微信、Facebook、Google、Twitter等）登录第三方应用程序或网站：

![](../../assets/c6082bb50bd11891.png)


在这种情况下，用户不需要创建新的账号和密码，而是选择使用其社交媒体账号进行登录。当用户同意授权该应用程序访问其社交媒体账号时，第三方应用程序可以获取用户的基本信息（如姓名、电子邮件地址、头像等）或者在用户的名义下执行某些操作（如发布推文、分享内容等）。下面是使用github和微信对第三方应用进行授权的页面截图：

![](../../assets/55ff0761297e924a.png)


第三方授权的优势在于用户可以方便地使用现有的身份验证凭据，而无需为每个应用程序创建和记住不同的账号和密码。同时，用户还可以更好地控制其数据的访问权限，选择性地授权应用程序可以访问的资源和操作。需要注意的是，第三方授权的安全性和隐私保护至关重要。用户应该**仔细审查并理解第三方应用程序请求的权限范围**，并只授权其信任的应用程序访问其敏感信息或执行敏感操作。服务提供者也应该采取适当的安全措施，确保用户的数据得到妥善保护。

这样的第三方授权在移动互联网应用领域十分常见，如果没有一套标准的授权框架，这种授权方式将很难实现。[OAuth](https://en.wikipedia.org/wiki/OAuth)正是为了解决这个问题而诞生的一个标准的授权框架。接下来，我们就进入OAuth协议框架。

### 4.2 OAuth协议框架

OAuth协议(全称Open Authorization)的产生是为了解决无须共享密码的情况下，从第三方应用程序(比如前面图中的S应用)安全地访问受保护数据、资源的问题。OAuth是一种行业标准的授权框架，它在第三方应用授权中发挥重要作用。OAuth协议的最新版本为OAuth2.0，并已经被广泛用于各厂家的互联网应用中。在原理上，OAuth2允许用户授权第三方应用，访问该用户在某服务平台存储的资源，而无需共享用户名和密码。它通过“访问令牌(access token)”实现授权。

注：从上述描述我们也能看出：所谓第三方授权其实是将身份认证与授权合为一体的一种机制，以授权为主要目的。因此OAuth被称为授权协议，而不是身份认证协议。


在OAuth协议的核心规范中，对于OAuth的授权流程定义了不同的角色，通过不同角色之间不同概念的信息传递对象的交互，完成整个授权流程。这些角色包括：

- 资源所有者（Resource Owner）

资源所有者是指受保护资源的所有者，当受保护资源被访问时，需要此所有者授予访问者访问权限。如果资源所有者是一个自然人时，即表示为最终用户(比如前面图中的用户A)。

- 资源服务器（Resource Server）

资源服务器是指托管接受保护资源的服务器(比如前面图中的S应用)，接收访问请求并使用访问令牌保护受保护的资源。

- 客户端（Client）

这里客户端通常是指代理用户发起受保护资源请求的客户端应用程序，比如前面图中的C应用。

- 授权服务器（Authorization Server）

客户端通过认证后，授权服务器(比如前面图中的S应用)会向客户端发布访问令牌并获得授权。

访问令牌是客户端应用程序访问受保护资源的凭据，没有访问令牌则无法访问受保护的资源。此令牌通常是授权服务器颁发的具有一定含义的字符串，包含此次授权的基本信息、授权范围、授权有效时间等信息。

授权过程与我们前面的示意图十分相似，结合OAuth协议定义的不同角色，我们借鉴下面示意图再来描述一下基于OAuth2的整个授权流程：

![](../../assets/347e378a40584b9c.png)



- 步骤1：客户端应用程序向资源所有者发送授权请求，这里的客户端是指普通的WebAPI、原生移动App、基于浏览器的Web应用以及无浏览器的嵌入式后端应用，在流程中充当用户行为代理(比如前图中的C应用)。
- 步骤2：资源所有者(比如前图中的用户A)同意授权客户端访问资源，即获得资源所有者的授权凭据，包含授权范围和授权类型。
- 步骤3：客户端使用上一步获得的授权凭据，向授权服务器进行身份认证并申请访问令牌Access Token。
- 步骤4：授权服务器对客户端进行身份认证，确认身份无误后，下发访问令牌AccessToken。
- 步骤5：客户端使用上一步获得的访问令牌Access Token，向资源服务器申请获取受保护的资源。
- 步骤6：资源服务器确认访问令牌Access Token正确无误后，向客户端开放所访问的资源。

OAuth协议核心文档定义了资源所有者给予客户端授权的4种方式：

- 授权码（authorization code）

这种方式下，第三方应用先申请一个授权码，然后再用该码获取令牌。

- 隐藏式（implicit）

适用于没有后端的纯前端应用，客户端直接获得访问令牌Access Token，而无须客户端授权码这个中间步骤。

- 密码式（password）

资源所有者的认证凭据（即用户名和密码）直接告诉第三方应用，该应用随即使用密码申请令牌。

- 凭证式（client credentials）

适用于没有前端的命令行应用，即在命令行下请求令牌。采用客户端自己的凭据，而不是用户的凭据来作为授权依据，获取资源的访问权限。

在这四种授权方式中，**授权码**是OAuth协议中主要的授权流程，相比其他的授权模式，其流程最为完备，适用于互联网应用的第三方授权场景。

由于OAuth授权相对较为复杂，涉及角色和环节很多，很难用一个例子将其全貌展现出来，这里就不举代码示例了。如果你的系统并不涉及到第三方，既不为第三方提供服务，也不使用第三方的服务，那引入OAuth 2.0其实就没必要。

## 5. 小结

本文首先介绍了授权的相关概念，着重说明了授权与访问控制的紧密联系和些许差别。之后，我们对5种常见的访问控制模型逐一做了说明，包括它们的使用场景与优缺点。为了帮助大家更好地理解当今主流使用的RBAC和ABAC模型，我还将一个示例分别用casbin和opa作了实现。

在文章的最后，我们简单介绍了用于第三方授权的OAuth授权框架，包括它的协议中涉及的主要角色以及资源所有者给予客户端授权的4种方式，大家可以根据自己的理解，自行基于像微信或github这样的支持三方授权的应用编写一些简单示例。

本文示例所涉及的Go源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/authz-examples)下载。

## 6. 参考资料

[《API安全实战》](https://book.douban.com/subject/36039150/)– https://book.douban.com/subject/36039150/[《API安全技术与实战》](https://book.douban.com/subject/35429043/)– https://book.douban.com/subject/35429043/[授权（上）：系统如何确保授权的过程可靠？](https://time.geekbang.org/column/article/331411)– https://time.geekbang.org/column/article/331411[授权（下）：系统如何确保授权的结果可控？](https://time.geekbang.org/column/article/332255)– https://time.geekbang.org/column/article/332255[Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)– https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html[Acess Control(owasp)](https://owasp.org/www-community/Access_Control)– https://owasp.org/www-community/Access_Control[Web App Access Control Design](https://owasp.org/www-pdf-archive/ASDC12-Access_Control_Designs_and_Pitfalls.pdf)– https://owasp.org/www-pdf-archive/ASDC12-Access_Control_Designs_and_Pitfalls.pdf[OPA: The Cloud Native Policy Engine](https://www.slideshare.net/TorinSandall/opa-the-cloud-native-policy-engine)– https://www.slideshare.net/TorinSandall/opa-the-cloud-native-policy-engine[ACL模型](https://en.wikipedia.org/wiki/Access-control_list)– https://en.wikipedia.org/wiki/Access-control_list[MAC模型](https://en.wikipedia.org/wiki/Mandatory_access_control)– https://en.wikipedia.org/wiki/Mandatory_access_control[DAC模型](https://en.wikipedia.org/wiki/Discretionary_access_control)– https://en.wikipedia.org/wiki/Discretionary_access_control[RBAC模型](https://en.wikipedia.org/wiki/Role-based_access_control)– https://en.wikipedia.org/wiki/Role-based_access_control[ABAC模型](https://en.wikipedia.org/wiki/Attribute-based_access_control)– https://en.wikipedia.org/wiki/Attribute-based_access_control[Open Policy Agent Introdution](https://www.openpolicyagent.org/docs/latest/#5-try-opa-as-a-go-library)– https://www.openpolicyagent.org/docs/latest/#5-try-opa-as-a-go-library[Casbin: Syntax for Models](https://casbin.org/docs/syntax-for-models)– https://casbin.org/docs/syntax-for-models[OAuth 2.0 的四种方式](https://www.ruanyifeng.com/blog/2019/04/oauth-grant-types.html)– https://www.ruanyifeng.com/blog/2019/04/oauth-grant-types.html[OAuth](https://en.wikipedia.org/wiki/OAuth)– https://en.wikipedia.org/wiki/OAuth

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

感谢分享，总结的非常详尽，做 Web 系统的权限管理，有这一篇文章就够了！