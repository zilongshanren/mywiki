---
title: 'Real-time path tracing: racing game'
url: http://raytracey.blogspot.com/2012/09/real-time-path-tracing-racing-game.html
author: Sam Lapere
published: '2012-09-11'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://raytracey.blogspot.co.nz/2011/09/unbiased-stunt-racer-in-hd.html](http://raytracey.blogspot.co.nz/2011/09/unbiased-stunt-racer-in-hd.html)). The game could run in real-time with path tracing because it only used spheres and boxes as primitives (about 50 primitives in total). Here's a screenshot:

Now, one year later, we can path trace dynamic scenes containing millions of triangles in real-time with Brigade, so the progress we made was not that bad. As a proof-of-concept, we've created a small racing game featuring a tiny race car, complete with physics. Thanks to some further optimizations, Brigade is now rapidly approaching a point where it can instantaneously render noise-free photorealistic images. The video below isn't even using the latest code (which has massively improved support for dynamic scenes) yet. The photorealism you can get out of Brigade nowadays is unrivaled and unique in the world of game engines. The potential of this tech is endless: for example, the automotive industry can render a photoreal and interactive car commercial in real-time or allow their customers to virtually drive around in a photoreal 3D city with the car of their dreams reflected in the display windows...

## 24 comments:

Wow, this is incredible. What hardware does that run on? I would never have dreamed to see real-time path tracing until some time around 2050 ... ;-)

Thanks. It's running on a couple of Geforce cards.

It's NOT path tracing, it's "just" AO + skydome. Impressive nonetheless, but Sam please don't try to give the impression that this fact is just some minor detail. In a scenario like this it may not matter that much (although I can clearly see it), but there are situations where it becomes absolutely visible that it's only a pretty crude approximation.

@mrhankey: I don't even know where to begin. Look at the static screenshots - the reflections show nearby objects without aliasing. It would require a very high resolution skydome to do that. Same with the lighting - there is no stepping/jaggies on the edges of the shadows, which would mean that the shadow maps would have to be very high resolution, or very well filtered.




The dead giveaway for me is the noise though. Path tracing inherently creates noise as a result of using random light bounces to get the "AO" effect. Again, this noise could be added in a post process with a pixel shader, but why would someone intentionally lower the quality of an image just to be able to claim that they're using a different technique?

Anyway, enough feeding the trolls.

Sam, this scene is beautiful and I'm amazed that you can render it in real-time; but, as always, the video on YouTube is heinously noisy with MPEG artifacts. Do you have any plans to tackle the noise issue(e.g. selective blur or Kalman filter)? Alternatively, could you upload the videos in a higher resolution, or bump up the denoising filter on your video encoder?

There's a fault in my post above ... rendering seems to be (whitted style rt) + AO + sampled sun + ambient term, not AO + sky. Sorry about that.


@Lachlan: First off, you say that the lack of jagged edges on shadows/hq rt reflections are the proof of *path tracing*. No, that's wrong. It indicates that there is some sort of ray tracing going on instead of traditional rasterization. Ray tracing != path tracing, my dear friend.

Once again: there is traditional rasterization (shadow maps and cube maps for reflections), there are different styles of ray tracing which are not solving the rendering equation like whitted style ray tracing (that's the sort of method used in those pictures/videos), and there is true path tracing which solves the rendering equation qith arbitrary precision (and is therefore 100% photorealistic).

And by the way, I don't know of any way to use a Kalman filter to reduce the noise stemming from quasi monte carlo rendering processes. Kalman filtering is used to estimate the state of a certain model. For that to happen you have to formulate a model in a so called state space representation. You simply can't do that with path tracing images with noise.

Please don't state that I am a troll. Your post tells me that you are clearly lacking some important knowledge when it comes to ray tracing. I have experience with both implementing a sophisticated path tracer and in the field of signals and systems. So please get yourself familiar with the stuff before you blame other people.

mrhankey, I won't go into the details of how Brigade renders the image, but the assumption you made is incorrect.


Lachlan: the mpeg artifacts in the youtube video are indeed extremely ugly resulting in splotches, the noise as it is displayed on my screen is very uniform and also visually pleasing. I might upload a much better video soon.

Sam,






I think you should just upload a 5 second video(uncompress AVI) of the same scene. Upload it to server somewhere.

Doing this will show properly how fast it converges on a result, and we get to see how the noise looks without the lame youtube artifact.

Why 5 seconds? well because the file would be HUGE otherwise :P

make it 720P if u do decide :)

