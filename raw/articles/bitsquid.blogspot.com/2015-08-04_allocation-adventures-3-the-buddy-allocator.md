---
title: 'Allocation Adventures 3: The Buddy Allocator'
url: https://bitsquid.blogspot.com/2015/08/allocation-adventures-3-buddy-allocator.html
author: Niklas
published: '2015-08-04'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

## Hello, allocator!

The job of a memory allocator is to take a big block of memory (from the OS) and chop it up into smaller pieces for individual allocations:

```
void *A = malloc(10);
void *B = malloc(100);
void *C = malloc(20);
------------------------------------------------------
| A | free | B | C | free |
------------------------------------------------------
```


The allocator needs to be fast at serving an allocation request, i.e. finding a suitable piece of free memory. It also needs to be fast at *freeing* memory, i.e. making a previously used piece of memory available for new allocations. Finally, it needs to prevent *fragmentation* -- more about that in a moment.

Suppose we put all free blocks in a linked list and allocate memory by searching that list for a block of a suitable size. That makes allocation an O(n) operation, where *n* is the total number of free blocks. There could be thousands of free blocks and following the links in the list will cause cache misses, so to make a competitive allocator we need a faster method.

*Fragmentation* occurs when the free memory cannot be used effectively, because it is chopped up into little pieces:

```
------------------------------------------------------
| A | free | B | C | free |
------------------------------------------------------
```


Here, we might not be able to service a large allocation request, because the free memory is split up in two pieces. In a real world scenario, the memory can be fragmented into thousands of pieces.

The first step in preventing fragmentation is to ensure that we have some way of *merging* free memory blocks together. Otherwise, allocating blocks and freeing them will leave the memory buffer in a chopped up state where it is unable to handle any large requests:

```
-------------------------------------------------------
| free | free | free | free | free | free |
-------------------------------------------------------
```


Merging needs to be a quick operation, so scanning the entire buffer for adjacent free blocks is not an option.

Note that even if we merge all neighboring free blocks, we can still get fragmentation, because we can't merge the free blocks when there is a piece of allocated memory between them:

```
-----------------------------------------------------------
| free | A | free | B | free | C | free | D | free |
-----------------------------------------------------------
```


Some useful techniques for preventing this kind of fragmentation are:

- Use separate allocators for long-lived and short-lived allocations, so that the short-lived allocations don't create "holes" between the long lived ones.
- Put "small" allocations in a separate part of the buffer so they don't interfere with the big ones.
- Make the memory blocks relocatable (i.e. use "handles" rather than pointers).
- Allocate whole pages from the OS and rely on the page mapping to prevent fragmentation.

The last approach can be surprisingly efficient if you have a small page size and follow the advice suggested earlier in this series, to try to have a few large allocations rather than many small ones. On the other hand, a small page size means more TLB misses. But maybe that doesn't matter so much if you have good data locality. Speculation, speculation! I should provide some real numbers instead, but that is too much work!

Three techniques used by many allocators are *in-place linked lists*, *preambles* and *postambles*.

*In-place linked lists* is a technique for storing linked lists of free memory blocks without using any extra memory. The idea is that since the memory in the blocks is free anyway, we can just store the `prev`

and `next`

pointers directly in the blocks themselves, which means we don't need any extra storage space.

A *preamble* is a little piece of data that sits just before the allocated memory and contains some information about that memory block. The allocator allocates extra memory for the preamble and fills it with information when the memory is allocated:

```
void *A = malloc(100);
------------------------
| pre | A | post|
------------------------
```


In C we pretty much need to have a preamble, because when the user calls `free(void *p)`

on a pointer `p`

, we get no information about how big the memory block allocated at `p`

is. That information needs to come from somewhere and a preamble is a reasonable option, because it is easy to access from the `free()`

code:

```
struct Preamble
{
unsigned size;
...
};
void free(void *p)
{
Preamble *pre = (Preamble *)p - 1;
unsigned size = pre->size;
}
```


Note that there are other options. We could use a hash table to store the size of each pointer. We could reserve particular areas in the memory buffer for allocations of certain sizes and use pointer compare to find the area (and hence the size) for a certain pointer. But hash tables are expensive, and having certain areas for allocations of certain sizes only really work if you have a limited number of different sizes. So preambles are a common option.

They are really annoying though. They increase the size of all memory allocations and they mess with alignment. For example, suppose that the user wants to allocate 4 K of memory and that our OS uses 4 K pages. Without preambles, we could just allocate a page from the OS and return it. But if we need a four byte preamble, then we will have to allocate 8 K from the OS so that we have somewhere to put those extra four bytes. So annoying!

And what makes it even more annoying is that in *most* cases storing the size is pointless, because the caller *already knows it*. For example, in C++, when we do:

```
delete x;
```


The runtime *knows* the actual type of *x*, because otherwise it wouldn't be able to call the destructor properly. But since it knows the type, it knows the size of that type and it could provide that information to the allocator when the memory is freed..

Similarly, if the memory belongs to an `std::vector`

, the vector class has a `capacity`

