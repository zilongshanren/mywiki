---
title: Coding structures that cause bugs
url: http://joostdevblog.blogspot.com/2014/03/coding-structures-that-cause-bugs.html
author: Joost van Dongen
published: '2014-03-16'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

One of those is better coding structure. Ideally code is structured in such a way that mistakes and oversights are not possible, and that the code is easy to understand. In practice these goals are often not fully achievable, for example because they contradict with the amount of time you have to build it, or the performance requirements, or maybe the problem you are solving is just too complex for easy code. Nevertheless, striving for good structure does make a big difference. Today I would like to give a couple of examples of common coding practices in C++ that can easily cause bugs. Even if you want to keep using them, knowing the pitfalls can help avoid issues.

You might disagree with the examples given here, but I hope they at least help you think about how you structure your code and why. In the end there is no absolute answer to what good code is, but I do believe that to be a good programmer, one needs to think about what good code structure is, and which features of a language to use and which to avoid.


*Initialise()*functionsSome classes have a separate

*initialise()*function. This means that after having constructed the class, you need to first call the

*initialise()*function before you use it for anything. This is often done because constructors don't have return values (and can thus not return errors in the normal way), or because classes cross-reference each other and they both have to exist before either can be fully initialised.

However, using

*initialise()*functions introduces a new situation that is prone to bugs: it is now possible to have an instance of a class that is not initialised and thus not ready for usage. All kinds of bugs might happen if you forget to call

*initialise()*and then start using the class. This can be fixed by keeping a

*bool isInitialised*in the class and checking for that before usage, but that of course introduces another thing that needs to be remembered and is thus ready to be overlooked by a future programmer working on that class, causing even more bugs.

For this reason it is generally wise to avoid separate

*initialise()*functions altogether. Just create everything in the constructor. This principle is called

