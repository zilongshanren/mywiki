---
title: Building a Data-Oriented Entity System (part 1)
url: https://bitsquid.blogspot.com/2014/08/building-data-oriented-entity-system.html
author: Niklas
published: '2014-08-27'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

We have recently started to look into adding an entity/component system to the Bitsquid engine.

You may be surprised to learn that the Bitsquid engine isn't already component based. But actually there has never been a great need for that. Since the gameplay code is usually written in Lua rather than C++, we don't run into the common problems with deep and convoluted inheritance structures that prompt people to move to component based designs. Instead, inheritance is used very sparingly in the engine.

But as we are expanding our [plugin system](http://bitsquid.blogspot.se/2014/04/building-engine-plugin-system.html), we need a way for C++ plugins to bestow game objects with new functionalities and capabilities. This makes a component architecture a very natural fit.

## Entities and Components

In the Bitsquid engine, we always strive to keep systems decoupled and data-oriented and we want to use the same approach for the component architecture. So, in our system, entities are not heap allocated objects. Instead, an entity is just an integer, a unique ID identifying a particular entity:

```
struct Entity
{
unsigned id;
};
```

A special class, the *EntityManager* keeps track of the entities that are alive.

A component is not an object either. Instead, a component is something that is handled by a *ComponentManager*. The task of a *ComponentManager* is to associate entities with components. For example, the *DebugNameComponentManager* can be used to associate debug names with entities:

```
class DebugNameComponentManager
{
public:
void set_debug_name(Entity e, const char *name);
const char *debug_name(Entity e) const;
};
```

Two things are interesting to note about this decoupled design.

First, there is no *DebugNameComponent* class for handling individual debug name components in this design. That is not needed, because all component data is managed internally by the *DebugNameComponentManager*. The manager *could* decide to use heap allocated *DebugNameComponent* objects internally. But it is not forced to. And usually it is much more efficient to lay out the data differently. For example, as a structure of arrays in a single continuous buffer. In a future post, I'll show some examples of this.

Second, there is no place where we keep a list of all the components that an entity has. It is only the *DebugNameComponentManager* that knows whether an entity has a debug name component or not, and if you want to talk about that component you have to do it through the *DebugNameComponentManager*. There is no such thing as an "abstract" component.

So what components an entity has is only defined by what has been registered with the different component managers in the game. And plugins may extend the system with new component managers.

It is up to the component manager to decide if it makes sense for an entity to have multiple components of its type. For example, the *DebugNameComponentManager* only allows a single debug name to be associated with an entity. But the *MeshComponentManager* allows an entity to have multiple meshes.

The manager is responsible for performing any computations necessary to update the components. Updates are done one component manager at a time, not one entity at a time, and when a component manager is updated it updates all its components in one go. This means that common calculations can be shared and that all the data is hot in the caches. It also makes the update easier to profile, multithread or offload to an external processor. All this translates to huge performance benefits.

## The EntityManager

We want to be able to use the entity ID as a weak reference. I.e., given an entity ID we want to be able to tell if it refers to a living entity or not.

Having a weak reference system is important, because if we only have strong references then if the entity dies we must notify everybody that might possibly hold a reference to the entity so that they can delete it. This is both costly and complicated. Especially since references might be held by other threads or by Lua code.

To enable weak referencing, we use the *EntityManager* class to keep track of all live entities. The simplest way of doing that would be to just use a set:

```
class EntityManager
{
HashSet<Entity> _entities;
Entity _next;
public:
Entity create()
{
++_next.id;
while (alive(_next))
++_next.id;
_entities.insert(_next);
return _next;
}
bool alive(Entity e)
{
return _entities.has(e);
}
void destroy(Entity e)
{
_entities.erase(e);
}
};
```

This is pretty good, but since we expect the *alive()* function to be a central piece of code that gets called a lot, we want something that runs even faster than a set.

We can change this to a simple array lookup by splitting the entity ID into an *index* and a *generation* part:

```
const unsigned ENTITY_INDEX_BITS = 22;
const unsigned ENTITY_INDEX_MASK = (1<<ENTITY_INDEX_BITS)-1;
const unsigned ENTITY_GENERATION_BITS = 8;
const unsigned ENTITY_GENERATION_MASK = (1<<ENTITY_GENERATION_BITS)-1;
struct Entity
{
unsigned id;
unsigned index() const {return id & ENTITY_INDEX_MASK;}
unsigned generation() const {return (id >> ENTITY_INDEX_BITS) & ENTITY_GENERATION_MASK;}
};
```

The idea here is that the *index* part directly gives us the index of the entity in a lookup array. The *generation* part is used to distinguish entities created at the same index slot. As we create and destroy entities we will at some point have to reuse an index in the array. By changing the generation value when that happens we ensure that we still get a unique ID.

In our system we are restricted to using 30 bits for the entity ID. The reason for this is that we need to fit it in a 32 bit pointer in order to be able to use a Lua *light userdata* to store it. We also need to steal two bits from this pointer in order to distinguish it from other types of *light userdata* that we use in the engine.

If you didn't have this restriction, or if you only targeted 64-bit platforms it would probably be a good idea to use some more bits for the ID.

We've split up our 30 bits into 22 bits for the index and 8 bits for the generation. This means that we support a maximum of 4 million simultaneous entities. It also means that we can only distinguish between 256 different entities created at the same index slot. If more than 256 entities are created at the same index slot, the *generation* value will wrap around and our new entity will get the same ID as an old entity.

To prevent that from happening too often we need to make sure that we don't reuse the same index slot too often. There are various possible ways of doing that. Our solution is to put recycled indices in a queue and only reuse values from that queue when it contains at least *MINIMUM_FREE_INDICES = 1024* items. Since we have 256 generations, an ID will never reappear until its index has run 256 laps through the queue. So this means that you must create and destroy at least 256 * 1024 entities until an ID can reappear. This seems reasonably safe, but if you want you can play with the numbers to get different margins. For example, if you don't need 4 M entities, you can steal some bits from *index* and give to *generation*.

A nice thing about only having 8 bits in *generation* is that we just need 8 bits per entity in our lookup array. This saves memory, but also gives us better performance, since we will fit more in the cache. With this solution, the code for the *EntityManager* becomes:

```
class EntityManager
{
Array<unsigned char> _generation;
Deque<unsigned> _free_indices;
public:
Entity create()
{
unsigned idx;
if (_free_indices.size() > MINIMUM_FREE_INDICES) {
idx = _free_indices.front();
_free_indices.pop_front();
} else {
_generation.push_back(0);
idx = _generation.size() - 1;
XENSURE(idx < (1 << ENTITY_INDEX_BITS));
}
return make_entity(idx, _generation[idx]);
}
bool alive(Entity e) const
{
return _generation[e.index()] == e.generation();
}
void destroy(Entity e)
{
const unsigned idx = e.index();
++_generation[idx];
_free_indices.push_back(idx);
}
};
```

In the next post, we will take a look at the design of the component classes.

Really interesting post, thank you for sharing! Reminds me of this article by Noel Llopis - http://gamesfromwithin.com/managing-data-relationships I'd be interested to hear your thoughts on the difference in design. Thanks!

ReplyDeleteIs EntityManager::alive really needed? Does the return value mean anything by itself? A "living" entity can be anything (sound, mesh, trigger, tank AI, whatever) So I suppose after calling alive() there would always be a second function call like TankManager::hasTankComponent(Entity), right?



ReplyDeleteIf the game code is multithreaded, won't EntityManager become a bottleneck very quickly?

Isn't the whole idea by having unique component managers that you wouldn't need to check if an entity has "this" component? No entity knows of its components. This makes EntityManager::alive essential to component managers to know if it should handle an registered entity or not.

DeleteYou could do without EntityManager::alive() and just say that an entity is alive iff it has any registered components. But things like destroying an entity becomes a bit tricky then... you have to go to each ComponentManager (which you don't have a list of) and tell it to destroy the entity. I think ::alive() is a better approach. It will hopefully be a bit clearer with the next post.

DeleteYour systems should determine if an entity is alive via its component (ie. health component).

DeleteThis comment has been removed by the author.

ReplyDeleteThe entity is just an index. It doesn't know anything. It doesn't have methods or anything.






ReplyDeleteAll "knowledge" should be in the component managers, actually this is why having EntityManager::alive() seems unnecessary.

If EM::alive() returns true that doesn't mean anything because that entity could be *anything*. A sound, a trigger, a tank, a finite state machine, whatever. So calling EM::alive(217) is more like asking "is the ID 217 used for anything?".

A much more likely use case is "is ID 217 a tank?", which should be handled by the TankComponentManager.

My English is far from perfect, so I hope this makes sense :)

How do you handle dependencies between components. E.g. a RagdollManager would also need to access the SkeletonManager. Or some AI component would need to access the physics manager for sensing its environment?

ReplyDeleteThe RagdollManager would talk directly to the SkeletonManager and get its component information for the entity. By definition, components that need to talk to each other need to be aware of each other.


Delete(You could also create a more abstract system where components fulfill services and one component could ask for a component that fulfills a certain service and talk to it through an abstract interface, but in 99 % of the cases that would be severe overdesign. Only use such a design where you absolutely need it.)

Thanks Niklas.

ReplyDeleteSince you mentioned 'services'. Did you think about having a couple of core services (e.g. rendering, input, physics + collision, etc) which would be available to component managers? Or do you have component managers for each of those as well. I am wondering where to pull the line between the engine systems and the entity component system?

In most cases, I think there will be "engine systems" which back the components. So the component manager would just be an interface to an underlying engine system. But for smaller things the system might reside entirely in the component manager.

DeleteThis comment has been removed by the author.

ReplyDeleteShouldn't

ReplyDeleteXENSURE(idx < (1 << ENTITY_INDEX_BITS));

be changed to

XENSURE(!(idx & ~ENTITY_INDEX_MASK));

?

Aren't those equivalent?

DeleteIndeed they are, my bad. By the way, thanks for another great article. I'm a great fan of your blog, I forgot to mention that :)

DeleteWhat's the advantage of using the approach you proposed, that Entity holds only its ID and then use Managers to indirectly access Entity's Components? Entity now knowing what Components does it have, and using indirect access to its components seems a bit weird. Could this (just an example):



ReplyDeletestruct MeshEntity {

uint renderCompId;

uint physicsCompId;

}

be used? It's much more straightforward when accessing components, it's logical and it can be easily extended to multiple types of mesh entity, if really needed. It would still benefit from cache hits and decoupled design of the objects, it's just prettier, or am I missing something? I hope my questions makes sense, and I apologize for my English.

I believe I found an answer here: http://www.dataorienteddesign.com/dodmain/node14.html (last chapter)


DeleteThe main advantage of the Entity-holds-only-its-id approach is that certain Entity can then dynamically get new Components attached to it. So you don't end up being restricted by the class definition which Components it can hold, but rather have full freedom to attach/detach components to Entity.

Have I understood right? Is there anything else? It seems to me that there are certain cases, where by directly saying which Components can some object have (so limiting it on purpose), would benefit even more. So, does that come down to the design decision choice for particular object/entity type?

P.S. Great articles.

The idea is to have a single Entity class/struct to represent all kinds of entities, not separate structs for different kinds of entities. So an entity is just a dynamic collection of components.





DeleteSo the usual alternative to my approach is something like:

struct Entity {

Array component;

};

But this is a lot more heavy handed... now you have dynamic memory allocation, inheritance and virtual functions. Plus you must cast the IComponent * to a concrete type to do anything useful with it.

>inheritance and virtual functions. Plus you must cast the IComponent * to a concrete type to do anything useful with it.

DeleteNot really.

You can still live without this problems, if you'll design your entities and component like that:

http://pastebin.com/9NZjQ52h

You'll have to provide a hash to your components (this can be easily done via Macro and if you forgot to add it, you'll get a compile-time error).

