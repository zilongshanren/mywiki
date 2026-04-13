---
title: Le Brigade nouveau est arrivé!
url: http://raytracey.blogspot.com/2013/10/brigade-3.html
author: Sam Lapere
published: '2013-10-22'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Time for an update on Brigade 3 and what we've been working on: until now, we have mostly shown scenes with limited materials, i.e. either perfectly diffuse or perfectly specular surfaces. The reason we didn't show any glossy (blurry) reflections so far, is because these generate a lot of extra noise and fireflies (overbright pixels) and because the glossy material from Brigade 2 was far from perfect. Over the past months, we have reworked the material system from Brigade and replaced it with the one from OctaneRender, which contains an extraordinary fast converging and high quality glossy material. The sky system was also replaced with a custom physical sky where sky and sun color vary with the sun position.And there's a bunch of brand new custom post effects, tone mapping filters and real camera effects like fish eye lens distortion (without the need for image warping).

We've had a lot of trouble finding a good way to present the face melting awesomeness that is Brigade 3 in video form and we've tried both youtube and Vimeo at different upload resolutions and samplecounts (samples per pixel). Suffice to say that both sites have ultra shitty video compression, turning all our videos in a blocky mess (although Vimeo is still much better than YT). We also decided to go nuts on glossy materials and fresnel on every surface in this scene, which makes everything look much a lot more realistic (in particular fresnel, which causes surfaces to look more or less reflective depending on the viewing angle), but the downside of this extra realism is a lot of extra noise.

So feast your eyes on the first videos of Brigade 3 (1280x720 render resolution):


Vimeo video (less video compression artefacts):


Youtube vids:

Vimeo video (less video compression artefacts):

