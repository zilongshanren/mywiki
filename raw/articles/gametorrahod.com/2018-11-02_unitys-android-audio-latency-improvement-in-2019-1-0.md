---
title: Unity’s Android audio latency improvement in 2019.1.0
url: https://gametorrahod.com/unitys-android-audio-latency-improvement-in-2019-1-0/
author: Sirawat Pitaksarit
published: '2018-11-02'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

Spicy news! Unity 2019.1.0a7 appears and in the release note, for the first time in forever, “audio latency” was mentioned!

![](../../assets/e06fa40514b3f87d.png)

For very long time, I have been reading all patch notes carefully looking for audio latency improvements to no avail that I decided to make a plugin to skip Unity altogether. This is one rare moment that deserves an article, for sure.

**Native Audio - Lower audio latency via OS's native audio library.***Native Audio is a plugin that helps you easily loads and plays an audio using each platform's fastest native method…*exceed7.com

For a refresher about Android’s audio with Unity, I recommended you to this hour-long article about my research into it.

**Android Native Audio Primer for Unity Developers***I will demystify the “black box” surrounding the Android audio system and analyze why Unity’s way of using it makes…*gametorrahod.com

I got a phone which I am quite sure is slower than average, the Xiaomi Mi A2. This phone is just recently released and is not a low-end phone, but with extremely high Unity audio latency. (acceptable audio latency once skipped to native, a whopping 321.2–78.2 = 243ms difference)

The Mi A2 likely received AudioTrack treatment, we will see what improvement Unity has this time. Additionally I still have the Xperia Z5 which will be tested too, but that phone has an already acceptable Unity latency.

![](../../assets/a97d61e94296654c.png)

For a recap, Native Audio forces OpenSL on all phones without mixer but utililze multiple OpenSL tracks for last-stage mixing. Unity in the case of OpenSL enabled, uses just 1 OpenSL tracks but mixed audio stream from the application level together for that track. This allows much more “virtual tracks” to work with inside Unity at the expense of having to mix/create a new summation stream for the final output.

## The test

As usual, I used a “nail sound recording” test to find out the difference in latency. It works by positioning the device at the same position and hit the screen loudly, recording the peak difference of nail’s sound and response audio coming from the phone going to a fixed position microphone. The settings for Unity’s audio is “Best Latency”.

![](../../assets/a5972bef62e1d550.jpeg)

![](../../assets/513cd7c31a22f8b6.jpeg)

The number alone means nothing since it is not a standard latency measurement, but the difference of this number is definitely the latency improvement. The test must be done without connecting the cable because that adds static charge and randomly includes touch latency.

