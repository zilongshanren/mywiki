---
title: 720p video of Tokap Arcade Madness running on a GTX 580 in 1080p!!!
url: http://raytracey.blogspot.com/2011/02/720p-video-of-tokap-arcade-madness-on.html
author: Sam Lapere
published: '2011-02-15'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is really great, I asked someone with a GTX580 (Radiant from Octane render forum) if he could capture a video of the Tokap game, and he has done a truly fantastic job, running Tokap Arcade Madness

**in 1080p(!)**and fiddling and tinkering with as much parameters as possible. Thank you Radiant!!!More than 6 minutes of pure awesomeness if I may say so myself:

ENJOY! Just twelve months ago, who would have thunk that real-time path tracing at 1080p would have been possible today? :-D

Some screen captures:

Download 'Tokap Arcade Madness' at

Currently working on integrating the open source Bullet 3D physics engine into Tokap, to have some real physics based gameplay. Stay tuned!

## 8 comments:

Wow, thats truly pure awesomeness :D I always thought that our technology was decades away from realtime unbiased rendering 0.o And its "only" plain pathtracing, so MLT and other advanced stuff would even converge faster, right? Is there any theoretical problem that would hinder the engine from running games like crysis with more complex geometry and animations? (apart form format and texture stuff and such insignificant things of course :D )

The code itself is based on 'tokaspt' which can only render spheres (because ray-sphere intersections are computationally cheap).


More advanced renders however (such as MLT etc.) could theoretically deal with any geometry.

As Kerrash (without whom tokap would have been impossible) said, the very fast convergence you see here is mainly due to the fact that only spheres are traced and very few of them (this scene contains 13 spheres).





If you would start raytracing triangles and triangle meshes, the speed would decrease by an order of magnitude and even much more if you don't use acceleration structures like BVH (bounding volume hierarchy). So the speed comes from the simplicity of the scene geometry (perfect spheres). An average level from Crysis contains about 1 million polygons, and it will be some years before those can be ray traced (and path traced) at the same speed as you see here. But I believe that we will definitely get there within five years.

For a taste of the future of game graphics, you should check out the youtube videos from Jacco Bikker, which are using the real-time path tracer Brigade (running on CPU and GPU) that is able to deal with arbitrary geometry and could theoretically handle an entire level of Crysis.

In a scene as simple as this one, MLT will not give you much benefit because the lightsource in this scene is very big and almost all surfaces are directly lit, only the ceiling and some parts of the background wall behind the bouncing spheres are indirectly lit (to see which parts of the scene receive indirect lighting only, just set the max paths slider to 1, which means zero bounces and only direct lighting). MLT is mainly useful in scenes with much indirect lighting e.g. a room where a beam of sunlight pierces through a small window.

Thanks for the kind words btw

It was fun making the video and exploring the program.





It would be good if you can have more control over the camera and have a more flexible/dark ish interface.

I dont really code [made a GUI calculator once >:D] so i dont really know how hard that would be to implement.

All the best,

Radiant

Hello Radiant! Once again, thanks a lot for the video.




I agree that the camera should have better controls, maybe a WASD scheme like in first person shooters would be appropriate, I'll see if that's possible.

The GUI was already in tokaspt, the framework on which tokap was built, and I didn't change anything about that. I'm planning to add some sliders which would let you control the amount of motion blur and the speed of the pong ball.

But first I'm concentrating on getting Bullet 3D physics working in tokap. I have spent a fair amount of time trying to figure out how to get it working, but as I'm not a coder, things are progressing verrry slowly. The scene is already up and running in Bullet (the easy part), but the user interaction doesn't work properly yet. There's some function named getWorldTransform -> setWorldTransform that I have to use to change the position of the paddle, but I'm having a lot of trouble with it.

I could look at adding camera control.



But given the game is pong controlling the camera doesn't seem as worthwhile as improving the AI or physics.

Perhaps a compromise? I could always have the camera pan or track the ball slightly? However this may make the blurring REALLY bad :)

Hello, sorry for the delayed response (I was off hiking in the French Alps during the weekend, which was utterly fantastic).




Kerrash, as you say, improving the AI and physics of the game are more important right now than controlling the camera. As you know, I've been messing around for the past week trying to get Bullet Physics working inside 'Tokap', but sadly to no avail. The web page

http://www.bulletphysics.org/mediawiki-1.5.8/index.php/Getting_Started

explains how to integrate Bullet physics into a project using a 'Hello World'-like example, but I'm not sure how to make this work with tokaspt. I would very much appreciate your help once again. If I knew how to use the xyz coordinates produced by the physics engine to update sphere positions in tokaspt, it would be a great help.

P.S: Once Bullet Physics are working, there are many possibilities beyond just Pong, such as Newton's cradle (youtube.com/watch?v=3CZShNRtT64)


I could also make a marble game with coloured glass spheres. Even a snooker game would be possible.

Post a Comment