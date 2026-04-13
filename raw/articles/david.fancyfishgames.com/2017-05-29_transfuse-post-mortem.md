---
title: TransFuse Post Mortem
url: http://david.fancyfishgames.com/2017/05/transfuse-post-mortem.html
author: Legend
published: '2017-05-29'
source_blog: The Legend of GameDev
source_site: http://david.fancyfishgames.com/
category: graphics
fetched: '2026-04-13'
---

This is the story of

[TransFuse](https://davidmaletz.itch.io/transfuse), a game made in 48 hours for the

[Butterscotch ShenaniJam](https://itch.io/jam/bscotch100).

## The Idea

At the start of the Jam, I rolled the theme: "Electric Leech." At first, we were at a loss about what to do - as while the theme brought a vivid picture to mind, it didn't really inspire any particular gameplay for us. All of our ideas were just games with electric leeches (and a few of the ideas were just leeches... the gameplay was pretty questionable). However, eventually I came up with the idea for a tower defense game where the enemies were leeches, and they both sucked your blood (leech) but also gave you power which you needed to build towers (electric). This double-edged enemy type was a very interesting twist to the tower defense gameplay - and changed the game from trying to have an impenetrable defense (letting as few enemies through as possible), to balancing how many enemies got through and how quickly.

About two hours into the jam, we had finalized the idea and came up with a quick design document for it.

## The First Day

After we came up with our idea and design document, we had about four hours left in the first day to make something. Aaron sent me quick placeholder art and I got to work setting up the grid and pathfinding for the ground leeches. I also looked through old code of mine and reused a bunch of stuff - mostly utility classes and the tower placement (and also a lot of the animation/display stuff). By the end of the day, there was no UI, but you could place towers that did nothing (except block leeches), and watch the leeches pathfind through your towers to reach your ship. Not really a game yet, but a good milestone.

## The Second Day

The only full day of the jam, this was where the majority of the work happened. By the end of this day, the game was very playable (and very fun, which is always a good sign). There was no title page, game over or victory screens, and you couldn't power/unpower or sell towers, but you could place towers which would automatically fire at leeches (including aiming for targets closer to your ship and leading - firing at where the leech will be instead of where it is), and you could fire the cannon and the majority of the UI was in place.

## The Third Day

Ideally, the third day of a jam is left for polishing, tweaking, and submitting. That was most of what we did (plus the title, game over and victory screens and the tower menu where you could power/unpower and sell towers). I also added the notifications so you could see how much blood/energy leeches took when they reached your ship, and did some balancing. Obviously the game isn't perfectly balanced and there are no tooltips, but for only 48 hours I am quite pleased with where it ended up. I also had to create the video for the game, which I didn't realize I needed until 2 hours before the deadline so it was a little bit of a crazy rush making that and adding the last of the art/music to the game, but we did it (with a whopping 5 minutes to spare).

## Final Thoughts

Overall I think the jam went very well, and I feel like we accomplished a lot in only 48 hours. While it's not perfectly polished and there's a ton of features that would be nice to add (like more towers, tower upgrades, more enemy types, ship upgrades, and a level or wave based progression), I feel that it is pretty complete and fun.

## No comments:

## Post a Comment