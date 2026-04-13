---
title: “错误即值”，不同实现：Go与Zig错误处理哲学对比
url: https://tonybai.com/2025/04/30/go-vs-zig-in-error-handling/
published: '2025-04-30'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# “错误即值”，不同实现：Go与Zig错误处理哲学对比

![](../../assets/17ac8f8d04db2a8d.jpg)


[本文永久链接](https://tonybai.com/2025/04/30/go-vs-zig-in-error-handling) – https://tonybai.com/2025/04/30/go-vs-zig-in-error-handling

大家好，我是Tony Bai。

使用Go语言有些年头的开发者，大多对其错误处理机制有着复杂的情感。一方面，我们认同 Rob Pike 所倡导的“错误即值 (Errors are values)”的核心哲学——错误不是需要特殊通道（如异常）处理的“二等公民”，它们是普通的值，可以传递、检查，甚至被编程。这赋予了错误处理极大的灵活性和明确性。

但另一方面，我们也不得不承认Go的错误处理有时可能相当**冗长**。标志性的if err != nil代码块几乎遍布在Go代码的各个角落，占据了相当大的代码比例，这常常成为社区讨论的热点。 有趣的是，近期另一门备受关注的系统编程语言 Zig，也采用了“错误即值”的哲学，但其实现方式却与Go大相径庭。

近期自称是Zig新手的packagemain.tech博主在他的一期视频中也分享了自己敏锐地观察到的Zig和Go在设计哲学上的相似性（都追求简洁、快速上手）以及在错误处理实现上的显著差异。

今天，我们就基于这位开发者的分享，来一场 Go 与 Zig 错误处理的对比，看看同一种哲学思想，是如何在两种语言中开出不同但各有千秋的花朵。

## Go 的错误处理：接口、显式检查与可编程的值

我们先快速回顾下 Go 的错误处理方式，这也是大家非常熟悉的：

### error 接口

Go中的错误本质上是实现了Error() string方法的任何类型。这是一个极其简单但强大的约定。

```
// $GOROOT/src/builtin/builtin.go
// The error built-in interface type is the conventional interface for
// representing an error condition, with the nil value representing no error.
type error interface {
Error() string
}
```


### 显式返回值

函数通过返回 (result, error) 对来表明可能出错。通常error放到函数返回值列表的最后一个，并且一个函数通常只返回一个错误值。

### 显式检查

调用者必须显式检查返回的 error 是否为 nil。

```
package main
import (
"fmt"
"os"
)
func readFileContent(filename string) (string, error) {
data, err := os.ReadFile(filename) // ReadFile returns ([]byte, error)
if err != nil {
// If an error occurs (e.g., file not found), return it
return "", fmt.Errorf("failed to read file %s: %w", filename, err) // Wrap the original error
}
return string(data), nil // Success, return data and nil error
}
func main() {
content, err := readFileContent("my_file.txt")
if err != nil {
// The iconic check
fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
// Here you would typically handle the error (log, return, etc.)
return
}
fmt.Println("File content:", content)
// Slightly shorter form for functions returning only error (like Close)
// Use dummy file creation/opening for example that runs
f, createErr := os.Create("temp_file.txt")
if createErr != nil {
fmt.Fprintf(os.Stderr, "Error creating file: %v\n", createErr)
return
}
if f != nil {
// Ensure file is closed even if writes fail later (using defer is better practice)
defer f.Close()
defer os.Remove("temp_file.txt") // Clean up the dummy file
// Example usage...
_, _ = f.WriteString("hello")
// Now explicitly check close error if needed at the end of func,
// though defer handles the call itself.
// For demonstration of the if err := ... style on Close:
// (Note: defer already schedules the close, this is just for syntax demo)
// closerFunc := func() error { return f.Close() } // Wrap Close if needed
// if err := f.Close(); err != nil { // Potential re-close if not careful with defer
// fmt.Fprintf(os.Stderr, "Error closing file: %v\n", err)
// }
// A more practical place for this pattern might be a non-deferred close.
}
}
```


示例中，对每一处返回错误的地方都做了显式检查，这保证了错误不会被轻易忽略，控制流清晰可见，但也导致了代码冗长。上面代码因my_file.txt文件不存在，会输出“Error reading file: failed to read file my_file.txt: open my_file.txt: no such file or directory”并退出。

### 错误是可编程的

**自定义错误类型**

开发者可以定义自己的 struct 实现 error 接口，从而携带更丰富的上下文信息。

```
package main
import (
"errors"
"fmt"
"os"
"time"
)
// Custom error type
type OperationError struct {
Op string
Err error // Underlying error
Timestamp time.Time
}
// Implement the error interface
func (e *OperationError) Error() string {
return fmt.Sprintf("[%s] operation %s failed: %v", e.Timestamp.Format(time.RFC3339), e.Op, e.Err)
}
// Function that might return our custom error
func performCriticalOperation() error {
// Simulate a failure
err := errors.New("connection refused")
return &OperationError{
Op: "connect_database",
Err: err,
Timestamp: time.Now(),
}
}
// (main function using this will be shown in the next point)
```


**错误检查**

标准库 errors 包提供了 errors.Is (检查错误值是否匹配特定目标) 和 errors.As (检查错误链中是否有特定类型并提取) 方法，允许对错误进行更精细的判断和处理。

```
// (Continuing from previous snippet within the same package)
func main() {
err := performCriticalOperation()
if err != nil {
fmt.Fprintf(os.Stderr, "Operation failed: %v\n", err) // Prints the formatted custom error
// Example: Check if the underlying error is a specific known error
// Note: Standard errors package doesn't export connection refused directly,
// this is conceptual. Real check might involve string matching or syscall types.
// if errors.Is(err, someSpecificNetworkError) {
// fmt.Println("It was specifically a network error")
// }
// Check if the error is of our custom type and extract it
var opErr *OperationError
if errors.As(err, &opErr) {
fmt.Fprintf(os.Stderr, " Operation details: Op=%s, Time=%s, UnderlyingErr=%v\n",
opErr.Op, opErr.Timestamp.Format(time.Kitchen), opErr.Err)
// Can now use opErr.Op, opErr.Timestamp etc. for specific handling
}
}
}
```


该博主认为，Go的方式虽然有点“乏味”和冗长，但非常**直接 (straightforward)**，且自定义错误携带**丰富上下文**的能力是一大优势，使得错误本身更具“可编程性”。

## Zig的错误处理：错误联合类型、语法糖与强制处理

Zig作为一门较新的语言(诞生于2016年)，同样推崇简洁和“无隐藏控制流”，并在错误处理上给出了不同的答案：

### 错误联合类型

Zig中可能失败的函数，其返回类型会使用!标记，形式如 !ReturnType 或 !void。这表示函数要么返回 ReturnType 类型的值，要么返回一个**错误集 (Error Set)** 中的错误值。错误本质上是一种特殊的枚举值。

```
const std = @import("std");
// Define possible errors for our function
const MyError = error{
InvalidInput,
ConnectionFailed,
SomethingElse,
};
// Function signature indicating it can return MyError or u32
fn doSomething(input: u32) MyError!u32 {
if (input == 0) {
return MyError.InvalidInput; // Return a specific error
}
if (input > 100) {
return MyError.ConnectionFailed; // Return another error
}
// Simulate success
return input * 2; // Return the successful result (u32)
}
// Example usage needs a main function
// pub fn main() !void { // Example main, !void indicates main can return error
// const result = try doSomething(50);
// std.debug.print("Result: {}\n", .{result});
// }
```


### 强制处理

在Zig 中，你不能像在 Go 中那样直接忽略一个可能返回错误值的函数的错误。Go 允许你使用空白标识符 _ 来丢弃返回值，包括错误，这在 Zig 中是不允许的，因为 Zig编译器强制要求调用者必须处理所有潜在的错误，不允许忽略。

但是，Zig 提供了几种方法来处理你不想显式处理的错误，尽管这些方法都需要你明确地承认你正在忽略错误，而不是简单地丢弃它。这个我们在下面会提及。

### 简洁的语法糖

Zig 提供了多种简洁的语法来处理错误：

#### try: 极其简洁的错误传播机制

下面代码中的**一行 try 基本等同于 Go 中三四行的 if err != nil { return err }**：

```
const std = @import("std");
const MyError = error{InvalidInput, ConnectionFailed}; // Simplified error set
// Function definition (same as above)
fn doSomething(input: u32) MyError!u32 {
if (input == 0) return MyError.InvalidInput;
if (input > 100) return MyError.ConnectionFailed;
return input * 2;
}
// This function also returns MyError or u32
fn processData(input: u32) MyError!u32 {
// If doSomething returns an error, 'try' immediately propagates
// that error from processData. Otherwise, result holds the u32 value.
const result = try doSomething(input);
// ... further processing on result ...
std.debug.print("Intermediate result in processData: {}\n", .{result});
return result + 1;
}
pub fn main() !void { // Main now can return errors (due to try)
const finalResult = try processData(50); // Propagate error from processData
std.debug.print("Final result: {}\n", .{finalResult});
// Example of triggering an error propagation
// Uncommenting the line below will cause main to return InvalidInput
// _ = try processData(0);
}
```


注：Zig中的try可不同于Java等支持try-catch等错误处理机制中的try。Zig 的 try 用于传播错误，而 Java 的 try-catch 用于捕获和处理异常。


#### catch: 用于捕获和处理错误

- 与代码块结合 (catch |err| { … })，执行错误处理逻辑

```
const std = @import("std");
const MyError = error{InvalidInput, ConnectionFailed};
fn doSomething(input: u32) MyError!u32 { /* ... */ if (input == 0) return MyError.InvalidInput; return input * 2; }
pub fn main() void { // Main does not return errors itself
const result = doSomething(0) catch |err| {
// Error occurred, execution enters the catch block
std.debug.print("Caught error: {s}\n", .{@errorName(err)}); // Prints "Caught error: InvalidInput"
// Handle the error, maybe exit or log differently
// For this example, we just print and return from main
return; // Exit main gracefully
};
// This line only executes if doSomething succeeded
// If input was non-zero, this would print.
std.debug.print("Success! Result: {}\n", .{result});
}
```


- 与回退值结合 (catch fallbackValue)，在出错时提供一个默认的成功值

```
const std = @import("std");
const MyError = error{InvalidInput, ConnectionFailed};
fn doSomething(input: u32) MyError!u32 { /* ... */ if (input == 0) return MyError.InvalidInput; return input * 2; }
pub fn main() void {
// If doSomething fails (input is 0), result will be assigned 999
const result = doSomething(0) catch 999;
std.debug.print("Result (with fallback): {}\n", .{result}); // Prints 999
const success_result = doSomething(10) catch 999;
std.debug.print("Result (with fallback, success case): {}\n", .{success_result}); // Prints 20
}
```


- 与命名块结合

label: { … } catch |err| { … break :label fallbackValue; })，既能执行错误处理逻辑，又能返回一个回退值。

