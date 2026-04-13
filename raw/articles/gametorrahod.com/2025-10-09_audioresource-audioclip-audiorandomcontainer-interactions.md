---
title: AudioResource, AudioClip, AudioRandomContainer Interactions
url: https://gametorrahod.com/audio-random-container/
author: Sirawat Pitaksarit
published: '2025-10-09'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

Long time no see. I'm currently trying to make a SFX player audio plugin based on `AudioResource`

, a new base class that covers both `AudioClip`

and `AudioRandomContainer`

(Unity 6 addition). I have several questions that the document didn't go into details that I had to research myself. I hope this article can impart this niche knowledge to those interested.

I'll start with reiterating prior behaviours first. (The gang consists of : `AudioMixer`

`AudioMixerGroup`

`AudioSource`

`AudioClip`

) Then I'll get to the `AudioResource`

and `AudioRandomContainer`

which is our new stuff whether they conform to the previous functions or not.

Small notes : There are graph time scheduling bug on `AudioRandomContainer`

plays when I test it on 6000.0.50f1, where pausing the game time or the editor will mess with its pulse/offset feature causing it to "miss" the schedule. It seemed to be fixed in 6000.0.59f2. So if you are still on older version please update before playing with it.

## Test Set

![](../../assets/123666c025c89617.png)

For audio memory testing, I'll use this long audio file with 10 MB original size and 3.8 MB compressed size. And I'll change up Load Type and Preload Audio Data on each study.

I also have a shorter 1 second file when the test requires a play to end.

## AudioMixer and Profiler

In a 2 `AudioMixer`

setup `MainMixer`

+ `SubMixer`

, where `MainMixer`

has several of its own `AudioMixerGroup`

, and one called "From SubMixer" that gets the audio from `SubMixer`

.

![](../../assets/49c1503581c5ffa4.png)

![](../../assets/d39a740bef216b8b.png)

They are presented in the Profiler like this (showing 4 play one shots currently playing under one of the mixer group) :

![](../../assets/7a571fe382ae82f1.png)

## AudioClip Memory

If scene has asset reference that eventually leads to `AudioClip`

and it has Preload Audio Data, then it takes memory immediately. How much depends on Load Type. Streaming Load Type cannot have Preload Audio Data.

If Preload Audio Data is not checked, then it is loaded on its first play.

`audioClip.UnloadAudioData()`

can unload audio that was loaded with Preload Audio Data.

`Resources.UnloadUnusedAssets()`

can work similarly to `audioClip.UnloadAudioData()`

without the need to have `AudioClip`

object reference. But the definition of "used" is by following objects in memory, and that means everything in the hierarchy are considered used. `Resources.UnloadUnusedAssets()`

cannot unload the audio memory if some `GameObject`

is still referencing it, even not actually playing it.

## AudioSource.PlayOneShot

The argument is still `AudioClip`

, not `AudioResource`

. Therefore you cannot use `RandomAudioContainer`

this way. Understandable, because it is possible to configure `RandomAudioContainer`

to be infinitely repeating according to the playlist.

In the Profiler, stacked `PlayOneShot`

of the same long `AudioClip`

shows up as new "Audio Voices" without incrementing "Total Audio Sources".

![](../../assets/a25ed966cc83f294.png)

By the way, this "Audio Voices" is what will be subjected to culling according to Max Real Voices in the Project Settings.

![](../../assets/c5724c3bf85fa768.png)

If `audioClip.UnloadAudioData()`

is called while `PlayOneShot`

of that `AudioClip`

is playing, it automatically stops all such one shot instances and the memory is unloaded.

While one shot audio are ongoing, changing `AudioSource`

's Volume, Pitch, `AudioMixerGroup`

output will live update all of the running one shot instances. This shows how I can move all the one shots to another place in the mixer tree at once.

![](../../assets/33b5ec96b5139973.png)

![](../../assets/4ee282b105289bc8.png)

On Load Type : Streaming, it seems to take fixed amount of memory (124 KB) to stream the audio no matter how long it is. It has a disadvantage that each stacking one shot instance will need its own 124 KB to stream concurrently, compared to Compressed in Memory or Decompress on Load that each instance can share the same memory. The 2nd image shows that streaming memory is now 248 KB for 2 consecutive streaming plays.

![](../../assets/f484fd1e3dffed6e.png)

![](../../assets/871fb2dd6873307f.png)

## AudioRandomContainer

With a default `AudioRandomContainer`

that plays 2 clips back to back:

![](../../assets/6337dcb55500616c.png)

The Profiler shows interesting technical aspect that is happening under the hood.

For any `AudioSource`

that had played `RandomAudioContainer`

