---
title: 'STL auto_ptr: A bad idea'
url: https://anki3d.org/stl-auto_ptr-a-bad-idea/
author: Panagiotis Christopoulos Charitos
published: '2011-01-14'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

C++ Standard Template Library (STL) offers a smart pointer called auto_ptr. auto_ptr is a template class that acts as a wrapper for a single dynamically allocated class instance. Its purpose and its usefulness is to deallocate the memory when this smart pointer gets out of scope. Its a way to do automatic garbage collection in C++ by saving us from the extra code writing. One extra reason to use auto_ptr is that it makes the code less error prone simply because it doesn’t rely on the programmer to do the memory dealocation.

In this short article we will discuss a case where auto_ptr fails to do what its supposed to do….


How the auto_ptr is being used:

// Begin of block { MyClass* newInstance = new MyClass; auto_ptr ptr(newInstance); } // End of block

At the end of the block the auto_ptr calls its destructor and checks if it holds a non null pointer. In our case its not null so it deallocates the newInstance.

Now that we roughly know what auto_ptr let us see why its a bad idea to use it at least in GCC. For our test case we have four files:


**ClassA.h**

#ifndef CLASS_A_H #define CLASS_A_H #include <memory> class ClassB; // Forward declaration of ClassB class ClassA { public: ClassA(); // Implicit destructor: //~ClassA() {} private: std::auto_ptr<ClassB> bPtr; }; #endif

In the above declaration we dont include the ClassB.h at all, the compiler wont complain at all because the forward declaration is sufficient for pointers and bPtr is essentially a pointer.


**ClassA.cpp**

#include "ClassA.h" #include "ClassB.h" ClassA::ClassA(): bPtr(new ClassB) {}


**ClassB.h**

#ifndef CLASS_B_H #define CLASS_B_H #include <iostream> class ClassB { public: ClassB() {std::cout << "ClassB()" << std::endl;} ~ClassB() {std::cout << "~ClassB()" << std::endl;} private: int x; }; #endif


**Main.cpp**

#include "ClassA.h" //#include "ClassB.h" int main(int, char**) { { ClassA a; } return 0; }

The output of the above test case is:

ClassB

If we uncomment the second line (#include “ClassB.h”) the output will become:

ClassB ~ClassB

In the first case the destructor of ClassB was not called at all! The “a” instance is deleted but the ClassA::bPtr destructor is never called. Is this an error or what? Actually in Main.cpp there is no mention of the ClassB destructor at all so a simple dealocation happens without calling the destructor. As you can see this is a VERY VERY bad situation where auto_ptr fails to do what its supposed to do. GCC could and should post a warning but even with -Wall and -Wextra enabled it failed to do so.

Boost library once again shows its brilliance and avoids these kind of logical errors with compile time assertions. In our test case we can use a boost::scoped_ptr to ensure that the ~ClassB destructor will be called. A simple replace of auto_ptr will not do the trick as we have to add a destructor in ClassA.cpp or remove the ClassB forward declaration from ClassA.h.