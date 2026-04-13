---
title: Using key poses to prototype character animations
url: http://joostdevblog.blogspot.com/2015/07/using-key-poses-to-prototype-character.html
author: Joost van Dongen
published: '2015-07-25'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is why our artists first draw key animation poses and throw those into the game as quickly as possible. During early development of a new character for

[Awesomenauts](http://www.awesomenauts.com)we playtest with just those key poses, without any animation. Less than 10 frames represent the entire movement set of the character. One frame for a jump, one for a fall, a couple for a walk, one for each attack, for sliding to a halt and for idling, and that's roughly it.

It's surprising how smooth and awesome a character can already feel with just one still frame per action. Doing this also has another benefit: the game design feels much more solid if a character isn't a box and doesn't look like some other character you already have in the game.

Of course, the phase after this is to create the actual animations. A finished character in Awesomenauts consists of hundreds of animation frames. But today I'd like to focus on the prototyping and concepting before the real animations are made.

Most of the characters we added to Awesomenauts during the past two years were animated by

[Ronimo](http://www.ronimo-games.com)artist Tim Scheel. Tim is a master at drawing dynamic poses and experiments a lot with the animations.

To show how this works I have dug into our archives and made a video of how Scoop, Nibbs and Rocco moved before they got any real animation. I think it's pretty amazing how powerful these already look!

Early animations of characters in Awesomenauts, using key poses only. |

A nice thing to notice in this video is that Tim adds some quick in-engine squash-and-stretch effects to make it look a little bit more dynamic. This is especially noticeable in Nibbs' idle and attack frames.

Before Tim puts anything in the game he first makes animation concept art. This is just a sheet with a lot of sketches of what the various animations might look like. Here are the sketches Tim made for Rocco:

![](../../assets/a8d6dd0ef74c8779.jpg)


![](../../assets/a8d6dd0ef74c8779.jpg)

*Click for high resolution*In Rocco's first gameplay design he couldn't move while doing special attacks. This allowed Tim to draw some really cool attack poses, as you can see in the sheet above. Later the game design changed and Rocco wasn't forced to stand still during attacks any more. This means Rocco needs to do his normal movement animations while doing a special attack, so the attacks changed from character animation to purely special effects.

A particular challenge when designing a character is the amount of detail. Awesomenauts has a strong cartoony style in which microscopic details don't really fit, especially since characters aren't that big on the screen. This means details that were in the concept art are often removed when the in-game version of a character is created. You can already see this happening in the concept art above: some shots have two little straps in the part around the neck, while others only have one of those, reducing the amount of detail a bit.

Rocco's scars were also a challenge: initially he had a scar on his nose but this turned out too small. The scar around his eyes was kept after making it a lot bigger to be more legible. The headphones had to go for a different reason: they had too little to do with Rocco's backstory and personality.

Another example of removing details can be seen below in Nibbs' animation concept art. Tn the bottom right you can see Nibbs' tongue hanging out while running. This is a little detail that I absolutely love: it makes Nibbs look so much more like an overly enthusiastic puppy dragon. However, it turned out to be too small and illegible in the actual game, so it was removed. How much detail there is, is an important part of any visual style, so this needs to be kept somewhat similar in all characters.

![](../../assets/1c6303a73ec92f1f.jpg)


![](../../assets/1c6303a73ec92f1f.jpg)

*Click for high resolution*Another great example of animation influencing a character's visual design can be found in

[Ori And The Blind Forest](https://www.youtube.com/watch?v=VrbGwU5Zx4M), one of my favourite games of recent years. In a presentation at GDC animator James Benson mentions that Ori has a tale because it helped him show the direction of movement better. It's interesting to hear that a crucial element like a tail is there mostly because of the animation, not because of anything else. Be sure to check out

[this video of his highly interesting presentation](http://www.gamasutra.com/view/news/246372/Video_Deconstructing_the_animation_of_Ori_and_the_Blind_Forest.php)!

Back to Awesomenauts! Because Scoop doesn't have legs, his walk cycle was a challenge. As you can see in the concept art below Tim drew a lot of poses for the walk cycle to try different things and find something that works.

![](../../assets/f16e31450c83a9e5.jpg)


![](../../assets/f16e31450c83a9e5.jpg)

*Click for high resolution*When drawing game art one must never forget the goal of the art: to be used in an actual game. The requirements of the gameplay need to be kept in mind. In Awesomenauts this means that melee attacks allow for much more freedom than ranged attacks. Melee attacks are generally just an animation that plays, so Tim go do whatever he wants to make it look awesome. Ranged attacks however need to be aimed at the cursor, which means that the gun-arm needs to be able to rotate freely even during the attack. Not being able to animate the gun-arm is a huge limitation to the animations. Such gameplay limitations are important to keep in mind and this is why Tim enjoys animating melee attacks more than ranged attacks: more freedom!

(For those interested, in 2012 I wrote two blogposts about

[making 2D characters aim in all directions](http://joostdevblog.blogspot.nl/2012/08/making-2d-characters-aim-in-all.html)and about

[shooting animations in Awesomenauts](http://joostdevblog.blogspot.nl/2012/09/shooting-animations-in-awesomenauts.html).)

A couple of years ago I hadn't realised that animations need prototyping and playtesting just as much as any other part of a game. The video at the start of this post gives a great example of this. I hope you enjoyed seeing Tim's animation concepting as much as I did!

Thanks, Joost! As an illustrator myself I loved this post.

ReplyDeletehttps://www.youtube.com/watch?v=OYjv8ogsEGE


ReplyDeleteThough your whole blog is my reflection of this video, this post in particular tickles my fancy.

I expect nothing less of this in the art book, with the commentary too of corse.

What the hell did I just watch...


Delete;)

this is creative!

ReplyDelete