---
title: 'Hardcore C++: why "this" sometimes doesn''t equal "this"'
url: http://joostdevblog.blogspot.com/2013/03/hardcore-c-why-this-sometimes-doesnt.html
author: Joost van Dongen
published: '2013-03-16'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*this*pointer can differ even though it is being used

*within the same object*.

This is a problem that one can spend a lot of time debugging on before finding out what happens. I encountered it last week, and the only reason it didn't cost me several days of debugging to figure it out, is because I ran into the exact same problem during a project at University years ago.

Let me first sketch an example of a situation in which this might occur. In some cases a unique identifier for an object is needed, but we don't actually need to do anything with that object, so it doesn't matter what type it is. In such cases, an obvious and easy solution is to simply use the address of the object itself and store it as a

*void**. This way we can, for example, register whether a call to a function is from an object that already called that function before.

Now the question is: does that always work?

Since I am writing this blogpost, the answer of course is "no". Here's why:

Let's start by looking at this simple case of inheritance:

void printPointer(void* pointer) { std::cout ‹‹ pointer ‹‹ '\n'; } class A { public: void printA() { printPointer(this); } int banana; }; class C: public A { public: void printC() { printPointer(this); } int kiwi; }; void main() { C object; object.printA(); object.printC(); } |

This code prints the

*this*-pointer twice, but from two different classes. Since this is from within the same object, basic intuition tells me it will print the same address twice. Here's what it prints:

0018FD8C

0018FD8C

Indeed, the same address twice! But what happens if we add multiple inheritance? Let's complicate the example by adding one more class and inheriting from both at the same time:

void printPointer(void* pointer) { std::cout ‹‹ pointer ‹‹ '\n'; } class A { public: void printA() { printPointer(this); } int banana; }; class B { public: void printB() { printPointer(this); } int ananas; }; class C: public A, public B { public: void printC() { printPointer(this); } int kiwi; }; void main() { C object; object.printA(); object.printB(); object.printC(); } |

This looks like we are doing pretty much the same thing as above, so the question is again: do all these calls print the same pointer? Let's have a look at what this prints:

0018FD8C

0018FD90

0018FD8C

As you can see, surprisingly, and totally against my own intuition, they do not print the same address! The call to

*printB()*prints a different, slightly higher address!

Now why is that? Surely there is something broken in C++? Or at least, that is what I thought when I first encountered this situation. There is, however, a totally reasonable explanation for this behaviour.

In memory, when using inheritance, the hierarchy of objects is simply put after each other. So these three objects look something like this:

![](../../assets/d0732d8eaa44a519.gif)

Now if we we have an object of type C and then on it a function from B, the

*this*pointer needs to point at where B actually starts in memory. It cannot point to where our C started, because the functions of B cannot have any knowledge of that they are inside a bigger object. So this is where all the pointers go:

![](../../assets/eb556bd778e96df3.gif)

The difference between 0018FD8C and 0018FD90 is exactly four bytes, which makes sense, since A only contains one integer number, which uses four bytes of memory.

So there you have it:

*this*does not always equal

*this*, even when used from inside the same object!

This curiosity in C++ is another good reason to think again on whether code structures that use

*void**are a good idea. Bugs caused by something like this are easy to overlook and terribly difficult to find. In fact, I know several good C++ programmers who were not even aware of this phenomenon. When I first encountered this at university years ago, it took me a lot of debugging and asking friends for help before I learned this was happening.

And this is not the only problem with

*void**: using it almost always means unsafe casting is somewhere near.

*Void**has its uses once in a while, but it is often avoidable. So whenever you are using a

*void**in your code, stop for a short moment to think about whether there is another solution that avoids it!

If you want you can even abuse the memory layout for memory leak detecting. For example inherting from a class which first 8 bytes are its unique identifier and then having your leak detector spew the first 8 bytes out of every leaked pointer makes you find them fairly easy :) (Note, don't use std::string, but char[])

ReplyDeleteNice trick! :) Not very practically necessary, though, since there are really good leak detectors on most platforms, that even tell you which line of code allocated the leaked memory.

Delete" I know several good C++ programmers who were not even aware of this phenomenon"


ReplyDeletelool =)

Example 1:



ReplyDeleteObject C inherits from object A, so it shares some mamory usage, especially sharing same functions

Example 2:

Object A AND B are self-supporting, hence they both recieve own memory blocks

Object C inherits block A AND B, but since A is placed first, it's sharing block A's function.

It would be memory leaking if for each class (especially inherited ones) to not have the same memory used. else (back in the day) we should've used a lot more memory to get our stuff running

Using multiple inheritance is bad pattern as it is.

ReplyDeleteNot always. There are plenty of very useful applications of multiple inheritance. For example, a Character in our engine is both "something that owns upgrades" and "something that can be damaged". Without multiple inheritance, these could not be separate groups, which is very limiting and awkward by itself. It is important to be careful around multiple inheritance, but not allowing it at all is overdoing it, in my opinion.

DeleteYou can always substitute containing with inheritance given you put in the effort to define a sharp interface what the trait offers the the owner of the trait. This enforces cleaner code but cost more development time.

DeleteNice article and lucid explanation with some good pictures.


ReplyDeleteWould like to invite you to read my post on C/C++ macros at http://www.hudku.com/blog/essential-macros-for-c-programming/ and interested to have the comments from you as well as from your readers.

Interesting read!


ReplyDeleteAnother similar WTF-causing moment in C++ is due to the fact that that the vtbl is updated multiple times during construction of an object. The parent constructors are run first and when they are run, the vtbl is setup as if that was the type of the object. Virtual methods don't work as you would think during construction! This holds for single inheritance as well! Very confusing until you realize what it happening.