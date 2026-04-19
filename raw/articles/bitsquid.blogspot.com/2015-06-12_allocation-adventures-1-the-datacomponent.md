---
title: 'Allocation Adventures 1: The DataComponent'
url: https://bitsquid.blogspot.com/2015/06/allocation-adventures-1-datacomponent.html
author: Niklas
published: '2015-06-12'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

When sketching out a new low level system I always start with the data layout, because that's the most important part. And I do that with two main goals:

- Make sure that memory is laid out and accessed linearly.
- Minimize the number of individual memory allocations.

The importance of the first goal should be obvious to anybody who has been following the data-oriented design movement. Modern CPUs are often memory bound. Writing cache friendly code is paramount. Etc.

The advantages of the second goal are less obvious.

Too some extent, it goes hand-in-hand with the first. For the cache to work efficiently you need to avoid pointer chasing, which naturally leads to fewer allocations. But there are other advantages as well.

Data with fewer individual allocations puts less pressure on the memory system. It gives you less fragmentation, more control over memory usage, allocation patterns that are easier to profile and optimize, etc.

It also makes the data easier to move and copy, since it requires less pointer patching, which let's you do lots of cool tricks with it. In general, it's just *neater*.

For static data, such as resources loaded from disk, both these goals can be easily achieved, by using the [blob method](http://bitsquid.blogspot.se/2010/02/blob-and-i.html).

For dynamic data, things get trickier. If you just use STL as you are told to, you end up with scary stuff like `std::map< std::string, std::vector<std::string> >`

where the cache and memory usage is all over the place.

So let's try and see how we can escape that monster's lair by looking at a component and improving it step-by-step until we get to something nicer.

## Introducing the `DataComponent`


The `DataComponent`

is a part of our entity system that is used to store small amounts of arbitrary dynamic data for an entity. For example, it can be used to store a character sheet:

```
name = "The One"
stats = {
health = 100
mana = 200
}
status_effects = {
drunk = true
delirious = true
}
```


As data format we use a restricted form of JSON where the only allowed values are:

- booleans
- floats
- strings
- objects
- arrays of numbers

Note that arbitrary arrays are not allowed. Arrays can only be lists of numbers, i.e. `[0 0.5 0.5 0.7]`

. If you want to have sets of other items, you need to use an object with unique values (possibly GUIDs) as the keys.

The reason for these restrictions is that we want to make sure that all operations on the data merge in simple and well-defined ways. This makes it easier to use the data in collaborative workflows.

Strings and float arrays are regarded as monolithic with respect to merging. This means that all data operations can be reduced to setting object keys, which makes them easy to reason about.

We assume that the amount of data stored for each entity will be small, but that lots of entities will have data and that it is important to keep memory use low and performance high.

## The naive approach

Representing a tree structure that can include both strings and arrays is pretty complicated and if we just start to sketch the structure using our regular STL tools it quickly becomes pretty messy:

```
enum class DataType {BOOL, FLOAT, STRING, OBJECT, ARRAY};
struct DataValue
{
DataType type;
union {
bool b;
float f;
std::string *s;
std::vector<float> *array;
std::map<std::string, DataValue> *object;
};
};
```


That doesn't look very fun at all. There are tons of allocations everywhere, both explicit (`std::string *`

) and implicit (inside `string`

, `vector`

, and `map`

). So let's start working.

## 1: Hash the keys

If we consider how we will use this data structure, we will always be setting and getting the values corresponding to certain keys. We don't have a pressing need to extract the key strings themselves. This means we can use hashed strings instead of the strings themselves for lookup.

Since we assume that the number of keys will be small, it is probably enough to use an `unsigned`

rather than an `uint64_t`

for the hash value:

`std::map<unsigned, DataValue> *object;`


Great start. That's a lot of allocations already gone and as a bonus we also got rid of a lot of string comparisons.

## 2: Flatten the structure

If we also sacrifice the ability of being able to enumerate all the (hashed) keys in a particular object we can go even further and flatten the entire structure.

That is, instead of representing the data as:

```
name = "The One"
stats = {
health = 100
mana = 200
}
status_effects = {
drunk = true
delirious = true
}
```


We will use:

```
name = "The One"
stats.health = 100
stats.mana = 200
status_effects.drunk = true
status_effects.delirious = true
```


