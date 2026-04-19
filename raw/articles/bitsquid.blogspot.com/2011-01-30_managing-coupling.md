---
title: Managing Coupling
url: https://bitsquid.blogspot.com/2011/01/managing-coupling.html
author: Niklas
published: '2011-01-30'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

[http://altdevblogaday.com/](http://altdevblogaday.com/).)

The only way of staying sane while writing a large complex software system is to regard it as a collection of smaller, simpler systems. And this is only possible if the systems are properly decoupled.

Ideally, each system should be completely isolated. The effect system should be the only system manipulating effects and it shouldn’t do anything else. It should have its own update() call just for updating effects. No other system should care how the effects are stored in memory or what parts of the update happen on the CPU, SPU or GPU. A new programmer wanting to understand the system should only have to look at the files in the effect_system directory. It should be possible to optimize, rewrite or drop the entire system without affecting any other code.

Of course, complete isolation is not possible. If anything interesting is going to happen, different systems will at some point have to talk to one another, whether we like it or not.

The main challenge in keeping an engine “healthy” is to keep the systems as decoupled as possible while still allowing the necessary interactions to take place. If a system is properly decoupled, adding features is simple. Want a wind effect in your particle system? Just write it. It’s just code. It shouldn’t take more than a day. But if you are working in a tightly coupled project, such seemingly simple changes can stretch out into nightmarish day-long debugging marathons.

If you ever get the feeling that you would prefer to test an idea out in a simple toy project rather than in “the real engine”, that’s a clear sign that you have too much coupling.

Sometimes, engines start out decoupled, but then as deadlines approach and features are requested that don’t fit the well-designed APIs, programmers get tempted to open back doors between systems and introduce couplings that shouldn’t really be there. Slowly, through this “coupling creep” the quality of the code deteriorates and the engine becomes less and less pleasant to work with.

Still, programmers cannot lock themselves in their ivory towers. “That feature doesn’t fit my API,” is never an acceptable answer to give a budding artist. Instead, we need to find ways of handling the challenges of coupling without destroying our engines. Here are four quick ideas to begin with:

**1. Be wary of “frameworks”.**

By a “framework” I mean any kind of system that requires all your other code to conform to a specific world view. For example, a scripting system that requires you to add a specific set of macro tags to all your class declarations.

Other common culprits are:

- Root classes that every object must inherit from
- RTTI/reflection systems
- Serialization systems
- Reference counting systems

Such global systems introduce a coupling across the entire engine. They rudely enforce certain design choices on all subsystems, design choices which might not be appropriate for them. Sometimes the consequences are serious. A badly thought out reference system may prevent subsystems from multithreading. A less than stellar serialization system can make linear loading impossible.

Often, the motivation given for such global systems is that they increase maintainability. With a global serialization system, we just have to make changes at a single place. So refactoring is much easier, it is claimed.

But in practice, the reverse is often true. After a while, the global system has infested so much of the code base that making any significant change to it is virtually impossible. There are just too many things that would have to be changed, all at the same time.

You would be much better off if each system just defined its own save() and load() functions.

**2. Use high level systems to mediate between low level systems.**

Instead of directly coupling low level systems, use a high level system to shuffle data between them. For example, handling footstep sounds might involve the animation system, the sound system and the material system. But none of these systems should know about the others.

So instead of directly coupling them, let the gameplay system handle their interactions. Since the gameplay system knows about all three systems, it can poll the animation system for events defined in the animation data, sample the ground material from the material system and then ask the sound system to play the appropriate sound.

Make sure that you have a clear separation between this messy gameplay layer, that can poke around in all other systems, and your clean engine code that is isolated and decoupled. Otherwise there is always a risk that the mess propagates downwards and infects your clean systems.

In the BitSquid Tech we put the messy stuff either in Lua or in Flow (our visual scripting tool, similar to Unreal’s Kismet). The language barrier acts as a firewall, preventing the spread of the messiness.

**3. Duplicating code is sometimes OK!**

Avoiding duplicated code is one of the fundamentals of software design. Entities should not be needlessly multiplied. But there are instances when you are better off breaking this rule.

I’m not advocating copy-paste-programming or writing complicated algorithms twice. I’m saying that sometimes people can get a little overzealous with their code reuse. Code sharing has a price that is not always recognized, in that it increases system coupling. Sometimes a little judiciously applied code duplication can be a better solution.

An typical example is the String class (or std::string if you are thusly inclined). In some projects you see the String class used almost everywhere. If something is a string, it should use the Stringclass, the reasoning seems to be. But many systems that handle strings do not need all the features that you find in your typical String class: locales, find_first_of(), etc. They are fine with just aconst char *, strcmp() and maybe one custom written (potentially duplicated) three-line function. So why not use that, the code will be much simpler and easier to move to SPUs.

Another culprit is FixedArray a . Sure, if you write int a[5] instead you will have to duplicate the code for bounds checking if you want that. But your code can be understood and compiled without fixed_array.h and template instantiation.

And if you have any method that takes a const Vector &v as argument you should probably take const T *begin, const T *end instead. Now you don’t need the vector.h header, and the caller is not forced to use a particular Vector class for storage.

A final example: I just wrote a patching tool that manipulates our bundles (aka pak-files). That tool duplicates the code for parsing the bundle headers, which is already in the engine. Why? Well, the tool is written in C# and the engine in C++, but in this case that is kind of beside the point. The point is that sharing that code would have been a significant effort.

First, it would have had to be broken out into a separate library, together with the related parts of the engine. Then, since the tool requires some functionality that the engine doesn’t (to parse bundles with foreign endianness) I would have to add a special function for the tool, and probably a #define TOOL_COMPILE since I don’t want that function in the regular builds. This means I need a special build configuration for the tool. And the engine code would forever be dirtied with the TOOL_COMPILE flag. And I wouldn’t be able to rearrange the engine code as I wanted in the future, since that might break the tool compile.

In contrast, rewriting the code for parsing the headers was only 10 minutes of work. It just reads a vector of string hashes. It's not rocket science. Sure, if I ever decide to change the bundle format, I might have to spend another 10 minutes rewriting that code. I think I can live with that.

Writing code is not the problem. The messy, complicated couplings that prevent you from writing code is the problem.

**4. Use IDs to refer to external objects.**

At some point one of your systems will have to refer to objects belonging to another system. For example, the gameplay layer may have to move an effect around or change its parameters.

I find that the most decoupled way of doing that is by using an ID. Let’s consider the alternatives.

Effect *, shared_ptr

A direct pointer is no good, because it will become invalid if the target object is deleted and the effect system should have full control over when and how its objects are deleted. A standardshared_ptr won’t work for the same reason, it puts the life time of Effect objects out of the control of the effect system.

Weak_ptr, handle

By this I mean some kind of reference-counted, indirect pointer to the object. This is better, but still too strongly coupled for my taste. The indirect pointer will be accessed both by the external system (for dereferencing and changing the reference count) and by the effect system (for deleting the Effect object or moving it in memory). This has the potential for creating threading problems.

Also, this construct kind of implies that external systems can dereference and use the Effectwhenever they want to. Perhaps the effect system only allows that when its update() loop is not running and want to assert() that. Or perhaps the effect system doesn’t want to allow direct access to its objects at all, but instead double buffer all changes.

So, in order to allow the effect system to freely reorganize its data and processing in any way it likes, I use IDs to identify objects externally. The IDs are just an integers uniquely identifying an object, that the user can throw away when she is done with them. They don’t have to be “released” like aweak_ptr, which removes a point of interaction between the systems. It also means that the IDs are PODs. We can copy and move them freely in memory, juggle them in Lua and DMA them back-and-forth to our heart’s content. All of this would be a lot more complicated if we had to keep reference counts.

In the system we need a fast way of mapping IDs back to objects. Note that std::map is not a fast way! But there are a number of possibilities. The simplest is to just use a fixed size array with object pointers:

Object *lookup[MAX_OBJECTS];

If your system has a maximum of 4096 objects, use 12 bits from the key to store an index into this array and the remaining 20 bits as a unique identifier (i.e., to detect the case when the original object has been deleted and a new object has been created at the same index). If you need lots of objects, you can go to a 64 bit ID.

That's it for today, but this post really just scratches the surface of decoupling. There are a lot of other interesting techniques to look at, such as events, callbacks and “duck typing”. Maybe something for a future entry...

Using IDs for external references, wouldn't that possibly incur a rather large cost for function calls on that object? For example, refering to an object in a scene graph, to change a property (like local transform) on that object you would have to call something like




ReplyDelete_scenegraph->set_object_transform( object_id, transform );

which would in effect translate to a lookup in the object table, a check to make sure the unique id is valid, and then a call to set the actual property data.

I guess you would use this with a design where external access to objects in a subsystem is restricted to higher level functions where the overhead costs are small in comparison with the actual function implementation? I.e not for get/set properties-like functions.

Love this. From the perspective of being the guy writing the messy gameplay-code, a sound structure is key to being able to work efficiently and in somewhat harmony with the engine, love it! I'm looking forward for future entries.

ReplyDelete@Mattias - I'm guessing in that case, the graph would consume a stream of set_transform events.



ReplyDeletehttp://bitsquid.blogspot.com/2009/12/events.html

Regarding the cost of ID validation -- on the bright side, this means you wont ever crash because of a bad pointer ;)