Access to all your components in subsystems should be done via function pointer.

However this design has a lot of advantages, depending on your needs.

This comment has been removed by the author.

ReplyDeleteVery interesting article,


ReplyDeleteonly a question, how do you represent entity hierarchy? here an entity is only an ID, so I imagine that is up to the EntityManager to keep track of childs-parent relationships... but how? or the childs ids are stored as a linked list in the parent Entity struct through a "_next" member?

- DC

Part 3 in this series talks about this. The transform component manages parent/child relationships between entities.

DeleteI guess you're using a Deque instead of a simple Array (as a stack) for _free_indices to make the usage of all indices more uniform rather than always tending to use the same indices (when Array is used instead)?

ReplyDeleteCan you explain why you use index and generation? Why can't id just be used directly to index into the array?

ReplyDeleteWhat's the disadvantages of turning the _generation array into a bool _is_alive array and using the entity id directly to index into that array?

DeleteIn that case you wouldn't be able to tell if a reference referred to an old deleted object or a new object that had been created and happened to end up in the same index slot.

DeleteBut if you keep using the _free_indices and set MINIMUM_FREE_INDICES to 256 * 1024 or higher, wouldn't that achieve the same thing as your index/generation approach but give you more available indices?

DeleteThis comment has been removed by the author.

ReplyDeleteShouldn't you have to first check that the supplied entity is alive in the destroy method?


