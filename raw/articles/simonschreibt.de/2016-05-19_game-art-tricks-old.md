---
title: Game Art Tricks OLD
url: https://simonschreibt.de/game-art-tricks-old/
published: '2016-05-19'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

All **G**ame **A**rt **T**ricks on one page! Feel free to visit the related [Polycount Thread](http://www.polycount.com/forum/showthread.php?p=1759176#post1759176) or use [RSS](http://www.simonschreibt.de/?cat=2&feed=rss2).

The cookie settings on this website are set to "allow cookies" to give you the best browsing experience possible. If you continue to use this website without changing your cookie settings or you click "Accept" below then you are consenting to this.

Thank you for extracting all of this useful info!

As skilled as you are in finding things out. Could you do a breakdown of how this is done?

(Uncharted 4: A Thief’s End™ flame torch fx study):

https://www.youtube.com/watch?v=zBGVTfSR2Co

Wow…this looks really stunning! I wished UC4 would be on PC so we could investigate how it’s done.

Looks like at least 2 camera facing sprite animations recorded from real fire, lined up on top of each other, one at the lower end with some wrap distortion possibly. Then the direction of the top flame is controlled by the characters movement and a distortion texture ramped way up here to give the impression of motion with some particle fx triggered above a certain speed?

Ramblings of a mad tech artist. :P Hope it gives some insight.

VFX artist here, pretty much on point there, though it’s not a sprite animation for the flames enveloping the top of the torch, it’s a model with some distortion and fresnel shader trickery. The top flame is a 2D sprite NOT recorded from real fire, but rather a fluid sim, which seems to have a fast and slow variant. When it’s not moving the flame looks a lot calmer and when he’s moving a little it looks a bit more violent. And when the torch is moving fast enough it starts spawning little animated flame particles.

I’m curious if they do anything to prevent seeing the flatness of the particle if you’re looking at the torch from above. In Tomb Raider, which uses a similar 2D sprite for the flame, but if you look at it from above they transition to spawning particles to hide the effect.

Ahh cool, interesting insight there. Cheers. Curious why they’d go for having two variants though, rather than a distortion texture and some shader magic.

Great job on finding all those tricks! Thanks for it.

Do you think you could look into how Prototype does it’s “hand to tentacle-ish weapon” morphing?

Thank you! :) Hm .. I thought Prototype is bound to consoles, isn’t it? Really hard to look into console stuff … especially since I don’t own any :,(

Concerning Deus Ex: it often seems to use both a grand defining texture and a detail texture map, and it just looks especially funky on the screens. It’s one of the few games that I’ve noticed utilising them, but that may be me. I suppose the game doesn’t quite have the texture resolution to keep the effect from being a bit jarring, but it’s still cool that you’ve got sharp texels even when standing right in front of something.

i dont know if this is something you can test, but I’ve always been perplexed by whatever method they use to create their “motion blur” effect in jet set radio future, considering it only affects the player model and seems to affect geometry rather than being a post-processing effect or a particle effect

https://www.youtube.com/watch?v=zgtHdRGRqfk

youll see it a lot during higher-speed segments especially when grinding on rails or jumping off them, here’s a few screensots of the effect i grabbed

https://puu.sh/xnoKi/e2cbf171e4.png

https://puu.sh/xnoVU/37e6e3ca1b.png

https://puu.sh/xnp3r/efff160222.png

http://puu.sh/xnpbh/e6d319a194.png

I’d love to see an explanation on how they accomplished this

Wow, that’s very cool! i love it! i put it on my list with notes … this definitelly deservers more investigation! :)

there is a cool rounded edge shader in lumion 8

https://www.youtube.com/watch?v=uAmf2GujGTA&feature=youtu.be&t=21m7s

and a paper on this topic

http://on-demand.gputechconf.com/gtc/2012/presentations/S0611-Edge-Aware-Shaders-for-RT-Computer-Graphics.pdf

i would love to here your thoughts on this and maybe how to approach this in unity

Wow, this is awesome! Just shared it on Twitter, thank you for the hint!

I just watched your RIME talk! You’re fantastic, thank you so much for contributing to the community!

Thank you :)

Hey, interessanter Blog! Ist der Blog noch aktiv?

Ja :) Allerdings nimmt das Schreiben der Artikel und das Aufnehme der Videos extrem viel Zeit ein. Derzeit komme ich kaum dazu neuen Content zu erstellen, aber es geht auf jeden Fall weiter. :)

I really enjoy these articles Simon!!

Thank you! ^^

I would love to have a breakdown on the making of a League Of Legends map. Is it vertex painted or is the entire map hand painted??

You can try it out yourself by searching the league tech blog (https://technology.riotgames.com/) and maybe you’re lucky and they explained it. If not, you could check the game out by using Intel GPA and investigating drawcall by drawcall.

would you be so kind as to add a search bar to your site?

Hi, thanks for the suggestion! I think I had one in the past… right now I usually click “Game Art Tricks” and use Ctrl+F for searching but it would of course be better to have a proper search field.

Hey Simon,

I was wondering, do you have any idea how RiME tree shaders where made, how did they made the canopee so smooth ?

I know how to edit vertex normals etc, but even with custom normals and things like lerping vectors with a two sided node my trees dont look as smooth.

The main problem is that my leaf cards still cast shadows on themselves and others and that breaks the “volumetric” look.

The only ways i have found to fix this are not suitable :

– Changing directionnal light bias to 2 or 3 which does give a nice look to the trees but break every other shadows

– Disabling ‘cast shadows’ on the tree but it wont cast shadow to the ground either.

Thanks in advance !

I tried to have a look at the data but unreal would only crash all the time :( I’m not certain but I have two thoughts: Maybe the Enlighten-System we used helped to let the self-shadowing appear less harsh or we used a “two sided foilage”-material which helped to do the same. I’m sorry but I did not make the material nor the trees so that I can’t help you further.

Thanks Simon, i do use a two sided foliage material ! anyway i will keep looking around if i find something i’ll let you know !

hey,

just found this because the gta fountain video, and i must say, really cool explanations!

could you do a breakdown on portal 2’s broken glass effect? i’m wondering how to recreate it since i’d first seen it.

it’s visible here, a little bit: https://youtu.be/_bhfSRVbYgQ?t=97

but it can be found many places in the game.

Genshin İmpact looks Really cool with all its shaders. Could you do breakdown for on water and sky, grass :D they all looks good.

I agree, it’s looks cool – very much like Zelda. Unfortunately I don’t have time for breakdowns right now :( Maybe you can try and do one by your own?