---
title: Function Pointers vs Member Function Pointers | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2012/04/function-pointers-vs-member-function-pointers/
author: Allen Chou
published: '2012-04-08'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

My second semester at [DigiPen](http://www.digipen.edu/) has almost come to an end. For the project of this semester, we are required to write our code in strict C, no fancy C++ stuff like generics and polymorphism. In order to get around this limitation, our team used a technique described in [this post](http://www.cjcat.net/2012/01/object-oriented-structures-in-c/) to mimic object-orientation in C.

I’m planning on starting building our team’s new game engine early in this summer to prepare for the upcoming fall semester. This time, of course, we’re allowed to write code in C++.

The first thing I’m planning on building is the event system, which is basically a framework with event dispatchers and event listener functions. But things turned out to be more complicated than I thought. In ActionScript, Java, and C#, the only functions we can define are strictly member functions, functions that are defined in a class body. Even the “main” function is simply the constructor of a document class or a public static void function inside a class. So we don’t have to worry about whether an event listener function is a member function or not.

In C++, however, not everything is object-oriented. A function can be an ordinary function defined in global scope or a member function defined in a class (or struct) body. The invocation to both types of functions are different, so we cannot treat them as equal: we cannot assign them to the same type of function pointer. But I want to treat them equally, so that I can register ordinary functions and member functions of the same signature to the same event dispatcher. This leads me to the research of [function delegates](http://en.wikipedia.org/wiki/Delegation_pattern).

For now, I’m just going to discuss the fundamental difference between ordinary functions and member functions. I’m also going to point out the difference between function pointers versus member function pointers.


### Function Pointers

Functions are actual pieces of reusable code in the program, so every function has its address, which is the starting point of the function in memory. Given the function below:

void printSomething(int x) { std::cout << x << std::endl; }

We can assign the address of this function to a function pointer with matching function signature called `fp`

:

void (*fp) (int) = &printSomething;

And then we can indirectly invoke the function through the syntax below:

*fp(10);

Say we have an event dispatcher class (some people might prefer to call it a signal) that dispatches an event with an integer information:

class Dispatcher { private: std::list<void (*) (int)> listeners_; public: void addListener(void (*listener) (int)) { listeners_.push_back(listener); } void dispatch(int value) { //loop through all listeners std::list<void (*) (int>::iteartor iter; for ( iter = listeners_.begin(); iter != listeners_.end(); ++iter ) { //invoke listener with the given event information *(*iter)(value); } } };

We can add multiple listener functions to the dispatch, and then the dispatch of an event would invoke all listener functions.

Dispatcher *dispatcher = new Dispatcher(); //assume f1, f2, and f3 all have the correct signature dispatcher->addListener(&f1); dispatcher->addListener(&f2); dispatcher->addListener(&f3);

Now if we have a class that defines a member function with the same signature:

class MyClass { private: int data_; public: MyClass(int data):data_(data) { } void printSomething(int x) { //The "this" keyword here is not necessary, //but I put it here for later convenience. std::cout << (x + this->data_) << std::endl; } };

It’s tempting to write the following code if you’ve been working with ActionScript or Java:

MyClass *obj = new MyClass(10); dispatcher->addListener(&obj->printSomething);

But it won’t work, because there’s a huge difference between the invocation of functions and member functions.

### Function Invocations

Suppose we call the global version of the function `printSomething(int)`

like this:

printSomething(10);

The function stack would look somewhat like this:

10;

Only the argument 10 that is passed in that is on the stack.

However, have you ever thought about how a member function gets the address value for the `this`

keyword, given that each member function has only one exact copy that lies somewhere in the memory, unlike a data member that has one copy per class instance? The value for the `this`

keyword is implicitly passed to the member function upon invocation.

Since there’s only one copy of each member function per class, we refer to a member function like this:

MyClass:printSomething;

The following member function invocation actually passes the address of `obj`

along with the other integer argument to the function.

//obj is the "callee" obj->printSomething(10);

So while the program counter is in the function, the stack looks somewhat like this (the order may vary depending on compiler implementation):

0xABCD (address of "callee"); 10 (argument passed in);

And the member function now knows what value to use for the `this`

keyword.

That’s the difference between the invocation of an ordinary function and a member function: a callee must be provided.

### Member Function Pointers

The syntax for invoking a member function through a member function pointer is a bit convoluted. First, to declare a member function pointer, you have to specify the function signature along with which class the member function belongs to. The following code declares a member function pointer of class `MyClass`

that points to a member function that returns void and takes in one integer argument, named `mfp`

:

void (MyClass::*mfp) (int);

The following code assigns the `MyClass::printSomething(int)`

member function address to the pointer:

mfp = &MyClass::printSomething;

And here’s the convoluted part. In order to invoke the function, you have to provide a “callee” object whose address is to be used as the value of the `this`

keyword in the member function. We do that by specifying the “callee” object and invoke the member function through the [member access operator](http://en.wikibooks.org/wiki/C%2B%2B_Programming/Operators/Operator_Overloading#Member_access_operators) “`->*`

“:

(obj->*mfp)(10);

### What’s Next?

Clearly, `void (*) (int)`

and `void (MyClass::*) (int)`

are different types and cannot be mixed together in the `Dispatcher`

class shown above. To make things worse, if a member function of the same signature is defined in another class `MyOtherClass`

, its type is `void (MyOtherClass::*) (int)`

and cannot be used interchangeable with `void (MyClass::*) (int)`

.

To treat functions and member functions from different classes that all have the same signature equally, we have to use a more advanced technique called [function delegates](http://en.wikipedia.org/wiki/Delegation_pattern). This is a topic that I am still researching by reading [this post](http://www.codeproject.com/Articles/7150/Member-Function-Pointers-and-the-Fastest-Possible), and I would post more about delegates once I have come up with something worth sharing.

Pingback: cocos2d-x委托模式 | 子龙山人

Pingback: Easy C++ Delegates | Ming-Lun "Allen" Chou

If you’re using Visual Studio 2010 (or later), you can use std::bind and std::function in the functional header. They come from the new C++11 Standard Library (and before that, from Boost) but they were implemented early in VS2010.

std::bind will create a std::function based on the parameters you pass to it. You can bind to a method or a function and you will get the same type (Also note that the type of a lambda expression is a std::function.) You can then implement a very generic Dispatcher or Signal class with std::function as your listener type.

The only gotcha is that if you bind the same function or method twice, you can’t compare the resulting functor unlike function object in ActionScript. So if you want to remove a listener, you need to keep std::function pointers or refs in your Dispatcher class and keep the result of your bind call somewhere (ex. as a member) so you can remove it later. This is a bit annoying so if you find something better, let me know.

Here’s a basic implementation : http://pastebin.com/UvMM2hQs

I think we’re not going to use the new features introduced in C++11 next semester, so std::bind is most likely not an feasible option for us. Still, thanks for the information, I’ll be sure to check it out when I have time 🙂

As for that basic implementation, that was actually my initial attempt to build a signal, and it turned out a single signal object like that cannot have listeners with the same signature that are a mixture of ordinary functions and member functions of different classes, the reasons explained in this post.

I’m currently researching the approach employed in this article, which allows users to bind ordinary functions and member functions of different classes of the same signature equally using delegates, and they are comparable.