```
const std = @import("std");
const MyError = error{
FileNotFound,
InvalidData,
};
fn readDataFromFile(filename: []const u8) MyError![]const u8 {
// 模拟读取文件，如果文件名是 "error.txt" 则返回错误
if (std.mem.eql(u8, filename, "error.txt")) {
return MyError.FileNotFound;
}
// 模拟读取成功
const data: []const u8 = "Some valid data";
return data;
}
fn handleReadFile(filename: []const u8) []const u8 {
return readDataFromFile(filename) catch |err| {
std.debug.print("Error reading file: {any}\n", .{err});
std.debug.print("Using default data\n", .{});
return "Default data";
};
}
pub fn main() !void {
const filename = "data.txt";
const errorFilename = "error.txt";
const data = handleReadFile(filename);
std.debug.print("Data: {s}\n", .{data});
const errorData = handleReadFile(errorFilename);
std.debug.print("Error Data: {s}\n", .{errorData});
}
```


注：对于Gopher而言，是不是开始感觉有些复杂了:)。


#### if/else catch

分别处理成功和失败的情况，else 块中还可以用 switch err 对具体的错误类型进行分支处理。

```
const std = @import("std");
const MyError = error{InvalidInput, ConnectionFailed, SomethingElse};
fn doSomething(input: u32) MyError!u32 {
if (input == 0) return MyError.InvalidInput;
if (input > 100) return MyError.ConnectionFailed;
if (input == 55) return MyError.SomethingElse; // Add another error case
return input * 2;
}
pub fn main() void {
// Test Case 1: Success
if (doSomething(10)) |successValue| {
std.debug.print("Success via if/else (input 10): {}\n", .{successValue}); // Prints 20
} else |err| { std.debug.print("Error (input 10): {s}\n", .{@errorName(err)}); }
// Test Case 2: ConnectionFailed Error
if (doSomething(101)) |successValue| {
std.debug.print("Success via if/else (input 101): {}\n", .{successValue});
} else |err| {
std.debug.print("Error via if/else (input 101): ", .{});
switch (err) {
MyError.InvalidInput => std.debug.print("Invalid Input\n", .{}),
MyError.ConnectionFailed => std.debug.print("Connection Failed\n", .{}), // This branch runs
else => std.debug.print("Unknown error\n", .{}),
}
}
// Test Case 3: SomethingElse Error (falls into else)
if (doSomething(55)) |successValue| {
std.debug.print("Success via if/else (input 55): {}\n", .{successValue});
} else |err| {
std.debug.print("Error via if/else (input 55): ", .{});
switch (err) {
MyError.InvalidInput => std.debug.print("Invalid Input\n", .{}),
MyError.ConnectionFailed => std.debug.print("Connection Failed\n", .{}),
else => std.debug.print("Unknown error ({s})\n", .{@errorName(err)}), // This branch runs
}
}
}
```


