---
title: Real-time path traced dynamic geometry in Octane Render
url: http://raytracey.blogspot.com/2012/07/real-time-path-traced-dynamic-geometry.html
author: Sam Lapere
published: '2012-07-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Quasi-random, more or less unbiased blog about real-time photorealistic GPU rendering

Wednesday, July 18, 2012

Real-time path traced dynamic geometry in Octane Render

OTOY NZ just released a preview build of Octane Render which supports instancing and real-time path traced dynamic geometry, check it out (1080p video):

I'm really looking forward to the time when instancing reaches gaming. There is such redundancy and bandwidth lost to scenes with largely repeating geometry!

Is octane to be the new brigade? Put another way: are they competing products?

Hi Sean, instancing is already being used by rasterized games, remember the launch games for the Xbox 360 like Ninety Nine Nights.

Octane and Brigade are actually complementary products. Octane will make no compromises on quality and Brigade will make no compromises on being real-time :)

Yes, of course... But I would expect that instancing via ray tracing would differ significantly to instancing via rasterization (I should have chosen my words better). As I understand it (and correct me if I'm wrong) instancing via rasterization means drawing a mesh multiple times and compositing the results for the final frame. I suppose this is similar enough to ray-tracing, though ray tracing will benefit far better as complexity increases.

Sam, probably you don't realize but your concept of real time rendering is strange. Anything that renders at 10+ frames per second, irrespective of actual number of rendered pixels per frame, pixel quality and image resolution you call real time. These are typical hollow phrases sales people tend to use.

Nik, this way of calling things 'real-time', causes it to loose all meaning.

It's like claiming a rendering algorithm that has super high quality anti-aliasing, taking several seconds to render an image, to be real time. Say for example 16x16 supersampling.

During animation you simply revert to 1x2 anti-aliasing, making it 128 times faster...

I usually call anything that can be manipulated at a reasonable turn-around time as "interactive" because you can interact with it; this can be from a few portions of a second to a few seconds. And anything that's aimed to be seamless (enough) to our human perception of continuous real-world time, as it happens, as "real-time".

"Real time" has nothing to do with fps, user experience or quality. It's a strict definition of rate of progression of time.

As it stands today, the term realtime means the video you are watching is running at the same speed as it is being generated/displayed on the users machine. For instance, a video could show a tech demo rendering frames at 0.001fps, but if this is the same rate that the frames are being generated on the actual machine, then it is realtime. The opposite of this would be a video that shows a animation running at 50fps, when in fact it takes a longer to do so (i.e 1 frame per hour).

What many people are wrongly confusing with 'realtime' is 'interactive'. They are very different. Interactive is about fluidity, fps and to a certain degree quality. This is very subjective

Maybe Sam can give his definition of real time, and add this as a side remark to his blog.

From the Siggraph Brigade entry: "In some “ideal” scenarios (scenes with open environments lit by a skylight or large light sources, with few indirect lights and simple materials), GPU-accelerated path tracing is now fast enough to converge at real-time frame rates"

Language is something means something slightly different to everyone, a definition is often altered to fit the perception of the majority, but maybe not be in the strictess sense correct. (what the definition of correct is the subject of anothe discussion)

Still, it doesn't mean that Vray RT publishers are correct just because they say so, does it?

Infact many of these GPU path tracers are realtime because they update as and when the user commands them to do so. Even if a frame hasn't converged to make a pretty image, the renderer can in theory instantly abandon the previous frame and start a new frame using the updated user information. This permits the user to control the output in real time (however ugly).

definition: re·al-time (rl-tm, rl-) adj. Of or relating to computer systems that update information at the same rate as they receive data, enabling them to direct or control a process such as an automatic pilot.

No where does it say how visually pleasing or enjoyable it would be to control a process. The latent period of many pathtracers is the time taken to generate 1 sample/pixel which is commonly less than 50msec. For some FPS gaming enthusiasts even 60fps isn't enough to have 'full' control. In contrast a Pre-rendered offline animation cannot respond to these changes.

Of course, I do understand what people mean when they call something 'realtime' but it would be much more informative to use a better word.

There is real time in games and real time in other industries (real time in aeronautics does not have that meaning at all, it is the fact that a system could react to any event at any time with a maximal predefined delay). Real time in games means > 10 fps. So a real time renderer aims to provide the best quality for the 30-60fps. If you are not doing a real time renderer, you are allowed to give a good result after 1 min or 1 hour. Interactive rendering allows you to produce a bad quality if it provides enough information.

Actually I don't care about how one defines real-time, it's all about the user experience really. Playing with Octane and Brigade on a powerful system is just blowing me away every single time, it's just unbelievable how photoreal and immersive these renderers are with a decent 3D mouse.

It's exactly the sort of tech that I have been dreaming of since 2001 and it's actually real now.

I agree with MrPapillon. Interestingly the phrase "realtime path tracing enging" means one thing to one person and the phrase "a realtime demonstration of a path tracing engine" means something different.

i think the misusage of the term "realtime" has lead to an unfair situation for products that can path-trace much much faster than octane or brigade. and thats a shame.

## 16 comments:

This == big deal...



I'm really looking forward to the time when instancing reaches gaming. There is such redundancy and bandwidth lost to scenes with largely repeating geometry!

Is octane to be the new brigade? Put another way: are they competing products?

Hi Sean, instancing is already being used by rasterized games, remember the launch games for the Xbox 360 like Ninety Nine Nights.


Octane and Brigade are actually complementary products. Octane will make no compromises on quality and Brigade will make no compromises on being real-time :)