field that stores how big the buffer is, so again the size is known.

In fact, you could argue that whenever you have a pointer, *some part* of the runtime *has to know* how big that memory allocation is, because otherwise, how could the runtime use that memory without causing an access violation?

So we could imagine a parallel world where instead of `free(void *)`

we would have `free(void *, size_t)`

and the caller would be required to explicitly pass the size when freeing a memory block. That world would be a paradise for allocators. But alas, it is not the world we live in.

(You could enforce this parallel world in a subsystem, but I'm not sure if it is a good idea to enforce it across the board in a bigger project. Going against the grain of the programming language can be painful.)

A *postamble* is a similar piece of data that is put at the *end* of an allocated memory block.

Postambles are useful for merging. As mentioned above, when you free a memory block, you want to merge it with its free neighbors. But how do you know what the neighbors are and if they are free or not?

For the memory block to the right it is easy. That memory block starts where yours end, so you can easily get to it and check its preamble.

The neighbor to the left is trickier. Since you don't know how big that memory block might be, you don't know where to find its preamble. A postamble solves that problem, since the postamble of the block to the left will always be located just before your block.

Again, the alternative to using preambles and postambles to check for merging is to have some centralized structure with information about the blocks that you can query. And the challenge is to make such queries efficient.

If you require all allocations to be 16-byte aligned, then having both a preamble and a postamble will add 32 bytes of overhead to your allocations. That is not peanuts, especially if you have many small allocations. You can get around that by using slab or block allocators for such allocations, or even better, avoid them completely and try to make fewer and bigger allocations instead, as already mentioned in this series.

## The buddy allocator

With that short introduction to some general allocation issues, it is time to take a look at the *buddy allocator*.

The buddy allocator works by repeatedly splitting memory blocks in half to create two smaller "buddies" until we get a block of the desired size.

If we start with a 512 K block allocated from the OS, we can split it to create two 256 K buddies. We can then take one of those and split it further into two 128 K buddies, and so on.

When allocating, we check to see if we have a free block of the appropriate size. If not, we split a larger block as many times as necessary to get a block of a suitable size. So if we want 32 K, we split the 128 K block into 64 K and then split one of those into 32 K.

At the end of this, the state of the allocator will look something like this:

```
Buddy allocator after 32 K allocation:
-----------------------------------------------------------------
512 | S |
-----------------------------------------------------------------
256 | S | F |
-----------------------------------------------------------------
128 | S | F |
---------------------------------
64 | S | F | S - split
----------------- F - free
32 | A | F | A - allocated
---------
```


As you can see, this method of splitting means that the block sizes will always be a powers of two. If you try to allocate something smaller, say 13 K, the allocation will be rounded up to the nearest power of two (16 K) and then get assigned a 16 K block.

So there is a significant amount of fragmentation happening here. This kind of fragmentation is called *internal* fragmentation since it is wasted memory inside a block, not wasted space between the blocks.

Merging in the buddy allocator is dead simple. Whenever a block is freed, we check if it's buddy is also free. If it is, we merge the two buddies back together into the single block they were once split from. We continue to do this recursively, so if this newly created free block *also* has a free buddy, they get merged together into an even bigger block, etc.

The buddy allocator is pretty good at preventing *external* fragmentation, since whenever something is freed there is a pretty good chance that we can merge, and if we can't the "hole" should be filled pretty soon by a similarly sized allocation. You can still imagine pathological worst-case scenarios. For example, if we first allocate every leaf node and then free every other of those allocations we would end up with a pretty fragmented memory. But such situations should be rare in practice.

```
Worst case fragmentation, 16 K block size
-----------------------------------------------------------------
512 | S |
-----------------------------------------------------------------
256 | S | S |
-----------------------------------------------------------------
128 | S | S | S | S |
-----------------------------------------------------------------
64 | S | S | S | S | S | S | S | S |
-----------------------------------------------------------------
32 | S | S | S | S | S | S | S | S | S | S | S | S | S | S | S | S |
-----------------------------------------------------------------
16 |A|F|A|F|A|F|A|F|A|F|A|F|A|F|A|F|A|F|A|F|A|F|A|F|A|F|A|F|A|F|A|F|
-----------------------------------------------------------------
```


I'm being pretty vague here, I know. That's because it is quite hard in general to say something meaningful about how "good" an allocator is at preventing fragmentation. You can say how good it does with a certain allocation pattern, but every program has a different allocation pattern.

## Implementing the buddy allocator

Articles on algorithms and data structures are often light on implementation details. For example, you can find tons of articles describing the high-level idea behind the buddy allocator as I've outlined it above, but not much information about how to implement the bloody thing!

This is a pity, because the implementation details can really matter. For example, it's not uncommon to see someone carefully implement the A*-algorithm, but using a data structure for the `open`

and `closed`

sets that completely obliterates the performance advantages of the algorithm.

So let's get into a bit more detail.

We start with allocation. How can we find a free block of a requested size? We can use the technique described above: we put the free blocks of each size in an implicit linked list. To find a free block we just take the first item from the list of blocks of that size, remove it from the list and return it.

If there is no block of the right size, we take the block of the next higher size and split that. We use one of the two blocks we get and put the other one on the free list for that size. If the list of blocks of the bigger size is also empty, we can go to the even bigger size, etc.

To make things easier for us, let's introduce the concept of *levels*. We say that the single block that we start with, representing the entire buffer, is at *level 0*. When we split that we get two blocks at *level 1*. Splitting them, we get to *level 2*, etc.

We can now write the pseudocode for allocating a block at level *n*:

```
if the list of free blocks at level n is empty
allocate a block at level n-1 (using this algorithm)
split the block into two blocks at level n
insert the two blocks into the list of free blocks for level n
remove the first block from the list at level n and return it
```


The only data structure we need for this is a list of pointers to the first free block at each level:

```
static const int MAX_LEVELS = 32;
void *_free_lists[MAX_LEVELS];
```


The `prev`

and `next`

pointers for the lists are stored directly in the free blocks themselves.

We can also note some mathematical properties of the allocator:

```
total_size == (1<<num_levels) * leaf_size
size_of_level(n) == total_size / (1<<n)
max_blocks_of_level(n) = (1<<n)
```


Note that `MAX_LEVELS = 32`

is probably enough since that gives a total size of `leaf_size * 4`

GB and we know `leaf_size`

will be at least 16. (The leaf nodes must have room for the `prev`

and `next`

pointers of the linked list and we assume a 64 bit system.)

Note also that we can create a unique index for each block in the buddy allocator as `(1<<level) + index_in_level - 1`

. The node at level 0 will have index 0. The two nodes at level 1 will have index 1 and 2, etc:

```
Block indices
-----------------------------------------------------------------
512 | 0 |
-----------------------------------------------------------------
256 | 1 | 2 |
-----------------------------------------------------------------
128 | 3 | 4 | 5 | 6 |
-----------------------------------------------------------------
64 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
-----------------------------------------------------------------
32 |15 |16 |17 |18 |19 |20 |21 |22 |23 |24 |25 |26 |27 |28 |29 |30 |
-----------------------------------------------------------------
```


The total number of entries in the index is `(1 << num_levels) - 1`

. So if we want to store some data per block, this is how much memory we will need. For the sake of simplicity, let's ignore the `- 1`

part and just round it of as `(1 << num_levels)`

.

What about deallocation?

The tricky part is the merging. *Doing* the merging is simple, we just take the two blocks, remove them from the free list at level *n* and insert the merged block into the free list at level *n-1*.

The tricky part is to know *when* we should merge. I.e. when we are freeing a block `p`

, how do we know if it is buddy is also free, so that we can merge them?

First, note that we can easily compute the address of the buddy. Suppose we have free a block `p`

at level `n`

. We can compute the index of that in the level as:

```
index_in_level_of(p,n) == (p - _buffer_start) / size_of_level(n)
```


If the index `i`

is even, then the buddy as at index `i+1`

and otherwise the buddy is at `i-1`

and we can use the formula above to solve for the pointer, given the index.

So given the address of the buddy, let's call it `buddy_ptr`

, how can we know if it is free or not? We could look through the free list for level `n`

. If we find it there we know it is free and otherwise it's not. But there could be thousands of blocks and walking the list is hard on the cache.

To do better, we need to store some kind of extra information.

We could use preambles and postambles as discussed earlier, but that would be a pity. The buddy allocator has such nice, even block sizes: 1 K, 2 K, 4 K, we really don't want to mess that up with preambles and postambles.

But what we *can* do is to store a bit for each block, telling us if that block is free or allocated. We can use the block index as described above to access this bitfield. This will require a total of `(1 << num_level)`

bits. Since the total size of the tree is `(1 << num_levels) * leaf_size`

bytes, we can see that the overhead of storing these extra bits is `1 / 8 / leaf_size`

. With a decent `leaf_size`

of say 128 (small allocations are better handled by a slab alloactor anyway) the overhead of this table is just 0.1 %. Not too shabby.

But in fact we can do even better. We can get by with just half a bit per block. That sounds impossible, but here is how:

For each pair of buddies `A`

and `B`

we store the single bit `is_A_free XOR is_B_free`

. We can easily maintain the state of that bit by flipping it each time one of the buddies is freed or allocated.

When we consider making a merge we *know* that one of buddies is free, because it is only when a block has just been freed that we consider a merge. This means we can find out the state of the other block from the XORed bit. If it is 0, then both blocks are free. If it is 1 then it is just our block that is free.

So we can get by with just one bit for every pair of blocks, that's half a bit per block, or an overhead of just `1 / 16 / leaf_size`

.

At this point, careful readers may note that I have been cheating.

All this time I have assumed that we *know* the level `n`

of the block that we are freeing. Otherwise we cannot compute the address of the buddy or its index in the node tree.

But to know the level `n`

of `ptr`

we must know the size of its allocated block. So this only really works if the user passes the size of the allocation when freeing the block. I.e, the `free(void *, size_t)`

interface that we discussed earlier.

If we want to support the simpler and more common API `free(void *p)`

, the alloator needs to somehow store the size of each alloation.

Again, using a preamble is possible, but we don't really want to.

We could use an array, indexed by `(p - _buffer_start) / leaf_size`

to store the sizes. Note that this is not the same as the block index. We can't use the block index, since we don't know the level. Instead this is an index of size `1 << (num_levels - 1)`

with one entry for each possible pointer that the buddy allocator can return.

We don't have to store the full size (32 bits) in the index, just the level. That's 5 bits assuming that `MAX_LEVELS = 32`

. Since the number of entries in this index is half that of the block index this ammounts to 2.5 bits per block.

But we can do even better.

Instead of storing the size explicitly, we can use the block index and store a single bit to keep track of whether the block at that level has been split or not.

To find the level *n* of an allocated block we can use the algorithm:

```
n = num_levels - 1
while n > 0
if block_has_been_split(ptr, n-1)
return n
n = n - 1
return 0
```


Since the leaf blocks can't be split, we only need `1 << (num_levels - 1)`

entries in the split index. This means that the cost of the split index is the same as for the merge index, 0.5 bits per block. It's a bit amazing that we can do all this with a total overhead of just 1 bit per block.

The prize of the memory savings is that we now have to loop a bit to find the allocated size. But `num_levels`

is usually small (in any case <= 32) and since we only have 1 bit per entry the cache usage is pretty good. Furthermore, with this approach it is easy to offer both a `free(void *)`

and a `free(void *, size_t)`

interface. The latter can be used by more sophisticated callers to avoid the loop to calculate the block size.

### Memory arrangements

Where do we store this 1 bit of metadata per block? We could use a separate buffer, but it is not that elegant. It would mean that our allocator would have to request two buffers from the system, one for the data and one for the metadata.

Instead, let's just put the metadata in the buffer itself, at the beginning where we can easily find it. We mark the blocks used to store the metadata as allocated so that they won't be used by other allocations:

```
Initial state of memory after reserving metadata:
-----------------------------------------------------------------
512 | S |
-----------------------------------------------------------------
256 | S | F |
-----------------------------------------------------------------
128 | S | F |
---------------------------------
64 | S | S |
-----------------
32 | S | S | S | F |
-----------------
16 |A|A|A|A|A|F|
-------------
********** Metadata
```


Note that when allocating the metadata we can be a bit sneaky and not round up the allocation to the nearest power of two. Instead we just take as many leaf blocks as we need. That is because when we allocate the metadata we know that the allocator is completely empty, so we are guaranteed to be able to allocate adjacent leaf blocks. In the example above we only have to use 5 * 16 = 80 K for the metadata instead of the 128 K we would have used if we rounded up.

(The size of the metadata has been greatly exaggerated in the illustration above to show this effect. In reality, since the tree in the illustration has only six levels, the metadata is just 1 * (1 << 6) = 64 bits, that's 8 bytes, not 80 K.)

Note that you have to be a bit careful when allocating the metadata in this way, because you are allocating memory for the metadata that your memory allocation functions depend on. That's a chicken-and-egg problem. Either you have to write a special allocation routine for this initial allocation, or be very careful with how you write your allocation code so that this case is handled gracefully.

We can use the same technique to handle another pesky issue.

It's a bit irritating that the size of the buddy allocator has to be a power of two of the leaf size. Say that we happen to have 400 K of memory lying around somewhere. It would be really nice if we could use *all* of that memory instead of just the first 256 K.

We can do that using the same trick. For our 400 K, we can just create a 512 K buddy allocator and mark the first 144 K of it as "already allocated". We also offset the start of the buffer, so that the start of the usable memory coincides with the start of the buffer in memory. Like this:

```
-----------------------------------------------------------------
512 | S |
-----------------------------------------------------------------
256 | S | F |
-----------------------------------------------------------------
128 | S | S |
---------------------------------
64 | S | S | S | F |
---------------------------------
32 | S | S | S | S | S | F |
-------------------------
16 |A|A|A|A|A|A|A|A|A|A|
---------------------
******************* Unusable, unallocated memory
MET * Metadata
^
+-- Usable memory starts here
```


Again, this requires some care when writing the code that does the initial allocation so that it doesn't write into the unallocated memory and causes an access violation.

## The buddy allocator and growing buffers

As mentioned in the previous post, the buddy allocator is perfect for allocating dynamically growing buffers, because what we want there is allocations that progressively double in size, which is exactly what the different levels of the buddy allocator offer.

When a buffer needs to grow, we just allocate the next level from the buddy allocator and set the capacity of the buffer so that it fills up all that space.

Note that this completely avoids the internal fragmentation issue, which is otherwise one of the biggest problems with the buddy allocator. There will be no internal fragmentation because the dynamic buffers will make use of all the available space.

In the next post, I'll show how all of this ties together.

Hi Niklas,










ReplyDeleteGreat post!

Coincidentally I was thinking about exactly the same setup recently (buddy allocators + vector style capacity increases), and was planning to blog about this, but I think you've covered this better than I would, and you're really spot on with a lot of the detail points here.

I'm really looking forward to the next post, where you actually integrate this with vectors.

As I see it there are basically two ways this could be handled:

* give vectors a fatter memory interface so that they can use this to take advantage of space that would otherwise be wasted as 'internal fragmentation'

or

* set things up so that the vector size increments happen to fall on your available memory buffer sizes

I was thinking along the lines of the first approach, based on the idea that the often used *2 or *1.5 capacity multipliers are actually pretty arbitrary. So I was thinking that a vector could say something like 'give me a bit of memory in this size range' where the size range corresponds to something like a capacity increase of between *1.2 and *2.5 (figures also chosen pretty arbitrarily, but this gives you a pretty good range).

But it sounds like you went for the other option (arrange for the vector capacity increments to match your memory sizes), and after reading your post I think that this is probably the best way to go. Not requiring any additional non-standard memory interface is definitely a big plus..

Nice post as usual. These are things I've thought about before but never wrote down or tried to take any serious steps forward with.



ReplyDeleteBy the way, congrats on the public release today :)

Working smoothly on my desktop. Hopefully they'll eventually give me source access, even though I'm mostly a solo dev. (Applied for it a while ago, but never heard back)

delete x; // the runtime might not know the real object type/size without RTTI/virtual_dtor

ReplyDeleteAlso c++ allows to delete a pointer of an incomplete type (thankfully some compilers provide a warning for this which can be enforced as an error)

DeleteI'm curious. What would be some good situations to use a custom allocator for PC development? And what systems should it be limited to? I've been thinking of implementing it... but I honestly curious about how devoted I should be to using it.

ReplyDeleteNowadays the linux kernel uses the heap allocator in user-space, but otherwise uses (SLAB,SLUB) allocator in kernel-space. Also user-space and kernel-space allocator preventing both external and internal fragmentation.

DeleteThat was really a great idea u have shared.It was really helpful and thanks a lot !!


ReplyDeleteWeb Development company in USA

Internet Marketing services in USA

I’d constantly want to be update on new content on this website, bookmarked! Personally, I have found that to get just about the most fascinating topics if this draws a parallel to. A well written article.



ReplyDeleteDental Website Designand Marketing 4 Dentists - OptimiZed360 #1 Web Design Company for Doctors in the USA.I have only a single question: Is the Buddy allocator a good choice for big size memory allocations? e.g. Is ok to manage a 50/100 MB memory block with this allocator?

ReplyDeleteWhy not store the free list for each level as a dynamic array? If you're just treating the list as a stack then there's no reason not to, right? Walking an array isn't hard on the cache at all.

ReplyDeleteHey, I’m David. I’m a web developer living in New York. I am a fan of technology, web development, and fashion. I’m also



ReplyDeleteinterested in writing and photography. You can visit my company website with a click on the button above.

geeksquad.com

geek squad tech support





ReplyDeleteGeek squad tech support

Geek squad tech support

Call us at our Southwest Customer Service and let us know all your issues. Our travel agents will answer all your questions. Our aviation experts will be happy to help you

ReplyDeleteOperating all the 24×7 on our Southwest Airlines Customer Service phone number we make sure that when we book any seat for our calling customers we book it with the cheapest airfare as well as the greatest discounts across any class, route, and segment of Southwest airlines.

ReplyDeleteWe are a very trusted travel agency on the planet. Call our Allegiant Airlines Toll Free Number 24 * 7 is open. So just book flights and take the toll-free number one step further with our Allegiant Airlines Toll Free Number.

ReplyDeleteOur experts are available on 24 * 7 in there. Contact American Airlines Cancellation with the latest best deals and offers in a simple way. Grab the opportunity to travel pocket-friendly for your life; Get the major discounts available to offer your dream trip.

ReplyDeleteWe feel that we can make money by making our customers happy so that’s why we have a team of professionals for you to resolve all your problems. Whenever you feel need you can connect anytime with our experts by dialling Etihad Airways Contact Number . Etihad Airways not only give you 24x7 available services but also offers you great deals and discounts for your vacations.

ReplyDeleteGet unmatched Geek Squad Tech Support by our experts 24/7. Get the best help for your gadgets with geek squad tech support or for any related queries right on the call.

ReplyDeleteWe work at Allegiant Airlines Toll Free Number provide the best deals and discounts on each flight ticket booked. Dial

ReplyDeleteAllegiant Airlines Toll Free Numberand get excellent guidance and support. Contact experts now to learn more about packages and offers.Find the cheapest flight on a

ReplyDeleteUnited Phone Number, and set yourself up for free. We welcome you with open arms and serve you in the best possible ways. Major Service 24 * 7 is available here in touch with our United Phone Number.If you are not using any antivirus you need to install www.norton.com/setup antivirus which protects your data,files,windows,devices if you want to install it you can visit our website http://safe-norton.com/ our technical assistance provide yo the complete information regarding the same.

ReplyDeleteI read your post, it was interesting and worth sharing. Being of an online growing community, I want to share you some best ways travel with Delta Airlines. For cheap tickets reach to


ReplyDeleteDelta Airlines Customer Serviceand speak to the agents, They will book your tickets instantly through Delta Airlines Customer Service Number.Make your vacation bigger and memorable through Book a Flight with Spirit Airlines Team and avail ample of services in less rates.


ReplyDeleteI read your blog, it was interesting and worth sharing. Being of an online growing community, I want to share you some best ways travel with Delta Airlines. For great deals and offers reach

ReplyDeleteDelta Airlines Reservationshelpdesk and speak to the agents, They will book the tickets instantly through Delta Airlines Reservations Phone Number.InsuranceAdvisor avails you the

ReplyDeleteCorporate Health Insurancewhich covers and protects the employees of any company. For best options and plans, contact 24/7.


ReplyDeleteModify your journey details according to your new itinerary with Hawaiian Airlines Manage Booking service. So change your details as per your requirements.

CrownQQ Agen DominoQQ BandarQ dan Domino99 Online Terbesar









ReplyDeleteYuk Buruan ikutan bermain di website CrownQQ

Sekarang CROWNQQ Memiliki Game terbaru Dan Ternama loh...

9 permainan :

=> Poker

=> Bandar Poker

=> Domino99

=> BandarQ

=> AduQ

=> Sakong

=> Capsa Susun

=> Bandar 66

=> Perang Baccarat (NEW GAME)

=> Bonus Refferal 20%

=> Bonus Turn Over 0,5%

=> Minimal Depo 20.000

=> Minimal WD 20.000

=> 100% Member Asli

=> Pelayanan DP & WD 24 jam

=> Livechat Kami 24 Jam Online

=> Bisa Dimainkan Di Hp Android0619679319

=> Di Layani Dengan 5 Bank Terbaik

=> 1 User ID 9 Permainan Menarik

Ayo gabung sekarang juga hanya dengan

mengklick CrownQQ

Link Resmi CrownQQ:

ratuajaib.com

ratuajaib.net

BACA JUGA BLOGSPORT KAMI:

Agen BandarQ Terbaik

Daftar CrownQQ

Agen Poker Online

Info Lebih lanjut Kunjungi :

WHATSAPP : +855882357563

Line : CS CROWNQQ

Facebook : CrownQQ Official

I am a family person and we all know that saving money for a family person is very difficult. One day I was searching some travelling sites then I got Lufthansa Airlines. When I dialed their


ReplyDeleteLufthansa Airlines Phone NumberI got amazing deals and discounted tickets even with best facilities. So without thinking too much I booked my tickets and I also enjoyed travelling with them.I am a traveller and I like to explore new places, I heard about Southwest Airlines a lot. So when I dialed



ReplyDeleteSouthwest Airlines Customer ServiceI got the flight tickets with best deals and offers which maybe I cannot get from anywhere. I want to travel with them next time too.I tried to avail the services at United Airlines and also got the best experience. With the easy procedures of cancelling a flight ticket when talking


ReplyDeleteUnited Airlines cancellation number, I got to travel and enjoy myself to make my trip hassle free. Thank you for this experience!تاینی موویز


ReplyDeleteدانلود آهنگ جدید

دانلود آهنگ مهستی

دانلود آهنگ قدیمی

دانلود آهنگ

دانلود آهنگ خارجی

دانلود آهنگ



ReplyDeleteWhile QuickBooks has easy-to-use features to maximize online accounting for your business, call QuickBooks Customer Service Number for the best guidance.

professional treatments provide long-lasting effects in comparison to homely methods. Get best-customized solutions for your property through Pest Control Everett WA Services.



ReplyDeleteWhen you spot or suspect a pest around or inside your property, it’s better to contact an expert Pest Control Miami FL service provider. It’s really tough to control pests activities with bug-killer spray as these chemicals can be very dangerous for your property and health.

ReplyDelete


ReplyDeleteAre looking for an effecting, long-lasting, and affordable solution for your rodent infestation problem? Contact ABC Rodent Exterminator and get the best Rodent Exterminator service.


ReplyDeleteSouthwest Customer Serviceexpert team is available for 24 hours a day or night. Feel free to call to connect throughSouthwest Airlines Customer Service. Here at Southwest Airlines are constantly working to make your journey very easy.du hoc canada vnsava




ReplyDeleteChuyên du học Canada Công ty tư vấn du học Canada nào tốt

Điều kiện du học Canada 2021

Học bổng du học Canada vnsava

vnsava

Thông tin du học Canada mới nhất

vnsava

Chính sách du học Canada 2020

vnsava

Du học Canada bao nhiêu tiền Việt

Học bổng du học Canada 2020

vnsava

Du học Canada 2020

Nhất ký du học Canada

vnsava

Du học Canada nên học ngành gì

công ty tư vấn du học Canada vnsava, chính sách điều kiện định cư Canada, học bổng, chi phí, điều kiện xin visa canada

#vnsava

@vnsava

vnsava

vnsava

vnsava

Our whole travel teams are working on

ReplyDeleteSouthwest Airlines Customer Servicefor 24*7 hours and offering to travel user advantage every time.Visit now

ReplyDeleteLufthansa Contact Numberto get wonderful trip plan from here.


ReplyDeleteTo be honest I found very helpful information your blog thanks for providing us such blogMore Worry For The Bowlers

That an amazing post. Yellowstone Coat

ReplyDelete123.hp.com/dj2600 - Follow the below steps to setup hp deskjet 2600 wireless setup ... Wireless connection with router using Wi-Fi Protected Setup

ReplyDelete


ReplyDeleteSnapdeal winner list 2020here came up with a list of offers where you can win specialSnapdeal winner nameandSnapdeal winner name 2020by just playing a game & winning prizes.Thanks for sharing this post. But, pests nowadays are a big problem. People suffer a lot of pests at home and office. We can get you the best price and quotes with


ReplyDeleteRansford Pest Control. If you want to contact them, reach their at toll free number for instant help.Joker Jackets

ReplyDeletethriller jacket

batman jacket

A well written Content provided by you. Your writing skills are perfect avianca airlines. i hope so avianca airlines flights you will write more content like this but if you are searching for flights then contact us or visit our website.

ReplyDeleteA well written Content provided by you. Your writing skills are perfect. i hope so you will cheap flights to canada offical site write more content like this but if you are searching for flights then contact us or visit our website.

ReplyDeleteI appericiate your comments i want to share that flights to denver Get all data about the flight booking of at the brisk and proficient helpline helping a large number of travelers.

ReplyDeleteThis blog has got all the thing I was searching for. Much obliged to you for sharing. Would i be able to inquire as to whether you think about your flights bookings visit us at:-flights to america

ReplyDeleteAmazing content your information through this blog is helpful to me i appericiate ur content i want to share regarding airlines reservation if u want to book flight tickets visit at:-cheap flights to canada

ReplyDeleteThanx for sharing this content i appericiate this type o knowlege if u want to book flights visit at :-deals2travel

ReplyDeleteI appericiate your comments i want to share that Get all data about the flight booking of flights to canada at the brisk and proficient helpline helping a large number of travelers.

ReplyDeleteAwesome to see your site. Keep up the great work. Thanks for all you could do.Lets stay in touch


ReplyDeleteWorldwide Medical Diagnostic Imaging Market 2020 Report Explores Key Regions, Company Profile, Opportunity and Challenge to 2025

Hey, thank you a lot for sharing this article with us. I can’t say, how grateful we are to read this


ReplyDeletePaints and Coatings Market Robust Pace of Industry during 2021-2026

you done a good job and also provide wonderful information for the visitors.


ReplyDeleteMitsubishi Heavy Industries sets out to commercialise the use of CO2 carriers

Fantastic article! I will definitely share this with my siblings.


ReplyDeleteCannabis Testing Industry Size study, result Type

Suggest good information in this message, click here.

ReplyDeleteไก่ชนอินเตอร์

เล่นสล็อต เวลาไหน

This is a great piece of blog you wrote about memory allocation and you are right 'Implementing the buddy allocator' is need of an hour and should be talked more often.

ReplyDeleteoffice.com/setup

office.com/setup

office.com/setup

office.com/setup and follow the on-screen instructions

office.com/setup

We're working to fix the issues that may comes up when using Office,We are here 24/7 to get instant help & support.

ReplyDeleteoffice.com/setup

microsoft365.com/setup

office setup

<a href = "https://office-setup-com.us/microsoft-365/office.com/renew</a>

google 3077

ReplyDeletegoogle 3078

google 3079

google 3080

google 3081

google 3082

www.google.com/url?q=https://www.littlescholar.school/blog/


ReplyDeleteNicely written, Enjoy reading, Thanks for writing informational content.




ReplyDeleteCheers

Amara

Preschool in Newark CA







ReplyDeleteHow to make Yahoo my homepage on Windows 10?Instances occur when you search for how to make Yahoo my homepage on Windows 10. To go about it, you need to select More on the address bar, then go to Settings. Under Open with, choose A specific page or pages. Select one of the default options or select Custom to enter the URL of another page you'd like to see each time you open the browser. Choose the plus button to save.

Also Read:-yahoo mail not syncing

yahoo mail not working on iphone

how to remove yahoo search from chrome

pop.verizon.net not working

The Best Stock broker compares and reviews


ReplyDeletebest Trading Platforms in IndiaStock Market. You will get the Best Trading Platform in India which is an important requirement for trading.This comment has been removed by the author.

ReplyDeleteWant to know about top 10 best trading apps in India? Here is a list of trading apps with reviews and ratings, choose best out of them.

ReplyDeleteThanks for sharing this knowledgeable post. What an excellent post and outstanding blog. Thanks for your awesome topic . Really I got very valuable information here. To resolve Spectrum Email Not Working Problem please contact our team for instant help.

ReplyDeleteAs we know Microsoft Office is a big software and sometimes users encounter some problems while trying to set up an office and we have already uploaded various articles on how to fix those errors and easily install office on one's Pc/Mac or any other device which is supported by Microsoft


ReplyDeleteoffice.com/setup

office.com/setup

office.com/setup

office.com/setup

Find a Next Intraday stock tips . Here you get a stock which is ... We help traders with market direction and trading strategies. With our stock alerts you.

ReplyDeleteThis is the first time that I visit here. I found so many exciting matters in this particular blog, One thing I would like to request you that pls keep posting such type of informative blog

ReplyDeletekavinsky jacket

Hello, we have a game to recommend.



ReplyDeleteทางเข้า ufabet

ufabet kick

รูเล็ตสายฟ้า

แทง บอล ผ่าน มือ ถือ

กา บอล1

Thank you for your interest."

I’m happy by reading your enjoyable article, Keep uploading more interesting articles like this Faux Jacket - Mens Vest

ReplyDeleteSharetipsinfo is known for providing highly accurate Indian stock market tips which covers Cash tips, F&O intraday tips, Nifty intraday tips, Mcx intraday commodity tips and Share market tips with high accuracy.

ReplyDeletepest control in pune & Services is a professionally managed pest control company aiming to better the environment and create better living conditions without any stress. Poona Pest Managment & Services has stringent norms to enforce quality pest control services that have lasting effects. Our pest treatment leave the desired effect on effective problem remediation by us.

ReplyDeletedownload learn Free Digital markting app

digoital marketing

Thank you for providing us with important information. It is quite beneficial to me. I always like to read high-quality information, such as the one in your article. Thanks for sharing your knowledge with us Georgina Campbell Jacket

ReplyDeleteThanks for permitting me to comment! Dollface Stella Cole Jacket

ReplyDeleteExcellent article.


ReplyDeletestranger things s04 Chrissy hoodie

This is quite interesting. I am so glad that you have shared this amazing blog post. Halloween Jackets for Men

ReplyDeleteDarchiteriors is a one-stop interior designing & architecture solutions provider for all your décor needs. For more info visit our website https://www.darchiteriors.in/ or make a call @+91-8882135895 for any query.


ReplyDeleteRegards

Best Interior designer in Vasundhara

Upstox is a top-rated discount brokerage firm in India that offers commission-free trading in stocks, futures, options, and currencies. With its user-friendly interface and advanced charting tools, Upstox is a great choice for novice traders. Read more in this Upstox review

ReplyDeleteThe best stock broker in India offers unparalleled trading services, combining cutting-edge technology with comprehensive market insights. They empower investors to make informed decisions with user-friendly platforms, competitive pricing, and a wide range of investment options. Here find the top 10 stock brokers in India.


ReplyDelete

ReplyDeleteFascinating journey into the Buddy Allocator in Allocation Adventures 3! Your exploration adds depth to understanding this crucial aspect. Thanks for the insightful! if you're interested in details on best paper trading apps, feel free to explore more.

Gain a comprehensive understanding of the stock market and trading by consulting with the most reputable best stock advisor in India.

ReplyDeleteWhen it comes to


ReplyDeleteLasik surgery austinis a top destination for those looking to improve their vision. This innovative procedure utilizes laser technology to reshape the cornea, resulting in clearer vision without the need for glasses or contact lenses. Austin boasts a plethora of reputable clinics and hospitals that specialize in LASIK surgery, ensuring that patients receive the highest quality care and achieve optimal results.Whether you're a local resident or considering traveling to Austin for this procedure, you can rest assured knowing that the city's medical professionals are at the forefront of this field.

Your post on the buddy allocator tool is fascinating! For those interested in optimizing resources, it’s also worth noting that there are vehicle assistance programs available through Cars for Your Help. These programs can be a game-changer for individuals in need of reliable transportation, especially if you're managing multiple allocations or projects. They offer support to help with acquiring vehicles, which can significantly improve access and efficiency. Thanks for sharing such insightful content!









ReplyDeleteThe discussion about buddy allocators and their impact is really intriguing! It’s fascinating to see how different systems handle resource distribution. On a related note, for single mothers in need of financial assistance, grants for single moms by Help Single Mother can offer significant support. These grants are designed to help single mothers manage their finances and achieve their goals, providing a much-needed boost. It’s great to see resources like this making a real difference in people’s lives!









ReplyDeleteIf you're in need of


ReplyDeletemobile repair near meservices, finding a reliable technician in your vicinity can greatly enhance your experience. Numerous local shops specialize in addressing a variety of issues, from cracked screens to battery replacements, ensuring that your device is restored to optimal condition.Searching online or utilizing map applications can help pinpoint the nearest repair centers, allowing you to read reviews and compare services. Many establishments also offer quick turnaround times, often fixing devices while you wait, so you can get back to your daily routine without significant disruption.

Digitechworx truly lives up to its name as the best digital marketing company in India. Their strategies are innovative, result-driven, and tailored perfectly to our brand’s unique goals and audience.


ReplyDeletebest digital marketing company in india

This content was exactly what I needed today. Your posts are always packed with practical value — keep it up!


ReplyDeleteDubai City Sightseeing