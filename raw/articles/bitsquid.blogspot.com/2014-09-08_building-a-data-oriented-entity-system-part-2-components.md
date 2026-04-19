---
title: 'Building a Data-Oriented Entity System (Part 2: Components)'
url: https://bitsquid.blogspot.com/2014/09/building-data-oriented-entity-system.html
author: Niklas
published: '2014-09-08'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

In the [last post](http://bitsquid.blogspot.se/2014/08/building-data-oriented-entity-system.html), I talked about the design of the *Entity Manager* and how we handle creation and destruction of game entities.

In this post we will look at how components can be implemented.

A quick recap: Components in our system are not individual objects, instead all components of a particular type are handled by a *component manager* for that type. The component manager has full control over how the component data is stored internally and how updates are applied.

To have something to talk about we will consider a fictitious component that handles point mass objects. For each component instance we want to store the following data:

```
Entity entity; ///< Entity owner
float mass; ///< Mass of object
Vector3 position; ///< Object's position
Vector3 velocity; ///< Object's velocity
Vector3 acceleration; ///< Object's acceleration
```


The component needs functions for accessing this data and simulating physics.

It is perhaps not self-evident why we want to store the entity that owns the component, but it will come in handy later.

*Note that this is not a real world example. We don’t actually have a component like this in the engine, and perhaps it’s not the best or most interesting design, but it gives us something to talk about.*

When considering how we should layout the data in the component manager we have two goals:

- Given an entity we want to be able to quickly look up the component data for that entity.
- We want the component data to be packed tightly in memory for good cache performance.

Let’s tackle the second question first.

Actual cache performance depends on how your CPU works and what the data access patterns in the code are. You can spend a lot of time trying to bend your mind around those things, but I would recommend going with a simple rule of thumb instead:

Pack the data in arrays that you access sequentially.


Only get more fancy than that when you are trying to fix a diagnosed performance issue.

A generally good approach is to use a structure-of-arrays. I.e., each field is stored in an array in memory, with one entry for each component instance:

```
[entity_1] [entity_2] [entity_3] ...
[mass_1] [mass_2] [mass_3] ...
[pos_1] [pos_2] [pos_3] ...
[vel_1] [vel_2] [vel_3] ...
[acc_1] [acc_2] [acc_3] ...
```


The advantage of having each field stored separately is that code that only processes some of the fields don’t have to waste precious cache space on the others.

You could go even further and put each *x*, *y* and *z* component of a `Vector3`

into its own array. An advantage of that is that you can do more efficient SIMD calculations, if you want to go down that route. But for this example, let’s keep things a bit simpler and store the `Vector3`

s together. Since the layout of the data is entirely encapsulated in the `ComponentManager`

class we can always go back and redesign that later if we need some extra performance.

The simplest way of implementing this data layout is to use an `Array`

for each component:

```
class PointMassComponentManager {
struct InstanceData {
Array<Entity> entity;
Array<float> mass;
Array<Vector3> position;
Array<Vector3> velocity;
Array<Vector3> acceleration;
};
InstanceData _data;
};
```


That works well enough, but it does mean that the data gets stored in five separately allocated memory buffers. So I use a different approach. I allocate the entire memory buffer as a single allocation and then just let `entity`

, `mass`

, etc, point to different parts of that buffer:

```
struct InstanceData {
unsigned n; ///< Number of used instances.
unsigned allocated; ///< Number of allocated instances.
void *buffer; ///< Buffer with instance data.
Entity *entity;
float *mass;
Vector3 *position;
Vector3 *velocity;
Vector3 *acceleration;
};
InstanceData _data;
void allocate(unsigned sz)
{
assert(sz > _data.n);
InstanceData new_data;
const unsigned bytes = sz * (sizeof(Entity) + sizeof(float) +
3 * sizeof(Vector3));
new_data.buffer = _allocator.allocate(bytes);
new_data.n = _data.n;
new_data.allocated = sz;
new_data.entity = (Entity *)(new_data.buffer);
new_data.mass = (float *)(new_data.entity + sz);
new_data.position = (Vector3 *)(new_data.mass + sz);
new_data.velocity = new_data.position + sz;
new_data.acceleration = new_data.velocity + sz;
memcpy(new_data.entity, _data.entity, _data.n * sizeof(Entity));
mempcy(new_data.mass, _data.mass, _data.n * sizeof(float));
memcpy(new_data.position, _data.position, _data.n * sizeof(Vector3));
memcpy(new_data.velocity, _data.velocity, _data.n * sizeof(Vector3));
memcpy(new_data.acceleration, _data.acceleration,
_data.n * sizeof(Vector3));
_allocator.deallocate(_data.buffer);
_data = new_data;
}
```


This avoids any hidden overheads that might exist in the `Array`

class and we only have a single allocation to keep track of. This is better both for the cache and the memory allocation system.

*Side note: I’m tempted to write a memory system with a 4 K allocation granularity. I.e. there is no traditional heap allocator, just a page allocator and you have to design your systems so that they only work with large allocations.*

Let’s consider the second issue, how we map from an entity to its component data. For the sake of simplicity, let’s assume for now that we don’t support multiple components per entity.

In the data layout, we refer to a particular component instance by its index in the `mass`

, `position`

, etc arrays. So what we need is a way to map from an entity to an index.

You may remember from the [previous post](http://bitsquid.blogspot.se/2014/08/building-data-oriented-entity-system.html), that `Entity`

itself contains a unique index. So one alternative would be to just use this index.

This could be a good approach if almost every entity in the game had this component. But if that is not the case our arrays will contain a lot of “holes” corresponding to entities that lack the component. This will waste memory, but also performance, because we will fill our caches with unused data.

We can improve this somewhat by using a level of indirection:

```
Array<unsigned> _map;
```


Here, the `_map`

allows us to look up a component index based on the entity index. This is a lot better, because now it is just the `_map`

array that has holes, not the `_data`

array, which means that the holes are fewer and smaller.

Still, I would only use this if I was certain that the component was almost universal and that lookups where performance critical. In most cases, I think a hash index is a better approach:

```
HashMap<Entity, unsigned> _map;
```


This uses less memory and lookups are still pretty fast.

Since the lookup from `Entity`

to instance index involves an extra step we want to reflect that in the API and not force the user to do multiple lookups when she wants to access different fields of the same component. Something like this:

```
/// Handle to a component instance.
struct Instance {int i;};
/// Create an instance from an index to the data arrays.
Instance make_instance(int i) {Instance inst = {i}; return inst;}
/// Returns the component instance for the specified entity or a nil instance
/// if the entity doesn't have the component.
Instance lookup(Entity e) {return make_instance(_map.get(e, 0));}
float mass(Instance i) {return _data.mass[i.i];}
void set_mass(Instance i, float mass) {_data.mass[i.i] = mass;}
Vector3 position(Instance i) {return _data.position[i.i];}
...
```


To support multiple component instance per entity, you can add a `next_instance`

field to the component data that allows you to traverse a linked list of component instances belonging to the same entity. This is left as an exercise to the reader.

Since the component data is laid out sequentially in memory, writing a function that simulates physics for all entities is simple:

```
void simulate(float dt)
{
for (unsigned i=0; i<_data.n; ++i) {
_data.velocity[i] += _data.acceleration[i] * dt;
_data.position[i] += _data.velocity[i] * dt;
}
}
```


This function traverses memory in-order which gives us good cache performance. It’s also easy to profile, vectorize and parallelize, should the need arise.

*Side rant: I’m somewhat allergic to methods being called update(). That is a bad remain from bad inheritance-based designs. If you take a second to think about it you can almost always come up with better, more informative names than update().*


When destroying components, we want to make sure that we keep the `_data`

array tightly packed. We can achieve that by moving the last element to the position of the component we want to remove. We must also update the `_map`

entry for the corresponding entity.

```
void destroy(unsigned i)
{
unsigned last = _data.n - 1;
Entity e = _data.entity[i];
Entity last_e = _data.entity[last];
_data.entity[i] = _data.entity[last];
_data.mass[i] = _data.mass[last];
_data.position[i] = _data.position[last];
_data.velocity[i] = _data.velocity[last];
_data.acceleration[i] = _data.acceleration[last];
_map[last_e] = i;
_map.erase(e);
--_n;
}
```


Another question is how we handle destruction of components when an entity is destroyed. As you may recall, the entity does not have an explicit list of components that it owns. Also, it seems onerous to require of the user of the API to manually destroy the right components when the entity dies.

Instead, we use one of two approaches.

Components that need to be destroyed immediately (perhaps because they hold external resources) can register a destruction callback with the `EntityManager`

and that callback will be called when the entity is destroyed.

However, for simpler components, like the *point mass* component, there is nothing that require components to be destroyed at exactly the same time as the entity. We can take advantage of that and use garbage collection to lazily destroy components instead of spending memory and effort on storing callback lists:

```
void gc(const EntityManager &em)
{
unsigned alive_in_row = 0;
while (_data.n > 0 && alive_in_row < 4) {
unsigned i = random_in_range(0, _data.n - 1);
if (em.alive(_data.entity[i])) {
++alive_in_row;
continue;
}
alive_in_row = 0;
destroy(i);
}
}
```


Here, we pick random component indices and destroy them if the corresponding entity has been destroyed. We do this until we hit four living entities in a row.

The nice thing about this code is that it cost almost nothing if there are no destroyed entities (just four passes of the loop). But when there are a lot of destroyed entities the components will be quickly destroyed.

In the next post, we will look at the *Transform Component* that handles links between parent and child entities.

Nice read. One question: since your simulate() loop touches most components (position, accel, velocity) of an entity every time, wouldn't it be more efficient to store those components close to each other? something like this:



ReplyDeletestruct SimData {

Vector3 position;

Vector3 acceleration;

Vector3 velocity;

};

struct InstanceData {

...

Entity *entity;

float *mass;

SimData *simData;

};

Yes, could be. That's what I meant when I said that the performance depends on the actual access patterns. But it depends... perhaps there is other code in the project that only looks at the position... you have to profile your project to find out.

DeleteHello, first thanks for these nice articles about ES ^^


ReplyDeleteI´m implementing an ES/component base system myself too, and i´m trying the Data-oriented approach like yours. But the problem I face is: on an dynamic world, there is a lot of parent/child transforms, render layers or sortings, dynamic component dependency changes, etc, so my components data rarely are processed in parallel, the components indexes are normally spread. How this can solve? (or, what other view/approach to this problem can we have?)

Yes, that can be tricky. You have to think about this when you design the system: How can I arrange my data and updates so that they can be done sequentially, in parallel, etc. Often there are things you can do, even when there are complex relationships. I'll touch on some of this in the next post when I talk about the transform component.

DeleteAre you going to make ComponentManager a base class? It could include `entity` array, number of components `n` and `gc` method.

ReplyDeleteNo, I'm not fond of "inheritance based designs"... they tend to lead to problems... for example, only certain managers would want to use garbage collection, others need to delete objects immediately.


DeleteI'd rather put such shared code in a common utility library, if it makes sense to reuse it.

Do you seriously have to do something like TransformSystem->set_mass(TransformSystem->lookup(entity), newMass) every time or how are you managing that? I imagine there's a better way, but the only thing I can think of is to either store what component instances belong to an entity in the entity (counter-productive to the cause) or in the entity system. Could you shed any light on this?

ReplyDeleteThe instance only moves rarely, so if you have an old instance from the first frame cached you could provide that to the lookup:




ReplyDeletelookup(entity, old_instance)

And the entity could then do a very quick check (basically an int comparison) to check if the entity instance was still located in the same place. Can't get much faster than that.

But I think thinking about optimization in this way is not that productive. Doing a single thing to a single component will always be "slow" in some sense, sense it involves a random memory access. We should worry more about arranging our code so that we do the same thing to many pieces of data simultaneously and then making sure that that runs fast.

Ok, second question for you: How did you write your mesh system? Vertices need to be in some sort of dynamic array for obvious reasons, but the type of memory allocation you're doing above seems designed to avoid needing to use in place new allocation and deallocation in the first place. I've got this working with vectors, but it requires inplace new memory management, which I think defeats the point of what you've written (perhaps?). That leads me to believe you're either not using this memory allocation pool for mesh data or you're not using dynamic arrays. Could you shed some light?

ReplyDeleteNot sure I understand the question. Most vertex data comes from resources, so it's static.



DeleteDynamic vertex data (UI, decals, particles) I think we mostly keep in fixed sized buffers or ring buffers.

Also we're not 100 % strict about this system, not all data gets treated this way, just where it makes sense.

Why have the Instance wrapper for that int? The only thing I can think of is that you want to try and force users of the API to work with Instances instead of int's directly, but I'm not sure why. It makes it awkward to iterate through as well.



ReplyDeleteAnd why is it an int and not an unsigned int? Couldn't you run into a situation where your Lookup() would return a number larger than "int" is capable of returning since the map is setup to return an "unsigned int"?

Just wondering what your line of reasoning was. This series has been a great education for me.

It distinguishes instances from other integers which makes things a bit more readable you could argue. But you could make an argument for using regular ints as well.




DeleteI used to use "unsigned" for everything that would not hold negative values. But lately I've switched to using "int" as the default and only use "unsigned" in places where I really use all 32 bits (such as bitmasks). I just think that ints are generally less error prone since there is no risk for underflow and wraparound... and usually 31 bits work just as well as 32. Plus, if you use ints almost everywhere you don't have to worry about casting between ints and unsigned.

But since my view has changed on this sometimes the code has a bit of a mix between ints and unsigned.

On a related note: I've also in many occassions stopped using -1 or 0xffffffff to indicate an invalid index and instead just use 0 for that. I sacrifice the first slot in the array to have more readable and less error prone code.

Definitely, it could go either way. Was just curious. And I know what you mean! I've been using unsigned int as well but after doing some more reading I don't think it's worth the potential headaches, plus the casting or compiler warnings are annoying.



DeleteI was curious what you were returning for an invalid index. I considered returning 0 but wasn't sure if that was a good way to go, so I started returning -1 but then got concerned about returning an int for an unsigned int. Good to know, I'll revisit the idea.

On that topic, I see you're not making that invalid index check in the Lookup. Is this because Lookup's happen frequently and you didn't want the check affecting performance (I assume then you make the check inside the other function calls then), or did you simply leave it out for the sake of brevity?

One of the things I'm considering for each system that requires access other systems is for those systems to contain its own complete data structure of all the information it needs, and then broadcast the delta (so only the data that's changed) to all other systems using that data when it does change. I forget where I read about that technique (possibly from you?) but it sounds really interesting. I'd essentially be trading memory space and some overhead for even better cache performance (hopefully). If you're not the one I read that from, have you thought about doing something similar?

ReplyDeleteSorry for double post. Refreshed the page and it posted again...

DeleteThis comment has been removed by the author.

ReplyDeleteThis post is quite old, but your series on data-oriented & entity pattern is probably the best introduction to the concept found anywhere. I'm wondering how storing your fields in separate arrays will affect your simulate method performance.




ReplyDeleteForgive me if I am completely off tracks here, but from what I understand, you seem to get a performance hit during simulate. Since your cpu will prefetch data locally, you will probably cache miss on acceleration[i] and position[i] (since these values are not contiguously stored). Especially if you have many components.

So my question is, are you optimizing for creation of the components? And wouldn't storing the whole structures contiguously help the prefetcher? Since that way all your data is definitely in cache, along with the next few objects.

Great article overall and thank you for all these eye-opening blogs :)

