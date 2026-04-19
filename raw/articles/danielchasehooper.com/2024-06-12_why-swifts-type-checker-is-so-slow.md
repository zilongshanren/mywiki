---
title: Why Swift’s Type Checker Is So Slow
url: https://danielchasehooper.com/posts/why-swift-is-slow/
published: '2024-06-12'
source_blog: Daniel Hooper
source_site: https://danielchasehooper.com/
category: graphics
fetched: '2026-04-19'
---

June 12, 2024・5 minute read

The Swift compiler can take an absurdly long time to compile expressions due to how types are inferred 1. Here’s an explanation by the creator of Swift, Chris Lattner (from from his

My experience with Swift is we tried to make a really fancy bi-directional Hindley-Milner type checker and it’s really great because you can have very beautiful minimal syntax but the problem is that A) compile times are really bad (particularly if you have complicated expressions) and B) the error messages are awful because now you have a global constraint system and when something goes wrong you have to infer what happened and the user can’t know that something over there made it so something over here can’t type check. In my experience it sounds great but it doesn’t work super well.


Let me explain what he means with an example:

```
enum ThreatLevel {
case normal
case midnight
}
enum KeyTime {
case midnight
case midday
}
func setThreatLevel(_ level: ThreatLevel) {...}
func setThreatLevel(_ level: Int) {...}
setThreatLevel(.midnight)
```


On the last line, `setThreatLevel`

could refer to one of two functions, and `.midnight`

could represent `ThreatLevel.midnight`

or `KeyTime.midnight`

. The Swift compiler uses a constraint solver to find the valid combination is `setThreatLevel(_ level: ThreatLevel)`

and `ThreatLevel.midnight`

. On longer expressions with many more possible combinations the constraint solver can get bogged down. Often the [ExpressibleBy protocols](https://developer.apple.com/documentation/swift/initialization-with-literals) and operator overloading create high combination counts, like in this example:

```
let address = "127.0.0.1"
let username = "steve"
let password = "1234"
let channel = 11
let url = "http://" + username
+ ":" + password
+ "@" + address
+ "/api/" + channel
+ "/picture"
print(url)
```


Swift 6 spends *42 seconds* on these 12 lines on an M1 Pro, only to spit out the notorious `error: the compiler is unable to type-check this expression in reasonable time; try breaking up the expression into distinct sub-expressions`

. In the same amount of time, Clang can perform a clean build of my 59,000 line C project *38 times*. The Swift standard library has 17 overloads of `+`

and 9 types adopting the `ExpressibleByStringLiteral`

Protocol. This leads to an exponential combination of types and operators for the constraint solver to try. Unfortunately for the solver, I included a type error in the expression. The `+`

operator cannot add the `channel`

Int to a String literal. No matter how many combinations the solver tries, none of them resolve this error. In this case the compiler gives up before trying them all and fails to point out the type mismatch.

You can fix the problem by converting `channel`

to String:

```
let url = "http://" + username
+ ":" + password
+ "@" + address
+ "/api/" + String(channel)
+ "/picture"
```


This successfully compiles in 0.19 seconds! The constraint solver is designed to try the most likely combinations first — that strategy pays off now that the code doesn’t have an error. It is possible to write expressions that successfully compile, but take a long time:

```
let result: Double = -(1 + 1) + -(1 + 1) - 1
```


Swift 6 takes *6.2 seconds* to compile this *one* line 2. Even

The nature of constraint solvers is that they may find unexpected solutions, or have unpredictable performance. For example, appending “+ 1” to the previous example makes it compile in 0.7 seconds. Very strange. Tweaking the expression in other ways gave me the `unable to type-check this expression in reasonable time`

error.

You may have expressions in your code slowing down compile times. To find the worst offenders, run:

```
xcodebuild clean build -project \
\
OTHER_SWIFT_FLAGS="-Xfrontend -debug-time-expression-type-checking" \
| grep -Ei '^\d+\.\d+ms\t/.+$' | sort -r
```


Use temporary variables to break the slow expressions into multiple statements. In addition, it might be worth adding `-Xfrontend`

and `-warn-long-expression-type-checking=100`

to your project’s “Other swift flags” build setting to be warned when an expression takes longer than 100 milliseconds to compile.

My friends within Apple tell me that they have learned to limit expression length to try to control compile times. I’ve heard similar stories from friends at Delta Air Lines and other companies.

The Swift team is aware of the issue, and lists the following item under [known problem areas](https://github.com/apple/swift/blob/main/docs/CompilerPerformance.md#known-problem-areas):

Expression type inference solves constraints inefficiently, and can sometimes behave super-linearly or even exponentially.


Unfortunately the current approach’s exponential worst case [is unavoidable](https://learn.microsoft.com/en-us/archive/blogs/ericlippert/lambda-expressions-vs-anonymous-methods-part-five). A different approach to type checking is required to fix it. I think it’s worth considering this course of action:

To learn more about Swift’s type checker, start by reading [Type Checker Design and Implementation](https://github.com/apple/swift/blob/main/docs/TypeChecker.md). The type checker source code is located in the [swift/lib/Sema folder](https://github.com/apple/swift/tree/main/lib/Sema)

Discuss on [Twitter](https://x.com/DanielcHooper/status/1800948752754335753)

Discuss on [Hacker News](https://news.ycombinator.com/item?id=40661001)