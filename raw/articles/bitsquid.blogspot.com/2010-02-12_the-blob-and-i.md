---
title: The Blob and I
url: https://bitsquid.blogspot.com/2010/02/blob-and-i.html
author: Niklas
published: '2010-02-12'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

*Shorter load times.*We can just stream the entire blob from disk to memory.*Cache friendly.*Related objects are at close locations in memory.*DMA friendly.*An entire blob can easily be transferred to a co-processor.

In past engines I've used placement

*new*and pointer patching to initialize C++ objects from a loaded blob. To save a resource with this system all the objects are allocated after each other in memory, then their pointers are converted to local pointers (offsets from the start of the blob). Finally all the allocated data is written raw to disk.When loading, first the raw data blob is loaded from disk. Then placement

*new*is used with a special constructor to create the root object at the start of the blob. The constructor takes care of pointer-patching, converting the offsets back to pointers. Let's look at an example:class A

{

int _x;

B *_b;



public:

A(int x, B *b) : _x(x), _b(b) {}

A(char* base) {

_b = (B*)( (char *)_b + (base - (char *)0) );

new (_b) B(base);

}

...

};

...

A *a = new (blob) A(blob);

Note that the constructor does not initialize

*_x*.*a*is placement*new*:ed into an area that already contains an*A*object with the right value for*_x*(the saved value). By not initializing*_x*we make sure that it keeps its saved value. The constructor does three things:- Initializes the vtable pointer of
*a*. This is done "behind the scenes" by C++ when we call*new*. It is necessary for us to be able to use*a*as an*A*object, since the vtable pointer of*A*saved in the file during data compilation will typically not match the vtable pointer of*A*in the runtime. - Pointer patches
*_b*, converting it from an offset from the blob base to its actual memory location. - Placement
*new*:s*B*into place so that*B*also gets the correct vtable, patched pointers, etc. Of course*B*'s constructor may in turn create other objects.

Like many "clever" C++ constructs this solution gives a smug sense of satisfaction. Imagine that we are able to do this using our knowledge of vtables, placement

*new*, etc. Truly, we are Gods that walk the earth!Of course it doesn't stay this simple. For the solution to be complete it must also be able to handle base class pointers (call a different

*new*based on the "real" derived class of the object, which must be stored somewhere), arrays and collection classes (we can't use*std::vector*, etc because they don't fit into our clever little scheme).Lately, I've really come to dislike these kinds of C++ "framework" solutions that require that every single class in a project conform to a particular world view (implement a special constructor, a special

*save()*function, etc). It tends to make the code very coupled and rigid. God forbid you ever had to change anything in the serialization system, because now the entire*WORLD*depends on it. The special little placement constructors creep in everywhere and pollute a lot of classes that don't really want to care about serialization. This makes the entire code base complicated and ugly.Also, it should be noted that naively "blobbing" a collection of scattered objects by just concatenating them in memory does not necessarily lead to optimal memory access patterns. If the memory access order does not match the serialization order there can still be a lot of jumping around in memory. The serialization order with this kind of solution tends to be depth-first and can be tricky to change. (Since the entire

*WORLD*depends on the serialization system!)In the BitSquid engine I use a much simpler approach to resource blobs. The BitSquid engine is

