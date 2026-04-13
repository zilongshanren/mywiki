---
title: New Prey 2 screenshot
url: http://graphicrants.blogspot.com/2011/08/new-prey-2-screenshot.html
author: Brian Karis
published: '2011-08-10'
source_blog: Graphic Rants
source_site: http://graphicrants.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

## Wednesday, August 10, 2011


### New Prey 2 screenshot

It has been a long time since I updated this blog with substantial content but I wanted to point out that Bethesda just released this new screenshot of Prey 2. It's a great shot but it's also a fantastic demonstration of some new graphical features I added to our latest build of the game.

First, there's the depth of field in the background which is HDR circular bokeh DOF.

Secondly, in the puddles on the ground, you will see screen space reflections. They aren't planer reflections, they work on every surface and run on every platform. SSR really adds a ton of dimension and accuracy to our wet, metal filled, alien noir city. I can't talk yet about how it works unfortunately.

So, check it out and tell me what you think. Hopefully in not too long I can start talking about how some of the tech works but for now you just get a glimpse.

-Brian

## 11 comments:

Why can't you talk about it? Other games have already shipped with ss reflections.

It's neat that you can write code to make depth of field work, but using it in your game makes any given frame significantly less interesting. Maybe it's not as bad when you can move around and explore, but in a single screenshot I feel like I'm being denied access to look at the detail of all that stuff in the scene besides his jacket.



This is normal in film, where the audience is a passive observer, but in an interactive medium I expect to be able to look at things unhindered.

Reflections are neat btw

What games have shipped with screen space reflections? I'm not aware of any.

Brian, Crysis DX11 patch has screen-space reflections; they already talked about it at SIGGRAPH. Their implementation is definitely not rocket science - trace a ray with depth checks, along with several fading heuristics to make reflections fade out near problematic areas. So it's just a lot of tuning.

I'm not at siggraph so I didn't get to see Crytek's presentation unfortunately. I'll have to wait for the slides to be posted to check it out. I figured they may be doing something similar but their reflections were an ultra option on PC and not supported on xbox or ps3. As I mentioned, this implementation is pretty fast and supported on all platforms.

I don't think their implementation relies on any DX10-specific features - it's just a performance hit (which obviously depends on total visible area of reflective objects and the ray sample count). And since they shipped this after the game release, it's understandable that the effect is not present on consoles - even if there's enough performance/memory, justifying a console patch release for a couple of visual improvements is hard.

Is that a PC or Xbox screenshot? Because how impressed I am depends greatly on which platform it is =)




COD:BO had a few areas with SSR, but they looked pretty bad, what you have is much higher quality. Personally I dislike the technique as I can easily find where it breaks down while playing the game normally, even in the high quality implementation in the Crysis 2 patch.

For the DOF, that would be really good quality for xbox but not very interesting for high end PC. It's lacking an interesting shape and the hard edges around HDR brights that you get in out of focus regions.

http://h5.abload.de/img/bokehdof_01_logo_textojz3.jpg

Also I agree with jrr, DOF needs to be used carefully so that only uninteresting parts of the scene are out of focus. In that shot I really want to see the background and it's obscured.

We take all screenshots on PC because that's where the screen shot tools are but the question is what settings did they take the shot at because the medium settings should look identical on xbox and ps3. I'm not sure but I'd expect high. Nonetheless the differences are fairly small between those quality settings. On high the SSR is done at full res vs half and for DOF there are more samples. The DOF is very similar to Crytek's console version (http://www6.incrysis.com/screenshots/crysis2_depth_of_field_with_bokeh.jpg) in that it just takes samples in roughly a circle shape. As far as why it may look better it could our support for full HDR color of the screen but it is probably mostly the type of scene we have shows off bokeh more. Ramping up settings for PC hasn't gotten much attention yet. I'm sure we'll be adding a lot more PC only features or settings as development progresses.


On the topic of DOF use, for screenshots it's the artist's responsibility to use it artistically. During gameplay I assure you it won't be blurring out stuff you will want to see because that is a pet peeve of mine as well. It's an argument I've had with a few folks. No, do not blur out the sky all the time because when I look at it I better be able to focus on it. When I look at the horizon in real life it's crystal clear. If I can't focus on things I'm instantly not immersed. To pull that off effectively in game is not a trivial matter but I'm hoping we can use it for more than just the obvious controlled cases such as look at gun, menus, cut scenes, etc. That's something I'm continuing to investigate.

Looks very nice.


Will you be using SSR as screen space specular ambient occlusion as well?

Sweet, jus found your blog man, I watched the Prey 2 demo a while back, and man, it's totally nice to see more info on that here. Cheers for that man, will be following your updates from now =) Thx's muchly =)

I know this post is old but I want to ask if you're only reflecting bright parts of the scene, or if you're reflecting the whole scene

Post a Comment