ReplyDeleteCalling destroy with a dead entity could have two effects:

- make the living entity in that spot die prematurely

- get an index pushed onto the unused deque twice

Agreed. That would be prudent.

DeleteThanks for this enlightening read. I have one concern about the Manager approach you use here. One part of the Entity-Component-System concept, is the idea that systems can utilize several different components, and that they can be shared between different systems. Doing it the way you describe here, won't you risk storing data within several managers? For example an entity's position in the world?

ReplyDeleteit seems your encoding is off:






ReplyDeleteUINT32 code =((id << ENTITY_INDEX_BITS) & ENTITY_INDEX_MASK) | (generation & ENTITY_GENERATION_MASK);

The latter seems to work for me....

this fails as you shift the index upwards and 'or' the generation in, but if I understand correct the generation part should be shifted into the high bits like shown below:

UINT32 code = ((generation & ENTITY_GENERATION_MASK) << ENTITY_INDEX_BITS) | (id & ENTITY_INDEX_MASK);

Is this for make_entity? I did this:



Deletereturn Entity { (generation << ENTITY_INDEX_BITS) | index };

Sorry but what is that XENSURE() function/macro? Can't find it anywhere.

ReplyDeleteI suppose this is assert.

DeleteWeb services are client and server applications that communicate over the World Wide Web’s (WWW) HyperText Transfer Protocol (HTTP). Web services provide a standard means of inter operating between software applications running on a variety of platforms and frameworks. Web Design Services

