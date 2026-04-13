---
title: Using Lua with C++ in practice. Part 2. Implementing the basics
url: https://eliasdaler.wordpress.com/2015/09/08/using-lua-with-cpp-in-practice-part-2/
published: '2015-09-08'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Part 1**. Intro to ECS and basic principles**Part 2**. Implementing the basics**Part 3.**Controlling entities in Lua by calling C++ functions.

Hello, this is a second part of “Using Lua with C++ in Practice” series. I recommend to read the first part to know what’s going on and why using Lua with C++ is awesome! (You’ll see it in this arcticle too, of course).

![](../../assets/550e26ff98fe3488.png)


This tutorial will implement a simple ECS model which I’ll improve and use in other parts of tutorials. Note that this is not the best way to implement ECS. I’m making the most basic ECS which can be used to show the main principles of how things work in my game and how you can use them in general. This is not a tutorial about C++, so I won’t spend too much time discussing C++ parts and I’ll mostly focus on Lua/C++ interaction and binding. Let’s start!


# Implementing basic ECS

Let’s create **Component** base class and simple **GraphicsComponent** and **NpcComponent** classes:

**Component.h**:

#pragma once class Component { public: virtual ~Component() {}; };

**GraphicsComponent.h**:

#pragma once #include <string> #include "Component.h" class GraphicsComponent : public Component { public: GraphicsComponent() {}; void setFilename(const std::string& filename) { this->filename = filename; } std::string getFilename() const { return filename; } private: std::string filename; };

**NpcComponent.h**:

#pragma once #include <string> #include "Component.h" class NpcComponent : public Component { public: NpcComponent() {}; void setPhrase(const std::string& phrase) { this->phrase = phrase; } std::string getPhrase() const { return phrase; } private: std::string phrase; };

Pretty simple. **Entity** class is a bit trickier

**Entity.h**:

#pragma once #include <map> #include <string> #include <typeindex> class Component; class Entity { public: ~Entity(); void addComponent(std::type_index type, Component* c); template <typename T> T* get() { auto it = components.find(std::type_index(typeid(T))); if (it != components.end()) { return dynamic_cast<T*>(it->second); } return nullptr; } void setType(const std::string& type) { this->type = type; } std::string getType() const { return type; } private: std::string type; std::map<std::type_index, Component*> components; };

We store components in

std::map<std::type_index, Component*> components;

This lets us store any components of different types in one **std::map**. Storing Component’s **std::type_index** as the key lets us get components by Component type like this:

auto gc = entity->get<GraphicsComponent>();

This is a very useful function to have. If the entity doesn’t have a component of type you’re trying to get with this function, it will return a **nullptr**.

The **type** member variable is a type of an entity. You can think about it as entity’s class. You can have a “ghost” entity, or a “tree” entity.

Entity.cpp is simple:

#include "Entity.h" #include "Component.h" Entity::~Entity() { for (auto& c : components) { delete c.second; } } void Entity::addComponent(std::type_index type, Component* c) { components[type] = c; }

Here’s how you can create an entity:

