---
title: Using Lua with C++(Part 2.5)
url: https://eliasdaler.wordpress.com/2013/11/17/lua_and_cpp_pt2_5/
published: '2013-11-17'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Part 2.5. Template getArray function and other modifications**

This is part 2.5 of my Lua tutorial. Why 2.5 and not 3? Well, because this tutorial doesn’t introduce any new concepts. I’ll point out some bug fixes I made and what improvements can be done. It won’t be too big.


## Getting an array

I wrote template version of the function implemented in the 2nd part.

template<typename T> std::vector<T> getArray(const std::string& name) { std::vector<T> v; if(!lua_gettostack(name.c_str())) { printError(name, "Array not found"); clean(); return std::vector<T>(); } lua_pushnil(L); while(lua_next(L, -2)) { v.push_back((T)lua_tonumber(L, -1)); lua_pop(L, 1); } clean(); return v; }

Note: this code is working only with numbers. To get string array you have to write template specialization like this:

template<> inline std::vector<std::string> getArray(const std::string& name) { std::vector<std::string> v; if(!lua_gettostack(name.c_str())) { printError(name, "Array not found"); clean(); return std::vector<std::string>(); } lua_pushnil(L); while(lua_next(L, -2)) { v.push_back(std::string(lua_tostring(L, -1)); lua_pop(L, 1); } clean(); return v; }

The code is almost the same, but note that it uses** lua_tostring**, not **lua_tonumber** as in template version.

This code is not 100% safe and can fail if your array contains both numbers and strings. To prevent this you can add additional check:

// for template version while(lua_next(L, -2)) { if(lua_isnumber(L, -1)) { v.push_back((T)lua_tonumber(L, -1)); } lua_pop(L, 1); }

// for std::string specialization while(lua_next(L, -2)) { if(lua_isstring(L, -1)) { v.push_back(std::string(lua_tostring(L, -1)); } lua_pop(L, 1); }

**Improvements**

Some people noted that using only one Lua state is enough. This way you can make Lua state a static variable. But you have to be careful, because you have to be sure that you’ll open and close files when it’s needed, so you don’t try to read variables from files where they’re not defined.

It’ll look like this:

- Open file1
- Load data
- Close file1
- Open file2
- Load data
- Close file2

That way you don’t have to create new Lua state for every script file. You can load files with** luaL_dofile(L, filename)** and close them with** lua_close(L)**

And that’s all for today. Part 3 is unfortunately delayed, because I still don’t use Lua code to modify C++ objects so I don’t really know what works well and what doesn’t.

P. S. I still didn’t recieve enough feedback about the first and the second tutorials. If you want to add something, please, write me. **eliasdaler@yandex.ru**

P. P. S. Simple “thanks” if you find my tutorials useful will do too! ;D

thank you! it enhance my horizon of lua !