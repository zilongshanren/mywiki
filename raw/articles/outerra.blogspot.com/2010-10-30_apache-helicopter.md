---
title: Apache helicopter
url: https://outerra.blogspot.com/2010/10/apache-helicopter.html
author: Outerra
published: '2010-10-30'
source_blog: Outerra
source_site: https://outerra.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[JSBSim](http://www.jsbsim.org/)library. There still seem to be some bugs and our parameters for the model aren't entirely right either, so the behavior might not be absolutely correct.

Still, flying the helicopter is a great fun. I wasn't able to fly helicopter in a simulator before, probably just because I never tried hard enough. But flying it here - over the forests and through the canyons and close to the rocky walls - that gives it a completely different feeling and experience, so even the types of me can get easily lost in time while wandering over the unknown lands here.

In case you are wondering, the camera comes out from the Hydra rocket launcher at the beginning of the video, made possible thanks to the use of

[logarithmic depth buffer](http://outerra.blogspot.com/2009/08/logarithmic-z-buffer.html).

In order to make this video we added support for "translucent" shadows so that the shadows from rotor blades look more natural, the hard shadows were quite disturbing.

Since the last blog update a number of things has been worked on - an updated atmospheric rendering code resulting in nicer and faster atmosphere rendering, while being also more consistent in various settings. There should be a separate and more technically oriented post about that for people who are fighting with atmospheric scattering which is quite hard to get right. And of course I need to write something about it so I can find how it works later when it drops off of my brain completely again.

As a part of the atmospheric code also the ambient light has been tweaked so the shaded and shadowed terrain is now looking better; this shows best on the features of rocks - previously it didn't have the right amount of contrast and looked quite bland.

Another batch of work done concentrated on GPU memory consumption optimizations; large terrains are quite demanding in this regard so an effective management of it is essential. We managed to save bits of memory here and there by employing various hacks and different formats, which totaled to hundreds of megabytes in the end. But while someone had to effort and tweak the system to save the megabytes, someone else just had to delete that dummy 80MB buffer that was sitting there :-)

Lastly, here are some screenshots with the helicopters:

Forum topic -

[Apache helicopter](http://www.outerra.com/forum/viewtopic.php?id=156).

## 16 comments:

My jaw dropped, I'm waiting for something like this, since 1997.


The rotor looks great, best one I've seen so far, especially the shadows it cast, though, the rotor would need some ... variable "thickness" and visible coning effect.

You could add a Hind to go with the Tatra :). Apache is fine though.


I was amazed when I saw the video, combination of your terrain and JSBSim does wonders. I would not be afraid to use any of the screens you posted as my desktop and tell people it's a photo.

Oh, guys... I envy you.

I want to know if this engine will have destructible enviroment like bf: bad company 2

As Brano mentioned, the JSBSim helicopter capability is very new. We are expecting an update from the model contributor in the near future. So, it will be an ongoin effort. Nevertheless, the video posted here is impressive. I haven't even tried the helicopter model myself, yet.



Nice work.

Jon

--

Development Coordinator,

JSBSim Project

www.jsbsim.org

There will be destructible terrain and trees, destructibility of buildings/objects will depend on the games themselves.

nice vid :D great work w/ scattering & depth buffer! model dimensions are perfect too. hummm everything seems to be in place :)


ps: what fov ru guys using?

I think 37.5 vertical, that should be 66.6 horizontal.

Congratulations guys, this work is awesome.



Is it possible to buy a license of your work ? for an example to develop a software using your technology ?

Bravo !

Not yet, it's still in development, but it will be possible.

This blog provides informative insights on emergency medical transportation. Over the past few years, there has been a tremendous rise in demand for timely and efficient medical transfer, particularly in urban cities. Air Ambulance Services in Kolkata are now an important component of the healthcare system, offering speedy response in cases of dire need where every second counts. With medical staff and sophisticated equipment on board, these services provide patients with necessary treatment during transport. It's heartening to hear such issues being raised more frequently. Increased awareness may assist in enabling citizens to make proper decisions in cases of life-threatening emergencies.


Find stylish ethnic wear with The Kapdakart's new collection. Choose from a range of fabrics, colors, and patterns when you Buy Unstitched Suit Sets Online , ideal for creating your own personal traditional look.



Urgent medical patients can depend on Air Ambulance Services in jamshedpur for quick and secure movement. These operations are equipped with sophisticated life support and trained medical staff to cater to emergencies quickly.


In urgent situations where every second counts, Air Ambulance Services in Siliguri provide quick and safe transport. With experienced medical professionals and state-of-the-art equipment, they ensure that patients get to critical care facilities without any delays, significantly boosting their chances of survival.



Gunship Battle takes mobile war games to another level. The combat is exciting, the upgrades are rewarding, and the missions keep you hooked. It’s perfect for quick battles or longer play sessions. Highly recommended for military action lovers!



A knowledge destination for professionals building relevance in a changing world.

Enrgtech Industrial Electronic Components

Post a Comment