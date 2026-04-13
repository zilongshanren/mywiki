---
title: Rhythos! Arcade BETA Development and Future
url: http://david.fancyfishgames.com/2013/05/rhythos-arcade-beta-development-and.html
author: Legend
published: '2013-05-02'
source_blog: The Legend of GameDev
source_site: http://david.fancyfishgames.com/
category: graphics
fetched: '2026-04-13'
---

I had contemplated making this game a long time ago, but never had the chance, given that the idea was vague and could take a long time to make (since I wanted out-of-battle RPG content as well as the music-focused battles). It wasn't until February that I began developing Rhythos in earnest, as part of One Game A Month. I came up with a concrete idea for the battle system, and decided to use free, open source

[LPC art](http://lpc.opengameart.org/)to speed up the art side of the development. However, after about two weeks I realized that I wouldn't have enough time in the month to complete the game as I had envisioned it, and so instead I created

[A Different Color](http://www.newgrounds.com/portal/view/612076)as my February 1GAM game. At that point I had already decided upon my March game, and so I didn't get back to Rhythos until April. Below is a screenshot of where I left off in development in mid-February.

This original battle system was a lot closer to a stepmania-type game than it is now, with all actions having to be hit at exact notes, and the closer you get to the note, the better the action performed. When I came back to the game in April, I decided not only that it would take too long to make, but that the system wasn't as fun as I'd envisioned, and could be greatly improved. A big problem with the original system is that it brought all of the focus to the arrow bars, and the character's actual battle below was extraneous, just a visual depiction of how well you did. I knew I had to bring the focus and attention to the battles. After some brainstorming of ideas, I eventually settled upon a battle mechanic very similar to the current one. After having to scrap most of the February code and doing some rapid prototyping for a week, I got what is shown below.

This prototype had no menus, it simply loaded and instantly put you into a battle with a skeleton, the only enemy type. At this point, only the bow weapon type was complete, I didn't even know what I wanted the other types to be. While primitive, it allowed me to see how the basic gameplay felt, and was a big first step.

Here are some screenshots from a week later (April 13th) - I had added spells, evading and defending for both the player and enemy. At this point I felt like I was making progress, since the gameplay felt cleaner and more focused. However, I was moving further from the original idea of a "rhythm" game, and more towards a pure action/fighting game. But I knew I would eventually figure out a way sync the game with the music, and so I just crunched out the basic systems.

After the third week of April, I had decided on all of the weapon types, added the combo bar, and added the UI framework that I would use to create all of the menus and dialogs. I still didn't have a main menu, the game just let you create your character, set his or her equipment, and then fight the same skeleton enemy. Things were finally starting to shape up, but I still had a long way to go, and it was already April 22nd by this point. I was starting to think that once again I had taken on too much, and would have to postpone releasing the game. I certainly wouldn't have time to add the out of battle elements or story elements that I had hoped for, and it wasn't even clear if I could make a well polished battle arcade game with only eight days to go. Ludum Dare 26 was coming up, so I was contemplating putting Rhythos on hold yet again, and submitting a Ludum Dare game as my April 1GAM.

Of course, I didn't stop working on the game while I waited for Ludum Dare to begin, and due to a combination of good progress on the game during those days, and not liking the theme of "Minimalism," I decided to crunch for making Rhythos! Arcade BETA. The "Arcade" subtitle is because it would just be battles up a ladder of enemies rather than a full RPG, and BETA because I would only have a few days to balance and tweak the game before releasing.

Late on April 28th, the game was finally "feature-complete," all of the features I wanted were in and tested, and all that was left was setting stats and balancing the game. I had created a little script that took a pattern of actions and the BPM of the song and automatically synced the enemy's actions to the beat, so the problem of syncing the battles to the music was also solved. The idea was that the player's actions would need to follow the beat in order to deal with the enemy's timed actions. The player wouldn't need to follow the music exactly, but a little leeway and flexibility doesn't hurt.

Fun Fact: It wasn't until around this point that I had finally come up with the name Rhythos! Before, I was just calling it MusicRPG, and without any story elements, I had trouble coming up with a name. Rhythos is actually a portmanteau of the words "Rhythm" and "Zythros," where Zythros is the name of the continent in my other RPG world (and has been used in several games I've made since I was in high school).

The animated stars are a cool feature I probably didn't have time to code, but I added them anyways!

The last two days of April involved a lot of play-testing, debugging and tweaking. I knew two days wouldn't be enough to get everything perfect, but I had the disclaimer "BETA" right in the title, so I decided to just get things as polished as I could. I can't even remember how many hours I played, testing out different weapons and spells, beating the game again and again as I changed stats around. But, I never hated playing the game, which was a good sign - as often after playtesting a game too much you can get very tired of it. That told me that the game had a lot of potential for being fun and had good replay value.

I had my friends and family play the game too, and posted a link on twitter for my followers. Finally, late on April 30th, I wrote the manual and created the

[Rhythos website](http://fancyfishgames.com/rhythos/). I was quite proud of the game itself, and of having crunched to finally finish this month instead of postponing it. I added achievements and uploaded it to Newgrounds the following day, on May 1st. Since then, it's had positive reviews, although some people complain that the game is too hard, while others complain that the game is too easy. I guess you can't win the balancing game, but at least it wasn't hard enough that everyone found it frustrating (or too easy that it bored everyone). So, all and all I'd say the rushed release was a success, and I've already gotten a lot of valuable feedback for future improvements.

Currently, I have two plans for the future of Rhythos, both of which are probably over-ambitious again! The first is making a full RPG using Rhythos as my battle engine, with a complete story and out of battle gameplay elements. It's what I always wanted with this game. The second is an RPG Maker-like editor for the game - I loved RPG Maker a lot as a kid, and think that allowing others to create their own RPGs on top of this battle engine would be great! Not to mention, a Rhythos editor would make it a lot easier to make my own RPGs. While a full-featured editor would be a lot of work, Rhythos already has a lot of the core functionality needed, and I have a decent sized code-base from a previous attempt to create an RPG editor. So, no promises, but both plans are something I'd like to do in the future if I can find the time.

So, that's the news for Rhythos, feel free to play it on my

[website](http://fancyfishgames.com/rhythos/)or on

[Newgrounds](http://www.newgrounds.com/portal/view/616768). Let me know what you think and if you have any suggestions for improving it! And, if you're interested in using an RPG Maker-like editor with this as the battle engine, let me know, as the more interest there is in that, the more motivated I'll be to make it!

## No comments:

## Post a Comment