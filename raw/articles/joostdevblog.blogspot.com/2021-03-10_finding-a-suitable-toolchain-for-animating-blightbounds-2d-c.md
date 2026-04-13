---
title: Finding a suitable toolchain for animating Blightbound’s 2D characters
url: http://joostdevblog.blogspot.com/2021/03/finding-suitable-tool-for-animating.html
author: Joost van Dongen
published: '2021-03-10'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

For [Blightbound](https://www.blightbound.com/) our technical ambitions for the 2D animation system were quite lofty: we wanted high quality animation, screen-filling bosses, crisp character art, high framerate and swappable gear. This required a complete rework of our animation pipeline, since the sprite sheets we used in [Awesomenauts](https://www.awesomenauts.com/) and [Swords & Soldiers 2](http://www.swordsandsoldiers2.com/) allow for none of those requirements, except for high quality animations. In today’s blogpost I’d like to explain the problems we faced, and what combination of tools we chose to solve them. This is the first half of a two-parter: next week I’ll discuss our skin editor and its implications on animation.

![](../../assets/647eded9f1e6139c.jpg)

*Blightbound features huge screen-filling bosses that need to animate smoothly without taking up insane amounts of memory.*

Traditionally 2D animation in games is done using sprite sheets. A sprite sheet is simply a big texture with all the frames for all a character’s animations in it. Sprite sheets aren’t limited to just character animation: they can also store other things, like special effects or plants. The frames might be in a grid, or spaced more efficiently like we did for Awesomenauts. In any case, it’s just a series of tightly packed images.

Sprite sheets are great because they allow for complete freedom. The animator can draw anything they like and it will just work. Extreme squash-and-stretch? Perspective changes? Morphs? Do as you please, to the game it’s all just images!

However, sprite sheets come with a few huge downsides. First is size. If you have a big character and want it to be crisp and high-resolution, then each frame is going to take up a lot of space. Having lots of large images is going to cost too much memory. In Awesomenauts this was indeed a problem for some of the characters. For Clunk to fit in one 4096*4096 sprite sheet (the maximum we chose for memory and compatibility reasons), we had to either lower the resolution a bit, or reduce the framerate. And that’s not even that big of a character! The high memory usage of sprite sheets means that screen-filling bosses either can’t be done, or need to have very few frames, or can’t be crisp.

![](../../assets/600c440fbebf17ca.jpg)

*In Awesomenauts, red Clunk occupies an entire 4k sprite sheet texture for all his animation frames. Clunk fit only after slightly downsizing him.*

The second major downside of sprite sheets is that since it’s just images, it’s very hard to do anything with them except simply showing them. For Awesomenauts we’ve often talked about letting players customise characters by changing for example their hat or other parts, but simple sprite sheets make that incredibly hard. The engine would need to know where the hat is exactly, but the sprite sheet doesn’t contain that information. Nor does it tell us whether there are different perspectives of the hat in different frames, or whether anything is ever in front of or behind the hat.

I can think of some workarounds for this problem, but it’s all so cumbersome that’s it’s not practical to actually do. This is the main reason why Awesomenauts only contains skins that swap the entire look of a character, and no swappable hats or clothing: those would be completely new sprite sheets for each combination.

![](../../assets/aff199d9e9a01a92.jpg)

*Since every skin change in Awesomenauts requires an entire new sprite sheet we decided to make full reskins instead of allowing the user to customise individual parts (like hats or weapons). These are the four looks for Ted McPain.*

So, sprite sheets can’t give us four of our requirements (screen-filling bosses, crisp character art, high animation framerate and swappable items). What can we do instead? The obvious direction for a solution is to split a character in parts, and let those parts move relative to each other. Or even to go for full skeletal animation.

If you have a background in 3D animation, you might think “*well skeletal animation of course, it’s awesome!*” And in 3D it is indeed, but in 2D it’s a lot more limited. Because we’re restricted to the 2D plane, there’s a lot of animation that can’t be done with a standard skeleton in 2D. Rotating the head of the character away from the camera is super easy in 3D, but impossible with 2D skeletal animation. Swinging a sword vertically is easy, but horizontally is very hard because that requires 3D perspective. Wanting to circumvent these limitations, we opted for a combination of 2D skeletal animation and traditional frame-to-frame animation on parts where needed.

A common tool for doing part-based 2D animation is [Spine](http://esotericsoftware.com/). Spine is used by a lot of games and we expected this to be our best option. We tried Spine and it was indeed quick and easy to use, as well as easy to integrate into our own engine. However, it turned out to be a bit *too* simple: Spine doesn’t allow swapping a part in the middle of an animation. This is needed if you want to mix skeletal animation with frame-to-frame animation, for example by switching to a different drawing of a head or hand. The workaround was to layer several skeletons on top of each other, but that was too clunky to work with. We reached out to Spine at the time, explaining this issue, and they confirmed this was the only way. Our evaluation was three years ago and we haven't tried Spine since, but according to [this post by them](http://esotericsoftware.com/blog/Rigging-new-poses-tutorial) their options for combining frame-to-frame with skeletal animation seem to have improved recently.

![](../../assets/23b3a49299772d69.jpg)

*Spine by Esoteric Software is a 2D character animation tool for games for creating animations using parts, skeletons and deformations (screenshot taken from one of Spine's tutorial videos).*

We also tried some other tools, including Blender and 3D Studio MAX, but those turned out to be too focussed on 3D to create a good workflow for 2D animation for us. Especially the nice skeletal systems they have became quite impractical when used for 2D animation.

So instead, we wanted to stick with After Effects. After Effects is mostly known as a tool for editing video and doing special effects and such, but it’s actually also just a really good general animation tool. Our artists happily used it for character animation in our previous games Awesomenauts and Swords & Soldiers 2. The basic idea is this: each part in an animation is a layer, and can be animated, linked and deformed freely. By turning layers on and off, you can do frame-to-frame animation on parts (like a hand opening and closing) or on the character as a whole.

I imagine After Effects would be a bad fit for full hand-drawn frame-to-frame animation, like in Cuphead, since After Effects doesn’t even allow drawing on layers directly (we draw all our parts in Photoshop). However, for our games it’s an excellent tool because we don’t want to redraw the entire character every frame anyway.

There was something missing though: After Effects is a great animation tool, but it’s not really tailored to 2D character animation. Good thing we already knew about the [Duik plug-in](https://rainboxlab.org/tools/duik/). Duik adds the rigging features that are common in 3D animation to After Effects. Combined with the strong tools After Effects already has, it’s a really effective 2D animation tool for games.

![](../../assets/c95abafa0db67dc1.jpg)

*Duik is an After Effects plugin that adds tons of 2D animation features (screenshot from*

[this tutorial video by Motion Tutorials](https://www.youtube.com/watch?v=jw0oxO7KWEk)).I previously mentioned we wanted to mix skeletal animation with frame-to-frame animation. That part is actually really simple with Duik. The artist just links several drawings of a part to a bone and switches which is visible. This way we can change facial expressions during animations, as well as do things like open and close hands, pivot or distort a torso and switch facial expressions.

![](../../assets/c70922dfd1c82d71.jpg)

*Thumbnails of most animation parts needed for one character in Blightbound. The various hands, faces and chests are for frame-to-frame animation on parts of the body.*

Happy with After Effects+Duik as our animation tool, another important thing was missing: After Effects files can’t be played back in real-time engines. So I set about the task of writing an exporter from After Effects that exports all the hierarchy and animation data. I also implemented the in-game side of playing that back in real-time.

At it’s core, this is a surprisingly simple task. Each part in an After Effects animation is a layer and we can just export all the layers with their animation frames and play them back. Where I went wrong though, is that I wanted to emulate Duik’s systems in-game. I thought Duik only did basic two-bone inverse kinematics and implemented that in the engine. This worked with simple animations, but for complete characters the animations were completely broken in-game. When I looked deeper I learned that Duik actually has a ton of different animation systems and approaches. Mimicking all of those in-game was totally undoable.

![](../../assets/85e2f5a655ccc02f.gif)

*Duik has so many features that only supporting parenting and two-bone IK produced completely wrong results in-game, as can be seen in this 'beautiful' monstrosity. This was intended to be a normal walk animation, early during development of Blightbound.*

Once I realised this, I went for an easy alternative: animation baking. I export the orientation, scale and position of each part at 30 frames per second, simply storing the values for each frame (unless they’re not changing). This is a lot more data, but compared to the size of textures it’s really negligible. I did keep the hierarchy of the bones, so parts don’t start to subtly 'float' compared to each other.

![](../../assets/7c32f3b78bf97ea8.gif)

*Our custom file format is simply a text file with a long list of all parts and the information needed to position and animate them correctly, including parenting and keyframes.*

I previously said we wanted high framerate. The game actually interpolates between these frames, so while they’re exported at 30fps, they’ll also run smoothly at 60fps, 144fps, or any other framerate. That’s also great for when slowing an enemy: in Awesomenauts, if you slow an enemy, you can see the low framerate of their slowed down walk animation. In Blightbound, movement remains perfectly smooth.

A note there is that whenever something needs to jump from one position to another instead of smoothly interpolating there, the artist needs to use a *hold* key. Our tool exports those and applies them correctly during playback. Overlooking this caused some bugs here and there, because artists aren’t used to needing to use hold keys when two frames are directly next to each other. In-game however there can be frames in between, so that case still needs a hold key.

![](../../assets/1b1affe292b21e10.gif)

*A few animations that Ronimo animator Tim Scheel made for the Blightbound character Karrogh.*

After Effects is a huge tool with tons of features, so it’s impossible to support them all in-game. Our exporter only supports what we actually need, and nothing else. This means our artists need to avoid using some After Effects features that they might want to use. In most cases this is fine, but one particular feature that we ended up not supporting due to a lack of time, is mesh deformations (also known as puppet pins). Being able to deform a part would have helped a lot, but we didn’t find the time to implement a good emulation of After Effects’ deformation features in-game. Quite a pity, and I wonder whether our artists have ever wished they had chosen Spine after all, since Spine supports deformations in-game out-of-the-box.

Our artists did apply a simple workaround for the lack of deformations. By doing them in Photoshop and saving them as different frames for a part, they work fine. Technically the engine then thinks it’s frame-to-frame animation, but it’s actually deformed instead of redrawn in Photoshop. This approach wasn’t used much because it requires a lot of handwork, especially when reusing animations on several characters, but it does get the job done when needed.

![](../../assets/cbe9c1703769418a.gif)

![](../../assets/01b61e3621c24699.jpg)

*The chest deformation in this animation from Blightbound was made by deforming the chest part in Photoshop and then exporting it as separate parts.*

From a memory perspective the result of our toolchain is pretty impressive. Whereas a single Awesomenauts character can take up 16mb of texture space (excluding skins and the blue team), all Blightbound characters and enemies together use only 65mb of texture space, spread out over 4,600 character parts. On top of that, Blightbound animations are much higher resolution and higher framerate and we can swap parts and weapons dynamically.

What we have so far is strong animation tools (After Effects + Duik) and a way to play animations back in-game. This is enough to make a playable game, but we wanted considerably more: easy reuse of animations between characters, equippable gear, attaching special effects to bodyparts and efficiently handling thousands of character parts. In next week’s blogpost I'll dive into how we achieved those goals using our own skin editor.

*Special thanks to Ronimo artists Koen Gabriels and Gijs Hermans for providing feedback on this article.*

Awesome to read that you also went this way. My main gripe with Spine was that it handled full scenes poorly, and I was planning on using it for animating level end dialogs and for instance flashy in-game shop promotions.


ReplyDeleteI’m using a crude system based off of BodyMovin’. It exports a JSON doc and copies the associated images. It can do background, color, easing, embedded movieclips (to accomplish that, it instances another AETimeline with a clip rect) and of course scale rotation position skew. We can add text labels that contain a localizable ID and then display them at the correct font size in-game.

Our format is a bit different. We actually generally save the keyframes and mimic the interpolation style. Only spatial velocity-based interpolation was too cumbersome to port, so those are dumped by frame :-)

On our own project, it never became more than a cool addition, because it wasn’t needed for the core content pipeline. We also didn’t need the skeletal system, but that seems very cool. I think it’s awesome that we worked on the same stuff (if only we knew, we could have helped each otger :-) and it’s cool to see that you fully integrated it into the workflow.

I’m sure your 2nd article will take this even further. A true inspiration!

[trying to post again because blogspot isn’t showing any feedback on submit]

Thanks for sharing, Luc! BodyMovin' looks like an interesting tool, could have been useful for us!


DeleteThe reason we only do individual animations in After Effects (characters and frame-to-frame special effects) is that we also have an in-game editor for animations. We use this for the bigger full scenes that you mention, as well as for lots of other stuff. This way we can add things like particles, sounds, dummies and text and be sure they render exactly like they will during gameplay. For example, texts in the animation editor use our localisation system, so they update in the editor based on what language you're playing in.