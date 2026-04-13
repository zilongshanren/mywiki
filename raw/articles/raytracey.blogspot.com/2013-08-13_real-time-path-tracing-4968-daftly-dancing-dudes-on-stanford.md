---
title: 'Real-time path tracing: 4968 daftly dancing dudes on Stanford Bunny'
url: http://raytracey.blogspot.com/2013/08/real-time-path-tracing-4968-daftly.html
author: Sam Lapere
published: '2013-08-13'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Another real-time path traced test of Brigade with HDR environment lighting, featuring the Stanford bunny and the dancing dude from one of the previous posts. Jeroen van Schijndel (Brigade's lead dev), had the outrageous idea to create an animated instance for every triangle of the Stanford bunny, resulting in 4968 instances. Each jolly dancer contains over 60k triangles, totalling over 300 million dynamic triangles in real-time.


720p video:

720p video:

[http://www.youtube.com/watch?v=huvbQuQnlq8](http://www.youtube.com/watch?v=huvbQuQnlq8)
Some screenshots below, notice the real-time color bleeding, reflections, soft shadows and soft realistic lighting from the HDR environment.

Soft shadows coming only from the HDR environment (no additional lights used):

## 49 comments:

wow, nice work!

Awesome stuff! I love how fast it converges and how the reflective surface and the animation seem to have very little to no impact on the performance on that.










Even though, again, the YT Compression really kills it.

I'm so happy that we get regular updates from you now!

Since I posted a question on the last post you made, I guess I will repeat it here:

I was wondering what brigade benefits the most from, on the graphics hardware side. SP FLOPS, DP FLOPS, Memory Bandwith etc.

Also, how many people are currently working on brigade?

nice! can they also dance asynchron and at different directions?

Irakli: thanks




Kevin: yep, YT totally fucks up the quality as usual, it's even worse this time. Uploading the video took me a long time and New Zealand is not really famous for its fabulous upload speeds.

Brigade doesn't use DP, I don't know any GPU path tracer that does (so it makes no sense to use Teslas for GPU rendering). Single precision and bandwidth are very important.

We're working on Brigade with a very small team to keep it lean and mean so we can iterate very quickly and implemetn ideas in less than a day: Jeroen van Schijndel, Rick de Bruijne, Hayssam Keilany and myself.

colocolo: thanks, we haven't tried to offset the animation per instance yet. Having them move in different directions is no problem, as rigid transformations are completely free.

The real-time video seems to have a greatly reduced level of color bleed compared to the static images. e.g. at 1m37s, the floor color changes but the bunny's overall coloration appears unchanged. At 2m40s, the color bleed finally seems to have appeared.


Is this a fixable bug (e.g. cached floor-bound secondary rays' colors don't update), a limitation caused by moving too quickly to reach convergence, or am I missing something?

Hi, do you use multiple BVH types i.e. SBVH, LBVH, ... ? I was also wondering how many spp / frame to achieve 30fps? I'm focussing on filtering techniques that achieve noise free output (with reflections, dof, color bleeding etc. in tact) with about 8spp. Currently I can only achieve about 10 fps with a resolution of 640x480 on a 7970 (with filter on).


This is really impressive and so fast on only one Titan so keep up the awesome work!

This is Brigade 2(see on screens) or 3 which 3x time faster? And would you add features like complex lighing improvements(400% faster) etc in the future?


What is Contribution of Jacco Bikker in Brigade? I know that he is one of the main developer.

and when acceleration structure are shown there are visible characters in squared holes on different side of bunny. is this bug or visualization artifact?

Are you runinng 2 GTX 580's?

Lachlan: the color bleeding is equal in strength during the entire video, it's just more noticeable in the second part when I'm shining a strong light directly on the red floor, while the same light was pointing towards the ceiling before.













Mauro: we use all kinds of novel acceleration structures in this scene, optimized to give the best performance depending on the scene/objects.

Anonymous: this is still Brigade 2 with some features from Brigade 3 (if you will). Brigade 3 is currently under heavy development and its quality of lighting and materials will blow you away, it's of a completely different level compared to what we have now and is offers the same quality of Octane (minus Oxtane powerful material system).

Irakli: Jacco Bikker is not working on the Brigade engine any longer. I will check the see-through bug.

Nuninho: this ran on 1 GTX Titan

Here i have a very fancy question. ;)

If a game studio would make a game with your latest Brigade version to which movie (year) could its overall graphics quality be compared to? One reference point could be Star Wars: Episode 1 made in 1999.

There is a strange comment on one of the screenshots.

I tried to make it recognizable:

http://imageshack.us/photo/my-images/560/pxzb.jpg/

Any ideas, where it comes from?

I mean, there is a strange shadow on one of the screenshots

I'm looking forward to see some videos of Brigade 3! Will it support amd graphic cards?

Sam Lapere,


Great news about Brigade 3! Will it be faster and noise free compare to Brigade 2? I'd imagine you guys are still focusing on the renderer and not so much about the pipeline(getting content(mesh, sound,ai,etc into brigade)tools something like UDK?

colocolo: it would be comparable to a movie that uses path traced GI and reflections, like Cloudy with a chance of meatballs (rendered with Arnold) or more recently Monster's University. Brigade doesn't support hair/fur/volumetrics (yet), but it can produce very realistic images. You'll see it once we reveal the true Brigade engine 3.






CosmicBlue: that's a shadow artefact caused when the geometry is too coarse, in this case the bunny. It's something all path tracers suffer from, so it's not a limitation or bug in Brigade.

Jeyhey: yep, Brigade supports AMD through OpenCL.

Anonymous: Brigade 3 will be a lot faster and almost noisefree compared to Brigade 2. We're implementing some techniques that will greatly reduce the noise without affecting the image quality. More importantly, the old material and lighting system has been thrown out completely and is replaced by a new one, which is essentially identical to that of Octane Render, so you won't be able to tell the difference between the two. So if you're not yet familiar with Octane's quality, believe me it will blow you away.

Right now, we're also working on tools to make it easier for game devs to start mucking around with Brigade.

apropos "will blow you away"

I have watched 'Arnold Showreel 2013' on youtube.......HOLY....

You mean sth like this Sam ?

And, the 'vastly improved light sampling in Octane Render' is crazy realistic. I have never seen so realistic CGI.

Another question.

You have said that in 1 or 2 years we could see a Brigade powered game.

Do you think that will happen considering that PC games are always kept at the almost same graphics level as console games.

Its hard to imagine how this supergraphics-games could fit into the upcoming PS4/XBox1 game repertoire.

Do you think Sony or Microsoft could prevent that game studios suddenly make games with such superior PC graphics?

Does Brigade 3 support caustics and use PMC or MTL?



I like too Octane Render 1.20 but still demo.

My PC with CRT monitor 21" (Samsung SyncMaster 1100P+) has i5-2500K@4.5GHz, 8GB DDR3-1600 and GTX 480@stock-reference. :D

colocolo: "Do you think that will happen considering that PC games are always kept at the almost same graphics level as console games"


Lol but wrong - PC is ALWAYS better than newer consoles!

"Right now, we're also working on tools to make it easier for game devs to start mucking around with Brigade."




Awesome Sam, UE4 as a toolset is something you guys should mimic, the GUI is pretty and flexible, the dark grey color is important for working long hours. Check out the recent UE4 video:

http://www.youtube.com/watch?v=PjSFbPv3SLc

toolsets have to have user friendly workflow.

@Anonymous (August 17, 2013 at 12:12 PM): UE4 isn't very realistic because it's ray-traced "limited". UE4 is very different to and much worse than Brigade. lool!



@Ssm: NOTICE! - last 3 my messages (MTL - bad but yes MLT kernel, sorry). ;)