That's just an example he showed prior to showing a better way to do it (see the code snippet just below the Array one. Look for "void *buffer"). In the one he's actually using, all the data is stored in one contiguous block of memory.


DeleteAnd you're right, this is hands down the best introduction to the concept out there. This series has been extremely helpful in making my own engine. Hit me up sometime, maybe we can compare notes =]

No I'm optimizing for update performance.









DeleteStoring the whole structure contiguously might help for certain update scenarios (if you touch all fields in order). But it won't help very much. You will only get a cache miss when you fetch the first element in each array, since after that you are fetching memory close to things you have already touched. So the extra overhead is O(1), it is only really significant with N is small and we are optimizing for large N. (Also, when N is small, because of our strategy of allocating from the same larger buffer, these different buffers will in fact be close together, so we don't even pay a high price.)

But it will definitely make things worse in a lot of other scenarios. In the example above, the update will probably be something like:

vel = vel + acc * dt

pos = pos + vel * dt

This update doesn't touch the mass or entity fields. That's 18.2 % of the cache space wasted. Since for this simple code we are probably memory bound, that's 18.2 % performance loss.

So in this simple example, SoA (structure-of-arrays) gives 18.2 % better performance, while AoS (array-of-structures) maybe has a small O(1) benefit.

This pattern appears again and again. AoS maybe has some small benefit in very specific scenarios. However, there are lots and lots of things that can cause SoA to have a really big benefits (as in the example above). Also SoA helps with rewriting the code to use SIMD in the future.

