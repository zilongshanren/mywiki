---
title: Using Lua with C++ (Part 1)
url: https://eliasdaler.wordpress.com/2013/10/11/lua_cpp_binder/
published: '2013-10-11'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

You can view full source code of this article [here](https://github.com/EliasD/unnamed_lua_binder)

*This is ***VERY** outdated, please refer to this version as the latest and up-to-date guide:

**VERY**outdated, please refer to this version as the latest and up-to-date guide:

##### If you want to see Lua in real world practice, check out [Using Lua with C++ in practice series](https://eliasdaler.wordpress.com/2015/08/10/using-lua-and-cpp-in-practice/).

**Part 1. Why Lua is great and why you should use it. Writing simple wrapper/binding and using Lua for configuration files****Part 2**. Getting arrays and calling Lua functions from C++**Part 2.5**. Template getArray function and other modifications**Part 3**. Calling C++ functions and creating C++ objects

## So, why use LUA?

![](../../assets/1aaac17c1c10f37d.gif)


I’ve seen game devs using different data formats. Some of them use[ JSON](http://www.json.org/), some use

**some use plain**

[XML](http://www.w3.org/XML/),**.txt**files etc.. As for me, I use

**Lua**for data, because:

- It is easy to use without any additional libraries(well, except of lua libraries, of course…)
- You can use different formulas in your files, for example:
**some_variable = math.sqrt(2) * 2** - It’s extremely lightweight and fast
- It’s under
[MIT license](http://www.lua.org/license.html), so you can use it in any way you want. Just download it and use it - It’s ported almost everywhere, because it’s written in C and compiles with almost any C compiler
- You can use tables to categorize your data which is easy to edit and read

Let’s look at example Lua file:

player = { pos = { X = 20, Y = 30, }, filename = "res/images/player.png", HP = 20, -- you can also have comments }With a little class(implementation is below) you can get data in this way:

LuaScript script("player.lua"); std::string filename = script.get("player.filename"); int posX = script.get("player.pos.X");

Pretty neat.## Bindings

You can find lots of bindings

[here.]

But I wanted to write my own, so here it is.

Note: my code is not perfect, but it works. I appreciate your suggestions on how I can improve my code. E-mail me if you find some errors or just to say thanks: eliasdaler@yandex.ru



Recommended reading to know how Lua stack works and view simple examples to know what’s going on:

[http://www.lua.org/pil/24.html]## Implementation

So, let’s start with a simple class

#ifndef LUASCRIPT_H #define LUASCRIPT_H #include &lt;string&gt; #include &lt;vector&gt; #include &lt;iostream&gt; // Lua is written in C, so compiler needs to know how to link its libraries extern "C" { # include "lua.h" # include "lauxlib.h" # include "lualib.h" } class LuaScript { public: LuaScript(const std::string&amp; filename); ~LuaScript(); void printError(const std::string&amp; variableName, const std::string&amp; reason); template&lt;typename T&gt; T get(const std::string&amp; variableName) { // will be implemented later in tutorial } bool lua_gettostack(const std::string&amp; variableName) { // will be explained later too } // Generic get template&lt;typename T&gt; T lua_get(const std::string&amp; variableName) { return 0; } // Generic default get template&lt;typename T&gt; T lua_getdefault(const std::string&amp; variableName) { return 0; } private: lua_State* L; }; #endif

Constuctor:LuaScript::LuaScript(const std::string&amp; filename) { L = luaL_newstate(); if (luaL_loadfile(L, filename.c_str()) || lua_pcall(L, 0, 0, 0)) { std::cout&lt;&lt;"Error: script not loaded ("&lt;&lt;filename&lt;&lt;")"&lt;&lt;std::endl; L = 0; } }Nothing special here. We create new Lua state and check if everything is okay.


Destructor:LuaScript::~LuaScript() { if(L) lua_close(L); }

printErrormethod is simple. It prints which variable was not loaded and why.void LuaScript::printError(const std::string&amp; variableName, const std::string&amp; reason) { std::cout&lt;&lt;"Error: can't get ["&lt;&lt;variableName&lt;&lt;"]. "&lt;&lt;reason&lt;&lt;std::endl; }lua_getdefault() is used when you need to return some null value for a variable. For numbers it will be okay to return 0, but for std::string we have to return “null”, for example. (You can add another cases for different types)


That’s why we add template specialization.(it goes in LuaScript.h)template&lt;&gt; inline std::string LuaScript::lua_getdefault() { return "null"; }Now we’ll implement template

getfunction(this will all go inLuaScript.hfile)The algorigthm for

lua_gettostackis simple . Suppose you have a variable you want to get, for example namedplayer.pos.X.

playertable is global, so you need to get it vialua_getglobalmethod. Nowplayertable will be on the top of your stack and you will uselua_getfieldfunction to getpostable and then variablex. We uselevelvariable to know which level we’re currently on and how many items are currently in stack

template&lt;typename T&gt; T get(const std::string&amp; variableName) { if(!L) { printError(variableName, "Script is not loaded"); return lua_getdefault&lt;T&gt;(); } T result; if(lua_gettostack(variableName)) { // variable succesfully on top of stack result = lua_get&lt;T&gt;(variableName); } else { result = lua_getdefault&lt;T&gt;(); } lua_pop(L, level + 1); // pop all existing elements from stack return result; } bool lua_gettostack(const std::string&amp; variableName) { level = 0; std::string var = ""; for(unsigned int i = 0; i &lt; variableName.size(); i++) { if(variableName.at(i) == '.') { if(level == 0) { lua_getglobal(L, var.c_str()); } else { lua_getfield(L, -1, var.c_str()); } if(lua_isnil(L, -1)) { printError(variableName, var + " is not defined"); return false; } else { var = ""; level++; } } else { var += variableName.at(i); } } if(level == 0) { lua_getglobal(L, var.c_str()); } else { lua_getfield(L, -1, var.c_str()); } if(lua_isnil(L, -1)) { printError(variableName, var + " is not defined"); return false; } return true; }And now for the template specializations(put them in

LuaScript.h):template &lt;&gt; inline bool LuaScript::lua_get(const std::string&amp; variableName) { return (bool)lua_toboolean(L, -1); } template &lt;&gt; inline float LuaScript::lua_get(const std::string&amp; variableName) { if(!lua_isnumber(L, -1)) { printError(variableName, "Not a number"); } return (float)lua_tonumber(L, -1); } template &lt;&gt; inline int LuaScript::lua_get(const std::string&amp; variableName) { if(!lua_isnumber(L, -1)) { printError(variableName, "Not a number"); } return (int)lua_tonumber(L, -1); } template &lt;&gt; inline std::string LuaScript::lua_get(const std::string&amp; variableName) { std::string s = "null"; if(lua_isstring(L, -1)) { s = std::string(lua_tostring(L, -1)); } else { printError(variableName, "Not a string"); } return s; }That’s all! You can find complete source code with a little example here:

[https://github.com/EliasD/unnamed_lua_binder]

(Note: you have to create Makefile or project yourself, don’t forget to add lua include/lib dirs to your project)## What to do next?

There are still lots of things you can do with Lua.


One useful feature is getting arrays of elements.-- somefile.lua some_array = { 1, 2, 3, 4, 5, 6}// getIntVector will be implemented in part 2 std::vector v = script.getIntVector("some_array")Another useful thing is getting list of table keys and calling Lua functions from C++. Part 2 will cover those two features.

[And here it is.]You can also call Lua functions from C++. And C++ functions from Lua. This will probably be in Part 3.

[And here it is in its full glory]Follow me on twitter

[@EliasDaler]if you don’t want to miss it.

Is this no longer working? Keep getting http://pastebin.com/P3jVqTLK on build

fixed

Hi, very good job! Is there a way to get the table keys of a table that is inside an other table? E.g. here: get the table keys of “pos”?

Hi. Thanks!

I’ve updated the “getKeys” code here: https://eliasdaler.wordpress.com/2013/10/20/lua_and_cpp_pt2/

AFAIK it should work for nested tables too.

Thanks for the quick response! I tried it and got following error:

–

TEMP:[string “function getKeys(name) s = “”for k, v in pa…”]:1: bad argument #1 to ‘pairs’ (table expected, got nil)

Error: can’t get [rules.[string “function getKeys(name) s = “”for k]. rules is not defined

Error: can’t get [rules. v in pa…”]:1: bad argument #1 to ‘pairs’ (table expected]. rules is not defined

–

I called the function as following:

std::vector keys = script.getTableKeys(“player.pos”);

What about this one? http://pastebin.com/ePkQaQtn

Oh yes, that did it! Thank you very much! Great job

Awesome! You’re welcome!

Thank you, awesome tutorial series!

You’re welcome! Thank you too :D

Hey Elias, I totally forgot that you were working on these tutorials. When I googled for “Lua c++” you were on the first place. I’ll dig into it right now, thanks! :)

Ha-ha, you’re welcome! :D

There is an bug with the formatting. Rather than having the “Greater than” and “Less than” signs displayed, “&>” is displayed for the “Greater than” sign and “&<” is displayed for the “Less than” sign. It is fine on the source code on GitHub so it isn’t an issue on my end. I have seen a few website like this recently. Not all websites though. Just a few of them. Anyhow, you should check out that freaky bug…

Oh yeah, that’s one of the reasons I made a new blog on github pages. :D

Is this particular tutorial on your github blog?

No, but I fixed problems with “” here.

just a heads up, looks like wordpress mangled your code a bit. There are “&” where “&” should be.

Thanks, fixed. That was one of the reasons I’ve created a new blog. xD

yeah it’s super annoying. I complained to wordpress devs about this stuff. I think they have since fixed some bugs in encoding, but it still has problem.

These days I usually write my blog posts in a gist and copy/paste the generated HTML into WordPress, or write the post in a plain .txt file in OneDrive. Basically, I avoid WordPress’ actual editor.