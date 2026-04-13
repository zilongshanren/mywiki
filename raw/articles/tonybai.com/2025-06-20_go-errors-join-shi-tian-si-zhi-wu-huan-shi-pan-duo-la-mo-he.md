---
title: Go errors.Join：是“天赐之物”还是“潘多拉魔盒”？——深入错误聚合的适用场景与最佳实践
url: https://tonybai.com/2025/06/20/about-errors-join/
published: '2025-06-20'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# Go errors.Join：是“天赐之物”还是“潘多拉魔盒”？——深入错误聚合的适用场景与最佳实践

![](../../assets/1e36d7fb3789fbda.png)


[本文永久链接](https://tonybai.com/2025/06/20/about-errors-join) – https://tonybai.com/2025/06/20/about-errors-join

大家好，我是Tony Bai。

错误处理，无疑是软件开发中永恒的核心议题之一。Go 语言以其独特的、显式的错误处理机制（即 error 作为普通值返回）而著称，这种设计强调了对错误的关注和及时处理。自 [Go 1.13 引入错误包装 (wrapping) 机制](https://tonybai.com/2023/05/14/a-guide-of-using-go-error-chain/)以来，Go 的错误处理能力得到了显著增强。而在[Go 1.20 版本](https://tonybai.com/2023/02/08/some-changes-in-go-1-20)中，标准库 errors 包更是带来了一个备受关注的新成员：errors.Join() 函数。

这个函数允许我们将多个 error 值合并成一个单一的 error 值，并且合并后的错误依然可以通过 errors.Is 和 errors.As 进行检查。一时间，社区中对其评价不一：有人称之为“天赐之物”，认为它在特定场景下能极大提升代码表达力和用户体验；也有人持审慎态度，强调应坚守“快速失败 (Fail Fast)”的原则，避免滥用错误聚合。

那么，errors.Join() 究竟是解决特定痛点的“良药”，还是可能被误用的“潘多拉魔盒”？它与 Go 一贯倡导的错误处理哲学是相辅相成，还是有所背离？今天，我们就结合社区的讨论，深入探讨 errors.Join() 的适用场景、潜在风险以及最佳实践。

## errors.Join()：是社区呼声的产物，还是多此一举？

在社区讨论中，有开发者盛赞 errors.Join()，认为它“在需要一次性检查多个不相关错误，或者创建类似伪堆栈跟踪结构以追踪错误传播路径的场景下，是天赐之物，非常棒！”

然而，一些资深 Go 开发者则给出了更审慎的观点：“请不要鼓吹无条件地聚合错误。遵循‘最小惊奇原则’，绝大多数情况下应该在遇到第一个错误时就‘快速失败’。合并错误的场景虽然存在，但合法地罕见。鼓励大家在假设需要合并错误之前，先思考 API 边界及其错误契约。”

这两种截然不同的看法，恰恰反映了 errors.Join() 在实践中可能带来的困惑和需要权衡的场景。

## errors.Join() 的“高光时刻”：何时它真的是“天赐之物”？

尽管“快速失败”是处理错误的主流且通常是正确的策略，但在某些特定场景下，聚合多个错误信息并一次性返回，确实能带来显著的收益。社区讨论中，开发者们也分享了他们认为 errors.Join() 非常适用的场景：

### 输入验证 (Input Validation)：一次性告知所有“罪状”

这是被提及最多的场景。当处理用户输入（如表单提交）或 API 请求参数校验时，如果每次只返回第一个发现的校验错误，用户就不得不反复提交、逐个修改，体验极差。此时，将所有校验不通过的字段错误聚合起来，一次性反馈给用户，无疑是更友好的做法。

```
// https://go.dev/play/p/pK6cVq9exkL
package main
import (
"errors"
"fmt"
"strings"
)
type UserRequest struct {
Username string
Email string
Password string
}
func validateRequest(req UserRequest) error {
var errs []error
if len(req.Username) < 3 {
errs = append(errs, errors.New("用户名长度不能小于3个字符"))
}
if !strings.Contains(req.Email, "@") {
errs = append(errs, errors.New("邮箱格式不正确"))
}
if len(req.Password) < 6 {
errs = append(errs, errors.New("密码长度不能小于6个字符"))
}
// 使用 errors.Join 合并所有验证错误
// errors.Join 会自动忽略 nil 错误
return errors.Join(errs...)
}
func main() {
req1 := UserRequest{"us", "email", "pass"}
if err := validateRequest(req1); err != nil {
fmt.Printf("请求1校验失败:\n%v\n", err)
// 调用方可以通过 errors.Is 或 errors.As 进一步检查具体错误类型
// 例如，如果错误是自定义类型，可以 errors.As(err, &targetErr)
}
req2 := UserRequest{"myuser", "myemail@example.com", "mypassword"}
if err := validateRequest(req2); err != nil {
fmt.Printf("请求2校验失败:\n%v\n", err)
} else {
fmt.Println("请求2校验通过！")
}
}
```


运行该示例的输出如下（对于请求1）：

```
请求1校验失败:
用户名长度不能小于3个字符
邮箱格式不正确
密码长度不能小于6个字符
```


### 并行任务的错误聚合：一个都不能少

当启动多个 goroutine 执行并行操作时（例如，并发请求多个下游服务、并行处理一批数据），如果只关心第一个发生的错误，可能会丢失其他并行任务中同样重要的错误信息。此时，等待所有任务完成，收集所有可能发生的错误，并用 errors.Join() 合并，能提供更全面的错误视图。

```
// https://go.dev/play/p/ZtAm2-Agyo1
package main
import (
"errors"
"fmt"
"sync"
"time"
)
func processAsyncTask(id int, fail bool) error {
fmt.Printf("任务 %d 开始...\n", id)
time.Sleep(time.Duration(id*50) * time.Millisecond) // 模拟不同耗时
if fail {
fmt.Printf("任务 %d 失败！\n", id)
return fmt.Errorf("任务 %d 执行失败", id)
}
fmt.Printf("任务 %d 完成。\n", id)
return nil
}
func main() {
tasks := []bool{false, true, false, true, false} // 任务是否失败的标志
var wg sync.WaitGroup
errs := make([]error, len(tasks)) // 用于收集每个任务的错误
for i, failFlag := range tasks {
wg.Add(1)
go func(idx int, fail bool) {
defer wg.Done()
errs[idx] = processAsyncTask(idx+1, fail)
}(i, failFlag)
}
wg.Wait()
// 使用 errors.Join 合并所有任务的错误
// errors.Join 会自动过滤掉结果为 nil 的 errs[idx]
combinedErr := errors.Join(errs...)
if combinedErr != nil {
fmt.Printf("\n并行任务执行完毕，发生以下错误:\n%v\n", combinedErr)
} else {
fmt.Println("\n所有并行任务执行成功！")
}
}
```


运行上述代码示例，我们将得到：

```
任务 5 开始...
任务 4 开始...
任务 1 开始...
任务 2 开始...
任务 3 开始...
任务 1 完成。
任务 2 失败！
任务 3 完成。
任务 4 失败！
任务 5 完成。
并行任务执行完毕，发生以下错误:
任务 2 执行失败
任务 4 执行失败
```


### defer 中的错误处理：确保信息不丢失

在函数中，defer 语句常用于执行清理操作，如关闭文件、释放锁等。这些清理操作本身也可能返回错误。如果函数主体也返回了错误，我们就面临如何处理这两个（或多个）错误的问题。简单地忽略 defer 中的错误或用它覆盖主体错误都可能导致重要信息的丢失。errors.Join() 提供了一种优雅的方式来合并它们。

```
//https://go.dev/play/p/ccKUkWXMbuN
package main
import (
"errors"
"fmt"
"os"
)
func writeFileAndClose(filename string, data []byte) (err error) {
f, err := os.Create(filename)
if err != nil {
return fmt.Errorf("创建文件失败: %w", err)
}
defer func() {
// 在 defer 中调用 Close，并将其错误与函数可能已有的错误合并
closeErr := f.Close()
if closeErr != nil {
fmt.Printf("关闭文件 %s 时发生错误: %v\n", filename, closeErr)
}
// 使用 errors.Join 合并主体错误和 defer 中的错误
// 如果 err 为 nil，Join 的行为是返回 closeErr
// 如果 closeErr 为 nil，Join 的行为是返回 err
// 如果两者都非 nil，则合并
err = errors.Join(err, closeErr)
}()
_, err = f.Write(data)
if err != nil {
// 为了能被 defer 中的 Join 合并，需要将错误赋值给命名返回值 err
err = fmt.Errorf("写入文件失败: %w", err)
return // defer 会在这里执行
}
// 模拟写入成功，但关闭失败的场景
// 或者写入失败，关闭也失败的场景
return nil // 如果写入成功，defer 仍会执行关闭并可能 Join 错误
}
func main() {
// 场景1: 写入成功，关闭成功 (假设)
// (为了演示，我们不实际创建文件，避免权限问题)
fmt.Println("测试场景：写入和关闭都成功 (理想情况)")
// err := writeFileAndClose("good.txt", []byte("hello"))
// fmt.Printf("结果: %v\n\n", err) // 应为 nil
// 场景2: 模拟写入失败 (err 非 nil)，关闭也可能失败 (closeErr 非 nil)
// 为了触发写入失败，我们可以尝试写入一个只读文件或无效路径
// 为了触发关闭失败，这比较难模拟，但 errors.Join 能处理这种情况
// 这里我们直接在函数逻辑中模拟这种情况
badWriteFunc := func() (err error) { // 使用命名返回值
fmt.Println("测试场景：写入失败，关闭也失败")
// 模拟写入失败
mainWriteErr := errors.New("模拟写入操作失败")
err = mainWriteErr // 赋值给命名返回值
defer func() {
simulatedCloseErr := errors.New("模拟关闭操作也失败")
fmt.Printf("关闭时发生错误: %v\n", simulatedCloseErr)
err = errors.Join(err, simulatedCloseErr) // 合并
}()
return // 返回 mainWriteErr，然后 defer 执行
}
errCombined := badWriteFunc()
if errCombined != nil {
fmt.Printf("组合错误:\n%v\n", errCombined)
// 我们可以检查这两个错误是否都存在
if errors.Is(errCombined, errors.New("模拟写入操作失败")) {
fmt.Println("包含：模拟写入操作失败")
}
if errors.Is(errCombined, errors.New("模拟关闭操作也失败")) {
fmt.Println("包含：模拟关闭操作也失败")
}
}
}
```


运行该示例：

```
测试场景：写入和关闭都成功 (理想情况)
测试场景：写入失败，关闭也失败
关闭时发生错误: 模拟关闭操作也失败
组合错误:
模拟写入操作失败
模拟关闭操作也失败
```


## “快速失败 (Fail Fast)”的黄金法则：为何它依然重要？

尽管 errors.Join() 在上述场景中表现出色，但我们不能忘记 Go 错误处理的一个核心原则——**快速失败。** 一些资深开发者在社区讨论中反复强调了这一点。

“快速失败”意味着：

- 一旦发生错误，应尽快中止当前操作。
- 将错误向上传播给调用者，由调用者决定如何处理。
- 避免在错误状态下继续执行，这可能导致更严重的问题或产生难以追踪的“幽灵Bug”。

在绝大多数情况下，“快速失败”是更简单、更可预测、更易于调试的错误处理策略。它符合“最小惊奇原则”，让代码的行为更符合直觉。

## API 边界与错误契约：思考在“Join”之前

有开发者还提出的另一个关键点是：“在假设你需要合并错误之前，先思考你的 API 边界及其错误契约。”

一个设计良好的 API 应该清晰地告知调用者：

- 它可能返回哪些类型的错误？
- 在什么情况下会返回错误？
- 调用者应该如何响应这些错误？

如果一个 API 的职责是单一且明确的，那么通常情况下，它在遇到第一个无法自行处理的错误时就应该返回，而不是试图收集所有可能的内部错误再“打包”抛给调用者。过度使用 errors.Join() 向上层传递大量不相关的细粒度错误，可能会让调用者无所适从，造成信息噪音，反而违背了 Go 错误处理的明确性原则。

## 何时应该对 errors.Join() 说“不”？

结合上述讨论，以下是一些不建议或需要谨慎使用 errors.Join() 的场景：

- 错误之间存在明确的因果或依赖关系：此时应优先处理或报告最根本的错误。
- 简单的“快速失败”就能满足需求：不要为了“聚合”而聚合，增加不必要的复杂性。
- API 边界清晰，且期望调用者处理单一主要错误：向调用者返回一堆它不关心或无法有效处理的内部错误，通常不是好的 API 设计。
- 可能导致信息过载或掩盖核心问题：合并后的错误信息如果过于冗长或杂乱，反而不利于快速定位问题。

## errors.Join() vs fmt.Errorf 包装多个错误：Go 1.20 的双重献礼

值得注意的是，在 Go 1.20 版本中，除了引入 errors.Join() 函数外，fmt.Errorf 的 %w 动词也得到了增强，**现在它支持同时包装多个错误**。这为我们组合错误信息提供了另一种选择。那么，这两者在使用和行为上有什么区别呢？

### 过滤 nil 错误的能力

- errors.Join(errs…) 会自动忽略 errs 切片中的 nil 错误。如果所有传入的错误都是 nil，则 errors.Join 返回 nil。
- fmt.Errorf 使用 %w 时，如果被包装的 err 是 nil，它仍然会生成一个非 nil 的错误（包含 nil 的字符串表示），除非所有 %w 对应的错误都是 nil 且格式化字符串本身在没有这些错误时会产生空错误。

我们来看一个例子：

```
// https://go.dev/play/p/X6aAjE0LdsY
package main
import (
"errors"
"fmt"
)
func main() {
var err1 = errors.New("错误1")
var err2 error // nil error
var err3 = errors.New("错误3")
// 使用 errors.Join
joinedErr := errors.Join(err1, err2, err3)
fmt.Printf("errors.Join 结果:\n%v\n\n", joinedErr)
// 输出会包含 err1 和 err3，err2 (nil) 会被忽略
// 使用 fmt.Errorf 包装多个错误
// 注意：如果 err2 是 nil，"%w" 会输出 "<nil>"
wrappedErr := fmt.Errorf("组合错误: 第一个: %w, 第二个(nil): %w, 第三个: %w", err1, err2, err3)
fmt.Printf("fmt.Errorf 结果:\n%v\n\n", wrappedErr)
// 演示 errors.Is 对两者的行为
fmt.Printf("errors.Is(joinedErr, err1): %t\n", errors.Is(joinedErr, err1)) // true
fmt.Printf("errors.Is(joinedErr, err2): %t\n", errors.Is(joinedErr, err2)) // false (因为 err2 是 nil 且被忽略)
fmt.Printf("errors.Is(joinedErr, err3): %t\n", errors.Is(joinedErr, err3)) // true
fmt.Printf("errors.Is(wrappedErr, err1): %t\n", errors.Is(wrappedErr, err1)) // true
// 对于 fmt.Errorf，如果被包装的 err 是 nil，errors.Is 无法通过 %w 找到它
fmt.Printf("errors.Is(wrappedErr, err2): %t\n", errors.Is(wrappedErr, err2)) // false
fmt.Printf("errors.Is(wrappedErr, err3): %t\n", errors.Is(wrappedErr, err3)) // true
// 如果所有错误都是 nil
var nilErr1, nilErr2 error
joinedNil := errors.Join(nilErr1, nilErr2)
fmt.Printf("errors.Join(nil, nil) is nil: %t\n", joinedNil == nil) // true
// fmt.Errorf 在所有 %w 都为 nil 时，如果格式化字符串本身为空，则可能返回 nil
// 但通常会包含格式化字符串本身，所以不为 nil
wrappedAllNil := fmt.Errorf("错误: %w, %w", nilErr1, nilErr2)
fmt.Printf("fmt.Errorf(\"错误: %%w, %%w\", nil, nil) is nil: %t\n", wrappedAllNil == nil) // false
}
```


运行示例输出如下结果：

```
errors.Join 结果:
错误1
错误3
fmt.Errorf 结果:
组合错误: 第一个: 错误1, 第二个(nil): %!w(<nil>), 第三个: 错误3
errors.Is(joinedErr, err1): true
errors.Is(joinedErr, err2): false
errors.Is(joinedErr, err3): true
errors.Is(wrappedErr, err1): true
errors.Is(wrappedErr, err2): false
errors.Is(wrappedErr, err3): true
errors.Join(nil, nil) is nil: true
fmt.Errorf("错误: %w, %w", nil, nil) is nil: false
```


### 解包 (Unwrapping) 多个错误的能力

- errors.Join 返回的错误类型（如果是非 nil 的）必然实现了 interface{ Unwrap() []error } 接口。这允许调用者获取一个包含所有被合并的非 nil 原始错误的切片，从而可以对每一个原始错误进行独立的检查。
- fmt.Errorf 通过多个 %w 包装错误时，它仍然是构建一个
**错误链 (error chain)**。这意味着错误是一层一层包装的，解包时需要多次调用 errors.Unwrap 来逐个访问。它不直接提供一次性获取所有被包装错误的方法。

```
// https://go.dev/play/p/8Zb2mvSFlFw
package main
import (
"errors"
"fmt"
)
type specialError struct {
msg string
}
func (e *specialError) Error() string {
return e.msg
}
func main() {
errA := errors.New("错误A")
errB := &specialError{"特殊错误B"}
errC := errors.New("错误C")
// 使用 errors.Join
joined := errors.Join(errA, errB, errC)
fmt.Println("使用 errors.Join 解包:")
if unwrap, ok := joined.(interface{ Unwrap() []error }); ok {
originalErrors := unwrap.Unwrap()
for i, e := range originalErrors {
fmt.Printf(" 原始错误 %d: %v (类型: %T)\n", i+1, e, e)
// 可以用 errors.As 检查特定类型
var se *specialError
if errors.As(e, &se) {
fmt.Printf(" 检测到 specialError: %s\n", se.msg)
}
}
}
fmt.Println()
// 使用 fmt.Errorf 包装多个错误
wrapped := fmt.Errorf("外层错误: (第一个: %w), (第二个: %w), (第三个: %w)", errA, errB, errC)
// 实际的错误链结构取决于 %w 的顺序和格式化字符串
// 例如，这里更像是 errA 被 wrapped 包裹，errB 被包裹 errA 的错误包裹，以此类推（具体取决于实现）
// 或者，它们可能被视为并列地被一个包含描述文字的错误所包裹。
// 为了清晰，我们假设一种简单的线性包裹（虽然内部实现可能更复杂，但 errors.Unwrap 行为类似）
fmt.Println("使用 fmt.Errorf 解包 (逐层):")
currentErr := wrapped
i := 1
for currentErr != nil {
fmt.Printf(" 解包层级 %d: %v (类型: %T)\n", i, currentErr, currentErr)
var se *specialError
if errors.As(currentErr, &se) { // 检查当前错误或其链中的错误
fmt.Printf(" 在链中检测到 specialError: %s\n", se.msg)
}
// errors.Is 也可以用于检查链中的特定错误实例
if errors.Is(currentErr, errA) {
fmt.Println(" 在链中检测到 错误A")
}
unwrapped := errors.Unwrap(currentErr)
if unwrapped == currentErr || i > 5 { // 防止无限循环或过多层级
break
}
currentErr = unwrapped
i++
}
}
```


运行该示例，我们将得到预期的输出：

```
使用 errors.Join 解包:
原始错误 1: 错误A (类型: *errors.errorString)
原始错误 2: 特殊错误B (类型: *main.specialError)
检测到 specialError: 特殊错误B
原始错误 3: 错误C (类型: *errors.errorString)
使用 fmt.Errorf 解包 (逐层):
解包层级 1: 外层错误: (第一个: 错误A), (第二个: 特殊错误B), (第三个: 错误C) (类型: *fmt.wrapErrors)
在链中检测到 specialError: 特殊错误B
在链中检测到 错误A
```


结合上述两个示例，我们可以看到：

- 如果你需要将多个独立的错误
**视为一个集合**，并希望轻松地**忽略其中的 nil 值**，同时方便地**一次性访问所有非 nil 的原始错误**，那么 errors.Join() 是更直接和语义化的选择。 - 如果你更倾向于传统的
**错误链**结构，通过错误包装来添加上下文信息，并且可以接受逐层解包，或者你的主要目的是在错误信息中包含多个原始错误的文本表示，那么 fmt.Errorf 配合多个 %w 也是可行的。

Go 1.20 同时提供这两种能力，让开发者在处理多个错误时有了更灵活的选择。理解它们的细微差别，有助于我们根据具体场景做出最合适的决策。

## 小结

Go 1.20 引入的 errors.Join() 无疑为 Go 语言的错误处理工具箱增添了一件强大的新工具。它在特定场景下——如输入验证、并行任务错误收集、defer 中的多错误处理——能够显著提升代码的表达力和用户体验，使得我们能够向调用者或用户提供更全面、更友好的错误信息。

然而，正如社区的讨论所揭示的，它并非“银弹”，更不应被滥用以取代“快速失败”这一久经考验的错误处理黄金法则。**理解 errors.Join() 的适用边界，审慎评估其在具体场景下的收益与成本（如可能带来的信息过载或对 API 错误契约的破坏），是每一位 Gopher 都需要具备的判断力。**

最终，优雅的错误处理，在于清晰、明确、以及在“最小惊奇”与“详尽信息”之间找到那个恰到好处的平衡点。errors.Join() 为我们实现这种平衡提供了一种新的可能性。

**社区讨论帖**：https://www.reddit.com/r/golang/comments/1ldyywj/use_errorsjoin/

**聊一聊，也帮个忙：**

**在你的 Go 项目中，你遇到过哪些适合使用 errors.Join() 的场景？或者，你认为哪些场景下应该坚决避免使用它？****除了文中提到的，你对 Go 语言的错误处理机制还有哪些独到的见解或最佳实践？****你认为“快速失败”和“错误聚合”这两种策略，在设计 API 时应该如何权衡？**

欢迎在**评论区**留下你的经验、思考和问题。如果你觉得这篇文章对你有帮助，也请**转发给你身边的 Gopher 朋友们**，让更多人参与到关于 Go 错误处理的深度讨论中来！

**精进有道，更上层楼**

[极客时间《Go语言进阶课》上架刚好一个月](https://mp.weixin.qq.com/s/GWGWTfCRCsOJ_4Pk-pxpHA)，受到了各位读者的热烈欢迎和反馈。在这里感谢大家的支持。目前我们已经完成了课程模块一『语法强化篇』的 13 讲，为你系统突破 Go 语言的语法认知瓶颈，打下坚实基础。

现在，我们已经进入模块二『设计先行篇』，这不仅包括 API 设计，更涵盖了项目布局、包设计、并发设计、接口设计、错误处理设计等构建高质量 Go 代码的关键要素。

这门进阶课程，是我多年 Go 实战经验和深度思考的结晶，旨在帮助你突破瓶颈，从“会用 Go”迈向“精通 Go”，真正驾驭 Go 语言，编写出更优雅、更高效、更可靠的生产级代码！

扫描下方二维码，立即开启你的 Go 语言进阶之旅！

![](../../assets/32b03e4c457f472e.gif)


商务合作方式：撰稿、出书、培训、在线课程、合伙创业、咨询、广告合作。如有需求，请扫描下方公众号二维码，与我私信联系。

![](../../assets/769fc94e8bba6b65.png)


© 2025, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

## 评论