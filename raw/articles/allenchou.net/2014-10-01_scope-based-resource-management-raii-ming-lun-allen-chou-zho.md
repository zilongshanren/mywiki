---
title: Scope-Based Resource Management (RAII) | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2014/10/scope-based-resource-management-raii/
author: Allen Chou
published: '2014-10-01'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Programming Series](http://allenchou.net/game-programming-series/).

It has been 4 months since I graduated from [DigiPen](http://www.digipen.edu/) and started working at [Naughty Dog](http://www.naughtydog.com) as a Game Programmer. Since then, I have been too lazy to write anything big and technical on my blog, mostly because I just want to relax and play games after work. From now on, instead of dealing with topics that are wide and deep like [game physics](http://allenchou.net/game-physics-series/) and [game math](http://allenchou.net/game-math-series/), I’ll probably just write about quick and tiny tips, most likely related to game development.

I’m going to begin with the programming idiom [RAII](http://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization) (Resource Acquisition Is Initilization). I like how some people on [StackExchange](http://stackexchange.com/) refer to RAII as a more friendly name, Scope-Based Resource Management, so I will stick with this name.

Scope-Based Resource Management is a very common and important resource management technique where the resource is tied to an object’s lifetime. This is done by allocating the resource in a helper object’s constructor and releasing the resource in the helper object’s destructor.

The usefulness and importance of this technique can be best illustrated by an example.


Say, you wrote a function that acquires a [mutex](http://en.wikipedia.org/wiki/Mutual_exclusion) at the beginning and releases it at the end:

void fun(Mutex& mutex) { mutex.Acquire(); // do stuff here mutex.Release(); }

Later, you want to add an early-out in the middle of the function. Since the function isn’t too long, you’ll quickly notice that the function acquires a mutex at the beginning and releases it at the end, so you remember to release the mutex before the early-out:

void fun(Mutex& mutex) { mutex.Acquire(); // do stuff here if (earlyOut) { // whew, good thing I remember to do this mutex.Release(); return; } // do stuff here mutex.Release(); }

Now, a year has passed and the function has grown into a beast of tons of lines. Many more early-outs have been added, and you’ve always remember to release the mutex before all early-outs. Some day, someone else comes along and decides to add another early-out to the function. He might not notice the mutex acquisition and releases buried in the sea of code:

void fun(Mutex &mutex) { mutex.Acquire(); // many lines of code if (newEarlyOut) { // oops... return; } // many lines of code mutex.Release(); }

Manual resource management is commonly prone to this exact type of human error. Scope-based resource management is the perfect solution to this problem. In C++ standards, an object on the stack will always execute its constructor upon initialization and execute its destructor when the program leaves its scope. We can use this to our advantage to automate resource management. Here is our helper class for automatically acquiring and releasing a mutex:

class AutoMutexLock { public: AutoMutexLock(Mutex &mutex) : m_mutex(mutex) { m_mutex.Acquire(); } ~AutoMutexLock(void) { m_mutex.Release(); } private: Mutex &m_mutex; }

We now only have to acquire the mutex at the beginning of your function, and we no longer need to remember to release the mutex before every single function return, because the destructor of the helper class will do that for us:

void fun(Mutex &mutex) { AutoMutexLock lock(mutex); // many lines of code if (newEarlyOut) { // no need to release mutex here return; } // many lines of code if (earlyOut) { // nor here return; } // many lines of code // not at the end, either }

This technique can extend to a lot of scenarios. For instance, if you allocate memory from the heap in a function and you’d like the memory to be freed when the program exits the function, you can use the [smart pointers](http://en.wikipedia.org/wiki/Smart_pointer) in [STL](http://en.wikipedia.org/wiki/Standard_Template_Library). The following example demonstrates a bare-bone implementation of a smart pointer class:

template <typename T> class SmartPtr { public: SmartPtr(T *ptr) : m_ptr(ptr) { } ~SmartPtr(void) { delete m_ptr; } T &operator*(void) { return *m_ptr; } T *operator->(void) { return m_ptr; } private: T *m_ptr; }

And the client code may look something like:

void fun(void) { // allocate memory here SmartPointer ptr(new MyDataClass()); // many lines of code // this works because operator-> is properly overloaded ptr->DoStuff(); if (earlyOut) { // memory automatically freed here return; } // many lines of code // memory automatically freed here, too }

Here’s yet another example related to memory. It is very common for console game developers to pre-allocate all available memory on the console upon launching the game. Some would divide it into chunks identified by “memory contexts”. Say, you have a global stack of memory contexts, where the top memory context determines which chunk of pre-allocated memory will the pointer returned from the `new`

operator point into.

If you want to use a specific chuck of pre-allocated memory within the scope of a function, you can push the corresponding memory context onto the stack at the beginning of the function, and then pop it off when the program exits the function. This should sound like an awfully familiar task to you by now. Here’s our helper class:

class AutoMemoryContext { public: AutoMemoryContext(MemoryContext &context) : m_context(context) { PushMemoryContxt(context); } ~AutoMemoryContext(void) { PopMemoryContext(context); } private: MemoryContext &m_context; }

And the client code is nothing surprising:

void fun(void) { // push memory context here AutoMemoryContext autoContext(kAiMemoryContext); // many lines of code if (earlyOut) { // memory context will be automatically popped here return; } // many lines of code // memory context will be automatically popped here, too }

With scope-based resource management, you pretty much get the logic to release resource properly inserted by the compiler for free!