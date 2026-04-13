---
title: 'Real-time GPU path tracing: Streets of Asia screens + video'
url: http://raytracey.blogspot.com/2012/04/real-time-path-tracing-streets-of-asia.html
author: Sam Lapere
published: '2012-04-06'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**UPDATE August 2012: much higher quality video and screens with dynamic objects, shown at Siggraph 2012, at the following link:**


[http://raytracey.blogspot.co.nz/2012/08/real-time-path-traced-brigade-demo-at.html](http://raytracey.blogspot.co.nz/2012/08/real-time-path-traced-brigade-demo-at.html)"The Streets of Asia" from Stonemason is a superb 3D scene to showcase what Brigade is capable of. The geometry and texture detail rivals what you see in today's highest end PC games. Combined with the real-time path traced lighting provided by OTOY's Brigade engine, the resulting images become stunningly photorealistic. Jeroen van Schijndel, a genius and self-taught programmer who develops OTOY's Brigade version, helped me with the materials and the moving sun. I really love this scene, so I took no less than twenty screenshots for your viewing pleasure:

**Youtube video (6 minutes)**:

[http://www.youtube.com/watch?v=gZlCWLbwC-0](http://www.youtube.com/watch?v=gZlCWLbwC-0)



These graphics will be possible in games in the very near future. The Brigade engine can be used not only for games but for all kinds of virtual reality applications and photorealistic simulators. Imagine walking in a photorealistic 3D version of the ancient Rome, or a fully navigable and photoreal Google Streetview in 3D. With dedicated fixed function ray tracing hardware this could be done at 1080p/60fps.



**UPDATE: I'm on the**
## 31 comments:

2th!

Anonymous, you're coming from Kotaku amirite? :)

Very nice. What maps are used in this? Just a diffuse?

Amazing rendering. What I find most impressive, is the fact that the engine still renders accurate shadows and occlusion on objects that already reside in another objects' shadow; in most current-gen engines when this happens, they use a very black, rather awkward occlusion.. It's also very nice to see the shadows rendered more realistic; both soft-edge and linear (am I saying this correctly?) shadows. In current-gen engines, I am often annoyed that only one of the two is possible (CryEngine; almost complete soft-edge; Uncharted; completely linear shadows).




Amazing job for a real-time engine. I saw it was running on (two?) GTX580, any chance that through strong optimization the next-gen consoles will be able to support the engine?

Hope you guys are able to show some animation features of the engine soon! I would also love seeing some AI in action (if that's even possible, huge amount of work. Guess that using solely GPU resources spares the CPU for some nice agent behavior? ;).

Keep it up! Amazing work.

@RayTracey




1) Very nice video.

2) If possible, would you want to add the samples per pixel and rendering resolution to the info bar on the top of the renderer? Then we would know the settings for every video you make without you having to say.

3) If you added a timer since the last movement to the top bar, we could see how long it took for the still shots to render.

add Alemic support!


http://www.alembic.io/

Looks good - try fresnel shading to really make the scene come alive. Currently, the colors look flat.

Maybe it looks flat, because it lacks HDRI lighting?


yStand acerati

Hey Ray Tracey, lovely engine! Any chance we can get some videos from a really high end PC. I would love to see this running on an 8 gpu (8x7970 perhaps) system. Do you think the current brigade 2 engine from in house could converge/denoise in real-time?




example system: RenderStream VDACTr8

http://www.youtube.com/watch?v=CZ1IRQTqMMY

keep the videos and research coming!

Anonymous (post 4): most materials are diffuse, the rainpipes and water surface are reflective, railings and some floors are glossy.

Bram: thanks! yeah, the beauty of path tracing is that it's very robust and all effects work out of the box in any situation. It feels incredibly immersive to walk around in this scene.

Next-gen consoles will not be able to handle this kind of graphics if I go by their rumored specs. But we have a solution for that :)

Multiple anonymouses: the lighting (skylight, sunlight), tonemapping and gamma are work in progress

James W: with a good edge-preserving and temporally coherent noise filter, it can render completely noise free. What I believe would be ideal is to use dedicated ray tracing hardware, which could be 10 - 50x faster than a GTX 580 and would consume MUCH less power. This is where the industry is headed anyway, look at Imagination Technologies which is incorporating Caustic Graphics ray tracing HW in their upcoming GPUs. I can't wait to run Brigade on one of those :)

Awesome :) By the way... does brigade support voxels / volumetrics / atmospheric effects?

Yeh, polygons are so old tech, no need for BVH with voxels.

Care to explain, how this GPU (RPU?) architecture might look like ? Incoherent raytracing is rather hard to do efficiently in hardware. On top of that you still need like 100s rays per pixel. Also it is unlikely that any kind of filtering will magically fill in all details of perfect tracing.

As a side remark, if you do server based rendering/streaming you need video compression, where you already throw away quite a bit of detail.

With video codecs, you also do motion estimation, so you can like interpolate between frames...

So if you aim compressed video streaming, the filtering might be good enough. Eventually you end up with kind of blurry images losing high frequency detail, but as global illumination is typically low frequency information, it will not be hurt too much by the video compression.

Jan

@Sam,




beautiful scene, question, does the scene have any normal maps? BTW does Brigade support normal and specular maps?

-SK

