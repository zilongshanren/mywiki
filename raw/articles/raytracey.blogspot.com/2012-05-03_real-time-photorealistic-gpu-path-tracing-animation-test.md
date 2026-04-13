---
title: 'Real-time photorealistic GPU path tracing: animation test'
url: http://raytracey.blogspot.com/2012/05/real-time-photorealistic-gpu-path.html
author: Sam Lapere
published: '2012-05-03'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Brigade 2 real-time path tracing test of a (self-made) weapon in first person view and a simple animated character (Doom 3 fat zombie):

Things I'm working on for this scene:

- post processing effects like HDR bloom and motion blur

- GUI with sliders for spp, material properties, ...

- user-controlled car with camera following the vehicle

- physics

- a simple game: a Quake 3 style deathmatch FPS with an oldskool AI bot jumping over the roofs and some cars that will run over the player Frogger-style. The player will also be able to fire a grapple at a building's facade and swing in Spiderman fashion. Intricate storyline with unexpected plot twists TBD.

## 15 comments:

I simply cannot wait to see this! Very exciting!

Hey, Sam.. I was wondering something. Is the graininess of videos less pronounced on your system in realtime tests, than it appears in youtube video due to intra-frame compression? Something tells me that it would be.

What is the definition of 'real time'? Or yours?

I read 2fps on that image and I'm not sure that qualifies...excellent results though, I'm following your progress closely...keep it up!

Yes, it's a little bit better in real life. Youtube tries to find as much spatial and temporal coherency between pixels as possible and their compression algorithm completely breaks down with Monte Carlo noise. However it shouldn't be taht bad in the current video.


Another thing, the video is using two weeks old Brigade code (i.e. ancient code in Brigade terms), which doesn't have last week's 30% performance boost. Also, today Brigade got twice as fast at converging by moving some code to the GPU :)

Octo: the video will be 'real-time' for sure, i.e. 30 fps at 16 spp.

Cool I have time to breath between those daily explosions of awesomeness. The pic shows that big monsters, without coherency errors everywhere in their lighting, are much more impressive even without textures.

Thanks! :)






Yes, I can't wait to see how this looks with the updated Brigade engine -- 30% boost is significant. I'm also curious how newer hardware (eg. GTX 690) would affect performance further!

I just had one of those obvious-in-hindsight ideas that could improve visual fidelity (food for thought):

When the frame is drawn, there is a noticeable black grain while the path-tracer fills in the scene. A post processing effect, could sample pixels surrounding the black and replace it with some combination of the colours (eg. mean colour, excluding black) as not to leave the pixel black. This eliminates the black grain.

Since most objects should have general coherency in colours (especially among adjacent pixels), my intuition tells me that the human eye will perceive the scene very differently as it fills in. It should look like a quickly receding 'blur', and be less harsh than the black grain...

Just a thought! :)

Thanks Mr Papillon



Sean, I'm also curious about the 690, the first previews seem to indicate that its ray tracing performance is almost equal to the performance of two GTX 680s (SmallLuxGPU benchmark on Anandtech: http://www.anandtech.com/show/5805/nvidia-geforce-gtx-690-review-ultra-expensive-ultra-rare-ultra-fast/15)

Masking the black pixels is something I've thought about as well. It can be handled with image reconstruction techniques, adaptive sampling which focuses the sampling on noisy areas and a Gaussian or bilateral (edge preserving) filter. Unfortunately, filtering always means losing fine texture and geometry details, which I want to avoid as much as possible. But I'm certainly going to test filtering techniques at some point, to see if the visual improvement outweighs the loss in detail.

73.71%, does this mean once it hits 100% it converges on the final image/frame?

No, that number just indicates the ratio of real world to maximum theoretical path tracing performance

Hey Sam,




Maybe you already heard about it but I felt like sharing though:

Nvidia will be announcing CUDA 5.0 on May 14th to 17th on the GTC. I'm an excited about the performance gain which they announced.

As for the post processing motion blur you are trying to implement there is a nice document over at nvidias developer section: http://http.developer.nvidia.com/GPUGems3/gpugems3_ch27.html

In your first comment you stated that Brigades performance increased by 30% the other day and got twice as fast yesterday. Now, speaking about the particular scene in the screenshot - how fast does the image converge to a similar quality we see here?

Thanks for the moblur link, I'll have a look at it.


I've tested the new code with the same viewpoint as in the screenshot and it reaches fully converged quality at 1280x720 resolution in 700 milliseconds on 2 GTX 580s. The speed is utterly insane, I can hardly believe it myself. And everything is brute force, there's still so much optimization stuff we can do.

After adding some custom code (frame averaging) it's more like 300-400 milliseconds, i.e. fully converged 720p frames at 2.6 fps :D


Something else I've noticed: the fans on both my GPUs are running at full speed all the time now, which is a good sign (Brigade is now constantly reaching 96-97% of theoretical maximum performance)

i'll upload a video in a minute.

Post a Comment