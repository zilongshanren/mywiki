---
title: Simonschreibt.
url: https://simonschreibt.de/gat/gat-doom-3-hdui/
author: Simon
published: '2013-05-09'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

[Doom 3](http://www.idsoftware.com/games/doom/doom3) was awesome but i only saw the first 10 minutes of the game since it scared me. Luckily all what i needed for [the last](http://simonschreibt.blogspot.de/2013/05/doom-3-volumetric-glow.html) and this article can be found in these first 10 minutes, before the first monster appears.

This screen shot shows what i want to point at this time:

Older games often had to reduce the texture resolution to match the hardware limits. The quality of the “Information” label is what you would expect from older games but look at the lower part of the screen shot: This text is sharp like a razor blade!

I was always impressed by the sharpness of their UI on displays and monitors and thought that it was maybe done via real fonts and vector shapes.

Surprise! I was wrong. Long story short: The game doesn’t use *one* texture for the whole UI element. Instead [there’s a script language](https://www.iddevnet.com/doom3/guis.html) like HTML (but more powerful!) where one panel consists of smaller elements. The content is stored in several textures. Most of the elements are placed manually but the text-quads are created by the engine (you just enter some text).

![](../../assets/e5b24d10c8dc1511.gif)


…and of course, all this can be interactive which is another awesome feature of the Doom 3 GUI. You can actually “played” this turkey game by pointing & clicking at the monitor – it’s not just an animation!

Thanks for reading! Feel free to contact me and if you know a mod which deletes all monsters in Doom 3, i would love to “play” it and just enjoy the graphics. :)

**Links**:

[Some crazy guys ported the original Doom on the UI of Doom 3](http://www.battleteam.net/tech/fis/index.html) (Thx to Felix Jones)

Your blog is more interesting than 90% of the tech blogs out there. Keep it up!

Thanks man! Warms my heart :)

Yup, this blog is pure gold!

This comment has been removed by the author.

Ahhhww cool! I always was fond of the awesome sharp UI in Doom3! Some developers went Flash for stuff like that. And STILL its not always crisp.

Didn’t know id created an own type of language for all that ^^ incredible!!

Thanks for investigating!

Glad you also noticed the UI quality :) Not many people seem to see how much awesomeness is in some game assets :D Bu

The interactivity of the terminals is huge.

As an example, this mod loads up Doom classic WADs and plays the in game, so it’s Doom Classic in Doom 3!

http://www.battleteam.net/tech/fis/index.html

This is sick :) Thank you very much for the link!

Hi Simon. There is a fix you should make at the “there’s a script language” link. The exact url is:

https://www.iddevnet.com/doom3/guis.html

Perfect, thank you! I’ve updated the link :)