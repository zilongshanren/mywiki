---
title: Real-time GPU path traced Gangnam style
url: http://raytracey.blogspot.com/2013/03/real-time-gpu-path-traced-gangnam-style.html
author: Sam Lapere
published: '2013-03-04'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Not that many updates lately, during the last two months we've been working on a kick-ass Brigade tech demo that will be shown on a conference in the second half of this month. I'll post screenshots and videos posted after the event, but in the meantime we're still doing some smaller tests, such as this as animated character instance test. The video and screenshots are rendered with Brigade's superfast path tracing kernel (maxdepth 6) and show 12 instanced characters animated in real-time.

**Update**: Some teaser images of a new scene, rendered in real-time with very nice color bleeding and real-time post processing:

More to come soon

## 42 comments:

Would be complete with some music :)

All of the shiny makes it that much more obvious that you're not rendering caustics. :-/

zproxy: I added a soundtrack to the video, sadly Youtube has only a limited selection of cool royalty free music


friedlinguini: tbh I don't care about caustics that much, I think it's way overrated in the rendering community. Rendering caustics can be pretty for the sake it, but most people won't notice it if it's lacking from a picture. That being said, Brigade has a bdpt kernel that can render most caustics pretty efficiently and very fast (the video is not using it). There are much more important visual cues besides caustics that path tracing offers over other rendering algorithms which can make a picture look completely real.

Sam, you mention that in this example brigade isnt using bdpt, is it using a pt or direct lighting only kernel?

It's pretty cool. What's the performance, resolution, GPU type and number for this demo? :)

Anonymous: vidoe and screenshots were rendered with path tracing, it gives the best results in interiors. Interiors also converge extremely fast with Brigade's path tracing kernel, in real-time when there are enough lights in your scene and you keep all the nice effects like color bleeding, soft shadows, depth of field etc.



Anonymous2: thanks. the performance is staggering, there is no comparison :) I used two cards for this video, but we also have a system with 4x 680 GPUs on which Brigade can do pretty much noiseless interiors in real-time (15-20 fps) at 1080p with a special kernel, provided the scene is lit with a sufficient number of mesh lights.

On a sidenote, the Geforce Titan is absurdly fast in Brigade, it's more than twice as fast as a gtx 680 and even beats a gtx 690 in performance. It's by far the best card since the legendary gtx 580 for path tracing. Plus it has 6 GB of RAM. I was initially disappointed with Kepler, but now GPU rendering has a very bright future again :)

Hi Sam..Last screenshots are very cool.. But I think you need use more realistic models of palm trees or maybe other trees (geometry + textures ) in the scene ))


Good to see a post again :) and good luck with the conference! I'm sure you'll ace it

I suppose the utopia pictures have had some time to converge as usual? Or is it noiseless like that in rt?

Hi Sam, I'm pretty interesting about the "noiseless quality with special kernel" in your comment "...do pretty much noiseless interiors in real-time (15-20 fps) at 1080p with a special kernel,..."



Is the kernel still physically based, unbiased, such as UDPT, BDPT? If yes, I would say it's pretty amazing.

Thanks.

Wow Sam! This looks fantastic, and it's really encouraging to hear of near-noisless realtime with a mere 4 680s. Thankfully, Moore's law will ensure that a single GPU should do this reliably in the near future. And if optimization continues, this time horizon shrinks further.


Game developers should start seriously considering bdpt for future titles!

IL: Thanks, the palm trees came with the scene, we haven't had any time yet to tweak them.






Paul: Thanks, that's the plan

mrhankey: the utopia screenshots are real-time on a system with 2x gtx 690s and 1 gtx 680. The screenshots of the interior were captured on a system with 1 gtx 590 and 1 gtx 680, I'll post something new next week.

Anonymous: yes, that kernel I was talking about is unbiased path tracing without any filtering. It has a specific optimization which costs about 10-15% in performance but can drastically reduce the noise in interiors compared to using multiple importance sampling alone.

Sean: exactly, the GTX Titan has proven to be an excellent card for path tracing. Both Octane and Brigade run more than twice as fast on the GTX Titan compared to the GTX 680. This result was completely unexpected and was a very pleasant surprise, considering the relatively weak performance of the first Kepler GPUs compared to Fermi.

as everything before. much too noisy ! the still images are looking ok but the movies are really sh... is there

demo availabel that i can use on my own ?

Hi Sam,




The evolution of this engine is really incredible..!

I'm wondering why there's never any roughness in the materials. All your exemple always shows perfect mirrors. How will really rough materials affect the rendering time. It affects a lot classical renderer like Vray, so it should have some effect on Brigade too.

... What is the final purpose of brigade? Is it just a tech demo, a pure research project ? or will it really be released as a game engine ? Eat by octane ? Is there any chance to see it release as a stand alone solution (or better, as a plugin for other software .. I would love it see integrated with sketchup !)

Sam, I’ve been captivated with some of the work you and your team have produced. This video proves to me that real-time path tracing is not a viable solution. Gutted but happy in I know what direction to go from now.

Anonymous: yep, gotta love that noise :) sorry, but there's no demo available





Mr WIP: rough glossy materials still need some work in Brigade.

