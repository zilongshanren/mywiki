---
title: Generative Generators
url: https://www.boristhebrave.com/2023/12/03/generative-generators/
author: Boris
published: '2023-12-03'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

This is a experiment I tried out for [ProcJam 2023](https://itch.io/jam/procjam2023). I wasn’t getting great results from it and got bored after a few days, but I’ve decided to share what I did manage.

The rules of the hackathon were changed this year, ruling out most forms of AI. I was thinking – what’s the furthest I can push that rule without crossing the line?

In the end, I designed a system where we used AI to design and build a standalone classical generator.

## Procedure

Specfically, I created a setup like this, modelled after GAN architecture.

### Generator

First I made a procedural image generator. It’s written in javascript. It has no AI components, instead I used a simple tree generation algorithms instead. It takes as input a set of parameters, for colors, branch probability, etc.

The generator is incredibly simple. It draws a solid blue background, and then a short line sprouting from the bottom, forming the trunk. That line has a randomized angle, and a randomized chance of forking into multiple lines. The process is repeated, with each branch randomly forking and twisting.

I included parameters for controlling the angular change, color, termination probability, length and thickness of the branches. All parameters were supplied in sets of 4 numbers, and the actual parameter was interpolated from those based on the number of iterations. This meant that the paramers could change from top to bottom of the tree (e.g. branches can get thinner).

A typical output looks like this.

![](../../assets/6b8113f0f85d1f9c.png)

### Optimising the Generator

I then made a wrapper in Python. The wrapper takes a set of parameters, passes them to a headless Chrome instance and extracts a fresh image from the generator. So essentially it treats the first program as a (randomised) function mapping from parameters to images.

My goal was to make an optimiser that could pick the best set of parameters for a given task. Tuning these parameters by hand can be quite difficult for some generators.

The optimiser needs a way of scoring images. I used pre-built image classifier called [CLIP](https://huggingface.co/docs/transformers/model_doc/clip). CLIP is really handy for this sort of thing – it converts images and image captions to the same embedding, meaning they can be directly compared. So I scored the images based on their [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) to a particular assigned caption.

Because the image generator is a non-differentiable black box, it’s not possible to use a gradient-descent based optimiser. Instead, I use [evolutionary programming](https://en.wikipedia.org/wiki/Evolutionary_programming). Each iteration of the optimiser, I take the current set of parameters and randomly tweak in different directions them by the learning rate. That gives a batch of candidate parameters to try. They are each scored as above, and the best scoring parameters are selected for the next round. I make no attempt to deal with randomness – it’s easier just to increase the batch size. Then in later experiments I fixed the seed to reduce the computation required.

## Results

Here is the evolution for 150 steps for description “`oak tree`

“.

It’s certainly got some details right – the bark is brown and the leaves are green. Here’s “`palm tree`

“

The colors are more beach colors than accurate to the tree. Presumably most palm tree photos tend to be on beaches. But it’s clearly understood this is a straight and narrow tree.

One more, here’s “`coral`

“:

## Conclusion

I got bored with the project pretty swiftly, so didn’t really investigate it as much as I should have. I think it’s working, even if the results are not much to look at.

But it’s not really working well and there’s a couple of reasons for that.

One reason is that the image generator is pretty low quality. My generator has a tiny number of parameters (36) and it’s not really capable of an interesting range of images. That means there’s not much for the optimiser to explore. All the colors are very saturated, because I hard-coded a very bright background color. In a real GAN setup, the generators are much more complex.

With the palm tree example we also saw that the image classifier was a bit confused. I think it includes features common to photos of palm trees. That’s a classic AI failure mode, but I think I’ve probably exacerbated it by having my generator make such poor images. My images are well outside of distribution for CLIP, it likely struggles to identify a tree at all. Fortunately this optimization process only cares on the relative score, so the procedure still works, but it’s bound to cause some quirks.

Performance was another limiting factor. The above evolutions only use 20 images per generation. There’s a lot of scope for improvement here (I only ran a single instance of chrome, and my GPU could be better). This tiny amount of images was sufficient for a small parameter generator with a fixed seed, but if I was to apply this to a more real example I think it would require some attention.

It’d be fun to try this again, say with a generator like [SpeedTree](https://store.speedtree.com/) and some real compute.