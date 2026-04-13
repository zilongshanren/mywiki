---
title: 'The making of Bankin'' Bacon: A dev experience we can take to the piggy bank'
url: https://blog.gemserk.com/2019/04/30/bankinbacon-ld44jam/
published: '2019-04-30'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

We want to share a bit about the game we did for Ludum Dare Jam #44 last weekend, it’s named:

![](../../assets/9f145cec3659179b.png)


Made by:

- Ariel Coppes (
[@arielsan](https://twitter.com/arielsan)) - Enzo Gaiero (
[@playorbust](https://twitter.com/playorbust)) - Rubén Garat (
[@rgarat](https://twitter.com/rgarat)) - Anthony García (
[@thonyg09](https://www.artstation.com/thonyg09))

Links

And now a bit of dev story by our friend Enzo.

## Dev Story

Initially, when we heard about the theme **Your life is currency** we were a bit bummed since we were set on doing a roguelike shoot em’ up game and were not so sure how to fit the theme into the mechanics, however, after a few cups of coffee and a brainstorming session around the whiteboard we ended up coming with the idea that would flesh out to be Bankin’ Bacon.

![](../../assets/44ca386837515700.png)


Initial ideas on character concept.

We discussed using lifesteal mechanics, simply addressing the theme through art assets, using HP for upgrades (but adding a lot of upgrades would take time away from polishing) and more. Eventually we ended up going for the idea of having HP being your ammo and the price to pay for every skill.

Once the core idea behind the mechanics was settled, we needed a main character. We tossed around many ideas like a gold golem being chased by dwarves, bankers throwing money stacks at each other but chose to go with a lovable character that would fit the theme perfectly… A piggy bank that shoots its own coins.

![](../../assets/b792d3af8e795d4b.png)


Our characters are taking shape.

A few hours later our awesome artist had this bouncy fella ready for integrating.

So, now that the character was settled and that the artist was working on the environment art we had to fully define the game’s mechanics.

Since we have some game jams under our belt we’ve learnt the hard way that the best way to address features during a jam is to have the ideal game in mind and the minimum viable product (MVP) to call it a closed game. Then, start building the MVP and polish our way on top of that.

![](../../assets/313d08dbbeef569f.png)


Terrain and colors concept.

Our main goal was to make a game that would deliver a fun couch multiplayer experience but instead of shooting like crazy you’d have to be frugal about it and make your shots count, after all… Your life is currency.

In order to make the players play frugally, we needed mechanics that would encourage that sort of play.

#### Planned mechanics that made it into the game :)

- Shooting does self damage to the shooter.
- Getting hit does more damage than shooting. (so shooting would make sense)
- Players die if getting shot drops their HP below zero.
- Dashing makes you invulnerable but costs HP.
- Players with no coins won’t be able to shoot. (So you can’t die from shooting.)

#### Planned mechanics that didn’t make it into the game :(

- Starting out with 50% max HP
- Dashing into coins would steal the coin shot.
- Player scale would vary according to HP. (so that the winning player would have a bigger hit box)
- Player speed would vary according to HP. (So that the losing player would be faster)
- Different coin values (i.e. quarters, nickels, pennies, etc.)

Why mention the mechanics that didn’t make it into the game? Well, to convey the whole “ideal game vs MVP” when it comes to jam development and also to explain the reason behind adding a new mechanic, coin dropping.

Even though we managed to make the game encourage players to be frugal about shooting and dashing, we were encouraging players not to do anything that was fun in the game, therefore, we needed a way to keep the coins around so players could keep playing, but doing regular powerup drops would inflate the game’s economy, thus, making about 80% of the coins used drop around the level was the right way to go.

When it comes to level design, we started by trying out Unity’s Probuilder, which came in handy for prototyping really complex levels with tunnels and nooks to hide in that would turn the game into more of a hide n’ seek type of play, but two issues came up from doing that:

- The camera needed for using tunnels and the like was a bit hectic for the type of game and stretched the art assets, so we ended up switching to a fixed camera.
- Doing that sort of levels would require an amount of art assets that would be impossible to make during a jam without sacrificing the art standards.

However, even though we didn’t use assets made in Probuilder, it played a crucial role alongside Progrid for testing out level sizes, prototypes and ultimately assembling the level with the final assets. After several iterations using complex designs, simple levels with little obstacles proved to be the way to go leaving more time for polishing the environmental decoration.

In conclusion, the overall experience was more than satisfactory, leaving us with a somewhat polished game that could provide plenty of fun couch multiplayer experiences.

To finish up, we leave you a longer gameplay video, enjoy!

Thanks for reading!