---
title: Object-Oriented Structures in C | Ming-Lun "Allen" Chou | 周明倫
url: https://allenchou.net/2012/01/object-oriented-structures-in-c/
author: Allen Chou
published: '2012-01-27'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This is my second semester at [DigiPen](http://digipen.edu/). We’re not allowed to build our game in C++ for this semester; instead, we can only use C. That means no function overloading, no polymorphism, no generics, and no operator overloading. However, this does not stop me from trying to mimic object-oriented programming with C. My instructor for the programming class last semester, Elie Abi Chahine, mentioned a book called “Object-Oriented Programming with ANSI C” by Axel-Tobias Schreiner (published in 1993). And that was where I started looking for inspirations.

The book was written almost 20 years ago, and a lot of the sample code is obsolete. After all, now that we have C++ at hands, why would anyone want to mimic object-oriented programming with C? But we have to use C, so I read the book. Half-way through the book, the code started to get ugly. Tons of code that I could not decipher was dedicated to fancy features such as run-time type check and virtual function tables. I decided to stop, because I thought I had learned enough concepts and the second half of the book would be an overkill for our project.

I spent a week trying to work out a feasible design to mimic object-oriented programming with C, and finally I came up with an approach that is simple enough, yet sufficient for our project.


### Object-Oriented Structures

Classes are emulated using structures, and virtual functions are mimicked using function pointers. Basically, to achieve polymorphism, the function pointers in **superstructures**?(or?**base structures**),?are re-assigned different functions in the **substructure**?(or **derived structure**)?constructors.

Let’s say we have a base structure that contains a name string and an update function.

typedef struct BaseStruct { char *name; void (*update) (struct BaseStruct self, const float dt); } BaseStruct;

The construction of this struct involves two separate functions: a **new** function and an **init** function. The former is for allocating memory, and the latter is for data member initialization.

BaseStruct *BaseStruct_new(const char *name) { //allocate memory BaseStruct *bs = (BaseStruct *) malloc(sizeof(BaseStruct)); //initialize data members BaseStruct_init(bs, name); return bs; } void BaseStruct_init(BaseStruct *self, const char *name) { //initialize name self->name = (char *) malloc(sizeof(char) * (strlen(name) + 1)); strcpy(self->name, name); //initialize member function pointer self->update = BaseStruct_update; }

Somewhere in the client code, the update function may be indirectly invoked through the function as follows:

void udpateStructure(BaseStruct bs, const float dt) { bs->update(bs, dt); }

Note a pointer to the structure itself has to be passed into the member function being invoked, since there is no **this pointer** in C.

Next, a derived structure with an extra data member of character array can be defined as below:

typedef struct DerivedStruct { BaseStruct super; char *message; } DerivedStruct;

The type of the first data member must be of the base structure, so the initial memory layout of both structures are identical. Therefore, an instance of the derived structure can be pointed by a pointer that points to instances of the base structure.

Here are the **new** and **init** functions for the derived structure:

DerivedStruct *DerivedStruct_new ( const char *name, const char *message ) { //memory allocation DerivedStruct*ds = (DerivedStruct*) malloc(sizeof(DerivedStruct)); //initialize data members DerivedStruct_init(ds, name, message); return ds; } void DerivedStruct_init ( DerivedStruct*self, const char *name, const char *message ) { //super constructor BaseStruct_init(&(self->super), name); //initialize message self->message = (char *) malloc(sizeof(char) * (strlen(message) + 1)); strcpy(self->message, message); //function overriding ds->super.update = DerivedStruct_update; }

The reason why I separated the **new** and **init** functions should become clear now. These two functions are separated so that in the **init** function of the derived structure, the **super** data member can get initialized by the **init** function of the base structure. This is just like how constructors work in C++. Also, the member function pointer gets assigned a different function, so the following function call would actually invoke the newly assigned member function, achieving polymorphism.

DerivedStruct *ds = DerivedStruct_new("myName", "myMessage"); //invoked the derived structure version udpateStructure(ds, 1.0f / 60.0f);

The **dispose** functions that clean up memory work in a fashion similar to destructors in C++: the memory de-allocation works in reverse order as opposed to memory allocation.

void BaseStruct_dispose(BaseStruct *self) { //de-allocate name free(self->name); } void DerivedStruct_dispose(DerivedStruct *self) { //de-allocate name free(self->message); //super deconstructor BaseStruct_dispose(&(self->super)); }

That’s pretty much how I mimic object-oriented programming with C. I’ve successfully built a hierarchical rendering system based on scene graphs (see [my article](http://www.cjcat.net/2011/02/matrix-stack-and-the-visitor-pattern/)) and a command framework (see [my tutorials](http://active.tutsplus.com/series/as3-command-pattern-tutorials/)) using this approach.

Now that we can create object-oriented structures in C, I’m really looking forward to how our project would turn out 🙂

Pingback: Function Pointers vs Member Function Pointers | CJ's Blog

I was wondering why the first data member of the derived class was of the base structure and not a base structure pointer. Then all was clear after I read this:

“The type of the first data member must be of the base structure, so the initial memory layout of both structures are identical. Therefore, an instance of the derived structure can be pointed by a pointer that points to instances of the base structure.”

But won’t the compiler still yell at you if you don’t typecast it? Might as well make it a pointer?

I think both ways work. I just like objects of the derived class to have identical memory layout as objects of the base class. Also, I prefer the following code:

`BaseStruct *obj = (BaseStruct *) derivedObject;`

than:

`BaseStruct *obj = derivedObject->super;`

Hey pretty cool blog post. We’re doing something really similar in our game too! Thanks for letting me read 🙂