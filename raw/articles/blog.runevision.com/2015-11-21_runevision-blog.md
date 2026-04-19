---
title: runevision blog
url: https://blog.runevision.com/2015/11/
published: '2015-11-21'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

[A Study in Composition](https://blog.runevision.com/search/label/A%20Study%20in%20Composition),

[demo](https://blog.runevision.com/search/label/demo),

[design](https://blog.runevision.com/search/label/design),

[game development](https://blog.runevision.com/search/label/game%20development),

[graphics](https://blog.runevision.com/search/label/graphics),

[procedural](https://blog.runevision.com/search/label/procedural),

[unity](https://blog.runevision.com/search/label/unity),

[video](https://blog.runevision.com/search/label/video)

Two weeks ago I participated in [Exile Game Jam](http://www.exile.dk/) - a cosy jam located remotely an hour's drive outside of Copenhagen. There was a suggested theme of "non-game" this year.

This was partially overlapping with the online [Procedural Generation Jam](http://itch.io/jam/procjam) (#procjam) which ran throughout last week with the simple theme of "Make something that makes something".

I wanted to make a combined entry for both jams. My idea was to create procedural landscapes with a focus on evoking a wide variety of moods with simple means. I formed a team with Morten Nobel-Jørgensen and got an offer to help with soundscapes from Andreas Frostholm, and we got to work.

You can download the final result here: [A Study in Composition at itch.io](http://runevision.itch.io/a-study-in-composition). You can also watch a video of it here:

Furthermore we decided to make the source code open source under the MIT license. You can see and download the [Unity project folder at GitHub](https://github.com/mortennobel/A-Study-in-Composition).

### Motivation

The motivation of the project was primarily to learn about how to create evocative and striking landscapes with simple means, particularly by creating harmonic and expressive color palettes. The name "A Study in Composition" is meant to convey this [in a similar sense as it's used in classical art](https://en.wikipedia.org/wiki/Study_%28art%29).

![](../../assets/7c7ae4fea45858b5.png)


![](../../assets/7c7ae4fea45858b5.png)

### Making the demo

Each scene consists of just a flat plane and a distribution of trees, all of it with simple colors without textures. Additionally there is a light source, variable fog amount, and sometimes a star-field. The trees are procedurally generated using L-systems and are distributed in many different ways using multiple noise functions.

#### Tree generation

Morten had created procedural trees with L-systems for previous work that we could make use of in this project. This was a huge head-start. During the project he worked on improvements such as support for leaves, a simple wind effect, and improvements to the algorithm.

#### Distribution of trees

We use a continuous noise function to distribute the trees. The function is evaluated twice - once at low frequency and once at higher frequency - and the values (between 0 and 1) are multiplied together. Simply put, this creates large clumps consisting of smaller clumps.

![](../../assets/d459339d243ac088.png)


![](../../assets/d459339d243ac088.png)

The resulting function is still between 0 and 1. For each position in a grid, we evaluate the function. The the function value is greater than a certain threshold, we place a tree.

The threshold value is different from scene to scene. We also add a random value to the threshold for each tree placement to make the edges of the clumps of trees more fuzzy. This randomness amount is also different from scene to scene. The result can create anything from dense forests to sparse savannas, and within a single scene, trees are not uniformly placed but clumps nicely in groups.

#### Color palettes

An important element of evoking different moods despite the simple means is in the color selection. First an initial color is chosen. This is done is HSV color space, where hue, saturation, and value are all values between 0 and 1. (The Value in HSV means brightness; not to be confused with lightness.)

A palette is created from the initial color by creating either a pair of complementary colors from it, or a color triad. The initial color determines the saturation and value of all the colors in the palette. This is a simple way to make the palette look consistent and harmonic.

![](../../assets/7006c091975d3adf.png)


![](../../assets/7006c091975d3adf.png)

Some extra color variations are created, and each scene element is then assigned a color from this palette. Each element knows its "normal" color and will attempt to choose a color from the palette similar to that. This will often result in natural landscapes with green grass, blue sky, brown branches, and green to red leaves. Sometimes though, nothing close to those colors will be available in the palette, and the result may be more surrealistic.

One thing I found during development was that palettes with low value (brightness) and high saturation always seemed to look bad. While I don't know for sure, my theory is that it's related to night vision. In our demo, a dark palette makes everything darker, including the sky, so it's synonymous with a darker light level, meaning dusk, overcast, or night time environments. In low-light environments, the color vision ability of the human eye becomes less effective, and the night vision ability - which is in gray-scale only - plays a larger role. So I think there's an expectation that low light environments don't have saturated colors, since our color vision is mostly out of play.

![](../../assets/df04eec2092a5c4c.png)

In any case, to avoid the unpleasant looking saturated dark colors, we simply multiplied the value (brightness) onto the saturation.

#### Soundscapes

Two thirds into the development, we showed the demo to Andreas who were making sounds for other jam projects too. In a short amount of time he managed to bang out soundscapes that added a lot of atmosphere to the demo while having zero constraints on how they should be played. The multiple pieces of sound files had different length but were each either non-rhythmical or only sporadically rhythmic, and they could be played on top of each other randomly and still sound good. The result is not always harmonic, but it intentionally uses the disharmony to create hypnotic soundscapes that interweaves between beautiful calm and eerie.

The sound files sounded fine all just playing simultaneously at the same value, but I added some extra variety by randomly adjusting the volume levels.

#### Cinematography

During development of the demo, I got tired of walking around manually using a first-person view, and pressing a button to change the environment. It seemed unnecessary to what we were doing, so we decided to make the camera movement and scene changes automatic instead. Non-games were encouraged and fully accepted in the two jams respectively anyway.

For camera movement we initially had a camera zooming fast by the trees, but following a tip from Tim Garbos to slow it down a lot made the scenes come much more to their right. Late in the process we settled on some variations of camera movement: Successive shots would vary between moving the camera forward or panning sideways left or right. It would also vary between being position at eye height (most common) or above the trees for a grander overview (more seldom).

We experimented with different ways of fading between shots. A cross-fade was impractical due to the need to have two scenes active at the same time, but we tried fading to black or white. Frequent fading detracted from the experience though. In the end we used no-frill cuts, but had every third cut be bridged by a dramatic cut to black inspired by the [opening to Vanilla Sky](https://www.youtube.com/watch?v=kagVPRjH0lE). I joked that we should win the award for pretentiousness if the jam had one.

Some tweaks were made after the Exile Jam was over, while ProcJam was still running. I made the groups of three scenes in between black cuts thematically coherent by keeping certain variables constant between them. While most variables are randomized in every new scene, the palette saturation and value, the fog amount, and the camera movement mode is only changed when a "black cut" happens. This lets you experience small variations of a theme with the black cuts resetting the senses in between changes to new themes.

### Future work

While there is a lot of ways the demo could be expanded and improved, we don't have any future work planned for this demo in itself. For me, I'm going to use what I've learned about creating variety in environments for my own other procedural projects.

We've also made [the source code for this demo available](https://github.com/mortennobel/A-Study-in-Composition) and if you do anything with it, we'd love to hear about it!