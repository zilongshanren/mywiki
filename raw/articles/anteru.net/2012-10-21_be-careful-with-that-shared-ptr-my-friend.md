---
title: Be careful with that shared_ptr, my friend
url: https://anteru.net/blog/2012/be-careful-with-that-shared-ptr-my-friend
published: '2012-10-21'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

If you are developing in C++, chances are high that you are using `shared_ptr`

. At least on this blog, [my article on shared_ptr](https://anteru.net/blog/2008/09/01/260/) is by far the one with the most hits. However, if you are using

`shared_ptr`nearly everywhere, you are

**doing it wrong**.

Over the years, my attitude to shared pointers has shifted. At the beginning, I was all in on shared pointers, wrapping nearly every call to `new`. While this solved all memory leaks once and for all, there were also a few subtle cases where one object would be kept alive while some dependency could die and other minor lifetime issues. Over time, these small issues became more and more of a problem, and as it turns out, they are intimately tied to shared pointers. The question you should always ask yourself is: Are the object ownerships clearly expressed?

If your answer is no, chances are high that some object can be floating with the help of a shared pointer while a dependency of it has been destroyed already, leaving you with unusable yet existing objects. A simple example: If you have a class which represents a file system, which returns file handles by shared pointer, what happens when the file system is destroyed? If you have given out shared pointers, you are doomed right now, as the clients will assume that their pointers are valid while in fact they are pointing to zombies. Recently, I did a large sweep over my codebase to remove shared pointers in such cases and replace them with handles (or in some cases raw pointers) – which more clearly expresses what is going on, making the code safer. You can still allow users to wrap a handle using a shared pointer and a custom deleter, but its explicit now and no longer implicit.

Sure, you can solve such problems with weak and shared pointers, and by referencing the parent from the children and even more code, but does it really make things easier? The easier the code, the better, and with shared pointers, it’s really easy to dig oneself into a hole from which it becomes increasingly complicated to get out. A simple handle makes ownership crystal clear and can simplify the code a lot.

The second problem arises once you return objects as shared pointers. While is doesn’t sound like a big deal at first, in practice it is. In most cases, the clients will only need an object for a short time. For instance, you might pass a file handle directly into an image loading function, and destroy it afterwards. In this case, using a shared pointer is simply a waste: It requires more memory to be allocated, atomic operations and generates more code. The core problem here is that returning a shared pointer is a very strong statement; indicating that clients will always want to reference count the object. If that is not the case, you still enforce the overhead of it onto your clients.

Fortunately, there is a much better alternative: In C++11 (and already supported by Clang, MSVC10 and GCC 4.6) you can return a unique pointer instead. It transparently converts into a shared pointer if necessary, but it’s a much more lightweight object and does not force the clients into any particular lifetime management solution. During the refactoring mentioned above, I also replaced pretty much every single function that returned a shared pointer into one returning a unique pointer. It turned out that on most call-sites, there was indeed no need for a shared pointer. As a side effect, the binary size was also reduced.

There are surely many places where shared pointers are the best solution, and I definitely would not recommended going back to manual memory management. However, shared pointers are not the only solution, and you should carefully consider if the resulting code is indeed simpler and easier to reason about. If not, consider handles or other, more explicit means of expressing ownership.