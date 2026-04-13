---
title: Tips on game sound effect processing
url: https://gametorrahod.com/tips-on-game-sound-effect-processing/
author: Sirawat Pitaksarit
published: '2019-05-21'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

There will be an occasion where searching the net is costing you more time to find the exact SFX you have in your head than sculpting one by yourself. Especially abstract ones like magic, combo attacks, or UI sounds.

In this blog post I would like to share some useful routine I discovered so far.

## Finding ingredients

You might be wondering how the sound appears in the first place if you had never made a SFX. Well, a "synthesizer" could make an audio from nothing but what's better for beginners are **samples**.

And no, you will not be layering a lone gunshot sound and magic sound from 2 different free audio website, because that's rarely get you what you want in your head. It is **not flexible enough** that the sound is already "named".

### Starting with recordings instead of samples

Instead of samples, we will be using "recordings". Field recordings are long, unedited sound captured from real world. They are usually abstract enough for you to cut up and play with. Listen to them with a good headphone is already fun on its own!

Well you could buy some recordings, but free ones like Game Audio GDC exists and likely be more than enough. It is celebration of GDC event every year, with a collective slice from paid products organized by [https://sonniss.com](https://sonniss.com/).

This guy is also amazing : [https://freetousesounds.com/](https://freetousesounds.com/). He travel the world and record sounds. You could get them all for free, but the complete bundle is **extremely** cheap for what you get and save you some time to collect them all since he offered a sync cloud. What I really like is that he did a blog post for each one with interesting story. Well, for example read how he got his cat meow sound from Thailand : [https://freetousesounds.com/cat-meows-sound-effects-chiang-mai-thailand/](https://freetousesounds.com/cat-meows-sound-effects-chiang-mai-thailand/)

### Recordings are keyword named

![](../../assets/7bfc41668068ecab.png)

With thier abstract-ness, they are named as a collection of keywords instead. This is very useful as when you are in your DAW you could type out **what you are thinking **and instantly get the ingredients with that related sound. For example one time I want to make the stone bombing sound that one boss could use. I try typing "crack" and found some usable sound instantly.

### Record them yourself

If you are going on a trip you may find interesting soundscape. It's fine to use your phone! Don't worry about "pro" audio since you could add effects later and make them abstract. This is not like you are recording a foley for a multi-million dollar movie where it require realism.

Also even recording packs it may take too much time sculpting the sound out of them, when you realize the attack sound you want in your head could be just by tearing some papers available on the desk.

Here are some tips I found :

- Be alert of your mic position, or which hole on the phone is the mic. It's no good when you get back from 800 km beach trip and discovered that all your recorded footsteps-on-sand sounds are off to the side and you realize you was not holding the phone on your crotch.
- Realize if you have a running nose, hold your breath while recording if possible. Or recognize any other your habits that make a sound such as clicking your tongue, etc. Sometimes I made strange sound without realizing since it became a habit. They will show up in the recording.
- Wind will kill your phone recording with nothing but exploding bass. You can put the phone in your shirt to prevent this if you don't have any other proper windshield like a sponge or a "dead cat". (feathery stuff that redirect winds)
- Try new mic positioning. When I record a walking sound of myself, I try putting the mic closer to the foot. My walking posture became funny but the recording came out great.
- You could left the phone alone for a while then pick it up later. It's better than holding the phone, get tired, and cause some unnatural sound when you move around.
- Pay attention to "far away" sound. When you are in the mountain for example and you want to record birds and leaves, you will start hearing something undesirable like construction sound echoed from very faraway town, or some motorcycle speeding from somewhere. Strangely you didn't notice these noises until you really want to record something.
- Name them immediately after the record. You will get lazy to re-listen to them what they are later and could mean a dead project.
- A new world of sounds is waiting for you if you make a contact microphone :
[https://www.instructables.com/id/Make-a-Contact-Microphone/](https://www.instructables.com/id/Make-a-Contact-Microphone/)or upgrade to Hydrophone so you could dip it in water for that water magic attacks :[https://flypaper.soundfly.com/produce/how-to-build-a-diy-hydrophone/](https://flypaper.soundfly.com/produce/how-to-build-a-diy-hydrophone/)

## Make something

This article is not for this, so go nuts with whatever DAW program you have! I have some tips though :

- Cutting and pasting interesting chunks on the timeline. Sometimes just spacing them out produce much more interesting sounds.
- Add EQ if something sounds unusable.
- Add some high boost to make things "exciting" for games.
- If you are about to ditch the sound because you think it wouldn't ever become what you want and it is better to search for a new one, try adding destructive effects like guitar effects, reverb/echo with insane parameter, flanger, bit crush, etc.
- If that is still not it, try reducing the volume and use it as "details" instead, then find a new "main" ones. You may end up with rich SFX. These details could be panned to extreme left and right to create interesting stereo accompanying main one on the center.
- It is useful to work together with a reference video from the game as you could know the sync and you could test if it really fits with the visual or not. Most DAW could play a synchonized video while scrubbing timeline. If your video looks buggy in the DAW, try following
[this article](https://gametorrahod.com/preprocess-a-reference-video-for-working-with-ableton-live/).

## Post processing

Finally we have arrived at what I want to say from the beginning. For **each **sound effects I found this effect chain useful. This is Ableton Live, but they are available on every modern DAWs.

When you are making 1 SFX, you may have to layer up multiple tracks that has audio clips that are positioned differently. So group them up by whatever group track feature your DAW could do, then prepare a final chain of effects on this grouped track.

![](../../assets/8629f92ac3101899.png)

The game in this screenshot is Pandora Hunter, an online mobile turn-based boardgame-like game : [https://www.facebook.com/PandoraHunterGame/](https://www.facebook.com/PandoraHunterGame/)

### Equalizer

First put an EQ with 3 controls :

- First one is high pass (= low cut). You might like how "bassy" your SFX sounded, but imagine in the game that they will have to compete with BGM. I always put highpass filter because I don't want it to clash with BGM's kick drum. Only if you have a specific design then you can leave the bass in. (Like a chill game with mostly ambient soundtrack, then you could fill in the bass with SFX)
- The 2nd one is a dip node for surgical cut. This has a high Q value so it forms a specific valley instead of smooth slope. Use it to dip out "annoying" frequency. If you couldn't find the problem, just move it left and right until it sounds great lol
- The 3rd one is a high shelve filter to boost brightness. (in audio "bright" refer to higher frequency). I found that most recordings are "dark" by default (especially if not synthesized but from real recordings) and usually doing this make things better 90% of the time. It also help the sound to "pierce the mix", ensuring it could be heard no matter how busy the scene may become. This is good for UI and notification sounds. The iconic "hit registered", "kill beep" and "headshot dink" from a game like Overwatch are mostly dry, high frequency content.

### Frequency Compressor

The second effect is a specific frequency compressor (called Multiband Dynamics in Ableton Live). This works like the 2nd node in the EQ to cut off annoying frequency, but this time do so only if they get excessive, so you don't lose that detail when they are not annoying (yet).

The most common problem for this is some kind of combo attack SFX, because they contained many audio blended together it is getting difficult to tame individual sound. For example, I am making a magic sword SFX where it has electric sounds (rather bright) at the beginning and end with an even more bright slash. The slash is kind of hurting the ear because the attack is sharp at the same time as the frequency is high, but reducing high frequency with EQ would destroy the electric sound that is already fine. By using a frequency compressor, it will only activate when the sword sound came since it went over the threshold.

### Convolution Reverb

![](../../assets/e3afaf95c75009c4.png)

Adding a **thin **reverb is for fixing that "hmm...". Usually if something sounds almost good, a reverb make it complete because it kinda blend things together like putting herbs at the end of cooking. But stay with low Dry/Wet ratio or you could lose your audio's character fast.

A convolution reverb draws reverb character from the real world, you capture impulse response (IR) from some room by clapping hand once for example and use it with this effect. You could put regular reverb instead of convolution, but a convolution allows you to scroll through different impulse response until it sounds good. The "repeat something mindlessly until it clicks" workflow is always good for lazy person like me!

### Stereo Control

There are 2 cases, the audio sounds too centered and boring then you could use the "imager" effect to widen it up, or something sounded too spread out that they are no good for mobile game when the player is not wearing the headphone, then you could narrow it down.

### Maximizer + Limiter

After this, put a limiter which prevent your audio from going red and cracks. Before the limiter, pump up the volume so it is as loud as possible without losing character you want. (Or you want that "slammed" character you could push more)

The reason for maximizing each effect despite what they are is because mostly in game engine you cannot increase volume, just decrease. It may sounds strange if your leaf sound that should be gentle souded obnoxious right now, because you will mix it to reasonable level in the game. Do not try to mix here.

### Gate

![](../../assets/c8093765f8e723b6.png)

If you made your sound "too epic", you may notice you now have problem where to cut off the audio to save out the file. Usually these reverb tail is too long and not going to be heard by the player anyways when together with BGM, so it is a good idea to cut off the tail earlier than they would have slowly fade out.

Cutting them out sharply is possible and wouldn't be that noticable, but it's better if the whole process is automatic. A Gate is an effect that could detect if audio went under a threshold, it should be cut off. This cut could be smoothen with Release so it produce a gentle slope like the green arrow instead of sharp cut. The red arrow shows what it would looks like if I didn't add the gate. If you do this to all SFX, you will ended up saving a lot of game's space! It may sounds uglier right now but remember that players rarely will be hearing the effect in isolated environment like you do now.

## How to render out the audio effectively

You may design multiple SFXs in one project. Then, you notice you have to select each SFX region and render them, like this :

![](../../assets/fda9f991020ea584.png)

But it is a hassle to do this on each SFX and have to be careful about that silence on both sides, especially at the beginning where it could add perceived latency on your audio.

What's better is just design a SFX on each track as you like, render out all tracks separately so it produces a lot of wasted space at first. Here, I have a reference video running at top so they ended up waterfall-y. Each track will contain a bit of SFX audio somewhere on its long range.

![](../../assets/be7f230712a61756.png)

Then, use a batch tool to trim out silence from both end of each track. I think [Audacity](https://www.audacityteam.org/) has a batch window and you could use "trim silence" or something. But I prefer command line so I use `sox`

. ([http://sox.sourceforge.net/](http://sox.sourceforge.net/))

I learned how to trim with `sox`

from this page : [https://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/comment-page-2/](https://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/comment-page-2/). In short, it is something like :

`sox in.wav out.wav silence 1 0.1 0.5% reverse silence 1 0.1 0.5% reverse`


Combined with Bash batch command to do it to all audio in the folder :

`for a in *.wav; do sox "$a" "${i%.*}-processed.wav" silence 1 0.1 0.5% reverse silence 1 0.1 0.5% reverse; done`


`%`

operator will cut out trailing `.*`

from your file variable, which would be the extension since the pattern is "dot then anything" (It is not the dot wildcard as in regex). Then I could add a suffix and restore the extension back.

And yes please export in a big `wav`

as they could then be compressed by the game engine later. You will have more choices in exchange of your disk space. (not the player's device space)

![](../../assets/cb635b76ef78c045.png)