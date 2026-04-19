---
title: Wanna play with OpenCL?
url: https://c0de517e.blogspot.com/2012/08/wanna-play-with-opencl.html
published: '2012-08-22'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

[OpenCL Studio](http://www.opencldev.com/)is a nice wrapper of OpenCL and Lua packed in a ad-hoc IDE. It’s a nice way to explore OpenCL and it has some video tutorials, but you might want to delve into it a bit faster than that.

Here’s a quick guide through its particles.3Dm example (OpenCLStudio 2.0). It won’t teach you anything of OpenCL, but it will guide you through a few things in OpenCLStudio and past that you should be at home if you know the basics of OpenGL and OpenCL (and Lua).

In fact (and that’s true for most my posts), I’m writing this as notes to self while I explore OpenCLStudio for the first time…

**1) The Project tree and the main Scene window**

Here you can create, view and edit (see the properties tab on the bottom of the application) all the main resources in the project (OpenGL, OpenCL and some OpenCLStudio specific things like its GUI and the Script Processor). Each resource is reflected and available to the scripting system (Lua).

Also notice on the top of the project tree two buttons, one to run the application, the other to reset it. The reset button executes all the non per frame scripts, so if you modify one of these you’ll need to reset to see the changes, all other scripts and shader code are automatically hotswapped after a successful compile.

Project tree elements can be added only if the project is in its reset state. In this state you get access also to some other edit abilities which don’t work after you run the application, for example if you create some OpenGL “geometry” it will be editable with manipulators in the scene, if the project is reset, but the manipulators won’t appear otherwise.

The scene window is pretty self explanatory, you can see here your 3d world (through the camera you have in the project tree) and all the GUI elements if you have them.

Notice that if you have the project running and you click on an OpenCL source in the tree (i.e. clParticles), in its properties you’ll get the timing of its various kernels. Nifty!

**2) Script walkthrough**

The tab named "script” shows the contents of one of the “script processors” (see again the project tree). The way this works is a bit unusual, the scripts are bound to objects in the scene tree (callbacks of said objects to be precise) and for some reason still unclear to me, each script processor can host only 32 objects and these are arranged in a 4x8 grid of slots in the processor.

You can create an arbitrary number of processors though and the position of a given object in a processor grid does not seem to mean anything, so in practice, if you want to script an object behavior, you just drag it into an empty slot of a processor and write some code for a given callback.

Most scripts associated with resources are to initialize them. Start looking at bfForce for example and its “OnDeposit” (creation) callback, and how it initializes its memory to zeroes. The “event” instance contains the information about the object whose callback is attached to, and its properties change depending on the object, you can read about them in help/inbuilt/classes.

Notice that all the windows with some code in them have a small red downward arrow button, that is the compile one. Kernels and shaders will be hotswapped after a compile, Lua scripts will be swapped as well but if they don’t execute every frame you won’t notice until you reset.

All the methods have a decent documentation that pops up automatically while autocompleting (or you can find it going in the Help tab, Inbuilt, and on the bottom selecting the Modules tab… OpenCLStudio seems to have some nice features but they are often slightly rough…).

Next, have a look at bfParams OnDeposit, which is a bit more complicated. Here it prepares this small param buffer and you can notice how the event is not read-only, in fact here it’s sizing the buffer based on struct.size(“System”) thus the size you declare in the object properties in the project tree won’t really matter (try to change it, reset the project, and see).

Ok, now it’s time to peek at the Global window in our Script tab… always visible this will get executed before everything else, and thus can declare some support structures for the entire script processor… Here you can see it creates the struct named “System” with some fields (struct is a way OpenCLStudio has to map raw data arrays to c-like structures) and then some global variables. Now it should be clear that bfParams OnDeposit takes the OpenCL buffer of the bfParams object, sizes it and then assigns to it an “intepretation” saying that it will correspond to the “System” structure which is used to pass to the OpenCL kernels the application parameters, then it maps it, telling that the buffer will be writable from the application (CPU).

You can peek around all the OnDeposit/OnRemove members, when you’re satisfied, go to the meat of the application, which is the per frame execution contained in OpenCL OnTime. This does everything, and really it’s in the OpenCL object but it doesn’t access the “event” so it could be everywhere in an OnTime, you can move it into the OpenGL object for example and you’ll notice it will still work.

This main application code is very straightforward and should not surprise you at all.

**3) GPU Code and how the particle system works**

The code tab is where the GPU code is. If you select and OpenCL module or an OpenGL shader in the project tree, the code tab will display its code.

So, how is this particles.3Dm example implemented? Well, looking around, starting from the OpenCL OnTime script, you’ll notice how things are arranged.

Particles are split into an OpenGL representation, made of three streams: Position, Color and Velocity. Position and Velocity are updated by OpenCL kernels (clEnqueueAcquireGLObjects…), Color is set via a Lua OnDeposit method and never changed. In this example the OpenGL shaders do not use the velocity stream, so it could have even not be declared as an OpenGL buffer.

The integration is done using a simpler Euler step (clIntegrate kernel followed by clClipBox), then particles get sorted via a spatial hash (clHash/radix sort/reorder kernels) into the bfSortedVel and Pos arrays.

Notice how the radix sort does not require all the clSetKernelArg calls and so on, it’s part of the

[libCl](http://www.libcl.org/index.html)opensource library (by the same authors of OpenClStudio) and has been wrapped by in a way that takes care of all the binding outside Lua.

After sorting, particles are assigned to buckets, which are represented by a start and end index into the sorted particle array (bfCellStart and End). This is done via the clBounds kernel, which per each particle it compares its hash with the hash of the next particle (remember, they are sorted by now) and when a difference is found it knows a particle block ended and it writes cellEnd and cellStart. This kernel is interesting as it uses the thread local space to avoid fetching twice from global memory the hashes (which on a modern card is not actually faster, but still...). Notice how the local space is assigned in the Lua script, clSetKernelArg reserves space for one unsigned int per thread plus another global int (see how the work is grouped into 256 thread units in clEnqueueNDRangeKernel).

All this bucketing is done obviously to speed up particle/particle collisions, done via clCollideParticles is a pretty unsurprising way, notice how in the global Lua script the CELLSIZE is twice the particle size. After that, analytic collisions with the scene’s big unmovable spheres is done, this again is fairly trivial and will also take care of getting the data back into the unsorted rendering arrays.

As you can see this example, I think for sake of clarity, does many more passes (kernels) than it could have, particles2.3Dm is not better, it just adds more eye candy, so it’s a nice starting point for your own experiments. Have fun!

## No comments:

Post a Comment