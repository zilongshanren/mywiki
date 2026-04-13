---
title: Improving Floating-Point Precision in C# - Alan Zucconi
url: https://www.alanzucconi.com/2020/08/03/improving-floating-point/
author: Alan Zucconi
published: '2020-08-03'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial continues the journey to understand floating-point arithmetic, and how to improve the precision of modern programming language types.

At the end of this article, you will find a link to download a simple C# library that provides a new type which improves the precision of traditional `float`

and `double`

variables.

## Introduction

In the previous part of this tutorial, we have introduced the concept of **floating-point arithmetic**. As the de-facto standard to represent real numbers in modern programming languages, understanding where and why floating-point arithmetic fail is very important if you want to master Computer Science.

The main issue arises from the fact that real numbers (which are potentially unbounded) need to be stored in a finite amount of memory. Floating-point representation allows to store small numbers very precisely, or large numbers with very low precision. Generally speaking, you cannot have both.

Libraries that allow performing computation without any rounding error do exist, but they tend to be fairly slow. This is mostly because most processors have built-in operations to perform floating-point arithmetic, at a speed that cannot be matched by any other software technique.

### Beyond Floating-Points in C#…

A good compromise that is often used is to use multiple floating-point numbers to store an even larger number. In this article, we will highlight how to exactly this, by using one number for the integer part, and another one number for the decimal one.

The idea is simple: any number ![Rendered by QuickLaTeX.com x \in \mathbb{R}](../../assets/79e276be982b74c6.png)

*integer* and its *fractional* parts, which we will call ![Rendered by QuickLaTeX.com I](../../assets/c2ab42bcab55cee7.png)

![Rendered by QuickLaTeX.com F](../../assets/43336663814e94d2.png)


(1) ![Rendered by QuickLaTeX.com \begin{equation*} x = I + F$$ \end{equation*}](../../assets/192de3d986dfc08a.png)


where:

(2) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align} I & = \left [ x \right ] \\ F & = \left \{ x \right \} \end{align} \end{equation*}](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8d0e6d0f39949da4d2ce7f739420c970_l3.png)


This can be easily implemented in C# using a `struct`

:

public struct Quad { public double I; public decimal F; }

In the snipped above, the integer part is defined as `double`

, while the fractional as `decimal`

. This is because `decimal`

s are designed to have a higher precision compared to `double`

s (which is why they are often used for financial transactions).

We can also easily create a constructor that converts any existing `double`

into a `Quad`

:

public Quad (double d) { double i = Math.Truncate(d); I = i; F = (decimal) (d - i); }

The cast to `decimal`

is necessary; `decimal`

s have higher precision compared to `float`

s, but they can store smaller numbers overall. In this case, the case is technically safe, since we are only interested in the decimal part of the expression.

To make this a “proper” new type, we should ensure that it can be used pretty much as other floating-point types can. This means:

- Performing implicit and explicit casts to and from other floating-point types:

// Implicit casts (safe) Quad qi = 1; // Quad from int Quad qf = 1f; // Quad from float Quad qd = 1; // Quad from double Quad qm = 1m; // Quad from decimal // Explicit casts (unsafe) Quad q; float f = (float) q; // Quad to float double d = (double) q; // Quad to double decimal m = (decimal) q; // Quad to decimal

- Performing all of the basic operations (addition, subtraction, multiplication, division, …) via their respective operators (
`+`

,`-`

,`/`

,`*`

, …):

Quad a = 1; Quad b = 2; Quad c = a+b;

- Supporting comparison and equality operators:

Quad a = 1; Quad b = 2; bool b = a > b;

### Casts to and from other types

To make the `Quad`

type more usable, it is important that it can be used pretty much as all of the other floating-point types can. This means being able to implicitly cast other types to `Quad`

—whenever it is safe to do so—, and forcing an explicit cast to convert a `Quad`

into a smaller type.

This is very easy in C#, thanks to the `implicit operator`

keyword:

public static implicit operator Quad(double a) { return new Quad(a); }

The method above is called every time a `double`

is assigned to a `Quad`

. As the name suggests, the cast happens *implicitly*, meaning that this method is behind called to construct a `Quad`

from a `double`

.

We can use a slightly different variant of this method to do the opposite: constructing a `double`

from a `Quad`

. This can be done with the `explicit operator`

keyword, which requires an explicit cast to the destination type.

public static explicit operator double (Quad a) { return a.I + (double) a.F; }

C# typically requires explicit casting every time an assignment could potentially cause a loss of precision (like in this case).

The implementation for the other four operators is omitted from the article, but is included in the library you can download at the end of the page.

### Operator Overloads

The next step is to make sure that `Quad`

variables support all basic operations. Let’s start with implementing the *addition*. C# allows defining how the `+`

operator should work when used with two `Quad`

s variables, through a feature called *operator overloading*:

public static Quad operator+ (Quad a, Quad b) { ... }

What is now needed is to write the code to add two `Quad`

variables.

