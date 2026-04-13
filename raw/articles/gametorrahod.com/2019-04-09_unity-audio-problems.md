---
title: Unity Audio Problems
url: https://gametorrahod.com/unity-audio-problems/
author: Sirawat Pitaksarit
published: '2019-04-09'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

First of all a disclaimer, I am an author of [Native Audio](http://exceed7.com/native-audio/), a plugin used to skip Unity and use more native method to play audio on iOS and Android, without mixing, for minimum latency. I do not care about functions in this plugin.

This article is not for advertising it, yet related to it. In multiple years of maintaining this plugin, I have encountered and learned about so many problems and quirks both by myself and from bug reports from my users in the [Discord channel](https://discord.gg/8gthuWA).

Together with my users I have always been researching, and I think it would be better to keep it here together Q&A style here. It is easier to edit and collect for me.

## I want to learn really deep about Android native audio

Here you go! It's super long! [https://gametorrahod.com/android-native-audio-primer-for-unity-developers/](https://gametorrahod.com/android-native-audio-primer-for-unity-developers/)

## Android's audio latency on Unity `AudioSource`

is ridiculously bad, but the device is very new and other apps performs well

Unity initialize native resource with a certain "safe" settings based on certain threshold. Some newer devices unfortunately has something that went over the threshold and got the "safe" (but slow) native sources.

In 2019.1 this threshold has been relaxed, more devices will get a better native sources. Native Audio could do faster but for the best built-in `AudioSource`

latency the 2019.1 upgrade is important.

## I made a native plugin that plays audio on Android, but on some device "**each play**" lags badly

I have discovered that starting and stopping the native source will cause heavy lag on some devices with bad "audio policy". One of the device I have Xiaomi Mi A2 has this problem. (And many other Chinese phones apparently)

There is a hack in Native Audio that always keep playing **silence **on the idle native sources.

Unity's built-in audio also requested 1 native source and I could observe Unity is also doing this "hack" as well. (It is active even if I still haven't touch any `AudioSource`

)

So, I guess you might want to add this hack to your native plugin too.

## I made a native plugin that plays audio on Android, but ...

Here's more problems I think it is good to know if you want to do something native. It is a shortened version from [this super long article](https://gametorrahod.com/android-native-audio-primer-for-unity-developers/).


: There is a limit of about 1MB to use audio on this. So it is not suitable for music. Also it will automatically manages which [SoundPool](https://developer.android.com/reference/android/media/SoundPool)`AudioTrack`

to use which is a limited resource per devices. If you play 33 sounds simultaneously with `SoundPool`

it will likely fail as the device only got 32, sometimes prevented to as low as 15 for one app.

(Java)

: You are now using the (Java) [AudioTrack](https://developer.android.com/reference/android/media/AudioTrack)`AudioTrack`

directly, and so the same limit I said on `SoundPool`

section still applies.

OpenSL ES : This is what Native Audio uses. The same limit also applies because you are now dealing with (C++) `AudioTrack`

even more directly.

### Taking the Unity audio to native side : by file

The easy solution is to use `StreamingAssets`

so the file placed there could be read from native side. You have to be aware of OBB splitting though, as your file may not be in the path you are assuming it would be. Both Native Audio ( `StreamingAssets`

mode, NA could also loads from C# `AudioClip`

) and [Android Native Audio](https://www.assetstore.unity3d.com/#!/content/35295) handles the OBB splitting well.

### Taking the Unity audio to native side : by memory

How Native Audio could use `AudioClip`

for native operation is by using [AudioClip.GetData](https://docs.unity3d.com/ScriptReference/AudioClip.GetData.html). This is **a copy **filling your array with floating point PCM. Currently there is no way to use **the same **data as your `AudioClip`

, so you have to pay for this copy. Also this only works with "decompress on load" for Vorbis compressed in the import settings, since the data that came out on the array will be uncompressed PCM. It can't comes out as OGG byte array.

After this you could find a way to interop this array to native side. Maybe send it as an `IntPtr`

but be sure to pin it first just to be safe with [GCHandle.Alloc](https://docs.microsoft.com/en-us/dotnet/api/system.runtime.interopservices.gchandle.alloc?view=netframework-4.7.2) when you are interoping.

## On some devices Unity audio sounds spooky/scary/slow/stutter/glitched/cracking/squealing

Audio are so abstract it is difficult to express what you are hearing. But this is likely the sound of "buffer underrun". If you use `AudioSource`

and they sounds like that, likely Unity got the buffer size wrong for the device. (Too low) See more in the buffer underrun section.

## Best Latency, Good Latency, Best Performance

### What they affect?

It is related to how large the** audio buffer size** will be. Before v5.0.0 you used to be able to type in the buffer size number directly, but now I think because each platforms has different requirement Unity choose to rename them to something ambiguous.

### How to change the buffer size again programmatically

If you think Unity got the wrong buffer size, you can use [AudioSettings.Reset](https://docs.unity3d.com/ScriptReference/AudioSettings.Reset.html). Be careful about odd numbered size. I remembered while making Native Audio, when I use odd number as buffer size it sounds funny. (So you may +1 if it `%2 != 0`

)

### Effects on Android

I thought it would be depending on devices, but as far as I was reported, Best Latency = 256, Good Latency = 512, Best Performance = 1024 **regardless **of devices. This cause problems when some device couldn't handle 256 when you use Best Latency for the build.

### Windows build is always failing on Best Latency

The last time (2018) I tried, no matter what Windows machine I run the Unity game built with Best Latency it always get buffer underrun. So the only way is to use Good Latency or above.

## Audio buffer size and buffer underrun

You can think there is a small memory space to put some audio data on and the speaker will vibrate according to this memory area. If this memory area is small, then the cycle of putting data and using the data is short and therefore latency could be smaller.

However, this putting/reading data doesn't wait for each other. If it is **too **small, you will cause "buffer underrun". Since there is no data left to read when time comes, the game is now ahead of audio and it sounds like spooky glitched gameboy slowdown sound you may have heard from some Pokemon creepy pasta.

## Players are reporting that some phone's audio are glitching really bad

These phones apparently fails to deliver audio with the buffer size 256 and maybe even 512, so Best Latency and Good Latency build doesn't work and make `AudioSource`

play garbled audio.

Huawei Mate 20 / Mate 20X / Mate 20 Pro / P20 / P20 Pro / Honor View 20 and MeiZu phones are some of the phones I received that cause the problem. I am not sure about Lite version.

From some search it seems these are all the device codes :

** Mate 20X** : EVR-L29 (Global market); EVR-AL00, EVR-TL00 (China)

**: LYA-L09, LYA-L29 (Global market); LYA-AL00, LYA-AL10, LYA-TL00 (China, Hong Kong); LYA-L0C (Canada)**

**Mate 20 Pro****: HMA-L09, HMA-L29 (Global market); HMA-AL00, HMA-ТL00 (China)**

**Mate 20****: SNE-LX1, SNE-LX2, SNE-LX3, SNE-L21, SNE-AL00**

**Mate 20 Lite****: CLT-L09, CLT-L29 (Global), CLT-AL00, CLT-AL01, CLT-TL01 (China, Hong Kong) HUAWEI P20 Pro Leather Limited Edition CLT-AL00L (China)**

**P20 Pro****: EML-L09C, EML-L29C (Global); EML-AL00, EML-TL00 (China, Hong Kong)**

**P20****: ANE-LX1, ANE-LX2 (Global); ANE-LX3, ANE-LX2J (LATAM, South Africa, Brazil, Canada); ANE-AL00 (India, China, Hong Kong); ANE-TL00 (China, Hong Kong)**

**P20 Lite****: PCT-LX9, PCT-L29(edited)**

**Honor View 20**There are so many variations, I wonder if we could just check if the string starts with 3 capital letters then a dash then just discard the back part?

What's surprising is that my Native Audio plugin is using the "native size" that these devices told me, sometimes they are **as low as 240, and it works**. That means the Unity way of playing requires more buffer size than my simple native play.

For Unity `AudioSource`

fix, it is unfortunate that we couldn't "detect underrun" programmatically. You may try blacklisting those devices by checking

then do a [deviceModel](https://docs.unity3d.com/ScriptReference/SystemInfo-deviceModel.html)[Reset](https://docs.unity3d.com/ScriptReference/AudioSettings.Reset.html) to size like 1024. The latency will increase, but better than unplayable. An another way other than blacklisting is to add a slider to adjust buffer size in your option screen that leads to [Reset](https://docs.unity3d.com/ScriptReference/AudioSettings.Reset.html), and tell your player to increase it if it sounds strange/slow/scary.

An another solution is using Android's native `MediaPlayer`

. `MediaPlayer`

uses a "good" buffer size that is more guaranteed to work and also works with OGG compressed file. A plugin like [Android Native Audio](http://christophercreates.com/android-native-audio/) which is now free has "ANA Music" feature that could use `MediaPlayer`

. But to let native side read Unity data your audio must be placed in `StreamingAssets`

as per the [documentation](http://christophercreates.com/androidnativeaudio/Android%20Native%20Audio.pdf) says. It would be difficult to migrate from imported `AudioClip`

for some games.

Personally I think the best solution now is using Native Audio for important sound effects + UI sound effects, and buffer size fix hack for Unity long audio since I don't want to sacrifice `AudioClip`

import settings and Unity's mixer.