So my rule of thumb would be, if you are coding for performance, you should always use SoA.

Note that there can be other reasons for choosing AoS, unrelated to performance. For example, it can make the code easier to follow, so it might be preferable for those reasons. (However, after using SoA for a while you may find that your perspective shifts and you start seeing it as simpler.)

Thank you so much for taking the time to answer. I don't seem to receive notifications about replies, I'll fix that right now.







DeleteI guess my uncertainty comes from having issues "seeing" or profiling how the cache prefetching works. All of the work I've been doing in data-oriented is backed by assumptions and gut-feelings (bad).

If I reiterate in cognitive layman terms, the prefetcher pulls, in parallel, from various parts of the memory. Or at least, you could think of it that way. The hot prefetched data will stick around, maybe it prefetches once every cycle, or less, but the data sticks around longer than I believed.

My (wrong) understanding was that it is 100% sequential. And for some reason, I probably under-estimate how much information can be prefetch. That every prefetch is trashing the last. So you would prefetch accelerate, than trash that for position etc.

So: SoA will prefetch less data, which means there is more room for relevant data. The prefetching is happening on multiple separated areas of the memory, and each time the data sticks around. It is prefetching a section of velocity array when you hit it first, a section accelerate and a section of position. After that, everything is in cache and bang bang bang super-speed xD

