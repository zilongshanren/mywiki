---
title: My Mutex Implementation | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2012/05/my-mutex-implementation/
author: Allen Chou
published: '2012-05-17'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

There are already lots of well-known and popular libraries out there that provide [mutices](http://en.wikipedia.org/wiki/Mutual_exclusion). But I wanted to try implementing it myself for the sake of just making it. Hey, it’s summer session at [DigiPen](https://www.digipen.edu/) and I don’t have to work on any school game projects. This means I can do whatever programming exercise I want during this time 🙂

My implementation relies on “Windows.h”, which already provides mutex objects. But hey, it’s summer session! Besides, I actually find my interface design more intuitive and easier to use, so I might end up using it in my next game project.

Below is the interface for the `Mutex`

class. It has a default constructor, a copy constructor and a destructor. It also has an assignment operator. Finally, it defines the very two operations a mutex object has: lock and unlock.


The `lockPtr_`

member represents shared lock among mutices guarding the same resource. The `hasLock_`

member indicates whether this mutex has been acquired or not. The `referenceCountPtr_`

is for counting references of mutices for the same resource.

class Mutex { private: typedef unsigned long ReferenceCount; typedef LONG Lock; Lock *lockPtr_; bool hasLock_; ReferenceCount *referenceCountPtr_; public: Mutex(void); Mutex(const Mutex &clone); ~Mutex(void); Mutex &operator=(const Mutex &rhs); void lock(void); void unlock(void); } };

### Default Constructor

The default constructor does pretty much you’d expect a mutex constructor to do. The lock is initialized to one, which denotes the state of being open to acquisition, and the reference counter is, of course, initialized to one.

Mutex::Mutex(void) : lockPtr_(new Lock(1UL)) , hasLock_(false) , referenceCountPtr_(new ReferenceCount(1UL)) { }

### Copy Constructor

The copy constructor copies over all the underlying pointers, and it also increments the reference counter by one.

Mutex::Mutex(const Mutex &clone) : lockPtr_(clone.lockPtr_) , hasLock_(false) , referenceCountPtr_(clone.referenceCountPtr_) { InterlockedIncrement(referenceCountPtr_); }

### Destructor

The destructor decrements the reference counter; also, if the mutex finds itself the last one associated with the lock, it frees all the underlying pointers.

Mutex::~Mutex(void) { //check if this is the last reference if (InterlockedDecrement(referenceCountPtr_) == 0UL) { //free resource delete lockPtr_; delete referenceCountPtr_; } }

### Assignment Operator

The assignment operator has to check whether this mutex is the last one associated with the lock. If yes, it frees all the underlying pointers. Finally, it associates itself with another mutex’s lock.

Mutex &Mutex::operator=(const Mutex &rhs) { //check self-assignment if (&rhs == this) return *this; //check target resource if (rhs.lockPtr_ == lockPtr_) return *this; //force release if (hasLock_) unlock(); //check if this is the last reference if (InterlockedDecrement(referenceCountPtr_) == 0UL) { //free resource delete lockPtr_; delete referenceCountPtr_; } //copy mutex lockPtr_ = rhs.lockPtr_; hasLock_ = false; referenceCountPtr_ = rhs.referenceCountPtr_; InterlockedIncrement(referenceCountPtr_); return *this; }

### Lock

The `lock()`

method is a little more complicated, so I’ll explain the details in the comments. It is making use of the atomic operation

provided by Windows API.[InterlockedExchange](http://msdn.microsoft.com/en-us/library/windows/desktop/ms683590(v=vs.85).aspx)

void Mutex::lock(void) { //do nothing if lock is already acquired if (hasLock_) return; //try acquire lock if (InterlockedExchange(lockPtr_, 0UL)) { //lock acquired, return hasLock_ = true; return; } //lock not acquired else { //wait until lock is acquired while (1) { //try acquire lock if (InterlockedExchange(lockPtr_, 0UL)) { //lock acquired, return hasLock_ = true; return; } else { //lock not acquired, yield time slice Sleep(1); } } } }

### Unlock

The `unlock()`

method is much more simpler than `lock()`

. It just “puts” the acquired “one” back to the lock.

void Mutex::unlock(void) { if (hasLock_) { hasLock_ = false; InterlockedExchange(lockPtr_, 1UL); } }

### Finished!

That’s it. I do love the simplicity of the interface. By the design of its copy constructor and assignment operator, the `Mutex`

class is to be passed by value among threads.

//...some code... const int NUM_ITERATIONS = 10000; int main(void) { //...some code... Mutex mutex; int i = 0; Thread(new Counter(&i, mutex, NUM_ITERATIONS)).start(); Thread(new Counter(&i, mutex, NUM_ITERATIONS)).start(); //...some code... //after the two threads have finished, //i should be exactly (2 * NUM_ITERATIONS) } Counter::Counter(int *target, Mutex mutex, int numIterations) : target_(target) , mutex_(mutex) , numIterations_(numIterations) { } Counter::run(void) { for (int i = 0; i < numIterations_; ++i) { mutex_.lock(); ++(*target_); mutex.unlock(); } }

mutex!

well, so miss C language~~~

process and thread~~~