---
title: Using Lua with C++(Part 2)
url: https://eliasdaler.wordpress.com/2013/10/20/lua_and_cpp_pt2/
published: '2013-10-20'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Part 2**. Getting arrays and calling Lua functions from C++

And you can view source code here: [https://github.com/EliasD/unnamed_lua_binder](https://github.com/EliasD/unnamed_lua_binder)


# Cleaning Lua stack

Here’s how you can clean Lua stack.

We can use **lua_gettop** function which returns number of elements in the array to know how many of items we have to pop.

void clean() { int n = lua_gettop(L); lua_pop(L, n); }

Simple and useful.

## Using arrays

You can define an array in Lua like this:

array = {1,2,4,5,6,7,8}

Well, there are actually no arrays in lua. “Array” is still a table, but that doesn’t really matter for now.

And here’s how you can get its contents in C++

std::vector LuaScript::getIntVector(const std::string& name) { std::vector<int> v; lua_getglobal(L, name.c_str()); if(lua_isnil(L, -1)) { return std::vector(); } lua_pushnil(L); while(lua_next(L, -2)) { v.push_back((int)lua_tonumber(L, -1)); lua_pop(L, 1); } clean(); return v; }

Here’s how it works.

At first we get global table and check if it is found or not. If it’s nil(not yet defined or, well…, nil) we just return an empty vector.

Then we push nil value to the top of the Lua stack. That’s because of what [lua_next](http://www.lua.org/manual/5.2/manual.html#lua_next) does

It pops a key from the stack and they pushes key-value pair to the stack. If there are no more elements in the array we clean the stack and return resulting vector.

You can also make a function for getting arrays of strings or floats. All you need to change is vector type and a few casts(if you want to make version for strings, don’t forget to change **lua_tonumber** to **lua_tostring**)

# Using Lua code in C++

Writing some parts of you code in Lua is *awesome*. Imagine that you have some big project which compiles for minutes/hours. And now you need to change something in it. And now you have to rebuild your project.

You’re lucky if your code is not used through your whole project so you don’t have to rebuild everything. But what if it is actually used quite a lot? Working on that code becomes **unbearable**. But Lua can change that.

I don’t recommend to use Lua for code where performance is critical(especially in your game loops! No way. But it’s okay for load or save state!)

When performance doesn’t matter it’s quite cool, because you can also use [lots of awesome Lua modules](http://luarocks.org/repositories/rocks/) to simplify your code.

Let’s start with a basic example.

Suppose you have this Lua function in **sum.lua** file:

function sum(x, y) return x + y end

Here’s how you can run this function from C++:

int sum(int x, int y) { lua_State* L = luaL_newstate(); if (luaL_loadfile(L, "sum.lua") || lua_pcall(L, 0, 0, 0)) { std::cout<<"Error: failed to load sum.lua"<<std::endl; return 0; } lua_getglobal(L, "sum"); lua_pushnumber(L, x); lua_pushnumber(L, y); std::cout<<"loaded"<<std::endl; lua_pcall(L, 2, 1, 0); int result = (int)lua_tonumber(L, -1); lua_pop(L, 1); return result; }

First, we create new Lua state and load a file.

Note: this is just an example, you should keep state with a loaded file somewhere to keep it from getting reloaded every time you use a function, because that’s not efficient.

Then we get global function named **sum** on the top of Lua stack. Using **lua_pushnumber** function we then push 2 variables and now our stack looks like this:

![Untitled Diagram](../../assets/839c1419f03b4388.png)


After that we call [lua_pcall](http://www.lua.org/manual/5.1/manual.html#lua_pcall). A little about its arguments. First one is **lua_State**, the second is the number of arguments in function you’re about to call. Third is the you expect function to return. Fourth is error code(you should probably read about that in Lua reference manual)

After we call a function, it’s popped off the stack with its arguments. The only thing left in the stack is the value **sum** function returns, so now we can get its value with** lua_tonumber** and pop it.

You can also call Lua code stored in C++** std::string**. Here’s how it’s done.

luaL_loadstring(L, code.c_str()); // where code is std::string with Lua code in it lua_pcall(0, 0, 0, 0);

And now you can do everything the same way you did with files.

# Getting keys of Lua table.

Getting all keys from table may be very useful. Suppose you have some table called animations structured like this:

animations = { walk = { ... some values there }, idle = { ... and some there } }

If you know all the keys of a given table it’s very easy to get data they store, but what if you don’t know how many of them is in the file and how they are named?

Using the function implemented above you can easily get std::vector containing all the table keys.(I don’t think that’s the most efficient way to do this, but it works, if someone knows how to do it better, please contact me, I’ll add your version to this tutorial!)

Here’s how you can get a string with table keys with comma delimiter in Lua:

function getKeys(name) s = "" for k, v in pairs(_G[name]) do " s = s..k.."," end " return s end

There’s **_G** table in Lua which lets you to get a table or variable by its name, so calling **_G[name]** gets us a table we want to get keys from.

[pairs](http://www.lua.org/manual/5.2/manual.html#pdf-pairs) is a function which lets us to iterate over the table in easy way. It returns “key-value” pair, so k is table key in that context

Calling this function for animations table will return this string: **“walk,idle,”**

And here’s a code for C++ function:

**NOTE: to use pairs function don’t forget to add luaL_openlibs(L); in LuaScript constructor!**

std::vector<std::string> LuaScript::getTableKeys(const std::string& name) { std::string code = "function getKeys(name) " "s = \"\"" "for k, v in pairs(_G[name]) do " " s = s..k..\",\" " " end " "return s " "end"; // function for getting table keys luaL_loadstring(L, code.c_str()); // execute code lua_pcall(L,0,0,0); lua_getglobal(L, "getKeys"); // get function lua_pushstring(L, name.c_str()); lua_pcall(L, 1 , 1, 0); // execute function

Now we’ve got the string on the top of the stack. The only thing left is getting it from the stack and tokenizing it. Here’s a simple way to do this:

std::string test = lua_tostring(L, -1); std::vector<std::string> strings; std::string temp = ""; std::cout<<"TEMP:"<<test<<std::endl; for(unsigned int i = 0; i < test.size(); i++) { if(test.at(i) != ',') { temp += test.at(i); } else { strings.push_back(temp); temp= ""; } } clean(); return strings; }

That’s all! I’ll probably write part 3 of the tutorial which will show how to call C++ functions from Lua.

You can send me your questions and suggestions here(your feedback is appreciated. Even a simple “thanks” will make my day better :D): **eliasdaler@yandex.ru**

And don’t forget to follow me on Twitter if you don’t want to miss it! [@EliasDaler](https://twitter.com/EliasDaler)

I’m subscribing. keep up the good work.

Will do, thanks.

great article! thank you

You’re welcome! Thanks to you too :)

just an FYI, I read all the docs and #defines, the whole lua_pop(L, lua_gettop(L)) is the same as lua_settop(L, 0) because removing all items in the stack is the same as setting the stack size to 0. The lua_pop is just syntax sugar for lua_settop with a negative index.