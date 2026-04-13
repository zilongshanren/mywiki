---
title: Finding Slow Frames With Instruments 8.0
url: http://hacksoflife.blogspot.com/2016/09/finding-slow-frames-with-instruments-80.html
author: Benjamin Supnik
published: '2016-09-20'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

There are two kinds of programmers: those that download a brand new version of X-Code on the very first day, and those that laugh at them when being an early adopter doesn't go well for them.


I am definitively in that second category; my view is that most software has gotten "good enough", so when a new version comes out, you pay a lot of disruption costs for not a lot of benefits. It's been years since a major OS update has shipped a feature I actually care about.


Yet the last two versions of X-Code actually have delivered new features compelling enough to make a tool-chain upgrade worth it. X-Code 7 delivered


X-Code 8 has Thread Sanitizer, which I will blog about shortly, but this post is show and tell from the new version of Instruments, which finally has a clean way to annotate your timeline.*

####



There's one case though where an adaptive sampling profiler falls on its face: if you need to find a single "slow frame" in a sea of fast frames.


Imagine we have 300 consecutive frames, each taking about 15 ms. In other words, our game is running solidly at 60 fps.


Then we hit a "slow" frame - some part of the frame takes 60 ms (!), making that frame 4x as slow as the other ones. This is a visible "hitch" to the user and a bug.


But here's the problem: we have 4500 ms of good frames and 60 ms of bad frames. The bad frame represents 1.3% of the sample data. Even if the bad frame is made up of one single 45 ms function call that pushed us past our budget, that function is < 1% of the sample data and is going to be buried in the noise of non-critical every-frame functions (like the 1% we spent on the overlay UI).

####



Points of interest is part of the system trace; the system trace is a fairly heavy instrument, so unfortunately you have to use it in Windowed mode - that is, tell it to record the last N seconds, then bail out within N seconds of something happening. Fortunately on my laptop I can run with a 15 second window


The newest Apple OSes have a framework to put debug markers into your app, but fortunately if you need to run on older tech, Apple has documented the secret spell to get a marker in legacy OS:




I have an SSD and all I was doing was circling around a parked plane, so this was really weird. I took a look at the back-traces around the VM activity and the GLSL shader compiler was being run.

####






Chris managed to psychically debug this: X-Plane dropped frames when I hit command-tab and switched out of X-Plane and back to Instruments to stop recording. Apparently every service in the universe on my machine is programmed to briefly wake up and reconsider its life choices when the foreground application changes.


The good news is that this kind of crazy activity was not at all present in the regular operation of the sim, and "sim drops frames when wildly changing between other apps" is not a bug I have to fix.




* Timeline markers in a profiler are not revolutionary at all. VTune has had this for at least longer than I have been using VTune. But even if a tool-chain feature is not new to the universe, it is still very useful when it is new to a

I am definitively in that second category; my view is that most software has gotten "good enough", so when a new version comes out, you pay a lot of disruption costs for not a lot of benefits. It's been years since a major OS update has shipped a feature I actually care about.

Yet the last two versions of X-Code actually have delivered new features compelling enough to make a tool-chain upgrade worth it. X-Code 7 delivered

