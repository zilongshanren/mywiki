---
title: Here's how I made my computer write music
url: http://joostdevblog.blogspot.com/2018/08/a-first-step-towards-procedural-music.html
author: Joost van Dongen
published: '2018-08-26'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Note that this video contains a selection of the nicer pieces, so it isn't all this good. Most of the other music it currently produces is a bit more boring, or too similar to these fragments. The program is a work-in-progress and it should improve a lot as I spend more time on it.

I started programming this for a rather odd reason: I wanted to practice improvising on my cello over complex chord schemes and figured a program that automatically produces those would do the trick. As usual with this kind of thing, it got out of hand and I've so far spent my time making it cooler instead of playing along to its tunes on my cello. I hope I can expand it to the point where it can be a game soundtrack, or a live streaming radio channel on Youtube that constantly produces new music.

My approach to procedural music is mostly based on my own ideas about composition. I'm deliberately steering away from a lot of common composition 'rules' since I expect that's been done already. I think I'll get something more interesting and more personal if I start from my own ideas instead. While I don't ignore music theory either, I do try to avoid rules like ending a chord progression with the dominant and then going back to the tonic or anything like that.

Just to be clear: my music generator is

*not*an AI or a self-learning system or anything like that.

The procedural music generator consists of a bunch of elements that together produce the music:

**Chords, rhythms and scales**

To 'teach' my program basic music theory I've created a bunch of text files that define a lot of common and less common chords, rhythms and scales. You can see which it's using in the video: it might for example choose to play a C major chord in 3/4 rhythm.

![](../../assets/c40cefaed4d561f8.gif)

**Structure generators**

The first thing needed to create a piece of music, is a basic structure. This part of the program randomly chooses the chord progression, the rhythm and the scales. It also chooses how individual instruments are allowed to deviate from the rhythm, so that there's some consistency between instruments without requiring them to do the exact same thing.

**Instrument layer generators**

These generate the notes for specific instruments. Each category of instruments has a role to fulfil and its own specific algorithm for that. For example, the generator for drums is completely different from the generator for bass. Most of these generators are still very basic so there's plenty of room for improvement there. A lot of the variation in the video above comes from having different combinations of instrument layer generators. For example, some have drums, others do not. I expect that having a lot of layer generators is where my procedural music will get most of its variation. Currently I have five, but I'd like to create at least a dozen. The most important missing layer at the moment is one for actual melodies, which is probably also the most challenging one to get right.

**VST instruments**

Actually performing the music is done using VST instruments. VST is a standard for digital instruments that is used by a lot of programs on Windows. A VST file is basically just a DLL and I've coded a simple music player that can handle them. For each instrument layer I'd like to have several VST instruments that can play that layer, so that I can get different sounds. Currently most of it sounds very digital, so it would be nice to also have VSTs for other types of instruments, like acoustic drums and guitars.

**Song structure**

This is an element that's currently completely missing: at the moment all music played by my music generator is simply a loop of 4 to 12 bars. I want to program systems for song structures with verse/chorus/bridge, but also for endlessly progressing music and for music that for example slowly builds up to a climax.

**Carefully restricted randomness**

All the systems in this generator contain a lot of randomness, but the randomness is limited to specific rules I've come up with. If those rules are too free then the result is noise, not music, while if the rules are too strict then the resulting music will always seem same, so carefully balancing the randomness is a big challenge here.

![](../../assets/3bf55e9442b1a94f.gif)

For future improvements I'd like to add more instrument layers and refine the current ones, add song structures and add more VST instruments. Since I've recently become a dad I don't have a whole lot of time to work on this, so I expect progress will be very slow. I hope to include a first basic version of my procedural music generator as a bonus feature in the home edition of

[Cello Fortress](http://www.cellofortress.com/), whenever that's actually finished.

Let's conclude with a question: do you know any communities for open source or free VSTs? There are plenty of VSTs that can be downloaded for free, but in many cases they just specify that they're free to use, not free to distribute with commercial software. I've so far had a hard time finding usable instruments or getting into contact with (hobby) instrument programmers who might be willing to allow me to include their instruments. Leave a comment if you've got suggestions or are a digital instrument programmer yourself.

I love this idea so much (and I respect the focus on your own creative process above and before the standards)! Also have to say I'm a fan of the diagrams you include in your posts Joost. How do you go about making them?

ReplyDeleteThanks! :)


DeleteThe diagrams are usually just handmade in Photoshop. Not sure why I do that though, because I like Libre Office Draw quite a lot. That program is free, easy to use and more suitable for this kind of thing.

Can you tell me if and where your Procedural Music Generator can be downloaded as standalone version ?

ReplyDeleteThanks

I'm currently developing it as a standalone application on Steam. It has been greatly improved and expanded since the version I've shown here, and will launch in a few months. You can see the new version and wishlist it on Steam here: https://store.steampowered.com/app/1808490/Robo_Maestro/

DeleteThanks


DeleteHope there will be an option for Midi Export to handle it

in a DAW

Absolutely! It can export to MIDI, to WAV, and each layer to a separate WAV. So it's very suitable to make something and then continue with it in your favourite DAW. :)

DeleteI was Happy for that , but (AARGH!) I see it will work only on Win 10 ! I'm on Win 7 _64 bit

Deleteand for many reasons I don't intend to change . Is there a chance you will set a version working on Win 7 ??

Best Regards

I see that Unreal supports Windows 7, so it will likely actually work on your PC. I don't have Windows 7 myself anymore, so I can't try it, and that's why I've put Windows 10 as minimum requirement on Steam.


DeleteI recommend just buying Robo Maestro when it launches, and if it turns out it doesn't work on your computer after all, just refund it on Steam. Steam will simply give you the money back.