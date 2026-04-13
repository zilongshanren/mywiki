---
title: How Squidlit's devs authentically recreated a Game Boy game in 2018
url: https://www.gamedeveloper.com/art/how-i-squidlit-i-s-devs-authentically-recreated-a-game-boy-game-in-2018
author: Game Developer
published: '2018-04-24'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

For those of you who miss the many shades of green, the chirpy sound effects, and the simplistic (yet challenging) gameplay of the Game Boy era, [Squidlit](http://store.steampowered.com/app/799510/Squidlit/) is the answer to your prayers.

A Game Boy-inspired platformer, Squidlit aims to create a nostalgic experience through simulating the limitations of the handheld with their title.

In a recent interview with IndieGames.com, Squidlit devs Alex Barrett and Samantha Davenport talked about the challenges that came with designing a game for the classic system.

What drew you to create an authentic Game Boy experience 15 years after its discontinuation?

Samantha: We are, first and foremost, people who really enjoy playing video games. To that effect, we have a collection of a few hundred games that spans back to the late 1970's. When Alex came up with the idea of creating our own video game, it seemed to make sense that we start, essentially, at the beginning with a console we know well and love. The first console Alex played was the Nintendo DMG Game Boy, so it was a natural choice.

When we looked at other games that sought to capture the nostalgia of a previous console, we always noticed that while capturing the look of a console like the Game Boy, it's hard to find one that goes to the lengths to recreate all the console's limitations as well. We thought to ourselves that if you don't see something you think should be there, make it yourself!

![squidlit_2.jpg squidlit_2.jpg](https://indiegames.com/assets_c/2018/04/squidlit_2-thumb-480x270-26126.jpg?width=646&auto=webp&quality=80&disable=upscale)


What challenges came with recreating the visual and audio style of the Game Boy?

Alex: I think the most challenging aspect of making Squidlit came from things going on in the background of the game. It was important to me that the four sound channels of the Game Boy be accurately represented. I had to make a system where if a sound effect used one of the channels dedicated to the music, the music on that channel would stop playing for the duration of the effect (it's most noticeable when you talk to ooblugs). Also, almost all animations in Squidlit are synced to the beat of the music, so everything is that much cuter. This also took some finagling. Perhaps someone more experienced would have an easier time with stuff like this, but as my very first game it took months to figure out.

How did the limitations of the Game Boy technology affect the game's design?

Alex: One of the more limiting aspects of the Game Boy was it's inability to display more than 10 sprites in a horizontal line. Plip, for example, is made up of two 8 x 16 pixel sprites so the amount of obstacles we could throw in front of her was limited. I didn't want any flickering to happen in Squidlit, so we had to go through every possible location of simultaneous objects on the screen and make sure we didn't exceed this limit. The Game Boy also had an itty bitty 160 x 144 resolution screen, so you can't see very far ahead of you. We put a lot of thought into trying to make the enemies fair in relation to your view.

![squidlit_3.jpg squidlit_3.jpg](https://indiegames.com/assets_c/2018/04/squidlit_3-thumb-480x270-26129.jpg?width=646&auto=webp&quality=80&disable=upscale)


Were the play styles or visual themes dictated by the Game Boy limitations? How so?

Alex: I started doodling squidlits in high-school all over really serious things like math and economics. When I started making a game, I found they translated really well to the Game Boy's limited palette. Kirby's Dreamland was a big inspiration for Squidlit. Masahiro Sakurai, its director, once stated that the original concept for it used only one button. We took this to heart in trying to design a game around the Game Boy's limited methods of input, and we ended up whittling the mechanics down to jumping and attacking using the same button.

What challenges did you face in creating cute characters and vibrant worlds when limited by the Game Boy's visual style?

Samantha: When creating the world for Squidlit, we wouldn't think about the technology at first. We would first talk about what the characters are like, what their world should be like, and what they would do. Skwit Skwot, God Emperor, does indeed have a reason for why she is creating this possibly dangerous magic, while Plip truly believes she must stop Skwit Skwot. The biggest challenge in this method was taking these grand ideas and finding ways to implement them into a GameBoy recreation. I think we managed quite well, as we ended up not having to sacrifice any of our major ideas.

If there was anything specific I had to point out, however, it's the word limitation on how much each character could say before it felt overly tedious. It seems like some of the characters are saying a whole lot at certain points, but what they're saying is very carefully condensed lore on what's truly going on. That being said, Squidlit is a test run and prologue to our next title, Super Squidlit.

![squidlit_4.jpg squidlit_4.jpg](https://indiegames.com/assets_c/2018/04/squidlit_4-thumb-480x270-26132.jpg?width=646&auto=webp&quality=80&disable=upscale)


How do you make your game feel fresh to modern players when working with a purposely-limiting older visual/audio style?

Samantha: In making a Game Boy recreation game, one thing we noticed was that a lot of platformer titles for the console didn't really incorporate story too heavily. We decided that putting in an over-arching plot with hints as to motivations for both sides of the story would draw in more modern players with aspects of storytelling they are more familiar with. We also made sure to sprinkle in a hearty dose of Squidlit-y love and comedy in there to make things lighthearted and squishy!

Were there any rules of Game Boy development that you didn't follow? Would this fit on an actual Game Boy cartridge?

Alex: To my knowledge, Squidlit doesn't do anything that a Game Boy can't. On that note, if anyone finds it doing something it's not supposed to be able to, let us know and we'll put out a patch! One could probably squeeze Squidlit onto a Game Boy cart from later in the console's lifetime, and that was a deciding factor for the length of the game. We would probably have to pull some shenanigans to get some of the more fluid animations to play, much like Donkey Kong Land did. We capped the game at 30 FPS, even though the Game Boy can run at a full 60, to accommodate for some of the more complex things it does.

This article was [originally published](http://indiegames.com/2018/04/squidlit_developers_talk_about.html) on Gamasutra sister site indiegames.com.