Am I understanding this somewhat correctly? I really need to thank you again for helping us understand these concepts. If you ever write a book, or make a conference I'd be one happy programmer!

Cheers

Hey,




DeleteI think the SoA works better for small N. You're talking about the cache, but how big is that cache?

You're storing the data like this:

pos|pos|pos|...|acc|acc|acc|...|vel|vel|vel|... and so on

So if you have a large N, where N * sizeof(pos) is greater than the size of the cache, then you have a lot of cache misses since you're jumping in the memory back and forth. What am I missing?

Having a large N that is larger than the cache is not really what a cache miss is. What you're describing is simply a reality of the cpu needing to pull the next chunk of RAM into its caches. With a SoA approach, we know that the data entering the caches is contiguous and can be ripped through by the CPU much faster than if it got a bunch of noncontiguous data it didn't need in addition to the data it did need (as is typical with AoS).


DeleteI was able to set up a simple example in C++ that compared the processing speeds of a SoA vs AoS and the results were pretty clear. Try it and see for yourself!

I understand this and I'll probably try it, however...



DeleteIf you have eg. 10k element (so 10k position, 10k velocity, 10k acceleration, etc.) with this layout and you're using the velocity and the acceleration component in a single line of code (eg. velocity[i] += acceleration[i]) then: If the velocity is a 3D vector then 1 element = 12 bytes, 10k element = 120k bytes.

