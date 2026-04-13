---
title: 'Detecting notes from a live cello: the core technology of Cello Fortress'
url: http://joostdevblog.blogspot.com/2013/05/detecting-notes-core-technology-of.html
author: Joost van Dongen
published: '2013-05-19'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Cello Fortress](http://www.cellofortress.com)is controlled by a cello. This is a really weird and unique thing, and comes with some serious challenges. So far I have discussed the game design aspect of this, but at the very core of the game lies a much more technical topic: detecting notes in real-time from a live cello. Cello Fortress really knows what notes I am playing. I developed my own algorithm for that, and although it is not perfect (it quite often shortly detects notes that are not actually played), it works surprisingly well for such a difficult technical problem. So how does it work? Let's have a look!

![](../../assets/b76cf69a32de11db.gif)

The big challenge here is that a cello produces a very complex sound pattern. There are all kinds of overtones, scratches and noises in it, and detecting the actual note from that is incredibly difficult. I did some research before I began programming the game, and it turns out that finding notes in a live acoustic instrument is in fact an unsolved problem. There is quite a lot of research in this field, but a perfect solution has not been found yet.

Of course, for a digital instrument like a keyboard this is easy, but as soon as it gets acoustic, it becomes problematic. For guitar there are some devices on the market that can find notes in sound: they can convert live guitar playing to MIDI with very little delay. However, they are supposedly still far from perfect, and don't work with cellos. A cello produces a much more complex tone than a guitar, since it lacks a clear strumming moment: notes just continue and smoothly flow into each other. People also often mention Melodyne to me, but as far as I know, Melodyne can only detect notes after recording, not in real-time.

Seeing that no easy existing solution was around, I decided to start experimenting with this problem myself. I'll have to admit that I didn't read all of the scientific literature on the subject, but it turned out I didn't have to: I managed to come up with an algorithm that detects notes well enough for what I need for Cello Fortress.

![](../../assets/8661288bed005c09.gif)

So, my basic input here is just a microphone signal. My first step is to grab the last 0.2 seconds of microphone input (9600 samples) and take the

*Fourier Transform*of that. The Fourier Transform is a rather standard mathematical operation that results in a frequency spectrum: a list of how strong each frequencu is within the signal. Since a cello has a very rich sound, a lot of frequencies are in a single note, but the Fourier Transform is still a great starting point for my algorithm.

The math behind Fourier Transforms can look pretty creepy and complex, but the nice thing is that they are usually calculated using the standard Fast Fourier Transform algorithm, which can simply be grabbed from the internet. It is also included in many audio libraries, for example in the awesome

[FMOD](http://www.fmod.org/). So to use the Fourier Transform, there is no need to understand the details of how it is calculated.

The spectrum below is from playing an G2 on my cello. Remarkably, there is a clear pattern in the spectrum for this note: there are peaks at evenly spaced frequencies. These are called

*overtones*. I knew about those before I started working on this algorithm, but I had never realized they look so simple. I know that the G I played here is 98hz (that is the open G-string on a cello). An indeed, the left-most peak is at exactly 98hz. Other peaks are at multiples of that: at 196hz, 294hz, 392hz, etc.

![](../../assets/35f00beb6a2d4c81.gif)

This spectrum looks so simple that it seems very easy to write an algorithm that detects notes. However, that turns out to be quite a bit more complex than this. For starters, I would really like to be able to detect chords, because I want to make gameplay with that. Another reason to want to detect chords, is because when I play from one note to the next, the previous note will still be audible due to reverb within the big body of the cello, and due to the previous string still vibrating. Being able to detect several notes at once will greatly help me handle the transition from one note to another. However, chords make the spectrum a whole lot more complex, as you can see in this example:

![](../../assets/68e3206f4c15d316.gif)

Regardless of how complex this looks, looking at this, a relatively simple algorithm comes to mind that is indeed the core idea of what I ended up with: let's list all the peaks, and then look for the peaks that would explain all other peaks through their overtones. For example, let's say I have peaks at 45hz, 90hz, 100hz, 135hz, 180hz and 200hz. Those are all multiples of 45hz and 100hz, so those must be the frequencies that are being played. In note names, those would be F#1 and G2.

This simple algorithm quickly turns into a big mess, though. It is difficult to make it handle peaks due to scratches and noise well, so I quickly ended up in a swamp of extra rules and magic numbers to compensate for those.

There is also a more fundamental problem: the spectrum is not very precise. For every block of about 3hz, the Fourier Transform tells me how strong it is. So I know the strength of 100hz, of 103hz, of 106hz, etc. Since a block is 3hz wide, the actual frequency for the bin at 103hz can be anything between 101.5hz and 104.5hz. This lack of precision is not a big problem for the higher notes: the difference between A3 (the open A-string) and the next note (A#3) is 13hz, which is well above 3hz. For low notes this is a bigger problem: the difference between C2 (the lowest note on a cello) and C#2 is only 3.9hz. This is so close to our 3hz precision, that this is bound to give problems.

![](../../assets/92f3fcf43e7eefdc.gif)

One solution to this would be to somehow increase the precision of the Fourier Transform. The only way to do this, is to feed it more samples. I currently feed it 0.2 seconds (9600 samples), so I could double the precision if I would feed it 0.4 seconds (19200 samples). However, this has two big downsides. The first is that this increases the delay between playing a note and detecting it. The second downside, and this is much worse, is that many notes are way shorter than that. If I play really fast, I can play 6 notes per second, which means that a period of 0.4s contains several notes. This completely clutters the spectrum and makes it much more difficult to detect individual notes. For these reasons I really don't want to increase the precision of the Fourier Transform by taking a longer sample period.

This lack of precision makes the previous idea of finding the peaks that explain all other peaks not work well. In the above example, I assumed a peak at 45hz. However, because of the size of the bin, the real frequency is anywhere between 43.5hz and 46,5hz. This makes a huge difference for the frequency of the higher overtones. The 10th overtone of 43.5hz is at 435hz, which is five bins away from 450hz (the 10th overtone of 45hz). I tried to modify my peaks for this, but it quickly got stuck in more and more exception-cases.

The solution I came up with is a different approach based on the same idea. I step over

*all*frequencies with steps of 0.5hz. For each frequency, I look up its own strength, and the strengths of the first 20 overtones. So for 43.5hz, I look up the strength at 43.5hz, and the strengths of the overtones at 87hz, 130.5hz, 174hz, etc.

Taking such small steps means I look in the same bin several times, since steps are only 0.5hz and bins are 3hz wide. But in the 20th overtone, those steps of 0.5hz correspond to 10hz, which is a difference of several bins. So doing more steps is actually relevant.

The final part of my algorithm is simple:

*a frequency must be a note if its own strength is strong enough, and if the added strengths of all its overtones is strong enough*. These two minimum strengths are settings that depend mostly on the microphone's output volume. Through experimentation I have found good minimum strengths for both the own frequency and the overtones. The algorithm now looks roughly like this:

for (float frequency = 60; frequency ‹ 450; frequency += 0.5f) { int baseBin = getBinFromFrequency(frequency); float baseStrength = spectrum[baseBin]; float overtonesStrength = 0; for (int multiplier = 2; multiplier ‹= 20; multiplier++) { int bin = getBinFromFrequency(frequency * multiplier); overtonesStrength += spectrum[bin]; } if (baseStrength >= baseStrengthMinimum && overtonesStrength >= overtonesMinimum) { print("Found a note! Frequency:", frequency); } } |

Note that this algorithm is bound to find the same tone at several frequencies: if 70hz is well above the thresholds, than 70.5hz and 69.5hz probably also are, even though they are the same note. So when several frequencies are close to each other, I simply take the strongest and throw the others away.

Despite that my bins are 3hz wide, the extra information from the overtones makes it so precise that I can use this to reliably tune the strings of my cello very precisely. Beforehand, I had never expected I would find an algorithm so simple, and yet giving such exact answers!

Does this mean I am done, that I found the golden solution? No, far from it... The result of this algorithm is indeed that with the right sensitivity settings, I can detect practically all notes I play on my cello. However, what we have now is still completely unusable, because it

*also*detects tons of false-positives: notes that are not really being played. Next week, I will explain why this happens, and what tricks I added to solve most of this problem. See you then!

I actually wrote a similar algorithm in mathlab for a course on signal recognition. We used Finite Impulse Resonse filters to clean up everything. It worked ok-ish for a piano. Btw isn't it easier to calculate from peaks the fundamental note instead of going from the fudamental note to the other peaks. This way you won't have the bin-precision problem I think. (Note that I'm probably messing up a lot of names for music theory related stuff here :) )

ReplyDeleteIsn't the algorithm you describe (from peaks to note) exactly what I describe halfway and discard because it gives too much trouble in practice? Or do you mean something else?

DeleteHmm, I read the entire article and still somehow forgot about that in the end. That was the idea I was going for indeed. We did some pre-filtering though so maybe that removed the problems you had with that method and we didn't need to be real-time so that too will make things easier. That being said it was only one assignment for a course a few years back so I'm not sure about the exact details anymore.

DeleteWell, as you said, it worked "ok-ish". I actually implemented it and it did work, but when I started tweaking and improving it to make it work better, that turned out to be really difficult with the way I had implemented it. Quickly became a mess.


DeleteThe algorithm at the end is much simpler and was better even before I did any tweaking. I guess the other one can be implemented in several ways, though, so the problem might simply have been in my implementation.

I played with this many years ago and was surprised about how complex it ended up being. I found that one of the nicest notes was a human whistling, which is a nearly perfect sine curve with no overtones.

ReplyDeleteSounds like a nice sequel: Whistler Fortress! ;)


DeleteI still have to try my code with tons of other instruments: there are probably several others that also work great, and whistling might be one of them. :)

Cool, I would like to see how well this works with a double bass.

ReplyDeleteIt looks like you are trying to reinvent the wheel, because what you are doing looks a lot like 'harmonic product spectrum' which is a method of pitch detection.

ReplyDeleteAlso, what is your sampling rate? because at a standard 44100 and without doing any downsapling, 9600 samples only gets you about 4.5hz of resolution. A lot of the lower notes are closer that that.

DeleteWhat if you artificially increase your sample frequency (by interpolating samples)? Surely that will increase your precision at the expense of some noise

ReplyDeleteGoogle "cepstrum pitch detection"

ReplyDeleteHave you used / heard of Max MSP?

ReplyDeleteI tried to build a pitch detector awhile back - never got it working that well, but one interesting thing I came across was the discrete-time Fourier transform. This is a version of the Fourier transform that works on discrete-time (sampled) signals, but allows continuous frequencies, so it avoids the binning problem with the regular FFT.



ReplyDeleteThe downside is it's pretty expensive and you have to test one frequency at a time. I had the idea of using the FFT to look for bins with peaks, then use the DTFT to zero in on the exact frequency of the peak much more precisely, using a golden section search or similar.

Probably not relevant for your case as you don't need very precise frequencies, but could be handy for making a tuner or something like that.

Hmm, interesting, I hadn't heard of DTFT yet!


DeleteAs for precision: because of my usage of the overtones as well, I already get 0.2hz precision, which is easily precise enough for a tuner. In fact, I discovered this way the subtle effect that if I play louder, the frequency is a little bit higher (which makes sense, since more pressure means tighter string means higher frequency).

Very interesting article. Thanks for the post. Be sure to share with our musicians.

ReplyDelete