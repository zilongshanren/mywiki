---
title: What Does gpus_ReturnGuiltyForHardwareRestart Mean?
url: http://hacksoflife.blogspot.com/2013/08/what-does-gpusreturnguiltyforhardwarere.html
author: Benjamin Supnik
published: '2013-08-25'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

First, a bunch of disclaimers: I do not know how the PowerVR SGX hardware really works, I do not have access to either the Apple OpenGL source or the PowerVR SGX driver source, and therefore what follows is all


With that out of the way, you're sitting in your office sipping iced coffee and coding OpenGL ES 2.0 subroutines for IOS. You test on the device and get an access violation with this back-trace.



From what I can tell, you get an intentional crash in gpus_ReturnGuiltyForHardwareRestart when something goes wrong on the GPU itself, asynchronously, that the driver failed (or didn't bother) to catch.


For example, if you are calling glDrawElements with VBOs bound for both the element array and all vertex buffer sources, then the draw call will be hardware accelerated*: the driver will write some commands to the command buffer to draw from addresses in the GPU address space (which I guess is just system memory for an iPhone) and the GPU will later read the command and start fetching elements.


If you have screwed up and requested an element index that is out of bounds for the vertex arrays, the driver won't notice, because it is not copying your vertex data (and fortunately isn't wasting time bounds-checking your index buffer). Instead the GPU will eventually start fetching vertices directly, and when it notices that one of the vertex fetches went out of bounds, it's going to make a note for the driver to fetch later.


So to sum up so far: you do a hardware-accelerated glDrawElements with bad index data (or the wrong VBO bound, or any other way to get out-of-bounds vertex fetches) and some time


So now we can look at why we blew up in glBufferData, a seemingly unrelated call. glBufferData called into GLEngine (which is Apple's common OpenGL engine), which eventually had to talk to the specific PowerVR SGX driver. (Apple's OpenGL stack is made of a common front-end that Apple produces, and back-end drivers that talk to specific hardware.) The SGX driver at that point goes to talk to the hardware and discovers that since its last check, something really bad happened (E.g. we went out of bounds in our draw call). The SGX driver then calls Apple back, calling gpus_ReturnGuiltyForHardwareRestart, which I guess is Apple's way to have a GPU vendor's driver tell them that the GPU itself seg faulted.


What makes these crashes exciting is their synchronous nature: the call that you get the crash in is (1) not the call that offended OpenGL and (2) affected by timing on both the CPU, and GPU (because the crash comes in the first CPU call to talk to the GPU after the GPU detects the problem, which happens whenever it has time to get to your draw call). So the normal technique (comment things out and see what changes) just moves the crash around.


Based on this speculation, the way I fixed the problem was: I wrote a (very slow) debug routine to check the indices of all glDrawElements and glDrawArrays calls, mapping back the buffers as needed, and asserting that things are sane. This immediately caught our real problem: a client-array draw call was failing to unbind VBOs - by luck the call before had changed to leave a VBO bound. The client-array call was now drawing out of VBO memory, not its own, and since the VBO was smaller than the client array being specified, the draw call would run off the end of the VBO.


Because we have macros that map all glDrawElements and glDrawArrays calls to our own routines (that then call the real glDrawElements and glDrawArrays calls) adding this error checking was quite trivial; why we have those macros will have to be another blog post.


* Well, maybe it will be hardware accelerated. If you have poorly aligned vertex data or use a wonky format, you might fall back to software vertex transfer. This is fairly easily spotted in Instruments because your draw call will have routines with IMM below them in the trace, and a lot of CPU time will be spent immediately copying your vertices. Accelerated draw calls themselves take almost no time to execute other than time to update GL state (which is also usually visible in Instruments).

*speculative engineering*(read: guess work). So if what follows is wrong, you've been warned.With that out of the way, you're sitting in your office sipping iced coffee and coding OpenGL ES 2.0 subroutines for IOS. You test on the device and get an access violation with this back-trace.