These guys are doing a great job, but probably have limited resources afaik, like two coders + Sam, so don't expect them to have everything already. It would be nice to have like a webpage listing all features and a roadmap. As they are now like merging with Octane renderer, I assume, the idea is to create one code base, or maybe even create a new engine in OpenCL...

Some research on Caustic Graphics led me to:

http://caustic.com/dev_intro.php

To make use of the RTU (ray tracing unit), you will have to make use of OpenRL.

OpenRL makes abstraction of the hardware, underlying can be CPU, GPU and RTU.

I'm just downloading the OpenRL SDK, which looks to making use of CPU.

They also seem to have a renderer similar to Brigade called Brazil, for which a Brazil SDK is available.

very good examples here.

thanks for that but i see

one problem in all vids: quality.

please let you cam rest for

20-30s fixed in a position

so that people can see pt quality

coming up and noise disappears.

And where is there any news about Brigade of Sam? I tired to wait :)

Dima, Brigade doesn't support voxels atm




anonymous, you can sort the incoherent rays in a way to extract maximum coherence, these sorted ray batches can be traced more efficiently and are more cache-friendly

SK: no normal maps in this scene, but Brigade supports them. Specular maps are not supported

Anonymous: a dedicated webpage is i the works

Outstanding Work!




I wonder... can't you render the spp to a seperate imagebuffer and blur the result before you combine it onto the scene? So you can have better results with less spp and save some rendertime?

Mabe just a stupid idea :)

Keep it up!

Thanks. Yeah, some sort of filtering would be nice, I don't like losing any detail though, so the best candidate would be a detail and edge preserving filter that also runs very efficiently on the GPU.

Fantastic job. Simply fantastic.





You must be annoyed by all of 'ideas,' but I'm a traditionalist, and have one more to add to the pile! :p

Have you considered caching lighting? Certainly in a static scene, caching lighting would dramatically cut down memory bandwidth and paths traced per image (until lighting changed). As new surfaces are exposed, or objects change, they would need re-calculation, but in a mostly static scene, I'm guessing this would save tons of time.

Just a thought! Honestly, amazing work!

Oh, and if you're on Google Plus, I would love to add you to my circles. I am very interested in this type of thing. I am:

+Sean Lumly

Hi Sean,



first of all thanks!

Light caching is on Brigade's roadmap. It could probably speed up things quite a bit :)

;) Of course, I should have figured that caching was already on the list... :p











I'm looking forward to following the fantastic progress, which I assume that it will be available on this blog.

I was telling my circles about Imgtec's OpenRL just today, which is a bit of a coincidence in that I read a comment of yours that showed some interest.

I'm curious weather OpenRL will target GPU-compute (ala CUDA) in the short-term vs. dedicated hardware. Something tells me that future PowerVR will be given certain optimizations that work well with OpenRL outside of a full-on hardware acceleration. Certainly the programmable pipeline will likely utilize hardware like the Pixel shader, in fact the technology looks very much like the GL pipeline! And Imagination seems confident that they can squeeze this into a mobile device, which is inspiring!

One other thing that came to mind re: Brigade. It has to do with the way that motion blur is being done.

Currently, and correct me if I'm wrong, you're using around 3 framebuffers and producing a 'trailing' motion blur by blending the FBO in such a way as to make the latest render the most visible, and combining it with the 'old' blended FBO with a <1 opacity. The final blended frame then becomes the 'old' FBO, and the next frame render ensues.

A more realistic temporal anti-aliasing scheme would maintain multiple buffers (say 9 for sake of argument), and the central buffer (5 in this case) would be the most opaque. All other buffers would be blended and their opacity would falloff slightly by some normal distribution (or sin wave to save time), and this composite would form the final frame. Each new frame would 'push' the oldest frame (9 to start) off of the queue and become the first.

Now, of course you wouldn't have to continually allocate buffers in this scheme, you could just determine the offset of the leader, and with each new frame, the index of the leader would decrement and that FBO cleared and rendered to.

This would give the impression of physical camera motion blur, with an interaction latency determined by the buffer-queue length. Since the middle buffer appears to be the current frame, it lags n/2 behind the most recent drawn frame, but should still be acceptable. The benefit is that it should provide a realistic 'depth-of-field' like effect to motion blur, and even open the door to blending effects between the buffers to smooth out the final frame.

The downsides are that this would come at a memory hit to maintain all of those buffers, and a performance hit to blend them as well, so I don't know if this would be ideal as it could cut your framerate down. Since you're doing post in GL, many modern games blend multiple buffers, so it may be doable on 2x GTX580s.

Anyway, food for thought!

Wow, that's a pretty concise comment :)



about OpenRL/Caustic: I have no idea how PowerVR is going to pull it off, but I'm keeping an eye on their first GPU with ray tracing HW. I can only hope it's going to be an order of magnitude faster than my 2 GTX 580s.

The frame averaging is just a neat OpenGL trick that uses the accumulation buffer, I can blend as many frames as I want without any performance loss. Your idea sounds pretty good, but I'm not convinced about the lagging displayed frame, which becomes a problem at lower framerates.

Great point re:lower framerates! :)



This is especially relevant for a cloud-based renderer where I expect additional latency can't be welcome (no matter how small)...

In any case, I'll be watching this project with great interest!

Would it be possible for us to get a higher-Res video than YouTube? If you put a download via bit torrent, it could save you lots of bandwidth. =]

Post a Comment