Just as before we represent these keys as hashed values, so `"stats.health"`

is represented by an `unsigned`

containing the hashed value of `"stats.health"`

.

(Note: we won't actually hash the string `"stats.health"`

directly, because that could lead to problems if some of our keys contained a `"."`

character. Instead we hash each sub key separately and then hash them all together.)

With this approach, the user will still be able to look up a particular piece of data, such as `stats.health`

, but she won't be able to enumerate all the keys and values under `stats`

, since the hierarchy information is lost. But that's ok.

Getting rid of the tree structure allows us to store our data in a flat array:

```
enum class DataType {BOOL, FLOAT, STRING, OBJECT, ARRAY};
struct Entry
{
unsigned key;
DataType type;
union {
bool b;
float f;
std::string *s;
std::vector<float> *array;
};
};
std::vector<Entry> data;
```


Note that we no longer have a lookup hierarchy for the entries. To find a particular key we have to linearly search `std::vector<Entry>`

for a match. Luckily, linear search is the best thing caches know and for reasonable sizes, the search will run faster than a `std::map`

lookup.

We could sort the entries and do a binary search, but since the number of entries will be small, it is probably not even worth bothering.

## 3: Rewrite using a structure-of-arrays approach

One thing that *does* slow the search for a particular key down is all the additional data we need to load into the cache to perform the search. As we scan the vector for a particular key, the cache will also be filled by the *type* and *value* data.

We can solve this with the standard techinque of rewriting our "array of structures" as a "structure of arrays". I.e., we break out each field of the structure into its own array:

```
enum class DataType {BOOL, FLOAT, STRING, OBJECT, ARRAY};
struct Value
{
union {
bool b;
float f;
std::string *s;
std::vector<float> *array;
}
};
std::vector<unsigned> keys;
std::vector<DataType> types;
std::vector<Value> values;
```


Now when searching for a particular key, we only need to load the `keys`

table which means the cache only contains useful data.

## 4: Co-allocate the arrays

Not too shabby, but we still have three separate allocations for the three vectors. To get rid of that we have to stop using these fancy `std::vector`

s and go back to the basics, and in terms of basics, a `std::vector<unsigned>`

is really just:

```
struct {
int capacity;
int size;
unsigned *data;
};
```


So we can represent our three vectors as:

```
int capacity;
int size;
unsigned *keys;
DataType *types;
Value *values;
```


Note that as a bonus, we can now share the capacity and the size fields between the vectors, since they all have the same values and change together.

The arrays are also all reallocated at the same time. We can make use of this and instead of doing three separate allocations, we just allocate one big buffer and lay them out sequentially in that buffer:

```
-----------------------------------
buffer | keys | types | values |
-----------------------------------
```


Which in code would be something like:

```
char *buffer = allocate(capacity * (sizeof(unsigned) + sizeof(DataType) + sizeof(Value));
keys = (unsigned *)buffer;
types = (DataType *)(keys + capacity);
values = (Value *)(types + capacity);
```


Presto, now we have all the header data stored in a single buffer.

## 5: Get rid of STL

We still have these pointers to deal with in the values union:

```
std::string *s;
std::vector<float> *array;
```


Let's start by getting rid of those STL types. At this point they are no longer helping. STL is based around individual allocations which we don't want. We also have two levels of indirection there. First, the pointer to the `std::vector`

, and then the pointer to the actual `data`

inside the `std::vector`

type.

So, we just replace them with their non-STL equivalents:

```
struct {
char *data;
} s;
struct {
int capacity;
int size;
float *data;
} array;
```


This actually bloats the size of the `Value`

union from 64 to 128 bits, which is less than stellar, but have faith, we are going in the right direction.

## 6: Put the value data in a buffer

We can now repeat the same trick that we did with the header data and put all the strings and float arrays in a big single buffer:

```
-------------------------------------------------------------
| "hello" | [0 1 3] | "mana" | [0 2] | ... unused space ... |
-------------------------------------------------------------
```


To allocate some data we just keep track of this buffer and how much of it is currently in use:

```
struct value_buffer
{
char *p;
unsigned capacity;
unsigned size;
};
void *allocate_memory(value_buffer &vb, unsigned size)
{
if (vb.size + size > vb.capacity)
return nullptr;
auto res = vb.p + vb.size;
vb.size += size;
return res;
}
```


