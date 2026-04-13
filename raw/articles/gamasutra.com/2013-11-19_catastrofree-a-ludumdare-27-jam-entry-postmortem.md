---
title: CatAstroFree, A LudumDare 27 Jam Entry - Postmortem
url: https://www.gamedeveloper.com/audio/catastrofree-a-ludumdare-27-jam-entry---postmortem
author: Game Developer
published: '2013-11-19'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# CatAstroFree, A LudumDare 27 Jam Entry - Postmortem

CatAstroFree, a collaborated jam project I did with 3 other game developers in remote sense for LudumDare 27 - Combo Entry. I reflected what we've done and summarized for what went right and wrong at the end.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

LudumDare 27 has passed long time ago, back in August 23 - 26. I've collaborated with fellows both from my own country, Thailand, and Singapore. Totally 4 of them for more or less specific roles to craft out the game at the end.

It was a nice time and a brave decision to collaborate with others especially one of them is in another country, but all in all we work in remote sense.

This postmortem will go back in time collecting all notable pieces from [Basement Dojo Blog](http://basementdojo.tumblr.com), a blog at which we were updating things during the jam, and also add up with other detail.


## Beginning

As usual it all began with the talk with [@suebphatt](https://twitter.com/suebphatt). I always do collaborated things with him, mostly. Previous jamming games I did with him are [CLD1](http://basementdojo.tumblr.com/post/57352858349/cld1-was-a-game-we-made-for-charity-game-jam), [Trois](http://basementdojo.tumblr.com/post/57353535406/a-ld25-title-which-was-archived-here-we-really), and [Eloong](http://basementdojo.tumblr.com/post/57405428030/haxpor-postmortem-of-developing-eloong-a-game). We work under the name of [Basement Dojo](http://basementdojo.tumblr.com/), it's just a gathering team name for instance.

This time I would love to make it a little more special by inviting some more fellows who has specific skill to help out the game, but with an implicit intention to collaborate and make a good friendship in indie sense.

They are as follows

[Suebphatt Leelertphong](https://twitter.com/suebphatt), 2d/3d artist (really hybrid and all around crafting-skill)

I’ve been done doing several game jams, client projects, and misc stuff with this guy since around 1 year ago up until now. We knew each other by instinct, and we will do it again in this time.[Sirawat Pitaksarit](https://twitter.com/5argon), sfx/music composer

He’s a sound composer guy at[Extend Interactive Studio](http://x10interactive.com/). He will take care of sfx/music for the game. He’s my junior friend and we know each other though the local community and from a good relationship I have with the studio as from time to time I have a chance to work with them for interesting projects, that things leads us to know each other.

[Bruce Chia](https://twitter.com/blufiro), monkey coder

He’s a co-founder of[Ludochip](https://www.facebook.com/Ludochip)with a steam released game called[Cubetractor](http://store.steampowered.com/app/235720/). In fact, this game is a winner in IGF China 2012. He’s a nice guy I firstly met in[Network Game Asia 2013](http://store.steampowered.com/app/235720/)hosted in Singapore back in May.

We’ve talked and decided that he will fill the gap in our game ie. UI, sound support, routing things together while leaving me to do things on the game logic as he might not be around for a day. So this makes sense.Jeremy Goh and

[Guo Yuan](https://twitter.com/gy_gwen), sfx/music - all around about sound!

They are good folks I met in the same way I met Bruce above. They’re co-founder of[IMBA Interactive](https://www.facebook.com/IMBAinteractive)which is based in Singapore. They did so many projects that involves sound and creative design in sound system, and involved with Singapore-based community a lot. Several project that they have contributed to went to well-known recognition ie. IGF. It’s good to have them to top up our game soundtracks, who knows it could be more! Their latest game they involved contributing sound is[Once Upon Light](http://www.youtube.com/watch?v=ZchVJG9cN7U).

Me - main monkey coder and facilitator


You know me.

It turned out at the end that colleagues in no.4 cannot make it to really participate as they had tight schedule already. So it's 4 of us.

To be said, Suebphatt is a hybrid guy who can do multiple or mostly anything. It can range from art stuff, music / sfx, to coding. So every time we collaborated, I took care of coding and let art stuff or (if needed) other minor coding things for him. Anyway, for this time, a hidden agenda deep inside my head was that we will be using Unity to make game.

It was safe to say that this was the first major chance I ever use Unity to make a game. I learned through some of Unity tutorials before I jumped start with this jam project. Personally, and honestly, the best way to learn a game framework or any related things in game sense is to learn them from making a real project, yeah, making a game.

So everyone was invited and knew ahead of time what to expect as I also created a private group on Facebook for ease of initial talk. We set for the first meeting on Skype to be exactly the time of the jam start, the time when a theme was announced. We're about to make something in 72 hours from now on ...


## Gathering up

As we got a private FB group already, I began to spread my personal inspiration with a hope that at the end we might do something similar or at least be able to reflect something out of it in addition to the fresh theme announced when the time comes.

Here are the inspirational thingies

As usual, LudumDare has bunch of themes to cast a vote on as all participants suggested them prior to the time we all will begin.

The following was the themes, one of them will be selected.

![image image](../../assets/b3227bb43f2c8d59.png)


By all means, 10 seconds was selected.


## Let's get started

We hooked up brainstorming session via Skype talk in the early morning as we knew the theme at that time.

![image image](../../assets/9674d4ed9edf46b9.png)


We started the collaboration call on 8:00 AM TH time (9:00 AM in SG) and by 11:15 we finally nailed down the concept to be [Nine Lives - Cat](http://en.wikipedia.org/wiki/Nine_Lives). The initial solid reason we thought about this was that 9-life is near 10 seconds (the theme), thus led us to this kind of topic.

During the talk, we have shared ideas and discuss on the possibilities of interesting game idea might be continued working on. The following is the links we gathered through.

[http://unity3d.com/gallery/made-with-unity/profiles/flippfly-race-the-sun](http://unity3d.com/gallery/made-with-unity/profiles/flippfly-race-the-sun)[http://flippfly.com/racethesun/](http://flippfly.com/racethesun/)

Race the sun, another good reference with interesting concept on level generator and similar gameplay to our idea.

We will inject the perspective through the cat as it’s falling down from the very virtual high places. In fact, the cat will fall down starting from the real physical world then go through the obstacles that allow our chance to use ghost trick to activate and clear the path letting a cat to progress through the level. Each gameplay will last long for only 10 seconds but by using ghost trick, we can slow down the pace of time a little bit more to peacefully act upon the obstacles ahead.


![image image](../../assets/8a73393d73a4edc2.jpg)


As the cat falls down each chunk of sub-world, it will go through transitioning into another chunk. We planned to have 10 chunks with different level set up and obstacles. Finally if a cat can touch the lowest ground in the lowest chunk, then it will go back to life (in real world) thus the name Nine Lives comes to play. We believe we take 10 seconds to work with the game idea in a creative way although there’s room for us to further think about it.

It's time for lunch so we decided to take it easy and refresh ourselves up, we will then get back and talk more about the plan in implementation along with the very first concept draft design from Suebphatt.

We use Trello, Google Docs, and Skype to communicate within the team but from time to time we hit each other through Twitter. I decided to let everything goes into public domain, let others not only our team but people in Internet know what we're up to. It serves a good purpose to pump us up, and keep the pace going. Check out our public [Trello - LD27](https://trello.com/b/5vHCZapm/ld27) board if you want.

I will write into parts covering what the team has done in terms of art, music, and code. Then at the end I will summarize for what went wrong and what went right for overall development of this game.


## Art

![image image](../../assets/c2f5089a73b3ea7d.jpg)


A main character Suebphatt designed.


![image image](../../assets/489a9b883f10bbfa.jpg)


Obstacles designed for level 1. Simply lots of weird stuff.


![image image](../../assets/130c92020d181d31.png)


![image image](../../assets/867dbee554c01089.png)


![image image](../../assets/228967c2940a7dfb.png)


![image image](../../assets/afb18fc11395c68d.png)


A cat :)


![image image](../../assets/8060c179835a732e.png)


![image image](../../assets/fa47bc94234719cb.png)


![image image](../../assets/5fb978e62b79f93d.png)


![image image](../../assets/ba3b18108386d34a.png)


Some of obstacles he modeled and textured. My most favorite one is Bieber Fan.


## Music

Sirawat did all the music for all levels. He edited all musics and fired into one shot here. He also took care of all the effect in the game especially and notably the cat's voice. The high praise for the game's humorous part comes from his hand.

Not to mention about one of the level as he injected his own voice as a level theme music. If you play the game, you will see it in level 3 (Bieber Fan level).


## Code

Bruce and I have talked and agreed to split the coding works to let UI, sound & effect programming to Bruce, then gameplay to me. Also as Bruce won't be available to work with the team for full 3 days, thus it's safe to let the core work to me.

After Bruce laid down the git project for the team, then he was firstly working on mainmenu UI as he will have a chance to test particle effect out along with UI stuff.

![image image](../../assets/fb63c8341f09852d.jpg)


For more detail about this part, read his update [here](http://basementdojo.tumblr.com/post/59184315883/blufiro-done-up-the-title-screen-and-chose-a).

Back to core gameplay. I was trying to create a free falling cat which was represented by a cylinder. The floor was simply represented by a plane.

![image image](../../assets/54f6f8b200ddda1a.png)


![image image](../../assets/cafd7386082d83d2.png)


We communicated back and forth via Skype chat. During that time Bruce finished creating a spawning system.

![image image](../../assets/3400b8b081ddc6ed.png)


![image image](../../assets/1c2d25b8e689f9aa.png)


Above was what after I integrated spawning system from Bruce and the free falling mechanics. Things went well. When the cat dropped down and finally touched the floor, the floor was changed into red for debugging purpose.

Read more detail update for his spawning system via this [post](http://basementdojo.tumblr.com/post/59205755796/blufiro-obstacle-spawning-groundwork-done-i).

Also the following is the snapshot for our git project. I really love how the graph would form throughout the whole development. It's a sideline eye candy to stare at.

![image image](../../assets/7fa1123908550aeb.png)


Next, Bruce add texture for create meteor's falling down effect, detail [here](http://basementdojo.tumblr.com/post/59259284612/blufiro-meteors-incoming-import-blender-to).

![image image](../../assets/1b665c905ae2b73a.png)


After around 2 day passed, Bruce had to get back to his days, he won't be able to help the team from that point on but it's acceptable as he helped creating important coding stuff and we talked ahead of time that he won't be fully operated for 72 hours. Thus it's only Suebphatt and me. I managed to integrated the spawning system created by Bruce, modified its settings to suit for each level. I went through using and taking benefit of Prefabs, hierarchical structure of objects, hooking up music and effect file to be played in Unity, loading scenes, exporting into various platform-option, making the gameplay fun to play as much as possible and tedious camera controls.

I have to admit that camera control is a hard topic to get it right. It would be great if you understand higher Maths, and how to manipulate things in 3D. It would reduce time and much of effort wasted in trial-and-error approach trying to make right. Not to mention that a little bit of physics thought would add realistic look into cushion of camera. I did't have much time to ponder through all of them, so there're some rough edges in which players saw it and posted comments in the [game entry page](http://www.ludumdare.com/compo/ludum-dare-27/?action=preview&uid=647) on LudumDare official website.

A rough thing I did come out with was using a simple primitive to represent the whole single object used as an obstacle. I can't get it accurate enough to the level of mesh as for some reasons at that time it won't work when I tried to select it with a mouse and dragged it to somewhere. So for an instance when a cat was falling down and colliding with that particular object, things won't be in expected way. Luckily it's not frequent, almost can be treated as skippable things to notice.

Personally I'm the slow pace programmer, thus it was a bit of pressure to get things done in time.

Above Vine video (long before the final version of the game) almost summarized everything the core gameplay should have; spawning system, free falling, ghost trick (slow motion).

At last for what we get ...

![image image](../../assets/2d46966fefbd85da.png)


![image image](../../assets/4509e69ebb7dbbd1.png)


We completed 7 levels from 10 we aimed at the beginning. The nice thing was that we created the system for a single level and reused that system with different setting on obstacles, spawning setting, level texture, and music for another level. Reusable stuff is really helpful that helped us be able to finish the game in time.

Also we got coverage by [JupCraftGaming](http://www.youtube.com/user/JupCraftGaming), head to 6:05.

Finally, here was our score for this LudumDare #27.

![image image](../../assets/71d4ea84a6643597.png)


Let's us now see what went right and what went wrong.

## What went right

All music, core gameplay mechanics (with a little twist), and of course 3D-content based game were there and we're happy!

Collaboration in remote sense especially between different country was positively proved that it worked.

Constant update through tumblr blog for incremental progress from each member helps the team member to see others' progress, and can be served for the purpose as valuable information for blogging later (like this postmortem).

We aimed to make a very humorous game, and we can accomplished that. People played our game and laughed.


(We checked through the comment in our[entry page](http://www.ludumdare.com/compo/ludum-dare-27/?action=preview&uid=647), and our friend telling us via Twitter stream)

Twisting one of gameplay mechanics a bit could help the game to be possible to finish.


Ghost trick feature is one of the thing that initially we thought to embed a puzzle into it in order to let players think a little more before activating. It has changed into simpler approach just to use that feature to avoid the obstacles, yes, use it to drag those objects out of the way one at a time.We really focus on the sound and mood of humor. The score above reflects that. By focusing on a few things, you're better at it. We completely knew ahead of time that this game won't incorporate any innovative thought or implementation, at least in some ways, so we didn't really focus or care that result much.


## What went wrong

The initial inspirational links I've sent to the group and story telling experience I told the group in brainstorming session weren't used at all as they are too high in abstraction and concept to reach. It's too much for the jam.

Two of the members (no.4) weren't be able to participate and contribute as they're still unsure whether they will have time but I invited them anyway. Better is to make sure first.

I thought that with this simple game, a camera control would be as simple as the game itself. But it's not true. Even the simple game, a camera control can become tedious to get it right. I've changed the way camera would act quite 3-4 times but still I didn't quite satisfied with the result.

All of our members included myself were busy during the rating period, thus our coolness score was quite low. If anything else, I wish I could do this part better. It's like a life lesson as it affected the final score. Next time, I would stick to the scheduled plan to rate a few games at a time per day, then throughout the weeks, you will get a bigger accumulated result.


## That's it!

Yeah, literally!

No matter what, we created just another game, a humorous one.

Go play the game: [Web](https://dl.dropboxusercontent.com/u/4019265/Games/ld27/CatAstroFree/CatAstroFree.html)

Grab the source, then modify and adapt on your peril: [Github](https://github.com/haxpor/LD27/)

Listen to nice soundtrack: [Soundcloud](https://soundcloud.com/haxpor/sets/nien-cat-ld27)

--

This is a cross-post to my blog at this [link](http://haxpor.org/post/67452790861/catastrofree-a-ludumdare-27-jam-entry-postmortem). Connect with me via Twitter [@haxpor](https://twitter.com/haxpor).