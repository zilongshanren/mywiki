---
title: '"Little puppets": The storybook art of rat-tastic action RPG Tails of Iron'
url: https://www.gamedeveloper.com/art/-little-puppets-the-storybook-art-of-rat-tastic-action-rpg-i-tails-of-iron-i-
author: Jack Yarwood
published: '2021-11-03'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

When [Odd Bug](https://www.oddbug.co.uk/) set out to make the follow-up to its 2017 VR platformer [The Lost Bear](https://store.playstation.com/en-gb/product/EP1731-CUSA04537_00-1234567890123456), the studio knew it wanted to continue with the same storybook aesthetic it had established with that previous game. On The Lost Bear, Odd Bug had designed environments to only be explorable in 2D, but gave them additional background layers to grant them a greater level of depth. It had also devised its characters to look like paper cut outs.

But Odd Bug art director Martin Reimann claims that working in VR limited the studio in regards to how many layers it could use to accomplish this and the amount of detail it could put into the game. So on the studios' first non-VR project [Tails of Iron](https://store.steampowered.com/app/1283410/Tails_of_Iron/)--a 2D action-RPG set in a world of anthropomorphic frogs and mice--the studio set out to create a much denser and more fully-realized world.

Tails of Iron follows a rat named Redgi as he rebuilds his kingdom after an attack from an army of vicious frogs. Players take control of Redgi and will explore a wide range of environments from farmlands to forests to crypts, battling frogs, bugs, and undead rodents to save friends and family, and restore the rat kingdom to its former glory. We recently spoke to Reimann, and the lead character artist, animator, and designer [Daniel Robinson](https://twitter.com/sleeping_dust?lang=en), to talk about how the developers created this storybook aesthetic and what inspired them to make a game about anthropomorphic rats.

## Clangers, Mouseguard, and Czech puppetry

Speaking to the pair, they tell me that there were a whole bunch of influences that informed Tails of Iron's art direction, characters, and story. Among these were Robinson's pet rats; children's TV shows like The Clangers and Bagpuss; and of course, other classics of the swords-and-whiskers subgenre.

"Mouseguard is one that we always kept close to us," says Robinson. "Purely because we can look at what they've done, but we use it not to cross too much into their territory because they have their very own style. If we go too mousey or too cute, it's always like 'It's too similar to that, let's pull further back.'"

"It's the same with Redwall as well," Reimann adds. "It's such a classic. Everyone knows it. So we always keep it in mind, but try not to go too close to it."

The pair say the look of Tails of Iron--with its marionette-style characters and layered backgrounds--came fairly naturally to them. The two originally developed this style while working together at Norwich University and have leaned into it ever since. They liken it to Czech puppet theatre, due to the hand-crafted look of the characters and the backgrounds that resemble a theatre set.

Most of the rats in the game are based on my pets so that gave me a strong starting point regarding characteristics and visuals.


"Since I started doing art in my childhood, I had developed my own style with those thick, black lines and bright colors and whatnot," says Reimann. "And then when we started doing The Lost Bear, I wanted to implement that style into a game so I thought that style kind of already looked like a theatre background. Then I combined it with Dan['s style]."

"[Martin and I] start working together and he is from the Czech Republic, so he kind of drove the art direction," Robinson adds. "But when we came together, we really liked how in European puppetry things were layered. And even with our characters, if you look closely, you'll see they are all cut up like they are a little puppet."

When it came to making Tails of Iron, the pair deciding to continue developing this style further. But this time around they needed to create a much broader cast of characters due to the demand for a greater number of NPCs, like enemies and quest-givers.

## Making the cast

Similar to in Redwall and Mouseguard, all of the characters in Tails of Iron are anthropomorphized animals. You'll encounter other rats, aggressive frogs, hostile bugs, and industrious moles. As a result, Robinson had to come up with a visual language for each. This is where good reference came in handy.

"Most of the rats in the game are based on my pets so that gave me a strong starting point regarding characteristics and visuals…" Robinson tells me. "And where I'm originally from in Hampshire, in Handover, there's [also] loads of frogs and toads, so when I was a kid if I ever turned over a rock or something like that, there was always a big ass toad looking at you. It was always a little bit scary as a kid."

Robinson used these examples not only to decide on the characteristics of the characters, but also to decide which colors he should use for them too. When designing characters in Adobe Photoshop, he tried to avoid heavily-saturated colors, as the in-game lighting and effects can often overly-brighten these. He also tried to inherit colors wherever possible from previous designs, in order to bind certain characters' together and establish common traits between them. After he has the design nailed down, it's then time to rig the character.


To do this, he imagines he's creating a paper cut-out puppet, which involves cutting off the limbs into separate pieces, while keeping the body as a mesh to give it some flexibility and add some "squishiness". What he ends up with is a sprite that he can start adding bones to in order to rig and animate the character. He uses a 2D animation tool for Unity called Puppet2D in order to accomplish this.

The number of characters wasn't the only challenge with Tails of Iron. Tails of Iron also features more environments than The Lost Bear, many of which change over time as the kingdom rebuilds, and many that feature significantly more layers.

## Setting the stage

Reimann compares the process of making these environments to setting up a theatre stage. Every asset – including trees and rocks--is its own separate asset that is hand-placed in layers at different z depths. Reimann then bundles these layers together for optimization using some code. One advantage of this is that the camera does the parallax naturally, with objects far away moving slower than those closer to the player's perspective.

According Reimann, the interiors are much quicker to make, but require a more handmade approach as he can't reuse any assets. This is the case, for instance, with the shop in Longtail Village, where players can purchase arrows or bolts. This shop contains a counter with a set of scales, as well as shelves of assorted bric-a-brac in jars and containers.

"For the shop, all those shelves are made specifically for that location," says Reimann. "And of course, the interiors are not that deep, so I don't have to worry too much about the parallax or the amount of layers. So, the interiors are definitely much easier to do. A shop I can do in a couple of days, but the much harder ones are the big outside sections and the big forests where you have to worry where the light hits the asset. Those take quite a while and they change quite a lot through development."

It's in these more open areas where the developers take advantage of these layers. Not only does the art team swap out certain layers to show the player's progress in rebuilding the kingdom, but they also use place NPCs in the background to foreshadow bosses and introduce some worldbuilding. For instance, you can see workers working away in Longtail Village and farmers tilling the land on the outskirts.

"We love how Playdead foreshadowed the spider in Limbo," says Robinson. "You'd always see it in the background but you wouldn't go against it. Even games like Super Metroid, they would do things like that where you would see the boss in the background and then you would fight it. We were always inspired by stuff like that. But then we just took it to the other side where it's like passive stuff--villagers doing their thing--because we felt that stuff just created like lore and made you feel more attached to what you're looking at."

The result of all this effort is that playing Tails of Iron feels like you're exploring a children's storybook come to life or manipulating a character on a stage. Like The Lost Bear, it feels intricate and handmade, and this immediately creates a personal connection with the player. While chatting, Reimann and Robinson dropped hints about continuing this style on their next project. And it will be interesting to see how they can take it further in the future.