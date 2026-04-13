---
title: Player model and animations
url: https://etodd.io/2014/03/31/player-model-and-animations/
published: '2014-03-31'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Player model and animations

One concern that pops up a lot on [Greenlight](http://steamcommunity.com/sharedfiles/filedetails/?id=239551444) is the low quality of the player model and animations in Lemma. The reason it's so bad is that I did all of it myself, and I'm not a character artist. People ask, "but couldn't you just try harder? What's so hard about modeling and animating a character anyway? Also, couldn't you just borrow an existing public domain model?"

Come, join me as I weave a wondrous tale of artistic achievement. It is the story of the current Lemma player model:

![Weeee!](../../assets/39bb0c49c7a127c5.jpg)

The story starts with modeling. The current player model consists of over **10,000** 3D points connected by over **20,000** edges. Being a novice Blender user, I wasn't about to attempt all that myself.

![](../../assets/b2b97eff61d6e92d.jpg)

Luckily, there's a great open-source project called [MakeHuman](http://makehuman.org/) that can generate all kinds of human models. You can tweak parameters like gender, height, weight, nationality, muscularity, facial features, and more.

I generated a suitable model, imported it into Blender, and made a few tweaks to fit the game's needs.

The next step was texturing. Normally I would have to painstakingly map each 3D point on the model to a 2D point on a texture surface (a process called "UV unwrapping"). Luckily, the model came with pre-generated UV coordinates, so only a few minor modifications were necessary.

However, the default textures didn't include clothes, so I used [GIMP](http://gimp.org/) to overlay some cloth textures. I also baked in some [ambient occlusion](http://en.wikipedia.org/wiki/Ambient_occlusion) for a bit of added realism.

![There's more than one way to skin a character model.](../../assets/6c7dc14d0514c8b2.jpg)

The next step is to add controls so that I can animate the character. Similar story here. Normally I would have to first create a skeleton of bones that roughly matches the shape of the model, then painstakingly assign up to **four numbers to each of the 10,000 vertices**in the model. These "weights" determine how much each vertex is affected by each bone. Thankfully, MakeHuman once again did the heavy lifting. However, the few modeling tweaks I made earlier had to be properly weighted, and even that was not easy for a novice like me.

![The green vertices will be affected by the forearm bone.](../../assets/892cb67164a0f650.jpg)

Finally, we're ready to animate this monstrosity! Over the course of development I've accumulated 34 poses and animations.

![](../../assets/54d1684ba392743c.jpg)

The animation code can blend between animations and even layer two different animations on top of each other. For example, the bottom half of the model can play a walking animation while the top half answers the phone.

Each animation contains [keyframes](http://en.wikipedia.org/wiki/Key_frame) that indicate the position, orientation, and scale of each bone. To make the player turn around, I could make a keyframe at 0 seconds with the model facing forward, and another keyframe at 1 seconds with the model completely turned around. The code would blend the two keyframes into a smooth turning animation. Easy enough, right?

Not so much. Here's just part of the "kick" animation, which lasts about half a second. Each dot is a keyframe.

![It's like Excel's nasty older brother.](../../assets/fc4fd7e62a925b24.jpg)

Once you take into account the fact that the skeleton has 70 bones, even simple animations can take hours to complete.

Long story short, 3D animation is hard! Professional outfits these days use motion capture, but even that requires weeks of intensive post-processing and cleanup by teams of professional animators.

Hopefully this little article gave you a glimpse into the world of game development, and hopefully you understand why I need help to bring the player model to the level of professionalism and quality that this game deserves.

Before I go, just a quick thank you to everyone for supporting Lemma, and a status update! The [Kickstarter](https://www.kickstarter.com/projects/et1337/lemma-first-person-parkour) is over **35%** funded and the [Greenlight](http://steamcommunity.com/sharedfiles/filedetails/?id=239551444) is now **73%** of the way to the top 100 games with almost **5,500** yes votes. Thank you guys!