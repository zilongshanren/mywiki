---
title: 'cocos2d Book, Chapter 14: Game Center'
url: http://www.learn-cocos2d.com/2010/09/cocos2d-book-chapter-14-game-center/
author: Nick says
published: '2010-09-26'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 14 - Game Center

This chapter will revolve all around Apple’s Game Center technology. Especially peer to peer networking is very interesting. The idea is to create a small multiplayer room using the Isometric game built in [Chapter 11](http://www.learn-cocos2d.com/2010/09/cocos2d-book-chapter-12-physics-engines-box2d-chipmunk/).

I actually had to buy a new iPod Touch 4 to be able to test all the new features. I was blissfully unaware that the more exciting features aren’t available on my iPhone 3G. Darn, technology moves so fast.

### Summary of working on Chapter 13 - Pinball Game

I think it’s an amazing game, and I’m happy that several commenters, Twitterers and people I know in real life (you know, those you can actually touch while you’re talking to them) mentioned a pinball game as a possible example. Come to think of it, a pinball game is just great! It’s almost a sandbox that you can add more stuff to it and experiment. And it allowed me to use [VertexHelper](https://github.com/jfahrenkrug/VertexHelper), which I haven’t been able to mention in the previous chapter.

Also, I’m a big pinball fan. Well, I used to be a computer pinball game crack. Have I ever mentioned that I was a beta tester for ![table5](../../../wordpress/wp-content/uploads/table5-156x300.png)


[Balls of Steels](http://www.3drealms.com/balls/index.html), the pinball game from Apogee/3D Realms? When the shareware table was officially released, the highscore I achieved held the #1 spot for roughly 6 months in the worldwide leaderboard. And I basically stopped playing this game session after about 12 consecutive hours, just because I didn’t see the end of it. I always had the extra balls maxed out and I was still on my first ball. I just got bored.

Anyhow, it was great fun to actually build a pinball table myself. I can now appreciate more than ever how complex it is to create these beasts, be it for real or as a computer simulation. My respect to all game developers who ever built a pinball game, most importantly: the developers of the [Pinball Dream](https://en.wikipedia.org/wiki/Pinball_Dreams)s/[Fantasies](https://en.wikipedia.org/wiki/Pinball_Fantasies)/[Illusions](https://en.wikipedia.org/wiki/Pinball_Illusions) series created by [DICE](https://en.wikipedia.org/wiki/EA_Digital_Illusions_CE), the developer of [Epic Pinball](https://en.wikipedia.org/wiki/Epic_Pinball) James Schmalz and of course the creators of the Balls of Steel game [Wildfire Studios](http://www.wildfire.com.au/content/standard.asp?name=Bos).

Of course, when you read this chapter you’ll learn more about the prismatic and revolute joints of [Box2d](http://www.box2d.org/) as well as joint limits and motors, among many other things. I’m also excited to see some of the readers turn this baby into a really good pinball game. I admit, this version, it don’t look too good. But as it is, it’s fully functional and incredibly cool for the short time frame I had to develop it in.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I think the pinball example game is great. This is one of the types of games I would love to tinker with! Thanks for your continued hard work on this book!

Thank you, these are the types of comments I love to hear!![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Whew, you move fast!

When I say your prior blog post requesting input for a physics game, I was going to suggest you continue expanding on the ShootEmUp game. You could add “bullets” that are affected by gravity (e.g. Mortars), show how to use collisions (and collision callbacks), maybe add a canon to the front of the ship to show vertexes, etc.

But, I see now that your true love is pinball!

Keep up the great work!

Thank you!

I liked the way you walked us through refactoring as you developed “ShootEmUp” in chapters 1-8. It was really valuable to see how to create a logically-structured, easy-to-maintain code base.

Can’t wait to see the Pinball game - to see how that structure changes when Box2D is added. e.g. Can you simply add Box2d to your existing entities, inherit from new entities or do you need to completely re-structure your code?

Any idea when you’ll post the source code?

I decided to create a BodyNode class, which is derived from CCNode and contains a box2d body and a CCSprite. It handles allocating and releasing both pointers for you, even if you change body or sprite along the way.

The code will be updated by Apress, I don’t know when.