There are two things we need to take care of here. First, we may run out of space in this buffer as we add more data. Second, the individual values we store may change size and no longer fit in their designated place.

The first issue is no big problem. If we run out of space, we can just allocate a bigger buffer as `std::vector`

does.

The second issue is no biggie either. If an item needs to grow, we just allocate a new bigger slot for it from the buffer. This will leave a hole where the item was originally located:

```
-------------------------------------------------------------
| ....... | [0 1 3] | "mana" | [0 2] | "hello more" | ..... |
-------------------------------------------------------------
```


These "holes" will cause fragmentation of the buffer and eventually make it run out of space. If this was a general purpose memory allocator that would be a serious issue that we would have to be seriously worried about.

But in our case it doesn't really matter. The number of items is small and we control the pointers to them, so we can easily move them around and defragment the buffer when necessary. But in fact, we don't even have to do that. If we get fragmentation we will eventually run out of space. This will reallocate the buffer which will also defragment it. This is enough for our purposes.

## 7: Slim down the `Value`

struct

Since all our value data are now allocated in a single buffer we can use the buffer offset rather than the pointer to refer to the data. This saves us memory (from 64 bits to 32 bits) and as an added bonus, it also allows us to relocate the buffer without having to do pointer patching.

For these small snippets of data 64 K is plenty, which means we can fit both the offset and the size in 32 bits:

```
struct Data {
uint16_t offset;
uint16_t size;
};
```


(If you need more memory, you could use a full `uint32_t`

for the offset and store the size in the buffer, together with the data.)

So know we have:

```
struct Value
{
union {
bool b;
float f;
Data data;
}
};
```


where the `data`

field is used for both strings and arrays. This means our `Value`

structure is now just 32 bits, half the size of the STL version.

## 8: Merge the final two allocations

Now we are down to just two buffers: one for the header (keys and types), and one for the values (strings and arrays). Wouldn't it be great if we could merge them to use just a single allocation?

Let's try our old trick and putting them together in the same buffer:

```
--------------------------------------------------------
| Header | Values | ....... free space ...... |
--------------------------------------------------------
```


This doesn't really work, because now the `Header`

part can't grow unless we move the values out of the way.

We could give them each a little bit of free space:

```
----------------------------------------------------------
| Header | ... free ... | Values | ... free ... |
----------------------------------------------------------
```


Now they both have some room to grow, but we are not utilizing the free space to its maximum potential. The `Values`

section may run out of free space before the `Header`

, forcing us to reallocate the buffer even though we actually have some free space left in it. That's a bummer.

But what if we do this:

```
----------------------------------------------------------
| Header | ........ free space ........ | Values |
----------------------------------------------------------
```


Instead of allocating the values bottom up, we allocate them top down in the buffer. Now the headers and the values can share the same free space and we don't have to reallocate the buffer until they meet in the middle. Nice!

## Benefits of single buffer structures

Stripping everything down to a single buffer gives us many of the same benefits that the blob approach gives us for static data.

Since the data is stored in a single buffer and doesn't contain any pointers it is fully relocatable. We can move it around in memory as we please and make copies of it with a simple `memcpy()`

.

If we want to save the data to disk, as a static resource or as part of a saved game, we don't need any special serialization code. We can just write and read the data directly.

The pointer arithmetic that is needed to manipulate data in this way may seem complex at first, if you are not used to think about pointer operations on raw memory. But I would argue that once you get used to that, this kind of representation is in many ways *simpler* than the multi-level `std::vector`

, `std::map`

based approach that we started with. And in that simplicity lies a lot of power.

## But wait, I have been cheating!

Yes, to be honest I have been cheating all this time.

I have ignored the old adage of data-oriented programming:

Where there is one, there are many.


All this time I have been talking about how *one* `DataComponent`

can store its data in a single buffer. But in our real system we will have *many* `DataComponents`

. We might have 1000 entities, each with a `DataComponent`

that stores a single `health`

float. Even if each component uses a contiguous buffer, that's still a lot of individual memory allocations.

Wouldn't it be nice if we could somehow bundle them together too?

But that represents a trickier challenge. We need to find a way to allocate a lot of individual objects in a single buffer in such a way that each individual object can grow and shrink independently.

