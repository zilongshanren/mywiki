---
title: Generating Tilesets with Stable Diffusion
url: https://www.boristhebrave.com/2025/02/04/generating-tilesets-with-stable-diffusion/
author: Boris
published: '2025-02-04'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

Recently I’ve been playing around more with gen AI techniques. I thought I’d try to generate a set of tiles that all connect together. It’s harder than it sounds – Stable Diffusion is hard to control, so there’s no easy way to get a set of images that are fully consistent with one another.

I’ve developed a technique for doing it that I’ll call **Non-Manifold Diffusion **as it involves doing diffusion over a set of patches that interlock to form a [non-manifold surface](https://blender.stackexchange.com/questions/7910/what-is-non-manifold-geometry).

Table of Contents

My older project [Resynth Tileset](https://github.com/BorisTheBrave/resynth-tiles/wiki/Tutorial) aims to do something similar, but using texture synthesis techniques instead of Stable Diffusion.

[MultiDiffusion](https://multidiffusion.github.io/) addresses generating images where different regions use different prompts, and generating a large image from several smaller generations.

There are various other modifications of Stable Diffusion that are aimed at splitting up generation of large images on graphics cards with low VRAM. These typically split up the generation into chunks 1 which are evaluated separately, similar to my technique. In particular, I use techniques similar to

[Tiled VAE](https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111/wiki/Tiled-VAE).

[Diffusion Illusion](https://diffusionillusions.com/) also generates multiple images that connect together in different ways. But it uses Stable Diffusion to define the loss for an optimization function, rather than running the model forward to denoise the image.

I aim to generate a [Marching Squares tileset](http://www.boristhebrave.com/permanent/24/06/cr31/stagecast/wang/2corn.html), though any layout would work with the same technique.

The idea is to generate a given tile, we’ll treat it as an in-fill generation, where we ask stable diffusion to fill in the middle tile of a 3×3 map of tiles called a **patch**. The eight surrounding tiles are appropriate ones drawn from the same tileset.

![](../../assets/6a2cc6b290326ff5.png)

Of course, this is a chicken and egg – how do we set up the surrounding tiles from the tileset when nothing has been generated? The trick is that we run all the generations in parallel. Stable Diffusion works by starting from random noise, then in a fixed number of steps *denoising* the the image until the desired result forms.

So we can start with a complete tileset of tiles filled with noise. Each step, every tile gets denoised using a patch formed of tiles from the previous step surrounding it. In principle, this means that all the tiles are generated together referencing each other 2.

The idea of a marching squares tileset is that each corner is labelled with one of two “terrains”, and the tile image smoothly transitions between all the corners. To make Stable Diffusion do this we load two different prompts, and do the denoising twice. The denoising updates are smoothly blended using a per-tile mask.

![](../../assets/31c1c690de313b9d.png)

This technique is largely unchanged from [MultiDiffusion](https://multidiffusion.github.io/).

The denoising process of Stable Diffusion doesn’t work directly on RGB images, but rather latent-space images. So the final step after denoising is to apply the VAE decoder. Unfortunately, the decoder is also not designed with consistency in mind. If you run the decoder on several different images, it’ll separately decide brightness/contrast for each of them, leading to obvious discontinuities between tiles.

![](../../assets/e317922385792836.png)

To fix this, I borrow a technique from [Tiled VAE](https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111/wiki/Tiled-VAE). This project identifies the [GroupNorm layers](https://pytorch.org/docs/stable/generated/torch.nn.GroupNorm.html) as the source of this inconsistency. These layers compute the mean and standard deviation of some features of the image and use that for normalization. Instead, I substituted a custom GroupNorm that computes mean/stddev across all the images, and shares the same value across all of them.

Here are some tilesets I made (scaled down from their original 512×512 view. I’ve arranged the 16 tiles of marching squares in a horizontal standard layout illustrated.

![](../../assets/3898c4d9c48a0305.png)


![](../../assets/3898c4d9c48a0305.png)

![](../../assets/f48b76a47e7b38ab.png)


![](../../assets/f48b76a47e7b38ab.png)

![](../../assets/a41cbb82dd5689bf.png)

Click to zoom in on the tilesets. The quality is pretty poor once you inspect the detail – some part of this process seems to degrade stable diffusion.

1) Despite the shared GroupNorm, it still seems that the separate tile generations look slightly different from each other and have visible transition lines, making the tile grid too obvious. Possibly this is because of GroupNorm’s in other parts of the stable diffusion process. Or it could be other globally shared data, like the attention keys, or issues with SD’s VAE which can [smuggle global data](https://news.ycombinator.com/item?id=39215242).

2) More fundamentally, even if the generation was perfect, that would only ensure the tiles fit together in latent space, it’s still possible to end up with problems when decoding back to RGB. Possibly some sort of averaging across tiles would help.

3) I found stable diffusion still hard to control. The base models are not really designed for textures, so don’t tend to produce images that can tile and blend well. When I tried a brick pattern, it wasn’t smart enough to realize that should have a very sharp transition to non-brick textures.I expect a better prompter / fine tuner than me would have no problem here.

4) Stable Diffusion designed for 512×512 images, and doesn’t work with smaller. So I usually scaled down after a slow and expensive generation!

Sometimes even 512 pixels seems to cause problems, it often gave very flat images when tiles wrap on both axes. I think it’s the GroupNorm giving problems again – nine copies of the same noise pattern will give an unnaturally low standard deviation. I fixed this by handling this case using [circular padding](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html) (wrapping) instead of literal copies of the same tile as padding, but it’s a bit of a hack.

![](../../assets/a2694deeec97a4bc.png)

![](../../assets/f7f21022c2f3e217.png)

I think this project is an interesting start, but the results are not that high quality. Getting some good results takes more fiddling than I’m prepared to go for.

There’s some obvious features that could be added to make this a production system, such as supporting [other tilesets](https://www.boristhebrave.com/2021/11/14/classification-of-tilesets/) or having better control over the mask.

But most importantly we need to ensure the tiles are actually seamless with each other, which means resolving points 1 and 2 in the limitations.

- These chunks are often called “tiles” in the ML world, but they not the same concept as the gamedev “tiles” I generally refer to. The former are a specific slice from a larger image, while the latter are distinct images, that are designed to be placed adjacently in various combinations.
[↩︎](https://www.boristhebrave.com#9044100c-7594-4842-b801-17f1abe4ca8e-link) - It’s worth noting that you do not
*need*parallel denoising. My older project[Resynth Tileset](https://github.com/BorisTheBrave/resynth-tiles/wiki/Tutorial)simply generates the tiles in a fixed order that has no cycles in dependencies, using wrapping (circular padding) to bootstrap the first few tiles. I haven’t experimented which approach is superior.[↩︎](https://www.boristhebrave.com#2a91f90f-6b8d-4370-8cd6-7a6d7db2d5d9-link)