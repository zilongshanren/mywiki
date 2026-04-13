---
title: Back of Beyond. A look behind the Infinite.
url: https://www.gamedeveloper.com/audio/back-of-beyond-a-look-behind-the-infinite-
author: Matt Bradley
published: '2016-03-24'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Back of Beyond. A look behind the Infinite.

A few weeks back I wrote about the challenging development of Beyond the Infinite (BtI) and how it nearly broke me. This week I want to talk more about what the project actually is and how it’s shaping up.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

This was originally posted on [antitranslate.com](http://antitranslate.com) on Wednesday 23rd March 2016.

A few weeks back [I wrote about](http://www.gamasutra.com/blogs/MattBradley/20160229/266350/Trying_and_failing_From_Industry_to_Indie_and_out_the_other_side.php) the challenging development of Beyond the Infinite (BtI) and how it nearly broke me. This week I want to talk more about what the project actually is and how it's shaping up.

At its core BtI is an anti-gravity racing game in the style of Playstation 1 classics [Wipeout ](https://www.youtube.com/watch?v=KRSVrkzDyuA)or [Rollcage ](https://youtu.be/nF5H5t4ge0E?t=45s)(which incidentally is [getting a reboot](https://www.youtube.com/watch?v=yfPRVRIQ1uM)).

It's inspired by many many hours of playing [Zone Mode in Wipeout HD](https://www.youtube.com/watch?v=IAp3JT1FOBU) as well as fewer hours playing less clearly relatable games like [Super Hexagon](https://www.youtube.com/watch?v=2sz0mI_6tLQ), [Tony Hawk's Pro Skater](https://www.youtube.com/watch?v=ssM60B5Z4EM) and [Rayman Legends](https://www.youtube.com/watch?v=fvHL_U0cQV8). In addition to games, [music videos](https://youtu.be/_dNht9Zr0CE), [art](https://vimeo.com/59142570) [installations](https://vimeo.com/58679460), [gifs](https://uk.pinterest.com/antitranslate/motion-graphics/), [DJ](https://soundcloud.com/methlab-recordings/vaetxh-methlab-mix-2013)[sets](https://soundcloud.com/methlab-recordings/vaetxh-methlab-mix-2013), and [sacred geometry](http://themindunleashed.org/wp-content/uploads/2015/08/phii.jpg) have all had their influence.

Given the project is named after [2001:A Space Odyssey](http://www.imdb.com/title/tt0062622/)'s fourth act, the film is clearly significant too. Not just for the incredible visual impact of [those concluding moments](https://youtu.be/ou6JNQwPWE0), but also for the subtlety of craft and patience to deliver it's story throughout. It's never overly explicit in it's intentions, which creates space for the audience to fill with their own imagination. I don't really get why games don't take this approach more often. Ambiguity can disguise many flaws, yet games are so eager to force heaps of exposition on the player

![](../../assets/b6d6c329a4103ea7.jpg)


While BtI doesn't really have a traditional narrative the aim is to provide a framework in which a story could be derived if the audience should want it. To achieve this I plan to use theming and visual presentation, or ‘environmental storytelling’ to give context without being specific. As an extension of this I'm keen to avoid adding any kind of dialogue spoken or written, and that includes the user interface. Whether this is practically possible or not is still up in the air..!

The central racing mechanic is supported by a host of other designs that reflect the previously mentioned varied influences on the project. Music features heavily and this is represented by three fundamental aspects of the game:

Firstly, a boost mechanic where each boost pad represents a musical element or sample that is played when hit. By design the player is encouraged to activate boost pads else they'll fall behind, in doing this they're creating the game's music as a by-product of competition.


Secondly, the speed at which the player travels is the tempo of the soundtrack. Hitting multiple boost pads in quick succession results in the player speed and soundtrack tempo permanently rising and the challenge increasing. Admittedly this is a mutated version of the Wipeout Zone Mode mechanic in which the player is forced to go faster and faster over time until they reach their limits and eventually explode, but it works great for pacing and ratchets up the tension over the course of a race – even if you're way out in front.


Thirdly, aspects of the soundtrack are represented as obstacles in the environment. This might be a gate that toggles between open and closed on each beat, or using the bassline to time the movement of an object that when touched will destroy the player. I always thought the idea of 'playing’ a music visualiser would be pretty cool and aesthetically stunning – a bit like

[Thumper](https://www.youtube.com/watch?v=uj0pNGvfF_8).

To facilitate these audio-focused mechanics the environment is generated at runtime making the gameplay experience differ slightly each time it's played. Technically it's somewhere between pre-made and procedural. This means the stages are all designed algorithmically using modular building blocks that can be deployed in thousands of different combinations resulting in every play-session having a seemingly unique soundtrack and visualisation. In practice this is tricky to pull off, but one of the few successes of the previous iteration of BtI was it's procedural audio composer. Think of it like a robot DJ that curates the gameplay the same way a DJ might adjust their set based on the crowd's feedback. Sorry, it doesn't take requests.

Having obstacles means there are navigational puzzles too. Given the speed the player is travelling at they're not overly complex, but they do open up further opportunities for interesting gameplay. Players have the ability to leap and spin around the environment, making jumps and dodging obstructions. In BtI's previous incarnation I thought that the player’s movement was the ideal host for audio based mechanics, but after trying out various different approaches based on this idea I’ve come to the conclusion it’s very difficult to move the player in time with the music without taking away agency, so this is my compromise.

I'm now in the process of throwing all these elements together. So far the environment dynamically generates from a toy-box of modular pieces and the player can navigate around these pieces by jumping and rotating. Hitting boost pads in sequence increases the player speed and tempo of the soundtrack, and the basic race format is in. My current task is building bots to race against. I've never designed or created complex ai like this before, but I'm up for the challenge and I already have semi-successful pathfinding in place. Once I have the bot finished up I'm shifting focus to bring everything together so I can release regular playable builds.

There is [so](https://trello.com/b/aJXtFT8m">so)[ much still to do](https://trello.com/b/aJXtFT8m), for now though take a look at the work in progress..!

![](../../assets/ff85d3c44d212e3a.gif)

![](../../assets/011ffc634437a2a4.gif)

![](../../assets/1977696394a0cd79.gif)

[Follow Anti-translate](http://antitranslate.com/connect) to keep up to date with the latest developments.