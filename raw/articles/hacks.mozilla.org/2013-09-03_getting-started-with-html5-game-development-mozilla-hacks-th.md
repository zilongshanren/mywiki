---
title: Getting Started With HTML5 Game Development – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/09/getting-started-with-html5-game-development/
author: Austin Hallock
published: '2013-09-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There are plenty of valid ways to create an HTML5 game, and quite a bit of material on the technical aspect of each, so for this article I’ll be giving more of a broad overview of HTML5 game development. How “HTML5” can be better than native, where to start with the development process, where to go when you’re stuck, and how to monetize and distribute games.

# Benefits of HTML5

![](../../assets/fbeacf066b90008f.png)


Most of the audience here already sees the value in HTML5, but I want to re-iterate why you should be building an HTML5 game. If you are just targeting iOS for your game, write the game in Objective-C, the cons outweigh the benefits in that scenario… *but* if you want to build a game that works on a multitude of platforms, HTML5 is the way to go.

## Cross-Platform

One of the more obvious advantages of HTML5 for games is that the games will work on any modern device. Yes, you will have to put extra thought into how your game will respond to various screen sizes and input types, and yes, you might have to do a bit of ‘personalization’ in the code per platform (the main inhibitor being audio); but it’s far better than the alternative of completely porting the game each time.

I see too many games that *don’t* work on mobile and tablets, and in most instances that really is a huge mistake to make when developing your game – **keep mobile in mind when developing your HTML5 game!**

## Unique Distribution

Most HTML5 games that have been developed to this point are built in the same manner as Flash and native mobile games. To some extent this makes sense, but what’s overlooked is the actual benefits The Web as a platform adds. It’s like if an iOS developer were to build a game that doesn’t take advantage of how touch is different from a mouse – or if Doodle Jump was built with arrow keys at the bottom of the screen instead of using the device’s accelerator.

