---
title: Designing good C++ game middleware
url: https://anki3d.org/designing-c-game-middleware/
author: Panagiotis Christopoulos Charitos
published: '2019-04-11'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

For many years I’ve been evaluating and using various game specific open source libraries and at the same time I was designing and implementing my own. Despite the fact that many libraries are quite competent on what they do, their overall design leaves a few things to be desired. Some of the concepts described here sound naive but you can’t imagine how many libraries get them wrong. This article focuses on a few good practices that designers/implementers of performance critical libraries should be aware of.

This article is built around five pillars:

- How public interfaces should look like.
- Data oriented design.
- The importance of thread-awareness.
- Memory management.
- And some general concepts.

Who is the target audience:

- People who want to create performance critical libraries/middleware.
- People who want to attract serious users and not only hobbyists.
- Mainly directed to opensource.

Who is not the target audience:

- People who want to create middleware solely for their own amusement.
- C++ purists.

## Introduction

Looking at the forest and not the tree a performance critical library should:

- be all about performance (obviously),
- should have a specialized set of functionality and shouldn’t be trying to do more than it should,
- and it should have tight integration with the engine.

A recurring example based on a **pseudo (rigid body) physics library** will be used throughout this article to demonstrate some of the good practices. This pseudo physics library exposes a number of collision objects (eg sphere, AABB, plane etc) and the rigid body object that points to some of the former collision objects.

This library has an “update” function (also known as stepSimulation) that:

- iterates the created rigid bodies,
- does a coarse collision detection (aka broadphase. It basically checks the AABBs of the collision shapes) and gathers some pairs of colliders,
- performs more refined collision detection (aka narrowphase. It checks the actual collision shapes) on those pairs,
- and finally it runs various solvers.

From now on “user” is used to refer to user(s) of a library.

## Public interfaces

A collection of public interfaces is the means a user will use to interact with your library. Can’t stress enough how important interfaces are for a library and its initial appeal. Having good interfaces is a big challenge and sometimes it’s half of the work. So, what makes a good interface? It should be **minimal, documented, self documented, stable, flexible and extendable**.

What makes an interface **minimal**? A minimal interface should avoid any clatter. Internal functionality and/or functionality the user is not expected to interact with, shouldn’t obscure the user’s vision. It’s amazing how many people get that wrong. One solution that hides private functionality is the use of PIMPL idiom. PIMPL is not great in terms of performance though since it implies an indirection (pointer dereference) and a memory allocation so try to avoid it. Similar solutions that will prevent inlining should also be avoided.

**Documentation** is very important as well. Using doxygen is a pretty standard way to document your interfaces. Even if none ever generates the html documentation having a universally accepted way to document your code is a plus.

**Self-documented** code is even more important than doxygen documentation. Having some rules that govern the logic of your library will help people understand and reason about every piece of your library’s functionality. One simple example is the use of “const” keyword. Having const methods most of the time implies thread-safety. This also applies to const arguments, member variables etc. Some languages (Rust) mark all of their variables as const by default, that’s how important const is. So don’t be lazy and use const everywhere.

A more complex example of self-documentation can be a scheme that governs the ownership and lifetime of objects (or memory in general). AnKi and Qt are using a scheme where passing objects as pointers means that the ownership of that object will be shared and less often that it will be totally owned by the pointer’s consumer or that the object is optional (nullptr). In all other cases references should be used. Co-ownership practically means that the pointer should be deleted after all the objects that co-own it. Example:

```
class Foo
{
public:
// boo is passed as pointer. This means that Foo co-owns boo. boo
// shouldn't be deleted before a Foo that co-owns it does.
void someMethod(Boo* boo);
// hoo is passed as a reference. hoo can be deleted after the call
// to someMethod2
void someMethod2(Hoo& hoo);
// Method returns a pointer. This means that the caller of newLoo
// should take (co)ownership of the pointer.
Loo* newLoo();
// Method returns a reference. The caller of getLoo shouldn't try to
// take ownership of the reference.
Loo& getLoo();
};
Boo* boo = new Boo();
Foo* foo = new Foo();
foo.someMethod(boo); // foo co-owns boo
delete foo; // First delete the “owner”
delete boo; // Then delete the “owned”
```

**The stability, flexibility and extensibility** are pretty abstract notions when it comes to interfaces and I don’t think there is a point in discussing them. They are very subjective.

