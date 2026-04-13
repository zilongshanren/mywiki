---
title: 'C++ Class: Accessing contents but not the container'
url: https://anki3d.org/cpp-class-accessin-contents-container/
author: Panagiotis Christopoulos Charitos
published: '2011-09-16'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

When constructing a C++ class a good practice is to never have any member variables in public scope and this includes containers. In this little article we will discuss how to have a C++ container as a private member and be able to expose its contents without exposing the container itself.


To put it more simply imagine that we have a container that it lies in the private scope of some class (aka a private member). We want to expose the container’s data in a read/write manner but we dont want to allow access to the container itself. For the user of this class, we grant him access to the nth element of this container but we don’t allow him to push_back or from the container.

class Foo { public: typedef std::vector Container; Container& getStrings() { return strs; } const Container& getStrings() const { return strs; } private: Container strs; }; ... Foo foo; ... foo.getStrings()[0] = "Hello"; // OK! foo.getStrings().push_back("World"); // Not Acceptable

The example above is a bad example of how to expose a container. It doesn’t feet our needs simply because we give access to the container itself.

After describing what we want to do and how **not** to do it lets see the correct way. Once again we will use the boost library and more especially the iterator_range module.

#include <boost/range/iterator_range.hpp> class Foo { public: typedef std::vector Container; typedef boost::iterator_range<Container::iterator> MutableRange; typedef boost::iterator_range<Container::const_iterator> ConstRange; MutableRange getStrings() { return MutableRange(strs.begin(), strs.end()); } ConstRange getStrings() const { return ConstRange(strs.begin(), strs.end()); } private: Container strs; }; ... Foo foo; ... // Iterate, OK! BOOST_FOREACH(std::string& one, foo.getStrings()) { std::cout << one << std::endl; one += "..."; } foo.getStrings()[0] = "Hello"; // OK! foo.getStrings().push_back("World"); // OK! Error compiler

In the above example we managed to do what we wanted. We can access the contents of Foo::strs vector, we can alter them, we can iterate and more importantly we cannot alter the container at all.

At this point you may ask about the overhead of range. Apparently its very lightweight and equal to two iterator copies.

Special thanks to K.K. for creating the original proof of concept.