even once, it starts managing an invisible audio playables called `AudioPlayable Group`

, revealing that the "backend" of `RandomAudioContainer`

is probably playable graphs. If I attempt to change `AudioMixerGroup`

, even if `AudioResource`

is removed from the slot, the Profiler shows that this `AudioPlayable Group`

is being moved to different part of the tree automatically.

![](../../assets/ae4566eec1985fab.png)

![](../../assets/4b6cc7ab1d537fec.png)

Unlike Play One Shot or Play on `AudioClip`

, the Object name is blank for any plays that occured within `AudioRandomContainer`

. This image below shows "Channels" mode without the groups so you can see that the name is blank. I play both `AudioClip`

way and `AudioRandomContainer`

way at the same time.

![](../../assets/6d2b31ea8f01320f.png)

Moreover, pausing Unity editor will remove the blank name channels from the Profiler on that frame. Because inspecting the Profiler automatically pauses the editor, you need to move the frame head back by one frame to see the audio played as a part of `AudioRandomContainer`

you want to see.

It appears that there is a short moment where Audio Voices count is 2 while transitioning to the next clip, despite the container didn't allow the clips to overlap.

![](../../assets/71ad7d4c5bbe1291.png)

![](../../assets/56fc2396af18eb6e.png)

![](../../assets/2504b1739eb2528e.png)

One more interesting thing is that, while the first sound nest the channel under `AudioPlayable Group`

, at the overlapping moment, and even after, you can see there are one more nested layer of `AudioPlayable Group`

. It seems there is a complex logic that decide how many playable graph group it needs under the hood to run. It should not affect performance, just make this tree a little bit cluttered.

If we allow short break on the transition, the Profiler now shows a more expected graph which the Audio Voices dropped from 1 to 0 and then back to 1 when the next clip plays.

![](../../assets/23a8b801a14d11ab.png)

![](../../assets/436ad6cafc673986.png)

If you are going crazy on back to back plays, it might worth keeping in mind that short instance where Audio Voices are bloated, just in case you might be close to hitting the limit.

`audioSource.Pause()`

and `Unpause()`

works as expected, if you pause and unpause repeatedly, it will go forward in the sequence bit by bit, including the wait time.

As for memory usage, it seems to do it clip by clip as expected. For example, I have sequential ARC of 10 MB each like this, with Preload Audio Data as false. It correctly starts as neither loaded. And when the ARC is played, only the first one is loaded because the 2nd is scheduled to be played with offset after the first one.

![](../../assets/5fc8b48eb40dc435.png)

The `audioSource.Play()`

while ARC's Trigger Mode is Manual has a self-overlaying effect similar to `PlayOneShot`

. This is very different from `.Play()`

while the asset is `AudioClip`

which when called repeatedly, it would just abruptly stop and restart the clip. This example shows `.Play()`

called consecutively 4 times, while Trigger is Manual and Playback is Sequential. It results in C and E graphs being added 2 times each. (4 total) Basically `.Play()`

fires a trigger once.

![](../../assets/14a363f4e9b11579.png)

![](../../assets/0e8174371c758f56.png)

`.Pause()`

and `.Unpause()`

is able to altogether pause all overlapping instances and resume them in one go. Pretty cool actually.

When Trigger is Automatic, it works more like it was previously. Repeated `Play()`

call will restart the whole playlist. For example if it is halfway through "E" and `Play()`

was called again, the E audio abruptly stops and it starts over from the beginning of C.

`AudioRandomContainer`

is also currently not very extensible. The class is `internal`

unlike `AudioResource`

and `AudioClip`

. And attempting to use reflection or direct `.asset`

file writing might be brittle because they don't want you to do that. This is a YAML file of an ARC. Each element added to the `AudioClip`

array is in fact not just `AudioClip`

but `AudioContainerElement`

, because it needs to hold adjustable volume and enabled checkbox per entry as well. Notice how `m_Element`

links to each `AudioContainerElement`

with `fileID`