You could even reserve object #0 in each system as a "null struct", and conditionally select offset '0' instead of 'ID' if 'ID' is invalid -- meaning you don't even have to branch to deal with bad pointers (they just read/write these pre-reserved junk "null structs").

@Mattias - As I said in the post, the cost is one extra pointer access (the test is nearly free, since you can branch hint that the object still exists). So not too bad.





ReplyDeleteAnd the IDs don't necessarily have to be indirect references. Since the external system just treats them as opaque data, they could be something else if you like.

For example, our scene graph is essentially just:

struct {

Vector local_transform;

Vector world_transform;

Vector parent;

}

And the object_id for the scene graph is just an integer index into these arrays.

@Action Man - I like your idea about a "null struct". Haven't thought about that. It is a nice way of getting rid of a lot of "does the object exist?" tests.

ReplyDelete@Action Man - Nice idea, I like it. But wouldn't that possibly lead to other hard-to-track strange behaviour if random readers of the null struct data get stuff from other random writers? Basically anything could be present in the null struct, which is as bad as reading from random memory (except for not getting a potential access violation).


ReplyDelete@Niklas - Ah, right, good point. I guess I'm still stuck a bit in my object oriented thinking, but seeing your example of a more data-oriented approach of the system the ideas fall in to place and makes a lot of sense. Cheers.

