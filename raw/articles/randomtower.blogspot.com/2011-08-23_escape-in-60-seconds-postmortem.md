---
title: Escape in 60 seconds, postmortem
url: https://randomtower.blogspot.com/2011/08/escape-in-60-seconds-postmortem.html
author: Pubblicato da Marte
published: '2011-08-23'
source_blog: Random tower of games
source_site: https://randomtower.blogspot.com/
category: game programming
fetched: '2026-04-13'
---

[LudumDare21](http://www.ludumdare.com/compo).

You can

[play it here](http://www.kongregate.com/games/Gornova81/escape-in-60-seconds)and

[source code is here](https://github.com/Gornova/EscapeIn60Seconds)(License is: make anything you want with it!) and my ludumDare journal is

[here](http://www.ludumdare.com/compo/author/gornova/).

The story

When I think of Ludum Dare i know that there are 48hours, a good amount of time to make a little, limited-scope game... but I have a life and I want to live it :D

So my time is limited. Knowing this right choice was to find a little game with simple mechanics that match the theme. I've voted Stealth and related themes for all voting round and

[declared](http://www.ludumdare.com/compo/2011/08/19/ld21-im-in-6/)use of

[Flashpunk](http://flashpunk.net),

[punk.ui](https://github.com/RichardMarks/punk.ui)and some sort of lighting.

I've learned from previous Ludum Dare mistake so I was prepared in some sort of crappy-paint graphics made by myself, but I don't care because most rewarding thing in LD is the experience itself, not final product. I love the stream of ideas, posts, tweets and all this energy that spread over internet reaching some cool developer (like notch and kevglass): learn from others is a great and follow their attempts is cool too.

Anyway after reading the chosen theme "Escape", Saturday morning after 2 hours I've found a direction: some sort of rougelike/puzzle game with simple mechanics: player just run, avoid enemies, but if he need fight it and cure with a potion, here my

[first update](http://www.ludumdare.com/compo/2011/08/20/first-update-5/).

Where come from this idea? I don't know. I thought about a flash rougelike before and have some unfinished demo on my hard disk, but with a different mechanics (enemy try to kill you, in this game they simple move randomly choosing a direction), maybe some inspiration come from

[Desktop Dungeon](http://www.desktopdungeons.net/)too.

I would spend some words about Flashpunk: build an anyone-accessible game in 2 hours is amazing and only using as reference

[flashpunk basic tutorial](http://flashpunk.net/tutorials/). With nothing spectacular here: grid movements, few sprites and two new features of flashpunk that I've discovered (I'm not a flashpunk master :P):

- GraphicList: useful to have one image as sprite for player/enemies and one for entity
[health status](https://github.com/Gornova/EscapeIn60Seconds/blob/master/src/Enemy.as#L29)I haven't found a decent way to remove from a GraphicList an image to update health status, so I removed it all and add again[bad coding here](https://github.com/Gornova/EscapeIn60Seconds/blob/master/src/Enemy.as#L106)!

- Entity.moveBy: Flashpunk is incredible for this features. The problem: move entity in a given direction, but stop when collide with a given type (for example Wall). Usually my crappy code was:

Entity ent = collide("wall",x,y);

if (ent==null){

// 32 is my block size

x += 32;

y += 32;

}

[in action here](https://github.com/Gornova/EscapeIn60Seconds/blob/master/src/Enemy.as#L68): it's too easy to use and you can pass a list of types to check collision. If there is a collision, no move,

[here more info](http://flashpunk.net/docs/net/flashpunk/Entity.html#moveBy%28%29).

Adding monsters was easy because I've refactored a bit first 2 hour version of the game adding Enemy class and extending with various monsters (for example

[Spider](https://github.com/Gornova/EscapeIn60Seconds/blob/master/src/Spider.as)). Now I think that could be better have one Enemy class only with a different type/sprite on constructor, than 4 monsters, dammit!

A nice pattern I've learned from flashpunk forum is having a Global class with static methods and variables,

[here's mine](https://github.com/Gornova/EscapeIn60Seconds/blob/master/src/Global.as). Using this little trick your code is more clean and adding "general" stuff in one class help in this kind of compo: adding variables, sound stuff and embedding graphics help in keep other classes. I insist on this topic because in a compo like Ludum Dare get lost on your own code could be a risk you have in mind!

I quit after 6 hours, because after afternoon I went out with my girlfriend and some friends and play minigolf (quite fun, but don't say to anyone).

Second day's morning was dedicated to define levels with

[Ogmo](https://randomtower.blogspot.com/Editor%20http:/ogmoeditor.com/): this editor is perfect for LD because you have to define first your level "template" (.oep file, you can

[find it here](https://github.com/Gornova/EscapeIn60Seconds/blob/master/src/data/levelTemplate.oep)) and then make levels. It's powerful (not so powerful as

[Tiled](http://www.mapeditor.org/)but easy and fast to use. As you can see on oep file, I've decided to have small levels (480x320 is my desired resolution) to force player in a small space and put few enemies moving around with fast-run mechanics in mind. I thought were better to have all entities on screen as object in game, with no ground-layer: everything is 32x32 pixels so it's easier to handle and debug.

Level design was fun because with small resolution what I've to do is:

- add walls,
- add starting point,
- add ends points,
- addenemies

[10 levels](https://github.com/Gornova/EscapeIn60Seconds/tree/master/src/data/levels)made in one hour or so on!

After playing a bit I realize that I need some other game element: first Pit and then glass.

Why this addition? Because I want to force player in certain directions in some levels without using always walls (and use of istant-kill pits is right choice) and glass because I want to force enemies to stay in certain areas to break levels in smaller areas where player can think-run-think fast (Glass can be used as no-monster tile, if you play it). My hope was to find a balance in levels between find the right path, run, avoid monsters, go to save glass and fight occasionally.

After some beta testing of my girlfriend I thought to have found the right balance: 10 levels are enough, 60 seconds too and levels are never hard, you have always to keep in movements!

Another addition was the

[menu](https://github.com/Gornova/EscapeIn60Seconds/blob/master/src/MenuWorld.as)with some instructions (thanks punk.ui!), win/lose conditions, time/move trackings (all into

[GameWorld class](https://github.com/Gornova/EscapeIn60Seconds/blob/master/src/GameWorld.as)) and some sort of ui (all done with

[Gimp](http://www.gimp.org/))

Let's talk about sfx and graphics. After levels design and ui, I spend two hours in the effort to make my graphics better. I've discovered new ways to use Gimp as pixel editor, but for basic sprite design I'm stuck on Paint and this is bad. I need some decent pixel editor for future compos. Anyway, I'm happy with

[wall tile](https://github.com/Gornova/EscapeIn60Seconds/blob/master/src/data/wall.png)with some dirty pixels and shadows :D

Sfx was all matter of beautiful

[as3sfxr](http://www.superflashbros.net/as3sfxr/)just use it and in minutes I've found all sfx I needed! I wasn't sure to have a decent result with music so I simply didn't add it :D

After playing a bit my game and found that is possible to finish it, I thought about distribution. First choice was obviously

[Kongregate](http://www.kongregate.com/)because have a simple api for highscore and this game is perfect for highscore, so put few lines in it and the game was ready: upload process on Kongregate was also simple and fast (they love flash game!) and my game is really lighter (160kb!).. perfect!

In the meanwhile ludumdare

[website go down](http://www.ludumdare.com/compo/2011/08/21/we-made-it-and-we-found-the-bug/)and I just enjoy some random tweets (nice resource for information on other people game progress and ideas!!) .. but for few minutes. So I was one of the first have submitted game :D

What went right

- Uses of Flashpunk: my experience with this library (
[S.H.T.G.H.](http://randomtower.blogspot.com/2011/05/summon-heroes-to-go-home.html),[RandomLD19](http://randomtower.blogspot.com/2010/12/ludum-dare-19-randomld19.html),[Airheat](http://randomtower.blogspot.com/2010/11/airheat-out.html)and[Zombie Employee](http://randomtower.blogspot.com/2010/04/zombie-employee-v05.html)) is enough to have simple games in few hours! Forums and documentation is enough too and I could add more effects and find solutions in no time (and there are some[other flashpunker](http://flashpunk.net/forums/index.php?topic=2840.0)on LD21) - Overall idea: I've found a fun idea in no time, yeah!
- Simple gameplay: instead follow the difficult path of find a new kind of gameplay in 48h I decided
[before compo starts](http://www.ludumdare.com/compo/2011/08/19/ld21-im-in-6/)to have a simple game with simple mechanics and this is the way. Innovate in few hours require all the time and more important more experience in various games - Level design: I could add more gameplay elements, sure, but I love simplicity of this idea.. and power of make levels in minutes, test it, get errors, fix it, go to next levels!

What went wrong

- graphics: I'm not ready for doing anything. I must decide to spend some time on pixel art to make at least one or two decent spites with animations!
- music: I need to put some effort on this too.. lack of music (mutable of cours) ia always a mistake on my games :(
- gameplay: oh yes, I'm happy with this kind of gameplay but some my decisions can't happy everyone. I thought about a stealth device to get unnoticed to monsters or a speed bonus or a better move mechanics, like move from (0,0) to (32,32) using a
[Tween](http://flashpunk.net/docs/net/flashpunk/Tween.htm)l many ideas that need to be explored to keep game fun

Conclusion

I will not win, for sure, but enjoyed the overall experience: like in this game, Ludum Dare is a run against me, my limits and time. If you want to join to this kind of compo, you MUST decide first your scope and tecnology, for sure, but also find a simple way to complete your game. I mean: have time to level design, decide what kind of gameplay is right for your game and all of this no-programming stuff you have to do.

At the next LD22 (maybe with a Platformer? Who knows!)

Thanks for reading!

## No comments:

## Post a Comment