[https://vimeo.com/77192334](https://vimeo.com/77192334)Youtube vids:

[http://www.youtube.com/watch?v=aKqxonOrl4Q](http://www.youtube.com/watch?v=aKqxonOrl4Q)
Another one using an Xbox controller:

The scene in the video is the very reason why I started this blog five years ago and is depicted in one of my very first blog posts from 2008 (see






[http://raytracey.blogspot.co.nz/2008/08/ruby-demo.html](http://raytracey.blogspot.co.nz/2008/08/ruby-demo.html)). The scene was created by Big Lazy Robot to be used in a real-time tech demo for ATI's Radeon HD 4870 GPU. Back then, the scene used baked lightmaps rendered with V-Ray for the diffuse lighting and an approximate real-time ray tracing technique for all reflective surfaces like cars and building windows. Today, more than five years later, we can render the same scene noise free using brute force path tracing on the GPU in less than half a second and we can navigate through the entire scene at 30 fps with a bit of noise (mostly apparent in shadowy areas). When I started this blog my dream was to be able to render that specific scene fully in real-time in photoreal quality and I'm really glad I've come very close to that goal.**UPDATE:**Screenshot bonanza! No less than 32 screenshots, each of them rendered for 0.5 - 1 second. The problem with Brigade 3 is that it's so much fun mucking around with the lighting, the time of day, depth of field and field of view with lens distortion. Moreover, everything looks so photoreal that it's extremely hard to stop playing and taking screenshots. It feels like you're holding a camcorder.
We plan to show more videos of Brigade 3 soon, so stay tuned...





**Update**: I've uploaded the direct feed version of the second video to MEGA (a New Zealand based cloud storage service, completely anonymous, fast, no registration required and free, just excellent :). You can grab the file here:[brigade3_purely_random_osumness](https://mega.co.nz/#!BlhWzSTY!QFySMkLeMlz45r9qilQAa0duccIm3rYpgYMZu4aVMXQ)(it's 2.40 GB)**Update 2:**The direct feed version of the first video can be downloade here:
## 81 comments:

Just awesome! Seems we really are only 1 or 2 generations of GPU away from the real-time general solution!

Thanks Mike.



>> Seems we really are only 1 or 2 generations of GPU away from the real-time general solution!

Absolutely agreed, but only if GPU makers put some extra hardware in their GPUs to accelerate some expensive ray tracing computations.

COOL! .. What hardware configuration did you use for this demo?

Sam, which GPU areas specifically do they need to address?


Do you expect Nvidia's Maxwell series to do this and do you expect any additional benefits from the R9 290x?

Anonymous: the demo was running on two GeForce Titan cards



Alex: I would say GPUs need hardware to improve ray coherency because thread divergence (where some threads in a warp take much longer than the others, effectively stalling the whole warp which sinks the efficiency) is a huge problem (maybe some ray sorting is possible in HW), to become more MIMD like, and to speed up ray traversal (intersections with the acceleration structure). Ray/triangle intersections (or ray/voxel if you want to do volumetric smoke) could be accelerated as well although. GPUs are already very fast at shading computations provided that ray coherency is preserved.

Of course, HW that can help building the acceleration structure on the GPU itself would be cool too. The Maxwell GPU should have a minimum of 4 ARM CPU cores on the same die as the GPU, which might alleviate some of these problems. Especially animated scenes should benefit from these architectural novelties. But it will also be possible to do much more funky stuff than just pure path tracing.

I don't know much about the R9 290x, but based on pure compute throughput numbers I'm pretty sure it should be a lot faster than the Titan for path tracing.

OMG yes! Octane Material System: Hell yes! You did an Vimeo Upload which I eagerly requested: Thank you sooooo much! I am very very pleased with what I am seeing here. It is so great to see that your team is so passionate on working on the engine. Since OTOY is in a partnership with Nvidia: Do these guys know about brigade? If not: go tell them! If they do: Go ahead and ask them if they really could develop some hardware for that. I mean one would need to be blind to not see that this is the future of gaming.

And by "know about Brigade" I mean Brigade in its current form and where it is heading and what kind of demands it has (obviously i am aware you guys held a talk on an nvidia conference)

Thanks Kevin :) Nvidia has Optix, so I don't know if they actually care about Brigade so much. Optix is not as cool as Brigade, so maybe they should care lol

Nvidia has the same ray coherence problems as everyone else so they should care. The new material system looks amazing, great work!

Fantastic! :)

Have you tried running each pixel for a fixed number of iterations, and if not finished adding it to a queue. Then in a second pass run through the queued pixels again, but in a group. This should help warp code divergence (but not data divergence obviously).

That's great to hear Sam. I hope you guys demo it using that card as well if possible.



Keep up the fantastic work.

In the mean time I willkeep trying to explain to gamers what this means, even if it looks like we'll have an uphill battle.

now some more fancy materials

are in place and noise goes up

like crazy. its now looking better

but performance seems to be like iray

or all the other full featured pathtracers.

whouuuuuuuuuuuuuuuuuuu!!!!


that looks..... turning the camera around one of those cars reminded me very much of some car ad TV spot. Apart from the rather low quality assests, like the houses and the street you can clearly see the huge power Brigade 3 has to offer. Nice! Cant wait to see more

of this awesome stuff.

Any serious optimisations yet coming?

SSSAAAAMMMM! Wanneer krijgen we een demo?

Why don't you finally start putting some good quality video up via torrent???

This BlockParty on YT is a real pain in the eyes and simply hide what this is all about: Noise and the way it fades!

Hi Sam. Where is the lamborghini?

"Suffice to say that both sites have ultra shitty video compression, turning all our videos in a blocky mess"And cloud gaming platforms use even shittier video compression. Low noise experience would probably require something like two NVIDIA GRID K520 - $7K server (at least) for a single player...

I'm starting to doubt that we will be able to play a real Brigade based game before 2018, because even cloud is far from being ready (economically) for this :(

Hm well.. I think it won't be before 2020 we really can play anything good with path tracing. But that's still good news for me as i'm still relatively young ;)

Sam, do you think that AMD's new "heterogeneous queuing (hQ)" technology will help Brigade?

Hi Sam ;)






Awesome work!

