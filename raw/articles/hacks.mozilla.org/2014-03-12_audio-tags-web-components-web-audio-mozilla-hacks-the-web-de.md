---
title: 'Audio Tags: Web Components + Web Audio = ♥ – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2014/03/audio-tags-web-components-web-audio-%e2%99%a5/
author: Soledad Penadés
published: '2014-03-12'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Article written by Soledad Penadés, edited by Angelina Fabbro.*

Last week we released [Brick 1.0](http://mozilla.github.io/brick/), our carefully curated set of web components for rapid development. Using components makes it very easy to use and integrate these UI widgets with existing code and frameworks.

And this week we bring you *Audio Tags*, an experiment building Web Components that represent Web Audio blocks that let us construct a complete instrument with an interface to play it. With reusable audio blocks, developers can experiment with Web Audio without having to write a lot of boilerplate code.

Let’s build a simple synthesiser to demonstrate how the different tags work together!

## The Audio Context

The first thing we need is an audio context. If you’ve ever done any [Canvas](https://developer.mozilla.org/en-US/docs/HTML/Canvas) programming, this will sound familiar. The context is akin to a toolbox: it’s got the functions (the tools) that you need and it’s also where everything happens. All other audio tags will be placed inside a context.

This is how an audio context looks like when using Audio Tags:

```
```

That’s it!

## Oscillators

While being able to create an audio context by typing just one tag declaration is great, it is not particularly exciting if we can’t get any audible output. We need something that generates a sound, and for this we’ll star with something simple and use an *oscillator*. As the name implies, the output is a signal that oscillates between two values: -1 and 1, generating a periodic waveform. We will place it inside an audio context to have its output automatically routed via the context’s output to the computer’s speakers:

```
```

([See it live](http://sole.github.io/audio-tags/examples/02_context_oscillator/)).

In the real world, [oscillators](http://en.wikipedia.org/wiki/Electronic_oscillator) can generate different signal shapes. Likewise, in the Web Audio world we have analogous wave types that we can use: sine, square, sawtooth, and triangle. Since web components are first class DOM elements, we can specify the desired wave type by using an attribute:

```
```

You could even change it *live* by opening the console and typing this:

```
document.querySelector('audio-oscillator').type = 'square';
```

Similarly, you can also change the frequency the oscillator is running at by setting the `frequency`

attribute:

```
```

## Mixer

Having a running oscillator is just the first step. Most synthesisers available have more than one oscillator playing at the same time to make the sound more complex and nuanced. We need some way of playing two or more sounds in parallel, while combining them into a single output.

This is commonly known as mixing audio, and therefore we need a *mixer*:

```
```

The mixer will take the output of each of its children, and join them together to form its own output, which is then connected to the context’s output. Note also that since we’re dealing with DOM elements, when we say “children” we literally mean the mixer’s DOM children elements.

([Example](http://sole.github.io/audio-tags/examples/03_mixer/)).

## Chain (and oscilloscope)

When you start adding multiple sounds it’s useful to be able to *see* what is going on in the synthesiser. What if we could, somehow, plug a component between the output of one child and the input of another, and display what the sound wave looks like at that point?

We can’t do that with the mixer, because it just joins all the outputs together. We need a new abstract structure: *chains*. An audio chain will connect the output of its first children to the input of the second children, and the output of the second children to the input of the third one, and so on, until we reach the last children and just connect its output to the chain output.

Or in other words: **while the mixer connects things in parallel, the chain connects them serially**.

Let’s connect a new element –the oscilloscope– to the output of an oscillator, using a chain. The oscilloscope will just display what is connected to its input, and the signal will pass through to its output without being modified at all. You can change the oscillator’s wave type to `square`

, and see how the oscilloscope changes its display accordingly.

```
```

([Example](http://sole.github.io/audio-tags/examples/04_chain/)).

## Filter

Synthesisers don’t limit themselves to just running several oscillators at the same time. They often add postprocessing units to this raw generated audio, which give the synthesiser its own distinctive sound.

There are many types of postprocessing effects, and some of the most popular are *filters*, which roughly work by highlighting certain frequencies or removing others. For example, we can chain a low pass filter to the output of an oscillator, and that would only allow the lower frequencies to go through. This produces a sort of dampening effect, as if we had put on some ear muffs, because higher frequencies travel through the air and we *hear* them with our ear pavilions, while lower frequencies tend to travel through the earth and objects too. So rather than hearing them, we *feel* them with our body, and it doesn’t matter whether you have something over your ears or not.

```
```

([Example](http://sole.github.io/audio-tags/examples/05_filter/)).

Web Audio natively implements [biquad pole filters](http://en.wikipedia.org/wiki/Digital_biquad_filter), and as happens with the `audio-oscillator`

tag, you can alter the filter behaviour by setting its `type`

attribute. For example:

```
```

You could even insert several oscilloscopes: one before and another after a filter, to see the effect the filter has on the signal:

```
```

([Example](http://sole.github.io/audio-tags/examples/05_filter_double_osc/)).

## And finally, the minisynth

We have enough components to build a synthesiser now! We want two oscillators playing together (one an octave higher than the other), and a filter to make the sound a little bit less harsh and more “self-contained”. So, without further ado, this is the structure for representing our minimal synth, the `<mini-synth>`

, using the components we’ve introduced so far:

```
```

For the sake of comparison, this is more or less how we would assemble a similar setup using raw Web Audio API objects and functions:

```
var mixerGain = context.createGain();
var osc1 = context.createOscillator();
var osc2 = context.createOscillator();
osc1.connect(mixerGain);
osc2.connect(mixerGain);
var filter = context.createBiquadFilter();
mixerGain.connect(filter);
// and the actual output is at *filter*
```

It’s not that the code is particularly complicated, it just doesn’t have the nice visual hierarchy of the declarative syntax. The visual cues from the syntax make understanding the relationship between elements quick and easy.

We still need a few lines of JavaScript to make the `<mini-synth>`

component behave like a synthesiser: it has to start and stop both oscillators at the same time. We can take advantage from the fact that the [AudioTag prototype](https://github.com/sole/audio-tags/blob/master/src/js/TagPrototype.js) has some common base methods that we can overload to get specific behaviours in our custom components.

In this particular case we’ll overload the `start`

and `stop`

methods to make the oscillators start and stop playing respectively when we call those methods in the synth. This way we abstract the internals of the synthesiser from the world, while still exposing a consistent interface.

```
start: function(when) {
// We want to make sure we don't clip (i.e. go under -1 or over 1),
// so we'll divide the gain by the number of oscillators in the synth
var oscGain = this.oscillators.length > 0 ? 1.0 / this.oscillators.length : 1.0;
this.oscillators.forEach(function(osc) {
osc.gain = oscGain;
osc.start(when);
});
}
stop: function(when) {
this.oscillators.forEach(function(osc) {
osc.stop(when);
});
}
```

The [implementation](https://github.com/sole/audio-tags/blob/master/examples/js/mini-synth.js) should be fairly easy to follow.

You might be wondering about the `when`

parameter. It is used to tell the browser when to actually start the action, so that you can schedule various events in the future with accurate timing. It means “execute this code at `when`

milliseconds”. In our case we’re just using a value of 0, which means “do that immediately”. I advise you to read more about `when`

in the [Web Audio spec](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html#dfn-when).

We also need to implement a method for actually telling the synthesiser which note to play, or in other words, which frequency should each oscillator be running at. So let’s implement `noteOn`

:

```
noteOn: function(noteNumber) {
this.oscillators.forEach(function(osc, index) {
// Each oscillator should play in a higher octave
// Each octave is composed of 12 notes
var oscNoteNumber = noteNumber + 12 * index;
// We're using a library to convert note numbers to frequencies
var frequency = MIDIUtils.noteNumberToFrequency(oscNoteNumber);
osc.frequency = frequency;
});
}
```

You don’t *need* to use [MIDIUtils](https://github.com/sole/MIDIUtils), but it comes handy if you ever want to *jam* with an instrument in your browser and someone else using a more traditional MIDI instrument. By using standard frequencies you can be sure that both your instruments will be tuned in the same pitch, and that is *GOOD*.

We also need a way for triggering notes in the synthesiser, so what better way than having an on screen keyboard component?

```
```

will insert a keyboard component with 2 octaves. Once the keyboard gets focus (by clicking on it) you can tap keys on your computer’s keyboard and it will emit `noteon`

events. If we listen to those, we can then send them to the synthesiser. And the same goes for the `noteoff`

events:

```
keyboard.addEventListener('noteon', function(e) {
var noteIndex = e.detail.index;
// 48 is the base note here = C-3
minisynth.noteOn(parseInt(noteIndex, 10) + 48);
minisynth.start();
}, false);
keyboard.addEventListener('noteoff', function(e) {
minisynth.noteOff();
}, false);
```

So it is [DEMO](http://sole.github.io/audio-tags/examples/07_mini_synth/) time!

And now that we have a synthesiser we can say we’re rockstars! But rockstars need to look *cool*. Real-life rockstars have their own signature guitars and customised cabinets. And we have… CSS! We can go as wild as we want with CSS, so just press the *Become a rockstar* button on the demo and watch as the synthesiser becomes *something else* thanks to the magic of CSS.

## Looking behind the curtains

So far we’ve only talked about these fancy new audio tags and assumed that they are *magically* available in your browser, even though it is obvious they are non-standard elements. We haven’t explained where they come from. Well, if you’ve read this far already you deserve to be shown the secrets of the kingdom!

If you look at the source code of any the examples, you’ll notice that we’re consistently including the `AudioTags.bundle.js`

([line 18](https://github.com/sole/audio-tags/blob/master/examples/02_context_oscillator/index.html#L18)) and `AudioTags.bundle.css`

([line 6](https://github.com/sole/audio-tags/blob/master/examples/02_context_oscillator/index.html#L6)) files. The CSS is not particularly exciting and the real magic happens in the JavaScript. This file includes a couple of utility libraries that give us the ability to define custom tags in the browser, and then the code for defining and making available these new tags in the browser.

On the utility side, we first include [AudioContext-MonkeyPatch](https://github.com/cwilso/AudioContext-MonkeyPatch/), for unifying Web Audio API disparities between browsers and enabling us to use a modern, consistent syntax. If you want to know more about writing portable Web Audio code, you can have a look at [this article](https://hacks.mozilla.org/2013/08/writing-web-audio-api-code-that-works-in-every-browser/).

The second library we’re including is [X-Tag](http://x-tags.org/), and more specifically, its very [innermost core](https://github.com/x-tag/core/blob/master/dist/x-tag-core.js). X-Tag is a custom elements polyfill, and custom elements are a part of the emerging [Web Components spec](http://w3c.github.io/webcomponents/explainer/), meaning this stuff will be built right into the browser soon. X-Tag is the same library that [Mozilla Brick](http://mozilla.github.io/brick/) uses. You can learn how to make your own custom elements [with this article](https://hacks.mozilla.org/2014/03/custom-elements-for-custom-applications-web-components-with-mozillas-brick-and-x-tag/).

That said, if you plan to use Brick and Audio Tags in the same project, a disaster might probably ensue, since both Brick and Audio Tags include X-Tag’s core in their distribution bundles. The authors of both libraries are discussing what’s the best way to proceed about this, but we haven’t settled on any action yet, because Audio Tags is such a newcomer to the *X-Tag powered* library-scene. In any case, the most likely outcome is that we’ll offer an option to build Brick and Audio Tags *without* including X-Tag core.

Also, here is a video of this same material at [CascadiaJS](http://2013.cascadiajs.com/), so you can watch someone build it right in front of you. It may help your understanding of the topic:

## What’s next for Audio Tags?

Many people have been asking me *what’s next* for Audio Tags. What are the upcoming features? What have I planned? How do you contribute? How do we go about adding new tags?

To be honest? I have no idea! But that’s the beauty of it. This is just a starting point, an invitation to think, play with and discuss about this notion of declarative audio components. There’s, of course, a list of things that don’t work yet, some random ideas and maybe potential features in the Audio Tags’ [README](https://github.com/sole/audio-tags#what-is-missing) file. I will probably keep extending it and filling the gaps–it is a good playground for experimenting with audio without getting too messy, and also a good test for Web Components that go past the usual “encapsulated UI widgets on steroids” notion.

Some people have found the project inspiring in itself; others thought that it would be useful for teaching signal processing, others mixed it with accelerometer data to create physically-controlled synthesisers, and others decided to ditch the audio side of it and just build custom components for WebRTC purposes. It’s up to each one of you to contribute if you feel like doing so!

## About
[
Soledad Penadés ](https://soledadpenades.com)

Sole works at the Developer Tools team at Mozilla, helping people make amazing things on the Web, preferably real time. Find her on #devtools at irc.mozilla.org

## About
[
Angelina Fabbro ](http://realityhacking.net)

I'm a developer from Vancouver, BC Canada working at Mozilla as a Technical Evangelist and developer advocate for Firefox OS. I love JavaScript, web components, Node.js, mobile app development, and this cool place I hang out a lot called the world wide web. Oh, and let's not forget Firefox OS. In my spare time I take singing lessons, play Magic: The Gathering, teach people to program, and collaborate with scientists for better programmer-scientist engagement.

## 15 comments

HugoMarch 12th, 2014 at 15:05Soledad PenadésMarch 12th, 2014 at 17:12HugoMarch 13th, 2014 at 12:32MarioMarch 13th, 2014 at 01:20Soledad PenadésMarch 14th, 2014 at 12:41AlexMarch 13th, 2014 at 10:37Soledad PenadésMarch 14th, 2014 at 12:40Zeno RochaMarch 14th, 2014 at 06:45Soledad PenadésMarch 14th, 2014 at 12:40AndersMarch 14th, 2014 at 09:11Soledad PenadésMarch 14th, 2014 at 12:38AndersMarch 17th, 2014 at 11:07Soledad PenadésMarch 17th, 2014 at 12:48Pablo CúbicoMarch 18th, 2014 at 15:58HugoMarch 31st, 2014 at 14:52