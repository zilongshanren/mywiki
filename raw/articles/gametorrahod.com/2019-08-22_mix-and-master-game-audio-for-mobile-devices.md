---
title: Mix and master game audio for mobile devices
url: https://gametorrahod.com/mix-and-master-game-audio-for-mobile-devices/
author: Sirawat Pitaksarit
published: '2019-08-22'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

## The problem

I am currently on the final phase before I could release my Duel Otters v2.0, it's the audio. There is a "bug" in this, specifically the snares of my new songs were too hot. I could hear nothing but snares and it is overpowering melodies. But they sounded fine on my ATH-M50 headphone, of course.

Bass also disappeared but I am not surprised. However I wish I moved the bass up the frequency range a bit so maybe players could faintly hear them. Amusingly the old songs I composed when I was a noob are in fact translated very well! Back then I have no idea what is the proper brightness and made the song too dull on headphones. It turns out balanced on mobile phone's speaker!

This is **mastering** problem. I wish I could test my song with as many phones as possible. (the same treatment as hunting bugs on your actual game)

Also I have to preface that **I am not an audio engineer, **my degree is unrelated, I don't have studio equipments, and I am all Google-taught about audio. So don't take this article as a professional advice. But as an indie dev sometimes we have to fix things as far as we could (...for free). Even though when you send your audio to a real engineer and they may say it's still shitty. I hope this for-programmer guide could make you a makeshift (game) audio engineer.

## Finding the workflow

Of course I am not satisfied with having to build the game and put in in the phone, and then go to that screen in the game, to finally notice that the high ends were too loud. That's a massively big turnaround time for an interactive / trial and error task like this.

The shortest path from my DAW (Digital Audio Workstation, basically a kind of program that made the song) to phone's speaker I could think of is exporting the file to Dropbox folder then use Dropbox app from the phone to preview it. It is a hassle as you might imagined despite the synching technology. Then I realized I don't want to export because it stops the audio and breaks my flow.

