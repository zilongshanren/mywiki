---
title: A new way of organizing header files
url: https://bitsquid.blogspot.com/2012/09/a-new-way-of-organizing-header-files.html
author: Niklas
published: '2012-09-03'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

Recently, I've become increasingly dissatisfied with the standard C++ way of organizing header files (one *.h* file and one *.cpp* file per class) and started experimenting with alternatives.

I have two main problems with the ways headers are usually organized.

First, it leads to long compile times, especially when templates and inline functions are used. Fundamental headers like *array.h* and *vector3.h* get included by a lot of other header files that need to use the types they define. These, in turn, get included by other files that need *their* types. Eventually you end up with a messy nest of header files that get included in a lot more translation units than necessary.

Sorting out such a mess once it has taken root can be surprisingly difficult. You remove an *#include* statement somewhere and are greeted by 50 compile errors. You have to fix these one by one by inserting missing *#include* statements and forward declarations. Then you notice that the Android release build is broken and needs additional fixes. This introduces a circular header dependency that needs to be resolved. Then it is on to the next *#include* line -- remove it, rinse and repeat. After a day of this mind-numbingly boring activity you might have reduced your compile time by four seconds. Hooray!

Compile times have an immediate and important effect on programmer productivity and through general bit rot they tend to grow over time. There are many things that can increase compile times, but relatively few forces that work in the opposite direction.

It would be a lot better if we could change the way we work with headers, so that we didn't get into this mess to begin with.

My second problem is more philosophical. The basic idea behind object-oriented design is that data and the functions that operate on it should be grouped together (in the same class, in the same file). This idea has some merits -- it makes it easier to verify that class constraints are not broken -- but it also leads to problems. Classes get coupled tightly with concepts that are not directly related to them -- for example things like serialization, endian-swapping, network synchronization and script access. This pollutes the class interface and makes reuse and refactoring harder.

Class interfaces also tend to grow indefinitely, because there is always "more useful stuff" that can be added. For example, a string class (one of my pet peeves) could be extended with functionality for tokenization, path manipulation, number parsing, etc. To prevent "class bloat", you could write this code as external functions instead, but this leads to a slightly strange situation where a class has some "canonized" members and some second-class citizens. It also means that the class must export enough information to allow any kind of external function to be written, which kind of breaks the whole *encapsulation* idea.

In my opinion, it is much cleaner to organize things by *functionality* than by type. Put the serialization code in one place, the path manipulation code in another place, etc.

My latest idea about organization is to put all type declarations for all structs and classes in a single file (say *types.h*):

```
struct Vector3 {
float x, y, z;
};
template <class T>
class Array<T> {
public:
Array() : _capacity(0), _size(0), _data(0) {}
~Array() {free(_data);}
unsigned _capacity;
unsigned _size;
T *_data;
};
class IFileSystem;
class INetwork;
```

Note that *types.h* has no function declarations, but it includes the full data specification of any struct or class that we want to use "by value". It also has forward declarations for classes that we want to use "by reference". (These classes are assumed to have pure virtual interfaces. They can only be created by factory functions.)

Since *types.h* only contains type definitions and not a ton of inline code, it ends up small and fast to compile, even if we put all our types there.

Since it contains all type definitions, it is usually the only file that needs to be included by external headers. This means we avoid the hairy problem with a big nest of headers that include other headers. We also don’t have to bother with inserting forward declarations in every header file, since the types we need are already forward declared for us in *types.h*.

We put the function declarations (along with any inline code) in the usual header files. So *vector3.h* would have things like:

```
inline Vector3 operator+(const Vector3 &a, const Vector3 &b)
{
Vector3 res;
res.x = a.x + b.x;
res.y = a.y + b.y;
res.z = a.z + b.z;
return res;
}
```

*.cpp* files that wanted to use these operations would include *vector3.h*. But *.h* files and other *.cpp* files would not need to include the file. The file gets included where it is needed and not anywhere else.

Similarly, *array.h* would contain thinks like:

```
template <class T>
void push_back(Array<T> &a, const T &item)
{
if (a._size + 1 > a._capacity)
grow(a);
a._data[a._size++] = item;
}
```

Note that *types.h* only contains the constructor and the destructor for *Array<T>*, not any other member functions.

