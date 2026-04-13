---
title: Using Lua with C++(Part 3)
url: https://eliasdaler.wordpress.com/2013/11/30/lua_and_cpp_pt3/
published: '2013-11-30'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Part 3. Calling C++ functions and creating C++ objects**

I am very excited to write about this topic because it shows how great Lua is. While Lua is great for configuration files (as I’ve shown in my previous tutorials) it’s even greater when you use it to call C++ functions and you can even create C++ objects classes and modify them with Lua (I’ll cover this in part 4)

Let’s begin.

*Note: if you don’t know about how Lua stack works, I recommend you to read this chapter of great “ Programming in Lua” book* :

[http://www.lua.org/pil/24.2.html](http://www.lua.org/pil/24.2.html)


# Calling C++ functions

# First simple function

Let’s implement a simple **write** function which will just print a string. Here it is:

void write(const char* str) { std::cout<<str<<std::endl; }

Now we have to create a special function Lua will register. “**Programming in Lua**” says:

Any function registered with Lua must have this same prototype, defined as

lua_CFunctioninlua.h:

typedef int (*lua_CFunction) (lua_State *L);

So, you have to pass** lua_State*** as the argument and return a number of variables your function returns. Yes, you can return multiple values!

Here’s how our l_write binding function looks:

static int l_write(lua_State* L) { const char* str = lua_tostring(L, 1); // get function argument write(str); // calling C++ function with this argument... return 0; // nothing to return! }

And now let’s register it in Lua. In **main** write:

lua_State* L = luaL_newstate(); luaL_openlibs(L); // load default Lua libs if (luaL_loadfile(L, "test.lua")) { std::cout<<"Error loading script"<<std::endl; } lua_pushcfunction(L, l_write); lua_setglobal(L, "write"); // this is how function will be named in Lua lua_pcall(L, 0, 0, 0); // run script

In **test.lua** write:

write("Hello, world!") write("The square root of 2 is "..math.sqrt(2)) x = 42 write("We can use variables too, x = "..x)

You should see the following output:

Hello, worldThe square root of 2 is 1.4142135623731We can use variables too, x = 42

Hey, that worked! Now let’s move on to another example.

Let’s write a function which sums two integers. (Yeah, it is pretty boring thing to do, but still it is very useful example)

int sum(int x, int y) { return x + y; } static int l_sum(lua_State* L) { int x = lua_tonumber(L, 1); int y = lua_tonumber(L, 2); // get function arguments lua_pushnumber(L, sum(x, y)); // push the result of a call return 1; // we're returning one result }

We register it as usual:

lua_pushcfunction(L, l_sum); lua_setglobal(L, "sum");

In **test.lua**:

x = sum(2, 8) write("Result = "..x)

Output:

Result = 10

Great. And now to a more practical example.

# How to use it in game development

Suppose you want to implement NPCs in your game. When the player comes near NPC and presses “activate” button NPCs do different things.

Healer heals player and says “Let me help you” and another NPC just says “Hello” and does nothing else. Your interaction code may look like this:

if(isPressed(ACTIVATION_BUTTON)) { Character* character = find_nearby_character(player); if(character) { character->interact(player); } }

But how do you implement character **interact** method?

Well the most obvious solution is to have **enum** with different types of characters:

enum CharacterType { Player, Talker, Healer }; CharacterType type;

And then write something like this:

void Character::interact(Character* secondCharacter) { switch(type) { case Character::Player: break; case Character::Talker: say("Hello"); break; case Character::Healer: say("Let me help you"); heal(secondCharacter); break; } }

But that’s probably a bad solution, because all behavior is hard-coded and as you create more types of characters it becomes harder to maintain this code.

Another solution is to make** interact** virtual function and use inheritance. But you’ll end up with classes for each type of NPC, which is really bad.

Or you may use [Strategy pattern](http://en.wikipedia.org/wiki/Strategy_pattern) which is better, but still, behavior is coded in C++ and you have to recompile your code to make even slight changes in character behavior. Not cool.

And that’s where Lua helps.

# Creating C++ objects and calling member functions

Let’s create a very simple **Character** class:

class Character { public: Character(const char* name, int hp); void say(const char* text); void heal(Character* character); const char* getName() { return name; } int getHealth() { return health; } void setHealth(int hp) { health = hp; } // will be implemented later void interact(Character* character); private: const char* name; int health; }; Character::Character(const char* name, int hp) { this->name = name; health = hp; } void Character::say(const char* text) { std::cout << name << ":" << text << std::endl; } void Character::heal(Character* character) { character->setHealth(100); }

And we encounter a problem there. How can we pass **Character*** as a parameter if Lua doesn’t now about this type? How can we register non-static member functions in Lua and call them? That’s where I’ve decided to use a good Lua wrapper. There are lots of them [there](http://lua-users.org/wiki/BindingCodeToLua).

I’ve decided to use [LuaWrapper](https://bitbucket.org/alexames/luawrapper/src) which has no additional dependencies and doesn’t need to be built. You just copy one header file to your project and you’re ready to go.

## LuaWrapper usage

Let’s write some of the functions(**interact** and **heal** will be trickier, so I’ll implement them later).

Here’s how constructor looks. Unfortunately, you can’t have different constructors:

Character* Character_new(lua_State* L) { const char* name = luaL_checkstring(L, 1); int hp = luaL_checknumber(L, 2); return new Character(name, hp); }

This type of function is required by LuaWrapper because it needs to know how to create new objects. Let’s implement another functions. Note, that they return **int** not **static int**

int Character_getName(lua_State* L) { Character* character = luaW_check<Character>(L, 1); lua_pushstring(L, character->getName()); return 1; } int Character_getHealth(lua_State* L) { Character* character = luaW_check<Character>(L, 1); lua_pushnumber(L, character->getHealth()); return 1; } int Character_setHealth(lua_State* L) { Character* character = luaW_check<Character>(L, 1); int hp = luaL_checknumber(L, 2); character->setHealth(hp); return 0; }

I’ll use **checknumber** instead of **tonumber** from now on. It’s basically the same but it will throw error message if something goes wrong.

LuaWrapper provides same method and you can get C++ objects with it. You can create objects and call their methods like this:

**player = Character.new(“Hero”, 100)**

**player:getHealth()**

Using **luaW_check(L, 1)** you can get **player** object and use it as usual in C++.

Let’s write the remaining code:

static luaL_Reg Character_table[] = { { NULL, NULL } }; static luaL_Reg Character_metatable[] = { { "getName", Character_getName }, { "getHealth", Character_getHealth }, { "setHealth", Character_setHealth }, { NULL, NULL } }; static int luaopen_Character(lua_State* L) { luaW_register<Character>(L, "Character", Character_table, Character_metatable, Character_new); return 1; }

**Character_table** is used for static functions. We don’t have them in **Character** class so this struct is empty.

**Character_metatable** is used for setting function names which you will use in Lua.

**luaopen_Character** registers a class. The first argument is **lua_State***, the second is how your class will be named in Lua scripts. Other arguments are static table, metatable and constructor function.

Write this in **main**:

luaopen_Character(L);

**Important**: you need to call this **before** calling **luaL_loadfile** because Lua doesn’t know about your class and it may think your code is incorrect.

Write this in **test.lua**:

player = Character.new("Hero", 100) player:setHealth(80) hp = player:getHealth() name = player:getName() print("Character name: "..name..". HP = "..hp)

Here’s what you should have in **main.cpp** so far: [http://pastebin.com/PbMTaM0g](http://pastebin.com/PbMTaM0g)

Output:

Character name: Hero. HP = 80

Awesome!

We still have **say**, **heal** and **interact** functions left to implement. I will do this in next part. See ya!


Follow me on twitter: **@EliasDaler**

Your feedback is welcome: **eliasdaler@yandex.ru**

Or you can just say “thanks” if you liked this article. I strongly appreciate that.

Absolutely great job! Thank you!

Thanks a lot!

Check out LuaBind, it’s a much nicer integration of Lua into C++.

It’s cool, but it seems like it’s been abandoned for some time and it also requires boost, which is a huge minus for me.

Hi, is there any hope left for the fourth part?

Hi. Well, I don’t think so, unfortunately. I’ve started using LuaBridge and like it more that LuaWrapper so I think next parts will be using LuaBridge

how would i add pre existing c++ objects into lua? also, how would i get all of the objects in lua to be used in c++?

You can make them global or pass them as parameters of the functions and use them there. Sorry, I don’t remember how to do this with LuaWrapper, you might want to check out the latest LuaBridge tutorial which shows how to do it.

Great Jop!!

Hey Elias,

I think you should replace (in your function l_write, line 3) the “write(str);” line by :

“std::cout << str << std::endl;" or "write(1, str, strlen(str));"

beside that, this is really helping me for my game ! sorry for my english and thanks from France !!

Fixed! Thanks :)

One question: Character_new returns a pointer to new Character, but I see no matching delete. Surely this means you need to create some kind of stack, maybe a vector or something, to deallocate whatever memory when you’re done, right?

Sorry, missed your comment. I wrote the article a long time ago and so I don’t think that I was doing allocation/deallocation in this case right. I recommend using some Lua/C++ binding to not care about such issues. sol2 is pretty awesome.

Hey Elias,

Before anything : Great work, this has been a huge help !

I wondered, if I had to call a c++ function that has to have a specific parameter from lua, how would I go about doing that, what I’m trying to do is call some sort of findActor(reference) with the reference being the reference to an existing ‘World’ full of objects.

Because the l_findActor function would have to be static in this case, the only way to get the reference to the findActor function would be via a second parameter, but lua_pushcfunction will not allow me to pass a function with more than the lua_State* argument.

Is there another way you know that would make it possible to use such a method ?

Thanks again

You’re welcome!

Check out the example here, it shows how to pass parameters to C functions: https://www.lua.org/pil/26.1.html

But I recommend to use sol2 for binding Lua and C++, it’s much easier and more convenient.

Thanks for this great tutorial.

I have one question, how do I access tables inside tables with no name.

for example :-

tileset = {

{

name = “tileset1”

},

{

name = “tileset2”,

data = {0, 1, 2, 3, 4, 5}

},

{

name = “tileset3”

someval = “tempval”

}

}

since tables inside tileset have no name how do access them ?

You access them by index, e.g. tilleset[1], tileset[2] and so on. In C API it’s done via lua_gettable