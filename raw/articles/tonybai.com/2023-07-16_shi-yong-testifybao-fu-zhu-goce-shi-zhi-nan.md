---
title: 使用testify包辅助Go测试指南
url: https://tonybai.com/2023/07/16/the-guide-of-go-testing-with-testify-package/
published: '2023-07-16'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 使用testify包辅助Go测试指南

![](../../assets/72c459d56b27ffb3.png)


[本文永久链接](https://tonybai.com/2023/07/16/the-guide-of-go-testing-with-testify-package) – https://tonybai.com/2023/07/16/the-guide-of-go-testing-with-testify-package

我虽然算不上Go标准库的“清教徒”，但在测试方面还多是基于标准库testing包以及go test框架的，除了需要mock的时候，基本上没有用过第三方的Go测试框架。我在[《Go语言精进之路》](https://book.douban.com/subject/35720729/)一书中对Go测试组织的讲解也是基于Go testing包和go test框架的。

最近看Apache arrow代码，发现arrow的Go实现使用了[testify项目](https://github.com/stretchr/testify)组织和辅助测试：

```
// compute/vector_hash_test.go
func TestHashKernels(t *testing.T) {
suite.Run(t, &PrimitiveHashKernelSuite[int8]{})
suite.Run(t, &PrimitiveHashKernelSuite[uint8]{})
suite.Run(t, &PrimitiveHashKernelSuite[int16]{})
suite.Run(t, &PrimitiveHashKernelSuite[uint16]{})
... ...
}
type PrimitiveHashKernelSuite[T exec.IntTypes | exec.UintTypes | constraints.Float] struct {
suite.Suite
mem *memory.CheckedAllocator
dt arrow.DataType
}
func (ps *PrimitiveHashKernelSuite[T]) SetupSuite() {
ps.dt = exec.GetDataType[T]()
}
func (ps *PrimitiveHashKernelSuite[T]) SetupTest() {
ps.mem = memory.NewCheckedAllocator(memory.DefaultAllocator)
}
func (ps *PrimitiveHashKernelSuite[T]) TearDownTest() {
ps.mem.AssertSize(ps.T(), 0)
}
func (ps *PrimitiveHashKernelSuite[T]) TestUnique() {
... ...
}
```


同期，我在[grank.io](https://www.grank.io/)上看到testify这个项目综合排名第一：

![](../../assets/c2fce9033cd42157.png)


这说明testify项目在Go社区有着广泛的受众，testify为何能从众多go test第三方框架中脱颖而出？它有哪些与众不同的地方？如何更好地利用testify来辅助我们的Go测试？带着这些问题，我写下了这篇有关testify的文章，供大家参考。

## 1. testify简介

testify是一个用于Go语言的测试框架，与go testing包可以很好的融合在一起，并由go test驱动运行。testify提供的功能特性可以辅助Go开发人员更好地组织和更高效地编写测试用例，以保证软件的质量和可靠性。

testify能够得到社区的广泛接纳，与testify项目中**包的简洁与独立的设计**是密不可分的。下面是testify包的目录结构(去掉了用于生成代码的codegen和已经deprecated的http目录后)：

```
$tree -F -L 1 testify |grep "/" |grep -v codegen|grep -v http
├── assert/
├── mock/
├── require/
└── suite/
```


关于Go项目代码布局设计的系统讲解，可以参见我的

[《Go语言第一课》专栏]的第5讲。

包目录名直接反映了testify可以提供给Go开发者的功能特性：

- assert和require：断言工具包，辅助做测试结果判定；
- mock：辅助编写mock test的工具包；
- suite：提供了suite这一层的测试组织结构。

下面我们就**由浅入深**的介绍testify的这几个重要的、可各自独立使用的包。我们先从**使用门槛最低**的assert包和require包开始，它们是一类的，这里放在一个章节中介绍。

## 2. assert和require包

我们在使用go testing包编写Go单元测试用例时，通常会用下面代码来判断目标函数执行结果是否符合预期：

```
func TestFoo(t *testing.T) {
v := Foo(5, 6) // Foo为被测目标函数
if v != expected {
t.Errorf("want %d, actual %d\n", expected, v)
}
}
```


这样，如果测试用例要判断的结果很多，那么测试代码中就会存在很多if xx != yy以及Errorf/Fatalf之类的代码。有过一些其他语言编程经验的童鞋此时此刻肯定会说：**是时候上assert了**! 不过很遗憾，Go标准库包括其[实验库(exp)](https://github.com/golang/exp)都没有提供带有assert断言机制的包。

注：Go标准库testing/quick包中提供的Check和CheckEqual并非assert，它们用于测试两个函数参数在相同输入的情况下是否有相同的输出。如果不同，则输出导致输出不同的输入。此外，该quick包已经frozen，不再接受新Feature。


testify为Go开发人员提供了assert包，为Go开发人员很大程度“解了近渴”。

assert包使用起来非常简单，下面是assert使用的常见场景示例：

```
// assert/assert_test.go
func Add(a, b int) int {
return a + b
}
func TestAssert(t *testing.T) {
// Equal断言
assert.Equal(t, 4, Add(1, 3), "The result should be 4")
sl1 := []int{1, 2, 3}
sl2 := []int{1, 2, 3}
sl3 := []int{2, 3, 4}
assert.Equal(t, sl1, sl2, "sl1 should equal to sl2 ")
p1 := &sl1
p2 := &sl2
assert.Equal(t, p1, p2, "the content which p1 point to should equal to which p2 point to")
err := errors.New("demo error")
assert.EqualError(t, err, "demo error")
// assert.Exactly(t, int32(123), int64(123)) // failed! both type and value must be same
// 布尔断言
assert.True(t, 1+1 == 2, "1+1 == 2 should be true")
assert.Contains(t, "Hello World", "World")
assert.Contains(t, []string{"Hello", "World"}, "World")
assert.Contains(t, map[string]string{"Hello": "World"}, "Hello")
assert.ElementsMatch(t, []int{1, 3, 2, 3}, []int{1, 3, 3, 2})
// 反向断言
assert.NotEqual(t, 4, Add(2, 3), "The result should not be 4")
assert.NotEqual(t, sl1, sl3, "sl1 should not equal to sl3 ")
assert.False(t, 1+1 == 3, "1+1 == 3 should be false")
assert.Never(t, func() bool { return false }, time.Second, 10*time.Millisecond) //1秒之内condition参数都不为true，每10毫秒检查一次
assert.NotContains(t, "Hello World", "Go")
}
```


我们看到assert包提供了Equal类、布尔类、反向类断言，assert包提供的断言函数有几十种，这里无法一一枚举，选择最适合你的测试场景的断言就好。

另外要注意的是，在Equal对切片作比较时，比较的是切片底层数组存储的内容是否相等；对指针作比较时，比较的是指针指向的内存块儿的数据是否相等，而不是指针本身的值是否相等。

注：assert.Equal底层实现使用的是reflect.DeepEqual。


我们看到assert包提供的断言函数第一个参数是testing.T的实例，如果一个测试用例里多次使用assert包的断言函数，我们每次都要传入testing.T的实例，比如下面示例：

```
// assert/assert_test.go
func TestAdd1(t *testing.T) {
result := Add(1, 3)
assert.Equal(t, 4, result, "The result should be 4")
result = Add(2, 2)
assert.Equal(t, 4, result, "The result should be 4")
result = Add(2, 3)
assert.Equal(t, 5, result, "The result should be 5")
result = Add(0, 3)
assert.Equal(t, 3, result, "The result should be 3")
result = Add(-1, 1)
assert.Equal(t, 0, result, "The result should be 0")
}
```


这很verbose! assert包提供了替代方法，如下面示例：

```
// assert/assert_test.go
func TestAdd2(t *testing.T) {
assert := assert.New(t)
result := Add(1, 3)
assert.Equal(4, result, "The result should be 4")
result = Add(2, 2)
assert.Equal(4, result, "The result should be 4")
result = Add(2, 3)
assert.Equal(5, result, "The result should be 5")
result = Add(0, 3)
assert.Equal(3, result, "The result should be 3")
result = Add(-1, 1)
assert.Equal(0, result, "The result should be 0")
}
```


注：我们当然可以使用表驱动测试的方法将上述示例做进一步优化。


require包可以理解为assert包的“姊妹包”，require包实现了assert包提供的所有导出的断言函数，因此我们将上述示例中的assert改为require后，代码可以正常编译和运行(见require/require_test.go)。

那么require包与assert包有什么不同呢？我们来简单看一下。

使用assert包的断言时，如果某一个断言失败，该失败不会影响到后续测试代码的执行，或者说后续测试代码会继续执行，比如我们故意将TestAssert中的一些断言条件改为失败：

```
// assert/assert_test.go
assert.True(t, 1+1 == 3, "1+1 == 2 should be true")
assert.Contains(t, "Hello World", "World1")
```


再运行assert_test.go中的测试，我们会看到下面结果：

```
$go test
--- FAIL: TestAssert (1.00s)
assert_test.go:34:
Error Trace:
Error: Should be true
Test: TestAssert
Messages: 1+1 == 2 should be true
assert_test.go:35:
Error Trace:
Error: "Hello World" does not contain "World1"
Test: TestAssert
FAIL
exit status 1
FAIL demo 1.016s
```


我们看到：两个失败的测试断言都输出了！

我们再换到require/require_test.go下做同样的修改，并执行go test，我们得到如下结果：

```
$go test require_test.go
--- FAIL: TestRequire (0.00s)
require_test.go:34:
Error Trace:
Error: Should be true
Test: TestRequire
Messages: 1+1 == 2 should be true
FAIL
FAIL command-line-arguments 0.012s
FAIL
```


我们看到当执行完第一条失败的断言后，测试便结束了！

这就是assert包和require包的区别！这有些类似于Errorf和Fatalf的区别！require包中断言函数一旦执行失败便会导致测试退出，后续的测试代码将无法继续执行。

另外require包还有一个“特点”，那就是它的主体代码(require.go和require_forward.go)都是自动生成的：

```
// github.com/stretchr/testify/require/reqire.go
/*
CODE GENERATED AUTOMATICALLY WITH github.com/stretchr/testify/_codegen
* THIS FILE MUST NOT BE EDITED BY HAND
*/
```


testify的代码生成采用了基于模板的方法，具体的自动生成原理可以参考[《A case for Go code generation: testify》] (https://levelup.gitconnected.com/a-case-for-go-code-generation-testify-73a4b0d46cb1)这篇文章。

## 3. suite包

Go testing包没有引入testsuite(测试套件)或testcase(测试用例)的概念，只有Test和[SubTest](https://tonybai.com/2023/03/15/an-intro-of-go-subtest/)。对于熟悉xUnit那套测试组织方式的开发者来说，这种缺失很“别扭”！要么自己基于testing包来构建这种结构，要么使用第三方包的实现。

![](../../assets/ce46e145debeeef3.jpg)



testify的suite包为我们提供了一种基于suite/case结构组织测试代码的方式。下面是一个可以对testify suite定义的suite结构进行全面解析的示例(改编自testify suite包文档中的ExampleTestSuite示例)：

```
// suite/suite_test.go
package main
import (
"fmt"
"testing"
"github.com/stretchr/testify/suite"
)
type ExampleSuite struct {
suite.Suite
indent int
}
func (suite *ExampleSuite) indents() (result string) {
for i := 0; i < suite.indent; i++ {
result += "----"
}
return
}
func (suite *ExampleSuite) SetupSuite() {
fmt.Println("Suite setup")
}
func (suite *ExampleSuite) TearDownSuite() {
fmt.Println("Suite teardown")
}
func (suite *ExampleSuite) SetupTest() {
suite.indent++
fmt.Println(suite.indents(), "Test setup")
}
func (suite *ExampleSuite) TearDownTest() {
fmt.Println(suite.indents(), "Test teardown")
suite.indent--
}
func (suite *ExampleSuite) BeforeTest(suiteName, testName string) {
suite.indent++
fmt.Printf("%sBefore %s.%s\n", suite.indents(), suiteName, testName)
}
func (suite *ExampleSuite) AfterTest(suiteName, testName string) {
fmt.Printf("%sAfter %s.%s\n", suite.indents(), suiteName, testName)
suite.indent--
}
func (suite *ExampleSuite) SetupSubTest() {
suite.indent++
fmt.Println(suite.indents(), "SubTest setup")
}
func (suite *ExampleSuite) TearDownSubTest() {
fmt.Println(suite.indents(), "SubTest teardown")
suite.indent--
}
func (suite *ExampleSuite) TestCase1() {
suite.indent++
defer func() {
fmt.Println(suite.indents(), "End TestCase1")
suite.indent--
}()
fmt.Println(suite.indents(), "Begin TestCase1")
suite.Run("case1-subtest1", func() {
suite.indent++
fmt.Println(suite.indents(), "Begin TestCase1.Subtest1")
fmt.Println(suite.indents(), "End TestCase1.Subtest1")
suite.indent--
})
suite.Run("case1-subtest2", func() {
suite.indent++
fmt.Println(suite.indents(), "Begin TestCase1.Subtest2")
fmt.Println(suite.indents(), "End TestCase1.Subtest2")
suite.indent--
})
}
func (suite *ExampleSuite) TestCase2() {
suite.indent++
defer func() {
fmt.Println(suite.indents(), "End TestCase2")
suite.indent--
}()
fmt.Println(suite.indents(), "Begin TestCase2")
suite.Run("case2-subtest1", func() {
suite.indent++
fmt.Println(suite.indents(), "Begin TestCase2.Subtest1")
fmt.Println(suite.indents(), "End TestCase2.Subtest1")
suite.indent--
})
}
func TestExampleSuite(t *testing.T) {
suite.Run(t, new(ExampleSuite))
}
```


要知道testify.suite包定义的测试结构是什么样的，我们运行一下上述代码即可：

```
$go test
Suite setup
---- Test setup
--------Before ExampleSuite.TestCase1
------------ Begin TestCase1
---------------- SubTest setup
-------------------- Begin TestCase1.Subtest1
-------------------- End TestCase1.Subtest1
---------------- SubTest teardown
---------------- SubTest setup
-------------------- Begin TestCase1.Subtest2
-------------------- End TestCase1.Subtest2
---------------- SubTest teardown
------------ End TestCase1
--------After ExampleSuite.TestCase1
---- Test teardown
---- Test setup
--------Before ExampleSuite.TestCase2
------------ Begin TestCase2
---------------- SubTest setup
-------------------- Begin TestCase2.Subtest1
-------------------- End TestCase2.Subtest1
---------------- SubTest teardown
------------ End TestCase2
--------After ExampleSuite.TestCase2
---- Test teardown
Suite teardown
```


信息量很大，我们慢慢说！

利用testify建立测试套件，我们需要**自行定义嵌入了suite.Suite的结构体类型**，如上面示例中的ExampleSuite。

testify与go testing兼容，由go test驱动执行，因此我们需要在一个TestXXX函数中创建ExampleSuite的实例，调用suite包的Run函数，并将执行权交给suite包的这个Run函数，后续的执行逻辑就是suite包Run函数的执行逻辑。在上述代码中，我们只定义了一个TestXXX，并使用suite.Run函数执行了ExampleSuite中的所有测试用例。

suite.Run函数的执行逻辑大致是：通过[反射机制](https://tonybai.com/2023/06/04/reflection-programming-guide-in-go)得到了*ExampleSuite类型的方法集合，并执行方法集合中名字以Test为前缀的所有方法。testify将用户自定义的XXXSuite类型中的每个以Test为前缀的方法当作是一个TestCase。

除了Suite和TestCase的概念外，testify.suite包还“预埋”了很多回调点，包括suite的Setup、TearDown；test case的Setup和TearDown、testcase的before和after；subtest的Setup和TearDown，这些回调点也由suite.Run函数来执行，回调点的执行顺序可以通过上面示例的执行结果看到。

注意：subtest要通过XXXSuite的Run方法执行，而不要通过标准库testing.T的Run方法执行。


我们知道：go test工具可以通过-run命令行参数来选择要执行的TestXXX函数，考虑到testify使用TestXXX函数拉起测试套件(XXXSuite)，因此从testify视角来看，通过go test -run可以选择执行哪个XXXSuite，前提是一个TestXXX中仅初始化和运行一种XXXSuite的所有测试用例。

如果要选择XXXSuite的方法(即testify眼中的测试用例)，我们不能用-run了，需要使用testify新增的-m命令行选项，下面是一个仅执行带有Case2关键字测试用例的示例：

```
$go test -testify.m Case2
Suite setup
---- Test setup
--------Before ExampleSuite.TestCase2
------------ Begin TestCase2
---------------- SubTest setup
-------------------- Begin TestCase2.Subtest1
-------------------- End TestCase2.Subtest1
---------------- SubTest teardown
------------ End TestCase2
--------After ExampleSuite.TestCase2
---- Test teardown
Suite teardown
PASS
ok demo 0.014s
```


综上，如果你使用testify的Suite/Case概念来组织你的测试代码，建议在每个TestXXX中仅初始化和运行一个XXXSuite，这样你可以通过-run选择特定的Suite执行。

## 4. mock包

最后我们来看看testify为辅助Go开发人员编写测试代码而提供的一个高级特性：mock。

在之前的文章中，我提到过：[尽量使用fake object，而不是mock object](https://tonybai.com/2023/04/20/provide-fake-object-for-external-collaborators/)。mock这种测试替身有其难于理解、使用场合局限以及给予开发人员信心不足等弊端。

注：近期原Go官方维护的

[golang/mock]也将维护权迁移给了uber，迁移后的新的mock库为[go.uber.org/mock]。我在[《Go语言精进之路 vol2》]一书中对golang/mock做过详细的使用介绍，有兴趣的朋友可以去读一读。

但“存在即合理”，显然mock也有它的用武空间，在社区也有它的拥趸，既然testify提供了mock包，这里就简单介绍一下它的基本使用方法。

我们用一个经典repo service的例子来演示如何使用testify mock，如下面代码示例：

```
// mock/mock_test.go
type User struct {
ID int
Name string
Age int
}
type UserRepository interface {
CreateUser(user *User) (int, error)
GetUserById(id int) (*User, error)
}
type UserService struct {
repo UserRepository
}
func NewUserService(repo UserRepository) *UserService {
return &UserService{repo: repo}
}
func (s *UserService) CreateUser(name string, age int) (*User, error) {
user := &User{Name: name, Age: age}
id, err := s.repo.CreateUser(user)
if err != nil {
return nil, err
}
user.ID = id
return user, nil
}
func (s *UserService) GetUserById(id int) (*User, error) {
return s.repo.GetUserById(id)
}
```


我们要提供一个UserService服务，通过该服务可以创建User，也可以通过ID获取User信息。服务的背后是一个UserRepository，你可以用任何方法实现UserRepository，为此我们将其抽象为一个接口UserRepository。UserService要依赖UserRepository才能让它的两个方法CreateUser和GetUserById正常工作。现在我们要测试UserService的这两个方法，但我们手里没有现成的UserRepository实现可用，我们也没有UserRepository的fake object。

这时我们仅能用mock。下面是使用testify mock给出的UserRepository接口的实现UserRepositoryMock：

```
// mock/mock_test.go
type UserRepositoryMock struct {
mock.Mock
}
func (m *UserRepositoryMock) CreateUser(user *User) (int, error) {
args := m.Called(user)
return args.Int(0), args.Error(1)
}
func (m *UserRepositoryMock) GetUserById(id int) (*User, error) {
args := m.Called(id)
return args.Get(0).(*User), args.Error(1)
}
```


我们基于mock.Mock创建一个新结构体类型UserRepositoryMock，这就是我们要创建的模拟UserRepository。我们实现了它的两个方法，与正常方法实现不同的是，在方法中我们使用的是mock.Mock提供的方法Called以及它的返回值来满足CreateUser和GetUserById两个方法的参数与返回值要求。

UserRepositoryMock这两个方法的实现是比较“模式化”的，其中调用的Called接收了外部方法的所有参数，然后通过Called的返回值args来构造满足外部方法的返回值。返回值构造的书写格式如下：

```
args.<ReturnValueType>(<index>) // 其中index从0开始
```


以CreateUser为例，它有两个返回值int和error，那按照上面的书写格式，我们的返回值就应该为：args.int(0)和args.Error(1)。

对于复杂结构的返回值类型T，可使用断言方式，书写格式变为：

```
args.Get(index).(T)
```


再以构造GetUserById的返回值*User和error为例，我们按照复杂返回值构造的书写格式来编写，返回值就应该为args.Get(0).(*User)和args.Error(1)。

有了Mock后的UserRepository，我们就可以来编写UserService的方法的测试用例了：

```
// mock/mock_test.go
func TestUserService_CreateUser(t *testing.T) {
repo := new(UserRepositoryMock)
service := NewUserService(repo)
user := &User{Name: "Alice", Age: 30}
repo.On("CreateUser", user).Return(1, nil)
createdUser, err := service.CreateUser(user.Name, user.Age)
assert.NoError(t, err)
assert.Equal(t, 1, createdUser.ID)
assert.Equal(t, "Alice", createdUser.Name)
assert.Equal(t, 30, createdUser.Age)
repo.AssertExpectations(t)
}
func TestUserService_GetUserById(t *testing.T) {
repo := new(UserRepositoryMock)
service := NewUserService(repo)
user := &User{ID: 1, Name: "Alice", Age: 30}
repo.On("GetUserById", 1).Return(user, nil)
foundUser, err := service.GetUserById(1)
assert.NoError(t, err)
assert.Equal(t, 1, foundUser.ID)
assert.Equal(t, "Alice", foundUser.Name)
assert.Equal(t, 30, foundUser.Age)
repo.AssertExpectations(t)
}
```


这两个TestXXX函数的编写模式也十分相近，以TestUserService_GetUserById为例，它先创建了UserRepositoryMock和UserService的实例，然后利用UserRepositoryMock来设置即将被调用的GetUserById方法的输入参数与返回值：

```
user := &User{ID: 1, Name: "Alice", Age: 30}
repo.On("GetUserById", 1).Return(user, nil)
```


这样当GetUserById在service.GetUserById方法中被调用时，它返回的就是上面设置的user地址值和nil。

之后，我们像常规测试用例那样，用assert包对返回的值与预期值做断言即可。

## 5. 小结

在本文中，我们讲解了testify这个第三方辅助测试包的结构，并针对其中的assert/require、suite和mock这几个相对独立的Go包的用法做了重点说明。

assert/require包是功能十分全面的测试断言包，即便你不使用suite、mock，你也可以单独使用assert/require包来减少你的测试代码中if != xxx的书写行数。

suite包则为我们提供了一个类xUnit的Suite/Case的测试代码组织形式的实现方案，并且这种方案与go testing包兼容，由go test驱动。

虽然我不建议用mock，但testify mock也实现了mock机制的基本功能。并且文中没有提及的是，结合[mockery](https://vektra.github.io/mockery/latest/)工具和testify mock，我们可以针对接口为被测目标自动生成testify的mock部分代码，这会大大提交mock test的编写效率。

综上来看，testify这个项目的确非常有用，可以很好的辅助Go开发者高效的编写和组织测试用例。目前testify正在策划[dev v2版本](https://docs.google.com/forms/d/e/1FAIpQLScQweSh4N4QqK3JESHTNyHjx0-lMApCK1--GvbXlB3dKyydeg/) ，相信不久将来落地的v2版本能给Go开发者带来更多的帮助。

本文涉及到的源码可以在[这里](https://github.com/bigwhite/experiments/tree/master/testify-examples)下载。

[“Gopher部落”知识星球](https://wx.zsxq.com/dweb2/index/group/51284458844544)旨在打造一个精品Go学习和进阶社群！高品质首发Go技术文章，“三天”首发阅读权，每年两期Go语言发展现状分析，每天提前1小时阅读到新鲜的Gopher日报，网课、技术专栏、图书内容前瞻，六小时内必答保证等满足你关于Go语言生态的所有需求！2023年，Gopher部落将进一步聚焦于如何编写雅、地道、可读、可测试的Go代码，关注代码质量并深入理解Go核心技术，并继续加强与星友的互动。欢迎大家加入！

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