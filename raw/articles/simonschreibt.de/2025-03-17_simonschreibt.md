---
title: Simonschreibt.
url: https://simonschreibt.de/gat/the-high-heel-problem/
author: Simon
published: '2025-03-17'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This article was updated. Jump to [Update 1](https://simonschreibt.de#update1).

# Introduction

This article looks at how different types of shoes can affect game development and examines how games deal with this in practice.

Before we dive in, let’s have a look what’s possible with high heels:

[#1](https://www.youtube.com/shorts/-ymWhRhoQ2o)

[#2](https://www.tiktok.com/@blumineck/video/7282440261223992609)

[#3](https://www.youtube.com/shorts/2DriKlNOJcc)

[#4](https://www.youtube.com/shorts/L-rvdMHA9ec)

[#5](https://www.youtube.com/shorts/79n-62kQttA)

Just in case I mess up the terminology, here is a little chart:

[Character Height](https://simonschreibt.de#height) | [Posture](https://simonschreibt.de#posture) | [Animation](https://simonschreibt.de#animation) | [Optimization](https://simonschreibt.de#clipping) | [Audio](https://simonschreibt.de#audio) | [Bonus](https://simonschreibt.de#bonus) | [Summary](https://simonschreibt.de#summary) | [Sources](https://simonschreibt.de#sources)

💘💘💘 Huge thanks to [Nicolas](https://www.linkedin.com/in/nicolas-gueroux-698a2027), Damrus, [Irina](https://www.artstation.com/irinaern), [Battz](https://www.artstation.com/battz), [Magari](https://bsky.app/profile/magarigames.bsky.social), [Luna](https://www.artstation.com/lunawullaert), [Angel](https://linktr.ee/AngelCake.s) for helping with this article. 💘💘💘

# Character Height

## 🚨 The Problem

Different character body sizes mean a lot of extra work for game developers. Here’s a great example for Dragons Dogma 2, where characters with different body sizes still manage to kiss:

[#1](https://youtu.be/4s31tU19dT8)&

[#2](https://youtu.be/LK44InP2Tdo)

Here we can see how the animation is adjusted so that the lips can meet. The camera also does a lot of work:

[#1](https://youtu.be/4s31tU19dT8)&

[#2](https://youtu.be/LK44InP2Tdo)

But even if all characters have the **same** height, different shoes can influence the height of a character as well! This results in new bone positions, so that, for example, a finger no longer hits a button on the wall.

[Mixamo “Romero”](https://www.mixamo.com/#/?page=1&type=Character)

Apart from precise interactions, there may be other special cases in which heels could lead to a problem: For example, you should be careful that heels do not give the player away behind cover:

[Mixamo “Romero”](https://www.mixamo.com/#/?page=1&type=Character)

If the character’s height changes, you may also need to update the **hit collision volumes** – especially in competitive games. This depends on how the engine handles such volumes. Better double-check!

Game developers are now on a cross road. Choose wisely!

Let’s talk about option A first, where we adjust the height of the character correctly and realistically!

## 💡 Solution A: “Adjust Height”

There are three ways to deal with the consequences of the characters’ different shoe heights:

- Hope for the best
- Fix Manually
- Fix Dynamically

### 🙈 1. Hope for the best

Some games can afford to adjust the character height because there are only **few precise interactions** with NPCs or the environment. When playing Infinity Nikki, for example, I mostly found animations where it doesn’t matter whether Nikki is 10cm taller or shorter (like opening a chest):

[Infinity Nikki](https://store.epicgames.com/fr/p/infinity-nikki-71fc64)

And I can’t remember any precise interaction in the cutscenes either (e.g. a handshake). So, raising the body is not much of an issue:

[Infinity Nikki](https://store.epicgames.com/fr/p/infinity-nikki-71fc64)

However, there is one exception: I have noticed a situation in which there is close interaction: Grooming. There are two outfits for this: one **with** and one **without** heels:

[Infinity Nikki](https://store.epicgames.com/fr/p/infinity-nikki-71fc64)

I think if I look **very closely**, I can see that there is a slight clipping problem with the animation with heels. Could be due to the different terrain though. I’m not sure, but it’s definitely not a big deal.

![](../../assets/a69cd01180efd6a7.jpg)


![](../../assets/a69cd01180efd6a7.jpg)

Saints Row is another game that correctly resizes the character, and it’s the only game I’ve stumbled across where you can wear heels as a **male** character (correction see [Update 1](https://simonschreibt.de#update1)):

[Saints Row](https://store.steampowered.com/app/742420/Saints_Row/)

### 💪 2. Manual Labor

If the game needs it, animators could create unique animations (per shoe type) where e.g. the hand positions are corrected. They will love it!

*stand_groom_barefoot.fbx**stand_groom_shoe_5cm.fbx**stand_groom_shoe_12cm.fbx*

But be careful! If not **all animations** are adapted, this can lead to problems. Here, for example, a specific golf animation only seems to be available for flat shoes:

[GTA Online](https://www.rockstargames.com/gta-online)

The same happens with the drinking animation (right), which only seems to be available for flat shoes. Special cases such as motorcycling also require special attention when heels are involved:

Here’s a closer look at what happens: The feet have to strike a different pose when high heels are worn (right). Otherwise it looks funny (left):

Incidentally, the same behavior can also be seen in Nikki for a **single frame** when the shoes are swapped. The shoe mesh is replaced one frame before the pose adjusts:

[Infinity Nikki](https://store.epicgames.com/fr/p/infinity-nikki-71fc64)

### ⚙️ 3. Dynamic Systems

**Manual adjustment** is a lot of work! Isn’t there a way to automate this? For example, it would be a nightmare if you wanted to have a hand-holding mechanic and then you need tons of animations to make sure that the hands of characters with different shoe heights still meet precisely.

[Hand Holding Mechanics](https://youtu.be/x8I2Xi8bRL8)

IK to the rescue!

Modern engines offer real-time IK systems. Most players are already familiar with them, as these systems adapt the foot orientation to the terrain:

[Infinity Nikki](https://store.epicgames.com/fr/p/infinity-nikki-71fc64)

Such systems can also be used for atmospheric procedural animations such as touching a wall as you walk by:

[iHeartGameDev | Uncharted](https://youtu.be/dlQqiJYdyYM)

Or, and this is particularly exciting for our topic, to dynamically adjust the hand position in the direction of a target, so that the character itself can have a different height and/or the target can be at a dynamic height in the level:

But be careful. If the IK target is not used correctly, you may end up with NSFW animations. You have been warned!

## 💡 Solution B: “Find Workaround”

Don’t want to manually adjust all animations or use a dynamic system? No problem!

Let’s take a look at some ways to equip characters with high heels **without** changing the actual body height to get around the things mentioned above.

Again, we have three options:

- Hide
- Shorten
- Bend

### 🙈 1. Hide!

If the shoe allows it, you can “hide” your feet in the soles. This makes the leg look shorter (just like in the next section) but neither the leg nor the shoe needs to be altered:

### 🦶 2. Shorten

I have seen this solution **very often** in my research: The lower leg is simply shortened so as not to change the height of the character.

Here is an example in Sims 4, as you can see: The hip stays in place, the upper leg **doesn’t** change, but the lower leg is shortened (the angle is moved up):

[Sims 4](https://store.steampowered.com/app/1222670/The_Sims_4/)

Another example while seated:

[Sims 4](https://store.steampowered.com/app/1222670/The_Sims_4/)

The same in Watchdog Legions. However, the **shape** of the lower leg changes here as it is slightly compressed:

[Watchdog Legions](https://store.steampowered.com/app/2239550/Watch_Dogs_Legion/)

And another example, this time from Cyberpunk:

[Cyberpunk 2077](https://www.cyberpunk.net)

Normally the leg geometry is exchanged for a different one. Theoretically, **blend shapes** could also be used, but these are **expensive**.

⚠️ **Important**: Only the mesh changes, **not** the skeleton. This means that the ankle around which the foot rotates still has the same position:

This can lead to strong visual distortions like in Final Fantasy 14:

In contrast, the ankle should be at this point when wearing high heels. Of course, you can never switch to flat shoes in Nier, so they could fit the skeleton perfectly:

### 🦵 3. Bend

Here’s a nice example where synchronized character heights are very important (otherwise the lips wouldn’t meet when kissing), but **instead** of shortening the lower leg, the legs are simply **bent** a bit more:

[3D Sex Villa 2](https://www.thrixxx.com/games/)

# Posture

If you want to do it right, it’s **not enough** to just lift the hips and turn the feet into the “high heel” pose. According to [this](https://www.oceansidepodiatrist.com/blog/item/1212-the-impact-of-high-heels-on-walking) and [this article](https://www.learningmethods.com/downloads/pdf/rossi--why.shoes.make.normal.gait.impossible.pdf), the whole posture changes! The main differences:

- redistribution of body weight
- forward tilted pelvis, spine arches gently
- engaged calf muscles
- accentuated curve of the buttocks

I tried to adapt this to my zombie by doing the following (I refrained from doing a blended shape for a fuller bum though):

- Raise the hips
- Rotate the feet (so that they meet the floor again)
- Redistribute the body weight by tilting the pelvis and arch the spine

[Mixamo “Romero”](https://www.mixamo.com/#/?page=1&type=Character)

And I did a test with a walking animation. I added my posture change as an **additive** to a mixamo walking animation and it worked! Check out my sexy zombie :)

[Mixamo “IV Pole Walking](https://www.mixamo.com/#/?page=1&type=Character)

By the way #1, I noticed a little detail in Cyberpunk: when the shoe is swapped, we can briefly see how the foot pose changes:

[Cyberpunk 2077](https://www.cyberpunk.net)

By the way #2: If you want to be really precise, you should also change the orientation of your big toe, as it is often squeezed unnaturally into the shoe:

[Foot in High Heel Turntable](https://youtu.be/dq9oyn9OlgA)

# Animation

Apart from height and posture, you may also need to change the entire animation, as high heels can drastically alter the gait:

[This article](http://dyros.snu.ac.kr/project/human-gait-analysis-using-3d-motion-capture/) even provides a little graphic showing the changes. They did a lot of motion capture analysis with 12 women:

And here we are at **another** cross road for game developers!

If you’ve decided to reuse only the flat shoe animations, don’t sweat it! I’ll give you two reasons not to worry too much:

- Other developers do the same
- Even in high heels a “normal” walk is possible

### 😊 1. Other developers do the same

Most games simply reuse their animations. The only example I could find where **custom animations** are used is a Skyrim **MOD**! There, the animation of the high heels leads to a crossing of the legs and a more accentuated hip movement:

[Conditional High Heel Walk](https://www.nexusmods.com/skyrimspecialedition/mods/75174)

And yes, it is true that such a gait can be observed in real life:

[Who says men not walk in heels](https://www.youtube.com/shorts/2DriKlNOJcc)

But…

### 👠 2. “Normal” Walk in High Heels

Such a **cross-over** gait is also possible with **FLAT shoes (left)**, while a moderate cross-over (center) or no cross-over at all (right) is also possible with high heels:

[Shutterstock](https://www.shutterstock.com/video/search/models/1058618608)

So wearing high heels **doesn’t** mean that your legs **automatically** cross and your hips go crazy. But if that’s what you want and your game “only” offers flat shoes, you can still do it. Anything is possible!

By the way, not even Nikki has a unique animation per shoe and this game is all about outfits and dressing in style:

[Infinity Nikki](https://store.epicgames.com/fr/p/infinity-nikki-71fc64)

What they do have, however, are different idle animations. I counted **four different** ones, depending on which shoe you’re wearing. That’s quite a lot in my eyes:

[Infinity Nikki](https://store.epicgames.com/fr/p/infinity-nikki-71fc64)

# Optimization

What happens to the polygons of the leg when it is covered by a shoe? Good handling can help prevent clipping, and of course it’s a nice optimization.

This is what we want to prevent:

Some games hide the polygons inside shoes. In Saints Row, the legs are made up of different pieces and can be hidden if necessary:

[Saints Row](https://store.steampowered.com/app/742420/Saints_Row/)

Watchdogs is also an interesting example:

**Left**: The whole leg is a**single draw call**and it is complete (the toes are there, even though they are covered by the shoe)**Right**: same location, only with a flat shoe. Now the leg is made up of**multiple meshes**(aka draw calls). I’m not sure why, as both shoes show about the same amount of skin…. strange! But in this case, the toes are optimized away!

[Watchdog Legions](https://store.steampowered.com/app/2239550/Watch_Dogs_Legion/)

Here is a static comparison of how the game handles the reduction of polygons:

- High Heels: Full leg (with toes) is used.
- Flats: Leg made of several pieces; Toes are removed.
- Boots: Leg made of several pieces; Lower leg removed.

And cyberpunk? They just keep the whole leg, even if the boots are massive and cover most of it!

[Cyberpunk 2077](https://www.cyberpunk.net)

# Audio

Depending on whether the shoe has a stiletto heel, the steps should sound different. The same applies if you are not wearing any shoes at all (barefoot). Cyberpunk does a good job here:

[Cyberpunk 2077](https://www.cyberpunk.net)

If you’re playing a **competitive game**, high heels might give away the player’s position more easily as they’re usually louder. This could be a balancing issue!

# Bonus Work

You’ve already built high heels into your game, everything works perfectly and now you’re bored? Here are some challenges:

- Implement a real-time muscle simulation to fulfill this:
.[“The lifted heel also engages the calf muscles and accentuates the curve of the buttocks […]”](https://www.oceansidepodiatrist.com/blog/item/1212-the-impact-of-high-heels-on-walking) - If you do a life-simulation where people can get injuries, you can implement long-term side effects of wearing high heels like joint degeneration, shrinking calf muscles, nerve tissue thickening and many more (
[source video](https://youtu.be/tyeIaTJ0IEE)). Does Dwarf Fortress simulate this already? - Implement a “Sink into the ground” feature depending on the heel and soil type:

[Ultimate Heel Guards for Walking on Grass](https://youtu.be/dHlMLmL8mco)

- Implement a higher range and damage for fighters wearing high heels but also add a 5% chance that they slip and need a long pause to recover:

[#1](https://youtube.com/shorts/aj81fNQFYH0?si=SullodiHCRVwOput)

[#2](https://youtu.be/C-cqUj99zMI)

# Summary

- Supporting different shoe types may change the characters height and foot orientation (and maybe hit volumes).
- If precise interaction with the environment or NPCs is necessary, the consequences for the height change require solutions (unique animations, IK systems) or workarounds (shorten lower legs, bent legs)
- Different shoe types may also change the posture, gait and footstep sound (the latter could pose a balance problem in competitive games).
- Many games use the same animation for all shoe types (but special cases such as motorcycling or sneaking with high heels may require special attention).
- Sometimes the polygons that are covered by the shoe are removed for optimization (can also prevent clipping). Usually meshes are swapped as blend shapes are too expensive.
- A graceful gait (crossed legs, accentuated hips) is also possible with flat shoes, while a “normal” gait is also possible with high heels.

# History Lesson

Originally, men started wearing high heels and then women adopted – * “it was in an effort to masculinise their outfits”*.

![](../../assets/50d769d1361236e7.png)

# Sources

## Articles & Studies

- The Impact of High Heels on Walking
[https://www.oceansidepodiatrist.com/blog/item/1212-the-impact-of-high-heels-on-walking](https://www.oceansidepodiatrist.com/blog/item/1212-the-impact-of-high-heels-on-walking) - Wearing high heels – Scholl Biomechanics
[https://youtu.be/xlnmvALaMZg](https://youtu.be/xlnmvALaMZg) - The influence of high heeled shoes on balance ability and walking in healthy women
[https://pmc.ncbi.nlm.nih.gov/articles/PMC6047962/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6047962/) - Human Gait Analysis using 3D Motion Capture
[http://dyros.snu.ac.kr/project/human-gait-analysis-using-3d-motion-capture/?ckattempt=1](http://dyros.snu.ac.kr/project/human-gait-analysis-using-3d-motion-capture/?ckattempt=1) - Walking in High Heels: The Physics Behind the Physique
[https://illumin.usc.edu/walking-in-high-heels-the-physics-behind-the-physique/](https://illumin.usc.edu/walking-in-high-heels-the-physics-behind-the-physique/) - Platinum Blog Near Automata
[https://www.platinumgames.com/official-blog/article/8997](https://www.platinumgames.com/official-blog/article/8997) - Walking in high-heel shoes induces redistribution of joint power and work
[https://pmc.ncbi.nlm.nih.gov/articles/PMC10291901/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10291901/)

## References

[https://www.shutterstock.com/video/search/woman-walk-side-view-heels](https://www.shutterstock.com/video/search/woman-walk-side-view-heels)[https://www.shutterstock.com/video/search/walk-side-view](https://www.shutterstock.com/video/search/walk-side-view)- Anatomy for Sculptors
[https://www.artstation.com/artwork/Vy3dXn](https://www.artstation.com/artwork/Vy3dXn) - SKAMotion 3D walk cycles
[https://www.youtube.com/@SKAmotion/videos](https://www.youtube.com/@SKAmotion/videos) - Rapa Motion Female Heels (Motion Capture Animations for Unreal Engine)
[https://youtu.be/RJWVI_6cgJU](https://youtu.be/RJWVI_6cgJU)

## Tutorials & Discussions

### General

[axyz women in heels and mocap](https://forums.cgarchitect.com/topic/72061-axyz-women-in-heels-and-mocap/)[how do devs implement changeable footwear for female characters?](https://www.reddit.com/r/gamedev/comments/1efzail/how_do_devs_implement_changeable_footwear_for/)[this is not how high heels work](https://www.reddit.com/r/cyberpunkgame/comments/sfelrs/this_is_not_how_high_heels_work/)[Conant Exiles High Heel Modder Guide](https://docs.google.com/document/d/1Z8-J7LGmXsN6epwl5MrsRo6rPvmwtuic3eyYyyMw9TI)

### Blender

- Blender rigging heels
[https://www.youtube.com/watch?v=bV2jn57oJ4c](https://www.youtube.com/watch?v=bV2jn57oJ4c) - Heel rigging in 60s
[https://www.youtube.com/watch?v=voYM3yyeZP4](https://www.youtube.com/watch?v=voYM3yyeZP4) - Royal skies rigging
[https://www.youtube.com/@TheRoyalSkies/videos](https://www.youtube.com/@TheRoyalSkies/videos) - How to Use Mixamo Animations in Blender 4.2
[https://youtu.be/F25_c-Q0_Qw](https://youtu.be/F25_c-Q0_Qw)

### Maya

- Maya Reverse Footroll Rigging
[https://www.artstation.com/blogs/dcbittorf/2ZYN/rigging-a-foot-roll-in-maya-using-a-reverse-foot](https://www.artstation.com/blogs/dcbittorf/2ZYN/rigging-a-foot-roll-in-maya-using-a-reverse-foot)

### Unity

- unity heel flat transform
[https://www.youtube.com/shorts/tLZ0cRhAjeM](https://www.youtube.com/shorts/tLZ0cRhAjeM) - Final IK: Interaction System (grabbing objects)
[https://youtu.be/RdSfLkFHTWM](https://youtu.be/RdSfLkFHTWM) - Learn Procedural Animation in Unity
[https://youtu.be/cg_vXWPaG8A](https://youtu.be/cg_vXWPaG8A) - How to handle high heel footwear in Unity characters/rigs?
[https://discussions.unity.com/t/how-to-handle-high-heel-footwear-in-unity-characters-rigs/59685](https://discussions.unity.com/t/how-to-handle-high-heel-footwear-in-unity-characters-rigs/59685)

### Unreal

- UE5 – Fix High Heels – TPS Template
[https://youtu.be/a58-dactGuU](https://youtu.be/a58-dactGuU) - Feet IK Improvement with ControlRig
[https://youtu.be/Yho2BOrBnQs](https://youtu.be/Yho2BOrBnQs) - High Heels and flat feet help
[https://forums.unrealengine.com/t/high-heels-and-flat-feet-help/147715/5](https://forums.unrealengine.com/t/high-heels-and-flat-feet-help/147715/5) - How to adapt High Heel shoe in Metahuman?
[https://forums.unrealengine.com/t/how-to-adapt-high-heel-shoe-in-metahuman/650189](https://forums.unrealengine.com/t/how-to-adapt-high-heel-shoe-in-metahuman/650189) - heels on meta human
[https://forums.unrealengine.com/t/attaching-high-heels-to-metahuman-resolved/1190673/5](https://forums.unrealengine.com/t/attaching-high-heels-to-metahuman-resolved/1190673/5) - How to add custom clothing onto Metahumans in Unreal Engine using Blender
[https://youtu.be/3_b60jkuDMY](https://youtu.be/3_b60jkuDMY) - Daz To Unreal – Dealing with Heels
[https://davidvodhanel.com/daz-to-unreal-dealing-with-heels/](https://davidvodhanel.com/daz-to-unreal-dealing-with-heels/) - Unreal Engine 5.5: Hand Holding Mechanics
[https://youtu.be/x8I2Xi8bRL8](https://youtu.be/x8I2Xi8bRL8) - Unreal Engine 4 Tutorial – Hands IK
[https://youtu.be/xsvvA042l98](https://youtu.be/xsvvA042l98) - Unreal Engine IK Rig Example Setup
[https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-in-unreal-engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/ik-rig-in-unreal-engine)

## Wearing Examples

- heels walk male/female
[https://www.youtube.com/shorts/2DriKlNOJcc](https://www.youtube.com/shorts/2DriKlNOJcc) - heels dance
[https://www.youtube.com/shorts/-ymWhRhoQ2o](https://www.youtube.com/shorts/-ymWhRhoQ2o) - extreme plateau heels jump
[https://www.youtube.com/shorts/L-rvdMHA9ec](https://www.youtube.com/shorts/L-rvdMHA9ec) - extreme plateau
[https://www.youtube.com/shorts/79n-62kQttA](https://www.youtube.com/shorts/79n-62kQttA) - fighting in heels
[https://www.tiktok.com/@blumineck/video/7282440261223992609](https://www.tiktok.com/@blumineck/video/7282440261223992609) - kicking in heels
[https://youtube.com/shorts/aj81fNQFYH0?si=aMkDqtuLvbueOWib](https://youtube.com/shorts/aj81fNQFYH0?si=aMkDqtuLvbueOWib) - convertible
[https://www.youtube.com/shorts/1pHgqF5M-74](https://www.youtube.com/shorts/1pHgqF5M-74)

## Effect on Health

[High Heels Change Your Bone Anatomy](https://youtu.be/tyeIaTJ0IEE)[What Can Happen to Your Body If You Wear High Heels Every Day](https://brightside.me/articles/what-can-happen-to-your-body-if-you-wear-high-heels-every-day-801163/)[High Heeled Shoes: A Real Pain](https://www.functionalps.com/blog/2012/12/20/high-heeled-shoes-a-real-pain/)[Why Shoes Make “Normal” Gait Impossible](https://www.learningmethods.com/downloads/pdf/rossi--why.shoes.make.normal.gait.impossible.pdf)

![](../../assets/ba0680151067ebbc.png)

Lady Estradiol explained in the comments that FFXIV lets **everyone** wear high heels (I mentioned above, that the only game I found so far was Saints Row).

I was also told that [Movie Star Planet 2](https://en.wikipedia.org/wiki/MovieStarPlanet) (a 2D dress up game) also offers the option to wear heels for everyone.

And [Noe](https://bsky.app/profile/petignome.bsky.social/post/3lknbdjwsi22k) showed an example for a special case: If the figure only wears moderately high heels or flat “ankle shoes” (no sneakers, no barefoot), then this method requires no change in the foot/leg when switching shoes:

The foot is simply **always** in a high heel position, and the flat shoes cover enough to hide this little secret.

Final Fantasy XIV does also have high heels that can be worn by both genders, particularly the 2B boots from the Nier crossover.

Thank you for the comment! I didn’t know that it can be worn by anyone. I will update this in my article :)

Great article, what is the best example you have come across of high heel implementation in games? And have you found any games where your bonus ideas have been implemented?

Hey :) I think the best Example is Nikki and Saints Row, but both do not seem to have precise Character interaction with other NPCs/Environment so maybe it was feasible for them to actually adapt the height. I don’t think that there is a game with my bonus ideas. If there would have been, I would have mentioned them as example.