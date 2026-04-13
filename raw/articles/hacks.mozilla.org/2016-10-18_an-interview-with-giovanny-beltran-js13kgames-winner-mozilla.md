---
title: An Interview With Giovanny Beltran, js13kgames Winner – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2016/10/an-interview-with-giovanny-beltran-js13kgames-winner/
author: Giovanny Andres
published: '2016-10-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[js13kgames](http://js13kgames.com/), a JavaScript coding competition for HTML5 game developers, announced this year’s winners a few weeks ago. Today we have an interview with [Giovanny Beltran](https://twitter.com/agar3s), winner of many categories at js13kgames, and one of the best entries in this year’s contest. Giovanny has been programming for 13 years, and began working with JavasScript five years ago. In his free time he likes to play and create game demos.

![6820295abe0128cf7248b1e20f7882de_1e63cr2](../../assets/9b815788a6331755.jpeg)


Giovanny is an organizer of [BogotaJS](http://www.meetup.com/BogotaJS/) and a Spanish-speaking indie game developer community called [Juegos Indies](https://www.facebook.com/groups/juegosindies). Originally he created games in Java but it was so difficult to share his creations with his partners, so for this reason he decided to learn JavaScript. JavaScript gave him an easier way to share his own game creations with friends.


**Hey Giovanny, tell us what you’re working on these days?**

I work full time for a biotech company called [Miroculus](http://www.miroculus.com/), and in my free time I work on video games and experimenting with new web technologies.

**We know you participated in the js13kgames challenge. Can you tell us about your entry?**

Yes, I participated this year (2016) and in 2014. This year’s contest theme was [Glitch](https://www.glitchthegame.com/). I’d been wanting to do a 2D shooter for a while. The idea was to combine the Glitch topic with a shooter game. Because Glitches are from the 80s and 90s, I went with the idea of building something retro to evoke the sensation and nostalgia of an old retro game. My entry was called [Evil Glitch](http://js13kgames.com/entries/evil-glitch).

**Nice. How does it work? Where did your ideas come from?**

I enjoy playing shooter games and one in particular really inspired me. It’s called [Devil Daggers](http://devildaggers.com/). Devil Daggers is frenetic and fast. Every match lasts about 4 minutes maximum, but that’s enough time to fall in love with playing it. So, it gave me the idea to create a game that’s exciting to play, with fast rounds to give you the adrenaline for yet another round and keep playing until you win or beat your high score. The protagonist of Evil Glitch is a 2D character whose world is invaded by 3D characters.

**What was it like developing and debugging Evil Glitch? Were there any surprises during the process?**

I have an automated build process, it’s executed every time I make a change in the source code of the game. This build process concatenates all the files and creates a single js file (without using [minify](http://www.minifier.org/)). There’s a debug constant to display performance stats and some variable values that act directly on the game. When you build a minified version, this debug variable goes to false and the minifier (closure) removes all the code that is inside of the debug context.

I should also say that the build system I used is based on the winning entry from last year’s js13kgames: [Behind Asteroids](https://github.com/gre/behind-asteroids) by Gaëtan Renaudeau.

**Did you use any specific tools and libraries for your entry? Any you like the most?**

I used [npm](https://www.npmjs.com/) to automate the build process, [livereload](http://livereload.com/) to update the game in *real time*, [closure](https://developers.google.com/closure/compiler/) to minify, [stats.js](http://github.com/mrdoob/stats.js) to validate memory and performance, [glslmin](https://github.com/chrisdickinson/glslmin) to minify webgl shaders, [webgl.js](https://github.com/gre/behind-asteroids/blob/master/src/lib/webgl.js) to handle shaders, [shadertoy](https://www.shadertoy.com/) as a reference for shaders, [jsfxr](https://github.com/mneubrand/jsfxr) for sound effects and [tinymusic](https://github.com/kevincennis/TinyMusic) for music. The last two tools are my favorites, as they help improve the experience of the game.

Looking for more? There is a big list of resources collected through the years available on [resources section](http://js13kgames.github.io/resources/) at js13kgames.

**In your opinion, what’s the most challenging part of building games for the web?**

Cross-browser compatibility is hard — making sure that the game behaves the same in all browsers. For this competition, the game must run at least in Firefox and Chrome, but in real life your game should run well in as many browsers as possible.

It’s also challenging to discover a way to monetize the games. Because these games are all available on the web, it’s all too easy to download the source code and reload the game elsewhere. This has actually happened already.

**What did you present as a speaker at JSConf Colombia?**

My talk for JSConf Colombia 2016 was selected before js13kgames 2016, so I was motivated to create a high level game with more detail and complexity than previous entries for the contest. I spoke about my experience developing Evil Glitch, and gave a workshop on the topic as well.

This is the link to [my slides](https://agar3s.github.io/js13k-2016-talk/#/) from [JSConf Colombia](https://jsconf.co/).

**Congratulations, you won!**

Thank you, I really worked hard to get the best results possible, however I didn’t expect to win. It was a big surprise due to the level of other competitors in the [js13kgames 2016](https://hacks.mozilla.org/2016/08/js13kgames-code-golf-for-game-devs/).

**Which js13kgames category did you won?**

I won 1st place in the Desktop category. I also won first place in two other categories (Facebook and Twitter) –thanks to the community of players who tested and upvoted my entry on the social networks.

Finally, I won in one other category – I won the most votes from all the game developers who participated in the challenge. Thanks to everyone in the jam who voted for my entry!

**What’s next for Giovanny Beltran? Are you going to participate in js13kgames next year? Any other contests or projects that you’re thinking about?**

There are many competitions about video games, but I really like js13kgames, due to the complexity of making a game in 13 kilobytes. I am going to put Evil Glitches on Steam, this is something I didn’t have planned but many people made the suggestion and pushed me to do it. You will be able to download [Evil Glitch from Steam](http://steamcommunity.com/sharedfiles/filedetails/?id=776834104) soon. So, yes, I am going to keep participating in js13kgames a few more times. Let’s hope I can do even better next year.

**Thank you, we hope to see you again with another awesome project or participating in another contest.**

Thanks for the interview. I want to try new things on the Web and experiment with WebGL. Some of these goals are not easy, but I am sure that by dedicating the time I can accomplish all of them.

Thanks to [Andrzej](http://dev.end3r.com/) and the js3kgames crew for keep running the contest every year, and to the [Colombia-Dev community](http://colombia-dev.org/), [GameDevLatam community](https://www.facebook.com/groups/comunidad.duval), and the JuegosIndies group for all the support.

## About
[
Giovanny Andres ](http://gioyik.com)

Giovanny is Porting Developer at Mozilla. He work developing solutions for IoT projects. Most of the people know him as Gio and enjoy his free time practicing extreme sports.