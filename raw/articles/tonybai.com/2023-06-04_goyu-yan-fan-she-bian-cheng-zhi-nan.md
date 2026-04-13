---
title: Go语言反射编程指南
url: https://tonybai.com/2023/06/04/reflection-programming-guide-in-go/
published: '2023-06-04'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go语言反射编程指南

![](../../assets/613339fdf1a29359.png)


[本文永久链接](https://tonybai.com/2023/06/04/reflection-programming-guide-in-go) – https://tonybai.com/2023/06/04/reflection-programming-guide-in-go

[反射](https://en.wikipedia.org/wiki/Reflective_programming)是一种编程语言的高级特性，它允许程序在运行时检视自身的结构和行为。通过反射，程序可以动态地获取类型(type)与值(value)等信息，并对它们进行操作，诸如修改字段、调用方法等，这使得程序具有更大的灵活性和可扩展性。

不过，反射虽然具有强大的功能，但也存在一些缺点。由于反射是在运行时进行的，因此它比直接调用代码的性能要差。此外，反射还可能导致代码的可读性和维护性降低，因为它使得程序行为更加难以预测和理解。因此，在使用反射时需要注意性能和可维护性。

Go从诞生伊始就在运行时支持了反射，并在标准库中提供了reflect包供开发者进行反射编程时使用。在这篇文章中，我们就来系统地了解一下如何在Go中通过reflect包实现反射编程。

注：我的

[Go语言精进之路]一书有关于Go反射的进阶讲解，欢迎阅读。

## 1. Go语言反射基础

相对于C/C++等系统编程语言，Go的运行时承担的功能要更多一些，比如[Goroutine调度](https://tonybai.com/2017/06/23/an-intro-about-goroutine-scheduler)、[Go内存垃圾回收(GC)](https://t.zsxq.com/0eXDduygo)等。同时反射也为开发者与运行时之间提供了一个方便的、合法的交互窗口。通过反射，开发者可以合法的窥探关于Go类型系统的一些元信息。

注：

[《Go语言第一课》]专栏第31~34讲对Goroutine调度以及Go并发编程做了系统详细的讲解，欢迎阅读。

Go语言的反射包（reflect包）是一个内置的包，它提供了一组API，能够在运行时获取和修改Go语言程序的结构和行为。reflect包也是所有Go反射编程的基础API，是进行Go反射编程的必经之路。

在本节中，我们将会探讨reflect包的一些基础知识，包括Type和Value两个重要的反射包类型，以及如何使用TypeOf和ValueOf方法来获取类型信息和值信息。

### 1.1 Type和Value

在reflect包中，Type和Value是两个非常重要的概念，它们分别表示了反射世界中的类型信息和值信息。

Type表示一个类型的元信息，它包含了类型的名称、大小、方法集合等信息。在反射编程中，我们可以使用TypeOf函数来获取一个值的类型信息。

Value表示一个值的信息，它包含了值的类型、值本身以及对值进行操作的方法集合等信息。在反射中，我们可以使用ValueOf函数来获取一个值的Value信息。

reflect包的TypeOf和ValueOf两个函数是进入反射世界的基本入口。下面我们来看看这两个函数的基本用法示例。

### 1.2 如何获取类型信息（TypeOf）

获取类型信息是反射的一个重要功能。在Go语言中，我们可以使用reflect包的TypeOf函数来获取一个值的类型信息。TypeOf函数的签名如下：

```
func TypeOf(i any) Type
```


TypeOf函数接受一个任意类型的值作为参数，并返回该值的类型信息，即interface{}接口类型变量中存储的动态类型信息。例如，我们可以使用TypeOf函数获取一个字符串的类型信息：

```
import (
"fmt"
"reflect"
)
func main() {
s := "hello, world!"
t := reflect.TypeOf(s)
fmt.Println(t.Name()) // string
}
```


用图直观表示如下：

![](../../assets/77653941871144b5.png)


### 1.4 如何获取值信息（ValueOf）

获取值信息是反射的另一个重要功能。在Go语言中，我们可以使用reflect包的ValueOf函数来获取一个值的Value信息。ValueOf函数的签名如下：

```
func ValueOf(i any) Value
```


ValueOf函数接受一个任意类型的值作为参数，并返回该值的Value信息，即interface{}接口类型变量中存储的动态类型的值的信息。例如，我们可以使用ValueOf函数获取一个整数的Value信息：

```
import (
"fmt"
"reflect"
)
func main() {
i := 42
v := reflect.ValueOf(i)
fmt.Println(v.Int()) // 42
}
```


在上述示例中，我们首先定义了一个整数i，然后使用ValueOf函数获取其Value信息，并调用Int方法获取其值。

用图直观表示如下：

![](../../assets/c664503bd1a51593.png)


以上就是reflect包TypeOf和ValueOf函数的基本用法的示例，下面我们再来详细看看获取不同类型的类型信息和值信息的细节。

## 2. 检视类型信息和调用类型方法

reflect.Type实质上是一个接口类型，它封装了reflect可以提供的类型信息的所有方法(Go 1.20版本中的reflect.Type)：

```
// $GOROOT/src/reflect/type.go
type Type interface {
// Methods applicable to all types.
// Align returns the alignment in bytes of a value of
// this type when allocated in memory.
Align() int
// FieldAlign returns the alignment in bytes of a value of
// this type when used as a field in a struct.
FieldAlign() int
// Method returns the i'th method in the type's method set.
// It panics if i is not in the range [0, NumMethod()).
//
// For a non-interface type T or *T, the returned Method's Type and Func
// fields describe a function whose first argument is the receiver,
// and only exported methods are accessible.
//
// For an interface type, the returned Method's Type field gives the
// method signature, without a receiver, and the Func field is nil.
//
// Methods are sorted in lexicographic order.
Method(int) Method
// MethodByName returns the method with that name in the type's
// method set and a boolean indicating if the method was found.
//
// For a non-interface type T or *T, the returned Method's Type and Func
// fields describe a function whose first argument is the receiver.
//
// For an interface type, the returned Method's Type field gives the
// method signature, without a receiver, and the Func field is nil.
MethodByName(string) (Method, bool)
// NumMethod returns the number of methods accessible using Method.
//
// For a non-interface type, it returns the number of exported methods.
//
// For an interface type, it returns the number of exported and unexported methods.
NumMethod() int
// Name returns the type's name within its package for a defined type.
// For other (non-defined) types it returns the empty string.
Name() string
// PkgPath returns a defined type's package path, that is, the import path
// that uniquely identifies the package, such as "encoding/base64".
// If the type was predeclared (string, error) or not defined (*T, struct{},
// []int, or A where A is an alias for a non-defined type), the package path
// will be the empty string.
PkgPath() string
// Size returns the number of bytes needed to store
// a value of the given type; it is analogous to unsafe.Sizeof.
Size() uintptr
// String returns a string representation of the type.
// The string representation may use shortened package names
// (e.g., base64 instead of "encoding/base64") and is not
// guaranteed to be unique among types. To test for type identity,
// compare the Types directly.
String() string
// Kind returns the specific kind of this type.
Kind() Kind
// Implements reports whether the type implements the interface type u.
Implements(u Type) bool
// AssignableTo reports whether a value of the type is assignable to type u.
AssignableTo(u Type) bool
// ConvertibleTo reports whether a value of the type is convertible to type u.
// Even if ConvertibleTo returns true, the conversion may still panic.
// For example, a slice of type []T is convertible to *[N]T,
// but the conversion will panic if its length is less than N.
ConvertibleTo(u Type) bool
// Comparable reports whether values of this type are comparable.
// Even if Comparable returns true, the comparison may still panic.
// For example, values of interface type are comparable,
// but the comparison will panic if their dynamic type is not comparable.
Comparable() bool
// Methods applicable only to some types, depending on Kind.
// The methods allowed for each kind are:
//
// Int*, Uint*, Float*, Complex*: Bits
// Array: Elem, Len
// Chan: ChanDir, Elem
// Func: In, NumIn, Out, NumOut, IsVariadic.
// Map: Key, Elem
// Pointer: Elem
// Slice: Elem
// Struct: Field, FieldByIndex, FieldByName, FieldByNameFunc, NumField
// Bits returns the size of the type in bits.
// It panics if the type's Kind is not one of the
// sized or unsized Int, Uint, Float, or Complex kinds.
Bits() int
// ChanDir returns a channel type's direction.
// It panics if the type's Kind is not Chan.
ChanDir() ChanDir
// IsVariadic reports whether a function type's final input parameter
// is a "..." parameter. If so, t.In(t.NumIn() - 1) returns the parameter's
// implicit actual type []T.
//
// For concreteness, if t represents func(x int, y ... float64), then
//
// t.NumIn() == 2
// t.In(0) is the reflect.Type for "int"
// t.In(1) is the reflect.Type for "[]float64"
// t.IsVariadic() == true
//
// IsVariadic panics if the type's Kind is not Func.
IsVariadic() bool
// Elem returns a type's element type.
// It panics if the type's Kind is not Array, Chan, Map, Pointer, or Slice.
Elem() Type
// Field returns a struct type's i'th field.
// It panics if the type's Kind is not Struct.
// It panics if i is not in the range [0, NumField()).
Field(i int) StructField
// FieldByIndex returns the nested field corresponding
// to the index sequence. It is equivalent to calling Field
// successively for each index i.
// It panics if the type's Kind is not Struct.
FieldByIndex(index []int) StructField
// FieldByName returns the struct field with the given name
// and a boolean indicating if the field was found.
FieldByName(name string) (StructField, bool)
// FieldByNameFunc returns the struct field with a name
// that satisfies the match function and a boolean indicating if
// the field was found.
//
// FieldByNameFunc considers the fields in the struct itself
// and then the fields in any embedded structs, in breadth first order,
// stopping at the shallowest nesting depth containing one or more
// fields satisfying the match function. If multiple fields at that depth
// satisfy the match function, they cancel each other
// and FieldByNameFunc returns no match.
// This behavior mirrors Go's handling of name lookup in
// structs containing embedded fields.
FieldByNameFunc(match func(string) bool) (StructField, bool)
// In returns the type of a function type's i'th input parameter.
// It panics if the type's Kind is not Func.
// It panics if i is not in the range [0, NumIn()).
In(i int) Type
// Key returns a map type's key type.
// It panics if the type's Kind is not Map.
Key() Type
// Len returns an array type's length.
// It panics if the type's Kind is not Array.
Len() int
// NumField returns a struct type's field count.
// It panics if the type's Kind is not Struct.
NumField() int
// NumIn returns a function type's input parameter count.
// It panics if the type's Kind is not Func.
NumIn() int
// NumOut returns a function type's output parameter count.
// It panics if the type's Kind is not Func.
NumOut() int
// Out returns the type of a function type's i'th output parameter.
// It panics if the type's Kind is not Func.
// It panics if i is not in the range [0, NumOut()).
Out(i int) Type
common() *rtype
uncommon() *uncommonType
}
```


我们看到这是一个“超级接口”，严格来说并不符合Go接口设计的惯例。

注：Go崇尚小接口。以Type接口为例，可以对Type接口做进一步分解，分解成若干内聚的小接口，然后将Type看成小接口的组合。


对于不同类型，Type接口的有些方法是冗余的，比如像上面的NumField、NumIn和NumOut方法对于一个int变量的类型信息来说就毫无意义。Type类型的注释中也提到：“Not all methods apply to all kinds of types”。

一旦通过TypeOf进入反射世界，拿到Type类型变量，那么我们就可以基于上述方法“翻看”类型的各种信息了。

对于像int、float64、string这样的基本类型来说，其类型信息的检视没有太多可说的。但对于其他类型，诸如复合类型、指针类型、函数类型等，还是有一些可聊聊的，我们下面逐一简单地看一下。

### 2.1 复合类型

#### 2.1.1 数组类型

在Go中，数组类型是一种典型的复合类型，它有若干属性，包括数组长度、数组是否支持可比较、数组元素的类型等，看下面示例：

```
import (
"fmt"
"reflect"
)
func main() {
arr := [5]int{1, 2, 3, 4, 5}
typ := reflect.TypeOf(arr)
fmt.Println(typ.Kind()) // array
fmt.Println(typ.Len()) // 5
fmt.Println(typ.Comparable()) // true
elemTyp := typ.Elem()
fmt.Println(elemTyp.Kind()) // int
fmt.Println(elemTyp.Comparable()) // true
}
```


注：通过类型信息无法间接得到值信息，反之不然，稍后系统说明reflect.Value时会提到。


在这个例子，我们输出了arr这个数组类型变量的Kind信息。什么是Kind信息呢？reflect包中是如此定义的：

```
// A Kind represents the specific kind of type that a Type represents.
// The zero Kind is not a valid kind.
type Kind uint
const (
Invalid Kind = iota
Bool
Int
Int8
Int16
Int32
Int64
Uint
Uint8
Uint16
Uint32
Uint64
Uintptr
Float32
Float64
Complex64
Complex128
Array
Chan
Func
Interface
Map
Pointer
Slice
String
Struct
UnsafePointer
)
```


我们可以将Kind当做是Go type信息的元信息，对于基本类型来说，如int、string、float64等，它的kind和它的type的表达是一致的。但对于像数组、切片等类型，kind更像是type的type。

以两个数组类型为例：

```
var arr1 [10]string
var arr2 [8]int
```


这两个数组类型的类型分别是[10]string和[8]int，但它们在反射世界的reflect.Type的Kind信息却都为Array。

再比如下面两个指针类型：

```
var p1 *float64
var p2 *MyFoo
```


这两个指针类型的类型分别是*float64和*MyFoo，但它们在反射世界的reflect.Type的Kind信息却都为Pointer。

Kind信息可以帮助开发人员在反射世界中区分类型，以对不同类型作不同的处理。比如对于Kind为Int的reflect.Type，你不能使用其Len()方法，否则会panic；但对于Kind为Array的则可以。开发人员使用反射提供的Kind信息可以处理不同类型的数据。

#### 2.1.2 切片类型

在Go中切片是动态数组，可灵活、透明的扩容，多数情况下切片都能替代数组完成任务。在反射世界中通过reflect.Type我们可以获取切片类型的信息，包括元素类型等。下面是一个示例：

```
package main
import (
"fmt"
"reflect"
)
func main() {
s := make([]int, 5, 10)
typ := reflect.TypeOf(s)
fmt.Println(typ.Kind()) // slice
fmt.Println(typ.Elem()) // int
}
```


如果我们使用上面的变量typ调用Type类型的Len和Cap方法会发生什么呢？在运行时，你将得到类似”panic: reflect: Len of non-array type []int”的报错！

那么问题来了！切片长度、容量到底是否是slice type的信息范畴呢? 我们来看一个例子：

```
var a = make([]int, 5, 10)
var b = make([]int, 7,
```



变量a和b的类型都是[]int。显然长度、容量等并不在切片类型的范畴，而是与切片变量值绑定的，下面的示例印证了这一点：

```
func main() {
s := make([]int, 5, 10)
val := reflect.ValueOf(s)
fmt.Println(val.Len()) // 5
fmt.Println(val.Cap()) // 10
}
```


我们获取了切片变量s的reflect.Value信息，通过Value我们得到了变量s的长度和容量信息。

#### 2.1.3 结构体类型

结构体类型是与反射联合使用的重要类型，下面代码展示了如何通过reflect.Type获取结构体类型的相关信息：

```
package main
import (
"fmt"
"reflect"
)
type Person struct {
Name string `json:"name"`
Age int `json:"age"`
gender string
}
func (p Person) SayHello() {
fmt.Printf("Hello, my name is %s, and I'm %d years old.\n", p.Name, p.Age)
}
func (p Person) unexportedMethod() {
}
func main() {
p := Person{Name: "Tom", Age: 20, gender: "male"}
typ := reflect.TypeOf(p)
fmt.Println(typ.Kind()) // struct
fmt.Println(typ.NumField()) // 3
fmt.Println(typ.Field(0).Name) // Name
fmt.Println(typ.Field(0).Type) // string
fmt.Println(typ.Field(0).Tag) // json:"name"
fmt.Println(typ.Field(1).Name) // Age
fmt.Println(typ.Field(1).Type) // int
fmt.Println(typ.Field(1).Tag) // json:"age"
fmt.Println(typ.Field(2).Name) // gender
fmt.Println(typ.Method(0).Name) // SayHello
fmt.Println(typ.Method(0).Type) // func(main.Person)
fmt.Println(typ.Method(0).Func) // 0x109b6e0
fmt.Println(typ.MethodByName("SayHello")) // {SayHello func(main.Person)}
fmt.Println(typ.MethodByName("unexportedMethod")) // { <nil> <invalid Value> 0} false
}
```


从上面例子可以看到，我们可以使用NumField、Field、NumMethod、Method和MethodByName等方法获取结构体的字段信息和方法信息。其中，Field方法返回的是StructField类型的值，包含了字段的名称、类型、标签等信息；Method方法返回的是Method类型的值，包含了方法的名称、类型和函数值等信息。

不过要注意：**通过Type可以得到结构体中非导出字段的信息(如上面示例中的gender)，但无法获取结构体类型的非导出方法信息(如上面示例中的unexportedMethod)**。

#### 2.1.4 channel类型

channel是Go特有的类型，channel与切片很像，它的类型信息包括元素类型、chan读写特性，但channel的长度与容量与channel变量是绑定的，看下面示例：

```
package main
import (
"fmt"
"reflect"
)
func main() {
ch := make(chan<- int, 10)
ch <- 1
ch <- 2
typ := reflect.TypeOf(ch)
fmt.Println(typ.Kind()) // chan
fmt.Println(typ.Elem()) // int
fmt.Println(typ.ChanDir()) // chan<-
fmt.Println(reflect.ValueOf(ch).Len()) // 2
fmt.Println(reflect.ValueOf(ch).Cap()) // 10
}
```


基于反射和channel可以实现一些高级操作，比如之前写过一篇[《使用反射操作channel》](https://tonybai.com/2022/11/15/using-reflect-to-manipulate-channels)，大家可以移步看看。

#### 2.1.5 map类型

map是go常用的内置的复合类型，它是一个无序键值对的集合，通过反射可以获取其键和值的类型信息：

```
package main
import (
"fmt"
"reflect"
)
func main() {
m := map[string]int{"a": 1, "b": 2, "c": 3}
typ := reflect.TypeOf(m)
fmt.Println(typ.Kind()) // map
fmt.Println(typ.Key()) // string
fmt.Println(typ.Elem()) // int
fmt.Println(reflect.ValueOf(m).Len()) // 3
}
```


我们看到，和切片一样，map变量的长度信息是与map变量的Value绑定的，另外要注意：**map变量不能获取容量信息**。

### 2.2 指针类型

指针类型是一个大类，通过Type可以获得指针的kind和其指向的变量的类型信息：

```
package main
import (
"fmt"
"reflect"
)
func main() {
i := 10
p := &i
typ := reflect.TypeOf(p)
fmt.Println(typ.Kind()) // ptr
fmt.Println(typ.Elem()) // int
}
```


### 2.3 接口类型

接口即契约。在Go中非作为约束的接口类型本质就是一个方法集合，通过reflect.Type可以获得接口类型的这些信息：

```
package main
import (
"fmt"
"reflect"
)
type Animal interface {
Speak() string
}
type Cat struct{}
func (c Cat) Speak() string {
return "Meow"
}
func main() {
var a Animal = Cat{}
typ := reflect.TypeOf(a)
fmt.Println(typ.Kind()) // struct
fmt.Println(typ.NumMethod()) // 1
fmt.Println(typ.Method(0).Name) // Speak
fmt.Println(typ.Method(0).Type) // func(main.Cat) string
}
```


### 2.4 函数类型

函数在Go中是一等公民，我们可以将其像普通int类型那样去使用，传参、赋值、做返回值都是ok的。下面是通过Type获取函数类型信息的示例：

```
package main
import (
"fmt"
"reflect"
)
func foo(a, b int, c *int) (int, bool) {
*c = a + b
return *c, true
}
func main() {
typ := reflect.TypeOf(foo)
fmt.Println(typ.Kind()) // func
fmt.Println(typ.NumIn()) // 3
fmt.Println(typ.In(0), typ.In(1), typ.In(2)) // int int *int
fmt.Println(typ.NumOut()) // 2
fmt.Println(typ.Out(0)) // int
fmt.Println(typ.Out(1)) // bool
}
```


我们看到和其他类型不同，函数支持NumOut、NumIn、Out等方法。其中In是输出参数的集合，Out则是返回值参数的集合。

注：上述示例foo纯粹为了演示，不要计较其合理性问题。


## 3. 获取与修改值信息

掌握了如何在反射世界获取一个变量的类型信息后，我们再来看看如何在反射世界获取并修改一个变量的值信息。之前在[《使用reflect包在反射世界里读写各类型变量》](https://tonybai.com/2021/04/19/variable-operation-using-reflection-in-go)一文中详细讲解了使用reflect读写变量的值信息，大家可以移步那篇文章阅读。

注：并不是所有变量都可以修改值的，可以使用Value的CanSet方法判断值是否可以设置。


## 4. 调用函数与方法

通过反射我们可以在反射世界调用函数，也可以调用特定类型的变量的方法。

下面是一个通过reflect.Value调用函数的简单例子：

```
package main
import (
"fmt"
"reflect"
)
func add(a, b int) int {
return a + b
}
func main() {
// 获取函数类型变量
val := reflect.ValueOf(add)
// 准备函数参数
args := []reflect.Value{reflect.ValueOf(1), reflect.ValueOf(2)}
// 调用函数
result := val.Call(args)
fmt.Println(result[0].Int()) // 输出：3
}
```


从示例看到，我们通过Value的Call方法来调用函数add。add有两个入参，我们不能直接传入int类型，**因为这是在反射世界**，我们要用反射世界的“专用参数”，即ValueOf后的值。Call的结果就是反射世界的返回值的Value形式，通过Value.Int方法可以还原反射世界的Value为int。

注：通过reflect.Type无法调用函数和方法。


方法的调用与函数调用类似，下面是一个例子：

```
import (
"fmt"
"reflect"
)
type Rectangle struct {
Width float64
Height float64
}
func (r Rectangle) Area(factor float64) float64 {
return r.Width * r.Height * factor
}
func main() {
r := Rectangle{Width: 10, Height: 5}
val := reflect.ValueOf(r)
method := val.MethodByName("Area")
args := []reflect.Value{reflect.ValueOf(1.5)}
result := method.Call(args)
fmt.Println(result[0].Float()) // 输出：75
}
```


通过MethodByName获取反射世界的method value，然后同样是通过Call方法实现方法Area的调用。

注：reflect目前不支持对非导出方法的调用。


## 5. 动态创建类型实例

reflect更为强大的功能是可以在运行时动态创建各种类型的实例。下面是在反射世界动态创建各种类型实例的示例。

### 5.1 基本类型

下面以int、float64和string为例演示一下如何通过reflect在运行时动态创建基本类型的实例。

- 创建int类型实例

```
func main() {
val := reflect.New(reflect.TypeOf(0))
val.Elem().SetInt(42)
fmt.Println(val.Elem().Int()) // 输出：42
}
```


- 创建float64类型实例

```
func main() {
val := reflect.New(reflect.TypeOf(0.0))
val.Elem().SetFloat(3.14)
fmt.Println(val.Elem().Float()) // 输出：3.14
}
```


- 创建string类型实例

```
func main() {
val := reflect.New(reflect.TypeOf(""))
val.Elem().SetString("hello")
fmt.Println(val.Elem().String()) // 输出：hello
}
```


更为复杂的类型的实例，我们继续往下看。

### 5.2 数组类型

使用reflect在运行时创建一个[3]int类型的数组实例，并设置数组实例各个元素的值：

```
func main() {
typ := reflect.ArrayOf(3, reflect.TypeOf(0))
val := reflect.New(typ)
arr := val.Elem()
arr.Index(0).SetInt(1)
arr.Index(1).SetInt(2)
arr.Index(2).SetInt(3)
fmt.Println(arr.Interface()) // 输出：[1 2 3]
arr1, ok := arr.Interface().([3]int)
if !ok {
fmt.Println("not a [3]int")
return
}
fmt.Println(arr1) // [1 2 3]
}
```


### 5.3 切片类型

使用reflect在运行时创建一个[]int类型的切片实例，并设置切片实例中各个元素的值：

```
func main() {
typ := reflect.SliceOf(reflect.TypeOf(0)) // 切片元素类型
val := reflect.MakeSlice(typ, 3, 3) // 动态创建切片实例
val.Index(0).SetInt(1)
val.Index(1).SetInt(2)
val.Index(2).SetInt(3)
fmt.Println(val.Interface()) // 输出：[1 2 3]
sl, ok := val.Interface().([]int)
if !ok {
fmt.Println("sl is not a []int")
return
}
fmt.Println(sl) // [1 2 3]
}
```


### 5.4 map类型

使用reflect在运行时创建一个map[string]int类型的实例，并设置map实例中键值对：

```
func main() {
typ := reflect.MapOf(reflect.TypeOf(""), reflect.TypeOf(0))
val := reflect.MakeMap(typ)
key1 := reflect.ValueOf("one")
value1 := reflect.ValueOf(1)
key2 := reflect.ValueOf("two")
value2 := reflect.ValueOf(2)
val.SetMapIndex(key1, value1)
val.SetMapIndex(key2, value2)
fmt.Println(val.Interface()) // 输出：map[one:1 two:2]
m, ok := val.Interface().(map[string]int)
if !ok {
fmt.Println("m is not a map[string]int")
return
}
fmt.Println(m)
}
```


### 5.5 channel类型

使用reflect在运行时创建一个chan int类型的实例，并从该channel实例接收数据:

```
func main() {
typ := reflect.ChanOf(reflect.BothDir, reflect.TypeOf(0))
val := reflect.MakeChan(typ, 0)
go func() {
val.Send(reflect.ValueOf(42))
}()
ch, ok := val.Interface().(chan int)
if !ok {
fmt.Println("ch is not a chan int")
return
}
fmt.Println(<-ch) // 42
}
```


### 5.6 结构体类型

使用reflect在运行时创建一个struct类型的实例，并设置该实例的字段值并调用该实例的方法：

```
type Person struct {
Name string
Age int
}
func (p Person) Greet() {
fmt.Printf("Hello, my name is %s and I am %d years old\n", p.Name, p.Age)
}
func (p Person) SayHello(name string) {
fmt.Printf("Hello, %s! My name is %s\n", name, p.Name)
}
func main() {
typ := reflect.StructOf([]reflect.StructField{
{
Name: "Name",
Type: reflect.TypeOf(""),
},
{
Name: "Age",
Type: reflect.TypeOf(0),
},
})
ptrVal := reflect.New(typ)
val := ptrVal.Elem()
val.FieldByName("Name").SetString("Alice")
val.FieldByName("Age").SetInt(25)
person := (*Person)(ptrVal.UnsafePointer())
person.Greet() // 输出：Hello, my name is Alice and I am 25 years old
person.SayHello("Bob") // 输出：Hello, Bob! My name is Alice
}
```


我们看到：上面代码在反射世界中动态创建了一个带有两个字段Name和Age的struct类型，注意该struct类型与Person并非同一个类型，但他们的**内存结构是一致的**。这就是上面代码尾部基于反射世界创建出的匿名struct显式转换为Person类型后能正常工作的原因。

注：目前reflect不支持在运行时为动态创建的结构体类型添加新方法。


### 5.7 指针类型

使用reflect在运行时创建一个指针类型的实例，并通过指针设置其指向内存对象的值：

```
type Person struct {
Name string
Age int
}
func main() {
typ := reflect.PtrTo(reflect.TypeOf(Person{}))
val := reflect.New(typ.Elem())
val.Elem().FieldByName("Name").SetString("Alice")
val.Elem().FieldByName("Age").SetInt(25)
person := val.Interface().(*Person)
fmt.Println(person.Name) // 输出：Alice
fmt.Println(person.Age) // 输出：25
}
```


## 5. 反射的使用场景

结合结构体标签，Go反射在实际开发中常用于以下两个场景中：

- 序列化和反序列化

这是我们最熟悉的场景。

反射机制可以用于将数据结构序列化成二进制或文本格式，或者将序列化后的数据反序列化成原始数据结构。比如标准库的encoding/json包、xml包、gob包等就是使用反射机制实现的。

- 实现ORM框架

反射机制可以用于在ORM（对象关系映射）中动态创建和修改对象，使得ORM能够根据数据库表结构自动创建对应的Go语言结构体。

注：我的

[Go语言精进之路]一书关于Go反射的讲解中，有一个基于Go对象生成sql语句的例子。

当然reflect的应用不局限在上述场景中，凡是需要在运行时了解类型信息、值信息的都可以尝试使用reflect来实现，比如：编写可以处理多种类型的通用函数(可以用interface{}以及泛型替代)、利用通过reflect.Type.Kind的信息在代码中做类型断言、根据reflect得到的类型信息做代码自动生成等。

下面是一个利用reflect手动解析json的示例，我们来看一下：

## 6. 利用reflect手解json的例子

请注意：这不是一个可复用的完善的json解析代码，仅仅是为了演示而用。


例子代码如下：

```
package main
import (
"fmt"
"reflect"
"strings"
)
type Person struct {
Name string
Age int
IsStudent bool
}
func main() {
jsonStr := `{
"name": "John Doe",
"age": 30,
"isStudent": false
}`
person := Person{}
parseJSONToStruct(jsonStr, &person)
fmt.Printf("%+v\n", person)
}
func parseJSONToStruct(jsonStr string, v interface{}) {
jsonLines := strings.Split(jsonStr, "\n")
rv := reflect.ValueOf(v).Elem()
for _, line := range jsonLines {
line = strings.TrimSpace(line)
if strings.HasPrefix(line, "{") || strings.HasPrefix(line, "}") {
continue
}
parts := strings.SplitN(line, ":", 2)
key := strings.TrimSpace(strings.Trim(parts[0], `"`))
value := strings.TrimSpace(strings.Trim(parts[1], ","))
// Find the corresponding field in the struct
field := rv.FieldByNameFunc(func(fieldName string) bool {
return strings.EqualFold(fieldName, key)
})
if field.IsValid() {
switch field.Kind() {
case reflect.String:
field.SetString(strings.Trim(value, `"`))
case reflect.Int:
intValue, _ := strconv.Atoi(value)
field.SetInt(int64(intValue))
case reflect.Bool:
boolValue := strings.ToLower(value) == "true"
field.SetBool(boolValue)
}
}
}
}
```


这段代码不是很难理解。

parseJSONToStruct函数首先将JSON字符串按行拆分，然后使用反射机制，获取v所对应的结构体的值，并将其保存在rv变量中。

接下来，函数遍历JSON字符串的每一行，如果该行以{或}开头，则直接跳过。否则，将该行按冒号:拆分成两部分，一部分是键（key），一部分是值（value）。

然后，函数使用反射机制，查找结构体中与该键对应的字段。这里使用了FieldByNameFunc方法，传入一个匿名函数作为参数，用于根据字段名查找对应的字段。如果找到了对应的字段，就根据该字段的类型，将值赋给该字段。这里支持了三种类型的字段：字符串、整数和布尔值。

最终，函数会将解析后的结果保存在v中，由于v是一个空接口类型的变量，实际上保存的是对应结构体的值的指针。所以在函数外部使用v时，需要将其转换为对应的结构体类型。

## 6. Go反射的不足

Go反射的优点在于它可以帮助我们实现更灵活和可扩展的程序设计。但是，Go反射也存在一些缺陷和局限性。其中，最主要的问题是性能。使用反射可能会导致程序性能下降，因为反射需要进行类型检查和动态分派，进出反射世界也需要额外的内存分配和装箱和拆箱操作。在编写高性能的Go程序时，应尽量避免使用反射机制。

此外，使用反射的代码可读性也相对较差，因为反射代码通常比较复杂和冗长。

## 7. 小结

Go反射是一种强大和灵活的机制，可以帮助我们实现运行时的类型和值信息获取、值操作、方法/函数调用以及动态创建类型实例，本文涵盖了所有这些操作的方法，希望能给大家带去帮助。

本文中涉及的代码可以在[这里](https://github.com/bigwhite/experiments/blob/master/reflect-guide)下载。

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