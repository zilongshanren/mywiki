---
title: Object-Oriented Programming Synonyms | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2012/02/object-oriented-programming-synonyms/
author: Allen Chou
published: '2012-02-16'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is written for my classmates at [DigiPen](https://www.digipen.edu/).

Most of the class have started learning object-oriented programming really for only two weeks, and the professor uses quite a few synonyms that sound really different but are actually the same things. I thought it is very confusing to many new-comers to OOP, so I felt like writing a post to clarify things up. I’ll just group synonyms of the exact same meaning together:


When class B **inherits from** class A, we can also say:

Class B **is derived from** class A.

Class B **extends** class A.

If class B **inherits from** class A, we say:

Class B is the **subclass**, and class A is the **superclass**.

Class B is the **child class**, and class A is the **parent class**.

Class B is the **derived class**, and class A is the **base class**.

When we declare a variable C in class A, we say:

C is a **data member** of A.

C is a **field** of A.

C is a **property** of A.

(As Ryan pointed out in the comment, properties in many object-oriented languages may involve implicit getters and setters)

When we declare a function D in class A, we say:

D is a **member function** of A.

D is a **method** of A.

This is pretty much what we need to know right now. I hope this post clarifies things up a little bit.

A more abstract relationship between parent & children:

– if class B inherits from class A, B “is-a” A

Between data members and owner class:

– if a variable of class C is declared in class A, A “has-a” data member C

Children derive from their parents? I thought they were just farther down a tree.

Looks good mostly.

I wouldn’t call member variables properties in c++ though. In most object oriented languages, properties have implicit setters and getters that can be full functions. Plus some implementations of c++ (I’m looking at you Microsoft) have real properties through crazy compiler intrinsics(not standard in any way).

Yeah, the properties in C# could be implicit getters and setters. Maybe the more proper name for data members is field? I just took it from Java and ActionScript, where data members are called properties (ActionScript also has implicit getter/setter feature). Thanks for pointing it out.

I like the term “property”, in that we can say “children inherits properties from their parent”. Properties in C# do mean different things than fields; as mentioned above they are automatically generated or explicitly implemented (saves the naming nonsense) getters and setters, similar to @synthesized / @property in objective C.

Allen,

Thanks a lot for these clarifications!

I also really like how you formatted this 😀

Glad you like it 🙂

I actually borrow this format from my Linear Algebra textbook, where it always groups more than 5 (sometimes even more than 10) mathematically equivalent statements together to make sure you understand every aspect of a fact. It seemed crazy at first, but later on I really appreciate such formatting, for it covers a topic very thoroughly and effectively.