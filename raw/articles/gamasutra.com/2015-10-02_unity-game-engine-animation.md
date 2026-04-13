---
title: Unity game engine animation
url: https://www.gamedeveloper.com/art/unity-game-engine-animation
author: Joris van Laar
published: '2015-10-02'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Unity game engine animation

Tips & tricks for game engine animation in Unity using the Legacy animation system, and when to go in-engine instead of animating in 3d software like 3dsmax and Maya.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Most 3d animators tend to swear by their preferred tools of the trade. Be it 3ds Max, Maya or Blender, each package has its own group of dedicated followers. But when it comes to animating for games, an extra player is added to the mix: the game engine.

Basic animation in an engine is not that different from a 'traditional' 3d package, but like any program, it has its own quirks. So I've tried to put together all the post-it notes that I've gathered over time on my monitors. I'd like to think of this post as a digital version of that colleague that walks up to your desk when hearing your frustrated cries and says "Oh yeah... there's an easier way for that." The examples used in this post are from Jets - Papercraft Air-O-Batics, a mobile game we at [Little Chicken Game Company](http://www.littlechicken.nl) made in Unity3d and recently launched on behalf of KLM Royal Airlines. Hopefully with these pointers I can save you some time when you decide to animate directly in-engine!

# Why in-engine?

Speed


Animating directly in the game engine can greatly improve your production speed, as you eliminate the extra step of continuously having to export from an external 3d package and importing it in the engine.WYSIWYG


It removes the risk of any 'translation' errors where the animation you originally created gets displayed differently in the engine after importing.

So why not always animate in the game engine?

Because it's simply not built for that. Even though the animation systems in engines are becoming increasingly more sophisticated, they're still quite basic when compared to dedicated packages. We chose to animate (almost) everything in the game engine, because we were working on a vehicle based game. To be more specific: a 3D endless runner with a paper plane that needs to dodge traffic in different cities over the world. Because of the lack of any characters, there was no need for complex rigs. Therefore we could get away with basic position/rotation/scale animations on the game objects.

## No bones? Go in-engine!


Another benefit of having an engine focused pipeline, is that we were able to automate the movement that brought the world to life. One of the team's developers Michiel Frankfort had made an editor that allowed us to quickly place vehicles in a game scene and with a few clicks create a path animation! To read more about Michiel and his ingenious ways check out his blog post [Doubling viewing-distance without LOD-ing or performance drop](http://gamasutra.com/blogs/TomasSala/20150929/254839/KLM_Jets_Doubling_viewingdistance_without_LODing_or_performancedrop.php)

