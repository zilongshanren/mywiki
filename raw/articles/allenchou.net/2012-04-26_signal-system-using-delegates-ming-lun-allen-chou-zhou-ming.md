---
title: Signal System using Delegates | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2012/04/signal-system-using-delegates/
author: Allen Chou
published: '2012-04-26'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

I introduced how to build your own C++ delegates in the [previous post](http://allenchou.net/2012/04/easy-c-delegates/). Now I’m going to show you the first practical (and probably the most common) usage of delegates: signal/event systems.

To clarify the terminology, the mapping between the system I’m going to show here and the terms in the [Observer Pattern](http://en.wikipedia.org/wiki/Observer_pattern) is as follows: a **signal** object is a **subject** object, and a **delegate** that **listens** to a signal object is an **obeserver** object that **observes** a subject object. The basic idea here is that the listeners that are interested in a specific signal object get invoked when the signal object **dispatches**. This is a very useful pattern in engine design, which can be used to eliminate [busy waiting](http://en.wikipedia.org/wiki/Busy_waiting) conditions, because the observers are **informed passively** as opposed to **actively querying** the subject for new information (this can be wasting CPU cycles if there is no actual data update).


In addition to the basic signal functionality, I’m going to add in **priorities**, which gives the client code more control over the order in which a signal inform the listeners. Note that this requires us to overload the **less-than (<)** operator for the delegate class, so that they can be ordered, which is a requirement if you want to add an element into a map or a set. I did not show how to do that in the last post, but it’s quite easy: since we have memory address of the functions, objects, and methods in delegates, we can just use those values as sorting keys.

Also, same as the previous post, to make things clear, here I’m just going to show the special case where the listener delegates only take one `int`

argument. Again, it is always easy to generalize the design with templates once you understand the basic idea.

### The `ListenerData`

Class

First, let’s look at the helper data class that is associated with each listener delegate, the `ListenerData`

class. It contains information concerning the listener delegate’s **priority**, **timestamp**, and whether the delegate is only invoked **once**.

We’re going to sort delegates according to their priority. If two delegates have the same priority, they are sorted based on the order they are added to the signal object (the timestamp). That is what the `operator<`

is doing.

class ListenerData { public: float priority; unsigned timestamp; bool once; ListenerData ( float priority_, unsigned timestamp_, bool once_ ) : priority(priority_) , timestamp(timestamp_) , once(once_) {} bool operator<(const ListenerData &rhs) const { //high priority goes to the beginning of the set if (priority != rhs.priority) { return priority > rhs.priority; } //lower timestamp goes to the beginning of the set else { return timestamp < rhs.timestamp; } } };

### The `Signal`

Class

Now let's look at the `Signal`

class. Note that there are two maps in the class, one that uses delegates as key, and the other uses listener data as key. They are "mirrored", because we need a map that is sorted by delegates for quick look up, and we need a map that is sorted by listener data to invoke the delegates in the correct order.

template <typename Param1> class Signal { private: //some typedefs for later convenience typedef std::map<Delegate<void, Param1>, ListenerData> DelegateDataMap; typedef std::pair<Delegate<void, Param1>, ListenerData> DelegateDataPair; typedef std::map<ListenerData, Delegate<void, Param1>> DataDelegateMap; typedef std::pair<ListenerData, Delegate<void, Param1>> DataDelegatePair; unsigned timestamp_; //sorted by delegates DelegateDataMap delegateDataMap_; //sorted by listener data DataDelegateMap dataDelegateMap_; public: Signal(void) : timestamp_(0) {} //Adds a delegate to the listener map. bool add ( Delegate<void, Param1> delegate, float priority = 0.0f, bool once = false ) { //duplicate listener, return false if ( delegateDataMap_.find(delegate) != delegateDataMap_.end() ) return false; delegateDataMap_.insert ( DelegateDataPair ( delegate, ListenerData(priority, timestamp_, once) ) ); dataDelegateMap_.insert ( DataDelegatePair ( ListenerData(priority, timestamp_, once), delegate ) ); //increment timestamp ++timestamp_; return true; } //overlaoded version that takes a static function bool add ( void (*func)(Param1), float priority = 0.0f, bool once = false ) { return add ( Delegate<void, Param1>(func), priority, once ); } //overloaded version that takes a method template <typename T, typename Method> bool add ( T *object, Method method, float priority = 0.0f, bool once = false ) { return add ( Delegate<void, Param1>(object, method), priority, once ); } //removes a delegate from the map bool remove(Delegate<void, Param1> delegate) { DelegateDataMap::iterator iter = delegateDataMap_.find(delegate); //delegate not found if (iter == delegateDataMap_.end()) return false; dataDelegateMap_.erase(iter->second); delegateDataMap_.erase(iter); return true; } //overloaded version that takes a static function bool remove(void (*func)(Param1)) { return remove(Delegate<void, Param1>(func)); } //overloaded version that takes a method template <typename T, typename Method> bool remove(T *object, Method method) { return remove(Delegate<void, Param1>(object, method)); } //dispatches the signal Signal &dispatch(Param1 param1) { //loop through the delegate map DataDelegateMap::iterator iter = dataDelegateMap_.begin(); while (iter != dataDelegateMap_.end()) { //invoke the delegate with the arguments iter->second(param1); //only invoke once if (iter->first.once) { delegateDataMap_.erase(iter->second); iter = dataDelegateMap_.erase(iter); } else { ++iter; } } return *this; } //removes all delegates void clear(void) { delegateDataMap_.clear(); dataDelegateMap_.clear(); timestamp_ = 0; } };

### The Client Code

That's it! Now let's look at some sample client code:

class A { public: void listener(int x) { std::cout << "A::listener(" << x << "). "; } }; void listener(int x) { std::cout << "listener(" << x << "). "; } int main(void) { A *a = new A(); Signal<int> s; s.add(&listener); s.add(a, &A::listener); //prints "listener(1). A::listener(1). " s.dispatch(1); s.clear(); s.add(a, &A::listener); s.add(&listener); //prints "A::listener(2). listener(2). " s.dispatch(2); s.clear(); s.add(&listener); s.add(a, &A::listener, 1.0f); //high priority //prints "A::listener(3). listener(3). " s.dispatch(3); s.clear(); s.add(&listener, 0.0f, true); //triggered once //prints "listener(4). " s.dispatch(4); //prints nothing s.dispatch(5); return 0; }

Done 🙂

I’ve been working for a while to set up this system and start experimenting with it, and I’ve got everything up through Delegates working fine and tested. Since setting up the Signal class, however, I’ve been trying and trying to get it to compile and can’t.

The problem seems to be the iterators used in add(), remove(), and dispatch(), for which I’ve already had to declare with the typename keyword so that the compiler would recognize them as a type, unlike your example. Now, G++’s errors involve not finding operator= for these iterators, and Visual Studio reports errors involving operator< and the "less" structure in it's internal libraries.

To double check, I copied your code verbatim and got the same exact errors. Did you run into similar errors while building this system, or are you using some sort of unique build settings/flags? My code is all in one file currently, did you implement it in a different fashion? Any help would be appreciated.

All questions retracted, ended up overloading some operators and making sure Delegates had deep copy constructors.

Glad you found it out: )