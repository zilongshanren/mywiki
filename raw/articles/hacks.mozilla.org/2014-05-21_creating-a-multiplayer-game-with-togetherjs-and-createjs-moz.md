---
title: Creating a Multiplayer Game with TogetherJS and CreateJS – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2014/05/creating-a-multiplayer-game-with-togetherjs-and-createjs/
author: Lu Wang
published: '2014-05-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Bubble Hell Duel is a multiplayer HTML5 dogfighting game. The object of the game is to dodge bubbles launched from your opponent while returning fire. This game was written mainly as a prototype for learning and the [source code is available on GitHub](https://github.com/coolwanglu/BubbleHellDuel). You can try the game out in single or multiplayer [here](http://coolwanglu.github.io/BubbleHellDuel/#). Currently the game does not contain any sound effects but uses [CreateJS](http://www.createjs.com/#!/CreateJS) and [TogetherJS](https://togetherjs.com/).

In this post I would like to share some of my experiences when developing the game. Please share your thoughts in the comments if you agree or have other suggestions.

## Game Engines

When developing a 2d game you can write you own engine or make use of some fantastic libraries that are available. After spending a few days looking at the various options available I decided to use CreateJS. As I have some experience with Flash, CreateJS made sense for my needs as there was not much of a learning curve. I also wanted to make use of some Flash animations and CreateJS supported this feature. I will elaborate a bit more on animations later in the article.

