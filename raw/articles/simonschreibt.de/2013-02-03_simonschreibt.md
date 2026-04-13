---
title: Simonschreibt.
url: https://simonschreibt.de/gat/sacred-2-crystal-reflexion/
author: Simon
published: '2013-02-03'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

The [Sacred 2 Addon “Ice & Blood”](http://sacred2.com/) contains a crystal area which has, in my eyes, pretty nice crystals. Or let’s say, they have very nice reflections. Of course we don’t have any realtime raytracing and also no updating cubemaps. But as you see, there is some reflection going on.

**+++ Attention! Artist tries to explain technical stuff! Attention! +++**

I try to explain, what was explained to me: The trick is, to use the last rendered frame as a reflection source.

1. You would take one pixel which shall get a reflection on. This pixel has a normal (screen space) and you can modify this normal by a factor.

2. You take you last rendered frame and look where the new, modified normal points at.

3. You draw this pixel of the last rendered frame, into the currently rendering frame where the normal “starts”

![](../../assets/675c7f2791e46a9a.jpg)


What i really like is, that even if a NPC is right behind a crystal, it doesn’t look wrong. In that case it looks like a refraction instead of a reflection. Also there is nothing like “only big objects are rendered into the reflection to save performance”.

But of course, this works only for strong “scattering” elements like theses crystals. I think you would notice the wrong perspective of the reflection very fast if this technique would be used for water.

Actually, it kinda does work in special cases, even on a sphere. I used the same approach for a game I’ve been working on with some friends of mine.

Image

Youtube

Ps.: I really like what your doing here :) keep it up!

Thank you for your comment! Oh wow you game looks very interesting. The reflexion looks really great. I want to play this! Where can i do it? :)

You can play it here: http://www.hammer-labs.com/skyarena/ :)

You’ll need a controller though. It can be played with up to 4 players locally and we’re having Online playtests every Saturday. ( the server is just online on a pay by hour basis, and we wouldn’t have enough players and content yet anyway :) )

This is awesome! I want to play it! With others. I love how the environment comes from “below” the horizon. Do you have Skype? I would have some questions.

Glad you like it!

Yep, I got skype :). I’ll write you an email once I get home tonight.

Hi Simon,

First let me say I really appreciate what you do. As a game dev/design newbie, your posts are very inspiring, and your Render hell is really an interesting piece too. I wish there were more learning sources like your site.

As for the matter of my comment here, the “reflexion but not quite reflexion” in this subject reminds me of something that has bugged me for a while. I even recently wrote an article about that, in part inspired by what you’re doing here.

It’s and oldie : Tomb Raider II on Psx.

Most of the blade objects in this version of the game do have a reflexion lookalike, but it can not possibly shaders with regards to the vintage hardware it runs on.

You can if interested read ( in french, sorry ) more about it here, and see some pics and videos :

http://game.arthus.net/?tomb-raider-ii-psx-vs-pc

There also is a thread on the psxdev.net forum, which you can find a link to at the end of the article.

I would very much be interested in your ( or anyone with insight for that matter ) opinion about this.

Anyway, keep it up,

Cheers,

Hi Arthus! Thanks for your comment and it’s great to hear that my stuff helps to learn :) The Tomb Raider Trick looks really like “we just use the last rendered frame” which is awesome. I love tricks like this. I wonder if there was a problem on the playstation with the memory – I mean you have to keep the old frame until the new one is rendered. Maybe they stored it in a smaller format to not have a fullsize framebuffer laying around? Maybe all this is explained in the french text :D