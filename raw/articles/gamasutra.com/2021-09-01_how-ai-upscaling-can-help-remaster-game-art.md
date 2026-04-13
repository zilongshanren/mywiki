---
title: How AI upscaling can help remaster game art
url: https://www.gamedeveloper.com/art/how-ai-upscaling-can-help-remaster-game-art
author: Tommy Thompson
published: '2021-09-01'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# How AI upscaling can help remaster game art

*Mass Effect Legendary Edition* is one of the first high-profile titles to use AI texture upscaling, but how does it work?

![](../../assets/1dc5932cba6bca38.png)


'AI and Games' is a crowdfunded YouTube series that explores research and applications of artificial intelligence in video games. You can support this work by visiting my [Patreon ](http://www.patreon.com/ai_and_games)page.

With each new generation of videogame hardware, the graphical quality of new titles continues to mature. Many older games are being revisited through re-releases and remasters or they're made available once again on modern hardware. While they can be rendered at higher framerates and resolutions they're fundamentally limited by the textures developed by artists for the game. So what if we can use AI to update the textures from older games so that they're larger, crisper and more detailed for running at higher resolutions?


Today we're taking a look at a process referred to as super-resolution: where you feed an image into a trained deep learning algorithm and it generates a version of that image at a higher resolution while maintaining the artists original intent. We'll take a look at how it works and the games that have benefitted from it, ranging from AAA titles such as the recent Mass Effect Legendary Edition, but also the modding communities that have pioneered this idea over the last couple of years.

Why Do We Need Texture Upscaling?

So let's start by explaining a little bit of how graphics works in games and why super-resolution for textures can prove valuable. In two-dimensional games, objects are put together courtesy of pixel art that is used to represent the player character, the background environment and everything else in between. Moving characters will have a sprite atlas, that allows you to swap out the active sprite at runtime to convey a change in behaviour. However, for three-dimensional games, objects are now comprised of multiple elements. The two key elements are the model and its textures.

![This image has an empty alt attribute; its file name is TextureUpscaling-1-1024x576.png This image has an empty alt attribute; its file name is TextureUpscaling-1-1024x576.png](https://www.aiandgames.com/wp-content/uploads/2021/08/TextureUpscaling-1-1024x576.png?width=1280&auto=webp&quality=80&disable=upscale)

Any object in a 3D game, be it a character, prop or environment is effectively blank upon creation. The model is sculpted by a 3D artist and then it is textured to give it detail. But there's more than one texture applied to any given object. While there is the main detail, typically referred to as the diffuse texture, there are additional textures used to help render that object in different light conditions. This includes your normal map for adding vertex details, a specular map for controlling colour and an emissive for non-cascading glows. This process has evolved in the past 10 years or so given the adoption of Physical Based Rendering or PBR in the likes of Unreal Engine. But while the workflow has slightly changed, the practice of applying multiple textures for surface and then details to a model is the norm.

![This image has an empty alt attribute; its file name is matthew-syrett-stylizedstonefloor02-1-1024x576.jpg This image has an empty alt attribute; its file name is matthew-syrett-stylizedstonefloor02-1-1024x576.jpg](https://www.aiandgames.com/wp-content/uploads/2021/08/matthew-syrett-stylizedstonefloor02-1-1024x576.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Now one of the big differences between 2D and 3D games is that 2D games largely hold up over time given the aesthetic of the sprite art. Plus those games are designed to be rendered at a fixed resolution, you can't really change the resolution without skewering the art. So when they're brought over to modern platforms, there is typically some form of scaling going on that helps retain the original aspect ratio, even if it begins to look a little chunky on modern screens and there are options for smoothing it out. However, this pixelated chunkiness (yes that's the scientific term for it) is exacerbated when you try to run older 3D games at higher resolutions. Rendering a 3D game at a higher resolution will result in the models looking sharper and ultimately presenting a more crisp image, but the textures used on those objects begin to look really bad. They look stretched out and heavily pixelated. Why? Because those textures were designed to support the game at the target resolutions for when the game launched. Nobody working on DOOM back in 1993 figured that people would be playing that game 30 years later on a 32-inch 4K widescreen gaming monitor. It was built to support the graphics and memory capabilities of the hardware at that time and the monitors it would have rendered on. Even games from the last 20 years dating back to the Nintendo Gamecube, Playstation 2 and original Xbox suffer the same fate given the limitations of the hardware.

![This image has an empty alt attribute; its file name is TextureUpscaling-2-1024x576.png This image has an empty alt attribute; its file name is TextureUpscaling-2-1024x576.png](https://www.aiandgames.com/wp-content/uploads/2021/08/TextureUpscaling-2-1024x576.png?width=1280&auto=webp&quality=80&disable=upscale)


More modern games have been able to work around this, given artists will typically build the original textures at a higher resolution than the target hardware. Hence a game receives a high-resolution texture pack as a DLC update or patch on Playstation 5 and Xbox Series X, because while it shipped with 1080p textures on the Playstation 4 and Xbox One, those were already downsampled from the original 4K textures made during development. Downsampling textures is a common practice, especially for multi-platform games targeting different resolutions and memory budgets. You are making a smaller texture that is less sharp an image but retains all of the core detail of the original while minimising pixelation or artefacts. While this is a relatively straightforward process in modern game engines and related tools, you can't go the other way: you can't make an original texture bigger without it looking chunky or blocky. And that's where the AI comes in.

AI upscaling attempts to reproduce the original image at a higher resolution, while minimising the pixelation and artefacts. This is achieved using a machine learning model that understands the underlying details of that image and can refine it as it is made bigger. Now it can't *add* information that isn't already there, so for example blurred illegible text written on signs can't be made legible, given it doesn't know what it said to begin with. But it can remove a lot of noise and grain from an image such that it is sharper and less pixelated. This can be applied either to sprites and art for classic 2D games or all of the different texture layers used in 3D games. And we're going to be focused on 3D games for the remainder of this video. In conjunction with all of this, there is ongoing work in texture synthesis: where AI is being used to figure out how an existing texture would have been drawn if it had a bigger canvas to work with, but that's a topic for another time.

![This image has an empty alt attribute; its file name is TextureUpscaling-3-1024x576.png This image has an empty alt attribute; its file name is TextureUpscaling-3-1024x576.png](https://www.aiandgames.com/wp-content/uploads/2021/08/TextureUpscaling-3-1024x576.png?width=1280&auto=webp&quality=80&disable=upscale)


Texture upscaling is slowly becoming an industry in and of itself, with many companies such as Topaz Labs now selling their own software for super-resolution, denoising and sharpening images and even videos - given they are after all a series of static images creating the illusion of movement. Meanwhile, Nvidia has their own NGX development tools for upscaling and more that are designed to run on an RTX-capable GPU and Adobe has recently integrated a super-resolution feature into their Camera Raw program. Plus as we'll see in a moment, many of the tools to start building your own super-resolution AI are freely available online and as such, many modders have started applying it to their favourite games.

## Texture Upscaling vs DLSS

Now all of this sounds pretty exciting, but it also sounds very similar to what is known as DLSS - Deep Learning Super Sampling. DLSS is an upscaling technology developed by Nvidia that runs on their RTX graphics cards. While similar, there are some differences and how it executes and it's worth clarifying what those are.

Deep Learning Super Sampling essentially achieves both upscaling of the image as well as some anti-aliasing, but it's upscaling from the output of the systems graphical processing unit or GPU. DLSS is designed with the intent of allowing the graphics card to render the game while you're playing it at a lower resolution than normal, meaning it uses fewer resources, and then the AI part upscales the image before it makes it to your screen. So you might have your GPU render the game at 1080p and then the DLSS upscales that image to 4K to appear on your monitor. This is because the DLSS has a model trained for that game that knows how it should look at a higher resolution.

![logo in a gray background |](../../assets/380f76f88c218549.png)



However, texture upscaling is all done in advance: you uprez the textures in the game during development, and then use it to replace the existing texture assets stored in the game engine. Naturally, this now means an increase in required GPU power and memory, given you're now rendering higher resolution images, but none of the upscaling processes are happening at runtime. It was all completed long before the player ever got their hands on the game.

If you are interested in finding out more about DLSS, check out our future AI and Games article that compliments this one as we go into detail on DLSS and how that works as well.

## How Does Texture Upscaling Work?

Okay, so let's get into the weeds: how does texture upscaling actually work? It's reliant on deep learning: a process that uses deep convolutional neural networks that are trained to upscale the image. But more specifically, it's reliant on a technique called Generative Adversarial Networks and there's not just one, but two networks at play. One network is attempting to upscale the image to a higher quality, while the second acts as a critic, assessing how good the images are and determines where they are fake or not. If they are deemed fake, then they are discarded. This process of generator and discriminator is critical to the process: both networks need to learn about the images they're dealing with. The discriminator needs to be able to identify images that evoke specific properties, while the generator needs to create new images that retain those artistic values sufficiently such that they can fool the discriminator.

![This image has an empty alt attribute; its file name is ESRGAN-architecture-1024x169.jpg This image has an empty alt attribute; its file name is ESRGAN-architecture-1024x169.jpg](https://www.aiandgames.com/wp-content/uploads/2021/08/ESRGAN-architecture-1024x169.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Now many of the examples we see throughout this video, are driven by a particular type of Generative Adversarial Network: an ESRGAN - or Enhanced Super-Resolution Generative Adversarial Network. The ESRGAN generator is powered by a convolutional neural network, using convolution layers to capture information about the original low-resolution image. As that image is passed in, it's capturing what is known as the 'feature space'. This is a collection of properties used to describe specific patterns in the image. Whether it's fur, or brick or any other common property or trait of that image. The convolutional layers are being used to process all of that information and store it such that when the super-resolution image is made, that new image will still retain that same feature space. So with this information captured, the generator begins to upscale the image to create the super-resolution image.

![This image has an empty alt attribute; its file name is Monkey1.png This image has an empty alt attribute; its file name is Monkey1.png](https://www.aiandgames.com/wp-content/uploads/2021/08/Monkey1.png?width=1280&auto=webp&quality=80&disable=upscale)

Now typically, a GAN's discriminator is interested in detecting fake input: that an image from the generator is not real and an attempted forgery of the training set. Instead, the ESRGAN uses what is referred to as a relativistic discriminator: meaning it assesses whether an image could be considered more realistic than the other one, rather than whether the image is fake. This is a small but critical distinction, given it's more interested in assessing the difference between the real input and fake output. This actually helps the ESRGAN learn more efficiently, given it can better differentiate the key distinctions between the original image and the fake one and focus on reproducing those in the final image.

The modified discriminator combined with changes to the generator GAN structure lead to one of the big benefits of ESRGAN compared to other Super Resolution GANs: it does a better job of retaining sharpness and detail in textures. A lot of existing methods would suffer from the significant blurring of things like fur, whiskers and hair or would lose detail in elements such as brickwork or tiling. These changes made a huge improvement to the overall performance.

Now while this technique works really well, it's still not perfect. A lot of super-resolution really benefits from high-quality images to begin with. So upscaling from 1080p to 4K is often a lot easier than grabbing much lower resolution images to start with. These will often result in artefacts that impact the final high-resolution image, an issue that impacts many of the projects we discuss later in the video.

All of this is of course just a high-level summary, and a list of resources on the intricacies of ESRGANs are available below for our more scholarly viewers. Now, let's start looking at the impact this is all beginning to have on the games industry.

## Texture Upscaling in Modding Communities


The boom in super-resolution has only really kicked off in the last 3 years, given the ESRGAN that we just explored was only first published back in 2018. But it's already having a huge impact in games, and much of this stems from modding communities. Many modding communities have long-established practices of providing revised texture packs for beloved games, and in many instances, there are groups of people working on new textures to replace existing ones, such as the new New Vision 1.5 mod for Deux Ex. But now there is a new wave of super-resolution mods being released where creators have ripped the original textures out of the game and passed them through the deep learning process to great effect. There are many notable examples out there such as Deus Ex New Vision 2.0 and we're going to take a look at some in a little more detail:

### DOOM Neural Upscale 2x

![This image has an empty alt attribute; its file name is TextureUpscaling-7-1024x576.png This image has an empty alt attribute; its file name is TextureUpscaling-7-1024x576.png](https://www.aiandgames.com/wp-content/uploads/2021/08/TextureUpscaling-7-1024x576.png?width=1280&auto=webp&quality=80&disable=upscale)

This mod is free to download and run with any GZDOOM installation. This made a splash in early 2018 and is reliant on Nvidia's GameWorks tools, which are a predecessor to their current Nvidia NGX, plus they used the Topaz Labs upscaler I mentioned earlier. What makes this set of DOOM textures really interesting, is that as you can see from watching the footage, the resolution has not been scaled up as high as you might expect. In fact, as the name implies, the textures here are only 2x their original size and a big reason for that was to retain their artistic integrity and clarity.

During development, they were originally upscaled all the way up to 8 times their original size, but as a result of the super-resolution process, some artefacts started to appear in the final textures and sprites. A big reason for that is that the original images are really small. As mentioned earlier, super-resolution is reliant on whatever information is already in the image and capturing that feature space. Hence you might be able to uprez a 1920x1080 image to 4k quite nicely because the base image has a lot of details to work with. However, the majority of the original DOOM textures are only 64 by 128, and some cases are 128 x 128. Hence trying to upscale them to 8 times their original size is going to result in problems as there isn't a lot of information to go on. So after upscaling to 8x their original size, they were then downscaled to 2x and then cleaned up by hand to remove any of the artefacts. Plus, any transparency masks applied needed to be resolved manually as well.

### Max Payne Remastered (Unofficial)

![This image has an empty alt attribute; its file name is TextureUpscaling-8-1024x576.png This image has an empty alt attribute; its file name is TextureUpscaling-8-1024x576.png](https://www.aiandgames.com/wp-content/uploads/2021/08/TextureUpscaling-8-1024x576.png?width=1280&auto=webp&quality=80&disable=upscale)

First released in late 2018 and received a couple of updates into early 2019. It's a notable example of ESRGANs and much like DOOM, it's a process of both automatically creating the desired textures, as well as a bit of manual tweaking.

The Remastered mod replaces around a couple thousand of the original textures, which accounts for around 95% of the original art assets from the game. The textures in this game range from a small 2x upscale all the way to 8x in some instances. This combined with a boost in resolution is rather effective and the game really does look a lot crisper and more accessible on modern devices, removing much of the blur that arises from the stretching of these relatively small textures to larger resolutions.

### Console Upscaling

Lastly, I wanted to take a moment to highlight that this isn't just for PC games. A suite of texture packs for consoles have also been appearing for use in emulators. Such as this set for Metroid Prime for the Nintendo Gamecube. There is a slow and growing community of modders provided texture sets for the Dolphin emulator, allowing you to upscale many a classic GameCube title, including the likes of Metroid Prime, Tony Hawks Pro Skater and Super Mario Sunshine.

## Examples in AAA Games

With the recent release of the Mass Effect Legendary Edition, we're beginning to see these techniques being applied by studios as part of their art production. AI upscaling was only one part of a much larger effort at rebuilding the art assets of the Mass Effect trilogy. With the likes of material shaders and particle systems being updated alongside the base character models themselves. Meanwhile, some materials were simply too low resolution to benefit from the upscaling, so they had to go in and do that themselves.

The Mass Effect trilogy was built in Unreal Engine 3, which was more than capable of handling the graphical expectations of contemporary hardware. But since the first game was released back in 2007, the rendering capabilities have increased drastically. A lot of the Mass Effect games actually ran at 720p resolution on the likes of the Playstation 3 and Xbox 360. So the textures and character models were often downscaled from their original versions. For the remaster, BioWare moved towards a later version of UE3 that could handle the original model and texture sizes and then went ahead and upscaled the original files. The move towards using AI upscaling was really one of minimising time and resources spent on the project: given the team sought to remaster as many textures from the original trilogy as possible. This was a significant undertaking, with over thirty thousand textures being upscaled to around 4x their original sizes.

![This image has an empty alt attribute; its file name is TextureUpscaling-9-1024x576.png This image has an empty alt attribute; its file name is TextureUpscaling-9-1024x576.png](https://www.aiandgames.com/wp-content/uploads/2021/08/TextureUpscaling-9-1024x576.png?width=1280&auto=webp&quality=80&disable=upscale)


While this is achieved through an automated batch process, it requires a lot of human oversight. Especially given it's important that consistency between the likes of the diffuse, albedo and normal maps are retained, otherwise a lot of detail would begin to look broken or mangled. Even with this batch automation, the art team still went in and manually cleaned up all of the upscaled textures. In addition, many of the character models used in the remaster are based on the higher-quality versions created in the latter games, and they were used as the starting point for the remasters. But still, this required the art team to go in, manually check all the textures are up to scratch and clean them up. Plus many of the character textures received even more love as the art team sought to improve on the existing versions.

Ultimately, the AI upscaling was just part of a significant body of work to revamp all of the art assets from the game. It still requires a large amount of time and energy from the art team to spot issues arising from the upscaling, clean them up and even go in and add that detail that the deep neural networks simply cannot generate.

Plus the upscaling was also applied in other areas: some of the cutscenes also got uprezzed too. While the vast majority of the cinematics were re-rendered in-engine in 4K resolution, for some of them this wasn't possible. So they went and upscaled the original video files. This is very similar to that seen back in episode 53, where the same process was applied to the cutscenes in Command and Conquer Remastered. While the rest of the game received a hand-crafted 4K upgrade, the cutscenes utilised AI upscaling because the original video files have been lost to time.

## Closing

Texture upscaling through super-resolution is an exciting new avenue for helping games to look fresh and adapt to modern hardware configurations. While you cannot entirely revamp the image with new details or intricacies, it acts as a great starting point that you can then drop into an existing game or use as a basepoint for human artists to take over. The state-of-the-art in super-resolution is still an ongoing development, and we can be sure to see more work like this emerging in modding communities and remasters of classic games in the coming years.

## Acknowledgements

Special thanks to Matthew Syrett for use of his texture art (and models in the accompanying video).