---
title: From Dogfooding to Catfooding
url: http://www.learn-cocos2d.com/2011/09/dogfooding-catfooding/
published: '2011-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Most developers have heard of the phrase [“Eat your own dog food”](https://en.wikipedia.org/wiki/Eating_your_own_dog_food). It refers to the habit of actually using what you’re creating.

A typical example would be a company building Yet-Another-Issue-Tracking-Tool™ while using said issue tracker to manage their Yet-Another-Issue-Tracking-Tool™ project. And you’ll surely have heard of a game engine that was initially only developed as a necessity to build a game, then polished and released to the public to great success, while the developer continued to create games with his own engine.

Dogfooding is considered a good practice, actually a best practice. You know that the tool you’re building works, and that it satisfies your needs.

But “your needs” is also the achilles heel of dogfooding, and it’s just a small step away from forever “perfecting” your product (known as [“gold plating”](https://en.wikipedia.org/wiki/Gold_plating_(software_engineering))). So sooner or later, you’ll have to do some catfooding, too. Meaning: to feed the user’s needs.


#### When cats start to eat your dog food!

“Gross! How could they? After all, that food is for dogs, not cats! Eeeew.”


Strangely, that is often the reaction (in some form or another) from developers who realize that their project is now being used not just in ways they haven’t imagined, but more importantly by users they never targeted. The result is sometimes seen on forums swamped by newbies given lots of “RTFM!” style answers (and the finger). Or worse, the indiscriminate deletion of many a beginner’s posts. That’s one step away from elitism - once we’ve built something valuable, we tend to want to share it only among “worthy” individuals.

It’s very sad to see it happening to developers who do start out eating their own dog food, do that for a while, but eventually are tasked with so many new things on their “core” technology that they don’t get to (or don’t want to) eat dogfood anymore. I’m guessing the replacement nurishment being fast-food.

In any case, this happens when game developers write a game engine on the side, then realize the game engine is becoming popular, and then end up writing only game engine code and stop using their own code in the way that users do: to create games. Clever game engine developers know that, and [run a contract and consulting team on the side](http://www.unity-studios.com/).

#### How to mix dog and cat food?

So, I’m now working on the [Kobold2D game engine](http://www.kobold2d.com/) full-time. I asked myself: how do I avoid becoming a “dog-eterian” and provide the cat food as well?

One part is that I believe it’s in my DNA. For the past 10 years there was one type of job I’ve always had: to support other game developers (ie colleagues, but also the occasional indie), to make them smarter and to make their work easier. It’s natural for me to think user first, and in particular users that have a lot less experience than I do, have different needs or different skill sets.

There’s also a few lessons’s that I’ve learned from UI and [Interaction Design](https://www.amazon.com/Art-Interactive-Design-Euphonious-Illuminating/dp/1886411840). The basics are quite simple: reduce the number of necessary steps to complete a task (eg [installing](http://www.kobold2d.com/x/0wEO) & [creating a project](http://www.kobold2d.com/x/XwMO)), and make information available where it’s needed but only when it’s needed (eg. [polling the input state](http://www.learn-cocos2d.com/2011/09/kobold2d-polling-user-input-kkinput/) at any time in any class).

Another way to stay in touch with the “cats” (users) is to provide a [means to provide feedback, ideas and suggestions](http://www.kobold2d.com/display/KKSITE/Kobold2D+Feedback). While most rely on forums to do that, I believe a dedicated feedback system like [UserVoice](http://uservoice.com/) literally gives user’s a voice. Ideas can be created by anyone without requiring an account, anyone can vote on existing ideas, and the ideas are neither discussed to death nor lost in the nirvana of hundreds of other forum threads. Most importantly, ideas can be visibly flagged as planned, in progress, completed or rejected. Which takes the guesswork out of user’s expectations. Guess [who else is using UserVoice](http://feedback.unity3d.com/forums/15792-unity) to gather feedback? Note: UserVoice is free if you can limit yourself to one forum.

Taking this one step further is [public task tracking](http://kobold2d.onconfluence.com/display/KKSITE/Kobold2D+Roadmap). Anyone can now see what I’m currently working on, what I’ve planned for the current iteration, what items are in the backlog or the icebox which contains all the unscheduled, unplanned tasks. I use [PivotalTracker](https://www.pivotaltracker.com/) for task tracking, public projects are free and surprisingly task planning software that allows public projects like Pivotal Tracker is hard to come by. But neither free nor public swayed me over, it was the ease of use despite being a web interface, the hosted solution and how it supports agile development. If you really dig Kobold2D, you might want to also follow [@Kobold2D_Dev](https://twitter.com/#!/Kobold2D_Dev) where all Kobold2D related task tracking events are tweeted. For me it’s also a good way to give the project more exposure through re-tweets by enthusiasts who filter the important bits out of the stream of updates.

Case in point: a Twitter user noticed I had AdMob integration as a task in the roadmap, and offered his AdMob implementation. Transparency encourages code sharing.

Finally, the development of Kobold2D should be self-sustainable. One way I’m going to achieve this is through commercial source code game kits, like my [Line-Drawing Game Starterkit](http://www.learn-cocos2d.com/store/line-drawing-game-starterkit/) or the [iPhone Game Kit](http://www.iphonegamekit.com/learn-cocos2d-com). I love making games and solving the gameplay-related challenges. But I also like to create generic systems that can be used by everyone. So I’m going to write feature-rich, playable games with Kobold2D and sell the source code. Maybe there’ll be even a game for the App Store coming out of it. Through developing game kits I get first hand game development experience with Kobold2D, and I know there will always be Kobold2D code improvements coming out of that process.

#### To sum up

Use the right tools (Uservoice, Pivotaltracker, Forum, Wiki, Mailing List) to make your development process transparent and to give yourself the necessary self-discipline to see it through. It has the added benefit that it shows users that you care and that you’re dedicated. It even allows you to make realistic estimates about the next release.

Kobold2D Preview 4 will be available next Tuesday, September 27th. There, I said it!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[achilles heel](http://www.learn-cocos2d.com/tag/achilles-heel/)•

[attitude](http://www.learn-cocos2d.com/tag/attitude/)•

[backlog](http://www.learn-cocos2d.com/tag/backlog/)•

[cat food](http://www.learn-cocos2d.com/tag/cat-food/)•

[developer](http://www.learn-cocos2d.com/tag/developer/)•

[dogfood](http://www.learn-cocos2d.com/tag/dogfood/)•

[exposure](http://www.learn-cocos2d.com/tag/exposure/)•

[fast food](http://www.learn-cocos2d.com/tag/fast-food/)•

[feedback](http://www.learn-cocos2d.com/tag/feedback/)•

[forum](http://www.learn-cocos2d.com/tag/forum/)•

[game developer](http://www.learn-cocos2d.com/tag/game-developer/)•

[game development](http://www.learn-cocos2d.com/tag/game-development/)•

[game engine](http://www.learn-cocos2d.com/tag/game-engine/)•

[github](http://www.learn-cocos2d.com/tag/github/)•

[gold plating](http://www.learn-cocos2d.com/tag/gold-plating/)•

[idevblogaday](http://www.learn-cocos2d.com/tag/idevblogaday/)•

[issue tracker](http://www.learn-cocos2d.com/tag/issue-tracker/)•

[kobold2d](http://www.learn-cocos2d.com/tag/kobold2d-2/)•

[open source](http://www.learn-cocos2d.com/tag/open-source/)•

[permission](http://www.learn-cocos2d.com/tag/permission/)•

[pivotaltracker](http://www.learn-cocos2d.com/tag/pivotaltracker/)•

[planning](http://www.learn-cocos2d.com/tag/planning/)•

[Programming](http://www.learn-cocos2d.com/tag/programming/)•

[progress](http://www.learn-cocos2d.com/tag/progress/)•

[Project](http://www.learn-cocos2d.com/tag/project/)•

[schedule](http://www.learn-cocos2d.com/tag/schedule/)•

[source code](http://www.learn-cocos2d.com/tag/source-code/)•

[teamwork](http://www.learn-cocos2d.com/tag/teamwork/)•

[treatment](http://www.learn-cocos2d.com/tag/treatment/)•

[UserVoice](http://www.learn-cocos2d.com/tag/uservoice/)