Entity* createGhostEntity() { Entity* e = new Entity; // create a graphics component GraphicsComponent* gc = new GraphicsComponent; gc->setFilename("ghost.png"); e->addComponent(std::type_index(typeid(GraphicsComponent)), gc); // create an NpcComponent NpcComponent* npcc = new NpcComponent; npcc->setPhrase("I'M A SCARY GHOST!!!"); e->addComponent(std::type_index(typeid(NpcComponent)), npcc); return e; }

Great, now let’s see how we can move entity descriptions to Lua and don’t hardcode stuff!

The code in the script looks like this:

**ghost.lua**:

ghost = { GraphicsComponent = { filename = "ghost.png" }, NpcComponent = { phrase = "I'M A SCARY GHOST!!!" } }

Here’s how we’ll create an entity using this script with LuaBridge (or a binding of your choice).

- Get a list of component names. In our case it would be {“GraphicsComponent”, “NpcComponent”}.
- Create each component, passing corresponding component table reference in component’s constructor. Component constructors will get data from those tables.
- Add components to entity.

# Geting a list of table keys

To create components, we need to get a list of entity’s table keys and iterate over it, creating components.

This is not as easy as it sounds. Most bindings I’ve used don’t have something like **getTableKeys** function. If your binding has it, lucky for you! Skip to the “Creating components by string” section.

(But I recommend you not to do this, this section will show you some cool stuff you can do with Lua and will remind you of some basic stuff of Lua/C++ interaction, mainly of Lua’s stack.).

You can also skip this section if you are okay with using less convenient syntax for entities. The table may look like this:

ghost = { { componentName = "GraphicsComponent", filename = "ghost.png" }, { componentName = "NpcComponent", phrase = "I'M A SCARY GHOST!!!" } }

In my opinion, this doesn’t look as readable as the previous version, but it lets you do stuff like this with LuaBridge:

using namespace luabridge; LuaRef ghostRef = getGlobal(L, "ghost"); for(int i = 0; i < ghostRef.length(); ++i) { std::string componentName = ghostRef[i + 1]["componentName"].cast<std::string>(); ... // create a component }

Okay, let’s implement the **getTableKeys** function which will let you get a **std::vector** of table keys like this:

std::vector<std::string> keys = luah::getTableKeys(L, "ghost"); // will return {"GraphicsComponent", "NpcComponent"}

Let’s create a header file which will contain function declarations:

**LuaHelperFunctions.h**:

#pragma once #include <vector> struct lua_State; namespace luah { bool loadScript(lua_State* L, const std::string& filename); // will be explained later void lua_gettostack(lua_State* L, const std::string& variableName); // ...and this one void loadGetKeysFunction(lua_State* L); std::vector<std::string> getTableKeys(lua_State* L, const std::string& name); }

Let’s look at this Lua function:

function getKeys(t) s = {} for k, v in pairs(t) do table.insert(s, k) end return s end

This function gets table **t** as the parameter and then returns a table which contains its keys.

Note, that Lua tables can have any non-nil value as a key. So a returned table may contain integers, strings and even other tables! We’ll just assume that the tables which we’ll get keys from would only contain strings for now (I’ll later show how you can ignore non-string keys)

You can store this code in a C++ string like this:

std::string code = R"(function getKeys(t) s = {} for k, v in pairs(t) do table.insert(s, k) end return s end)";

**R** is a **raw string literal**. It’s a pretty cool C++11 feature which lets you to store a string as it is, without adding all that “\n”‘s or “\\” when you want to insert one slash.

Before we can use it, we need to compile and add this function to our Lua state (you have to do this once for every Lua state you intend to use this function with).

Here’s how you can do this:

luaL_dostring(L, code.c_str());

Let’s add this code to **LuaHelperFunctions.cpp**:

void luah::loadGetKeysFunction(lua_State* L) { std::string code = R"(function getKeys(t) s = {} for k, v in pairs(t) do table.insert(s, k) end return s end)"; luaL_dostring(L, code.c_str()); }

Let’s start writing **getTableKeys** function. First, we get our **getKeys** function from globals. If it’s not found there, it means that we didn’t load it before so we need to do this before we can proceed:

std::vector<std::string> luah::getTableKeys(lua_State* L, const std::string& name) { lua_getglobal(L, "getKeys"); // get function if (lua_isnil(L, -1)) { std::cout << "Get keys function is not loaded. Loading..." << std::endl; loadGetKeysFunction(L); lua_getglobal(L, "getKeys"); }

Next, we need to get the table to the stack:

lua_getglobal(L, name);

So, the stack currently looks like this:

![](../../assets/aacffc48a72eead0.png)


Now we can call **getKeys** Lua function:

lua_pcall(L, 1, 1, 0); // execute getKeys function. // One parameter, one return

We’ll also push **nil** to the stack (you’ll see why we need this in a moment).

Here’s what we have on the stack now:

![](../../assets/05a6b0252c913038.png)


**s** is a table of keys which getKeys function returned. We’ll get strings one by one testing whether or not the value in table is a string.

**keys** vector will store string keys:

std::vector<std::string> keys;

And here’s how we get strings from the table:

while (lua_next(L, -2)) { // get values one by one if (lua_type(L, -1) == LUA_TSTRING) { // check if key is a string keys.push_back(lua_tostring(L, -1)); } lua_pop(L, 1); }

Here’s how it works, according to Lua documentation about [lua_next](http://www.lua.org/manual/5.2/manual.html#lua_next):

Pops a key from the stack, and pushes a key–value pair from the table at the given index (the “next” pair after the given key). If there are no more elements in the table, then lua_next returns 0 (and pushes nothing).


We also have to check if the value we just got is a string before we convert it to a string.

Okay, now we only need to remove **s** table which is still on the stack and return the vector:

lua_settop(L, 0); // remove s table from stack return keys; }

Okay, this should work. But this only works with global tables. What if you need to get values from the table which is inside another table? There’s a solution to this too!

Suppose the table we want to get keys of is in the table **someTable**:

someTable = { interestingTable = { ... } }

We’ll call getTableKeys function like this:

auto v = luah::getTableKeys(L, "someTable.interestingTable");

Unfortunately this wouldn’t work for the implementation I’ve given above. That’s because we can’t do this:

lua_getglobal(L, "someTable.interestingTable");

Which our function would try to do. Let’s change this.

Suppose “getKeys” function is already in the stack.

Fist, we have to call lua_getglobal(L, “someTable”) and then lua_getfield(L, “interestingTable”).

Here’s what we’ll have on stack after doing this:

![](../../assets/4465c77c6832bf88.png)


If we call lua_pcall(L, 1, 1, 0) then **someTable** would be used as a function parameter, not **interestingTable**!

So, we need to remove someTable from the stack before we can do this.

Let’s write a function which would let us get tables on stack like this:

lua_gettostack(L, "someTable.interestingTable")

Here’s what we do first:

void luah::lua_gettostack(lua_State* L, const std::string& variableName) { int level = 0; std::string var = ""; for (unsigned int i = 0; i < variableName.size(); i++) { if (variableName.at(i) == '.') { if (level == 0) { lua_getglobal(L, var.c_str()); } else { lua_getfield(L, -1, var.c_str()); } if (lua_isnil(L, -1)) { std::cout << "Error, can't get " << variableName << std::endl; return; } else { var = ""; level++; } } else { var += variableName.at(i); } } if (level == 0) { lua_getglobal(L, var.c_str()); } else { lua_getfield(L, -1, var.c_str()); }

We use dots as separators. The first token of the **variableName** string is a name of a global table which we get with **lua_getglobal**. Then we get other tables which are one inside the other with **lua_getfield**.

Suppose we write this:

lua_getglobal(L, "player.Pos.x")

Here’s what happens:

![](../../assets/77f5348b875b0510.png)


The stack looks like this:

![](../../assets/ac0e8023bcbef96e.png)


We only need to x table to stay on the stack, so we need to do this:

if (level == 0) { return; } // no need to remove anything int tableIndex = lua_gettop(L) - level; lua_replace(L, tableIndex); lua_settop(L, tableIndex); }

We need to remove other tables (**player**, **pos**) from stack if needed. We do this by placing the table which we needed to get in the position where the global table (**player** in our case) was (we can’t just call **lua_replace(L, 0)** because something may already be in the stack!). Then we call **lua_settop** which pops all the unneeded tables from stack.

So, now we need to change this line in luah::getTableKeys:

lua_getglobal(L, name);

to this:

lua_gettostack(L, name);

And our function will work for all tables. Okay, let’s get back to creating components and entities.

# Creating components

Okay, now we can get a list of components to create. But how are we going to create them?

First of all, you need to find a way to create component instances by strings. There are lots of Object Factory implementations, so I won’t provide any, I’ll relay on if/else for simplicity instead.

Let’s add this helper function in our main.cpp:

template <typename T> void addComponent(Entity* e) { e->addComponent(std::type_index(typeid(T)), new T()); }

And here’s our entity creation function which should go in the same file:

Entity* loadEntity(lua_State* L, const std::string& type) { auto e = new Entity(); e->setType(type); auto v = luah::getTableKeys(L, type); for (auto& componentName : v) { if (componentName == "GraphicsComponent") { addComponent<GraphicsComponent>(e); } else if (componentName == "NpcComponent") { addComponent<NpcComponent>(e); } std::cout << "Added " << componentName << " to " << type << std::endl; } return e; }

Great! Now we can create entities like this:

auto e = loadEntity(L, "ghost");

But… this function only create empty components without any data from our scripts, so let’s change that.

This is where LuaBridge comes into play. If you’re using other bindings, don’t worry, I think you’ll find a way to use this code with some changes.

Let’s add forward declaration to **LuaRef** class in **Component.h** like this:

namespace luabridge { class LuaRef; } // forward declaration

And now let’s change GraphicsComponent’s and NpcComponent’s default constructors to this:

GraphicsComponent(luabridge::LuaRef& componentTable);

NpcComponent(luabridge::LuaRef& componentTable);

**componentTable** is a reference to a table from the script which contains data about entity’s component.

Look at the **ghost.lua**. We’ll pass reference to ghost.GraphicsComponent in GraphicsComponent constructor and reference to ghost.NpcComponent in NpcComponent constructor.

Let’s look how these constructors are implemented:

**GraphicsComponent.cpp**:

#include "GraphicsComponent.h" #include <LuaBridge.h> #include <iostream> GraphicsComponent::GraphicsComponent(luabridge::LuaRef& componentTable) { using namespace luabridge; auto filenameRef = componentTable["filename"]; if (filenameRef.isString()) { filename = filenameRef.cast<std::string>(); } else { std::cout << "Error, GraphicsComponent.filename is not a string!" << std::endl; } }

Pretty easy. You can make the error message better if you pass entity type in the constructor, so the error message would tell you which entity’s component data is bad.

NpcComponent constructor looks mostly the same:

**NpcComponent.cpp**:

#include "NpcComponent.h" #include <LuaBridge.h> #include <iostream> NpcComponent::NpcComponent(luabridge::LuaRef& NpcTable) { using namespace luabridge; auto phraseRef = NpcTable["phrase"]; if (phraseRef.isString()) { phrase = phraseRef.cast<std::string>(); } else { std::cout << "Error, NpcComponent.phrase is not a string!" << std::endl; } }

Okay, now let’s change our **addComponent** function:

template <typename T> void addComponent(Entity* e, luabridge::LuaRef& componentTable) { e->addComponent(std::type_index(typeid(T)), new T(componentTable)); }

**loadEntity** function needs to be changed as well:

Entity* loadEntity(lua_State* L, const std::string& type) { using namespace luabridge; auto e = new Entity(); e->setType(type); auto v = luah::getTableKeys(L, type); LuaRef entityTable = getGlobal(L, type.c_str()); for (auto& componentName : v) { if (componentName == "GraphicsComponent") { LuaRef gcTable = entityTable["GraphicsComponent"]; addComponent<GraphicsComponent>(e, gcTable); } else if (componentName == "NpcComponent") { LuaRef npccTable = entityTable["NpcComponent"]; addComponent<NpcComponent>(e, npccTable); } std::cout << "Added " << componentName << " to " << type << std::endl; } return e; }

Not many things changed, but we get **LuaRef**s for corresponding components with **LuaRef** and pass them to **addComponent** function which then passes it to a corresponding Component constructor.

Okay, let’s test it, put this code into your **main** function:

lua_State* L = luaL_newstate(); luaL_openlibs(L); luah::loadScript(L, "ghost.lua"); luah::loadGetKeysFunction(L); auto e = loadEntity(L, "ghost"); auto npcc = e->get<NpcComponent>(); std::cout << e->getType() << " says: " << npcc->getPhrase() << std::endl; lua_close(L);

The output should look like this:

“ghost says: I’M A SCARY GHOST!!!”


Awesome!

# But wait, there’s more!

And that’s it for now. There are lots of things to make while I’m writing the next tutorial. Try to make this system work with some libraries like SFML. Create a EntityFactory class to make entity creation better, create a bunch of components. Experiment and send your feedback to me.

Next time I’ll show you how to call C++ functions from Lua and do this effectively.

Hope you’ve enjoyed the tutorial!

Subscribe to my blog or to [my twitter](https://twitter.com/EliasDaler) to not miss the next part of the tutorial.

Thanks for reading!

Hello

Nice post, as always. :)

Is it possible to unload lua script when its no longer needed to save memory ?

Without deleting whole lua_State ofc :)

Thanks! No, you can’t “unload” a script, you can only remove global variables in your lua_State. So, you have to get list of all global variables in a script and remove them. I’ll show how to do it in the next article. :)

I’ve been reading through your tutorials to try to get a feel for C++ after my long trip to ‘C# land’ :P and I’ve encountered a problem. I can’t push_back into the components map O_o

I’ve updated the post, there was a mistake there. You have to do “components[type] = c;”

Thank you :D

You’re welcome!

Better than std::map use std::unordered_map<std::type_index, std::unique_ptr>

Yeah, I can agree with unique_ptr, I’ll fix it a bit later. undordered_map is not neccessary, though, because Entities always have around 5-10 components, comparing two std::type_index’es is fast, so std::map will do fine and will require less memory than std::unordered_map.

Hello! Great articles, really, but i’m having difficulties understanding a certain part.

Let’s say my GraphicsComponent is dependant on a InputComponent(which takes keyboard input) to decide which sprite animation to draw. How would this work? Doing something like gc->setInputComponent(component); seems like a bad idea to me. Do you have any recommendations on how to do this?

And again, great articles!

Regards,

Oscar

On second thought i’m guessing it’s something to do with the System part of ECS? Like the GraphicsSystem loads all graphics entities and then loads GraphicsComponent and InputComponent?

Hi! The easiest way to decouple InputSystem from everything else is to use events. So, when a player presses the button, you create a “ButtonPressed” event and all systems which are interested in it, get it and process it. For example, GraphicsSystem gets this ButtonPressed event and then sets the needed animation. (But this is too simple, I think you’ll need to have some sort of StateSystem, which’ll get input events and then change the animations)

If the systems are very coupled and use several components very often, you can do such system without any problems, just store two lists of components together! (For example: PhysicsSystem may work on PositionComponent and MovemenComponent and CollisionComponent)

Hello, I was wondering how you would implement a function in your component? i.e. On the last tutorial an image of the ghosts lua file showed CollisionComponent having a collide function. Thanks for the great tutorials!

This will be explained in the next part of the series probably, but here’s a head start: you can store luabridge::LuaRef to collide function from CollisionComponent table and later call it when needed (from C++).

Also, check out this article about Lua entity handles: https://eliasdaler.wordpress.com/2015/11/12/using-lua-with-cpp-in-practice-part-3/

std::string componentName = ghostRef[i + 1][“componentName”].cast();

with this line, I am getting a weird error:

PANIC: unprotected error in call to Lua API (attempt to index a nil value)

any ideas?

Try this:

LuaRef ghostTableRef = ghostRef[i+1];

auto componentName = ghostTableRef[“componentName”].cast();

If it doesn’t help, check if ghostTableRef or ghostTableRef[“componenName”] is nil or not. If it is, maybe you’ve made a mistake somewhere in your script.

that works, any reason as of why the other one wont work? it seems like its essentially the same thing

That’s probably because operator[] returns luabridge::Proxy and not LuaRef so calling operator[] on proxy doesn’t work because it’s a temporary object. I’ll fix this in tutorial later :)

I am not sure if you will read this post because this tutorial is a bit old.

Anyway, I created a namespace which includes those two functions which you wrote into your main.cpp, i. e. loadEntity and addComponent.

Unfortunately, i get an error in that line: LuaRef entityTable = getGlobal(L, type.c_str());

The error says: error: cannot convert ‘lua_State*’ to ‘luabridge::lua_State*’ for argument ‘1’ to ‘luabridge::LuaRef luabridge::getGlobal(luabridge::lua_State*, const char*)’

I am confused why there is the function luabridge::getGlobal with the luabridge::lua_State as parameter instead of the normal lua_State.

My header looks like this

// include ….

struct lua_State;

namespace entityh{

template

void addComponent(entityx::EntityManager& es, const entityx::Entity::Id& id, luabridge::LuaRef& componentTable);

entityx::Entity::Id loadEntity(lua_State* L, entityx::EntityManager& es, const std::string& type);

}

Here is the code snippet of the source file where the error occurs.

entityx::Entity::Id entityh::loadEntity(lua_State* L, entityx::EntityManager& es, const std::string& type){

using namespace luabridge;

entityx::Entity e = es.create();

auto v = luah::getTableKeys(L, type);

LuaRef entityTable = getGlobal(L, type.c_str());

and great tutorial by the way :D

Hey

You need to include first and then include Lua headers.

That’s because LuaBridge creators decided that putting Lua headers into namespace luabridge was a good idea…