As previously discussed, adding numbers that are wildly different in range can lead to floating-point errors. The safest and simplest option here is summing up two `Quad`

s components by components:

public static Quad operator+ (Quad a, Quad b) { Quad c; c.I = a.I + b.I; c.F = a.F + b.F; return c; }

This works, but leads to a problem: the fractional part can potentially go above one. For instance, if ![Rendered by QuickLaTeX.com a=1.5](../../assets/2a4f9d24dfcc8c40.png)

![Rendered by QuickLaTeX.com b=0.5](../../assets/aa9dde96e3b126f7.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


While summing two integers is guaranteed to produce another integer, that is not necessarily the case for fractions. When that occurs, we need to carry the integer remainder from the fractional part to the integer one.

We can take care of this with a method that re-normalises the `Quad`

:

public void Normalise() { if (Math.Abs(F) < 1m) return; decimal i = Math.Truncate(F); F -= i; I += (double) i; }

If we ensure that `Normalise`

is called before `operator+`

returns, we have successfully implemented addition between two `Quad`

variables.

### Comparisons

Another important feature is to ensure that `Quad`

variables can be compared to each other. In C# this can be done by implementing the `IComparable<Quad>`

interface.

The snippet implements the CompareTo method from the `IComparable<Quad>`

interface, by relying on the `CompareTo`

methods of the integer and fractional parts. By specification, in fact, `CompareTo`

must return 0 if two numbers are equal.

public int CompareTo(Quad other) { int c = I.CompareTo(other.I); if (c != 0) return c; return F.CompareTo(other.F); }

It is good practice to also overload the `>`

, `<`

, `>=`

and `<=`

operators, as seen in the [IComparable<T> interface](https://docs.microsoft.com/en-us/dotnet/api/system.icomparable-1?view=netcore-3.1) page on the .NET documentation:

public static bool operator > (Quad a, Quad b) { return a.CompareTo(b) == +1; } public static bool operator < (Quad a, Quad b) { return a.CompareTo(b) == -1; }

Even though we have only implemented comparison between two `Quad`

variables, we are able to perform comparisons with other floating-point types as well. This is because we have instructed the compiler that `float`

s and `double`

s can be implicitly cast to `Quad`

s.

### Equality Test

Another step that needs to be taken is to make sure we can use `==`

to check whether or not two `Quad`

s are the same. Like before, this can be done by overloading the `==`

operator, and by implementing the `IEquetable<Quad>`

interface.

However, this is not *strictly* necessary. By default, using the `==`

operator with two structs of the same type in C# has the behaviour of comparing all of their fields. This is doing through reflection, which can be quite slow. So it is always best to re-implement a more efficient version by hand:

public bool Equals(Quad other) { return I.Equals(other.I) && F.Equals(other.F) ; }

Overloading the `==`

operator also requires to overload `!=`

. And it is good practice to also override the `Equals`

method inherited from the `Object`

class.

When `Equals`

is changed, you should also override the `GetHashCode`

, which is used by many .NET libraries such as `Dictionary`

and `HashSet`

.

This leads to the rather unpleasant situation where, for something as simple as the `Quad`

type, you end up having to add at least ten (TEN!) methods just to get comparisons and equality to work properly.

### Trigonometric Functions

At the beginning of this article, we justified the need for a more precise floating-point variable with the example of a gravity simulator. If we really are to use `Quad`

variables in a simulator of that kind, we do need a way to handle trigonometric functions.

To get the sine of a Quad, we could simply do this:

Quad q; Quad s = Math.sin(q);

However, this is basically killing the precision we so spent so much time preserving. A better way would be to calculate the sine on the integer and fractional parts separately, and then to join them later. This is a good ideal, but is not as straightforward as it might sound. The reason is simple: trigonometric functions are not linear. In fact, the sine of the sum is not the sum of the sines; quite the opposite:

(3) ![Rendered by QuickLaTeX.com \begin{equation*} \begin{align} \sin\left(I+F\right) & = \sin\left(I\right) \cos\left(F\right) &+ \cos\left(I\right) \sin\left(F\right) \\ \cos\left(I+F\right) & = \cos\left(I\right) \sin\left(F\right) &- \sin\left(I\right) \sin\left(F\right) \end{align} \end{equation*}](../../assets/47485d9dc9c27fab.png)


The sine function can be implemented like this:

public Quad Sin() { Quad sinI = new Quad(Math.Sin(I)); Quad cosI = new Quad(Math.Cos(I)); double sinF = Math.Sin((double) F); // no Math.Sin for decimal double cosF = Math.Cos((double) F); // no Math.Cos for decimal return sinI * cosF + cosI * sinF; }

There are a few drawbacks, however. First, the lack of trigonometric functions that operate on `decimal`

variables. Currently, the `Math`

library can only handle `double`

s.

## Conclusion & Download

This post concludes the two-part tutorial on floating-point arithmetic in C#.

You can download the C# `Quad`

library on [Patreon](https://www.patreon.com/posts/39965604). It is available fully compatible with Unity.

## Leave a Reply Cancel reply