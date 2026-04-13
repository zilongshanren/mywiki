---
title: Update 2 on Futuristic Buildings
url: http://raytracey.blogspot.com/2011/07/update-2-on-futuristic-buildings.html
author: Sam Lapere
published: '2011-07-19'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/4993e74ac3e072bf.png)


![](../../assets/4993e74ac3e072bf.png)

There are no 'hitboxes' (aabb acceleration structure) around the car and the buildings yet, which is responsible for the greatly reduced framerate. The path tracing performance should get a nice boost once they are implemented.


Video rendered on the ultra low end 8600M GT (4 spp at 480x360):





Download the new demo at



Next on my todo list:


- implement AABB hitboxes to boost performance

- make the car "drivable" with the keyboard and track the car with the camera

- get Bullet physics in for some real gameplay (this is quite tricky)

- implement oriented bounding boxes (ray-OBB intersection is similar to ray-AABB intersection but there is an additional cost because every ray first needs to be multiplied by the inverse transformation matrix of the OBB). OBBs will be needed for creating physics animations involving collapsing buildings like

Video rendered on the ultra low end 8600M GT (4 spp at 480x360):

Download the new demo at

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)Next on my todo list:

- implement AABB hitboxes to boost performance

- make the car "drivable" with the keyboard and track the car with the camera

- get Bullet physics in for some real gameplay (this is quite tricky)

- implement oriented bounding boxes (ray-OBB intersection is similar to ray-AABB intersection but there is an additional cost because every ray first needs to be multiplied by the inverse transformation matrix of the OBB). OBBs will be needed for creating physics animations involving collapsing buildings like

[this one](http://www.youtube.com/watch?v=yPU6xNNCE68)- (add more sorts of geometric primitives: cylinders, cones, tori, capsules)

- (add more complex materials like coated glossy with roughness and fresnel parameters)

- (add a GUI with sliders using nv widgets)

- (make an OpenCL version)

UPDATE:

The car mechanics are sorta working now. The choppy framerate in the video below is due to the fact that it's still being rendered on a 8600M GT and because there aren't any acceleration structures yet. I bet this will run smooth as butter on a GTX 580 :D. I also temporarily removed the second skyscraper until the AABB acceleration structures are properly implemented:


Download the executable demo "Futuristic Buildings Drivable Car" from

[http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list](http://code.google.com/p/tokap-the-once-known-as-pong/downloads/list)

## 7 comments:

Great progress !

I'm no sure you really need to use OOBB: just adapting an AABB to the enclosed geometry may already help ! (and will definitely be easier on the programming side)

Thanks for the tip!



I haven't done much research on ray-OBB intersections yet, but I will look into it after I've upped the performance again.

I've updated the post with a new video showing the "driving mechanics" ;-)

Note that I don't know Physics Engine, hence the previous post concerns mostly the rendering part.

Your work is awesome. Nice to see that you're having fun with the ray tracer. :)

@SFReader: I've been thinking about this and I'm still going to need OBB's for proper physics simulations, because the OBB's are used as scene geometry, and not only as acceleration structure.




@ Jacco: Thanks a lot!!

Your path tracer and the code is just awesome, in open scenes the convergence of the image is just so damn fast it's not funny any more :)

I'm having heaps of fun and I'm planning to make some great things with it (see my post today on Bullet Physics to get an idea ;)

@Ray Tracey, Do as you need. If you use the OOBB for ray-tracing though, make sure you get the correct distance for the intersection...

I did find an interesting link to a page with ray-object intersections at http://www.realtimerendering.com/intersections.html



But first I will concentrate on the physics aspect more. Expect some cool videos in the next few days :)

Post a Comment