Is your cache big enough to fit more than 120 kbytes of data? If not, there's a cache miss.

I think I see what you're saying now. I might have an answer? I was looking back at the Component Updates section and wondered if maybe the cache for velocity, acceleration, position, and velocity came in sections to the cache. If so, then maybe the next few would iterations would still be warm in the cache? Good question.

DeleteYou are misunderstanding how caches work. The cache does not hold a single contiguous chunk of memory, it holds little pieces from all over memory. So when using the velocity[i] and acceleration[i], the cache will not load all the memory between them.

DeleteOh I see, my bad. Thanks for the reply! :)


DeleteThen what's the point of packing the data into a small POD struct instead of using purely struct of arrays? It seems that packing data is the worst thing we can do (at least from the cache friendlyness perspective).

How do you think something like this compares to the actor model? There's a lot to be said for data-oriented design, but that still leaves concurrency to the developer. Using something like Akka or CAF (C++ Actor Framework) makes that almost transparent, even for distributed computing.

ReplyDeleteDo you think allowing an entity to have multiple components of the same type is an good idea?



ReplyDeleteAnd how would you design the parent-child relationship in entity-component system?

In Unity, it allows multiple components of the same type, and stores the hierarchy in Transform component, but I don't know whether it is a good design or not.

(But storing the hierarchy in each type of component that needs it may cause some problem, for example, if I want to hide an entity, then all its children should be hided, but how do I determine this relationship should be got from which component's data?)

Thanks for reading my questions, and sorry for my poor English.

I think allowing multiple components of the same type is usually a good idea. Because you may want multiple meshes for an entity, etc. The alternative is you only have one mesh component for the entity but you can have multiple meshes in that component. Both approaches work and are good in different ways. Assuming that the mesh component holds only one mesh simplifies the mesh component. While assuming that entities can only have a single component of a particular type simplifies the entity model. We choose the former, but I think you could make an argument for the latter too.


DeleteWe store the hierarchy in the Transform component too, and only there, to avoid having the same thing stored in multiple places and risking them getting out of sync.

Thank you !


DeleteSomething I want to know is that when allowing multiple components of the same type, how to distinguish the one you need from others ?

Another one question is, when storing the hierarchy in Transform, it means when other components need the information, it should first get access to its entity, and get the component, and get the parent entity ? Or this would be a rare case ?

Thanks again for reading my questions !

Your articles and replies are both very helpful to me.

We have a unique ID that identifies each component.





DeleteYes, in general, information is only stored in a single place... and if another component wants to access it, it needs to access the component that stores it first. Note that for some components it might make sense to "cache" that data locally though... and only update the cache when it detects that the owning component has changed -- if the component needs frequent access to the data.

However, as a general rule, only create caches when you REALLY need them, because they have a tendency to complicate the system and add subtle bugs.

"There are only two hard things in Computer Science: cache invalidation and naming things."

-- Phil Karlton

Although this post is a bit old, it is still a gem. I would ask, however, for a quick clarification about using the lazy GC for destroying destroyed entities' components.




ReplyDeleteWhenever you iterate over the data of a given component manager (e.g. to update transforms), how do you handle the components that belonged to entities that are now dead, but were not yet garbaged collected?

It seems to me that you would have to do one two things: either a) check in every iteration whether each component belongs to an alive entity or b) don't bother and just iterate and do calculations over the components of dead entities, since that won't matter provided that they are indeed excluded from some critical component managers (e.g. rendering).

