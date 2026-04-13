---
title: Real-time ray traced augmented reality for surgeons
url: http://raytracey.blogspot.com/2015/02/real-time-ray-traced-augmented-reality.html
author: Sam Lapere
published: '2015-02-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

With last month's unveiling of Microsoft's augmented reality glasses project dubbed

["HoloLens"](http://www.wired.com/2015/01/microsoft-hands-on/), today's announcement of Sony's plans to release a similar AR device called the["SmartEyeGlass"](http://venturebeat.com/2015/02/17/look-out-hololens-sonys-dorky-augmented-reality-glasses-go-on-sale-in-march-for-840/), and with more details surfacing on[Magic Leap's retina projecting fiber optic AR glasses](http://gizmodo.com/how-magic-leap-is-secretly-creating-a-new-alternate-rea-1660441103)(cleverly reconstructed from publicly available patents by a Gizmodo journalist), the hype around augmented reality seems to be reaching a peak at the moment. Unfortunately, most of the use cases for these technologies that have been demonstrated so far, for example husbands assisting their wives with screwing[a new syphon on a sink](http://futurist.buzz/microsoft-hololens/),[projecting the weather forecast for Maui on the kitchen wall](http://www.vox.com/2015/1/26/7915201/microsoft-hololens-big-deal)or casually[investigating a suspicious rock on the surface of Mars](http://www.theverge.com/2015/1/26/7878735/nasa-mars-exploration-holograms-microsoft-hololens), look either gimmicky, far-fetched or both.
The area where I see a real and immediate use for these high tech AR devices is in the operating room. In my previous life as a medical student, I've spent quite some time in the operating theatre watching surgeons frantically checking if they were cutting the right part of the brain by placing a sharp needle-like pointer (with motion capture dots) on or inside the brain of the patient. The position of the pointer was picked up by 3 infrared cameras and a monitor showed the position of the needle tip in real-time on three 2D views (front, top and side) of the brain reconstructed from CT or MRI scans. This 3D navigation technique is called stereotactic neurosurgery and is an invaluable tool to guide neurosurgical interventions.

While I was amazed at the accuracy and usefulness of this high tech procedure, I was also imagining ways to improve it, because every time the surgeon checks the position of the pointer on the monitor, he or she loses visual contact with the operating field and "blindly" guiding instruments inside the body is not recommended. A real-time three-dimensional augmented reality overlay that can be viewed from any angle, showing the relative position of the organs of interest (which might be partially or fully covered by other organs and tissues like skin, muscle, fat or bone) would be tremendously helpful provided that the AR display device minimally interferes with the surgical intervention and the augmented 3D images are of such a quality that they seamlessly blend with the real world. The recently announced wearable AR glasses by MS, Sony and Magic Leap seem to take care of the former, but for the latter there is no readily available solution yet. This is where I think real-time ray tracing will play a major role: ray tracing is the highest quality method to visualise medical volumetric data reconstructed from CT and MRI scans. It's actually possible to extend a volume ray caster with physically accurate lighting (soft shadows, ambient occlusion and indirect lighting) to add visual depth cues and have it running in real-time on a machine with multiple high end GPUs. The results are frighteningly realistic. I for one can't wait to test it with one of these magical glasses.

As an update to my previous post, the people behind

[Scratch-a-Pixel](http://www.scratchapixel.com/)have launched a v2.0 website, featuring improved and better organised content (still work in progress, but the old website can still be accessed). It's by far the best resource to learn ray tracing programming for both novices (non engineers) and experts. Once you've conquered all the content on Scratch-a-Pixel, I recommend taking a look at the following ray tracing tutorials that come with source code:
-

[smallpt](http://www.kevinbeason.com/smallpt/)from Kevin Beason: an impressively tiny path tracer in 100 lines of C++ code. Make sure to read David Cline's[slides](https://docs.google.com/open?id=0B8g97JkuSSBwUENiWTJXeGtTOHFmSm51UC01YWtCZw)which explain the background details of this marvel.
-

[Rayito](https://github.com/Tecla/Rayito), by Mike Farnsworth from[Renderspud](http://renderspud.blogspot.co.nz/)(currently at Solid Angle working on Arnold Render): a very neatly coded ray/path tracer in C++, featuring path tracing, stratified sampling, lens aperture (depth of field), a simple BVH (with median split), Qt GUI, triangle meshes with obj parser, diffuse/glossy materials, motion blur and a transformation system. Not superfast because of code clarity, but a great way to get familiar with the architecture of a ray tracer
-


-

[Renderer 2.x:](https://github.com/Tecla/Rayito)a CUDA and C++ ray tracer, featuring a SAH BVH (built with the surface area heuristic for better performance), triangle meshes, a simple GUI and ambient occlusion-

[Peter and Karl's GPU path tracer](http://gpupathtracer.blogspot.co.nz/): a simple, but very fast open source GPU path tracer which supports sphere primitives, raytraced depth of field and subsurface scattering (SSS)
If you're still not satisfied after that and want a deeper understanding, consider the following books:

- "Realistic ray tracing" by Peter Shirley,

- "Ray tracing from the ground up" by Kevin Suffern,

- "Principles of Digital Image Synthesis" by Andrew Glassner, a fantastic and huge resource, freely available

[here](https://www.google.co.nz/url?sa=t&rct=j&q=&esrc=s&source=web&cd=13&cad=rja&uact=8&ved=0CDsQFjAM&url=http%3A%2F%2Fwww.realtimerendering.com%2FPrinciples_of_Digital_Image_Synthesis_v1.0.1.pdf&ei=ODPlVLe7Foek8AWmh4HoDA&usg=AFQjCNFgNfsmRaWJuyjzd-ffEWbIoUKUxA&sig2=0BVqxxTrnH8oh5sHQ0uXEw&bvm=bv.85970519,d.dGc), which also covers signal processing techniques like Fourier transforms and wavelets (if your calculus is a bit rusty, check out[Khan academy](https://www.khanacademy.org/), a great open online platform for engineering level mathematics)
- "Advanced global illumination" by Philip Dutré, Kavita Bala and Philippe Bekaert, another superb resource, covering finite element radiosity and Monte Carlo rendering techniques (path tracing, bidirectional path tracing, Metropolis light transport, importance sampling, ...)

## 24 comments:

wow, cool. thanks for all the sources and info.

AR will be quiet powerful in medicine,

i could imagine.

Since i heard what Magic Leap is trying to do, imagination started to run wild in my brain.

Yes it would be great to have a hologram

right in front of you that would display a nervous system layer, muscle tissue, bone structure and organs all separately just for learning purpose. Could be quiet interesting and also at some day very useful if there isn't right away a doctor in case of an accident.

We learn only by imagination , ar and vr can reinforce our learning quiet significantly IMO.

In principle we learn very ineffective. First our brain encodes text symbols, then puts it into meaningful context. Then tries to connect the meaning of the text into animated images.

Why not learn just right away with

animated holograms displayed into the real world. :)

Exactly! Medical education through visual learning is one of the things I'm focusing on right now, from molecules to proteins, cells, tissues, organ systems and the entire body. The potential of real-time ray tracing is huge there (and not only for visualisation, but also simulation, check for example the Virtual Physiological Human).

that is cool.


i have read a book about molecular biology and i have to say it is quiet staggering what is happening inside

of each cell within our body.

I watched also a fancy documentary

about virus entering human cells with animations right down to the molecular level, wobbly cell membrane,microtubuli, nuclues.

That was so awesome.

I would love to be in the school of future, where students sit around in circles and watch in the center

happening molecular biology in midair.

Don't miss Mr. Abovitz speaking at TED. :)

http://blog.ted.com/2015/02/17/meet-6-new-speakers-just-added-to-the-ted2015-speaker-lineup/

May it be a bit more informative than his last talk in 2012. hehe

Agreed, I really loved learning about molecular biology as well, the inner workings of the cell are fascinating. Simulating how all those molecules interact with each other is an emerging and quickly growing field. The next big step will be physics based cell animations, where Monte Carlo ray tracing is used to both render molecules and efficiently compute their random intermolecular forces on massively parallel hardware (using the same efficiency optimisations developed for rendering like acceleration structures, importance sampling, bidirectional path tracing, etc), allowing researchers to visualise and simulate cell processes on the molecular level. Ultimately, one could switch virtual genes on and off and study their effect on disease.

Anywho, thanks for the link to the TED talks, will definitely be an interesting watch.

I am following many virtual reality projects and almost none of them is focusing on modeling, construction or engineering.




What about modeling 3d objects with hands? or constructing buildings on from bigger perspective to modifying tiny details. i.e. electronics or performing experiments in a virtual environment.

What about navigation like this www.youtube.com/watch?v=itAGfMzfiOw it is the first thing that comes to mind.

What do you think Sam.



Maybe Nvidia will present ray tracing hardware on 3.3.?

5 years of work to redefine gaming?

LIFEH2O: I don't think 3d modeling with your hands is very accurate, you can't beat the precision of a mouse, keyboard and graphics tablet. I'm also not sure if a VR headset would make the modeling process more efficient.


@Retina: Nvidia is cooking something up with a central role for ray tracing for sure. Dedicated ray tracing hardware might be an option.

“Maybe Nvidia will present ray tracing hardware on 3.3.?”




I don’t know if NVidia will but PowerVR could do on that date. The Dedicated ray tracing hardware for devs is due to ship this year. That would be the perfect show to demonstrate the hardware. Last year’s talks where very interesting, cannot wait to see how far ray tracing has moved on in 1 year.

http://www.gdcvault.com/play/1020741/New-Techniques-Made-Possible-http://www.gdcvault.com/play/1020688/Practical-Techniques-for-Ray-Tracing

would be great.



Computer Graphics is converging towards

CGI.

Nvidia knows that very well.

Nothing more in their DNA as to make realtime raytracing a virtual reality.

could be great times. PLayed recently

'the vanishing of eth carter'. Holy Cow. Almost everything was scanned in.

Apart from dynamic lighting which was done in uE3, it looked so astonishingly photoreal.

Most of the time, i thought iwas in a forest. haha

Combine that realism with ray tracing.

Nothing better than scanning.

Waste of effort to let an artist design a photoreal stone or tree.

He can't reach it anyway.

Retina, that's another cool benefit of ray tracing, it handles massive datasets such as scanned geometry much better than rasterization and there's less geometry clean-up and preparation needed.

I have read about OTOys ORBX tech.

How would lightfields behave for real time ray tracing?

Would it increase the amount of rays you need. Or is it just that now rays

cross over in the pixel plane?

Can#t get my head around it.

Retina, I don't know anything about that technology.

actually i got a bit confused with

the terms.

was just wondering about how lightfields work with raytracing

and if there would be a performance increase connected with it.

By the way, there is this eye-tracking VR headset called FOVE. They are rolling out devkits in summer.

They say there is a 6x performance increase with foveated rendering.

Couldn't this mean noiseless 60fps

ray tracing? :)

https://www.youtube.com/watch?v=3eh1aOIR18E

Yep, foveated rendering sure is interesting. There's a paper about OpenCL ray tracing for VR using foveated rendering claiming a 20x reduction in pixels to shade: "Our technique

effectively reduces the number of pixels to shade by 1/20,

achieving more than 75 fps while preserving the same visual quality" http://research.lighttransport.com/foveated-real-time-ray-tracing-for-virtual-reality-headset/index.html

this is going to be a pretty exciting GDC. Brad Wardell from Star Dock recently gave an interview about DX12.

Quiet shocking what he told about what games are going to look like.

And that AMD is going to show off something - pause- Crazzy.

hmmm......

Thank you so much from Spain!! Such an amazing idea to make our class more enjoyable! I love it!

Augmented Reality

This is how to create the highest-performance processor :










Emitter-coupled logic

Explicit Data Graph Execution

SRAM

Ultraconductor™

Tridimensional integrated circuit

Dynamic combinational logic

SPIN OS

Mercury programming language

Real-time 3D-graphics might consist of ...




Voxels

Rendering each separate ray of light ‘manually’

Image Metrics

Performance level of a computer is solely dependant on logic 's propagation delay, and increase in amount of transistors will not help anyways !




NO graphics API / NO video driver {implying NO video card} = performance gain

Moreover, there still is wait state that cannot be resolved through using caches/standard ILP methods.

Finally, Windows takes 1GB of operating memory up, which is highly unacceptable.

Path tracing as being a principally inferior rendering technique could already be in use had they in time implemented the 2006' 3-nm 3D-FinFET.

experimental Full Dive VR in 2025.

Possible because of real-time encoding of brain activity done in the BRAIN Initiative.

Just to let people know.....where we are heading....

thanks for all the links to ray tracing basics..... :)



i was looking for a good book on raytracing.

i think realistic ray tracing from Peter Shirley might be a good book, or not?

time to write my own path tracer....

afterwards i will have a look into opencl.... ouuuuch.... XD

Retina: Peter Shirley's book is ok, but I wouldn't recommend it to beginners in ray tracing as it's not very detailed. The Scratch-a-pixel website has a lot more background info, but the C++ code is quite advanced at some points. If you really need a book, go for "Ray tracing from the ground up" from Kevin Suffern. Let me know if you need some tips when you start writing your own path tracer.

thanks for the recommendation. I'll let you know when i need some advice.

Post a Comment