Great post, I was just wondering how you would add/delete data to the simple arrays of objects?

ReplyDelete@Amir You can use an "in-place free list". I.e. you keep a linked list of the free slots in the lookup[] array. But you store the linked list in the lookup[] array itself. So in each free slot in lookup[] you store the index of the next free slot in the linked list. And then you use a variable first_free_slot to point to the first free slot.






ReplyDeleteTo add an object to the array, allocating it from the free list:

int slot = first_free_slot;

first_free_slot = (int)lookup[slot];

To remove an object from the array, adding it to the free list:

lookup[slot] = (Object *)first_free_slot;

first_free_slot = slot;

To make this a complete system, you also need an index value to mark the end of the list (such as 0xffffffff) and a way of allocating a slot when the free list is empty (just keep a count of the number of slots you have used and allocate from the end of the array in that case).

Nice, very minimal and interesting. Now I am wondering how the list of objects can be traversed. How can we know if an element in the array is actually containing an object pointer or represents the next free index? Any specific bits reserved maybe?

ReplyDeleteYes you would need some kind of flag for that. You could go to a struct {} with room for both the flag and the Object *. Or you could try to be clever with bit twiddling. For example, assuming that all allocations are 4-byte aligned, bit 0 of the pointers is never actually used, so you could use that to mark free or occupied nodes.

ReplyDeleteNiklas, how do you handle the case when several subsystems trying to access the entity by its ID?



ReplyDeleteFor example, Scripting subsystem may be working with Foo* entity acquired by some ID, while at the same time this entity gets somehow removed from the World by another subsystem(say Physics).

How do you handler this case? In shared/weak ptrs schema this is handled by "locking" the weak_ptr thus turning it into a shared_ptr. In your case the most obvious way is to access the entity by ID only and never cache the pointer to it. Right? Or you also "lock" the entity explicitly somehow?

No, I solve this at a higher level, by structuring the code so that object deletes cannot happen at the same time as objects are processed.


ReplyDeleteWhen objects are processed in a background thread, I typically do this by delaying deletes. I. e., object deletes are delayed and put in a queue and only executed by the system when it "knows" it is safe. (When it is in sync with the background processing threads.)

Sorry for waking a sleeping thread but while I'm really enjoying this series I'm a bit confused as to how this works for a system like a scene graph. For example:



ReplyDelete1) Children

How do child nodes know when the parent node has been deleted or moved? Is the idea that higher level objects are responsible for aggregating transforms and then deleting/updating them as necessary (e.g. the Car object takes care of telling the wheel transforms that the chassis transform has been deleted)?

2) Updating

How do you keep the various arrays that represent the transforms laid out in the proper order for updating sequentially? Seems like you would have to sort your arrays every time you added or removed a node in the transform hierarchy which looks like a lot of copying of data for such a frequent event.

We don't have a complete graph for the entire scene, instead we have local scene graphs in each of our units/entities.




ReplyDeleteEach node in the graph has a dirty flag that is set if its local matrix has been modified. When we process the graph we check each node in order and compute the new world matrix if its local matrix or its parent's world matrix has been modified.

