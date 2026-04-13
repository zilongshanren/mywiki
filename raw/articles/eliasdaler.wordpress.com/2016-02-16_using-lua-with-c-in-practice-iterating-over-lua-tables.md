---
title: Using Lua with C++ in Practice. Iterating over Lua tables
url: https://eliasdaler.wordpress.com/2016/02/16/using-lua-with-c-iterating-over-lua-tables/
published: '2016-02-16'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Hello, this is new part of Using Lua with C++!

This part will be short, but very helpful. It will use **LuaBridge** and **Lua C API**, but it’s pretty easy to rewrite stuff for other Lua/C++ bindings.

#### The problem

Suppose you have a Lua table this:

someTable = { 1, 5, 10, 20 }

Suppose that **someTableRef** is a **LuaRef** pointing

It’s pretty easy to iterate over it using LuaBridge:

for (int i = 0; someTableRef.length(); ++i) { // note the i + 1 here, it's because arrays in Lua start with 1 LuaRef elementRef = someTableRef[i + 1]; ... // do something with the element }

But what if you have a table like this:

someTable = { firstKey = "someString", anotherKey = { ... -- some stuff } }

and want to iterate over it?

This can be easily done in Lua:

for k, v in pairs(someTable) do ... -- do stuff with k end

But how do we do the same in C++? I’ve found no way to do it in **LuaBridge** (and seems like lots of other libraries don’t include this functionality as well), but fortunately we can use lua_next from **Lua C API** to do the thing for us!


#### Solution

So, here’s a complete code to the function which will return **unordered_map** where the key is a Lua table key and the value is Lua value which is associated with the key:

std::unordered_map<std::string, luabridge::LuaRef> getKeyValueMap(const luabridge::LuaRef& table) { using namespace luabridge; std::unordered_map<std::string, LuaRef> result; if (table.isNil()) { return result; } auto L = table.state(); push(L, table); // push table lua_pushnil(L); // push nil, so lua_next removes it from stack and puts (k, v) on stack while (lua_next(L, -2) != 0) { // -2, because we have table at -1 if (lua_isstring(L, -2)) { // only store stuff with string keys result.emplace(lua_tostring(L, -2), LuaRef::fromStack(L, -1)); } lua_pop(L, 1); // remove value, keep key for lua_next } lua_pop(L, 1); // pop table return result; }

This functions works because when you call **lua_next**, it pushes table’s key and corresponding value to the stack. We need key to remain to call **lua_next** and get next key/value, so we pop the value from stack and repeat the process for all remaining keys.

#### Details

This function will only process string keys, because that’s what you want to do most of the time. If you need to iterate over key which can be of any type, feel free to rewrite the function which will return **std::unordered_map**.

You also get **O(1)** access by string key, which is awesome and almost like Lua tables work (they use hashes and this let’s you get stuff by **O(1)**)

#### How to use this function

Here’s how you can iterate over the resulting **unordered_map**:

for(auto& pair : getKeyValueMap(someTableRef)) { auto& key = pair.first; auto& value = pair.second; ... // do some stuff }

One good thing about this is that lifetime of that map is the for loop only which we want most of the time.

Here’s a more practical example. I store entity definitions in my game like this:

someEntity = { GraphicsComponent = { ... }, CollisionComponent = { ... }, ... -- etc. }

So I can easily create iterate over this table using **getKeyValueMap** function:

for(auto& pair : getKeyValueMap(entityTableRef)) { auto& componentName = pair.first; auto& componentTable = pair.second; // Create component by string. componentTable is passed to Component's ctor // which loads all the stuff from it. Tutorial on Factories is coming soon // which will show a cool way to do this stuff auto component = createComponent(componentName, componentTable) ... // do other stuff }

#### Complete example and conclusion

And, at last here’s a complete example for you to test. [Here](http://pastebin.com/LSD3ZnLz).

You should get output like this:

Here's what table contains: someKey = 8 someAnotherKey = this is a string

And that’s it! I hope this function is useful for you (I use it a lot and find it really neat!)

The next part will be a lot more complex and will talk about wrapping Lua libraries in easy to use manager and dealing with awful dependencies which some libraries may cause.

See ya!

Here are some other parts of Using Lua with C++:

This is already doable with LuaBridge::Iterator

ie

LuaRef toBeIterated;

if (!toBeIterated.isNil()) {

Iterator iterate(toBeIterated);

while (!iterate.isNil()) {

LuaRef curObj = iterate.value();

…

++iterate;

}

}

your solution is also interesting though. Just make sure your tables within “toBeIterated” are uniquely named or you’ll bail out of the while, lol I banged my head against that for way too long

Thanks, didn’t know about it!

As for unique names inside the table – do you mean all tables should have unique keys inside the table you iterate over? Isn’t it obvious, because one value would overwrite another on Lua side?

Well this is amusing – came across this while looking for ‘lua_next’ info, and see you are using LuaRef. I wrote LuaRef originally and gave it to the LuaBridge guy. :-D – merlinblack / Nigel Atkinson

Ha-ha, that’s great! :D

I’m not using LuaBridge now, though. I use sol2 which is just a perfect binding library. :)