PS> is this running the latest Brigade code(post Siggraph)?

@Sam: The way Brigade renders here must be a hell of a lot closer to what I posted than to what path tracing would look like. Perhaps I'm not 100% correct but I must be very close.

Can you then at least confirm that this is NOT path tracing and that this does NOT incorporate any sort of indirect light bounce (apart from AO)? Thanks.

Good scene and some car physics (hope to see video with updated code!); btw - is GTX680 video good for this stuff? I hear NVIDIA made some simplifications in GPGPU functions of this chip series...

The physics is great on that video, love it!


More info about Brigade Technology can be seen here :P

http://igad.nhtv.nl/~bikker/btech.htm

hio! nice demo, pretty impressive.



still i agree that i don't see any signs of pathtracing (bolor bleeding, bounce lighting, specular reflections, etc), i only see a constant blue colro coming from the dome with ambient occlusion and a yellow directional keylight. this is raytracing going on here, but not pathtracing. of let me put it in other words, if there is pathtracing, there must be something wrong with the material brdfs, cause it looks like direct lighting + AO to me.

still very impressive of course!

Nice work Sam ;-) arjanvanwijnen

Yeah no color bleeding means you lack features in comparison to the Unreal Engine 4. That means if it does not ship directly with the raytracing engine, it would have to be hacked in some way.

I remembered the communication to be more informative in the past and less a PR job (or Unlimited Detail PR).

The image quality looks awesome in some pictures compared to games' lighting. I am waiting for a scene with tens of lights and particles though.

Sam, how about a video of night-time car driving (where the primary light source are car's headlamps)?.. I guess there would be too much noise?

The stills look nice, but it's hard to be impressed by "realtime" when the compression of the video is that bad... can't you upload a proper 720p/1080p to Youtube?

It's fantastic how far the technology has come in such a short time. You guys should really take advantage of a completed game's content to demonstrate this for people. Why not import OpenArena's levels and gameplay to let people use a raytracing engine as more than a tech demo?

@mrhankey:


You are so wrong its funny in a way, Brigade is a path tracing engine running in realtime using inthis case two Nvidia GTX580's.

I think the scene doesnt show the colour bleeding off of things too clearly but it definately is path tracing, I know because Ive mucked about with earlier incarnations of the brigade engine source code and Ive written my own pathtracer...

i like it... i'm a vfx 2d guy, and not a huge head but imo..




the biggest thing that gives this away as non photo-real is the lack of motion blur.. several applications do gpu motion blur so hopefully this is possible for you?

...also the upshot of motion blur would be that it would hide the noise artifacts for most of the time ;)

great work, keep it up - it wont be long now before film and computers games meet...

I don't see any signs of path tracing, but indeed interesting. The demo shown in the video is very catchy and splendid.

I even have been getting a lot of helpful and informative material in your web site.

mermaid world summit

Though your post is exact one year old but i am looking for this game from many days and after landing to your blog my search is over much appreciated effort you have put in thanks.


online strategy war games

I am surprised why other specialized don’t perceive your site I’m greatly cheerful I discovered this. minecraftium


congratulations guys, quality information you have given!!! code xbox live gold gratuit


Your work article, blogs I mean over all contents is must read material. Get more info about Abschluss Pruefer

lliam

Post a Comment