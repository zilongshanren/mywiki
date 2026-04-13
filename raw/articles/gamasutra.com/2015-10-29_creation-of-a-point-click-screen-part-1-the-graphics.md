---
title: 'Creation of a Point & Click screen - PART 1 : The graphics'
url: https://www.gamedeveloper.com/art/creation-of-a-point-click-screen---part-1-the-graphics
author: Fabrice Breton
published: '2015-10-29'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Creation of a Point & Click screen - PART 1 : The graphics

Some "behind the scenes" on the creation of a room in Demetrios! Here we study the art side.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

I thought it would be interesting to offer you some "behind the scenes" on how Demetrios is created!

And I figured the most interesting would be the creation of a screen in the game.

![](https://ksr-ugc.imgix.net/assets/004/685/716/e3e5c76071a23865406a4058d9c5a8a8_original.png?v=1444760949&w=639&fit=max&auto=webp&lossless=true&s=fd5d8f2749dd04d63abbd35a1277d0dd&width=1280&quality=80&disable=upscale)


I've made it very simple, so you'll understand even if you're not a game developer!

### Drawing

The first step is obvious : drawing the picture of the screen.

For this purpose, I'm using a regular Wacom graphical tablet. (the most basic one, actually!)

![](https://ksr-ugc.imgix.net/assets/004/685/728/13d643d254705f0a1d4dd3ca6ff54aaf_original.jpg?v=1444761058&w=639&fit=max&auto=webp&q=92&s=2fbff2370c377a6be4223acd7b38e694&width=1280&quality=80&disable=upscale)


At this stage, I'm cheating a bit. The game is a remake, so I use the old screens as a starting point!

![How the room looked like in the 1999 version How the room looked like in the 1999 version](https://ksr-ugc.imgix.net/assets/004/685/734/22c99d7c58e9567ff082e5e63d430023_original.png?v=1444761084&w=639&fit=max&auto=webp&lossless=true&s=7df0a45c733a1c0cf2bc1f9c45cd7c5b&width=1280&quality=80&disable=upscale)


How the room looked like in the 1999 version


At this stage, I have to think about several things, such as not putting important items too close to the edges of the screen, or having two items too close to each other. (In the first screens of the game, I often made that mistake, and correcting this later resulted in a real pain - better anticipate!)

I will also make some changes, such as adding, removing or moving items and parts of the scenery. Those changes make the game more interactive, and for other various gameplay reasons.

Then I will draw over the old drawing, but on another layer in my picture editing software. Considering I have the old version as reference, I skip the "sketching" part.

![](https://ksr-ugc.imgix.net/assets/004/685/744/4f94d167e46b0cc2c7d3132aa61e4cb1_original.png?v=1444761126&w=639&fit=max&auto=webp&lossless=true&s=d725d02ec67e1e1c1fd9a7a2fcf06a01&width=1280&quality=80&disable=upscale)



I have to be careful to draw some of the objects on different layers. For example, each object that will be animated or picked up by the player is put into its own layer! The reason being that each of them will become separate sprites on the screen.

### Coloring

Then, I start coloring parts of the screen, on separate layers. I have two personal technics for coloring :

- For natural elements (most often outdoors : grass, ground...), I fill each part with a single color first. Then I paint over it manually, using shades variations according to the light sources, in order to render depth. Then I use a smudge pencil over it so it looks more soft and natural.

![](https://ksr-ugc.imgix.net/assets/004/685/759/22c77fc200940b782e513513c311cc4d_original.png?v=1444761218&w=639&fit=max&auto=webp&lossless=true&s=b5eee47d1c0892b5ea44746a30f71f5b&width=1280&quality=80&disable=upscale)


- For inanimate / synthetic elements (most often indoors), I also fill each part with a single color. But after that, I create another layer, with a "Multiply" blending mode. This is used to add a shading over the objects, but without changing the coloring itself.

This has an artificial look to it, which is why I mostly use it on synthetic things. (for example, the parasol here)

![](https://ksr-ugc.imgix.net/assets/004/685/768/ad251a7104461dbb63fe0a9739092d56_original.png?v=1444761249&w=639&fit=max&auto=webp&lossless=true&s=e1451e147631e7ea07391f299f8f70ac&width=1280&quality=80&disable=upscale)


Both technics are complementary and gives Demetrios this unique style that fits my needs :)

### Animations and last steps

When it's done, I'm also adding shadows to all the elements on the screen with "Multiply" layers in the same way, according to the light sources directions.

Then I repeat the same process for each frame of every animated object on screen. Yes, there are often 3 layers for each frame of each object : the drawing layer, the color layer, and the "shading" layer!

To make the picture slightly better looking, I will actually color over the drawing lines according to the object color (eg : a dark green for the grass edges) This is something you'll often see with Disney art or modern comic books.

![Final picture without the animated sprites Final picture without the animated sprites](https://ksr-ugc.imgix.net/assets/004/685/784/f7f1d9f3a726baffda92c32c3046f973_original.png?v=1444761322&w=639&fit=max&auto=webp&lossless=true&s=0ab809907190b09e4a415527f62066c3&width=1280&quality=80&disable=upscale)


Final picture without the animated sprites


When the picture is finished, it's not rare that I end up with over a hundred different layers - for a single room picture!

Finally, I export all of these layers to separate image files, in order to be integrated into the game.

As a reference, I usually spend one day to do the drawing, one day for the coloring, and one day for the animations.

Three days for one room, multiplied by about 50 rooms in the game, and that's about half a year - just for that!

![Final picture with everything Final picture with everything](https://ksr-ugc.imgix.net/assets/004/685/792/ad3c00c4fcc3f21fb4622ca7d2053da9_original.png?v=1444761386&w=639&fit=max&auto=webp&lossless=true&s=f057c382af0df606c5d415a7ef2184c1&width=1280&quality=80&disable=upscale)


Final picture with everything


None were used in that particular example room, but I also often use "Overlay" blend mode layers in order to render light. This is seen for example in the living room at the start of the game : varying the opacity of that layer in-game gives the feeling of real time lighting!

![Lighting example Lighting example](https://ksr-ugc.imgix.net/assets/004/685/797/b549b04eb24e2bbdd6918f7d263b2313_original.png?v=1444761412&w=639&fit=max&auto=webp&lossless=true&s=d3b2d20e4473042b8ad012ed119f9f6d&width=1280&quality=80&disable=upscale)



NB : I've never had art lessons and I've learnt pretty much everything by myself, so I don't mean to give lessons - I have a lot to learn yet! :p

This "behind the scenes" will be continued in a next article.

If you liked this, please consider [voting for Demetrios on Steam Greenlight](http://steamcommunity.com/sharedfiles/filedetails/?id=502785332)!

Stay tuned! :)