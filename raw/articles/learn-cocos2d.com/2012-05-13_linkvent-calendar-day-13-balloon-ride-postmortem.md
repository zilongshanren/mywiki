---
title: 'Linkvent Calendar, Day 13: Balloon Ride Postmortem'
url: http://www.learn-cocos2d.com/2010/12/linkvent-calendar-day-13-balloon-ride-postmortem/
author: Fandang
published: '2012-05-13'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Today’s Linkvent Calendar entry comes from David Sutoyo. His second Cocos2D game, Balloon Ride, was published on the App Store on Dec 1st. David took some time to write a postmortem about making Balloon Ride. He starts out by saying that programming in Objective-C is hard, game design is even harder but marketing is the hardest part. However, he concludes that the overall design process is fun and he is now toying with the idea of using Corona because programming in Lua is simpler than Objective-C.

I spend a lot of time coming up with ideas that will help you become a better app developer. I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. Help me help you by browsing the products in the Learn Cocos2D Store.

You can also show your (much appreciated!) generosity by sending me a gift.

Since I’m still on game design level I would agree with David. Just imagine what kind of professionals design BIG games, like StarCraft for example…
And I can’t get idea to use Corona, instead of Cocos2D. Yes, Lua is simplier … But are there any other benefits? And what are general differences, except programming language used?

About Corona, the big plus is that it’s cross-platform (iOS, Android, more to come). Then it’s designed to be device-independent, any game runs with any resolution.

Besides that, Lua is a big plus on one hand, it’s easier to understand and has automatic memory management. On the other side it’s harder to debug (no breakpoints, no stepping through code).

And there are great tools available or coming soon, SpriteDeck Level Editor, Corona Project Manager and ParticleCandy.

One plus for Cocos2D though: you can choose which libraries you want to use, Corona is a closed system where you can’t add 3rd party libraries or iOS features (eg Game Center support) without Ansca adding it to the engine. On the other hand, this is exactly what most beginning developers struggle with: integrating other libraries and in general other developer’s code, because it often differs from how Cocos2D works (mostly a matter of design philosophy).

Steffen, what way do you prefer and why?
And please make some tutorial about game design and let me know HOW for example Blizzard makes their games sooooo balanced.

Well, historically I’m a big fan of Cocos2D, but because I’ve been using it for so long I’m also a big critic, so you could say it’s a love-hate relationship.

As for Corona I know I love Lua, but that is also a love-hate relationship too. For me as a programmer, at the end of the day I *need* a debugger, and I want full control. But for someone starting out, or who is “Objective(C)ly challenged”, Corona is a much better option. It’s the perfect middle ground between a game creation tool like Game Salad and “hardcore” programming like Cocos2D / iOS.

Oh, forgot about Blizzard. Well there’s one simple explanation: they can give a rat’s rear for budgets and schedules. Their primary goal above all else is quality and that’s achieved through rigorous and repeated testing.

The reason why most other games are below par is because their development stops around the 80% falloff curve, where further development has little gain. Yet it’s those remaining 20% that Blizzard is able to indulge in because they have fewer constraints than other studios. They do great games because they have had past success. Other studios just aren’t so lucky but could deliver the same quality, if you gave them twice the budget or twice the time, or both. (But honestly, I’m sure 80% of the cases where that actually happens, you’d still get a crappy game out of it).

Regarding StarCraft. Yes, I know they game launch scheduling rules (as soon as possible ). But I wonder how they do characters balancing. You know, all three races are so good balanced. Huge amount of work. Are there special known techniques? Or is it just “many years” experience.

>>But I wonder how they do characters balancing. You know, all three races are so good balanced. Huge amount of work. Are there special known techniques? Or is it just “many years” experience.<<

Both. You can definitely balance a lot on paper by making complex formulas, taking into account hitpoints, damage dealt, attack range, movement speed, and so on. The next step is to actually simulate this ingame. If you remember Warcraft, the first or second one, in the main menu when you just waited for a couple seconds the game would start and 20 orcs would fight 20 humans. That’s what you do ingame. Automated fights with various setups, multiple runs and then analysing the data afterwards.

We did that for Spellforce to get the game at least decently balanced, because testing this with human players alone would be nearly impossible.

Rapidly create your own RPG or action-adventure game with this complete starter kit. Includes an ebook, game source code and a royalty-free art package. More Affiliate Products …

Since I’m still on game design level I would agree with David. Just imagine what kind of professionals design BIG games, like StarCraft for example…

And I can’t get idea to use Corona, instead of Cocos2D. Yes, Lua is simplier … But are there any other benefits? And what are general differences, except programming language used?

Thanks in advance.

About Corona, the big plus is that it’s cross-platform (iOS, Android, more to come). Then it’s designed to be device-independent, any game runs with any resolution.

Besides that, Lua is a big plus on one hand, it’s easier to understand and has automatic memory management. On the other side it’s harder to debug (no breakpoints, no stepping through code).

And there are great tools available or coming soon, SpriteDeck Level Editor, Corona Project Manager and ParticleCandy.

One plus for Cocos2D though: you can choose which libraries you want to use, Corona is a closed system where you can’t add 3rd party libraries or iOS features (eg Game Center support) without Ansca adding it to the engine. On the other hand, this is exactly what most beginning developers struggle with: integrating other libraries and in general other developer’s code, because it often differs from how Cocos2D works (mostly a matter of design philosophy).

Steffen, what way do you prefer and why?


And please make some tutorial about game design and let me know HOW for example Blizzard makes their games sooooo balanced.

Well, historically I’m a big fan of Cocos2D, but because I’ve been using it for so long I’m also a big critic, so you could say it’s a love-hate relationship.

As for Corona I know I love Lua, but that is also a love-hate relationship too. For me as a programmer, at the end of the day I *need* a debugger, and I want full control. But for someone starting out, or who is “Objective(C)ly challenged”, Corona is a much better option. It’s the perfect middle ground between a game creation tool like Game Salad and “hardcore” programming like Cocos2D / iOS.

Oh, forgot about Blizzard. Well there’s one simple explanation: they can give a rat’s rear for budgets and schedules. Their primary goal above all else is quality and that’s achieved through rigorous and repeated testing.

The reason why most other games are below par is because their development stops around the 80% falloff curve, where further development has little gain. Yet it’s those remaining 20% that Blizzard is able to indulge in because they have fewer constraints than other studios. They do great games because they have had past success. Other studios just aren’t so lucky but could deliver the same quality, if you gave them twice the budget or twice the time, or both. (But honestly, I’m sure 80% of the cases where that actually happens, you’d still get a crappy game out of it).

Thanks Steffen!

Regarding StarCraft. Yes, I know they game launch scheduling rules (as soon as possible

). But I wonder how they do characters balancing. You know, all three races are so good balanced. Huge amount of work. Are there special known techniques? Or is it just “many years” experience.

>>But I wonder how they do characters balancing. You know, all three races are so good balanced. Huge amount of work. Are there special known techniques? Or is it just “many years” experience.<<

Both. You can definitely balance a lot on paper by making complex formulas, taking into account hitpoints, damage dealt, attack range, movement speed, and so on. The next step is to actually simulate this ingame. If you remember Warcraft, the first or second one, in the main menu when you just waited for a couple seconds the game would start and 20 orcs would fight 20 humans. That’s what you do ingame. Automated fights with various setups, multiple runs and then analysing the data afterwards.

We did that for Spellforce to get the game at least decently balanced, because testing this with human players alone would be nearly impossible.

Sounds interesting

By the way, Spellforce was great, if I remember game it means that game was great