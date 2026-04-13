---
title: Using Lua with C++ in Practice. Getting data from scripts and why globals are
  evil.
url: https://eliasdaler.wordpress.com/2016/01/07/using-lua-with-c-in-practice-part4/
published: '2016-01-07'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Part 1**. Intro to ECS and basic principles**Part 2**. Implementing the basicsControlling entities in Lua by calling C++ functions[Part 3.](https://eliasdaler.wordpress.com/2015/11/12/using-lua-with-cpp-in-practice-part-3/)[Iterating over Lua tables.](https://eliasdaler.wordpress.com/2016/02/16/using-lua-with-c-iterating-over-lua-tables/)

This part doesn’t depend on the others, so you can read it even if you haven’t read previous parts. (I suggest to check them out, though. You may find some interesting stuff!)

This part will mostly use Lua C API only. LuaBridge is used for a small part to show some cool stuff. (Though you’ll be able to follow with most other bindings)

This part contains one of the most important practices in Lua programming which I discovered pretty recently and felt dumb afterwards because for the last two years I’ve been doing stuff wrong.

Today I’m going to talk about storing Lua tables and variables in scripts.

Storing data in Lua is great. You can easily store stuff in neat way and you can also store functions which you can later call from C++. You can store tables (or other variables) in scripts in two ways: as **global** variables and as **local** variables. Let’s talk about each one.


#### Bad way (global tables)

One way to get data from Lua is to store a global table in a script file like this:

-- window.lua window = { width = 640, height = 480, title = "Test window" }

Let’s see how we can get values from this table. Let’s create functions which can get us values from table by a key (assuming that when we call them the table is on the top of the stack).

int getIntField(lua_State* L, const char* key) { lua_pushstring(L, key); lua_gettable(L, -2); // get table[key] int result = (int)lua_tonumber(L, -1); lua_pop(L, 1); // remove number from stack return result; } std::string getStringField(lua_State* L, const char* key) { lua_pushstring(L, key); lua_gettable(L, -2); // get table[key] std::string result = lua_tostring(L, -1); lua_pop(L, 1); // remove string from stack return result; }

These functions are pretty simple. First, you push a key name to the stack. Then you call **lua_gettable** to get value of the key (it could be another table or just a simple variable). Now that you have the needed value on the stack, you can convert it to **int** or **const char*** by calling **lua_tonumber** or **lua_tostring** respectively.

Here’s a complete example of a program which gets data from the script and prints it.

#include <iostream> #include <string> extern "C" { # include "lua.h" # include "lauxlib.h" # include "lualib.h" } int getIntField(lua_State* L, const char* key); std::string getStringField(lua_State* L, const char* key); // see implementations above int main() { lua_State* L = luaL_newstate(); luaL_loadfile(L, "window.lua"); lua_pcall(L, 0, 0, 0); lua_getglobal(L, "window"); int width = getIntField(L, "width"); int height = getIntField(L, "height"); std::string title = getStringField(L, "title"); std::cout << "Width = " << width << std::endl; std::cout << "Height = " << height << std::endl; std::cout << "Title = " << title << std::endl; lua_close(L); }

This works, but this approach has several problems…

**Name collisions**. Suppose you load another script file and it contains a global table (or a variable) named “**window**“. Now the**window**table from**window.lua**in**lua_State**gets overwritten after you load the script! This behavior is rarely wanted and may lead to some problems. If you have lots of script files and several people working on the project, it’s hard to make sure that all tables have unique names.**Scoping**. Once you load a file with global variables in it, you can easily change their values from everywhere which is bad practice most of the time.**Variable lifetime**. Once you load the**window**table, it’s going to occupy some memory until you set it to**nil**and call garbage collector. So, you have to manually check if your program needs some variables in**lua_State**or not and manage their lifetimes, so that the**lua_State**doesn’t get big after loading lots of script files.

And, after all, do you really have to keep variables used to get data from scripts for a long time? Most likely you’ll just use them to create some stuff / set some C++ variables and then you won’t need them anymore. There’s no need for such Lua variables to be**global**, they should be**local**.

#### Awesome way (local tables)

So, here’s a better version of **window.lua**:

-- window.lua local window = { width = 640, height = 480, title = "Test window" } return window

Some changes are needed in C++ code. Now you have to do this:

lua_pcall(L, 0, 1, 0); // lua_getglobal(L, "window") <- don't need this line anymore

Notice that the third argument of **lua_pcall** has now value of 1. This argument is a number of returned variables you expect to get from a chunk of code you call. After this **lua_pcall** the window table gets placed on the stack.

You can also have a script file which returns 2 tables:

-- some_file.lua local table1 = { ... } local table2 = { ... } return table1, table2

You can get these tables on the stack like this:

// C++ lua_loadfile(L, "some_file.lua"); lua_pcall(L, 0, 2, 0);

But you can do even better by calling **lua_pcall** like this:

lua_pcall(L, 0, LUA_MULTRET, 0); // LUA_MULTRET = -1

Or you can just call **lua_dofile** which calls both **lua_dofile** and** lua_pcall(L, 0, LUA_MULTRET, 0)** for you!

And now you get all returned variables to the stack. You can know how many tables you got by doing this (assuming that the stack was empty before **lua_pcall** call):

int numberOfTables = lua_gettop(L);

Let’s go back to **window.lua** example. The **window** table is on the stack and now you can use it to get data from it just as you did in the first example after calling **lua_getglobal(L, “window”)**

But now the **window** table is **local**. Once you clean the stack with **lua_settop(L, 0)** the **window** table is gone forever from **lua_State** and this is exactly what we need!

Another cool thing we can use is LuaBridge’s **LuaRef** to control table’s lifetime (many bindings contain similar objects for referencing Lua variables).

Here’s how you can do it after calling **lua_pcall**:

// create LuaRef of item at the top of the stack auto windowRef = luabridge::LuaRef::fromStack(L, -1); // Now we can get values from table like this: int width = windowRef["width"].cast<int>(); int height = windowRef["height"].cast<int>(); int title = windowRef["title"].cast<std::string>();

What happens after we call **lua_setttop(L, 0)** and clean the stack? The **window** table isn’t removed! You can still access it by **windowRef** which is useful if you want to make window lifetime a little longer (for example, if you want to do some other stuff with stack and still be able to use **window** table)

This is possible because **luabridge::LuaRef** acts just as references in Lua do. Once you remove the **LuaRef**, reference count decreases by one and when it becomes zero then the table will be removed by garbage collector. (you can call it directly from C++ or Lua)

#### Outro

And that’s all for now. Next time I’ll talk about entity descriptions in Lua scripts and controlling their lifetime. (And maybe I’ll write some stuff about combining Lua and JSON).

Thanks for reading, I hope you’ve enjoyed the article. As always, I’ll love to hear your feedback in comments or you can [write me an email](mailto:eliasdaler@yandex.ru).

You can also subscribe to [my twitter](https://twitter.com/eliasdaler) to get updates about new articles.

See ya!

Hello Elias, I’ve just finished reading your articles.

Your run-time Lua-scripting-based approach is very interesting and definitely useful for games that require run-time composability. The implementation, however, is definitely not good. (It will work perfectly fine for any kind of small game/application, though.)

Here’s a list of problems/possible improvements:

* You should look into an existing C++11/14 Lua wrapper library. There are many good ones that greatly simplify binding.

* There is a lot of run-time dispatching, with mixed approaches. You use `dynamic_cast`, `typeid`, and `std::strings` to achieve it. You should look into a cleaner and more efficient solution. If most of your component types are known at compile-time, you should be able to assign an unique ID to every type (at compile-time), reducing the required amount of run-time dispatch techniques. Look into efficient polymorphic storage – a good place to start is: http://bannalia.blogspot.it/2014/05/fast-polymorphic-collections.html

* Excessive use of `std::cout` and `std::endl`. Find a way to separate error handling from logging, and use `\n` when you don’t need to flush the stdout buffer.

* You’re returning `std::string` by value in many `const` member functions. You could avoid this copy by returning by `const&`.

* (!!!) You’re using raw `new` and `delete`. This is a big no in modern C++11/14 code. Look into smart pointers.

* When implementing your factories, don’t use `if-else` chains. Use an hash table instead.

* Look into “perfect forwarding”, so that you can write efficient setter member functions (for strings, as an example).

* Use variadic templates and perfect forwarding to replace unnecessary run-time polymorphism:

`e->addComponent(std::type_index(typeid(GraphicsComponent)), gc);`

…could become…

`e->addComponent(…)`.

If you really require the run-time dispatch even in C++ game/application code, you should provide a similar template-based overload anyway, since there may be occasions where a new entity’s component types are known at compile-time.

If you want more details on anything, I will be happy to clarify your doubts!

Hi! Nice to see you reading my blog, I’ve watched you tutorials on ECS and they’re pretty cool! :D

Thanks for you awesome feedback!

Here’s my opinions about some some parts of it.

There aren’t many. I’ve checked out sol and Selene and they lacked lots of stuff I really need to have. I’ve never yet seen library which was as powerful as LuaBridge and was header only. Maybe I’m missing something?

The use of std::string is unavoidable here, because I need to convert from string key in Lua to C++ type. As for compile time ID, I agree. I’ll think about how I can implement this. Later I can have a map which helps me get this ID by a string.

The article you linked is pretty interesting but is only useful if I had virtual functions in my components. But I don’t have any. I don’t want to put update() function in Component, because I want all of the logic to remain in systems.

dynamic_cast is only used when I need to get component from entity, but most of the time it’s not used, because systems have arrays of pointers to concrete components so dynamic_cast is not used there. I’ll write about all this stuff in the future.

Completely agreed, I’ll fix that later.

Agreed, I just wasn’t very experienced with unique_ptr at the time I wrote the article and MSVC 2013 had some problems with it (problems with default move ctors/operator=). But now I’m using them all around, so I’ll rewrite the code to be better, yeah.

Of course, this was done just to simplify stuff, because using hash table would be a bit harder, maybe I’ll have an article about implementing Factories and then I’ll change the code in the if/else part of the tutorial. :)

I’ve never run into problems when that one extra copy mattered. If the object which is passed is huge, I agree (and when you pass rvalue references often). But most of the time you pass lvalue references, so this doesn’t matter at all.

I also dislike the way setters look with perfect forwarding, because they have to be templated and so it’s kinda hard to tell which type it expects you to pass in this function.

Can you provide an example of that, please?

Regarding Lua libraries: I used “luawrapper” with success for my projects, you can find it here:

https://github.com/ahupowerdns/luawrapper

I’ve found many promising popular Lua wrappers by searching for ‘lua “c++11″‘ and ‘lua “c++14″‘ on GitHub. I think that pretty much all of them allow you to bind functions, classes and variables without explicitly dealing with the Lua stack.

—

Using perfect-forwarding allows you to correctly handle lvalues, copy-only and move-only types. It is not only a possible performance improvement, but it’s also more correct in terms of semantics.

—

I made the example you requested in a gist:

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.

Learn more about bidirectional Unicode characters

example_lua_ecs.cpp

hosted with ❤ by GitHub

There are some problems with newer Lua bindings. Most of them lack the functionality I need for my game. For example, this wrapper you linked doesn’t seem to handle Lua references which are used very often in my game to quickly access functions and hold local variables. And it’s the same with other bindings. They look good at first, but then you find out that they lack some feature that you need. LuaBridge has everything that I need. And if it doesn’t have some things, it’s very easy to write them yourself.

___

99% of the time I use lvalues which are not copy-only (ints, floats, strings, etc.), so it doesn’t really matter if I write forwarding setter or not.

___

Hmm, there’s no link to a gist

I wasn’t aware of the limitations of those wrappers, now your choice does make sense. Have you thought about contributing those features to one of the existing wrappers?

Whoops, here’s the Gist link: https://gist.github.com/SuperV1234/3d9bbc9dd0d04ca23721

Yeah, I’ve thought about that, but I don’t have much time at the moment, so maybe I’ll try to contribute later. :)

___

As for the gist… this won’t work for a later implementation which loads a list of components from Lua, so there’s no way to get a type from string, like “GraphicsComponent”, AFAIK.

Hi, great article. I always look forward to your posts. I am wondering how you would read a nested table from the local table version? I am hesitant to use LuaBridge as I cant tell if it still supported.

Say you had color = { 255,255,255,255 }, inside the window table and you wanted to get those values returned as a vector or something?

I am also curious about the same with a multi dimensional table like say: stuff = { foo{1,2,3}, chi ={3,4,5} }

Thanks! :D

You do this just as you did with other variables. Suppose, you have window table on stack. First, you push “color” string. Then you call lua_getfield and now you have color table at top of the stack and you can get values from it just like with the window table.

It becomes easier with LuaBridge:

auto window = luabridge::LuaRef::fromStack(L, -1);

luabridge::LuaRef colorRef = window["color"];

int r = colorRef[1].cast<int>();

…

“I am hesitant to use LuaBridge as I cant tell if it still supported.”

Yeah, that’s a problem, but so far I haven’t found a binding library which had all the stuff I need. LuaBridge is simple enough to modify yourself, but I rarely encounter any bugs or find that I need some functionality which it doesn’t provide.

Thank you. I will give LuaBridge a shot.

Hello Elias :D!

First off, great articles, I’ve read all of them. Secondly, I was curious about some of the details of your LuaScriptManager and LuaRefWrapper. I was trying to implement something similar, but I couldn’t find out how you would use LuaBridge without including the header. Does LuaScriptManager use only Lua, no LuaBridge? If so why do you need the wrapper? Thanks again!

Hello! Thank you. :)

That’s a topic of my next tutorial which will come out this month. :D

Just some hints: LuaRefWrapper has unique_ptr, so you don’t have to include LuaBridge.h. LuaScriptManager uses only LuaRefWrapper instead of LuaRefs. This comes with price, though – you can only use LuaRefWrapper with a limited number of types which is okay in most cases.

More about it will be in the next part of tutorial. Now I’m even more determined to finish it sooner. :D

You wrote lua_setttop instead of lua_settop (you typed not needed “t”)

Sorry.

Thank you for finding the typo. I’ll fix it a bit later. :)