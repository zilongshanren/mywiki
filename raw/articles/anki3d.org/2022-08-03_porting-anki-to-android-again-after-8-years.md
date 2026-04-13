---
title: Porting AnKi to Android… again after ~8 years
url: https://anki3d.org/porting-anki-to-android-again-after-8-years/
author: Panagiotis Christopoulos Charitos
published: '2022-08-03'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

I think it was 8 or 9 years ago when AnKi was first ported to Android for a demo competition and I remember the process being quite painful. Building native projects for Android was a hack, the micro differences between OpenGL ES and desktop OpenGL required compromises, GLSL related issues were a constant pain (compilation issues, bugs, shader reflection differences between implementations etc). These and more issues were the reason I left the Android port to rot and eventually remove from the codebase.

All that changed 10 months ago when I decided to re-port AnKi to Android. But if it was so painful why try again? The main reason is that the ecosystem had improved over the years. Android tooling for native code development (basically C/C++) got better but the biggest motivator was Vulkan. I was optimistic that there will be less issues with Vulkan this time around. At the end of the day was it less painful? The short answer is “yes” but if you want the long answer continue reading.

Disclaimer: This piece doesn’t express the opinion of past, current or future employers of the author. It doesn’t express the opinion of employers from parallel dimensions as well.

## Step 1: Make it build

The first step of porting to a new platform is to make things build. Doesn’t matter how many corners you will cut, just make everything compile to completion. Recent Android officially uses **Gradle** as its build system. Gradle is well supported and there are online examples on how to utilize it for native application development. Unlike **ndk-build** (or whatever it was called) which AnKi had to target 8 years ago, Gradle is a welcome improvement primarily because it interfaces with CMake natively. To get started I took some random Gradle NDK project with all of its directory structure and adapted it for AnKi. After a few fixes in AnKi’s CMakeLists.txt and after commenting out a bunch of code everything built to completion. Figuring out the directory structure of a Gradle project wasn’t the easiest thing in the world but there are quite a few open source projects out there if someone wants to draw inspiration.

[Android Studio](https://developer.android.com/studio) was used throughout the process in order to build and debug AnKi Android projects. Android Studio is something that didn’t exist 8 years ago. Debugging native code that was running on a phone or tablet was an almost impossible task back then. After setting a few breakpoints and firing up the debugger I started stepping through the code. While moving around I was adapting and adding back the commented-out functionality.

## Step 2: Platform code

The first thing I encountered while stepping through the code was some missing functionality in the filesystem. The resource filesystem would have to read files from inside the **APK** (APK is the native package format of Android applications) in addition to what’s possible on Linux and Windows. Fortunately AnKi had some dormant code from the first porting attempt so that step completed quickly.

Next stop was the window and input handling. AnKi uses SDL on Linux and Windows but for Android I decided to use native APIs. Trying to figure out how to make SDL build for Android (SDL is supposed to be working on Android as well) seemed more complicated than writing everything from scratch. After all Android’s window and input handling is much more simple than Linux and Windows so the effort was low.

The next big change was **Vulkan**. AnKi was using Vulkan 1.2 for quite some time already but Android is stuck on Vulkan 1.1. That required a downgrade which is not a huge deal really but more of an annoyance. While enabling the extensions (that were previously part of Vulkan 1.2) I realized that my Android device didn’t support integer 64bit types or 64bit atomics. Not a huge deal. I went and added a 32bit path on some shaders.

Moving through the code the next step was to start loading **ASTC** **textures**. AnKi has a texture format that can host multiple compressions into a single file. What I needed to do was to add support for ASTC in AnKi’s texture converter and also repack some of the asset textures of some samples/demos. That was quite straightforward and didn’t cause any headaches.

## Step 3: Fixing GPU errors on Vendor A

Up until this point AnKi can read files, initialize the Vulkan device and swapchain and there is no outstanding functionality missing. The next step was to let things run with **Vulkan validation** enabled and see what breaks. Vulkan validation works a little bit differently on Android and enabling it requires a different approach than Linux and Windows. In reality it’s pretty simple. Building the validation layers for Android will spit a few dynamic libraries for different architectures (.so files). The only thing left to do is to copy the appropriate .so to your Gradle project tree and re-build the APK. Enabling the Vulkan validation programmatically from C++ is the same as Linux and Windows. Easy. Vulkan validation found a few issues but nothing major. Some compute shaders had more than 512 threads than vendor A supported.

Next phase was to let things run until completion. Unfortunately I was getting a device lost from Vulkan. The problem with device losts on Android & Vulkan is that there is no good way to find the cause if it. Android logcat was showing a bizarre message but that wasn’t very helpful. The only solution is to start removing renderpasses until something worked. After removing everything except one simple renderpass the screen in my Android device turned magenta. Great! Something works. After removing and adding code I quickly found out that the culprit was the compute dispatch that was doing light binning in clusters. The next step was to comment out code inside that compute shader until something worked. I’ve reached a point where a barrier() was causing the shader to hang. After some search online I found out something that I wasn’t aware of. Apparently it’s not allowed for shaders to return if a barrier() follows that return. Apparently that pattern was in other compute shaders as well.

Fixing the barrier() issue made the device lost go away and that was pretty much it. I could see Sponza running on my phone. The first milestone was done.

## Step 4: Fixing GPU issues on Vendor B

A few months down the line a need arose to run AnKi on another mobile vendor. This process was done with the help of a colleague.

The first thing that happened when running on vendor B was an intermittent crash. Fortunately Android’s log printed a back-trace full of LLVM functions. So the problem must have been in vendor’s B shader compiler. The first assumption was that the compiler was allergic to some SPIR-V binary that was fed to it but because the issue was intermittent this theory was quickly rejected. The next thing to try was to add a mutex around every vkCreateGraphicsPipeline and voila the crashes disappeared. You see AnKi creates PSOs in multiple threads but that never caused any issues. A workaround had do be created for vendor B.

**Side note**: I see a lot of people bashing low level APIs (Vulkan and DX12) complaining about stuttering caused by PSO compilation. At the same time there are not many mobile games that compile PSOs from multiple threads (I’m only aware of a single game that compiles PSOs from multiple threads at load time). If multithreaded PSO compilation was a thing the crash mentioned above wouldn’t exist.

After the crash went away Sponza started showing up but it was rendering incorrectly. With some help from a colleague we found out that the indirect diffuse probes were having wrong values. After experimenting we found out that the compute shader that was doing the irradiance integration was not working correctly. I decided to re-write that shader using subgroup operations (aka wave operations in DX land) instead. Unfortunately the new subgroup powered compute shader also didn’t work correctly for vendor B but possibly for different reasons. At this point we gave up.

## Closing thoughts

One thing worth mentioning is that the initial porting process (be able to see Sponza on vendor A) took about a month but there were many improvements and optimizations since then. Also I haven’t mentioned anything about performance. Future improvements and performance deserves its own article and hopefully I’ll find some time to write it.

Anyway. Overall Android native code development has improved over the years. Gradle and Android Studio are a much needed improvement and Vulkan (ATM) is a more robust API especially for people who understand mobile hardware.

On the other hand, some things remained static and that’s a shame. It’s a constant source of frustration the fact that Android is still plagued by GPUs that never receive driver updates. The level of support on Android is unacceptable. The 2nd big issue is that Android’s native APIs (NDK) have stagnated and never really expanded. There is a lot of functionality that is absent from the NDK and the only way to be utilized by native applications is through Java hacks.

That’s it for now. For questions and comments feel free to reach out.