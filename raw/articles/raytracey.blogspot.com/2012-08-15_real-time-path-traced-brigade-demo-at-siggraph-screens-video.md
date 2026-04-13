---
title: Real-time path traced Brigade demo at Siggraph (screens + video)
url: http://raytracey.blogspot.com/2012/08/real-time-path-traced-brigade-demo-at.html
author: Sam Lapere
published: '2012-08-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Real-time path tracing is back. I haven't posted Brigade updates for a while, but development has never been stronger. This post is for the unhappy few who weren't able to attend Siggraph this year and couldn't witness our face-meltingly awesome Brigade demo with their own eyes. For your convenience, I have captured a video and a few screens of the Brigade demo, which you can see below.

Brigade's path tracing performance has gotten an enormous boost once again (thanks to the awesome work of Jeroen van Schijndel and Jacco Bikker), this time specifically for dynamic stuff. The demo shows a real-time dynamic water mesh, a skinned game character (from the IGAD student game 'It's about time') and an exploding horse. Since Siggraph the performance for dynamic scenes has almost tripled again.

What you see in the video is not exactly what was shown at Siggraph. The actual Siggraph demo was rendered with real-time path tracing at 1280x720 resolution at 60 fps and was running in OTOY's cloud with post processing. (My local system is not capable of video capturing and rendering with Brigade at 720p, so I had to turn down the resolution to get an acceptable framerate, the video is also using pretty ancient Brigade code, without the dynamic optimizations).


Without further ado, here's some screenshots and a video of the future of real-time graphics. Enjoy!

Without further ado, here's some screenshots and a video of the future of real-time graphics. Enjoy!

Fin.

## 15 comments:

Future of realtime graphics is here ^__^

Sam...why have some bits of the Streets of Asia scene missing in this video - e.g. the ivy that hangs down on the all just to the left of the big tunnel entrance it is missing? ( I quite liked that bit!)

Nice work there. :)


I am curious about character animations within Brigade. Is it already possible? How does it affect performance?

Sam,



I really love the approach you guys took this time around, with having the female character walk around via a over the shoulder camera. Keep pushing in that direction as far as presentation, it make it feel very much like a game.

PS> work on the over the should camera abit, check out Resident Evil 4 game for a good example, or Gears of War.

Thanks for the great comments everyone, make sure you're at E3 this year for our next unveiling ;-)




anonymous: character animation works pretty good, just watch the video till the end :) Brigade has been severely optimized for rigid dynamic objects, deforming meshes and randomly moving triangles in the past weeks (an early version of this tech can be seen in the video).

Hey Sam!




First off all: Thanks for the update!

It looks quite promising but I don't really get why you used "pretty ancient Brigade code" in the video? Since you are close to the source what stopped you from using the latest code? :D

Sam,



I thought E3 is over with? Maybe you meant next year(2013)?

@anon 4:42, I think the ivy was removed because Brigade doesn't support alpha channel on TGA files yet.

What hardware was used to run this demo? :)

Btw, if i whant to make an commercial benchmark app on Brigade engine - when SDK will be avalible for that? Is indie licencing planned (like 20%-30% royality to SDK creators)? Actual...

astroKevin: the video uses the Brigade code that was updated during Siggraph time. In the last 2-3 weeks (after Siggraph), the dynamic system has gotten a very large performance boost again (close to 3x), which is not reflected in the video. That's why i called it ancient code.







Anonymous: I was joking when I said Brigade would be at E3 2013. It's still a possibility though, GDC is very likely too :)

About the hardware: I used two Fermi cards to capture the video, the actual framerate (when not capturing video) is about double what you see in the video.

Lex4art; a benchmark like Unigine Heaven would be a great idea, I've been thinking about it as well, it could be used as a GPU compute benchmark whenever a new video card launches. About licensing for indie devs, we're going to announce that soon as well.

With the recent performance improvements for dynamic scenes, Brigade could be used for a photorealistic Riven-like adventure/puzzle game. We just need someone who can create extremely detailed and vibrant game worlds like this

Sam,


great to hear indy license will be announce soon, do you guys at otoy have a roadmap laid out for Brigade? Will Brigade get an official forum on the otoy website?

I dig the screenshots with the sun,looks more natural!

What if put more computation into center of the screen initially and post-blur noisy area and progressively increase circular(oval?) area of sharpness?


Was discussed somewhere (timothy lottes) recently in a bit different context but may suit this as well.

Contact Cyan ask if they still have all the scene files and if they would like to do a real time remake of Riven, Exile etc.


When the chess piece disintegrates it turns into triangles I thought Brigade was a voxel based engine.

Post a Comment