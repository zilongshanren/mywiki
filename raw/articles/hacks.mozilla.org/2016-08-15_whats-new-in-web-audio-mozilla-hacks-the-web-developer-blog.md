---
title: What’s new in Web Audio? – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/08/whats-new-in-web-audio-2/
author: Soledad Penadés
published: '2016-08-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The [Web Audio API](https://webaudio.github.io/web-audio-api/) is still under development, which means there are new methods and properties being added, renamed, shuffled around or simply removed!

In this article, we look at what’s happened since our [last update](https://hacks.mozilla.org/2015/02/whats-new-in-web-audio/) in early 2015, both in the Web Audio specification and in Firefox’s implementation. The demos all work in [Firefox Nightly](https://nightly.mozilla.org/), but some of the latest changes might not be present in Firefox release or Developer Edition yet.

# API changes

## Breaking change

The reduction attribute in `DynamicsCompressorNode` is now a `float` instead of an `AudioParam`. You can read the value with `compressor.reduction` instead of `compressor.reduction.value`.

This value shows the amount of gain reduction that the compressor is applying to the signal, and it had been read-only anyway, so it makes sense to have it as a `float` and not an `AudioParam` (since no changes can be scheduled).

To detect whether the browser your code is running on supports the `AudioParam` or `float` data type, you can check for the existence of the `.value` attribute on `reduction`:

```
if(compressor.reduction.value !== undefined) {
// old style
} else {
// new style
}
```


Take a look at [this example](https://mozdevs.github.io/WebAudio-examples/DynamicsCompressor) where the `reduction` attribute is accessed while a drum loop is playing. Notice how the value changes to react to the loudness in the track, and how we’re detecting which API version the browser supports before reading the attribute `value`.

## New properties and methods

### New life cycle management methods in `AudioContext`

With `AudioContext`s being rather expensive, three new methods have been added: `suspend()`, `resume()` and `close()`.

These allow developers to suspend the processing for some time until it is needed again, and to free some resources with `close()` when the `AudioContext` isn’t required anymore.

Essentially, when an `AudioContext` is suspended, no sounds will be played, and when it resumes, it will continue playing where it left off. The [description for suspend()](https://webaudio.github.io/web-audio-api/#widl-BaseAudioContext-suspend-Promise-void) in the specification has all the details.

[This example](https://mozdevs.github.io/WebAudio-examples/AudioContext) demonstrates the usage of these methods.

### Precise `AudioNode` `disconnect()` methods

In the past, you could not disconnect nodes selectively: if you ran `disconnect()` on a given node, it would disconnect it from all other nodes.

Thankfully, the `disconnect()` method can now be overloaded to increase the type of disconnections you can perform:

`disconnect()`– disconnects a node from every node (this is the existing function)`disconnect(outputNumber)`– disconnects all connections from the node’s`outputNumber`channel`disconnect(anotherNode)`– disconnects all connections to`anotherNode``disconnect(anotherNode, outputNumber)`– disconnects all connections from`outputNumber`channel from node`anotherNode``disconnect(anotherNode, outputNumber, inputNumber)`– disconnects connections to`anotherNode`from`outputNumber`into`inputNumber`channels`disconnect(audioParam)`– disconnects connections from this node to`audioParam``disconnect(audioParam, outputNumber)`– disconnects connections from this node’s`outputNumber`channel to`audioParam`

I strongly recommend you read [the specification for AudioNode](https://webaudio.github.io/web-audio-api/#methods-3) to understand all the details on the effects of these disconnections. You can also read

[the original discussion](https://github.com/WebAudio/web-audio-api/issues/6)to find out about the motivation for this change.

### New length attribute in `OfflineAudioContext`

This new attribute reflects the value that was passed to the constructor when the `OfflineAudioContext` was initialised, so developers don’t have to keep track of it on a separate variable:

```
var oac = new OfflineAudioContext(1, 1000, 44100);
console.log(oac.length);
>> 1000
```


Here’s [an example](https://mozdevs.github.io/WebAudio-examples/OfflineAudioContext/) that demonstrates using that attribute and also rendering a sound wave with a gain envelope.

### New `detune` attribute in `AudioBufferSourceNode`

This is similar to the `detune` attribute in `OscillatorNode`s, but can now be used for fine-tuning samples with more accuracy than just using the existing `playbackRate` property.

### New `AudioParam`-typed position and orientation attributes in `PannerNode`

These new attributes are `AudioParam`s, which means you can use automation to modify them instead of continuously calling the `setPosition()` or `setOrientation()` methods in a loop.

The `StereoPannerNode` `pan` attribute was already an `AudioParam`, so all the nodes that let you pan sounds in space also allow you to automate their spatial properties. Great stuff for modular synthesis!

That said, we still lack the ability to automate the position and orientation properties in `AudioListener`, which means that if you want to update these periodically you have to use `setPosition()` and `setOrientation()` methods on the `AudioListener` for now. (Bug #[1283029](https://bugzilla.mozilla.org/show_bug.cgi?id=1283029) tracks this).

### Passing values to set initial parameters for `PeriodicWave` instances

You can now pass an options object when creating instances of `PeriodicWave`:

```
var wave = audioContext.createPeriodicWave(real, imag, { disableNormalization: false });
```


Compare with the previous syntax:

```
var wave = audioContext.createPeriodicWave(real, imag);
wave.disableNormalization = false;
```


In the future, all node creation methods will allow developers to pass objects to set their initial parameters, and will also be *constructible*, so we’ll be able to do things such as `new GainNode(anAudioContext, {gain: 0.5});`. This will make Web Audio code way more succinct than it actually can be when it comes to initialising nodes. Less code to maintain is always good news!

## New node: `IIRFilterNode`

If `BiquadFilterNode` is not enough for your needs, `IIRFilterNode` will allow you to build your own custom filter.

You can create instances calling the `createIIRFilter()` function on an `AudioContext`, and passing in two arrays of coefficients representing the `feedforward` and `feedback` values that define the filter:

```
var customFilter = audioContext.createIIRFilter([ 0.1, 0.2, ...], [0.4, 0.3, ...]);
```


This type of filter node is not automatable, which means that once created, you cannot change its parameters. If you want to use automation, you’ll have to keep using the existing `BiquadFilter` nodes, and alter their `Q`, `detune`, `frequency` and `gain` attributes which are all `AudioParams`.

The spec has more data on [these differences](https://webaudio.github.io/web-audio-api/#the-iirfilternode-interface), and you can use the [Digital Filter Design](https://rtoy.github.io/webaudio-hacks/more/filter-design/filter-design.html) resource to design and visualise filters and get ready-to-use Web Audio code with prepopulated `feedforward` and `feedback` arrays.

## Chaining methods

Some more “syntactic sugar” to improve developers’ ergonomics:

The `connect()` methods return the node they connect to, so you can chain multiple nodes faster. Compare:

Before:

```
node0.connect(node1);
node1.connect(node2);
node2.connect(node3);
```


After:

`node0.connect(node1).connect(node2).connect(node3);`


And the `AudioParam` automation methods can be chained as well, as each method returns the object it was called on. For example, you could use it to define envelopes faster:

Before:

```
gain.setValueAtTime(0, ac.currentTime);
gain.linearRampToValueAtTime(1, ac.currentTime + attackTime);
```


After:

```
gain.setValueAtTime(0, ac.currentTime)
.linearRampToValueAtTime(1, ac.currentTime + attackTime);
```


## Coming up in the future

The Web Audio Working Group is almost finished writing the specification for `AudioWorklet`s, which is the new name for `AudioWorker`s. These will replace the `ScriptProcessorNode`, which also lets you write your own nodes, but runs on the UI thread, so it’s not the best idea performance-wise.

[The pull request defining AudioWorklets](https://github.com/WebAudio/web-audio-api/pull/869) and associated objects on the specification must be merged first, and once that’s done vendors can start implementing support for

`AudioWorklet`s on their browsers.

# Firefox changes: performance and debugging improvements

Three hard-working engineers (Karl Tomlinson, Daniel Minor and Paul Adenot) spent at least six months improving the performance of Web Audio in Firefox. What this means, in practical terms, is that audio code now takes less time to run and it’s faster than or as fast as Chrome is. The only exception is when working with `AudioParam`s, where Firefox performance is not as good… *yet*.

Similarly, `ScriptProcessorNode`s are now less prone to introduce delay if the main thread is *very* busy. This is great for applications such as console emulators: low latency means a more faithful emulation, which in turns makes for lots of fun playing games!

Going even deeper, assembly level optimisations for computing DSP kernels have been introduced. These take advantage of [SIMD](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/SIMD) instructions on ARM and x86 to compute multiple values in parallel, for simple features such as panning, adjusting gain, etc. This means faster and more efficient code, which uses less battery—especially important on mobile devices.

Additionally, cross-origin errors involving `MediaElement` nodes will now be reported to the developer tools console, instead of silently failing. This will help developers identify the exact issue, instead of wondering why are they getting only silence.

There were many more fixed bugs—probably too many to list here! But have a look at [the bug list](https://bugzilla.mozilla.org/buglist.cgi?resolution=FIXED&query_format=advanced&component=Web%20Audio&product=Core) if you’re really curious.

## About
[
Soledad Penadés ](https://soledadpenades.com)

Sole works at the Developer Tools team at Mozilla, helping people make amazing things on the Web, preferably real time. Find her on #devtools at irc.mozilla.org