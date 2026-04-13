---
title: Android Native Audio Primer for Unity Developers
url: https://gametorrahod.com/android-native-audio-primer-for-unity-developers/
author: Sirawat Pitaksarit
published: '2018-07-05'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

I will demystify the “black box” surrounding the Android audio system and analyze why Unity’s way of using it makes your audio latency even higher than the already awful Android latency.

Actually a supplementary documentation for the plugin [Native Audio](http://exceed7.com/native-audio/) which skips all Unity’s audio system for the best latency, but it should also be useful for anyone who want to know more about the mystery of Android’s audio.

(Also I hate manually editing HTML for long article with proper code tags and uploading images is a chore so I choose to put it here instead.)

Be prepared for an hour-long audio lesson! Android is really complicated!

## Why skip Unity’s audio? What is the point of Native Audio?

Latency! It is quite critical in some kind of games. If you have time you can read all of the reason from this front page :

**Native Audio - Lower audio latency via OS's native audio library.***Native Audio is a plugin that helps you easily loads and plays an audio using each platform's fastest native method…*exceed7.com

### What is Unity doing

- On application start, Unity request 1 "native source" from Android device. This native source is configured based on unknown algorithm that sometimes results in a slow source.
- On
`AudioSource.Play`

in C# code, it will**wait**and collects all these kind of commands until the end of frame. - When at the end of frame, Unity will calculate based on fall off, mixer, effects, etc. then finally mix them together.
- That one native source get the mixed audio bytes. You get virtually unlimited concurrent audio.
- Imagine you do 3
`AudioSource.Play`

in a different`Update`

. They will sound exactly at the same time after passing through latency.

### What is Native Audio doing (briefly)

- On application start, NA allocates several "native source" with settings geared toward low latency. Also preload audio bytes waiting.
- On
`NativeAudioPointer.Play`

, one of the native sourcce is seleted to play at specified audio bytes memory area immediately, right at that C# line without waiting for the end of frame, and without mixing or effects. It even works from threads. - One source is exclusively for one preloaded audio. This is the "
**no mix**" policy. - "Native source" is a limited resource per device, NA only allocates 3 by default and that means only 3 concurrent audio maximum until you have to cut off old sounds.
- Imagine you do 3
`AudioSource.Play`

in a different`Update`

. They will sound at**slightly different**time depending on which one comes first, since native plugin doesn't wait for frame.

You will learn about "native source" later how to get the fast one and various experiments like, what happen if we request too many.

## Ways of playing native audio in Android from Unity

We will start from learning why my plugin Native Audio choose **OpenSL ES** as the implementation in Android side.

Note : When I say “faster than Unity” from this point on, that is compared with Unity + the setting “Best Latency” (plays the fastest possible) in Audio Settings. (It minimize the buffer size, but we don’t know how small it is or could it be smaller). This is opposite of “Best Performance” with BIG buffer to ensure the audio does not drop out but the latency will go to hell with that setting.

### AndroidJavaClass / AndroidJavaObject / AndroidJavaProxy / AndroidJNI / AndroidJNIHelper

They are not directly related to audio, but with these helper classes, you are able to use Java stuff from C# without writing a single Java code. This open up a way to access `MediaPlayer`

, `SoundPool`

, and (Java) `AudioTrack`

from Unity. Which you will get to know them next.

### SoundPool

**SoundPool | Android Developers***A SoundPool is a collection of samples that can be loaded into memory from a resource inside the APK or from a file in…*developer.android.com

[I have confirmed](http://exceed7.com/mobile-native-audio/research.html#results) that [SoundPool](https://developer.android.com/reference/android/media/SoundPool.html) is slower than (Java) `AudioTrack`

.

The definition of `SoundPool`

is so that you don't have to worry about underlying "native source" but rather a pool of sounds you want to use. One from many native sources will be selected and maintained automatically, instantiated more if not enough. Those native source are sometimes referrred as "stream".

For example you play 3 different sounds quickly while having 2 sources, it will allocate you a new one. If you wait a bit and play the 4th sound and some earlier sound ended, `SoundPool`

knows which one to reuse. You can fine tune this by giving "[priority](https://developer.android.com/reference/android/media/SoundPool#setPriority(int,%20int))" weight to each native source (stream) as well.

It is ideal for example entering a level and you load all the possible sounds in that level to one pool. With (Java) `AudioTrack`

if you want to do the same you will have to command the push and pull of audio data manually to change sounds.

![](../../assets/784ac7a54199609c.jpg)

If you need `SoundPool`

-based solution for Unity, a plugin [ Android Native Audio by CHRISTOPHER CREATES](https://assetstore.unity.com/packages/tools/audio/android-native-audio-35295) is the choice (now free!). That means a plethora of functions that Native Audio cannot do like setting play rate.

This ANA plugin is based on various Java helper classes in Unity mentioned earlier, which helps you do C# -> Java talk without actually using any Java. Should you need to hack it to add or access other methods on `SoundPool`

, you won't have to write any native code or go compile a new .AAR package in Android Studio or something.

`SoundPool`

's limitation is concurrency and total size of **each** audio [https://stackoverflow.com/questions/18170517/android-soundpool-limit](https://stackoverflow.com/questions/18170517/android-soundpool-limit) . It is not suitable for music.

On the reason why Native Audio (OpenSL ES) is much more limited, setting sampling rate in terms of OpenSL ES means destroying the source and create a new ones with different rate which we absolutely cannot do for latency critical audio playing, while for `SoundPool`

it is already there for you and it just works. I don’t know what it is doing underneath... Moreover for OpenSL ES, just by having the set rate feature enabled and even not using it yet disqualify you from obtaining the fast audio mixer.

And remember even if OpenSL ES has less latency, `SoundPool`

is still much superior to Unity’s mixing latency. So if you also want utility plus still less latency, try it.

Note : `SoundPool`

is actually able to use **fast flag** like OpenSL ES , the underlying solution of Native Audio. See :

**Design For Reduced Latency | Android Open Source Project***The fast mixer runs periodically, with a recommended period of two to three milliseconds (ms), or a slightly higher…*source.android.com

Later on, when you learned about native `AudioTrack`

and how Native Audio do it, we will come back to `SoundPool`

vs Native Audio again, because in essence Native Audio is trying to reinvent the wheel of `SoundPool`

but with settings geared for the lowest latency + sacrificing functions.

### MediaPlayer

![](../../assets/8e0eb1824fb57535.gif)

**MediaPlayer | Android Developers***Playback control of audio/video files and streams is managed as a state machine. The following diagram shows the life…*developer.android.com

A very multimedia-ish player class for audio and video available in Java with sophisticated state machine. Just from this definition it is not for minimizing latency. (Sure enough I have tested and the latency was pretty bad)

If you need `MediaPlayer`

-based solution, ** Android Native Audio **mentioned above has

**“ANA Music”**feature.

**ANA Music is also based on doing Java helper call to get you a**

`MediaPlayer`

from Java, and you have the priviledge of using OGG compression on your audio file.Native Audio could also use OGG now, but it will need to be decompressed completely to PCM data. (That is, decompressed to sized as big as WAV file.) But `MediaPlayer`

could play the compressed file as-is.

Also I know one case where in some Android device/version that `SoundPool`

lags on play but `MediaPlayer`

does not (explained later in “AudioPolicyManager” part), so I guess you can also use `MediaPlayer`

to play sound effects even if the usage suggests to play music.

### OpenAL

**OpenAL: Cross Platform 3D Audio***OpenAL is a cross-platform 3D audio API appropriate for use with gaming applications and many other types of audio…*www.openal.org

Native Audio maps to OpenAL in the iOS’s native side since I have confirmed it to be the best latency-wise there. I have no idea how OpenAL interfaces to iOS, but it is doing a good work.

From the name you might think OpenAL is cross platform, why not use OpenAL in Android also when we have confirmed it is the best in iOS?

- In iOS I use it because while it is not by Apple, Apple include it in Xcode
**by default**for use. - In Android the default open standard is OpenSL ES, which translate to (C++)
`AudioTrack`

. To use OpenAL I would have to find an implementation that some one made which likely maps to (C++)`AudioTrack`

anyways. - I would like to stay pure and official rather than being able to reuse the code from iOS part.

So I did not choose OpenAL.

### (Java) AudioTrack

**AudioTrack | Android Developers***Upon creation, an AudioTrack object initializes its associated audio buffer. The size of this buffer, specified during…*developer.android.com

We are finally at the lowest level of audio solution in (Java) Android, `AudioTrack`

!

This topic is `AudioTrack`

as in the class name of Java. Android has an another (C++) “AudioTrack” [defined at hardware level](https://source.android.com/devices/audio/terminology) which this (Java) `AudioTrack`

class interface to. OpenSL ES also interface to that (C++) “AudioTrack” low-level (it's C++ to C++).

The reason of the same name is that one Java instance of `AudioTrack`

really corresponds to one (C++) `AudioTrack`

at native side **one to one**. As opposed to one `SoundPool`

which governs multiple native (C++) `AudioTrack`

s. When you `new`

the (Java) `AudioTrack`

, you are really working with (C++) `AudioTrack`

via Java.

![](../../assets/0d9308e24e0dfaa2.png)

How this class works is that you **have to push audio data** into the track’s buffer and it will push the content out to your speaker. Very few utilities unlike `SoundPool`

but from my very first experiment, I have confirmed that it is the fastest and almost equal in latency to OpenSL ES. So why am I not using this Java ones but the OpenSL ES wrapper instead?

`AudioTrack`

is a class in Java. Remember that we are not making an Android native game but must issue commands from Unity. In Unity we have to use[AndroidJavaClass](https://docs.unity3d.com/ScriptReference/AndroidJavaClass.html)to talk with Java which might be costly.- If we use OpenSL ES which is in C language code (can talk to Java via JNI also), Unity can talk to it directly via
`extern`

(similar to how iOS plugin works with Unity) which could be very good for reducing latency. - There’s this thing very important called FAST TRACK audio which just from the name obviously we will try to get at all costs. There are many conditions we must met (I will talk about them for sure) and to meet all those conditions in Java, look at this image it is
**HELL**.

![](../../assets/71aa1b66164b2830.png)

In Android they have change, add, and remove API on almost every new version. Unfortunately it’s audio library is also one of the changes.

In Unity, the lowest selectable is still Jelly Bean (API level 16) while the latest one is Oreo (API level 26). I want to support all the way down to what’s selectable in Unity.

However this results in a compile time error if you try to use anything that is not available in Jelly Bean, unless you put it in an if ( `Build.VERSION.SDK_INT`

>= ....) At the same time, newer API seems to have settings that can potentially improves latency that we can't ignore.

Instead of using the least common possible setting I have go to great lengths to make sure my players get the most updated API as possible. For example with Nougat but not Oreo, you get `AudioAttributes.FLAG_LOW_LATENCY`

in your `AudioAttributes`

. With Oreo or newer, you instead get `AudioTrack.PERFORMANCE_MODE_LOW_LATENCY`

in your `AudioTrack`

.

…all of that is actually in my Native Audio plugin version 1.0 where I used (Java) `AudioTrack`

. Since v2.0.0 Native Audio is now pure OpenSL ES.

### OpenSL ES

OpenSL ES will in turn making us "native track" (C++) `AudioTrack`

for us much like what (Java) `AudioTrack`

did.

And one more reason, look at this page :

**High-Performance Audio | Android NDK | Android Developers***High performance audio apps typically require more functionality than the simple ability to play or record sound. They…*developer.android.com

Only 2 options (and there is no (Java) `AudioTrack`

) officially recommended here is **OpenSL ES** and AAudio. So we are in a good company!

However with OpenSL ES in C language, you can't use those Java helper class from C# to work on it. Native Audio comes with precompiled .AAR package. Inside this package is a mix of Java and OpenSL ES C code. We can no longer work entirely from C# unlike [Android Native Audio](https://assetstore.unity.com/packages/tools/audio/android-native-audio-35295) plugin.

### AAudio

**AAudio | Android NDK | Android Developers***AAudio is a new Android C API introduced in the Android O release. It is designed for high-performance audio…*developer.android.com

[Newly introduced in Android Oreo](https://developer.android.com/ndk/guides/audio/aaudio/aaudio), this is very interesting as it is Google’s answer to OpenSL ES by making it a new (closed) standard fitted for Android only rather than open.

But! Not a lot of players right now would be able to use this until Oreo is old enough, but I am looking forward to assessing its performance and add it along with the old OpenSL ES approach that works pre-Oreo.

Look at this page :

**AAudio and MMAP | Android Open Source Project***AAudio is an audio API introduced in the Android 8.0 release. The Android 8.1 release has enhancements to reduce…*source.android.com

It is really exciting that AAudio can put the data very close to the audio driver! It says in EXCLUSIVE mode we actually use the same memory area with the driver itself. So imagine all the goodness! All the fun music games you can make! I will do a research comparing AAudio with OpenSL ES for sure when I can afford a new phone with Oreo 8.1 or higher.

It is also in C language similar to OpenSL ES so also you can fast-talk with it from Unity without going to Java. Now that I got OpenSL ES working and recovered my pointer arithmetic knowledge, I am quite confident to try putting in AAudio next so if the player has Oreo or higher he would get the goodness… but for now let’s dive deeper into OpenSL ES + (C++) `AudioTrack`

.

### Oboe

![](../../assets/33edc4cf4be61d84.jpg)

This aims to fix the headache I said earlier. "Automatically use AAudio when the Android phone is able to, otherwise use OpenSL ES". It is maintained by Google! I better migrate my own plugin to this one but migrating various hacks I put in might take time.

There is an Oboe implementation usable from Unity too, with this Asset Store item : Oboe for Unity ([https://assetstore.unity.com/packages/tools/audio/oboe-for-unity-134705](https://assetstore.unity.com/packages/tools/audio/oboe-for-unity-134705)) He even mentions my own plugins in the description!

Oboe still needs PCM uncompressed data (16-bit or floating point).

### Superpowered

![](../../assets/01042ae21e682f2f.png)

**iOS, OSX and Android Audio SDK, Low Latency, Cross Platform, Free.**[iOS, OSX and Android Audio SDK, Low Latency, Cross Platform, Free.superpowered.com](http://superpowered.com/)

Everyone searching for how to eliminate latency on Android might have came across this website, which provides plenty of audio latency knowledge in Android. The first thing catching your eye is probably their “<10ms SOLVED”. And sure enough you want it in your game!

The license is either contact for pricing, or splash screen + <500,000 downloads + publicly available game.

It might not be very obvious after reading their website’s wording, but in short, this solution requires a custom “Media Server” that works with (free) Superpowered API.

Of course, our player’s Android device is not going to have those custom modification so it is not possible to go this route. They are using the “10ms” to advertise Superpowered as a whole but to beat this 10ms we need a special install on the device. (It cannot come together automatically with a game from Play Store)

**Android 10 ms Problem? SOLVED.***In a series of extremely popular articles we explained Android’s audio architecture problems, preventing entire…*superpowered.com

And so if you are making something like local tech demo running on your Android tablet for one-day presentation and need fast audio, this is in fact the perfect solution because you can root and do anything to your own device as you like!

The media server speeds up the Android service space unaccessible before, but for user space/application space, higher latency than 10ms but still faster than Unity using only their API is still possible. It contains convenient audio functions while maintaining good latency, but how does it compare to other solution without the media server?

![](../../assets/5c703693fc8d8190.png)

Faster than OpenSL ES? How can that be if OpenSL ES is the final gate of audio on Android?

From

**What Developers Can and Cannot Do to Lower Android Audio Latency for Android’s 10ms Problem***To best understand the origins (and fixes) of Android audio latency, it is best to segregate contributions to total…*superpowered.com

![](../../assets/db4e2ebc965e841d.png)

Ok, now it is clear. The keyword is **audio processing **is faster than using the one from OpenSL ES (which contains various audio processor “wrapper” over something else on Android) But for **audio I/O **we cannot avoid OpenSL ES on Android and that’s the same for Superpowered.

So if you are planning to **process **(like effects, mixing, resampling, etc.) **before playing with OpenSL ES** then Superpowered is your possible solution, plus it is cross platform. Their processing engine is entirely their own. There are so many of their features that is in the hard “blacklist” (the variable is named like this in the Android source code!) and will force disable fast audio on OpenSL ES Android.

![](../../assets/182febbb48b6a88c.png)

But because they process audio by their own program it does not subject to this blacklist. Now it is up to you to test their claim if their processing time is good enough for you or not. Also I have no information about their true license pricing without the 3 restrictions.

In Native Audio such features that impairs latency are not of my interest and are not included in the first place. Native Audio cannot and will not process anything on play (actually it can pre-resample but that is not on every play), it just use OpenSL ES as an I/O for Unity audio. So with this understanding, Superpowered cannot be faster than Native Audio on audio playing.

![](../../assets/838c1368ef7ee3a7.png)

We are in agreement here. And Native Audio will do just what this 10. says.

I still highly recommended reading through their website to understand about audio path in Android. There are cool stuff like what changed from 5.0 to 6.0, why AAudio is actually make the latency worse in 8.0 and riddled with stereo bugs, etc.

### SAPA : Samsung Professional Audio API

Whoops, I completely forgot about this one. It only works on Samsung device and was announced in 2013. It is actually interesting even though it works only on subset of all Androids in the world, since Samsung dominates the Android market! Look!

**The most popular Android smartphones - 2018***Here are the most popular Android smartphones from across the globe, based on Q2 2018 data from our network of partner…*deviceatlas.com

So should I code SAPA and have Samsung players have it? Unfortunately supporting that is a hell lot of work. This article by Superpowered says it all.

**Why Samsung Professional Audio SDK is not the best solution for low latency Android audio***As of this writing, Android's audio latency is still not at parity with iOS. Samsung has made valiant efforts in…*superpowered.com

When the article said “Believe me, most developers run screaming away from JNI + OpenSL ES. And the Samsung Professional Audio SDK increases app development complexity by an order of magnitude.” it is true! I managed to not run screaming away from OpenSL ES but this SAPA made me give up. Also the article mentions a lack of SAPA audio input, but not a problem for Native Audio which only wants the fastest output.

And even Superpowered who initially managed to support SAPA have already gave up, search for “SAPA is dead” in this article.

**Android Audio Latency Problem Just Got Worse***Oh no, Android 8.0, say it ain't so! Being the bearer of bad news isn't pleasant -- but with Android 8.0, Android's 10…*superpowered.com

But hold on, from my own benchmark using SAPA **is better that the best I could do from Unity. **(That is using my own Native Audio plugin) The sound was recorded from my best attempt at reducing latency from Unity vs. Samsung’s own Soundcamp app which uses SAPA.

**Soundcamp | Apps | Samsung***Get this top-notch music-making app for your Galaxy smartphone. Soundcamp is the ultimate recording studio on your…*www.samsung.com

SAPA could do better for about 10–20ms from my best effort from Unity!

![](../../assets/841575c6e62972d7.png)

How? Apparently SAPA knows the device and it skips Android’s media server. Much like a custom media server way Superpowered used for their sub 10ms latency. Superpowered requires custom modification but works on all devices, while SAPA that custom modification is the Samsung device itself that can talk with SAPA API. Interesting difference.

Now the question is :

- Is that 20ms the other (?) overhead from Unity? Can a native Android app with OpenSL ES + all the best practices beats SAPA?
- Can I use SAPA from Unity and get the same latency as Samsung’s Soundcamp?
- Can I detect cleanly which device can use SAPA from Unity and switch accordingly?
- My best effort uses OpenSL ES. How about AAudio vs SAPA? If it is similar then there is no reason to go for Samsung-specific SAPA and just implement AAudio.

And so, SAPA support for Native Audio requires much more investigation. It is even not in the update plan I put on in the website, but I will definitely keep it in mind. I will continue about this some time in the future but definitely not before AAudio support.

The latest SDK update from Samsung is May 2018 for Android Oreo support, indicating that it is not necessary abandoned. In fact I hope it is maintained and Unity utilize them in the future. (Now that Unity is already collaborating with Samsung on the [Adaptive Performance](https://blogs.unity3d.com/2019/04/01/higher-fidelity-and-smoother-frame-rates-with-adaptive-performance/) feature.. why not audio too?)

### Criware adx2

![](../../assets/67fc2a9ffdc4108c.png)

Along with FMOD and wwise there is this Criware from Japan. It is quite popular there! What I really liked is that they are so upfront specifically about "Android audio problem" and address this directly in various place of their API. It has various licensing scheme, including "free until you profit". [Take a look here](https://www.criware.com/en/licensing/index.html). The Unity plugin costs 99$, see more [here](https://unityplugin.crimiddleware.com). (You still need to pay licensing fee)

Typical for audio middleware, you will be able to author and program your audio in a separated program. You can program repeated, randomize, intro-looping, combo, ambient, etc. easily. Criware will also skip Unity when used with Unity plugin and manage OpenSL ES operation for you. But unlike Native Audio, you get tons of features from the authoring program.

What's in our interest is that **specifically for Android** they have several specific settings.

![](../../assets/a65596e0e669a3b3.png)

If you check the box, you are using what they called "NSR" (Native `SoundRenderer`

) and judging from this slide [https://www.slideshare.net/GTMF/gtmf-2015-cri](https://www.slideshare.net/GTMF/gtmf-2015-cri)

![](../../assets/9fa973238e6fdbb0.png)

NSR is using "1 native source per 1 sound" direct output just like what Native Audio is doing. In a way it is reassuring that if a big company is also doing this, Native Audio seems to be on the right track : P

I haven't use adx2 extensively myself, but I guess you may want to try it. If NSR mode is what I think it is, then it is 100% better than Native Audio since NA is a subset, just the NSR mode of adx2. But adx2 got so much more.

## Fast track problem

Ok we are back on the main track. So how do we enable this special audio path of native (C++) `AudioTrack`

which OpenSL ES will create? (I will type `AudioTrack`

without C++ to mean "native track" from now on, since we ditched the Java ones.)

First the definition from [terminology page](https://source.android.com/devices/audio/terminology) : “ `AudioTrack`

or `AudioRecord`

client with lower latency but fewer features on some devices and routes.”

### The flag

Let’s look back a bit when I was using `AudioTrack`

from Java. The first (easy) requirement is that we tell AudioTrack the flag `AUDIO_OUTPUT_FLAG_FAST`

. And still choosing the right flag is not that easy because it change places depending on API version. (Look at the HELL image earlier you can see multiple variant of the flag)

And here’s what I get :

`04-13 10:06:43.977 31827 31841 AudioTrack W AUDIO_OUTPUT_FLAG_FAST denied by client; transfer 4, track 44100 Hz, output 48000 Hz`


The flag was denied by client? The `logcat`

says that I created an audio track of 44100Hz but the device’s **native sampling rate **is 48000Hz thus denied the fast track.

The first requirement is we must have a **matching sampling rate** to the phone's native rate to enable the fast track. First of all for those who is wondering what exactly is a sampling rate…

(And in OpenSL ES we don’t have this stupid flag… just a matching sampling rate automatically enables the fast track!)

### Sampling rate primer

Each audio sample is how the membrane of your speaker should vibrate and it make your ear’s membrane vibrate in the same way, so create the “hearing”.

Sampling rate is how often the file capture these vibrations. In the real world our ear vibrates in an infinite resolution but that would not be friendly for sound storage. We choose only some snapshot overtime and turns out that is enough to recreate the original waveform.

See also [Nyquist–Shannon sampling theorem](https://en.wikipedia.org/wiki/Nyquist%E2%80%93Shannon_sampling_theorem) which states how much is enough to recreate the perfect waveform.

### The use of sampling rate for audio players

Then! Why would we need to tell sampling rate to an audio player like `AudioTrack`

?

It is the speed of its play head that would go well with an audio sampled at that rate. Imagine I have an audio file sampled at 44100Hz but my `AudioTrack`

says it is going to move the head quite fast suitable for 48000Hz sampled audio.

(If you are still confused, in 1 second it is going to consume 48000 samples. Does it sounds like the head moves faster than consuming 44100 samples in 1 second?)

Playing 44100Hz audio with 48000Hz AudioTrack would speed up the sound (pitch chipmunked) of what I recorded because the head used up the data too soon. It would be perfect if I have more data packed. (i.e. recorded at 48000Hz)

### Can’t the rate of audio player dynamically change to whatever the audio is coming in?

Unfortunately it is not that simple as doing that is equal to destroying and recreating it. Creating an `AudioTrack`

is quite involved and Android must reserve many things such as memory, threads, etc. for us. Recreating the `AudioTrack`

every time a foreign rate comes in would not be a good idea for latency.

### So it is only a matter of pairing the correct audio with the correct rate. What’s the deal with “device’s native sampling rate”?

If I say I **will** always hand in 44100Hz files in an entire game and hard code 44100Hz AudioTrack all is well right?

Yes the output sound would be correct and not chipmunked, but the device itself **wants **to work on audio in a specific interval. My Xperia Z5 says 48000Hz but my Nexus 5 says 44100Hz.

This is the condition of fast track, you MUST have the `AudioTrack`

at the same rate as what the device would like to work on. (Maybe it depends on the crystal clock on the circuit? I don’t know.)

For the purpose of this plugin we absolutely don’t want to miss this. And so we will always make the player at the phone’s rate. How to know the phone’s rate?

### Asking for device’s audio preferences

Unfortunately you must consult Java for this. So even if we use C language OpenSL ES we would have to have some part in Java. Native Audio already do this by having the `NativeAudio.Initialize()`

ask for these information in Java, then the most important `Play`

method only need to talk to C language because the appropriate track is already created.

![](../../assets/863c863a2ca58b80.png)

Let’s see the `adb logcat`

of that on my Xperia Z5

![](../../assets/0aa1f160ec12b98a.jpeg)

![](../../assets/cd164cc43ba06a1a.png)

How about on my another crap-phone? (~35$ Lenovo A1000 or something)

![](../../assets/0394d3fd9a5d34e4.jpeg)

![](../../assets/1ba4e8e608849f08.png)

This log is of course not turned on in the real Native Audio. But something interesting here :

- Higher-end phones would likely use 48000Hz rather than 44100Hz and even more device in the future might use 48000Hz. (But there is no guarantee that there will be no other rates than these two)
- My crap phone actually has larger “optimal buffer size” at 640 vs 192 (will talk about it soon) the buffer size is actually the smaller the better, as it means only few data and it is ready to play. (= taking less time) But too small you may get buffer underrun problem where it could not pour out enough audio in time.
- LOW LATENCY FEATURE and PRO AUDIO FEATURE flag is not related to whether we can get fast track or not, but can tell about overall audio greatness of the phone. (See
[here](https://source.android.com/compatibility/android-cdd#5_6_audio_latency)and[here](https://source.android.com/compatibility/android-cdd#5_10_professional_audio)) Interesting to know but no use. *EDIT :[https://forum.unity.com/threads/android-sound-problem.359341/page-3#post-3638170](https://forum.unity.com/threads/android-sound-problem.359341/page-3#post-3638170)I got corrected from Unity team, it do have a use. The LOW LATENCY FEATURE flag is supposed to guarantee fast mixer track support.

We can finally match the audio player rate to the device whether it is `AudioTrack`

or OpenSL ES. Do we 100% have fast track now?

`04-13 11:41:49.161 6318 6332 AudioTrack W AUDIO_OUTPUT_FLAG_FAST denied by server; frameCount 144000`


Previously denied by client, this time **denied by server**! What is the reason of this? Maybe you are using non-fast feature such as audio send, reverb effects, pitch shifting, etc. Or the device simply cannot do fast track?

With (Java) `AudioTrack`

I was rejected by that reason numerous time before but with OpenSL ES somehow the more concise settings there often enable the fast track just fine!

The reason for this rejection is sampling rate of the **audio. **Just the native source matching phone's rate isn't enough.

### The (re) Sampling Paradise

We don’t know what device the player will use so we cannot pre-made the audio file to fit. One other way is to include **both** 44100 and 48000 version of every audio! But of course it is inconvenient, take more than double space, and there is no guarantee that other device with preferred rate 96000Hz will not appear.

So one other way is to **resampling** on the fly! What is resampling? It is to convert one rate to another. Imagine to make 44100Hz audio into 48000Hz what would you fill the empty data?

What empty data? For example let’s play this number game. I have this sequence 1 3 4 17 but a new sampling rate expands the data into 1 _ 3 _ 4 _ 17 what would you fill in the blank? (This new rate by the way have the **ratio **of 7/4 = 1.75)

The answer is not so trivial. You might just put 1 **1** 3 **3** 4 **4** 17, (the “zero order hold” method) you might put 1 **2** 3 **3.5** 4 **10.5** 17 (the “linear interpolation” method) or maybe more sophisticated method like fitting a sinc wave to make a nice fill-up.

If you are interested in learning more about audio resampling, I recommend this paper!

**Digital Audio Resampling Home Page**[Digital Audio Resampling Home Pageccrma.stanford.edu](https://ccrma.stanford.edu/~jos/resample/)

To make 44100Hz to 48000Hz that would be an **upsampling **of x1.08843 ratio. As you can see, making up non-existence data is not easy. Consider also **downsampling** if we use 48000Hz audio but encounters 44100Hz device thus 44100Hz AudioTrack. Will you just discard some samples? Or will you “sand” the data around it to smooth them up?

Anyways, I decided this would be the best way if we want fast track and want to include only one copy of each audio. The trade off would be more load time, because you are creating a new audio on load instead of just putting the audio data in when you see a mismatch.

To fight this you might predict that more of your players are using 48000Hz phone and include 48000Hz file by default so they don’t have to spend time resampling. Making the player with 44100Hz phone spend time resampling instead.

Android has some built-in resampler, but it cannot be used manually on any audio. It resample automatically when the sample rate does not match, which results in more latency. What we want is to **not **trigger these resamplers.

**Sample Rate Conversion | Android Open Source Project***The ideal resampler would exactly preserve the source signal's amplitude and frequency bandwidth (subject to…*source.android.com

### Detailed approach of how to resample an audio data

What method to use for resampling? If I am to write my own resampler it would be very stupid one (just put the previous value in the empty data in the case of upsampling, for downsampling I have no idea lol)

Luckily we have an open source solution like **libsamplerate (Secret Rabbit Code) **with a very permissive 2-clause BSD license. Native Audio uses this for resampling and don’t forget to do your part in attribution if you are also going to use it!

**Secret Rabbit Code (aka libsamplerate)***The Secret Rabbit Code Home Page*www.mega-nerd.com

Next, we have the entire WAV data loaded in memory which Native Audio take care of in the Java part too. (It has to be Java, as it should also dig up all the OBB extension package just in case. C part can only do regular Android asset.) The program read the sampling rate number from WAV header and take the “d a t a” part out to resample using `libsamplerate`

. The various offset is like this :

**Microsoft WAVE soundfile format***The WAVE file format is a subset of Microsoft’s RIFF specification for the storage of multimedia files. A RIFF file…*soundfile.sapp.org

Note that we cannot just offset 44 bytes and always get the data since sometimes it is a bit longer than that! (And I don’t want even a mere 2–4 bytes fake latency in front of my audio…) After reading the rate and tearing out the data chunk it is time for the `libsamplerate`

to do the magic and we are done. Fresh audio data fitted to the rate that the device likes. If you are using the new `AudioClip`

loading feature of Native Audio v4.0.0+, you can skip the WAV header extraction part since we get float array from Unity.

![](../../assets/919f6305f8aa4c94.png)

### Even faster! With “native buffer size”

The log about phone’s audio preference earlier show something about “native buffer size”. From [https://developer.android.com/ndk/guides/audio/audio-latency](https://developer.android.com/ndk/guides/audio/audio-latency) it says :

The[PROPERTY_OUTPUT_FRAMES_PER_BUFFER]property indicates the number of audio frames that the HAL (Hardware Abstraction Layer) buffer can hold. You should construct your audio buffers so that they contain an exact multiple of this number. If you use the correct number of audio frames, your callbacks occur at regular intervals, which reduces jitter.

That means if we have 147 frames of audio for example and the device native buffer size is 50, we should make it into 150 frames of audio so that the phone is happy. Native Audio already do this regardless of resampling or not. Remember that “frame” is the length in byte / 2 if we have 2 channels of data. Keep in mind that the “multiple of” is of the “frame” and not the total byte.

My crap phone with larger native buffer size is actually at disadvantage here because we likely have to zero-pad more to make a multiple of 640 instead of multiple of 192. Note that this is not related to the fast mixer track, but it helps the scheduling of pushing audio data consistent.

Also if you want to know your own, Superpowered guys have developed a very easy to use app to measure latency of any phone and also gives the mentioned buffer size. Your phone might already be in the table in this page! (If not, consider getting the app and do the test to add to their database. Just press the red button with your phone.)

**Test iOS and Android Audio Latency with Superpowered Latency Test App***Measure the performance of any mobile device immediately with the Superpowered Mobile Audio Latency Test App for…*superpowered.com

The buffer size that Unity choose for its own native source seems to be based on Best Latency / Good Latency / Best Performance settings. From what I know it always return 256 / 512 /1024 regardless of devices. (Is it really?) This cause problem when you use Best Latency but the phone could not handle 256 size, causing buffer underrun from all Unity's built in `AudioSource`

play. (Notably on Huawei Mate 20/Mate 20 Pro/P20/P20 Pro/Honor View 20 from reports from my users.)

Interestingly, Native Audio which ask the phone's native rate sometimes get a number as low as 240 but it works, where Unity ones doesn't work on 256 or 512. Unity may incur too much processing that the phone could not make it for a size that small anymore, vs. my super simple play.

### We 100% get fast path now? Yay?

Not quite!

## The limited number of AudioTrack problem

### Number of concurrent audio problem

We are facing with yet another problem : we can play only one sound at the time! Given that one `AudioTrack`

is a linear buffer player, you push something in it plays. You put 2 things in, it plays in a sequential order and not at the same time.

We might think that the solution is easy. Just create more `AudioTrack`

! So let’s say we have 100 `AudioTrack`

and every time we play we choose the next one from previous play so we don’t have to cut off the old one.

We now can have 100 concurrent audio right? Unless it is a very rapid machine gun with 10 second sound for a shot it is very unlikely to have to stop some track to play a new one…

### Limited number of total AudioTrack problem

However Android has a hidden limit of possible `AudioTrack`

** shared for the whole device.**

A [StackOverflow ](https://stackoverflow.com/questions/11964623/audioflinger-could-not-create-track-status-12/12024769)thread suggests that it is some number below 32, which I found it is 24 on my Nexus 5. Maybe it is even limited per app so one app can't hoard all the sources. (I saw this on some lower tier phone)

`SoundPool`

do have this annoying problem too, just that it abstract you out from managing sources. It could fail the same way when it couldn't get more native source.

### Limited number of FAST AudioTrack problem

Not only that **total** limit, here’s a logcat result of OpenSL ES program trying to create 32 AudioTrack :

![](../../assets/1371e9a60d8dfe5c.png)

You can see I got 5 **FAST** AudioTrack from OpenSL ES, the 6th one was created just fine but the fast flag denied by server! Indicating that even if we still have more `AudioTrack`

quota it might not be a fast one anymore. **Fast track is even more limited**.

And a bit later :

![](../../assets/4158f452c23af82a.png)

We are at one more mysterious limit at only 13th AudioTrack. The 14th ones says that “no more track names available” and it crash the program if not handled correctly. (Native Audio handle this correctly if you tell it to create this many, but I recommend just 3–4 tracks or something and not 32) I am guessing this is a limit **per app** for this phone. Some lower tier phones could go to 32 on one app.

### Then how the hell Unity audio can play 32 sounds concurrently on Android build?

![](../../assets/fec4e29ba0f9d2d7.png)

You might remember this settings. It indicates that you can play 32 sounds over each other! How can that be!

The answer is the mixer. If you sums up all the incoming audio before feeding to just **one **`AudioTrack`

that would work just fine (if there is no clipping) and then it means you can have infinite number of concurrent sound!

But of course that is one of the source of latency which this Native Audio plugin is trying to skip in the first place!! You would have to have some audio staging bus where you wait to mix them all, etc. adding more pipeline.

Unity in fact use an audio engine FMOD internally and likely that is doing all the work before finally sending finished audio stream to Android’s (or any other platform) audio player. Good solution for multiplatform engine like Unity. Turns out, this 32 is the **number of** **loudest voices** selected to be mixed on FMOD’s mixing thread and the rest are skipped to save some processing.

**FMOD***In this intermediate tutorial series, sound designer and composer Daniel Sykora remixes the sound and music in Unity's…*www.fmod.com

![](../../assets/6ce4890469e946ba.png)

In the recent Unite Berlin 2018 Day 1 talk “Unity’s Evolving Best Practices” it even has one section that says Unity uses FMOD in which way and how to optimize it.

Other non-latency-critical part of your audio would still be in Unity’s default mixer instead of Native Audio’s harsh restriction so it is a recommended watch. (4:09:13).

Plus remember, Unity’s mixer can handle audio clipping, can do ducking, can organize with sends and together attenuate down or up like having BGM/SFX settings in the option menu linked to the mixer. It is not necessary evil and latency is the enabler of these technologies. If you need it then use it.

FMOD might also explain why Unity can take any sampling rate we hand it. First, we can resampling to whatever rate we like at the importer.

![](../../assets/080c760679cf150a.png)

And then FMOD probably does not care and can mix them all (it is not an audio player, but an engine) If it is doing good, probably it should create a final stream adapting to device’s native rate before sending to Android.

### What approach does Native Audio choose then?

If you want mixers then Unity ones is already doing excellent job, so with Native Audio for the best latency we are going **mixer-less**!

That means the number of `AudioTrack`

we have strictly determines how many sounds we can play at the same time, if we are not going to sum them up in any case.

The algorithm to choose which one is very simple, it just round robin all the tracks like this each time you play : 1 2 3 4 1 2 3 4 1 … if we have 4 tracks. Even simpler than how `SoundPool`

choose the native source which it could do "priority" weight.

We can improve the concurrency by checking which one had finished playing and is vacant and choose that one, but given the purpose of this plugin I fear anything that might add any latency… I think I should keep it simple as round robin. (You can still force it to use any source with the advanced play option overload, if you know what you are doing.)

The next question is, how many native source should we take? As much as possible? Or just a few? 2? 4? Of course 1 is a bit low because we would like some concurrency just in case our hero wants to attack at the same time as collecting coins.

### Could we really take as many `AudioTrack`

as possible?

Looks like the track is shared for the whole device and it depends on other factor how many are taken at a given moment. Logically it sounds really bad if your game took them all and `AudioFlinger`

cannot issue an another `AudioTrack`

for other apps (like your mom’s incoming call) ?

Time to confirm with this adb command run while the phone connected. This is at the home screen without anything open.

`adb shell dumpsys media.audio_flinger`


(If you remove the media.audio_flinger part it would dump almost every information at you)

![](../../assets/cb7f2be0f69179fb.png)

![](../../assets/f79cff32fd8b4f6c.png)

### Examining the dumps

You see 4 output threads! With

- Output device: 0x2 (SPEAKER)
- Output device: 0x1 (EARPIECE)
- Output device: 0x2 (SPEAKER) (different details)
- Output device: 0x10000 (TELEPHONY_TX)

On the first thread you see a familiar number : “HAL frame count: 192" and “Sample rate: 48000 Hz”. (HAL = Hardware abstraction layer, the thing that operate the hardware directly) Yes, this is probably what your game will use.

Note the EARPIECE thread having as high as Sample rate: 192000 Hz. I wonder what is that?

More importantly on the first thread :

```
FastMixer command=COLD_IDLE writeSequence=21018 framesWritten=2017728
numTracks=1 writeErrors=0 underruns=94 overruns=125
sampleRate=48000 frameCount=192 measuredWarmup=10.4 ms, warmupCycles=6
mixPeriod=4.00 ms
Simple moving statistics over last 3.2 seconds:
wall clock time in ms per mix cycle:
mean=4.00 min=0.10 max=9.56 stddev=0.66
raw CPU load in us per mix cycle:
mean=97 min=0 max=408 stddev=48
Fast tracks: sMaxFastTracks=8 activeMask=0x1
Index Active Full Partial Empty Recent Ready Written
0 yes 245 0 0 full 1152 2012928
1 no 0 0 0 full 0 0
2 no 52 0 1 empty 0 9984
3 no 0 0 0 full 0 0
4 no 0 0 0 full 0 0
5 no 0 0 0 full 0 0
6 no 0 0 0 full 0 0
7 no 0 0 0 full 0 0
```


Being a simple man… ehh, an author of Native Audio I see the word “Fast” I like it!

“Fast track availMask=0xf0” also kind of hinting that 1000 0000 means there are 7 fast track slots for use?

Wondering what is the only user of the first thread process ID (PID) 2768 when we are still having no apps open? You check it with :

`adb shell ps`


And that is, the phone!

![](../../assets/bed84fa4ace99efc.png)

### Try the dump with a vanilla Unity game

Starting with Native Audio’s test scene. **Without** pressing Initialize button this is the dump.

![](../../assets/7e1f3923f8a2a75c.png)

![](../../assets/8763067b7b8e7489.png)

If you cannot find it, search for the number “24000” and you should see that line. The reason for this number comes later in the article. But you now know this is Unity’s default android audio track requested **for the entire game**.

You will also see `yes`

, meaning that it is already active even if I am still not playing anything yet. (“actively” playing silence?) Notice that the thread name is AudioOut_15 and there is **no letter “F”** in the “T” column. This letter F means Fast Mixer Track and that is Unity does **not** get a fast one. (Unity do get a fast one on this phone on 2019.1 or later. Read more [here](https://gametorrahod.com/unitys-android-audio-latency-improvement-in-2019-1-0/).)

Note, there is a chance that Unity will get the fast one but I don’t know the criteria that Unity team uses. They probably have more defensive coding which only gives fast track when they are really sure of something I don’t know about.

That is without activating Native Audio. Let’s see next what happen when I start using Native Audio and requesting the `AudioTrack`

for myself.

![](../../assets/fc3970a67d7da4d0.jpeg)

As we launch the game that uses Native Audio, a new PID would be available in `adb shell ps`

, we remember this.

![](../../assets/446c80fa5409e61e.png)

And then the dump :

![](../../assets/10992536e5766501.png)

Who’s 24255 when 24670 is our game? I checked and it is a freaking **screenshot! **Probably the sound when you take screenshot… maybe.

![](../../assets/0a38e1efb7d00ced.png)

Down below you see that fast track’s command is now `MIX_WRITE`

instead of `COLD_IDLE`

now that Unity game is using the sound. 3 clients are already using this thread :

![](../../assets/85bdc7c17fae52e7.png)

Also the thread is now `AudioOut_D`

(not in the screenshot) Meaning that the source we received is not in the same thread as what Unity requests, why? Let’s do a side by side comparison.

(Below is not the same test as before, the PID is now 28714, new phone, and I have requested 2 tracks for my Native Audio app, Unity takes 1)

![](../../assets/a7dd7eaa1cbdfdb9.png)

The little window is the thread which contains Unity’s `AudioTrack`

. You will notice that thread’s “Sample rate” are **both** 48000Hz according to the phone’s native rate, but Unity’s 24000Hz track can also stay in that settings. Indicating that the thread’s rate does not have to match with the containing track’s rate. However, there are several differing behaviour on the thread. (not track)

- HAL Buffer Size and Frame Count of what Native Audio use is much smaller. Actually, it looks like Unity just add 0 to the end there! (192->1920, 768 -> 7680) The smaller the better for latency, and I am not sure why Unity wants 10x of the size. (remember this is already with “Best Latency” audio settings) Normal frame count is also smaller.
- Native Audio process in float, but I didn’t specify this anywhere in my plugin it just goes like that? (However I use 16-bit PCM audio directly)
- Unity is in “Block in write”. Unity get a syncrounous write stream type and that is one of the reason that Unity cannot get “F” the fast track. Native Audio has callback stream type and not synchronous as you will see later on.
- Unity ones has a
`DEEP_BUFFER`

flag. From[this Google search](https://groups.google.com/d/msg/android-porting/0iq6rha9qLA/1OBn0ZVjPA8J)it seems like not a good thing for latency. Native Audio’s thread along with phone’s`AudioTrack`

has`FLAG_FAST`

. This is the best for latency. - The fact that Native Audio stays with the rest of your phone’s audio is promising because it follows the phone’s best effort to output good audio.

All of this incompatibility put Unity’s track in a separated thread since several traits is on the thread and not on the track. Being alone in a separated thread might be a good thing? But this thread certainly has bad settings for audio latency in my understanding.

### Unity’s tactics of never stopping their 1 and only AudioTrack

You will notice that the Active column of Unity’s track before already says `yes`

. But it is `yes`

even if I am not playing any sound on Unity. How can that be? Actually this is their secret sauce : **Unity never stops the **`AudioTrack`

.

When we use `audioSource.Play()`

probably it (mixes and) pushes data to the track that is always playing. It is like you change the cassette tape without stopping the spinning player. Doing it this way drains battery more, but with benefit.

I learned about this the hard way in v1.999 of Native Audio where I was hunting down a **performance bug **together with my friend in the Discord channel. Only on some phone, Native Audio would drop frame rate where Unity is fine. (Of course Unity has more latency, but no frame rate drop. Completely different thing by the way!)

I thought it is because the phone cannot handle rapid double buffering callback for low latency I am using but I was wrong. It is because I stop — clear — start the `AudioTrack`

every time. It sounds like the best practice to do but unfortunately a more hacky way is required.

One of the “differing per device” thing of Android is `AudioPolicyManager`

** **where each manufacturer can config as they like. (nightmare ensues) And this is the log from my test program that sheds light to me :

![](../../assets/235d8096730fea61.png)

Look at the right. The search hit for `AudioTrack: start()`

is a lot on the period Native Audio is playing. But the little hit at the top is Unity's. Unity only start once at the beginning.

And then this cause problem on only** some phone**, since `AudioPolicyManager`

is not the same between each phone. In this case the phone Le X620 I guess it do something too much on each start. (The dolby thing?) All my other phones even with lower-end ones does not have this problem on rapid start-stop.

Phone that does not drop frame rate does not have a policy that do much work at `AudioTrack: start()`

and `AudioTrack: stop()`

. I think this is why Unity choose to not ever stopping the `AudioTrack`

. To stop playing, just stop sending data. But that will make stopping a bit late depending on the buffer size.

By this, I finally found the original cause of my troubled customer that came to the Discord channel months ago. He said other native audio plugins and also including my Native Audio v1.0 would drop frame rate after upgrading a certain phone to Oreo. I spent time improving Java-based `AudioTrack`

to OpenSL ES hoping to fix it. The latency is better but the frame rate drop remains.

Apparently that phone has `AudioPolicyManager`

programmed for Android 7.0.0 that does not work well with 8.0 Oreo, and it became much more aggressive on every stop and play of `AudioTrack`

. I assume other plugin makers also stop-play `AudioTrack`

like v1.0 of my plugin so the same problem was reproduced no matter what way to play audio… except by Unity. (which you now know why Unity has the priviledge of not dropping the frame rate)

With that in mind, Native Audio 2.0 also use this “always playing” approach by **keep feeding silence** even if we have nothing to play. I tried a more efficient way, buy we cannot just stop sending data because if the buffer runs out and we do nothing, it will automatically stop unfortunately…

I **believe** silence feeding is what Unity did to achieve the constant `yes`

. Being a game engine, it make sense that the sound would be active almost always or the game would be very boring. And with Unity’s approach of 1 `AudioTrack`

per game it should not introduce any noticable battery drain problem with constant silence feeding.

For Native Audio though, it translates to more battery drain proportional to how many `AudioTrack`

you requested so be careful. But I doubt it will be significant compared to the game itself. For example this is when you want 3 `AudioTrack`

s for Native Audio. It get 3 track that is always playing silence when not busy so that it stays active. (stay `yes`

)

![](../../assets/bb4780419aa20fea.png)

![](../../assets/99487efe82243d9e.png)

Above : Unity’s track. Below : Native Audio’s 3 fast tracks which we keep them active with silence feeding. Notice the same PID, indicating that the two really came from the same app but separated in 2 different audio thread. Unity ones has 24000Hz rate and is not fast. I have no idea what “FS” means?

(But, in the test below of this article it is possible to not be a yes since it was using a verison of Native Audio that stops the track.)

Here’s an another rapid stopping log from Xiaomi Mi A2. Being an “Android One” phone it does not have extreme modification and looks like stopping does not do much, but still some `AudioPolicyManager`

are there. (It does not drop frame rate though)

![](../../assets/56b11fb6d293337c.png)

Also keeping the track active with silence is actually good for latency, since when the audio circuit is cold you will end up with more latency on the first few plays. It is explained officially here :

**Audio Latency | Android NDK | Android Developers***Audio latency: buffer sizes Building great multi-media experiences on Android Latency is the time it takes for a signal…*developer.android.com

### Trying to max out the `AudioTrack`


Now let’s compare with an another Unity game where we instantiate `AudioTrack`

like no tomorrow. This is after opening the game, before taking more AudioTrack :

![](../../assets/1b1bd11b9302c85b.png)

After !

![](../../assets/361cb55e0bac2c5e.png)

Our game quickly swarmed the thread. We learned :

- The thread
**max out at 16 AudioTrack**? We can only instantiate 13 additional tracks because at first Unity, the god damn screenshot, and the phone took the first 3. - We have maximum of 7 fast tracks and we can only have 4 more because the first 3 are already a fast one (damn it screenshot, I know you don't need that fast track). It is indicated by the
**letter F at the front.**In all I got 4 + 1 = 5 fast tracks for my game. You see there is only 7 F characters. This is the hard limit of all Android phone.

About 7 fast tracks, this is definitely the case as I found out later from this Android Souce Code docs :

**Design For Reduced Latency | Android Open Source Project***The fast mixer runs periodically, with a recommended period of two to three milliseconds (ms), or a slightly higher…*source.android.com

You will also see the fast track does not support sample rate conversion. This is why we need a resampling library to transform our audio first to be fast.

More questions… is this a good idea? What if we do this then … the other app want some. What will happen? Crash? Which one crash?

### Over-allocating the `AudioTrack`


First, I try using Native Audio to play sound rapidly so that it round robin and use up all the tracks :

![](../../assets/777cd1adbda96247.png)

Understandably all of them except the phone now say `yes`

on `Active`

column… but wait, where is the god damn screenshot? Somehow the total track dropped to 15 now but whatever. Maybe it already give back to the OS.

I will start over again and make 2 of that app and have it fight with each other to see what happen.

I do this : The first app request as much as possible. The second app request 4 AudioTrack. (+1 track Unity will take) Go back to the first app and use all tracks. What would happen?

![](../../assets/d35aec518638be5f.png)

The first app take 1 + 13. The phone take 1. The second app **successfully** take 1 + 4 more. **The maximum track is now 20!** (By the way the second app was granted all non-fast track)

Looks like my assumption that the thread max out at 16 was wrong and it is rather a certain number (14?) per app. The second app can get more just fine while the first one was prevented.

What about **3 separate apps **all requesting as much as 32 AudioTrack then?

The first app : It took 1+13. Results in 15 tracks. **All 7 fast tracks used up.**

![](../../assets/62b13bfdaa86e0b0.png)

![](../../assets/4af10ccd168211ea.png)

The second app : At open Unity take 1 more results in 16 tracks.

![](../../assets/b6b04ffdf69cfe45.png)

At request : still can take 13 more like the first app! Resulting in 29 total tracks. **All of them got non-fast track.**

![](../../assets/82250f6b63f75f1d.png)

The third app : At open take one more as usual resulting in 30 tracks.

![](../../assets/3914e7bb283e4833.png)

However at request it can only take 2 more! Resulting in 32 total tracks. A nice number that signify the real limit.

![](../../assets/dea2d59947d240f0.png)

At this point it’s time to fire up my Unity game and see what will happen…

**It has no sound!**

Also not just my game. I could run this `AudioTrack`

-hoarding app first then reliably start **any Unity game **without sound. You can use `adb logcat`

while starting the app to see if it is Unity or not. I have several music games in my phone that made by Unity and they all starts without sound in the maxed-out `AudioSource`

state.

This 32 tracks limit is documented officially in the source code documentation here :

**Design For Reduced Latency | Android Open Source Project***The fast mixer runs periodically, with a recommended period of two to three milliseconds (ms), or a slightly higher…*source.android.com

The log is not without any abnormalities. Here we can see something wrong after the standard Unity startup log :

![](../../assets/e8f772197ae2eb2b.png)

See `libOpenSLES`

? That is the same as what Native Audio uses! And you can see that it even try 2 times struggling to make one audio source but fail in both. “no more track names available” is the same error message as when we instantiated the 14th additional audio track of one app.

You will also notice that both times are not exactly the same. At the end of the first time it says :

```
FMOD failed to initialize the output device.: "An error occured that wasn't supposed to. Contact support."
Forced to initialize FMOD to to the device driver's system output rate 48000, this may impact performance and/or give inconsistent experiences compared to selected sample rate 24000
```


The second time :

```
FMOD failed to initialize the output device.: "An error occured that wasn't supposed to. Contact support."
FMOD failed to initialize any audio devices, running on emulated software output with no sound. Please check your audio drivers and/or hardware for malfunction.
```


The first message is a a bit curious as it says like the “selected 24000Hz” is the best choice, but it is being forced to use 48000Hz… (which we try so hard to achieve) This is more hint to Unity’s 24000Hz rate AudioTrack.

What if at this moment that I have this full 32 sources, without closing any apps, **we go watch YouTube or something?**

![](../../assets/343b6f5597de9c33.png)

![](../../assets/5a22b56cf405a1e6.png)

Oh no! It uses the thread `AudioOut_1D`

and not the thread `AudioOut_D`

that we have filled up with 32 sources so it seems there is no problem… also this thread uses deep buffer so it saves energy in exchance for more latency.

If your mom called when we have 32 sources probably it will use the `TELEPHONY_TX`

thread and also has no problem.

How about the voice recorder app?

![](../../assets/1901303bce50356e.png)

![](../../assets/198f198c64cfc367.png)

Yet another thread `AudioOut_3D`

and not the same as our game’s thread. This one uses `DIRECT`

flag which unfortunately cannot be `FAST`

at the same time. How about a music player?

![](../../assets/d82cd68bdcce9ce2.png)

This time it is `AudioOut_45`

with some effects inside. At this point if we go back to the apps it would still work. All the `AudioTrack`

it has reserved was still there.

What criteria makes Android put `AudioTrack`

in the first thread? I am not sure, but I have one more game in my phone which the log says it is a Cocos2D-x game and it also occupies the first thread the same as Unity game. Not sure about other games which does not use Unity nor Cocos2D? I think Android match thread’s spec and group the `AudioTrack`

that wants the same thing together.

### Dead `AudioTrack`

and the headphone

One more problem though! We have learned that one Unity game can make 1 + 13 = 14 `AudioTrack`

s and 6 of them could be fast. (The phone took 1 fast track) So is 13 the magic number? We could have 13 concurrent sound this way…

If we plug in the head phone, the output device of almost all thread changes to `WIRED_HEADPHONE`

like this :

![](../../assets/eb57d63066d47413.png)

But that is not all. At this moment **all **`AudioTrack`

** will be “dead”. **Luckily it has an auto-life functionality when we going to use it instead of segmentation fault or something. This is the log from normal Unity game when we plug/unplug the headphone :

![](https://gametorrahod.com/content/images/downloaded_images/Android-Native-Audio-Primer-for-Unity-Developers/1-XFrHcJMyi3g5kEzlpyzHQg.png)

So the game is trying to `obtainBuffer()`

and it create a new one **in place. **This revived `AudioTrack`

does not take one more space but overwrites the old one.

But! One problem is it create before overwrite itself. What I want to say is if you are in the state that no more `AudioTrack`

can be created, you get this :

![](../../assets/fc9091213185f225.png)

And so… all of your 14 `AudioTrack`

s are dead just by plugging/unplugging the head phone and cannot be revived. Very sad as the game will be muted forever until the player restarts the game. This would not happen if you instantiate **one less **`AudioTrack`

so that the “creating a new one” works. (Anyway, you are better off requesting something like 3 tracks and not be so greedy.)

### Is it the same on any other devices?

Would not be an Android without “Oh no it worked before but why not on this phone”.

Let’s try it again on my crap-phone. At home screen :

![](../../assets/479519e333bb55a6.png)

```
PID 532 : system_server
PID 710 : com.android.systemui
```


This time it is really short! This phone has only 1 audio thread. And even at home screen, somehow system has **already taken 5 fast **`AudioTrack`

**.**

When opening the Unity app

![](../../assets/4253c1a38fd463f9.png)

The difference is the word “OpenSL ES” is no where to be found, but we get this `AudioPolicyManager`

instead where OpenSL ES + `AudioTrack`

message would happen.

At this point PID 15510 of Unity take one more `AudioTrack`

**and of course it is not a fast track (no F at front) **because clearly on the `SRate`

column it uses 24000… but it is now together with others! (Because we have only 1 thread on this phone where else can it be?)

One more difference, if we make the app inactive …

![](../../assets/e24d4c1de4702b63.jpeg)

![](../../assets/67488e9d14a3ee44.jpeg)

The PID 15510 immediately disappear this time! But when putting it back the track came back magically, I did not modify the code to be able to remember `AudioTrack`

, destroy it temporarily, restoring, etc. at all!

Hinting that this phone might not have a capability to thread and so it has a special policy to keep `AudioTrack`

in hibernation, or something?

I think that is the work of a custom `AudioPolicyManager`

not on my higher end Xperia Z5. This was printed when we minimize/maximize the app :

![](../../assets/b8826f443d3073ba.png)

![](../../assets/217540f922dcfc58.png)

`releaseOutput()`

might be the one freeing `AudioTrack`

. Understandable because this phone has only one audio thread. The question is higher end phone might also have this policy if we do manages to overload all thread?

Next, it is time to create 32 `AudioTracks`

.

![](../../assets/29b59c8569a90c98.jpeg)

![](../../assets/b25fd36005566afa.png)

This time there is no limit of 14 ATs anymore! We get a whopping 26 players resulting in full 32 `AudioTrack`

s.

Moreover the fast track now is at **7 fast tracks**. Native Audio got 2 more by requesting for 44100Hz track plus we already have 5 at start. Unity missed the chance. We maxed out at 7 F as usual.

But also interestingly, this time in the log there is no mention of fast track flag being rejected/accepted at all. (But you can see some PID 15510 get the F at front after Native Audio initialization)

Playing YouTube right now could be really bad right? We have all 32 ATs occupied and there are no other threads unlike in my Z5.

Fortuantely, that `AudioPolicyManager`

** **saves the day with its auto release-auto reclaim `AudioTrack`

ability. Do you get it? When we switch apps in any way we will 100% get back 1 AudioTrack. This means we never have to fear that other app cannot make sound…

![](../../assets/286ce7c698702404.jpeg)

![](../../assets/e73e91b9726762f2.jpeg)

![](../../assets/5320511fc2a21896.jpeg)

Remember that my Xperia Z5 did not do this and left the `AudioTrack`

there, maybe because it is confident that other app can use other available threads.

*(This assumption is wrong, as you will find out in the next section)* This “guaranteed 1 track” seems to have a property that it **cannot be fast **so that it is the most flexible and is usable for every app that you would like to switch to. That’s why Unity failed to have fast track at the start up. But additional request like what Native Audio do can have fast track (or fail because over 32 tracks)

### It is possible for some phone to not provide any fast track

This is a `dumpsys`

from Huawei Y9, a device that doesn't provide any fast track no matter how matching the `AudioTrack`

spec I gave it. This device comes out in 2018, it is not old. And also I had found a device cheaper than this 10x that could provide fast track too. (But ultimately results in worse latency) This is the case where Native Audio will barely make any difference from Unity audio.

![](../../assets/15f7ce2008608132.png)

### Unity’s “24,000Hz” sampling rate?

As seen earlier when I have overloaded the `AudioTrack`

count and made Unity reveal that it is using 24000 sampling rate somewhere all along. What exactly is that?

From this extremely informative thread :

Many found that on their Android device they get this 24000 number out of `AudioSettings.outputSampleRate`

variable. Does Unity default this to device native rate / 2?

Now that my crap-phone is 44100 native rate, I went and test logging this variable and turns out, it prints 24000 anyways and not 22050. So I think it is a **hard fixed** value from Unity. Also it is similar on iOS where it uses 24000 by default, but interestingly switch on the fly to higher number on using **bluetooth **headphone/speaker. (Not happening on plugging wired headphone)

I don’t know why Unity choose the number 24000 specifically for Android because on Editor it says 44100. And I don’t know on iOS if it changes between devices also?

And so **I guess** the Unity’s audio pipeline would look like this from start (Unity) to finish (Android’s `AudioTrack`

). The resampler at runtime would be hard coded to do downsampling to 24000 on Android. And if your player are lucky to have 48000 device they would get fast track.

![](../../assets/fc946e45be41ad5e.png)

Where Native Audio pipeline would be like this :

`Fixed rate audio X Hz -> Runtime resampler (X to Y Hz if X != Y) -> AudioTrack (Y Hz) match the device native rate Y -> Device HAL`


So that we would always get the fast track, and we can skip resampling as a bonus if the prepared file match the device rate.

Currently I have a rule to fix the file at 44100 so if your player is at 48000 a resampling is required, but in the code it actually can handle 48000 now. And that would be the better choice since in the future less and less player would come to your game with 44100 device. But I still have that rule on since on iOS side of Native Audio I still haven’t implemented the resampler yet and it fixed on 44100 Hz at the moment.

### Confirm with the log dump, deep dive into Android source codes

For confirmation, Android always log things on `adb logcat`

when it is doing something natively. When Unity started and when Native Audio initialized it logs the same thing about AudioTrack since ultimately both mine and Unity uses `AudioTrack`

. Then it is possible to compare what Unity instruct Android to do vs. what I programmed Native Audio to create an AudioTrack.

![](../../assets/10ced91126083ec2.png)

Your device’s log might not be exactly like this, depending on Android version and phones. That log was from Le X620 (Android 6.0.0) phone. Here’s one from Xiaomi Mi A2 (Android 8.1 Oreo/Android One program). It looks similar with different wording (has flags, sample/samplingRate, type/usage, etc.)

![](../../assets/ca499b7443cbe512.png)

Anyways, no matter what phone you have the Unity ones can be found easily by searching for “GLES” (that’s the graphic related OpenGL) but there is only one line which the upper big `GL_`

chunk in the left side in the picture above follows. You can easily tell if a game was made by Unity or not by adb logcat and look for this big chunk at start… unless the game uses Vulkan this one disappears, then you have to find the logs a bit above.

A bit below from that should be an initialization of one and only `AudioSource`

for Unity. Search for the number “24000” and you should found it. By examining the format here, it is now possible to search for the one Native Audio produces. Here on the right side I found them. (Around them are logs which is not present in the store version of Native Audio, it is for my development use)

Again, the Unity ones you also see something about “DEEP buffer”. And again from [this Google search](https://groups.google.com/d/msg/android-porting/0iq6rha9qLA/1OBn0ZVjPA8J) it seems like not a good thing for latency. I am not sure why Unity do that but my Native Audio does not have it.

You can clearly see “24000” in Unity, while my Native Audio ask what the device want and instantiate 44100 (the first phone)/48000 (the second phone) rate audio source.

If you are looking to make sense with any of these logs, unfortunately in the entire Google the only reliable source is… the Android source code. The log must be somewhere from the source, and it is a very good way to start learning from source since log string searching often returns just a few results, now you know where to start from. For example, the numbers in the highlighted line. You can Google and end up at :

**media/libaudioclient/AudioTrack.cpp - platform/frameworks/av - Git at Google***Edit description*android.googlesource.com

And then knowing that this file produced the log, you can search for that line. Then you know each one’s data type and finally search for the meaning of them. You might end up at `audio.h`

:

**include/system/audio.h - platform/system/core - Git at Google***android / platform / system / core / android-5.0.0_r2 / . / include / system / audio.h*android.googlesource.com

Or `AudioTrack.h`


**include/media/AudioTrack.h - platform/frameworks/av - Git at Google***android / platform / frameworks / av / e2d617f5ba7fb90f27b03e2593666b2c927e4dc9 / . / include / media / AudioTrack.h*android.googlesource.com

These header files has some nicely commented codes. (thank god)

For example you know Unity’s stream type of -1 meaning `AUDIO_STREAM_DEFAULT`

. Unfortunately without source code digging you don’t know what exactly each one is, but at least the `enum`

is more readable than `int`

! Actually I believe this one maps to managed side of “content type”, but there are so many more native values I don’t know what is the managed equivalent.

**Audio Attributes | Android Open Source Project***Audio players support attributes that define how the audio system handles routing, volume, and focus decisions for the…*source.android.com

Also the flags # you see Unity has 0 and my Native Audio has 4. This is also in audio.h and you will see `AUDIO_OUTPUT_FLAG_FAST = 0x4`

. Meaning that Unity ones does not get the fast track but Native Audio did because the sampling rate match with the device.

From that header file you might notice

`AUDIO_OUTPUT_FLAG_DIRECT = 0x1, // this output directly connects a track // to one output stream: no software mixer``


which sounds promising, but then [in the source code I see a comment](about:invalid#zSoyz) like :

`// FIXME why can’t we allow direct AND fast?`


So… if the dev even ask themselves this question then I also have no idea WHY.

For `transferType`

Unity’s value of 3 signifying `TRANSFER_SYNC`

as stated in `AudioTrack.h`

but Native Audio’s 0 means `TRANSFER_DEFAULT`

which will be converted to `TRANSFER_CALLBACK`

in `AudioTrack.cpp`

. Note that in place like `AudioStreamTrack.cpp`

there is a comment like :

`// Note that TRANSFER_SYNC does not allow FAST track`


So it means when Unity does not get a fast track it writes to the `AudioTrack`

synchronously. I am not sure what happen when Unity does get the fast track. But Native Audio is based on the callback way. When you use OpenSL ES with Buffer Queue it is always the case that we have to use callback way as I interpreted from the source code. (See `android_AudioPlayer.cpp`

of OpenSL ES for this, around the call to `new android::AudioTrack`

)

If you want to dive into the source too, I suggest cloning the git and use Visual Studio Code to search for something you want to know. This is the Android `AudioTrack`

part.

`git clone https://android.googlesource.com/platform/frameworks/av`


The bridging from-to OpenSL ES part is called the **Wilhelm project**. Quoted from here :

**src/README.txt - platform/frameworks/wilhelm - Git at Google***android / platform / frameworks / wilhelm / refs/heads/master / . / src / README.txt*android.googlesource.com

This is the source code for the Wilhelm project, an implementation of native audio and multimedia for Android based on Khronos Group OpenSL ES and OpenMAX AL 1.0.1.

Clone it here :

`git clone https://android.googlesource.com/platform/frameworks/wilhelm`


### That basically means all audio are degraded with Unity Android by default no matter what the import settings you have!

Yes, and I think it is a strange design decision. There must be some reason for the Unity team to do this but anyways :

![](../../assets/8af925a231603622.jpeg)

I made a performance test APK to debug frame rate problem, but accidentally found interesting thing related to this. When you run the APK Unity will play sounds with `audioSource.Play()`

followed by my Native Audio.

The Unity one **sounds different in a bad way **compared to Native Audio ones** **but both are exactly the same file. Just that the first one passed through Unity’s importer, **with maximum quality import settings**. Unity’s audio sounds bad even with PCM (no compression/no quality settings)

(This scene is included with NativeAudio v2.0+ purchase. You can see for yourself an obvious degrade Unity puts on)

From what I have always been assuming, PCM should be equivalent to playing just the .wav file and should be = Native Audio quality because Native Audio in this test is using the wav file directly from `StreamingAssets`

.

So my theory is Unity really did resample to 24000Hz on play (not on import) according to the last section, and there is no way to stop this. As long as it passed the importer it will be resampled?

Not to mention in the importer it even has a box that says “Preserve Sample Rate”. This makes the box a lie since in the real device the rate was not preserved after the play. But you wasted space for the preserved rate.

(On platform other than Android it might not be forcefully resampled to 24000Hz, haven’t investigated.)

![](../../assets/c3a855d543ff5752.png)

Imported size = original size means already at possible best quality.

And I have used `sox`

on the original file manually `sox input.wav -r 24000 output.wav`

to force 24000Hz file out of it. When I listen to that it sounds **just like what Unity played in Android.**

For now I would like to conclude that** the audio is always degraded in Android Unity** (as of 2018.2.3f1) no matter how high quality your original music was. That’s my guess. If it cannot even play this little wav file in its original quality then what about your real music? This makes Native Audio also a superior solution in regarding to audio quality, not just latency. Remember, I don’t know the reason of this yet. There must be a good reason to intentionally code this in the engine.

For the time being, if you use **“ANA Music”, **the `MediaPlayer`

based solution I mentioned in the beginning, I think you could skip Unity’s 24000Hz problem while still using OGG with `StreamingAssets`

. The plugin does not mention superior quality to Unity in its description but with this findings, it is actually a very good solution for high quality music with Unity since unlike sound effects, we not really need minimum latency for starting a music. Just the quality. The downside is that you don't have that quality slider in Unity with using `StreamingAssets`

.

My Native Audio from v4.0.0 can now use OGG by piggybacking `AudioClip`

that was imported with Vorbis option in Unity, but unlike `MediaPlayer`

solution it must be fully decompressed to play. So you save only the game size but not RAM space on the actual use, and could get you into trouble if you want to play long music. But you can use the quality slider in Unity this way too unlike ANA Music.

### Other reasons for being denied the fast track

I recently won the Galaxy S10+ for submitting many bugs to Unity. This device shows one more interesting case :

![](../../assets/80402492f3046173.jpg)

This scene on `Start`

will deallocate all previous tracks, and request 4 new ones. You know fast track is available for more than 4, and surely we just released them all (except for the one Unity took, which we have no control) an expected result is that all requested track should be fast.

![](../../assets/e8c8184c079d52fc.jpg)

Turns out some of them weren't fast. And this reflects very obviously on the test scene when audio cycles the source it wants to use, some of them comes out slow and fast, in consistent patterns.

What is this "throttle time"? Googling returns nothing, I guess the phone needs some time after releasing the source to refresh its fast track to be available again. The take away is that, there may be more reasons you could not get a fast one other than track limit.

### Stuck partial wake locks

Fast forward to 2019 but problems still won't stop coming to me.. one user reports that Native Audio was draining battery and trigger a stuck wake lock.

This is when the app is holding onto something when minimized. And the cause is because Native Audio was not letting go of its native sources when minimized, killing battery. We can confirm with :

`adb shell dumpsys power`


And you could be seeing something like

`PARTIAL_WAKE_LOCK 'AudioMix' ACQ=-27s586ms (uid=1041 ws=WorkSource{10331})`


Which when left for too long, became :

` PARTIAL_WAKE_LOCK 'AudioMix' ACQ=-3m3s26ms LONG (uid=1041 ws=WorkSource{10331})`


This is not only bad for battery, Google Play Store do detect apps with this behaviour and put something like this on your app. Potentially reducing your app's rating.

![](../../assets/5bf670e1bc83f1c5.png)

And you know most gamers... just tends to minimize the game and forgot about it. The game will still holding the native `AudioTrack`

(which is a shared resource, remember). From v4.3.0 onwards, Native Audio will dispose the native sources on minimize and get back the same amount on maximize. The downside is that the game can no loger play audio on minimize, but that's usually a function of music player not a game. If you are doing native Android audio works, be sure to think about this too.

## Benchmarking time!

We will do a measurement by placing the device in fixed position, recording the peak of nail sound touching the screen to the response sound produced by the app.

While this is not a standard latency measurement approach like loopback cable method and the number alone is not comparable between devices, but **time difference of the same device truly show how much the latency decreased** without doubt.

The pure Unity’s audio was measured with “Best Latency” settings on Audio Settings, the fastest playing (smallest buffer) Unity can achieve without any plugins. (And assuming that the phone could handle the small buffer size Unity selected)

At first I wasn’t annoyed by Unity’s latency that much, but after a clear contrasting with Native Audio (especially on Android) the latency reduction is insane. It is surprising how I was able to live with that bad latency when there’s nothing to compare with.

And the device’s positioning according to the mic actually has significance. The time below includes touch processing time + mic latency + **sound traveling through air** time to the mic. If I move the device away for just 4 centimeters, it would result in 12ms increase of measured time given that the sound travel at 331m/s in the air. (0.04/ 331) * 1000 = 12 ms. Anyways, I guarantee that the same device has the distance from device to the mic fixed. I am really careful about this.

Here’s the publicly accessible Google Sheet test result. I will keep adding to it once I get a chance to come across more devices.

![](../../assets/327721fd1344f90d.png)

**Native Audio Benchmark Data***Form Responses 1 Timestamp, Untitled Question Sheet1 Click here for notes, Sample 1, Sample 2, Sample 3, Sample 4…*docs.google.com

For your information “Native Touch” is my other plugin designed to make the touch faster. If a touch plays feedback audio then it will translate directly to better **perceived** audio latency. Anyways, it is not of our interest in this article.

**Native Touch - Faster touch via callbacks from the OS, with a real hardware timestamp***Did you feel like your app has oddly not as satisfying experience as other apps installed on the same device? Did you…*exceed7.com

There is a reason I choose the Xiaomi Mi A2 for the official teaser video of Native Audio. **The gain is huge!**

- Comparing the new Mi A2 with a quite old Z5, the Z5 has much better default Unity latency but Native Audio bring them close together. Something is wrong with the A2? The fact that Z5 has both “pro audio” and “low latency” flag might have to do somethin with this. Why “what Unity added” the Z5 can do it better? (Because Native Audio removes what Unity did to the game and the number became similar)
- The reason of previous point, is probably Mi A2 does not report the track and Unity cannot guarantee fast mixer track support and does not give out one. (
[Forum reply from Unity team](https://forum.unity.com/threads/android-sound-problem.359341/page-3#post-3638170))[The 2019.1 update](https://gametorrahod.com/unitys-android-audio-latency-improvement-in-2019-1-0/)gets a better track for Mi A2, making the time much closer to Native Audio. - Xperia M almost does not care about anything I do and the number changed in an unmeaningful way. Perhaps the OS version is too old. (On some version there is a huge audio upgrade,
[like Marshmallow](https://superpowered.com/android-marshmallow-latency)) So obviously I have not include this device in the homepage. Plus.. no one would still playing games with this phone + Jelly Bean anymore right? I hope… - A1000, this device is VERY low-end (about 30$) and sold in only developing country I think. But it shows improvement with Native Audio. Probably thanks to Lollipop.
- Not related to Android but here it is, the iOS. The latency number that makes every Android user drooling! I heard even the 1st iPhone has something around this number. Not to mention that this Gen 5 is very old and has been actively used for all its lifetime until now. iOS has a very pronounced gain from Native Touch, since the touch consistently arrives faster by 1 frame and land at the same place every time unlike Android which arrives in other thread at variable time.

### Lesson learned

- One Unity game take 1
`AudioTrack`

at start. All default Unity audio mix into this one`AudioTrack`

. Not the fastest but efficient on resource! - There is a limit of certain
`AudioTrack`

**per game**depending on device, or no limit at all. - There is a limit of 7 FAST
`AudioTrack`

**per device**distributed in a first come first serve basis. (One game can take all of them and the game execute later can get none of them) - There is a limit of 32
`AudioTrack`

**per device.** - The
`AudioTrack`

claimed can’t be forced stolen by other apps that comes later. - To auto-revive dead
`AudioTrack`

cause by output device changing you need to satisfy both having under AudioTrack limit in a game, and 31 or lower`AudioTrack`

in the whole device. Because it needs to be able to allocate one more before able to replace itself. - Non-game application being (higher-end phone) in a different audio thread, seems to not using the track in the 32 track quota too so there is not much fear that your game will mute or crash other apps. The first defense being your game can take up to only some tracks while the true limit is 32. It is very unlikely that other game will use Native Audio, eat up a lot of tracks, and is running at the same time as your game.

### Back to the very first question, how many `AudioTrack`

for Native Audio?

- Remember that you can use non-critical audio with Unity ones just fine.
- Often fast audio is some kind of response sound. Game which play in holding position probably need only 2 for both thumb or maybe 3–4 at most.
- If 2 sounds is to be layered exactly at the same time with no chance of ever having more offset between each other, consider merging the sound file rather than mixing using multiple
`AudioTrack`

. - If you want as much fast tracks as possible to your game, choose 5
`AudioTrack`

for Native Audio. 1 for your game’s Unity and 1 for the phone PID and that’s all 7. But if you have some games running before opening your game, the number of fast track you get will be reduced and you will get some non-fast track in the mix. This might be bad as the algorithm cycle through the tracks and you will get slow track every now and then as a result.

Anyways in my crap-phone example the phone already took 5 outright so still this is not a guarantee… (but arguably crap-phone would not benefit much from fast track I think) - If you want the most concurrency without caring about having non-fast track in the round robin, use at most 12 AudioTrack as 13 make you unable to bring back dead AudioTrack after plugging the headphone. Not sure about the limit on other phones though.
- Personal opinion :
**3 is enough**and that will be the default in Native Audio’s code. (you can change it at`Initialize(initializationOptions)`

) The other 2 fast track is left for maybe other Unity game is taking it (e.g. You have Unity-made mobage minimized waiting for stamina while playing some more active games) and maybe some stupid thing like screenshot process took it.

## Android Native Audio (`SoundPool`

) vs Native Audio (OpenSL ES)

Armed with all the knowledges about (native) `AudioTrack`

, we are now ready to learn what `SoundPool`

(And in turn [Christopher Create’s “Android Native Audio”](https://assetstore.unity.com/packages/tools/audio/android-native-audio-35295)) really do, in a way comparable with Native Audio.

Everything in Android must ended up using these 7 fast, 32 total AudioTrack. `SoundPool`

and OpenSL ES ended up being the same thing after all.

There are lots of info in the `SoundPool`

official docs including how it governs the underlying `AudioTrack`

(worded as “stream”)

**SoundPool | Android Developers***A SoundPool is a collection of samples that can be loaded into memory from a resource inside the APK or from a file in…*developer.android.com

### Instantiating

`SoundPool`

: On instantiating a Java instance variable`new SoundPool(maxStreams)`

**NO**native`AudioTrack`

will be requested at this stage.`maxStreams`

will be used when playing later. This instance is not the audio track, but think of it as an automatic track spawner/manager. (Can later instantiate multiple tracks)- Comparing with (Java)
`AudioTrack`

, that one is really one instance per (native)`AudioTrack`

. The name matches, so that make sense. - Native Audio : On calling
`NativeAudio.Instantiate`

you request 3 (or more) (native)`AudioTrack`

upfront with a guaranteed FAST mode if the 7 FAST quota is still not used up. (More about this quota :[https://source.android.com/devices/audio/latency/design](https://source.android.com/devices/audio/latency/design))

### Loading sounds

`soundPool.load(__)`

It can handle compressed audio also according to Google’s docs. No restriction at all. (You can load one mono 44100Hz file, then one stereo 48000Hz file etc.) The loaded sounds is contained in the`soundPool`

instance neatly, so you can`release()`

on the instance once to release all sounds.`NativeAudio.Load(__)`

After loading we will try our best so that it match with the requested FAST AudioTrack. This includes agreeing on a certain format beforehand, pre-resample after load, etc. You can release each sound individually. You can use imported`AudioClip`

instead of what's in`StreamingAssets`

.- If your game uses a lot of sounds,
`SoundPool`

has big advantage on this alone because you can halves sampling rate, halves resolution, use ogg, etc. Native Audio could also use**decompressed**OGG by grabbing data from`AudioClip`

, but it will be decompressed, not compressed as-is like`SoundPool`

,`SoundPool`

is the clear winner here. - SoundPool is an
**inverse**to Native Audio in this aspect. Because a track will be made to fit (destroy/recreate) the audio you want to play dynamically. (Setting the rate of play also requires reinstantiating the track) Native Audio fixed the track spec for the fastest play first and foremost, then try to transform (resample, etc) a loaded audio to be playable in those tracks.

### Playing

`soundPool.play(__)`

Using the loaded ID we can play it. Remember we still have no`AudioTrack`

.**The AudioTrack will be requested at this moment.**And a FAST flag is not guaranteed because imagine you are playing loaded 44100Hz audio but your phone is 48000Hz, that track cannot be fast. This method return an ID of the new track.- If you play again quickly, while the previous one is not over yet
`SoundPool`

will automatically**instantiate a new track dynamically**for this play so that the sound can overlap with prior one.

If the`SoundPool`

has over`maxStreams`

streams it will try to stop a stream to play new sound based on “by age” and priority algorithm. If this happen, the method instead return an ID of that stopped and replaced track. The track selection probably have to care if the audio is able to be played on the track or not. I don’t know what will happen if it mismatches.

For example, currently owning 2 tracks both are playing 44100Hz audio,`maxStreams = 2`

, then the next sound is 48000Hz, which track would`SoundPool`

stop? Because no track is compatible with 48000Hz and no more can be allocated due to`maxStreams`

. I guess it will have to spend some time resampling to match the track. - You see that the track is never freed, just continuously increasing when it wants automatically while you play sounds. All tracks can be freed along with loaded audio with
`.unload()`

`NativeAudioPointer.Play(__)`

It is more efficient on play since Native Audio has already allocated all streams (`AudioTrack`

) up front. We just put sound in one of them. The sound is guaranteed to works with all tracks, and all tracks already having fast flag if possible.

The selection algorithm is more basic though, just round-robin through all available track. However with advanced play argument you are able to pinpoint which track you want to stop and replace, unlike the all automatic`SoundPool`

.- It also returns something similar to
`SoundPool`

track ID. You can then use it to pause, etc. just like`SoundPool`

. `SoundPool`

has more advanced track selection algorithm such as setting a priority value so that some playing sound does not get replaced forcefully by lower priority sound. Native Audio is more stupid because it just select the next ID from the last one to be overwritten without even checking for a vacant track. (However you can specifically choose which track if you want)

### Concurrency

- Both has the same concurrent count restriction, but the difference is just that
`SoundPool`

request tracks as you play upto`maxStreams`

(fast track is not a priority, but getting a track that can play that audio) while Native Audio request them all upfront. (try its best to get a fast track). So it is not true that Native Audio can play less concurrent sounds than`SoundPool`

. It is completely in the same system and restrictions because both does not have any mixer. Mixing with multiple tracks is analogous to buying 3 PC just to play 3 songs at the same time. Unity’s way is mixing with application code to 1 track, adding latency. - Also for your information, ANA has a default of 16
`maxStreams`

on creating the`SoundPool`

instance. You can achieve the same thing on Native Audio by using 16 tracks on the`NativeAudio.Initialize(intializationOption)`

, you would get around 4–6 fast tracks and the rest are normal tracks.

![](../../assets/a48cc95ba2d27f38.png)

### Functions

- For
`AudioTrack`

, there’s only play, stop, load, and unload. There’s no such thing as pause, resume, loop. It is up to how you manipulate just those elementary functions to “simulate” pause, resume. Also changing playback rate requires destroying the track and create a new one. `SoundPool`

can pause, resume, set rate (speed up/slow down), and loop. Native Audio can just stop, and a basic pause/resume/ loop. It will not support setting a play rate because it is in the blacklist of fast track. If we enable a variable rate function that track can’t be fast.- Choose
`SoundPool`

when you want these auxillary functions more than latency.

`SoundPool`

abstracts all the `AudioTrack`

shenanigans away from user but under the cover spawn them dynamically, making the user feel like they can play unlimited number of overlapping sounds. Native Audio cares about fast track the most, so it has to make all `AudioTrack`

s upfront and try to fit all loaded audio to be compatible to those tracks.

## Unity 2019.1’s latency improvement

Exciting news is in the patch note of 2019.1.0a7! Please read this separated article for the details. But in summary, Unity no longer make strange decision of choosing 24000Hz and put the track in deep buffer thread on some phones affected.

**Unity’s Android audio latency improvement in 2019.1.0***Spicy news! Unity 2019.1.0a7 appears and in the release note, for the first time in forever, “audio latency” was…*gametorrahod.com

And finally the most scary thing about Android :

How can we be so sure, that hundreds of other devices out there now and in the future will not have any other strange behaviors than what we have discovered so far?

That’s all. Thanks for reading! I wish I can come back to update some more if I manages to add AAudio to Native Audio but it won’t be soon. At least until Android P arrive and I buy some Android One phone. (So I get a guaranteed Q + R update) EDIT : I got the Xiaomi Mi A2 !!

## A talk at Unity Bangkok

I have submitted a talk at [Unity Bangkok event](https://www.eventbrite.com/e/unitybangkok-2018-tickets-49373492445) and got accepted. It is a 1-hour skimmed version of this article to raise audio awareness (I feel like a cult leader now). It was a good experience! Even though some of the audience have a face that says "player nowadays play with sound off dude.."

I have uploaded the slide right here, but by the time you have read the article to this point you have already know everything the slide could offer and more. You might want to look at them for fun?

Some memorial photos :

![](../../assets/73b8fb29c2c15e7c.jpg)

![](../../assets/35afb5b8a04d56bd.jpg)

![](../../assets/5d04e6e628dd30ea.jpg)

![](../../assets/fa92686bec50c8bc.jpg)

![](../../assets/77a69a9bcdd3a733.jpg)

## Acknowledgements

The version 2.0 of Native Audio, which the pain and agony of making it cumulated into this article, is not possible without **PuzzledBoy/PZB**, once a customer of Native Audio v1.0. He come to the Discord channel to discuss about performance problem of Native Audio and how other solution didn’t help either.

I have no idea how to do the Android part better other than abandon everything, go OpenSL ES, and hope for the best. At that time I have never thought I would encounter so many problems with 0 solution on the entire internet, and then I decided to start this article as a journal. Surprisingly it keeps growing, the frustration never ends. I hope it can be that light someone like me 2–3 months ago desperately need for tackling Android audio + Unity.

Without that request the Android part of Native Audio would forever stuck with Java AudioTrack class implementation and I would not have the self drive to learn all of this. Also part of the drive is that my game would also be affected by the performance problem if I don’t fix it and I feel the responsibility for both my game and my customer. (All plugins from me are active in my own game, I can’t ignore bugs.)

What’s funny is that I correctly predicted that he could be from a team that make a recently released music games, which I also get a private open beta invitation via e-mail even before we met on the Discord. Being a fellow music game programmer the talk went very smoothly and every hours I spent on Native Audio will both improve his game and my own game at the same time.

Also he has many magical Android phone which produces all sorts of problems. (That’s great!) We worked together very closely. I sent an APK to him, he return with some logs for me to hunt down more problems. Tiring, but it was very fun. His game is going forward very strong (also I am honored to be [metioned in the credit screen](https://twitter.com/5argondesu/status/1028515157364731904) :P) and I wish I could follow by releasing my game soon with this new Native Audio! Maybe in the future a collaboration is possible? (daydreaming)