And that will be the topic for another post.

Another awesome post! But I would like to clarify one thing... Where there is one DataComponent, there are many, where there is one component, there are many, where there is one class (system, manager... ), there are many... and so on. Are there any limits? Do you dream about an universal system that would manage memory for a whole game?

ReplyDeleteNah... not really.






DeleteI believe in managing the things that are instances of the same thing together. So all DataComponents are the same (except with different content), so there are lots of benefits to managing them together.

As for different components, like a DataComponent and a MeshComponent -- they are so different that there aren't any big benefits in managing them together. Quite the opposite actually. They are so dissimilar that I think we should actively try NOT to manage them together. Otherwise we risk creating couplings between unrelated things that limit our design options.

If you are not careful with coupling you can end up with completely silly things, like having empty render() and update() functions in the DataComponent because "all components should be able to render and update".

Besides, a universal memory system would essentially be a generic memory allocator and I have no great desire to write one of those :)

But I believe in each system being in complete control over its own memory allocations and bundling them together into bigger & fewer allocations. Ideally, they should be so big that we can allocate them directly from the page allocator (which means no fragmentation, yay) and so few that we can use garbage collection when needed (and worry less about threading issues). But that is just a distant dream...

Thank you for a detailed answer.

DeleteI was really worried that the lack of new posts is related to Bitsquid's acquisition... It's not to difficult to imagine that someone could find releasing some kinda' internal stuff to public inappropriate. I'm very glad that you came back to blogging and the future of this blog is not currently in danger.

No, Autodesk has only ever encouraged us to blog more, so no issues there. The blog may at some point move to a different address and platform (I'm not too happy with Blogger), but it's in no danger. It's just that sometimes I get stuck in the daily work and forget to post. And then I look up and two months have flown by.

DeleteGlad to have you back, Niklas. And thanks for sharing practical insights in DOD.

ReplyDeleteCool approach!


ReplyDeleteWould be interesting to also see some benchmark results showing the improvement of this method. So many hours can sink into optimising things and it is nice to see to what extent it pays back. :)

I love how you build the topics from the ground up to help understand better the way you've handled a particular problem. Thank you!

ReplyDeleteThanks for writing, it's inspiring and gives hope that there is something beyond oop!





ReplyDeleteI have written a small benchmark with different implementations. I got interested into that because we have one of these std data object at work and it's slow and I hate it. I'm not hopping that I will be able to get the team to accept a data driven implementation, the whole project is so oop and virtual and people don't know better so it's a lost cause.

Anyway I implemented the oop version and the final version. the dod version shows a 5 times speedup over the std version. The test as to construct small objects such as presented above and performing a few queries.

The (quick and dirty) implementation can be found here:

https://gist.github.com/oilandrust/e8b4202ce8786ce85a58ee075defc851

They are necessary command. That's what I need much abcya

ReplyDeleteThis is an informative blog i would love to see more from you.

ReplyDeletegoogle 1770

ReplyDeletegoogle 1771

google 1772

google 1773

google 1774

We Level Up texas mental health treatment offers top-tier addiction treatment detox using evidence-based therapy along with secondary dual diagnosis programs.

ReplyDeleteLevel Up addiction solutions of florida Treatment Center in West Palm Beach is located in stunning South Florida. Our clients who are looking for the best alcohol or drug treatment to overcome their fixation for the last time come from the United States, Canada, and even the world to receive our treatment plan.

ReplyDeleteWorld-class We Level Up alcoholic Addiction Treatment Center providing Dual-Diagnosis Recovery Programs.

ReplyDeleteNice one! thank you so much! Thank you for sharing this post. Your blog posts are more interesting and impressive.

ReplyDeleteหวยออนไลน์

Finding a trustworthy


ReplyDeletelaptop service near menearby can significantly reduce downtime and restore your device's functionality. It's advisable to choose a service center that not only has a solid reputation but also provides quick turnaround times. Many local shops offer diagnostic services to identify problems accurately before proceeding with repairs.Furthermore, consider the convenience of location and whether they provide on-site services or pick-up options. By taking these factors into account, you can ensure that your laptop receives the best possible care without the hassle of long-distance travel.

Nice explanation! This Pashmina Shawl Manufacturer seems very reliable.

ReplyDelete