[Address Sanitizer](http://hacksoflife.blogspot.com/2016/07/this-is-why-asan-makes-big-bucks.html), which was a huge step forward in catching memory scribbles.X-Code 8 has Thread Sanitizer, which I will blog about shortly, but this post is show and tell from the new version of Instruments, which finally has a clean way to annotate your timeline.*

#### Finding Dropped Frames

Adaptive Sampling Profilers are spectacular for finding performance problems, because by the definition of their sampling, they are better at finding the code that's taking the most CPU time. If you want to focus your effort on performance problems that really matter, an adaptive sampling profile will tell you where to aim.There's one case though where an adaptive sampling profiler falls on its face: if you need to find a single "slow frame" in a sea of fast frames.

Imagine we have 300 consecutive frames, each taking about 15 ms. In other words, our game is running solidly at 60 fps.

Then we hit a "slow" frame - some part of the frame takes 60 ms (!), making that frame 4x as slow as the other ones. This is a visible "hitch" to the user and a bug.

But here's the problem: we have 4500 ms of good frames and 60 ms of bad frames. The bad frame represents 1.3% of the sample data. Even if the bad frame is made up of one single 45 ms function call that pushed us past our budget, that function is < 1% of the sample data and is going to be buried in the noise of non-critical every-frame functions (like the 1% we spent on the overlay UI).

#### Mark My Words

What we need is some kind of marker, showing us*where*in the timeline the bad frame occurred. Instruments 8 adds this with the "points of interest" track, which is basically user-data where you can mark what the app was doing.Points of interest is part of the system trace; the system trace is a fairly heavy instrument, so unfortunately you have to use it in Windowed mode - that is, tell it to record the last N seconds, then bail out within N seconds of something happening. Fortunately on my laptop I can run with a 15 second window

*and*the high frequency timed profiler and the machine is okay (barely). I would describe this performance as "usable" and not "amazing" - but then the Instruments team probably has access to some performance tools to make Instruments faster.The newest Apple OSes have a framework to put debug markers into your app, but fortunately if you need to run on older tech, Apple has documented the secret spell to get a marker in legacy OS:

`#if APL`


#include

#include

#endif



`syscall(SYS_kdebug_trace, APPSDBG_CODE(DBG_MACH_CHUD,0) | DBG_FUNC_NONE,0,0,0,0);`


That puts a single marker into the timeline, and it is what I used to see my frame boundaries.


Here's a zoom-in of my timeline - the S in a circle are the frame boundaries - the short spans are solid fps and the long spans are the drops.


The middle blue track is VM activity - as you can see, the VM manager goes haywire every time we glitch.Here's a zoom-in of my timeline - the S in a circle are the frame boundaries - the short spans are solid fps and the long spans are the drops.

![](../../assets/9873460bdc5f5674.png)

![](../../assets/9873460bdc5f5674.png)

I have an SSD and all I was doing was circling around a parked plane, so this was really weird. I took a look at the back-traces around the VM activity and the GLSL shader compiler was being run.

#### You Know That's Really Stupid, Right?

One of the purposes of this blog is to act as a confessional for dumb things I have coded; I try to bury these at the bottom of the post so no one sees them.

In this case, X-Plane has an inherited legacy that haunts us: on-the-fly shader compile. I will write another blog post about OpenGL and Vulkan and why this will never

*really*be fixed until we go to a modern API that promises to not compile on the fly behind our backs, but for now the thing to note is that as you fly, X-Plane sometimes discovers that it hasn't compiled the terrain shader with the right options for the particular scenario it hits, which is a function of time of day and weather, the particular scenery, the rendering pass, and user rendering settings.
Here we can do even better with the points of interest: we can mark

*regions*of interest like this:```
``````
syscall(SYS_kdebug_trace, APPSDBG_CODE(DBG_MACH_CHUD,1) | DBG_FUNC_START,0,0,0,0);
```

/* do really slow stuff */

syscall(SYS_kdebug_trace, APPSDBG_CODE(DBG_MACH_CHUD,1) | DBG_FUNC_END,0,0,0,0);


In the picture above, you can see the red bars at the very top - these mark the in-frame shader compiles, and they exactly fit the 'extra space' in the long frames. Problem child found!



So I switched to the "core" view, where the system trace shows you what each CPU is doing. I have an i7, so we can see 8 virtual cores. New to Instruments 8, the orange sections are where there are more runnable threads at reasonably high priority than there are cores - in other words, performance is degraded by running out of core count.


The play-head annotates what process is running over any given section, and the amazing thing about this trace is that as you scrub over all of those tiny blocks, it's almost never the same process twice. What happened?#### What Was That?!?!

I did hit*one*dropped frame that did not have a shader compile in the middle - the sim went totally crazy with VM activity, and yet the time profile showed*nothing*unusual. It didn't make any sense.So I switched to the "core" view, where the system trace shows you what each CPU is doing. I have an i7, so we can see 8 virtual cores. New to Instruments 8, the orange sections are where there are more runnable threads at reasonably high priority than there are cores - in other words, performance is degraded by running out of core count.

![](../../assets/be0b0fd15b2b7056.png)

![](../../assets/be0b0fd15b2b7056.png)

Chris managed to psychically debug this: X-Plane dropped frames when I hit command-tab and switched out of X-Plane and back to Instruments to stop recording. Apparently every service in the universe on my machine is programmed to briefly wake up and reconsider its life choices when the foreground application changes.

The good news is that this kind of crazy activity was not at all present in the regular operation of the sim, and "sim drops frames when wildly changing between other apps" is not a bug I have to fix.

* Timeline markers in a profiler are not revolutionary at all. VTune has had this for at least longer than I have been using VTune. But even if a tool-chain feature is not new to the universe, it is still very useful when it is new to a

*platform*if you are using that platform. VTune's ability to spot long frames two years ago was of no help to our iPhone app!
Heh, what a coincidence, this week I'm trying to convince V-Tune to show timeline markers for things I'm interested in, but I failed.


ReplyDeleteCan you tell me what API are you using to create the markers? Does it work in basic hotspot analysis mode?

For basic frame boundaries, I'm doing this:











Delete#if VTUNE

if(g_vtune_xplane)

{

__itt_frame_end_v3(g_vtune_xplane, NULL);

__itt_frame_begin_v3(g_vtune_xplane, NULL);

}

#endif

where g_vtune_xplane is my vtune domain created via

#if VTUNE

g_vtune_xplane = __itt_domain_create("X-Plane");

#endif

One more - here's annotation of a task on a queue loop:

const char * who = t->get_runloop_name();

#if VTUNE

__itt_string_handle * tname = __itt_string_handle_create(who);

__itt_task_begin(g_vtune_xplane,__itt_null,__itt_null,tname);

#endif

{

t->do_runloop_work();

}

#if VTUNE

__itt_task_end(g_vtune_xplane);

#endif

If nothing else, hopefully that points to the right man pages to look up.

Disclaimers: it's been a while since I ran this stuff, and I think there's a new vtune out that I haven't upgraded to.

I'm afraid I can't remember whether I was using basic hot-spot analysis or concurrency analysis. I've definitely used both.

(One thing I do like about instruments is the a la carte approach to sampling data. Unfortunately the overhead in Instruments is high enough that picking a ton of instruments isn't a great idea.)

Thanks, I'm using those, too, but they are not that useful when the application is not a game or something that is running at high framerate.


DeleteI thought you've found a way to emit user markers, which can be used to mark the start/end of a bigger task running on multiple threads.

Interesting read. Just a heads-up: your angle brackets after #include became HTML. What's this sys tag of yours?

ReplyDelete