---
title: 'BioWare pulls back the veil on Dragon Age: The Veilguard''s magical hair tech'
url: https://www.gamedeveloper.com/art/bioware-pulls-back-the-veil-on-dragon-age-the-veilguard-s-magical-hair-tech
author: Bryant Francis
published: '2024-11-12'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Davrin, a Black elf from Dragon Age: The Veilguard. Davrin, a Black elf from Dragon Age: The Veilguard.](../../assets/b5a0727eb027578f.jpg)

## At a Glance

- High-fidelity hair can be a tricky challenge in video games. BioWare's shown off its solutions for Dragon Age: The Veilguard.

Among the many, many things players and developers have [praised](https://www.thegamer.com/dragon-age-the-veilguard-long-hair-physics-fans-love/) about BioWare's Dragon Age: The Veilguard is the incredible hair options in the character creator. Players have the option of picking from over 100 styles when making their perfect version of Rook, many of them capturing the high-quality nuances that come with hairstyles not typically seen in video games, like hair for Black characters.

How'd they do it? Well we got a bit of an answer today when BioWare and EA un-Veil-ed [a technical deep dive](https://www.ea.com/technology/news/strand-hair-dragon-age-the-veilguard) into Dragon Age: The Veilguard's hair technology, which describes how the studio used the Frostbite engine to simulate up to 50,000 individual strands of hair.

There's plenty of insights not shared in the piece—like the finer workings of Frostbite's tooling—but the data provided by BioWare is surprisingly robust, and offers developers a benchmark for their own hair systems in future games. As studio technical director Maciej Kurowski wrote, the system is called the "Strand Hair" rendering system (which is memory and GPU dependent) and uses a bespoke compute software rasterizer to composite hair into the frame before blending it with other opaque and transparent objects.

## The Veilguard hair system needed to render alongside far more transparent objects.

As BioWare's post explains, Strand Hair is an existing hair system in the Frostbite engine that's been used on EA's various sports series like EA Sports FC and Madden NFL.

In those games, the hair system is meant to simulate how hair works not just on the field, but often through the point-of-view of television cameras that capture depth of field. Those games however don't feature waist-length hair, hair that flows around horns on a character's head, or hair that is rendered at the same time as a billion magical particles flying out from a staff while smoke blows all around them.

According to BioWare, the final result is a system where hair attachments move "seamlessly," and the simulation and render dessellation of hair had been fully decoupled. The maximum hair length has also extended from "63 points" to "255 points," allowing for those waist-length hairstyle fantasies to come to life.

The technique, senior rendering engineer James Power wrote, involves splitting the hair into "two distinct passes," the first one being opaque, then one that's transparent. "To split the hair up, we added an alpha cutoff to the render pass that composites the hair with the world and first renders the hair that is above the cutoff (>=1, opaque), and subsequently the hair that is lower than the cutoff (transparent)," he wrote.

Before the split passes are rendered, the depth of the transparent part of the hair is rendered first, often creating the "ends" of the hair strands. It becomes a spatial barrier between transparent pixels that are "under and on top of" the strand hair. The the game renders the opaque part of strand hair, then the transparent objects.

To figure out if the shading pixel goes "under" or "on top of" the strand hair, it checks the transparent hair depth texture for information. If it's "under," the engine renders the hair and marks a "stencil bit." If it's "on top," the pixel is discarded and nothing gets rendered.

After that, the game draws transparent objects again, using the "stencil bit" to see where transparent objects weren't drawn before, allowing transparent objects to be rendered "properly."

All that detail gets extra tricky to manage in the in-engine cutscenes that populate the game. When lighting those scenes, the hair had to accommodate a wide range of lights like wide-angle lights, distant lights, etc. Thus, the game renders "hero shadows" for every Strand Hair object according to every corresponding light that is designated "important" to a shot by artists.

As you can see in an accompanying rendering of the character Bellara, the Hero Shadows create a more natural-feeling texture and preserve some of the different shades of her hair.

![Left, Bellara rendered without Hero Shadows. Right, with Hero Shadows. Note the differences in fidelity of transmission on the left side of the character head. Left, Bellara rendered without Hero Shadows. Right, with Hero Shadows. Note the differences in fidelity of transmission on the left side of the character head.](../../assets/6cfdf5b8d30e3b73.jpg)


Image via BioWare/Electronic Arts.

This does mean every single Strand Hair asset has a high memory footprint, which eats into how much memory can be allocated on other assets. The Veilguard does render fewer characters onscreen at once than most sports titles, but there's still a lot of assets vying for precious memory. Rendering the player character and the "full field" of followers has a flat GPU cost of 128mb.

Luckily, hair needs "less memory" to occupy less pixels, and the cost can be dynamically adjusted depending on what's in the scene. The Xbox Sereis X and PlayStation 5 costs apparently run around 400mb, though high-end PCs can run all the way up to 600mb. The Xbox Series S and lower-end PCs can swap Strand Hair assets for "Card Hair" assets when needed, which have lower memory footprints and allow other high-fidelity assets to render properly.

"To ensure we meet our frame time requirements, we set a maximum frametime budget for strand hair rendering for consoles at 6.5ms for 30 FPS (33.3ms frame time) and 3ms for 60 FPS (16.6ms frame time) with eight strand hair assets on screen," Power wrote. "Our hair resolution control will adjust the resolution within a minimum and maximum resolution based on our upsampler and DRS settings and keep the hair costs proportional to those targets. This is important since hair does not go through upsampling, as mentioned earlier, and will not have its load reduced by those technologies."

Hair renderings done on GPU tend to hvoer around 2ms, with some spikes to 5ms "depending on the complexity of the hair."

## Beauty is in the eye of the beholder

BioWare's impressive hair technology spotlights how the battle for high-quality, realistic graphics has now pushed into the need for intricate solutions to render seemingly ordinary actions and objects. The average player won't think much about the fact that characters in Thedas suddenly have much longer hair—but the one who wanted to live their full [Ariana Grande fantasy](https://www.allure.com/story/ariana-grande-long-hair-secret) now have that opportunity.

Though further graphical advancements may be more and more invisible to the eye, they won't require any less hard work than the kind shown off by Power, Kurowski, and their colleagues.