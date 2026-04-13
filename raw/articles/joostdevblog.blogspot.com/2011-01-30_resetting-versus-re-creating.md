---
title: Resetting versus re-creating
url: http://joostdevblog.blogspot.com/2011/01/resetting-versus-re-creating.html
author: Joost van Dongen
published: '2011-01-30'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Ronimo Games](http://www.ronimo-games.com)right out of school and was the only programmer, and thus directly the lead. Since I did my internship as a

[3D](http://student-kmt.hku.nl/~joost1/Oogst3D/index.php?file=3DLO/DesertEagle.txt)

[artist](http://student-kmt.hku.nl/~joost1/Oogst3D/index.php?file=3DLO/Van.txt), this means I never saw how other companies handle their programming. The result is that all of the coding style decisions at Ronimo are just based on my own opinion, and I may be missing some important things that I simply never thought about.

Interestingly, we have been hiring some programmers in the past year, growing the team from just me to five full-time programmers next March. Although the two programmers who have already been working with us for the past year (Ted and Maarten) are former interns of mine, it turned out that as soon as we hired them as real employees, they actually had Opinions. Which is great, because not just blindly doing what I come up with greatly helps against tunnel visions!

One important thing I learned that way recently, is that resetting and reusing objects is error prone, and that a structural change can avoid this.

Let me explain this through an example. In Ronimo's Secret New Game (tm), the player can control a character that when killed, will respawn after a while. My method for doing this, was to hide the character on death, and then reset him when he is respawned, and make him visible again so that the player can continue playing with him.

![](../../assets/8bc19995b1b6eec8.gif)

The problem with this is, that it is easy for the programmer to forget some elements when hiding and resetting. The character consists of many graphical elements, and since they are in very different categories (like healthbar, shadow, character, special effects, etc.), it is not feasible to put all of them in a single list. So when programming the hiding, I need to think of all these elements. The same kind of issue occurs when resetting: many aspects need to be reset (like combo counters, cooldowns on actions, poison time remaining, etc.), and again I need to think of all of them when resetting.

Adding new features is even worse: I always need to remember to add them to the hiding function and to the resetting function. Forgetting one of them results in a bug. Not hiding something is an easy bug to spot, but not resetting something is a lot more difficult to notice, since many effects may usually time out before the respawn timer is over. So it is easy to overlook that sometimes a cooldown may not have expired yet when the player respawns.

This may seem like a subtle and irrelevant issue, but it is very easy to accidentally introduce bugs here when developing a game with more then one programmer, since not everyone may know about these details. So I had been struggling with this for a while, without being able to think of a good solution.

Recenlty, my colleague Maarten came up with a really simple fix: why not completely delete the character on death, and re-create him on respawn? Now we don't need to hide or reset anything. Win!

![](../../assets/6ada327b89e01593.gif)

It turns out that this simple principle actually applies to a lot of things. For example, in

[Swords & Soldiers](http://www.swordsandsoldiers.com), we create all the menus when the game starts, and then just hide them all, except for the one that is currently in view. But why not simply delete them entirely?

Kind of strange that I hadn't thought of this myself, really!

Experienced C++ programmers may counter this argument by saying that dynamic memory allocation costs performance, so resetting is more efficient. This is probably true in most cases. However, I consider design that prohibits bugs to be a lot more important than performance. Current console hardware is very fast and we are not trying to make the next Killzone or Uncharted here.

Anyway, this could also be implemented using

*placement new*(which constructs objects on a piece of memory that you allocated before, instead of requesting new memory). Finally, we have a really fast custom memory manager at Ronimo, so small allocations (up to 256 bytes) are very fast anyway.

Although I didn't think of this re-creation trick myself, it very much fits the coding style at Ronimo: we always try to find structures that make it as difficult as possible to accidentally introduce bugs. Destroying and re-creating objects instead of resetting and reusing them is a great example of this philosophy! Although this example is no super-complex science, I think that one of the most important skills for any programmer is to constantly look at your own code for these kinds of small improvements.

Another great post! My only comment would be that while porting some code to Windows Phone 7 platform, i learned that the garbage collector isn't your friend. By recreating objects you generate garbage which will be collected when a threshold is reached and cause a mini lag spike in your game. I normally use this in C+, and it's awesome, but in C# on the compact .net framework, it's best to reset everything, and even better, pool objects for reuse as much as possible.

ReplyDeleteIs it possible to do something like placement new in C#? The scheme I described here could still be used if you could call the constructor on an already existing object to overwrite it. Can that be done in C#?

ReplyDeleteI don't think so, i think you're locked down to their memory management. It's a shame because i've grown to love C# more and more, except for some silly things like that.

ReplyDelete( StackOverflow seems to agree: http://stackoverflow.com/questions/1162379/net-placement-new )

Pity! But then again, I guess many of my programming principles don't apply to weaker devices anyway, like the Nintendo DS and mobile phones. PC/Mac/Wii/PS3/360 are fast enough to not care about these things. :)

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteDavid, why not use a memory pool, in this case you have the same effect of the garbage collector not screwing around with you. But its good to finally see this "feature" be gone :) Always the magic reset point -1000,-1000 was it?

ReplyDeleteNield, read the last line of my first post again ;)

ReplyDeletePooling is definitely the way to go in C#. Note that also applies to XNA on the Xbox, sadly also running the compact .net framework.

I think you'd be better off sticking with the reset, rather than delete + reallocate. The solution to making sure you don't overlook anything when you reset is to only have one initialization path. To create a new one, you do new + init. To reset, you do hide + init.

ReplyDeleteI think both methods can be very useful in game development and the decision which method you should use is entirely depended on what kind of game you are making / what kind of game mechanics are in the game and which device you are making the game for!

ReplyDeleteI think that for example particles should be done with the reset method rather than the recreate method. It maybe is a bit more dirty but speed is the thing you want with particles. Your example of the player is a great example for recreating. Still you need to be careful not to delete info you are currently using in the game.

Honestly, it sounds like you've rediscovered RAII (where the resource is the character's in-game assets as opposed to typical resources like memory and sockets).

ReplyDeleteAs far as I know, RAII is about having uninitialised classes that are essentially broken/incomplete until you call an initialise function or something like that. That is not the case here: when resetting or hiding, the character is still always completely valid. The problem is just that it has more states.


ReplyDeleteBut of course, this topic is not about rocket science. It is not like we discovered anything new, I just thought it an interesting observation. :)