For units we keep track of which units are linked to other units. Most units are not linked and we update all of those in parallel. The linked units are sorted by link depth and then updated in that order. That guarantees that parents are updated before children.

The transform graphs within units are never resorted. We could do that, but we have not yet found any reason to "re-root" a unit's scene graph.

Great article but it's left me with a few questions.



ReplyDelete1.) Where are the systems?

By this I mean, do you keep an instance of each active system in some kind of World/Engine object or do higher level systems actually own an instance of the lower level systems they depend upon?

2.) Where are the components?

Does each system own an array of components or are they to kept in arrays elsewhere?

e.g. A number of systems need to access world transforms, do those systems need to query the "SceneGraph" system to access a world transform or can they directly reference a pool of components?

1) Systems are owned at the level where it makes sense. Globally shared stuff, like MemoryManager and ThreadManager are owned by the Application. Stuff local to a World (there can be multiple worlds) like ParticleWorld, SoundWorld, etc are owned by the world. Lower level systems get passed references to the shared objects they need when created.


Delete2) They query the scene graph.

Thanks for the response, it's a lot clearer now.

DeleteReally interesting article! I've been struggling with coupling recently. Question: how do you decouple behaviour tree actions? Specifically with disaggregating state into smaller bits to feed into the functions. Everything I've seen seems to pass in the same matching state into every behaviour even if the behaviour only requires a small subset of that state. This isn't scaling for me well though! Any thoughts?

ReplyDeleteNice knowledge gaining article. This post is really the best on this valuable topic.



ReplyDeletenorton.com/setup

office.com/setup

norton.com/setup

such a great information. I like this article.Gas Turbine Labyrinths

ReplyDeleteWe are happy to share this information that we provide an incredible variety of Escorts ladies to customers in Delhi by helping Paharganj escorts also are one in every of them. Hence, don’t suppose an excessive amount of regarding obtaining the nude fucking partner services for your engagements as a result of currently you'll ensure the sex with the correct one.


ReplyDeletePaharganj escorts

Thanks for sharing this brilliant article it was a very useful and helpful article.



ReplyDeleteBangalore Escorts

Banaswadi Escorts

Call Girls in Vijaynagar

Celebrity escorts bangalore

Russian Escorts in Bangalore

whitefield escorts

Call Girls in Bangalore

I enjoyed reading the article above, it explains everything in detail, the article is practical and very interesting. I wish you the best of luck with your future writings. Thank you. Share a profile about the wpm typing tool that will help you improve your typing speed. For more information, check the profile.

ReplyDeleteGreat information you will share.

ReplyDeleteEscorts in Moti Nagar ||

Hauz Khas Escort ||

Munirka Escort ||

Gurgaon Escorts ||

East of Kailash Escorts ||


ReplyDeleteGoa Companionis a professional dating and matchmaking service that helps busy, successful men find beautiful, ambitious girls in Goa.Massage treatments employ essential oils taken from plants to increase relaxation and boost emotional well-being. They are usually included in baths, body to body massage near me or steam therapies.

ReplyDeleteThe relaxing effect triggered by body to body massage in bangalore may result in the reduction of blood pressure, thereby improving the health of your heart.

ReplyDeleteYou are sharing important information in the blog. But there need to be some images to understand the information well



ReplyDeletevisit: Coupling manufacturers in India

camlock coupling manufacturer

quick release coupling manufacturer

Enjoy our massage in hyderabad services from the beautiful hot massage girl therapists, then you must be happy and feel how good your body is after the services

ReplyDeletelooking for a non stop body to body spa near me with afforadable prices and mind blowing therapist.

ReplyDeletethe massage in chennai has gained immense popularity for its unique benefits and techniques

ReplyDeleteOur services are tailored to meet the specific needs of men. visit female to male spa near me hyderabad

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteamazing and great....

ReplyDeletemassage centres near me

good insight

ReplyDeletespa near by me

exciting

ReplyDeletenuru massage in chennai

camlock coupling | quick release coupling manufacturer

ReplyDeleteDr. Rishabh Jaiswal Best Orthopedic Surgeon in Lucknow is a highly skilled and result-oriented professional with over 10 years of experience in Orthopedic Surgery and Consultancy.


ReplyDeletehttps://maps.app.goo.gl/aQpb8vnPQPZzAESZ8

This article gave me the motivation I needed to take action. Thanks for the encouragement!

ReplyDeleteFind the perfect



ReplyDeletelaboratory machinefor your pharma, R&D, or education lab at Tipco Engineering. Quality equipment to meet every experimental need.