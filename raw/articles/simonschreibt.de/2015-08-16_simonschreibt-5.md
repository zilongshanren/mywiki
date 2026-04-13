---
title: Simonschreibt.
url: https://simonschreibt.de/gat/renderhell/
author: Simon
published: '2015-08-16'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/29dc2625ba927234.png)


![](../../assets/29dc2625ba927234.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

- Added
[a whole new book](http://simonschreibt.de/gat/renderhell-book2)covering the pipeline in detail - Added
[2 new videos](https://simonschreibt.de#update2-newvideos)and[32 new links](https://simonschreibt.de#update2-newlinks)to great articles, whitepapers, … - Extended the section
[copying data from HDD to graphic card](http://simonschreibt.de/gat/renderhell-book1#update2-copydata). - Updated some terms in the
[pipeline animation](http://simonschreibt.de/gat/renderhell-book1#update2-logicalpipelinewarning)and made clear that this is only the**logical pipeline**. - Updated
[some smaller text passages](http://simonschreibt.de/gat/renderhell-book3#update2-manydrawcalls1)in the book about the**problems**. - Added
[some new problems](http://simonschreibt.de/gat/renderhell-book3#update2-newproblems). - Added
[a new solutions](http://simonschreibt.de/gat/renderhell-book4#update2-newsolutions)and some general words.

See Render Hell 1.1 Change Log

![](../../assets/57864f9016e56102.jpg)


[here](http://simonschreibt.de/gat/renderhell#update11-5).[here](http://simonschreibt.de/gat/renderhell#update11-4). Madsy9 pointed it out [here](http://www.reddit.com/r/programming/comments/2dm0xe/render_hell_10/cjqxl59).[Here](http://www.reddit.com/r/programming/comments/2dm0xe/render_hell_10/) and [here](http://www.reddit.com/r/gamedev/comments/2djgnx/what_are_draw_calls_why_do_you_care_what_makes/).[here](http://simonschreibt.de/gat/renderhell/#update11-2). Thx [sccrstud92](http://www.reddit.com/user/sccrstud92), [tmachineorg](http://www.reddit.com/user/tmachineorg) and [koyima](http://www.reddit.com/user/koyima)[Cort](https://twitter.com/postgoodism) mentioned this [these](http://s09.idav.ucdavis.edu/talks/02_kayvonf_gpuArchTalk09.pdf) slides about “How Shader Cores Work”.[NVidia specifications](http://simonschreibt.de/gat/renderhell#update11-1) with actual core counts. Thx [Jan](http://twitter.com/JKashaar), Volkan and Hakan Candemir[in his comment](http://simonschreibt.de/gat/renderhell/#comment-502).[OddEyesCG](https://twitter.com/OddEyesCG) for mentioning![Thx Flannon and RXMESH](../../assets/5ee120058866c68a.img) for the code.And [garblefart](https://twitter.com/garblefart) for all the feedback.

A lack of knowledge sometimes can be a strength, because you naively say to yourself “Pfff..how complicated can it be?” and just dive in. I started this article by thinking “Hm…what exactly is a draw call?”. During my 5-Minute-Research I didn’t find a satisfying explanation. I checked the clock and since i still had 30 minutes before bedtime i said …

![](../../assets/ebe450f92e093152.png)

… and just started. This was two months ago and since that i was continuously reading, writing and asking a lot questions.

It was the hardest and low levelest research i ever did and for me as a non-programmer it was a nightmare of “yes, but in this special case…” and “depends on the api…”. It was my personal render hell – but i went through it and brought something with me: five books, each representing an attempt to explain one part of rendering from an artist perspective. I hope you’ll like it.

[Open this Book
](http://simonschreibt.de/gat/renderhell-book1)

![](../../assets/10c681ccc40de8ae.jpg)

[Open this Book](http://simonschreibt.de/gat/renderhell-book2)

![](../../assets/a180b128333b9a31.jpg)


![](../../assets/a180b128333b9a31.jpg)

[Open this Book](http://simonschreibt.de/gat/renderhell-book3)

![](../../assets/ff40e6bdc328a626.jpg)


![](../../assets/ff40e6bdc328a626.jpg)

[Open this Book](http://simonschreibt.de/gat/renderhell-book4)

![](../../assets/08f708b57e07f418.jpg)


![](../../assets/08f708b57e07f418.jpg)

[Open this Book](http://simonschreibt.de/gat/renderhell-book5)

![](../../assets/d4520fa96ae94110.jpg)


![](../../assets/d4520fa96ae94110.jpg)

Thank you!

Thanks goes out to all readers but especially to the people listed below. This article wouldn’t be there without you guys! Thank you for answering all my questions, reading over all my text iterations and supporting me.

[Christoph Kubisch](https://twitter.com/pixeljetstream)

[Timon](http://about.me/timon37)

[Matthias Wloka](https://www.linkedin.com/in/matthiaswloka)

[Cort Stratton](https://twitter.com/postgoodism)

[Markus Pohl](http://www.mobygames.com/developer/sheet/view/by_year/developerId,165720/)

[Nigel Brooke](https://twitter.com/nigelbrooke)

[Chance Millar](https://twitter.com/ValeourM)

[Michael Silverman](https://twitter.com/m_silverman)

[Merlijn Van Holder](https://twitter.com/MerlijnVH)

[Mathias Wahlin](https://twitter.com/fohx)

[Fabrice Piquet](https://twitter.com/Froyok)

[Adam Martin](https://twitter.com/t_machine_org)


[Warby](http://www.warby.de/)

[Janina Gerards](http://xeocon.de/janina)

Links & Resources

Videos

[v01] [CPU vs GPU Demonstration with Paint-Gun-Robots](https://www.youtube.com/watch?v=-P28LKWTzrI)

[v02] [Multiple Materials in one Draw Call](http://cgcookie.com/unity/2013/03/21/quick-tips-combining-multiple-materials-into-a-single-draw-call/)

Podcast

[p01] [Overview about Rendering, APIs and all that stuff](http://www.upup.fm/show/complete-tub-of-crap/)

Book

[b01] [Real-Time Rendering](http://www.realtimerendering.com/book.html): Page 711

Articles

[a01] [MSDN: Accurately Profiling Direct3D API Calls (Direct3D 9)](http://msdn.microsoft.com/en-us/library/windows/desktop/bb172234(v=vs.85).aspx)

[a02] [GPU Programming Guide GeForce 8 and 9 Series](http://developer.download.nvidia.com/GPU_Programming_Guide/GPU_Programming_Guide_G80.pdf)

[a03] [MSDN: States (Direct3D 9)](http://msdn.microsoft.com/en-us/library/windows/desktop/bb206120(v=vs.85).aspx)

[a04] [MSDN: Efficiently Drawing Multiple Instances of Geometry (Direct3D 9)](http://msdn.microsoft.com/en-us/library/windows/desktop/bb173349(v=vs.85).aspx)

[a05] [Understanding Modern GPUs](http://traxnet.wordpress.com/2011/07/22/understanding-modern-gpus-3/)

[a06] [A trip through the Graphics Pipeline](http://fgiesen.wordpress.com/2011/07/09/a-trip-through-the-graphics-pipeline-2011-index/)

[a07] [Understanding GPUs from the ground up](http://www.botchco.com/agd5f/?p=50)

[a08] [Flushing the pipeline](http://infocenter.arm.com/help/topic/com.arm.doc.dui0380d/CACEBFGC.html)

[a09] [Sides: Avoiding Catastrophic Performance Loss](http://www.slideshare.net/basisspace/avoiding-catastrophic-performance-loss#btnNext)

[a10] [Radeon R5xx Acceleration](http://www.x.org/docs/AMD/old/R5xx_Acceleration_v1.5.pdf)

[a11] [SIGGRAPH 2006: GPU Shading and Rendering](http://www.csee.umbc.edu/~olano/s2006c03/)

[a12] [Tool: GPUView for performance measurement](http://graphics.stanford.edu/~mdfisher/GPUView.html)

[a13] [Real-Time Graphics Architecture](http://www.graphics.stanford.edu/courses/cs448a-01-fall/lectures/lecture14/system.2up.pdf)

[a14] [How GPUs Work ](http://www.cs.virginia.edu/~gfx/papers/pdfs/59_HowThingsWork.pdf)

[a15] [NVidia GPU Gems Book](http://http.developer.nvidia.com/GPUGems/gpugems_part01.html)

[a16] [Wikipedia: Shader](http://en.wikipedia.org/wiki/Shader)

[a17] [Wikipedia: Graphics Pipeline](http://en.wikipedia.org/wiki/Graphics_pipeline#3D_geometric_primitives)

[a18] [ExtremeTech 3D Pipeline Tutorial](http://www.extremetech.com/computing/49076-extremetech-3d-pipeline-tutorial/5)

[a19] [Linux Programmer’s Reference Manuals](https://01.org/linuxgraphics/documentation/driver-documentation-prms)

[a20] [More AMD References (like [a10])](http://www.x.org/docs/AMD/old/)

[a21] [OpenGL Lecture](http://www.elmindreda.org/lectures/opengl-lecture1.pdf)

[a22] [Learning Modern 3D Graphics Programming](http://www.arcsynthesis.org/gltut/index.html)

[a23] [OpenGL Programming Guide](http://www.ics.uci.edu/~gopi/CS211B/opengl_programming_guide_8th_edition.pdf)

[a24] [Draw Call Batching](http://docs.unity3d.com/Manual/DrawCallBatching.html)

[a25] [OpenGL Step by Step](http://ogldev.atspace.co.uk/index.html)

[a26] [OpenGL 3 & DirectX 11: The War Is Over](http://www.tomshardware.com/reviews/opengl-directx,2019-8.html)

[a27] [Rendering Pipeline Overview](http://www.opengl.org/wiki/Rendering_Pipeline_Overview)

[a28] [GPU Parallelizable Methods](http://www.oxford-man.ox.ac.uk/gpuss/simd.html)

[a29] [Parallelism in NVIDIA GPUs](http://yosefk.com/blog/simd-simt-smt-parallelism-in-nvidia-gpus.html)

[a30] [Many SIMDs Make One Compute Unit](http://www.anandtech.com/show/4455/amds-graphics-core-next-preview-amd-architects-for-compute/4)

[a31] [PowerPoint: Modern GPU Architecture](https://www.google.de/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&ved=0CD4QFjAD&url=http%3A%2F%2Fweb.cse.ohio-state.edu%2F~crawfis%2Fcse786%2FReferenceMaterial%2FCourseNotes%2FModern%2520GPU%2520Architecture.ppt&ei=VpfWU9fMA-nZ4QTg_YGIBQ&usg=AFQjCNGxCKDQOgJOgltlrXD6dr9Amn4NCw&cad=rja)

[a32] [Unreal: Layered Material](https://docs.unrealengine.com/latest/INT/Engine/Rendering/Materials/LayeredMaterials/index.html)

[a33] [Unity: One draw call for each shader](http://forum.unity3d.com/threads/one-draw-call-for-each-shader-with-dynamic-meshes-the-bob-script.88604/)

[a34] [Reducing GPU Offload Latency via Fine-Grained CPU-GPU Synchronization](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=JgyxYiUAAAAJ&citation_for_view=JgyxYiUAAAAJ:u-x6o8ySG0sC)

[a35] [Accurately Profiling Direct3D API Calls](http://msdn.microsoft.com/en-us/library/windows/desktop/bb172234(v=vs.85).aspx)

[a36] [Technical Breakdown – Assassins Creed II](http://www.mapcore.org/page/features/_/articles/technical-breakdown-assassins-creed-ii-r24)

[a37] [NVidia GPU Gems 2](http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter03.html)

[From Shader Code to a Teraflop: How Shader Cores Work by Kayvon Fatahalian](http://s09.idav.ucdavis.edu/talks/02_kayvonf_gpuArchTalk09.pdf)

[a44]

[The minimum number of triangles per draw call](http://www.g-truc.net/post-0666.html)

[a45]

[How GPU Shader Cores Work](http://bps10.idav.ucdavis.edu/talks/03-fatahalian_gpuArchTeraflop_BPS_SIGGRAPH2010.pdf)

[a46]

[Interpolant Shader Processes](https://www.terathon.com/wiki/index.php/Interpolant_Shader_Processes)

[a47]

[Latency numbers every programmer should know](https://gist.github.com/hellerbarde/2843375)

[a48]

[Structure of the GTX680 GPU](http://images.bit-tech.net/content_images/2012/03/nvidia-geforce-gtx-680-2gb-review/gtx680-21b.jpg)

[a49]

[Structure of the Tegra K1](http://images.anandtech.com/doci/7622/Screen%20Shot%202014-01-06%20at%206.18.42%20AM.png)

[a50]

[Comparision: Structure of Kepler vs Maxwell GPUs](http://www.xander.com.tw/pic/2(2).jpg)

[a51]

[Structure of the GTX680 Kepler GPU](http://images.ht4u.net/reviews/2012/nvidia_geforce_gtx_680_kepler_sli_evga_zotac_test//geforce_gtx_680_block_diagram_final.png)

[a51]

[NVidia GF100 Whitepaper](http://www.hardwarebg.com/b4k/files/nvidia_gf100_whitepaper.pdf)

[a53]

[Wikipedia: Processor Registers](http://en.wikipedia.org/wiki/Processor_register)

[a54]

[Life of a triangle – NVIDIA’s logical pipeline](http://pixeljetstream.blogspot.de/2015/02/life-of-triangle-nvidias-logical.html)

[a55]

[Fast Tesselated Rendering on Fermi GF100](http://www.highperformancegraphics.org/previous/www_2010/media/Hot3D/HPG2010_Hot3D_NVIDIA.pdf)

[a56]

[TechRadar: Nvidia’s Fermi graphics architecture explained](http://www.techradar.com/news/computing-components/graphics-cards/nvidia-s-fermi-graphics-architecture-explained-657489)

[a57]

[GLSL Core Tutorials – Primitive Assembly](http://www.lighthouse3d.com/tutorials/glsl-core-tutorial/primitive-assembly/)

[a58]

[Image Processing and Computer Graphics – Rendering Pipeline](http://cg.informatik.uni-freiburg.de/course_notes/graphics_01_pipeline.pdf)

[a59]

[Geometry Shader Programming in OpenGL](https://open.gl/geometry)

[a60]

[Rasterization](https://www.cse.msu.edu/~cse872/rasterization.pdf)

[a61]

[OpenGL NVIDIA Command-List: Approaching Zero Driver Overhead](http://www.slideshare.net/tlorach/opengl-nvidia-commandlistapproaching-zerodriveroverhead)

[a62]

[A SIMD-efficient 14 Instruction Shader Program for High-Throughput Microtriangle Rasterization](http://attila.ac.upc.edu/wiki/images/9/95/CGI10_microtriangles_presentation.pdf)

[a63]

[Article based on the GF100 Whitepaper](http://www.legitreviews.com/nvidia-gf100-fermi-architecture-and-performance-preview_1193/2)

[a64]

[GLSL Core Tutorial – Rasterization and Interpolation](http://www.lighthouse3d.com/tutorials/glsl-tutorial/rasterization-and-interpolation/)

[a65]

[Wikipedia: Kepler Architecture](https://en.wikipedia.org/wiki/Kepler_(microarchitecture))

[a66]

[Guard Band Clipping by NVidia](http://developer.download.nvidia.com/assets/gamedev/docs/Guard_Band_Clipping.pdf)

[a67]

[CryEngine Documentation about Overdraw](http://docs.cryengine.com/display/SDKDOC2/Getting+Started+Modeling#GettingStartedModeling-TexturingandUVWs)

[a68]

[NVIDIA OpenGL extension showcasing perf benefits of new concepts in APIs](http://on-demand.gputechconf.com/gtc/2015/presentation/S5135-Christoph-Kubisch-Pierre-Boudier.pdf)

[a69]

[OpenGL From Zero To Hero](http://in2gpu.com/)

[a70]

[Nvidia Guard Band Clipping Power Point Presentation](http://www.byteboss.com/288180.ppt)

[a71]

[Cuda Core Programming Guide: Compute Capabilities](http://docs.nvidia.com/cuda/cuda-c-programming-guide/#compute-capabilities)

[a72]

[Interactive Indirect Illumination Using Voxel Cone Tracing](https://research.nvidia.com/publication/interactive-indirect-illumination-using-voxel-cone-tracing)

[a73]

[Triangle Tesselation](http://prideout.net/blog/?p=48)

[a74]

[Quad Tesselation](http://prideout.net/blog/?p=49)

[a78]

[Humus: Triangulation](http://www.humus.name/index.php?page=Comments&ID=228&start=0)

[a78]

[Humus: Particle Trimming Tool](http://www.humus.name/index.php?ID=266)

[a79]

[Fermi GF100 Graphics Processing Unit (GPU)](http://www.hotchips.org/wp-content/uploads/hc_archives/hc22/HC22.23.110-1-Wittenbrink-Fermi-GF100.pdf)

Forum Discussions

[f01] [2 Materials on one mesh](http://answers.unity3d.com/questions/397466/2-materials-on-one-mesh-2-draw-calls.html)

[f02] [Which is faster](http://superuser.com/questions/252959/which-is-faster-copying-everything-at-once-or-one-thing-at-a-time)

[f03] [Multiple Materials with one glDrawElements()](https://www.opengl.org/discussion_boards/showthread.php/176149-Multiple-materials-with-one-glDrawElements())

[f04] [What Is A Draw Call? How Does It Effect My Product?](http://nuveraonline.com/kb/article.php?id=21)

[f05] [Why are draw calls expensive](http://stackoverflow.com/questions/4853856/why-are-draw-calls-expensive)

[f06] [A great reddit discussion about the content of this article](http://www.reddit.com/r/programming/comments/2dm0xe/render_hell_10/)

[f07] [Another great reddit discussion about the content of this article](http://www.reddit.com/r/gamedev/comments/2djgnx/what_are_draw_calls_why_do_you_care_what_makes/)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/abfec339fb02502a.gif)

This is pretty cool! Thanks for the guide, I’d been wondering about all of this for a while now. Good stuff :)

As for current-gen GPU core amounts, I usually look at AnandTech’s GPU comparisons, e.g.:

http://www.anandtech.com/show/8069/nvidia-releases-geforce-gtx-titan-z (scroll down a bit for a table.)

Nvidia (didn’t check ATI) have the number of cores listed in the tech specs for their GPUs, and in the feature lists on their website.

I vaguely remember reading that there are seperate, specialized cores for handling textures, but I don’t know anything certain about that.

Oh really nice! Thanks for the link! That’s the first time i see some numbers. Might not explain anything but now i’ve a vague idea about what count we’re talking about :)

For GPU core counts, looking up any GPU’s specification page would do. Take the best GPU so far, GeForce GTX 780 Ti for example: http://www.geforce.com/hardware/desktop-gpus/geforce-gtx-780-ti/specifications

The webpage reads 2880 CUDA cores.

That’s a great work you’ve done there. I enjoyed reading it all along. Keep it up:)

Uhw, nice! Thanks for the link. I’ll add it to the link list later. Awesome :,) Oh and thank you for the big compliment :) Glad you enjoy reading it!

Fastest NVIDIA card: GTX TITAN Z (5760 cores)

Fastest AMD card: Radeon R9 295X2 (5632 cores)

Both cards have two GPUs, so it’s 2880 (NVIDIA) or 2816 (AMD) cores per GPU.

Wow, cool! Thank you for those numbers! :)

Cool article, very good explanation, maybe in the next chapter you could go more in depth regarding vertex & index buffers. Keep up the good work im sure your site will get lots of traffic.

GLad you like the article! Hm i’m not sure if i shall do another article in that technical level :D It almost crushed me and i’m always not sure how thrustworthy i’m as an artist are, when i try to explain programmerstuff. But thanks for the compliment. Regarding the buffers: As far as i know those buffers are justs lists…and the index buffer refers to a part of the vertex list. Are there special questions which are bothering you?

I have a suggestion for another tip right after “ask the coder”:

Embrace the coder

First do this literally, he or she won’t bite. Done? Good. Now think about your relationship: Normally the artist starts with an asset solely based on artistic premises. In the next step the coder(s) will try to optimize the things you want to display as much as possible, hopefully with your help.

Why not reverse this process and start with an interesting technique? After all this is how many great games were made, a good example being Minecraft. Yes, it does not have fancy high-end graphics, but that’s because the foremost goal was to create a world that is completely editable.

Yes of course, good communication is key and i think from the start all the different artisans have to work together and don’t sit in a separated room, thinking about something for 2 years and then confront the team with there special idea which just isn’t possible to execute. But minecraft has its issues too – all those cubes need to be handled and i just saw an article recently where they solved some sorting issue because they weren’t able to cull the dungeons below the surfaces (which weren’t visible BUT which were in your viewcone). So even this simple style has its problems. :D

Hopefully this article gives you, and other artists, a better appreciation of the programmers :) It seems like we are becoming less and less relevant as the game engines slowly try to replace us with artist friendly tools.

Hehe sometimes i think the other way around. While art is often outsource-able, you always need a lot coders in the core team. Sure, you can “easily” create a standard shooter with an engine which gives you the tools to do that, but mostly you need a unique selling point (e.g. portals) and if the engine doesn’t support such a game mechanic, you always need programmers. But when i see that this Limit Theory guy does (all procedural generated graphics) and how stunning it looks, i feel fear about my future :D

But in general i think every department deserves appreciation. I really don’t like these “fights” about designer vs coders etc – I really like to work together with programmers, designers, testers, … :)

very nice writeup, complete with very fun and nice animations…and you used html5/webm! thanks for that. not doing that wouldve brought any high end system to it’s knees in any browser (e.g. using gif, flash, etc). now if only more people could follow your example :)

Thanks for the compliment :) I can understand thath people use GIF because it’s just simple. I had to to several tests and only because of very nice twitter followers i was able to manage that those videos run on every browser and operating system. But of course, it saves a lot of space! On the other side: i received a message that those videos make use of a core to 100% in firefox….so maybe gif is less CPU-dependent? Anyway, i’ll use webm/mp4 in the future and i’m really happy with it. And i’m glad that you like it too :)

Very nice article, i would had loved to find as good explanation three months ago :P I and our lead programmer have been going through the exactly same research this summer for our upcoming game . Couldn’t highlight more how important it is to have good communication between artist and programmer.

Keep up good work, been loving your game art tricks series :D

sorry, failed with the tags, how do i edit?

Thanks man. Sorry for coming too late :D I’ve wished to finish this beast faster but it took me two month :D Your game looks nice! Just faved it :)

Hi. I just want to say BIG THANK YOU for this article. I remember days long ago when I started to learn 3d graphics and I really missed articles like this – basic things from the very beginning. Thought I’m a programmer and absolutely not an artist I’m reading your blog with a great pleasure and I hope that you won’t stop and continue share you knowledge. Simon if you have any questions about programming/graphics you can freely contact me, maybe I can be useful (or you’ll teach me something new, hehe :) ).

Hi Nikita! Thanks a lot for this offer! But beware, i can have a lot questions. In fact, most of my articles only exist because i had the luck to have people to ask. I annoyed Timon (first place in the thanks-list) almost every day and wrote long mails to other programmers and stole their time :D

Oh and…pssst…this isn’t my knowledge. To be honest, most of the stuff was surprising to me and i had to do research to find out how that stuff works :) So it’s actually my not-knowledge, which makes me have questions and write the answers into articles :D

Great article! I really liked the animations, it strengthened your explanation. Keep up the good work :) For GPU cores you can check these links :

For Nvidia:

http://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units

For AMD:

http://en.wikipedia.org/wiki/List_of_AMD_graphics_processing_units

For Intel:

http://en.wikipedia.org/wiki/List_of_Intel_graphics_processing_units

Wow cool, thanks! This will all go into 1.1 of the article :) I need a bit time for the preparation but then it will be included. Thanks a lot!

WebMs dont work!! I wish I could see these awesome animations that reddit is talking about :(

Should be fixed now. The server was overloaded so i moved all videos to vimeo and embedded them. I hope there are no problems anymore?

Hello, I can host you something if you need, I have a server in France. Contact me if you need!

Thanks man! As far as i see, it wasn’t the traffic, but the processor power needed to decompress hte mp4/webm videos. I moved them to vimeo, now it should work :)

Been enjoying going through this writeup over the past few days :) Wish I’d found a nice overview like this when I was learning these things originally.

As for video hosting, maybe try services like Gfycat, or maybe even Coub or Vine? What did you make them in—is there any chance it can export to SVG Animation or an HTML5 script? (I’m honestly not sure if that would perform better or worse than GIF, but it would sure be smaller at least!)

Thanks for the compliment :) Regarding the html5: i have no idee :D but i moved that stuff to vimeo and it should work. i already used standard html5 video tags but it seems that server cpus don’t like that :,( OR the server CPU was jealous because he wasn’t in the article :D

Hi Simon! Maybe you can host your WebM files here:

http://webmup.com/

I’ve used it before, but it seems to work…

And thank you for the awesome write-up. This is super helpful!

Thanks for the suggestion :) I use vimeo for now….does it work for you? Oh man, i’m so glad that some people find that helpful. I was often very near to give up because i thought “nobody needs that stuff” :D

Vimeo is great. The article is great. You are great.

Thank you!

Stop making me blush :D Thanks! But actually YOU are great, you take the time and read my stuff and even give me feedback. That’s so cool :)

Great article! This is the most understandable sum-up of CPU-GPU interplay I’ve seen, with hilarious animations to boot.

One relevant technique that bears mentioning, though outside of the scope of the article, is billboards. It’s one of the oldest tricks in the book, long predating programmable shaders. It’s how Creative Assembly rendered thousands of Japanese fighting men back in Shogun Total War, and, more subtly, the same way they showed even greater numbers in 2003 with the “fully 3D” Rome. Believe it or not, even GTA 4 renders crowd members as anonymous animated billboards when things get really heavy.

Why are billboards so effective? You can show anything in a quad, and a quad can be cheap no matter what. In the case of batching, it’s not so painful to upload four verts per object per frame to the GPU. This scaled to the thousands even a decade and a half ago. In the case of instancing, you’re elegantly liberated from the restriction that all objects each command share unique defining geometry, simply because a quad is generic geometry defined by its texture content.

Thank you!

And yes, billboards are cool. Especially when they get rendered dynamically by the engine (Imposters). Do you know, if the textures for the billboards in GTA are pre-calculated?

They definitely appear pre-calculated in GTA 4, as in the Total War games. It looks goofy as hell when you focus in on the people, yet I only noticed the other day, having clocked hundreds of hours in the game before. Rockstar got away with murder!

Have you ever seen dynamic imposters used for distant chunks of environments, apart from small objects like trees?

http://i.imgur.com/Alu67Yf.jpg

Here, I’ve collected some examples of what I call “shadow people” in GTA 4, including side-by-sides and single shots. Zoom into the image. Note that they respond to the lighting environment, but have no color information- they’re just gray blobs! Presumably this is to make them reusable across more pedestrian types. It’s fascinating how Rockstar pulled them off with just a human silhouette and grounding in the environment through lighting.

They animate more smoothly than you’d expect for imposters, but what makes them clearly pre-calcuated is the limited directions they’re visible in, which itself is only apparent when they’re running away from the player’s carnage.

Thanks for the picture! This is really interesting. I would also think that they are pre-calculated but i must say, that imosters in distance are only updated if the viewing angle changes drastically. A *plop* between direction changes would be expected i think – so even real-time generated imposters could look like they were pre-calculated … i would think (but i don’t know it).

No, that*s why i wrote to the guy from Limit Theory because he said in his last dev diary that he uses imposters for asteroids. I would love to see this in action (if they are real-time generated) :D

Wow!

Nicely explained article. Really liked the way you have explained some of the complex stuff neatly. Please keep up the great work.

Cheers,

Rupesh.

Thanks for the kind words :) With all that great feedback i can’t not continue :,)

Great post Simon :)

If your looking for numbers on how many triangles you can draw for “free” on different GPUs you can find them . This is for OpenGL but I suspect they will be the same for Direct-X as it is decided by the hardware more then the API.

Also the same guy did a similar article on the optimal number of triangles.

Oops, messed up the tags… The last line in the end was about the optimal number of TRIANGLES.

Wow Thanks! That looks exactly like what i searched for. cool! I corrected your comment :D

Very nice, did not read everything but what got me is this: “A draw call is a command to render one mesh.”

I don’t know if you clarify later. But it is more than “one mesh”, it’s a set of buffers. With modern techniques you can actually draw the whole scene with one multi-draw-indirect call (you must use some uber-shader). See the following for details:

http://www.openglsuperbible.com/2013/10/16/the-road-to-one-million-draws/

And here discussions how to implement it for Ogre3D, some complex sh#t, the user “gsellers” here is the author of the previous links content:

http://www.ogre3d.org/forums/viewtopic.php?f=25&t=81060

I mentioned that, modern system fill a command buffer and send it as whole to the GPU and/or are able to fill several buffers at the same time. But your links look very good and i’ve to read them later and will add them to version 1.3 of the article. Great, thanks for your time, comment and the links :)

That was an excellent well researched and presented article. Thanks loads for taking the effort to piece this together!

Thank you very much! I’m working on version 1.2 and hope you’ll like it too as soon as it’s released :)

As an artist, I find asset optimization intimidating but you really broke it down. I was having trouble trying to decide on modular characters or not (swappable hair/armor/weapons) including lots of small textures; now I see the overhead this creates. It’s good to know since it is unnecessary for my game and was more of an uninformed design choice. I need to optimize since I am limited to the restrictions of a console but I wasn’t sure how. This is exactly what I was looking for. Thank you so much! :)

Glad to hear that i could help :) But you should also checkout other sources and maybe post the question in some forums. It’s really hard to define overall rules – so many dependancies. It’s all so complicated :(

Is there already something to show about your project? :)

I don’t have anything online yet, but I hope to release it late this year. It’s a fantasy turn-based tactical RPG for the Wii U. My programmer partner is optimizing his side, I’m glad now that I can also optimize mine. The game is not complete so we cannot tell if more optimization is necessary yet, but everything is running very well so far. :)

Sounds great! For Wii U? This is kind of special, right? I’m looking forward seeing some screenshots :) Not many people developing something for the Wii U i’ve heard. Is it hard to get a DevKit or does Nintendo support “external” developers as much as e.g. Sony?

It’s as easy to become a developer for Nintendo as it is for Sony. There are a bunch of indie developers getting projects ready for release on Wii U but not a whole lot of them, especially compared to some other systems.

If you’d like I could send you a link for screenshots on Reddit once we go public with our game.

Didn’t know that. Thanks for updating me :) I wish you the best for your game and would love to see what you’re working on!

“… and brought something with me: Four books,” – its actually Five already :)

Ups :) I’ll change it. Thanks for the hint!

Oh how could I ended up here ?

THIS IS A TREASURE CHAMBER OMG XD

Thanks for making this, I’m sure learned a lot from this.

Hello,

Thanks for the tut.

I was asking my self a question but maybe you can answer me.

I need to do a shader where I need a gradient in it to make an effect.

I have to choice:

– Create a new map with the gradient

– Create a uv2 where I will use the Y coordinate to drive the gradient

Which case do you think is more optimized ?

Having one more map or having one more uv set ?

Thanks

I think the question goes about having several different gradients in one texture, right? Or is there another reason why you want to sample the gradient-texture by Y of a second UV-Set (for example to morph the gradient-colors over time)?

It’s more about performance. Extra texture vs extra uv set.

Also sampling a gradient with the uvs will be more precise if I’m not mistaken, no chance to have color banding

Hello!

I would suggest to put the video links to open in a new tab.

I kind of closed the tab a lot of times after watching the videos.

Thanks for the suggestion! I wonder: Are you watching the content on mobile? Because on PC the videos should just start right there so I wonder how it happened that you accidentally closed a tab?

Hi Simon!

The Render Hell articles are really great! It help me a lot to understand the GPU HW.

I come from China. Can I translate these articles into chinese on my blog? I’ll not change the author of them.

Waiting for your reply. Thanks very much!

Yes of course. That’s super cool! If you give me the Link to your blog afterwards I’ll link to it :) Looking forward to your translation!

Hi Simon:

Thanks for your approval! I have translated the Book I ~ V into chinese as follow links:

Book I:

https://blog.csdn.net/hexiaolong2009/article/details/104084445

Book II:

https://blog.csdn.net/hexiaolong2009/article/details/104088308

Book III:

https://blog.csdn.net/hexiaolong2009/article/details/104089572

Book IV:

https://blog.csdn.net/hexiaolong2009/article/details/104108749

Book V:

https://blog.csdn.net/hexiaolong2009/article/details/104108917

Or you can find them here:

https://blog.csdn.net/hexiaolong2009/category_9705063.html

Because the CSDN blog can not upload videos directly, I have to convert all the animations into GIF before upload. That make all the anmations not be true to the original videos. Anyway, I think chinese programer will still be interested in these articles and your videos.

Thanks again for your effort!

Wow super cool! Thank you so much for your work! I’ll add a link the articles. Do you have a Twitter account?

Hi Simon:

I have no Twitter account because of the China network limitation. In China, we use WeChat instead of Twitter.

But you can still send email to me!

My e-mail: 343005384@qq.com

Oh ok :) I used your blog-account to link your name. I hope your audience likes the articles! Thanks again for the translation!

Wow! That’s really cool!

Thank you all the same!

Very nice article(s). I just started playing around on shaders in Unity (shadergraph, the easy start) and finding this website was an amazing experience. Everything I read is very interesting and super helpful.

Many thanks for your work!

Thank you for taking the time to write such a nice comment! <3

Hi Simon!

I’ve just found out about The Render Hell series and they are amazing.

Can I translate these articles into Vietnamese and post them anywhere you demand ?

Or I can post them on my Patreon page, of course these articles will be published for free, forever.

In the past, I used to translate The Book of Shader here (https://thebookofshaders.com/).

I also mentioned your YouTube channel as a helpful learning resource for Technical Artists in the past (https://youtu.be/eDUP4divjI4?t=3760).

Looking forward to hearing from you.

Thank you very much! Sure, feel free to translate it and as soon as you have a link for me, I can add it on top where the other translations are already linked. :)

Hi Simon!

I’ve finished translating your books into Vietnamese here:

Book 1: https://www.patreon.com/posts/108358543/

Book 2: https://www.patreon.com/posts/108655711/

Book 3: https://www.patreon.com/posts/109018057/

Book 4: https://www.patreon.com/posts/109018096/

Book 5: https://www.patreon.com/posts/109018114/

Although my translation is already finished, I still give the audience a time-window to read your books in the original language, here, to encourage them reaching out for non-native-language resources. That’s why I also published a fixed schedule to make them available as well: https://www.patreon.com/posts/108792531/

FYI, all the audience will be treated equally for this content, and they’re guaranteed to be free forever.

Hi Simon!

I’ve enjoyed translating your books into Vietnamese and completed them here: https://www.patreon.com/collection/664057?view=expanded

Hi Simon!

I’ve enjoyed translating your books and finished them here:

– Index: https://www.patreon.com/posts/vn-render-hell-108792531

– Book 1: https://www.patreon.com/posts/vn-render-hell-1-108358543

– Book 2: https://www.patreon.com/posts/vn-render-hell-2-108655711

– Book 3: https://www.patreon.com/posts/vn-render-hell-3-109018057

– Book 4: https://www.patreon.com/posts/vn-render-hell-4-109018096

– Book 5: https://www.patreon.com/posts/vn-render-hell-5-109018114

– Appendix: https://www.patreon.com/posts/vn-render-hell-108655563

Looking forward to hearing from you

Hi Simon,

I’ve finished translating your books into Vietnamese here: https://www.patreon.com/collection/664057?view=expanded

Super cool! Thank you so much for taking the time! <3

Hi Simon!

I’ve enjoyed translating your books into Vietnamese and completed them here: https://www.patreon.com/collection/664057?view=expanded

Hi Simon!

I’ve enjoyed translating your books and finished them here:

– Index: https://www.patreon.com/posts/vn-render-hell-108792531

– Book 1: https://www.patreon.com/posts/vn-render-hell-1-108358543

– Book 2: https://www.patreon.com/posts/vn-render-hell-2-108655711

– Book 3: https://www.patreon.com/posts/vn-render-hell-3-109018057

– Book 4: https://www.patreon.com/posts/vn-render-hell-4-109018096

– Book 5: https://www.patreon.com/posts/vn-render-hell-5-109018114

– Appendix: https://www.patreon.com/posts/vn-render-hell-108655563

Looking forward to hearing from you