#### catch unreachable

在不期望出错或不想处理错误（如脚本中）时使用，若出错则直接 panic。

```
const std = @import("std");
// Assume this function logically should never fail based on guarantees elsewhere
fn doSomethingThatShouldNeverFail() !u32 {
// For demo, make it fail sometimes
// if (std.time.timestamp() % 2 == 0) return error.UnexpectedFailure;
return 42;
}
pub fn main() void {
// If doSomethingThatShouldNeverFail returns an error, this will panic.
// Useful when an error indicates a programming bug.
const result = doSomethingThatShouldNeverFail() catch unreachable;
std.debug.print("Result (unreachable case): {}\n", .{result});
// To see it panic, you'd need doSomethingThatShouldNeverFail to actually return an error.
}
```


该博主认为，Zig 的错误处理方式功能更丰富、更强大、也**更简洁 (concise)**。try 关键字尤其强大，极大地减少了错误传播的样板代码。

## 对比与思考：殊途同归，各有侧重

对比 Go 和 Zig 的错误处理，我们可以看到：

![](../../assets/3b42dea1f0a055c3.png)


两者都坚守了“错误即值”的阵地，避免了异常带来的隐式控制流跳转。但：

**Go 选择了更直接、更“笨拙”但上下文信息更丰富的路径。**它的冗长换来的是每一处错误检查点的明确无误，以及通过自定义类型深度编程错误的能力。**Zig 则选择了更精巧、更简洁且由编译器强制保证的路径。**它通过强大的语法糖显著减少了样板代码，提升了编写体验，但在错误本身携带上下文信息方面目前有所欠缺。