Another interesting concept revolves around the **programming language of the public interfaces**. Many libraries have a C++ implementation but C public interfaces. This is generally a good idea because C will force the public interface to be minimal and clean and at the same time it will make the library easy to embed into other languages (eg python bindings). But that doesn’t apply to everything so keep that in mind.

## Data oriented design

**Cache misses** are one of the worst performance offenders nowadays and minimizing them should be a priority. Constructing a data oriented aware public interface for your library will play a vital role in performance. The pseudo physics engine is a prime example where wrong interfaces will result in suboptimal performance.

So let’s imagine that our pseudo physics library exposes the rigid body class in a way that allows the user to place it in memory however they want:

```
class MyLibRigidBody
{
public:
void setForce(...);
void setMass(...);
private:
// Internal members
float m_mass;
Vec3 m_gravity;
// ...
};
```

The library’s context holds a list of rigid bodies that will be used to iterate during simulation time. The user is pushing their own rigid bodies down to the context:

```
class MyLibContext
{
public:
// ...
void pushRigidBody(MyLibRigidBody* body)
{
m_rigidBodies.pushBack(body);
}
void popRigidBody(MyLibRigidBody* body)
{
// ...
}
// ...
private:
// ...
Vector<MyLibRigidBody*> m_rigidBodies;
// ...
};
```

And the **update** function iterates the user provided rigid bodies for various operations. Example:

```
void update(MyLibContext& ctx, double deltaTime)
{
// Broadphase
Vector<Pair> pairs;
for(unsigned i = 1; i < ctx.m_rigidBodies.getSize(); ++i)
{
const MyLibRigidBody& a = *ctx.m_rigidBodies[i - 1];
const MyLibRigidBody& b = *ctx.m_rigidBodies[i];
if(collide(a, b))
{
pairs.pushBack(a, b);
}
}
// Narrophase
for(Pair& pair : pairs)
{
if(detailedCollide(pair.a, pair.b))
{
// Append to a new vector
}
}
// run the somulation
runSolver(deltaTime, ...);
}
```

The fact that the library allows the user to allocate MyLibRigidBody themselves sounds like a nice idea. You might think that this is good design since the library gives some responsibility (allocation of MyLibRigidBody) to the user. Well, it’s not.

The update function iterates all the rigid bodies one after the other and does some computations (broadphase). Ideally, all of those rigid bodies should be in a contiguous piece of memory and they should be visited in the order they are laid in memory, this is the way to minimize cache misses. Giving the car keys to the user might not be the best thing to do in this example.

Instructing the user to pack their rigid bodies into a huge contiguous array is also not enough. The update function iterates the m_rigidBodies array in an order only the MyLibContext knows. As we mentioned before, to have optimal caching performance the order of m_rigidBodies should match the user’s memory layout. But that’s not easy in the given example especially if the user pushes and pops rigid bodies all the time.

In this case having your library allocating MyLibRigidBody instead of the user might be a better idea.

```
class MyLibContext
{
public:
// ...
MyRigidBody* newRigidBody();
// ...
private:
// ...
Vector<MyLibRigidBody> m_rigidBodies;
// ...
};
```

## Thread awareness

Having a thread-aware library is very important nowadays since multi-core applications have been the de-facto for ages. At the same time your library shouldn’t be trying to solve problems that the user can solve better.

So the first big thing to solve is to show which functionality is thread-safe and which isn’t. The section about interfaces and **const correctness** covered that so I won’t expand.

The next big thing to be aware of is that your library shouldn’t be trying to optimize its algorithms by parallelizing its workloads. This practically means that your library **should never be spawning any threads**. A good library should be flexible enough by providing to its users the means to multithread the workload themselves. By using our pseudo physics library as an example imagine an “update” function that takes as a parameter the number of threads. Internally that “update” function can run the broadphase collision detection in a multithreaded manner, then the narrowphase, then the solver (to some extent). Integrating that “update” function into a task-based system (that many modern engines have) will be quite problematic. The physics’ library threads will fight with the game threads. One solution is for the library to provide a number of “update” functions and a set of rules that describe their dependencies or intended flow. Another alternative is to have an interface that the user will implement themselves and pass it to the library.