That test app is actually a demo of Native Audio available for free [in the home page](http://exceed7.com/native-audio/), but it was built with pre-2019.1 Unity. You could try it on some phone you suspect is getting Java AudioTrack to see how slow it is. (I guess I should upload a 2019.1-built version later too for comparison)

## Result

Impressive! On the Xiaomi Mi A2, the reduction from previous Unity version is an insane -200ms ! (If skipped Unity completely to native, -317ms)

On the Xperia Z5 there’s no meaningful improvement, indicating that the phone is already using OpenSL ES in the version prior.

![](../../assets/cb7049c77db7c7d4.png)

Here are “android audio spec” for both phones.

### Xiaomi Mi A2 (Released 2018 / Oreo 8.1.0)

`Native Sampling Rate: 48000 | Optimal Buffer Size: 192 | Low Latency Feature: False | Pro Audio Feature: False`


### Xperia Z5 (Released 2015 / Nougat 7.1.1)

`Native Sampling Rate: 48000 | Optimal Buffer Size: 192 | Low Latency Feature: True | Pro Audio Feature: True`


## What’s happening!?

Of course I am not fully satisfied with just the result. Let’s find out by looking into the native audio track settings Unity got this time. We once again use this command :

`adb shell dumpsys media.audio_flinger`


### Unity 2018.3.0b7 ’s track

Immediately after opening a Unity game, 1 track has been allocated.

![](../../assets/b92104d10b987756.png)

![](../../assets/c17a4d1c926a933a.png)

But Unity is not so smart. The first (good) output thread with 192 frame count, 48000Hz sampling rate matching the phone, fast track enabled is currently occupied by **your phone’s track **and not the Unity game. (Confirmed with the client PID 2297, which is not Unity game and its active status of “no” even though I tried to play some audio)

But Unity’s track ended up in an another thread with whopping 1920 frame count (10x !), sampling rate suspiciously mismatching the track ( SRate 24000 ), and the thread got AUDIO_OUTPUT_FLAG_DEEP_BUFFER even. This flag is related to power saving feature, it is the complete opposite of low-latency. This result is the same as in [my previous research article.](https://gametorrahod.com/androids-native-audio-primer-for-unity-developers-65acf66dd124)

**Unity 2019.1.0a7 ’s track**

Immediately after opening a Unity game, 1 track has been allocated. But this time Unity get it right! The track is together with phone’s default track with “F” indicating fast track has been enabled. This must be the sign of OpenSL ES being enabled correctly.

![](../../assets/5d2efbf5a5b4d960.png)

When Native Audio adds 2 more tracks :

![](../../assets/4c4e2fa89a44191a.png)

Hey! Now you see both my Native Audio instantiated track and Unity’s track is in the same output thread. Sampling rate is not 24000 but correctly 48000. Indicating that Unity is following exactly the best setup for the Mi A2 phone, inlining with Native Audio, and the phone, and everyone else.

Both Unity and Native Audio is of equal native performance now, the only difference of latency time you see from the previous section is then in the application level, which is unavoidable if we want the game’s engine convenience of mixer buses and effects.

## A possible change in track instantiation routine

Once, I talked in the forum with Unity team member before about Android’s audio latency :

We learned that **to be 100% safe **Unity is trusting the “Low Latency Feature” and “Pro Audio Feature” flag reported from the device completely (*edit : not completely, there are other factors [https://forum.unity.com/threads/unitys-android-audio-latency-improvement-in-2019-1-0.577594/#post-3848590](https://forum.unity.com/threads/unitys-android-audio-latency-improvement-in-2019-1-0.577594/#post-3848590)) to decide to use OpenSL ES or Java AudioTrack. And you can see on Mi A2, both are false.

`Native Sampling Rate: 48000 | Optimal Buffer Size: 192 | Low Latency Feature: False | Pro Audio Feature: False`


By the way, Xperia Z5 which has true on both exhibit a “smart” 2019.1.0a7 behaviour from any Unity version before 2019.1. Further confirm that the initialization routine probably based on these flags alone.

`Native Sampling Rate: 48000 | Optimal Buffer Size: 192 | Low Latency Feature: True | Pro Audio Feature: True`


However these flags are not based on hardware performance or anything, it is just a boolean set manually by the manufacturer after they think the phone passed Google’s requirement. If the phone is actually decent in audio latency but the manufacturer didn’t set the flag like the Mi A2, then you get hideous latency from Unity where somewhere else in the phone the latency seems fine.

I am guessing in the 2019.1 version, Unity finally can decide to use OpenSL ES even if the flag returns false *edit : The actual new requirement is that buffer size ≤ 192 will now get OpenSL regardless of the flag [https://forum.unity.com/threads/unitys-android-audio-latency-improvement-in-2019-1-0.577594/#post-3848590](https://forum.unity.com/threads/unitys-android-audio-latency-improvement-in-2019-1-0.577594/#post-3848590) but he said this is still a risky change. Yury said “we are looking into making things better soon! Our best people are on it.” and then it’s really here. Thank you for the hard work!

## Summary

I recommend all rhythm game developers to upgrade to 2019.1 as soon as possible, as these Xiaomi device is pretty widespread for its low price tag. Who knows which devices out there reports false low latency feature flag when it can actually handle low latency?

If you wish to discuss more about audio latency feel free to join the like-minded (those who cares about these little times) [in my Discord channel](http://discord.gg/8gthuWA) #native-audio. If you scroll back you can already see quite a bit of heated and constructive discussions thanks to all rhythm game developer friends!