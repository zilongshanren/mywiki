---
title: MIDI Music in AS3
url: http://david.fancyfishgames.com/2013/03/midi-music-in-as3.html
author: Legend
published: '2013-03-04'
source_blog: The Legend of GameDev
source_site: http://david.fancyfishgames.com/
category: graphics
fetched: '2026-04-13'
---

First, why would I want to play MIDI files in AS3? Well, MIDI files are small (think kb for long songs, not mb), and very easy to manipulate. Since MIDI files contain just information about the volume, pitch, and duration (and a bunch of metadata/instruments that I wont handle, so I'll ignore in this blog post), it's trivial to edit the song, increase or decrease the tempo, and perform pitch shifts or even changing of instruments, and this can all be done dynamically. Unfortunately, for whatever reason, Flash does not support native playback of MIDI files, nor can you access the native soundbanks (instruments) to play the MIDI files from flash. I've seen some as3 projects use sockets to play the MIDI files via an external java applet, and I've seen some as3 projects that load sound bank files as well, but the first method requires an external dependency, and the second method requires loading the soundbank files for every instrument you want (which can be tens or hundreds of mb). However, there's a third option too - dynamically generating the soundbanks, and that's what I wanted to experiment with.

The idea came from as3sfxr:

[http://www.superflashbros.net/as3sfxr/](http://www.superflashbros.net/as3sfxr/)(which I found on the One Game A Month website). It allows you to dynamically generate sound effects with a bunch of interesting parameters. You can see some of their example sound effects on the left. However, tweaking with the parameters, I thought I could come up with some interesting instruments. You can control the start frequency and the sustain time to change the pitch and duration of a note - everything you need to play a MIDI file. To get a nice clean tone, I recommend setting everything to the defaults, and then choosing sinewave (which produces a pretty generic sinewave), but experimenting with the settings, you can create a whole set of instruments, like electronic, retro, and even real-world sounding instruments. So, I had my dynamic, tweakable "soundbank," all I needed to do was load a MIDI file and then play the generated sounds at the right times, with the right pitches and right durations.

The Instrument class handles playing a note with specified sfxr parameters. It changes the frequency and duration parameters for each note you wish to render, and then ADDS the generated sound samples to the passed buffer (at it's current position). Adding sound samples together is an approximation of two overlapping sounds playing at the same time. To be fully realistic, you would want to add the frequencies of the two clips (using a fourier transform), not the samples - but that is not only complicated, but also very computationally expensive if we're doing it on the fly, and adding the samples sounds good enough. So, if you learn one lesson from this blog post, it's that if you have two sound clips and you want to generate a new sound clip that has both of them playing at the same time, just add the samples (if you don't know what samples are, that's another topic, but feel free to ask me and I can explain it, or just look at tutorials on WAV files).

Some minor details - sfxr takes a decent amount of time to generate the samples from the parameters, so I had to cache the results for every pitch and duration the instrument came across. That sounds crazy, but computers have a lot of memory, and the same note will occur many times, so it speeds things up many times. Also, sfxr's start frequency and sustain time parameters are very unintuitive - they are numbers from 0 to 1. The static method getLengthFromS in Instrument takes an input (in seconds) and returns a sfxr value from 0-1 (or higher if it's longer than 2.something seconds, luckily I hacked sfxr to allow sustainTimes larger than 1 - I also made some other minor changes to sfxr, mainly to access private methods). The static method getFreqFromHz in Instrument takes an input frequency in hz and returns a sfxr value (clamping from 0-1 is ok here, as frequencies below 0 and above 1 sound terrible anyways). I had to see what the code was doing to figure out the mapping function, but trust me, it works, just trust these methods :P. The static method getFreqOfMidiNote in Instrument takes a midi pitch number and converts it to a frequency in hz and then calls getFreqFromHz to return the sfxr frequency for the midi pitch. This algorithm I found online, 2^((n-69)/12)*440 - basically, every 12 midi numbers is an octave, which means multiplying or dividing by two, and note 69 is an A with a hz value of 440 that's a baseline.

The Instrument class is the most important one, but we also need a way to manage tracks of notes. The Track class has a single instrument, and then an array of note start, duration and frequencies. You can add notes to it by calling addNote (they should be added in ascending order of note start for playback with MIDISound, any order is fine with CachedSound). The renderNote function renders a single note with the track's instrument to the correct position in the byte array. The render function renders ALL notes with the track's instrument to the correct position in the byte array (this can take some time). The prepare function ensures all of the notes are cached for quick playback, and runs asynchronously with a callback.

The Main class uses as3midilib (

[https://code.google.com/p/as3midilib/](https://code.google.com/p/as3midilib/)) to load the midi song and add the notes to a Track class, and then plays it. This is relatively straightforward, but MIDI files don't give you note duration, instead they have note start and note end events. So I had to keep playing notes in a hash and then when I got the note end event update the duration. I've noticed some bugs with the MIDI loading, the division value isn't always correct (which is why it's 0.6/file.division instead of 1/division), and one file had events at the wrong times, but it mainly works with a little tweaking.

Finally, I have two playback classes. CachedSound takes a ByteArray of samples and plays it in a loop. This can play a rendered midi sound from Track.render, or whatever else you want. But, the render method can take some time, so I also added a MIDISound playback class. It allows you to add tracks you want to play, prepares them all so that all of the instruments are cached, and then will render and play the full MIDI byte array at the same time (it assumes notes are in ascending order of start time to do this). It will also loop, and after the first play it will render from a cached version just like CachedSound.

That's all for this experiment. You can hear an old MIDI song of mine (composed in middle school >_>) being played with a clear sinewave here:

[http://fancyfishgames.com/MidiPlayer](http://fancyfishgames.com/MidiPlayer)(entire swf is only 17 kb!)

You can hear the same song played using the generateBlipSelect method of SfxrParams for the instrument here:

[http://fancyfishgames.com/MidiPlayer/blip.html](http://fancyfishgames.com/MidiPlayer/blip.html)(literally change p.resetParams(); p.waveType = 2; p.decayTime = 0.15; to p.generateBlipSelect(); to in the Instrument class do this).

And the source code plus all dependencies is here:

[http://fancyfishgames.com/MidiPlayer/MidiPlayer.zip](http://fancyfishgames.com/MidiPlayer/MidiPlayer.zip)(undocumented, but I explained most of it above). Feel free to experiment with MIDI files and instruments! Oh yeah, the Main.status.text lines are just there to set that one line of text, feel free to remove!

If you have questions, feel free to ask!

Very nice! I tried with a multi-track midi, only the first one plays, but when the track is finished, all the tracks play!

ReplyDeleteYeah, that's a bug with multi-tracks and the on-the-fly renderer (the caching renderer works fine, but that requires it to generate the entire song up front). I have a fix, but if there are too many tracks, it gets laggy and doesn't play smoothly! Unfortunately, the MIDI generation is slow, and it takes time to composite lots of simultaneous notes. It could use some optimization!

ReplyDeleteThis is awesome. Can't wait to play with it. :)

ReplyDeleteI was looking forward to building something like this, when I first saw the asfxr. You beat me to it and saved me a lot of work. Thanks for sharing. I allready drove everybody in the house mad with those old 'gamy' sounds today.

ReplyDeleteI don't mind the multitrack bug, it would take up to much processor power to render on the fly anyway and all I want to use it for is saving space. Oh, and well done on the seperate instrument class. I'll try and implement some cool FM-synthesis routines I have lying around. In short, thanks for sharing.

Glad it helped you out! I created this script just because I thought the idea was interesting and wanted to learn more about the internals of sound generation - so it's great that it's actually getting used!



ReplyDeleteThe on the fly renderer is just too slow in practice unless there are only one or two tracks I have the updated code that fixes that problem btw - the code here would render the next note on ALL the tracks at once, but sometimes that means it would render a note that was not needed for a while on a track that had few notes, but as mentioned even though the problem no longer occurs it still chokes up with too many notes at times. If you have a complex song, it's best to just cache the entire song upfront.

Let me hear if you create anything awesome or cool - I'm interested to hear what kinds of instruments you come up with!