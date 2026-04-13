---
title: Making SoA Tollerable
url: http://hacksoflife.blogspot.com/2021/02/making-soa-tollerable.html
author: Benjamin Supnik
published: '2021-02-27'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Chandler Caruth (I think - I can't for the life of me find the reference) said something in a cppcon talk years ago that blew my mind. More or less, 95% of code performance comes from the memory layout and memory access patters of data structures, and 5% comes from clever instruction selection and instruction stream optimization.

That is...terrible news! Instruction selection is now pretty much entirely automated. LLVM goes into my code and goes "ha ha ha foolish human with your integer divide by a constant, clearly you can multiply by this random bit sequence that was proven to be equivalent by a mathematician in the 80s" and my code gets faster. There's not much I have to worry about on this front.

The data structures story is so much worse. I say "I'd like to put these bytes here" and the compiler says "very good sir" in sort of a deferential English butler kind of way. I can sense that maybe there's some judgment and I've made bad life choices, but the compiler is *just going to do what I told it. "*Lobster Thermidor encrusted in Cool Ranch Doritos, very good sir" and Alfred walks off to leave me in a hell of L2 cache misses of my own design that turn my i-5 into a 486.

I view this as a fundamental design limitation of C++, one that might someday be fixed with generative meta-programming (that is, when we can program C++ to write our C++, we can program it to take our crappy OOPy-goopy data structures and reorganize them into something the cache likes) but that is the Glorious Future™. For now, the rest of this post is about what we can do about it with today's C++.

### There Is Only Vector

To go faster, we have to keep the CPU busy, which means not waiting for memory. The first step is to use vector and stop using everything else - see the [second half of Chandler's](https://www.youtube.com/watch?v=fHNmRkzxHWs) talk. Basically any data structure where the next thing we need isn't directly after the thing we just used is bad because the memory might not be in cache.

We experienced this first hand in X-Plane during the port to Vulkan. Once we moved from OpenGL to Vulkan, our CPU time in driver code went way down - 10x less driver time - and all of the remaining CPU time was in our own code. The clear culprit was the culling code, which walks a hierarchical bounding volume tree to decide what to draw.

I felt *very clever* when I wrote that bounding volume tree in 2005. It has great O(N) properties and lets us discard a lot of data very efficiently. So much winning!

But also, it's a tree. The nodes are almost never consecutive, and a VTune profile is just a sea of cache misses each time we jump nodes. It's slow because it runs at the speed of main memory.

We replaced it with a structure that would probably cause you to fail CS 102, algorithms and data structures:

1. A bunch of data is kept in an array for a a sub-section of the scenery region.

2. The sub-sections are in an array.

And that's it. It's a tree of fixed design of depth two and a virtually infinite node count.

And it screams. It's absurdly faster than the tree it replaces, because pretty much every time we have to iterate to our next thing, it's right there, in cache. The CPU is good at understanding arrays and is going to get the next cache line while we work. Glorious!

There are problems so big that you still need O(N) analysis, non-linear run-times, etc. If you're like me and have been doing this for a long time, the mental adjustment is how big N has to be to make that switch. If N is 100, that's not a big number anymore - put it in an array and blast through it.

### We Have To Go Deeper

So far all we've done is replaced every STL container with vector. This is something that's easy to do for new code, so I would say it should be a style decision - default to vector and don't pick up sets/maps/lists/whatever unless you have a really, really, really good reason.

But it turns out vector's not that great either. It lines up our objects in a row, but it works on *whole objects*. If we have an object with a lot of data, some of which we touch all of the time and some of which we use once on leap years, we waste cache space on the rarely used data. Putting whole objects into an array makes our caches smaller, by filling them up with stuff we aren't going to use because it happens to be nearby.

Game developers are very familiar with what to do about it - perhaps less so in the C++ community: vector gives us an **array of structures** - each object is consecutive and then we get to the next object; what we really want is a **structure of arrays - **each *member* of the object is consecutive and then we hit the next object.

Imagine we have a shape object with a location, a color, a type, and a label. In the structure of arrays world, we store 4 shapes by storing: [(location1, location2, location3, location4), (color 1, color 2, color3, color4), (type 1, type2, type3, type 4), (label 1, label2, label3, label4)].

First, let's note how much better this is for the cache. When we go looking to see if a shape is on screen, all locations are packed together; every time we skip a shape, the next shape's location is next in memory. We have wasted no cache or memory bandwidth on thing we won't draw. If label drawing is turned off, we can ignore that entire block of memory. So much winning!

Second, let's note how absolutely miserable this is to maintain in C++. Approximately 100% of our tools for dealing with objects and encapsulations go out the window because we have taken our carefully encapsulated objects, cut out their gooey interiors and spread them all over the place. If you showed this code to an OOP guru they'd tell you you've lost your marbles. (Of coarse, SoA isn't object oriented design, it's data oriented design. The objects have been minced *on purpose*!)

### Can We Make This Manageable?

So the problem I have been thinking about for a while now is: how do we minimize the maintenance pain of structures of arrays when we have to use them? X-Plane's user interface isn't so performance critical that I need to take my polymorphic hierarchy of UI widgets and cut it to bits, but the rendering engine has a bunch of places where moving to SoA is *the* optimization to improve performance.

The least bad C++ I have come up with so far looks something like this:

struct scenery_thingie {

int count;

float * cull_x;

float * cull_y;

float * cull_z;

float * cull_radius;

gfx_mesh * mesh_handle;

void alloc(UTL_block_alloc * alloc, int count);

scenery_thingie& operator++();

scenery_thingie& operator+=(int offset);

};

You can almost squint at this and say "this is an object with five fields", and you can almost squint and this and say "this is an array" - it's both! The trick is that each member field is a base pointer into the first object (of count's) member field, with the next fields coming consecutively. While all cull_y fields don't have to follow cull_x in memory, it's nice if they do - we'd rather not have them on different VM pages, for example.

Our SoA struct can both be an array (in that it owns the memory and has the base pointers) but it can also be an iterator - the increment operator increments each of the base pointers. In fact, we can easily build a sub-array by increasing the base pointers and cutting the count, and iteration is just slicing off smaller sub-arrays in place - it's very cheap.

This turns out to be pretty manageable! We end up writing *iter.cull_x instead of iter->cull_x, but we more or less get to work with our data as expected.

### Where Did the Memory Come From?

We have one problem left: where did the memory come from to allocate our SoA? We need a helper - something that will "organize" our dynamic memory request and set up our base pointers to the right locations. This code is doing what operator new[] would have done.

class UTL_block_alloc {

public:

UTL_block_alloc();

template<typename T>

inline void alloc(T ** dest_ptr, size_t num_elements);

void * detach();

};

Our allocation block helper takes a bunch of requests for arrays of T's (e.g. arbitrary types) and allocates one big block that allocates them consecutively, filling in dest_ptr to point to each one. When we call detach, the single giant malloc() block is returned to be freed by client code.

We can feed any number of SoA arrays via a single alloc block, letting us pack an entire structure of arrays of structures into one consecutive memory region. With this tool, "alloc" of an SoA is pretty easy to write.

void scenery_thingie::alloc(UTL_block_alloc * a, int in_count)

{

count = in_count;

a->alloc(&cull_x,c);

a->alloc(&cull_y,c);

a->alloc(&cull_z,c);

a->alloc(&cull_r,c);

a->alloc(&mesh_handle,c);

}

A few things to note here:

- The allocation helper is taking the sting out of memory layout by doing it dynamically at run-time. This is probably fine - the cost of the pointer math is trivial compared to actually going and getting memory from the OS.
- When we iterate, we are using memory to find our data members. While there exists some math to find a given member at a given index, we are storing one pointer per member in the iterator instead of one pointer total.

### Someday We'll Have This

Someday we'll have meta-programing, and when we do, it would be amazing to make a "soa_vector" that, given a POD data type, generates something like this:

struct scenery_thingie {

int count;

int stride

char * base_ptr;

float& cull_x() { return (*(float *) base_ptr); }

float& cull_y() { return *((float *) base_ptr + 4 * stride); }

float& cull_z() { return *((float *) base_ptr + 8 * stride); }

/* */

};

### Nitty Gritty - When To Interleave

One last note - in my example, I split the X, Y and Z coordinates of my culling volume into their own arrays. Is this a good idea? If it was a vec3 struct (with x,y,z members) what should we have done?

The answer is ... it depends? In our real code, X, Y and Z are separate for SIMD friendliness - a nice side effect of separating the coordinates is that we can load four *objects *into four lanes of a SIMD register and then perform the math for four objects at once. This is the biggest SIMD win we'll get - it is extremely cache efficient, we waste no time massaging the data into SIMD format, and we get 100% lane utilization. If you have a chance to go SIMD, separate the fields.

But this isn't necessarily best. If we had to make a calculation based on XYZ, together, and we *always* use them together and we're not going to SIMD them, it might make sense to pack them together (e..g so our data went XYZXYZXYZXYZ, etc.). This would mean fetching position would require only one stride in memory and not three. It's not bad to have things together in cache if we want them together in cache.

Hi!








ReplyDeleteGood read. I agree with everything!

I just came in to add that there is 3rd way to layout position data in memory. You mentioned:

1.

XXXX

YYYY

ZZZZ

2. XYZXYZXYZXYZ

3. The 3rd one is AoSSoA (Arrays of Structures of Structure of Arrays):

XXXXYYYYZZZZ

e.g.

struct AoSSoA

{

float x[4];

float y[4];

float z[4];

}

The benefit is that data for a single position element is one or at most 2 cache lines away.

The disadvantage is that it doesn't scale too well for large SIMD e.g. 512 bits SIMD, as the distance for a single element ends in 3 different cache lines. AVX-512 consumes too much power anyway, so that's rarely an issue.

Right - the idea here is that the "inner" array matches the SIMD stride but the outer array keeps at least _part_ of the objects (e.g. components of a position vector) together?





ReplyDeleteI can see how this would be optimal for certain cases. My one thought is: this is pretty straight forward if you are _always_ going to use SIMD to loop over objects - since you're always going to iterate by 4 objects at a time (or whatever your SIMD lane count is) then the two-part iteration (outer and inner) is basically free.

But if for some reason code has to iterate the collection one object at a time, that code becomes more complex. It might be that if you have that kind of code, that kind of code is wrong if you're really serious about the SIMD.

Our code already had getter and setters for data such position and orientation; thus the getter/setter call an "extract" function that deinterleaves the SIMD for us to non-SIMD.




DeleteThus externally the SIMD is hidden.

But indeed, the recommendation is to not call these functions too frequently (i.e. no more than once per frame per object; assuming you are forced to call it on all objects every frame for some reason) since de-interleaving for reading and interleaving again for setting has its overhead.

But indeed: It's tradeoffs. We also included a macro to dynamically adjust the "width" at build time.

So if for some reason the SIMD code is very detrimental to your use case, you can disable the SIMD code and now data is layed out XYZXYZXYZ in memory. You loose SIMD but gain in lower overhead per object.