---
title: 'The Game Engine Dating Guide: How to Pick up an Engine for Single Developers'
url: http://www.learn-cocos2d.com/2012/05/the-game-engine-dating-guide-how-to-find-the-right-engine-for-your-game/
author: Pavel Says
published: '2012-05-03'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I frequently see questions like ![527560_435522206477238_205344452828349_1549369_31406319_n](../../../wordpress/wp-content/uploads/527560_435522206477238_205344452828349_1549369_31406319_n-300x242.jpg)


*Should I use game engine A or game engine B?*Sometimes the question is slightly more specific like

*Is game engine A right for this game?*

These questions are not unlike giving a list of features or requirements and then asking *Is potential partner A better for me than potential partner B?* And some are closer to asking the general public a very subjective question that requires intimate knowledge about the person who is asking: *With whom will I have better sex, A or B? *

Well … while there’s a checklist of features that A and B may or may not have that might have some influence on the decision, more often than not **your** choice depends a whole lot more on whether it *just feels right*.

You may feel attracted to A because A is so reasonable and the support is responsive and helpful, or you may simply find yourself attracted to how B is open to everything and free of charge. You may also find that despite A or B lacking a specific feature you crave, other aspects that you didn’t even think of more than make up for it. Features aren’t everything, more important is the spirit and ease of use.

Not uncommonly a fully featured game engine (or partner) with all bells and whistles may turn out to have a really steep learning curve, many restrictions, limitations, policies, quirks while “free” may cost you a lot more than you bargained for.