It’s so easy to fall into the mindset of doing what has worked in the past, but that stifles innovation. It’s a trap I’ve fallen into – trying to 100% emulate what has been successful on iOS, Android, and Flash – and it wasn’t until chatting with former Mozillian [Rob Hawkes](http://rawkes.com/) before I fully realized it. While emulating what worked in the past is necessary to an extent, The Open Web is a different vehicle for games, and innovation can only happen when taking a risk and trying something new.

Distribution for HTML5 games is often thought of as a weakness, but that’s just because we’ve been looking at it in the same sense as native mobile games, where a marketplace is **the only** way to find games. With HTML5 games you have the incredible powerful hyperlink. Links can so easily be distributed across the web and mobile devices (think of how many links you click in the Facebook and Twitter apps), and it certainly should not just be limited to the main page for the game. The technology is there to be able to link to your game and do more interesting things like jump to a specific point in a game, try to beat a friend’s score, or play real-time against that friend – use it to your advantage!

Take a good look at was has worked for the virality of websites and apply those same principles to your games.

## Quicker Development Process

No waiting for compilation, updates and debugging in real-time, and once the game is done, you can push out the update immediately.

# Choosing a Game Engine

Game engines are just one more level of abstraction that take care of a few of the more tedious tasks of game development. Most take care of asset loading, input, physics, audio, sprite maps and animation, but they vary quite a bit. Some engines are pretty barebones, while some ([ImpactJS](http://impactjs.com) for example) go as far as including a 2D level editor and debug tools.

## Decide Whether or Not You Need a Game Engine

This is largely a personal decision. Game Engines will almost always reduce the time it takes for you to create a fully-functional game, but I know some folks just like the process of building everything from the ground up so they can better understand every component of the game.

For simple games, it really isn’t difficult to build from scratch (assuming you have a JavaScript background and understand how games work). [Slime Volley](http://slime.clay.io) ([source](https://github.com/claydotio/Slime-Volley)) for example was built without having a game engine, and none of the components were rocket science. Of course, Slime Volley is a very basic game, building an RPG from the ground up would likely lead to more hair pulling.

## Choosing Between a “Game Engine” and a “Game Maker”

Most of the typical audience of Mozilla Hacks are probably going to lean toward using a game engine or building from scratch, but there is also the alternative of using a “Game Maker” like [Construct 2](https://www.scirra.com/construct2). Using a Game Maker means you won’t actually write in JavaScript; instead, you create code-like events in the editor. It’s a trade of ease-of-use and quickness to prototype/develop vs customization and control over the end result. I’ve seen some very impressive games built with either, but as a developer-type, I tend to favor writing from scratch / using an engine.

## Finding the Right Game Engine / Game Maker for you

There are so many HTML5 game engines out there, which in part is a good thing, but can also be a bad thing since a large percentage have either already stopped being maintained, or will soon stop being maintained. You definitely want to pick an engine that will continually be updated and improved over the years to come.

[HTML5GameEngine.com](http://html5gameengine.com) is a great place to start your search because the hundreds of game engines are narrowed down to about 20 that are established, actively maintained, and have actual games being developed with them.

For a more complete list of engines (meaning there can be some junk to sift through), [this list on GitHub](https://github.com/bebraw/jswiki/wiki/Game-Engines) is your best bet.

# Learning Tools

If you’re going with a game engine, typically their site is the best resource with tutorials and documentation.

## Technical Tutorials

[jsGameWiki](https://github.com/DaRaFF/jsgamewiki)is full of links to technical tutorials and resources.[HTML5 Gamedev Starter](http://html5devstarter.enclavegames.com/)– similar to jsGameWiki, but a bit easier to digest.[Mozilla Hacks -> Games](https://hacks.mozilla.org/category/games-2/)[How To Design A Mobile Game With HTML5](http://mobile.smashingmagazine.com/2012/10/19/design-your-own-mobile-game/)for developing a game that’s mobile friendly.[No Tears Guide to HTML5 Games](http://www.html5rocks.com/en/tutorials/canvas/notearsgame/)is relatively old (2.5 years), but still is a very good learning tool if you’re not using a game engine.

## Game Design Tutorials

With game development, the technical aspect isn’t everything – what’s more important is that the game actually be **fun**. Below are a few places to start when learning about game mechanics.

# Helpful Game Tools

## User Retention, Monetization and more

*Full disclosure here: I am a co-founder at Clay.io.*

Making a game function is just part of the equation. You also want players to play longer, come back, tell their friends about it, and maybe even buy something. Common elements in games that focus on these areas are features like user accounts, high scores, achievements, social integration, and in-game payments. On the surface most are typically easy enough to implement, but there are often many cross-platform issues and intricacies that are overlooked. There is also value in having a central service running these across many games – for example, players genuinely care about achievements on Xbox Live because Gamerscore matters to them.

[Clay.io](http://clay.io/development-tools)– user accounts, high scores, achievements, in-game payments, analytics, distribution, and more.[Scoreoid](http://scoreoid.com/)– similar to above.

## Development Tools

[stats.js](https://github.com/mrdoob/stats.js)– A JavaScript performance monitor. Displays framerate, and performance over time.[Socket.IO](http://socket.io/)– realtime client-server communication (if you’re going to have a backend for your game).[pixi.js](https://github.com/GoodBoyDigital/pixi.js)– A canvas and WebGL rendering engine.[CocoonJS](http://www.ludei.com/tech/cocoonjs)– Improves HTML5 game performance on iOS and Android with an accelerated canvas bound to OpenGL ES.

# Motivation

Regardless of what you’re building, extra motivation is always helpful. For games, that motivation often comes from surrounding yourself with others who are in the same boat as you – working on games.

js13kGames is a competition that is currently taking place at the time of this writing. You have until September 13th, 2013 to develop an HTML5 game that, when compressed, is less than 13kb.

Mozilla runs a game competition every year from December through February with some fantastic prizes – last year’s was [an all-expense paid, red carpet trip to San Francisco for GDC 2013](https://blog.mozilla.org/gameon/2012/12/11/introducing-this-years-game-on-competition/).

Clay.io (full disclosure, I am a founder) runs an annual HTML5 game development competition for students. Last year was the first year and we had [over 70 games submitted](http://clay.io/play/gotgame). The next competition is planned for February / March 2014.

Ludum Dare isn’t for tangible prizes, nor is is specific to HTML5 games, but there are plenty of HTML5 developers that participate.

One Game a Month isn’t so much a competition as it is an accountability tool. This isn’t restricted to HTML5 games, but many of the participants work with HTML5. The goal is to crank out one game every month. I wouldn’t recommend this long-term since one month is too short of a time to create a *great* game, but it’s good when learning to force yourself to develop *and finish* simple games.

# Help From the Community

HTML5GameDevs has quickly become the most active community of HTML5 game developers. Most folks are very friendly and willing to help with any issues you run into.

#BBG is the go-to IRC channel for HTML5 games – you’ll even find quite a few Mozillians hanging around.

# How to Make Money

## In-Game Purchases

In-game payments, in my opinion, are the way to go for HTML5 game *in the long-term*. For now, most HTML5 games don’t have enough quality content, nor the game mechanics in place to get player purchasing items.

This is the revenue model with the highest potential, but it’s also the most difficult to achieve by far – not technically, but having the right game. I’d say the best way to learn how to properly monetize your game in this aspect is to take a look at games that do it really well on Flash and Mobile – games from King.com and Zynga typically have this nailed down pretty well. There’s also some good reading material, like [The Top F2P Monetization Tricks](http://www.gamasutra.com/blogs/RaminShokrizade/20130626/194933/) on Gamasutra.

## Licensing

Where we’re at right now with HTML5 games, licensing games is the strongest, most consistent way to make money – if and only if your game works well on mobile devices.

There are countless “Flash Game Portals” that receive organic mobile traffic, but can’t monetize it with the Flash games they have. Their solution is to go out and find HTML5 games to buy non-exclusive licenses (the right to put the game on their site, often making small adjustments) to offer their mobile visitors.

Typically non-exclusive HTML5 game licenses (meaning you can sell to more than one site) go for $500-$1,000 depending on the game and publisher. Some publishers will do a revenue share model instead where you’ll get a 40-50% share on any advertising revenue, but no up-front money.

**Licensing is the safest way to make money right now, but the cap is limited** – the most you’re going to make with a single game is in the $5,000-$6,000 range, but it is easier to hit that mark than it is with in-game payments or advertising.

## Advertising

Advertising is the middle-ground between in-game payments and licensing. It’s easier than in-game payments to make money and with a higher potential cap than licensing (but probably less than in-game payments). It’s easy enough to implement ads: just pick your ad network of choice (be wary of Adsense’s strict terms) and implement them either surrounding the game, or at various stopping points.

The commonly used ad networks are [LeadBolt](http://www.leadbolt.com/) for mobile and [CPMStar](https://www.cpmstar.com/) for desktop. You can also use [Clay.io](http://clay.io/docs/advertisingapi) which makes it a bit easier to implement advertising, and tries to maximize the revenue by using different ad networks depending on the device used and other factors.

# Distribution

The final stage in a game’s development is distribution. The game is done, now you want people playing the game! Fortunately, with HTML5 there are plenty of places to have your game (many of which often go unused).

More and more marketplaces these days are accepting HTML5 games as-is. Each has their own requirements (Facebook requires SSL, most require a differently formatted manifest file, etc…), but the time it takes to get into each is typically less than 30 minutes. If you want to reduce that even more, Clay.io helps auto-generate the manifest files and promotional image assets you’ll need (as well as takes care of the SSL requirement) – [documentation on that here](http://clay.io/docs/distribute).

![](../../assets/e85b8600052bc4b7.png)


[Firefox Marketplace](https://marketplace.firefox.com/)[Clay.io](http://clay.io/development-tools)[Chrome Webstore](https://developers.google.com/chrome/web-store/)[Windows App Store](https://appdev.microsoft.com/StorePortals/en-US/Account/signup/start)[Facebook](https://developers.facebook.com/docs/web/)[Amazon Appstore](https://developer.amazon.com/welcome.html)[HTML5Games.com](http://html5games.com/)[Kongregate](http://developers.kongregate.com/),[Newgrounds](http://www.newgrounds.com/)(and many other similar Game Portals)

Some marketplaces you’ll need to have a native wrapper for your game – primarily the iOS App Store and Google Play. A wrapper like PhoneGap is one option, but the native webviews have pretty terrible JavaScript engines, so for now you’re better off with tools like [CocoonJS](http://www.ludei.com/tech/cocoonjs) and [Ejecta](http://impactjs.com/ejecta).

**Now it’s up to you to go forth and make a great, innovative web game – I’m looking forward to see what’s on the horizon in the coming months and years!**

## About
[
Austin Hallock ](http://clay.io)

Austin Hallock is CEO of Clay.io - provider of high-level tools and distribution for HTML5 game developers.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 18 comments

PixelCutSeptember 3rd, 2013 at 02:25Austin HallockSeptember 3rd, 2013 at 11:55Max SchmittSeptember 3rd, 2013 at 05:31Austin HallockSeptember 3rd, 2013 at 11:54BenjaminSeptember 12th, 2013 at 09:20Max SchmittSeptember 12th, 2013 at 14:07Marcus StenbeckSeptember 4th, 2013 at 00:29Austin HallockSeptember 4th, 2013 at 13:52Fede BalboaSeptember 4th, 2013 at 11:37Austin HallockSeptember 4th, 2013 at 13:44OkSeptember 5th, 2013 at 07:05Austin HallockSeptember 5th, 2013 at 21:09GabrieleSeptember 6th, 2013 at 05:15Robert Nyman [Editor]September 9th, 2013 at 00:38YesiateyoursheepSeptember 8th, 2013 at 02:55AdrianSeptember 10th, 2013 at 20:06AmlanSeptember 16th, 2013 at 23:49Austin HallockSeptember 17th, 2013 at 23:40