Yes, of course... But I would expect that instancing via ray tracing would differ significantly to instancing via rasterization (I should have chosen my words better). As I understand it (and correct me if I'm wrong) instancing via rasterization means drawing a mesh multiple times and compositing the results for the final frame. I suppose this is similar enough to ray-tracing, though ray tracing will benefit far better as complexity increases.

Sam, probably you don't realize but your concept of real time rendering is strange.

Anything that renders at 10+ frames per second, irrespective of actual number of rendered pixels per frame, pixel quality and image resolution you call real time.

These are typical hollow phrases sales people tend to use.

Anonymous, what you don't realise is that in the computer graphics industry, "real-time" is used to describe anything with instant visual feedback.



This is real-time.

It does not describe the time it takes to render a finished image (100% convergence, etc) which may be several seconds or even hours.

Nik, this way of calling things 'real-time', causes it to loose all meaning.



It's like claiming a rendering algorithm that has super high quality anti-aliasing, taking several seconds to render an image, to be real time.

Say for example 16x16 supersampling.

During animation you simply revert to 1x2 anti-aliasing, making it 128 times faster...

I usually call anything that can be manipulated at a reasonable turn-around time as "interactive" because you can interact with it; this can be from a few portions of a second to a few seconds. And anything that's aimed to be seamless (enough) to our human perception of continuous real-world time, as it happens, as "real-time".

I think your all missing the point.



"Real time" has nothing to do with fps, user experience or quality. It's a strict definition of rate of progression of time.

As it stands today, the term realtime means the video you are watching is running at the same speed as it is being generated/displayed on the users machine. For instance, a video could show a tech demo rendering frames at 0.001fps, but if this is the same rate that the frames are being generated on the actual machine, then it is realtime. The opposite of this would be a video that shows a animation running at 50fps, when in fact it takes a longer to do so (i.e 1 frame per hour).

What many people are wrongly confusing with 'realtime' is 'interactive'. They are very different. Interactive is about fluidity, fps and to a certain degree quality. This is very subjective


Real time is objective, it just means 1x speed

Antzrhere, sorry, but you are completely wrong.




It is a common term used with unbiased GPU renderers. Look at Vray RT, for example.

Look on the octane site, for another example: http://render.otoy.com/features.html

See how it says real-time, and it doesn't mean what you said?

Maybe Sam can give his definition of real time, and add this as a side remark to his blog.


From the Siggraph Brigade entry:

"In some “ideal” scenarios (scenes with open environments lit by a skylight or large light sources, with few indirect lights and simple materials), GPU-accelerated path tracing is now fast enough to converge at real-time frame rates"

Language is something means something slightly different to everyone, a definition is often altered to fit the perception of the majority, but maybe not be in the strictess sense correct. (what the definition of correct is the subject of anothe discussion)








Still, it doesn't mean that Vray RT publishers are correct just because they say so, does it?

Infact many of these GPU path tracers are realtime because they update as and when the user commands them to do so. Even if a frame hasn't converged to make a pretty image, the renderer can in theory instantly abandon the previous frame and start a new frame using the updated user information. This permits the user to control the output in real time (however ugly).

definition:

re·al-time (rl-tm, rl-)

adj.

Of or relating to computer systems that update information at the same rate as they receive data, enabling them to direct or control a process such as an automatic pilot.

No where does it say how visually pleasing or enjoyable it would be to control a process. The latent period of many pathtracers is the time taken to generate 1 sample/pixel which is commonly less than 50msec. For some FPS gaming enthusiasts even 60fps isn't enough to have 'full' control. In contrast a Pre-rendered offline animation cannot respond to these changes.

Of course, I do understand what people mean when they call something 'realtime' but it would be much more informative to use a better word.

There is real time in games and real time in other industries (real time in aeronautics does not have that meaning at all, it is the fact that a system could react to any event at any time with a maximal predefined delay).

Real time in games means > 10 fps. So a real time renderer aims to provide the best quality for the 30-60fps.

If you are not doing a real time renderer, you are allowed to give a good result after 1 min or 1 hour. Interactive rendering allows you to produce a bad quality if it provides enough information.

Interesting discussion :)



Actually I don't care about how one defines real-time, it's all about the user experience really. Playing with Octane and Brigade on a powerful system is just blowing me away every single time, it's just unbelievable how photoreal and immersive these renderers are with a decent 3D mouse.

It's exactly the sort of tech that I have been dreaming of since 2001 and it's actually real now.

I agree with MrPapillon. Interestingly the phrase "realtime path tracing enging" means one thing to one person and the phrase "a realtime demonstration of a path tracing engine" means something different.

i think the misusage of the

term "realtime" has lead to

an unfair situation

for products that can path-trace

much much faster than octane

or brigade. and thats a shame.

Post a Comment