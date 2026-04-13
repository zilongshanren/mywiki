---
title: Building for OSX,iOS,tvOS & watchOS on Windows
url: https://www.jonolick.com/home/building-for-osxiostvos-watchos-on-windows
author: Aimee E link
published: '2018-01-08'
source_blog: Jon Olick - Home
source_site: https://www.jonolick.com/home
category: graphics
fetched: '2026-04-13'
---

|
Note: This is a work-in-progress and still being tested for possible distribution issues. I will update this blog post as the work progresses. Trying to simplify my life a bit over here, I am on a journey to eliminate my Mac from the build iteration cycle. The goal is to completely ship all binaries for both Bink and Oodle Lossless Image (OLI) directly from my PC rather than occasionally building on a mac only to find that Apple broke yet another thing in the latest OSX update or iSDK release (seriously, stop that!). First thing first, your gonna need a toolchain. I used the toolchain from
I also used MSys (via
To build for OSX, iOS, tvOS and watchOS you are going to need some sysroots from a real mac. You can find these and some frameworks you are going to need in each SDK release at the following paths
Next use clang to build for Apple by specifying some additional parameters. The first of which is your target specification.
Second, specify your framework directory. This is located in your {SDK}/System/Library/Frameworks directory, so would be specified as "-F{SDK}/System/Library/Frameworks" Third, you need to specify your sysroot as "--sysroot {SDK}". The sysroot tells the compiler where your headers and libs are. That's about it for building stuff (I think?). Just use as normal. To make a DMG file you need to do things a bit differently since there is no hdiutil on windows as it is closed-source apple tech. Instead of hdiutil, you use mkisofs (you can get that with mingw, or provided also right here... invocation would look something like
mkisofs -J -R -o {file}.dmg -mac-name -V "{title}" -apple -v -dir-mode 777 -file-mode 777 {dmg_directory} As for signing executables, I haven't yet had to worry about that... hoping I won't! I would point you to the pmbaty ios tools which has an executable signer in there. If I missed anything, or something is not clear or not working for you, please let me know in the comments below and I'll help if I can!
|
## Archives
## Categories |