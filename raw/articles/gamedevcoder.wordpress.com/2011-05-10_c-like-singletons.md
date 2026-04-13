---
title: C-like singletons
url: https://gamedevcoder.wordpress.com/2011/05/10/c-like-singletons/
published: '2011-05-10'
source_blog: Gamedev Coder Diary
source_site: https://gamedevcoder.wordpress.com
category: game programming
fetched: '2026-04-13'
---

It is my impression that template based singleton patterns for C++ like [this one](http://www.codeproject.com/KB/cpp/singleton_template.aspx) are very popular and widely used. Why? I believe it’s mostly because OOP design patterns in people’s minds often take precedence over code simplicity and prevent them from thinking even for a while of what approach is best as a whole.

Having read [this post](http://www.gamedev.net/topic/599398-depencenies/page__p__4808364) on gamedev.net yesterday I decided to quickly present my preferred way of implementing singletons in C/C++.

For a start let me say that I’m a big fan of simple and minimalistic coding style which when I’m coding in C++ often results in code that looks almost like pure C i.e. mostly just functions and C structures. This is funny by the way because if you asked me a couple of years ago I’d probably say something different. Well, people change and I did change too in that matter (largely thanks to great coworkers at [BlueTongue](http://bluetongue.com/)). Having experienced variety of approaches, from heavy object oriented designs to pure C-like data oriented designs, I now choose the latter whenever possible. It’s just a lot simpler and easier to maintain and it pays off when implementing large systems. And there’s added bonus that it’s often significantly more efficient approach, especially on consoles.

Now, back to main topic. Let’s assume we need some text localization manager. Here’s my way of doing it:

**LocalizationMgr.h:**


//! Starts up localization manager

void LocalizationMgr_Startup(const char* language = "EN");

//! Shuts down localization manager

void LocalizationMgr_Shutdown();

//! Loads translation set

bool LocalizationMgr_LoadTranslationSet(const char* setName);

//! Localizes ‘sourceText’ phrase; returns NULL on failure

const char* LocalizationMgr_Translate(const char* sourceText);



As you can see the header file only contains the very minimum interface. As a user of that system you don’t even get to see the internals of the manager – it’s all hidden in a source file as can be seen below.

**LocalizationMgr.cpp:**


struct LocalizationMgrData { bool m_isInitialized; char m_language[16]; LocalizationMgrData() : m_isInitialized(false) {} }; static LocalizationMgrData s_data; void LocalizationMgr_Startup(const char* language) { assert(!s_data.m_isInitialized); strcpy(s_data.m_language, language); s_data.m_isInitialized = true; } void LocalizationMgr_Shutdown() { assert(s_data.m_isInitialized);

// TODO: Unload all translation sets – irrelevant for this sample

s_data.m_isInitialized = false; } bool LocalizationMgr_LoadTranslationSet(const char* setName) { assert(s_data.m_isInitialized);

// TODO: Load translation set – irrelevant for this sample

} const char* LocalizationMgr_Translate(const char* sourceText) { assert(s_data.m_isInitialized);

// TODO: Return translation of the ‘sourceText’ phrase – irrelevant for this sample

}

As you can see the source file contains data structure of type `LocalizationMgrData`

declared as a static variable. This way it’s only visible from that single cpp. If it was to be visible from multiple source or header files, I’d simply put it into LocalizationMgr_Private.h. An important thing is that this data does not have to be parsed by the compiler when you #include LocalizationMgr.h – hence the compilation process is much faster. This really pays off when you design all of your game engine systems like that.

`[Update]`

As per [Arseny](http://zeuxcg.org/)‘s comment, it’s worth pointing out that there’s slightly safer approach to declaring your data than what’s presented above. By making your `s_data`

a pointer (i.e. `static LocalizationMgrData* s_data`

) you benefit in 2 ways:

(a) you avoid static initialization order problems

(b) your code will most likely just crash if you use a function while system isn’t initialized; that is especially useful in Release builds where asserts won’t hit but it’s also useful if you simply forget to put an assert

The downside to that is that you need to dynamically allocate / deallocate memory in your `Startup`

and `Shutdown`

functions but this is a must anyway if you’re dealing with more complex data. In my example I was only using primitive types (`char`

, `bool`

etc.) which is why it was “okay”.

Now, here’s summary of my approach:

Pros:

- Header file contains the very minimum code from the user’s point of view
- easy to read for a programmer
- fast to compile for a compiler

- Explicit rather than implicit singleton initialization (must call
`Startup`

/`Shutdown`

“manually”)

Cons:

- All singleton “attributes” must be accessed via
`s_data`

- Have to put
`assert(s_data.m_isInitialized)`

in each singleton function in order to make sure it’s initialized when used - No easy way to support singleton polymorphism (in my opinion not a problem in 99% cases)
- Code documentation generation tools like
[Doxygen](http://www.stack.nl/~dimitri/doxygen/)won’t be able to figure out that all functions with`LocalizationMgr_`

prefix belong to same logical module; my solution to that is to use[grouping](http://www.stack.nl/~dimitri/doxygen/grouping.html)feature using`/defgroup`

around my header file but this isn’t perfect obviously; now, I’m also a big fan of self-documenting code, so ideally one wouldn’t need the docs at all, just looking at the header file should be enough 🙂 - Similar problem as above with Intellisense; you won’t be able to type in “module” (e.g.
`LocalizationMgr`

) name’s prefix, press enter, and then start typing in remainder of the function name (e.g.`Translate`

)

`[Update]`

The 2 issues above can be solved in C++ by putting all of your functions into namespaces (e.g. namespace being `LocalizationMgr`

and function being `Translate`

) as suggested by Arseny in the comments.

As you can see there’s still some disadvantages to my approach but the (a) and (b) on the pros list are still more important to me than all of the cons. Which approach you choose is up to you, but before you make that decision ask yourself what your requirements are and which solution meets them best. For me, as with majority of programming related topics, [KISS principle](http://en.wikipedia.org/wiki/KISS_principle) is a major one!

– You can put all functions in a namespace LocalizationMgr; that way you get better Intellisense info, better Doxygen info, etc.

– You can make s_data a pointer; that way you avoid scary static initialization order problems, change the initialized check to s_data != NULL, and even if you forget to assert for this you’ll crash instead of making some code go crazy because of uninitialized data.

Hi Arseny,

Good points, thanks!

As for making s_data a pointer, that’s what I typically end up doing when initialization order matters or whenever the data contains any non-primitive C++ type. But I also agree it would be safer to do that always for the reason you brought up.