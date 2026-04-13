---
title: Porting AnKi to Android
url: https://anki3d.org/porting-anki-to-android/
author: Panagiotis Christopoulos Charitos
published: '2014-01-06'
source_blog: AnKi 3D Engine Dev Blog
source_site: https://anki3d.org
category: graphics
fetched: '2026-04-13'
---

After months of careful planning, reading the GL specs and waiting for Google to add OpenGL ES 3.0 support, AnKi was finally ported to Android. This article presents the result and briefly expands on the challenges of porting a game engine to Android. More precisely, there is a video showing a demo running on an Android tablet, the second is a pre-build .apk of that demo that you can download and install to your Android device and the third is a few thoughts on Android development and mobile GPUs.

# Video

The video is showing a flyby demo running on a Samsung/Google Nexus 10 tablet equipped with Mali T604 GPU. Please note that the demo is a bit slower because of HDMI. The resolution is 720p, the FPS (without HDMI) ~17 and the lights are in the worst case ~10.


# Download the prebuild package

You can download the .apk [from this location](https://drive.google.com/file/d/0B5tJTlYMUW8SeG0wSVBlMEk3ZTA/edit?usp=sharing).

After downloading copy the .apk to your device (in sdcard). From your device navigate using a filemanager to where the .apk is located. Install it by using the filemanager (not sure if stock Android can install application without using a filemanager). Alternately, if you have the Android SDK installed you can push the .akp by typing:

adb install /path/to/AnKiBench-debug.apk

The requirements of the demo are:

- Android greater or equal to 4.3
- OpenGL ES 3.0 GPU

The demo has been tested on:

- Google Nexus 10 (Mali T604)
- Samsung Galaxy Note 2014 edition (Mali T628)

If something goes wrong and you want to report it please send me an email with the log file:

/sdcard/.anki/anki.log

# Thoughts on porting to mobile

The process of porting a game application to Android requires a few steps and a few leaps. If we try to present them the first is making the code build for the new platform, the second is adding the platform specific bits and pieces, the third is making sure that everything runs on the specific OpenGL ES version and the last is optimizing.

The first step is making AnKi **build for Android**. Unfortunately this is where things get ugly. Google’s decisions on the preferred way of writing applications are quite unreasonable in my opinion. The first foul move is that the official language is Java. I guess Java is fine for most things but when performance is important Java is a bad choice even if it’s used with a just-in-time compiler (maybe ART will fix that). Also, nobody wants to re-write their game in Java, after all 95% of games are written in C/C++. Fortunately Google added support for native application development with **Android NDK**. Nevertheless, building using the NDK requires Android specific makefiles (**Android.mk**) and this decision pretty much invalidates any existing build system. This is Google’s second foul move. After some complaining from developers, Google provided the means to invoke the compiler and be able to use it with any existing build system. For AnKi’s CMake based build system I just used **android-cmake** ([link](https://github.com/taka-no-me/android-cmake)) and to my surprise everything worked out quite well.

The second step is adding the **platform specific** bits and pieces for Android. These bits and pieces are code for window creation, EGL/GL context creation, input, window events, timers, file manipulation, threads and other. Fortunately Android is a Linux-based OS and most of the code required is already there for AnKi. But Android has it’s quirks once again. The first is that it implements a subset of the POSIX standard and Google’s cut down version of libc is also a subset of what we have on Linux. Because of that missing support I had to patch code including external libraries like LUA and Bullet. The second problem is that **Android C API is under-documented and limited** compared to what Google offers for Java. In the near future I will try using **SDL2** and replace the platform specific code with something that I don’t have to maintain.

The third step is moving from an nVidia desktop GL 3.3 implementation to an ARM GLES 3.0 one. Fortunately that didn’t prove to be a big challenge because GLES 3.0 spec was available for quite some time already and the time to read it, understand it and implement any required changes was enough. Also, the fact that Khronos kept GLES 3.0 close to desktop GL 3.3 is a plus. One point of frustration was the changes that were needed for the shaders. nVidia is known for their over-relaxed interpretation of the spec and that required a few alterations to make the shaders compile on a stricter compiler.

The last step is **optimizing for mobile GPUs with deferred rendering architecture** like Mali T6xx. There are a few nice articles out there on how to optimize for mobile GPUs and once someone understands how these architectures work, squeezing some FPS out of them becomes easy. Maybe the two most important notions that someone should keep in mind is “keep the bandwidth as low as possible” and “invalidate the framebuffers when makes sense”. One additional plus of mobile GPUs is that most of the vendors out there have profiling tools or compilers that work on Linux as well. That is a big plus at least for those of us who don’t like booting to a windows machine to profile. Also, one additional benefit that came after optimizing for mobile is that AnKi became faster on desktop as well. Trying to optimize for one architecture most of the times benefits the rest of the architectures as well.

# Footnote and future plans

Porting to Android has its difficulties but the fact that Android is so popular made it possible to have a workaround for every problem. At the same time Google should step their game up because writing native Android apps is at best “hackish”. The fact that it got me 1.5 months to complete porting AnKi (in a somewhat acceptable state) proves that the overall task can be quite easy for a big professional studio.

On the other hand AnKi always wanted to be cutting-edge and soon we will have to struggle to maintain a GLES 3 and a GL 4.4 codebase and that’s something I am not happy about. What will probably happen is that the GLES 3.0 path (and desktop GL 3.3) will be killed in favor of GL 4.4 until GLES adds support for compute shaders and separate programs.

That’s all for now. Enjoy codding!