---
title: 'js13kGames: Code golf for game devs – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2016/08/js13kgames-code-golf-for-game-devs/
author: Andrzej Mazur
published: '2016-08-08'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

How much is 13 kB? These days a couple of kilobytes seem like a drop in the ocean. Rewind back to the dawn of video game history, however, and you’ll soon realise that early pioneers had to work with crazy limitations.

The beloved [Atari 2600](https://en.wikipedia.org/wiki/Atari_2600), for example, had a measly 128 bytes of RAM with cartridges supplying an additional 4 kilobytes. As the saying goes: **constraints inspire creativity**. The annual js13kGames competition channels creativity by challenging aspiring game developers to create a game using just 13,312 bytes, zipped.

## A coding competition for HTML5 game developers

[Js13kGames](http://js13kgames.com) is an annual online JavaScript competition for HTML5 game developers that began in 2012. The fun part is the file-size limit, set to 13 kilobytes. Participants have a whole month (August 13th – September 13th) to build a game on the given theme – in 2015, the theme was *Reversed*.

![js13kgames banner](../../assets/57e551a74cbed250.jpg)


Thanks to our friends and sponsors, this competition offers plenty of prizes, includes a panel of expert judges, free t-shirts, and other goodies, shipped worldwide for free. But winning is only one of the benefits of participation. There’s lots to be gained from being a part of the js13kGames community. People help each other if they’re stuck on something, share their tools, workflows, tips, and tricks. Plus, the constraint of a limited time frame helps you finish a game, and trains your skills in the process.

## Last year’s winners

Thirteen kilobytes is not enough even for a low resolution image. The small screenshots on the entries pages are usually bigger than the games themselves! And yet, you may be surprised by what can be achieved in such a small size. Take a look at some of last year’s winners for inspiration:

[Behind Asteroids – The Dark Side](http://js13kgames.com/entries/behind-asteroids-the-dark-side)by Gaëtan Renaudeau[Road Blocks](http://js13kgames.com/entries/road-blocks)by Ash Kyd[RoboFlip](http://js13kgames.com/entries/roboflip)by Eoin McGrath

Wondering how such features are implemented? I’ve interviewed the winners, asking them to share some of their secrets to success. They share tooling and techniques for game development with extreme constraints. And if you’re craving more details: [all games are on GitHub](https://github.com/js13kGames), so you can dig through the source code yourself.

## RoboFlip

![RoboFlip](../../assets/d726b1aee1ab9f80.jpg)


[Eoin McGrath](http://eoinmcg.github.io/) describes some aspects of his workflow for RoboFlip:

*“The final entries can be zipped. Zip compression works much better on a single file than multiple files, so the best thing to do is inline all images, concatenate files, minify your JavaScript and remove any white space. Thanks to task runners like Grunt and Gulp this process can be largely automated. Check out the Gulp file that I used. A simple gulp build command takes care of all the heavy lifting and lets me know how much valuable space I have left.”*


![Gulp build task in action](../../assets/832a2974f6d1e2ca.png)


### Graphics

*“First off, forget about high resolution sprite sheets with lots of animation frames. Simplicity is the key. A lot can be achieved with procedural generation or SVGs. I personally went for a retro-style pixellated look. First, all images were created at tiny resolutions (from about 6×6 pixels) in GIMP. I then encoded them in base64 and used the Canvas API to redraw them at a larger scale.”*

![Scaled up sprites](../../assets/46071748a96a22d7.png)


*“Another handy trick I used was to run all images through a function that replaced non-transparent color values with white.”*

![Damage frame for crate sprite](../../assets/f42447cc9a6de264.png)


*“This proved a cheap and effective way to have damage frames available for all sprites.”*

### Sound

*“A game with no sound effects is like coffee without the caffeine. Obviously, there is no way you can fit a single .mp3 or .ogg file into your game with the given limitations. Thankfully, there is *


[jsfxr](https://github.com/mneubrand/jsfxr), which is a very nice library you can use to create some 8bit styled beeps.

For the musically inclined you can also have a stab at creating a soundtrack

using the [Sonant-X library](https://github.com/nicolas-van/sonant-x-live) – check out [this awesome playable example](http://nicolas-van.github.io/sonant-x-live/#N4Igzg9gdg5gMgUyiAXARgEwGYA05owAiAhgC7GoDaoEYAxmgPoR2moCcetDjAJgmxQAGLvSb9SAVygJUIkNyYAPJADc5onqogAbVGgBsaTUwDuxVQgBmEAE4BbDQvoZmrDptcSn3LwOmyKAAsnowqUOrCodp66AAcGKHmljYOTlAQAJZgCIxWxPy2TmqMZOR0ANb6QvIlYJJg5JnI8WhxeCW2CDoIxDn6cW3GICX2faQIRejsiSBWSnmZOhNT8vN5XQCOTutdkFDEUHSBGACsIXML%2FDrEAJ6MpJn2gQZ469d3pfaCaELtl4wAA6HDYIbYoXAA4FQL6CIx4HQ2ZhiUHg%2BSIiB5BZWLZODGo1CQ%2FHEb4cC745LWOyOFCzQFUYyJRk4ZmsnBM9ksznMkSJXAhZn8nCnHCvADsOHapwAung6FRQC1KGggokROqcBqtZqddqNSq9bqjWgsO1DVrpQBfHCKhlYEXmo2O51O43210ms26q02kBKg06z2B90u7Um%2FWqwNBfUh11h01On22lDK2OhuPBiNqjMxh1ur3qpN%2BhnYHNl9MV8tF%2F1YSt18sNi3W5PKjAFxsd%2BvO6sMtCcE3GLsZzCvNAqztVy1FxRuQT%2FGfeKLOHgSAI%2BFHhSLyGcxdc8SmpGnblyz1Dzk%2BL490PxSGR71yb%2B%2BMXdL3yMA%2FU9JZHJ5AqTfScCMESlKQ5RVOgNQdMB9SNMQzTFMBXQ9H0gRYAYaFQaojBjI0%2F7TLM6xWEsKz6G82K4iggyQQCezQIcxz6KcrwAh89yPM8qAEVc3SfCSggYFxQIgjiYKEmRQkwnxqBBESSIziJaIIkihEUeiymqUpmJSUuFIWFSaRLvSKb6typkcuZXIWWyVlmZZsogPKKYtiaeYuW6rnum5IhecGHkij5PnebGbkBWmLLBfaPYpqFeZBX54XxbmvkJclSVxSl6WZSlLlWtOKIsHCJh8AIe7iP4d6vhuailc%2BugAbMM4fgZwxvgVZ6hJeHXlYE57XmE1WVX1L4JEkemHpxeAZNkuT5IUCFYWUxCVNUtTQQ0TQtEE5wikBWFIb0%2FS0mKGASrt2HjHhfaCURyx4ZCKmiUd1G7Ag%2Bz0T1O3vDxbFPC84msbCqAGGsCzQgSKDMesYPaXEzH4vJGkgPiD3gsMyMUadxKkhBcNIk1R54EZlCGsYgpcmTpOcrglN8uTVP2Y51DFtFnmeUEEoxSy7PZaz%2Fnc5zKoc7z2X8xFfNC%2F5wuCxlIsS1FyrRlz3mnEyiveYraAq0r2sBprqsRsr%2Bs6xrWsBurhvG%2BbLKm2rOs2xg8sDuFpMyc7wYu9TWCk17bsqp7g6%2B67TtBiHpxBV6ofh%2BF7SR9HwYx2H4VirlzbLkwbUoKdC4lYNZW3oEV7KANhe1bEbRZyi%2BMTcurgZztb6dTXxX59Xb6Pug0R1eg8JN1XtKTd%2BM1%2FqsmEgWBK2jzBG0DG0o%2F7ShnHHadowXVMmD3dixGXeJCkAc9Cy0QcRyBIYgkA%2BxJz%2Fd9gPoKcG8SeDkOgyC2k9%2FDKK7zpynkY9aPqY9swsY%2FHYLjTEfdIRE0rJTNkNM6YwMsnA%2BmcoFTM1TJLSWMc2ZMjZlHEKrNMF82wXzXBUsEwhUjOQkh6C47kKITrU0jsg5B1OHzXA6tqYsK5tTJhHD2Fcw5kwvhIcyFBxEdw3BGsyFiJoRQyRMdoyOzCkOZRnYU6%2BhnBnXqecaqrgqiXduLUUQviukVPuV5a7uEzl1QQ5jm5rkGg%2BAahihpdzFLYvuswpo%2Flmnhf4JRFrLQgqtLCU84ItGCYweeh12BCBiaPHCJFu4XEIlvKY10KIsP3pE16dFj6cUVixa%2BF8gZXxuPcbSpxhhQ2EhRe%2B0NsYGFAciHgn81KYhRnif%2BikkZIm0m098Y1PyGSoCo7yiDoHjJZAzFBNZYoeiUTLEmCy0ruRzGomg%2BVLEVxXDnEuuiC5FXbiXYxMxTGDIMg1E8mjrFPn2SUpuRzO5lziBcN8HiB7TV%2FHNWkwx%2FGgSWuBaMNQImhPgrSbaFxOjdAOoEGJcL4mr1QGKU6KTbppJ3hjX4INslvTyfEf4X0ykPF%2Bu1QpRLtLSyhDUx6yTn6SQaYBd%2BLTEbIx%2FqjTS4NMa9OxmgMUTS%2B7DEgROMMVMcAClFeK2mkqcBChlMgpyqDArCuVcoxh2ZRkqtUanf0bZNUarrIwther5ntn1YouZ%2BrjXmnWWnU8lEiqN2zi3XO%2FUIg1RfCXMxoRrlN0dRebqT5HlNw9aNFIQz5BeKHt8lUfjgIBPAmhDCZ1QWbW2nPaFC8IRwoiQky6SbUWJPSY9L2WTD7vX0AJUpnxikoE%2BtxclPKsCCTBq08S9SbEcoRo9fpHSO49PaRkjlFLub9oGWGgy8ghWWpMhyampl%2BTTIVUqF0Sr6yrpVfLFdyyPQGGzOu0Zm6yz7o7JrAOSzEpxnNVa69oYU72VsBAUwiAWhMSEMxJAvAAAKZRJgtFrJaIAAAA%3D).” (You may need to hit “Play Song” to initiate.)

## Road Blocks

*“One of the things I love about the js13kGames competition is the artificial limitation it places on you in terms of what you can achieve,”* writes [Ash Kyd](https://github.com/AshKyd), a game developer from Australia.

*“I find as an indie dev, with more open-ended projects it’s possible to get bogged down by all the possibilities and end up with nothing to show at the end, whereas setting some hard limits makes you more creative in terms of what you can accomplish.”*

![Road Blocks](../../assets/294aba7e12dc455e.jpg)


*“Thanks to the filesize limitation, Road Blocks is a fundamentally simple game and didn’t require a massive amount of coding work. As a result, a lot of my time was spent polishing the gameplay and smoothing rough edges during the competition, which resulted in a higher quality product at the end of the month.”*

## Behind Asteroids – The Dark Side

*“Js13kGames is a great opportunity to discover and experiment with cool technologies like WebGL or Web Audio — and improve your skills. With a 13 kB limit, you can’t afford to hide behind a framework. Also, obviously, you shouldn’t use images but try to procedurally generate them. That said, it’s up to you to find your style and use the tricks that suit you. Don’t fall into doing all the tricks right away – prototype first and compress your code at the very end,”* advises veteran game developer and js13kGames winner [Gaëtan Renaudeau](https://github.com/gre).

![Behind Asteroids](../../assets/76a28711512594ea.jpg)


*“One of the interesting tricks I’ve found to save bytes is to avoid object-oriented style. Instead, I just write functions and use Arrays as tuple data type – I’ve used this technique in the past for a previous js1k entry.*

*This is the third year I’ve participated in the js13kGames competition and the third time I’ve had fun with WebGL. My 2015 submission is a remake of Asteroids where you don’t actually control the spaceship but you instead send the asteroids. This is my take on the Reversed theme.*

*On desktop, the game is implemented by typing – a letter is displayed on each asteroid and you have to type it at the right moment. On mobile, it simply turns into a touch-enabled game.*

*The game is paced with different levels from beginners to more experienced players who control the spaceship which you must destroy with the asteroids. The spaceship controls are driven by an AI algorithm.”*

### How the game is rendered

*“The game uses hybrid rendering techniques: it is first rendered on Canvas using basic 2D shapes and is then piped into multiple WebGL post-processing effects.*

The 2D Canvas drawing involves circles for particles and bullets, polygons for asteroids and spaceships, and lines for the procedural font as [the path of each letter is hardcoded](https://github.com/gre/behind-asteroids/blob/master/src/lib/asteroids.font.js). Game shapes are drawn exclusively with one of the 3 color channels (red, blue and green) to split objects into different groups that the post-processing can filter – for instance, bullets are drawn in blue so we can apply specific glare effects for them. This is an interesting technique to optimize and store different things into a single texture as the game is in monochrome.

*The different effects involved in the WebGL post-processing are detailed in this post-mortem. The important goal of this final step is to graphically reproduce the great vector graphics of the original arcade machine.*

*A background environment map where you see a player reflecting into the arcade game screen is also added in the background. It is entirely procedurally generated in a Fragment Shader.”*

## Summary

You can employ a myriad of approaches to shave precious bytes off your code base. These range from the [fairly well known](http://www.sitepoint.com/shorthand-javascript-techniques/) to the [more obscure](http://codegolf.stackexchange.com/questions/2682/tips-for-golfing-in-javascript). There’s an article on [How to minify your HTML5 game](http://gamedevelopment.tutsplus.com/articles/how-to-minify-your-html5-game-for-the-js13kgames-competition--cms-21883) over at Tuts+ Game Development, and you will also find a nicely curated list of tools and other materials at [js13kGames Resources](http://js13kgames.github.io/resources/) page.

I hope you’ve enjoyed this brief tour of js13kGames landscape and some of the winning [code golf](https://en.wikipedia.org/wiki/Code_golf) tricks past winners recommend. Tempted to give it a go this year? The 2016 competition starts in just a few days – on August 13th. [ Join us!](http://2016.js13kgames.com/) It’s not too late to start coding.

## About
[
Andrzej Mazur ](https://end3r.com)

HTML5 Game Developer, Enclave Games indie studio founder, js13kGames competition creator, and Gamedev.js Weekly newsletter publisher. Tech Speaker passionate about new, open web technologies, excited about WebXR and Web Monetization.