u said you use 2x GFirce Titan

... if the R9 290x should be a lot faster than the Titan for path racing, how it seems with Intel "Knights Corner" oder the Newer Intel "Knights Landing"??

What do you think About that?

thx for your great (Art)work!

So what do you think about R9 290x having up to 64 Compute Command queues? how much better should the 8 ACE's make the R9 290x at Path/Ray Tracing?


These videos are amazing by the way.

Mauro: thanks

















_: good idea, we should try that

Alex: good luck with it :)

Anonymous: I take it you haven't really used iray that much then

colocolo: thanks, the scene is actually the highest quality scene we have at the moment, all the cars and even the ones in the background consist of hundreds of thousands of triangles, which is overkill, but luckily it doesn't affect the performance too much. We want to bring our own assets to the scene

Anonymous: of course, we're continuously improving the efficiency, there's something very useful coming up for nightscenes

Mattijs, als 't aan mij lag, had je al lang een demo in je handen om mee rond te klooien, want het is echt ongelooflijk de max om mee te spelen. Dit gezegd zijnde ga ik er godverdomme alles aan doen dat deze tech zo snel mogelijk toegankelijk wordt voor iedereen

PartyArty: yep, i'm thinking of uploading the direct feed video to Mega

anonymous: the lamborghini is coming in another video

anonymous: I dunno about that yet

anonymous/Onq: I don't know enough about AMD's new architecture, looks nice on paper, but so did the first gen Kepler and that turned out to be a real disappointment for path tracing. So until we've got the hardware in our hands, we can't say much about it.

Anonymous: re Intel's Knight's Corner/Ferry/Xeon Phi: it's about half as fast as the GeForce Titan in path tracing and about 4 times as expensive, so not very interesting

One concern of mine is multi-light rendering. If I put tens of lights acting on a single object, that might increase the noise from an order of magnitude.

I hope you have some solution on this one, the number of lights is also correlated to the path tracing promises.

Neural matrix (ZISC) is the most effective device for implementing Monte Carlo Ray Tracing.
















At the moment, 180-picometre transistors & nitro-graphene substrate are officially available.

But mind that C++ does always create a bloated code..

Anyway, everyone who heartily roots for a lot better 3D graphics and is sane (unlike others) should be supporting the following idea how exactly to build the most powerful video game console ever right now, you bet:

~ Fattest Room-Temperature Superconductor non-volatile (due to a superconductive high-capacity accumulator built-in) Emitter-Coupled Logic SRAM

~ 6-layer Occam Process Superconducting Multiwire integrated picocircuit with a plenty of 4D Room-Temperature Dayem bridge Josephson junction Superconductor Bipolar Transistors between which are multiple paraffin wax filled graphite tubes

~ Explicit Data Graph Execution {that is non-von-Neumann} & Super-Threading & Single-Core

~ Adiabatic Ejector negative feedback cooling system

* SED Display

* Hyper CD-ROM

* Single-electron Room-Temperature Superconducting Digital-to-Analog Converter with Arbitrary-precision arithmetic capabilities

* Fullerite diaphragm based full-range mono speaker

* Hexa-nanotube-Litz-wire Teflon-isolated analog interconnect

~ Non-von-Neumann the Mercury computer language {usually used on artificial intelligence tasks} as the main programming source for purest Voxel Engines & Each-Separate-Ray-of-Light Modelling

MrPapillon: we've got a solution for it and it works astonishingly well, even with hundreds of lights. Each pixel knowsexactly which lights it should sample from.


Anonymous: fully agreed. Brigade would fly on a console with those specs, especially the fullerite diaphragm is an absolute must to reduce the noise

cool, hundreds of lights. New York, Neeeeeew York! dadadadada

any progress on cutting down process time with complex objects like forests?

Just a couple of remarks:



* the Josephson junction comprises a pure Teflon layer as dielectric

* the DAC utilizes the neutron clock

