---
title: The Mobile 2D Game Engine Popularity Index – November 2013
url: http://www.learn-cocos2d.com/2013/11/mobile-game-engine-popularity-index/
author: Jeff Says
published: '2013-11-14'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Topics: Overall interest in cocos2d is waning. Unity and libgdx fighting for 1st place. Sprite Kit skyrocketing from day one.

This sums it up. Now for the details. Since [my last game engine popularity measurement](http://www.learn-cocos2d.com/2013/07/measuring-game-engine-popularity/) I tried to improve and streamline the process.

### Game Engine Popularity on Stackoverflow.com

For stackoverflow.com data I’m searching for tagged questions created in a specific month. The search query looks like this:

```
[cocos2d-x] is:question created:2013-11
```


I repeated this for every tag for every month as far back as there were questions with the given tag.


For cocos2d-iphone I had to use two passes, one for each tag [cocos2d] and [cocos2d-iphone]. Though these tags are now synonymous, stackoverflow.com did not combine these tags in the search results as one for the time where they were considered separate tags. So I simply added both results together, even if that may include the occasional niche cocos2d engine question, including the original Python cocos2d.

I then did a third pass to subtract all questions tagged [cocos2d-x] since the [cocos2d-x] practically excludes cocos2d-iphone. Almost all questions containing both tags are simply tagged incorrectly and do in fact revolve around cocos2d-x rather than cocos2d-iphone or, very rarely, both (ie “which cocos2d should I use?”).

For Sprite Kit I hopefully fixed all incorrect uses of [sprite] and [kit] which only affected early questions before the [sprite-kit] tag was added. I also did several passes for class-specific tags that did not include the [sprite-kit] tag, for example [SKSpriteNode], [SKAction], [SKPhysicsBody]. I noticed that contrary to other class tags like [CCSprite] these did not include the engine tag itself. This also may have been an early-days glitch.

I did not exclude closed questions, after all I want to measure overall interest and not the quality of the questions.

#### Stackoverflow Tag Popularity Analysis

Click on the image for the fullsize version. The graph contains the tag query results with moving average trendlines in black, over a 4-month period.

These recent trends are notable:

- Since summer 2013 cocos2d-iphone activity has been steadily declining. The ups and downs are almost parallel to the second half of 2012, only this year the activity is far lower and has reached a historical 2.5-year low.
- Unity has been trending steeply upwards since August 2013. Its trendline almost crosses that of cocos2d-iphone, and in raw numbers for the past two months more questions were tagged with [unity3d] than [cocos2d-iphone]/[cocos2d]. Perhaps the announcement of the Unity 2D Tools explains the recent increase in questions, though the actual release was only a couple days ago.
- Libgdx and cocos2d-x are both gaining traction slowly but very steadily trending upwards. Both did not shoot through the roof as Unity did in the past two months. While both engines were very close over the course of 2011 through 2012, libgdx popularity is growing slightly but consistently faster than cocos2d-x over the course of 2013. This trend is actually a lot more pronounced in google trends (analysis below).
- Sprite Kit simply popped into existence, beating both libgdx and cocos2d-x in popularity practically from day one. Sprite Kit looks keen on overtaking cocos2d-iphone in sheer number of questions this year already. A fantastic start but not the least bit surprising.

The big winners this year are cleary Unity and Sprite Kit, whereas cocos2d-iphone has lost its first place, undisputed for the past five years, to Unity. It may even fall back to third place behind Sprite Kit before the year counter increments.

Both libgdx and cocos2d-x are delivering a head-to-head. Currently libgdx has the lead on programming-centric cross-platform 2D mobile game development. In a way, this is also a fight between Java and C++. So far, Java seems to be winning (as reflected by all three programming language indexes btw, see the next paragraph).

### Google Game Engine Trends

Since stackoverflow is only one side of the story I’m using google trends to confirm or disprove trends seen on stackoverflow.com. The google trends graphs reflect developer interest more accurately since some engine’s users are more likely to post on stackoverflow.com than others. Case in point: despite its popularity only a relative minority of Unity developers seek help on stackoverflow.com.

The idea for using google trends comes from the [PYPL Popularity of Programming Language Index](https://sites.google.com/site/pydatalog/pypl/PyPL-PopularitY-of-Programming-Language), an alternative to the [TIOBE Programming Community Index](http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html). The [Transparent Language Popularity Index](http://lang-index.sourceforge.net/) remains a more viable and more accurate option for the future because it’s open source.

In line with the PYPL index, each engine’s name is appended by “tutorial” to find users interested in learning (more) about that specific engine.

Unity in particular is quite ambiguous, even within the software engineering world. Since my main interest is in 2D game engines, I used the search phrase “unity 2d tutorial”.

You’ll find the exact search terms and the numbers for particular months by moving the mouse over the graphs.

#### cocos2d-iphone vs cocos2d-x vs the contenders

In this graph I split up cocos2d by using the search phrase “cocos2d-iphone -android -cocos2dx -cocos2d-x” to remove both cocos2d-android and cocos2d-x from the equation.

Again you can see cocos2d-iphone trending downwards, except here it has been on a slow but steady decline for the past two years since November 2011 with no sign of recovery. One can argue that at least partially this is caused by cocos2d-x cannibalizing on the cocos2d-iphone user base.

But it also falls in line with the growth of Unity (for 2D development) and libgdx. Both have become more popular for 2D mobile game development than cocos2d-iphone in the past couple months. Another factor will surely be raising interest in Android or cross-platform development in general.

Surprisingly cocos2d-x doesn’t show any signs of catching up as it did in the stackoverflow graph. Though I assume that the cocos2d-x line dropping to zero this November must be a glitch.

Sprite Kit (purple line) is at least as popular as cocos2d-x now, and once more it seemed to have come out of nowhere.

#### Cocos2D vs The Rest

I thought it’d be interesting to see what difference it makes if we consider cocos2d as a whole by using the simplest search terms “cocos2d tutorial”. At the same time I added Corona SDK to the mix (red line). I omitted Sprite Kit from this graph since it’s just that little blurb in the corner at this point.

Despite counting all of cocos2d together, it’s still less popular now than Unity, libgdx and Corona.

What’s interesting for Corona is that it seemed to have grown in three concrete steps. Each time popularity suddenly raised significantly above the previous level, and then steadily remained at that level for at least a year. My guess is that this is both influenced by pricing changes and running marketing campaigns.

#### Unity vs The Rest

I was wondering how Unity fit into this picture overall, by using it’s most common but still non-ambiguous search term “unity 3d tutorial”.

This shows clearly how much of a lead Unity has. Up until the middle of 2011 cocos2d was able to grow steadily at almost the same pace as Unity. But then it stagnated over the course of 2012 and since 2013 is now trending downwards.

Unity giving away their mobile versions for free and the announcement of Sprite Kit seems to coincide with a more accelerated downwards trend for cocos2d in the recent months. Let’s hope v3 can turn this trend around.

Here are some key dates for this graph:

April 2010: Corona 2.0, Corona Game Edition announced

September 2010: Unity 3.0

December 2010: Learn Cocos2D book released

January 2011: Corona runs on Windows

May 2011: Cocos2D developers hired by Zynga

July 2011: Learning Cocos2D book released

February 2012: Unity 3.5

July 2012: cocos2d-iphone 2.0

November 2012: Unity 4.0

May 2013: Unity for iOS & Android now free

June 2013: cocos2d-iphone 2.1, new lead developer

#### Just the names …

Lastly I wanted to see what graphs we get when searching without “tutorial”, just using the engine names. This doesn’t reflect engine use or interest of course, since without “tutorial” we can’t be sure of the intention to actually use the engine.

I added OpenGL ES to the mix as a nice and steady baseline. Interestingly OpenGL ES is also slowly trending downwards over the past 1-2 years, perhaps attributed due to the fact that overall rendering engines as well as the increasing horsepower of modern devices slowly diminish the need to learn or use OpenGL ES.

Corona is once again interesting, showing a nearly linear graph over its entire lifetime. Admittedly this may be due to using a slightly different search phrase, with “SDK” appended. Solar eclipses are rather popular, so much so that without “SDK” all the other lines are neatly squashed together at the bottom. So take the Corona line here with a grain of salt.

### Final Observations

All of this leaves me with one question: where is cocos2d heading? And as a consequence, what am I going to do?

Cocos2d-iphone v3 may or may not rekindle interest. For one Apportable is now sponsoring development, including the successor of CocosBuilder named SpriteBuilder. On the other hand Sprite Kit has a big bonus coming from Apple, and it is capable of doing what the great majority of developers need. Not only that, it’s more than capable enough for new game developers to not look for alternatives.

Personally I think the downwards trend will continue in the near term, regardless of cocos2d-iphone v3. Cocos2d-iphone v3 will fill a niche for developers who want low-level access but nevertheless don’t want to write their own renderer. SpriteBuilder is an advantage but a comparable game editor for Sprite Kit is only a matter of time. In fact it would make a lot of sense if SpriteBuilder would support both renderers.

Sprite Kit will now doubt continue to take over by storm. For the great majority of current cocos2d developers it’s going to be the natural replacement and for beginning iOS game developers it’s the obvious choice. Why bother with an external library if you already get everything you need built-in? That will make the first-use experience a lot more important for cocos2d-iphone to sway users over.

I was initially surprised to find libgdx winning over cocos2d-x, I have never given libgdx much thought honestly. But one aspect may have been cocos2d-x’s attempt at modelling workflows based on Objective-C code, which is just odd. Another turn off is that it’s quite difficult and error prone to set up, more so the more exotic the targeted platform and the more external dependencies (such as compilers) are needed.

Whereas libgdx has the advantage of a simpler and safer language (Java) with the added advantage of having not only a cross-platform compiler built-in (well, Java) but also a common IDE for all platforms (Eclipse). There’s no need for users to install additional compilers, IDEs or adapt to different environments for each platform. This seamless experience is a huge bonus for libgdx.

Corona opening up their C++ framework to enterprise developers has done them well in that market. For programming-centric studios who want a capable cross-platform mobile game engine with no proprietary components, this is a top choice. It also happens to be cheaper than Unity, too.

Unity on the other hand is great for 3D games and in fact for any game that needs a good toolset. It’s a great choice for designer/content centric studios. The 2D toolset will no doubt further nibble on cocos2d’s userbase and all other 2d engines, given their marketing prowess. But make no doubt about it: Unity may be free, but it’s not really free enough to make great games with it. Or have you seen a popular or even best-selling Unity game that still has the forced Unity splashscreen on launch? Eventually there’s a purchase to be made, and it doesn’t come cheap ($4,500 per developer for iOS + Android).

On the other hand, “free” is not a feature for developers looking to actually make a buck making games.

#### I did this to see the future…

This brings me to … myself. In the past I have made “add-ons” to rendering engines with Kobold2D, KoboldTouch and Kobold Kit. Now I’m looking more globally at all rendering engines because what I really wanted to build all along is a **game** engine. Or as I call it, a [game world simulation engine](http://opengameworld.com/) (OpenGW).

When you look at each of these engines, including Unity, what they really excel at is drawing stuff to the screen. But with the exception of Unity’s component-based design, none of these rendering engines provide any structure or framework to write game logic code in, or to re-use existing game logic code.

I’m really excited to see the platformer built with OpenGW is now working on Sprite Kit/Kobold Kit **and** cocos2d-iphone 2.1 at the same time, depending only on which target I build. While these two rendering engines are comfortably similar, it really doesn’t take that much effort to switch out one renderer in favor of another in general. After all, a sprite is a sprite, a label is a label, a view is a view.

The same basic principle is applicable to other renderers. While porting OpenGW to other languages is still way out, I’m beginning to think that instead of a C++ port the better alternative may be to port to C# to support both Unity and Monogame, plus the still large following of XNA developers. That is besides the fact that porting Objective-C ARC code to C# is much easier than the gruntwork required to adapt to C++ (even considering C++11).

#### Last but not least: the smaller contenders …

Surprisingly, besides cocos2d-x I could not find one comparably popular, purely C++ cross-platform mobile rendering engine. Instead what I found comparing the lesser known contenders is this:

Honestly it seems more tempting to support Sparrow Framework in OpenGW before porting to any other language. But also Monogame being on-par with cocos2d-x makes me more confident that C# is the first language to go to, while AndEngine makes a fairly good point about Java despite seeing a downward trend.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Good article, but you have some kind of google trend embedded graphics that take way way too long to load… like you need to leave the page open for 30 minutes to start seeing all the graphs, or they just dont show up at all.

Hmmm strange, I don’t have that problem. But Google Trends has a per-IP usage restriction which prevents them from loading when you access too many in too short a time (ie several page reloads might cause this). Or perhaps they work faster with a google account currently logged in.

I may need to revert to exporting trends as csv and import them in excel, I avoided that extra effort after I noticed the embed button.

Hey,

great article, would be interesting to see whether it makes a difference if you include queries for example in Chinese language. I read that especially cocos2d-x is very famous over there and out of my experience they would not search in english.

Good point. The review is certainly skewed towards english language users.

@Steffen: nice article!

yeah, cocos2d-x has massive audience in Asia: China, Korea, Japan… Your chart will be much different if including those markets.

Also, cocos2d-x v3.0 (in beta now) is a re-designed pure C++ 11 game engine. All the early objc styles have been removed. Check it out and your feedback is always welcome!

Can’t go wrong with C#. It is located in too many sweet-spots: multi-paradigm, multi-typed, cross-platform.

Two best points here:

“Unity on the other hand is great for 3D games and in fact for any game that needs a good toolset.”

- IMHO, this is Unity’s biggest strength, and why I think its use has grown so well and so fast.

“When you look at each of these engines, including Unity, what they really excel at is drawing stuff to the screen. But with the exception of Unity’s component-based design, none of these rendering engines provide any structure or framework to write game logic code in, or to re-use existing game logic code.”

-Calling out Unity’s component based design is something that has helped many dev’s get results fast in Unity, which then leads to even higher adoption, especially among indies and small team.

Thanks for sharing, nice article.

How about analyzing HTML5 tools for game dev next?

[…] This is an update to the Mobile Game Engine Popularity Index I published 2.5 months ago. […]