Both options sound quite wasteful in terms of resources, while the first has also the additional downside of defeating a lot of the DOD purposes. Am I missing something? How do you handle the not-yet GCed components from already dead entities?

It probably depends on the component. Some might need to be deleted immediately because the cost of calculating is greater than the cost of lazily garbage collecting it, while others are trivial to just calculate and clean up later. I haven't profiled it, but I wonder how much a simple alive check would really hinder the cache efficiency of the update loop? Don't know. Good question. Hopefully we learn the answer. By the way, if you haven't checked out his series on YouTube it's definitely worth watching. :)

DeleteHi. Don't know if I missed something but I guess the simulate function, for updating physics is wrong. You won't have same index for different components, because you may have static entities, which have position but don't have velocity, and dynamic objects, which have both, so you may end up with components like:

ReplyDeleteposition memory: ssssddddssssdddd

velocity memory: dddddddd

The indexes between components of same entity will have offset.

> Side rant: I’m somewhat allergic to methods being called update(). That is a bad remain from bad inheritance-based designs. If you take a second to think about it you can almost always come up with better, more informative names than update().



ReplyDeleteIn my opinion, "simulate" carries no more information than "update". You are much better of sticking with "update" as it very common and standard terminology. If I encounter a large unfamiliar and poorly documented code file, the first thing I'll look for is a function called update, as it is likely to be one of the main functions that is driving everything else. Coming up with creative alternative synonyms like Simulate which carry no additional information is a futile exercise in obfuscation.

Permainan Sabung Ayam tentunya sudah pada tahu ya, yang dimana ayam melawan ayam pertandingan yang sangat seru ini bisa kalian nonton secara live lohh, banyak yang bermain di situs kami dan merasa sangat nyaman, bagi kalian yang ingin bermain bisa kunjungi situs kami, dijamin kalian akan merasa sangat senang.























ReplyDeletedeposit sabung ayam pakai pulsa

deposit s128 pakai pulsa

deposit sabung ayam via pulsa

deposit s128 via pulsa

s128 deposit pakai pulsa

s128 deposit via pulsa

cara deposit pulsa sabung ayam

cara deposit pulsa s128