colocolo: a forest seen from above should be doable, but having the camera inside a densely packed forest will be the real challenge, because most of the light will be indirect. I just need to find a good forest scene to test.

The human models need a bit of work, but otherwise the screenshots look perfect!

anonymous: thanks. Yep, the models are low poly, but nothing prevents us to use higher poly ones, the difficulty is where to find high quality assets

Cant wait to see some high quaity scenes, like sci-fi room

Sam did you test already performance on AMD cards? Any big difference like in OpenCL LuxRender(over 2 times better than nvidia) Brigade is so exciting! Very interesting to see high poly-quality scenes, forest and dynamic water. By the way did you know about fluid v.3? Real-time opensource fluid simulations(on a good hardware).



http://www.rchoetzlein.com/fluids3/

Is It possible to see it running together with brigade? Brigade 3 + Bullet Phycics 3(comes soon) + Fluid v.3 + Full Hd Oculus rift + some gadjets like leap motion = Matrix... Ahhh dreams.

Aaand ver interesting how Clay looks on Brigade 3. =3

Just out of curiosity. How much faster do you think you can go, algorithmically? Do you think you have exhausted existing hardware?

Sam, half a second for one image.

Does that mean that it has to become 10x faster?(50ms,20frames) does it behave that linear?

Noise is already low...but screenshots look a lot better. ;)

for me a playable threshold isnt reached(shadow reagion), but anyway awesome stuff! if one day it looks like on the screenshots, man...artists will make a hell of a Matrix with that. :)

Is the brigade engine gonna be cloud only?

Or will it also be a game engine similar to Unreal Engine?

Sam,Could you do me a favour and find out what happened to cinema 2 engine shown in the ruby demo. Would love to find out more about it's raterisation/raytrace engine design. Even better as it's so old and obviously nothings beeing done with it open source to the community (or for a small fee say $100) for indie devs to play with. Also ive been building assets for a futuristic pod racer like style racer for over 8 months (and building my own opengl engine), I f i nocked up a complete level with a few racer designs would love to see you run it through brigade 3. Cheers. James

Hi Sam,


You're getting close for sure. Porting Octane material system to Brigade is great but what are we porting to Octane?

I.e. what does Octane still offer us that Brigade doesn't? (Except a gazillion plugins of course...) Will Octane see these speeds?

Will the two apps converge?

Any thoughts on this?

Seekerfinder

A couple of remarks:



* Carbyne diaphragm full-range mono speaker

* Six Teflon-isolated colossal carbon tubes Litz-wire analog interconnect

hi,images look pretty good for

1s rendering.

if we would like to have this

quality in games @20fps, we need

20x the perf. of 2x titan. so a long

way to go...

Stunning! I tip my hat to you sir

@anonymous ha

i think for desktop gaming/oculus

its a longer way.

But until then there are still some next gen games that will look awesome. and if you have the budget you can play them in 4k if Oculus releases 2016 a new version. (they are indeed already planning for that, so Iribe)

Nevertheless Brigade is something complete different i think.

When it will go into market then with a big explosion.

Graphics card will have 32GB memory, memristors.....hybrid memory cube...500GB blu rays....

The detail and quality fidelity will be humongous i think.

No need to go to cinema anymore...

ECL-driven 3.8 THz hot electron bipolar transistors + 4800°C-resistive highly-thermoconductive nitric graphene substrate = already obsolete technology due to the room-temperature superconductivity first discovered in 1978 (Russia) & later then in 2003 (SAR).


Thus, any of the future graphics cards should have been rubbish..

Apropos, game distributors might take advantage of the 100EB (exabyte) Hyper CD-ROMs originally being made in Romania..

Brigade looks absolutely beautiful. You've made some amazing vids. Is there any way I could d'load & play with the demos? Where is it available?

Yeah, new AMD's 290X architecture has better compute performance and more compute 64 Queues from 8 ACEs (GTX Titan GPU has 32 compute Queues). Sam Lapere, make the path tracing version for AMD GPU's please. Thanks.