. ([Related article](https://unity.com/blog/engine-platform/understanding-unitys-serialization-language-yaml))

![](../../assets/4c1efba54f4c271f.png)

Because `AudioRandomContainer`

is entirely `internal`

you lose control on `AudioClip`

that it is made of, for example what if you want to `audioClip.UnloadAudioData()`

to everything that's in the playlist of `AudioRandomContainer`

?

The manual loading and unloading of non-Preload Audio Data clip I think is a critical feature in competent game. In loading screen I'd load all the expected audio so it doesn't introduce unwanted hiccups. The most memorable case for the game I worked on is level up SFX. It's not often that the player leveled up, but it is a very important feedback sound. The fanfare is also quite long so if I didn't preload it, it is guaranteed to skip a few frames of beautiful level up animation. Now imagine that if I went all in to `RandomAudioContainer`

and have a level up audio that would be randomized from 2-3 variations. Because the API provide no `public`

way to access those 2-3 `AudioClip`

from `AudioRandomContainer`

, I'd need to separately have reference to them elsewhere, or use reflections. This will quickly complicate things when the game has 300+ sounds each with 2~3 randomized variations.

## What about my plugin?

Around 2022 to 2024, I have been developing an audio plugin where it plays everything with audio playable graph. It supports volume, pitch, sequencing, start midway, and chaining up audio playable assets endlessly, etc. It's almost the same feature set you see in `AudioRandomContainer`

right now. I see right away because you are not supposed to be able to play multiple audio with different pitches on `AudioSource`

because adjusting that affects every currently playing audio in real time, unless you do it as playable graph and use the pitch argument in one of the node that's on different branch from the others that goes into the mixer.

My plugin uses concept similar to `AudioRandomContainer`

, able to wrap each `AudioClip`

in a new container that allows per-clip volume adjustment, randomized play, and whatnot. And the name is more generic `AudioSet`

/ `AudioObject`

because sometimes it is not supposed to random things. But it has editor tooling to automatically wraps every single `AudioClip`

into the wrapper asset. As a bonus, if you named your audio clips like `Foo-1`

`Foo-2`

`Foo-3`

you get only one `Foo`

wrapped asset that is already setup to randomize the play between 3 versions. It also has a base serialilzable class just like `AudioResource`

.

I took like 1~2 years to finish the plugin, **only to discover that **in production use when I put my playable-backed SFX slinging engine to test I was flooded by undebuggable FMOD warnings and sometimes runtime error. I had to pivot my plugin hard so everything is played by the old `PlayOneShot`

. Many code documentation about making regular person understand what playable graphs are were already written however, that I have to soon discard them.

Today now that I discovered `AudioRandomContainer`

will end up connecting the audio graph I'm not having very good feeling about this. `AudioRandomContainer`

looks great even if to just wrap a single `AudioClip`

just so you could access its per-asset volume attenuation. But can I really bet my entire game's audio on this?

At one time (2 years ago?) the plugin wire up playable graph like how ARC is doing here. But Unity is so buggy with it (e.g. FMOD error spam I can't make any sense when a lot of audio is played through playable system.) It is clearly not something I can sell to anyone. I actually had my own cases that was unresolved, but since they decommissioned fogbugz and I didn't capture any screenshot I have nothing to show you other than these.

[https://fogbugz.unity3d.com/default.asp?1259935_h4lbeo17t8685ksl](https://fogbugz.unity3d.com/default.asp?1259935_h4lbeo17t8685ksl)[http://fogbugz.unity3d.com/default.asp?1167289_7t1ofosrlthhs3eo](http://fogbugz.unity3d.com/default.asp?1167289_7t1ofosrlthhs3eo)

I had to implement "compatibility mode" that turns the entire plugin into essentially `PlayOneShot`

machine. (This was before the plugin was named "One Shot Framework" and more like SFX Framework) Then life happened, fast forwarded to Unity 6 they came out with what was said in this article. Now, I want to continue developing this plugin, I'm thinking should I use `AudioRandomContainer`

instead of "my class" for the wrapper? Or at least base my base class on `AudioResource`

instead of my own?

After this entire research, the answer is likely no. The whole thing looks feature rich, but inextensible and I had trust issue to commit into it with reflections and direct `.asset`

file writing tricks.

Slightly related, when I test it (2 years ago?) anything audio playables are broken in WebGL build despite this page [https://docs.unity3d.com/Manual/webgl-audio.html](https://docs.unity3d.com/Manual/webgl-audio.html) saying nothing about them. By the way, that page also promises `PlayScheduled`

being supported in WebGL build, which my plugin [Introloop](http://exceed7.com/introloop) heavily uses, but schedule ended up buggy and unusable.

## My Evaluation

`AudioRandomContainer`

looks very feature-rich and almost made me wanted to wrap every single `AudioClip`

in my project into `AudioRandomContainer`

. But the opaqueness of the class and how it is playable-backed made me hesitate. The asset being only able to create one by one by hand reliably also discourage me from using it. What if I spent time setting everything up in ARCs and now I found the same FMOD errors later?

For now I will **recreate **a similar `AudioClip`

wrapping system, except that it should eventually leads to the battle tested `PlayOneShot`

. It's too risky to go all in on ARCs right now. The first step I'd like to see from Unity would be making the class not `internal`

. And at least each `AudioContainerElement`

should be accessible by script.