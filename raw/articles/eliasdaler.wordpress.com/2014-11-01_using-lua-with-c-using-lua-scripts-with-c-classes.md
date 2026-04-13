---
title: Using Lua with C++. Using Lua scripts with C++ classes.
url: https://eliasdaler.wordpress.com/2014/11/01/using-lua-with-c-luabridge-part-2-using-scripts-for-object-behaviour/
published: '2014-11-01'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

*Read the first part about LuaBridge here to see how to install it and use it for basic things.*

You can find the complete source code of this article [here](https://github.com/EliasD/luabridge-classes)

![](../../assets/a19fafc981944b5b.png)


This part will show you how to register C++ classes in Lua, call member functions and how to apply scripts to something practical like putting object behaviour code in scripts.

I’m a game developer, so I’ve used examples related to gamedev but you can use Lua almost everywhere, so take a look even if you’re not interested in gamedev.

The code used in this article is as simple as possible while also remaining a complete example which you can run and compile.

I leave out the details which are irrelevant to focus on the main topic: scripts.


## The first approach

Suppose you want to make NPCs which react differently to the player interacting with them.

First of all, we have a Guard which just says “Hello” and a witch, who heals the player if his health is low.

![](../../assets/611367ebbb63fe93.png)


Let’s go with a naive implementation.

Here’s the **Player** class:

// Player.h #pragma once #include <string> class Player { public: Player(); int getHp() const { return hp; } void setHp(int hp); int getMaxHp() const { return maxHp; } void setMaxHp(int maxHp) { this->maxHp = maxHp; } private: int hp; int maxHp; }; // Player.cpp #include "Player.h" #include <iostream> Player::Player() { maxHp = 10; hp = maxHp; } void Player::setHp(int hp) { this->hp = hp; std::cout << "> Player: " << hp << " HP" << std::endl; }

**Character** base class:

// Character.h #pragma once #include <string> #include "Player.h" class Character { public: virtual ~Character() = default; virtual void interact(Player& player) = 0; std::string getName() const { return name; } void setName(const std::string& name) { this->name = name; } protected: std::string name; };

**interact** if a function which gets called each time player interacts with characters, for example, talks with them.

Let’s derive **Guard** and** Witch** classes from the** Character** class.

**Guard** class:

// Guard.h #include "Character.h" class Guard : public Character { public: void interact(Player& player) override; private: }; // Guard.cpp #include "Guard.h" #include <iostream> void Guard::interact(Player& player) { std::cout << name << ": Hello! Be safe!" << std::endl; }

**Witch** class:

// Witch.h #pragma once #include "Character.h" class Witch : public Character { public: void interact(Player& player) override; private: }; // Witch.cpp #include "Witch.h" #include <iostream> void Witch::interact(Player& player) { if (player->getHp() == player.getMaxHp()) { std::cout << name << ": Hi! Come back when you're wounded." << std::endl; } else { std::cout << name << ": Hi! Let me heal you." << std::endl; player.setHp(player.getMaxHp()); } }

And now we can use all these classes:

// main.cpp #include <iostream> #include "Guard.h" #include "Player.h" #include "Witch.h" int main() { Player player; Witch witch; witch.setName("Lucia"); Guard guard; guard.setName("Sam"); std::cout << "|Player walks around the town and talks with some npcs" << std::endl; witch.interact(player); guard.interact(player); std::cout << "|Player goes on a great adventure!" << std::endl; std::cout << "|but gets beaten up by some foes..." << std::endl; player.setHp(player.getHp() - 5); std::cout << "|Back to the town... Let's talk to the witch" << std::endl; witch.interact(&player); }

Here’s the output:

|Player walks around the town and talks with some npcs Lucina: Hi! Come back when you're wounded. Sam: Hello! Be safe! |Player goes on a great adventure! |but gets beaten up by some foes... > Player: 5 HP | Back to the town... Let's talk to the witch Lucina: Hi! Let me heal you. > Player: 10 HP

Cool, let’s now analyze how scripts can make this whole thing better.

Let’s look closer at **Guard** and **Witch** classes.

The only thing different about them is an **interact** function.

This will be the only difference between classes for the most friendly NPCs. Do we really need to make a new class for this?

We can use the [Strategy pattern](http://en.wikipedia.org/wiki/Strategy_pattern). But still, we have to create a new class for each new behaviour. And it’s all in the code. This is not very good especially if you’re working with someone who doesn’t know how to program. If another dev wants to change some NPC’s behaviour or add a new type of NPC, he has to ask the programmer to do it. This is not very productive.

And even if you’re a programmer, there are still nice things which scripting will give to you. One of the most important: you don’t have to recompile the code when you change something in scripts. You can even change object behaviour during runtime, reload the its script and continue playing the game. Isn’t it awesome?

Let’s get to the scripting!

## Scripting

![](../../assets/84d24a388871b7f2.png)


First of all, let’s get rid of **Witch** and **Guard** classes. We won’t need them anymore.

Let’s start by modifying **Character** class.

// Character.h #pragma once #include <memory> #include <string> #include <LuaBridge.h> class Player; class Character { public: Character(); void loadScript(luabridge::lua_State* L, const std::string& scriptFilename, const std::string& tableName); virtual ~Character() = default; void say(const std::string& text); std::string getName() const { return name; } void setName(const std::string& name) { this->name = name; } void interact(Player& player); protected: std::string name; std::unique_ptr<luabridge::LuaRef> interactFunc; };

What has changed? First of all, we have a **LuaRef** pointer named **interactFunc** which we’ll use to call a Lua **interact** function. It’s a pointer because **LuaRef** doesn’t have a default constructor so you have to allocate memory for **interactFunc** once you get if from the script.

I’ll assume that each NPC will have its own Lua table to make things as simple as possible.

What if you want to create multiple objects that use the same interact function? Loading the **interactFunc** over and over seems inefficient.

You can handle it this way: create some “template” characters from which you will copy the **interact** function. Use **shared_ptr** for **interactFunc** for reference counting to see how many objects use the particular interact function.

We also have **loadScript** function which will load character’s name and an **interact** function from the script.

Now let’s see how **Character**‘s methods are defined

Character::Character() : interactFunc(nullptr) { } void Character::loadScript(luabridge::lua_State* L, const std::string& scriptFilename, const std::string& tableName) { using namespace luabridge; if (luaL_dofile(L, scriptFilename.c_str()) == 0) { // script has opened LuaRef table = getGlobal(L, tableName.c_str()); if (table.isTable()) { if (table["name"].isString()) { name = table["name"].cast<std::string>(); } else { name = "Null"; } if (table["interact"].isFunction()) { interactFunc = std::make_unique<LuaRef>(table["interact"]); } } } else { std::cout << "Error, can't open script!" << std::endl; } }

It’s pretty self-explanatory if you’ve read the previous part of my tutorial.

Notice all the error checking. Make sure you do it all the time when you handle scripts. It’ll save you someday.

The **Character** table will look like this in a Lua script:

some_Character = { name = "some name" interact = function(player) -- put interaction code there end }

Here’s another function. Pretty simple:

void Character::say(const std::string& text) { std::cout << name << ": " << text << std::endl; }

And **interact** function looks like this.

void Character::interact(Player& player) { if (interactFunc) { try { (*interactFunc)(this, player); } catch (luabridge::LuaException const& e) { std::cout << "LuaException: " << e.what() << std::endl; } } }

We just call Lua interact function using pointers to **Character** and **Player**. There’s exception handling. You can make some mistakes in interact function but that wouldn’t crash your program and you’ll see where you made this mistakes. Very useful.

Here’s how **Player** class looks now:

// Player.h #pragma once #include <string> #include "Character.h" class Player : public Character { public: Player(); int getHp() const { return hp; } void setHp(int hp); int getMaxHp() const { return maxHp; } void setMaxHp(int maxHp) { this->maxHp = maxHp; } private: int hp; int maxHp; }; // Player.cpp #include "Player.h" #include <iostream> Player::Player() : maxHp(10) { hp = maxHp; } void Player::setHp(int hp) { this->hp = hp; std::cout << "> Player: " << hp << " HP" << std::endl; }

Not much have changed. But notice that **Player** class is now derived from **Character** class. We’ll see how we can register derived classes in a moment.

We can now register C++ classes using LuaBridge so Lua can handle them.

Here’s how it’s done.

lua_State* L = luaL_newstate(); luaL_openlibs(L); getGlobalNamespace(L) .beginClass<Character>("Character") .addConstructor<void(*)(void)>() .addProperty("name", &Character::getName, &Character::setName) .addFunction("say", &Character::say) .endClass() .deriveClass<player, character="">("Player") .addProperty("hp", &Player::getHp, &Player::setHp) .addProperty("maxHp", &Player::getMaxHp, &Player::setMaxHp) .endClass();

Let’s go line by line:

beginClass<Character>("Character")

You start registering class with this. Notice that class name in Lua may be different in C++. It’s convenient for them to be the same though.

addConstructor<void(*)(void)>()

Here’s how you add constructor. You have to specify its arguments using function pointer syntax. You can’t have overloaded constructors.

addProperty("name", &Character::getName, &Character::setName)

Lua can handle some member variables as properties. So you can write something like this in Lua:

characterName = character.name character.name = "Some guy"

Getters and setters will be called for each operation with a property.

If you want the property to be read only, just pass a getter to **addProperty** method without a setter.

Adding functions is simple too:

addFunction("say", &Character::say)

And we end class registration with this function.

endClass()

We can register derived classes like this:

deriveClass<Player, Character>("Player")

Virtual methods work normally. No special syntax needed.

Here are some notes from [LuaBridge manual](http://vinniefalco.com/LuaBridge/Manual.html):

The `deriveClass` takes two template arguments: the class to be registered, and its base class. Inherited methods do not have to be re-declared and will function normally in Lua. If a class has a base class that is

notregistered with Lua, there is no need to declare it as a subclass.

Here are some more important things to know:

- LuaBridge does not support overloaded functions
- Const methods are detected automatically. Const-correctness is enforced
- Destructor is registered automatically

It’s also important to know how objects are passed to Lua and which lifetime (C++ or Lua) they have. I’ll cover this in next article.

And now let’s write some scripts!

-- witch.lua witch = { name="Lucia", interact=function(witch, player) if(player.hp == player.maxHp) then witch:say("Hi! Come back when you're wounded.") else player.hp = player.maxHp witch:say("Hi! Let me heal you.") end end }

-- guard.lua guard = { name="Sam", interact=function(guard, player) guard:say("Hello! Be safe!") end }

Not too much to explain here. Notice that you call member functions with ‘**:**‘ like this:

witch:say(...)

And now the remaining part of **main.cpp**

Player player; player.setName("Player"); Character witch; witch.loadScript(L, "witch.lua", "witch"); Character guard; guard.loadScript(L, "guard.lua", "guard"); std::cout << "|Player walks around the town and talks with some npcs" << std::endl; witch.interact(player); guard.interact(player); std::cout << "|Player goes on a great adventure!" << std::endl; std::cout << "|but gets beaten up by some foes..." << std::endl; player.setHp(player.getHp() - 5); std::cout << "|Back to the town... Let's talk to the witch" << std::endl; witch.interact(player);

The output is the same as for previous C++ only version.

And there you have it. I hope you’ve seen how useful Lua scripts can be.

## What’s next?

But things don’t end here! Explore and try Lua yourself. Maybe you’ll find some more cool things!

In the next chapter I’ll cover object creation and their lifetime.

I also plan to write a chapter which will show how I use scripts in my game (I’ve written a lot about that in my dev logs, but I need to organize it a bit). I don’t have classes which I have to register because I use Entity/Component/System model so things are a bit different there.

See ya next time!

If you’ve noticed mistakes or just want to provide some feedback, feel free to send me an e-mail: **eliasdaler@yandex.ru**

Yeah ! Another awesome tutorial ! :)

Thanks a lot ! I’ll try to adapt this for the Entity Component System i use, i hope i’ll succeed !

Glad you liked it. You’re welcome!

Feel free to ask me anything about it if you have some questions.

When are you going to write the next part? I found these tutorials and they are fantastic(best ones I’ve found) but I really need to know about object creation and their lifetime! Thanks.

Thank a lot!

I’m planning to write it somewhere this month or next month maybe. This stuff takes lots of time so I can’t really promise a lot. :)

Thanks for replying! I appreciate it and take your time :)

No problem!

By the way, there’s an official LuaBridge manual which explains a lot about object lifetime, you can find it here: https://raw.githubusercontent.com/vinniefalco/LuaBridge/master/Manual.html

My tutorial will use it as reference but I’ll also try to show some practical examples and show what happens if you do some incorrect stuff (like changing value of const variable) and stuff like that. :)

Thanks for the great info! I’ll be glad to check it out.

Hey Elias, me again, sorry for bombarding you with questions, but I am trying to use the technique you used here with the interaction function but I’m trying to implement the collide function we previously discussed. From what I can tell this should work well, and the bounding box in the example gives me no trouble, however when I call my collide function I get an access violation runtime error (Meaning I am reading memory I shouldn’t be). Anyway here is my code:

http://pastebin.com/EfxbgUNF

anything not shown here is exactly the same as your code. Except for maybe some names. Let me know if you need anything else.

Hey, no problem, feel free to ask as many questions as you need.

So, did you check didCollide function after loading it? It shouldn’t be nullptr and it’s LuaRef shoudn’t have mRef == -1. And can you show me your script, please?

Thanks again, I appreciate the help.

If by checking didCollide you mean doing if (didCollide) { … } then yes. The only difference between my code and the code in this article is that I load the function in the constructor of my class, as shown by one of your other articles. Ghost script: http://pastebin.com/2e7k8gRC

Then here is the loading/calling of didCollide: http://pastebin.com/pe5atppX

Hmm, pretty strange, this should work. If mRef in didCollide LuaRef equals to -1 then it means that something goes wrong. It’s hard to know what.

And by the way, you shouldn’t pass pointers to the function, you should pass references, so you should write:

(*didCollide)(*ent1, *ent2);

(Sorry it took me so long to answer)

Hmm, okay thanks for the tip!

You’re welcome :)

i have got question. let’s say we programing RTS (…strategy) and we need difference interaction for player, ghost, guard, and even not character ( for example chest ) how to write that code? use field name?

Yes, you should have a field which specifies entity type. Maybe it’ll be string or some unique int identifier for each entity type.

there shouldn’t be “delete interactFunc;” in the Character destructor. It’s a shared_ptr so it cleans itself up automatically. You shouldn’t give Character a destructor at all, the default compiler-generated one is fine.

You’re right. That’s a thing I forgot to take out, because previously the code used raw pointers. I’ve even changed shared_ptr to unique_ptr as it’s better in this case.

“If you want the property to be read only, just pass a setter to addProperty method.” I guess you meant “getter” here?

Yep. Fixed!

i recomend printing lua errors like this = std::cout<<"ERROR "<<lua_tostring(L,-1)<<std::endl; gives more verbose about the problem.