Hi Sam, I research the web looking for innovation on game/graphic engines. Your work is the TOP 1! (makes second place looks boring!)



Is it possible to render a scene composed of trees lakes, mountains, grass, sun light, etc? Just to show the potential of Brigade on these kind of virtual landscape?

Great work!

@Sam Lapere



"the models are low poly, but nothing prevents us to use higher poly ones, the difficulty is where to find high quality assets"

Try this site high quality models:

axyz-design.com

@Sam Lapere







Here is a quick demo showing some of the uses of pre-rigged and animated humans in 3D animations and product presentations of AXYZ Design 3D models:

http://www.youtube.com/watch?v=lbH2yV9aocU

Realtime Ray Tracing Rendering of a Human 3D still model:

http://www.youtube.com/watch?v=CLG-HHAcHgk

Simulating moving crowd using AXYZ Design an(i)ma:

http://www.youtube.com/watch?v=9nswpC-DQFQ

This is fucking AWESOME. Really cool to see what possible, with enough brain ;-)




I use to do some renderings for architecual images but its always between 3 to 10 hours per picture.

This is sweet eye-candy.

PS: good music as well

Skif: yes, it runs more than fine on AMD OpenCL, Clay needs a break, he's tired of all the dancing and so are we








Anonymous: no idea, but I'm pretty sure we haven't exhausted everything algoritmically speaking yet. Brigade is getting a few percent faster almost every day, and not seldomly there's even a much larger jump in performance. That's the cool thing about GPU programming, it's such a brand new and uncharted territory that a small tweak can cause an enormous speed boost. I think there's still a huge amount of untapped potential even in the current gen of GPUs.

colocolo: yes, we're currently only a factor of 10x away from game quality noisefree images in real-time. That means that if we don't do any further algorithmic optimizations, GPU's will have the power to run this at high image quality in 720p in 5 years. But if you take into account that there will be substantial algorithmic and hardware improvements, I think it will be closer to 1.5-2 years from now (for 1080p/30fps).









Fady: I don't know, it would make sense as cloud-only engine initially

James: I don't know what happened to the Cinema 2.0 demo, but actually I don't care since we can do all the lighting and animation in that scene in real-time now (it was prebaked in the original demo). That's what matters to me

Seekerfinder: Octane has tons of production grade features which offline 3d artists can't live without, but which Brigade doesn't need for its purpose. It's that relative simplicity that makes Brigade faster than Octane.

Anonymous: non von Neumann is the key

Mark: no demo yet unfortunately

Andre: I would loveto test a forest/mountain scene, but I need to find a good one.

Anonymous/axyz design/cg river: those models look good, thanks. Next time you should render the promo video with Octane instead of Keyshot, you'll get an instantaneous render with HDRI :)

Anonymous: it is indeed fuck awesome. It's nuts if you think that these images used to take hours just a few years back. I started doing ray tracing in 2008 and I remember it took me about 3 hours to render a glossy

Android model on the CPU. Today I can do that same render at higher quality in less than a second with Brigade or Octane on two Titan GPUs. That's more than 10,000 times faster in just 5 years. It's absolutely mind boggling if you realize this.

10,000 times faster. funny, yesterday i saw an interview of an intel guy speaking about the new xeon phi. he worked on a supercomputer 1997 with 10,000 processors and it could execute 1TFLOP. then he showed the xeon phi processor with 50 cores that can do also 1TFLOP and laughed.

then i thought, man a supercomputer in 1997 was still too slow for some pure ray tracing graphics. fortunately it arrives at all. i thought we would never have this graphics on PCs.

Thanks Sam and the other guys at OTOY for telling me the Matrix is possible. :)

No problem colocolo :) IMO, the Xeon Phi card feels like it's too little too late. The latest GPUs from both Nvidia and AMD are already much faster at path tracing and the gap is only going to get bigger.

There are some sad predictions regarding GPU and CPU power increase in the near future: The end of Moore's law, extreme slowdown of process migration and dark silicon problem.






