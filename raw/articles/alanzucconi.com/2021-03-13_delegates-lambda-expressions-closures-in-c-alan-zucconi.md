---
title: Delegates, Lambda Expressions & Closures in C# - Alan Zucconi
url: https://www.alanzucconi.com/2021/03/13/delegates-lambda-closures/
author: Alan Zucconi
published: '2021-03-13'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

If you are familiar with programming, you might have heard of a specific paradigm called **functional programming**. Most modern languages, such as Java and C#, have integrated some functional elements over time. Other, like Scala and Haskell, were built around that very idea of functional programming.

This online course will look at some of the functional features available in C# 3.0, including the concept of **anonymous functions**, **delegates** and **lambda expressions**. But before doing that, we need to understand what *functional programming* actually means.

If you are interested, keep reading, and we will explore the following topics:

- Anonymous functions
- Delegates
- Anonymous delegates
- Multicast delegates
- Lambda expressions
- Lambda statements
- Expression-body members
- Expression trees
- Local functions
- Closures

In a traditional, imperative piece of code, you might use variables to store the values of earlier computations. These variables typically contain two things: either a *primitive* type (an integer number, a floating point number, a boolean value, …) or a *reference* to an object (a class that has been instantiated using the keyword `new`

).

The first novelty that comes with functional programming is that variables can also contain (references to) functions. Assigning functions to variables allows passing them as parameters to other functions, and even to be returned. C# is said to treat functions as [first-class citizens](https://en.wikipedia.org/wiki/First-class_function), because it gives them the same privileges that all other variables have. Namely, you should be able to:

- pass functions as arguments to other functions,
- return functions as the values from other functions,
- assigning them to variables.

C# has been extending its support for functions programming for years. While massive improvements have been made since its first version, you should expect a somehow confusing syntax often worsen by the strong limitations imposed by the compiler.

# Referencing Methods

In C# all variables have a type. For instance, `int x`

is a variable called x which can contain an integer number. The same applies to functions: if functions can be stored into a variable, what kind of *type* do we need?

Let’s start with an easy example. Let’s imagine a simple function that takes no parameters and has no return value.

void F () { Debug.Log("Hello Function!"); }

While `F()`

invokes the function (meaning that the code it contains is being executed), the expression `F`

represents a reference to the function. We can use a function name to refer to it. Since functions are first-class citizens in C#, this means that there is a way to assign `F`

to a variable. In this particular case, a variable that can hold `F`

can have `System.Action`

type:

Action a = F;

`Action`

is not a keyword of C#, but rather a type introduced by .NET. It represents the type of a function with no parameters or return type.

Now that the variable `a`

contains a reference to `F`

, we can invoke it by simply treating `a`

itself as a function: `a()`

.

## Delegates

C# has the concept of **delegate**, which is a way to describe the type of a method. `Action`

, for instance, is a built-in delegate defined inside .NET that represents all functions with no parameters or return type. Such delegate can be defined like this:

delegate void Action ();

Basically, it works by adding the keyword `delegate`

before the template signature of all functions we want to be able to reference. The name used—`Action`

, in this case—becomes the name of the delegate and, consequently, the name a new type that can be used to reference void functions with no parameters.

It is important to notice that delegates are a *type definition*s, not *variable declarations*. So, in the same way you cannot define a new enum type inside a method, you cannot define a new delegate type inside a method either.

