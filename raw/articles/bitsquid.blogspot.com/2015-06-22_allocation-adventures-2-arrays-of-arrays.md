---
title: 'Allocation Adventures 2: Arrays of Arrays'
url: https://bitsquid.blogspot.com/2015/06/allocation-adventures-2-arrays-of-arrays.html
author: Niklas
published: '2015-06-22'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

[Last week's post](http://bitsquid.blogspot.se/2015/06/allocation-adventures-1-datacomponent.html) ended with a puzzle: How can we allocate an array of dynamically growing and shrinking things in an efficient and data-oriented way? I.e. using contiguous memory buffers and as few allocations as possible.

The example in that post was kind of complicated, and I don't want to get lost in the details, so let's look at a simpler version of the same fundamental problem.

Suppose we want to create a `TagComponent`

that allows us to store a number of `unsigned`

*tags* for an entity.

These *tags* will be hashes of strings such as `"player"`

, `"enemy"`

, `"consumable"`

, `"container"`

, etc and the `TagComponent`

will have some sort of efficient lookup structure that allows us to quickly find all entities with a particular tag.

But to keep things simple, let's ignore that for now. For now we will just consider how to store these lists of tags for all our entities. I.e. we want to find an alternative to:

`std::vector< std::vector < unsigned> > data;`


that doesn't store every list in a separate memory allocation.

## Fixed size

If we can get away with it, we can get rid of the "array of arrays" by setting a hard limit on the number of items we can store per entity. In that case, the data structure becomes simply:

```
enum {MAX_TAGS = 8};
struct Tags
{
unsigned n;
unsigned tags[MAX_TAGS];
};
Array<Tags> data;
```


Now all the data is contained in a single buffer, the data buffer for `Array<Tags>`

.

Sometimes the hard limit is inherent in the problem itself. For example, in a 2D grid a cell can have at most four neighbors.

Sometimes the limit is a widely accepted compromise between cost and quality. For example, when skinning meshes it is usually consider ok to limit the number of bone influences per vertex to four.

Sometimes there is no sensible limit inherent to the problem itself, but for the particular project that we are working on we can agree to a limit and then design the game with that limit in mind. For example we may know that there will never be more than two players, never more than three lights affecting an object, never more than four tags needed for an entity, etc.

This of course requires that we are writing, or at least configuring, the engine for a particular project. If we are writing a general engine to be used for a lot of games it is hard to set such limits without artificially constraining what those games will be able to do.

Also, since the fixed size must be set to the maximum array size, every entity that uses fewer entries than the maximum will waste some space. If we need a high maximum this can be a significant problem and it might make sense to go with a dynamic solution even though there is an upper limit.

So while the fixed size approach can be good in some circumstances, it doesn't work in every situation.

## Linked list

Instead of using arrays, we can put the tags for a particular entity in a linked list:

```
struct Tag
{
unsigned tag;
Tag *next;
};
Array<Tag *> data;
```


Using a linked list may seem like a very bad choice at first. A linked list can give us a cache miss for every `next`

pointer we follow. This would give us even worse performance than we would get with `vector < vector < unsigned > >`

.

But the nodes in the linked list do not necessarily have to be allocated individually on the heap. We can do something similar to what we did in the last post: allocate the nodes in a buffer and refer to them using offsets rather than pointers:

```
struct Node
{
unsigned tag;
unsigned next;
};
Array<Node> nodes;
```


With this approach we only have a single allocation -- the buffer for the array that contains all the tag nodes -- and we can follow the indexes in the `next`

field to walk the list.

**Side note:** Previously I have always used `UINT_MAX`

to mark an *nil* value for an `unsigned`

. So in the struct above, I would have used `UINT_MAX`

for the `next`

value to indicate the end of the list. But recently, I've switched to using `0`

instead. I think it is nice to be able to `memset()`

a buffer to `0`

to reset all values. I think it is nice that I can just use `if (next)`

to check if the value is valid. It is also nice that the invalid value will continue to be `0`

even if I later decide to change the type to `int`

or `uint_16t`

. It does mean that I can't use the `nodes[0]`

entry, since that is reserved for the `nil`

value, but I think the increased simplicity is worth it.

Using a single buffer rather than separate allocations gives us much better cache locality, but the `next`

references can still jump around randomly in that buffer. So we can still get cache misses. If the buffer is large, this can be as bad as using freely allocated nodes.

Another thing to note is that we are wasting a significant amount of memory. Only half of the memory is used for storing tags, the rest of it is wasted on the `next`

pointers.

We can try to address both these problems by making the nodes a little bigger:

```
enum {MAX_TAGS_PER_NODE = 8};
struct Node
{
unsigned n;
unsigned tags[MAX_TAGS_PER_NODE];
unsigned next;
};
Array<Node> nodes;
```


This is just as before, except we have more than one tag per node. This gives better cache performance because we can now process eight tags at a time before we have to follow a next pointer and jump to a different memory location. Memory use can also be better. If the nodes are full, we are using 80 % of the memory for actual tags, rather than 50 % as we had before.

However, if the nodes are *not* full we could be wasting even more memory than before. If entities have three tags on average, then we are only using 30 % of the memory to store tags.

We can balance cache performance and memory use by changing `MAX_TAGS_PER_NODE`

. Increasing it gives better cache coherence, because we can process more tags before we need to jump to a different memory location. However, increasing it also means more wasted memory. It is probably good to set the size so that "most entities" fit into a single node, but a few special ones (players and enemies maybe) need more.

One interesting thing to note about the cache misses is that we can get rid of them by sorting the nodes. If we sort them so that the nodes in the same `next`

chain always appear directly after one another in the array, then walking the list will access the data linearly in memory, just as if we were accessing an array:

```
--------------------------------------------------
| A1 --|--> A2 --|--> A3 | B | C1 --|--> C2 |
--------------------------------------------------
```


Note that a complete ordering is not required, it is enough if the linked nodes end up together. Single nodes, such as the `B`

node above could go anywhere.

Since these are dynamic lists where items will be added and removed all the time, we can't really do a full `O(n log n)`

sort every time something changes. That would be too expensive. But we could sort the list "incrementally". Every time the list is accessed, we do a little bit of sorting work. As long as the rate of mutation is low compared to the rate of access, which you would expect in most circumstances, our sorting should be able to keep up with the mutations and keep the list "mostly sorted".

You would need a sorting algorithm that can be run incrementally and that works well with already sorted data. Two-way bubble sort perhaps? I haven't thought too deeply about this, because I haven't implemented this method in practice.

## Custom memory allocator

Another option is to write a custom memory allocator to divide the bigger buffer up into smaller parts for memory allocations.

You might think that this is a much too complex solution, but a custom memory allocator doesn't necessarily need to be a complex thing. In fact, both the *fixed size* and *linked list* approaches described above could be said to be using a very simple kind of custom memory allocator: one that just allocates fixed blocks from an array. Such an allocator does not need many lines of code.

Another criticism against this approach is that if we are writing our own custom memory allocator, aren't we just duplicating the work that `malloc()`

or `new`

already does? What's the point of first complaining a lot about how problematic the use of `malloc()`

can be and then go on to write our very own (and probably worse) implementation of `malloc()`

?

The answer is that `malloc()`

is a generic allocator that has to do well in a lot of different situations. If we have more detailed knowledge of how the allocator is used, we can write an allocator that is both simpler and performs better. For example, as seen above, when we know the allocations are fixed size we can make a very fast and simple allocator. System software typically uses such allocators (check out the [slab allocator](https://en.wikipedia.org/wiki/Slab_allocation) for instance) rather than relying on `malloc()`

.

In addition, we also get the benefit that I talked about in the previous post. Having all of a system's allocations in a single place (rather than mixed up with all other `malloc()`

allocations) makes it much easier to reason about them and optimize them.

As I said above, the key to making something better than `malloc()`

is to make use of the specific knowledge we have about the allocation patterns of our system. So what is special about our `vector < vector < unsigned > >`

case?

**1. There are no external pointers to the data.**

All the pointers are managed by the `TagComponent`

itself and never visible outside that component.

This means that we can "move around" memory blocks as we like, as long as the `TagComponent`

keeps track of and updates its data structures with the new locations. So we don't have to worry (that much) about fragmentation, because when we need to, we can always move things around in order to defrag the memory.

I'm sure you can build something interesting based on that, but I actually want to explore another property:

**2. Memory use always grows by a factor of two.**

If you look at the implementation of `std::vector`

or a [similar class](https://bitbucket.org/bitsquid/foundation/src/7f896236dbafd2cb842655004b1c7bf6e76dcef9/array.h?at=default) (since STL code tends to be pretty unreadable) you will see that the memory allocated always grows by a factor of two. (Some implementations may use 1.5 or something else, but usually it is 2. The exact figure doesn't matter that much.)

The `vector`

class keeps track of two counters:

`size`

which stores the number of items in the`vector`

and`capacity`

which stores how many items the`vector`

has*room for*, i.e. how much memory has been allocated.

If you try to push an item when `size == capacity`

, more memory is needed. So what typically happens is that the `vector`

allocates twice as much memory as was previously used (`capacity *= 2`

) and then you can continue to push items.

This post is already getting pretty long, but if you haven't thought about it before you may wonder why the `vector`

grows like this. Why doesn't it grow by one item at a time, or perhaps 16 items at a time.

The reason is that we want `push_back()`

to be a cheap operation -- O(1) using computational complexity notation. When we reallocate the vector buffer, we have to move all the existing elements from the old place to the new place. This will take O(n) time. Here, *n* is the number of elements in the vector.

If we allocate one item at a time, then we need to allocate every time we push and since re-allocate takes O(n) that means push will also take O(n). Not good.

If we allocate 16 items at a time, then we need to allocate every 16th time we push, which means that push on average takes O(n)/16, which by the great laws of O(n) notation is still O(n). Oops!

But if we allocate 2*n items when we allocate, then we only need to reallocate after we have pushed *n* more items, which means that push on average takes O(n)/n. And O(n)/n is O(1), which is exactly what we wanted.

Note that it is just *on average* that push is O(1). Every *n* pushes, you will encounter a push that takes O(n) time. For this reason, push is said to run in *amortized constant time*. If you have really big vectors, that can cause an unacceptable hitch and in that case you may want to use something other than a `vector`

to store the data.

Anyways, back to our regular programming.

The fact that our data (and indeed, any kind of dynamic data that uses the `vector`

storage model) grows by powers of two is actually really interesting. Because it just so happens that there is an allocator that is very good at allocating blocks at sizes that are powers of two. It is called the [buddy allocator](https://en.wikipedia.org/wiki/Buddy_memory_allocation) and we will take a deeper look at it in the next post.

While reading this and the previous post a question came to my mind...

ReplyDeleteDo you design your engine with an assumption that components are an internal concept, or do you allow game-specific components?

DragonComponent, or just "beast" tag in TagComponent and "dragon.fire_power" in DataComponent?

The system is extensible so games will be able to create their own C components.


ReplyDeleteBut there will also be "flexible" components, like DataComponent, ScriptComponent and FlowComponent that you can use to implement dynamic game-specific behaviour without having to write your own component on the C side.

Pure C, or did something eat two pluses?

DeleteOur plugin interface is C based (C++ does not have a stable ABI), but of course the C callbacks in your DLL could call out to C++ functions.

DeleteI know that probably you can't use modern C++ in your work, but you could check out my `multivector` class, that implements a dynamic struct of arrays, providing vector-like programming interface. I'm interested in your opinions.


ReplyDeletehttps://github.com/cubuspl42/Nete/blob/cf654bfc88875b97f1e31ffcf7a6987cbdc1e663/tests/nete_tl_tests.cpp

I'm not a huge fan of modern C++. It's such an extremely complicated langauge. I find it hard to read, hard to debug and the compile errors are obtruse.





DeleteFor me, when I try to achieve a specific low-level effect, all these C++ abstractions get in the way. I find it hard to know if the compiler is really optimizing everything properly the way I expect wihtout checking the assembly output. Something is wrong if you find yourself reading assembly code when you are programming in a supposedly high-level langauge.

It's too easy to miss something and get bitten by it. For example we had a significant performance hit because we used vector for temporary buffers, and the char's were being initialized on every resize.

To me, being C like and using direct pointer manipulations is simpler, faster and less error prone.

Thank you very much for your reply. I agree with you, abstraction often get into programmer's way and the code of classes like `std::vector` (or my `multivector`) is relatively complicated, due to its nature. On the other hand, code like this:





Deletechar *buffer = allocate(capacity * (sizeof(unsigned) + sizeof(DataType) + sizeof(Value));

keys = (unsigned *)buffer;

types = (DataType *)(keys + capacity);

values = (Value *)(types + capacity);

is quite readable... but isn't it bug-prone? Every class that needs struct-of-arrays storage needs to write this again and again. And how does this code handle alignment? What if you need dynamic expansion? If it sums up, wouldn't it justify writing an universal template class for that? It could have an option for not initializing trivial types, too. Aren't consoles' outdated compilers the real reason for not writing such classes?

Yes, it is bug-prone boiler plate code. It sucks. It does not make me happy.





DeleteBut at least it is transparent. If there is a bug I can look at it and quite quickly figure out what is going on. The performance characteristics are plain to see. If it is slow I can see why and fix it. To me readability and simplicity are the most important things, because it makes the code easy to work with. And code is never static, there are always new bugs, new features, new performance improvements, new hardware characteristics, new compilers, new things to push.

Today you have to add initialization skipping to your class. Tomorrow maybe you have to add serialization/deserialization, or "reusing" slots so you can delete entries without changing the indices of other entries... or something else.

I don't believe in creating "perfect" library classes that cover every use case but are unreadable by anyone other than C++ experts. I've seen horrorshows like Singleton classes that have six boolean "traits" for things like is it thread-safe or not, etc. Congratulations you have taken a very simple thing (singleton) and made a complex monstrosity out of it. Instead, I believe in things that are "hackable".

My dream language would be C with a small & simple template engine on top so you could avoid boiler plate like this and extend the langauge freely. But sadly, that dream is not C++.

This comment has been removed by the author.

ReplyDeleteAs expert plumbing technicians, we are the finest response to your query for ‘Plumbers Near Me’. Speak to us and leave your plumbing worries to us for the best care.


ReplyDeleteWelcome to My Blog

ReplyDeletejinglebellrun.org/

thehonorsgolfclubdallas.com/

google 3489

ReplyDeletegoogle 3490

google 3491

google 3492

google 3493

Pretty nice post. I just stumbled upon your weblog and wanted to say that I have really enjoyed browsing your blog posts. After all I’ll be subscribing to your feed and I hope you write again soon!สล็อตออนไลน์

ReplyDeleteI just want to let you know that I just check out your site and I find it very interesting and informative..สล็อตแตกง่าย

ReplyDeleteThis article gives the light in which we can observe the reality. This is very nice one and gives indepth information. Thanks for this nice article.บา คา ร่า วอ เลท

ReplyDeleteYou have a good point here!I totally agree with what you have said!!Thanks for sharing your views...hope more people will read this article!!!บา คา ร่า วอ เลท

ReplyDeleteMost of the time I don’t make comments on websites, but I'd like to say that this article really forced me to do so. Really nice post!บาคาร่าวอเลท

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteYou’ve got some interesting points in this article. I would have never considered any of these if I didn’t come across this. Thanks!.เว็บตรงสล็อต

ReplyDeleteIt was a very good post indeed. I thoroughly enjoyed reading it in my lunch time. Will surely come and visit this blog more often. Thanks for sharing.เว็บ ตรง

ReplyDeleteThanks for sharing this quality information with us. I really enjoyed reading. Will surely going to share this URL with my friends.เกมสล็อต

ReplyDeleteJOKER123 ฝากถอนไม่มีขั้นต่ำ ทางเข้าJoker123 Auto สล็อตออนไลน์ ระบบอัตโนมัติ


ReplyDeleteสล็อตออนไลน์ ระบบอัตโนมัติ ฝาก-ถอน ผ่านหน้าเว็บ สมัครฟรี ไม่มีค่าบริการ และยังมีเกมให้ท่านได้เลือกเล่นมากกว่า 30 ค่าย สนใจสมัคร คลิกที่นี่ สล็อตPP

I think you've made some truly interesting points.Keep up the good work. I would like to thank you for the สมัครบาคาร่า efforts you have made in writing this article. I am hoping the same best work from you in the future as well. Thanks

ReplyDelete진안출장안마

ReplyDelete무주출장안마

장수출장안마

임실출장안마

순창출장안마

고창출장안마

부안출장안마

서울출장안마

고흥콜걸

ReplyDelete구례콜걸

곡성콜걸

광양콜걸

담양콜걸

나주콜걸

순천콜걸

여수콜걸

I’m so glad I read this! The tips were very helpful.

ReplyDelete