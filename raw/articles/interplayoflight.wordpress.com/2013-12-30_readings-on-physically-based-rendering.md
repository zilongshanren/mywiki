---
title: Readings on Physically Based Rendering
url: https://interplayoflight.wordpress.com/2013/12/30/readings-on-physically-based-rendering/
author: Kostas Anagnostou
published: '2013-12-30'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

Over the past two years I’ve done quite a bit of reading on Physically Based Rendering (PBR) and I have collected a lot of references and links which I’ve always had in the back of my mind to share through this blog but never got around doing it. Christmas holidays is probably the best chance I’ll have so I might as well do it now. The list is by no means exhaustive, if you think that I have missed any important references please add them with a comment and I will update it.

**Linear Lighting and Shading**

There is probably no point in talking about PBR, without first understanding why we should do all lighting and shading in linear space. This is why:

[The Importance of being Linear](https://developer.nvidia.com/gpugems/GPUGems3/gpugems3_ch24.html). A good introduction to the topic.[Adventures with Gamma-Correct Rendering](http://renderwonk.com/blog/index.php/archive/adventures-with-gamma-correct-rendering/). Another great introduction by Naty Hoffman[Gamma FAQ – Frequently Asked Questions about Gamma](http://www.poynton.com/notes/colour_and_gamma/GammaFAQ.html). Poyton’s FAQ explains a lot of the terminology involved in gamma and linear spaces. While you are there you might as well read the[Color FAQ](http://www.poynton.com/notes/colour_and_gamma/ColorFAQ.html)also.[Uncharted 2: HDR lighting](http://www.slideshare.net/naughty_dog/lighting-shading-by-john-hable)by John Hable. This is covers many areas, but it has a great introduction to linear lighting+shading. There is also a[writeup of this presentation](http://filmicgames.com/archives/299)on John’s blog.[The value of Gamma-compression](http://hacksoflife.blogspot.jp/2010/11/value-of-gamma-compression.html). Gamma space is not all bad, this is how our eyes perceive light intensity as well as it is the preferred space for image compression and 8-bit image storing.- Nutty software have a nice
[WebGL demo](http://www.nutty.ca/?page_id=352&link=gamma_correction)of Gamma correction.

**Physically based reflection models**

Once we are convinced of the importance of linear lighting and shading we can move onto physically based reflection models.

Siggraph’s Physically Based Shading courses provide both an introduction (mainly by Naty Hoffman which is a must read) and in depth coverage of many PBR topics.

[2017 Course](http://blog.selfshadow.com/publications/s2017-shading-course/)– Presentations from Unity, Infinity Ward, DreamWorks, Framestore, ImageWorks, Pixar.[2016 Course](http://blog.selfshadow.com/publications/s2016-shading-course/)– Presentations from DICE, Unreal, Unity, Pixar, ILM. This year there was also a[video recording](https://www.youtube.com/watch?v=zs0oYjwjNEo&feature=youtu.be&t=14m48s)of some of the presentations.[2015 Course](http://blog.selfshadow.com/publications/s2015-shading-course/)– Presentations from Activision, Ready at Dawn, Weta Digital, Disney, SledgeHammer. Also Naty Hoffman’s seminal “Introduction to Physically Based Shading in Theory and Practice”presentation video recording is available[online](https://www.youtube.com/watch?v=j-A0mwsJRmk&feature=youtu.be).[2014 Course](http://blog.selfshadow.com/publications/s2014-shading-course/)– Presentations from Frostbite, Pixar, Tri-ace among others. Frostbite’s PBR presentation course notes (must read) are[also available](http://www.frostbite.com/2014/11/moving-frostbite-to-pbr/).[2013 Course](http://blog.selfshadow.com/publications/s2013-shading-course/)– Presentations from COD:Black Ops II, Unreal Engine 4, The Order:1886 and Pixar among others[2012 Course](http://blog.selfshadow.com/publications/s2012-shading-course/)– Presentations from Far Cry 3, TriAce, Disney and Pixar among others[2010 Course](http://renderwonk.com/publications/s2010-shading-course/)– Presentations from TriAce, ILM and Sony[2006 Course](http://www0.cs.ucl.ac.uk/staff/j.kautz/GameCourse/)– Very interesting introduction to PBR, including combining PBR and Image based lighting.[Physically based lighting in COD:Black Ops](http://advances.realtimerendering.com/s2011/Lazarov-Physically-Based-Lighting-in-Black-Ops%20(Siggraph%202011%20Advances%20in%20Real-Time%20Rendering%20Course).pptx). There was no PBS course in 2011 but this is a very interesting talk on the topic.- Peter Shirley’s “
[Basics of physically based rendering](http://www.cs.utah.edu/~shirley/papers/basics12.pdf)” Siggraph Asia 2012 course notes

Other interesting talks from conferences include

- Michael Drobot’s
[Lighting of Killzone:Shadowfall](http://www.slideshare.net/guerrillagames/lighting-of-killzone-shadow-fall)presentation is well worth reading, it covers a lot of PBR related topics. - Same with the video of
[GDC 2013 Panel – Metal Gear Solid 5 & Fox Engine](http://www.youtube.com/watch?v=FQMbxzTUuSg). [Static Sky Unite 2013 Presentation](http://framebunker.com/blog/static-sky-unite-presentation/)which describes the approach the game team followed to implement Physically Plausible Rendering on mobile platforms, baking a simplified Cook-Torrance BRDF into a lookup table and approximating glossiness using the mip levels of the texture.[Mastering DX11 with Unity](https://developer.nvidia.com/sites/default/files/akamai/gamedev/files/gdc12/GDC2012_Mastering_DirectX11_with_Unity.pdf)discusses Physically based shaders implemented in Unity[Physically based shading in Unity 5](http://aras-p.info/texts/files/201403-GDC_UnityPhysicallyBasedShading.pdf)GDC2014 presentation by Aras Pranckevičius (and[notes](http://aras-p.info/texts/files/201403-GDC_UnityPhysicallyBasedShading_notes.pdf)).[“The Order:1886”](http://t.co/17GYfuVOze)GDC2014 presentation by David Neubelt and Matt Pettineo is also full of useful information on the game’s material and lighting pipeline.[Moving to the Next Generation – The Rendering Technology of Ryse](http://www.crytek.com/download/2014_03_25_CRYENGINE_GDC_Schultz.pdf)GDC2014 presentation by Nicolas Schulz describes among others the shading model used in the game.[Mastering Physically Based Shading in Unity 5](http://www.slideshare.net/RenaldasZioma/unite2014-mastering-physically-based-shading-in-unity-5)from Unite2014 ([video](https://www.youtube.com/watch?v=eoXb-f_pNag)) describes in depth how Unity handles PBR, good background reading as well.

TriAce’s [Research department](http://research.tri-ace.com/) is doing some excellent work on PBR, unfortunately many of the presentations are in Japanese only. Of special note are the “[Practical Physically Based Rendering in Real-Time](http://research.tri-ace.com/Data/GDC2012_PracticalPBRinRealtime.ppt)” talk from GDC 2012 and the “[How to Design Your Art Assets for Physically Based Rendering](http://research.tri-ace.com/Data/cedec2012_FlowForPBR.pptx)” talk from CEDEC 2012. The latter is in Japanese unfortunately, so if yours is a bit rusty then [here is a translation](https://github.com/meshula/Translations/blob/master/Cedec2012_PBArtAssets.txt).

The freely available “Programming Vertex Geometry and Pixel Shaders” e-book provides a [great introduction to PBR](http://content.gpwiki.org/D3DBook:Lighting) presenting many [BRDFs](http://en.wikipedia.org/wiki/Bidirectional_reflectance_distribution_function) with shader samples.

Then there is a wealth of information available through numerous blog posts:

- Sébastien Lagarde has written some very informative blog posts on the topic, well worth reading:
[Adopting a physically based shading mode](http://seblagarde.wordpress.com/2011/08/17/hello-world/)l,[Feeding a physically based shading model](http://seblagarde.wordpress.com/2011/08/17/feeding-a-physical-based-lighting-mode/)as well as the[DONTNOD specular and glossiness char](http://seblagarde.wordpress.com/2012/04/30/dontnod-specular-and-glossiness-chart/)t. Also environment mapping (aka image based lighting) is crucial for realistic looking materials, especially metals, and this post explains[how to prepare them with AMD Cubemapgen](http://seblagarde.wordpress.com/2012/06/10/amd-cubemapgen-for-physically-based-rendering/). A good writeup of the topics described in the blog posts can be found in this[fxguide feature article on Remember Me](http://www.fxguide.com/featured/game-environments-parta-remember-me-rendering/). - More good introductions to PBR by
[Julien Guertault](http://lousodrome.net/blog/light/2012/04/15/introduction-to-light-shading-for-real-time-rendering/)and[Rory Driscoll](http://www.rorydriscoll.com/2013/11/22/physically-based-shading/) - A good introduction to
[microfacet BRDFs](http://simonstechblog.blogspot.co.uk/2011/12/microfacet-brdf.html)from Simon’s Tech Blog [Energy conservation](http://www.rorydriscoll.com/2009/01/25/energy-conservation-in-games/)is an important aspect of a BRDF, a great introduction from Rory Driscoll again. Energy conservation is worth pursuing even if you use non realistic lighting models like[wrapped-diffuse](http://blog.stevemcauley.com/2013/01/30/extension-to-energy-conserving-wrapped-diffuse/). On the topic of normalisation, Fabian Giesen shows how the[normalisation factor for Phong specular](http://www.farbrausch.de/~fg/stuff/phong.pdf)is derived and[The Blinn-Phong Normalization Zoo](http://www.thetenthplanet.de/archives/255)discusses the various options for the Phong and Blinn-Phong specular.- Brian Karis posted a
[great BRDF reference](http://graphicrants.blogspot.co.uk/2013/08/specular-brdf-reference.html)with many options for the various terms. Also worth reading is his Siggraph 2013 presentation on[Physically Based Shading in Unreal Engine 4](http://blog.selfshadow.com/publications/s2013-shading-course/karis/s2013_pbs_epic_slides.pdf). - Matt Pettineo’s
[follow up](http://mynameismjp.wordpress.com/2013/07/28/siggraph-follow-up/)to the very interesting[The Order: 1886](http://blog.selfshadow.com/publications/s2013-shading-course/)Siggraph 2013 presentation expands on some PBR topics and adds pointers to source code. [Basic Theory of Physically-Based Rendering](http://www.marmoset.co/toolbag/learn/pbr-theory)by Jeff Russell, another good, maths free, introduction to PBR.- John Hable has started blogging again, his
[Filmic Worlds](http://www.filmicworlds.com/)blog has many worth reading posts on PBR. - A very useful
[wiki page](http://wiki.nuaj.net/index.php?title=BRDF)with lots of information on BRDFs. - An easy to follow
[derivation of PI](http://www.joshbarczak.com/blog/?p=272)in NDFs by Joshua Barczak - Steve Anichini describes (among others)
[PBR in Bioshock Infinite](http://solid-angle.blogspot.co.uk/2014/03/bioshock-infinite-lighting.html)while Spencer Luebbert[describes the system](http://slueb.blogspot.co.uk/2014/04/irrational-tech-art.html)from a tech artist’s point of view. [Physically Based Deferred Rendering in Costume Quest 2](http://nosferalatu.com/CQ2Rendering.html), discusses the non-photorealistic approach to PBR taken for this game.[Physically based shading on mobile](https://www.unrealengine.com/blog/physically-based-shading-on-mobile), follows Brian Karis’[Siggraph 2013 presentation](http://blog.selfshadow.com/publications/s2013-shading-course/)up discussing adjusting the Unreal 4’s PBR model from mobile platforms.- Nathan Reed has written 2 very informative posts about Photometry and Radiometry, useful to understand light measurement units:
[Radiometry Versus Photometry](http://www.reedbeta.com/blog/2014/08/17/radiometry-versus-photometry/),[The Buttered-Toast Model Of Radiometry](http://www.reedbeta.com/blog/2014/11/02/the-buttered-toast-model-of-radiometry/). - In
[Moving Frostbite to PBR](http://www.frostbite.com/2014/11/moving-frostbite-to-pbr/)Sébastien Lagarde and Charles de Rousiers discuss realistic camera implementation in the context of PBR. - This series of posts Implementing a Physically Based Camera:
[Understanding Exposure](http://placeholderart.wordpress.com/2014/11/16/implementing-a-physically-based-camera-understanding-exposure/)and[Manual Exposure](http://placeholderart.wordpress.com/2014/11/21/implementing-a-physically-based-camera-manual-exposure/)is although worth reading.

If you don’t mind reading academic papers, some links to the original publications for various BRDFs

[Blinn-Phong](http://research.microsoft.com/pubs/73852/p192-blinn.pdf)[Ashikhmin-Shirley](http://www.cs.utah.edu/~michael/brdfs/jgtbrdf.pdfhttp://www.cs.utah.edu/~michael/brdfs/jgtbrdf.pdf)[Walter (GGX)](http://www.cs.cornell.edu/~srm/publications/EGSR07-btdf.pdf)[Cook-Torrance](http://www.cs.columbia.edu/~belhumeur/courses/appearance/cook-torrance.pdf)[Torrance-Sparrow](http://www.graphics.cornell.edu/~westin/pubs/TorranceSparrowJOSA1967.pdf)[Ward](http://www.cs.berkeley.edu/~ravir/6998/papers/p265-ward.pdf)[Oren-Nayar](http://www1.cs.columbia.edu/CAVE/publications/pdfs/Oren_SIGGRAPH94.pdf)[An overview of BRDF models](http://digibug.ugr.es/bitstream/10481/19751/1/rmontes_LSI-2012-001TR.pdf)[Making shaders more physically plausible](http://users.tricity.wsu.edu/~bobl/personal/mypubs/1993_plausible.pdf), early paper on PBR, touches many PBR related topics- Morgan McGuire et al describe a nice method to achieve
[“Physically based” cubemap specular reflections](http://graphics.cs.williams.edu/papers/EnvMipReport2013)without actually prefiltering the cubemaps with good results. - “
[Fast Filtering of Reflection Probes](http://josiahmanson.com/research/ggx_filtering/ggx_filtering.pdf)“describes a filtering technique with isotropic kernels that can be used to approximate GGX filtering (among others). [Understanding the Masking-Shadowing Function in Microfacet-Based BRDFs](http://hal.inria.fr/docs/00/94/24/52/PDF/RR-8468.pdf)by Eric Heitz, with an updated version[here](http://jcgt.org/published/0003/02/03/).- Filament’s
[PBR documentation](https://google.github.io/filament/Filament.md.html)is pretty extensive.

**PBR Tools**

[BRDF Explorer by Disney Animation](http://www.disneyanimation.com/technology/brdf.html)is a very useful tool for visualising a large number of BRDFs as well as creating your own.[cmftStudio](https://github.com/dariomanesku/cmftStudio)is another useful tool for viewing PBR models. It also comes with a[cubemap filtering tool](https://github.com/dariomanesku/cmft).- Seb Lagarde has modified AMD Cubemapgen to
[create preconvolved environment maps for PBR.](http://seblagarde.wordpress.com/2012/06/10/amd-cubemapgen-for-physically-based-rendering/) [Image based lighting baker](http://www.derkreature.com/iblbaker)is another a useful tool for baking diffuse irradiance and specular pre-convolved environment maps.- There is a free Photoshop plugin for PBR material painting created by Andrew Maximov
[here](https://www.youtube.com/watch?v=_MU3M6xqhe4). He also offers some PBR textures through his[website](http://artisaverb.info/PBT.html).

**PBR for Artists
**

The maths of PBR is only half the story and mainly concern the graphics programmers. The other half, of more interest to artists, is how to author the texture assets. In contrast to the first days of PBR, there are now a few great presentations that focus on PBR texture authoring.

[Physically based shading in Real time rendering](http://www.thetenthplanet.de/archives/3684)by Christian Schüler, a very easy to follow introduction to PBR without the maths. No texture authoring in this one but well worth a read by artists.[The Art and Rendering of Remember Me](http://seblagarde.files.wordpress.com/2013/08/gdce13_lagarde_harduin_light.pdf)from GDCEurope 2013 by Sébastien Lagarde and Lauren Harduin cover a lot of aspects of PBR and provide artist guidelines for texture authoring.[Calibrating Lighting and Materials in Far Cry 3](http://blog.selfshadow.com/publications/s2012-shading-course/)by Stephen McAuley from Siggraph 2012, including capturing and colour correcting textures.[How to Design Your Art Assets for Physically Based Rendering](http://research.tri-ace.com/Data/cedec2012_FlowForPBR.pptx)by Yoshiharu Gotanda, another good set of guidelines on how to author maps for PBR ([translation](https://github.com/meshula/Translations/blob/master/Cedec2012_PBArtAssets.txt))[Shining the Light on Crysis 3](http://www.crytek.com/cryengine/presentations/shining-the-light-on-crysis-3)by Pierre-Yves Donzallaz provides another good non-maths introduction to PBR, describes Crysis 3’s lighting pipeline and provides guidelines for environmental art.[RYSE – The transition to Physically Based Shading](http://www.makinggames.de/index.php/magazin/2391_ryse__the_transition_to_physically_based_shading)explains why the team moved to PBS, describes the art pipeline changes provides a high level overview of the game’s lighting system.[The tech of Crytek’s Ryse: Son of Rome](http://www.fxguide.com/featured/the-tech-of-cryteks-ryse-son-of-rome/)alsohas some info on the game’s PBS.- Defrost Game’s
[Feeding a Physically Based Lighting model](http://www.indiedb.com/games/project-temporality/news/nordic-game-conference-2013-feeding-a-physically-based-lighting-model)is another good math free introduction to PBR. - A great “PBR for artists by an artist”
[video presentation](https://www.youtube.com/watch?v=LNwMJeWFr0U)by Andrew Maximov. - A good, maths free and artist friendly,
[introduction to PBR](http://www.marmoset.co/toolbag/learn/pbr-practice)by Marmoset. While you are there, it is worth reading their[Theory of Physically Based Rendering](http://www.marmoset.co/toolbag/learn/pbr-theory)and[PBR Texture Conversion](http://www.marmoset.co/toolbag/learn/pbr-conversion)articles as well. - An easy to read and comprehend
[introduction to PBR for artists](http://www.filmicworlds.com/2014/02/24/physically-based-specular-for-artists/)by John Hable. - The
[Physically Based Rendering Encyclopedia](https://docs.google.com/document/d/1Fb9_KgCo0noxROKN4iT8ntTbx913e-t4Wc2nMRWPzNk/edit)is a good, easy to understand, summary of many PBR related topics. - Wolfire’s intro to
[Physically Based Rendering](http://blog.wolfire.com/2015/10/Physically-based-rendering).

You can also find a modular implementation of the BlinnPhong BRDF model with demonstration of the impact of each term and sample source code in [this blog post](https://interplayoflight.wordpress.com/2013/12/23/an-educational-normalised-blinn-phong-shader/) (shameless plug).

**Physically based lights**

Physically based shading focuses on how a material responds to light that bounces off the surface in a plausible way. To get better results one should consider the type of light that shines upon the surface as well. Point lights, typically used in games, do not have a counterpart in the real world so several attempts have been made recently to model more realistic, area, lights in games.

[An early attempt to model area lights analytically](http://research.microsoft.com/en-us/um/people/johnsny/papers/arealights.pdf)by John Snyder (Microsoft Research).[The Art and Rendering of Remember Me](http://seblagarde.files.wordpress.com/2013/08/gdce13_lagarde_harduin_light.pdf)by Lagarde and Harduin talks about how they added area lights to the game- Same with
[Physically Based Shading in Unreal Engine 4](http://blog.selfshadow.com/publications/s2013-shading-course/karis/s2013_pbs_epic_slides.pdf)by Karis, a WebGL demo based on the techniques presented[here](http://alteredqualia.com/xg/examples/deferred_tubelights.html). [Killzone:Shadowfall](http://www.slideshare.net/guerrillagames/lighting-of-killzone-shadow-fall)has also put area lights to good use with great results- A very interesting introduction to
[Area Light Shadows](http://www.geomerics.com/downloads/AltDevConf-SamMartin-RealTimeAreaLighting.pdf)by Sam Martin - Some very nice research on
[Area Lights](https://labs.unity.com/article/real-time-polygonal-light-shading-linearly-transformed-cosines)by Eric Heitz et al.

**BRDFs in deferred rendering environments**

A variety of BRDFs can easily be implemented in forward rendering architectures. Things become harder with deferred shading though due to the typically low amount of information we can store in a g-buffer. Anisotropic BRDFs are even harder to support, due to the need for a tangent vector. In many cases a single BRDF is enough to represent a variety of materials if you have the capacity to store glossiness and specular colour in the g-buffer. There are cases you might need more though. Some pointers to how people have address this problem so far:

- Bake BRDFs in a 3D lookup table, each layer representing a different BRDF and within each layer addressed by (N.L, N.H). This method was used in
[STALKER’s deferred shading engine](http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter09.html). - Another approach is to store Material IDs in the g-buffer and during the lighting pass branch to select the desired BRDF. This is the method used in
[Battlefield 3](http://www.slideshare.net/DICEStudio/spubased-deferred-shading-in-battlefield-3-for-playstation-3). - At
[Creative Assembly](http://www.creative-assembly.com/news/120724/develop-2012-light-fantastic)they use the stencil buffer to store the material ID and render each BRDF in a different pass. - And of course you can always forward render special-case BRDF materials. This is the approach followed recently by Ryse: Son of Rome to
[render specialised BRDFs](http://www.makinggames.de/index.php/magazin/2391_ryse__the_transition_to_physically_based_shading). - The “
[Deferred Lighting in Uncharted 4](http://advances.realtimerendering.com/s2016/)” Siggraph 2016 presentation describes how to support multiple BRDFs in a deferred rendering engine with bit-packing in the GBuffer and a table of material-specialised shaders running per-tile.

Not directly related to deferred rendering, being more of a material authoring pipeline, Material Layering is receiving a lot of attention lately after [Disney](http://blog.selfshadow.com/publications/s2012-shading-course/), [Unreal Engine 4](http://blog.selfshadow.com/publications/s2013-shading-course/) and [The Order:1886](http://blog.selfshadow.com/publications/s2013-shading-course/) successfully demonstrated the variety and complexity of materials that can achieve. In short, with this technique we bake parameters of a specific BRDF (that express different materials) into textures which can then be blended before the lighting pass either offline or in the shader. In The Order:1886 blending of different BRDFs is also supported albeit at a greater cost.

**Importance Sampling**

You will hear [Importance Sampling](http://en.wikipedia.org/wiki/Importance_sampling) being mentioned in the context of PBR, image based lighting and area lights, quite a lot so it is worth having an idea what it is all about. In short it is a method of sampling a function, image, cubemap etc with a set number of samples by assigning larger weight to important areas of the sampled function (or image, or cubemap). This way we can achieve better representation of the signal without actually increasing the number of samples. This method was feasible only in offline rendering but GPUs are catching up.

[GPU-based Importance Sampling](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch20.html), a method of sampling environment maps for image-based lighting using BRDFs. Some more information about this work[here](http://cgg.mff.cuni.cz/~jaroslav/papers/2007-sketch-fis/Final_sap_0073.pdf). The original page is not there anymore, you can try your luck with[web archive](http://web.archive.org/web/20080522131112/http://graphics.cs.ucf.edu/gpusampling/).[Killzone: Shadowfall](http://www.slideshare.net/guerrillagames/lighting-of-killzone-shadow-fall)uses importance sampling to sample area lights- If you have the ShaderX7:Advanced Rendering Techniques book it is worth reading the “Efficient post processing with Importance Sampling” chapter by Toth, Szirmay-Kalos and Umenhoffer

**Tonemapping**

Not directly related to PBR, but when normalising a BRDF the specular highlight intensity can easily reach values above 1 and appear to burnout. For that reason we typically combine PBR with a tonemapping solution. A few pointers to get you started:

[A Closer Look At Tone Mapping](http://mynameismjp.wordpress.com/2010/04/30/a-closer-look-at-tone-mapping/), Matt Pettineo provides a showcase of popular tonemapping operators with sample code.- Hable’s
[Uncharted 2 Lighting](http://www.slideshare.net/naughty_dog/lighting-shading-by-john-hable)presentation as well as his[blog](http://filmicgames.com/archives/category/tonemapping)provide a lot of valuable background info on tonemapping. - Angelo Pesce’s
[HDR Workflows](http://www.scribd.com/doc/125071012/HDR-Workflows-for-Video-Game-Rendering)is another good introduction to the subject providing many useful insights [Postprocessing in the Orange box](http://www.gdcvault.com/play/185/%28103%29-Advanced-Visual-Effects-with)by Alex Vlachos details Valve’s HDR pipeline- The Programming Vertex, Geometry and Pixel shaders ebook has a nice
[introduction to HDR/Tonemapping](http://content.gpwiki.org/D3DBook:High-Dynamic_Range_Rendering)as well. - A nice
[WebGL demo](http://www.nutty.ca/?page_id=352&link=hdr)showcasing the Reinhard tonemapping operator ([original paper](http://www.cs.utah.edu/~reinhard/cdrom/tonemap.pdf)). [This paper](http://cinematiccolor.com/)which introduces the colour pipelines behind modern feature-film visual-effects and animation is also relevant.

**Shader Antialiasing**

Again, this topic is not directly related to PBR, but it is a shame to make all that effort to create realistic materials only to have specular highlights crawl and shimmer as the camera moves and surfaces look flatter at a distance.

- Togsvig presented a
[cheap and nice looking method](https://developer.nvidia.com/content/mipmapping-normal-maps)to adjust the specular power based on the mipmapped normal variation. Stephen Hill has created a[WebGL demo](http://www.selfshadow.com/sandbox/gloss.html)of this technique. - Stephen Hill’s
[Rock Solid Shading](http://advances.realtimerendering.com/s2012/Ubisoft/Rock-Solid%20Shading.pdf)Siggraph talk as well as the related blog post on[Specular AA](http://blog.selfshadow.com/2011/07/22/specular-showdown/)are a must read. [Spectacular Specular-LEAN and CLEAN specular highlights](http://www.gdcvault.com/play/1014558/Spectacular-Specular-LEAN-and-CLEAN)by Dan Baker details the Specular AA technique used in Civilisation 5 as well as describing the specular aliasing problem.[Frequency Domain Normal Map Filtering](http://www.cs.columbia.edu/cg/normalmap/normalmap.pdf), the specular AA method used in[The Order:1886](http://blog.selfshadow.com/publications/s2013-shading-course/)is based on, calculates an[NDF](http://www.reedbeta.com/blog/2013/07/31/hows-the-ndf-really-defined/)for each texel of the normal map using all normals from the highest-resolution mip level that contribute to a single lower-resolution texel. This NDF is then convolved with the BRDF. The produced BRDF that properly accounts for the variance of all normal map texels for a specific pixel.- In
[this blog post](http://mynameismjp.wordpress.com/2013/07/28/siggraph-follow-up/)Matt published a sample application that implements and showcases popular specular AA techniques including Frequency Domain Normal Map Filtering, well worth a look. [Antialiasing Physically Based Shading with LEADR Mapping](https://interplayoflight.wordpress.com/Antialiasing%20Physically Based Shading with LEADR Mapping)Siggraph 2014 presentation also has lots of good information on antialiasing in PBR pipelines.- The recent work of Anton Kaplanyan et al on rendering stable subpixel glints and details is also worth following:
[Real-time Rendering of Procedural Multiscale Materials](https://research.nvidia.com/publication/real-time-rendering-procedural-multiscale-materials),[Rendering Highly Specular Materials](http://on-demand.gputechconf.com/siggraph/2016/presentation/sig1666-anton-kaplanyan-rendering-highly-specular-materials.pdf)([video](http://on-demand.gputechconf.com/siggraph/2016/video/sig1666-anton-kaplanyan-rendering-highly-specular-materials.mp4)). - Temporal antialiasing is very popular lately, check Marco Salvi’s
[GDC2016 presentation](https://www.dropbox.com/sh/dmye840y307lbpx/AAAQpC0MxMbuOsjm6XmTPgFJa)for an introduction.

I focused on materials readily available on the Internet. There are books worth looking at if you want to find more info though, such as:

[Physically Based Rendering](http://www.pbrt.org/)by Matt Pharr and Greg Humphreys, with source code[Real-Time Rendering](http://www.realtimerendering.com/), by Tomas Akenine-Möller, Eric Haines, and Naty Hoffman- High Dynamic Range Imaging: Acquisition, Display, and Image-Based Lighting 2nd edition by Erik Reinhard, Wolfgang Heidrich, Paul Debevec, Sumanta Pattanaik, Greg Ward and Karol Myszkowski
- “An Efficient and Physically Plausible Real Time Shading Model” by Christian Schüler in ShaderX7 – Advanced Rendering Techniques

As I’ve already mentioned, this list is not exhaustive, if you think that I have missed an important link or topic please add it to the comments sections.

Enjoy!

*Edit 03/08/2018 – Added Filament’s PBR documentation reference*

*Edit 22/11/2017 – Added Siggraph 2017 PBS course link*

*Edit 11/08/2016 – Added Deferred Lighting in Uncharted 4, Subpixel glint/details rendering links and the video recording of Intro to PBS talk kindly suggested by Naty Hoffman.
*

*Edit 10/08/2016 – Added Siggraph 2016 PBS course link, Area lights with Linearly Transformed Cosines link
*

*Edit 22/10/2015 – Added Wolfire’s intro to Physically Based Rendering*

*Edit 16/08/2015 – Added Siggraph 2015 PBS course link *

*Edit 21/02/2015 – Added Allegorithmic’s PBR guides and Tri-ace’s Siggraph 2014 talk. *

*Edit 22/12/2014 – Fixed HDR Workflows broken link and added Cinematic Colour paper suggested by Kyle Hayward*

*Edit 30/11/2014 – Added Physically based camera links kindly suggested by Seb Lagarde, PBR in Unity kindly suggested by Aras Pranckevičius, Antialasing PBR with LEADR mapping SIG2014 presentation and Marmoset’s Preparing textures for PBR article.*

*Edit 23/11/2014 – Added Siggraph 2014 Course links, Unreal 4 PBR on mobile, Nathan Reed’s Photometry and Radiometry blog posts and PBR for Costume Quest 2 article. Also added new section about Tools for PBR.*

*Edit 27/07/2014 – Added Bioshock Infinite PBR posts, PBR Encyclopedia, and Photoshop PBR Plugin.
*

*Edit 11/04/2014 – Replaced broken WebGL gamma correction demo link, thanks to Peter Liu for the heads up.
*

*Edit 27/03/2014 – Added Crytek’s GDC2014 presentation, “The tech of Crytek’s Ryse: Son of Rome” suggested by Sébastien Lagarde and the BRDF wiki page suggested by Peter Liu.
*

*Edit 23/03/2014 – Added “Physically based shading in Unity5”, “The Order: 1886” GDC2014 talks as well as Hable’s Filmic Worlds blog links.
*

*Edit 25/02/2014 – Added “Introduction to PBR for artists” article by John Hable to the PBR for Artists section.*

*Edit 23/02/2014 – Added “Introduction to PBR” article by Marmoset to the PBR for Artists section.
*

*Edit 11/01/2014 – Added “Understanding the Masking-Shadowing Function in Microfacet-Based BRDFs” technical report as well as Russell’s “Basic Theory of Physically-Based Rendering” article.
*

*Edit 31/01/2014 – Added PBR for Artists video by Andrew Maximov*

*Edit 03/01/2014 – Added “An Efficient and Physically Plausible Real Time Shading Model” ShaderX7 book chapter reference kindly suggested by Sébastien Lagarde*

*Edit 31/12/2013 – Added a few missing links kindly suggested by Sébastien Lagarde and Aras Pranckevičius*

* *

Hey there Kostas. Great collection, thanks!

Here’s something you might also find useful:

cheers

Added, great presentation, thanks!

http://wiki.nuaj.net/index.php?title=BRDF

about brdfs concept.

Updated, thanks!

I’ve hosted a mirror of the Gamma correction WebGL demo here, for anyone interested: https://dl.dropboxusercontent.com/u/3017460/WebGL/index.src.htm

That’s great, thank you! Updated blog post.

hello!

in your “Linear Lighting and Shading” part

there is an list “Devmaster has a nice WebGL demo on Gamma correction (EDIT: unfortunately this demo does not seem to work for me anymore. EDIT 2: there is a mirror of that demo here). ”

the origin website link maybe comes from here(it looks ok)

http://www.nutty.ca/?page_id=352&link=gamma_correction

Thanks for the heads up, I’ve replaced the link.

[…] https://interplayoflight.wordpress.com/2013/12/30/readings-on-physically-based-rendering/ […]

[…] I’ve been thinking about experimenting with physically based rendering for a long time, but at first I didn’t want to write any code. So I turned to the Blender Cycles path tracer. Cycles is great because it should give the “ground truth” path traced solution, so later I can see how close I got to that. However, simply importing a model doesn’t give you nice results outright, you have to set up the materials. I also read a lot about PBR from mainly here: https://interplayoflight.wordpress.com/2013/12/30/readings-on-physically-based-rendering/ […]

[…] Based Rendering theory: – https://interplayoflight.wordpress.com/2013/12/30/readings-on-physically-based-rendering/ – […]

[…] https://interplayoflight.wordpress.com/2013/12/30/readings-on-physically-based-rendering/ […]

This is a great collection of information, thanks.

Thanks a lot for this. Was kind of hard to find, though. Should be shared a lot more often!

hi

Click to access CS-Jimenez-Kwast-Daniel.pdf

well, it is just basics of brdf paper, i have found it in one paper reference

Thank you Kostas, your post is very comprehensive and helpful!

Thank so much Kostas! Very comprehensive resources for PBR. Please keep updating so the community has the to-go reference on this.

The “Deferred Lighting in Uncharted 4” talk from this year’s “Advances” course would be good to add to the “BRDFs in deferred rendering environments” section – it talks about another way to support multiple BRDFs in deferred (bit-packing in GBuffer + table of material-specialized shaders running per-tile). Also, in the section about LEAN & similar approaches, it would be good to add some references which go to the next step and support “glinty” appearance rather than over-smoothing as the normal-map filtering approaches do (e.g. The I3D 2016 paper by Kaplanyan et al). Also, my background intro video from the 2015 PBS course (which is likely to be the last one, at least for a while since I’ve changed to a less “backgroundy” type of intro starting this year) has been posted online: https://youtu.be/j-A0mwsJRmk

Thanks for the suggestion Naty! I will add them to the list.

[…] PBR 相关参考资料：Interplay of Light […]

[…] This blog has a lot of links for you to hunt: https://interplayoflight.wordpress.com/2013/12/30/readings-on-physically-based-rendering/ […]

Thank you very much for this topic!

Thank you so much, the first link changed: “https://developer.nvidia.com/gpugems/GPUGems3/gpugems3_ch24.html”

Thank you, I updated the post.

[…] plug for my list of Physically based rendering resources […]