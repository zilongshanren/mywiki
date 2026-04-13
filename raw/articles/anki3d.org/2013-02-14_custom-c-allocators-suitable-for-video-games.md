---
title: Custom C++ allocators suitable for video games
url: https://anki3d.org/cpp-allocators-for-games/
author: Panagiotis Christopoulos Charitos
published: '2013-02-14'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

In C++ allocators are special classes that practically do what their name suggests, they allocate and deallocate memory. They are used mainly by STL containers (vector, map etc) and they act as an interface/guide for the container’s memory management.

Allocators is a somewhat hidden feature that most C++ programmers don’t bother messing around with. For the most cases the default STL allocator (std::allocator) is enough and it works just fine. For some specific cases though where performance is essential developers create their own allocators that work around some design problems and limitations the default allocator has.

This article presents some consepts relevant to game development in C++11. More specifically:

1. Create a custom allocator that resembles std::allocator

2. Why replace the default allocator?

3. Stack allocator


# Create a custom allocator that resembles std::allocator

The first section is introductory and will present a way to create an custom allocator that is similar to std::allocator and adds some debugging information on top of that.

An STL compatible allocator is a template class of the form:

template<typename T> class Allocator

it must contain some typedefs on public scope

typedef size_t size_type; typedef ptrdiff_t difference_type; typedef T* pointer; typedef const T* const_pointer; typedef T& reference; typedef const T& const_reference; typedef T value_type;

and it must contain all of the following methods

/// Default constructor Allocator() throw(); /// Copy constructor Allocator(const Allocator& other) throw(); /// Copy constructor with another type template<typename U> Allocator(const Allocator<U>&) throw(); /// Copy Allocator<T>& operator=(const Allocator& other); /// Copy with another type template<typename U> Allocator& operator=(const Allocator<U>& other); /// Get address of a reference pointer address(reference x) const; /// Get const address of a const reference const_pointer address(const_reference x) const; /// Allocate n elements of type T pointer allocate(size_type n, const void* hint = 0); /// Free memory of pointer p void deallocate(void* p, size_type n); /// Call the constructor of p void construct(pointer p, const T& val); /// Call the constructor of p with many arguments. C++11 template<typename U, typename... Args> void construct(U* p, Args&&... args); /// Call the destructor of p void destroy(pointer p); /// Call the destructor of p of type U template<typename U> void destroy(U* p); /// Get the max allocation size size_type max_size() const /// A struct to rebind the allocator to another allocator of type U template<typename U> struct rebind { typedef Allocator<U> other; };

Now that we know how an allocator should look like we can create one that wraps *malloc()* and *free()*. It also tracks the allocations and informs the user if he forgot to deallocate some space.

/// Define a global that holds the allocated size extern size_t gAllocatedSize; /// Default constructor Allocator() throw() {} /// Copy constructor Allocator(const Allocator&) throw() {} /// Copy constructor with another type template<typename U> Allocator(const Allocator<U>&) throw() {} /// Destructor ~Allocator() {} /// Copy Allocator<T>& operator=(const Allocator&) { return *this; } /// Copy with another type template<typename U> Allocator& operator=(const Allocator<U>&) { return *this; } /// Get address of reference pointer address(reference x) const { return &x; } /// Get const address of const reference const_pointer address(const_reference x) const { return &x; } /// Allocate memory pointer allocate(size_type n, const void* = 0) { size_type size = n * sizeof(value_type); gAllocatedSize += size; return (pointer)::malloc(size); } /// Deallocate memory void deallocate(void* p, size_type n) { size_type size = n * sizeof(T); gAllocatedSize -= size; ::free(p); } /// Call constructor void construct(pointer p, const T& val) { // Placement new new ((T*)p) T(val); } /// Call constructor with more arguments template<typename U, typename... Args> void construct(U* p, Args&&... args) { // Placement new ::new((void*)p) U(std::forward<Args>(args)...); } /// Call the destructor of p void destroy(pointer p) { p->~T(); } /// Call the destructor of p of type U template<typename U> void destroy(U* p) { p->~U(); } /// Get the max allocation size size_type max_size() const { return size_type(-1); } /// A struct to rebind the allocator to another allocator of type U template<typename U> struct rebind { typedef Allocator<U> other; };

An example of usage for Allocator is the following:

std::vector<Foo, Allocator<Foo>> vec; vec.resize(10, Foo(something)); std::cout << "Allocated size: " << gAllocatedSize << std::endl;