*data-centric*rather than*class-centric*. The data design is done first -- laid out in simple structs, optimized for the typical access patterns and DMA transfers. Then functions are defined that operate on the data. Classes are used to organize higher level systems, not in the low level processing intensive systems or resource definitions. Inheritance is very rarely used. (Virtual function calls are always cache unfriendly since they resolve to different code locations for each object. It is better to keep objects sorted by type and then you don't really need virtual calls.)I believe this "old-school" C-like approach not only gives better performance, but also in many cases a better design. A looser coupling between data and processing makes it easier to modify things and move them around. And deep, bad inheritance structures are the main source of unnecessary coupling in C++ programs.

Since the resource data is just simple structs, not classes with virtual functions, we can just write it to disk and read it back as we please. We don't need to initialize any vtable pointers, so we don't need to call

*new*on the data.The problem with pointer patching is solved in the simplest way possible -- I don't use pointers in the resource data. Instead, I just use offsets all the time, both in memory and on disk. For example, the resource data for our particle systems looks something like this (simplified):

Yes, having offsets in the resource data instead of pointers means that I occasionally need to do a pointer add to find the memory location of an object. I'm sure someone will balk at this "unnecessary" computation, but I can't see it having any significant performance impact whatsoever. (If you have to do it a lot, then you are jumping around in memory a lot and then

*that*is the main source of your performance problem.)The advantage is that since I'm only storing offsets I don't need to do any pointer patching at all. I can move the data around in memory as I like, make copies of it, concatenate it to other blobs to make bigger blobs, save it to disk and read it back with a single operation and no need for pre- or post-processing. There is no complicated "serialization framework". No system in the engine needs to care about how any other system stores or reads it data.


As in many other cases the data-centric approach gives a solution that is simpler, faster, more flexible and more modular.

As in many other cases the data-centric approach gives a solution that is simpler, faster, more flexible and more modular.

I like & fully agree!

ReplyDeleteI've refactored my code to use tightly packed structs as internal representation for scene entities and added "interfaced wrappers" created on fly (reusable pool is your friend) to access entities from game code. In this way you still be able to do something like SceneManager->GetEntityByName()->SetTrasform() and do not overcomplicate whole interface by exposing details of scene entities implementation. Profit.

ReplyDeleteHow do you handle dynamic arrays in this system?

ReplyDeleteMaciejS: This is resource data, so it is static in the runtime (arrays do not grow or shrink in-game). But of course during data compile time we want to be able to generate arrays of any length.






ReplyDeleteTo handle arrays of variable length, I just put the data directly after the header struct that describes the array.

For example, an array of ints:

struct int_array {

size_t num_ints;

};

This is followed, directly in memory (and on disk) by num_ints ints. So to access the array I would do:

int get_array_item(int_array *a, size_t i)

{

int *start = (int *)( (char *)a + sizeof(int_array) );

return start[i];

}

How to reuse your code that contain the same part of many objects?

ReplyDelete"Since the resource data is just simple structs, not classes with virtual functions, we can just write it to disk and read it back as we please."


ReplyDeleteWell, how do you cope with alignment constraints and portability?

A: The runtime data is platform specific and always (cross-)compiled on Win32 (see the post "Our Tool Architecture").



ReplyDeleteWe do endian swapping in the cross-compiler when we write the data (so that we don't need to do anything when we read the data).

We could do platform specific padding for structure alignment at that point as well, but so far we haven't seen any need for that, we use the same alignment on all platforms.

I really like this idea.





ReplyDeleteI had thought there could be an annoyance when only using offsets because you need to base address of you memory chunk in order to follow the pointer. Then I realised - as it looks like in your diagram - that the offsets are can be offset from the offset's address (like a short jump instruction). That's great. Have I understood correctly?

These are ideas I've been sitting on myself for many years. We used to use tricks like this when sharing memory between processes before threads really took off. The pointer swizzling (as it was called) was big with "object" databases. Konstantin Kniznick has a great little example of this kind of thing http://www.garret.ru/ipc.html .

I presume that use of STL is still problematic? Perhaps it would be possible if the container were parameterised with an allocator and a pointer template.

I'm interested in language support for this style of programming and the needs of high-performance computing applications - particularly games. This style feels mostly functional - perhaps with lessons from array/vector languages such as APL. Any thoughts?

Oh, Kniznick's example is called Shm.

ReplyDeleteYou could use either relative or absolute offsets. I've actually mostly used absolute offsets. Typically because the pointers tend to appear in "header data" (like in the particle example above) and when I handle the header data I have ready access to the base pointer. However I can certainly see situations where it would make more sense to use relative offsets.



ReplyDeleteYes, I don't use STL container classes (I use though) partially because of this but also for other reasons (the custom allocator interface is strange, std::map is not super-fast, std::deque is not a ringbuffer, etc).

It would be nice if the language had a way to describe this kind data structures (variable sized structs, etc). So that they could be used without too much pointer casting

That should say: "I use <algorithms> though." Blogspot ate my angle brackets.

ReplyDeleteHow do references between resources fit into this scheme? For example, if the particle system needs to reference a texture. It seems a shame to do pointer patching when the blob would otherwise be read-only.

ReplyDeleteIn the blob the resource is referenced by name (hash), during runtime the system resolves that name to a pointer using the resource manager. The pointer is then typically stored in runtime/dynamic data (if it needs to be kept around).

ReplyDeleteThat makes sense. Thanks for sharing this info.

ReplyDelete"We could do platform specific padding for structure alignment at that point as well, but so far we haven't seen any need for that, we use the same alignment on all platforms."


ReplyDeleteHow do you force the alignment on your structs? Is something like struct Foo {...} __attribute__((aligned (4))); + fwrite(Foo); enough to cope with alignment constraints on each and every platform?

We make sure when we create the blob that the structs are aligned with the start of the blob in accordance with the platform that has the strictest requirements. (We just manually pad to enforce the alignment.) Then when we allocate the memory to read the blob into, we also make sure that we allocate the memory with sufficient alignment.

ReplyDeleteNorton.com/setup -Let's get Started with Norton Security as we are here to get you the easiest way to Setup Norton Security. Feel free to contact us if you need any help visit on : norton.com/setup .





ReplyDeleteGet robust protection by downloading and installing the McAfee antivirus. Go to mcafee.com/activate and enter the product key to activate your McAfee product. Create an account on McAfee website at mcafee.com/activate and then go through the downloading, installing and activating the process.






ReplyDeleteNorton Internet Security or Norton Antivirus products are the essential tools for protecting the computer or digital devices from malware, spyware, Trojans and other virus attacks. For Internet threats Norton products are very effective.

norton.com/setup

If you want to use your Webroot service, you need to redeem the activation code. It is a 20 digit alphanumeric code that you can find in your registered email ID's inbox when you purchase it online. Please check the retail card if you bought it from an offline store. You can also try logging in to your Webroot account at webroot.com/safe and get the keycode.


ReplyDeletegarmin.com/express is a direct url for garmin updates and installation for every Garmin product. Device Support is also available just use the chat icon on the website and get instant help about your concern.



ReplyDeletegoogle 2786

ReplyDeletegoogle 2787

google 2788

google 2789

google 2790

google 2791




ReplyDeletejoker123

ฝาก-ถอนไม่เกิน 5 วิ ไวมาก





ReplyDeleteslotxo auto

ฝาก-ถอน ไวจริง

Get the latest Ecdp stock quotes, news and trends at your fingertips across all of your devices, available 247. Our stock quote system helps financial professionals keep up on the latest data and locate charts to help in their own business.


ReplyDeleteAFM Logistics Pvt Ltd is an international freight forwarding and customs clearing company established in Delhi. The company was constituted in 2012 and is indulged in providing complete logistics solution. The company has its own setup and wide network of agents throughout the world. . Best Custom Clearing Company in Delhi . They are the best air cargo and ocean freight forwarding company in Delhi, India. AFM Logistics Pvt Ltd has been working as Import and Export Agent in India since 2012. They have been providing personal baggage shipping services in India for a very long time.

ReplyDelete영주출장안마



ReplyDelete군산출장안마

장수출장안마

영천출장안마

영천출장안마

익산출장안마

임실출장안마

We offer a Global Logistics Network with our worldwide offices and also high quality distribution facilities which are staffed by dedicated teams of the top experts. We have more than 30 years of experience in this field.





ReplyDeleteServices:

Air Freight Forwarding Services

Ocean Freight

Railway Logistic

Third Party Import Export

Trucking Delivery

Third Country

Custom Clearance

Phone:- +91-859-585-1414

Email: info@guppygold.com

Website: www.guppygold.com

This article is full of useful tips. I’ll be sure to implement them!

ReplyDelete