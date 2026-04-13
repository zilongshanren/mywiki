---
title: Easy C++ Delegates | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2012/04/easy-c-delegates/
author: Allen Chou
published: '2012-04-24'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

As I mentioned in my [previous post](http://allenchou.net/2012/04/function-pointers-vs-member-function-pointers/), I was working on delegates for C++.

The [first article](http://www.codeproject.com/Articles/7150/Member-Function-Pointers-and-the-Fastest-Possible) I read was recommended by one of my programming TAs. The author’s main concern was portability and performance, so he special-cased extensively throughout his code, in order to make sure the code works perfectly fine across multiple compilers while still yielding optimal performance. This resulted in very verbose and convoluted code. I was half way through comprehending all his code and gave up. The article itself, however, is certainly worth reading; it covers in details the difference between function pointers and member pointers and points out why they are not easy (also not too hard) to deal with correctly.


The [second post](http://www.codeproject.com/Articles/11015/The-Impossibly-Fast-C-Delegates) I read was a follow-up to the first one. The code is easier to read; however, the author used macros extensively to avoid code duplication in his source files, so trying to untangle the macros in mind while reading the code is not a light task. Fortunately, the author provided a clean and “untangled” example in the post, which is just enough to understand the logic behind it.

I found the [last article](http://www.codeguru.com/cpp/cpp/cpp_mfc/pointers/article.php/c4135/DELEGATES-and-C.htm) by Googling “C++ delegates”. It is the easiest of the three (in terms of sample code), since the author’s first concern was simplicity instead of performance, and it was just what I needed. He used polymorphism to handle function pointers and member function pointers differently. His sample code helped me the most in coming up with my own delegate class design. I didn’t read through the entire article, though, because it was kind of hard for me to read.

As mentioned before, I started my research on delegates because I wanted to implement a robust event/signal system for my next school game project at [DigiPen](http://www.digipen.edu). Thus, one of my concerns was to make the code as simple as possible, so that it would be easy for me to explain how it works to my teammates.

Here I’m going to show you what I’ve come up with. In order to make things simple, I am going to show you simplified version of the delegate class, where it can only point to a function with one parameter. It can be easily generalized with templates to deal with any number of parameters once you understand it.

### The `Callback`

Class

The responsibility of the `Callback`

is to provide an interface for a delegate to invoke the underlying function, be it a regular function (static function) or a member function associated with a pointer that holds the object address to be used as the value of the `this`

pointer.

template <typename Ret, typename Param0> class Callback { public: virtual Ret invoke(Param0 param0) = 0; };

The `Ret`

type is the return type of the function, and the `Param0`

type is the type of the one parameter passed to the function. We are going to extend this class and create two subclasses, one is responsible for static function callbacks, and one responsible for member function callbacks.

### The `StaticFucntionCallback`

Class

Static function callbacks are easy to implement, where all you have to do is declare an appropriate function pointer, and invoke it using the function pointer invocation syntax.

template <typename Ret, typename Param0> class StaticFunctionCallback : public Callback<Ret, Param0> { private: Ret (*func_)(Param0); public: StaticFunctionCallback(Ret (*func)(Param0)) : func_(func) {} virtual Ret invoke(Param0 param0) { return (*func_)(param0); } };

### The `MethodCallback`

Class

Member function (method) callbacks require just a little more work, where we have to keep track of which object address to use for the `this`

pointer while invoking the method.

template <typename Ret, typename Param0, typename T, typename Method> class MethodCallback : public Callback<Ret, Param0> { private: void *object_; Method method_; public: MethodCallback(void *object, Method method) : object_(object) , method_(method) {} virtual Ret invoke(Param0 param0) { T *obj = static_cast<T *>(object_); return (obj->*method_)(param0); } };

Note that I used the template type `Method`

to handle all possible member function types. It is not type-safe; I could have used some non-type template parameter like `Ret (T::*method)(Param0)`

and take extra care of it, just as in the aforementioned articles. However, my goal here is to make things simple, so I just use a regular type parameter.

### The `Delegate`

Class

Finally, we’re going to wrap `Callback`

objects into the `Delegate`

class. The constructor is overloaded to handle both cases: static functions and member functions. The corresponding `Callback`

object is created, and the function invocation operator would call the correct version of the `invoke`

method through polymorphism.

template <typename Ret, typename Param0> class Delegate { private: Callback<Ret, Param0> *callback_; public: Delegate(Ret (*func)(Param0)) :callback_(new StaticFunctionCallback<Ret, Param0>(func)) {} template <typename T, typename Method> Delegate(T *object, Method method) :callback_(new MethodCallback<Ret, Param0, T, Method>(object, method)) {} ~Delegate(void) { delete callback_; } Ret operator()(Param0 param0) { return callback_->invoke(param0); } };

### Some Sample Client Code

We’re pretty much done here. Now I’ll just show you how you would use this delegate class in the client code.

First, I declare four classes with single inheritance and multiple inheritance (just to show that this works in both cases), as well as a static function `foo`

.

class A { public: virtual int foo(int p) { std::cout << "A::foo(" << p << ")" << std::endl; } }; class B : public A { public: virtual int foo(int p) { std::cout << "B::foo(" << p << ")" << std::endl; } }; class C { }; class D : public C, public A { public: virtual int foo(int p) { std::cout << "D::foo(" << p << ")" << std::endl; } }; int foo(int x) { std::cout << "foo(" << x << ")" << std::endl; }

Finally, in the main function, four delegates are created to demonstrate different scenarios. I’ve tested it with GNU g++ compiler and Microsoft Visual Studio C++ Compiler 2008 and it worked perfectly.

int main(void) { A *a = new A(); A *b = new B(); A *d = new D(); //static function Delegate<int, int> d1(foo); //member function Delegate<int, int> d2(a, &A::foo); //member function + subclass instance Delegate<int, int> d3(b, &A::foo); //member function + subclass instance + multiple inheritance Delegate<int, int> d4(d, &A::foo); d1(100); //"foo(100)" d2(200); //"A::foo(200)" d3(300); //"B::foo(300)" d4(400); //"D::foo(400)" return 0; }

Pingback: 委托模式 – 守望科技博客

Really helpfull article 😉 It combines several great sources and one custom delegate implementation. Thank you so much 😀

Awesome work, this article really helped me get over a hurdle with neat event handling for my educational game engine. Professionally everyone usually uses Don’s fastdelegate which is great but unreadable.

One modification I performed to the code you supplied was implementing a default no argument constructor to the Delegate and then splitting out the existing ctor to an AddCallback(T *object, Method method) public function to set up the delegate for use.

Then I reference count the callback_ member so one delegate can register many member functions for subscriber type usage.

Hi, I find your blog by searching c++ delete on google.

After reading the articles you mentioned and your code, I write the following implementation for my c++ callback.