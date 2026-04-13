---
title: 'cocos2d Book, Chapter 13: Physics Game'
url: http://www.learn-cocos2d.com/2010/09/cocos2d-book-chapter-13-physics-game/
author: Daniele Says
published: '2010-09-20'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 13 - Physics Game

After the introduction of the physics engines Box2d and Chipmunk, this chapter will focus on one physics engine in greater depth by making a physics game using Box2d.

What kind of game? If you have an idea real quick let me know, because I haven’t decided yet. I was thinking about a space game with gravity but also a bit like Pinball, or more like a Sandbox game with some optional goals. Or something else entirely. The only caveat is: it has to be do-able in less than a week while also writing the chapter and I should be able to illustrate some details about the physics engine! That’s no mean feat.

### Summary of working on Chapter 12 - Physics Engines

I basically split this chapter in half and gave each of the two physics engines, Box2d and Chipmunk, a good treatment. Initially I started with the templates provided by cocos2d, just to get all the code together and not having to talk about setting up the Xcode project. I quickly realized that the application templates are inadequate, erroneous and outdated, probably because they have barely been maintained as both Box2d and Chipmunk matured. They seriously need a refresher, and I was thinking that maybe I’ll turn the two projects for this chapter into cocos2d application templates for physics engines, replacing the current ones and using my Xcode template project, so that I don’t need to go in and change them every time cocos2d gets an update.

Anyway, both physics engines got their treatment and I built the same project for both. So now you can actually compare them, side-by-side, be it performance or behavior or just plain coding style or number of lines.![2010-09-20_00.26.23](../../../wordpress/wp-content/uploads/2010-09-20_00.26.23-300x156.png)


Unfortunately, there’s a lot to talk about even for just doing the basics. I got both projects to the point of adding more boxes to the world, then adding rudimentary collision detection and a simple joint example with 4 bodies strung together. There wasn’t enough space for more. But I did foresee it which is why I planned in the Physics Game chapter as a follow-up. Let me know real quick if you have an idea for a simple physics game, or send me a link to an existing game on the App Store. Ideally within the next 24 hours.

### My Opinion

I once again realized why some developers may be preferring Chipmunk because it is more “direct” and easier to pickup, as in you just add a new callback method and that’s that. I can see that but it’s very misleading. Chipmunk is making me cry by throwing all those one-letter e, u, i, f, m, p, etc. fields at me, so I’ll have to remember that u is for friction, for example. I’m not a machine! And because you can’t hide private fields in C those are exposed as well, adding to the confusion. I found myself having to look up a lot of things frequently in the Chipmunk manual. The bad thing is, it’s a manual, and not an API reference - but I keep having to use it like it were an API reference by using search a lot. Box2d provided a much cleaner API and both a manual and an API reference, which made it a lot less painful to figure things out, to look things up.

People’s arguments about which physics engine is better often runs along the lines of language, features, performance, memory footprint and what not. But if I have to choose, I’d say both are fairly complete and mature physics engines, so for me the choice is really about API design and documentation. And in that area, Box2d is the clear winner in my book. Of course, I kept a neutral tone writing the book, I don’t want to bias anyone because at the end of the day, the important thing is that you can make a great game with both engines, and not everyone is familiar with C++ and that’s a very daunting language to learn.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

pinball or sandbox looks cool.

I’d like to see a character (could be a simple bouncing ball) that goes through a scrolling world and interacts with different kinds of objects to push the physics engine to its limits. For example, a sticky part where objects don’t bounce much, an ice world with little friction, a world with little black holes that increase gravity when you’re near them etc. This way you could show many different implementations in one little “game”.

I definetely want to have objects that “emit” a gravitational pull. After some experiments I finally decided I should try a barebones pinball game. It has a ball, it has objects that, on contact, give the ball an impulse, you have the moving flippers and rubber bands pushing the ball. You can do all kinds of things with a pinball game, so there will also be an object that attracts the ball (magnet).

Thanks for all the suggestions, that was very helpful!