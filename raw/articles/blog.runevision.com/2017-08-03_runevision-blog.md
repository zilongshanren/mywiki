---
title: runevision blog
url: https://blog.runevision.com/2017/
published: '2017-08-03'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

Here's the latest updates on the development of my Vive VR game [Eye of the Temple](http://blog.runevision.com/search/label/Eye%20of%20the%20Temple).

For the past several months I've been working on improving the whip I prototyped last year. In the [last post](http://blog.runevision.com/2017/06/june-update-verticality-puzzles-whip.html), I showed how it could grab levers, but there were a lot of issues and the whip and lever didn't exactly look pretty. Now see what it looks like now:

This feels really good to use now. It didn't get to this point without a lot of issues on the way though.

![](../../assets/30f52e611f108abb.gif)


Here's the latest updates on the development of my Vive VR game [Eye of the Temple](http://blog.runevision.com/search/label/Eye%20of%20the%20Temple).

For the past month I've been mainly working on improving the whip I prototyped last year. It can now be used to grab levers at a distance, and then you can yank the whip backwards to activate the lever.

Testing whip and lever in Eye of the Temple. Still some way to go, but getting there.

— Rune Skovbo Johansen (@runevision)[#gamedev][#indiedev][#vr][#HTCvive][pic.twitter.com/8TZHflQnM2][May 20, 2017]

There's still some way to go, especially with getting the audio cues right. The physics will never be quite like a real whip, but making it satisfying to use is the top priority.

Apart from this I've been looking into designing more puzzles for the game. I'm no expert puzzle designer, but bit by bit I come up with some that I think work well. The latest involve tall rotating towers, activated by levers (no whip use necessary for this one) where you need to step around on and in them at two different levels.

This also marks my increased effort in making better use of verticality in the level design. Experiencing the great heights is a draw of the game, and I'm figuring out how to use that optimally.

"Add more verticality" they said, and I agree! New puzzle elements in

— Rune Skovbo Johansen (@runevision)[@eyeofthetemple][#VR][#HTCVive][#madewithunity][https://t.co/hvxgYxW0uR][pic.twitter.com/tjDuCk2ufo][June 13, 2017]

I don't have a new build with these new things yet. The work right now is on smaller isolated pieces and puzzles, and once I have a set of those that fit nicely together, I'll begin integrating it all back into the overall world design.


Here's the latest updates on the development of my Vive VR game [Eye of the Temple](http://blog.runevision.com/search/label/Eye%20of%20the%20Temple).

![](../../assets/a2988bd800f707b6.jpg)

New additions:

**Fire!**One challenge tunnel now has fire hazards.**Blades!**One challenge tunnel now has swinging blades.**Speedrun mode!**A more challenging way to play the game. More notes below.**Hat!**You're now wearing a hat. Hope you like hat.**Experimental spectator camera.**3rd person view. More notes below.

![](../../assets/bb86df04871b4187.gif)

- Field of view is now restricted when close to falling and when falling in order to further reduce risk of motion sickness.
- Placeholder ambient soundscape taken out of the game for now since it had confusing footstep sounds.

### Speedrun mode

For those of you who wanted more challenge in the game, there is a new speedrun mode. This mode times your play-through but also speeds up the platform movements as long as you can keep up.

This mode is has a higher risk of being uncomfortable, causing motion sickness, and falling over, so engage on your own risk.

- Each time you take a perfectly timed step onto a new platform, the game will speed things up a little bit.
- Each time you miss an opportunity to step onto a new platform, the game will slow things down a little bit. (This can occasionally happen through no fault of your own.)
- When you die, the speed is reset, so it's recommended to keep to a speed you can handle in order to not lose momentum in your speedrun. You can avoid speeding thing further up by taking steps in a slightly slower way.

I do not recommend this mode to people who haven't already played through the game at least once, so in the final game I'll probably only unlock the speedrun mode by completing the game.

How to use: For now though, you start a speed run by first starting a new game, and then press Shift+R on the keyboard.

### Experimental spectator camera

The gameplay in Eye of the Temple can be hard to get an impression of for others by looking out in first person. I've experimented with an alternative camera angle shown on the monitor that shows the action from 3rd person perspective.

How to use: Activate/toggle 3rd person spectator camera by pressing X on the keyboard.

This view requires extra resources from your computer, so if you get performance problems, turn it off.

What do you think of 3rd person spectator camera? Is it something you might use for streaming, videos, or for people watching you play? It's still a bit buggy and has room for improvement, but I'm curious what you think of the overall idea.


Here's the latest updates on the development of my Vive VR game [Eye of the Temple](http://blog.runevision.com/search/label/Eye%20of%20the%20Temple).

![](https://i.giphy.com/nuKD5ehCqP4e4.gif)

New features:

- There are now gems throughout the temple that you can collect.
- Moving platforms have glowing symbols on them.
- Visuals: Intro area has some red stones and some of the dungeons have grittier gray stones and spikes.
- The way the platforms move has been tweaked, hopefully to further reduce potential for dizziness.

### Notes on gems

The gems are found throughout the temple. The exact placement tries to take player proportions into account so that they are at a comfortable distance for reaching. I haven't tested this on different people yet though. If you could let me know how it works for you and how tall you are, that would be helpful. If you don't want to share that, that's ok too.

Right now the gems don't do anything yet. Later I will implement at the minimum a way for you to see how many you collected.

Beyond that I need to decide if the gems have a critical or non-critical function:

A critical function of the gems could be if they are used to unlock new areas in the game and thus are needed to progress. Or an almost-critical function would be to unlock alternative paths or secret rooms not otherwise accessible. This is still fairly critical because it would be annoying if you're trying to see 100% content of a game to find out you can't due to some mistake made earlier that's too late to do anything about. Currently there are one-way platforms that you can take which will prevent you from going back to collect any gems you might have missed. If I make the gems critical, I'd have to find a way to make it possible to always go back to all areas of the temple.

Non-critical functions of the gems could be high-score, achievements, and, I dunno, unlockable hats if I get a selfie stick implemented for the game. :P Old games would typically grant you extra lives, but it doesn't work for modern games with infinite lives.

For now I refrained from placing gems at platforms that only go one way. If there were gems there and you failed to pick one up, you wouldn't have a second chance and I thought that might feel unfair or frustrating.


### Early testers online forum

In order to try to get faster feedback and shorter iteration cycles, I opened up for people to [sign up online to be early testers of the game](https://itch.io/t/59040/early-testers-welcome-thread-introduce-yourself). If you have access to a Vive (and 2.2 by 2.2 meters space) and would like to try out the game and provide detailed feedback based on your experience, please don't hesitate to join!


For a while, my focus for my Vive VR game [Eye of the Temple](http://blog.runevision.com/search/label/Eye%20of%20the%20Temple) have been to not expand more on gameplay right now but rather on improving what I've got in order to make it as presentable as possible.

That has meant:

- Improving visuals.
- Addressing usability issues found in play-testing.

(If anybody wonder what happened to the [Whip Arena spin-off game](http://blog.runevision.com/2016/12/spin-off-game-whip-arena.html), I put that on hold after it become clear it only worked well with a quite large physical VR space, which very few people have available.)

### 3D models

*Gate model. Two keys must be inserted above the gate to unlock and open it:*

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEigTTtJ-QCittQesdyKqW5_vj5em-sdIcv6kKdb3UF8C78CrVgU0rjs7vF9ixLE2nGIygKN1bJCAocPqfRSG081B9DlZ1sL4a9WLBESl56ss3kO-UCrp-tELkCB-H04ZqNUJUfcd_IHrGQ/s800/2017-01-08_GateModelWIP.png)


![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEigTTtJ-QCittQesdyKqW5_vj5em-sdIcv6kKdb3UF8C78CrVgU0rjs7vF9ixLE2nGIygKN1bJCAocPqfRSG081B9DlZ1sL4a9WLBESl56ss3kO-UCrp-tELkCB-H04ZqNUJUfcd_IHrGQ/s800/2017-01-08_GateModelWIP.png)

*Stone torch model. You light these with your torch to trigger things happening:*

![](../../assets/34fce84d1838fcf6.png)


![](../../assets/34fce84d1838fcf6.png)

*Cliffs model. The temple used to just float in the air; now it's grounded:*

![](../../assets/e8b300bfab42353d.png)


![](../../assets/e8b300bfab42353d.png)

For a long time the game was full of placeholder models made of simple boxes and cylinders. There's still some of those left, but I've been working on replacing them all with proper models.

After briefly planning to work with contractors for 3D models, I decided to learn 3D modeling myself instead (and deal with the [various challenges](http://blog.runevision.com/2017/01/the-quest-for-automatic-smooth-edges.html) that come with it).

The models I need have highly specific requirements (they need to have very exact measurements and functionality to fit into the systems of the game) yet in the end they are quite simple models (man-made objects with no rigging).

With this combination it turned out that back-and-forth communication even with a very skilled artist took as much time as just doing the work myself. I'll still be working with artists for the game, just not for the simple 3d models I need.

Several of the models still have placeholder texturing. I have an idea for a good texture creation workflow for them, but it will take a little while to establish, so I'm postponing that while there's more pressing issues.

### Intro section

My goal is that Eye of the Temple should be a rather accessible game. You need a body able to walk and crouch, and not be too afraid of heights, but I want it simple enough to play that people who don't normally play computer games can get into it without problems.

This has largely been a success. Gamers or not, I normally just let people play without instructions, and they figure things out. My dad completed the whole thing in one hour-long session when he was visiting.

The game did throw people in at the deep end though, asking them right from the start to step between moving platforms four meters above the ground. Some people would hesitate enough to end up mis-timing their step and stumble, making the experience even more extreme right from the beginning.

To ease people a bit more in, I've worked on an intro section that starts out with only a 0.75 meter drop, and the first two platforms have no timing requirement. I have yet to get wide testing of this to see if it helps.

![](../../assets/dcb8406cf53b0be8.png)


![](../../assets/dcb8406cf53b0be8.png)

There is *one* particular problem I've toiled with for a while, which is to design a platform that bridges two spots in a compact manner. Why this is tricky relates to how the game lets you explore a large virtual space using just a small physical space.

Originally I had platforms rotating around a center axis, but that made some people motion sick who otherwise didn't have problems with the rest of the game.

![](../../assets/aa6a06f0ab524bd5.gif)


![](../../assets/aa6a06f0ab524bd5.gif)

I tried various contraptions to replace it, but they were complicated and awkward to use. My latest idea is using just a barrel-like rolling block, which is nice in its simplicity, and also a fun little gimmick to balance on *once you understand how to use it*.

Figuring out what you're meant to do is easy to miss though, as I found out with the first tester trying it. I have some ideas for a subtle way to teach it, but that will take quite some time to implement. For now I settled for slapping a sign up that explains it.

![](../../assets/445f46fd710eb908.png)


![](../../assets/445f46fd710eb908.png)

### Early testers online forum

There is no substitute for directly observing people playing a game, but this is impractical for me to do frequently when I also have a full-time job. I'm lucky if I get to do it two times a month.

In order to try to get faster feedback and shorter iteration cycles, I've now opened up for people to [sign up online to be early testers of the game](https://itch.io/t/59040/early-testers-welcome-thread-introduce-yourself). If you have access to a Vive and would like to try out the game and provide detailed feedback based on your experience, please don't hesitate to join!


I'm currently learning simple 3D modeling so I can make some models for my game. I'm using Blender for modeling.

The models I need to make are fairly simple shapes depicting man-made objects made of stone and metal (though until I get it textured it will look more like plastic). There are a lot of flat surfaces.

The end result I want is these simple shapes with flat surfaces - *and smooth edges*. In the real world, almost no objects have completely sharp edges, and so 3d models without smooth edges tend to look like they're made of paper, like this:

![](../../assets/56624d7575b062f0.png)


![](../../assets/56624d7575b062f0.png)

What I want instead is the same shapes but with smooth edges like this:

![](../../assets/d565e0db012f14ab.png)


![](../../assets/d565e0db012f14ab.png)

Here, some edges are very rounded, while others have just a little bit of smoothness in order to not look like paper. No edges here are actually completely sharp.

![](../../assets/e3ffa79e2fa3587a.png)


![](../../assets/e3ffa79e2fa3587a.png)

The two images above shows the end result I wanted. It turns out it was much harder to get there than I had expected! Here's the journey of how I got there.

How are smooth edges normally obtained? By a variety of methods. The Blender [documentation](https://www.blender.org/manual/modeling/meshes/editing/smoothing.html) page on the subject is a bit confusing, talking about many different things without clear separation and with inconsistent use of images.

#### Edge loops plus subdivision surface modifier

From my research I have gathered that a typical approach is to add *edge loops* near edges that should be smooth, and then use a *Subdivision Surface* modifier on the object. This is also mentioned on the documentation page above. This has several problems.

First of all, subdivision creates a lot of polygons which is not great for game use.

Second, adding edge loops is a manual process, and I'm looking for a fully automatic solution. It's important for me to have quick iteration times. To be able to fundamentally change the shape and then shortly after see the updated end result inside the game. For this reason I strongly prefer a [non-destructive editing](https://en.wikipedia.org/wiki/Non-linear_editing_system) workflow. This means the that the parts that make up the model are kept as separate pieces and not "baked" into one model such that they can no longer be separated or manipulated individually.

Adding edge loops means adding a lot of complexity to the model just for the sake of getting smooth edges, which then makes the shape more cumbersome to make major changes to afterwards. Additionally, edge loops can't be added around edges resulting from procedures such as *boolean subtraction* (carving one object out of another) and similar, at least not without baking/applying the procedure, which is a destructive editing operation.

Edge loops and subdivision is not the way to go then.

#### Bevel modifier

Some posts on the web suggests using a *Bevel* modifier on the object. This modifier can automatically add bevels of a specified thickness for all edges (or selectively if desired). The Bevel modifier in Blender does what I want in the sense that it's fully automatic and creates sensible geometry without superfluous polygons.

![](../../assets/b5e7e82a90f8708c.png)


![](../../assets/b5e7e82a90f8708c.png)

However, by itself the bevel either requires [a lot of segments](http://blender.stackexchange.com/questions/811/most-efficient-way-to-round-edges), which is not efficient for use in games (I'd want one to two segments only to keep the poly count low) or when fewer segments are used it creates a [segmented look](http://blender.stackexchange.com/questions/2534/how-can-i-round-the-edges-of-a-mesh) rather than smooth edges, as it can also be seen below.

![](../../assets/9e02b8c30534f7d1.png)


![](../../assets/9e02b8c30534f7d1.png)

#### Baking high-poly details into normal maps of low-poly object

Another common approach, especially for games, is to create both a high-poly and a low-poly version of the object. The high-poly one can have all the detail you want, so for example a bevel effect with tons of segments. The low-poly one is kept simple but has the appearance from the high-poly one [baked into its normal maps](http://www.chrisalbeluhn.com/Normal_Map_Tutorial.html).

This is of course a proven approach for game use, but it seems overly complicated to me for the simple things I want to achieve. Though I haven't tried it out in practice, I suspect it doesn't play well with a non-destructive workflow, and that it adds a lot of overhead and thus reduces iteration time.

#### Bevel and smooth shading

Going back to the bevel approach, what I really want is the geometry created by the Bevel modifier but with smooth shading. The problem is that smooth shading also makes the original flat surfaces appear curved.

Here is my model with bevel and smooth shading. The edges are smooth sure enough, but all the surfaces that were supposed to be flat are curvy too.

![](../../assets/5adbd397f0a6ce2d.png)


![](../../assets/5adbd397f0a6ce2d.png)

Smooth shading works by pretending the surface at each point is facing in a different direction than it actually does. For a given polygon, the faked direction is defined at each of its corners in the form of a *normal*. A normal is a vector that points out perpendicular to the surface. Only, we can modify normals to point in other directions for our faking purposes.

The way that smooth shading typically calculates normals makes all the surfaces appear curved. (There is typically a way to selectively make some surfaces flat, but then they will have sharp edges too.) The diagram below shows the normals for flat shading, for typical smooth shading, and for a third way that is what I would need for my smooth edges.

![](../../assets/52c6494f10c3c51b.png)


![](../../assets/52c6494f10c3c51b.png)

So how can the third way be achieved? I found a post that asks [the same question](http://blender.stackexchange.com/questions/39674/how-to-keep-flat-faces-flat-when-using-smooth-shading) essentially. The answers there don't really help. One incorrectly concludes that Blender's Auto Smooth feature gives the desired result - it actually doesn't but the lighting in the posted image is too poor to make it obvious. The other is the usual edge loop suggestion.

When I posted question myself requesting clarification on the issue, I was pointed to a Blender add-on called Blend4Web. It has a [Normal Editing feature](https://www.blend4web.com/en/community/article/131/) with a Face button that seems to be able to align the normals in the desired way - however as a manual workflow, not an automated process. I also found [other forum threads](http://polycount.com/discussion/154664/a-short-explanation-about-custom-vertex-normals-tutorial) discussing the technique.

#### Using a better smoothing technique

At this point I got the impression there was no way to get the smooth edges I wanted in an automated way inside of Blender, at least without changing the source code or writing my own add-on. Instead I considered an alternative strategy: Since I ultimately use the models in Unity, maybe I could fix the issue there instead.

In Unity I have no way of knowing which polygons are part of bevels and which ones are part of the original surfaces. But it's possible to take advantage of the fact that bevel polygons are usually much smaller.

There is a common technique called *face weighted normals* / *area weighted normals* ([explained here](http://www.bytehazard.com/articles/vertnorm.html)) for calculating averaged smooth normals which is to weigh the contributing normals according to the surface areas of the faces (polygons) they belong to. This means that the curvature will be distributed mostly on small polygons, while larger polygons will be more flat (but still slightly curved).

From the discussions I've seen, there is general consensus that this usually produces better results than a simple average ([here's one random thread about it](http://polycount.com/discussion/85809/face-weighted-normals)). It sounds like Maya uses this technique by default since at least 2014, but smooth shading in Blender doesn't use it or support it (even though people have discussed it and made custom add-ons for it [back in 2008](https://forum.guildofwriters.org/viewtopic.php?f=59&t=2197)), nor does the model importer in Unity (when it's set to recalculate normals).

#### Custom smoothing in Unity AssetPostprocessor

In Unity it's possible to write *AssetPostprocessors* that can modify imported objects as part of the import process. This can also be used for modifying an imported mesh. I figured I could use this to calculate the smooth normals in an alternative way that produces the results I want.

I started by implementing just area weighted normals. This technique still make the large faces slightly curved. Here is the result.

![](../../assets/d91a654b609fdf2a.png)


![](../../assets/d91a654b609fdf2a.png)

Honestly, the slight curvature on the large faces can be hard to spot here. Still, I figured I could improve upon it.

I also implemented a feature to let weights smaller than a certain threshold be ignored. For each averaged normal, all the contributing normals are collected in a set, and the largest weight is noted. Any weight smaller than a certain percentage of the largest weight can then be ignored and not included in the average. For my geometry, this worked very well and removed the remaining curvature from the large faces. Here is the final result again.

![](../../assets/2003230c57318f88.png)


![](../../assets/2003230c57318f88.png)

The code is available [here as a GitHub Gist](https://gist.github.com/runevision/6fd7cc8d841245a53df5d09ccf6b47ff). Part of the code is derived from [code by Charis Marangos, aka Zoodinger](http://schemingdeveloper.com/2014/10/17/better-method-recalculate-normals-unity/).

#### Future perspectives

The technique of aligning smooth normals on beveled models with the original (pre-bevel) faces seems to be well understood when you dig a bit, but poorly supported in software. I hope Blender and other 3D software one day will have a "smooth" option for their Bevel modifier which retains the outer-most normal undisturbed.

A simpler prospect is adding support for *area weighted normals*. This produces almost as good result for smooth edges, and is a much more widely applicable technique, not specific to bevels or smooth edges at all. That Blender, Unity and other 3D software that support calculating smooth normals do not include this as an option is even more mind-boggling, particularly given how trivial is it to implement. Luckily there workarounds for it in the form of AssetPostprocessors for Unity and custom add-ons for Blender.

If you do 3D modeling, how do you normally handle smooth edges? Are you happy with the workflows? Do some 3D software have great (automatic!) support for it out of the box?