@Nuninho



You totally miss my point. I'm not using UDK as a reference for awesome rendering technology, the video shows the proper material workflow, this is becoming standard with next generation(PS4). Brigade need similar material editing workflow and they really need to hire more people to work on the toolset. It has to look good, UDK,Unity,Cryengine GUI all look good but more important they are offer user friendly game creation toolsets. Brigade renderer is superior to UDK/Unity,etc but it will also need an equally beautifully polish game toolsets.

@Sam, FBX is such a standard file format, I hope you guys add support for it in your toolset. Its a great way to bring animation and 3D content in one nice file format.

@Sam,


I forgot to say thank you for being transparent about brigade, I look forward to seeing how awesome Brigade 3 will be!

colocolo: on some occasions, it will look as good as Arnold minus the hair/fur/volumetrics because Brigade doesn't support that as I said before.






Brigade will have its own very clever light sampling technique, independently developed from the one in Octane to deal with noise coming from thousands of light sources at once. It works extremely well so far and is one Brigade 3's ground breaking features.

>>> Do you think Sony or Microsoft could prevent that game studios suddenly make games with such superior PC graphics?

To be honest, I couldn't care less about MS or Sony or any other next gen console manufacturer. A Brigade powered game will probably not run on PS4 or Xbox and cloud gaming will make consoles obsolete in a few years, so your best bet will be Brigade games in the cloud.

Nuninho: no, Brigade doesn't support MLT or PMC as it doens't make sense in real-time. Those techniques are much more relevant for Octane.

Anonymous: yep, a CryEngine Sandbox like editor would be really cool, and also a lot of work. The good thing about path tracing is that you need a lot less parameters to tweak, which will simplify the Brigade GUI a lot.

Sounds very interesting.

Wonder what those ground breaking features are.

