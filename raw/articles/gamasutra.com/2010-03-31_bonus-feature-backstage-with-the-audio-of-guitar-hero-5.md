---
title: 'Bonus Feature: Backstage With The Audio Of Guitar Hero 5'
url: https://www.gamedeveloper.com/audio/bonus-feature-backstage-with-the-audio-of-i-guitar-hero-5-i-
author: Tom Parker
published: '2010-03-31'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Bonus Feature: Backstage With The Audio Of *Guitar Hero 5*

Neversoft audio programmer Tom Parker picks apart the process used to make the sound in the *Guitar Hero* games really stand out and be player-responsive -- and talks about tying in their custom tools with off the shelf solutions.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

While music from artists as diverse as Megadeth to Stevie Wonder and Muse immediately grab your attention when you talk about audio in a game like Guitar Hero, they are just a component of what makes the game fun to play.

There's a lot going on behind the scenes to help really put people up on that stage and to make sure it's fun, even as players clang a few notes. In this article I'll look at some of the things we did in the audio and how we did our part to take Guitar Hero up a notch.

We used FMOD as our sound engine, so some of our approaches might be more applicable to people who are familiar with the software, But even if you use a different engine, I hope that you might understand what we were aiming for, and why we did the things we did -- and find this info useful.

# The Song Audio Player

When we were given the honor of tackling the next Guitar Hero in 2007, we knew that we had to build on what the game offered to keep the series' momentum. It was also obvious that audio would be a major part of how we'd do it. That meant really sitting down and looking at the technology we had on hand, and how we were going to use it.

This led to a number of goals for our song audio player. It not only had to have great performance but also all a lot of new functionality to support the features we had planned, including: adding drums and vocals; letting players play the instruments they wanted, even if that meant doubling up; allowing a new drop-in and drop-out party mode and giving the player even more of a sense of location and space where their virtual band was playing.

We needed a system that would give us great audio streaming performance directly from a disc, a number of audio tracks with per-track digital signal processing, almost instant player feedback plus an audio visualizer, as well as atmospheric audio spatialization and on-the-fly reconfiguration for all of the above.

![](../../assets/c65ecea0d8113c33.img)


(click for full size)

# Streaming System

In early versions of Guitar Hero, there were, at most, three stereo tracks per song: guitar, bass or rhythm guitar and everything else. By adding drums and vocals, and giving the drums the space they required, we would have to triple the number of stereo tracks to nine. To ensure that this amount of data would smoothly stream off disk without performance issues we had to take some special measures. In this case it meant interleaving into three multichannel files.

Instead of having one massive file, three interleaving tracks of similar sonic complexity let us take advantage of variable bit rate space savings as well as the optimizations built into FMOD for handling 8, 6 and 4 channel input files.

Basically, it means instead of having one big file with the same bit rate for all instruments, we have three smaller files each with their own bit rate which changes based on the varying requirements of each group of instruments. Only sending bits down the stream when they are needed means more efficient streaming and disk space savings.

This is the layout of the stereo tracks:

FSB #1

1 - kick

2 - snare

3 - tom

4 - cymbal

FSB #2

5 - guitar

6 - bass

7 - misc

FSB #3

8 - vocal

9 - crowd sing-along

# Per-track Digital Signal Processing Effects

Once we have the tracks off the disc we need to be able to manipulate each track separately so we can have them respond to each player's actions. So, at run-time each stereo track is split apart from the interleaved FMOD Sound Bank (FSB) file and routed into a custom DSP network or "DSP Route" for further processing.

In order to do this processing, we abstracted an interface to FMOD's custom DSP API, and called it a "DSP Route". By adding this additional software layer we could manage input and output connections and add a DSP effect chain, very similarly to a channelgroup that is standard in FMOD, but giving us more control of our connections and the series of effects we can apply to any audio sent down that specific route.

All of this, in effect would give us an efficient way of streaming audio off of the disc, while giving us full control of each track at run-time. We need this for several reasons, including player feedback and atmospheric spatialization.

# Player Feedback

In a music-based game direct audio feedback is vital. The system has to be able to react to the people with the instruments and the more finesse we have with how we can alter the audio based on the player's action, the more we can make them feel like stars headlining their own virtual show.

First, of course, we need to turn on and off the volume of the player's instrument according to whether he or she is hitting the notes in the game.

Second, we want to provide some audio feedback to the user when Star Power is triggered. In this case, we wanted to accentuate that player's instrument audio to make it stand out more. Simply adding reverb to the instrument track -- be it guitar, bass or drums -- seemed to do the trick. It just nudged the spotlight in the right direction without being overpowering.

Third, we want to enhance player feedback for multiplayer situations. Depending on where the player's highway is positioned on the screen, we pan that player's audio slightly over in that direction. We found it just helped to place people in the room.

With Guitar Hero World Tour adding drums, and Guitar Hero 5 adding support for multiple instances of the same instrument this piece of polish managed to get pretty complicated pretty quickly. With vocals, there are 256 possible instrument and highway position combinations.

