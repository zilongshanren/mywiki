---
title: Simonschreibt.
url: https://simonschreibt.de/gat/battlefront-ii-layered-explosion/
author: Simon
published: '2023-04-25'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

## Foreword: Back to the roots!

Some people might have noticed, that I didn’t create new “classic” articles lately. This has two reasons: First, my blog is the main reason why I have the privilege to work in VFX, [giving talks](https://simont.de/#talks) and [teaching classes](https://simont.de/#teaching). Unfortunately, the success of the blog makes me spend a lot of time in preparing talks and classes instead of making new blog content (also, I felt the need to push [my own skills](https://www.artstation.com/simont) instead of “only” investigating the geniality of others).

And second: While my articles were tiny at the beginning, they grew more and more complex, and then I’ve even started to create a video for each of them (#overhead)!

While an article from the beginning did just cost some hours to write, the later posts could cost weeks or even months to put together. This resulted in longer (better) articles, but also created pressure to never release something smaller again. And also took away a bit of the fun because it felt more like work and created a barrier: IF I’d start a new article, I knew it will cost A LOT of time – this mountain of work could make me hesitate to start at all. So I’d like to go back to the roots. This means: If I observe something cool in a game, I’d like to have the mental freedom to put it into a post even thought it may be only one or two images and without the pressure of having to create a video.

This is also a way to secure information for the future. Sometimes I see cool threads on Twitter and I always wonder: What if Twitter shuts down or what if the account gets banned for some reason? Putting stuff on your own blog (maybe in addition to Twitter/Mastodon/Facebook … lol, Facebook :D As if someone would still use it! :’D) gives the information more security.

And that’s why I’d like to convert [a Twitter-Thread I did in 2020 about Explosions in Battlefront II](https://twitter.com/simonschreibt/status/1281255407516778496) into a small article here on my blog.

I hope you like it and let me know in the comments what you think about getting back to the roots! :)

## Battlefront II: Boom

I’ve checked out some VFX (but mostly an explosion) from [Star Wars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/) and wanted to share the gained knowledge. At first glance, it might look like 1 flipbook put on 1 particle. But in fact, it’s quite more complex than that!

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

Almost all VFX textures are gathered in **one** huge atlas (12288x8192px, DDS = 96 MB). Most flipbooks are loop-able. Some are unique: They show for example how smoke/fire builds up and then dissolves over time.

![](../../assets/6f8883ba5457e98f.jpg)


![](../../assets/6f8883ba5457e98f.jpg)

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

Here you can see the wireframe of the explosion particles (pink) some blue trails and on the right some blue stuff which I don’t know what it is :D But the important part is the wireframe because as I mentioned before: The effect consists of more single particles than one would think.

![](../../assets/0b153d257fe45ece.jpg)


![](../../assets/0b153d257fe45ece.jpg)

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

I was surprised how many particles the explosion used and how volumetric the “geometry” is. This gives the whole effect a good depth.

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

Some particles are “duplicated”. I guess one uses a smoke-texture and the other one a fire-texture (more about this below):

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

The separation of smoke and fire was shown in the [official blog post about their VFX](https://www.reddit.com/r/StarWarsBattlefront/comments/cho15m/community_transmission_visual_effects_in_star/). As you can see, there is a smoke layer and on top a perfectly fitting fire layer:

[Visual Effects in Star Wars Battlefront II](https://www.reddit.com/r/StarWarsBattlefront/comments/cho15m/community_transmission_visual_effects_in_star/)

I can see this also in the data: There are **two** flipbooks for the **same** smoke/explosion. The channels RGB1+RGB2 contain 6 lightmaps in total (if you ask yourself “why 6 lightmaps?!” [please follow this link](https://realtimevfx.com/t/6-way-lightmap-wip/5457)). At least, I guess that they are lightmaps. I didn’t see any normal map or motion vectors. The Alpha of the first flipbook is the transparency, and the alpha of the second flipbook contains the emissive fire part.

If you take the emissive fire part and put it on top of the smoke, it fits perfectly (here I show 1 frame of the whole flipbook). I guess that’s why we see the “double” particle geometry (mentioned above).

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

For colouring the smoke/fire, they seem to use a LUT:

This is one of the loop-able textures in motion. Fantastic work! ♥

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

**By the way**: I created a [Houdini-Tutorial](https://www.youtube.com/watch?v=OmoiPRvnSm0) on how you can create such loop-able flipbooks and I wrote an [article](http://simonschreibt.de/gat/fallout-4-the-mushroom-case/) about an explosion in Fallout 4 which makes heavy use of a loop-able flipbook as well! (see links below)

We can also see some smoke trails. Here is their geometry:

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

**By the way**: There is a very interesting [video](https://www.youtube.com/watch?v=nRiGrO-rrCo) which compares the explosions of Battlefront 1 and 2. In my eyes, the explosions in Battlefront 2 look more advanced, but the ones from Battlefront 1 look more like Star Wars. What do you think?

**Bonus 1**: I love how this texture looks for their smoke.

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

**Bonus 2**: I love the little leaf-clusters (which seem to be generated when the camera moves to hide their creation?)

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

**Bonus 3**: The impacts do make use of the nice smoke textures as well.

[Starwars Battlefront II](https://store.steampowered.com/agecheck/app/1237950/)

I hope you liked this little VFX overview.

Have a very nice day,

Simon 🌞

To the lightmaps/normal maps distinction; if you think about it, volumetrics don’t strictly have any surface normals. But if you want to to light a particle that represents a volume, you still want a direction to (dot) compare your light direction to. That’s where those 6-directional “lightmaps” come in.

Whether it should be called a normal map can be debated. Unlike normal maps, these include light occlusion from the volume (ao/shadows).

Embergen calls it a 6 point normal map, and lets you export these quite easily:

https://docs.jangafx.com/embergen/pages/references/node_list.html#capture-types

(the gif cycles through capture types, including 6 point)

Thank you! Still need to dive into EmberGen. Didn’t find the time yet :(