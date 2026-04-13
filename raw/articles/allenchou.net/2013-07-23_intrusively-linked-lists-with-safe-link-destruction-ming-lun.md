---
title: Intrusively Linked Lists with Safe Link Destruction | Ming-Lun "Allen" Chou
  | 周明倫
url: https://allenchou.net/2013/07/intrusively-linked-lists-with-safe-link-destruction/
author: Allen Chou
published: '2013-07-23'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Programming Series](http://allenchou.net/game-programming-series/).

My current game project at [DigiPen](https://www.digipen.edu) greatly benefits from “smart” intrusively linked lists that support **multiple links per object** and **automatic link removal** from lists upon destruction. My implementation was inspired by Patrick Wyatt’s [implementation](https://github.com/webcoyote/coho/blob/master/Base/List.h) and [Randy Gaul](http://www.randygaul.net/)‘s implementation. Randy showed me both implementations.

The implementation I’m going to present here is probably not the most efficient, but it is STL-compatible in terms of **iterators**, and it can be used with the [ranged-based for loop](http://en.cppreference.com/w/cpp/language/range-for) introduced in C++11. Such implementation has turned out to be very convenient while writing client code, and has never become a performance bottleneck for me.

### Traditional V.S. Intrusively Linked Lists

First, let’s go over a quick overview of intrusively linked list and its comparison with traditional linked lists.

Below is a very straightforward implementation of a traditional doubly linked list node:

template <typename T> struct ListNode { ListNode *prev, *next; T data; };

A link to the previous node, and link to the next node, and the data, simple. However, this implementation breaks down when we want to have the same data in multiple linked lists. This is a very common situation in a game engine; for instance, game objects are kept in a main game object list, as well as in a “to-be-destroyed” list that contains game objects that are marked for destruction at the end of current frame, so that we don’t have to loop through the (possibly very long) main list for a second time to check which game objects are marked for destruction at the end of each frame.

A fix to this problem using the traditional linked list is to make the node data a pointer, which points to the real data.

template <typename T> { ListNode *prev, *next; T *data; };

This brings up another problem: we can’t perform a constant-time node removal just by giving the data pointer to all the lists that contain it, because the actual data object and the nodes are de-coupled. Also, when the data is deleted from memory, we have to know which lists contain pointers to this data and remove the corresponding nodes beforehand. Too much bookkeeping. Yuck.

The solution to these problems is, you guessed it, intrusively linked lists.


### Our Goal

As its name suggests, intrusively linked lists “intrusively” embed links into data objects, but we’ll go into the details later. Let’s take a quick look at what the client code would look like if we used intrusively linked lists. The code below uses macros for list and node declarations as a syntactical sugar. I’ll explain the macros later.

// GameObject is the "host type" of the nodes struct GameObject { // intrusively linked list nodes LIST_LINK(GameObject) mainLink; LIST_LINK(GameObject) deadLink; string name; map<ComponentID, Component *> components; GameObject(string const &name) : name(name) { } }; // two lists LIST(GameObject, mainLink) mainList; LIST(GameObject, deadLink) deadList; // create game objects GameObject *obj1 = new GameObject("object1"); GameObject *obj2 = new GameObject("object2"); GameObject *obj3 = new GameObject("object3"); // add game object to main lists mainList.push_back(obj1); mainList.push_back(obj2); mainList.push_back(obj3); // just add object 1 & 3 to dead list // in reverse order deadList.push_back(obj3); deadList.push_back(obj1); // use range-based for loop to delete objects // no need to remove from main list // because it is automatically handled // as will be shown later for (auto &obj : deadList) delete &obj;

### The Interface

**Link Interface**

I put a pointer to the owning list inside the link class, so the link can update the list size. This list pointer can also come in handy for debugging and various assertions. It can be removed if you don’t need it.

// forward declaration template <typename T> class List; // forward declaration template <typename T> struct ListIterator; // forward declaration template <typename T> struct ListConstIterator; // list link interface template <typename T> struct ListLink { public: ListLink(void); ~ListLink(void); // inserts link between two links void Link(ListLink *prev, ListLink *next); // unlinks link from list void Unlink(void); private: // these classes need to access private data members friend class List<T>; friend struct ListIterator<T>; friend struct ListConstIterator<T>; ListLink *m_prev, *m_next; List<T> *m_list; };

**Iterator Interface**

And here’s the interface for the iterator. It’s pretty standard: increment/decrement operators, dereference operators, and comparison operators. I decided to copy the link offset into the iterator from the list, instead of storing a pointer back to the list, so no indirection is needed when it needs to access the link offset. Nevertheless, having a pointer back to the list can be useful for debugging, so you can choose to selectively include such information using debug configuration defines.

// iterator interface template <typename T> struct ListIterator { public: ListIterator ( unsigned linkOffset = 0, ListLink<T> *link = nullptr ); T &operator* (void) const; T *operator->(void) const; ListIterator &operator++(void); ListIterator &operator--(void); ListIterator operator++(int); ListIterator operator--(int); bool operator==(const ListIterator &rhs) const; bool operator!=(const ListIterator &rhs) const; private: // list needs to access private data members friend class List<T>; unsigned m_linkOffset; ListLink<T> *m_link; };

**List Interface**

Last but not least, the interface for the intrusively linked list. They `typedef`

s and the `begin`

/`end`

/`cbegin`

/`cend`

methods are what make this interface STL-compatible. For simplicity’s sake, I omitted some other methods such as `pop_front`

, `pop_back`

, `insert_before`

, and `insert_after`

. The use of dummy head and tail links makes it very easy to implement iterators.

template <typename T> class List { public: // STL-compatible iterator typedefs typedef ListIterator<T> iterator; typedef ListConstIterator<T> const_iterator; List(unsigned linkOffset = 0); ~List(void); void push_back (T *obj); void push_front(T *obj); iterator erase(T *obj); iterator erase(iterator obj); void clear(void); unsigned size(void) const; // STL-compatible range methods iterator begin(void); iterator end (void); const_iterator begin (void) const; const_iterator end (void) const; const_iterator cbegin(void) const; const_iterator cend (void) const; private: // these classes need to access private data members friend struct ListLink<T>; friend struct ListIterator<T>; friend struct ListConstIterator<T>; // memory offset of links into host type const unsigned k_linkOffset; // dummy links ListLink<T> m_head; ListLink<T> m_tail; unsigned m_size; };

### The Implementation

**Helper Functions**

For convenience, here are two helper functions that convert between host type pointers and link pointers using the memory offset.

template <typename T> ListLink<T> *GetLinkFromObj(T *obj, unsigned linkOffset) { return reinterpret_cast<ListLink<T> *> ( reinterpret_cast<char *>(obj) + linkOffset ); } template <typename T> T *GetObjFromLink(ListLink<T> *link, unsigned linkOffset) { return reinterpret_cast<T *> ( reinterpret_cast<char *>(link) - linkOffset ); }

**Link Constructor & Destructor**

The link constructor basically initializes everything to null, and the link destructor handles the removal of the link from the owning list.

template <typename T> ListLink<T>::ListLink(void) : m_prev(nullptr) , m_next(nullptr) , m_list(nullptr) { m_prev = m_next = this; } template <typename T> ListLink<T>::~ListLink(void) { Unlink(); }

**Link Methods**

The `Link`

and `Unlink`

methods are just standard doubly linked list pointer manipulation. Note these two methods update the list size. The size update cannot be put in the list methods, because the list has no idea when the link’s `Unlink`

method is going to be called.

template <typename T> void ListLink<T>::Link(ListLink *prev, ListLink *next) { // update prev link prev->m_next = this; this->m_prev = prev; // update next link next->m_prev = this; this->m_next = next; // update list pointer m_list = next->m_list; // update list size ++m_list->m_size; } template <typename T> void ListLink<T>::Unlink(void) { if (m_list) { // update links m_prev->m_next = m_next; m_next->m_prev = m_prev; // update list size --m_list->m_size; // clean up pointers m_list = nullptr; m_prev = m_next = nullptr; } }

**List Constructor**

The list constructor links the dummy head and tail links together, and the list destructor clears the links.

template <typename T> List<T>::List(unsigned linkOffset) : k_linkOffset(linkOffset) , m_size(0) { m_head.m_next = &m_tail; m_tail.m_prev = &m_head; m_head.m_list = m_tail.m_list = this; } template <typename T> List<T>::~List(void) { clear(); }

**List Manipulation**

The `push`

methods delegate the push operation to the link’s `Link`

method. Similarly, the omitted `pop`

methods would use the link’s `Unlink`

method. The `erase`

method returns an iterator that points to the link next to the erased link, following the STL convention.

template <typename T> void List<T>::push_back(T *obj) { push_back(GetLinkFromObj(obj, k_linkOffset)); } template <typename T> void List<T>::push_front(T *obj) { push_front(GetLinkFromObj(obj, k_linkOffset)); } template <typename T> void List<T>::push_back(ListLink<T> *link) { link->Link(m_tail.m_prev, &m_tail); } template <typename T> void List<T>::push_front(ListLink<T> *link) { link->Link(&m_head, m_head.m_next); } template <typename T> typename List<T>::iterator List<T>::erase(T *obj) { ListLink<T> *link = GetLinkFromObj(obj, k_linkOffset); if (link == nullptr) return iterator(0, nullptr); iterator next(k_linkOffset, link->m_next); link->Unlink(); return next; } template <typename T> typename List<T>::iterator List<T>::erase(typename List<T>::iterator iter) { ListLink<T> *link = iter.m_link; if (link == nullptr) return iterator(0, nullptr); iterator next(k_linkOffset, link->m_next); link->Unlink(); return next; } template <typename T> void List<T>::clear(void) { while (m_head.m_next != &m_tail) { m_head.m_next->Unlink(); } }

**List Iterators**

The list’s iterator methods make use of the dummy head and tail links to yield expected `begin`

and `end`

behaviors. The `begin`

methods should return iterators pointing at the first link, which is one next to the dummy head link; the `end`

methods should return iterators pointing at the one-past-last link, which is the dummy tail link. This is why I said dummy links are convenient.

template <typename T> typename List<T>::iterator List<T>::begin(void) { return iterator(k_linkOffset, m_head.m_next); } template <typename T> typename List<T>::iterator List<T>::end(void) { return iterator(k_linkOffset, &m_tail); } template <typename T> typename List<T>::const_iterator List<T>::begin(void) const { return const_iterator (k_linkOffset, const_cast<ListLink<T> *>(m_head.m_next)); } template <typename T> typename List<T>::const_iterator List<T>::end(void) const { return const_iterator (k_linkOffset, const_cast<ListLink<T> *>(&m_tail)); } template <typename T> typename List<T>::const_iterator List<T>::cbegin(void) const { return const_iterator (k_linkOffset, const_cast<ListLink<T> *>(m_head.m_next)); } template <typename T> typename List<T>::const_iterator List<T>::cend(void) const { return const_iterator (k_linkOffset, const_cast<ListLink<T> *>(&m_tail)); }

**Iterator Methods**

The iterator implementation is pretty trivial compared to what has been shown so far, so I’ll let the code speak for itself. The implementation for `ListConstIterator`

is almost identical, only with different `const`

ness.

template <typename T> ListIterator<T>::ListIterator(unsigned linkOffset, ListLink<T> *link) : m_linkOffset(linkOffset) , m_link(link) { } template <typename T> T &ListIterator<T>::operator*(void) const { return *GetObjFromLink(m_link, m_linkOffset); } template <typename T> T *ListIterator<T>::operator->(void) const { return GetObjFromLink(m_link, m_linkOffset); } template <typename T> ListIterator<T> &ListIterator<T>::operator++(void) { m_link = m_link->m_next; return *this; } template <typename T> ListIterator<T> &ListIterator<T>::operator--(void) { m_link = m_link->m_prev; return *this; } template <typename T> ListIterator<T> ListIterator<T>::operator++(int) { ListIterator copy = *this; ++*this; return copy; } template <typename T> ListIterator<T> ListIterator<T>::operator--(int) { ListIterator copy = *this; --*this; return copy; } template <typename T> bool ListIterator<T>::operator==(const ListIterator &rhs) const { return m_link == rhs.m_link; } template <typename T> bool ListIterator<T>::operator!=(const ListIterator &rhs) const { return !operator==(rhs); }

### Helper Macros

With the above implementation, if we were to attempt to write the client code shown above (far, far above), then it’d turn out to be something like this:

// GameObject is the "host type" of the nodes struct GameObject { // intrusively linked list nodes ListNode<GameObject> mainLink; ListNode<GameObject> deadLink; string name; map<ComponentID, Component *> components; GameObject(string const &name) : name(name) { } }; // two lists List<GameObject> mainList(offsetof(GameObject, mainLink)); List<GameObject> deadlist(offsetof(GameObject, deadLink));

Here we’re using the `offsetof`

macro to determine the memory offset of the links into the host type. It works, but each list declaration involves typing the host type twice and a long macro expression. So here we’re going to declare a helper class template and a macro to create some syntactical sugar.

#define LIST(HostType, LinkName) \ ListDecl<HostType, offsetof(HostType, LinkName)> template <typename T, unsigned LinkOffset> class ListDecl : public List<T> { public: ListDecl(void) : List(LinkOffset) { } };

Even though the link declaration isn’t that long, but for consistency’s sake, here’s the macro for link declaration.

#define LIST_LINK(HostType) ListLink<HostType>

There you have it. Nice syntactical sugar.

// GameObject is the "host type" of the nodes struct GameObject { // intrusively linked list nodes LIST_LINK(GameObject) mainLink; LIST_LINK(GameObject) deadLink; string name; map<ComponentID, Component *> components; GameObject(string const &name) : name(name) { } }; // two lists LIST(GameObject, mainLink) mainList; LIST(GameObject, deadLink) deadList;

### Caveats

**Circular Dependency**

The use of `offsetof`

macro requires complete declaration of the host type, not just a forward declaration. This might result in circular dependency. If such scenario cannot be avoided, the only solution is to fall back to using the ugly list declaration in header files, and “manually” initialize the link’s memory offset in source files using the `offsetof`

macro.

**Copy Constructors**

The auto-generated copy constructor of the link’s host type would in turn call the auto-generated copy constructor of the link class, which would copy the `prev`

and `next`

points. This is not a desirable behavior, so we should make the link class non-copyable by declaring the copy constructor private, or inherit from a non-copyable mixin class.

Thank you very much

Why the iterator methods:

ListIterator &operator++(void);

ListIterator &operator–(void);

ListIterator operator++(int);

ListIterator operator–(int);

The last two do not return references, instead they return a copy, why? (Just because have to follow stl style?)

Nope, this has nothing to do with STL compliance. The latter two methods are the postfix increment and decrement operators (e.g. i++, i–). Postfix operators return values BEFORE the increment/decrement, so a copy is needed.

Is that cbegin and cend methods in the List class should be rbegin and rend?

Short answer: Nope.

Long answer: According to STL convention,

`cbegin`

and`cend`

return constant iterators (`const_iterator`

), which evaluate to constant reference (`const T &`

) when dereferenced.`rbegin`

and`rend`

return reverse iterators (`reverse_iterator`

), which act as iterator but iterate the collection backwards. The constant version of`rbegin`

and`rend`

are`crbegin`

and`crend`

, respectively.