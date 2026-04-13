---
title: 'Polishing a Level Select screen: process and implementation'
url: https://www.gamedeveloper.com/art/polishing-a-level-select-screen-process-and-implementation
author: Matt Hackett
published: '2012-06-27'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Polishing a Level Select screen: process and implementation

In this article, I walk through the process of determining how to polish a level select screen, followed by implementation details including graphical and user interface improvements.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

We’re just about ready to launch Lunch Bug, which means I’ve been polishing every rough edge until it shines. One of the roughest edges until just recently was the “level select” screen, where players progress through the game.

![Lunch Bug level select (before) Lunch Bug level select (before)](../../assets/373244c1fd7dc869.png)


The level select screen was simple and worked fine, but it wasn’t much to look at and certainly wasn’t fun to interact with. Also the number of rows in each column were uneven in portrait mode. We can do better!

![Lunch Bug level select (before) Lunch Bug level select (before)](../../assets/57ff0f1ce808070b.png)


## The plan

After [some brainstorming](http://www.lostdecadegames.com/media/images/posts/lunch_bug/level_select/sketch.jpg), I came up with this plan of attack:

Break up this single screen into multiple pages to enhance the feeling of progression.

Improve the user interface regarding current goal and level unlocking.

Polish up the screens with unique graphics and animations.


![Brainstorming Brainstorming](../../assets/4f9dac8db98f5447.jpg)


## 1. Break it up

The first step was to split the level select screen into separate pages. Since Lunch Bug has 20 levels, 4 screens displaying 5 levels each felt like a good separation. Once the buttons were positioned correctly, I converted them into simple images instead of buttons.

![Step 1: break up the screen into multiple pages Step 1: break up the screen into multiple pages](../../assets/347cf0f03e98b073.png)


In this first iteration, I also threw in “back” and “next” buttons to allow users to navigate through the pages. The steps I take are deliberately small, in an attempt to isolate potential issues early on and avoid tripping on bugs as I get deeper into the implementation.

Once I removed the large majority of buttons from the design, I noticed that the screen looked especially bare. Always on the lookout for ways to give our graphics longer legs, it occurred to me that the overhanging leaves from the title screen would work here too.

![Lunch Bug level select (old) Lunch Bug level select (old)](../../assets/0d6a5ad364a9e507.png)


## 2. Better user interface

The previous level select screen wasn’t just unpolished, it also had a clunky user interface. When players unlocked a new level, the button representing the next level would simply become enabled (changing its color from grey to black). Pretty lame, not very rewarding, and worst of all, not a very clear message to the player.

To fix this, I highlighted the current level button with what I ended up calling “guide bugs.” I positioned these little guys in a circle around the highlighted button. This clearly messages to the player which level is next, and since they dance around, it makes the screen more entertaining to look at too.

![Step 2: better user interface Step 2: better user interface](../../assets/234d96c58620c23d.png)


I also added tweening animations when players unlock levels. The guide bugs swarm in on the button of the level the player just beat, then tween to the next level’s button. It’s a little reward to the player for finishing a level and reinforces what the player’s next goal is.

## 3. Graphics and animation

The final step was graphical work. In place of the buttons which were only ever enabled or disabled, I wanted images with three states (locked, unlocked and current) that fit the game’s theme. To solve this I opted for picnic baskets. Since they already have “closed” and “opened” states, they’re easily visually mapped to “locked” and “unlocked.” To represent the “current” state, I filled it with a berry and made it glow.

I also rendered the paths between levels in the same style as the background tiles in the game. This draws a visual path between the levels and helps fill the design out.

![Step 3: graphics and animation Step 3: graphics and animation](../../assets/a3968b47a93e5946.png)


Lastly, nothing says polish like parallax scrolling! With a little Photoshop work, I made the leaves image into a repeating pattern. I then added a second leaves image stacked to the right, and after some easy tweening math, had them slowly scrolling along with the background. Parallax scrolling can be one of the simplest and most impactful visual effects to add when polishing your game.

## Take it further

Polish is one of those deep holes that you can spend tons of time on, but you’ll always want to add more! Once I had the paginated level select screen in place, it created the perfect situation to introduce new graphics and music to the game.

![Lunch Bug tiles Lunch Bug tiles](../../assets/217a28a83039e994.png)


The first step was to add new repeating tile graphics to the mix. This rewards the player for progressing through the game with interesting new graphics to enjoy. Since Lunch Bug’s composer [Joshua Morse](http://jmflava.com/)had already made four songs for the gameplay, it was easy to load those on the fly too.

![Step 3: graphics and animation Step 3: graphics and animation](../../assets/26237200304cb410.png)


As a strategic puzzle game, Lunch Bug can take a long time to master. The hope is that these new pages of levels will enhance the feeling of progression. Changing up the look and feel should also reinvigorate players to keep enjoying the game.

## Summary

Polish can be hard work but it is absolutely mandatory if you want your game to shine. This process took about one entire week of development, but I think it was well worth it. When a part of your game isn’t polished shiny, the overall experience of playing it can suffer.

Lunch Bug is the next HTML5 game from Lost Decade Games, soon to be released on Facebook, Pokki, the Chrome Web Store, Mac App Store, iOS, Android and the open web. [Follow us on Twitter](https://twitter.com/#!/lostdecadegames) and we’ll let you know when it’s ready to play!