cara deposit s128 pakai pulsa

cara deposit s128 via pulsa

login sabung ayam s128

login s218 apk

login sabung ayam apk

login s128 sabung ayam online

cara login s128

cara login sabung ayam s128

cara login s128 apk

link login s128

link login sabung ayam

This comment has been removed by the author.

ReplyDeleteWOW! I Love it...



ReplyDeleteand i thing thats good for you >>

LUCKY ZODIAC Thank you!

Fix Garmin GPS Won't Turn on While It's Plugged In. Minimal GPS gadgets, for example, Garmin's Nuvi arrangement give various incredible route includes that advantage long stretch truckers, neighborhood conveyance drivers, course salesmen and numerous different business clients.

ReplyDeleteThe information you give is very interesting. Yellowstone Coat

ReplyDeleteIt's really nice tutorial


ReplyDeleteIklan Baris Gratisclick on one of the sites below to get a variety of the best tips and tricks in life.



ReplyDeletedata togel china 2020

your article is very helpful. you can visit my website.

ReplyDeletehttps://cracksmob.com/

click on one of the sites below to get a variety of the best tips and tricks in life. live draw sgp tercepat

ReplyDeleteclick on one of the sites below to get a variety of the best tips and tricks in life.




ReplyDeletelive hongkong 6d

live draw sd

google 4332

ReplyDeletegoogle 4333

google 4334

google 4335

google 4336

google 4337

google 4338





ReplyDeleteslotxo auto

แตกง่ายจ่ายไว

Magnificent piece of work, great contents and fantastic information. free ESUT post utme past questions

ReplyDeleteThis is such good site for everyone. If you like to read some of wonderful of topic then this site is best. There are lots of good topic as Black Friday Web Hosting Deals and others. I have read it.

ReplyDeleteHello, we have a game to recommend.



ReplyDeleteทางเข้า ufabet

ufabet kick

รูเล็ตสายฟ้า

แทง บอล ผ่าน มือ ถือ

กา บอล1

Thank you for your interest."

Get Upto 90% Discount on Fastcomet Hosting Discount and Enjoy cloud hosting with 99.9% uptime.


ReplyDeleteDaebak! that’s what I was looking for, what a information! present here at this website


ReplyDelete바카라사이트

I really enjoy reading your well-written articles. It looks like you spend a lot of effort and time on your blog. I have bookmarked it and I am looking forward to reading new articles. Keep up the good work. umyu approved school fees schedule for direct entry


ReplyDeletembah syair



ReplyDeletesyair hk

syair sgp

It's really amazing piece of writing, I have got much clear idea regarding this post. Thank you so much for the post it is very helpful, keep posting such type of Article. Amazing!

ReplyDeleteeaseus os2go crack

itop vpn premium crack

game fire pro crack

wondershare repairit crack

startallback crack

easeus recexperts crack

Also Visit fultech.org

Data Sdy

ReplyDeleteThis comment has been removed by the author.

ReplyDelete

ReplyDeleteI am taking a look forward to your next submit, I’ll attempt to get the hold of it! Thank you for sharing. dominion university post utme format


ReplyDeleteUkraine's capital Kyiv has been attacked from the air by Russia for the ninth time this month.รับ สร้าง บ้าน เชียงใหม่

진안출장안마

ReplyDelete무주출장안마

장수출장안마

임실출장안마

순창출장안마

고창출장안마

부안출장안마

서울출장안마

Have you ever found yourself immersed in the glittering world of "Emily in Paris" and wondered about the captivating character of brooklyn clark emily in paris?

ReplyDelete고흥콜걸

ReplyDelete구례콜걸

곡성콜걸

광양콜걸

담양콜걸

나주콜걸

순천콜걸

여수콜걸

Avast Premier Security Download is a web safety request that defend every one CPU, telephone, with drug. Cyber security by Avast best anti-virus there modified plan near your exact supplies. It assists you inside get online defense next to your internet challenger.

ReplyDeleteAvast Premier Crack

I love the way you simplify things. This is exactly what I needed!

ReplyDeletecek Live Draw SDY

ReplyDeleteTraining consistency builds both strength and self-belief. Lifestyle identity discussions including Peaky Blinders Immortal Man 2026 Outfits support athlete motivation.

ReplyDelete