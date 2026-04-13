---
title: Your game will always be paused in edit mode
url: https://dewitters.com/your-game-will-always-be-paused-in-edit-mode/
published: '2015-05-16'
source_blog: deWiTTERS
source_site: https://dewitters.com
category: game programming
fetched: '2026-04-13'
---

One of the main ideas behind RPG Playground is to [minimize the effort and time between playing and editing your game](http://www.koonsolo.com/news/game-designers-need-instant-feedback/). I didn’t want to make another game making tool where you need to build your game before play-testing it.

RPG Playground does just that. Play your game, and if you want to make a modification, just open the edit project pane on the left, and edit it straight away. After that, you can continue playing just were you left off.

Now, I also thought it was a good idea to keep the game running while editing it. It seemed like a good idea, because you can test a few things while the edit dialog is still open. However, maintaining this extra feature is becoming a real burden. Every time I add new functionality, I have to keep in mind what will happen when some event occurs in-game when the edit pane is open. How should the editor respond to that, etc. It takes a lot of my time, and therefore features aren’t implemented as fast as I want to.

Because of this reason, I decided to always pause the game while in edit mode. This means features can be delivered faster, and they will be less error prone, less strange things occurring etc.

When thinking about it, keeping the game running while editing is not that huge of a benefit. If you would edit a platform game for example (oops, I revealed some of my long term plans here… ;)), you probably *want* to pause the game, so your hero doesn’t die.

One of the drawbacks that I see, is for example when adapting the speed of an enemy. When the game would run in edit mode, you just change the number and immediately see the result. But now that the game is paused, you change the number, but have to do the extra click to close the edit dialog to see your modification. But then again, this is probably not that much of a loss.


*P.S.: Almost done with implementing doors that take you to another level :).*

## 0 Comments