Audio ray tracing? ;)

You'll see it once we reveal the true Brigade engine 3. ---> please when you make it let a part for a forest/natural scene as i can't wait to see how it perform :)


Ps: i know that you told me yes before so do not worry :)

Ps2: english is not my native language so sorry if i made faults.

@Sam,




"yep, a CryEngine Sandbox like editor would be really cool, and also a lot of work. The good thing about path tracing is that you need a lot less parameters to tweak, which will simplify the Brigade GUI a lot."

IMO, its only logical to have something like CryEngine Sandbox for Brigade. Or even UE4, as an example can run C++ within the editor, so people won't need a SDK. It is ALOT of work no doubt, I'm not sure if you guys have the man power for it? OTOY could always hire a team of people to work on the toolset and keep the render team small and streamline. When you add hair you'll need a way to interact with it, same with cloth simulation,etc.

Anyway I can wait to see version 3!

@Sam, I forgot to mention there is a cloud version of Cryengine sandbox in the works.

Sam!, Dude!. Not been on here for while but after your latest post I was intrigued. Octane is making the move to Blender, As far as I understand octane for max also comes with Brigade for max? Why doesn’t Octane for Blender have this?!!!?. Also you may remember me being one of the first asking about indie dev support. If otoy are aiming brigade to the big dev's without the same access to indie's ill be MASSIVLY disappointed. What is the official stance on Brigade? Can we expect a half decent indie/New API response, e.g Epic style pay £300 for Blender octane, But you get Brigade with for example a £50,000 free pass before having to pay any royalties to Otoy, when you make more than the £50,000 all other profits from work if from game projects, architectural design works and realtime walkthrough apps for clients etc etc you then pay Otoy 10-15% of all earnings,(you build a bad ass game that sells £500,000,000 product otoy then take 10-15% after the £50,000 free pass, which isn’t out of the question when you look at sales from example call of duty. Think Black opps made near a Billion). Please try to think Indie,Indie,Indie, Not feeding the monster of current studios. Heard Apple are really pushing in the direction of Opencl now because they realise there products need it to compete, Consortiums need to appear to slap AMD drivers into place. You do that the game really starts, but only an Nvidia based platform can never be seen as a complete new api for dev's. Get in early and support the small guys, with indie community support you have the chance to challenge the Microsofts,Sony's. If not they build their own similar products within 2 years and even though being the pioneers you lose.

@Sam,


Did blurry reflection and alpha channel support(for grass) make it into Brigade 3.0 ?

About Brigade and games on the cloud:



I was a strong believer in cloud-gaming a year ago, but my interest completely disappeared when Oculus entered the arena.

We really can't deal with the latency when doing headtracked VR.

Cloud-gaming VR or multiplayer-VR can be a deal, but only in a range of r = 300km-500km (for Germany this would cover already the whole country). Cloud latency for online VR really has to be under 10ms. But anyway, cloud-gaming would be only a interim solution.

In 5-10 years every cheap PC will be able to render path tracing.

<10ms is acceptable, problem is that that is the best case.



In reality we are going to have occasional spikes.

This is a huge problem, we get dizzy at very small levels of latency.

And I suspect that it is even worse with varying latency.

@Sam,





Is open OpenSubdiv 2.0 fast enough to use in/with Brigade?

http://graphics.pixar.com/opensubdiv/

Good. Now make the animation offset for each dude unique.


Mwahahahahahahahah!

There's a place when we can download the latest version of Brigade?

On the off-chance that you're still reading this comment thread: http://blog.qwrt.de/improved-pre-warping-for-wide-angle-hmds/



Some researchers at Intel made physically accurate prewarping algorithms for the Oculus Rift that output images that are far sharper than the bilinearly filtered ones coming out of the current prewarp post-processes. But they could only do it using Raytracing.

You're in the unique position where you have a game engine that can output prewarped images for VR with less overhead than raster games AND with higher quality than what is achievable in those games. It would be a killer feature for the brigade engine to have.

Is it possible to write game engines in the Unicon programming language ?

Thomas the actual issues of the post-process warp are not that important. Things are blurred anyway on your peripheral vision because of the density of pixels fading away near the edges. The most important thing is too enhance the pixels that are in front of you.

Sega Planning New Console For 2015 using the RayCore® technology

here is the link -


http://virtuamorris.wordpress.com/

is this the official Brigade 3 website? looks legit - from an OTOY developer Hayssam Keilany


http://icelaglace.com/projects/brigade-3-0/

It is from a team member. But I guess when Brigade will be released some time in the future there will be a different site. For now it's a sleek site that will inform people about the benefits of Brigade 3.0.


Sam, it's been a month since you posted an update. Would you mind giving us some news what you have been working on lately?

I can't wait to see the progress :D

Post a Comment