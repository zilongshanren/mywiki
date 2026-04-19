---
title: Rendepth Developer Preview
url: https://cybereality.com/rendepth-developer-preview/
author: Cybereality
published: '2024-10-21'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![](../../assets/132e8b225eb338df.jpg)

Started working on Rendepth for real this time. Had two previous prototypes, one in OpenGL and one in an engine I won’t mention. I also have a command-line processor in Python (for the color depth estimation portion). This past week I decided to reboot fresh with [SDL3](https://wiki.libsdl.org/SDL3/FrontPage) and make something I felt was production ready. Managed to get the bread and butter of a 2D photo viewer up and running. Still a few features missing, such as zoom and pan, though the basics are already working.

![](../../assets/30bf2acc89913aee.jpg)

SDL 3.0 has been pretty great to work with. For the most part it’s just an overhaul of the 2.0 release, with more modern features, like support for HDR monitors. The big new addition is the [GPU API](https://github.com/TheSpydog/SDL_gpu_examples), which encapsulates the major graphics APIs (Vulkan, DirectX, and Metal) so you can write to one target and (theoretically) it runs on everything. The shaders are using SPIR-V, and can be written with the Vulkan dialect of GLSL. Overall, it was not hard to work with, given I have experience with Vulkan. That said, there are literally zero tutorials and not much high level information. The documentation amounts to API reference material, which is well written, but you still have to know what you are looking for. There are also about a dozen samples, but they are very basic (clearing the screen, colored triangle, etc.) and I don’t believe even show you how to send a uniform to a shader. It took me about 3 hours to find how to pass a vec3 into my shader. Granted it was super simple and only a few lines of code, but I had to dig around the source to figure it out. In general, though, the RHI is solid and turned what would have been well into 1,200 lines of Vulkan C++ code into maybe 200 lines of SDL3 C++. Much cleaner and easier to work with. Perhaps not as lightweight as raw OpenGL, but also sort of in the ballpark. Keep in mind that it’s still in beta and not even officially out, but appears stable to me, and they claim API locked.

My designer has completed the app icons, and I’ll be coding a UI next. This will probably not be super fully featured at first, just some textured quads and hit testing. But I feel the design is pretty minimal and slick. You can see the original mock-up I did above. SDL3 has built-in font support, which will make this a little easier, and the [SDL Image 3.0](https://wiki.libsdl.org/SDL3_image/FrontPage) library has modern image format compatibility, so I’m able to open JPEG-XL, AVIF, and WebP, with no issues, as well as almost every older format (JPG, PNG, BMP, etc.). Having this all go through the same API is a godsend as it makes the loading code a lot more straight-forward.

Other than that, you can see the features I’ve implemented in the developer preview video. It’s almost replicated the essential features from the GNOME Image Viewer, or the one that comes with Windows. Still have a ways to go, though this is only the first week. At this pace, I’m confident I can have an initial release next month. I also finalized the Rendepth logo, and the website is being designed right now. Will probably try to support just the few newer glasses-free displays that came out, namely the [Looking Glass Go](https://lookingglassfactory.com/looking-glass-go-spatial-photo-frame) and [Acer Predator SpatialLabs View 27](https://www.acer.com/us-en/predator/monitors/spatiallabs-view-27). Will also want to look at the [Lume Pad 2](https://www.leiainc.com/lume-pad-2) after that (though this is Android and will be more complex). If all goes well I could complete within the year (fingers crossed) though I will also want to look at support for VR headsets and standard 2D displays, eventually, since those are fairly large markets. Stay tuned.