[RAII](http://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization)("Resource Acquisition Is Initialisation"). If you want to do error checking in the constructor, you can solve the problem of not having a return value by using

*try/catch*.

**Default parameters**

Default parameters are parameters in functions that have a default value, so that you can skip them if you don't need something special. Like for example:

void eatFruit(string fruitType = "banana"); //Can leave out the fruitType when calling this function eatFruit(); eatFruit("kiwi"); |

Default parameters are a useful tool: some functions are often called with the same parameters so it is nice to be able to just skip them in those cases. However, default parameters can also be dangerous because it is easy to forget about them, especially when refactoring. In the development version of

[Awesomenauts](http://www.awesomenauts.com)I recently created a crash bug while refactoring a piece of code. Here is what I changed:

//Old code TemporaryAnimation(ParticleFadeManager* particleFadeManager, RumbleManager* rumbleManager, unsigned int textLocalizationIndex, RenderGroup renderGroup = RG_STANDARD); //New code after refactoring, with one new parameter TemporaryAnimation(ParticleFadeManager* particleFadeManager, RumbleManager* rumbleManager, ReplayFrameStorer* replayFrameStorer, unsigned int textLocalizationIndex, RenderGroup renderGroup = RG_STANDARD); |

I use the compiler a lot while refactoring, so when I change something like adding a function parameter I often just hit compile to see where it is used. In this case however this was a bad choice because the default parameter caused the compiler to interpret my code in a different but still compilable way. Here is the line that caused the crash:

animation = new TemporaryAnimation(particleFadeManager, globalRumbleManager, 0, RG_MENU); |

Originally the '

*0*' was the

*textLocalizationIndex*, but after refactoring it was interpreted as a

*NULL*pointer for the

*replayFrameStorer*. The compiler didn't complain because

*RenderGroup*is an enum and can thus be interpreted as an

*unsigned int*. So

*RG_MENU*was now interpreted as the

*textLocalizationIndex*and the

*renderGroup*now used the default parameter

*RG_STANDARD*. Really broken code, no compiler error.

Had I not used default parameters here, the compiler would have given an error because I was passing in one parameter too few.

This is just one example of a situation where default parameters have given me such headaches: I have encountered several other situations where I overlooked things because of default parameters.

Also, I prefer if someone who calls a function actually thinks about what he is passing to it, and default parameters don't encourage thinking: they encourage ignoring. So despite their usefulness, I generally try to avoid default parameters.

**Constructor overloading**

When a class has several constructors, this is called

*constructor overloading*. In university I was taught this is a useful tool for all kinds of things, but in practice it turns out it is often a headache. It creates situations where it is easy to overlook something and introduce new bugs. Let's have a look at an example of this:

class Kiwi { private: string colour; const float softness; const float tastiness; public: Kiwi(const string& colour_): colour(colour_), softness(1), tastiness(1) {} Kiwi(float softness_): colour("green"), softness(softness_), tastiness(1) {} }; |

The problem here is that I need to initialise everything in every constructor. The

*tastiness*variable is always set to 1, but I have to set it in each function. This means code duplication. Code duplication can be avoided by using a common function that all constructors call, but this is not always possible. In this specific case for example the

*tastiness*variable is

*const*and can thus only be initialised in the initialiser list, not in a separate function.

Even worse worse than code duplication is that if I add a new variable to the class, I need to remember to initialise it in every constructor. Forgetting about one of the constructors has caused bugs in our code in several situations, so we now try to avoid constructor overloading altogether.

**Conclusion**

These three examples show how certain structures cause bugs. None of these structures are bad per se and they each have their use, despite the risks. In fact, I use these occasionally myself, simply because sometimes the alternatives are worse. However, knowing the risks of certain structures helps make good decisions on when to use them and when not to use them, and to first consider alternatives whenever you think you need them. It is important as a programmer to think about the pros and cons of anything you do, and to always look for better structure.

The initialise function can sometimes be useful if you deal with resources that should not be allocated in host/device memory at the time of construction. It is also useful in case the copy constructor is allowed and you want to pass a reference to the resource instead of allocating it from the constructor.



ReplyDeleteThere are actually more reasons to use an initialise or 'realise' function. It just depends on the situation whether it is useful to use it or not.

Sometimes when I look at code it feels we are too often copying behaviors from each other and think too little about what we are actually doing. An example, is error management. Everyone does it, but is it actually useful? I have seen many programs that provide error handling but if errors actually occur they go into a ghost state.

Error management is only useful if the error being encapsulated is actually sometimes expected and can be dealt with in such a way that the program does not have to stop. A simple example is a resource that fails to load. The program may continue without it.

The default parameter could have been anticipated if you would have used the 'explicit' keyword in conjunction with constructors. It might be a good behavior to use the explicit keyword if you expect implicit compiler conversions such as 'char/short' to int or enum to int. Personally i never use it though. Apart from that, you have to consider the amount of extra time needed to master these skills against the time it will take to find and fix a bug. Is it worth it? Is reading all these books and theories (which take a lot of time) about how one should program worth the time versus (rarely) occurring bugs?

The problem with Constructor overloading in C++ is, is that it is generally considered good practice to initialise member variables before the constructor body. In C# this is not possible. Therefore, an internal function in the class can be written (eg. initialise) that covers all the variables with default parameters. This function is then called from the overloading contructors with or without certain variables and so no duplication of code or accidentally wrongly initialise default paramaters can be made.

"Is reading all these books and theories (which take a lot of time) about how one should program worth the time versus (rarely) occurring bugs?"

DeleteYES! YES IT IS! Enormous amounts of time in game development are spent on bug fixing. This is easily 25% of all time spent on game development on big projects. Also, depending on code structure, adding new things can be quick and easy or a lot of work. Anything that can reduce those is very quickly worth the time.

25%? Then you should really consider moving to C# + .Net :-) It speeds up coding by 1000%? And errors are much less easily made. At least, that is my experience so far.



DeleteUltimately this is a step that all game programmers must take at some point anyway i believe. Hardware gets faster and faster and the actual game code covers a smaller part of the game's performance rapidly. Due to the increasing complexity of hardware and the expectations of the game industry, you will rely more and more on 3rd party libraries as it is unreasonable to write everything inside a company. At least, that is what I expect to happen.

It is good practice to write those 3rd party libraries in C++ as they may not be susceptible to change much. However, game code is.

Furthermore, due to the increasing complexity of C++ (C++11) it is hard for hardware designers to write compilers that produce native computer code as writing a compiler becomes very complicated. It must be hell to write C++11 template correct compiler. Instead, C# compiles to intermediate language which is much easier to port to native instructions.

In the long run you are probably right, but right now there is no proper C# on most consoles, and I don't know any available engines that are fit for a 2D multiplayer game as complex as Awesomenauts.


DeleteAs for C# fixing bugs: it only fixes low level bugs. Most bugs I encounter are due to complex/unexpected gameplay situations and C# won't help much there.

Actually Bart, the general 'feeling' inside the industry (and amongst C++ developers - although clearly they provide a biased view!) is that as Moore's law declines in effect, low-level languages like C++ become ever more important to get the performance gains everyone wants. And don't forget about other platforms like phones and tablets, on which the performance gap between garbage-collected languages and something like C++ is clear.



DeleteC++11 does add some complexity to an already-complex language, but we don't need to worry ourselves about how difficult it is to write a compiler for - the leading compiler vendors are already offering partial C++11 support (or even complete, in the case of clang).

Joost is right; C# avoids a class of bugs, but doesn't improve things by as much as you'd imagine. Once your codebase gets beyond a certain size and maturity, bugs tend to become more about logic errors than getting caught out by language oddities/failures. I'd estimate that more than 90% of bugs I've fixed have been caused by logic errors rather than C++ coding mistakes.

Wow, someone from Rare replying on my blog, nice! :D



DeleteInteresting points! I'm surprised that you say you expect C++ to become even more important in the future, since the quality that can be achieved with higher level tools and engine is rising quickly. I recently played the beta for The Last Tinkerer and I was surprised that a game with such cool graphics is actually made in Unity. Those tools are definitely getting closer to what is needed for high quality games.

Would you say the point of C++ becoming more important is mostly about AAA and less about smaller scale games?

In Visual Studio, in the refactoring menu, there is a tool to edit the header of a function, and at the same time modify all the calls to that same function. I'm pretty sure that your development enviornment should have something similar

ReplyDeleteRAII == "Resource Acquisition Is Initialisation". Subtle difference :)



ReplyDeleteDefault parameters: I Completely agree; I've been caught out by this many times. Sadly there are some conversions that are completely legal and for which compilers don't emit warnings, which makes them difficult to detect. The explicit keyword Bart mentions is only helpful for constructors taking one argument, or conversion operators, it can't be applied to function arguments. I now avoid default parameters like the plague, and am very careful with overloading functions (which sometimes does the same thing) - usually I prefer to name functions differently if they take a different set of arguments.

Constructor overloading: C++11 delegating constructors should fix the code duplication and make this nice again.

Luckily these are fixed or at least helped by C++11 (delegating constructors, strongly-typed enums etc.).

ReplyDeleteOne additional important note about constructors vs initialization methods in C++ is that within a base class's constructor `this` has not yet been set up as an instance of your subclass. What this means is that virtual methods overridden by your subclass will not call into your subclasses' definition! IE:









ReplyDeleteclass Baseclass

{

Baseclass() { color = getCustomColor(); }

virtual Color getCustomColor() { ... }

};

class Subclass : public Base

{

virtual Color getCustomColor() { ... } // will not get called by Base::Base()

};

The C++ FAQ has more on why C++ chooses to do this.

http://www.parashift.com/c%2B%2B-faq-lite/calling-virtuals-from-ctors.html

One workaround that I had employed in an entire framework was using static instancing methods instead of new. We all knew never to use new and put the onus on the class creator to create an overriding instancing method like this:

static Subclass *Subclass::create(...)

{

Subclass *result = new Subclass();

result->initialize(...);

return result;

}

Of course this meant that the onus was on the class creator to make sure he/she created the method like that! It obviously was not automatic and therefore a source of breakdown. Additionally if we used multiple initialize overloads (vs constructor overloads), which we did at times, building a parallel static create for each init was a pain and more source for error.

However one great result was an enforcement of smart pointer usage. Rather than returning a raw pointer as in the example above the framework used static creates to automatically give you a shared_ptr:

static shared_ptr Subclass::create(...)

{

shared_ptr result (new Subclass() );

result->initialize(...);

return result;

}