Luckily, the vocal system is totally separate to the song audio streams, so it whittles it down to a mere 81. Fortunately, we are able to simplify this further by layering panning configurations based on the number of shared instruments.

![](../../assets/f73fc0fc87dd9430.img)


(click for full size)

# Atmospheric Audio Spatialization

Once we had grounded players a little more firmly in how their action affected the song and how their sound slotted into the overall group, we wanted to help move that group into the game world. Bar or an auditorium, players should be able to close their eyes and feel it, but we wanted to take it a step further.

Particularly in freeplay, when no players have joined in yet, we try to make it sound like you are standing at the back of the venue, as a bystander. However, once you have joined the game, we then try to bring the listener into the center of the action. To do this, we adjust a series of Reverb, EQ, and Compressor settings on each track.

# Audio Visualizer

While we considered how to make the game more interesting from a sound perspective we also wanted to make it more interesting from a visual stand point. Of course, we would work on the look and feel of the graphics, but we also wanted to use the visuals to help give players more feedback about the music itself and their performance.

Beginning in Guitar Hero 5, we have a real-time audio visualizer as a feature of the game. This can visualize the entire audio mix and each of the separate player instrument tracks, individually. This requires that we set up the networks in a specific way so we can capture the audio we want to visualize.

This can be as simple as adding another effect. To give a specific example, the guitar and bass routes have a special custom DSP effect, as shown in our DSP network captures as the "Nx Audio Grabber." This effect just simply copies the audio as it passes through and launches other engine threads to do spectral processing for the graphics system, freeing up FMOD's time to do other processing.

# On-the-fly reconfiguration

Something that was also very important to us was expanding the accessibility of the series. This was something else that heavily impacted on our audio system. We knew that Guitar Hero was a partyfavorite. We also knew what it was like to miss the start of a song and having to wait around, or having to let other players down by deserting a song part way through as we're dragged away by other friends or burning party food.

With Guitar Hero 5, we created a new mode called "Party-Play." This mode allows players to join in and drop out of the game at will, while a song is in progress, and even while other players are playing.

This feature demanded a dynamic system that can reconfigure itself smoothly while playing back audio. For each of the nine stereo tracks of the song, we create a DSP Route for each instrument. DSP effect chains on each route are definable by our designers, and CPU willing, they could put whatever they wanted on these routes.

There is also a stand-alone Reverb processor, which we use as a "Send Effect." Each route can "send" audio to this effect at a definable volume and pan setting. This all allows us to add, remove and "move" instruments on-the-fly.

Even without a drop-in, drop-out system, the sheer number of player and instrument combinations means that we have to do a lot of reconfiguration every time a new song is selected. The instruments that influence the song streams are guitar, bass or drums and for guitar and bass, we must add a new DSP effect, the whammy.

What's more, more than one player can choose to play the same instrument. In the case of guitar or bass, we need to add a second whammy effect and we must split the track into two separate DSP Routes, both with separate whammy effects. However, since the buss (or final mix) volume is applied later on in the processing, we must recombine these tracks later on.

![](../../assets/3e9afb59fcef612a.img)


(click for full size)

# Latency

Although latency isn't strictly an audio problem, it is a big concern in a game like Guitar Hero, and many things must be done to address it which do touch on these systems. To make the game playable, we must synchronize the controller input and scoring with the video and audio. There are many variables involved with each system, and that is why we need the calibration screen.

You would be surprised how much latency modern TV sets can introduce in both the audio and video. Many televisions have a special mode called "game mode" to deal with exactly this issue.

Typically, this mode will turn off special video smoothing algorithms designed to "upscale" or otherwise make the picture look better, but require the television to store and delay several milliseconds of video and sometimes audio. The TV is also not the only thing to blame. Each game console has its own audio, video and wireless controller latency figures as well.

There are two parts to the calibration screen, one for synchronizing the video, and another for audio. The user is prompted to rhythmically tap the controller in time with scrolling notes on the screen, and then later with audio beeps. The video portion actually calculates the round-trip lag time from video output to controller input latency time, and adjusts the offset of the note highway so that the notes match up with the controller input.

The audio test tests the lag time for the audio output. Based on the calculated lag time, the song audio will be delayed so that it matches up with the controller input.

![](../../assets/ff96354c394075f9.img)


(click for full size)

# Let's Hear It

Game audio doesn't always get the credit it deserves and I think that's because it tends to be the most powerful when it is at its most subtle. A game like Guitar Hero is fun to make because it lets us focus more on the sounds. It's all about music, atmosphere, performance and cheering crowds.

The technology we used had to help us capture all of that and give our sounds a descriptive quality that most games shift on to their graphics. If you do well, the sound will tell you, if you don't do so well you will hear that also; when you use a power-up everyone will hear it in your notes, where you are standing in the line-up is reflected in the audio, as is the hall where the game is set.

As you can appreciate all of this takes a lot of subtle (and not so subtle) things happening in concert, and while we did a lot of things to try make Guitar Hero a success I think that the elements I've outlined above give a pretty good look at some of the behind-the-scenes audio that might go unnoticed but doesn't go unfelt.