![automated-path-animation automated-path-animation](http://www.littlechicken.nl/wp-content/uploads/automated-810x444.png?width=1280&auto=webp&quality=80&disable=upscale)


# Legacy vs. Mecanim

Even though Mecanim is now the main animation system for Unity, back when we were in development it just got introduced and was mainly geared towards humanoid character animation. So for us the choice for Legacy was quite easy, as we weren't working with any characters. But even now I can imagine teams opting for the Legacy system if they're constrained on time. Mecanim does have a richer toolset, but also has a higher learning curve and quickly becomes overkill when you just want a basic animation clip that a developer can trigger when necessary. No need for any fancy blending, retargeting or muscle control.


# Legacy animation system: tips & tricks

So here are some notes I've collected during my journey as an in-engine animator. Take it from me that some of these points were relatively easy to figure out whilst some took real blood, sweat and tears, and the occasional "@$%! now I can start all over!"![post-it-overload post-it-overload](http://www.littlechicken.nl/wp-content/uploads/post-it-overload-300x213.jpg?width=1280&auto=webp&quality=80&disable=upscale)


So to spare you that feeling, let me describe the different situations where I was left hanging with a big question mark over my head and their solutions:

Okay, I got Unity fired up, what do I do now?

The core workflow is always the same: you add an Animation component (not Animator, that's Mecanim!) in the inspector on the object you want to animate. You open up the Animation Window (CTRL+6) where you create an Animation Clip. In the Animation Window you place your keys and adjust your curves, which get stored in the Animation Clip that a developer can trigger.

Why are my keys greyed out?

Imported animations are read-only in Unity. If you want to adjust the animation, you have to do this in the package you exported it from.

I got this big, beardy programmer coming up to my desk asking me why I'm importing the same character a million times. What do I do?

Shave him! Or instead of animating every individual action of the character in a separate scene file in your external 3d package, you could animate all its actions on one timeline. When imported, Unity offers you the option to create multiple animation clips by selecting the start & end frame.

EDIT: I received a helpful suggestion for an alternative approach, where you export your animations separately from the mesh + bones in your external 3d package. Unity is able to link the animation data to the separately imported model. This way, there's no need to animate all the animations on one timeline in your external 3d package, which results in a cleaner workflow. Thanks for the tip [Daan Boon](http://www.daanboon.nl/)!

![pigeon-multiple-animation-clips pigeon-multiple-animation-clips](http://www.littlechicken.nl/wp-content/uploads/pigeon-multiple-animation-clips-300x554.png?width=1280&auto=webp&quality=80&disable=upscale)


Create multiple animation clips from one imported fbx.

Damn son, I'm on fire! Look at all that fanciness: modifiers/deformers all over the place. I just need to import my animation in the engine........wait.........WHAT?!!!

Computer says no. Unity can only import bone based animation, vertex based animation won't work. There are some plugins in the Asset Store that claim to fix this, but I have no experience with these.

I have imported a completely bone based animation, but it still isn't displayed the same in-engine as in my 3d package.

Bake your animation in your 3d package, and in Unity check the import settings for the correct animation type (Legacy) and turn off Keyframe Reduction.

Is this an engine for ants? What's up with that tiny Camera Preview window in my Unity scene?

Size doesn't matter.....said nobody ever! I hope you have a second monitor, because you should display your Game Window there in order to see your animation in its full glory.

Is there a faster way to layout my camera?

Head on over to the menu bar -> GameObject. There you will find three handy align functions: Move to View, Align with View & View to Selected.

♪Dumdumdumdum♪ a keyframe here, a keyframe there, life has never been better! Ok, let's preview what I've got so far. Huh? Why does my preview only show the animation of the selected object? I want to preview the animation of all the objects in my scene at once!

Silly you for expecting this to work like EVERY other animation system out there. I pity the fool who now has to start over. What you should have done before animating anything is to create an empty GameObject that acts as a parent for all your animated objects. So instead of placing an Animation Component on all the individual objects, you place one Animation Component on the parent GameObject. Previewing this way ensures that you'll see the animation on all the objects.

What are all these mystery properties doing in my Animation Window? I've never animated those.

There's a silent killer on the loose in your workspace. And no, it's not the new intern with that strange look on his face. It's the Autokey function in Unity. When scrubbing through your animation in the Animation Window, the Autokey function gets automagically activated. This is indicated by the Record button in the top left of your Animation Window. When this is activated and you move anything in the scene or adjust a value in the inspector, this change gets added as a property in the Animation Window.

I'm sure nothing can go wrong when I just set two keys with the same value...

WRONG! The default tangents for your keys are set to Auto in Unity, which actually means they are set to Spline. This means that you almost always can count on an overshoot when setting keys. Just right-click on the offending keys and set them to Flat in the Animation Window to get rid of any overshoot. In most 3d packages the Auto and Spline mode are different modes, where Auto mode handles interpolation in a way to prevent extreme overshoots. Not in Unity.

My game needs explosions, because explosions. But why doesn't the particle GameObject gets activated on the keyframe I animated it to be active?

I have to admit I haven't delved that deep into particles in Unity yet, so my solution is probably a bit unconventional. I have found that Unity is a bit like you when your girlfriend asks you to put out the trash: you'll probably need a gentle reminder. Basically when I key the particles to be active on a certain frame, I make sure to set a second key later in time (usually the end of the animation) where the particles are set to active again. Suddenly the particles do get activated on the first key! There must be a better way and I don't know why this works, but I've just come to accept it. Unity works in mysterious ways...

![particles particles](http://www.littlechicken.nl/wp-content/uploads/particles-810x173.png?width=1280&auto=webp&quality=80&disable=upscale)


Add that second magical key to truly activate your particles.

I want to add some 2d elements to my 3d animation.

You could create a quad GameObject (GameObject -> 3D Object -> Quad). Drag the 2D texture on top of the quad and voila! Well not quite yet, it's probably looking a bit jagged. In the inspector set the shader of the quad to Unlit -> Transparent Cutout. To make sure the quad is always facing correct towards the camera simply parent it to the camera and set its scale to zero and scale it in the moment you need it.

The QA guy just tested the game on some devices and says my animation is partially out of screen!

Never liked that guy. But you should be aware of the different aspect ratio's of all the target devices you're animating for. In the top left of your Game Window there's a dropdown where you can select different aspect ratio's, be sure to preview your animation in all the necessary ones before handing it over. Think of it as a safe frame like in Max/Maya. That's it, I'm all out! I hope I could be of some help and prevented some headaches along the way.

# Wait! What about Mecanim?

Aaah man, it's almost weekend! But you have a point, Mecanim is already the main animation system for Unity and at some point Legacy will be phased out. I'm actually quite keen to get my hands on Mecanim and will probably use it for our next project. So expect a part two on this blog post, once I have come to grips with Mecanim!