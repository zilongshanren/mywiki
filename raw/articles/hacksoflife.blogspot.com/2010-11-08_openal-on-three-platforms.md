---
title: OpenAL on Three Platforms
url: http://hacksoflife.blogspot.com/2010/11/openal-on-three-platforms.html
author: Benjamin Supnik
published: '2010-11-08'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[OpenAL](http://climpxwss01.creativelabs.com/openal/default.aspx)is a cross-platform 3-d sound API. It is not my favorite sound API, but it is cross-platform, which is pretty handy if you work on a cross-platform game. Keeping client code cross-platform with OpenAL is trivial (as long as you don't depend on particular vendor extensions) but actually getting an OpenAL runtime is a little bit trickier. This post describes a way to get OpenAL on three platforms without too much user hassle.

OS X

On OS X things are pretty easy: OpenAL ships with OS X as a framework dating back to, well, long enough that you don't have to worry about it. Link against the framework and go home happy.

Well, maybe you do have to worry. OpenAL started shipping with OS X with OS X 10.4. If you need to support 10.3.9, weak link against the framework and check an OpenAL symbol against null to handle a missing installation at run-time.

Linux

On Linux, OpenAL is typically in a shared object, e.g. libopenal.so. The problem is that the major version number of the .so changed from 0 to 1 when the reference implementation was replaced with OpenAL Soft. Since we were linking against libopenal.so.0, this broke X-Plane.

My first approach was to yell and complain in the general direction of the Linux community, but this didn't actually fix the problem. Instead, I wrote a wrapper around OpenAL, so that we could resolve function pointers from libraries opened with dlopen. Then I set X-Plane up to first try libopenal.so.1 and then libopenal.so.0.

(Why did the .so number change? The argument is that since the .0 version contained undocumented functions, technically the removal of those undocumented functions represents an ABI breakage. I don't quite buy this, as it punishes apps that follow the OpenAL spec to protect apps that didn't play by the rules. But again, my complaining has not changed the .so naming conventions.)

Windows

The Windows world is a bit more complicated because there are two separate things to consider:

- The implementation of OpenAL (e.g. who provided openal32.dll).
- The renderer (e.g. which code is actually producing audio).

OpenAL Soft makes things interesting: you can install OpenAL soft into your system folder and it becomes yet another renderer. Or you can use it instead of any of the Creative components and then you get OpenAL soft and no possible extra renderers.

Now there's one other issue: what if there is no OpenAL runtime on the user's machine? DirectSound is pretty widely available, but OpenAL is not.

Here we take advantage of our DLL wrapper from the Linux case above: we package OpenAL Soft with the app as a DLL (it's LGPL). We first try to open openal32.dll in the system folder (the official way), but if that fails, we fall back and open our own copy of LibOpenAL Soft. Now we have sound everywhere and hardware acceleration if it's available.

One final note: in order to safely support third party windows renderers like Rapture3D, we need to give the user a way to pick among multiple devices, rather than always opening the default device (which is standard practice on Mac/Linux). This can be done with some settings UI or some heuristic to pick renderers.

Regarding the Linux OpenAL ABI breakage, this is often the case when it comes to binary packages. But since most applications for GNU/Linux is source-based it won't introduce any problems for them unless the prototypes are changed in an incompatible way. So if the only breakage was to remove undocumented functions any (source-based) package conforming to the spec would not be affected. I see why you find it annoying with a binary package though, and you're not alone.




ReplyDeleteAnother "workaround" would be to build your code as a shared library with unresolved references, and provide source code to load this library and link it against external libraries like OpenAL. It could be as simple as

int main(){ return real_main();}

Then again, this will make it harder to distribute to end-users unless you provide distribution specific packages (.deb, .rpm, .ebuild etc)