---
title: 'Linkvent Calendar, Day 9: The State of Cocos2D Game Engines'
url: http://www.learn-cocos2d.com/2010/12/linkvent-calendar-day-9-the-state-of-cocos2d-game-engines/
author: Karl says
published: '2010-12-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I took some time to research the various ports which carry the Cocos2D name or are Cocos2D in spirit if not by name. The following list is - to the best of my knowledge and at the time of writing - complete and accurate. I counted a total of eight ports.

The dates are based on the earliest public record I was able to find. Of course the project might have been in development for longer, but not publicly or not where I’ve been looking (mostly google code and github). I usually checked the source code commit history, the first issue being tracked, the first post made on the forum or wiki, the history of downloadable files, and similar things. The list is sorted by date of inception. Underneath you’ll find my analysis of the state of the Cocos2D game engines, as I perceive it, and I try an outlook into the future.

Language: Objective-C
Platform(s): iOS Devices, Mac OS X
Around since: June 2008
Latest update: November 2010 (Latest Stable: July 2010, Latest Commit: December 2010)

Language: C#
Platform(s): iOS (MonoTouch)
Goal: to also support other .NET platforms like Windows, Windows Phone and Xbox 360
Around since: October 2009
Latest update: September 2010

Language: Java
Platform(s): Android
Versions: cocos2d-android (code on github), active branch: cocos2d-android-1 (code on github)
Notable: cocos2d-android-1 was branched off of cocos2d-android in October 2010 because some developers were dissatisfied with its slow progress. Apparently source code commits had stopped in June.
Around since: January 2010
Latest update: June 2010 (cocos2d-android), December 2010 (cocos2d-android-1)

Language: C++
Platform(s): Windows, Windows Mobile
Notable: this project was apparently short-lived. One big code push, one blog post, no updates since, neither code nor blog or anything else. I believe we can consider this port dead, especially in light of Cocos2D-X.
Around since: April 2010
Latest update: May 2010

Language: C++
Platform(s): iOS, Android, uPhone, Win32, others
Notable: although the project started in July 2010 (from what I can tell) the project was not widely known until November 13th by announcing it on Twitter.
Around since: July 2010
Latest update: December 2010

The State of Cocos2D Game Engines

In my opinion, we currently have only two serious contenders: Cocos2D for iOS and Cocos2D X.

The former has a history of regular updates for over 2.5 years and a strong community, the latter is growing fast because there’s a whole team behind it which is sponsored/financed by China Unicom. If I extrapolate what has happened in recent months with these two game engines, I’m convinced that rather sooner than later Cocos2D X will be on par or overtaking Cocos2D for iOS in terms of maturity, stability and general applicability. You just have to consider a team of paid (?) developers vs. (for the most part) a single developer, and my guess is they don’t have a problem with and may even be supportive of 3rd party commercial add-on products. I do agree that Cocos2D for iOS will remain the most interesting platform for beginning developers, developers with a strong background in Objective-C programming and those who simply don’t want to take their games and apps to multiple platforms. For everyone else: keep a close eye on Cocos2D X. It certainly had a lot of developer’s eyebrows raised.

There’s one strong follow-up and that is Cocos2D for Web (cocos2d-javascript). Frequently updated and in a well protected niche that can’t be covered by the aforementioned Cocos2D versions. Plus, and this is freaky, you could even make web-based Cocos2D games that also run on the iPhone’s browser - think of the opportunities! It’s iRepetetiveWebBasedGameMakingTonsOfMoney time. Just kidding, except that I’m not. I think Cocos2D for Web stands a good chance at becoming relatively popular and seeing actual use, and with continued and relatively frequent updates this might be happening over the course of 2011. Keep at it!

Cocos2D (Python), the grandparent, is a niche project and it’ll remain a niche project. Too long has it been a niche, too seldom do we see updates, too low is its version number still (v0.4 after 2.5 years), too little interest is there in general for entirely Python based game engines, too strong are the contenders both from the same language (specifically PyGame) as well as most other game engines with a focus on 2D games. The same goes for ShinyCocos - who would want to write iPhone games in Ruby? Don’t kill me, I know you’re out there, but you have to admit that you’re just a little too freaky for your own good. 😉

Cocos2D for Android and CocosNet are both ports I wish I could believe in, but I don’t just yet. For the former, the recent branch has made it more interesting and actively supported, but who knows for how long? And then there’s Cocos2D X which takes some wind out of both, but especially the Android version. Unless you’re Java-esque through and through. For CocosNet I wish it’ll one day reach its goal and hopefully be based on or ported to the XNA platform, and not Mono (yikes!), so that we can write Cocos2D games for the Xbox 360, Zune, Windows and Windows Phone 7 and publish them through/on Microsoft’s AppHub. That would rock! Count me in if that ever happens.

Which leaves Cocos2D for Windows. This is a project that’s so typical of a certain type of open source projects. I dub these occurrences “open source dumps”. It’s literally some programmer coming out of his apartment after months of hard work, telling the world “Hey guys, look, I’m bringing my trash out!”. Except that the trash is actually quite interesting, yet it’s incomplete, unfinished and de facto unusable so it stays in the trashbin and everyone stopping by and taking a sniff is going “Ewwwww!!!”. Well, and said developer goes back to his apartment, probably working on his next trash dump. If we’re lucky, it’ll be an update to the former project - but by the time the second update appears, most developers with an interest have lost faith in the project. But more often than not, we’ll never see or hear of this developer again. In other words: Cocos2D for Windows was practically dead the day it started. And now with Cocos2D X I seriously doubt we need it anymore. It’s a shame.

Add your link to the Cocos2D Linkvent Calendar

Do you have something to share with the Cocos2D community? I haven’t received enough submissions to fill all the days until Xmas, although I do have enough links to post one each day, I’d rather post a link to your website or blog post.

I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. Help me help you by browsing the products in the Learn Cocos2D Store.

You’re right about the original, it stinks that it’s true but it is. Python is a nice langauge for someone who is like me where you don’t have to write 10x the amount of code to do the same thing. The original doesn’t get as much respect as it should, since it’s in my eyes the perfect version of what a game framework SHOULD be. Since it includes a ton of things pygame doesn’t. Pygame includes the bare min while cocos includes exactly what’s needed to make good games. I won’t argue that the other languages are better or worse that’s not why i’m here. But some things just don’t recieve the respect they deserve

TilemapKit is the complete solution for tilemap game developers. Click an image to learn more!

Iso Map rendered by TilemapKit

Ortho Map rendered by TilemapKit

Hex Map rendered by TilemapKit

Steffen's Books

The iOS Action RPG Engine

Rapidly create your own RPG or action-adventure game with this complete starter kit. Includes an ebook, game source code and a royalty-free art package. More Affiliate Products …

Thanks, I really don’t know cocos2d has so many platforms until see your article.

cocos2d-iphone rulez!

[…] Linkvent Calendar, Day 9: The State of Cocos2D Game Engines […]

You’re right about the original, it stinks that it’s true but it is. Python is a nice langauge for someone who is like me where you don’t have to write 10x the amount of code to do the same thing. The original doesn’t get as much respect as it should, since it’s in my eyes the perfect version of what a game framework SHOULD be. Since it includes a ton of things pygame doesn’t. Pygame includes the bare min while cocos includes exactly what’s needed to make good games. I won’t argue that the other languages are better or worse that’s not why i’m here. But some things just don’t recieve the respect they deserve