Then the next idea is maybe I could put some EQ or emulations in the DAW. There is even a plugin called M-Ref to do this : [http://www.m-ref.com](http://www.m-ref.com/) , but maybe you don't trust it or you want to hear it jumbled with room noises instead of from your headphones.

The idea workflow is to press spacebar in the DAW and somehow hearing that audio from the phone instead of your headphone, or better both at the same time.

One wacky idea is to find a cheap or broken Android / iOS then rip off the speaker, solder some low gauge cable to the speaker, and line output from your computer. It probably requires some amplifier or power source, and also [here the author of M-Ref said that](https://www.gearslutz.com/board/showpost.php?p=12117652&postcount=32) the phone contains a lot of DSP chain you still need to emulate, if you managed to make your ripped speaker works it is still not the real thing your player will hear.

Then finally I think I should just find some application that broadcast wireless audio with the receiver on the phone side. Searching the internet usually returns an inverse because people wants to sends an audio **from **their little phone to bigger speakers instead of crushing audio **into** crappy phone speaker.

So, I hope this article can catch searches in the future, and I present a solution **Airfoil** to achieve this. Also I have no affiliation with them. (It would be great if they give me something!) But first, terminologies.

## It's easier in the mixing phase

Before you master your track, you do what is called "mixing". It is to get loudness of all instruments and tracks right together.

Usually this calls for various tactics such as EQ to make room for others, panning to make space, or chaging volume dynamically to avoid the other tracks only when required. After this you produce one audio with a single track. Then mastering begins.

When you try to do some gymnastics in mastering phase, maybe the solution is as easy as moving that snare fader down a bit and call it a day. In mastering phase you affect other tracks as a whole so you may create an another problem. And therefore it is very useful to **mix on the phone's speaker, **which an application that I will introduce later could help you.

## What is mastering?

The goal of mastering an audio is to make your finished product translate well to as many audiences and mediums as possible.

This depends on the media your listener will use too. For example, if your song will be for arcade games maybe you have to hear how it interacts with loudspeaker's character and big location's reverb, because it may dilute the volume. I once got my song in a dance game Pump It Up via a competition, and I camped at the arcade in the morning on the release day because I want to play my own song the first. But it turns out that the song sounds not as impactful as other competitor's songs.

If I am not living in a dorm and have an actual speaker monitor maybe I could master more accurately for dance game, even though obviously that is not a real dance cabinet in my house, but at least it is a speaker. Also I may have to think how player's footstep may interfere with the song. If you achieve this, it is said that your song "translates well" to other media. (well-mastered song)

Mastering should have some kind of purpose as well. Catch-all master is usually a master of none. For example, OST (sold separately) from the game that maybe originally a mobile game is mastered "for OST" and aren't the same as the audio that you may rip from the game file. Those were mastered "for game".

In this article I will talk about mastering "for mobile". This means you have 2 targets : for players that uses headphones (that comes with the phone, or higher-end), and for players that use the phone's speaker. Usually accounting the phone's speaker is more important.

Or maybe you could skip that and add a screen at the beginning that says "best experience with a headphone" like most music games did. That means your game wasn't mastered for mobile speakers and you are not responsible if it sounds crappy or unplayable on speaker. (For example, if you add a playable note for bass sound that ended up looking like imaginary notes to player without a headphone, now it's not your fault.)

Though, this article assumes a casual game where it is more likely that players will **not** use a headphone. Or have the audio off and not affecting gameplay at all, in that case please keep in mind you are making the sound designer sad.

### Volume

Usually this means maximizing the volume as much as possible while still sounding good, because listeners do not like to repeatedly adjust his volume when your song arrives. Maybe you need to listen to other's music and try to "compete" with them. This results in the [Loudness War](https://en.wikipedia.org/wiki/Loudness_war).

**But in mobile/console games, **volume is of less importance since you are in control of everything in your game, and the player usually **willing **to adjust his phone's volume for your game, once or twice.

Make your game sounds equally loud is still a requirement but there is no problem like normal music listening where music from other composers may come next to yours and overpower your music. (Unless you are making your own album, then you need to master it to sit well with your other songs in the album.)

Now there is instead a problem of phone's enclosure which filters your audio differently.

Interestingly a game Monster Hunter World I found that there is a "mixing feature" built in! So you could adjust dynamic range of the audio. If this is set to wide, then when you are not fighting it's very quiet, and it improves realism somewhat because the fight would then be very explosive. Then because I don't have a good sound system for the quiet to be audible I could change it to narrower dynamic. Also you can tune it for headphones or for speakers.

![](../../assets/bfe921c1d228c623.png)

### Frequency response

I will speak mainly for mobile games since this is where it gets difficult. Bass usually disappears on phone's speaker, but some bass with high attack/sharp transient may still be heard, like a slap bass.

Also the higher frequency usually sounds hotter than what you heard in the headphone. Maybe a bit more "crushed" as well, like it was going through saturator/overdrive effects.

This is very obvious when playing a well-rounded piano piece on phone speaker, since piano is an instrument that covers wide spectrum on its own. You will instantly recognize that something is missing or some notes disappearing, as opposed to something like trumpet which could be heard clearly on phone speaker.

### Transients

Time-dependent characteristic of a sound can be described in [ASDR envelope](https://en.wikipedia.org/wiki/Envelope_(music)). An audio with quickly, suddenly rising attack could be described as having sharp transient.

I noticed that this is exaggerated a bit on mobile speaker. My live drum kit has an especially dry and hard "head" on the snare and this character became too much on the phone.

To fix this you may use a compressor to reshape the transient since it got attack knob to rounds out the harsh head. Or maybe you can use a dedicated transient shaper effects. For example, Ableton Live has this free 3-band compressor of sorts. First I fence out the desired frequency then I could either increase or decrease the harshness of attack just around that frequency. (C/E stands for Compress/Expand, which 0 does nothing.)

![](../../assets/bd541699cbc5d135.png)

### Stereo balance - mono cancelling

Many phones under 300$ still only have one speaker, and so summed your stereo audio to mono. Even though the phone advertises it got stereo speakers it may still jumbled and sounds like mono when the audio reaches player's ear. Not to mention that the hand may obstruct the speaker. But you don't want to go as far as making everything mono!

Anyways, your carefully panned audio that sounds fantastic on headphone may **cancel each other out**. This may call for a narrower mix.

The easiest is to mono the bass frequency since stereo bass usually sounds funny. The Utility effect of Ableton Live even has a button "Bass Mono" to do exactly this.

![](../../assets/8653c4373988bcfe.png)

If you own mastering plugins, then usually it's on on the imager section.

![](../../assets/0c7d25de73bc78f8.png)

Well this only works on mono-ing the bass at mastering phase. If you found this problem and want to fix by re panning some of your other instruments, you are going back to mixing stage, fix the pan, then you master the song again.

Note that mono checking could be done in the DAW without your phone as well. But still best to check on a real mono phone later.

You may try to fix the problem more subtly by managing the phase of sound wave so that the summation don't completely cancel each other out. Many plugins offer a phase shift you could try to play with, and check in mono if that makes any difference or not. When phase shifting, it is hard to notice any difference in stereo!

### Stereo balance - orientation

If you master for club music, then you may go for mono-compatible dancing music considering the sound system. (So you may try [mixing in mono](https://www.edmtips.com/mixing-in-mono/)) If you master for headphones, then you may use stereo effects and spacious mix to please the listener, or use sweeping effect that travels left and right effectively. Or if you mix for a game with surround sound system, you can make an audio coming from the player's back.

Well the thing is the speakers don't move, obviously. In surround situation, imagine if the player face away from the screen. What's coming from the back is now his front! Of course you play the game facing the television so that's very unlikely.

![](../../assets/a09e5945c99e72b2.jpg)

However for mobile phones there are landscape and portrait orientations. For landscape orientation, the stereo speakers make sense since you are likely holding the device like driving a car, and each hole sends the audio more directly to your ear.

But if your game is portrait orientation and the phone supports stereo speakers, then likely that **left is now the top and right is now the bottom **of the phone. It doesn't make sense anymore and you may as well consider this situation a mono speaker that sum your 2 channels weirdly.

What I observed is that the thing I panned to the left now sounded more "in the face" than to the right, and the right speaker (which is now the bottom) is more likely to be obstructed by player's hand. There are now some biases on the channel.

![](../../assets/47f4a6224d6718e6.jpg)

![](../../assets/c990a28792a9bb5b.jpg)

An example of how to use this findings : I have tambourines and hi hats panned to left and right without much thought, I just want them not in the center. But after hearing the music on Samsung Galaxy S10+, the tambourine sounded too pronounced and I want the hi hats to hit your face instead. So the solution is that I just switch their place.

### File compressions

Mobile games aren't going to use your perfect version of the song, since app size matters. Unity for example can compress to Vorbis, then you may choose an arbitrary compression quality for each song. So! You need to make the song sounds good on **that **target compression quality you are going to use. It likely won't be a 320 kbps MP3 equivalent of quality either, it could be much much lower since the space saving is very tempting.

If the song contains a lot of sharp, crisp high frequency elements, it is likely that you **cannot** use aggressive compression. So think, you want to waste the game size for this song, or you EQ the higher ends away to allow more compression. (High ends that got compressed sounds more "glitchy" than if you EQ that out yourself.)

![](../../assets/69b5337efe8560ff.png)

If you are not the composer, you may make him angry for having to crush his hardwork. The same way you may have to deal with the art asset artist. Luckily I made all my tracks so I could make this trade off without getting into any arguments!

If the song is for example, a leaf ambient mixed with wind blowing, I could go as low as quality 10/100 and it still sounded like a leaf.

All these also applies to sound effects, not just music. Imagine a sound of earthquake magic, that's an example of something that could disappear completely on mobile phones. You may have to make the stones crash violently instead of low end rumblings you imagined is more "proper". It won't be proper if your player didn't use a headphone.

### Pad sounds

This is a specific kind of sound in your song that is prolonged, and usually plays in chords rather than individual notes. It is usually a synthesizer, but real life instrument like bagpipes or organs can also produce this kind of sustained sound. (Organ opens holes that make sounds as long as you press the key, it is unlike piano which the key strikes the wire with a hammer inside.)

Pad sounds are usually preserved in the mobile speaker mix, but can sounds **muddier** than when you listen to it on the headphone. I guess the reason is that these kind of sound has low tolerance of going through phone case without being deformed in the air. (I feel like that, there is no scientific evidence.)

Quick and easy way to make pad sounds comes out more "in pieces" rather than a muddled mess is putting a compressor with sidechain routed to your drums to make a less busy mix. This means when the drum came, pad sounds will be reduced its volume. (Not suddenly, with attack and release slope to your taste.)

You may feel like your pad is ruined from "it's pure form" when listening on your good studio headphone right now, but you will barely notice any missing pad sound on the phone. Instead it improves clarity. Balance out the settings so it sounds good **enough **for both phone speaker and headphones. Remember, you have 2 targets of this master, not to perfect either one.

![](../../assets/21d3db318de36f10.png)

## Airfoil

Finally I found an app that make pressing spacebar in my DAW and hear it on the phone possible. It's Airfoil. The requirement is just that you connect to the same network. And it is not depending on Bluetooth, so no pairing required.

Actually there is a pairing of sorts by pressing the note with waves button, then you can also stop receiving on the phone while the computer continues sending out audio.

![](../../assets/3fa8b9030a469130.jpg)

![](../../assets/4ff2993d97fe40f7.jpg)

Airfoil experience was much more polished than I thought.

The receiver ("satellite") syncs immediately and magically to the one on my computer, with the same toggles that also syncs. (So I could toggle things on the phone as well, not just computer to phone.) The computer could also run the satellite, but our purpose the computer is the sender.

And selecting running application "just works", after you install "ACE" it asks you to. This is on macOS, this software supposedly prepares all audio to be rerouted, I think. There is no plugin needs on Windows maybe?

![](../../assets/2c97b35e4eb4b7d2.png)

However you must select your output by pressing that note with the waves button. You cannot simply blast all speakers in your vicinity immediately.

You can see "DeployBose" in the list there? That's actually not mine but a speaker in the coffee shop. Of course this speaker is not a mobile phone and has no satellite installed. But I pressed the button a bit and instantly the audio that was playing stops! So it seems to work but I quickly switched off though because I don't want to cause problems. In the web it says it works with Bluetooth devices, that's probably why it knows how to talk to each other.

![](../../assets/d86a7177a98625aa.jpg)

So press the one that says your phone's name and the spacebar DAW to phone workflow is instantly achieved. Yes!

### But it cuts off the audio on my DAW that I was listening to on my headphone

To fix this instead of keep toggling Airfoil on and off, you avoid choosing your DAW as the source on Airfoil.

Instead, use a simulated audio path like Soundflower on macOS. I don't know about Windows but there should be an app like this. This make Airfoil cut off the Soundflower audio instead.

Then, in my DAW I instead set it up to output to 2 sources, not just one. One to the headphone output, and one to Soundflower for Airfoil to take away. Now I could hear things in my headphone at the same time as on my Android phone. The problem is there is only one dropdown for choosing the output. What to do?

I don't know about Windows but in macOS one could achieve this by making a new "Multi-Output Device" and let's say please go to both headphone and Soundflower. This one virtual path now represents 2 outputs.

![](../../assets/265a411a5cb61f3a.png)

Finally I tell my DAW to use this new, imaginary multi-output device (NOT Soundflower). Done!

![](../../assets/a7a2e7516838aba8.png)

## Latency

Being a wireless application you can guess it is probably not real time. And yes there is a **massive latency of about 2-4 seconds** from when you press play on the computer. (The wireless is fast enough to download 10GB in 5-10 minutes) So it is not great for realtime use.

However for audio monitoring task this is not a problem. We just want the audio to somehow come out of phone's speaker. Press spacebar and by the time you finished taking off your headphone the latency is already over.

## What's the catch of trial version?

![](../../assets/91f3b2f20b000411.png)

An app of this quality can't possibly be free. There is also a bundle of macOS + Windows version for purchase. If not, a continuous white noise is overlaid onto the stream. This noise is loud, so you need to restart it to get around.

![](../../assets/dde08a5e15ffc54e.png)

But apparently, this trial condition is not affecting much for mixing/mastering task because it gibbed the audio after 10 minutes per launch, but you only need a few plays from your DAW when checking your mix. This is a problem on prolonged use, the intended use for normies of this application. Such as to listen to music, or for broadcasts, forwarding audio for recording etc.

However I admit Airfoil is a very polished software, I ended up supporting the company anyways, so I don't have to restart Airfoil when I finished fixing the mix/master each time.