```
``````
frame #0: 0x31e23916 libGPUSupportMercury.dylib`gpus_ReturnGuiltyForHardwareRestart + 10
frame #1: 0x31e24398 libGPUSupportMercury.dylib`gpusSubmitDataBuffers + 104
frame #2: 0x2c38888c IMGSGX543GLDriver`SubmitPackets + 124
frame #3: 0x2f74d6be GLEngine`gleCleanupOrphans + 130
frame #4: 0x2f72151e GLEngine`glBufferData_Exec + 254
frame #5: 0x010be8e6 libglInterpose.dylib`buffer_data(__GLIContextRec*, unsigned int, long, void const*, unsigned int) + 158
frame #6: 0x2f7b1c26 OpenGLES`glBufferData + 38
```


The question is: WTF? What does this mean? You look at your call to glBufferData and it looks (1) totally sane and (2) seems to have exploded on the 405th invocation. Why did it just stop working now?From what I can tell, you get an intentional crash in gpus_ReturnGuiltyForHardwareRestart when something goes wrong on the GPU itself, asynchronously, that the driver failed (or didn't bother) to catch.

For example, if you are calling glDrawElements with VBOs bound for both the element array and all vertex buffer sources, then the draw call will be hardware accelerated*: the driver will write some commands to the command buffer to draw from addresses in the GPU address space (which I guess is just system memory for an iPhone) and the GPU will later read the command and start fetching elements.

If you have screwed up and requested an element index that is out of bounds for the vertex arrays, the driver won't notice, because it is not copying your vertex data (and fortunately isn't wasting time bounds-checking your index buffer). Instead the GPU will eventually start fetching vertices directly, and when it notices that one of the vertex fetches went out of bounds, it's going to make a note for the driver to fetch later.

So to sum up so far: you do a hardware-accelerated glDrawElements with bad index data (or the wrong VBO bound, or any other way to get out-of-bounds vertex fetches) and some time

*later*the GPU gets around to executing your command (which has not been pre-checked), notes that it went out of bounds, and leaves a note for the driver to pick up.So now we can look at why we blew up in glBufferData, a seemingly unrelated call. glBufferData called into GLEngine (which is Apple's common OpenGL engine), which eventually had to talk to the specific PowerVR SGX driver. (Apple's OpenGL stack is made of a common front-end that Apple produces, and back-end drivers that talk to specific hardware.) The SGX driver at that point goes to talk to the hardware and discovers that since its last check, something really bad happened (E.g. we went out of bounds in our draw call). The SGX driver then calls Apple back, calling gpus_ReturnGuiltyForHardwareRestart, which I guess is Apple's way to have a GPU vendor's driver tell them that the GPU itself seg faulted.

What makes these crashes exciting is their synchronous nature: the call that you get the crash in is (1) not the call that offended OpenGL and (2) affected by timing on both the CPU, and GPU (because the crash comes in the first CPU call to talk to the GPU after the GPU detects the problem, which happens whenever it has time to get to your draw call). So the normal technique (comment things out and see what changes) just moves the crash around.

Based on this speculation, the way I fixed the problem was: I wrote a (very slow) debug routine to check the indices of all glDrawElements and glDrawArrays calls, mapping back the buffers as needed, and asserting that things are sane. This immediately caught our real problem: a client-array draw call was failing to unbind VBOs - by luck the call before had changed to leave a VBO bound. The client-array call was now drawing out of VBO memory, not its own, and since the VBO was smaller than the client array being specified, the draw call would run off the end of the VBO.

Because we have macros that map all glDrawElements and glDrawArrays calls to our own routines (that then call the real glDrawElements and glDrawArrays calls) adding this error checking was quite trivial; why we have those macros will have to be another blog post.

* Well, maybe it will be hardware accelerated. If you have poorly aligned vertex data or use a wonky format, you might fall back to software vertex transfer. This is fairly easily spotted in Instruments because your draw call will have routines with IMM below them in the trace, and a lot of CPU time will be spent immediately copying your vertices. Accelerated draw calls themselves take almost no time to execute other than time to update GL state (which is also usually visible in Instruments).

hi.


ReplyDeletecould you please offer more details about how to check the indices of all gldrawelemnts calla?

I have also met this bug information. And really confused how to solve this.

Thx . :-)

The basic procedure to check an indexed draw call is:





ReplyDeleteScan the entire index buffer to find the lowest and highest indices in the draw call.

For each enabled vertex attribute (GL_VERTEX_ATTRIB_ARRAY_ENABLED):

- Get the attribute's bound VBO object (GL_VERTEX_ATTRIB_ARRAY_BUFFER_BINDING)

- Get that VBO's size (GL_BUFFER_SIZE)

- Get the attribute's stride, size (that is, component count), and type (GL_VERTEX_ATTRIB_ARRAY_SIZE, GL_VERTEX_ATTRIB_ARRAY_TYPE, GL_VERTEX_ATTRIB_ARRAY_STRIDE)

- Get the attribute's base ptr within the VBO (GL_VERTEX_ATTRIB_ARRAY_POINTER)

- Convert the GL type to a byte size, e.g. GL_UNSIGNED_INT = 4, GL_SHORT = 2, etc.

Now you can calculate the range of the buffer read for that attribute:

start within VBO = base ptr + stride * lowest idx in the draw

end within VBO = base ptr + stride * high index + attribute type's size * number of components.

If start > end or start < 0 or end > VBO size, you're out of bounds.

thx a lot. ~although i am a newer about OpenGL. I will try to check my code as you said later. thx! :-D

Deleteso, you mean that i do all of these instructions after each gldrawarrays is called, right?

Delete1. You must call these _before_ glDrawArrays/glDrawElements.

Delete2. For glDrawArrays, the range of indices is clear from the arguments; for glDrawElements you must get the element buffer (possibly by mapping the element VBO) and find the low/high indices. This case is a lot more important for debugging because junk indices are a common cause of 'going off the end' of your VBO.

One last note - we accomplish this with a global #define that remaps glDrawArrays and glDrawElements to our own call - this lets us (at the cost of speed) automatically run checking code before every draw call in debug mode.

DeleteHi how did you get sensible output mine is mangled is there a way to demangle it ?


ReplyDeleteThis is how it looks like:

libGPUSupportMercury.dylib`gpus_ReturnGuiltyForHardwareRestart:

0x35572904: movw r1, #0xbeef

0x35572908: movs r0, #0x1

0x3557290a: movt r1, #0xdead

0x3557290e: str r1, [r0]

0x35572910: bx lr

0x35572912: nop

Hi Benjamin,




ReplyDeleteI try to fix this kind of bug in my app for one year now - without any success and without any idea how to. So I am exited that your post could be a possible solution.

I googled a lot and started the implementation. I progressed a lot, but I am not sure if I'm doing the right thing (It is not possible to copy the code to the post because it is too long :( ).

Would it be possible for you to go over the code? Or could your share your code with me? This would be awesome!

Please get in contact with me settgleforge(at)unicorn-production.com