ReplyDeleteThat is very great. Yellowstone Coat

ReplyDeleteThanks for sharing the depth of knowledge with us.

ReplyDeleteLeather Jacket

We don't have a place to keep track of all the components that an entity possesses. Only the DebugNameComponentManager knows whether an entity has a debug name component, and help with coursework writing you must communicate with it via the DebugNameComponentManager.

ReplyDeletegoogle 3405

ReplyDeletegoogle 3406

google 3407

google 3408

google 3409

The Canon, the famous brand has everything in it's variety starting from their cameras, canon.com/ijsetup to cinematography solutions to the scanner as well as printers – each single thing has its own specific productivity. Download from canon.com/ijsetup

ReplyDeleteand setup on your device. Canon printers are all in one printer that facilitates print, copy and scan. canon.com/ijsetupThe canon printers are designed for personal as well as business use. canon.com/ijsetupThe Canon, the famous brand has everything in it's variety starting from their cameras, to cinematography solutions to the scanner as well as printers – each single thing has its own specific productivity. Download from canon.com/ijsetup and setup on your device.The Canon printer enhances scan functionality, and includes a robust security feature set. canon.com/ijsetup Using a Canon printer service phone, you can get a full installation of the Canon printer and go to the installed Canon printer to download the canon.com/ijsetup driver.Download Canon Printer Drivers from canon.com/ijsetup then Install and setup your canon printer product by visiting canon.com/ijsetup canon.com/ijsetup is the official Web address Provided By Canon So You can Download Driver, Manual & Guides for your Canon Printer. canon.com/ijsetup Canon IJ does not come with the Manual CD for the installation of printer drivers.

This is not the first time I order works here, and I have never had any complaints from the teachers. Therefore, I get out of this situation with the help of professor essay https://essaysprofessors.com

ReplyDeleteThis blog is what I was looking for. This piece of content will really help me. Thanks for sharing it.

ReplyDeletehttps://www.athleisurex.com/football-team-uniforms

수원출장샵


ReplyDelete남해출장샵

가평출장샵

광명출장샵

광명출장샵

안산출장샵

부천출장샵

심심출장샵





ReplyDelete남양주출장샵

의정부출장샵

제천출장샵

횡성출장샵

충주출장샵

부천출장샵

인천출장안마

ReplyDelete세종출장안마

울산출장안마

대구출장안마

부산출장안마

대전출장안마

광주출장안마

제주도출장안마

제주출장안마

서귀포출장안마

Creating an entity in the real world by creating instances of essay revise service essay revise service that differ from each other in attribute values. On this basis, an interaction between entities is established, where an attribute is a property of an entity.

ReplyDeleteI suggest reviewing the training material do my assignment on developing web-based gaming applications, which is basic for developing skills and abilities in using this tool. It forms students' competence systems for the practical use of game code development technologies using modern programming languages.

ReplyDeleteFew people know that this pastime not only adds bright colors and sharp sensations to our everyday lives but also strengthens our mental health. For students who need a break from the busyness of the curriculum, they can trust the services to purchase college research papers who will complete assignments to get a high grade and attend a session of watching a magical movie.


ReplyDeleteBuilding a Data-Oriented Entity System is akin to crafting a meticulously planned journey – one that requires structure, efficiency, and a guiding force. Just as a seasoned traveler relies on a trusted guide like happylife.es to navigate the complexities of a new destination, so too does a developer need a reliable framework to streamline data management in the realm of software development.

ReplyDeleteTypical questions from students, what to do if the topic is not interesting and the teacher is not inspiring? In this case, we look, how to run plagiarism check on google docs and see interesting aspects of a maybe uninteresting topic and look at it from a different angle that gradually becomes interesting for you to refine it in your creative pursuit.

ReplyDeleteHi, thanks for the information about such an interesting theme. I know that every person has an opportunity to buy blog articles for a good price at https://exclusive-paper.com/buy-blog-article-online.php and you can also try.

ReplyDelete고흥콜걸

ReplyDelete구례콜걸

곡성콜걸

광양콜걸

담양콜걸

나주콜걸

순천콜걸

여수콜걸

Excellent post! I learned a lot and can’t wait for more.

ReplyDeleteAppreciate the clear information in this post. If you are studying with

ReplyDeletedatabricks certified data engineer associate dumps, this content helps you understand how to practice effectively. It focuses on building strong fundamentals along with regular testing.