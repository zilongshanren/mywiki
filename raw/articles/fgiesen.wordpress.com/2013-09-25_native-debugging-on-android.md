---
title: Native debugging on Android
url: https://fgiesen.wordpress.com/2013/09/25/native-debugging-on-android/
published: '2013-09-25'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Native debugging on Android

Another Android post. As you can tell by the previous post, I’ve been doing some testing on Android lately, and before that came building, deploying, and testing/debugging. As part of the latter, I was trying to get `ndk-gdb`

to work, on which I spent about one and a half day full-time (without success), and then later about as much time waiting (and sometimes answering questions) when some Android devs on Twitter took pity on me and helped me figure the problem out. Since I found no mention of this issue in the usual places (Stack Overflow etc.), I’m writing it up here in case someone else runs into the same issues later.

### First problem: Android 4.3

The symptom here is that `ndk-gdb`

won’t be able to successfully start the target app at all, and dies pretty early with an error. “Package is unknown”, “data directory not found” or something similar. This is apparently something that got broken in the update to Android 4.3 – see [this issue](https://code.google.com/p/android/issues/detail?id=58373) in the Android bug tracker. If you run into this problem with Android 4.3 running on an “official” Google device (i.e. the Nexus-branded ones), it can be fixed by flashing the device to use the [Google-provided Factory Images](https://developers.google.com/android/nexus/images) with Android 4.3. If you’re not on a Nexus device – well, sucks to be you; there’s some other workarounds mentioned in the issue, and Google says that the problem will be fixed in a “future release”, but for now you’re out of luck.

### Second problem: “Waiting for Debugger” – NDK r9 vs. JDK 7

The second problem occurs a bit further down the line: `ndk-gdb`

actually manages to launch the app on the phone and gets into gdb, but the app then freezes showing a “Waiting for Debugger” screen and won’t continue no matter what you do. Note that there are lots of ways to get stuck at that screen, see Stack Overflow and the like; in particular, if you see that screen even when launching the app directly on the Android device (instead of starting it via `ndk-gdb --start`

or `ndk-gdb --launch`

on the host), this is a completely different problem and what I’m describing here doesn’t apply.

Anyway, this one took ages to figure out. After about two days (when I had managed to find the original problem I was trying to debug on a colleague’s machine, where `ndk-gdb`

worked), I realized that everything seemed to work fine on his machine, which had an older Android NDK, but did not work on two of my machines, which were both using NDK r9. So I went over the change log for r9 to check if there was anything related to `ndk-gdb`

, and indeed, there was this item:

- Updated ndk-gdb script so that the
`--start`

or`--launch`

actions now wait for the GNU Debug Server, so that it can more reliably hit breakpoints set early in the execution path (such as breakpoints in JNI code). ([Issue 41278](http://b.android.com/41278))

Note: This feature requires jdb and produces warning about pending breakpoints. Specify the

`--nowait`

option to restore previous behavior.

Aha! Finally, a clue. So I tried running my projects with `ndk-gdb --start --nowait`

, and indeed, that worked just fine (in retrospect, I should have searched for a way to disable the wait sooner, but hindsight is always 20/20). That was good enough for me, although it meant I didn’t get to enjoy the fix for the Android issue cited in the change log. This is annoying, but not hard to work around: just `sleep`

for a few seconds early in your JNI main function to give the debugger time to attach. I was still curious about what’s going on though, but I had absolutely no clue how to proceed from there – digging into it any further would’ve required knowledge of internals that I just didn’t have.

This is when an Android developer on Twitter offered to step in and see if he could figure it out for me; all I had to do was give him some debug logs. Fair enough! And today around noon, he hit paydirt.

Okay, so here’s the problem: as the change log entry notes, the “wait for debugger” is handled in the Java part of the app and goes through jdb (the Java debugger), whereas the native code side is handled by gdbserver and gdb. And the problem was on the Java side of the fence, which I really don’t know anything about. Anyway, I could attach jdb just fine (and run jdb commands successfully), but the wait dialog on the Android phone just wouldn’t go away no matter what I did. It turns out that the problem was caused by me using JDK 7, when Android only officially supports JDK 6. Everything else that I’ve tried worked fine, and none of the build (or other) Android SDK scripts complained about the version mismatch, but apparently on the Android side, things won’t work correctly if a JDK 7 version of jdb tries to connect. And while you’re at it, make sure you’re using a 32-bit JDK too, even if you’re on a 64-bit machine; I didn’t make that mistake, but apparently that one can cause problems too. After I switched to the 32-bit JDK6u38 from [here](https://jdk6.java.net/download.html) (the old Java JDK site, which unlike the new Oracle-hosted site won’t make you create an user account if you want to download old versions) things started working: I can now use `ndk-gdb`

just fine, and it properly waits for the debugger to attach so I can set breakpoints as early as I like without resorting to the `sleep`

hack.

### Summary (aka TL;DR)

Use Android 4.2 or older, or flash to the “factory image” if you want native debugging to even start.

If you’re using the NDK r9, make sure you’re using a 32-bit JDK 6 (not 7) or you might get stuck at the “Waiting for Debugger” prompt indefinitely.

Thanks to Branimir Karadžić for pointing out the first issue to me (if I hadn’t known that it was a general Android 4.3 thing, I would’ve wasted a lot of time on this), and huge thanks to Justin Webb for figuring out the second one!

*Well done, Android. The Enrichment Center once again reminds you that Android Hell is a real place where you will be sent at the first sign of defiance.*

That sounds miserable, guess they don’t care much about native. I haven’t done anything with android yet, but will probably do so in the future so I’ll keep this in mind.. thanks.

Shouldn’t that say “flashing the device to use… with Android 4.2”? I got confused until the summary.

Not sure it is still relevant, but you can also use a JDWP client like jdb to let the app actually run.

See https://source.android.com/devices/tech/debug/gdb