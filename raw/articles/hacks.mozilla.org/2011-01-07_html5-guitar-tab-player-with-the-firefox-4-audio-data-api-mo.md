---
title: HTML5 Guitar Tab Player with the Firefox 4 Audio Data API – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2011/01/html5guitar/
author: Paul Rouget
published: '2011-01-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Greg Jopa](http://www.gregjopa.com), an Illinois State University grad student studying web development, built a web-based guitar tab player using Firefox’s [Audio Data API](https://developer.mozilla.org/en/Introducing_the_Audio_API_Extension) and [Vexflow (HTML5 music notation rendering API)](http://www.vexflow.com/). Here is some details from Greg. You can also read more about this experiment [on his blog](http://www.gregjopa.com/2010/12/html5-guitar-tab-player-with-firefox-audio-data-api/).

I created a mashup using the Firefox 4 [Audio Data API](https://developer.mozilla.org/en/Introducing_the_Audio_API_Extension), [MusicXML](http://recordare.com/musicxml), and [Vexflow](http://vexflow.com) to create a HTML 5 Guitar Tab Player.

*This is a Youtube video. It uses the HTML5 <video> tag if you activate it here.*

Using JavaScript, this guitar tab player converts the music note data from a [MusicXML](http://recordare.com/musicxml) file to frequencies playable by the Audio Data API. This note data is also converted to a format that can be read by Vexflow to display the guitar tab.

I have broken down this functionality into 4 steps. Here’s how the HTML5 Guitar Tab Player works:

## MusicXML

When a tab (a [tablature](http://en.wikipedia.org/wiki/Tablature)) is selected, the jQuery ajax() function loads the MusicXML file, parses through the contents, and appends all the formatted note data to a <script> tag. The format for each note is: `playNote(note, octave, duration)`

.

```
playNote(notes.C, 4, 1);
```

The tablature notation information in the MusicXML file is also processed and appended to a <div> tag for Vexflow.

Here is the structure of the nodes I am using from the MusicXML file:

```
```
1024
C
4
1024
1
2
the note node repeats for the rest of the notes in the measure…

And here is the generated source that is produced by the ajax() function.

For the audio:

```
```

For the tab:

```
tabstave notation=true
notes :q 1/2 :q 1/2 :q 3/1 :q 3/1 | :q 5/1
…
```

## Frequency Calculation

When the Play button is clicked the music data `<script id=”audio”>`

tag is evaluated and the note information is converted to frequencies using the following formula (assumes equal temperament):

`frequency = 440 * 2^(n/12)`


440 is the frequency for the note A at the 4th octave.

`n = distance away from A4 (440)`


I am using an array to store the distance between a certain note and the base note “A”

`notes = {C:-9, Cs:-8, D:-7, Ds:-6, E:-5, F:-4, Fs:-3, G:-2, Gs:-1, A:0, As:1, B:2};`


And to incorporate that a note can be played at different octaves I have adapted the above formula to the following:

`frequency = 440 * 2^((octave-4) * 12 + distance)/12);`


## Audiodata.js

I am using the Audiodata.js library in the guitar tab player which makes it easy to play continuous audio using a single array. This library encapsulates the Audio Data API methods. Audiodata.js is available on GitHub here: [https://github.com/notmasteryet/audiodata](https://github.com/notmasteryet/audiodata). The Audiodata.js project contains a score example with “Twinkle, Twinkle, Little Star” which inspired me to build this guitar tab player.

## Vexflow and the Animated Cursor

Vexflow is an open-source web-based music notation rendering API based on the HTML5 canvas element ([http://www.vexflow.com/](http://www.vexflow.com/)). I am using Vexflow to display the tab for each MusicXML file. I have added an additional canvas element on top of the Vexflow canvas to control the red cursor that links the audio to the tablature. The speed of the audio is controlled by the tempo which is measured in beats per minute. By converting this tempo to milliseconds I am able to use it for the redraw speed of the second canvas. Every time this canvas is redrawn the red cursor is moved 5 pixels to the right to highlight which note is currently being played.

Keep in mind that this HTML5 Guitar Tab Player is just a proof of concept and can only play single notes.

**If you have recommendations on how to make this tab player better or would like to contribute to this project check out the following post:** [http://www.gregjopa.com/2010/12/html5-guitar-tab-player-with-firefox-audio-data-api/ ](http://www.gregjopa.com/2010/12/html5-guitar-tab-player-with-firefox-audio-data-api/ )

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.

## 11 comments

PatrickJanuary 7th, 2011 at 15:27DaDudeJanuary 7th, 2011 at 17:56EdwardJanuary 7th, 2011 at 20:36GregJanuary 10th, 2011 at 09:41JasonJanuary 8th, 2011 at 08:02BrianJanuary 8th, 2011 at 10:34Gaurav MishraJanuary 11th, 2011 at 01:04Saeed NeamatiJune 5th, 2011 at 01:12MichaelSeptember 5th, 2011 at 15:3401dAugust 1st, 2012 at 22:34GiancaMarch 31st, 2013 at 10:41