Furthermore, I prefer to design classes so that the "zero-state" where all members are zeroed is always a valid empty state for the class. That way, the constructor becomes trivial, it just needs to zero all member variables. We can also construct arrays of objects with a simple *memset()*.

If a class needs a more complicated empty state, then perhaps it should be an abstract interface-class instead of a value class.

For *IFileSystem*, *file_system.h* defines the virtual interface:

```
class IFileSystem
{
virtual bool exists(const char *path) = 0;
virtual IFile *open_read(const char *path) = 0;
virtual IFile *open_write(const char *path) = 0;
...
};
IFileSystem *make_file_system(const char *root);
void destroy_file_system(IFileSystem *fs);
```

Since the “open structs” in *types.h* can be accessed from anywhere, we can grop operations by what they do rather than by what types they operate on. For example, we can put all the serialization code in *serialization.h* and *serialization.cpp*. We can create a file *path.h* that provides path manipulation functions for strings.

An external project can also "extend" any of our classes by just writing new methods for it. These methods will have the same access to the *Vector3* data and be called in exactly the same way as our built-in ones.

The main drawback of this model is that internal state is not as "protected" as in standard object-oriented design. External code can "break" our objects by manipulating members directly instead of using methods. For example, a stupid programmer might try to change the size of an array by manipulating the *_size* field directly, instead of using the *resize()* method.

Naming conventions can be used to mitigate this problem. In the example above, if a type is declared with *class* and the members are preceded by an underscore, the user should not manipulate them directly. If the type is declared as a *struct*, and the members do not start with an underscore, it is OK to manipulate them directly. Of course, a stupid programmer can still ignore this and go ahead and manipulate the members directly anyway. On the other hand, there is no end to the things a stupid programmer can do to destroy code. The best way to protect against stupid programmers is to not hire them.

I haven’t yet written anything really big in this style, but I've started to nudge some files in the Bitsquid codebase in this direction, and so far the experience has been positive.

Cool stuff man. The more I use c++, the more I start to hate all its fancy features and start leaning towards traditional c-style (structs and functions), wrapped up in namespaces. Seems like what your explaining is similar to what im doing! Except you go one step further to group by functionality instead of type.


ReplyDeleteI would like to see how types.h ends up on any large scale project if _all_ your types are literally in there

It's a pain that object implementation is linked to heap and stack allocation, it would be cool to be able to declare a type interface in a header, with all the methods, and the object storage into another header. If you include only the interface, you can only work with said object via pointers or references, and create it on the heap.



ReplyDeleteIt would be possible to hack this I guess having a class with no member variables and hacking new to allocate the needed space for the private data structure, but then you would not be able to work with said class on the heap at all, you would break the debugger and so on...

So nothing, your approach is nice, I was wondering if it could be worth to have private members and all your external functions as static in a friend class instead. That could give you still the separation between public and private members. It would not work with operators though and it's probably not a bright idea. As you say, naming conventions are enough and if programmers want to hack around them, they can hack around anything.

The idea of using a types.h with class/struct using "_" prefix as naming convention,


ReplyDeleteand then having functions operating on these types,

is just like the Go programming language.

Nice to see it adapted in C++.

Breaking out the state and functionality has been something I've been doing lately and it's really, really nice. Knowing that all state is, inherently, represented in a single structure is pretty incredible when it comes to managing memory and serialization.



ReplyDeleteHaving a central types.h file create something of a nasty hotspot for recompilation. Wouldn't any trivial change to any data structure result in a recompile of any file using the types (which is probably everything)?

Breaking out the class/struct definitions into separate files would still provide most of the benefits as far as I can see, but is there a reason aside from ease use to have everything in that single header?

Yes, but in my experience, core data types don't change *that* often. (When headers change it is usually because you add new methods.) Second, a change in the fundamental data types is likely to trigger a recompile of a large part of the code anyway. And third, with this approach a full recompile should take less than a minute, so it is not a catastrophe.


ReplyDeleteStill for a large system I would probably do some partitioning of types.h (maybe having things like math_types.h, collection_types.h, etc). But having a *_types.h file for every .h file leads to too much file juggling for my taste.

Material for ideas...




ReplyDeleteExperiments With Includes