>> What is the final purpose of brigade? Is it just a tech demo, a pure research project ? or will it really be released as a game engine ? Eat by octane ? Is there any chance to see it release as a stand alone solution (or better, as a plugin for other software .. I would love it see integrated with sketchup !)

Actually all of the above, we're also working on an editor now to make it easier for indie game devs.

KingBadger3D: I think it's actually very viable for games and in the very near future as well, but tastes differ I guess :)

KingBadger3D, you should also consider the big difference on time and efforts required to produce the same quality with a rasterizer.

Producing content for path tracing techs will certainly not be of the same order of magnitude.

Hi Sam,




once again you give a great look of the bright future of the 3D rendering engines. No doubt that this tech will be used in a few years in the broadcasting area also.

I would like to make some artistic installations here in Paris, but I want it to be interactive with the public. Using the leap-motion and Brigade should help me a lot. Do you know when or if there will be a public version soon ?

Great work from you guys at Otoy.

This engine would be freaking

perfect if it mastered also

Tessellation.

The animation looks impressive.

However I'm suspecting this is not real skinning.

Could it be that all frames of the model are precalculated ?

Ciboulot: Thanks. Unfortunately, I don't have a timeframe of Brigade's availability yet. It should be soon though.









colocolo: the beauty of Brigade is that you don't need to do tesselation, we can do 60 billion polygons at 30 fps :) We'll be showing that very soon at the GTC. Also, yesterday we tested a ZBrush model with 28 million unique polygons on Octane (over 4 GB of mesh and texture data) and we were able to get 40 fps on 1 GTX Titan with path tracing enabled. Just to say that extremely detailed meshes are not a problem any longer :) We also have some ideas to animate these meshes in real-time.

Anonymous: it's real skinning, we thought about precalculating the frames, but after some tests we decided to calculate the data structures in real-time so we can do procedural ragdoll physics animation. Brigade can animate around 400k random triangles in real-time (30 fps) and render them at the same time. And we can also animate tons of characters at 30 fps. You will see this at the GTC. It's pretty impressive :)

"Actually all of the above, we're also working on an editor now to make it easier for indie game devs."


I'm not a programmer(more of a 3D artist) but I have experience with game editor(hammer,UDK,Cryengine) I hope you plan on having an open beta for the editor in the future, I'd be interested in testing it and providing feedback.

WOOOW.

60 Billion polys and no need for tessellation. How many of them are instanced and how many unique -

Sounds to good to be true.

This blog is really remarkable. Thanks for sharing this great stuff. Keep sharing more useful and conspicuous stuff like this. Thank you so much. Lets have look to my website

http://clippingpathsource.com/Have Fun!!Thanks for the post. I'm also an expert and i have just began writing blogs which i believed was very hard to do until I read your own article. I found your blog handy with fresh thoughts I did not know ahead. In the next few weeks, I'll be busy writing a number of articles for my own new blog. I'm hoping people will find them useful like yours. Please visit http://clippingpathsource.com/ to know more about clipping path.

ha ha liked it so much.

Thanks for the post. I'm also an expert and that i have just started writing blogs which i considered was very hard to perform until I read your own article. I found your blog very helpful with fresh concepts I did not know before. In the next few weeks, I'll be busy writing a number of articles for my own new blog. I really hope people will find them valuable like yours.


Please visit http://clippingpathsource.com/ to know more about clipping path service.

satisfying details, prized and very good conceive, as share good stuff with good notions and notions, allotments of large details and figures and inspiration, both of which I need. Clipping Path Service

lol nice

It was really amazing! I would like to say that it's a fantastic work.

Hey there Sam,






This is very impressive stuff, it makes me hopeful for the games and vfx future.

I saw you typed that the Titan us a great card for path-tracing. I assume it's also great for gpu rendering in general right?

How would you say it compares to the Tesla K40?

Also, do you have any good reference or research sources for GPU rendering cards and renderes when it comes to non-realtime renderers like those made for 3dsmax?

I'm curious about gpu rendering and would maybe want to get into it.

Regards,

I Would like to thank for creating this interesting blog and its great resource to lots of peoples, so you can add mare information in this same blog, because most of them getting good knowledge from here.


Clipping Path Genius (CPG) is one of the best quality clipping path service providers in the world. Clipping | path clipping | clipping paths | clipping service | masking | retouching | retouching photograph | retouching photo| photo retouching | clipping path service provider

Online clipping path service provider we are support 24 hour. Your satisfy our company condition.

unique clipping path (UCP) is the best clipping path service provider in Bangladesh

Clipping Path | Clipping Path Services | Photo Retouching | Clipping Path Service | Photo editing service

Great post. Its very interesting and enjoyable. Its must be helpful for us. Thanks for sharing your nice post.



Clipping Path Service

Good felling after reading the post. The post is very creative and helpful no doubt about it.


clipping path service

Great post thank you for sharing with us.

testosterone

Great post thank you for sharing with us.

testosterone

Great post thank you for sharing with us.

testosterone

Finally very professiona work, I much appreciate on this task.


Clipping Path Service | Clipping Path Service | Clipping Path Service

Post a Comment