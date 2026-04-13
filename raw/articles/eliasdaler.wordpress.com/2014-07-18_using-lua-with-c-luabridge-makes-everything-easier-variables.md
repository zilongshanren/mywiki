---
title: Using Lua with C++. LuaBridge makes everything easier. Variables and functions
url: https://eliasdaler.wordpress.com/2014/07/18/using-lua-with-cpp-luabridge/
published: '2014-07-18'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

# Why use Lua?

Using scripts with C++ is great. They provide lots of flexibility and free you from using those .txt files for your configuration files and also let you write complex functions. You can modify your scripts without recompiling. This is really important because you get distracted less often. Even a short compilation can break your concentration.

And you can even design your system that even those people who don’t know how to code can create new scripts or modify existing object behavior without modifying your source code! If you want to know more reasons of what makes Lua great read [the beginning of this article.](https://eliasdaler.wordpress.com/2013/10/11/lua_cpp_binder/)

I wrote about how you can develop your own binding library in previous chapters. But this library is very basic, it doesn’t have the power some other libraries have. It’s really hard to write your own binding because it usually involves lots of templates magic and meta-programming.

I’ve tested lots of libraries and found **LuaBridge** to be the most awesome. It has MIT license, doesn’t have any dependencies(like Boost which some libraries use) and it doesn’t require C++11. You don’t need to build it. Just drop LuaBridge folder in your project folder, include one header and you’re ready to go!


# Minimal project setup

Download LuaBridge from [the repository](http://github.com/vinniefalco/LuaBridge)

You also need to [download Lua](http://luabinaries.sourceforge.net/).

Add Lua **include/** directory and LuaBridge to include directories and link **lua52.lib** to your project.

Create** script.lua** with this code in it:

testString = "LuaBridge works!" number = 42

Add **main.cpp** to your project:

// main.cpp #include <LuaBridge.h> #include <iostream> extern "C" { # include "lua.h" # include "lauxlib.h" # include "lualib.h" } using namespace luabridge; int main() { lua_State* L = luaL_newstate(); luaL_dofile(L, "script.lua"); luaL_openlibs(L); lua_pcall(L, 0, 0, 0); LuaRef s = getGlobal(L, "testString"); LuaRef n = getGlobal(L, "number"); std::string luaString = s.cast<std::string>(); int answer = n.cast<int>(); std::cout << luaString << std::endl; std::cout << "And here's our number:" << answer << std::endl; }

Compile and run this program. You should see the following output

LuaBridge works! And here's our number:42

**Note**: if your program doesn’t compile and you get something like “*error C2065: ‘lua_State’ : undeclared identifier*” in **luahelpers.h**, you need to do the following

1) Add this to the beginning of LuaHelpers.h

extern "C" { # include "lua.h" # include "lauxlib.h" # include "lualib.h" }

2) Change 460th line of Stack.h from this

lua_pushstring (L, str.c_str(), str.size());

to this

lua_pushlstring (L, str.c_str(), str.size());


Okay, here’s how the code works.

#include <LuaBridge.h> #include <iostream> extern "C" { # include "lua.h" # include "lauxlib.h" # include "lualib.h" }

We include all important headers first. Nothing special here.

using namespace luabridge;

LuaBridge has its own namespace (you should probably put it only where you use luabridge, though)

lua_State* L = luaL_newstate();

We create** lua_State** with this line.

luaL_dofile(L, "script.lua");

This line opens our script.

You don’t need to create new **lua_State** each time you open new file. You can load scripts using just one state.

Then we load Lua’s libraries and call the script (you can find more explanation in the [first part](https://eliasdaler.wordpress.com/2013/10/11/lua_cpp_binder/)):

luaL_openlibs(L); lua_pcall(L, 0, 0, 0);

We can then create **LuaRef** object which can hold everything Lua variable can: **int**, **float**, **bool**, **string**, table, etc.

LuaRef s = getGlobal(L, "testString"); LuaRef n = getGlobal(L, "number");

Then we can convert **LuaRef** to C++ string like this:

std::string luaString = s.cast<std::string>(); int answer = n.cast<int>();

# Error checking

But some things can go wrong and you should handle errors gracefully. Let’s check some of the most important errors

## What if Lua script is not found?

if (luaL_loadfile(L, filename.c_str()) || lua_pcall(L, 0, 0, 0)) { ... // script is not loaded }

## What if variable is not found?

You can easily check if the variable you want to access is **nil** or not

if (s.isNil()) { std::cout << "Variable not found!" << std::endl; }

## Variable is not of the type we expect to get

If you want to be sure that the variable is **string**, for example, you can check this:

if(s.isString()) { luaString = s.cast<std::string>(); }

# Tables

Tables are not just arrays: they’re amazing structures that can hold every Lua type and even tables!

Let’s write this in **script.lua**

window = { title = "Window v.0.1", width = 400, height = 500 }

And this code in C++:

LuaRef t = getGlobal(L, "window"); LuaRef title = t["title"]; LuaRef w = t["width"]; LuaRef h = t["height"]; std::string titleString = title.cast<std::string>(); int width = w.cast<int>(); int height = h.cast<int>(); std::cout << titleString << std::endl; std::cout << "width = " << width << std::endl; std::cout << "height = " << height << std::endl;

You should see the following output:

Window v.0.1 width = 400 height = 500

As you can see we can access table elements using operator **[]**. We can even write shorter:

int width = t["width"].cast<int>();

You can also change table contents like this:

t["width"] = 300

It doesn’t change the script, but if you try to get this variable again it will have another value:

int width = t["width"].cast<int>(); // 400 t["width"] = 300 width = t["width"].cast<int>(); // 300

Suppose you have a table like this:

window = { title = "Window v.0.1", size = { w = 400, h = 500 } }

How can we get value of **window.size.w**?

Here’s how:

LuaRef t = getGlobal(L, "window"); LuaRef size = t["size"]; LuaRef w = size["w"]; int width = w.cast<int>();(This is the shortest way of doing it I’ve found. If someone knows how to do this better, shoot me an e-mail or write a comment, it will be very appreciated)

You can go to the first part of my tutorial and find my implementation more convenient for getting data from tables because you can do something like this:

int width = script->get<int>("window.size.w");

# Functions

Let’s write a simple function in C++

void printMessage(const std::string& s) { std::cout << s << std::endl; }

Write this in **script.lua**

printMessage("You can call C++ functions from Lua!")

Now we need to register the function in C++:

getGlobalNamespace(L). addFunction("printMessage", printMessage);

**Note**: You must do this before loading the script using luaL_dofile.

**Note**: C++ and Lua functions can have different names

You just registered **printMessage** function. If you want to register it in some namespace you can do something like this:

getGlobalNamespace(L). beginNamespace("game") .addFunction("printMessage", printMessage) .endNamespace();

You then need to call it from Lua like this:

game.printMessage("You can call C++ functions from Lua!")

Lua namespaces have nothing to do with C++ namespaces. They’re used for logical grouping and convenience mostly.

Let’s now call Lua function from C++

-- script.lua sumNumbers = function(a,b) printMessage("You can still call C++ functions from Lua functions!") return a + b end

// main.cpp LuaRef sumNumbers = getGlobal(L, "sumNumbers"); int result = sumNumbers(5, 4); std::cout << "Result:" << result << std::endl;

You should see the following output:

You can still call C++ functions from Lua functions! Result:9

Well, isn’t that cool? You don’t need to tell LuaBridge function arguments and what you expect to get returned.

There are some thing to consider, though.

**You can’t have more that 8 arguments for one function.**

If you pass more arguments than function expects, LuaBridge will silently ignore them

However, if something goes wrong LuaBridge will throw a **LuaException**. Be sure to catch and handle it!

Here’s the full code of the functions example:

-- script.lua printMessage("You can call C++ functions from Lua!") sumNumbers = function(a,b) printMessage("You can still call C++ functions from Lua functions!") return a + b end

// main.cpp #include <LuaBridge.h> #include <iostream> extern "C" { # include "lua.h" # include "lauxlib.h" # include "lualib.h" } using namespace luabridge; void printMessage(const std::string& s) { std::cout << s << std::endl; } int main() { lua_State* L = luaL_newstate(); luaL_openlibs(L); getGlobalNamespace(L).addFunction("printMessage", printMessage); luaL_dofile(L, "script.lua"); lua_pcall(L, 0, 0, 0); LuaRef sumNumbers = getGlobal(L, "sumNumbers"); int result = sumNumbers(5, 4); std::cout << "Result:" << result << std::endl; system("pause"); }

# What? There’s even more?

Yes. There are some neat things which I’ll cover in next part: classes, object creation, object lifetime… **That’s a lot of stuff!**

I also recommend you to check out my **re:Creation** dev logs which show how I use Lua scripts in the development. Lua makes my life as a gamedev much easier. Try it, maybe it will make yours easier too?

Follow me on twitter to get updates! [@EliasDaler](https://eliasdaler.wordpress.com/twitter.com/EliasDaler)

cam ơn bạn vì đã chia sẽ

You’re welcome :)

Very helpful, thank you.

This is great! :) exactly what I was looking for. Lua makes a lot of sense now! I can’t wait to implement this myself and read on!

Thanks!

I am having a problem with LuaBridge, though :/ lua seems to have installed correctly. I downloaded LuaBridge from the linked source and got LuaBridge-master. I moved the contents of the LuaBridge directory (details folder; Luabridge.h … ) into my xcode includes folder and added #include to my main.cpp.

Is this all I had to do? I’m getting annoying errors when I try to build your sample code.

“Undefined symbols for architecture i386: “_luaL_checkinteger”, referenced from: luabridge::Stack::get(luabridge::lua_State*, int) in main.o

Sorry, do you know what this means? I appreciate any help :)

This is really strange. I’ve never encountered such errors in my programming experince, ha-ha. You should try other compilers. E-mail me if you have problems with them

I ended up fixing this problem by changing a small setting, “Build Active Architecture Only”, to yes instead of no. (I am using XCode, if I did not mention this.) Apparently liblua.a is built as an archive and xcode ignores that type of library build when it searches for libraries to link; changing this setting allows xcode to see liblua.a and pick it up :) I think this is an xcode-specific problem. Am I able to ask you another question about your code? Ha ha I am getting a silly error.

Glad to hear you fixed it. And yeah, feel free to ask

Will you be continuing this tutorial? It’s extremely helpful! I’m looking forward to learning more about creating objects with components and behaviors, if you’re planning to cover it.

Yes, I will. :)

I’ll talk about C++ objects and classes in Lua. But I can’t really say when it’ll be done. Maybe two weeks. Maybe a month… :D

Exactly what i was searching for ! You don’t know how much you helped me ! Thanks a lot ! I still have a question though, is there a way to call a C++ function that takes an array or vector (or any type of container) from Lua ? Something like this :

—

answer = choice(“Would you like to …”, {“Yes”, “No”})

—

Because, after all a string is a sort of array, so is it possible ? If yes, how ?

Thanks a lot for your help !

You’re welcome! Nice to hear that. :)

Hmm, I don’t know how to do this, but I have some ideas. I’ll try it out and reply again later.

Here, it works. Be sure to add some error and type checking, of course.

http://pastebin.com/GmEZybb6

Awesome ! So this way it’s possible to bypass the 8 arguments limit ! Thanks a lot for your help ! :)

You’re welcome! Glad to help :)

I am using LuaBridge for a project of mine, https://github.com/pisto/spaghettimod

At first I was enthusiastic as you about LuaBridge, then after some plumbing and as my application grew mature, I see now that it has a lot of problems.

The C++ inteface to Lua makes all calls without wrapping in pcall. It doesn’t matter if you don’t call functions, even a table creation can trigger an error (if a garbage collection cycle happens to be issued and a __gc metamethod fails), killing instantly your application. I don’t need this interface so I just removed it, but be warned.

There are no clear semantics for references, and copy by value. It is debatable what the right approach would be to translate C++ semantics to Lua, as they are very different languages, but in in my opinion it should be arithmetic type and boolean => pass by value, rvalues (functions returning objects) => create userdata, anything else (references / pointers) => create references. There are several occasions where the vanilla LuaBridge fails: for example, functions that take references cause a copy of the object to be made (http://git.io/dBdbcQ), const references to arithmetic types won’t work (http://git.io/HBBiVg), fields of structs that are non arithmetic or pointers are passed by valued and copied (http://git.io/EqR41Q).

Every time a pointer of a reference is passed to Lua, a new proxy object is created, which is an unnecessary overhead. The wrapping object could be saved in the registry table with a weak reference, and reused when needed. It is not easy to implement this in a proper way (think what happens if you delete the object, then create a new object of the same type and maybe the malloc implementation returns the same piece of memory), but it would be a great performance gain.

And yeah, missing array access sucks big time. Had to implement it as you did (http://git.io/EZiUxw).

The way in which stuff is bound to Lua makes it very intense for the compiler, because of template instantiations. gcc takes almost 1GB of ram to compile my biggest compile unit (which is indeed quite a monster). gcc is to blame here partially, as clang performs much better, but It’s not clear to me whether there could be a way to arrange bindings in a more performing way. For sure getting rid of the boilerplate for different arity of functions with C++11 variadic templates (it’s almost 2015 now!) could simplify things and templates resolution. But you know, the library is not maintained anymore.

After all, it’s been a good time with you LuaBridge. The big pros are that it’s easy and you can actually (almost) understand the code, but probably now I need to switch to something more polished.

That’s some interesting things to know, thanks. Please, shoot me an e-mail if you find something better than LuaBridge. (eliasdaler@yandex.ru)

Me too please.

PD: great tutorial.

Thanks! :)

My lua works just fine, but when i include LuaBridge, i get 25 errors like:

error: variable or field ‘lua_rawsetp’ declared void inline void lua_rawsetp (lua_State* L, int idx, void const* p)

error: ‘lua_State’ was not declared in this scope

And so on.

Tried different versions of lua, still no result. What can be wrong with it?

Now everything works, just included bridge after lua :\

When I include , I get luabridge\detail\userdata.h(409): error C2061: syntax error : identifier ‘lua_newuserdata’

But then if I switch to release mode, it compiles fine.. o_O

Hi! It’s really hard to say what causes the problem without looking at your project, so the only thing I can advice is too look closely for differences between Debug and Release build options. :)

I am too getting this error. Not sure what the problem is.

Hmm… Do you use the master version of Luabridge from repository? Are you sure that you use correct Lua 5.2 for your compiler?

how can i properly setup LuaBridge in VisualStudio 2013?

Go to Project settings and add LuaBridge folder to your include directories. Then go to Linker->Input and add lua52.lib (get it here: http://sourceforge.net/projects/luabinaries/files/5.2/Windows%20Libraries/Dynamic/) to Additional Libraries.

Then change fix the line in luahelpers.h (described in the article) and you’re good to go.

Console output:

LuaBridge works!

And here’s our number:42

Thanks a lot !!

You’re welcome!

You can also replace:

lua_pushstring (L, str.c_str(), str.size());

with:

lua_pushstring (L, str.c_str());

by simply deleting the last argument.

From the LuaBridge 2.0 Reference Manual. I have myself not yet used LuaBridge, however what you are teaching leads to “undefined behavior”. Please Update.

http://a8u-tutorial-sources.googlecode.com/git-history/311fd6c18b5548db7d52f1e59eaf45c1a37b5533/Game/External/LuaBridge-2.0/Manual.html#s2.6

2.7 – lua_State

Sometimes it is convenient from within a bound function or member function to gain access to the `lua_State*` normally available to a `lua_CFunction`. With LuaBridge, all you need to do is add a `lua_State*` as the last parameter of your bound function:

void useState (lua_State* L);

getGlobalNamespace (L).addFunction (“useState”, &useState);

You can still include regular arguments while receiving the state:

void useStateAndArgs (int i, std::string s, lua_State* L);

getGlobalNamespace (L).addFunction (“useStateAndArgs”, &useStateAndArgs);

When the script calls useStateAndArgs, it passes only the integer and string parameters. LuaBridge takes care of inserting the lua_State* into the argument list for the corresponding C++ function. This will work correctly even for the state created by coroutines. Undefined behavior results if the lua_State* is not the last parameter.

AFAIK, this is what you need to do if you intend to use or reference lua_State in C++ function called from Lua. It’s fine to not do this when you don’t intend to change lua_State.

hi there, great blog really liking it. but i’v got a bit of a problem, after including lua and luaBridge, linking the lua library and writing the main() function; i’m getting #LNK “13 unresolved externals” errors, has this happened to you, any ideas?

Hello. Thank you!

Can you provide your source code and some error messages you’re getting? Are linking errors from Lua? Do you get them if you just simply create lua_State in main()?

Hi, what are the changes required to migrate to Lua 5.3.3? I need to support 64bit integers.

Thank you

To be fair, I didn’t work with Lua 5.3, so I can’t answer to that. :)

Very Helpful Tutorial Series, well explained and taking care of all the sensitive part

thanks for the tutorials, keep it up

You’re welcome! Check out sol2, though, it’s much superior binding! :D

What function is that “lua_pcall” calling in the first example? I’m guessing it’s one of the Lua-side return values from luaL_dofile?

lua_pcall executes stuff on stack. It’s unnecessary when doing dofile, because dofile = loadfile + pcall. I don’t remember why I added it. :D

Hello, when I try to addFunction I get error assert failed, namespace.h

Hi. Can you show me your code and which assert fails?

I’ve downloaded the lua binaries, but there is no lua52.lib, only a lua53.dll and three executables. Any ideas?

https://sourceforge.net/projects/luabinaries/files/

Download Lua from here

Thanks very much :)