https://twitter.com/ID_AA_Carmack/status/392866033939132416

https://twitter.com/ID_AA_Carmack/status/394111220476678145

http://www.pcper.com/reviews/Editorial/Next-Gen-Graphics-and-Process-Migration-20-nm-and-Beyond

http://intelligence.org/2013/10/21/hadi-esmaeilzadeh-on-dark-silicon/

Interesting links, thanks. If true, then the time is ripe for fixed function ray tracing hardware :)

Waiting for links =3 Also maybe interesting to see prerendered demo with brigade to see what exactly we can expect in a future from yours passionate creativity! Anyway big thanks Sam for your entusiasm and very significant progress! Glory!

Skif, thanks a lot and the video download link is up btw. RE: prerendered animation, Brigade isn't really made for offline rendering, it would be easy to add such functionality but it would defeat the purpose of real-time path tracing. To give you an idea of the quality we can have with Brigade with instantly noisefree images, check out this CG animation:



https://vimeo.com/37517970

Right now, Brigade can do the exact same thing as what you see in the animation sans the smoke and motion blur. That animation actually inspired me to try the NYC scene you see in this post (and which was featured in my first blogpost in 2008) in Brigade and I must say that the results greatly exceeded my expectations.

Hey Sam,



Would something like this be applicable as a post-process effect to turn the noise down?

http://www.youtube.com/watch?v=Ee51bkOlbMw

There are a few more render targets to produce and it might still be too slow at the moment, but if that can be processed in a few milliseconds in the near future, that could be well worth it.

The shrinkage problem isn't really all that serious. Intel at least has been working with theoretical models to shrink all the way down to single-digit nanometer feature size using modifications of current tech. And there are also entirely new ways to do it that are in R&D phase; entire departures from photo-lithography.



We also have 3D chips to look forward to. Successful implementation will be more significant than the boost Moore's Law gives us. We could be scaling much more than just 2x every 18 months.

It's a problem worth thinking about, because the problem IS real, but that doesn't mean solutions don't or won't exist. Computers are not hitting a brick wall. We have many more performance increases to look forward to for the foreseeable future.

High-performance computing is very important to a lot of people. The scientific and engineering communities depend on it, and that's the prime reason a lot of supercomputers even exist. That's an unfathomably big industry. Everyone from professors and grad students working with theoretical models, to big agencies like NASA and pharmaceuticals need to run compute-heavy models. Then you've got agencies that just deal with a lot of computation in general, like the NSA and private firms.


High-performance computing is in higher demand now then ever. We're not gonna see progress suddenly stop, because too much of the world depends on it progressing as quickly as it can.

@Anthony Eadicicco

yeah i know, was just kidding...

but i have heard also that some nations build supercomputers only for the prestige of their country...yet i dont know what that means for the average utilization of those SPCs....

Anyway, it's "Le Beaujolais nouveau est arrivé", if you targeted that. It's not pure street-friendly french, but this is the way it is said.

Mr Papillon: thanks, fixed now :)


PS, I've also updated the post with a link to the direct feed version of the first video and a few new screenshots.

Anonymous: that filtering technique is too slow unfortunately. It's often more advantageous too spend more time on rendering extra samples instead of filtering pixels with not enough samples. And even though the amount of noise (variance) gets cut in half with the square of the number of samples, the perceptual difference in noise between 4 and 16 spp is much larger than the perceptual difference between 16 and 64 spp.





colocolo, Anthony: I'm not too worried about hitting a wall in the performance increase of 3d chips, but I do believe that some of the stages in the ray tracing pipeline can be massively accelerated by dedcated hardware. Now is the perfect time for Nvidia and AMD to look into that, because the next gen consoles will stagnate the advancements in game graphics for another 5-6 years until the cloud takes over completely (I'm fairly sure there will be never be a PS5 or Xbox One.5)