As I am a C++ developer I believe [emscripten](https://github.com/kripken/emscripten/wiki) is also a good choice. It allows C/C++ code to be compiled to JavaScript, which can be executed in the browser. I am of the opinion that the static type checking and compile-time optimizations are great assets when developing large code bases. I have used emscripten before and it works very well, but for this project I wanted the fast and convenient prototyping capabilities of JavaScript. I also wanted to expand my JavaScript knowledge.

I’d like to mention a few other libraries that seem very interesting: [Cocos2d-x](http://www.cocos2d-x.org/) is making an emscripten port and they already support [HTML5 binding](http://www.cocos2d-x.org/wiki/Cocos2d-JS). I also like [pixi.js](http://www.pixijs.com/) as it provides a webGL renderer but also supports Canvas fallback when the browser does not support webGL.

## C++ vs JavaScript

At first I was a little bit worried about the performance of JavaScript, and that was the reason my decision between using CreateJS or emscripten was difficult. Fortunately a simple benchmark showed that a naive collision detection algorithm with about 400 balls on screen could still reach 40+ fps, which was enough for my simple experiment.

As someone who has coded more in C++ than JavaScript I loved how quickly I could translate my thoughts into code and test them out on multiple browsers. On the other hand it was not very comfortable debugging my JavaScript. C++ compilers are quite good at pointing out misspellings and other mistakes that cause runtime issues. While the “use strict” directive and other mechanisms like closure compilers have their purpose they were not very helpful to me especially when variables became undefined. Rooting for the cause of errors can be somewhat difficult comparatively.

As an example of difficult debugging, I encountered the following issue. I was using float numbers for coordinates and other geometric values like angles. These values were passed to the other player using the TogetherJS.send method for synchronization:

```
var player = { x: 10.0, y: 10.0 };
TogetherJS.send({type:'sync',x:player.x,y:player.y});
TogetherJS.hub.on('sync', function(msg){
enemy.x = msg.x;
enemy.y = msg.y;
});
```

This worked, but lots of decimals were sent in this way, so I decided to relax the accuracy:

```
TogetherJS.send({type:'sync', x:Math.round(player.x), y:Math.round(player.y) });
```

Then I thought integers might not be accurate enough for collision detection, so I added more digits to the messages:

```
TogetherJS.send({type:'sync', x:player.x.toFixed(2), y:player.y.toFixed(2) });
```

While this seemed a reasonable solution, it actually induced a bug that was very hard to find and I did not notice it until I tested the game after implementing some more features. I noticed while playing the game the opponent would never move.

It took me hours in debugging before I could locate the cause. I do not think I would have made this mistake using C++.

If you would like to see this bug in action take a look at this [jsFiddle](http://jsfiddle.net/coolwanglu/eu8vT/3/) project. Look at the three canvas tag outputs and you will notice the third canvas contains the bug. This issue occurs because [toFixed](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/toFixed) returns a string representation.

I am not sure using a closure compiler would have avoided this issue, but I did find in [another project](https://github.com/coolwanglu/pdf2htmlEX) that it definitely helps with optimizations.

## Animation with Flash

As with most games I wanted to use a good deal of animation. I was very familiar with creating animations in Flash and found that CreateJS supported several ways of consuming the Flash animations and presenting them in HTML5. [CreateJS](http://www.createjs.com/#!/CreateJS) is a set of libraries and tools used to create interactive HTML5 content. So by using CreateJS I could consume my animations as well as use the other libraries available for loop handling, resource management and in the future, sound manipulation. For a quick introduction to CreateJS take a look at this [video](http://www.youtube.com/watch?v=OWHJa0jKJgo).

CreateJS, which Mozilla now sponsors, offers great support for Flash animations.

There are two ways of using Flash animations in HTML5 with CreateJS. The first option is to directly export the Flash animation in a way that you can access all the elements in their original form, including paths, transformations and tweens. The advantage to this approach is that it produces smaller files, and CreateJS allows you to transfer them into a sprite sheet on the client side, for faster rendering. Adobe Flash CS6 offers the CreateJS Toolkit plugin that allows the designer to export all the content of an animation to HTML5 files. This generally results in a JavaScript file with all the graphics and tweens, an HTML file, and a set of image files. You can open up the HTML document in your browser and see the animation.

Another option is to export the animation into a sprite sheet, that is an image containing all the frames with a JavaScript file describing the position and size of each frame. These files can be easily integrated into HTML based games or applications via the [SpriteSheet](http://createjs.com/Docs/EaselJS/classes/SpriteSheet.html) class in CreateJS. This is the approach I used for this game. To see the code where I use the SpriteSheet have a look at this [link](https://github.com/coolwanglu/BubbleHellDuel/blob/master/js/arena.js#L31). If you want some more detail on this approach take a look at this [video](http://www.youtube.com/watch?v=HaJ615V6qLk).

I should also note that you can use a tool called [Zoë](http://www.createjs.com/#!/Zoe) to export directly to a sprite sheet or a JSON file from a Flash Animation as well.

The above image is an example of a sprite sheet that I use in the game and was generated as described above. The original image came from the game *Touhou Hisouten ~ Scarlet Weather Rhapsody*, which is availabe at [http://www.spriters-resource.com](http://www.spriters-resource.com).

## Multiplayer with TogetherJS

On my first iteration of the code the game was not multiplayer. Originally it was a single-player bullet hell game, with a boss foe randomly moving across the screen. I could not last more than 30 seconds before succumbing to withering fire. It was interesting enough that I thought multiplayer would be exciting.

I had heard of Together.js not long after it was released. The jsFiddle project is powered by Together.js and offers an impressive collaboration mode. This led me to using Together.js in my game. It is also very nice that Mozilla offers a default hub server simplifying the process of creating a multiplayer web based game. To learn more about Together.js be sure to check out this [article](https://hacks.mozilla.org/2013/10/introducing-togetherjs/).

It was easy and comfortable integrating Together.js into my game, as it works like other event dispatcher/listeners frameworks.

With Together.js, I was able to implement random match and invitation only multiplayer modes in the game. I did face a few design challenges that I had to overcome when designing the communication protocol.

First off, I did not put code in to prevent cheating with two-party communications and assumed a certain level of trust between players. In the game design currently all collision detection of a player is done locally. Theoretically if you block corresponding messages you can mask that you have taken damage.

Another area that I hacked a bit is that the bubbles of the enemy avatar are generated locally and randomly. This means that the bubbles seen from your character avatar are not necessarily the same as your opponent is seeing.

In practice neither of these shortcuts should ruin the fun of the game.

I did encounter a couple of issues or caveats with Together.JS.

- I did not find a way to disable the cursor updating in Together.js. While this is useful in collaborative tools I did not need it in my game.
- I am using Together.js in an asymmetric way, where both players see themselves as the red skirted Avatar (Reimu). This allows for easier placement of the player at the bottom of the screen and the opponent at the top. This also means that when you move the main player from an opponent’s view of the game your move is seen as the opponents move and vice versa.

## The Fun of Making Mistakes

There are two visual effects in the game that came as unexpected surprises:

- When a round finishes and the message ‘You Win’ or ‘You Lose’ appears, the time is frozen for a few seconds. This acts like a dramatic pause.
- When a charge attack is released, the bullets are fixed and then gradually blown away toward the enemy.

Neither of these effects was designed in this way. I didn’t want the pause and I wanted the bullets to continue rotating around the player upon releasing. However I made mistakes, and the result seemed to be much better than I had planned, so they made the final cut.

## Conclusion and Future Plans

It is always fun learning new things. I like the fact that I could prototype and visualize pretty quickly. In the future I might add more patterns for the bullet curtains, and a few sound effects. In addition I will probably also draw more background images or possibly animate them.

While developing the game I did realize in order to get a natural and intuitive feel required more effort than I expected. This is something I have always taken for granted while playing game.

The code is open source, so feel free to fork and play. Be sure to comment if you have any suggestions for improving the game or the existing code.

## About
[
Lu Wang ](https://wang-lu.com)

A happy hacker behind pdf2htmlEX and scanmem/GameConqueror.

## 16 comments

SimonMay 22nd, 2014 at 02:58Lu WangMay 22nd, 2014 at 04:03LukeMay 22nd, 2014 at 17:51Simon SpeichMay 22nd, 2014 at 23:46Simon SpeichMay 22nd, 2014 at 23:53Lu WangMay 24th, 2014 at 07:28SimonMay 22nd, 2014 at 04:24Lu WangMay 22nd, 2014 at 06:14simonMay 22nd, 2014 at 08:14Lu WangMay 22nd, 2014 at 10:36Simon SpeichMay 22nd, 2014 at 23:44Lu WangMay 22nd, 2014 at 23:49AblarMay 22nd, 2014 at 16:32Lu WangMay 22nd, 2014 at 23:48AblarMay 24th, 2014 at 14:14niksMay 24th, 2014 at 04:01