http://gamearchitect.net/Articles/ExperimentsWithIncludes.html

Even More Experiments with Includes

http://gamesfromwithin.com/even-more-experiments-with-includes

Niklas, can you give us roughly:




ReplyDelete* the number of #include's you were able to eliminate by nudging the Bitsquid codebase toward a "types.h" approach

* the compile-time speedup you attained

* what build environment you use (distributed compilation? CPU speeds? HDDs or SSDs?)

I'm curious to know how big the win has been for you.

I think the only significant downside to a "types.h" approach is, as Ryan pointed out, a near-full rebuild upon any change of types.h. This sounds fine for a 1-2 minute Bitsquid build, but would be catastrophic (at least at first) for some of the commercial game engines I've worked with (where full builds routinely exceeded 20 minutes with compilation distributed over 10 decent PCs).

Thanks for the articles, Niklas -- they're always good reading.

I have only done some very small baby steps for the Bitsquid code base, which haven't really affected the compile time. (It's a production code base, so I don't want to make drastic changes.)





ReplyDeleteWe have ~1 minute compile times ATM. We do multithreaded builds and use SSDs. We don't do distributed builds.

I don't think types.h will change *that* much. It is usually quite rare that you change the fundamental data types (at least if you have thought things through). I think overall there might be *less* recompiling... because currently a lot of recompiling happens because I add a private helper member function -- that would disappear.

And of course the goal of this is to reduce our build times... once a full rebuild is down at 30 s -- we don't even have to care that much if it happens once in a while.

But I agree that if you are at 20 minute distributed builds there might be other reorganization that you need to do before you go all out with this approach.

Violation of the Once And Only Once principle. Duplication of function prototypes.

ReplyDeleteThe idea's actually not that uncommon. Most people who have deployed it actually reorganize their classes as follows:




ReplyDelete1) Pure type declaration (.h file)

2) Inline definitions (.inl file)

3) Non-inline definitions (.cpp file)

There's a brief discussion here on StackOverflow: http://stackoverflow.com/questions/1208028/significance-of-a-inl-file-in-c

The only downside I've seen to this approach is extra burden on any client .cpp file to always include the .inl. You can get into a state where missing includes may not be detected until link time and be entirely dependent on your compiler options. Example:

1) ClientOne.cpp needs ClassA's inline functions so includes ClassA.inl.

2) ClientTwo.cpp also needs those but forgets to include ClassA.inl.

If ClientOne.o and ClientTwo.o are linked into the same executable you may get undefined references from ClientTwo.o:

1) If the inline functions were able to be inlined then ClientOne has the code but ClientTwo does not.

2) If the inline functions were too big to be inlined then ClientTwo accidentally gets access to ClientOne's weak-reference copies and linking succeeds.

I don't think that's exactly the same thing.


ReplyDeleteWith the .inl approach you would still typically have the function declarations in the .h file. What I'm proposing is to move the function declarations as well to a separate file, and just have the minimal raw data definitions in the _types.h file.

Hello! Semantic segmentation annotation outsourcing is very popular in today's world, but how do you find the best service provider on the market? I advise you to pay attention to our company Mobilunity-BPO! We have access to the best specialists and have been helping companies around the world for many years!

ReplyDeleteThe cost of a smart tv price in pakistan might vary significantly in Pakistan, depending on the budget and tastes. Screen size, resolution quality (HD, Full HD, 4K), intelligent features (such as built-in WiFi and streaming app compatibility), and other technical improvements (like HDR and Quantum Dot display) all have an impact on the price.

ReplyDeleteIt's so easy to send smiles all throughout Dubai with our amazing flower delivery service! They add something special to every event with their exquisite assortment of flowers and their timely, dependable delivery. Easily spread happiness with their exquisite bouquets! Click Here for more flowers delivery in dubai

ReplyDeleteAttract Group's expertise in airline and aviation software development is truly impressive. Their commitment to enhancing operational efficiency through innovative technology solutions is evident. By focusing on industry-specific challenges, they provide tailored software that meets the unique needs of airlines and aviation companies. Their approach not only streamlines processes but also enhances customer experience, setting a new standard in the aviation sector. It's exciting to see how they drive advancements in this critical industry!

ReplyDelete