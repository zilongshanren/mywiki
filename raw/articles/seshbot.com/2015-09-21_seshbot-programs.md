---
title: Seshbot Programs
url: http://seshbot.com/blog/
author: Paul Cechner
published: '2015-09-21'
source_blog: Seshbot Programs
source_site: http://seshbot.com/
category: game programming
fetched: '2026-04-13'
---

*For a more in-depth rundown on covariance and contravariance explained in terms of category theory have a look at Thomas Patricek’s blog*

Covariance and contravariance are things you’ll probably ignore until you start using generics in ernest. Then one day you’ll want to pass an enumerable to a function that takes a slightly different yet related type of enumerable and then *BAM* – you’re hit with some crazy error messages and then all of a sudden you’re up to your elbows in browser tabs of StackOverflow articles.

To cut straight to the chase, this is the problem:

1 2 |
|

Sometimes we want the OO polymorphism substitution rules (AKA Liskov’s substitution principle) to apply to generic types too. Covariance and contravariance provide us a mechanism to allow this substitution to take place.

To be more specific, [co|contra]variance are necessitated due to the interaction of two different forms of polymorphism – object inheritance and generic typing. And yet sometimes you want to combine the two – while `MyType<T>`

and `MyType<U>`

share no inheritance relationship and therefore are not substitutable for each other, sometimes you want to treat them as if they are substitutable if `T`

and `U`

are themselves related.

So a covariant or contravariant generic type (e.g., a `IEnumerable<T>`

) might be bound to other references of that type (e.g., `IEnumerable<U>`

) when there is an inheritance relationship between the two predicated types. This allows you to pass your `IEnumerable<Employee>`

to a function that actually accepts an `IEnumerable<Person>`

without the compiler complaining that they are different types.

The rule of thumb with inheritance is that if U inherits from T you could say that *U is-a-kind-of T*. With covariant and contravariant types, I like to think of them in terms of *can-be-used-as-a* relationship. To determine if `MyType`

should be covariant or contravariant you could ask if Dog is-a-kind-of Animal, is it true that MyType<Dog> can-be-used-as-a MyType<Animal>?

*Covariance* and *contravariance* are two different ways that differently specialised generic types should themselves be substitutable for each other like derived types are:

**Covariance**: `MyType<T>`

is covariant if typing `MyType<Base> x = new MyType<Derived>()`

makes sense (this looks very much like standard substitution rules.)

An example of this is an `IEnumerable`

-derived type, and is classified as having methods that *return* the predicated type, or *getters* (hence C# uses the `out`

keyword.)

The implication is that the relationship between the covariant generic types is the **same** as the relationship between their predicated types, e.g.:

1 2 3 4 5 |
|

**Contravariance**: `MyType<T>`

is contravariant if typing `MyType<Derived> x = new MyType<Base>()`

makes sense.

An example of this is the .Net generic `Action`

type, and is classified as having methods that *accept* the predicated type as a parameter, or *setters* (hence C# uses the `in`

keyword.)

Contravariant types are probably less common than covariant types, and imply that the relationship between the generic types is the **inverse** of the relationship between their predicated types. E.g.:

1 2 3 |
|

[Read on →](http://seshbot.com/blog/2015/09/21/co-and-contra-variance-made-easy/)