该博主最后总结道，他个人很喜欢这两种语言的实现方式（特别是与有异常的语言相比）。Zig提供了一种功能更丰富、强大且简洁的方式；而 Go 则更直接，虽冗长但易于理解，且拥有丰富的上下文错误处理能力。

## 小结

Go 与 Zig 在错误处理上的不同实现，完美诠释了语言设计中的权衡 (trade-offs)。追求极致简洁和强制性，可能会牺牲一部分灵活性或信息承载能力；追求灵活性和信息丰富度，则可能带来冗余和对开发者约定的依赖。

这场对比并非要评判孰优孰劣，而是展示“错误即值”这一共同哲学在不同设计选择下的具体实践。了解这些差异，有助于我们更深刻地理解自己所使用的语言，并在技术选型或学习新语言时做出更明智的判断。或许，Go 的未来版本可以借鉴 Zig 的某些简洁性？又或者，Zig 的生态会发展出更丰富的错误上下文传递机制？这都值得我们期待。

你更喜欢 Go 还是 Zig 的错误处理方式？为什么？欢迎在评论区留下你的看法！

**深入探讨，加入我们！**

今天讨论的 Go 与 Zig 错误处理话题，只是冰山一角。在我的知识星球 **“Go & AI 精进营”** 里，我们经常就这类关乎 Go 开发者切身利益、技术选型、生态趋势等话题进行更深入、更即时的交流和碰撞。

如果你想：

- 与我和更多资深 Gopher 一起探讨 Go 的最佳实践与挑战；
- 第一时间获取 Go 与 AI 结合的前沿资讯和实战案例；
- 提出你在学习和工作中遇到的具体问题并获得解答；

欢迎扫描下方二维码加入星球，和我们一起精进！

![img{512x368}](../../assets/46c6ee234c360d9a.jpg)


**感谢阅读！**

商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

我感觉Go的返回值最大的问题还在于他两个值是不互斥的，比如下面这段代码：

“`go

type Foo struct {

…

}

func New() (*Foo, error) {

return nil, nil

}

“`

按约定，if err != nil 理论上Foo就不为nil, 但这取决于实现者的编程素养

文章的永久地址格式变了：

实际地址 https://tonybai.com/2025/04/30/httpstonybai-com20250430go-vs-zig-in-error-handling/

文章中给的地址 https://tonybai.com/2025/04/30/go-vs-zig-in-error-handling

感谢提醒，已修正。