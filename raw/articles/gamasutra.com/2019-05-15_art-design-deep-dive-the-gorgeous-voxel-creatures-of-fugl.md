---
title: 'Art Design Deep Dive: The gorgeous voxel creatures of Fugl'
url: https://www.gamedeveloper.com/art/art-design-deep-dive-the-gorgeous-voxel-creatures-of-i-fugl-i-
author: Game Developer
published: '2019-05-15'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

The Gamasutra Deep Dives are an [ongoing series](http://gamasutra.com/deepdives) with the goal of shedding light on specific design, art, or technical features within a video game, in order to show how seemingly simple, fundamental design decisions aren't really that simple at all.

# Who:

My name is Marco Peschiera, and I’m the art director of the upcoming [Fugl](https://store.steampowered.com/app/643810/Fugl/).

# What:

Modeling and animating voxel creatures living within the different biomes of Fugl, a relaxing, free-roaming sandbox game where players take on the role of a shape-shifting bird.

# Why and how:

In Fugl, every creature, aside from the player’s avatar, is animated using frames. Each frame is a separate voxel model representing a segment of the animation. The majority of the creatures have 4-6 frames that loop in place, creating a specific movement or action for the creature. This is designed to make the creature look natural and fluid, like a living being in this voxel world.

When the frames are looped together it looks like this:

For software, I use Magica Voxel (by [@Ephtracy](https://twitter.com/ephtracy)) to create all my work. It allows me to group frames together and be able to cycle through the frames as I tweak them.

The creatures in Fugl have a variety of movements. To name a few: hopping, walking, running, swimming, flying, attacking, etc... These movements help identify the creature and really bring the biomes to life.

Before an animation is made, the creature is created in a passive pose. These are the default poses from which the creature is animated. Here are some examples:

### Standing (land)

![](../../assets/3c2210d8ddf084c2.img)



Soaring (air)

![](../../assets/3c2210d8ddf084c2.img)

![](../../assets/1af4d8b53ecbce44.img)



Floating (water)

![](../../assets/1af4d8b53ecbce44.img)

![](../../assets/afecc75a17427baa.img)

After the creature has been modeled and colored, the animation planning starts. Sometimes, I’ll use real life references depending on the creature. I’ve also sketched out the frames on a sheet of paper to later model them on my MacBook. A third option would be to place the frames side by side to help get more accurate movements. Like this, for example:![](../../assets/7a53f8ff7fa38169.img)

![](../../assets/01eef80f8f4eb733.img)


Once the animation’s finished, it can be used as reference for the general movement of a similar creature, and that movement can be modified to fit a new creature if needed.

Creatures seem more alive when they have a lot of moving parts. Sometimes, the movements should be subtle, like just on the neck area, for example. Other times, the movements are more distanced from each other, like moving limbs. It’s also good to keep in mind the type of material or texture the voxels are representing, like feathers or fur.

The “selection” tab allows you to move body parts around and quickly improve the quality of your animation.

![](../../assets/0589c18f4a085461.img)


There is such a thing as too many body parts moving as once. Starting with the most important movements and then adding the subtle touches later has helped me keep the animation natural and less forced or artificial.

I also noticed that most animations can be based on patterns or sequences. Knowing this has helped me map movements without having to check outside references. I use single voxels as placeholders to later attach the body parts. The great thing about voxels is that all the cubes are the same size, so the voxels themselves are the standard of measurement to calculate distance between the body parts. Like this dragon, for example:

![](../../assets/28ffd866d2cc73b1.img)


There is an interesting pattern I noticed that helps give the animations a more natural feel. Sometimes, if a body part starts to move, the body parts next to it could follow in the next frame. These patterns help create a variety of different movements that could make the creature feel more alive and realistic. For example, this jellyfish expands, and then the movement continues through the following frames, as shown here.

Often, when modeling frames, slightly extending an arm or leg can make a noticeable difference and offer a better read for the movement. When using fewer frames, it’s critical to position the body parts in a way that best conveys the movement in mind.

Coloring is another huge part of how the creatures are created. Fugl is nature-oriented, and there is a realistic element to the creatures. I mostly color using gradients, as this can help different-colored body parts transition smoothly within each other. I found that gradients help make the colors appear less flat and also give the body some texture.

When the frames are colored, it can be tricky for the gradients to be consistent throughout. With 1 or 2 colors taking up a bigger area, it gives room to keep the colors consistent between frames. I normally color the rest of the frames once they have been made; this helps save time if the animation gets a lot of iterations.

Once the animation is in its finishing stages, it goes through a testing phase. Basically, the animation is checked from different angles to make sure all the voxels are colored-in. This checking procedure also helps fine-tune and smooth out certain areas where there is an excess or a lack of voxels. Some areas just need tweaking for the overall movement to look more coherent.

Once the animation’s finished, I normally make a GIF to keep as reference. This helps me for future animations. When I’m having trouble figuring out how specific body parts should move, it helps to look at past work to see what has worked for me before.

Animating voxel models with frames can definitely be time consuming. It’s best to plan ahead by sketching your frames on paper and preferably using fewer frames if they are able to effectively display the desired movement. I found it very helpful to place a voxel in all four corners of the model to always know where to come back to if you need to rotate, flip or loop the model.

# Result:

To conclude, animating voxels through frames seems to work well, and can produce satisfying results. Frames appear to completely bypass the unforgiving edges of the cubes. This way of animating seems to successfully achieve the illusion of fluid movement, along with the added charm attached to it.