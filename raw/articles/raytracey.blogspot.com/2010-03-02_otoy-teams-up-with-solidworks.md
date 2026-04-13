---
title: OTOY teams up with SolidWorks
url: http://raytracey.blogspot.com/2010/03/otoy-teams-up-with-solidworks.html
author: Sam Lapere
published: '2010-03-02'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[the realtimerendering.com blog](http://www.realtimerendering.com/blog)!

Otoy's cloud technology

Dassault Systems SolidWorks frustrated the media at SolidWorks World 2010 by being vague on the technical details of their cloud-based CAD, despite it apparently being under development for three years. So I was happy to speak with Jules Urbach of OTOY, the ceo of the company behind the curtain.

It was OTOY technology that powered the SolidWorks-in-the-cloud demo. OTOY uses a different approach from than of other technology providers, such as VisualTao (renamed PlanPlatform, renamed Autodesk Israel, recently acquired by Autodesk for its Project Butterfly for online co-editing of AutoCAD files).

The primary problem with running software on the cloud is latency -- the delay between the distant server and your computer. Latency is a function of bandwidth (how fast is the Internet connection?), distance (how far is the server from your computer?), resolution-quality of the screen images (how much data needs to be sent to your computer?), and the processing speed on the server (how quickly the data can be generated?).

Mr Urbach has been working on this problem for a decade, originally developing just such a system for playing video games over the Internet on behalf of entertainment companies like Nickelodeon. For the last couple of years, though, he's been working with AMD to deliver very high resolution images very quickly over even relatively slow connections -- which solves most of the problems associated with latency .

How OTOY Technology Works

The solutions are to (a) greatly compress images and (b) generate images at very high speeds on very low cost "computers." Compression is merely a software problem; the high-speed-but-cheap computing is made possible by AMD's new RV770 GPU with its 800 stream processing units and 2GB of 256-bit RAM boasting a bandwidth of 115GB/sec. "We're talking pennies per vector core doing parallel processing," Mr. Urbach told me.

The software-hardware combination can deliver real-time encoding of up to 3840x2160 resolution. For the more typical 1080p display, OTOY generates a frame every millisecond -- that's 1,000 frames per second. Indeed, he envisions running BluRay video from the cloud on iPhones and other devices, complete with all BluRay menuing systems.

The one problem he cannot completely solve is distance; it is desirable to keep latency under 16msec, for which the maximum distance should be about a thousand miles. But even with a server in San Francisco and the client in New York (3,000 miles), the delay is just 85msec; to Japan, about 100msec. He gets excited about the possibilities of applying his technology to ultrahigh bandwidth countries like Korea. (Companies like Akamai specialize in hosting replicated data in centers distributed around the world to cut latency for clients like CNN.)

more here:

[http://www.upfrontezine.com/2010/upf-635.htm](http://www.upfrontezine.com/2010/upf-635.htm)

## 1 comment:

Open a new assembly in Solid Works then insert your part into the assembly.. . You can then edit the parts in the assembly .. . However if you have a problem making a sketch where you cannot convert entities and get a defined line (Blue instead of Black) ensure the following option is NOT selected in your settings.. . . System Option > External References >Assemblies > Do Not Create References External to the Model. . Was checked, this disables the automatic mating of new parts and is a feature of SW to allow you to create a part without referencing a parts dimension. Unchecking this allowed the convert entities to create a defined object.... . . I had this issue a few weeks ago and it was preventing me from creating defined sketches and performing extrusions.



Solidworks TrainingPost a Comment