namespace TestNameSpace { delegate void TestDelegate1 (); // ✔️ Defined in a namespace public class TestClass { public delegate void TestDelegate2 (); // ✔️ Defined inside a class public void Start () { delegate void TestDelegate3 (); // ❌ Defined inside a method } } }

Below, a more complex example that shows a delegate (called `IntTest`

) for all functions that are taking one integer and returning a boolean:

delegate bool IntTest (int x);

When specifying input parameters, delegates need to give an actual name to each one. Those names are not binding, meaning that you can match any method which takes an integer as a parameter, regardless of its name.

### Built-in Delegates

In C#, there are several built-in delegates that you can use. They cover the majority of cases, so that you do not have to create new delegates every time. `Action`

, for instance, is one such delegate. But there is also a generic variant that matches methods with one parameter and no return type, called `Action<T>`

:

void F (int x) { ... } void G (float x) { ... } void Start () { Action<int> di = F; Action<float> df = G; }

.NET includes 16 generic variants of `Action`

, so that you use them to match void functions with up to 16 parameters. If you need more (do you???) you will need to create a new custom delegate.

.NET also includes generic delegates for functions which have a return type. `Func<TResult>`

, for instance, represents a function with no parameters with return type `TResult`

. And, as it happened for `Action`

, there are 16 other variants to support input parameters, in the form of `Func<T1, T2, ..., TResult>`

.

There are also `Predicate`

and `Predicate<T1, T2, ...>`

which are used for boolean functions.

`Action`

`Action<T1, ...>`

`Func<TResult>`

`Func<T1, ..., TResult>`

`Predicate`

`Predicate<T1, ...>`


But there are many other used for specific purposes, such as event handling and thread synchronisation.

## Lambda Expressions

C# 3.0 introduced a new syntax to create anonymous methods, which are very handy in many scenarios. This feature is referred to as **lambda expression**, and it get its name from a concept known in programming as **lambda**. Based on the context and language, lambdas are also known as (or strongly related to) *anonymous functions*, *blocks* or *closures*.

Effectively, lambdas are a more expressive way to define a function, and are specifically designed to work well in the context of functional programming. This means that lambdas are often used to pass code as parameters to other functions.

Lambdas are effectively methods, and so they can be assigned to any delegate which matches their signature. So let’s see an example of how to initialise an `Action`

delegate in three different ways:

void Start () { // ✔️ Method → Delegate Action a0 = F; // ✔️ Anonymous delegate → Delegate Action a1 = delegate () { Debug.Log("Hello World!"); } // ✔️ Lambda → Delegate Action a2 = () => Debug.Log("Hello World!"); } void F () { Debug.Log("Hello World!"); }

All of the three methods above are equivalent: the `Action`

delegate will contain a reference to a method which prints the `"Hello World!"`

string to the console. However, the third one is undoubtedly the most compact.

What really defined the lambda function is the **lambda operator**, `=>`

(which is also known as **hashrocket operator** in Ruby) and it supposed to be read as “*goes to*“. So, the lambda expression `x => x+1`

should be read as “`x`

goes to `x+1`

“. You can read more about this on the relative [=> operator (C# reference page](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-operator)).

Their anatomies can be tricky to grasp at first. The first two round brackets contain a list of the input parameters. Unlike a delegate, they only include *names*, and not *types*. This is because the type of a lambda expression is automatically inferred by its context.

### Statement Lambdas

On top of *expression* lambdas, the C# notation also supports **statement lambdas**. These are a way to create anonymous functions which need more than a single expression. They work in a very similar way, but the *expression* part is replaced with the more traditional body of a function, including the curly brackets and `return`

keyword (if needed).

// Lambda expression Func<int, int> a = x => x + 1; // Lambda statement Func<int, int> a = x => { return x + 1; };

## Scope and Closures

**Closures** are one of those topics that—along *monads* and other functional-related terms—is often poorly explained or misunderstood. Understanding what closures are in C# and why they are important …is important!

We can think of lambdas—and anonymous functions in general—as pieces of code that we can define and call. It is very common for a lambda to have all of its necessary data passed as a parameter. A typical example is `x => x+1`

, which takes one parameter and it only operates on that parameter alone. Understanding and implementing those kind of lambdas is *easy*.

Generally speaking, the code of most lambda expressions can be “stored” by the compiled inside a private methods. This works well for both the “self-contained” lambdas. But what happens when the lambdas are trying to access something that is outside their scope?

The answer, unsurprisingly, depends on *what* exactly they are trying to access. The easiest case is when a lambda is referencing a member of the same class.

The example below (check on [ShaderLab.io](https://sharplab.io/#v2:CYLg1APgAgTAjAWAFBQMwAJboMLIN7LpGYYCWAdgC7oAe6AvOgAwDchx7RamALOgLLoAFAEpO6AkmLTMcGOgCGAY0qkA9uQbCRDAHwTaW1ugC+bKcRPITQA=)) shows a simple lambda that sets a public member of its class to zero. If we look at the generated C# code through a decompiled, we will see that the lambda has simply been “converted” to a private method (renamed `ResetMethod`

for clarity):

// Original code public class C { public int x = 0; public void Start () { Action action = () => { x = 0; }; } } // Compiled (with variables renamed for clarity) public class C { public int x = 0; public void Start() { Action action = ResetMethod; } private void ResetMethod() { x = 0; } }

This works even if the lambda is invoked from another class. The original instance will not be garbage collected until all references to the lambdas are released.

### Closures

Things get more complicated when a lambda accesses a variable inside the scope of the function in which it is defined. What makes this case much more complicated is the fact that the lambda could be potentially invoked when the function (along its stack) has already ended. This means that the variables it needs to access might have been already destroyed.

To ensure that the lambda stays “callable”, the variables it is accessing must somehow survive the end of the function in which they are defined. C# already provides a mechanism to do this: classes! This means that when a lambda accesses a variable defined inside a function, that variable (along with the lambda code) gets extracted and placed in a newly created class by the compiler. This is what a *closure* is.

You can see the original code, and its compiled version, below (check on [SharpLab.io](https://sharplab.io/#v2:CYLg1APgAgTAjAWAFBQMwAJboMLIN7LpGYZQAs6AsugBQCUhxBSxr6AlgHYAu6AHugC86AAwBuRm3SS2UODHQBDAMbd2Ae05DadIQD50eftvHoAvhJbEzyM0A===)):

// Original public class C { public void Start () { int x = 0; Action action = () => { x = 0; }; } } // Compiled (with variables renamed for clarity) public class C { private sealed class Closure { public int x; internal void ResetMethod() { x = 0; } } public void Start() { // Instantiates the closure Closure closure = new Closure(); closure.x = 0; // Assigns the delegate Action action = Closure.ResetMethod; } }

The class `Closure`

provides the environment necessary to run the lambda code safely (i.e.: the variable `x`

, now “upgraded” to a class member). In the Computer Science literature, `x`

is also referred to as a **free variable**, and it is said to be **captured**.

If you are interested to learn about closures in C#, [A Simple Explanation of C# Closures](https://www.simplethread.com/c-closures-explained/) is a comprehensive and accessible read.

### Implementation

To better understand how anonymous functions work, it is helpful to see how lambdas and delegates are actually compiled. There are many online tools that can show you compiled C# code, including [SharpLab.io](https://sharplab.io/#v2:CYLg1APgAgTAjAWAFBQMwAJboMLIN7LpGYZQAs6AsgBQCUhxBSxLmcM6AhgMYAuAlgHsAdugC86OuIB86POn7De6YQFcAtuPQAGANzoAvvvQMiB5AaA=). The code below shows how a simple lambda expression gets compiled (variable names have been changed for clarity):

// Original public class C { public void Start () { Action action = () => { Debug.Log("Hello World!"); }; } } // Compiled (with variables renamed for clarity) public class C { [Serializable] private sealed class Lambda { public static readonly Lambda Singleton = new Lambda(); public static Action HelloWorldDelegate; internal void HelloWorldMethod { Debug.Log("Hello World!"); } } public void Start () { // Instantiates the delegate (if it has not done before) if (Lambda.HelloWorldDelegate == null) Lambda.HelloWorldDelegate = Lambda.Singleton.HelloWorld; // Assigns the delegate Action action = Lambda.HelloWorldDelegate; } }

The lambda `() => { Debug.Log("Hello World"); }`

becomes the method (called `HelloWorldMethod`

) of a new class (called `Lambda`

) which is generated by the compiler (the exact same thing would happen if we had used an anonymous delegate instead). Yes: anonymous function in C# are actually methods of a new class created *ex novo* by the compiler.

It is interesting to see that for this to work, an instance of `Lambda`

(referenced in the static member called `Singleton`

) must be created. When used in this way, anonymous functions do cause memory allocation.

If other delegates or lambdas are to be created in the same class, each one will all become a different members of the compiler-generated `Lambda`

class.

## Conclusion

This articles provided a general introduction to the concept of functional programming in C#, exploring the following constructs:

- Anonymous functions
- Delegates
- Anonymous delegates
- Multicast delegates
- Lambda expressions
- Lambda statements
- Expression-body members
- Expression trees
- Local functions
- Closures

There is so much more that could be say about functional programming in C#! Future posts will explore some of the most commonly used patterns in functional programming, including a deep dive into one of C#’s most loved/hated extension: LINQ.

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

If you think this article helped you, please, consider supporting me on [Patreon](https://www.patreon.com/AlanZucconi).

Thank you! 🙏

## Leave a Reply Cancel reply