Thanks Sam for screens and vids, but i'm sure, obviously, this scene can't show even 10% of brigade potential. All you show before is static, are brigade ready for dynamic environment like moving trees, fireballs, water etc multilight; and in general this is question more of rude compute power or brigade flexibility? Ps what are you preparing for us next? =p White dots on 6th screen dof or rendering error?

Infinite-Realities' scanned models combined with Brigade would be completely amazing. If you haven't checked them out, you should. They're some of the most realistic real-time 3d models I've ever seen. There's a downloadable demo called HydraDeck-Humans that you can check out if you've got an Oculus Rift. Inside the Rift they're so realistic that it's almost creepy that they're not moving. It feels like they're real dead people. I think Brigade combined with those models, realisticly animated, would be the holy grail of gaming. Here's a quick video of the demo.


https://www.youtube.com/watch?v=7bytIGCeGxo

Skif, re moving trees, it's possible with instancing, but all the trees would move in lockstep unless you can find a way to offset/randomize the swaying tree animation for each tree. Regarding multiple lights, Brigade 3 has a specific optimization to deal efficiently with hundreds of lights of varying size and orientation. The next demo will have something to do with the Lamborghini model. The white pixels you see in screen 6 are fireflies, they're more common in out of focus areas.


Michael, yep I've seen those, they look great, looking forward to see them animated

1) Moving trees is an easy & simple task for a doxel engine .




2) The extremely fast room-temperature superconducting camera should be lot better at 3D scanning than what InfiniteRealities are capable of yet .

Hey Sam, Kingbadger3d here. Just wanted to share a few thoughts about the new AMD GCN cards. You probably heard of this new true audio (or something like that can't quite remember the name). Lots of people have mistakenly thought this was a sound card replacement, IT@S NOT. The new cards now include a VERY powerfull programable DSP on die, the dsp is being used for this new level of sound processing but after looking into it further being a fully programable DSP it can be used for anything the user likes if you write your own code. Im looking at ways this can be used for even faster BVH builds etc etc, Thinking even a realtime low latency noise reduction algorithm is more than feasable. You and your boys should look into this. Let me know what you think Bruda. Cheers J

Has anyone been able to download the Brigade video from MEGA? It starts to download but stops at 1% all the time. Do I need an account with them to download pass 1%? lol

If anyone has trouble downloading from MEGA on firefox, get the MEGA extension add-on: https://mega.co.nz/#firefox

Hi Sam, great work! I need to mention something. You said that we are a factor of 10x from playable realtime pathtracing. While I'd love that, I don't think that's the case.






Judging by the video you posted, in that video it takes about 2 seconds for the image to converge and be noise free. Which means 0.5FPS for noise free image.

Given the fact that we need around 50FPS for playable games, that makes the factor 100x of the current level.

Also if we factor in the fact that like you said you are using two Titans, well then the factor goes up to 200x the current level of a single top end GPU.

So, I'd say that 5-10 years is more like a realistic timeframe, providing we will also have algorithmic improvements.

Hi sam,


- Are you using explicit light sampling (aka next event estimate) ?

- Are you using stream compaction to improve warp occupancy ?

What are your thoughts on the Adapteva Epiphany 64 core processors to use for this type of application?




http://www.adapteva.com/epiphanyiv/

Very good hope this version I walk with my "amd 7870 DirectCU 2". I na query any idea when will be one? or when a demo version out?. The other question is whether it is possible to move a file from blender 3.0 per brigade.

_____

Muy bueno espero que esta versión ande con mi " amd 7870 directcu 2 ". Tengo na consulta alguna idea para cuando estara una? o para cuando salga una version demo?. La otra consulta es si es posible pasar de un archivo de blender por brigade 3.0.

I LOL'ed when the robot started boogieing, reminded me of the Citroen C4 commercial with the dancing Transformer (https://www.youtube.com/watch?v=bRArw9l3hFw). Hard to believe this can be done in real-time.

What do you think about Imagination's (PowerVR) ray tracing? They will have fixed function hardware just for ray tracing. Is that compatible with the Brigade Engine?

Post a Comment