Since your library shouldn’t be the one solving the thread scaling problem does that mean that **thread contention/protection **(smart pointers, locks and other sync primitives) is outside the scope of your library? Yes and no. Smart pointers should be largely avoided since atomic operations are not free. Ownership should be the responsibility of the user and the library should provide documentation and proper interfaces. But what about locks? There are cases where a function is largely thread-safe but one small part of its work requires a lock. If the locking is left to the user the critical path will be wider since the user will have lock the whole function. In that case, having the library handling the critical sections might be better for performance. One example is malloc-like functions. It’s given that malloc-like functions should be thread-safe by design and this is a prime example of functionality that should be responsible for protecting its critical sections. But things should be transparent. Having the option to lock or not is one solution, having your library accepting an interface for the lock itself is another. A mutex abstraction that the user will implement might be a good idea especially on game engines that instrument mutexes (prime example of “tight integration” we mentioned earlier).

Next thing, **avoid globals variables** (meaning mutable global variables, not your typical “static const char* someString;” thing) and that includes singletons. Globals may make sense for some thread local arenas or other use cases but generally they imply laziness and create issues around multithreading. Try to avoid them.

## Memory management

As mentioned before the library should have tight integration with the engine and as little responsibility as possible. Memory management is a great example where these two rules apply. Ideally, the library should be **accepting a number of user provided allocators** (you’ll see later why you might need a number of them) and leave the memory management to the user. The allocator could have a pretty simple interface like this one:

```
class MyLibAllocator
{
public:
void* m_userData;
void* (*m_allocationCallback)(
void* userData, unsigned size, unsigned alignment);
void (*m_freeCallback)(void* userData, void* ptr);
};
```

There are a few things to note about MyLibAllocator. It doesn’t have virtuals, yes. Virtual methods have an indirection through the vtable. Since the allocation functions will be used a lot and because performance is critical, plain old C callbacks are preferable. Also, providing tight alignment in the allocation function is also preferable.

Another thing that many (actually all) libraries get wrong is that they take the user provided allocator and store it in some global variables (most of the time they store 2 callbacks and maybe a void*). This is a side effect of C++ because overridden operator new and operator delete are static methods and that creates some complications (long talk and I won’t expand here). But we already discussed that globals are bad and that applies to the way the allocator is stored. For that reason have a context that holds the user allocator. Then require all objects of your library to know about that context. If the object knows the context then it can also allocate memory.

```
class MyLibContext
{
public:
// Create a context with optional user allocators
MyLibContext(const MyLibAllocator& userAllocators = {})
: m_allocator(userAllocator)
{}
private:
// A copy of the user allocator
MyLibAllocator m_allocator;
};
```

The library shouldn’t necessarily be tight to a specific allocator since it’s absolutely possible and desirable to **accept specialized allocators** besides a global one. For example, our pseudo physics library can use the global allocator (stored in the MyLibContext) to allocate the MyLibSphereCollisionShape or the MyLibRigidBody classes but have a fast allocator that will be used for the duration of a single function. Example:

```
// Library code:
extern void update(MyLibAllocator& fastAllocator, double deltaTime);
// User code:
MyLibAllocator superFastStackAllocator;
update(superFastStackAllocator, dt);
superFastStackAllocator.freeAllMemory();
```

So, the fastAllocator could be a fast linear allocator that doesn’t do any deallocations. The update function will perform temporary allocations using that allocator and when it’s done the application will free all the memory or recycle it.

## General concepts

**Avoid exceptions**. Not because they are bad but because game engines traditionally avoid them and discourage them.

The **internal source** code of your library should be in pristine shape just like your public interfaces. Self documented code and regular documentation is pretty important for advanced users that may end up debugging your code or because they want to extend it. Using **clang-format** (a popular C/C++ code formatter used in projects such as LLVM), for example, will also give points to your codebase as it implies consistency.

If possible, **try to avoid STL containers**. STL containers are too generic for most use cases and whenever you see the word “too generic” expect performance issues. If you really really want use them make sure that you have built an STL compatible allocator to pass into them.

## Conclusion

The general theme of this article is to always assume that the users of your middleware are smarter than you. Not because they really are but because they might have use cases you haven’t even imagined. The users of your library are software engineers and the more experienced they get, the more their OCD (Obsessive Compulsive Disorder) kicks in. Things that they don’t appear important to you might be to them so try to take feedback seriously.

Hope you’ve found this article useful. Comments and suggestions are welcome.