You can check the *gAllocatedSize* at the end of the application and report any memory wasted.

# Why replace the default allocator?

The answers on that question are many but for a game engine the rationale is simple. To understand the problem better we need first to understand that malloc and free work optimally when we allocate big chunks and we don’t call them that often. Calling malloc many times for small blocks will result on **memory fragmentation**. Fragmentation means that data will be scattered all over place a fact that affects the memory locality. Increased fragmentation implies more cache misses and thus slower reads from memory. On top of that the system will need more system memory because of the unused memory holes.

Another problem comes from game consoles needs. On consoles the **memory is pretty limited and requires strict management**. Wasting memory is not an option. Also allocating more memory than we have is not an option as well. For those reasons console game engines can trigger various events when memory is running low like freeing non essential assets. Other reasons may be super optimal alighment etc.

Another reason may be **memory debugging**. In that case all the allocations go through a single allocator and at some point (maybe at program’s end) we can identify memory leaks. This is what we described on the *Allocator* example above.

In AnKi the scene consists of a number of scene nodes. The actual number of nodes is high and each node is a relativity small sized class. Once it’s time to load a level AnKi allocates a big number of objects and this implies a high number of allocations. When the scene is no longer needed then a number of deallocations must happen to free memory which is slow.

To optimize the allocation/deallocation of scene nodes a new concept must take in place. What if we allocate a big chunk of memory up front and use that for all the small allocations? I sounds reasonable. When the scene is going to get freed we expect all scene nodes to be freed. That property of the scene implies a single deallocation as well.

For that we created a stack allocator…

# Stack allocator

The stack allocator is essentially a prellocated chunk of memory that has an (annoying) characteristic: the allocations/deallocations must be in a LIFO order. This characteristic obviously bind us to the fact that we cannot deallocate whenever we want but on the other hand its extremely fast.

Before we create an allocator we need to create a memory pool. This memory pool is a class that holds:

1. the preallocated memory,

2. a pointer to the top of the stack and

3. a few other things.

To make things more interesting the memory pool is fully thread safe by using atomic operations, curtesy of C++11 as well.

The class definition (as it is now in AnKi’s source code tree) is the following:

/// Thread safe memory pool class StackMemoryPool: public NonCopyable { public: /// Default constructor StackMemoryPool(PtrSize size, U32 alignmentBits = 16); /// Move StackMemoryPool(StackMemoryPool&& other) { *this = std::move(other); } /// Destroy ~StackMemoryPool(); /// Move StackMemoryPool& operator=(StackMemoryPool&& other); /// Access the total size PtrSize getSize() const { return memsize; } /// Get the allocated size PtrSize getAllocatedSize() const; /// Allocate memory /// @return The allocated memory or nullptr on failure void* allocate(PtrSize size) throw(); /// Free memory in StackMemoryPool. If the ptr is not the last allocation /// then nothing happens and the method returns false /// /// @param[in] ptr Memory block to deallocate /// @return True if the deallocation actually happened and false otherwise Bool free(void* ptr) throw(); /// Reinit the pool. All existing allocated memory will be lost void reset(); private: /// Pre-allocated memory chunk U8* memory = nullptr; /// Size of the pre-allocated memory chunk PtrSize memsize = 0; /// Points to the memory and more specifically to the top of the stack std::atomic<U8*> top = {nullptr}; /// Alignment of allocations U32 alignmentBits; /// Calculate tha aligned size of an allocation PtrSize calcAlignSize(PtrSize size) const; };

The class is non-copyable, to be more precise it’s the definition of non-copyable. The most important methods are the *allocate()* and *free()*. Both of them do not throw exceptions for reasons that are out of the scope of this article. The alignment is very important and it’s been used so the *allocate()* outputs correctly allocated memory. If the memory was not allocated there is a high risk for the application to crash. Also for some systems it can be useful for speed.

The implementation of the class is more interesting:

//============================================================================== struct MemoryBlockHeader { U32 size; }; //============================================================================== StackMemoryPool::StackMemoryPool(PtrSize size_, U32 alignmentBits_) : memsize(size_), alignmentBits(alignmentBits_) { ANKI_ASSERT(memsize > 0); memory = (U8*)::malloc(memsize); if(memory != nullptr) { top = memory; } else { throw ANKI_EXCEPTION("malloc() failed"); } } //============================================================================== StackMemoryPool::~StackMemoryPool() { if(memory != nullptr) { ::free(memory); } } //============================================================================== StackMemoryPool& StackMemoryPool::operator=(StackMemoryPool&& other) { if(memory != nullptr) { ::free(memory); } memory = other.memory; memsize = other.memsize; top.store(other.top.load()); alignmentBits = other.alignmentBits; other.memory = nullptr; other.memsize = 0; other.top = nullptr; return *this; } //============================================================================== PtrSize StackMemoryPool::getAllocatedSize() const { return top.load() - memory; } //============================================================================== void* StackMemoryPool::allocate(PtrSize size_) throw() { // memory is nullptr if moved ANKI_ASSERT(memory != nullptr); PtrSize size = calcAlignSize(size_ + sizeof(MemoryBlockHeader)); ANKI_ASSERT(size < std::numeric_limits<U32>::max() && "Too big allocation"); U8* out = top.fetch_add(size); if(out + size <= memory + memsize) { // Write the block header ((MemoryBlockHeader*)out)->size = size; // Set the correct output out += sizeof(MemoryBlockHeader); } else { // Error out = nullptr; } return out; } //============================================================================== Bool StackMemoryPool::free(void* ptr) throw() { // memory is nullptr if moved ANKI_ASSERT(memory != nullptr); // Correct the p U8* realptr = (U8*)ptr - sizeof(MemoryBlockHeader); // realptr should be inside the pool's preallocated memory ANKI_ASSERT(realptr >= memory && realptr < memory + memsize); // Get block size U32 size = ((MemoryBlockHeader*)realptr)->size; // Atomic stuff U8* expected = realptr + size; U8* desired = realptr; // if(top == expected) { // top = desired; // exchange = true; // } else { // expected = top; // exchange = false; // } Bool exchange = top.compare_exchange_strong(expected, desired); return exchange; } //============================================================================== void StackMemoryPool::reset() { // memory is nullptr if moved ANKI_ASSERT(memory != nullptr); top = memory; } //============================================================================== PtrSize StackMemoryPool::calcAlignSize(PtrSize size) const { return size + (size % (alignmentBits / 8)); }

The constructor and destructor are pretty trivial.

When *allocate()* is been called the pool calculates the size of the block to allocate. The block consists from a header (see MemoryBlockHeader) plus the requested memory. The header in this case consists from just a number, the size of the allocated bytes (including the header). The size is kept because the free() will not be called with size just like the standard free(). At this moment take a breath. Why call *free()* without size when the allocator’s *deallocate()* method passes the size? The truth is that the StackMemoryPool does not need the block header if it’s been used only in allocators but in AnKi it’s been used for other stuff as well. You can ignore the block header from now on.

The *free()* decrements the top of the stack but in a thread-safe way. We mentioned before that the allocations and deallocations should happen in LIFO order. If the requested deallocation in *free()* is not the last then the top will not change and false will be returned. The atomic operation *compare_exchange_strong()* is explained in the comments and it’s essetial for making this operation thread safe.

The *calcAlignSize()* is been used to align the given size for reasons mentioned before.

Now that we have the memory pool we can create the stack allocator. The code is the following:

/// Stack based allocator /// /// @tparam T The type /// @tparam deallocationFlag If true then the allocator will try to deallocate /// the memory. This is extremely important to /// understand when it should be true. See notes /// @tparam alignmentBits Set the alighment in bits /// /// @note The deallocationFlag can brake the allocator when the deallocations /// are not in the correct order. For example when deallocationFlag==true /// and the allocator is used in vector it is likely to fail. /// /// @note Don't ever EVER remove the double copy constructor and the double /// operator=. The compiler will create defaults template<typename T, Bool deallocationFlag = false, U32 alignmentBits = 16> class StackAllocator { template<typename U, Bool deallocationFlag_, U32 alignmentBits_> friend class StackAllocator; public: // Typedefs typedef size_t size_type; typedef ptrdiff_t difference_type; typedef T* pointer; typedef const T* const_pointer; typedef T& reference; typedef const T& const_reference; typedef T value_type; /// Default constructor StackAllocator() throw() {} /// Copy constructor StackAllocator(const StackAllocator& b) throw() { *this = b; } /// Copy constructor template<typename U> StackAllocator( const StackAllocator<U, deallocationFlag, alignmentBits>& b) throw() { *this = b; } /// Constuctor with size StackAllocator(size_type size) throw() { mpool.reset(new StackMemoryPool(size, alignmentBits)); } /// Destructor ~StackAllocator() {} /// Copy StackAllocator& operator=(const StackAllocator& b) { mpool = b.mpool; return *this; } /// Copy template<typename U> StackAllocator& operator=( const StackAllocator<U, deallocationFlag, alignmentBits>& b) { mpool = b.mpool; return *this; } /// Get the address of a reference pointer address(reference x) const { return &x; } /// Get the const address of a const reference const_pointer address(const_reference x) const { return &x; } /// Allocate memory pointer allocate(size_type n, const void* hint = 0) { ANKI_ASSERT(mpool != nullptr); (void)hint; size_type size = n * sizeof(value_type); void* out = mpool->allocate(size); if(out != nullptr) { // Everything ok } else { throw ANKI_EXCEPTION("Allocation failed. There is not enough room"); } return (pointer)out; } /// Deallocate memory void deallocate(void* p, size_type n) { ANKI_ASSERT(mpool != nullptr); (void)p; (void)n; if(deallocationFlag) { Bool ok = mpool->free(p); if(!ok) { throw ANKI_EXCEPTION("Freeing wrong pointer. " "The deallocations on StackAllocator should be in order"); } } } /// Call constructor void construct(pointer p, const T& val) { // Placement new new ((T*)p) T(val); } /// Call constructor with many arguments template<typename U, typename... Args> void construct(U* p, Args&&... args) { // Placement new ::new((void *)p) U(std::forward<Args>(args)...); } /// Call destructor void destroy(pointer p) { p->~T(); } /// Call destructor template<typename U> void destroy(U* p) { p->~U(); } /// Get the max allocation size size_type max_size() const { ANKI_ASSERT(mpool != nullptr); return mpool->getSize(); } /// A struct to rebind the allocator to another allocator of type U template<typename U> struct rebind { typedef StackAllocator<U, deallocationFlag, alignmentBits> other; }; /// Reinit the allocator. All existing allocated memory will be lost void reset() { ANKI_ASSERT(mpool != nullptr); mpool->reset(); } const StackMemoryPool& getMemoryPool() const { ANKI_ASSERT(mpool != nullptr); return *mpool; } private: std::shared_ptr<StackMemoryPool> mpool; }; /// Another allocator of the same type can deallocate from this one template<typename T1, typename T2, Bool deallocationFlag, U32 alignmentBits> inline bool operator==( const StackAllocator<T1, deallocationFlag, alignmentBits>&, const StackAllocator<T2, deallocationFlag, alignmentBits>&) { return true; } /// Another allocator of the another type cannot deallocate from this one template<typename T1, typename AnotherAllocator, Bool deallocationFlag, U32 alignmentBits> inline bool operator==( const StackAllocator<T1, deallocationFlag, alignmentBits>&, const AnotherAllocator&) { return false; } /// Another allocator of the same type can deallocate from this one template<typename T1, typename T2, Bool deallocationFlag, U32 alignmentBits> inline bool operator!=( const StackAllocator<T1, deallocationFlag, alignmentBits>&, const StackAllocator<T2, deallocationFlag, alignmentBits>&) { return false; } /// Another allocator of the another type cannot deallocate from this one template<typename T1, typename AnotherAllocator, Bool deallocationFlag, U32 alignmentBits> inline bool operator!=( const StackAllocator<T1, deallocationFlag, alignmentBits>&, const AnotherAllocator&) { return true; }

The StackAllocator contains lots of things but most of them are standard allocator things. StackAllocator is essentialy a wrapper on top of StackMemoryPool. The only interesting thing about it is the *deallocationFlag*. If the allocator is used in the propper LIFO way then we can set this flag to 1, if we set it to 0 then the allocator will ignore deallocations. Why we ignore deallocations? This happens because the STL containers don’t work in a LIFO order and trying to deallocate like that is for the most cases useless.

One other thing to mention is that the *mpool* member variable is shared_ptr, this makes the StackAllocator totaly thread safe.

An example of StackAllocator usage follows:

// With strings StackAllocator<char, false> alloc(128); typedef std::basic_string<char, std::char_traits<char>, StackAllocator<char, false>> Str; Str str(alloc); str = "lalala"; str = "lalalalo"; // With Foo class StackAllocator<Foo> fooalloc(128); std::vector<Foo, StackAllocator<Foo>> vec(fooalloc); for(int i = 0; i < 10; i++) { vec.push_back(Foo(i)); }

That’s all for now. Comments and suggestions on the comments section bellow.