Following is my game engine dating advice that you can take to places like [MobileGameEngines.com](http://mobilegameengines.com/) to make your pick. These are the things that I consider the most important when choosing a game engine for small projects, and that is irregardless of the type of game I might want to develop.


#### Pick the game engine for you, not for your game

The number one mistake is to pick a game engine based on the requirements for a specific game you have in mind. Unless the game requires a specialized engine, this approach is wrong.

I can assure you that you can make almost anything work with any game engine, some merely make it somewhat easier to achieve the goal. Whether you can realize a specific type of game with a particular game engine is moot. And even if the game engine supports features that would help you develop the game, other factors are more important. You’ll read more about them in this article.

Moreover, the game you intend to develop initially will end up being scrapped anyhow. Realistically speaking. So you may be picking a game engine based on false assumptions. Once you picked the perfect engine for your game, you’re quite likely to stick to it due to the investement of time (and possibly money) thus far. Hence the advice to ignore the game you intend to develop, and focusing solely on whether you are likely to enjoy working with that game engine in general, and whether you can realize a number of games with that engine.

A game engine is a toolbox. It doesn’t do anything by itself unless you can handle the tools. It’ll be more important to enjoy working with the tools and being able to understand them well enough than how many or which kind of tools you have at your disposal. More often than not, limiting your toolset can be helpful to actually complete a project, if only because it’s easier to learn and master the tools. Being restricted can also bolster your creativity. If in doubt and given a choice, prefer the simpler, more barebones game engine and not those used by larger game development studios.

#### Apply the Marketing Filter

![](../../../wikipedia/commons/5/5b/95-98_Ford_Explorer.jpg)


When you’re trying to sort through game engines, you will be heavily influenced by marketing, peers and social networks. It’s very difficult, if not impossible, to filter that out. You might end up using the wrong engine because of promises that don’t hold true, or awesome and unique features that you end up not using at all.

To make a car analogy, consider how SUVs perfectly fit the needs of park rangers, farmers, smugglers and anyone who needs to drive safely over harsh road conditions with plenty of load - [yet who is really driving SUVs is soccer moms](http://www.time.com/time/specials/2007/article/0,28804,1658545_1658544,00.html).

Don’t be a soccer mom! Only consider what you really need, and ignore the promises and the non-essential feel-good features. Make a checklist and compare. But most importantly: do a test drive! Try for yourself. There is no substitution for that.

#### Performance is not a feature!

Few game engines neglect to mention how well they perform. Yet this is utterly irrelevant. I dare to say that 99% of all game engines are reasonably fast. As in: fast enough.

![](../../../diesel-engine-performance-part.jpg)


For a game engine that means that the code **you** write has a far greater impact on performance than the game engine itself. You can easily bring a super-duper fast game engine to its knees with a few lines of inconspicuous code. If you know what causes slow performance, you can squeeze a fair amount of awesomeness out of even a very unoptimized game engine.

At the end of the day, even the fastest game engine can’t fix your sloppy code. And often performance statements are very subjective. Be wary of sentences adorned with innumerable adjectives like “a lot more”, “much, MUCH faster”, “greatly improved performance” but not giving any concrete numbers. And even with the numbers know that game engine benchmark tests are very artificial, using setups you’ll not encounter in an actual game, and typically don’t compare each other.

Interestingly you’ll hardly find benchmarks comparing one game engine’s performance with that of another game engine. If you have no point of reference whatsoever, that renders all performance statements null and void.

#### Prefer a Programming Language you already know

I prefer game engines using a programming language that I’m familiar with. You should too.

However, be wary of solutions that make game engine A written in programming language X work with your favorite programming language Y. In my experience, those wrappers are quite often awkward to use, and may still require proficiency in X. Sometimes you lose crucial features, like the ability to debug your code or compatibility with other code or development lagging behind the main platform or or or …

![](../../../-6xwmcN_KkJE/T1jOZrK0-yI/AAAAAAAAFLI/pzBi6nAko8U/s1600/Duqu-Trojan-developed-in-unknown-programming-language.jpg)


You should also prefer to use the language that’s native for the operating system or platform, because there’ll be a lot more help for it. For example when I started writing code for iOS I decided that learning Objective-C will be helpful in the long run as it is the platform’s native language. Even though using either C or C++ would have been possible, and faster, and I had a lot of experience with both.

Lastly, when given the choice between game engines where none of them uses a language you’re familiar with, you may want to go with the game engine using a scripting language. If that’s not available, pick one that has automatic memory management, for example Java, C#, Objective-C with ARC.

#### Documentation

![](../../../2012/02/documentation.jpg)


There’s also the type of documentation that was written to lure developers in. So make sure the documentation has depth, and not just wonderfully crafted beginner’s tutorials which only cover the basics. This is particularly important if the game engine has a free and a commercial version. The free version’s documentation may either be limited, or describe features only available in the commercial version, or tries to upsell the commercial version in other ways.

One sure way to know if a game engine is well documented is to figure out if there’s a book about the game engine available which is less than one year old. Game engines for which you can’t find a single book don’t have the critical mass (yet). Though only an indicator it’s probably safe to assume that no book means that documentation about the engine will be harder to find in general. Use google to confirm.

#### Maintenance

Most game engines have a list of past releases hidden somewhere, typically in a file named HISTORY or CHANGELOG. Open source engines have an advantage here as you can simply check the commit log. For commercial engines it may be more difficult to find out when the last few major updates were released. Sometimes you can find this information in press releases, other times you’ll be lucky enough to find it in the engine’s downloads section. In some cases you may not find this information at all. If that happens, be sure to check the support forum to see if many users are complaining about the update policy.

If there weren’t any substantial updates to the engine in over a year, this should alarm you. On the other hand, there are game engines which haven’t seen a new version in years. That may be ok and it may actually be a good sign that the engine has matured enough to do exactly what it is supposed to do. But those cases are rare and apply mostly to specialized engines, for example game creation kits that were made to create only specific types of games (ie Point & Click Adventures, Side-Scrolling Shoot’em Ups, old-school RPGs and so on).

Maintenance is most important if the engine is not open source. Otherwise you may have to wait many months before you can use a new feature of a platform, for example iOS Game Center. But maintenance can be crucial for open source engines as well, primarily if you don’t have an interest to dabble in the engine’s source code or the target platform or operating system changes more frequently than the engine itself.

#### Support

Commercial engines often advertise their level of support, but it’s hard to judge. You might want to give this a try and ask the support staff general questions about the game engine before making a purchase. If you don’t get satisfactory answers within a reasonable period of time, chances are the technical support may not be great either.

Free engines rarely offer official support, but they do have forums, discussion groups or mailing lists. If not, or if they’re rarely frequented, it’s a good sign that you might want to stay away from the engine if you expect to have questions as you start working with it. If the engine is open source, and you can read code and have a DIY attitude, then it may not be much of an issue after all.

You will also want to find the cases where developers are reporting issues that actually get fixed and suggestions that actually get implemented, respectively a lack thereof. It’s rare that engines receive lots and lots of updates but not the ones developers were asking for, but it happens. Free engines are most prone to this as developers don’t make a buck with the engine and the authors may rather work on whatever they like working on or happen to be working on anyway.

Finally, look for a frequently answered questions (FAQ) document or thread. This is one of the two most important indicators for good support. The FAQ should be up to date to the most recent version and the questions ought to sound like they’re rather frequently asked and not mundane (“How much does it cost? It’s free.”) or relatively niche (“How do I enable the asymmetric haptic input command module?”).

The other important factor to consider is the type of communication that happens in the forum or other community places. Look for questions that you are having or can imagine to have and were asked like you would ask them. Check the responses. Some places are known for shunning obvious beginner questions but indulging in excellent discussions about advanced subjects with lots of interesting code being shared (think: IRC). Others may be very welcoming and helpful to beginners but barely anyone will answer to any advanced question with a definite answer. In any case you don’t want to see many reasonable questions at about your level of expertise with no or unhelpful answers.

And a quick test to see if you can find support for the engine besides the official channels is to search [Stackoverflow.com](http://stackoverflow.com/) and [Game Development Stack Exchange](http://gamedev.stackexchange.com/). If you can’t find any helpful answers for the game engine on these sites, you will most likely have to rely on the official support channels.

#### Cost

Any game engine that costs less than $300 (per year) is practically free. If you intend to use the engine for a longer period of time, or if you plan to sell your apps, and generally if you’re being serious about it - hobbyist or not - then whether you pay a few hundred bucks or nothing at all doesn’t really matter. Especially if you see it as an investment in yourself and your career.

Game engines must be considered as a service, not as a product. So you should not consider the price tag alone but the total cost of ownership (I’m not sure if there’s a usership but it would apply here). Even free engines can cost you a lot of a valuable resource: your time. Sometimes your nerves, too.

At the extreme end of the spectrum are engines that cost you 4 digit numbers or more. Sometimes even per-license. You’d have to be dead serious (ie running a successful game studio) to consider using those. Or affluent, that would work too. Definitely not the right choice for single game developers without 5+ years of industry experience. Don’t be in awe, ignore those engines. They’re made for professional teams, not individuals.

Of course there’s a dropoff that’ll be different for every developer. Some just can’t afford to spend any money at all, or simply don’t want to (yet). In that case all commercial engines are out, and free it is. But do consider that the price you pay for commercial engines usually pays back in better and friendlier support, more documentation, frequent updates, excellent tools, and what not. Whereas free (and usually open source) means that you have to do a lot of the groundwork yourself and may end up spending a lot more time on your app, and really no one is obliged to help you out. That’s when you learn how “free” your time really is.

If you consider a free game engine that has a number of highly recommended commercial tools, do add the costs for these tools to your calculations as well. Because such a game engine will only live up to its strengths if you do use at least the essential tools. For cocos2d-iphone that’s easily $50 in the essential texture atlas, bitmap font and particle design tools. More than $100 if you’re also interested in purchasing starterkits, books and online tutorial videos.

#### Features

Practically all game engines offer the necessary features to write excellent games. However, their marketing departments think otherwise. I find features are the least important aspect of game engines that you should consider, yet feature lists are typically the most widely considered aspect. That’s because marketing knows how much we long for more and better in easily comparable lists and tables. Features are a tempting promise to get to where we like to go faster with greater ease, but unless you’ve had first-hand experience, they’re no more than a promise.

![](../../../wikipedia/commons/7/7d/Rolls-Royce_Merlin.jpg)


Editing tools may be part of the engine, or 3rd party. Either way, tools always help developers getting things done faster, more reliably, or at all. The integration of the tools with the engine, their maturity, stability, usability and the workflow is where the biggest differences are. There’s no perfect tool, but having tools is always better than no tools at all.

One truth about good tools is that they’re never free. I would say 90% of all free game editing tools I’ve ever used just downright suck (overall lack of features, polish, stability, functionality, usability, purpose, maintenance, documentation). There are a few shiny exceptions, and you’ll know them when you use them, and those you should hold dear. [Tiled](http://www.mapeditor.org/) comes to mind. The rest you pay for, and they’re well worth every cent.

Exceptions to this rule are free tools published by commercial companies because the tool’s development cost is subsidized in other ways. Apple’s Xcode is a great example. It’s free because developers need it to create apps, and it pays because registered developers pay $99 per year to Apple to be able to publish apps, among other things.

Most other game engine features besides 2D/3D, tools and perhaps a specialization for a specific game genre are not nearly as relevant as you might think. Most game engines are general purpose and offer no more and no less than basic graphics rendering and animations. You will still have to programm 99% of the game yourself, and that typically includes collision detection, setting up the scene graph and screen flow, user interfaces and HUDs, input handling and audiovisual responses, artificial intelligence, pathfinding, and other game logic algorithms.

And features can be very misleading. Collision detection may be a check, but does it support the exact type of collision detection and resolution that you need: ray intersections of arbitrary polygons? Does tile rendering include support for the tile editor of your choice, hexagonal maps with arbitrary orientation and multiple layers? And does the user interface feature include more than simple buttons, text boxes and sliders?

You’d be surprised how often you’ll find that a game engine supports feature X but when you start using it, it’s not quite as complete as you’d hoped it to be, or worse. Hope is not a strategy, that’s why you need to test-drive the engine at least for a couple hours. Test all aspects of the features you need to be sure it meets your requirements.

And don’t even get me started on purely visual features. Who cares if the game engine supports polynomial fractal shaders 4.0 with volumetric shadow stencil aliasing and deferred hidden-surface glow. It’s your game’s assets, the camera movements and basic lighting and particle effects that define the look of your game the most, not the renderer.

#### Open Source is not a feature

What good is an open source engine if you don’t RTFC? I occasionally see questions that could easily be answered by jumping to the source code of the particular method in question. Or by stepping through the code in the debugger to see why the code is failing. Allowing that is the beauty of open source game engines.

Open source becomes a beast though if the game engine’s code overwhelms you and you never look at it. You won’t benefit from open source if you’re not spending time browsing and understanding the code. With every open source game engine I’ve used, I came to learn a great deal about it’s inner workings (mostly involuntarily I might add), and only then do you really start to benefit from an open source game engine.

In other words: open source is not a feature, it’s an opportunity and an invitation to learn, modify and share. If you don’t RTFC then an open source game engine will not help you in any way.

Open source engines are typically more difficult to work with since any source code can generate compile errors and updating the game engine’s source code is prone to generating such errors. The initial setup may also be cumbersome, especially when compared to a commercial level game engine with an installer. For beginning game developers, a closed source game engine will almost always be the better choice.

#### So which game engine is better?

The question must be rephrased: which game engine is best for you?

And since that decision requires intimate knowledge about you and your preferences and goals, the only person who can reasonably answer that question is **you**. In other words: if you have to ask, it doesn’t even matter.

The worst you can do is to spend too much time finding and deciding on the perfect game engine, instead of actually working on your game. Avoid [Analysis Paralysis](https://en.wikipedia.org/wiki/Analysis_paralysis) - if in doubt, follow your gut feeling and a quick facts check. You can always switch game engines later or for the next project if it doesn’t work out between the two of you.

The most productive programmers just download a game engine they like and start working with it.

One more thing: if you’re using a new and unfamiliar game engine, start with a simple test project. No matter how experienced you are as a game developer, your first project’s code will be crappy.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I like the sex analogy. Right on the spot![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Interesting reading. Hhmm, I got a doubt. I have always considered that cocos2d is not a game engine, but a graphics engine with some additions. What do you think?

Depends on the definition I guess. Personally I also see it more as a graphics library because when you get to actually implementing a game, you still have to do a lot of groundwork.

For mobile devices, performance is important especially if the engine is used on certain script language.

I had a painful experience about it. Switching engine in the middle of development is not fun at all.

What engine was that? The only one I know is based on a scripting language is Corona.

[…] The game engine dating guide: how to pick up an engine for single developers Steffen Itterheim wrote a detailed guide to choosing the right game engine when you’re working on your own. It’s a gem and even if you aren’t interested in writing games, it’s worth a read — a lot of his advice translates to choosing frameworks and even programming languages. […]

Steffen,

Enjoyed the article. Advice is applicable to LOTS of development frameworks.

FYI .. ‘irregardless’ is not a word. The word you want to use here is regardless. I guess irregardless would mean with regard since it implies a double negative.

Just sayin’