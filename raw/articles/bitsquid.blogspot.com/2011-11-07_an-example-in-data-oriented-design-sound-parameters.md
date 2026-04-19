---
title: 'An Example in Data-Oriented Design: Sound Parameters'
url: https://bitsquid.blogspot.com/2011/11/example-in-data-oriented-design-sound.html
author: Niklas
published: '2011-11-07'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

```
force = 35.3
material = "wood"
weapon = "axe"
```

In the sound editor the sound designer can setup curves and switches that depend on these parameters. So, for example, the designer can choose to play different wav files for a weapon impact, depending on the weapon that was used and the material it hit. In addition the volume and pitch of the sound can be controlled by a curve connected to the force of the impact.

To implement this behavior, we need a way of representing such parameter sets in the engine. Since there can potentially be lots of playing sounds, we need a representation that is as efficient as possible.

If you did a by-the-book C++ design of this problem, you might end up with an abomination like this:

```
struct ParameterValue
{
enum Type {STRING_TYPE, NUMERIC_TYPE};
Type type;
std::string string_value;
float numeric_value;
};
typedef std::map<std::string, ParameterValue> Parameters;
struct SoundInstance
{
// Other members...
Parameters *parameters;
};
std::vector<SoundInstance> playing_sounds;
```

which would result in tons of pointer chasing, memory allocation and data copying.

So let’s fix it!

First, let’s get rid of the strings. Strings should almost only be used for text that is

*displayed to the end user*. For everything else, they are usually a bad idea. In this case, since the only thing we need to do is match strings that are equal (find the parameter named ”material”, check if its is value ”wood”, etc) we can use a hash instead of the full string value:

```
struct ParameterValue
{
enum Type {STRING_TYPE, NUMERIC_TYPE};
Type type;
union {
IdString32 string_value;
float numeric_value;
};
};
typedef std::map<IdString32, ParameterValue> Parameters;
```

IdString32 is our type for representing hashed strings. It just stores a 4-byte string hash. Since it is a POD-type, we can put it in a union together with the numeric value. This takes the ParameterValue struct down to a manageable 8 bytes with no dynamic data allocation.

But we can actually make it even smaller, by just getting rid of the type:

```
union ParameterValue {
IdString32 string_value;
float numeric_value;
};
```

We can do this because when we access the parameter we know which type we want. If we are evaluating a curve, we want a numeric value. If we want to compare it to a hash, we want a string value. Getting rid of the type means we can’t

*assert()*on type errors (if someone has done something silly like setting the ”material” to 3.5 or the ”force” to ”banana”). But other than that everything will work as before.

Next, let’s attack the map:

```
typedef std::map<IdString32, ParameterValue> Parameters;
```

Just like std::string, std::map should set off all kinds of warning bells in your head. std::map is almost never a good choice. Better alternatives are: linear search in a std::vector (for smallish maps), binary search in a sorted array (for larger, static maps) or hash_map.

In this case, we don’t expect there to be that many parameters set on a sound (<10 in the typical case), so linear search is fine:


struct Parameter {

IdString32 key;

union {

IdString32 string_value;

float numeric_value;

};

};


typedef std::vector<Parameter> Parameters;


struct SoundInstance

{

// Other members...

Parameters *parameters;

};


std::vector<SoundInstance> _playing_sounds;


A lot better than what we started with. But I’m still not 100 % satisfied.

I don’t like the fact that we have a vector of sound instances, and each of those contains a vector of parameters. Vectors-in-vectors raise performance warning flags for me. I like it when my data structures are just arrays of POD structs. Then I know that they are cache friendly and don’t put much strain on the memory system. 512 parameter vectors allocated on the heap for 512 playing sounds make me uneasy.

So what can we do? We could go to a fixed number of parameters:

```
struct SoundInstance
{
// Other members...
unsigned num_parameters;
Parameter parameters[MAX_INSTANCE_PARAMETERS];
};
```

Now the SoundInstance is a POD and all the data is just one big happy blob.

The drawback of this approach is that you might need to set

*MAX_INSTANCE_PARAMETERS*pretty high to be able to handle the most complicated sounds. This would waste some memory for all the sounds that use just one or two parameters.

Say you have 512 sounds and MAX_INSTANCE_PARAMETERS = 32, with 8 bytes in the Parameter struct that then totals to 131 K. Not terrible, but not a tuppence either.

There should be some way of doing better. But if we can’t use a dynamic vector, nor a static array, what can we then possibly use?

A linked list!

Regular linked list have horrible cache behavior and are best stayed away from. But we can achieve the benefits of linked lists while still having decent cache performance by putting the list in an array:

```
struct ParameterNode {
IdString32 key;
union {
IdString32 string_value;
float numeric_value;
};
ParameterNode *next;
};
ParameterNode nodes[MAX_PARAMETERS];
struct SoundInstance
{
// Other members...
ParameterNode *parameters;
};
std::vector<SoundInstance> playing_sounds;
```

Now we have all the parameters stored in a single memory blob. And instead of having a maximum number of parameters per sound, we have a total limit on the number of set parameters (which works much better when most sounds have few parameters). We could get rid of that limit as well if we needed to, by using a vector instead of an array to store the nodes and indices instead of pointers for the ”links”.

You can use many different strategies for allocating nodes from the array. My favorite method is to walk over the array until the next free node is found:

```
unsigned last_allocated = MAX_PARAMETERS-1;
Node *allocate_node()
{
while (true) {
last_allocated = (last_allocated + 1) % MAX_PARAMETERS;
if (nodes[last_allocated].key == 0)
break;
}
return &nodes[last_allocated];
}
```

Here, an empty key is used to indicate free nodes.

The advantage of this method is that nodes that are allocated at the same time end up in adjacent array slots. This means that all the parameters of a particular sound (which tend to get set at the same time) get stored next to each other in memory, which means they can be accessed without cache misses.

Could you please clarify on usage of indices instead of pointers for "links" in case of vectors? Is it because pointers on vector items may get invalidated?

ReplyDeleteYes, exactly. If the vector is resized so that its buffer gets reallocated, pointers to its elements will be invalidated. By using indices instead the links remain valid.

ReplyDeleteIf sound instances are created and destroyed, then eventually the nodes will no longer be adjacent. How shall we deal with this?

ReplyDeleteThe idea is that when the last_allocated counter wraps around, most of the sounds from the previous round will have stopped playing (the only exception being a few very long-lived or looping sounds). So the nodes will still be "mostly" adjacent on subsequent rounds (only interspersed with the parameters from a few long-lived sounds).

ReplyDeleteHi, I've read the post http://bitsquid.blogspot.com/2010/09/custom-memory-allocation-in-c.html about custom allocators and I have a question. You said, that all were required to alloc memory through this (allocators) system, but what about libraries like OpenGL or DirectX? After all, there isn't possibility to change the way they alloc memory..., is it?

ReplyDeleteDo you have numbers on this? Appart from the memory size. Average number of cache misses, execution time, performance increase with your code..

ReplyDeleteNope, since I wrote the code like this to start with, I don't have any old code to compare with.



ReplyDeleteIn general I'm a bit sceptic to synthetic micro-benchmarks. (Measuring the performance of a very isolated tiny tiny part of the code.) They can easily lead you to focus on the wrong thing (optimizing a tiny part of the code that don't matter at all to your total performance). They can also lead you to "overfit" your code to synthetic data. I.e. changes that improve the performance in your for(i=1; i<1000000; ++i) test case may have no effect or actually be bad for performance on "real-world" data.

What I do instead is do a reasonable, good-performance, cache-friendly design of every system up front (to avoid "death-by-a-thousand-cuts") and then focus my optimization efforts on the areas where a top-down profiler tells me I'm spending the most time.

Good blog for this site. Commenting on a blog is an art. This site article is very good.




ReplyDeletewww.office.com/setupoffice setupnorton setupThe Norton Setup atwww.norton.com/setup Norton setup is a process where reach you enter the Norton Setup Key at www.norton.com/setup to trigger & install Norton product. One can get your hands on Norton from retail include or online

ReplyDeleteHow to download and install microsoft office on your device. Follow the steps given here. Ms office is best application of microsoft application.




ReplyDeletewww.office.com/setup, office.com/setup, office setup, office 365 setup, install ms office, ms office setup

www.office.com/setup, office.com/setup, office setup, office 365 setup, install ms office, ms office setup,

www.hulu.com/activate, hulu.com/activate, hulu com activate, hulu activate, hulu.com activate, Hulu Activation Code

www.hulu.com/activate, hulu.com/activate, hulu com activate, hulu activate, hulu.com activate, Hulu Activation Code

This is my blog. Click here.

ReplyDeleteวิธีเล่นสล็อตให้ได้เงิน ส่งตรงจากนักพนันสายทำเงิน"

McAfee Antivirus Tools are developed by Symantec Corporation, provides a complete Anti-Virus suite for PCs.o to your McAfee Antivirus software and Open it. · Enter the 25 digits alpha-numeric product key that was mailed to you

ReplyDeletewww.mcafee.com/activate

mcafee.com.com/activate"

<a href="https://mcafee-activation.com/>mcafee activation</a>

Suggest good information in this message, click here.

ReplyDeleteมวยออนไลน์

ไก่ชนออนไลน์

google 1108

ReplyDeletegoogle 1109

google 1110

google 1111

google 1112

google 1113

google 1114

This is a very Useful & Informative Topic, I got lots of information from it,


ReplyDeleteThere is also something to discuss with you guys,

Door Services Rancho Santa Fe CA

You guys try it for the best Home Inspection services.

StayColdApparel Have exclusive new Designs for you available in Pre-order




ReplyDeleteBook your with StayColdApparel "Stay Cold" (staying cold) to distance yourself from the opinions and expectations of others so you'll be able to achieve the freedom, to go your own way, live true to your own values and become yourself, no matter what! Its your life and you set the rules! Make the best out of it. Stay Cold.

For more details Visit us:- www.staycoldapparel.com

This article was such a pleasant surprise. The tips are practical and easy to put into practice right away.

ReplyDeleteThis comment has been removed by the author.

ReplyDelete


ReplyDeleteThis post really reminded me of my own experience. I had a chemistry exam coming up and there were so many topics to study—it felt like my brain was full of messy information, just like too many sound parameters in the system. I couldn’t stay focused and didn’t know where to start. That’s when I searched for Help with Chemistry Exams online and found a service that explained everything in a simple way. It really helped me stay calm and study better!