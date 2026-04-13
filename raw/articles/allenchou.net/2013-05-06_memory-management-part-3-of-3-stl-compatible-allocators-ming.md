---
title: 'Memory Management part 3 of 3: STL-Compatible Allocators | Ming-Lun "Allen"
  Chou | 周明倫'
url: https://allenchou.net/2013/05/memory-management-part-3-of-3-stl-compatible-allocators/
author: Allen Chou
published: '2013-05-06'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Memory Management Series](http://allenchou.net/memory-management-series/).

In [part 1](http://allenchou.net/2013/05/memory-management-part-1-of-3-the-allocator/) and [part 2](http://allenchou.net/2013/05/memory-management-part-2-of-3-c-style-interface/) of this series, I showed how to implement a fix-sized memory allocator and a C-style interface. Part 3 will demonstrate how to make an allocator that is compatible with STL containers.

### STL Compatibility?

You probably have used various STL containers in C++, like vectors and lists:

std::vector<int> myVector; myVector.push_back(1); myVector.push_back(2); myVector.push_back(3); std::list<int> myList; myList.push_back(1); myList.push_back(2); myList.push_back(3);

But do you know that these STL containers actually take a second template argument?

The second argument is for you to specify a custom memory allocator type that you’d like the containers to use. By default, the `std::allocator`

class template is used, which is simply a wrapper around `malloc`

and `free`

. If we can crate an allocator class that conforms to the STL allocator interface, we can tell STL containers to use our allocator instead of the default one.


### The Interface & Implementation

This is the [interface](http://en.cppreference.com/w/cpp/memory/allocator) we need to stick with. Since the link already explains the interface in detail, we’re just going to dive into the implementation:

template <typename T> class allocator { public: typedef T value_type; typedef T *pointer; typedef T &reference; typedef const T *const_pointer; typedef const T &const_reference; typedef unsigned size_type; typedef unsigned difference_type; template <typename U> struct rebind { typedef allocator<U> other; }; pointer allocate(unsigned n) { return reinterpret_cast<T *> (Allocate(sizeof(T) * n)); } void deallocate(pointer p, unsigned n) { Free(p, sizeof(T) * n); } void construct(pointer p, const_reference clone) { new (p) T(clone); } void destroy(pointer p) { p->~T(); } pointer address(reference x) const { return &x; } const_pointer address(const_reference x) const { return &x; } bool operator==(const allocator &rhs) { return true; } bool operator!=(const allocator &rhs) { return !operator==(rhs); } };

### Sample Client Code

If we insert our allocator as the second template argument to STL containers, they would *automagically* start using our allocator instead of the default one.

std::vector<int, allocator<int>> myVector; myVector.push_back(1); myVector.push_back(2); myVector.push_back(3); std::list<int, allcator<int>> myList; myList.push_back(1); myList.push_back(2); myList.push_back(3);

### End of Series

This is the end of my 3-part Memory Management series. I hope you enjoyed it 🙂

Simple and wonderful! It’s a good example for beginners in C ++.